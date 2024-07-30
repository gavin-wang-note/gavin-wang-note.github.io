---
layout:     post
title:      "监控BigteraStore cache中inode消耗状况"
subtitle:   "Watch inode from BigteraStore cache"
date:       2021-10-09
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [shell]
tags:
    - shell
    - Linux
---



# 概述

S3性能测试， 向单一Bucket下持续灌入4K大下的对象，观察存储是否会随着Bucket下Objects熟的增多而出现性能衰减现象。

在此测试过程中，增加了一个脚本，用于监控BigteraStore cache中inode消耗状况，记录之。


# Script

`watch_inode_bt_cach_dump.sh`


```shell
#!/bin/bash

osd_ids=`ps -ef |grep ceph-osd | grep -v grep | awk '{{print $13}}' | sort`
inode_info='df -ih /data/cache/*'
all_mon_ips=`ceph mon dump | grep mon.* | awk -F ':' '{{print $2}}'`

i=1
max_loop=600
log_file='s3_watch_dump.log'

while true
do
    if [ $i -ge ${max_loop}  ]; then
        cur_date="`date +%Y-%m-%d,%H:%m:%s`"
        echo -e [${cur_date}] " Finished, exit\n" >> ${log_file}
        break
    else
        echo -e "\n=======================================  $i  ============================================" >> ${log_file}
        echo -e "\n-- ceph df output: --\n" >> ${log_file}
        echo -e "`ceph df`" >> ${log_file}
        echo -n "" >> ${log_file}

        echo -e "\n-- dump bigterastore output: --" >> ${log_file}
        for each_ip in ${all_mon_ips}
        do
            for each_id in ${osd_ids}
            do
                echo -e "\n[${each_ip}] osd.${each_id} perf dump bigterastore info" >> ${log_file}
                perf_info=`ceph daemon osd.${each_id} perf dump bigterastore`
                cur_date="`date +%Y-%m-%d,%H:%m:%s`" 
                echo -e [${cur_date}] [${each_ip}] "${perf_info}" >> ${log_file}
            done
        done
        sleep 0.5

        for each_ip in ${all_mon_ips}
        do
            cur_date="`date +%Y-%m-%d,%H:%m:%s`" 
            cache_info=`ssh ${each_ip} 'df -ih /data/cache/*'`
            echo -e "\n[${each_ip}  cache inode usage info" >> ${log_file}
            echo -e [${cur_date}] "\n${cache_info}" >> ${log_file}
            sleep 1
        done
        i=`expr $i + 1`
        sleep 600
    fi
done
```
