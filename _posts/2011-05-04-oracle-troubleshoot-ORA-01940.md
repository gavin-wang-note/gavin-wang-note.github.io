---
layout:     post
title:      "Oracle案例--错误码之ORA-01940"
subtitle:   "Oracle error code troubleshoot--ORA-01940"
date:       2011-05-04
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-01940：无法删除当前已链接的用户 

## 现象

```shell
SQL> drop user ufuser cascade;    
drop user ufuser cascade
*
ERROR at line 1:
ORA-01940: cannot drop a user that is currently connected
```

## 原因

当前用户正在与数据库建立连接，session关系还在。

## 解决方法

Kill掉对应的session既可。

1、	查询对应用户与当前数据库连接的session信息

```shell
SQL> set wrap off    
SQL> set lin 200
SQL> set pagesize 0
SQL> select username,sid,serial# from v$session where username ='UFUSER';
UFUSER                                513         81
UFUSER                                515         62
UFUSER                                516      49583
UFUSER                                517      38584
UFUSER                                519      12508
UFUSER                                520      36408
UFUSER                                522      64260
UFUSER                                523      59321
UFUSER                                524       4285
UFUSER                                525      42644
UFUSER                                529        181
UFUSER                                530      44970
```

2、kill session操作

```shell
alter system kill session'513,81';
alter system kill session'515,62';
alter system kill session'516,49583';
alter system kill session'519,12508';
alter system kill session'520,36408';
alter system kill session'522,64260';
alter system kill session'523,59321';
alter system kill session'524,4285';
alter system kill session'525,42644';
alter system kill session'529,181';
alter system kill session'530,44970';
```

3、查询session信息确定该session是否被kill

```
select saddr,sid,serial#,paddr,username,status from v$session where username is not null and username ='UFUSER';
```

status 为要删除用户的session状态，如果还为inactive，说明没有被kill掉，如果状态为killed，说明已kill。

4、如果session被kill掉，然后执行drop user操作。

