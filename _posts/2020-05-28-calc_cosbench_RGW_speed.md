---
layout:     post
title:      "Cosbench wirte speed scenario test script"
subtitle:   "Cosbench wirte speed scenario test script"
date:       2020-05-28
author:     "Gavin"
catalog:    true
tags:
    - shell
    - python
---


# Overview

A recent test scenario was encountered:
The customer wanted to know how fast the product writes S3 Object per second (the customer required 3000/s), so it started to construct a test scenario, and wrote 120 million objects in total by counting the writing speed every 10 million objects interval.

Unify the write speed on the RGW side, and the write speed on the cosbench side, and the write speed to ES esrally.

# Script directory structure

```
root@scaler80:/mnt/code/cosbench_elastic_search# ls -lR
.:
total 16
-rw-r--r-- 1 root root 2248 May 28 01:42 calc_cosbench_speed.py
-rw-r--r-- 1 root root 2092 May 28 01:42 calc_rgw_write_speed.py
drwxr-xr-x 2 root root 4096 May 28 01:42 run_cosbench
-rw-r--r-- 1 root root 2274 May 28 01:42 write_json_data_for_esrally.py

./run_cosbench:
total 8
-rw-r--r-- 1 root root 1063 May 28 01:42 cosbench.sh
-rw-r--r-- 1 root root 2866 May 28 01:42 roundN_10K_10Mfiles_Write.xml.in
root@scaler80:/mnt/code/cosbench_elastic_search# 
```

# Script Introduction

calc_cosbench_speed.py         -->  From cosbench archive log to get Write/Read/Mix speed and AVG Time
calc_rgw_write_speed.py        -->  From output of 'ceph df' to get RGW write speed
write_json_data_for_esrally.py -->  Struct data for esally to write into ES
run_cosbench                   --> Submit cosbench task


# Script contents

calc_cosbench_speed.py

{% raw %}```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from __future__ import unicode_literals

import os
import sys
import time


ARCHIVE_PATH = "/root/0.4.2.c4/archive"
HISTORY = "run-history.csv"

HISTORY_FILE = ARCHIVE_PATH + os.sep + HISTORY

if not os.path.exists(HISTORY_FILE):
    print("\033[31m \n  [ERROR]  Not find path for : ({}) \033[0m \n".format(HISTORY_FILE))
    sys.exit(1)

his_content = os.popen("cat {}".format(HISTORY_FILE)).read()
for each_line in his_content.strip().split("\n"):
    if each_line.startswith("Id"):
        continue

    try:
        line_list = each_line.split(',')
        task_id = line_list[0]
        task_name = line_list[1]
        task_state = line_list[6].strip()

        if task_state == 'finished':
            work_dir = "{}/{}-{}".format(ARCHIVE_PATH, task_id, task_name)
            start_time = line_list[3]
            end_time = line_list[4]

            start_time_array = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time_array = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_times_tamp = time.mktime(start_time_array)
            end_times_tamp = time.mktime(end_time_array)
            time_diff = end_times_tamp - start_times_tamp

            total_objs_cmd = "cat {}/driver*.csv | grep write | grep -v init " \
                             "| awk -F',' '{{print $3}}'".format(work_dir)
            count_str = os.popen(total_objs_cmd).read().strip()
            couts_str_list = count_str.split("\n")
            couts_str_int = map(int, couts_str_list)
            total_objs = sum(couts_str_int)

            write_speed = total_objs / time_diff

            print("\033[32m  Task : ({}-{}), total: ({}), elapsed : ({}s), "
                  "speed : ({}) \033[0m\n".format(task_id, task_name, total_objs, time_diff, write_speed))
        else:
            print("\033[33m  [WARN]  Task : ({}-{}) status is not finished, but : ({}), "
                  "please pay more attention \033[0m\n".format(task_id, task_name, task_state))

    except Exception as ex:
        print("\n\033[31m \n  [ERROR]  Parase file of '{}' "
              "exception : ({}) \033[0m\n".format(HISTORY_FILE, str(ex)))
        sys.exit(1)


if __name__ == "__main__":
    pass

``` {% endraw %}

calc_rgw_write_speed.py

