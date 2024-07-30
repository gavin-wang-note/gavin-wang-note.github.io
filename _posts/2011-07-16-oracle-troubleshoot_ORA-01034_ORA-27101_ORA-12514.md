---
layout:     post
title:      "Oracle案例--错误码之ORA-01034  ORA-27101，ORA-12514"
subtitle:   "Oracle error code troubleshoot--ORA-01034  ORA-27101，ORA-12514"
date:       2011-07-16
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-01034  ORA-27101，ORA-12514解决方法

## 现象

```shell
ORA-01034: ORACLE not available
ORA-27101: shared memory realm does not exist
```

## 原因

（1）	一般是因为数据库未正常停止导致；

（2）	相关数据文件过大；

（3）	还有其它原因，具体原因请具体对待。

## 解决方法

这里以数据文件过大导致上述现象的解决方法，如下：

在数据文件存放路径目录下发现一个文件，undotbs01.dbf 大的惊人！ 16G

解决方法就是压缩这个undo文件。

```shell
SQL> startup   
ORACLE instance started.   
  
Total System Global Area  135338868 bytes   
Fixed Size                   453492 bytes   
Variable Size             109051904 bytes   
Database Buffers           25165824 bytes   
Redo Buffers                 667648 bytes   
Database mounted.   
ORA-01157: cannot identify/lock data file 2 - see DBWR trace file   
ORA-01110: data file 2: ''D:ORACLEORADATAORCLUNDOTBS01.DBF''  
  
  
SQL> alter system set undo_management=''MANUAL'' scope=spfile;   
  
System altered.   
  
SQL> alter database    
datafile ''d:oracleoradataorclundotbs01.dbf'' offline drop   
;   
  
Database altered.   
  
SQL> alter database open;   
  
Database altered.   
  
SQL>   
  
SQL>   
create undo tablespace undotbs2 datafile '   
'd:oracleoradataorclundotbs02.dbf'' size 100M;   
Tablespace created.   
SQL> select * from v?$tablespace;   
  
       TS# NAME                           INC   
---------- ------------------------------ ---   
         3 CWMLITE                        YES   
         4 DRSYS                          YES   
         5 EXAMPLE                        YES   
         6 INDX                           YES   
         7 ODM                            YES   
         0 SYSTEM                         YES   
         8 TOOLS                          YES   
         1 UNDOTBS1                       YES   
         9 USERS                          YES   
        10 XDB                            YES   
         2 TEMP                           YES   
  
       TS# NAME                           INC   
---------- ------------------------------ ---   
        11 UNDOTBS2                       YES   
  
12 rows selected.   
  
  
SQL> alter system set undo_management=''AUTO'' scope=spfile;   
  
System altered.   
  
SQL> alter system set undo_tablespace=''UNDOTBS2'' scope=spfile;   
  
System altered.   
  
SQL> shutdown immediate;   
Database closed.   
Database dismounted.   
ORACLE instance shut down.   
SQL> startup   
ORACLE instance started.   
  
Total System Global Area  135338868 bytes   
Fixed Size                   453492 bytes   
Variable Size             109051904 bytes   
Database Buffers           25165824 bytes   
Redo Buffers                 667648 bytes   
Database mounted.   
Database opened.   
SQL> show parameter undo   
  
NAME                                 TYPE        VALUE   
------------------------------------ ----------- -----   
undo_management                      string      AUTO   
undo_retention                       integer     10800   
undo_suppress_errors                 boolean     FALSE   
undo_tablespace                      string      UNDOTBS2   
SQL>  
SQL> startup
ORACLE instance started.

Total System Global Area  135338868 bytes
Fixed Size                   453492 bytes
Variable Size             109051904 bytes
Database Buffers           25165824 bytes
Redo Buffers                 667648 bytes
Database mounted.
ORA-01157: cannot identify/lock data file 2 - see DBWR trace file
ORA-01110: data file 2: ''D:ORACLEORADATAORCLUNDOTBS01.DBF''


SQL> alter system set undo_management=''MANUAL'' scope=spfile;

System altered.

SQL> alter database 
datafile ''d:oracleoradataorclundotbs01.dbf'' offline drop
;

Database altered.

SQL> alter database open;

Database altered.

SQL>

SQL>
create undo tablespace undotbs2 datafile '
'd:oracleoradataorclundotbs02.dbf'' size 100M;
Tablespace created.
SQL> select * from v?$tablespace;

       TS# NAME                           INC
---------- ------------------------------ ---
         3 CWMLITE                        YES
         4 DRSYS                          YES
         5 EXAMPLE                        YES
         6 INDX                           YES
         7 ODM                            YES
         0 SYSTEM                         YES
         8 TOOLS                          YES
         1 UNDOTBS1                       YES
         9 USERS                          YES
        10 XDB                            YES
         2 TEMP                           YES

       TS# NAME                           INC
---------- ------------------------------ ---
        11 UNDOTBS2                       YES

12 rows selected.


SQL> alter system set undo_management=''AUTO'' scope=spfile;

System altered.

SQL> alter system set undo_tablespace=''UNDOTBS2'' scope=spfile;

System altered.

SQL> shutdown immediate;
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup
ORACLE instance started.

Total System Global Area  135338868 bytes
Fixed Size                   453492 bytes
Variable Size             109051904 bytes
Database Buffers           25165824 bytes
Redo Buffers                 667648 bytes
Database mounted.
Database opened.
SQL> show parameter undo

NAME                                 TYPE        VALUE
------------------------------------ ----------- -----
undo_management                      string      AUTO
undo_retention                       integer     10800
undo_suppress_errors                 boolean     FALSE
undo_tablespace                      string      UNDOTBS2
SQL>
```

完成以上操作后，重新启动oracle。

