---
layout:     post
title:      "Oracle案例--RMAN常见问题总结"
subtitle:   "Oracle troubleshoot--RMAN"
date:       2011-03-05
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 概述

本文介绍在使用RMAN过程中，碰到的几个RMAN问题并进行记录/总结。

# RMAN命令无反应

## 表象

RMAN命令输入后终端无反应，一直处于等待状态，且长时间如此

```shell
node1:oracle:mmsgdb > rman

```

## 原    因：

操作系统也有一个rman命令，这里执行的是操作系统的rman命令了，而非oracle的RMAN命令。


## 解决方法：

Oracle用户登陆后，修改环境变量，在.bash_profile或者.profile文件中增加如下信息，重新source一下即可：

```shell
export PATH=$ORACLE_HOME:$PATH
```

# RMAN无法进行备份操作/查看备份信息/配置信息


## 表象

```shell
oracle@mmsc103:~> rman target/

恢复管理器: Release 11.1.0.6.0 - Production on 星期六 3月 5 09:27:48 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

连接到目标数据库: MMSGDB (DBID=3148145279)

RMAN> connect catalog rman/rman@mmsgdb

连接到恢复目录数据库

RMAN> list backupset;

RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-03002: list 命令 (在 03/05/2011 09:28:03 上) 失败
RMAN-06004: 恢复目录数据库发生 ORACLE 错误: RMAN-20001: target database not found in recovery catalog

RMAN> backup database;

启动 backup 于 05-3月 -11
RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-03002: backup 命令 (在 03/05/2011 09:28:32 上) 失败
RMAN-03014: 恢复目录的隐式重新同步失败
RMAN-06004: 恢复目录数据库发生 ORACLE 错误: RMAN-20001: 在恢复目录中未找到目标数据库

RMAN> show all;

db_unique_name 为 MMSGDB 的数据库的 RMAN 配置参数为:
RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-03002: show 命令 (在 03/05/2011 09:35:28 上) 失败
RMAN-06004: 恢复目录数据库发生 ORACLE 错误: RMAN-20001: 在恢复目录中未找到目标数据库

RMAN>
```

## 原因

RMAN未注册。

## 解决方法

注册RMAN:

```shell
RMAN> register database;

注册在恢复目录中的数据库
正在启动全部恢复目录的 resync
完成全部 resync

RMAN> 

RMAN> list backupset;


RMAN> show all;

db_unique_name 为 MMSGDB 的数据库的 RMAN 配置参数为:
CONFIGURE RETENTION POLICY TO REDUNDANCY 1; # default
CONFIGURE BACKUP OPTIMIZATION OFF; # default
CONFIGURE DEFAULT DEVICE TYPE TO DISK; # default
CONFIGURE CONTROLFILE AUTOBACKUP OFF; # default
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '%F'; # default
CONFIGURE DEVICE TYPE DISK PARALLELISM 1 BACKUP TYPE TO BACKUPSET; # default
CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE ARCHIVELOG BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE MAXSETSIZE TO UNLIMITED; # default
CONFIGURE ENCRYPTION FOR DATABASE OFF; # default
CONFIGURE ENCRYPTION ALGORITHM 'AES128'; # default
CONFIGURE COMPRESSION ALGORITHM 'BZIP2'; # default
CONFIGURE ARCHIVELOG DELETION POLICY TO NONE; # default
CONFIGURE SNAPSHOT CONTROLFILE NAME TO '/opt/oracle/product/11g/dbs/snapcf_mmsgdb.f'; # default

RMAN>
```

# RMAN备份文件异常删除

## 原因

RMAN备份的文件存放在某个目录下，该文件没有通过rman命令delete删除，而是在操作系统侧执行rm操作，导致再去删除这个备份文件时无法删除掉。

```shell
RMAN-06207: 警告: 由于状态不匹配, 所以不能删除 2 对象 (对于 DISK 通道)。
RMAN-06208: 请用 CROSSCHECK 命令修正状态
RMAN-06210: 不匹配对象的列表
RMAN-06211: ==========================
RMAN-06212: 对象类型   文件名/句柄
RMAN-06213: --------------- ---------------------------------------------------
RMAN-06214: Backup Piece    /opt/oracle/rmanbak/db_u%_s%_p%
RMAN-06214: Backup Piece    /opt/oracle/flash_recovery_area/MMSGDB/autobackup/2011_03_05/o1_mf_s_744975873_6q35d3y8_.bkp
```

## 解决方法

使用crosscheck backupset命令检查后再去执行delete操作。

