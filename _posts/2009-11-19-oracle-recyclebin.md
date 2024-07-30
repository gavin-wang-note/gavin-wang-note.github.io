---
layout:     post
title:      "Oracle 回收站介绍"
subtitle:   "Oracle Recyclebin Desc"
date:       2009-11-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 回收站(recycle bin)介绍

实际上，Recycle Bin只是一个保存被drop的对象的一个数据字典表。所以，可以通过如下语句查询回收站中的信息：

```shell
node1:oracle:mmsgdb > sqlplus /nolog 

SQL*Plus: Release 11.1.0.7.0 - Production on 星期四 11月 19 10:34:34 2009

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

SQL> conn wyz/wyz
已连接。
SQL> select * from recyclebin;

OBJECT_NAME                    ORIGINAL_NAME                    OPERATION
------------------------------ -------------------------------- ---------
TYPE                      TS_NAME                        CREATETIME
------------------------- ------------------------------ -------------------
DROPTIME               DROPSCN PARTITION_NAME                   CAN CAN
------------------- ---------- -------------------------------- --- ---
   RELATED BASE_OBJECT PURGE_OBJECT      SPACE
---------- ----------- ------------ ----------
BIN$eIz0mM1Ef7DgQKjA3GRWvg==$0 VPNCORP_300                      DROP
TABLE                     WYZ                            2009-11-04:11:41:34
2009-11-17:15:20:06   10198071                                  YES YES
     46354       46354        46354          8

已选择708行。

SQL>
```

除非拥有sysdba权限，每个用户只能看到属于自己的对象。所以，对于用户来说，好像每个人都拥有自己的回收站。即使用户有删除其他schema对象的权限，也只能在recyclebin中看到属于自己的对象。

# 实践

## 查询当前回收站中数据

```shell
node1:oracle:mmsgdb > sqlplus /nolog

SQL*Plus: Release 11.1.0.7.0 - Production on 星期四 11月 19 10:45:32 2009

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

SQL> conn wyz/wyz 
已连接。
SQL> select * from recyclebin;

未选定行

SQL>
```

上面显示回收站为空。

## 删除一记录

数据库用户wyz删除一条记录：

```shell

SQL> urop table interfaceaccount_20091117;

表已删除。
```

## 查看回收站信息

```shell
SQL> select object_name,original_name from recyclebin;

OBJECT_NAME                    ORIGINAL_NAME
------------------------------ --------------------------------
BIN$eLFmxee63zrgQKjA3GR4Sw==$0 IDX_I_20091117
BIN$eLFmxee73zrgQKjA3GR4Sw==$0 SYS_C0048264
BIN$eLFmxee83zrgQKjA3GR4Sw==$0 INTERFACEACCOUNT_20091117

SQL>
```

上面显示3条记录，记录表interfaceaccount_20091117被删除时的信息。

以下几种drop不会将相关对象放进RecycleBin：

* drop tablespace： 会将RecycleBin中所有属于该tablespace的对象清除
* drop user：      会将RecycleBin中所有属于该用户的对象清除
* drop cluster：    会将RecycleBin中所有属于该cluster的成员对象清除
* drop type：      会将RecycleBin中所有依赖该type的对象清除

RecycleBin中的对象会被系统自动按照规则重命名，这是为了防止命名冲突。命名格式为：BIN$unique_id$version，其中unique_id是26个字符的对象唯一标识符，version则是对象在数据库中的版本号。

## 验证命名规则

已经删除了表interfaceaccount_20091117，创建该表，再次删除一次。

```shell
SQL> create table interfaceaccount_20091117 as select * from interfaceaccount_20091119 where 1=2;   #创建表interfaceaccount_20091117
SQL> drop table interfaceaccount_20091117;    #再次删除表interfaceaccount_20091117

表已删除。

SQL> select object_name,original_name from recyclebin;   #查看回收站信息

OBJECT_NAME                    ORIGINAL_NAME
------------------------------ --------------------------------
BIN$eLFmxee63zrgQKjA3GR4Sw==$0 IDX_I_20091117
BIN$eLFmxee73zrgQKjA3GR4Sw==$0 SYS_C0048264
BIN$eLFmxee83zrgQKjA3GR4Sw==$0 INTERFACEACCOUNT_20091117
BIN$eLFmxefD3zrgQKjA3GR4Sw==$0 INTERFACEACCOUNT_20091117

SQL>
```

