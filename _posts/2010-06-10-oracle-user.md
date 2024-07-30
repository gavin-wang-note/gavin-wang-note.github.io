---
layout:     post
title:      "Oracle SQL篇之账号"
subtitle:   "Oracle SQL -- Users"
date:       2010-06-10
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 显示当前连接用户

```shell
SQL> show user       
USER 为 "SYS"
SQL>
```

# 在某个用户下找所有的索引

```shell
select user_indexes.table_name, user_indexes	.index_name,uniqueness,column_name 	 
from user_ind_columns, user_indexes   
where user_ind_columns.index_name = user_indexes.index_name 
and user_ind_columns.table_name = user_indexes.table_name 
order by user_indexes.table_type, user_indexes.table_name, user_indexes.index_name, column_position;
```

# 查询每个用户的权限

```shell
SQL> SELECT * FROM DBA_SYS_PRIVS;
```

# 获取有哪些用户在使用数据库

```shell
SQL> select username from v$session; 

USERNAME
------------------------------------------------------------
MMSG
MMSG

SYS
SYS
MMSG
MMSG
MMSG

已选择7行。

SQL>
```

# 查询用户拥有的权限

```shell
mmsg:oracle:mmsgdb > sqlplus / as sysdba

+SQL*Plus: Release 11.1.0.6.0 - Production on Tue Feb 22 15:58:54 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options


SQL> SELECT *  FROM DBA_SYS_PRIVS where grantee='MMSG';

GRANTEE                        PRIVILEGE                                ADM
------------------------------ ---------------------------------------- ---
MMSG                           UNLIMITED TABLESPACE                     NO
MMSG                           CREATE VIEW                              NO
MMSG                           CREATE TABLE                             NO
MMSG                           CREATE SESSION                           NO
MMSG                           CREATE PROCEDURE                         NO
MMSG                           CREATE SEQUENCE                          NO

6 rows selected.

SQL>
```

# 锁用户/用户解锁

## 锁用户

```shell
SQL> alter user wyz account lock;

用户已更改。

SQL> connect wyz/wyz@mmsgdb
ERROR:
ORA-28000: 帐户已被锁定


警告: 您不再连接到 ORACLE。
```


## 用户解锁

```shell
SQL> alter user wyz account unlock;

用户已更改。

SQL> connect wyz/wyz@mmsgdb
已连接。
SQL> exit
```
