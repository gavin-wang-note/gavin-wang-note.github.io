---
layout:     post
title:      "Oracle导入导出之数据泵(expdp/impdp)"
subtitle:   "Oracle data pump(expdp/impdp)"
date:       2010-09-22
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 概述

数据泵（data pump）是oracle 10g新增的功能。

工具EXPDP将数据库对象的元数据（对象结构）或数据导出到转储文件中；而数据泵导入则是使用工具IMPDP将转储文件中的元数据及其数据导入到Oracle数据库中。

EXPDP可以导出表、导出用户模式、表空间和全数据库4种方式；相应的，impdp可以导入表、导出用户模式、表空间和全数据库。

expdp和impdp的使用，类似与exp和dmp 

```
expdp help=y
impdp help=y
```
 
```
oracle@GW_8:~> expdp help=y

Export: Release 11.1.0.7.0 - 64bit Production on 星期五, 01 2月, 2013 9:31:19

Copyright (c) 2003, 2007, Oracle.  All rights reserved.


数据泵导出实用程序提供了一种用于在 Oracle 数据库之间传输
数据对象的机制。该实用程序可以使用以下命令进行调用:

   示例: expdp scott/tiger DIRECTORY=dmpdir DUMPFILE=scott.dmp

您可以控制导出的运行方式。具体方法是: 在 'expdp' 命令后输入 
各种参数。要指定各参数, 请使用关键字:

   格式:  expdp KEYWORD=value 或 KEYWORD=(value1,value2,...,valueN)
   示例: expdp scott/tiger DUMPFILE=scott.dmp DIRECTORY=dmpdir SCHEMAS=scott
               或 TABLES=(T1:P1,T1:P2), 如果 T1 是分区表

USERID 必须是命令行中的第一个参数。

关键字               说明 (默认)
------------------------------------------------------------------------------
ATTACH                连接到现有作业, 例如 ATTACH [=作业名]。
COMPRESSION           减小转储文件内容的大小, 其中有效关键字
                      值为: ALL, (METADATA_ONLY), DATA_ONLY 和 NONE。
CONTENT               指定要卸载的数据, 其中有效关键字
                      值为: (ALL), DATA_ONLY 和 METADATA_ONLY。
DATA_OPTIONS          数据层标记, 其中唯一有效的值为:
                      使用 CLOB 格式的 XML_CLOBS-write XML 数据类型
DIRECTORY             供转储文件和日志文件使用的目录对象。
DUMPFILE              目标转储文件 (expdat.dmp) 的列表,
                      例如 DUMPFILE=scott1.dmp, scott2.dmp, dmpdir:scott3.dmp。
ENCRYPTION            加密部分或全部转储文件, 其中有效关键字
                      值为: ALL, DATA_ONLY, METADATA_ONLY,
                      ENCRYPTED_COLUMNS_ONLY 或 NONE。
ENCRYPTION_ALGORITHM  指定应如何完成加密, 其中有效
                      关键字值为: (AES128), AES192 和 AES256。
ENCRYPTION_MODE       生成加密密钥的方法, 其中有效关键字
                      值为: DUAL, PASSWORD 和 (TRANSPARENT)。
ENCRYPTION_PASSWORD   用于创建加密列数据的口令关键字。
ESTIMATE              计算作业估计值, 其中有效关键字
                      值为: (BLOCKS) 和 STATISTICS。
ESTIMATE_ONLY         在不执行导出的情况下计算作业估计值。
EXCLUDE               排除特定的对象类型, 例如 EXCLUDE=TABLE:EMP。
FILESIZE              以字节为单位指定每个转储文件的大小。
FLASHBACK_SCN         用于将会话快照设置回以前状态的 SCN。
FLASHBACK_TIME        用于获取最接近指定时间的 SCN 的时间。
FULL                  导出整个数据库 (N)。
HELP                  显示帮助消息 (N)。
INCLUDE               包括特定的对象类型, 例如 INCLUDE=TABLE_DATA。
JOB_NAME              要创建的导出作业的名称。
LOGFILE               日志文件名 (export.log)。
NETWORK_LINK          链接到源系统的远程数据库的名称。
NOLOGFILE             不写入日志文件 (N)。
PARALLEL              更改当前作业的活动 worker 的数目。
PARFILE               指定参数文件。
QUERY                 用于导出表的子集的谓词子句。
REMAP_DATA            指定数据转换函数,
                      例如 REMAP_DATA=EMP.EMPNO:REMAPPKG.EMPNO。
REUSE_DUMPFILES       覆盖目标转储文件 (如果文件存在) (N)。
SAMPLE                要导出的数据的百分比; 
SCHEMAS               要导出的方案的列表 (登录方案)。
STATUS                在默认值 (0) 将显示可用时的新状态的情况下,
                      要监视的频率 (以秒计) 作业状态。
TABLES                标识要导出的表的列表 - 只有一个方案。
TABLESPACES           标识要导出的表空间的列表。
TRANSPORTABLE         指定是否可以使用可传输方法, 其中
                      有效关键字值为: ALWAYS, (NEVER)。
TRANSPORT_FULL_CHECK  验证所有表的存储段 (N)。
TRANSPORT_TABLESPACES 要从中卸载元数据的表空间的列表。
VERSION               要导出的对象的版本, 其中有效关键字为:
                      (COMPATIBLE), LATEST 或任何有效的数据库版本。

下列命令在交互模式下有效。
注: 允许使用缩写

命令               说明
------------------------------------------------------------------------------
ADD_FILE              向转储文件集中添加转储文件。
CONTINUE_CLIENT       返回到记录模式。如果处于空闲状态, 将重新启动作业。
EXIT_CLIENT           退出客户机会话并使作业处于运行状态。
FILESIZE              后续 ADD_FILE 命令的默认文件大小 (字节)。
HELP                  总结交互命令。
KILL_JOB              分离和删除作业。
PARALLEL              更改当前作业的活动 worker 的数目。
                      PARALLEL=<worker 的数目>。
REUSE_DUMPFILES       覆盖目标转储文件 (如果文件存在) (N)。
START_JOB             启动/恢复当前作业。
STATUS                在默认值 (0) 将显示可用时的新状态的情况下,
                      要监视的频率 (以秒计) 作业状态。
                      STATUS[=interval]
STOP_JOB              顺序关闭执行的作业并退出客户机。
                      STOP_JOB=IMMEDIATE 将立即关闭
                      数据泵作业。
```

