---
layout:     post
title:      "Oracle闪回"
subtitle:   "Oracle flashback"
date:       2012-02-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 特性概述

闪回技术通常用于快速、简单恢复数据库中出现的人为误操作等逻辑错误，即：闪回只对逻辑错误有意义，对数据块损坏和联机日志损坏必须采用介质恢复。

# 闪回类型

从闪回的方式可以将闪回分为：

* 1、基于数据库级别闪回
* 2、表级别闪回
* 3、事务级别闪回

根据闪回对数据的影响程度又可以分为:

* 1、闪回恢复
* 2、闪回查询

闪回恢复将修改数据，闪回点之后的数据将全部丢失。而闪回查询则可以查询数据被DML的不同版本，也可以在此基础之上确定是否进行恢复等。

# 如何启用闪回

## 启用闪回前检查

### 确认是否启用闪回功能

```shell
SQL> select flashback_on from v$database;

FLASHBACK_ON
------------------
NO

SQL>
```

说明：
*  1、flashback_on取值为NO，说明尚未启用闪回功能，取值为YES则表示启用了闪回功能。
*  2、该参数仅能在数据库mount状态下修改。

### 确认当前日志归档模式

```shell
SQL> archive log list
Database log mode              Archive Mode
Automatic archival             Enabled
Archive destination            /opt/oracle/product/11g/dbs/arch
Oldest online log sequence     216
Next log sequence to archive   220
Current log sequence           220
SQL>
```

说明：
* 如果非归档模式下，启用闪回失败：

```shell
SQL> alter database flashback on;
alter database flashback on
*
ERROR at line 1:
ORA-38706: Cannot turn on FLASHBACK DATABASE logging.
ORA-38707: Media recovery is not enabled.

oracle@mmsc101:~> oerr ora 38706
38706, 00000, "Cannot turn on FLASHBACK DATABASE logging."
// *Cause:  An ALTER DATABASE FLASHBACK ON command failed.
//          Other messages in the alert log describe the problem.
// *Action: Fix the problem and retry.
oracle@mmsc101:~> oerr ora 38707
38707, 00000, "Media recovery is not enabled."
// *Cause: An ALTER DATABASE FLASHBACK ON command failed because media
//         recovery was not enabled.
// *Action: Turn on media recovery with an ALTER DATABASE ARCHIVELOG
//          command and then retry the command.
```

### 检查/修改恢复区设置

```shell
SQL> show parameter db_recovery_file_dest

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
db_recovery_file_dest                string
db_recovery_file_dest_size           big integer 0
SQL>
```

说明：
* 上述查询结果展示db_recovery_file_dest取值为空，则表示没有配置闪回区域，启用闪回后需要设置该值，string类型的串。

### 检查/修改闪回时间设置

```shell
SQL> show parameter db_flashback_retention_target

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
db_flashback_retention_target        integer     1440
SQL>
```

说明：
* 1、db_flashback_retention_target单位为分钟，表示能恢复数据的时间长短，默认值为1440（24*60）；
* 2、如果想调整这个参数的取值，可以使用如下语句进行调整：

```
alter system set db_flashback_retention_target=1440;
```

### 检查闪回区域大小

```shell
SQL> show parameter DB_RECOVERY_FILE_DEST_SIZE

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
db_recovery_file_dest_size           big integer 0
```

说明：
* db_recovery_file_dest_size参数单位为G；


## 启用闪回

说明：
下列步骤为在归档模式下，在没有启用闪回功能前提下启用闪回功能的操作步骤，详细信息如下

### 步骤1 手工创建闪回数据存放路径

在/opt/oracle/目录下创建flash_recovery目录。

### 步骤2 修改闪回数据存放路径

```shell
SQL> alter system set db_recovery_file_dest_size  = 2048M scope=both;

System altered.

SQL>
```

### 步骤3 重新启动数据库到Mount状态

