---
layout:     post
title:      "Oracle案例--非DBA用户连接oracle，报权限不允许"
subtitle:   "Oracle troubleshoot--Permission denied for not oracle user"
date:       2010-03-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 在AIX操作系统，非DBA用户连接oracle，报权限不允许

## 表象

在AIX操作系统，非DBA用户连接oracle，报权限不允许：


```shell
2 p570flpar2 [nss] :/home/nss>sql      
sqlplus startup unsuccessfully : Permission denied(13)
```

在该用户下打开oracle安装目录：

```shell
7 p570flpar2 [nss] :/home/nss/mms_home/cfg>cd $ORACLE_HOME
/opt/oracle/oracle/app/product/11.1.0/db_1: 文件访问许可不允许执行指定的操作。
```

## 解决方法

从错误内容，可以知道这是权限不足问题。

用oracle用户登陆：

查看权限，发现oracle目录没有执行权限

```shell
% ll 
total 4917192
drwx--x--x    2 oracle   dba             256 Mar 18 10:00 Mail
-rw-r--r--    1 oracle   dba       650295797 Mar  2 11:49 aix.ppc64_11gR1_database_1of2.zip
-rw-r--r--    1 oracle   dba      1867281765 Mar  2 14:39 aix.ppc64_11gR1_database_2of2.zip
drwxr-x---    3 oracle   dba             256 Mar  8 20:12 app
drwxr-x---    3 oracle   dba             256 Mar  2 16:39 cdy
drwxr-x---    3 oracle   dba             256 Mar  5 09:49 hzw
drwxr-x---    2 oracle   dba             256 Mar 18 10:38 infoxwebdata
drwxr-x---    3 oracle   dba             256 Mar  4 13:47 lcx
drwxr-xr-x    2 oracle   dba             256 Mar 18 11:21 mmsdata
drwxr-x---    3 oracle   dba             256 Mar  8 20:07 oracle
drwxr-x---    3 oracle   dba             256 Mar  2 16:55 oradata
-rw-r--r--    1 oracle   dba            4629 Mar 19 15:56 smit.log
-rw-r--r--    1 oracle   dba             611 Mar 19 15:56 smit.script
-rw-r--r--    1 oracle   dba            1203 Mar 19 15:56 smit.transaction
```

增加目录权限：

```% chmod -R 755 oracle ```

然后到$ORACLE_HOME/bin目录下，给tnsping与sqlplus添加读与执行的权限：

```shell
% chmod 755 tnsping
% chmod 755 sqlplus
```

修改权限，回到原用户执行命令，可以看到，数据库已经可以连上：

```shell
10 p570flpar2 [nss] :/opt/oracle/oracle/app/product/11.1.0/db_1>tnsping mdsp 10

TNS Ping Utility for IBM/AIX RISC System/6000: Version 11.1.0.6.0 - Production on 19-MAR-2010 16:05:38

Copyright (c) 1997, 2007, Oracle.  All rights reserved.

Used parameter files:


Used TNSNAMES adapter to resolve the alias
Attempting to contact (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = p570flpar2)(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = mdsp)))
OK (100 msec)
OK (0 msec)
OK (0 msec)
OK (0 msec)
OK (10 msec)
OK (0 msec)
OK (0 msec)
OK (0 msec)
OK (0 msec)
OK (0 msec)

9 p570flpar2 [nss] :/home/nss/mms_home/cfg>cd $ORACLE_HOME
10 p570flpar2 [nss] :/opt/oracle/oracle/app/product/11.1.0/db_1>

16 p570flpar2 [nss] :/home/nss>sql

SQL*Plus: Release 11.1.0.6.0 - Production on Fri Mar 19 16:09:02 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> exit
Disconnected from Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
```