```shell
RMAN> list backupset by backup summary;


备份列表
===============
关键字     TY LV S 设备类型 完成时间   段数 副本数 压缩标记
------- -- -- - ----------- ---------- ------- ------- ---------- ---
98      B  F  A DISK        05-3月 -11 1       1       NO         FULL_DB_BAK
113     B  F  A DISK        05-3月 -11 1       1       NO         TAG20110305T094433

RMAN> crosscheck backupset;

使用通道 ORA_DISK_1
交叉校验备份片段: 找到为 'EXPIRED'
备份片段句柄=/opt/oracle/rmanbak/db_u%_s%_p% RECID=1 STAMP=744975858
交叉校验备份片段: 找到为 'EXPIRED'
备份片段句柄=/opt/oracle/flash_recovery_area/MMSGDB/autobackup/2011_03_05/o1_mf_s_744975873_6q35d3y8_.bkp RECID=2 STAMP=744975875
已交叉检验的 2 对象


RMAN> delete backupset;

使用通道 ORA_DISK_1

备份片段列表
BP 关键字  BS 关键字  Pc# Cp# 状态      设备类型段名称
------- ------- --- --- ----------- ----------- ----------
99      98      1   1   EXPIRED     DISK        /opt/oracle/rmanbak/db_u%_s%_p%
120     113     1   1   EXPIRED     DISK        /opt/oracle/flash_recovery_area/MMSGDB/autobackup/2011_03_05/o1_mf_s_744975873_6q35d3y8_.bkp

是否确定要删除以上对象 (输入 YES 或 NO)? YES
已删除备份片段
备份片段句柄=/opt/oracle/rmanbak/db_u%_s%_p% RECID=1 STAMP=744975858
已删除备份片段
备份片段句柄=/opt/oracle/flash_recovery_area/MMSGDB/autobackup/2011_03_05/o1_mf_s_744975873_6q35d3y8_.bkp RECID=2 STAMP=744975875
2 对象已删除


RMAN> list backupset by backup summary;


RMAN>     #无数据展示，说明已经删除完毕了.
```

# 执行RMAN备份报错，RMAN-03009  ORA-19809  ORA-19804

## 表象

```shell
oracle@mmsc103:~/rmanbak> rman target/

恢复管理器: Release 11.1.0.6.0 - Production on 星期三 3月 16 17:57:10 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

连接到目标数据库: MMSGDB (DBID=3148145279)

RMAN> connect catalog rman/rman@mmsgdb

连接到恢复目录数据库

RMAN> list backupset;


RMAN> backup database;

启动 backup 于 16-3月 -11
分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=294 设备类型=DISK
通道 ORA_DISK_1: 正在启动全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00005 名称=/opt/oracle/oradata/mmsgdb/mmsgdata01
输入数据文件: 文件号=00007 名称=/opt/oracle/oradata/mmsgdb/mmsg_yjh
输入数据文件: 文件号=00002 名称=/opt/oracle/oradata/mmsgdb/sysaux01.dbf
输入数据文件: 文件号=00001 名称=/opt/oracle/oradata/mmsgdb/system01.dbf
输入数据文件: 文件号=00003 名称=/opt/oracle/oradata/mmsgdb/undotbs01.dbf
输入数据文件: 文件号=00006 名称=/opt/oracle/oradata/mmsgdb/rman_data.dbf
输入数据文件: 文件号=00004 名称=/opt/oracle/oradata/mmsgdb/users01.dbf
通道 ORA_DISK_1: 正在启动段 1 于 16-3月 -11
DBGANY:     Mismatched message length! [17:57:48.295] (krmiduem)
DBGANY:     Mismatched message length! [17:57:48.296] (krmiduem)
MAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-00600: internal error, arguments [3045] [] [] [] []
RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-03009: backup 命令 (ORA_DISK_1 通道上, 在 03/16/2011 17:57:48 上) 失败
ORA-19809: 超出了恢复文件数的限制
ORA-19804: 无法回收 52428800 字节磁盘空间 (从 2147483648 限制中)
oracle@mmsc103:~/rmanbak>
```

## 原因

开通了闪回功能后，默认的备份存储区域为闪存区域，区域大小默认为2G。

```shell
SQL> show parameter db_recovery_file_dest_size 

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
db_recovery_file_dest_size           big integer 42G
SQL>
```

当归档日志文件数量总和的大小超过这个默认值后，执行备份则报错，原因就是空间不足。

## 解决方法

通过修改闪回区域大小，重启数据库后解决问题。

```shell
SQL> alter system set db_recovery_file_dest_size = 4G scope =spfile;

系统已更改。

SQL>shutdown immediate
SQL>startup
```

