---
layout:     post
title:      "Oracle案例--找不到INITSID.ORA文件解决方法（ORA-01078）"
subtitle:   "Oracle troubleshoot of can't find INITSID.ORA"
date:       2009-11-09
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# ORA-01078 找不到INITSID.ORA文件解决方法


## 表象

```
node1:oracle:mmsgdb > sqlplus '/as sysdba'
SQL*Plus: Release 11.1.0.7.0 - Production on 星期一 11月 9 11:25:48 2009
Copyright (c) 1982, 2008, Oracle.  All rights reserved.
已连接到空闲例程。
SQL> startup mount
ORA-01078: failure in processing system parameters
LRM-00109: ???????????????? '/opt/oracle/product/11g/dbs/initmmsgdb.ora'
SQL> startup force
ORA-01078: failure in processing system parameters
LRM-00109: ???????????????? '/opt/oracle/product/11g/dbs/initmmsgdb.ora'
SQL> exit
已断开连接
```

## 原因

```
Failure during processing of INIT.ORA parameters during system startup.
```

## 解决方法

### 方法一

拷贝init.ora.9262009101410文件到指定目录

步骤：

（1） 进入$ORACLE_BASE/admin/mmsgdb/pfile，检查文件 init.ora.xxxxxx 是否存在（如：init.ora.9262009101410），存在，执行步骤（2）；

（2） 拷贝文件init.ora.9262009101410到/opt/oracle/product/11g/dbs/目录下 （cp init.ora.9262009101410 /opt/oracle/product/11g/dbs/）;

（3）更改init.ora.9262009101410文件名为需要的init文件名（mv init.ora.9262009101410 initmmsgdb.ora）;

（4） 启动数据库实例

```
sqlplus '/as sysdba'  
startup
```

### 方法二

没有init文件，就去创建这个文件。

Oracle最后检查的文件为initmmsgdb.ora,让我们创建这个文件,然后数据库实例即可创建:

```
SQL> ! echo "db_name=mmsgdb" > /opt/oracle/product/11g/dbs/initmmsgdb.ora
SQL> startup nomount;
```
