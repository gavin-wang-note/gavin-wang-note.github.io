---
layout:     post
title:      "Oracle案例--控制文件损坏如何恢复"
subtitle:   "Oracle troubleshoot--controll file recovery"
date:       2010-12-24
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 概述

本文介绍控制文件的损坏与恢复操作方法，控制文件的损坏分为损坏部分控制文件和全部控制文件损坏。

# 部分控制文件损坏的恢复

损坏部分控制文件，只要还有其他的可用的控制文件，在关闭数据库情况下，将可用的控制文件拷贝并重命名即可。

具体操作如下：

## 步骤一  启动数据库报错

```
SQL> alter session set nls_language = american;

Session altered.

SQL> shutdown immediate
ORA-01507: database not mounted


ORACLE instance shut down.
SQL> startup
ORACLE instance started.

Total System Global Area 6747725824 bytes
Fixed Size                  2160312 bytes
Variable Size            4362078536 bytes
Database Buffers         2348810240 bytes
Redo Buffers               34676736 bytes
ORA-00205: ?????????, ??????, ???????


SQL>
```
 
## 步骤二  查看错误码

```
oracle@mmsg02:~> oerr ora 00205
00205, 00000, "error in identifying control file, check alert log for more info"
// *Cause:  The system could not find a control file of the specified name and
//         size.
// *Action: Check that ALL control files are online and that they are the same
//         files that the system created at cold start time.
```

## 步骤三  查看trace日志，获取更详细信息

```
oracle@mmsg02:~/diag/rdbms/infoxdb/infoxdb/alert> vi /home/oracle/diag/rdbms/infoxdb/infoxdb/trace/infoxdb_m000_2951.trc

Trace file /home/oracle/diag/rdbms/infoxdb/infoxdb/trace/infoxdb_m000_2951.trc
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining,
Oracle Database Vault and Real Application Testing options
ORACLE_HOME = /home/oracle/product/11g/db
System name:    Linux
Node name:      mmsg02
Release:        2.6.16.46-0.12-smp
Version:        #1 SMP Thu May 17 14:00:09 UTC 2007
Machine:        x86_64
Instance name: infoxdb
Redo thread mounted by this instance: 0 <none>
Oracle process number: 19
Unix process pid: 2951, image: oracle@mmsg02 (m000)


*** 2010-12-24 12:25:25.526
*** SESSION ID:(648.5) 2010-12-24 12:25:25.526
*** CLIENT ID:() 2010-12-24 12:25:25.526
*** SERVICE NAME:() 2010-12-24 12:25:25.526
*** MODULE NAME:(MMON_SLAVE) 2010-12-24 12:25:25.526
*** ACTION NAME:(DDE async action) 2010-12-24 12:25:25.526

========= Dump for error ORA 202 (no incident) ========
----- DDE Action: 'DB_STRUCTURE_INTEGRITY_CHECK' (Async) -----
DDE: Problem Key 'ORA 202' was flood controlled (0x1) (no incident)
ORA-00202: ????: ''/home/oracle/oradata/infoxdb/control01.ctl''
ORA-27048: skgfifi: ????????
DDE: Problem Key 'ORA 202' was flood controlled (0x1) (no incident)
ORA-00202: ????: ''/home/oracle/oradata/infoxdb/control02.ctl''
ORA-27048: skgfifi: ????????
ORA-00210: ???????????
ORA-00202: ????: ''/home/oracle/oradata/infoxdb/control01.ctl''
ORA-27048: skgfifi: ????????
kcidr_process_controlfile_error:
 IO Check was called but no error was found
ORA-00210: ???????????
ORA-00202: ????: ''/home/oracle/oradata/infoxdb/control02.ctl''
ORA-27048: skgfifi: ????????
ORA-00210: ???????????
ORA-00202: ????: ''/home/oracle/oradata/infoxdb/control01.ctl''
ORA-27048: skgfifi: ????????
kcidr_process_controlfile_error:
 IO Check was called but no error was found
ORA-00210: ???????????
ORA-00202: ????: ''/home/oracle/oradata/infoxdb/control02.ctl''
ORA-27048: skgfifi: ????????
ORA-00210: ???????????
ORA-00202: ????: ''/home/oracle/oradata/infoxdb/control01.ctl''
ORA-27048: skgfifi: ????????
-------------------------------------------------------
```

