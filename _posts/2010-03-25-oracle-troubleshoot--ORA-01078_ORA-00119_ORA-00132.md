---
layout:     post
title:      "Oracle案例--错误码之ORA-01078,ORA-00119,ORA-00132"
subtitle:   "Oracle error code troubleshoot--ORA-01078,ORA-00119,ORA-00132"
date:       2010-03-25
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-01078  ORA-00119 ORA-00132 案例

## 表象

```shell
oracle@mmsg01:~/product/11g/network/admin> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on Thu Mar 25 09:51:02 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

Connected to an idle instance.

SQL> startup 
ORA-01078: failure in processing system parameters
ORA-00119: invalid specification for system parameter LOCAL_LISTENER
ORA-00132: syntax error or unresolved network name 'LISTENER_MMSGDB'
SQL> exit
```

## 解决方法

将监听文件中HOST处改成具体的IP地址

```shell
LISTENER_MMSGDB =
  (ADDRESS = (PROTOCOL = TCP)(HOST = your host ip )(PORT = 1523))
```

