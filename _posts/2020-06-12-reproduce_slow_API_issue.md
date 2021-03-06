---
layout:     post
title:      "API响应慢问题复现"
subtitle:   "Reproduce Slow API response issue"
date:       2020-06-12
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - shell
---


# 概述

现在测试有个需求，需要验证某个API响应时间，之所以关注这个API时间，是因为有时响应太久，超过30s，估计这个时间客户也无法容忍。


# 具体要求

具体的API是RAID界面，去list出RAID卡上所有的VD，PD，SSD，RAID card等诸多信息，如果响应时间超过预定时间，比如30s，则认为API出状况了。

上述过程，使用测试脚本完成，一旦响应时间超过预定时间，程序退出。


# 实践


## shell

```
root@node76:~# cat raid_api_elapsed.sh
#!/bin/bash

PUBLIC_IP=7.73.7.76
STORAGE_IP=1.1.1.76
TIMEOUT=30
LOG_FILE=./raid_api_elapsed.log

# Login
login_res=`curl --insecure --cookie-jar cookie.jar -s -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${PUBLIC_IP}:8080/auth" --data '{"password": "1", "user_id": "admin"}'`
login_return_code=`echo ${login_res} | sed 's@{"name": "login", "return_code": @@' | sed 's/}//'`

if [ x"${login_return_code}" == x"300" ]; then
    echo ""
    echo "[ERROR]  Login Failed, exit!!!"
    echo ""
    exit 1
elif [[ ${login_return_code} =~ 'session_id' ]]; then
    echo ""
    echo "Login success"
    echo ""
fi

echo "======================================================= RAID API Elapsed Time Test =======================================================" | tee ${LOG_FILE}

while :
do
    # RAID API
    # start_time=`date +%F-%H-%M.%N`
    start_time=`date "+%Y-%m-%d %H:%M:%S"`
    start_time_stamp=`date -d "${start_time}" +%s`
    start_mills=$((${start_time_stamp}*1000+`date "+%N" | sed 's/^[0]*//'`/1000000))

    result_code=`curl --insecure --cookie cookie.jar --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" -s -I -m ${TIMEOUT} -w %{http_code} "https://${PUBLIC_IP}:8080/system/host/${STORAGE_IP}/disk/raid"`
    end_time=`date "+%Y-%m-%d %H:%M:%S"`
    end_time_stamp=`date -d "${end_time}" +%s`
    end_mills=$((${end_time_stamp}*1000+`date "+%N" | sed 's/^[0]*//'`/1000000))

    if [[ ${result_code} =~ '200' ]]; then
        time_diff=`expr ${end_mills} - ${start_mills}`
        echo "${end_time}  --> OK, elapsed time is : (${time_diff} milliseconds), now sleep 2s" | tee ${LOG_FILE}
        sleep 2
    elif [[ ${result_code} =~ '401'  ]]; then
        echo "[WARN]  Session timeout, login again"
        curl --insecure --cookie-jar cookie.jar -s -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${PUBLIC_IP}:8080/auth" --data '{"password": "1", "user_id": "admin"}'
    else
        echo "${end_time}  [ERROR]  Cost more than ${TIMEOUT}s, exit!" | tee ${LOG_FILE}
        echo ""
        exit 1
    fi
done
```


核心是-s -I -m 10 -w %{http_code}，解释一下携带的参数信息：

```
-I 仅测试HTTP头

-m 10 最多查询10s

-o /dev/null 屏蔽原有输出信息

-s silent 模式，不输出任何东西

-w %{http_code} 控制额外输出
```

这里还有另外一个方法:

```
root@node76:~# curl --insecure --cookie cookie --header 'Accept: application/json, text/javascript, */*; q=0.01' --header 'Content-Type: application/json' -o /dev/null -s -w "time_connect: %{time_connect}\ntime_starttransfer: %{time_starttransfer}\ntime_total: %{time_total}\n" https://7.73.7.76:8080/system/host/1.1.1.76/disk/raid
time_connect: 0.000
time_starttransfer: 8.435
time_total: 8.436
root@node76:~# 
```

可以根据time_total时间来判断，此时间超过一定值，就退出。

```
root@node76:~# cat raid_api_elapsed2.sh 
#!/bin/bash

PUBLIC_IP=7.73.7.76
STORAGE_IP=1.1.1.76
TIMEOUT=30
LOG_FILE=./raid_api_elapsed.log

# Login
login_res=`curl --insecure --cookie-jar cookie.jar -s -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${PUBLIC_IP}:8080/auth" --data '{"password": "1", "user_id": "admin"}'`
login_return_code=`echo ${login_res} | sed 's@{"name": "login", "return_code": @@' | sed 's/}//'`

if [ x"${login_return_code}" == x"300" ]; then
    echo ""
    echo "[ERROR]  Login Failed, exit!!!"
    echo ""
    exit 1
elif [[ ${login_return_code} =~ 'session_id' ]]; then
    echo ""
    echo "Login success"
    echo ""
fi

