---
layout:     post
title:      "ESXi remount VMFS"
subtitle:   "ESXi remount VMFS"
date:       2017-06-06
author:     "Gavin Wang"
catalog:    true
categories:
    - [ESXi]
    - [shell]
tags:
    - shell
    - ESXi
---


# Overview

The ESXi product has a bug that when the cluster is restarted, the cluster is not yet in a healthy state, during which the ESXi side scans early and hangs on VMFS, but it no longer fills up after a certain number of durations; and after the cluster is restored to health, ESXi does not initiate scanning actions anymore.

Write a script, put it on the ESXi side, set a timed task, and initiate a scan.


# Script of vmware_scan_remount.sh

```shell
#!/bin/sh

# add by bigtera wyz for remout vmfs at 2017-06-06 15:10
remount_log="/vmfs/volumes/datastore1 (1)/bigtera-cron/remount_vmfs.log"

echo "rescan all adapter"  >> ${remount_log}

for i in {1..50}
do
    echo "`date '+%Y-%m-%d %H:%M:%S'`  $i times to rescan" >> ${remount_log}
    esxcli storage core adapter rescan --all
    sleep 10
done

vmfs_uuid=`esxcli storage vmfs snapshot list | grep -i "vmfs uuid" | awk -F ":"
if [ ${vmfs_uuid} != "" ];then
    echo "`date '+%Y-%m-%d %H:%M:%S'`  need remount vmfs, vmfs uuid is ${vmfs_uu
    esxcli storage vmfs snapshot mount -u ${vmfs_uuid}
else
    echo "`date '+%Y-%m-%d %H:%M:%S'`  not found needed remount vmfs, skip remou
fi




min=1
max=50
while [ $min -le $max ]
do
    echo $min
    min=`expr $min + 1`
done  
```
