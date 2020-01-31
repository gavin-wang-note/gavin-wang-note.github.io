---
layout:     post
title:      "Oracle案例--错误码之ORA-27046"
subtitle:   "Oracle error code troubleshoot--ORA-27046"
date:       2011-04-26
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# ORA-27046  错误码解决方法

## 背景

当前数据库undo表空间使用undotbs1，数据文件大小已大26G，严重占用系统分区空间。为了解决这个问题，重新创建另外一个undo表空间，并使数据库在使用新的undo表空间启动。在使用新的undo表空间前，创建pfile文件，结果就出现了本文描述的问题。

## 现象

通过spfile文件创建pfile，报ORA-27046

```
SQL> create pfile='/home/oracle/product/11g/dbs/pfile' from spfile;
create pfile='/home/oracle/product/11g/dbs/pfile' from spfile
*
ERROR at line 1:
ORA-01565: 标识文件 '?/dbs/spfile@.ora' 时出错
ORA-27046: 文件大小不是逻辑块大小的倍数
Additional information: 1
```

## 原因分析

出现这个原因，往往是因为spfile文件被破坏导致的。Spfile文件是一个二进制文件，不能修改，一旦修改，则使用该spfile文件启动数据库时，数据库是无法启动的。即：修改了spfile文件后，该文件报废。

## 解决方法

方法1：使用admin下init文件启动数据库，并重新创建spfile文件；

方法2：将现有的spfile文件中的有效内容拷贝到文本文件中，使用该文本文件启动数据库后并重新创建spfile文件。

