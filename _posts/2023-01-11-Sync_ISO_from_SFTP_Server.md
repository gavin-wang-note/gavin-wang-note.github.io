---
layout:     post
title:      "Sync ISO script from SFTP Server"
subtitle:   "Script of sync ISO from SFTP Server"
date:       2023-01-11
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [shell]
tags:
    - shell

---


# Overview

Because Build Man is not in Nanjing, I need to synchronize ISO to NJ Lab from the corresponding server in other cities of the company, so I wrote a script.
In the early days, it was automatically synced from the source to NJ, but later, due to the company's network security reinforcement, it could only be synced from the intranet, and in the sftp way.


# Files list

```shell
8.x_iso_scp.sh
for_sftp_sync_fstab
sftp_iso.sh
```


# Scripts

## Modify /etc/fstab

```shell
10.16.172.102:/vol/share/Builds/buildwindow/centos7/virtualstor_scaler_8.2 /mnt/centos7/8.2    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/centos7/virtualstor_scaler_8.3 /mnt/centos7/8.3    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/centos7/virtualstor_scaler_8.0 /mnt/centos7/8.0    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_8.2 /mnt/xenial/8.2    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_8.3 /mnt/xenial/8.3    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_8.0 /mnt/xenial/8.0    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.2 /mnt/cone/1.2    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.2_oem_putian /mnt/cone/1.2_oem_putian    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.3 /mnt/cone/1.3    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_oem_putian_8.0 /mnt/xenial/8.0_oem_putian    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_oem_fiberhome_8.0 /mnt/xenial/8.0_oem_fiberhome    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_oem_fiberhome_8.2 /mnt/xenial/8.2_oem_fiberhome    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_oem_thinkingdata_8.2 /mnt/xenial/8.2_oem_thinkingdata    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.2_oem_fiberhome /mnt/cone/1.2_oem_fiberhome    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.2_oem_thinkingdata /mnt/cone/1.2_oem_thinkingdata    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.2_oem_xinzhe /mnt/cone/1.2_oem_xinzhe    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.2_oem_xinzhe_dark /mnt/cone/1.2_oem_xinzhe_dark    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.3_oem_fiberhome /mnt/cone/1.3_oem_fiberhome    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/cone/1.3_oem_thinkingdata /mnt/cone/1.3_oem_thinkingdata    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_oem_hygon_8.0 /mnt/xenial/8.0_oem_hygon    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_oem_chaoyun_8.2 /mnt/xenial/8.2_oem_chaoyun    nfs    defaults        0 0
10.16.172.102:/vol/share/Builds/buildwindow/xenial/virtualstor_scaler_oem_srie_8.0 /mnt/xenial/8.0_oem_srie    nfs    defaults        0 0
10.16.172.103:/vol/share/Builds/buildwindow/cone/1.4 /mnt/cone/1.4    nfs    defaults        0 0
10.16.172.104:/vol/share/Builds/buildwindow/cone/1.4_oem_daasbank /mnt/cone/1.4_oem_daasbank    nfs    defaults        0 0
10.16.172.104:/vol/share/Builds/buildwindow/cone/2.1 /mnt/cone/2.1    nfs    defaults        0 0
```

mount point下内容：

