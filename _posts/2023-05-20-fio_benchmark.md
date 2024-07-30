---
layout:     post
title:      "fio benchmark"
subtitle:   "fio benchmark"
date:       2023-05-20
author:     "Gavin Wang"
catalog:    true
categories: 
    - [shell]
    - [performance]
    - [fio]
tags:
    - shell
    - performance
    - Linux
    - fio
---

# Overview

Write a performance tool to test NFS, CIFS, SAN Device, and output result after each scene.

# SOP

## 1. Prepare test environment

  * Install CentOS 7 as clients (Ubuntu should also be OK), client number is suggested same as that of gateways
  * The IP address of clients must be sequential
  * Yum install some packages, including fio, expect, psmisc, iscsi-initiator-utils, mount.nfs
  * Install dstat on storage node

## 2. Configure NFS/iSCSI in web UI

  * For NFS test

    * Create pool and shared folder within the pool
    * Mkdir some subfolders under the shared folder, number of subfolders is identical to gateway number

  * For iSCSI test

    * Create pool and some iSCSI targets, number of targets is identical to gateway number
    * Create one iSCSI LUN on each iSCSI target

## 3. Access storage from clients

  * For NFS test

    * Create mount point, same as the value of "nfsmount" in parameters.conf
    * Mount subfolders from clients, one subfolder to one client to one gateway
  * For iSCSI test

    * Discovery and login iSCSI LUN, one target to one client to one gateway
    * Make sure all clients have same /dev/sdx for iSCSI LUN, and the value is identical to "iscsilun" in parameters.conf
      -- Go to /etc/multipath, delete all of files under this folder, logout all of iscsi session, then login iscsi

## 4. Run test

   - Unzip the fio_benchmark in one of the clients

   - Modify parameters.conf, adjust client/server info

   - Check configs under fio_conf to adapt current situation

   - Run 01_fio_deploy.sh to deploy scripts on all clients

   - Run 03_run_remote_fio.sh to execute fio scripts as config order

   - Run 04_collect_fio_result.sh and 05_analayse_reslut.sh to collect results

   - Run 06_aggregate_result.sh is used to aggregate results of several cycles

## Content

#### parameter.conf:

This conf defines items below:

1. Info of clients and storage nodes
2. NFS mount point and iSCSI dev name
3. Location of scripts on each client

Scripts are usually executed by order of the number prefixed to the filename.

#### 00_run.sh:

This script can be treated as a set which is constituted by the following scripts. You can modify the steps to fill the concrete requirements.

#### 01_fio_deploy.sh: 

This script is used to copy related scripts and debs to all clients according to parameter.conf. The location is previously defined in parameter.conf. Since this script uses expect to interact, it is requested to install expect has not been installed on this client.

#### 02_install_rpm.sh:

This step is optional. Execute it to install fio on all clients if have no fio installed before. 【Deprecated】

#### 03_run_remote_fio.sh:

Execute this script if everything is ready.

#### 04_collect_fio_result.sh:

Collect all fio result logs to subfolder called fio_result on this client. The results are orgnized by client IP and located under result folder.

#### 05_analayse_reslut.sh:

It parses the results collected with 04_collect_fio_result.sh, convert result logs to csv for further disposal, and generate a report "Total.result" under result folder.

#### 06_aggregate_result.sh

Format result and store to result folder

#### 07_result_process.sh

Format and summary all of test result, so can copy the result into Excel

#### fio_conf/:

Put all fio configs under this folder, can decide the running sequence by specfying proper filename.

#### rpm/:

Include expect and fio tools.

#### subin/:

Some internal functions used by scripts.



# Files list

```shell
root@scaler80:/mnt/code/fio-benchmark# ls -l
total 152
-rw-r--r-- 1 root root  2082 May 28 04:13 00_run.sh
-rw-r--r-- 1 root root  2510 May 28 04:13 01_fio_deploy.sh
-rw-r--r-- 1 root root   571 May 28 04:13 02_install_rpm.sh
-rw-r--r-- 1 root root  2991 May 28 04:13 03_run_remote_fio.sh
-rw-r--r-- 1 root root  1301 May 28 04:13 04_collect_fio_result.sh
-rw-r--r-- 1 root root  4578 May 28 04:13 05_analyse_result.sh
-rw-r--r-- 1 root root  1582 May 28 04:13 06_aggregate_result.sh
-rw-r--r-- 1 root root  1668 May 28 04:13 07_result_process.sh
drwxr-xr-x 2 root root  4096 May 28 04:13 dpkg
drwxr-xr-x 3 root root  4096 May 28 04:13 fio_conf
-rw-r--r-- 1 root root   198 May 28 04:13 parameters.conf
-rw-r--r-- 1 root root   480 May 28 04:13 rdma_mount.sh
-rw-r--r-- 1 root root  3232 May 28 04:13 README.md
drwxr-xr-x 8 root root  4096 May 28 04:13 result
drwxr-xr-x 2 root root  4096 May 28 04:13 rpm
-rw-r--r-- 1 root root  1042 May 28 04:13 server_collect.sh
drwxr-xr-x 2 root root  4096 May 28 04:13 setup_env
drwxr-xr-x 4 root root  4096 May 28 04:13 storage-snapshot
drwxr-xr-x 2 root root  4096 May 28 04:13 subin
drwxr-xr-x 2 root root  4096 May 28 04:13 utils
-rw-r--r-- 1 root root  1877 May 28 04:13 watch_state.sh
root@scaler80:/mnt/code/fio-benchmark# 
```


