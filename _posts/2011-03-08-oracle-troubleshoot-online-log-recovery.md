---
layout:     post
title:      "Oracle案例--联机日志损坏"
subtitle:   "Oracle troubleshoot--online log recovery"
date:       2011-03-08
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 损坏非当前联机日志

## 步骤一  启动数据库，报错：ORA-00313和ORA-00312

```
SQL> startup
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
ORA-00313: 无法打开日志组 3 (用于线程 1) 的成员
ORA-00312: 联机日志 3 线程 1: '/opt/oracle/oradata/mmsgdb/redo03.log'
```

## 步骤二  查看v$log视图

```
SQL> select group#,sequence#,archived,status from v$log;

    GROUP#  SEQUENCE# ARC STATUS
---------- ---------- --- ----------------
         1          1 NO  CURRENT
         3          0 YES UNUSED
         2          0 YES UNUSED

SQL>
```

上述结果显示，联机日志3不是当前日志，且已经归档。

## 步骤三   用CLEAR命令重建该日志文件

```
SQL> alter database clear logfile group 3;

数据库已更改。

如果是该日志组还没有归档，则需要用
SQL>alter database clear unarchived logfile group 3;
```

## 步骤四   打开数据库，并备份数据库

```
SQL> alter database open;

数据库已更改。

SQL>
```

说明：
* 1、如果损坏的是非当前的联机日志文件，一般只需要clear就可以重建该日志文件，但是如果该数据库处于归档状态但该日志还没有归档，就需要强行clear。
* 2、建议clear，特别是强行clear后作一次数据库的全备份。
* 3、此方法适用于归档与非归档数据库.

# 损坏当前联机日志

归档模式下日志损坏有两种情况，

## 一、数据库正常关闭，日志文件中没有未决的事务需要实例恢复，

当前日志组的损坏，可以直接使用alter database clear unarchived logfile group N;命令来重建，步骤如下：

```
oracle@mmsc103:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期二 3月 8 17:46:33 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> exit
从 Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options 断开
oracle@mmsc103:~> cd oradata/mmsgdb/
oracle@mmsc103:~/oradata/mmsgdb> rm -rf redo02.log 
oracle@mmsc103:~/oradata/mmsgdb> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期二 3月 8 17:47:14 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

已连接到空闲例程。

SQL> startup
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
ORA-00313: 无法打开日志组 2 (用于线程 1) 的成员
ORA-00312: 联机日志 2 线程 1: '/opt/oracle/oradata/mmsgdb/redo02.log'


SQL> alter database clear unarchived logfile group 2;

数据库已更改。

SQL> alter database open;

数据库已更改。

SQL>
```

## 二、日志组中有活动事务，需要介质恢复，

日志组需要用来数据同步，有两种解决方法：

1、通过不完全恢复，保持数据库数据一致性，这种方法要求数据库运行在归档方式下，且有可用的数据文件的备份；

### 步骤一  模拟当前日志组中日志文件损坏

```
SQL> set wrap off
SQL> set linesize 200
SQL> select * from v$log;

    GROUP#    THREAD#  SEQUENCE#      BYTES    MEMBERS ARC STATUS           FIRST_CHANGE# FIRST_TIME
---------- ---------- ---------- ---------- ---------- --- ---------------- ------------- --------------
         1          1          4   52428800          1 YES INACTIVE                754910 08-3月 -11
         2          1          0   52428800          1 YES UNUSED                  776870 08-3月 -11
         3          1          6   52428800          1 NO  CURRENT                 798385 08-3月 -11

SQL> host          
oracle@mmsc103:~/oradata/mmsgdb> rm -rf redo03.log 
oracle@mmsc103:~/oradata/mmsgdb> exit
exit
```

### 步骤二  启动数据库，报错