echo "======================================================= RAID API Elapsed Time Test =======================================================" | tee ${LOG_FILE}

while :
do
    # RAID API
    start_time=`date "+%Y-%m-%d %H:%M:%S"`

    time_total=`curl --insecure --cookie cookie.jar --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" -o /dev/null -s -w "%{time_total}\n" "https://${PUBLIC_IP}:8080/system/host/${STORAGE_IP}/disk/raid"`
    end_time=`date "+%Y-%m-%d %H:%M:%S"`

    int_time_total=`echo $time_total | cut -d '.' -f1`
    if [[ ${int_time_total} -lt ${TIMEOUT} ]]; then
        echo "${end_time}  --> OK, elapsed time is : (${time_total} milliseconds), now sleep 2s" | tee ${LOG_FILE}
        sleep 2
    elif [[ ${result_code} =~ '401'  ]]; then
        echo "[WARN]  Session timeout, login again"
        curl --insecure --cookie-jar cookie.jar -s -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${PUBLIC_IP}:8080/auth" --data '{"password": "1", "user_id": "admin"}'
    else
        echo "${end_time}  [ERROR]  Cost time : (${time_total}) is more than ${TIMEOUT}s, exit!" | tee ${LOG_FILE}
        echo ""
        exit 1
    fi
done
```


## python

```
root@node76:~# cat raid_api_elapsed.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import json
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HttpSession(requests.Session):
    """  http request session  """

    def __init__(self):
        super(HttpSession, self).__init__()

        # Not verify SSL certificate
        self.verify = False

        # timeout time
        self.timeout = (60, 600)

        # session information
        self.session = ""

    def login_session(self, user_id, password, public_ip):
        """ Login Session """
        login_url = "https://{}:8080/auth".format(public_ip)

        login_data = {"user_id": user_id,
                     "password": password}

        self.session = requests.session()
        self.session.keep_alive = False
        self.session.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
        # print("[Login]    login_url: %s, login_data: %s", login_url, json.dumps(login_data))
        response = self.session.request("POST", login_url, json=login_data, verify=False)

        if response.status_code != 200:
            print("[ERROR]  Login web error, http status code is {}".format(response.status_code))
            sys.exit(1)

        return self.session

    def http_request(self, session, http_method, url, user_id, password, public_ip, params=None, data=None):
        """  Send HTTP request, support GET/POST  """
        params = {} if params is None else params
        data = {} if data is None else data

        # set SSL Verify to False
        session.verify = False

        # Set session keep alive to False
        session.keep_alive = False

        try:
            start_time = time.time()
            start_trans = time.localtime(start_time)
            format_start_time = time.strftime('%Y-%m-%d %H:%M:%S.%3d', start_trans)

            if "cgi-bin" in url:
                # Legacy CGI
                response = session.request(http_method, url, params=params, data=data)
                if response.status_code == 401:
                    session = self.login_session(user_id, password, public_ip)
                    response = session.request(http_method, url, params=params, data=data)
            else:
                # Restful CGI
                response = session.request(http_method, url, params=params, json=data)

                if response.status_code == 401:
                    session = self.login_session(user_id, password, public_ip)
                    response = session.request(http_method, url, params=params, json=data)

            elapsed_sec = response.elapsed.seconds
            if elapsed_sec >= 30:
                print("[{}]  [ERROR]  URL response elapsed time : ({}), return_text : ({})".format(format_start_time, elapsed_sec, response.text))
                sys.exit(1)
            else:
                print("[{}]    URL response elapsed time : ({})".format(format_start_time, elapsed_sec))
        except Exception as ex:
            print("[WARN]  Session request exception : (%s)", str(ex))

        return response


def call_raid_api(user_id, password, http_method, url, public_ip, storage_ip):
    """  Call API """
    session = HttpSession()
    login_s = session.login_session(user_id, password, public_ip)

    for i in xrange(100):
        session.http_request(login_s, http_method, url, user_id, password, public_ip) 


if __name__ == '__main__':
    public_ip = '7.73.7.76'
    storage_ip = '1.1.1.76'
    user_id = 'admin'
    password = '1'
    http_method = 'GET'
    url = "https://{}:8080/system/host/{}/disk/raid".format(public_ip, storage_ip)

    call_raid_api(user_id, password, http_method, url, public_ip, storage_ip)
