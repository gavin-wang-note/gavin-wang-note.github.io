---
layout:     post
title:      "Oracle案例--错误码之ORA-01113"
subtitle:   "Oracle error code troubleshoot--ORA-01113"
date:       2011-09-24
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-01113 文件需要介质恢复

## 表象

```shell
SQL> startup
ORACLE instance started.

Total System Global Area 8351150080 bytes
Fixed Size                  2176320 bytes
Variable Size            4580182720 bytes
Database Buffers         3758096384 bytes
Redo Buffers               10694656 bytes
Database mounted.
ORA-01113: 文件 17 需要介质恢复
ORA-01110: 数据文件 17: '/home/oracle/dls_tbs_idx.dbf'
```

## 解决方法

```shell
oracle@linux25:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期六 9月 24 17:43:45 2011

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining,
Oracle Database Vault and Real Application Testing options

SQL> recover datafile '/home/oracle/dls_tbs_idx.dbf';
Media recovery complete.
SQL> alter database open;

Database altered.

SQL> 
```