由上可知，控制文件被损坏，被损坏的控制文件分别是control01.ctl和control02.ctl

## 步骤四  检查是否有可用的控制文件

这里由于日志未报控制文件control03.ctl出错，可以推断控制文件3是好的，也可以检查一下：

```
oracle@mmsg02:~/oradata/infoxdb> dbv file=control03.ctl  blocksize=16384

DBVERIFY: Release 11.1.0.7.0 - Production on 星期五 12月 24 12:33:39 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

DBVERIFY - 开始验证: FILE = /home/oracle/oradata/infoxdb/control03.ctl


DBVERIFY - 验证完成

检查的页总数: 602
处理的页总数 (数据): 0
失败的页总数 (数据): 0
处理的页总数 (索引): 0
失败的页总数 (索引): 0
处理的页总数 (其它): 40
处理的总页数 (段)  : 0
失败的总页数 (段)  : 0
空的页总数: 562
标记为损坏的总页数: 0
流入的页总数: 0
加密的总页数        : 0
最高块 SCN            : 5771 (65535.5771)
oracle@mmsg02:~/oradata/infoxdb> 
oracle@mmsg02:~/oradata/infoxdb> dbv file=control02.ctl  blocksize=16384

DBVERIFY: Release 11.1.0.7.0 - Production on 星期五 12月 24 12:33:44 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


DBV-00107: 未知标头格式 (11) (201326603)
oracle@mmsg02:~/oradata/infoxdb> dbv file=control01.ctl  blocksize=16384

DBVERIFY: Release 11.1.0.7.0 - Production on 星期五 12月 24 12:33:53 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


DBV-00107: 未知标头格式 (11) (201326603)
dbv检查控制文件1和2，发现控制文件1和2被损坏，和日志正好吻合。
```

## 步骤五  替换被损坏的控制文件，并启动数据库

```
SQL> shutdown immediate
ORA-01507: database not mounted


ORACLE instance shut down.
SQL> host
oracle@mmsg02:~> cd oradata/infoxdb/
oracle@mmsg02:~/oradata/infoxdb> mv control01.ctl bak_control01.ctl
oracle@mmsg02:~/oradata/infoxdb> mv control02.ctl bak_control02.ctl
oracle@mmsg02:~/oradata/infoxdb> cp control03.ctl control01.ctl
oracle@mmsg02:~/oradata/infoxdb> cp control03.ctl control02.ctl
oracle@mmsg02:~/oradata/infoxdb> l
total 6233266
drwxrwxrwx 2 oracle oinstall        616 Dec 24 12:35 ./
drwxrwxrwx 3 oracle oinstall         72 Dec 19 19:37 ../
-rw-r----- 1 oracle oinstall 1048584192 Dec 18 11:17 INFOX_GNSROUTE_DATA.dbf
-rw-r----- 1 oracle oinstall    9879552 Dec 23 22:16 bak_control01.ctl
-rw-r----- 1 oracle oinstall    9879552 Dec 23 22:16 bak_control02.ctl
-rw-r----- 1 oracle oinstall    9879552 Dec 24 12:34 control01.ctl
-rw-r----- 1 oracle oinstall    9879552 Dec 24 12:35 control02.ctl
-rw-r----- 1 oracle oinstall    9879552 Dec 23 22:16 control03.ctl
-rw-r----- 1 oracle oinstall  209723392 Dec 23 22:15 data20
-rw-r----- 1 oracle oinstall  209723392 Dec 23 22:05 data21
-rw-r----- 1 oracle oinstall  209723392 Dec 23 22:05 data22
-rw-r----- 1 oracle oinstall   31465472 Dec 22 16:11 data23
-rw-r----- 1 oracle oinstall   52429312 Dec 23 22:08 redo01.log
-rw-r----- 1 oracle oinstall   52429312 Dec 23 22:16 redo02.log
-rw-r----- 1 oracle oinstall   52429312 Dec 23 21:56 redo03.log
-rw-r----- 1 oracle oinstall  744497152 Dec 23 22:16 sysaux01.dbf
-rw-r----- 1 oracle oinstall 3523223552 Dec 23 22:16 system01.dbf
-rw-r----- 1 oracle oinstall   29368320 Dec 23 22:11 temp01.dbf
-rw-r----- 1 oracle oinstall  214966272 Dec 23 22:16 undotbs01.dbf
-rw-r----- 1 oracle oinstall    5251072 Dec 23 22:05 users01.dbf
oracle@mmsg02:~/oradata/infoxdb> exit
exit

SQL> startup mount
ORACLE instance started.

Total System Global Area 6747725824 bytes
Fixed Size                  2160312 bytes
Variable Size            4362078536 bytes
Database Buffers         2348810240 bytes
Redo Buffers               34676736 bytes
Database mounted.
SQL> alter session set nls_language=american;

Session altered.

SQL> alter database open;

Database altered.

SQL> select * from dba_data_files;
```