```
SQL> startup force
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
ORA-00313: 无法打开日志组 3 (用于线程 1) 的成员
ORA-00312: 联机日志 3 线程 1: '/opt/oracle/oradata/mmsgdb/redo03.log'
ORA-27037: 无法获得文件状态
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3


SQL> select * from v$log;

    GROUP#    THREAD#  SEQUENCE#      BYTES    MEMBERS ARC STATUS           FIRST_CHANGE# FIRST_TIME
---------- ---------- ---------- ---------- ---------- --- ---------------- ------------- --------------
         1          1          4   52428800          1 YES INACTIVE                754910 08-3月 -11
         3          1          6   52428800          1 NO  CURRENT                 798385 08-3月 -11
         2          1          0   52428800          1 YES UNUSED                  776870 08-3月 -11

SQL>
```

### 步骤三  clear不成功

```
SQL> alter database clear unarchived logfile group 3;
alter database clear unarchived logfile group 3
*
第 1 行出现错误:
ORA-01624: 日志 3 是紧急恢复实例 mmsgdb (线程 1) 所必需的
ORA-00312: 联机日志 3 线程 1: '/opt/oracle/oradata/mmsgdb/redo03.log'


SQL>
```

### 步骤四  拷贝有效的备份，进行不完全恢复

文件拷贝

```
oracle@mmsc103:~> cd bak_20110307/mmsgdb/
oracle@mmsc103:~/bak_20110307/mmsgdb> l
total 2256564
drwxr-x--- 2 oracle oinstall       4096 2011-03-07 15:47 ./
drwxr-x--- 3 oracle oinstall       4096 2011-03-07 15:46 ../
-rw-r----- 1 oracle oinstall    9912320 2011-03-07 15:46 control01.ctl
-rw-r----- 1 oracle oinstall    9912320 2011-03-07 15:46 control02.ctl
-rw-r----- 1 oracle oinstall    9912320 2011-03-07 15:46 control03.ctl
-rw-r----- 1 oracle oinstall 1048584192 2011-03-07 15:47 mmsgdata01
-rw-r----- 1 oracle oinstall  524296192 2011-03-07 15:47 mmsgdata02
-rw-r----- 1 oracle oinstall   52429312 2011-03-07 15:47 redo01.log
-rw-r----- 1 oracle oinstall   52429312 2011-03-07 15:47 redo02.log
-rw-r----- 1 oracle oinstall   52429312 2011-03-07 15:47 redo03.log
-rw-r----- 1 oracle oinstall  209723392 2011-03-07 15:47 rman_data.dbf
-rw-r----- 1 oracle oinstall   20979712 2011-03-07 15:47 rman_tmp.dbf
-rw-r----- 1 oracle oinstall  288235520 2011-03-07 15:47 sysaux01.dbf
-rw-r----- 1 oracle oinstall  356524032 2011-03-07 15:47 system01.dbf
-rw-r----- 1 oracle oinstall   20979712 2011-03-07 15:47 temp01.dbf
-rw-r----- 1 oracle oinstall  209723392 2011-03-07 15:47 undotbs01.dbf
-rw-r----- 1 oracle oinstall    5251072 2011-03-07 15:47 users01.dbf
oracle@mmsc103:~/bak_20110307/mmsgdb> cp * ../../oradata/mmsgdb/

不完全恢复
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
SQL> recover database until cancel;
完成介质恢复。
SQL> alter database open resetlogs;

数据库已更改。

SQL>
```

注意：
* 这个时候是不能用RMAN进行恢复的，否则报错：

```
ORA-00283: 恢复会话因错误而取消
ORA-00313: 无法打开日志组 3 (用于线程 1) 的成员
ORA-00312: 联机日志 3 线程 1: '/opt/oracle/oradata/mmsgdb/redo03.log'
ORA-27037: 无法获得文件状态
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3
```

说明：
* 1、这种办法恢复的数据库是一致的不完全恢复，会丢失当前联机日志中的事务数据
* 2、这种方法适合于归档数据库并且有可用的数据库全备份。
* 3、恢复成功之后，记得再做一次数据库的全备份。
* 4、建议联机日志文件一定要实现镜相在不同的磁盘上，避免这种情况的发生，因为任何数据的丢失对于生产来说都是不容许的。

2、通过强制性恢复，这种方法会导致数据的不一致性，推荐使用方法一。

### 步骤一 模拟当前日志组中日志成员被损坏

