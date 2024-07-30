---
layout:     post
title:      "Oracle案例--表空间满，数据库报错(01653,ORA-06512)"
subtitle:   "Oracle troubleshoot--tablespace full(ORA-01653,ORA-06512)"
date:       2011-11-29
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 表空间满，数据库报错

## 表象

当表空间已经满时，执行数据库操作数据库会报错，例如：

```shell
ORA-01653: 表 MMSG.TMP_BASE_RESULT 无法通过 8 (在表空间 MMSG 中) 扩展
ORA-06512: 在 "MMSG.LOG2DB_UTIL", line 92
ORA-06512: 在 line 1
```

## 原因

查看错误码信息，如下：

```shell
ORA-01653
node1:oracle:mmsgdb > oerr ora 01653
01653, 00000, "unable to extend table %s.%s by %s in tablespace %s"
// *Cause:  Failed to allocate an extent of the required number of blocks for 
//          a table segment in the tablespace indicated.
// *Action: Use ALTER TABLESPACE ADD DATAFILE statement to add one or more
//          files to the tablespace indicated.
node1:oracle:mmsgdb >
```

## 解决方法

通过上述错误码给出的原因和解决方法，需要扩展表空间。

扩展操作命令如下：

```shell
alter database datafile '/opt/oracle/admin/mmsgdb/mmsgdata/mmsgdata01' AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED；
```

下面的两个命令也可以：

```shell
alter tablespace mmsg add datafile '/opt/oracle/admin/mmsgdb/mmsgdata/mmsgdata01' size 1024M reuse;
alter database datafile '/opt/oracle/admin/mmsgdb/mmsgdata/mmsgdata01' resize 2048M;
```