说明：
* 1、损失单个控制文件是比较简单的，因为数据库中所有的控制文件都是镜相的，只需要简单的拷贝一个好的就可以了
* 2、建议镜相控制文件在不同的磁盘上
* 3、建议多做控制文件的备份，长期保留一份由alter database backup control file to trace产生的控制文件的文本备份

# 所有控制文件损坏的恢复

损坏所有的控制文件或者人为的删除所有的控制文件，通过备份复制已经不能解决问题，只能重新建立新的控制文件。

使用具有dba权限的用户重新创建新控制文件，需要列出控制文件、数据文件、重做日志文件的路径信息，或者使用alter database backup controlfile to trace中产生的trace日志，修改这段日志脚本，使用该脚本重新创建控制文件。

具体测试步骤如下：

## 步骤一 alter database backup controlfile to trace

```
oracle@mmsc103:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期三 3月 9 09:05:25 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> alter database backup controlfile to trace;

数据库已更改。

SQL> 
```

## 步骤二 查看alter 和trace日志

```
<msg time='2011-03-09T09:06:22.712+08:00' org_id='oracle' comp_id='rdbms'
 client_id='' type='UNKNOWN' level='16'
 module='sqlplus@mmsc103 (TNS V1-V3)' pid='12477'>
 <txt>Backup controlfile written to trace file /opt/oracle/diag/rdbms/mmsgdb/mmsgdb/trace/mmsgdb_ora_12477.trc
 </txt>


oracle@mmsc103:~/diag/rdbms/mmsgdb/mmsgdb/alert> more /opt/oracle/diag/rdbms/mmsgdb/mmsgdb/trace/mmsgdb_ora_12477.trc
Trace file /opt/oracle/diag/rdbms/mmsgdb/mmsgdb/trace/mmsgdb_ora_12477.trc
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
ORACLE_HOME = /opt/oracle/product/11g
System name:    Linux
Node name:      mmsc103
Release:        2.6.16.46-0.12-smp
Version:        #1 SMP Thu May 17 14:00:09 UTC 2007
Machine:        x86_64
Instance name: mmsgdb
Redo thread mounted by this instance: 1
Oracle process number: 38
Unix process pid: 12477, image: oracle@mmsc103 (TNS V1-V3)

*** 2011-03-09 09:06:22.710
*** SESSION ID:(285.20924) 2011-03-09 09:06:22.710
*** CLIENT ID:() 2011-03-09 09:06:22.710
*** SERVICE NAME:(SYS$USERS) 2011-03-09 09:06:22.710
*** MODULE NAME:(sqlplus@mmsc103 (TNS V1-V3)) 2011-03-09 09:06:22.710
*** ACTION NAME:() 2011-03-09 09:06:22.710
 
-- The following are current System-scope REDO Log Archival related
-- parameters and can be included in the database initialization file.
--
-- LOG_ARCHIVE_DEST=''
-- LOG_ARCHIVE_DUPLEX_DEST=''
--
-- LOG_ARCHIVE_FORMAT=%t_%s_%r.dbf
--
-- DB_UNIQUE_NAME="mmsgdb"
--
-- LOG_ARCHIVE_CONFIG='SEND, RECEIVE, NODG_CONFIG'
-- LOG_ARCHIVE_MAX_PROCESSES=4
-- STANDBY_FILE_MANAGEMENT=MANUAL
-- STANDBY_ARCHIVE_DEST=?/dbs/arch
-- FAL_CLIENT=''
-- FAL_SERVER=''
--
-- LOG_ARCHIVE_DEST_10='LOCATION=USE_DB_RECOVERY_FILE_DEST'
-- LOG_ARCHIVE_DEST_10='OPTIONAL REOPEN=300 NODELAY'
-- LOG_ARCHIVE_DEST_10='ARCH NOAFFIRM NOEXPEDITE NOVERIFY SYNC'
-- LOG_ARCHIVE_DEST_10='REGISTER NOALTERNATE NODEPENDENCY'
-- LOG_ARCHIVE_DEST_10='NOMAX_FAILURE NOQUOTA_SIZE NOQUOTA_USED NODB_UNIQUE_NAME'
-- LOG_ARCHIVE_DEST_10='VALID_FOR=(PRIMARY_ROLE,ONLINE_LOGFILES)'
-- LOG_ARCHIVE_DEST_STATE_10=ENABLE
--
-- LOG_ARCHIVE_DEST_1='LOCATION=/opt/oracle/archivelog'
-- LOG_ARCHIVE_DEST_1='OPTIONAL REOPEN=300 NODELAY'
-- LOG_ARCHIVE_DEST_1='ARCH NOAFFIRM NOEXPEDITE NOVERIFY SYNC'
-- LOG_ARCHIVE_DEST_1='REGISTER NOALTERNATE NODEPENDENCY'
-- LOG_ARCHIVE_DEST_1='NOMAX_FAILURE NOQUOTA_SIZE NOQUOTA_USED NODB_UNIQUE_NAME'
-- LOG_ARCHIVE_DEST_1='VALID_FOR=(PRIMARY_ROLE,ONLINE_LOGFILES)'
-- LOG_ARCHIVE_DEST_STATE_1=ENABLE
--
-- Below are two sets of SQL statements, each of which creates a new
-- control file and uses it to open the database. The first set opens
-- the database with the NORESETLOGS option and should be used only if
-- the current versions of all online logs are available. The second
-- set opens the database with the RESETLOGS option and should be used
-- if online logs are unavailable.
-- The appropriate set of statements can be copied from the trace into
-- a script file, edited as necessary, and executed when there is a
-- need to re-create the control file.
--
--     Set #1. NORESETLOGS case
--
-- The following commands will create a new control file and use it
-- to open the database.
-- Data used by Recovery Manager will be lost.
-- Additional logs may be required for media recovery of offline
-- Use this only if the current versions of all online logs are
-- available.
-- After mounting the created controlfile, the following SQL
-- statement will place the database in the appropriate
-- protection mode:
--  ALTER DATABASE SET STANDBY DATABASE TO MAXIMIZE PERFORMANCE
STARTUP NOMOUNT
CREATE CONTROLFILE REUSE DATABASE "MMSGDB" NORESETLOGS  ARCHIVELOG
    MAXLOGFILES 16
    MAXLOGMEMBERS 3
    MAXDATAFILES 100
    MAXINSTANCES 8
    MAXLOGHISTORY 292
LOGFILE
  GROUP 1 '/opt/oracle/oradata/mmsgdb/redo01.log'  SIZE 50M,
  GROUP 2 '/opt/oracle/oradata/mmsgdb/redo02.log'  SIZE 50M,
  GROUP 3 '/opt/oracle/oradata/mmsgdb/redo03.log'  SIZE 50M
-- STANDBY LOGFILE
DATAFILE
  '/opt/oracle/oradata/mmsgdb/system01.dbf',
  '/opt/oracle/oradata/mmsgdb/sysaux01.dbf',
  '/opt/oracle/oradata/mmsgdb/undotbs01.dbf',
  '/opt/oracle/oradata/mmsgdb/users01.dbf',
  '/opt/oracle/oradata/mmsgdb/mmsgdata01',
  '/opt/oracle/oradata/mmsgdb/rman_data.dbf'
CHARACTER SET ZHS16GBK
;
-- Configure RMAN configuration record 1
VARIABLE RECNO NUMBER;
EXECUTE :RECNO := SYS.DBMS_BACKUP_RESTORE.SETCONFIG('CONTROLFILE AUTOBACKUP','ON');
-- Configure RMAN configuration record 2
VARIABLE RECNO NUMBER;
EXECUTE :RECNO := SYS.DBMS_BACKUP_RESTORE.SETCONFIG('RETENTION POLICY','TO RECOVERY WINDOW OF 10 DAYS');
-- Commands to re-create incarnation table
-- Below log names MUST be changed to existing filenames on
-- disk. Any one log file from each branch can be used to
-- re-create incarnation records.
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- Recovery is required if any of the datafiles are restored backups,
-- or if the last shutdown was not normal or immediate.
RECOVER DATABASE
-- All logs need archiving and a log switch is needed.
ALTER SYSTEM ARCHIVE LOG ALL;
-- Database can now be opened normally.
ALTER DATABASE OPEN;
-- Commands to add tempfiles to temporary tablespaces.
-- Online tempfiles have complete space information.
-- Other tempfiles may require adjustment.
ALTER TABLESPACE TEMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/temp01.dbf'
     SIZE 20971520  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER TABLESPACE MMSG_TMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/mmsgdata02'
     SIZE 524288000  REUSE AUTOEXTEND OFF;
ALTER TABLESPACE RMAN_TMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/rman_tmp.dbf'
     SIZE 20971520  REUSE AUTOEXTEND OFF;
-- End of tempfile additions.
--
--     Set #2. RESETLOGS case
--
-- The following commands will create a new control file and use it
-- to open the database.
-- Data used by Recovery Manager will be lost.
-- The contents of online logs will be lost and all backups will
-- be invalidated. Use this only if online logs are damaged.
-- After mounting the created controlfile, the following SQL
-- statement will place the database in the appropriate
-- protection mode:
--  ALTER DATABASE SET STANDBY DATABASE TO MAXIMIZE PERFORMANCE
STARTUP NOMOUNT
CREATE CONTROLFILE REUSE DATABASE "MMSGDB" RESETLOGS  ARCHIVELOG
    MAXLOGFILES 16
    MAXLOGMEMBERS 3
    MAXDATAFILES 100
    MAXINSTANCES 8
    MAXLOGHISTORY 292
LOGFILE
  GROUP 1 '/opt/oracle/oradata/mmsgdb/redo01.log'  SIZE 50M,
  GROUP 2 '/opt/oracle/oradata/mmsgdb/redo02.log'  SIZE 50M,
  GROUP 3 '/opt/oracle/oradata/mmsgdb/redo03.log'  SIZE 50M
-- STANDBY LOGFILE
DATAFILE
  '/opt/oracle/oradata/mmsgdb/system01.dbf',
  '/opt/oracle/oradata/mmsgdb/sysaux01.dbf',
  '/opt/oracle/oradata/mmsgdb/undotbs01.dbf',
  '/opt/oracle/oradata/mmsgdb/users01.dbf',
  '/opt/oracle/oradata/mmsgdb/mmsgdata01',
  '/opt/oracle/oradata/mmsgdb/rman_data.dbf'
CHARACTER SET ZHS16GBK
;
-- Configure RMAN configuration record 1
VARIABLE RECNO NUMBER;
EXECUTE :RECNO := SYS.DBMS_BACKUP_RESTORE.SETCONFIG('CONTROLFILE AUTOBACKUP','ON');
-- Configure RMAN configuration record 2
VARIABLE RECNO NUMBER;
EXECUTE :RECNO := SYS.DBMS_BACKUP_RESTORE.SETCONFIG('RETENTION POLICY','TO RECOVERY WINDOW OF 10 DAYS');
-- Commands to re-create incarnation table
-- Below log names MUST be changed to existing filenames on
-- disk. Any one log file from each branch can be used to
-- re-create incarnation records.
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- Recovery is required if any of the datafiles are restored backups,
-- or if the last shutdown was not normal or immediate.
RECOVER DATABASE USING BACKUP CONTROLFILE
-- Database can now be opened zeroing the online logs.
ALTER DATABASE OPEN RESETLOGS;
-- Commands to add tempfiles to temporary tablespaces.
-- Online tempfiles have complete space information.
-- Other tempfiles may require adjustment.
ALTER TABLESPACE TEMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/temp01.dbf'
     SIZE 20971520  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER TABLESPACE MMSG_TMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/mmsgdata02'
     SIZE 524288000  REUSE AUTOEXTEND OFF;
ALTER TABLESPACE RMAN_TMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/rman_tmp.dbf'
     SIZE 20971520  REUSE AUTOEXTEND OFF;
-- End of tempfile additions.
--
```