```
oracle@GW_8:~> impdp help=y

Import: Release 11.1.0.7.0 - 64bit Production on 星期五, 01 2月, 2013 10:52:27

Copyright (c) 2003, 2007, Oracle.  All rights reserved.


数据泵导入实用程序提供了一种用于在 Oracle 数据库之间传输
数据对象的机制。该实用程序可以使用以下命令进行调用:

     示例: impdp scott/tiger DIRECTORY=dmpdir DUMPFILE=scott.dmp

您可以控制导入的运行方式。具体方法是: 在 'impdp' 命令后输入
各种参数。要指定各参数, 请使用关键字:

     格式:  impdp KEYWORD=value 或 KEYWORD=(value1,value2,...,valueN)
     示例: impdp scott/tiger DIRECTORY=dmpdir DUMPFILE=scott.dmp

USERID 必须是命令行中的第一个参数。

关键字               说明 (默认)
------------------------------------------------------------------------------
ATTACH                连接到现有作业, 例如 ATTACH [=作业名]。
CONTENT               指定要加载的数据, 其中有效关键字为:
                      (ALL), DATA_ONLY 和 METADATA_ONLY。
DATA_OPTIONS          数据层标记, 其中唯一有效的值为:
                      SKIP_CONSTRAINT_ERRORS - 约束条件错误不严重。
DIRECTORY             供转储文件, 日志文件和 sql 文件使用的目录对象。
DUMPFILE              要从 (expdat.dmp) 中导入的转储文件的列表,
                      例如 DUMPFILE=scott1.dmp, scott2.dmp, dmpdir:scott3.dmp。
ENCRYPTION_PASSWORD   用于访问加密列数据的口令关键字。
                      此参数对网络导入作业无效。
ESTIMATE              计算作业估计值, 其中有效关键字为:
                      (BLOCKS) 和 STATISTICS。
EXCLUDE               排除特定的对象类型, 例如 EXCLUDE=TABLE:EMP。
FLASHBACK_SCN         用于将会话快照设置回以前状态的 SCN。
FLASHBACK_TIME        用于获取最接近指定时间的 SCN 的时间。
FULL                  从源导入全部对象 (Y)。
HELP                  显示帮助消息 (N)。
INCLUDE               包括特定的对象类型, 例如 INCLUDE=TABLE_DATA。
JOB_NAME              要创建的导入作业的名称。
LOGFILE               日志文件名 (import.log)。
NETWORK_LINK          链接到源系统的远程数据库的名称。
NOLOGFILE             不写入日志文件。
PARALLEL              更改当前作业的活动 worker 的数目。
PARFILE               指定参数文件。
PARTITION_OPTIONS     指定应如何转换分区, 其中
                      有效关键字为: DEPARTITION, MERGE 和 (NONE)
QUERY                 用于导入表的子集的谓词子句。
REMAP_DATA            指定数据转换函数,
                      例如 REMAP_DATA=EMP.EMPNO:REMAPPKG.EMPNO
REMAP_DATAFILE        在所有 DDL 语句中重新定义数据文件引用。
REMAP_SCHEMA          将一个方案中的对象加载到另一个方案。
REMAP_TABLE           表名重新映射到另一个表,
                      例如 REMAP_TABLE=EMP.EMPNO:REMAPPKG.EMPNO。
REMAP_TABLESPACE      将表空间对象重新映射到另一个表空间。
REUSE_DATAFILES       如果表空间已存在, 则将其初始化 (N)。
SCHEMAS               要导入的方案的列表。
SKIP_UNUSABLE_INDEXES 跳过设置为无用索引状态的索引。
SQLFILE               将所有的 SQL DDL 写入指定的文件。
STATUS                在默认值 (0) 将显示可用时的新状态的情况下,
                      要监视的频率 (以秒计) 作业状态。
STREAMS_CONFIGURATION 启用流元数据的加载
TABLE_EXISTS_ACTION   导入对象已存在时执行的操作。
                      有效关键字: (SKIP), APPEND, REPLACE 和 TRUNCATE。
TABLES                标识要导入的表的列表。
TABLESPACES           标识要导入的表空间的列表。
TRANSFORM             要应用于适用对象的元数据转换。
                      有效转换关键字为: SEGMENT_ATTRIBUTES, STORAGE,
                      OID 和 PCTSPACE。
TRANSPORTABLE         用于选择可传输数据移动的选项。
                      有效关键字为: ALWAYS 和 (NEVER)。
                      仅在 NETWORK_LINK 模式导入操作中有效。
TRANSPORT_DATAFILES   按可传输模式导入的数据文件的列表。
TRANSPORT_FULL_CHECK  验证所有表的存储段 (N)。
TRANSPORT_TABLESPACES 要从中加载元数据的表空间的列表。
                      仅在 NETWORK_LINK 模式导入操作中有效。
VERSION               要导出的对象的版本, 其中有效关键字为:
                      (COMPATIBLE), LATEST 或任何有效的数据库版本。
                      仅对 NETWORK_LINK 和 SQLFILE 有效。

下列命令在交互模式下有效。
注: 允许使用缩写

命令               说明 (默认)
------------------------------------------------------------------------------
CONTINUE_CLIENT       返回到记录模式。如果处于空闲状态, 将重新启动作业。
EXIT_CLIENT           退出客户机会话并使作业处于运行状态。
HELP                  总结交互命令。
KILL_JOB              分离和删除作业。
PARALLEL              更改当前作业的活动 worker 的数目。
                      PARALLEL=<worker 的数目>。
START_JOB             启动/恢复当前作业。
                      START_JOB=SKIP_CURRENT 在开始作业之前将跳过
                      作业停止时执行的任意操作。 
STATUS                在默认值 (0) 将显示可用时的新状态的情况下,
                      要监视的频率 (以秒计) 作业状态。
                      STATUS[=interval]
STOP_JOB              顺序关闭执行的作业并退出客户机。
                      STOP_JOB=IMMEDIATE 将立即关闭
                      数据泵作业。
```