可以看到，删除table interfaceaccount_20091117后，重建一个名为interfaceaccount_20091117的table，再次删除，其unique_id是不一样的。

通过这种命名方式，避免了对于删除table后又重建了同名table的情况可能造成的命名冲突。

# 启用/禁用回收站

启用或禁用回收站，通过设置初始化参数recyclebin，可以控制是否启用回收站功能，默认是开启的。

```shell
SQL> alter system set recyclebin=off;        #关闭回收站
系统已更改。
SQL> alter system set recyclebin=on;        #开启回收站
系统已更改。
SQL> 
```

修改该参数后，重启实例生效。


# 查看RecycleBin中的信息

前面已经提及，即使用：

```shell
SQL> select object_name,original_name from recyclebin;
```

或（必须是sysdba用户）：

```shell
SQL> select owner,synonym_name,table_owner,table_name from dba_synonyms where synonym_name='RECYCLEBIN';

OWNER                          SYNONYM_NAME
------------------------------ ------------------------------
TABLE_OWNER                    TABLE_NAME
------------------------------ ------------------------------
PUBLIC                         RECYCLEBIN
SYS                            USER_RECYCLEBIN


SQL>
```

或

```shell
SQL> show recyclebin 
ORIGINAL NAME    RECYCLEBIN NAME                OBJECT TYPE  DROP TIME
---------------- ------------------------------ ------------ -------------------
INTERFACEACCOUNT BIN$eLFmxefD3zrgQKjA3GR4Sw==$0 TABLE        2009-11-19:10:58:22
_20091117
INTERFACEACCOUNT BIN$eLFmxee83zrgQKjA3GR4Sw==$0 TABLE        2009-11-19:10:49:00
_20091117
SQL>
```

# 清除RecycleBin中的对象

Oracle10g提供了回收站功能，回收站类似Windows的回收站，是个虚拟的容器。回收站的东西多了，自然需要清除：

自oracle 10g之后，oracle提供了purge来执行清除recyclebin的功能。

purge table table_name可以清除指定的table，这里的table_name既可以是table原来的名字，也可以是回收站中按规则自动命名的名字。