```shell
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
Database mounted.
SQL> startup mount  
ORACLE instance started.

Total System Global Area 8284340224 bytes
Fixed Size                  2145944 bytes
Variable Size            6375342440 bytes
Database Buffers         1879048192 bytes
Redo Buffers               27803648 bytes
Database mounted.
SQL>
```

### 步骤4 启动flashback database选项

```shell
SQL> alter system set db_recovery_file_dest='/opt/oracle/flash_recovery' scope=both;

System altered.
SQL> alter database flashback on;

Database altered.

SQL> alter database open;

Database altered.

SQL>
```

### 步骤5 检查闪回进程是否启动

```shell
SQL> ho ps -ef | grep rvwr 
oracle   23486     1  0 17:09 ?        00:00:00 ora_rvwr_sdp
oracle    1634 14984  0 17:26 pts/6    00:00:00 /bin/bash -c ps -ef | grep rvwr
oracle    1636  1634  0 17:26 pts/6    00:00:00 grep rvwr

SQL>
```

# 闪回数据库（flashback database）概述

## flashback database的特性

flashback data1base闪回到过去的某一时刻，闪回点之后的工作全部丢失。使用resetlogs创建新的场景并打开数据库(一旦resetlogs之后，将不能再flashback至resetlogs之前的时间点)。

常用的场景：truncate table、多表发生意外错误等。

## flashback database的组成

闪回缓冲区：当启用flashback database，则sga中会开辟一块新区域作为闪回缓冲区,大小由系统分配；

启用新的rvwr进程:rvwr进程将闪回缓冲区的内容写入到闪回日志中。

## 闪回日志与联机重做日志的区别

闪回日志不同于联机重做日志，闪回日志在联机重做日志基础之上生成，是完整数据块映像的日志。联机日志则是变化的日志。闪回日志不能复用，也不能归档。

闪回日志使用循环写方式,简单的讲，就是：联机日志会记录改变前后的值，而闪回日志只记录改变前的值。

## 闪回数据库的实现机理

buffer cache<-->flashback cache<-->rvwr<-->闪回日志【日志只记录修改前的旧值】

# 闪回database的配置

## 查看闪回数据量、时间等相关信息

下面查看闪回区分配的大小为大约32M，闪回1440分钟以内的数据则需要46M左右的空间

```shell
SQL> select oldest_flashback_scn old_flhbck_scn,oldest_flashback_time old_flhbck_tim,
  2  retention_target rete_trgt,flashback_size/1024/1024 flhbck_siz,
  3  estimated_flashback_size/1024/1024 est_flhbck_size
  4  from v$flashback_database_log;

OLD_FLHBCK_SCN OLD_FLHBCK_TIM       RETE_TRGT FLHBCK_SIZ EST_FLHBCK_SIZE
-------------- ------------------- ---------- ---------- ---------------
       5813199 02/09/2012 17:09:06       1440 32.0078125      46.2890625

SQL>
```

说明：
* 列oldest_flashback_time说明了允许返回的最早的时间点。

## 查看闪回

```shell
SQL> set wrap off
SQL> select * from v$flashback_database_stat;
truncating (as requested) before column ESTIMATED_FLASHBACK_SIZE


BEGIN_TIME          END_TIME            FLASHBACK_DATA    DB_DATA  REDO_DATA
------------------- ------------------- -------------- ---------- ----------
02/09/2012 17:09:06 02/09/2012 17:57:12        1351680    1466368     326144

SQL>
```

## 查看闪回中sga分配的空间大小

```shell
SQL> select * from v$sgastat where name like 'flashback%';

POOL         NAME                            BYTES
------------ -------------------------- ----------
shared pool  flashback generation buff    33554432
shared pool  flashback_marker_cache_si        9200

SQL>
```

## 查看生成的闪回日志

```shell
SQL> ho ls -hlt $ORACLE_BASE/flash_recovery/SDP/flashback
total 33M
-rw-r----- 1 oracle oinstall 33M 2012-02-09 17:59 o1_mf_7m739k3t_.flb

SQL>
```