【注】

* 在10g之前，传统的导出导入分别使用exp工具和imp工具。从oracle database 10g开始，不仅保留了原有的exp和imp工具，还提供了数据泵导出导入工具expdp和impdp。
* 从11g开始，在传统的export和import应用程序中可用的任何特性在data pump中都可用。

在使用expdp和impdp工具时，应该注意以下几点：

* exp和imp是客户端工具程序，它们既可以在客户端使用，也可以在服务器端使用。
* expdp和impdp是服务器工具程序，它们只能在oracle服务器端使用，不能再客户端使用。
* imp只适用于exp导出的文件，不适用于expdp导出文件；impdp只适用与expdp导出的文件，不适用于exp导出文件。data pump导出导入所得到的文件跟传统的import/export应用程序导出导入的文件不兼容。

使用EXPDP和IMPDP还可以实现移动表空间，即将表空间从一个数据库移动到另一个数据库中。

在Oracle 10g前，移动表空间只能在相同的操作系统平台之间进行。在Oracle 11g中，不仅允许在相同平台之间移动表空间，而且允许在不同平台之间移动表空间。通过查询动态性能视图V$TRANSPORTABLE_PLATFORM，可以显示在哪些OS平台之间可以移动表空间。


# pump数据字典

|数据字典           | 说明  |
|----------------------|---------------------------------------------------|
|dba_datapump_jobs  |显示运行数据泵作业的信息，也可以使user_datapump_jobs变量|
|dba_datapump_sessions | 提供数据泵作业会话级别的信息|
|datapump_paths  | 提供一系列有效的对象类型，可以将其与export或者impdp的include或者exclude参数关联起来|
|dba_directories |提供一系列已定义的目录 |

