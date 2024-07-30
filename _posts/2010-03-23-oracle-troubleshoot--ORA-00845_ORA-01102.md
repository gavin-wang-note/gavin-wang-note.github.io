---
layout:     post
title:      "Oracle案例--错误码之ORA-00845，ORA-01102"
subtitle:   "Oracle error code troubleshoot--ORA-00845，ORA-01102"
date:       2010-03-23
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-00845  和  ORA-01102案例

## 表象

```shell
oracle@mmsg01:/home> sqlplus "/ as sysdba"

SQL*Plus: Release 11.1.0.7.0 - Production on Tue Mar 23 17:55:21 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

Connected to an idle instance.

SQL> startup
ORA-00845: MEMORY_TARGET not supported on this system
SQL> exit
Disconnected
oracle@mmsg01:/home> oerr ora 00845
00845, 00000, "MEMORY_TARGET not supported on this system"
// *Cause: The MEMORY_TARGET parameter was not supported on this operating system or /dev/shm was not sized correctly on Linux.
// *Action: Refer to documentation for a list of supported operating systems. Or, size /dev/shm to be at least the SGA_MAX_SIZE on each Oracle instance running on the system.
oracle@mmsg01:/home> 
```

## 原因

这个问题是由于设置SGA的大小超过了操作系统/dev/shm的大小：

## 解决方法

解决这个问题只有两个方法：

一是修改初始化参数，使得初始化参数中SGA的设置小于/dev/shm的大小；

二是调整/dev/shm的大小。

修改/dev/shm的大小可以通过修改/etc/fstab来实现

```shell
mmsg01:/etc/init.d # df -k /dev/shm
Filesystem           1K-blocks      Used Available Use% Mounted on
shmfs                  4194304         0   4194304   0% /dev/shm                     

vi /etc/fstab
mmsg01:/etc/init.d # vi /etc/fstab

/dev/disk/by-id/scsi-3600508e000000000da19d06c68ac5e0b-part2 /                    reiserfs   acl,user_xattr        1 1
/dev/disk/by-id/scsi-3600508e000000000da19d06c68ac5e0b-part5 /home                reiserfs   acl,user_xattr        1 2
/dev/disk/by-id/scsi-3600508e000000000da19d06c68ac5e0b-part1 swap                 swap       defaults              0 0
proc                 /proc                proc       defaults              0 0
sysfs                /sys                 sysfs      noauto                0 0
debugfs              /sys/kernel/debug    debugfs    noauto                0 0
usbfs                /proc/bus/usb        usbfs      noauto                0 0
devpts               /dev/pts             devpts     mode=0620,gid=5       0 0
shm                  /dev/shm             tmpfs      size=8g               0 0
＃shmfs /dev/shm tmpfs size=4g 0
shmfs /dev/shm tmpfs size=8g 0  #新增加的一行
```

解邦

```shell
umount /dev/shm
```

重新邦定

```shell
mount /dev/shm
```

查看邦定结果

```shell
df -k
mmsg01:/etc/init.d # df
Filesystem           1K-blocks      Used Available Use% Mounted on
/dev/sda2             41944376   4417892  37526484  11% /
udev                   8218880       240   8218640   1% /dev
/dev/sda5             73398648  15426492  57972156  22% /home
shm                    8388608         0   8388608   0% /dev/shm
```

启动数据库

```shell
oracle@mmsg01:~/oradata/mmsgdb> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on Tue Mar 23 20:33:20 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

Connected to an idle instance.

SQL> startup      
ORA-00845: MEMORY_TARGET not supported on this system
SQL> startup
ORA-00845: MEMORY_TARGET not supported on this system
SQL> startup
ORACLE instance started.

Total System Global Area 8417955840 bytes
Fixed Size                  2161312 bytes
Variable Size            4429186400 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27185152 bytes
ORA-01102: cannot mount database in EXCLUSIVE mode


SQL> 
```

出现了另外一个错误：ORA-01102

这个错误主要是lk<SID>文件造成的，该文件位于ORALCE_HOME下的dbs目录下, 这个lk<SID>的主要作用是：

说明DATABASE MOUNT上了,不用再去MOUNT了。 

具体解决ORA-01102问题的步骤：

```shell
oracle@mmsg01:~/product/11g/dbs> /sbin/fuser -u lkMMSGDB
lkMMSGDB:            24500(oracle) 24508(oracle) 24510(oracle) 24514(oracle) 24516(oracle) 24518(oracle) 24520(oracle) 24522(oracle) 24524(oracle) 24526(oracle) 24528(oracle) 24585(oracle) 24589(oracle) 24667(oracle) 24669(oracle) 24693(oracle)
```

发现lkMMSGDB文件没有释放，使用fuser命令kill掉lkMMSGDB

```shell
oracle@mmsg01:~/product/11g/dbs> /sbin/fuser -k lkMMSGDB 
lkMMSGDB:            24500 24508 24510 24514 24516 24518 24520 24522 24524 24526 24528 24585 24589 24667 24669 24693
```

再去检查lkMMSGDB文件是否释放

```shell
oracle@mmsg01:~/product/11g/dbs> /sbin/fuser -u lkMMSGDB
```

不显示任何信息，说明lkMMSGDB文件已经释放

重新启动数据库

```shell
oracle@mmsg01:~/product/11g/dbs> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on Tue Mar 23 20:41:22 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

Connected to an idle instance.

SQL> startup 
ORACLE instance started.

Total System Global Area 8417955840 bytes
Fixed Size                  2161312 bytes
Variable Size            4429186400 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27185152 bytes
Database mounted.
Database opened.
SQL> exit
```

启动成功

