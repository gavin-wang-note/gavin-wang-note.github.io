---
layout:     post
title:      "借助lftp从SFTP Server下载ISO"
subtitle:   "lftp sftp to sync ISO"
date:       2023-01-09
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - lftp 
    - sftp
---


# 概述

之前一直提供的是ssh 协议下远程sync ISO，当时借助的是scp来copy，但受限于网络带宽的限制，两地sync速度太慢。
后台更换了公网IP下的SFTP Server，理论带宽是120Mib/s，所以此次输出sftp sync ISO script， mark之.


# SHELL Code

需要先安装lftp.
* 说明:
* * 需要先安装lftp.


{% raw %}```
root@apidoc:~$ cat sftp_iso.sh 
#!/bin/bash

if [ ! -n "$3" ] ;
then
    echo -e "\033[33musage: sftp_iso.sh [scaler/converger/cone] [centos7/xenial/cone] [version]"
    exit 0
fi

sftp_host="ftp-server-ip or domain name"
sftp_user="ftp-user-name"
sftp_password="ftp-user-password"
sftp_port=22
log_file="/var/log/sftp_sync_is.log"

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
    if [ ! -f "${list_build_id_res}" ]; then
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
    if [[ ${#array[@]} -gt 1 && ${remote_iso_name} =~ "ConvergerOne" ]]; then
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
                    lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${var}'; bye"&
                    wait
                    current_time=`date "+%Y-%m-%d %H:%M:%S"`
                    echo -e "[${current_time}]  End to get ISO :(${remote_path}/${latest_build_id}/${var}) to : (${local_path}/${daily_folder})" | tee -a ${log_file}
                    # lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${var}'; bye"
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
            lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${remote_iso_name}'; bye"&
            wait
            current_time=`date "+%Y-%m-%d %H:%M:%S"`
            echo -e "[${current_time}]  End to synced ISO : (${remote_path}/${latest_build_id}/${remote_iso_name}) to (${local_path}/${daily_folder})" | tee -a ${log_file}
            # lftp sftp://${sftp_user}:${sftp_password}@${sftp_host} -e "lcd ${local_path}/${daily_folder};reget '${remote_path}/${latest_build_id}/${remote_iso_name}'; bye"
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
``` {% endraw %}



# 额外补充


这里有一个当时碰到的问题，就是如何同remote端目录结构下最后一个Build ID，当时有参考：
```
https://stackoverflow.com/questions/49678020/how-to-get-the-latest-file-from-sftp-folder
```

虽然没有使用到，但这里mark一下，防止未来有碰到类似状况需要这篇文章中的操作指令。

最后自己的解决方法是整个list出来到本次文件，从本地文件中grep出来。