# 实践

## 准备工作

创建一个外部目录。

data pump要求为将要创建和读取的数据文件和日志文件创建目录，用来指向使用的外部目录。在oracle中创建目录对象时，可以使用 create directory语句。

```
SQL> create directory mypump as '/opt/oracle/admin/mmsgdb/dpdump/';
目录已创建。
SQL> grant read, write on directory mypump to mmsg;
授权成功。
SQL>
SQL> select * from dba_directories;   //查询所有目录 
OWNER                          DIRECTORY_NAME                 DIRECTORY_PATH
------------------------------ ------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------
SYS                            MYPUMP                         /opt/oracle/admin/mmsgdb/dpdump/
SYS                            QUEST_SOO_UDUMP_DIR            /opt/oracle/diag/rdbms/mmsgdb/mmsgdb/trace/
SYS                            QUEST_SOO_CDUMP_DIR            /opt/oracle/diag/rdbms/mmsgdb/mmsgdb/cdump/
SYS                            QUEST_SOO_ADUMP_DIR            /opt/oracle/admin/mmsgdb/adump/
SYS                            QUEST_SOO_BDUMP_DIR            /opt/oracle/diag/rdbms/mmsgdb/mmsgdb/trace/
SYS                            DATA_PUMP_DIR                  /opt/oracle/admin/mmsgdb/dpdump/
SYS                            ORACLE_OCM_CONFIG_DIR          /opt/oracle/product/11g/ccr/state
已选择7行。
SQL> 
```

至此，准备工作结束。

## 表模式导出

