---
layout:     post
title:      "Oracle案例--错误码之ORA-01536"
subtitle:   "Oracle error code troubleshoot--ORA-01536"
date:       2011-07-20
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-01536 案例


## 表像

执行刷库脚本，创建表报错

```shell
SQL> SQL> SQL>   2    3    4    5    6  CREATE TABLE "ECTOSIINFO"
*
ERROR at line 1:
ORA-01536: space quota exceeded for tablespace 'MMSG'
```

## 原因分析

1、查看错误码

```shell
01536, 00000, "space quota exceeded for tablespace '%s'"
// *Cause:  The space quota for the segment owner in the tablespace has
//          been exhausted and the operation attempted the creation of a
//          new segment extent in the tablespace.
// *Action: Either drop unnecessary objects in the tablespace to reclaim
//          space or have a privileged user increase the quota on this
//          tablespace for the segment owner.
```

显示可能为表空间段扩展问题。

2、查看表空间使用率

观察一下表空间是否已经满了，无法自动扩展或者扩展已达配额

```shell
TABLESPACE_NAME                USED_SPACE TABLESPACE_SIZE USED_PERCENT
------------------------------ ---------- --------------- ------------
MMSG                                13384         4194302   .319099578
MMSG_TMP                                0           64000            0
```

MMSG表空间使用率很低啊，3.27G的空间只使用了104M

3、查看表空间限额

表空间限额和表空间是两个不同的概念，表空间限额约束了表空间的使用情况，如果表空间200M，表空间限额只分配20M，剩下的180M的空间能够被数据库所使用的空间就被浪费掉了。

```shell
SQL>select tablespace_name,username,bytes,max_bytes from dba_ts_quotas;

TABLESPACE_NAME                USERNAME                            BYTES  MAX_BYTES
------------------------------ ------------------------------ ---------- ----------
IMAPLOGDB                      IMAPLOGDB                        12779520         -1
IMAPTMDB                       IMAPTMDB                           786432         -1
IMAPSMDB                       IMAPSMDB                          5177344         -1
SYSTEM                         IMAPUSER                                0         -1
ALARMDB                        ALARMDB                          17432576         -1
PERFDB                         PERFDB                          135135232         -1
NMSGUEST                       NMSGUEST                           262144         -1
PERFDB_IDX                     PERFDB_IDX                              0         -1
IMAP_DB                        IMAP_DB                          53739520         -1
已选择9行。

SQL>
```

发现并没有对表空间MMSG有限额分配的信息，推论表空间MMSG应该使用默认的分配限额（具体是多少，暂时不知）。

## 解决方法

为表空间分配使用限额，设置扩大或者不限制。方法如下：

```alter user mmsg quota unlimited on MMSG; ```

或者

```grant unlimited tablespace to MMSG;```

