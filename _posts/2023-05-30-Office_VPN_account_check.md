---
layout:     post
title:      "NJ Office OpenVPN 账号访问认证"
subtitle:   "NJ Office of VPN Account Auth"
date:       2023-05-30
author:     "Gavin"
catalog:    true
tags:
    - VPN
---


# Overview

NJ Office 开放了Open VPN，方便大家远程办公，但没有对访问者进行鉴权认证，任何一个人拿到VPN Config后，都可以接入到NJ Office LAB 网络，存在极大的安全隐患。

本文介绍如何对 Open VPN 账号的鉴权认证，对于非法用户，禁止登录；对于长期休眠账户，禁止登录（解禁后方可恢复正常）。


# 实践


## 修改 Open VPN 的 server.conf

增加用户名校验配置项，在尾部增加如下内容：

```
username-as-common-name
```

## 设定账号密码文件

psw-file 文件内容片段参考如下：

```
Gavin gUOl3h
Kevin NJl3uQ
Echo sHd4cQ
```

一行一个记录，第一列是用户名，第二列是密码


## 增加密码校验脚本

checkpsw.sh 内容如下：

```
#!/bin/bash
###########################################################
# checkpsw.sh (C) 2004 Mathias Sundman <mathias@openvpn.se>
#
# This script will authenticate OpenVpn users against
# a plain text file. The passfile should simply contain
# one row per user with the username first followed by
# one or more space(s) or tab(s) and then the password.
###########################################################
 
PASSFILE="/etc/openvpn/psw-file"
LOG_FILE="/etc/openvpn/openvpn-password.log"
TIME_STAMP=`date "+%Y-%m-%d %T"`
 
readarray -t lines < $1
username=${lines[0]}
password=${lines[1]}

if [ ! -r "${PASSFILE}" ]; then
echo "${TIME_STAMP}: Could not open password file \"${PASSFILE}\" for reading." >> ${LOG_FILE}
exit 1
fi
 
CORRECT_PASSWORD=`awk '!/^;/&&!/^#/&&$1=="'${username}'"{print $2;exit}' ${PASSFILE}`
 
if [ "${CORRECT_PASSWORD}" = "" ]; then
echo "${TIME_STAMP}: User does not exist: username=\"${username}\", password=\"${password}\"." >> ${LOG_FILE}
exit 1
fi
 
if [ "${password}" = "${CORRECT_PASSWORD}" ]; then
echo "${TIME_STAMP}: Successful authentication: username=\"${username}\"." >> ${LOG_FILE}
exit 0
fi
 
echo "${TIME_STAMP}: Incorrect password: username=\"${username}\", password=\"${password}\"." >> ${LOG_FILE}
exit 1
```

脚本中定义了：

```
PASSFILE="/etc/openvpn/psw-file"
LOG_FILE="/etc/openvpn/openvpn-password.log"
```

其中 ```/etc/openvpn/openvpn-password.log``` 用于登录账户解析使用，因为不同的账户访问VPN都会记录日志，其中含有当前登录用户名。

## 增加openvpn-password.log日志解析

```
#!/bin/bash

record_log='/etc/openvpn/vpn_login_time_check.log'
log_file='/etc/openvpn/openvpn-password.log'
user_file='/etc/openvpn/psw-file'

all_users=`cat ${user_file} | grep -v bigtera | awk '{print $1}'`

current=`date "+%Y-%m-%d %H:%M:%S"`
echo -e "[${current}] Start to check VPN log in time for all of users..." >> ${record_log}

for each_user in ${all_users};
do
    last_login_data=`cat ${log_file} | grep ${each_user} | grep 'Successful authentication' | sed -n '$p' | awk '{print $1, $2}' | sed 's/:$//g'`
    # echo ${each_user}, ${last_login_data}
    if [[ x${last_login_data} != x'' ]];then
        current=`date "+%Y-%m-%d %H:%M:%S"`
        cur_time_stamp=`date -d "${current}" +%s`
        last_login_time_stamp=`date -d "${last_login_data}" +%s`
        # echo ${cur_time_stamp}, ${last_login_time_stamp}
        time_diff=`expr ${cur_time_stamp} - ${last_login_time_stamp}`
        # echo "---  time_diff : (${time_diff})"
        if [[ ${time_diff}  -ge 604800 ]];then  # 7 days
            if [[ x${each_user} == x'Gavin' ]]; then
                email_addr='Gavin.wang@bigtera.com.cn'
            elif [[ "${each_user}" == "Sky" ]]; then
                email_addr='Sky_wu@bigtera.com.cn'
            elif [[ "${each_user}" == "Simon" ]]; then
                email_addr='simon.chen@bigtera.com.cn'
            elif [[ "${each_user}" == "Anhao" ]]; then
                email_addr='stephen.sun@bigtera.com.cn'
            else
                email_addr=''
            fi

            send_mail_cmd='echo -e "\t您已长时间未访问南京VPN，账号('${each_user}')存在过期风险. \n\t您上次访问日期是: '${last_login_data}'\n\n此邮件为系统自动发出，请勿回复." | mail -s "NJ LAB of VPN account expiration notification" '${email_addr}''
            echo "${send_mail_cmd}" >> ${record_log}
            `${send_mail_cmd}`
        fi
    fi
done
```



## 校验失败log参考

当VPN账号认证失败后，会记录 vpn_login_time_check.log，内容格式如下：

```
echo -e "\t您已长时间未访问南京VPN，账号(Howard)存在过期风险. \n\t您上次访问日期是: 2023-04-29 20:30:57\n\n此邮件为系统自动发出，请勿回复." | mail -s "NJ LAB of VPN account expiration notification" 
echo -e "\t您已长时间未访问南京VPN，账号(Seven)存在过期风险. \n\t您上次访问日期是: 2023-04-30 09:48:44\n\n此邮件为系统自动发出，请勿回复." | mail -s "NJ LAB of VPN account expiration notification" seven.chen@bigtera.com.cn
echo -e "\t您已长时间未访问南京VPN，账号(Wangbx)存在过期风险. \n\t您上次访问日期是: 2023-05-15 20:34:49\n\n此邮件为系统自动发出，请勿回复." | mail -s "NJ LAB of VPN account expiration notification" wangbx@bigtera.com.cn
```


# 综述

有了账号认证，每个用户在访问VPN时，都会校验改用户的有效性、合法性，提高了LAB 服务器访问的安全性。

