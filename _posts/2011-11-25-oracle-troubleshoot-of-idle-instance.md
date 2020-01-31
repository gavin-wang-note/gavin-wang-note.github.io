---
layout:     post
title:      "Oracle案例--Oracle已启动，dba连接报空闲实例"
subtitle:   "Oracle troubleshoot of idle instance"
date:       2011-11-25
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# Oracle已启动，dba连接报空闲实例

## 表象

Oracle服务的启动是VCS5.1启动的，VCS启动日志中显示数据库已经成功启动，且双机运行正常，但是，使用dba用户连接数据库时，报连接到空闲实例，如下：

```
oracle@dlsc01:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on Fri Nov 25 09:31:17 2011

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

Connected to an idle instance.

SQL>
```

查看oracle进程，进程存在，且正常

```
oracle@dlsc01:~> ps -ef | grep oracle
oracle     301     1  0 Nov18 ?        00:00:03 ora_dbw0_dlscdb
oracle     305     1  0 Nov18 ?        00:00:09 ora_lgwr_dlscdb
oracle     309     1  0 Nov18 ?        00:00:49 ora_ckpt_dlscdb
oracle     313     1  0 Nov18 ?        00:00:03 ora_smon_dlscdb
oracle     317     1  0 Nov18 ?        00:00:00 ora_reco_dlscdb
oracle     321     1  0 Nov18 ?        00:00:07 ora_mmon_dlscdb
oracle     325     1  0 Nov18 ?        00:00:00 ora_mmnl_dlscdb
oracle     387     1  0 Nov18 ?        00:00:01 ora_arc0_dlscdb
oracle     391     1  0 Nov18 ?        00:00:07 ora_arc1_dlscdb
oracle     395     1  0 Nov18 ?        00:00:01 ora_arc2_dlscdb
oracle     399     1  0 Nov18 ?        00:00:00 ora_arc3_dlscdb
oracle     403     1  0 Nov18 ?        00:00:00 ora_fbda_dlscdb
oracle     411     1  0 Nov18 ?        00:00:00 ora_qmnc_dlscdb
oracle     458     1  0 Nov18 ?        00:00:01 /home/oracle/product/11g/bin/tnslsnr LISTENER -inherit
oracle     465     1  0 Nov18 ?        00:11:44 ora_cjq0_dlscdb
oracle     659     1  0 Nov18 ?        00:00:00 ora_q000_dlscdb
oracle     663     1  0 Nov18 ?        00:00:00 ora_q001_dlscdb
oracle    2045     1  0 Nov18 ?        00:00:00 ora_smco_dlscdb
oracle   17630     1  0 09:25 ?        00:00:00 ora_w000_dlscdb
root     18771 18770  0 09:30 ?        00:00:00 login -- oracle              
oracle   18772 18771  0 09:30 pts/2    00:00:00 -bash
oracle   19150 18772  0 09:31 pts/2    00:00:00 sqlplus   as sysdba
oracle   19153 19150  0 09:31 ?        00:00:00 oracledlscdb (DESCRIPTION=(LOCAL=YES)(ADDRESS=(PROTOCOL=beq)))
oracle   19242     1  0 09:32 ?        00:00:00 ora_j000_dlscdb
oracle   19370 19150  0 09:32 pts/2    00:00:00 /bin/bash
oracle   19385 19370  0 09:32 pts/2    00:00:00 ps -ef
oracle   19386 19370  0 09:32 pts/2    00:00:00 grep oracle
oracle   32739     1  0 Nov18 ?        00:00:00 ora_pmon_dlscdb
oracle   32743     1  0 Nov18 ?        00:00:00 ora_vktm_dlscdb
oracle   32749     1  0 Nov18 ?        00:00:00 ora_diag_dlscdb
oracle   32753     1  0 Nov18 ?        00:00:00 ora_dbrm_dlscdb
oracle   32757     1  0 Nov18 ?        00:00:00 ora_psp0_dlscdb
oracle   32761     1  0 Nov18 ?        00:00:02 ora_dia0_dlscdb
oracle   32765     1  0 Nov18 ?        00:00:01 ora_mman_dlscdb
```

由进程信息，可以看出，数据库的SID为dlscdb，查看环境变量中的sid

```
oracle@dlsc01:~> echo $ORACLE_SID
dlscdb
```

启动的数据库SID与环境变量中的SID一致，数据库为单实例，不存在多实例问题，所以连接异常问题不是SID不一致导致的。

## 原因

Oracle使用的环境变量.profile文件中，设置的ORACLE_HOME中多加了个/

```export ORACLE_HOME=$ORACLE_BASE/product/11g/ ```

## 解决方法

修改环境变量文件中的.profile文件中的ORACLE_HOM的环境变量，去掉多余的/“”，并source环境变量文件。

```
oracle@dlsc01:~> source .profile
oracle@dlsc01:~> echo $ORACLE_HOME
/home/oracle/product/11g

oracle@dlsc01:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on Fri Nov 25 09:48:07 2011

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL>
```

说明
* 上述现象仅在使用VCS启动数据库时出现，手工启动数据库不出现上述问题。
* 在oracle环境中，不论资料还是具体的测试环境，对于预设的oracle环境变量，避免在路径末尾加个“/”。