```
oracle@mmsg:~> expdp mmsg/mmsg directory=mypump  dumpfile=table_module.dmp tables=interfaceaccount_20100916,interfaceaccount_20100920 logfile=table_module.log
Export: Release 11.1.0.7.0 - 64bit Production on 星期六, 18 9月, 2010 10:38:13
Copyright (c) 2003, 2007, Oracle.  All rights reserved.
连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
启动 "MMSG"."SYS_EXPORT_TABLE_01":  mmsg/******** directory=mypump dumpfile=table_module.dmp tables=interfaceaccount_20100916,interfaceaccount_20100920 logfile=table_module.log 
正在使用 BLOCKS 方法进行估计...
处理对象类型 TABLE_EXPORT/TABLE/TABLE_DATA
使用 BLOCKS 方法的总估计: 128 KB
处理对象类型 TABLE_EXPORT/TABLE/TABLE
处理对象类型 TABLE_EXPORT/TABLE/INDEX/INDEX
处理对象类型 TABLE_EXPORT/TABLE/CONSTRAINT/CONSTRAINT
处理对象类型 TABLE_EXPORT/TABLE/INDEX/STATISTICS/INDEX_STATISTICS
处理对象类型 TABLE_EXPORT/TABLE/STATISTICS/TABLE_STATISTICS
. . 导出了 "MMSG"."INTERFACEACCOUNT_20100916"          7.375 KB       4 行
. . 导出了 "MMSG"."INTERFACEACCOUNT_20100920"          7.507 KB       6 行
已成功加载/卸载了主表 "MMSG"."SYS_EXPORT_TABLE_01" 
******************************************************************************
MMSG.SYS_EXPORT_TABLE_01 的转储文件集为:
  /opt/oracle/admin/mmsgdb/dpdump/table_module.dmp
作业 "MMSG"."SYS_EXPORT_TABLE_01" 已于 10:38:21 成功完成
oracle@mmsg:~>
```

【注意】
* 当导出的dumpfile名称与已有的dmp文件名重复时，导出失败，不覆盖原先存在的dmp文件

```
oracle@mmsg:~> expdp mmsg/mmsg directory=mypump  dumpfile=table_module.dmp tables=interfaceaccount_20100916,interfaceaccount_20100920 logfile=table_module.log
Export: Release 11.1.0.7.0 - 64bit Production on 星期六, 18 9月, 2010 10:40:16
Copyright (c) 2003, 2007, Oracle.  All rights reserved.
连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
ORA-39001: 参数值无效
ORA-39000: 转储文件说明错误
ORA-31641: 无法创建转储文件 "/opt/oracle/admin/mmsgdb/dpdump/table_module.dmp"
ORA-27038: 所创建的文件已存在
Additional information: 1
```

## schema模式导出 