## 步骤三 模拟控制文件全部丢失

```
oracle@mmsc103:~> cd oradata/mmsgdb/
oracle@mmsc103:~/oradata/mmsgdb> l
total 2268880
drwxr-x--- 2 oracle oinstall       4096 2011-03-08 18:21 ./
drwxr-x--- 3 oracle oinstall       4096 2011-03-03 18:20 ../
-rw-r----- 1 oracle oinstall    9912320 2011-03-09 09:11 control01.ctl
-rw-r----- 1 oracle oinstall    9912320 2011-03-09 09:11 control02.ctl
-rw-r----- 1 oracle oinstall    9912320 2011-03-09 09:11 control03.ctl
-rw-r----- 1 oracle oinstall 1048584192 2011-03-09 09:11 mmsgdata01
-rw-r----- 1 oracle oinstall  524296192 2011-03-08 18:12 mmsgdata02
-rw-r----- 1 oracle oinstall   52429312 2011-03-09 09:11 redo01.log
-rw-r----- 1 oracle oinstall   52429312 2011-03-08 22:01 redo02.log
-rw-r----- 1 oracle oinstall   52429312 2011-03-09 03:00 redo03.log
-rw-r----- 1 oracle oinstall  209723392 2011-03-09 09:11 rman_data.dbf
-rw-r----- 1 oracle oinstall   20979712 2011-03-08 18:12 rman_tmp.dbf
-rw-r----- 1 oracle oinstall  300621824 2011-03-09 09:11 sysaux01.dbf
-rw-r----- 1 oracle oinstall  356524032 2011-03-09 09:11 system01.dbf
-rw-r----- 1 oracle oinstall   20979712 2011-03-09 06:28 temp01.dbf
-rw-r----- 1 oracle oinstall  209723392 2011-03-09 09:11 undotbs01.dbf
-rw-r----- 1 oracle oinstall    5251072 2011-03-09 09:11 users01.dbf
oracle@mmsc103:~/oradata/mmsgdb> rm -rf control0*
oracle@mmsc103:~/oradata/mmsgdb> l
total 2239792
drwxr-x--- 2 oracle oinstall       4096 2011-03-09 09:12 ./
drwxr-x--- 3 oracle oinstall       4096 2011-03-03 18:20 ../
-rw-r----- 1 oracle oinstall 1048584192 2011-03-09 09:11 mmsgdata01
-rw-r----- 1 oracle oinstall  524296192 2011-03-08 18:12 mmsgdata02
-rw-r----- 1 oracle oinstall   52429312 2011-03-09 09:11 redo01.log
-rw-r----- 1 oracle oinstall   52429312 2011-03-08 22:01 redo02.log
-rw-r----- 1 oracle oinstall   52429312 2011-03-09 03:00 redo03.log
-rw-r----- 1 oracle oinstall  209723392 2011-03-09 09:11 rman_data.dbf
-rw-r----- 1 oracle oinstall   20979712 2011-03-08 18:12 rman_tmp.dbf
-rw-r----- 1 oracle oinstall  300621824 2011-03-09 09:11 sysaux01.dbf
-rw-r----- 1 oracle oinstall  356524032 2011-03-09 09:11 system01.dbf
-rw-r----- 1 oracle oinstall   20979712 2011-03-09 06:28 temp01.dbf
-rw-r----- 1 oracle oinstall  209723392 2011-03-09 09:11 undotbs01.dbf
-rw-r----- 1 oracle oinstall    5251072 2011-03-09 09:11 users01.dbf
```