# 使用flashback闪回数据库实践

前提条件：归档日志可用。

步骤1 关闭数据库

步骤2 启动数据库到mount状态

步骤3 闪回至某个时间点、scn或log sequence number

步骤4 使用resetlogs打开数据库

## 使用sqlplus闪回数据库


### sqlplus几种常用的闪回数据库方法

#### 基于SCN闪回

```shell
FLASHBACK [STANDBY] DATABASE [<database_name>]  TO [BEFORE] SCN <system_change_number>
```

#### 基于时间戳闪回

```shell
FLASHBACK [STANDBY] DATABASE [<database_name>]  TO [BEFORE] TIMESTMP <system_timestamp_value>
```

#### 基于时点闪回

```shell
FLASHBACK [STANDBY] DATABASE [<database_name>]  TO [BEFORE] RESTORE POINT <restore_point_name>
```

如下面的示例：

```shell
SQL> flashback database to timestamp('2010-10-24 13:04:30','yyyy-mm-dd hh24:mi:ss'); 

SQL> flashback database to scn 5813199;

SQL> flashback database ro restore point wyz_test;
```

#### a.基于时间戳闪回

##### 步骤1、 创建测试表，并插入数据

```shell
oracle@mmsc101:~> sqlplus mmsg/mmsg@sdp

SQL*Plus: Release 11.1.0.6.0 - Production on Thu Feb 9 18:14:31 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
SQL> create table scn_test(id int);

Table created.

SQL> insert into scn_test values(1);

1 row created.

SQL> insert into scn_test values(2);

1 row created.

SQL> commit;

Commit complete.

SQL> select count(0) from scn_test;

  COUNT(0)
----------
         2

SQL>
```

说明：
* 上述测试表中有两个记录。

##### 步骤2、获取系统当前时间

```shell
SQL> select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss')  time from dual; 

TIME
---------------------------------------------------------
2012-02-09 18:39:30

SQL>
```

##### 步骤3、删除表scn_test

```shell
SQL> drop table scn_test;

Table dropped.

SQL> commit;

Commit complete.

SQL>
```

##### 步骤4、新创建表tmp

```shell
SQL> create table tmp as select * from modules;

Table created.

SQL> commit;

Commit complete.

SQL>
```

说明：
* 目的是为了验证闪回后这张表不存在。


##### 步骤5、启动数据库到mount状态

```shell
oracle@mmsc101:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on Thu Feb 9 18:24:49 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> shutdown immediate
SQL> startup mount
```

##### 步骤6、dba用户实施闪回

```shell
SQL> flashback database to timestamp to_timestamp('2012-02-09 18:39:30','yyyy-mm-dd hh24:mi:ss');  

Flashback complete.

SQL> alter database open resetlogs;

Database altered.

SQL>
```

##### 步骤7、闪回结果查看

```shell
SQL> connect mmsg/mmsg@sdp
Connected.
SQL> select count(0) from scn_test;

  COUNT(0)
----------
         2

SQL> select * from tmp;
select * from tmp
              *
ERROR at line 1:
ORA-00942: table or view does not exist


SQL>
```

上述查询结果说明表已经闪回恢复，闪回点之后的数据全部丢失。

#### b.基于SCN号闪回

##### 步骤1 获取当前SCN

```shell
SQL> select current_scn from v$database;

CURRENT_SCN
-----------
5815970
```

##### 步骤2 删除mmsg用户下的scn_test表

```shell
SQL> connect mmsg/mmsg@sdp
Connected.
SQL> drop table scn_test;

Table dropped.

SQL> commit;

Commit complete.
```

##### 步骤3 手动执行检查点

```shell
SQL> alter system checkpoint;

System altered.

SQL>
```

##### 步骤4 实施闪回