```shell
SQL> show recyclebin 
ORIGINAL NAME    RECYCLEBIN NAME                OBJECT TYPE  DROP TIME
---------------- ------------------------------ ------------ -------------------
INTERFACEACCOUNT BIN$eLFmxefD3zrgQKjA3GR4Sw==$0 TABLE        2009-11-19:10:58:22
_20091117
INTERFACEACCOUNT BIN$eLFmxee83zrgQKjA3GR4Sw==$0 TABLE        2009-11-19:10:49:00
_20091117

SQL>  purge table  INTERFACEACCOUNT_20091117;

表已清除。

SQL> purge table BIN$eLFmxee83zrgQKjA3GR4Sw==$0;            
purge table BIN$eLFmxee83zrgQKjA3GR4Sw==$0
                                      *
第 1 行出现错误:
ORA-00933: SQL 命令未正确结束


SQL> purge table "BIN$eLFmxefD3zrgQKjA3GR4Sw==$0";  #需要加引号

表已清除。

SQL>

Purge tablespace tablespace_name user user_name则可以清除Recycle中属于指定tablespace和指定user的所有对象。
node1:oracle:mmsgdb > sqlplus '/as sysdba'

SQL*Plus: Release 11.1.0.7.0 - Production on 星期四 11月 19 11:34:04 2009

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> select * from dba_tablespace_usage_metrics;  #查看表空间信息

TABLESPACE_NAME                USED_SPACE TABLESPACE_SIZE USED_PERCENT
------------------------------ ---------- --------------- ------------
MMSC                                 4088           12800      31.9375
MMSG                                 4864          128000          3.8
SYSAUX                              35440         4194302   .844955847
SYSTEM                              63648         4194302    1.5174873
TEMP                                    0         4194302            0
UNDOTBS1                              816         4194302   .019454965
USERS                                 128         4194302   .003051759
WYZ                                  6008           12800      46.9375
YJH                                 10064          128000       7.8625
YKLOG_DATA                            256          256000           .1
YKLOG_INDEX                           128          128000           .1

TABLESPACE_NAME                USED_SPACE TABLESPACE_SIZE USED_PERCENT
------------------------------ ---------- --------------- ------------
ZJUN                                 4992           25600         19.5

已选择12行。

SQL>
SQL> select * from dba_users where username='WYZ';

USERNAME                          USER_ID PASSWORD
------------------------------ ---------- ------------------------------
ACCOUNT_STATUS                   LOCK_DATE      EXPIRY_DATE
-------------------------------- -------------- --------------
DEFAULT_TABLESPACE             TEMPORARY_TABLESPACE           CREATED
------------------------------ ------------------------------ --------------
PROFILE                        INITIAL_RSRC_CONSUMER_GROUP
------------------------------ ------------------------------
EXTERNAL_NAME
--------------------------------------------------------------------------------
PASSWORD E
-------- -
WYZ                                    36

USERNAME                          USER_ID PASSWORD
------------------------------ ---------- ------------------------------
ACCOUNT_STATUS                   LOCK_DATE      EXPIRY_DATE
-------------------------------- -------------- --------------
DEFAULT_TABLESPACE             TEMPORARY_TABLESPACE           CREATED
------------------------------ ------------------------------ --------------
PROFILE                        INITIAL_RSRC_CONSUMER_GROUP
------------------------------ ------------------------------
EXTERNAL_NAME
--------------------------------------------------------------------------------
PASSWORD E
-------- -
OPEN                                            25-4月 -10

USERNAME                          USER_ID PASSWORD
------------------------------ ---------- ------------------------------
ACCOUNT_STATUS                   LOCK_DATE      EXPIRY_DATE
-------------------------------- -------------- --------------
DEFAULT_TABLESPACE             TEMPORARY_TABLESPACE           CREATED
------------------------------ ------------------------------ --------------
PROFILE                        INITIAL_RSRC_CONSUMER_GROUP
------------------------------ ------------------------------
EXTERNAL_NAME
--------------------------------------------------------------------------------
PASSWORD E
-------- -
WYZ                            WYZ_TMP                        27-10月-09

USERNAME                          USER_ID PASSWORD
------------------------------ ---------- ------------------------------
ACCOUNT_STATUS                   LOCK_DATE      EXPIRY_DATE
-------------------------------- -------------- --------------
DEFAULT_TABLESPACE             TEMPORARY_TABLESPACE           CREATED
------------------------------ ------------------------------ --------------
PROFILE                        INITIAL_RSRC_CONSUMER_GROUP
------------------------------ ------------------------------
EXTERNAL_NAME
--------------------------------------------------------------------------------
PASSWORD E
-------- -
DEFAULT                        DEFAULT_CONSUMER_GROUP

USERNAME                          USER_ID PASSWORD
------------------------------ ---------- ------------------------------
ACCOUNT_STATUS                   LOCK_DATE      EXPIRY_DATE
-------------------------------- -------------- --------------
DEFAULT_TABLESPACE             TEMPORARY_TABLESPACE           CREATED
------------------------------ ------------------------------ --------------
PROFILE                        INITIAL_RSRC_CONSUMER_GROUP
------------------------------ ------------------------------
EXTERNAL_NAME
--------------------------------------------------------------------------------
PASSWORD E
-------- -


USERNAME                          USER_ID PASSWORD
------------------------------ ---------- ------------------------------
ACCOUNT_STATUS                   LOCK_DATE      EXPIRY_DATE
-------------------------------- -------------- --------------
DEFAULT_TABLESPACE             TEMPORARY_TABLESPACE           CREATED
------------------------------ ------------------------------ --------------
PROFILE                        INITIAL_RSRC_CONSUMER_GROUP
------------------------------ ------------------------------
EXTERNAL_NAME
--------------------------------------------------------------------------------
PASSWORD E
-------- -
10G 11G  N

USERNAME                          USER_ID PASSWORD
------------------------------ ---------- ------------------------------
ACCOUNT_STATUS                   LOCK_DATE      EXPIRY_DATE
-------------------------------- -------------- --------------
DEFAULT_TABLESPACE             TEMPORARY_TABLESPACE           CREATED
------------------------------ ------------------------------ --------------
PROFILE                        INITIAL_RSRC_CONSUMER_GROUP
------------------------------ ------------------------------
EXTERNAL_NAME
--------------------------------------------------------------------------------
PASSWORD E
-------- -


SQL>

SQL> purge tablespace wyz user wyz;   #第一个wyz为表空间名称，第二个wyz为数据库用户名
表空间已清除。

Purge recyclebin可以清除执行该命令的用户所能看到的所有recyclebin对象。也就是普通用户能清除属于自己的对象，而sysdba用户则能清除所有recyclebin中的对象。
SQL> purge recyclebin;
回收站已清空。
```