```shell
root@apidoc:/mnt$ ll
total 0
drwxr-xr-x.  3 root root           17 Dec 29  2021 arm
drwxr-xr-x.  5 root root           39 May 28  2021 centos7
drwxr-xr-x. 16 root root          286 Jan  6 10:25 cone
drwxr-xr-x.  1 1000 1000 820255811108 Jan  5 12:01 kylin
drwxr-xr-x. 12 root root          203 Feb 23  2022 xenial
root@apidoc:/mnt$ cd xenial/
root@apidoc:/mnt/xenial$ ll
total 0
drwxrwxr-x. 1 nfsnobody nfsnobody 131011422392 Aug 16  2021 8.0
drwxrwxr-x. 1 nfsnobody nfsnobody   4225724416 Jun 25  2021 8.0_oem_fiberhome
drwxrwxr-x. 1 nfsnobody nfsnobody   4222875648 Nov 10  2021 8.0_oem_hygon
drwxrwxr-x. 1 nfsnobody nfsnobody   8437528576 Jun 25  2021 8.0_oem_putian
drwxrwxr-x. 1 nfsnobody nfsnobody   4225492992 Feb 23  2022 8.0_oem_srie
drwxrwxr-x. 1 nfsnobody nfsnobody 338626134376 Aug 16  2021 8.2
drwxrwxr-x. 1 nfsnobody nfsnobody   9681530880 Nov 10  2021 8.2_oem_chaoyun
drwxrwxr-x. 1 nfsnobody nfsnobody  29034631168 Sep  7  2021 8.2_oem_fiberhome
drwxrwxr-x. 1 nfsnobody nfsnobody   9652283392 Jul  5  2021 8.2_oem_thinkingdata
drwxrwxr-x. 1 nfsnobody nfsnobody 518908765624 Aug 16  2021 8.3
root@apidoc:/mnt/xenial$ 
root@apidoc:/mnt/xenial$

root@apidoc:/mnt/cone$ 
root@apidoc:/mnt/cone$ ll
total 0
drwxr-xr-x. 3 root      root                18 Jan  6 15:32 1.0
drwxrwxr-x. 1 nfsnobody nfsnobody   5272838144 Jun 21  2021 1.2
drwxrwxr-x. 1 nfsnobody nfsnobody   5262286848 Oct 11  2021 1.2_oem_fiberhome
drwxrwxr-x. 1 nfsnobody nfsnobody   5264971776 Jun 21  2021 1.2_oem_putian
drwxrwxr-x. 1 nfsnobody nfsnobody 232057397248 Oct 11  2021 1.2_oem_thinkingdata
drwxrwxr-x. 1 nfsnobody nfsnobody   5270681600 Oct 11  2021 1.2_oem_xinzhe
drwxrwxr-x. 1 nfsnobody nfsnobody   5285871616 Oct 11  2021 1.2_oem_xinzhe_dark
drwxrwxr-x. 1 nfsnobody nfsnobody  21246191616 Jan  6 15:31 1.3
drwxrwxr-x. 1 nfsnobody nfsnobody  10607448064 Apr  5  2022 1.3_oem_fiberhome
drwxrwxr-x. 1 nfsnobody nfsnobody   5314854912 Oct 12  2021 1.3_oem_thinkingdata
drwxrwxr-x. 1 nfsnobody nfsnobody 429528580220 Aug 25 12:42 1.4
drwxrwxr-x. 1 nfsnobody nfsnobody   9762013184 Aug 25 16:42 1.4_oem_daasbank
drwxr-xr-x. 3 root      root                18 Sep  2 10:46 1.4_oem_dassbank
drwxrwxr-x. 1 nfsnobody nfsnobody  11154866176 Jan  6 17:17 2.1
root@apidoc:/mnt/cone$ 

root@apidoc:/mnt$ cd centos7/
root@apidoc:/mnt/centos7$ ll
total 0
drwxrwxr-x. 1 nfsnobody nfsnobody 139628591104 Aug 16  2021 8.0
drwxrwxr-x. 1 nfsnobody nfsnobody 413614030848 Aug 16  2021 8.2
drwxrwxr-x. 1 nfsnobody nfsnobody 443107670532 Jan  6 15:47 8.3
root@apidoc:/mnt/centos7$ cd 8.3/
root@apidoc:/mnt/centos7/8.3$ ll
total 0
drwxr-xr-x. 1 nfsnobody nfsnobody            0 Dec  2  2021 converger
drwxr-xr-x. 1 nfsnobody nfsnobody 453293586948 Jan 10 06:09 scaler
root@apidoc:/mnt/centos7/8.3$ 
```



