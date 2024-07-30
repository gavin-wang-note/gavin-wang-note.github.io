---
layout:     post
title:      "Monitor mds failed"
subtitle:   "Monitor mds failed"
date:       2021-11-04
author:     "Gavin Wang"
catalog:    true
categories:
    - [ceph]
    - [shell]
tags:
    - mds
    - ceph
    - shell
---


# Scripts

`monitor_mds_failed.sh`

```shell
#!/bin/bash

if read -t 5 -p "WARN: Have you confirmed that the maximum number of active-mds has been set for VS? [y|n] :" yn
then
    if [[ $yn == [Yy] ]];then
        echo -e 'Running...'
    elif [[ $yn == [Nn] ]];then
        echo -e "\e[0;31;1mExit ...\e[0m"
        exit
    else [[ $yn != [YyNn] ]]
        echo -e "\e[0;33;1mPlease check what you input! Only can input y or n\e[0m"
        exit
    fi
else
    echo " "
    echo -e "\e[0;33;1mTimeOut ...\e[0m"
    exit
fi


log_file="mds_failed.log"

rm -rf ${log_file}

echo -e "  To stop all of btmds-agent for all enabled GW nodes"
onnode -p all '/usr/bin/python /usr/local/bin/btmds-agent stop'

for i in {1..1000}; 
do
    echo "--------------------------- ${i} ----------------------" >> ${log_file}
    date_time1=`date '+%Y-%m-%d %H:%M:%S'`
    echo -e "  --  [${date_time1}]  restart ceph-mds.target on all nodes" >> ${log_file}
    onnode -p all systemctl restart ceph-mds.target;sleep 5

    date_time2=`date '+%Y-%m-%d %H:%M:%S'`
    echo -e "  --  [${date_time2}]  Check mds failed status" >> ${log_file}
    for j in {0..100000}
    do
        res=`ceph -s | grep 'mds:'`
        if [[ ${res} =~ 'failed' ]];then
            date_time3=`date '+%Y-%m-%d %H:%M:%S'`
            msg="[${date_time3}]  [ERROR]  Find failed ceph-mds, exit!!"
            echo -e ${msg} 
            echo -e ${msg} >> ${log_file}
            exit
        else
            date_time4=`date '+%Y-%m-%d %H:%M:%S'`
            echo -e "--  [${date_time4}]  [${j}]time(s), not find failed mds, sleep 5s will try again" >> ${log_file}
            sleep 5
            if [[ ${j} -gt 19 ]];then
                break
            fi
        fi
    done
done

```

