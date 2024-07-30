---
layout:     post
title:      "Oracle案例--oracle本地磁盘数据文件更改到lv上"
subtitle:   "Oracle troubleshoot--Change local data files to LV"
date:       2011-08-31
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# oracle本地磁盘数据文件更改到lv上

## 背景

oracle数据库的所有数据文件安装在本地系统盘，现要将所有本地系统盘上的数据文件转移到外挂磁阵lv上。

## 实现过程

说明：
* 这里仅以一个本地永久数据文件转移到lv上为示例。

### 步骤一、创建测试表空间

#### 本地数据文件

```shell
SQL> create tablespace wyztest datafile '/opt/oracle/oradata/mmsgdb/wyztest.dbf' size 50M;   

表空间已创建。
```

### 步骤二、创建用户表，并插入数据记录

#### 创建用户并授权

```shell
SQL> create user test identified by test  
  2  default tablespace wyztest 
  3  profile default;

用户已创建。

SQL> grant create table to test;

授权成功。

SQL> grant create session to test;

授权成功。

SQL> grant resource to test; 

授权成功。

SQL> grant unlimited tablespace to test;

授权成功。

SQL> commit;

提交完成。

SQL> exit
```

从 Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production With the Partitioning, OLAP, Data Mining and Real Application Testing options 断开

#### 创建用户表，并插入两条记录

```shell
oracle@mmsc103:~> sqlplus test/test@mmsgdb

SQL*Plus: Release 11.1.0.6.0 - Production on 星期三 8月 31 12:11:17 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> show user
USER 为 "TEST"
SQL> create table modules (id integer not null);

表已创建。

SQL> insert into modules values(1);

已创建 1 行。

SQL> insert into modules values(2);

已创建 1 行。

SQL> commit;

提交完成。

SQL> select * from modules;        #表中数据有两条记录，用于迁移后检查数据是否有丢失

        ID
----------
         1
         2

SQL> exit
```

### 步骤三、创建lv，修改lv属主为oracle

#### 创建lv

```shell
mmsc103:/opt/oracle # lvcreate -L 290M -n oratest vg_dlsc_uoa
  Rounding up size to full physical extent 292.00 MB
  Logical volume "oratest" created
```

#### 修改lv属主信息

```shell
mmsc103:/opt/oracle # cd /dev
mmsc103:/dev # chown -R oracle.oinstall vg_dlsc_uoa
mmsc103:/dev # chown -R oracle.oinstall vg_dlsc_uoa/*
mmsc103:/dev/vg_dlsc_uoa # ls -l
total 0
lrwxrwxrwx 1 oracle oinstall 35 Aug 31 11:41 lv_dlsc_uoa -> /dev/mapper/vg_dlsc_uoa-lv_dlsc_uoa
lrwxrwxrwx 1 oracle oinstall 31 Aug 31 12:16 oratest -> /dev/mapper/vg_dlsc_uoa-oratest
mmsc103:~ # cd /dev/mapper/
mmsc103:/dev/mapper # ls -l
total 0
lrwxrwxrwx 1 root root     16 Aug 31  2011 control -> ../device-mapper
brw------- 1 root root 253, 0 Aug 31 11:41 vg_dlsc_uoa-lv_dlsc_uoa
brw------- 1 root root 253, 1 Aug 31 12:16 vg_dlsc_uoa-oratest
mmsc103:/dev/mapper # chown -R oracle.oinstall vg_dlsc_uoa-oratest
mmsc103:/dev/mapper # 
```

说明：
* 父目录、目录下文件以及mapper文件的属主都要修改，否则rman操作会报权限不足（Permission denied）


### 步骤四、mount状态下拷贝本地文件到lv上

#### 关闭数据库

```shell
SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
```

#### 启动数据库到mount状态

```shell
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2144824 bytes
Variable Size            1124074952 bytes
Database Buffers          469762048 bytes
Redo Buffers                7430144 bytes
数据库装载完毕。
SQL> exit
```

从 Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production With the Partitioning, OLAP, Data Mining and Real Application Testing options 断开

#### 复制本地数据文件到lv上

```shell
oracle@mmsc103:~> rman target/

恢复管理器: Release 11.1.0.6.0 - Production on 星期三 8月 31 11:45:14 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

已连接到目标数据库: MMSGDB (DBID=3157020426, 未打开)

RMAN> copy datafile '/opt/oracle/oradata/mmsgdb/wyztest.dbf' to '/dev/vg_dlsc_uoa/oratest';

启动 backup 于 31-8月 -11
使用目标数据库控制文件替代恢复目录
分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=316 设备类型=DISK
通道 ORA_DISK_1: 启动数据文件副本
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/wyztest.dbf
输出文件名=/dev/vg_dlsc_uoa/oratest 标记=TAG20110831T115029 RECID=1 STAMP=760621832
通道 ORA_DISK_1: 数据文件复制完毕, 经过时间: 00:00:01
完成 backup 于 31-8月 -11

RMAN> quit
```

### 步骤五、修改控制文件并open数据库

```shell
oracle@mmsc103:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期三 8月 31 11:50:50 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> alter database rename file '/opt/oracle/oradata/mmsgdb/wyztest.dbf' to '/dev/vg_dlsc_uoa/oratest';     

数据库已更改。

SQL> alter database open;

数据库已更改。
```

### 步骤六、查看迁移结果

```shell
SQL> select FILE_NAME from dba_data_files where TABLESPACE_NAME ='WYZTEST';

FILE_NAME
--------------------------------------------------------------------------------
/dev/vg_dlsc_uoa/oratest     #路径已经不是本地路径（/opt/oracle/oradata/mmsgdb）了

SQL> quit 
从 Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options 断开
```

#### 查看前后后表中数据记录

```shell
oracle@mmsc103:~> sqlplus test/test@mmsgdb

SQL*Plus: Release 11.1.0.6.0 - Production on 星期三 8月 31 12:21:50 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> select * from modules;

        ID
----------
         1
         2

SQL> 
```

此时看到，两条记录，数据都在。


### 步骤七、环境清理（可选）

可以删除本地路径下的原迁移前的数据文件，可选操作。

## 附录

### 变更永久数据文件位置步骤

1、db处于mount状态；

2、mv或者cp操作，将文件拷贝到指定位置；

3、修改控制文件：alter database rename file ‘xxxx’ to ‘xxxxxxx’;

说明：

* 永久数据文件包括：

```shell
select file_name from dba_data_files;
system01.dbf 
sysaux01.dbf 
undotbs01.dbf
users01.dbf

select member from v$logfile;
redo01.log
redo02.log
redo03.log
```

### 变更临时文件位置

由于临时文件不存放数据，可以将原先临时文件drop掉，并重新创建在lv上既可。

```shell
select file_name from dba_temp_files;
temp01.dbf
```

### 变更控制文件位置

```shell
select * from v$controlfile;
control01.ctl
control02.ctl
control03.ctl
```

由于控制文件比较特殊，并没有想到好方法，思路如下：

1、在lv上新增控制文件（建议数量为3个）；

2、创建pfile文件，修改控制文件路径信息为lv上的控制文件；

3、使用pfile创建spfile，并启动数据库

说明：
* oracle自11gR2版本开始，控制文件数默认不再是三个，而是两个。