{% raw %}```
#!/usr/bin/env python

import os
import sys
import time
import datetime

from ezs3.command import do_cmd


def get_object_counts(pool_name):
    cur_objects_info = do_cmd("ceph df | grep {}".format(pool_name)).strip()
    if cur_objects_info:
        cur_objects = int(cur_objects_info.split()[-1])

        return cur_objects
    else:
        print("[ERROR]  Not get objects from pool : ({})".format(pool_name))
        return


def calc_rgw_speed(pool_name=None, sleep_time=None, loop_times=None):
    pool_name = 'default.rgw.buckets.data' if pool_name is None else pool_name
    sleep_time = 5 if sleep_time is None else sleep_time
    loop_times = 10 if loop_times is None else loop_times

    rgw_speed_list = []
    log_file = "rgw_write_speed.log"

    if os.path.exists(log_file):
        cur_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        bak_log = log_file + '_{}'.format(cur_time)
        do_cmd("mv {} {}".format(log_file, bak_log))

    title = "--------------- Before Counts ---------- After Counts ---------- Sleep Time ----------- RGW Speed --------"
    print(title)
    do_cmd("echo '{}' >> {}".format(title, log_file))

    for i in xrange(loop_times):
        before_count = get_object_counts(pool_name)
        time.sleep(sleep_time)
        after_count = get_object_counts(pool_name)

        if after_count - before_count == 0:
            print("[ERROR]  Maybe has been writed over, exit!")
            sys.exit(1)

        write_speed = (after_count - before_count) / sleep_time
        out_put = "\t\t{}  \t\t {} \t\t  {} \t\t\t {}".format(before_count, after_count, sleep_time, write_speed)
        print(out_put)
        do_cmd("echo '{}' >> {}".format(out_put, log_file))
        rgw_speed_list.append(write_speed)

    avg_speed = sum(rgw_speed_list) * 1.0 / len(rgw_speed_list)
    avg_speed_output = "RGW AVG speed : {}".format(avg_speed)

    print(avg_speed_output)
    do_cmd("echo '{}' >> {}".format(avg_speed_output, log_file))


if __name__ == '__main__':
    # calc_rgw_speed()
    calc_rgw_speed(sleep_time=600, loop_times=300)

``` {% endraw %}



write_json_data_for_esrally.py

{% raw %}```
#!/usr/bin/env python

import os
import sys
from random import choice
from string import digits
from string import ascii_lowercase


def rand_low_ascii(length=10):
    return ''.join([choice(ascii_lowercase) for i in xrange(length)])


def rand_alpha(length=9):
    return ''.join([choice(digits) for i in xrange(length)])



"""
{
    "bucket": "bucket01",
    "owner": {
        "id": "user01",
        "display_name": "user01"
    },
    "instance": "",
    "meta": {
        "expires": "",
        "storage_class": "",
        "content_encoding": "",
        "mtime": "2020-05-27T03:14:57.855Z",
        "content_language": "",
        "custom-date": {
            "name": "",
            "value": ""
        },
        "content_type": "application/octet-stream",
        "custom-int": {
            "name": "",
            "value": ""
        },
        "custom-string": {
            "name": "7385228445730524",
            "value": "8590745273515960"
        },
        "size": "10",
        "content_disposition": "",
        "etag": "e7b4c2f4a8153de9c7a070e5d6550ab1",
        "tail_tag": "a3a5cefd-376d-421b-9080-08b98962e7c1.4520.681216"
    },
    "permissions": "",
    "name": "25_1590549297.82",
    "versioned_epoch": "0"
}
"""

def json_data():
    src = {"bucket":"bucket01","owner":{"id":"user01","display_name":"user01"},"instance":"null","meta":{"mtime":"2020-05-2{}T1{}:2{}:3{}.{}Z".format(rand_alpha(1), rand_alpha(1), rand_alpha(1), rand_alpha(1), rand_alpha(3)),"content_type":"application/octet-stream","custom-string":{"name":"{}".format(rand_alpha(16)),"value":"{}".format(rand_alpha(2048))},"size":"{}".format(rand_alpha(3)),"etag":"e7b{}f4a{}de9c7a070e5d{}ab1".format(rand_alpha(3), rand_alpha(4), rand_alpha(4)),"tail_tag":"a3a5cefd-376d-421b-{}-08b{}e7c1.4520.{}".format(rand_alpha(4), rand_alpha(5), rand_alpha(6))},"name":"{}_{}.{}".format(rand_alpha(2), rand_alpha(10), rand_alpha(2)),"versioned_epoch":"0"}

    return src


def write_data(src):
    with open("./documents-2.json", 'a') as f:
            # replace ' to "
            new_str = str(src).replace("'", '"')
            f.write(new_str)
            f.write('\n')



if __name__ == '__main__':
    for i in xrange(300000000):
        src = json_data()
        write_data(src)

``` {% endraw %}