## 步骤四  动数据库，报错

```
oracle@mmsc103:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期三 3月 9 09:12:46 2011

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

已连接到空闲例程。

SQL> startup 
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes
ORA-00205: ?????????, ??????, ???????
```

## 步骤五  查看错误码和跟踪日志，获取详细信息

```
SQL> host
oracle@mmsc103:~> oerr ora 00205
00205, 00000, "error in identifying control file, check alert log for more info"
// *Cause:  The system could not find a control file of the specified name and
//         size.
// *Action: Check that ALL control files are online and that they are the same
//         files that the system created at cold start time.
oracle@mmsc103:~>

<msg time='2011-03-09T09:12:51.555+08:00' org_id='oracle' comp_id='rdbms'
 client_id='' type='UNKNOWN' level='16'
 module='' pid='20849'>
 <txt>ORA-00210: ???????????
ORA-00202: ????: &apos;&apos;/opt/oracle/oradata/mmsgdb/control03.ctl&apos;&apos;
ORA-27037: ????????
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3
ORA-00210: ???????????
ORA-00202: ????: &apos;&apos;/opt/oracle/oradata/mmsgdb/control02.ctl&apos;&apos;
ORA-27037: ????????
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3
ORA-00210: ???????????
ORA-00202: ????: &apos;&apos;/opt/oracle/oradata/mmsgdb/control01.ctl&apos;&apos;
ORA-27037: ????????
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3
 </txt>
</msg> 
```

