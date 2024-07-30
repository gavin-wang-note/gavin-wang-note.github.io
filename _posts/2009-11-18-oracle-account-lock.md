---
layout:     post
title:      "Oracle账号被锁--ORA-28000"
subtitle:   "Oracle account lock--ORA-28000"
date:       2009-11-18
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 表象

Oracle数据库帐号被锁, oralce报ORA-28000错误。

# 原因

账户被锁：

```shell
oracle@mmsg:~> oerr ora 28000
28000, 00000, "the account is locked"
// *Cause:   The user has entered wrong password consequently for maximum
//           number of times specified by the user's profile parameter
//           FAILED_LOGIN_ATTEMPTS, or the DBA has locked the account
// *Action:  Wait for PASSWORD_LOCK_TIME or contact DBA
```

账号被锁主要原因：

```shell
SQL> show parameter sec_max_failed_login_attempts

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
sec_max_failed_login_attempts        integer     10
SQL>
```

oracle系统参数sec_max_failed_login_attempts默认值为10，即连续输入用户口令10次均不正确后，数据库自动锁住当前用户，用户一旦锁住，不会自动解锁，需要dba权限用户手工干预（关闭该功能，详见本文oralce SQL篇之账号）。

# 解决方法

Oracle系统用户登录数据库，对用户执行解锁操作。

```shell
oracle@mmsg:~> sqlplus '/as sysdba'

SQL*Plus: Release 11.1.0.7.0 - Production on 星期三 11月 18 19:12:47 2009

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options 
SQL> alter user user_name account unlock;
User altered.
SQL>
```
