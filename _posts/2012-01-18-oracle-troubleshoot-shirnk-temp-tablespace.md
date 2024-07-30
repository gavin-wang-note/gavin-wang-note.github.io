---
layout:     post
title:      "Oracle案例--表空间--收缩临时表空间"
subtitle:   "Oracle tablespace troubleshoot--Shrink temporary tablespace"
date:       2012-01-18
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 收缩临时表空间

从oracle 11g R1版本开始，新增对历史表空间的shrink操作。目的是：当临时表空间扩展过大时（临时表空间主要用于排序操作，当需要的空间不足时，会自动扩展【前提是允许临时表空间自动扩展】，排完序后，已经扩展的空间不会回缩，这样就会导致临时表空间不断变大），占用磁盘空间，可以适当的对临时表空间进行压缩。

shrink操作只适用于临时表空间，收缩临时表空间有两种方法：

## 方法一：使用keep子句

```shell
SQL> alter tablespace  MMSG_TMP shrink space keep 20M;

表空间已更改。

SQL>
```

## 方法二：自动将临时表空间压缩至最小

```shell
SQL> alter tablespace  YJH_TMP shrink tempfile '/home/yjh/oradata/yjhdata02';
```

附：

查询临时表空间名称与大小SQL语句

```shell
select t1.file_name,t1.tablespace_name,t2.bytes/1024/1024 from dba_temp_files t1,v$tempfile t2 where t1.file_name=t2.name
```