```shell
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup mount
ORACLE instance started.

Total System Global Area 8284340224 bytes
Fixed Size                  2145944 bytes
Variable Size            6375342440 bytes
Database Buffers         1879048192 bytes
Redo Buffers               27803648 bytes
Database mounted.
SQL> flashback database to scn 5815970;

Flashback complete.

SQL> alter database open resetlogs;

Database altered.

SQL>
```

##### 步骤5 查询闪回结果

```shell
SQL> connect mmsg/mmsg@sdp
Connected.
SQL> select count(0) from scn_test;

  COUNT(0)
----------
         2

SQL>
```

#### c.基于时点闪回

##### 步骤1 创建测试表

```shell
SQL> create table test(id int,describe varchar2(20));

Table created.

SQL> insert into test values(1,'ABC');

1 row created.

SQL> insert into test values(2,'DEF');

1 row created.

SQL> commit;

Commit complete.
SQL> select * from test;

        ID DESCRIBE
---------- --------------------
         1 ABC
         2 DEF

SQL>
```

##### 步骤2 创建闪回点

```shell
oracle@mmsc101:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on Thu Feb 9 18:54:11 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> create restore point wyz_test;

Restore point created.

SQL>
```

##### 步骤3 再次插入记录

```shell
SQL> insert into test values(3,'GHI');

1 row created.

SQL> commit;

Commit complete.

SQL> select * from test;

        ID DESCRIBE
---------- --------------------
         1 ABC
         2 DEF
         3 GHI

SQL>
```

##### 步骤4闪回实施

```shell
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup mount
ORACLE instance started.

Total System Global Area 8284340224 bytes
Fixed Size                  2145944 bytes
Variable Size            6375342440 bytes
Database Buffers         1879048192 bytes
Redo Buffers               27803648 bytes
Database mounted.
SQL> flashback database to restore point wyz_test;

Flashback complete.

SQL> alter database open resetlogs;

Database altered.

SQL>
```

##### 步骤5 查看闪回结果

```shell
SQL> connect mmsg/mmsg@sdp
Connected.
SQL> select * from test;

        ID DESCRIBE
---------- --------------------
         1 ABC
         2 DEF

SQL>
```

说明：
* 闪回点是全局的，不区分用户，即在某个point后，不同用户做了不同的操作，只有闪回到该point后，该point后的不同用户的操作都将丢失。

## 使用RMAN进行flashback database

使用RMAN进行闪回数据库的几种常用办法

```shell
RMAN> flashback database to scn=918987;

RMAN> flashback database to sequence=85  thread=1;
```

### a.基于时间戳闪回

#### 步骤1 创建测试表

```shell
oracle@mmsc101:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on Thu Feb 9 19:02:24 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> create table mmsg.tmp as select * from mmsg.modules;

Table created.

SQL> select count(0) from mmsg.tmp;

  COUNT(0)
----------
        18
```

#### 步骤2 获取数据库当前时间

```shell
SQL> select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') tm from dual;

TM
-------------------
2012-02-09 19:03:14
```

#### 步骤3 删除测试表

```shell
SQL> drop table mmsg.tmp;

Table dropped.

SQL> commit;

Commit complete.
```

#### 步骤4 闪回实践

```shell
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup mount
ORACLE instance started.

Total System Global Area 8284340224 bytes
Fixed Size                  2145944 bytes
Variable Size            6375342440 bytes
Database Buffers         1879048192 bytes
Redo Buffers               27803648 bytes
Database mounted.
SQL>

oracle@mmsc101:~/product/11g/bin> ./rman target/

Recovery Manager: Release 11.1.0.6.0 - Production on Thu Feb 9 19:05:03 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

connected to target database: SDP (DBID=2998391018, not open)

RMAN> flashback database to time="to_date('2012-02-09 19:03:14','yyyy-mm-dd hh24:mi:ss')";

Starting flashback at 02/09/2012 19:05:09
using target database control file instead of recovery catalog
allocated channel: ORA_DISK_1
channel ORA_DISK_1: SID=1086 device type=DISK


starting media recovery
media recovery complete, elapsed time: 00:00:03

Finished flashback at 02/09/2012 19:05:14

RMAN>


oracle@mmsc101:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on Thu Feb 9 19:05:36 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> alter database open resetlogs;

Database altered.
```