```
SQL> set wrap off
SQL> set linesize 200
SQL> select * from v$log;

    GROUP#    THREAD#  SEQUENCE#      BYTES    MEMBERS ARC STATUS           FIRST_CHANGE# FIRST_TIME
---------- ---------- ---------- ---------- ---------- --- ---------------- ------------- --------------
         1          1          1   52428800          1 NO  CURRENT                 688817 08-3月 -11
         2          1          0   52428800          1 YES UNUSED                       0
         3          1          0   52428800          1 YES UNUSED                       0

SQL> host
oracle@mmsc103:~/oradata/mmsgdb> rm -rf redo01.log 
oracle@mmsc103:~/oradata/mmsgdb> exit
exit

SQL> startup force
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
ORA-00313: 无法打开日志组 1 (用于线程 1) 的成员
ORA-00312: 联机日志 1 线程 1: '/opt/oracle/oradata/mmsgdb/redo01.log'
ORA-27037: 无法获得文件状态
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3

SQL>
```

### 步骤二  修改pfile文件，增加隐性参数

```
vi /opt/oracle/admin/mmsgdb/pfile/init.ora.232011183420
#add for test by wangyunzeng
_allow_resetlogs_corruption=TRUE
```

### 步骤三  通过pfile文件启动数据库

```
SQL> startup force pfile='/opt/oracle/admin/mmsgdb/pfile/init.ora.232011183420' 
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
ORA-00313: 无法打开日志组 1 (用于线程 1) 的成员
ORA-00312: 联机日志 1 线程 1: '/opt/oracle/oradata/mmsgdb/redo01.log'
ORA-27037: 无法获得文件状态
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3
```

### 步骤四  进行介质恢复

```
SQL> recover database until cancel;
ORA-00279: 更改 688820 (在 03/08/2011 18:14:25 生成) 对于线程 1 是必需的
ORA-00289: 建议: /opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_08/o1_mf_1_1_%u_.arc
ORA-00280: 更改 688820 (用于线程 1) 在序列 #1 中


指定日志: {<RET>=suggested | filename | AUTO | CANCEL}
cancel
ORA-01547: 警告: RECOVER 成功但 OPEN RESETLOGS 将出现如下错误
ORA-01194: 文件 1 需要更多的恢复来保持一致性
ORA-01110: 数据文件 1: '/opt/oracle/oradata/mmsgdb/system01.dbf'


ORA-01112: 未启动介质恢复


SQL> alter database open resetlogs;

数据库已更改。

SQL>
```

### 步骤五   关闭数据库，去掉pfile文件中隐性参数，重启数据库

```
SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
数据库已经打开。
SQL> select * from v$log;

    GROUP#    THREAD#  SEQUENCE#      BYTES    MEMBERS ARC STATUS           FIRST_CHANGE# FIRST_TIME
---------- ---------- ---------- ---------- ---------- --- ---------------- ------------- --------------
         1          1          1   52428800          1 NO  CURRENT                 688821 08-3月 -11
         2          1          0   52428800          1 YES UNUSED                       0
         3          1          0   52428800          1 YES UNUSED                       0

SQL> show parameter spfile

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
spfile                               string      /opt/oracle/product/11g/dbs/sp
SQL>
```

这里使用的是spfile文件，所以不需要修改pfile文件也可以，只有重启数据库就行。

### 步骤六 备份整个数据库

物理冷备或者物理热备或者RMAN备份都行。

### 步骤七  导入数据

如果有相关的exp导出的数据，可以执行imp导入操作，毕竟数据发生丢失。

### 步骤八  表数据分析

建议执行一下表分析

```
SQL> ANALYZE TABLE time VALIDATE STRUCTURE CASCADE;

表已分析。
```

说明：
* 1、该恢复方法是没有办法之后的恢复方法，一般情况下建议不要采用，因为该方法可能导致数据库的不一致
* 2、该方法也丢失数据，但是丢失的数据没有上一种方法的数据多，主要是未写入数据文件的已提交或未提交数据。
* 3、建议成功后严格执行以上的6到8步，完成数据库的检查与分析
* 4、全部完成后做一次数据库的全备份
* 5、建议联机日志文件一定要实现镜相在不同的磁盘上，避免这种情况的发生，因为任何数据的丢失对于生产来说都是不容许的

