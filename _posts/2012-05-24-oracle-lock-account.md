---
layout:     post
title:      "关闭Oracle用户多次登录失败锁定账户的功能"
subtitle:   "Disable feature of Oracle users to lock accounts after multiple login failures"
date:       2012-05-24
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# 前言

有时候工作环境密码太多，切换不同的环境，难免要输入多次密码，但万一达到尝试上限了，怎么破？ 有的环境只能等待了。。。。。。

本文介绍关闭数据库多次登录失败锁定账户的功能，执行此任务可以设置单个用户连续登录失败的次数为不限制。在Oracle11g默认配置下，如果单个账户如果连续10次登录失败，系统将会锁定账户，只能通过对账户解锁。

# 如何关闭数据库多次登录失败锁定账户的功能 

关闭该功能，具体操作如下：

(1)查询当前允许登录失败次数

以oracle用户登录，连接数据库。

```
$ sqlplus "/ as sysdba"
```

查看系统允许用户登录失败的次数:

```
SQL> select LIMIT from dba_profiles where PROFILE='DEFAULT' and RESOURCE_NAME='FAILED_LOGIN_ATTEMPTS';
屏幕显示中有如下信息。（仅供参考）
LIMIT
--------------------------------------------------------------------------------
10
```

(2)修改允许登录失败次数

修改系统允许用户登录失败的次数为不限制:

```
SQL> ALTER PROFILE DEFAULT LIMIT FAILED_LOGIN_ATTEMPTS UNLIMITED;
屏幕显示中有如下信息。（仅供参考）
Profile altered.
```

(3)确认修改效果

查看修改后的允许用户登录失败的次数。

```
SQL> select LIMIT from dba_profiles where PROFILE='DEFAULT' and RESOURCE_NAME='FAILED_LOGIN_ATTEMPTS';
屏幕显示中有如下信息。（仅供参考）
LIMIT
--------------------------------------------------------------------------------
UNLIMITED
```
