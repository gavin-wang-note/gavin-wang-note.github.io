---
layout:     post
title:      "Oracle升级碰到的问题"
subtitle:   "Oracle upgrade issue"
date:       2009-03-16
author:     "Gavin"
catalog:    true
tags:
    - oracle 
---


# 现象
Oracle11g 11.1.0.6.0安装小补丁版本失败,安装小补丁：p6928169_111060_Linux-x86-64.zip

```
opyright (c) 2007, Oracle Corporation.  All rights reserved.


Oracle Home       : /opt/oracle/app/product/11.1.0/db_1
Central Inventory : /opt/oraInventory
   from           : /etc/oraInst.loc
OPatch version    : 11.1.0.6.0
OUI version       : 11.1.0.6.0
OUI location      : /opt/oracle/app/product/11.1.0/db_1/oui
Log file location : /opt/oracle/app/product/11.1.0/db_1/cfgtoollogs/opatch/opatch2009-03-06_14-16-49PM.log

ApplySession applying interim patch '6928169' to OH '/opt/oracle/app/product/11.1.0/db_1'

Running prerequisite checks...
Prerequisite check "CheckActiveFilesAndExecutables" failed.
The details are:


Following executables are active :
/opt/oracle/app/product/11.1.0/db_1/bin/oracle
ApplySession failed during prerequisite checks: Prerequisite check "CheckActiveFilesAndExecutables" failed.
System intact, OPatch will not attempt to restore the system

OPatch failed with error code 74
oracle@expsmgw:/opt/oraInventory/6928169>
```

# 解决方法

当时没解决，只有安装了大补丁才解决问题。不过不建议这也操作，会比较麻烦，一旦升级出错，恢复数据库有难度，除非升级之前已经备份数据库。

正确安装信息显示如下：

```
oracle@MMSGDS:/opt/oraInventory/6928169> export OBJECT_MODE=32_64
oracle@MMSGDS:/opt/oraInventory/6928169> /opt/oracle/product/11g/db_1/OPatch/opatch apply
Invoking OPatch 11.1.0.6.0

Oracle Interim Patch Installer version 11.1.0.6.0
Copyright (c) 2007, Oracle Corporation.  All rights reserved.


Oracle Home       : /opt/oracle/product/11g/db_1
Central Inventory : /opt/oraInventory
   from           : /etc/oraInst.loc
OPatch version    : 11.1.0.6.0
OUI version       : 11.1.0.6.0
OUI location      : /opt/oracle/product/11g/db_1/oui
Log file location : /opt/oracle/product/11g/db_1/cfgtoollogs/opatch/opatch2009-04-13_15-50-35PM.log

ApplySession applying interim patch '6928169' to OH '/opt/oracle/product/11g/db_1'

Running prerequisite checks...

OPatch detected non-cluster Oracle Home from the inventory and will patch the local system only.


Please shutdown Oracle instances running out of this ORACLE_HOME on the local system.
(Oracle Home = '/opt/oracle/product/11g/db_1')


Is the local system ready for patching? [y|n]
y
User Responded with: Y
Backing up files and inventory (not for auto-rollback) for the Oracle Home
Backing up files affected by the patch '6928169' for restore. This might take a while...
Backing up files affected by the patch '6928169' for rollback. This might take a while...

Patching component oracle.rdbms, 11.1.0.6.0...
Updating archive file "/opt/oracle/product/11g/db_1/lib/libserver11.a"  with "lib/libserver11.a/jska.o"
Updating archive file "/opt/oracle/product/11g/db_1/lib/libserver11.a"  with "lib/libserver11.a/jskc.o"
Running make for target ioracle
ApplySession adding interim patch '6928169' to inventory

Verifying the update...
Inventory check OK: Patch ID 6928169 is registered in Oracle Home inventory with proper meta-data.
Files check OK: Files from Patch ID 6928169 are present in Oracle Home.

The local system has been patched and can be restarted.


OPatch succeeded.
oracle@MMSGDS:/opt/oraInventory/6928169>
```

# ORA-01092  ORACLE 实例终止,强制断开连接 解决方案

## 表象

```
SQL> startup 
ORACLE 例程已经启动。 

Total System Global Area  109051904 bytes 
Fixed Size                  1295272 bytes 
Variable Size              92277848 bytes 
Database Buffers            8388608 bytes 
Redo Buffers                7090176 bytes 
数据库装载完毕。 
ORA-01092: ORACLE 实例终止。强制断开连接
```

## 分析步骤

### alert日志信息片段

```
<txt>Errors in file /home/oracle/diag/rdbms/mmsgdb/mmsgdb/trace/mmsgdb_ora_438512.trc:
ORA-00704: 引导程序进程失败
ORA-39700: 必须用 UPGRADE 选项打开数据库
 </txt>
```

### 查看错误码信息

```
% oerr ora 01092
01092, 00000, "ORACLE instance terminated. Disconnection forced"
// *Cause:  The instance this process was connected to was terminated
//          abnormally, probably via a shutdown abort. This process
//          was forced to disconnect from the instance.
// *Action: Examine the alert log for more details. When the instance has been 
//          restarted, retry action.
%

% oerr ora 39700
39700, 00000, "database must be opened with UPGRADE option"
// *Cause:  A normal database open was attempted, but the database has not 
//          been upgraded to the current server version.
// *Action: Use the UPGRADE option when opening the database to run 
//          catupgrd.sql (for database upgrade), or to run catalog.sql 
//          and catproc.sql (after initial database creation).
```

# 原因

Oracle数据库升级后，数据字典没有升级，或者数据字典升级失败

# 解决方法

oracle dba用户执行catupgrd.sql、cataproc.sql和catlog.sql

1、以startup upgrade打开数据库 

2、以sysdba运行‘升级数据字典’脚本和‘创建数据字典’脚本 

product/11g/rdbms/admin/catupgrd.sql 和 product/11g/rdbms/admin/catalog.sql和catproc.sql

具体的需要根据trace日志中的提示信息去执行哪个sql文件。

例如：

```
/opt/oracle/product/11g/rdbms/admin/catupgrd.sql

cat /opt/oracle/product/11g/rdbms/admin/catupgrd.sql | sqlplus / as sysdba
```

如果还不行，再去刷一个catproc.sql

```
cat /opt/oracle/product/11g/rdbms/admin/catproc.sql | sqlplus / as sysdba
```

如果还不行，再去刷一个catlog.sql

```
 cat /opt/oracle/product/11g/rdbms/admin/catlog.sql | sqlplus / as sysdba
```