## `8.x_iso_scp.sh`

```shell
#!/bin/bash

all_versions=(8.3 8.2 8.0)
scp_shell="/root/sftp_iso.sh"
iso_sync_file="/tmp/iso_sync.txt"
log_file="/var/log/sftp_sync_is.log"

if [  ! -f ${scp_shell} ]; then
   echo "[ERROR] scp_iso.sh not exist, exit!!!"
   exit 1
fi

if [  -f ${iso_sync_file} ]; then
    rm -rf ${iso_sync_file}
fi

LOCK_FILE=/tmp/iso_sync.lock
exec 100>"$LOCK_FILE"
flock -n 100
if [ "$?" != 0 ]; then
    echo "[Process Check] $0 This Script Has Old Process Running, exit..."
    exit 1
fi
# 因primjs markdown的渲染问题，这里井号前加了\，实际使用需要拿掉\
for(( i=0;i<${\#all_versions[@]};i++)) 
do
    echo "Srart to sync ${all_versions[i]}"
    bash ${scp_shell} scaler xenial ${all_versions[i]}
    bash ${scp_shell} scaler centos7 ${all_versions[i]}
done;

# bash ${scp_shell} cone cone 1.2
# bash ${scp_shell} cone cone 1.2_oem_putian
# bash ${scp_shell} cone cone 1.2_oem_fiberhome
# bash ${scp_shell} cone cone 1.2_oem_thinkingdata
# bash ${scp_shell} cone cone 1.2_oem_xinzhe
# bash ${scp_shell} cone cone 1.2_oem_xinzhe_dark
bash ${scp_shell} cone cone 1.3
# bash ${scp_shell} cone cone 1.3_oem_fiberhome
# bash ${scp_shell} cone cone 1.3_oem_thinkingdata
# bash ${scp_shell} scaler xenial 8.0_oem_fiberhome
# bash ${scp_shell} scaler xenial 8.0_oem_putian
# bash ${scp_shell} scaler xenial 8.2_oem_fiberhome
# bash ${scp_shell} scaler xenial 8.2_oem_thinkingdata
# bash ${scp_shell} scaler xenial 8.2_oem_chaoyun
# bash ${scp_shell} scaler xenial 8.0_oem_hygon
# bash ${scp_shell} scaler xenial 8.0_oem_srie
bash ${scp_shell} cone cone 1.4
# bash ${scp_shell} cone cone 1.4_oem_Dassbank
bash ${scp_shell} cone cone 2.1


function wait_task_finished(){
if [ -f ${iso_sync_file} ]; then
    while [ "1" = "1" ]
        do
            current_time=`date "+%Y-%m-%d %H:%M:%S"`
            iso_sync_res=`cat ${iso_sync_file} | awk '{{print $NF}}' | grep -vi md5`
            array=(${iso_sync_res// / })
            for var in ${array[@]}
            do
                ps_res=`ps -ef | grep ${var} |grep -v grep`
                if [[ ! ${ps_res} ]]; then
                    echo -e "[${current_time}]  Finished to sync : ${var}" | tee -a ${log_file}
                    sed -i "/${var}/d" ${iso_sync_file}
                else
                    echo -e "[${current_time}]  ISO : (${var}) sync ongoing" | tee -a ${log_file}
                fi
            done
            sleep 60
        done
else
    current_time=`date "+%Y-%m-%d %H:%M:%S"`
    echo -e "[${current_time}]  [ERROR]  Not find file : (${iso_sync_file}), no need to check ISO sync stats. exit!!!" | tee -a ${log_file}
    exit 8
fi
}

wait_task_finished
```



## `sftp_iso.sh`

