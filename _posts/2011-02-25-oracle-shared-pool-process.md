---
layout:     post
title:      "Oracle Shared Pool与Processes参数的关系"
subtitle:   "Shared Pool and Processes"
date:       2011-02-25
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 前言

大家都知道，我们使用ORACLE数据库时，常常会为实例配置一个processes参数，此参数故名思意，就是设置整个数据库系统可以启动多少个进程(包括系统自己的后台进程)

设置不合理的processes参数值，会导致实例无法启动。此参数还有其它许许多多的含义和作用，影响着数据库系统的运行。

比如，ORACLE在哪里为其分配内存,分配多大内存？此内存信息在ORACLE instance级的作用？为什么processes参数是一个静态参数？

通过本文，相信大家能找到一个的答案。下面是通过一些测试，来回答上述问题。

# 实践

## 测试环境

```
OS: SUSE Linux Enterprise Server 10 SP1 (x86_64) Kernel 2.6.16.46-0.12-smp (1)
ORACLE VERSION: Release 11.1.0.6.0
```

## 修改processes

```
SQL> alter system set processes=20000 scope=spfile;

系统已更改。

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。


oracle@mmsc101:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期五 6月 24 11:17:55 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

已连接到空闲例程。

SQL> startup nomount
ORA-27154: post/wait create failed
ORA-27300: OS system dependent operation:semids_per_proc failed with status: 0
ORA-27301: OS failure message: Error 0
ORA-27302: failure occurred at: sskgpwcr2
ORA-27303: additional information: semids = 132, maxprocs = 20000
SQL>
```

从上面的错误说明，oracle会根据processes参数的值在共享池中分配一定数量的内存，参数值越大，分配的内存也越多。

## 修改process

修改process为300，重启数据库，查看shared pool  中processes值

```
SQL> show parameter processes

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
aq_tm_processes                      integer     0
db_writer_processes                  integer     1
gcs_server_processes                 integer     0
global_txn_processes                 integer     1
job_queue_processes                  integer     1000
log_archive_max_processes            integer     4
processes                            integer     300


SQL> select * from v$sgastat where pool='shared pool' and name like '%process%';

POOL         NAME                            BYTES
------------ -------------------------- ----------
shared pool  generic process shared st         456
shared pool  ksb ci process list (each         688
shared pool  process count for each CI         320
shared pool  dia* process descriptor            16
shared pool  ksb cic process list              632
shared pool  Background process state           48
shared pool  process group array             66704
shared pool  ksb process so list               632
shared pool  processes                        2400  --300个进程要在共享池中分配2400字节

已选择9行。
```

修改process为100，重启数据库，查看shared pool  中processes值

```
SQL> alter system set processes = 100 scope=spfile;

系统已更改。
重启数据库后
SQL> show parameter processes 

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
aq_tm_processes                      integer     0
db_writer_processes                  integer     1
gcs_server_processes                 integer     0
global_txn_processes                 integer     1
job_queue_processes                  integer     1000
log_archive_max_processes            integer     4
processes                            integer     100
SQL>

SQL> select * from v$sgastat where pool='shared pool' and name like '%process%';

POOL         NAME                            BYTES
------------ -------------------------- ----------
shared pool  generic process shared st         456
shared pool  ksb ci process list (each         688
shared pool  process count for each CI         320
shared pool  dia* process descriptor            16
shared pool  ksb cic process list              632
shared pool  Background process state           48
shared pool  process group array             66704
shared pool  ksb process so list               632
shared pool  processes                         800  --100个进程要在共享池中分配800字节

已选择9行。
```
从上面两次修改processes参数的值，可以看出每个进程将会在shared pool中分配8字节内存，那此8字节信息是什么呢？

我们查看如下的v$process视图