## 步骤六  重建数据库控制文件

### 修改trace日志中创建控制文件部分内容

```
oracle@mmsc103:~> more control.sql 
STARTUP NOMOUNT
CREATE CONTROLFILE REUSE DATABASE "MMSGDB" NORESETLOGS  ARCHIVELOG
    MAXLOGFILES 16
    MAXLOGMEMBERS 3
    MAXDATAFILES 100
    MAXINSTANCES 8
    MAXLOGHISTORY 292
LOGFILE
  GROUP 1 '/opt/oracle/oradata/mmsgdb/redo01.log'  SIZE 50M,
  GROUP 2 '/opt/oracle/oradata/mmsgdb/redo02.log'  SIZE 50M,
  GROUP 3 '/opt/oracle/oradata/mmsgdb/redo03.log'  SIZE 50M
-- STANDBY LOGFILE
DATAFILE
  '/opt/oracle/oradata/mmsgdb/system01.dbf',
  '/opt/oracle/oradata/mmsgdb/sysaux01.dbf',
  '/opt/oracle/oradata/mmsgdb/undotbs01.dbf',
  '/opt/oracle/oradata/mmsgdb/users01.dbf',
  '/opt/oracle/oradata/mmsgdb/mmsgdata01',
  '/opt/oracle/oradata/mmsgdb/rman_data.dbf'
CHARACTER SET ZHS16GBK
;
-- Configure RMAN configuration record 1
VARIABLE RECNO NUMBER;
EXECUTE :RECNO := SYS.DBMS_BACKUP_RESTORE.SETCONFIG('CONTROLFILE AUTOBACKUP','ON');
-- Configure RMAN configuration record 2
VARIABLE RECNO NUMBER;
EXECUTE :RECNO := SYS.DBMS_BACKUP_RESTORE.SETCONFIG('RETENTION POLICY','TO RECOVERY WINDOW OF 10 DAYS');
-- Commands to re-create incarnation table
-- Below log names MUST be changed to existing filenames on
-- disk. Any one log file from each branch can be used to
-- re-create incarnation records.
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- ALTER DATABASE REGISTER LOGFILE '/opt/oracle/flash_recovery_area/MMSGDB/archivelog/2011_03_09/o1_mf_1_1_%u_.arc';
-- Recovery is required if any of the datafiles are restored backups,
-- or if the last shutdown was not normal or immediate.
RECOVER DATABASE
-- All logs need archiving and a log switch is needed.
ALTER SYSTEM ARCHIVE LOG ALL;
-- Database can now be opened normally.
ALTER DATABASE OPEN;
-- Commands to add tempfiles to temporary tablespaces.
-- Online tempfiles have complete space information.
-- Other tempfiles may require adjustment.
ALTER TABLESPACE TEMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/temp01.dbf'
     SIZE 20971520  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER TABLESPACE MMSG_TMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/mmsgdata02'
     SIZE 524288000  REUSE AUTOEXTEND OFF;
ALTER TABLESPACE RMAN_TMP ADD TEMPFILE '/opt/oracle/oradata/mmsgdb/rman_tmp.dbf'
     SIZE 20971520  REUSE AUTOEXTEND OFF;
```

