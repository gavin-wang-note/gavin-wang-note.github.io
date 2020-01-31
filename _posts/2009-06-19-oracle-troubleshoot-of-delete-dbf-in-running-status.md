---
layout:     post
title:      "Oracle案例--删除正在运行数据库的DBF文件导致数据库启动异常（ORA-01157，ORA-01110）"
subtitle:   "Oracle troubleshoot of delete dbf which is in running status"
date:       2009-06-19
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 删除DBF导致实例启动失败

## 表象

未通过正确渠道、直接删除了数据库正在使用的数据文件，导致数据库启动实例时出错。

```
SQL> startup
ORACLE instance started.
Total System Global Area  320309728 bytes
Fixed Size                   731616 bytes
Variable Size             285212672 bytes
Database Buffers           33554432 bytes
Redo Buffers                 811008 bytes
Database mounted.
ORA-01157: cannot identify/lock data file 14 - see DBWR trace file
ORA-01110: data file 14: '/opt/oracle/oradata/mmsgdb/mmsgdata01'
```

## 解决方法

脱机相关数据文件后，重新启动数据库。具体步骤如下：

### 将该数据文件脱机

```
SQL>alter database datafile '/opt/oracle/oradata/mmsgdb/mmsgdata01' offline drop;
```

### 关闭数据库后重新启动则恢复正常

drop相应的Tablespace释放资源

```
SQL>drop tablespace MMSG including contents and datafiles;
```

其中MMSG是此数据库数据文件mmsgdata01对应的表空间名称。