```
oracle@mmsg:~> expdp system/sys directory=mypump dumpfile=schema.dmp schemas=mmsg nologfile=y
Export: Release 11.1.0.7.0 - 64bit Production on 星期六, 18 9月, 2010 10:49:31
Copyright (c) 2003, 2007, Oracle.  All rights reserved.
连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
启动 "SYSTEM"."SYS_EXPORT_SCHEMA_01":  system/******** directory=mypump dumpfile=schema.dmp schemas=mmsg nologfile=y 
正在使用 BLOCKS 方法进行估计...
处理对象类型 SCHEMA_EXPORT/TABLE/TABLE_DATA
使用 BLOCKS 方法的总估计: 9.375 MB
处理对象类型 SCHEMA_EXPORT/USER
处理对象类型 SCHEMA_EXPORT/SYSTEM_GRANT
处理对象类型 SCHEMA_EXPORT/DEFAULT_ROLE
处理对象类型 SCHEMA_EXPORT/PRE_SCHEMA/PROCACT_SCHEMA
处理对象类型 SCHEMA_EXPORT/TABLE/TABLE
处理对象类型 SCHEMA_EXPORT/TABLE/INDEX/INDEX
处理对象类型 SCHEMA_EXPORT/TABLE/CONSTRAINT/CONSTRAINT
处理对象类型 SCHEMA_EXPORT/TABLE/INDEX/STATISTICS/INDEX_STATISTICS
处理对象类型 SCHEMA_EXPORT/PACKAGE/PACKAGE_SPEC
处理对象类型 SCHEMA_EXPORT/PROCEDURE/PROCEDURE
处理对象类型 SCHEMA_EXPORT/PACKAGE/COMPILE_PACKAGE/PACKAGE_SPEC/ALTER_PACKAGE_SPEC
处理对象类型 SCHEMA_EXPORT/PROCEDURE/ALTER_PROCEDURE
处理对象类型 SCHEMA_EXPORT/VIEW/VIEW
处理对象类型 SCHEMA_EXPORT/PACKAGE/PACKAGE_BODY
处理对象类型 SCHEMA_EXPORT/TABLE/STATISTICS/TABLE_STATISTICS
. . 导出了 "MMSG"."AREANUMBERPREFIX"                   5.476 KB       2 行
********************************中间数据省略************************************
. . 导出了 "MMSG"."VASSUBSCRIBEINFO"                       0 KB       0 行
已成功加载/卸载了主表 "SYSTEM"."SYS_EXPORT_SCHEMA_01" 
******************************************************************************
SYSTEM.SYS_EXPORT_SCHEMA_01 的转储文件集为:
  /opt/oracle/admin/mmsgdb/dpdump/schema.dmp
作业 “SYSTEM”.“SYS_EXPORT_SCHEMA_01” 已于 10:49:50 成功完成
```

## 表空间导出

两种情况

### 1：表空间数据的导出

```
oracle@mmsg:~> expdp system/sys directory=mypump dumpfile=tablespace_data.dmp tablespaces=mmsg 
Export: Release 11.1.0.7.0 - 64bit Production on 星期六, 18 9月, 2010 10:51:45
Copyright (c) 2003, 2007, Oracle.  All rights reserved.
连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
启动 "SYSTEM"."SYS_EXPORT_TABLESPACE_01":  system/******** directory=mypump dumpfile=tablespace_data.dmp tablespaces=mmsg 
正在使用 BLOCKS 方法进行估计...
处理对象类型 TABLE_EXPORT/TABLE/TABLE_DATA
使用 BLOCKS 方法的总估计: 9.375 MB
处理对象类型 TABLE_EXPORT/TABLE/TABLE
处理对象类型 TABLE_EXPORT/TABLE/INDEX/INDEX
处理对象类型 TABLE_EXPORT/TABLE/CONSTRAINT/CONSTRAINT
处理对象类型 TABLE_EXPORT/TABLE/INDEX/STATISTICS/INDEX_STATISTICS
处理对象类型 TABLE_EXPORT/TABLE/STATISTICS/TABLE_STATISTICS
. . 导出了 "MMSG"."AREANUMBERPREFIX"                   5.476 KB       2 行
. . 导出了 "MMSG"."ROUTERTABLE"                        5.703 KB      17 行
********************************中间数据省略************************************
. . 导出了 "MMSG"."TRACEMSGINFO"                           0 KB       0 行
. . 导出了 "MMSG"."VASMISCMAPPER"                          0 KB       0 行
. . 导出了 "MMSG"."VASSUBSCRIBEINFO"                       0 KB       0 行
已成功加载/卸载了主表 "SYSTEM"."SYS_EXPORT_TABLESPACE_01" 
******************************************************************************
SYSTEM.SYS_EXPORT_TABLESPACE_01 的转储文件集为:
  /opt/oracle/admin/mmsgdb/dpdump/tablespace_data.dmp
作业 "SYSTEM"."SYS_EXPORT_TABLESPACE_01" 已于 10:52:00 成功完成
```

### 2：可移动表空间导出

先将对应的表空间设置成只读状态，然后执行可移动表空间元数据导出