cosbench.sh

{% raw %}```
#!/bin/bash

INFILE=roundN_10K_10Mfiles_Write.xml.in
CLI=/root/0.4.2.c4/cli.sh
EP1=10.16.172.161
EP2=10.16.172.162
EP3=10.16.172.163
ACCESS_KEY=73WH14UOZ7QU0H8KYR2V
SECRET_KEY=4WR0T7wPNlRTJsOvEEmWo3w7bwAyJ5vzHQd9dTTA

ssh root@${EP1} ceph status
ssh root@${EP1} ceph df
for round in {1..40}
do
    while (( $(${CLI} info |& grep PROCESSING | wc -l) >= 1 )); do
        sleep 60
    done

    sed "s/@@@ROUND@@@/${round}/g" ${INFILE} | \
    sed "s/@@@ENDPOINT_1@@@/${EP1}/g" | \
    sed "s/@@@ENDPOINT_2@@@/${EP2}/g" | \
    sed "s/@@@ENDPOINT_3@@@/${EP3}/g" | \
    sed "s/@@@ACCESS_KEY@@@/${ACCESS_KEY}/g" | \
    sed "s/@@@SECRET_KEY@@@/${SECRET_KEY}/g" > workload.xml
    ${CLI} submit workload.xml

    date
    # Get memory for each node
    ssh root@${EP1} python /root/run_nmon.py
    ssh root@${EP2} python /root/run_nmon.py
    ssh root@${EP3} python /root/run_nmon.py

    date
    sleep 60

    while (( $(${CLI} info |& grep PROCESSING | wc -l) >= 1 )); do
        sleep 60
    done

    ssh root@${EP1} ceph status
    ssh root@${EP1} ceph df

done
```{% endraw %}


roundN_10K_10Mfiles_Write.xml.in

```
<?xml version="1.0" encoding="UTF-8"?>
<workload name="Datasearch_round@@@ROUND@@@_10K_files_write_once" description="Datasearch_round@@@ROUND@@@_10K_files_write_once">
<storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_1@@@/" />

  <workflow>
		<!-- ******************************* -->
  	<!-- 1mch 20wrks 60threads write job -->
		<!-- ******************************* -->

    <workstage name="10K-10M-40wrks-write-init">
        <work name="10mch-40wrks-160threads-write-init" type="init" workers="1" interval="10" division="container" runtime="0" rampup="0" rampdown="0" driver="driver1"  config="cprefix=dana;containers=r(1,1)" />
    </workstage>

    <workstage name="10K-10M-40wrks-write-WRITEJOB">
        <work name="write1" type="write" workers="40" interval="10" division="object" totalOps="3500000" rampup="0" rampdown="0" driver="driver1">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_1@@@/" />
            <operation type="write" ratio="100" division="object" config="cprefix=dana;oprefix=round@@@ROUND@@@_10KB_;containers=s(1,1);objects=r(1,3500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2" type="write" workers="40" interval="10" division="object" totalOps="3500000" rampup="0" rampdown="0" driver="driver1">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_2@@@/" />
            <operation type="write" ratio="100" division="object" config="cprefix=dana;oprefix=round@@@ROUND@@@_10KB_;containers=s(1,1);objects=r(3500001,7000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write3" type="write" workers="40" interval="10" division="object" totalOps="3000000" rampup="0" rampdown="0" driver="driver1">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_3@@@/" />
            <operation type="write" ratio="100" division="object" config="cprefix=dana;oprefix=round@@@ROUND@@@_10KB_;containers=s(1,1);objects=r(7000001,10000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
    </workstage>

<!--
    <workstage name="1mch-20wrks-60threads-write-cleanup">
          <work type="cleanup" workers="1" driver="driver1" config="cprefix=tmo;oprefix=round2_10KB_;containers=r(1,1);objects=r(1,10)" />
    </workstage>
    <workstage name="1mch-20wrks-60threads-write-dispose">
          <work type="dispose" workers="1" driver="driver1" config="cprefix=tmo;containers=r(1,1)" />
    </workstage>
-->

	</workflow>
</workload>


```