另外，purge index可以清除index对象。

```shell
SQL> select object_name,original_name,type from recyclebin;

OBJECT_NAME                    ORIGINAL_NAME
------------------------------ --------------------------------
TYPE
-------------------------
BIN$eLIogOtK7vDgQKjA3GRztA==$0 INTERFACEACCOUNT_20091117
TABLE

BIN$eLIogOtS7vDgQKjA3GRztA==$0 IDX_I_20091103
INDEX

BIN$eLIogOtT7vDgQKjA3GRztA==$0 SYS_C0019958
INDEX


OBJECT_NAME                    ORIGINAL_NAME
------------------------------ --------------------------------
TYPE
-------------------------
BIN$eLIogOtU7vDgQKjA3GRztA==$0 INTERFACEACCOUNT_20091103
TABLE


SQL>
SQL> purge index IDX_I_20091103;

索引已清除。

SQL>
```

如果出现

```shell
SQL> purge index IDX_I_20091103;
第 1 行出现错误:
ORA-00604: 递归 SQL 级别 1 出现错误
ORA-02429: 无法删除用于强制唯一/主键的索引
```

这里由于IDX_I_20091103是table主键的索引，所以无法单独清除。可直接清除回收站：

```shell
SQL> purge recyclebin;
回收站已清空。
```

# 还原RecycleBin中的对象

使用Flashback table来还原过被删除的table。

```shell
SQL> flashback table  INTERFACEACCOUNT_20091117  to before drop rename to INTERFACEACCOUNT_wyztest;

闪回完成。

SQL> select object_name,original_name,type from recyclebin;

OBJECT_NAME                    ORIGINAL_NAME
------------------------------ --------------------------------
TYPE
-------------------------
BIN$eLIogOtT7vDgQKjA3GRztA==$0 SYS_C0019958
INDEX

BIN$eLIogOtU7vDgQKjA3GRztA==$0 INTERFACEACCOUNT_20091103
TABLE


SQL>
闪回完成。闪回是oracle11g的亮点。
SQL> desc INTERFACEACCOUNT_wyztest;
 名称                                      是否为空? 类型
 ----------------------------------------- -------- ----------------------------
 MODULETYPE                                NOT NULL NUMBER(38)
 MODULEID                                  NOT NULL NUMBER(38)
 ACCOUNTDATANAME                           NOT NULL VARCHAR2(64)
 STARTDATETIME                             NOT NULL VARCHAR2(14)
 STOPDATETIME                              NOT NULL VARCHAR2(14)
 ACCOUNT                                   NOT NULL NUMBER(38)

SQL>
```

如果多次删除同名的table，则使用上面的语句还原的是最后一个被删除的INTERFACEACCOUNT_20091117表，这里也可以使用RecycleBin给table的名字来做还原。

```shell
SQL> flashback table " BIN$eLIogOtU7vDgQKjA3GRztA==$0" to before drop rename to wyz_test_2009-11-19;
```