```
SQL> alter tablespace wyztest read only;
表空间已更改。
SQL> host expdp system/sys directory=mypump dumpfile=tablespace.dmp transport_tablespaces=wyztest;
Export: Release 11.1.0.7.0 - 64bit Production on 星期六, 18 9月, 2010 10:56:48
Copyright (c) 2003, 2007, Oracle.  All rights reserved.
连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
启动 "SYSTEM"."SYS_EXPORT_TRANSPORTABLE_01":  system/******** directory=mypump dumpfile=tablespace.dmp transport_tablespaces=wyztest 
处理对象类型 TRANSPORTABLE_EXPORT/PLUGTS_BLK
处理对象类型 TRANSPORTABLE_EXPORT/POST_INSTANCE/PLUGTS_BLK
已成功加载/卸载了主表 "SYSTEM"."SYS_EXPORT_TRANSPORTABLE_01" 
******************************************************************************
SYSTEM.SYS_EXPORT_TRANSPORTABLE_01 的转储文件集为:
  /opt/oracle/admin/mmsgdb/dpdump/tablespace.dmp
******************************************************************************
可传输表空间 WYZTEST 所需的数据文件:
  /opt/oracle/oradata/mmsgdb/wyztest.dbf
  /opt/oracle/oradata/mmsgdb/wyztest01.dbf
作业 "SYSTEM"."SYS_EXPORT_TRANSPORTABLE_01" 已于 10:56:54 成功完成
SQL> alter tablespace wyztest online;
表空间已更改。
SQL>
```
 
### 全库模式导出

```
expdp system/sys directory=mypump dumpfile=full_oracle.dmp full=y  logfile=full_oracle.log
expdp mmsg/mmsg  directory=mypump dumpfile=app_oracle.dmp full=y   logfile=full_oracle.log
```

### 表模式导入

```
SQL> host impdp mmsg/mmsg directory=mypump dumpfile=table_module.dmp tables=interfaceaccount_20100916,interfaceaccount_20100920 table_exists_action=replace
Import: Release 11.1.0.7.0 - 64bit Production on 星期六, 18 9月, 2010 11:09:41
Copyright (c) 2003, 2007, Oracle.  All rights reserved.
连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
已成功加载/卸载了主表 "MMSG"."SYS_IMPORT_TABLE_01" 
启动 "MMSG"."SYS_IMPORT_TABLE_01":  mmsg/******** directory=mypump dumpfile=table_module.dmp tables=interfaceaccount_20100916,interfaceaccount_20100920 table_exists_action=replace 
处理对象类型 TABLE_EXPORT/TABLE/TABLE
处理对象类型 TABLE_EXPORT/TABLE/TABLE_DATA
. . 导入了 "MMSG"."INTERFACEACCOUNT_20100916"          7.375 KB       4 行
. . 导入了 "MMSG"."INTERFACEACCOUNT_20100920"          7.507 KB       6 行
处理对象类型 TABLE_EXPORT/TABLE/INDEX/INDEX
处理对象类型 TABLE_EXPORT/TABLE/CONSTRAINT/CONSTRAINT
处理对象类型 TABLE_EXPORT/TABLE/INDEX/STATISTICS/INDEX_STATISTICS
处理对象类型 TABLE_EXPORT/TABLE/STATISTICS/TABLE_STATISTICS
作业 "MMSG"."SYS_IMPORT_TABLE_01" 已于 11:09:44 成功完成
```

## schema模式导入

```
impdp system/sys directory=mypump dumpfile=schema.dmp schemas=mmsg nologfile=y
```

## 表空间数据导入

```
impdp system/sys directory=mypump dumpfile=tablespace_data.dmp tablespaces=mmsg 
```

## 可移动表空间导入

将对应的表空间设置成只读状态，然后执行可移动表空间元数据导出

```
   SQL>  alter tablespace wyztest read only;
   SQL>  host impdp system/sys directory=mypump dumpfile=tablespace.dmp transport_tablespaces=wyztest;
   SQL>  alter tablespace wyztest online;
```

## 全库模式导入

```
impdp system/sys directory=mypump dumpfile=full_oracle.dmp full=y
```

