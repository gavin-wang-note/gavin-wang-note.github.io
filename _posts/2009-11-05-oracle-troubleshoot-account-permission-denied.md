---
layout:     post
title:      "Oracle案例--应用用户登录数据库报没权限或找不到LIB库文件"
subtitle:   "Oracle troubleshoot of not oracle account permission denied"
date:       2009-11-05
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 非oracle终端用户telnet情况下，应用用户登录数据库报没权限或找不到LIB库文件

## 表象

非oracle用户telnet登录终端，如mmsg终端用户登录，执行sqlplus命令查看应用数据库信息，报没权限。

```
30 mmsg [mmsg] :/home/mmsg>p

===========华为 infoX IAG 系统运行状态 2009年11月05日 19:51:08=================
系统安装位置：/home/mmsg/mms_home。
监控进程未运行。

=================================本机IP地址列表=================================
10.164.74.222       127.0.0.1           192.164.100.222     
[2009-11-05 19:51:08.052] 数据库错误:libclntsh.so: cannot open shared object file: No such file or directory

DBMS API Library 'libclntsh.so' loading fails
This library is a part of DBMS client installation, not SQLAPI++
Make sure DBMS client is installed and
this required library is available for dynamic loading

Linux/Unix/UnixWare:
1) The directories in the user's LD_LIBRARY_PATH environment variable
2) The list of libraries cached in /etc/ld.so.cache
3) /usr/lib, followed by /lib
 dbname:"mmsgdb", dbuser:"mmsg"
31 mmsg [mmsg] :/home/mmsg>cd ${ORACLE_HOME}/lib32
/opt/oracle/product/11g/lib32: 权限不够.
```

## 原因

非oracle终端用户telnet情况下，该终端用户没权限访问数据库。

## 解决方法

将当前telnet终端用户加入oinstall组中：

（1）usermod -G oinstall mmsg

（2）当前用户退出终端，重新登录就OK啦！

