---
layout:     post
title:      "Oracle案例--表空间--UNDO表空间膨胀"
subtitle:   "Oracle tablespace troubleshoot--UNDO space collision"
date:       2011-02-06
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# UNDO表空间过大

## 现象

## 查看UNDO表空间名称

```shell
SQL> show parameter undo_tablespace  

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
undo_tablespace                      string      UNDOTBS1
SQL>
```

### 查看当前UNDO表空间大小

```shell
SQL> select bytes/1024/1024 from dba_data_files where tablespace_name like 'UNDO%';

BYTES/1024/1024
---------------
           5745

SQL>
```

### 检查UNDO Segment状态

```shell
SQL> select usn,xacts,rssize/1024/1024/1024,hwmsize/1024/1024/1024,shrinks from v$rollstat order by rssize;

       USN      XACTS RSSIZE/1024/1024/1024 HWMSIZE/1024/1024/1024    SHRINKS
---------- ---------- --------------------- ---------------------- ----------
         0          0            .000358582             .000358582          0
         3          0            .004020691             .030387878         92
         2          0            .004997253             .029411316         80
         9          0            .004997253             .037223816         82
         6          0            .004997253             .027458191         77
         7          0            .004997253             .028434753         85
         1          0            .005973816             .026481628         80
        10          0            .005973816             .028434753         78
         4          0            .006950378             .028434753         84
         8          0            .009880066             .028434753         82
         5          0            .013786316             .028434753         88

11 rows selected.

SQL>
```

如果表空间过大，最终将mount点free空间消耗完，oracle最终将因系统空间不足而崩溃。

## 解决方法

### 重新创建新的UNDO表空间

```shell
create undo tablespace undotbs1 
datafile '/opt/oracle/oradata/mmsgdb/UNDOTBS2.dbf' size 1000m reuse 
autoextend on next 800m maxsize unlimited;
```

注：
* 一般不建议这么创建，一次性给予undo表空间足够大的空间，并关闭自动增长。

### 修改pfile文件

```shell
SQL> alter system set undo_tablespace=undotbs2 scope=both;
```

### 等待原UNDO表空间所有UNDO SEGMENT OFFLIN

```shell
SQL> select usn,xacts,rssize/1024/1024/1024,hwmsize/1024/1024/1024,shrinks from v$rollstat order by rssize;
```

注：
* 创建好新的UNDO表空间后，不能立即删除原有的UNDO表空间，等到所有的回滚段offline或者达到undo_retention设定值后，方可执行drop掉旧的undo表空间。

### 删除旧的undo表空间

```shell
SQL> drop tablespace undotbs1 including contents and datafiles;
```

### 确认删除是否成功

```shell
SQL>select * from dba_data_files where tablespace_name like ‘UNDO%’;
```