### 重新创建控制文件

关闭数据库，修改trace文件中创建control文件部分

```
SQL> @control.sql
ORACLE 例程已经启动。

Total System Global Area 8417955840 bytes
Fixed Size                  2146024 bytes
Variable Size            4429185304 bytes
Database Buffers         3959422976 bytes
Redo Buffers               27201536 bytes


控制文件已创建。


PL/SQL 过程已成功完成。


PL/SQL 过程已成功完成。

ORA-00283: ??????????
ORA-00264: ?????



系统已更改。


数据库已更改。


表空间已更改。


表空间已更改。


表空间已更改。

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup
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

如果没有trace日志文件中记录的重新创建控制文件部分内容，可以手工书写重建控制文件的sql脚本，内容可参考上面的trace日志中内容。

说明：
* 1、重建控制文件用于恢复全部数据文件的损坏，需要注意其书写的正确性，保证包含了所有的数据文件与联机日志
* 2、经常有这样一种情况，因为一个磁盘损坏，我们不能再恢复(store)数据文件到这个磁盘，因此在store到另外一个盘的时候，我们就必须重新创建控制文件，用于识别这个新的数据文件，这里也可以用这种方法用于恢复;
* 3、如果数据库运行在归档方式下，有可用的控制文件的备份(CONFIGURE CONTROLFILE AUTOBACKUP ON)，则可以使用restore controlfile from ‘备份的控制文件路径+文件名’来完成控制文件的恢复操作，详细操作可参考本文中“控制文件的恢复”内容。


# 损坏临时数据文件的恢复方法

临时数据文件的恢复是比较简单的，因为临时文件中不涉及到其它的有用的数据，仅用来排序，所以可以删除后重建。

#### 1、关闭数据库

```
SQL>shutdown immediate
```

#### 2、删除临时数据文件，模拟媒体失败

#### 3、启动数据库，检测到文件错误

#### 4、脱机该数据文件

```
SQL>alter database datafile ‘全路径+文件名’ offline drop;
```

#### 5、打开数据库

```
SQL>alter database open
```

#### 6、删除该临时表空间

```
SQL>drop tablespace temp(或其它临时表空间名称) including contents and datafiles;
```

#### 7、重新创建该表空间，并重新分配给用户

说明：
* 1、临时数据文件是非重要文件，不保存永久数据，可以随时删除重建，不影响数据库的数据安全
* 2、如果重新建立以后，别忘了重新分配给用户。

