---
layout:     post
title:      "Oracle案例--错误码之ORA-00257"
subtitle:   "Oracle error code troubleshoot--ORA-00257"
date:       2010-04-07
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-00257  归档程序错误。在释放之前仅限于内部连接案例

## 现象

```shell
========== Running state of HUAWEI infoX IAG system 20100407 09:09:05 ==========
The path of the installation : /home/mmsg/mms_home. 
The monitor process  is running well-balanced . pid:7753

=============================== List of Local IP ===============================
10.164.75.102       127.0.0.1           192.168.100.106     
[2010-04-07 09:09:05.527] DB Error :ORA-00257: 归档程序错误。在释放之前仅限于内部连接
 dbname:"mmsgdb_222", dbuser:"mmsg"
```

尝试登录数据库

```shell
164 mmsg01 [mmsg] :/home/mmsg>sqlplus mmsg/mmsg@mmsgdb_222

SQL*Plus: Release 11.1.0.7.0 - Production on Wed Apr 7 09:09:54 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

ERROR:
ORA-00257: 归档程序错误。在释放之前仅限于内部连接


Enter user-name: mmsg
Enter password: 
ERROR:
ORA-01034: ORACLE not available
ORA-27101: shared memory realm does not exist
Linux-x86_64 Error: 2: No such file or directory
Process ID: 0
Session ID: 0 Serial number: 0


Enter user-name:
```

## 原因

```shell
00257, 00000, "archiver error. Connect internal only, until freed."
// *Cause:  The archiver process received an error while trying to archive
//       a redo log.  If the problem is not resolved soon, the database
//       will stop executing transactions. The most likely cause of this
//       message is the destination device is out of space to store the
//       redo log file.
// *Action:  Check archiver trace file for a detailed description
//        of the problem. Also verify that the
//       device specified in the initialization parameter
//       ARCHIVE_LOG_DEST is set up properly for archiving.
```

查看数据库日志运行模式，发现是在归档模式下，上述错误码信息显示是out of space to store the redo log file.存储空间不足。

查看文件系统

```shell
oracle@mmsg:~> df
Filesystem           1K-blocks      Used Available Use% Mounted on
/dev/sda2             30969600   3364888  26031548  12% /
udev                   8218880       176   8218704   1% /dev
/dev/sda5             50150072  29613880  17988688  63% /home
/dev/sda6             41286796  39191128         0 100% /opt
opt空间已满！
```

## 解决方法

1、停止数据录和监听，清除oracle目录下相关文件，包括告警、trace日志文件，以及在归档模式下产生的归档日志文件（dbs目录下的.dbf文件）；

2、查看文件系统空间信息

```shell
oracle@mmsg:/opt/oraInventory> df
Filesystem           1K-blocks      Used Available Use% Mounted on
/dev/sda2             30969600   3364888  26031548  12% /
udev                   8218880       176   8218704   1% /dev
/dev/sda5             50150072  29615732  17986836  63% /home
/dev/sda6             41286796  35579632   3609880  91% /opt
```

3、修改数据库日志运行模式，由原来的归档模式修改为非归档模式，并启动数据库。

```shell
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             620759568 bytes
Database Buffers          973078528 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。

SQL> alter database noarchivelog;

数据库已更改。

SQL> alter database open;

数据库已更改。

SQL> archive log list
数据库日志模式             非存档模式
自动存档             禁用
存档终点            /opt/oracle/product/11g/dbs/arch
最早的联机日志序列     626
当前日志序列           628
SQL>
```