```
SQL>  desc v$process;
 名称                                      是否为空? 类型
 ----------------------------------------- -------- ----------------------------
 ADDR                                               RAW(8)
 PID                                                NUMBER
 SPID                                               VARCHAR2(24)
 USERNAME                                           VARCHAR2(15)
 SERIAL#                                            NUMBER
 TERMINAL                                           VARCHAR2(30)
 PROGRAM                                            VARCHAR2(48)
 TRACEID                                            VARCHAR2(255)
 TRACEFILE                                          VARCHAR2(513)
 BACKGROUND                                         VARCHAR2(1)
 LATCHWAIT                                          VARCHAR2(16)
 LATCHSPIN                                          VARCHAR2(16)
 PGA_USED_MEM                                       NUMBER
 PGA_ALLOC_MEM                                      NUMBER
 PGA_FREEABLE_MEM                                   NUMBER
 PGA_MAX_MEM                                        NUMBER


SQL> select addr from v$process;

ADDR
----------------
00000000BF4EB598
00000000BF4EC588
00000000BF4ED578
00000000BF4EE568
00000000BF4EF558
00000000BF4F0548
00000000BF4F1538
00000000BF4F2528
00000000BF4F3518
00000000BF4F4508
00000000BF4F54F8

ADDR
----------------
00000000BF4F64E8
00000000BF4F74D8
00000000BF4F84C8
00000000BF4F94B8
00000000BF4FA4A8
00000000BF4FB498
00000000BF4FC488
00000000BF4FD478
00000000BF4FE468
00000000BF4FF458
00000000BF500448

已选择22行。

SQL>
```

字段ADDR字段刚好为8字节 ,在共享池中保存process进程的信息很有可能就是其地址信息，知道了其地址，也就知道了PGA在哪里，从PGA里的数据结构就可以知道系统进程号等等之类的东西。PMON进程也是利用此信息，在pmon timer到来之际，通过地址信息检查各数据库服务器进程的状态；

此地址信息也是执行alter system kill session命令的重要纽带。怎样从Shared Pool到PGA，或者说怎样从PGA到Shared Pool?共享池中保存process进程的信息成了关键性的作用。

顺便提一句，在ORACLE 9i之上，共享池划分了很多的subpool,在实例启动时，oracle根据processes参数的值，只会挑选其中一个子池来保留此信息

为什么processes参数是一个静态参数？这跟ORACLE关于此参数的内存申请很有关系，个人猜想，此控制结构的信息是以数组的方式保存的，大家都知道数组结构是不能动态扩大的，不像队列或者线性链表。


db_cache与pga之间走的是数据流；shared pool保存的一些信息，可以看成了对pga的控制流。

刚才查看了64位AIX 6.1操作系统

```
SQL> show parameter processes

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
aq_tm_processes                      integer     0
db_writer_processes                  integer     2
gcs_server_processes                 integer     0
global_txn_processes                 integer     1
job_queue_processes                  integer     1000
log_archive_max_processes            integer     4
processes                            integer     150
SQL> select * from v$sgastat where pool='shared pool' and name like '%process%';

POOL         NAME                            BYTES
------------ -------------------------- ----------
shared pool  ksb ci process list (each         688
shared pool  generic process shared st          96
shared pool  processes                        1200
shared pool  dia* process descriptor            16
shared pool  ksb process so list               632
shared pool  process count for each CI         320
shared pool  ksb cic process list              632
shared pool  Background process state           48
shared pool  process group array             66448

已选择9行。
```

AIX5.3

```
% sqlplus "/ as sysdba"

SQL*Plus: Release 9.2.0.8.0 - Production on Fri Jun 24 12:01:48 2011

Copyright (c) 1982, 2002, Oracle Corporation.  All rights reserved.


Connected to:
Oracle9i Enterprise Edition Release 9.2.0.8.0 - 64bit Production
JServer Release 9.2.0.6.0 - Production

SQL>
SQL> show parameter processes

NAME                                 TYPE                   VALUE
------------------------------------ ---------------------- ------------------------------
aq_tm_processes                      integer                1
db_writer_processes                  integer                1
job_queue_processes                  integer                20
log_archive_max_processes            integer                2
processes                            integer                1000

SQL> select * from v$sgastat where pool='shared pool' and name like '%process%';

POOL                   NAME                                                      BYTES
---------------------- ---------------------------------------------------- ----------
shared pool            processes                                               1368000
```

oracle11g数据库，AIX6.1系统，为每个进程在共享池中分配8字节；oracle9i数据库，AIX5.3系统每个进程在共享池中分配1368字节，看来这个分配，跟OS，与ORACLE版本都很有关系的。