#### 步骤5 查看闪回结果

```shell
SQL> select count(0) from mmsg.tmp;

  COUNT(0)
----------
        18

SQL>
```

### b.基于SCN闪回

### c.基于sequence闪回

说明：
* RMAN闪回操作和sqlplus闪回类似，命令可参考sqlplus的操作。


# 闪回表

就是将表里的数据推回到过去的某个时间点，是利用undo表空间里记录的数据被改变前的值，如果闪回表所需要的undo数据，由于保留的时间超过了初始化参数undo_retention所指定的值，从而导致该undo数据块被其他事务覆盖，就不能恢复到指定的时间点了。


闪回表的局限：当前的时间点到要闪回到的时间点之间不允许有ddl操作，否则闪回无法成功。

示例：

```shell
SQL> select count(0) from mmsg.tmp;

  COUNT(0)
----------
        18

SQL> drop table mmsg.tmp;

Table dropped.

SQL> flashback table mmsg.tmp to before drop;

Flashback complete.

SQL> select count(0) from mmsg.tmp;

  COUNT(0)
----------
        18

SQL>
```

说明：
* 闪回表，需要在数据库启用回收站条件下才能进行表的闪回，否则报错：

```shell
SQL> FLASHBACK TABLE mmsg.TEST TO BEFORE DROP;
FLASHBACK TABLE mmsg.TEST TO BEFORE DROP
*
ERROR at line 1:
ORA-38305: object not in RECYCLE BIN
```

# 闪回版本查询

所谓版本指的是每次事务所引起的数据行的变化的情况，每一次变化就是一个版本。闪回版本查询使用的undo表空间里记录的undo数据。

示例：

1、创建测试表，并插入数据

2、查询表中数据总量

3、drop 表中某个记录，查询表中总量

4、查看对应的该表中的闪回版本信息

```shell
select versions_starttime, versions_endtime, versions_xid,
    versions_operation, moduleid
    from modules versions between timestamp minvalue and maxvalue
    order by VERSIONS_STARTTIME
```

说明：
* 其中modules为测试表的表名称。

# 闪回事务查询

闪回事务查询提供的是一个视图，flashback_transaction_query，利用这个视图，可以显示哪些事务引起了数据的变化，并为此提供了撤销事务的SQL语句。

闪回事务查询利用的是undo表空间的undo数据

示例：

1、dba用户登录数据库，查询视图信息；

```select * from flashback_transaction_query where table_owner='MMSG'；```

2、查找对应的闪回事务，确定闪回操作时间点，执行UNDO_SQL字段提供的回滚语句进行闪回操作。

# 闪回查询

查询过去某个时刻表的数据的情况，一旦确认某个时刻的数据满足我们的需求以后，可以根据这个时间执行闪回表。

# 附录

## 查看闪回区使用情况

```shell
SQL> select name,space_limit/1024/1024 sp_limt,space_used/1024/1024 sp_usd,
  2  space_reclaimable/1024/1024 sp_recl,
  3  number_of_files num_fils from v$recovery_file_dest;

NAME
--------------------------------------------------------------------------------
   SP_LIMT     SP_USD    SP_RECL   NUM_FILS
---------- ---------- ---------- ----------
/opt/oracle/flash_recovery
      2048  918.15918          0         12


SQL>
```

## 将某些表空间排除在闪回之外

```shell
SQL> alter tablespace MMSG flashback off;

SQL> select name,flashback_on from v$tablespace where ts#=4;

        NAME            FLA

        --------------- ---

        MMSG           NO
```

说明：
* 如果需要对上述表空间启用闪回功能，则需要在mount模式下对该表空间进行开启该功能。