```shell
#!/bin/bash

if [ ! -n "$3" ] ;
then
    echo -e "\033[33musage: sftp_iso.sh [scaler/converger/cone] [centos7/xenial/cone] [version]"
    exit 0
fi

sftp_host="21.22.26.12"
sftp_user="ftpusername"
sftp_password="ftpuserpassword"
sftp_port=22
log_file="/var/log/sftp_sync_is.log"
iso_sync_file="/tmp/iso_sync.txt"

product=$1
product_type=$2
product_version=$3

case $product in
         scaler | converger | cone)
           current_time=`date "+%Y-%m-%d %H:%M:%S"`
           echo -e "\n======================================================  [${current_time}]  =================================================" | tee -a ${log_file}
           echo -e "[${current_time}]  Product is $product." | tee -a ${log_file}
         ;;
         *)
           echo "[${current_time}]  [ERROR]  Product must be scaler/converger/cone, script exits!"
           exit 1
         ;;
esac


case ${product_version} in
         8.0 | 8.2 | 8.3 | 1.0 | 1.2 | 1.2_oem_putian | 1.2_oem_fiberhome | 1.2_oem_thinkingdata | 1.2_oem_xinzhe | 1.2_oem_xinzhe_dark | 1.3 | 1.3_oem_fiberhome | 1.3_oem_thinkingdata | 1.4 | 1.4_oem_daasbank | 2.1 | 8.0_oem_fiberhome | 8.0_oem_putian | 8.2_oem_thinkingdata | 8.2_oem_fiberhome | 8.2_oem_chaoyun | 8.0_oem_hygon | 8.0_oem_srie)
           current_time=`date "+%Y-%m-%d %H:%M:%S"`
           echo -e "[${current_time}]  Version is ${product_version}" | tee -a ${log_file}
         ;;
         *)
           echo -e "\033[31mVersion must be 8.0 8.2 8.3 1.2 1.2_oem_putian 1.2_oem_fiberhome 1.2_oem_thinkingdata 1.2_oem_xinzhe 1.2_oem_xinzhe_dark 1.3 1.3_oem_fiberhome 1.3_oem_thinkingdata 1.4 1.4_oem_daasbank 8.0_oem_fiberhome 8.0_oem_putian 8.2_oem_thinkingdata 8.2_oem_fiberhome 8.2_oem_chaoyun 8.0_oem_hygon 8.0_oem_srie, script exits!!! "
           exit 6
         ;;
esac


function check_mount_point(){
    if [ ! -d "$1" ]; then
        echo -e "[ERROR]  Path : ($1 not exist, exit!!!) "
        exit 2
    else
       mnt_res=`mountpoint $1`
       if [[ ${mnt_res} =~ "is not a" ]]; then
           echo -e "[ERROR]  Path : ($1) is not a mountpoint, exit!!! "
           exit 3
       fi
    fi
}


function iso_download()
{
    list_build_id_res="/tmp/ls_build_id.output"
    list_builds_res="/tmp/ls_builds.output"

    if [ X${product} = X"scaler" ]; then
        if [ X${product_version} = X"8.0" ]; then
            remote_path="scaler/virtualstor_8.0/builds"
            if [ X${product_type} = X'xenial' ]; then
                mnt_path="/mnt/xenial/8.0"
                local_path="${mnt_path}/scaler"
            elif [ X${product_type} = X'centos7' ]; then
                mnt_path="/mnt/centos7/8.0"
                local_path="${mnt_path}/scaler"
            fi
            check_mount_point ${mnt_path}
        elif [ X${product_version} = X"8.2" ]; then
            remote_path="scaler/virtualstor_8.2/builds"
            if [ X${product_type} = X'xenial' ]; then
                mnt_path="/mnt/xenial/8.2"
                local_path="${mnt_path}/scaler"
            elif [ X${product_type} = X'centos7' ]; then
                mnt_path="/mnt/centos7/8.2"
                local_path="${mnt_path}/scaler"
            fi
            check_mount_point ${mnt_path}
        elif [ X${product_version} = X"8.3" ]; then
            remote_path="scaler/virtualstor_8.3/builds"
            if [ X${product_type} = X'xenial' ]; then
                mnt_path="/mnt/xenial/8.3"
                local_path="${mnt_path}/scaler"
            elif [ X${product_type} = X'centos7' ]; then
                mnt_path="/mnt/centos7/8.3"
                local_path="${mnt_path}/scaler"
            fi
            check_mount_point ${mnt_path}
        fi
    fi

    if [ X${product} = X"cone" ]; then
        if [ X${product_version} = X"1.0" ]; then
            remote_path="cone/virtualstor_converger_one_1.0/builds"
            mnt_path="/mnt/cone/1.0"
            local_path="${mnt_path}/cone"
            check_mount_point ${mnt_path}
        elif [ X${product_version} = X"1.2" ]; then
            remote_path="cone/virtualstor_converger_one_1.2/builds"
            mnt_path="/mnt/cone/1.2"
            local_path="${mnt_path}/cone"
            check_mount_point ${mnt_path}
        elif [ X${product_version} = X"1.3" ]; then
            remote_path="cone/virtualstor_converger_one_1.3/builds"
            mnt_path="/mnt/cone/1.3"
            local_path="${mnt_path}/cone"
            check_mount_point ${mnt_path}
        elif [ X${product_version} = X"1.4" ]; then
            remote_path="cone/virtualstor_converger_one_1.4/builds"
            mnt_path="/mnt/cone/1.4"
            local_path="${mnt_path}/cone"
            check_mount_point ${mnt_path}
        elif [ X${product_version} = X"2.1" ]; then
            remote_path="cone/virtualstor_converger_one_2.1/builds"
            mnt_path="/mnt/cone/2.1"
            local_path="${mnt_path}/cone"
            check_mount_point ${mnt_path}
        fi
    fi

    current_time=`date "+%Y-%m-%d %H:%M:%S"`
    echo -e "[${current_time}]  Will to get latest ISO file for : (${product} ${product_version} ${product_type}) from remote path : (${remote_path})" | tee -a ${log_file}

    # If file exist, delete it first
    if [ -f "${list_build_id_res}" ]; then
        rm -rf ${list_build_id_res}
    fi

    lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "ls ${remote_path} | grep -v latest; bye" | tee ${list_build_id_res}
    if [ ! -f "${list_build_id_res}" ]; then
        current_time=`date "+%Y-%m-%d %H:%M:%S"`
        echo -e "[${current_time}]  [ERROR]  Not get build id info to local, please to check lftp command, exit!!!" | tee -a ${log_file}
        exit 4
    fi

    latest_build_id=`awk '{print $NF}' ${list_build_id_res} | grep -v '\.' | sort -nr | head -n1`
    latest_build_id=${latest_build_id//$'\r'}
    current_time=`date "+%Y-%m-%d %H:%M:%S"`
    echo -e "[${current_time}]  Latest Build id : ${latest_build_id}" | tee -a ${log_file}

    # If builds info of file exist, delete it
    if [ -f "${list_builds_res}" ]; then
        rm -rf ${list_builds_res}
    fi

    lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "ls ${remote_path}/${latest_build_id}; bye" | tee ${list_builds_res}
    
    if [ ! -f "${list_builds_res}" ]; then
        current_time=`date "+%Y-%m-%d %H:%M:%S"`
        echo -e "[${current_time}]  [ERROR]  Not get builds info to local, please to check lftp command, exit!!!" | tee -a ${log_file}
        exit 5
    fi

    if [ X${product_type} = X"cone" ]; then
        if [[ X${product_version} = X"1.4" ]]; then
            current_time=`date "+%Y-%m-%d %H:%M:%S"`
            echo -e "[${current_time}]  ConevergerOne Product and version is 1.4" | tee -a ${log_file}
            build_day_str_lines=`cat ${list_builds_res} | awk '{{print $NF}}' | grep iso | awk -F '~' '{{print $2}}' | uniq | cut -b 1-8 | uniq | awk '{print NF}'`
            build_day_str=`cat ${list_builds_res} | awk '{{print $NF}}' | grep iso | awk -F '~' '{{print $2}}' | uniq | cut -b 1-8 | uniq`
        elif [[ X${product_version} > X"2.0" ]]; then
            current_time=`date "+%Y-%m-%d %H:%M:%S"`
            echo -e "[${current_time}]  ConevergerOne Product and version is >= 2.1" | tee -a ${log_file}
            build_day_str_lines=`cat ${list_builds_res} | awk '{{print $NF}}' | grep iso | awk -F '-' '{{print $6}}' | uniq | cut -b 1-8 | uniq | awk '{print NF}'`
            build_day_str=`cat ${list_builds_res} | awk '{{print $NF}}' | grep iso | awk -F '-' '{{print $6}}' | uniq | cut -b 1-8 | uniq`
        else
            current_time=`date "+%Y-%m-%d %H:%M:%S"`
            echo -e "[${current_time}]  ConevergerOne Product and version is <=1.3" | tee -a ${log_file}
            build_day_str_lines=`cat ${list_builds_res} | grep iso | awk '{{print $NF}}' | awk -F '~' '{{print $2}}' | cut -b 1-8 | uniq | awk '{print NF}'`
            build_day_str=`cat ${list_builds_res} | grep iso | awk '{{print $NF}}' | awk -F '~' '{{print $2}}' | cut -b 1-8 | uniq`
        fi
    else
        current_time=`date "+%Y-%m-%d %H:%M:%S"`
        echo -e "[${current_time}]  Scaler Product" | tee -a ${log_file}
        build_day_str_lines=`cat ${list_builds_res} | grep iso | awk '{{print $NF}}' | awk -F '~' '{{print $2}}' | cut -b 1-8 | uniq | awk '{print NF}'`
        build_day_str=`cat ${list_builds_res} | grep iso | awk '{{print $NF}}' | awk -F '~' '{{print $2}}' | cut -b 1-8 | uniq`
    fi

    if [[ ${build_day_str_lines} -gt 1 ]]; then
        current_time=`date "+%Y-%m-%d %H:%M:%S"`
        echo -e "[${current_time}]  [ERROR]  Find different days from path of ($(remote_path)), exit!!!" | tee -a ${log_file}
        echo -e "[Debug] ${build_day_str}" | tee -a ${log_file}
        exit 6
    fi

    # build_day_str, like this: 20230106
    year=`echo ${build_day_str} | cut -b 1-4`
    month=`echo ${build_day_str} | cut -b 5-6`
    day=`echo ${build_day_str} | cut -b 7-8`
    daily_folder="${year}-${month}-${day}"
    if [[ ${daily_folder} =~ "--" ]]; then
        current_time=`date "+%Y-%m-%d %H:%M:%S"`
        echo -e "[${current_time}]  [ERROR]  Wrong type of daily folder name, exit!!!"
        exit 7
    fi

    if [ ! -d "${local_path}/${daily_folder}" ]; then
        current_time=`date "+%Y-%m-%d %H:%M:%S"`
        echo -e "[${current_time}]  Local path has no folder of ${local_path}/${daily_folder}, now create it" | tee -a ${log_file}
        mkdir -p ${local_path}/${daily_folder}
    fi

    # If local path has the file, which size and build id same as remote, skip to sync
    if [ X${product_type} = X"cone" ]; then
        product_type="ConvergerOne"
    fi
    remote_iso_name=`cat ${list_builds_res} | grep -i iso | grep -vi md5 | grep -i ${product_type} | awk '{{print $9, $10}}'`
    remote_iso_name=`echo ${remote_iso_name} | sed -e 's/^[ \t]*//g'`
    array=(${remote_iso_name// / })
    # 下面这里的井号前的\，实际使用时需拿掉\
    if [[ ${\#array[@]} -gt 1 && ${remote_iso_name} =~ "ConvergerOne" ]]; then
        # If has more than one ISO under remote folder
        for var in ${array[@]}
            do
                remote_iso_size=`cat ${list_builds_res} | grep ${var} | grep -v md5 | grep -i ${product_type} | awk '{{print $5}}'`
                local_iso_size=`ls -l ${local_path}/${daily_folder} | grep -vi md5 | grep -vi total | grep ${var} | awk '{{print $5}}'`
                if [ X${remote_iso_size} = X${local_iso_size} ]; then
                    current_time=`date "+%Y-%m-%d %H:%M:%S"`
                    echo -e "[${current_time}]  [SKIP]  Has been synced ISO : (${remote_path}/${latest_build_id}/${var}) to (${local_path}/${daily_folder})" | tee -a ${log_file}
                else
                    current_time=`date "+%Y-%m-%d %H:%M:%S"`
                    echo -e "[${current_time}]  Start to get ISO :(${remote_path}/${latest_build_id}/${var}) to : (${local_path}/${daily_folder}) at backend" | tee -a ${log_file}
                    echo ${var} >> ${iso_sync_file}
                    lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${var}'; reget '${remote_path}/${latest_build_id}/${var}.md5'; bye"&
                    # lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${var}'; reget '${remote_path}/${latest_build_id}/${var}.md5'; bye"
                fi
            done
    else
        # Only one ISO under the remote folder
        remote_iso_size=`cat ${list_builds_res} | grep iso | grep -v md5 | grep -i ${product_type} | awk '{{print $5}}'`
        local_iso_size=`ls -l ${local_path}/${daily_folder} | grep -vi md5 | grep -vi total | grep ${latest_build_id} | awk '{{print $5}}'`
        # remote_iso_name=${remote_iso_name//$'\r'}
        # remote_iso_size=${remote_iso_size//$'\r'}
        # local_iso_size=${local_iso_size//$'\r'}
        if [[ X${remote_iso_size} = X${local_iso_size} ]]; then
            current_time=`date "+%Y-%m-%d %H:%M:%S"`
            echo -e "[${current_time}]  [SKIP]  Has been synced ISO : (${remote_path}/${latest_build_id}/${remote_iso_name}) to (${local_path}/${daily_folder})" | tee -a ${log_file}
        else
            current_time=`date "+%Y-%m-%d %H:%M:%S"`
            echo -e "[${current_time}]  Start to get ISO :(${remote_path}/${latest_build_id}/${remote_iso_name}) to : (${local_path}/${daily_folder}) at backend" | tee -a ${log_file}
            echo ${remote_iso_name} >> ${iso_sync_file}
            lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${remote_iso_name}'; reget '${remote_path}/${latest_build_id}/${remote_iso_name}.md5'; bye"&
            # lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${remote_iso_name}'; reget '${remote_path}/${latest_build_id}/${remote_iso_name}.md5'; bye"
        fi
    fi
}


iso_download

# function iso_download()
# {
#     expect <<- EOF
#     set timeout 1800
#     spawn sftp -P $sftp_port $sftp_user@$sftp_host
# 
#     expect { 
#         "(yes/no)?" {send "yes\r"; expect_continue }
#         "*assword:" {send "$sftp_password\r"}
#     }
#     expect "sftp>"
#     send "cd $sftpLoadPath \r"
#     expect "sftp>"
#     send "lcd $myDir \r"
#     expect "sftp>"
#     set timeout -1
#     send "reget $fileFilter \r"
#     expect "sftp>"
#     send "bye\r"
# EOF
# }
```



# 额外补充


这里有一个当时碰到的问题，就是如何同remote端目录结构下最后一个Build ID，当时有参考：

```shell
https://stackoverflow.com/questions/49678020/how-to-get-the-latest-file-from-sftp-folder
```

虽然没有使用到，但这里mark一下，防止未来有碰到类似状况需要这篇文章中的操作指令。

最后自己的解决方法是整个list出来到本次文件，从本地文件中grep出来。

