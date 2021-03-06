---
layout:     post
title:      "Oracle案例--错误码之ORA-32004"
subtitle:   "Oracle error code troubleshoot--ORA-32004"
date:       2011-03-04
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# ORA-32004  案例


## 表象

启动数据库时，报错误码：ORA-32004

```
SQL> startup
ORA-32004: obsolete and/or deprecated parameter(s) specified
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
数据库已经打开。
SQL> 
```

启动数据库，收到ORA-32004错误码，多是过时的且不在当前系统中使用的参数导致，遇见这类问题，直接reset即可。

## 原因

错误码分析

```
oracle@mmsc103:~> oerr ora 32004
32004, 00000, "obsolete and/or deprecated parameter(s) specified"
// *Cause:  One or more obsolete and/or parameters were specified in 
//          the SPFILE or the PFILE on the server side.
// *Action: See alert log for a list of parameters that are obsolete.
//          or deprecated. Remove them from the SPFILE or the server 
//          side PFILE.
oracle@mmsc103:~> 
```

查看告警日志

```
<msg time='2011-03-04T10:11:39.436+08:00' org_id='oracle' comp_id='rdbms'
 msg_id='kspdmp:13638:2661745733' type='WARNING' group='system_param'
 level='16' pid='5220'>
 <txt>Deprecated system parameters with specified values:
 </txt>
</msg>
<msg time='2011-03-04T10:11:39.437+08:00' org_id='oracle' comp_id='rdbms'
 msg_id='kspdmp:13644:2633769647' type='WARNING' group='system_param'
 level='16' pid='5220'>
 <txt>  log_archive_start        
 </txt>
</msg>
<msg time='2011-03-04T10:11:39.437+08:00' org_id='oracle' comp_id='rdbms'
 msg_id='kspdmp:13652:3788363585' type='WARNING' group='system_param'
 level='16' pid='5220'>
 <txt>End of deprecated system parameter listing
 </txt>
</msg>
```

## 解决方法

从spfile文件中清除过时的参数，重启数据库

```
SQL> alter system reset log_archive_start scope=spfile sid='*';

系统已更改。

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup       #重启后未报错
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
数据库装载完毕。
数据库已经打开。
SQL>
```

查看当前版本不再使用的参数信息

```
select name,description from v$parameter where isdeprecated='TRUE'
 
```
<img class="shadow" src="/img/in-post/oracle-parameter.png" width="600">

