---
layout:     post
title:      "Oracle案例--登录RAC间歇性成功"
subtitle:   "Oracle troubleshoot--Access RAC login intermittently successful"
date:       2009-03-14
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


## 表象

用户登录RAC集群数据库时，时而登录成功，时而登录失败，且TNSNAMES.ORA文件无问题。

## 解决方法

修改spfile文件中remote_listener 的VALUE值为空。

sys用户登录，修改spfile文件中remote_listener 的VALUE值为空。

```
node1:oracle:ora11g > sqlplus sys/oracle@ora11g as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on Thu May 14 17:23:06 2009

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, Real Application Clusters, OLAP, Data Mining
and Real Application Testing options

SQL> show parameter remote

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
remote_dependencies_mode             string      TIMESTAMP
remote_listener                      string      //如果remote_listener的VALUE值不为空，修改值为空。
remote_login_passwordfile            string      EXCLUSIVE
remote_os_authent                    boolean     FALSE
remote_os_roles                      boolean     FALSE
result_cache_remote_expiration       integer     0
SQL> alter system set remote_listener ='' scope=spfile;

系统已更改。
```

修改后重启RAC数据库实例后生效。