```


# 测试效果如下：

## shell

```
root@node76:~# tailf raid_api_elapsed.log 
2020-06-12 12:41:05  --> OK, elapsed time is : (8433 milliseconds), now sleep 2s
2020-06-12 12:41:27  --> OK, elapsed time is : (8514 milliseconds), now sleep 2s
2020-06-12 12:41:37  --> OK, elapsed time is : (8698 milliseconds), now sleep 2s
2020-06-12 12:41:48  --> OK, elapsed time is : (8518 milliseconds), now sleep 2s
2020-06-12 12:42:09  --> OK, elapsed time is : (8436 milliseconds), now sleep 2s
2020-06-12 12:42:20  --> OK, elapsed time is : (8660 milliseconds), now sleep 2s
2020-06-12 12:42:51  --> OK, elapsed time is : (8559 milliseconds), now sleep 2s
2020-06-12 12:43:02  --> OK, elapsed time is : (8501 milliseconds), now sleep 2s
2020-06-12 12:43:12  --> OK, elapsed time is : (8597 milliseconds), now sleep 2s
2020-06-12 12:43:23  --> OK, elapsed time is : (8470 milliseconds), now sleep 2s
.................................. 中间省略 ....................................
2020-06-12 12:53:50  --> OK, elapsed time is : (8632 milliseconds), now sleep 2s
2020-06-12 12:54:00  --> OK, elapsed time is : (8605 milliseconds), now sleep 2s
2020-06-12 12:54:22  --> OK, elapsed time is : (8526 milliseconds), now sleep 2s
2020-06-12 12:55:04  --> OK, elapsed time is : (8507 milliseconds), now sleep 2s
2020-06-12 12:55:14  --> OK, elapsed time is : (8483 milliseconds), now sleep 2s
2020-06-12 12:56:07  --> OK, elapsed time is : (8357 milliseconds), now sleep 2s
2020-06-12 12:56:39  --> OK, elapsed time is : (8671 milliseconds), now sleep 2s
2020-06-12 12:56:50  --> OK, elapsed time is : (8573 milliseconds), now sleep 2s
2020-06-12 12:57:11  --> OK, elapsed time is : (8435 milliseconds), now sleep 2s
2020-06-12 12:57:26  [ERROR]  Cost more than 30s, exit!
```



## python

```
root@node76:~# python raid_api_elapsed.py 
[2020-06-12 14:33:13.012]    URL response elapsed time : (8)
[2020-06-12 14:33:22.012]    URL response elapsed time : (8)
[2020-06-12 14:33:30.012]    URL response elapsed time : (8)
[2020-06-12 14:33:39.012]    URL response elapsed time : (8)
[2020-06-12 14:33:48.012]    URL response elapsed time : (8)
[2020-06-12 14:33:56.012]    URL response elapsed time : (8)
[2020-06-12 14:34:05.012]    URL response elapsed time : (8)
[2020-06-12 14:34:13.012]    URL response elapsed time : (8)
.......................... 中间省略 .........................
[2020-06-12 14:39:30.012]    URL response elapsed time : (8)
[2020-06-12 14:39:38.012]    URL response elapsed time : (13)
[2020-06-12 14:39:52.012]    URL response elapsed time : (8)
.......................... 中间省略 .........................
[2020-06-12 14:44:19.012]    URL response elapsed time : (9)
[2020-06-12 14:44:29.012]    URL response elapsed time : (9)
[2020-06-12 14:44:38.012]    URL response elapsed time : (9)
[2020-06-12 14:44:47.012]    URL response elapsed time : (8)
[2020-06-12 14:44:55.012]    URL response elapsed time : (9)
[2020-06-12 14:45:05.012]    URL response elapsed time : (9)
[2020-06-12 14:45:14.012]    URL response elapsed time : (8)
[2020-06-12 14:45:23.012]    URL response elapsed time : (8)
[2020-06-12 14:45:31.012]    URL response elapsed time : (8)
[2020-06-12 14:45:40.012]  [ERROR]  URL response elapsed time : (39), return_text : ({"assigned": [{"vd": "0", "current_cache_policy": "WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU", "drive_num": "7", "pds": [{"slot": "1", "copyback_progress": null, "other_error": 0, "healthy": "none", "rebuild_progress": null, "adapter": null, "size": "7.277 TB", "media_error": 0, "pd_type": "SATA", "lifetime_remaining": -1, "firmware_state": "Online, Spun Up", "pd": "0", "media_type": "HDD", "device_id": "38", "smart_info": "smartctl 7.0 2018-12-30 r4883 [x86_64-linux-4.14.148-server] (local build)\nCopyright (C) ....后面省略，这里展示具体的response详细信息...
```



# 其他

看了同事写的一个python版本，非常简洁，不过没有考虑session过期问题，脚本内容参考如下:

```
root@246:/home# cat c.py 
# -*- coding: utf-8 -*-

import time
import urllib3
import requests

urllib3.disable_warnings()

ip = "1.1.7.246"
storage_ip = "1.1.1.246"
headers = {"accept": "application/bigtera.vs.v1+json, application/json"}

session = requests.Session()
# login
url = "https://{}:8080/auth".format(ip)
response = session.post(
    url, json={"user_id": "admin", "password": "1"}, headers=headers, verify=False
)

while True:
    start = time.time()
    # get raid info
    url = "https://{}:8080/system/host/{}/disk/raid".format(ip, storage_ip)
    response = session.get(url, headers=headers, verify=False)
    end = time.time()
    try:
        response.raise_for_status()
    except Exception as e:
        print(e)
        break

    if end - start > 10:
        print("last request cost {} seconds", end - start)
        break
```

