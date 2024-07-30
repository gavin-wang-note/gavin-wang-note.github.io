---
layout:     post
title:      "Loop assign GWs to different VS"
subtitle:   "Loop assign GWs to different VS"
date:       2023-03-31
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---

# Overview

RD has a scenario like the fallowing:

* 3-node cluster, each node with GW services enabled, all under Default VS by default
* Create VS-1 and assign GW1 to VS-1
* Create VS-2 and assign GW2 and GW3 to VS-2
* Create VS-3, assign GW1 to VS-3, and delete VS-1
* Create VS-4, assign GW2 and GW3 to VS-4, and delete VS-2
* So on and so forth, after each round of allocation, you need to check the health status of ctdb under the current VS

Considering that manual testing can be time consuming, write a test script and run it overnight or more rounds (e.g: loop 1000 times) and see how the test works the next day.


# Script of assign_gw_v8.3.sh

```shell
#!/bin/bash

target="1.2.3.164"
user="admin"
pass="1"
gateways1="1.2.3.164"
gateways2="1.2.3.165"
single_gateways="1.2.3.166"
no_gws=2
previous_vs="Default"
log_file="/var/log/assign_vs.log"


function login(){
    login_res=`curl --insecure --cookie-jar cookie.jar -s -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${target}:8080/auth" --data "{\"password\": \"${pass}\", \"user_id\": \"${user}\"}"`
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
}


function loop_assign_gws(){
    for i in `seq 1 1000`
    do
      echo "============================  ($i) times to run  ============================\n" | tee -a ${log_file}
    
      date_time=`date +"%Y-%m-%d %H:%M:%S"`
      echo -e "[${date_time}]  Start to create VS and assign GW to VS" | tee -a ${log_file} 
      vs="vs-$i"
      res=`curl --insecure --cookie cookie.jar "https://${target}:8080/cgi-bin/ezs3/json/gwgroup_create?name=${vs}&vs_type=standard"`
      if [[ ${res} =~ 'unauthorized' ]]; then
          login
          curl --insecure --cookie cookie.jar "https://${target}:8080/cgi-bin/ezs3/json/gwgroup_create?name=${vs}&vs_type=standard"
      fi
      curl --insecure --cookie cookie.jar -X PUT --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${target}:8080/vs/${vs}/pool" --data '{"pools":["Default"]}'
      curl  --insecure --cookie cookie.jar -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${target}:8080/vs/${vs}/host" --data "{\"ip\":\"${gateways1}\"}"
      curl  --insecure --cookie cookie.jar -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${target}:8080/vs/${vs}/host" --data "{\"ip\":\"${gateways2}\"}"
    
      if [ $i -ge 2 ]; then
          old_vs="vs-$((i-1))"
          curl  --insecure --cookie cookie.jar -X POST --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${target}:8080/vs/${old_vs}/host" --data-raw "{\"ip\":\"${single_gateways}\"}"
      fi
    
      ctdb_cnt=`ssh root@${target} 'ctdb status|grep OK|wc -l'`
      while [ $ctdb_cnt -ne ${no_gws} ]
      do
        date_time=`date +"%Y-%m-%d %H:%M:%S"`
        echo -e "[${date_time}]  Not done yet, wait for 5 seconds." | tee -a ${log_file}
        sleep 5
        ctdb_cnt=`ssh root@${target} 'ctdb status|grep OK|wc -l'`
      done

      date_time=`date +"%Y-%m-%d %H:%M:%S"`
      echo -e "[${date_time}]  All gateways successfully assigned to virtual storage ${vs}." | tee -a ${log_file}

      if [ $previous_vs != "Default" ]; then
         date_time=`date +"%Y-%m-%d %H:%M:%S"`
         echo -e "[${date_time}]  Delete VS ${vs}"  | tee -a ${log_file}
         curl --insecure --cookie cookie.jar -X DELETE --header "Accept: application/json, text/javascript, */*; q=0.01" --header "Content-Type: application/json" "https://${target}:8080/vs/$previous_vs"
      fi
      previous_vs=$vs
    done
}


login
loop_assign_gws
```

