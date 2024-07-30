---
layout:     post
title:      "Oracle案例--修改数据库实例名和数据库名"
subtitle:   "Oracle troubleshoot--modify instance name and DB name"
date:       2010-09-27
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 概述

在oracle9i之前，修改数据库实例比较麻烦，需要重建oracle的控制文件以及需要reset redolog。从oracle 9i R2版本开始，oracle 提供了nid系统命令，使得修改oracle的数据库名和实例名更加简单。

本文描述将数据库名和实例名为mmsgdb的修改为inomc

# 具体操作描述

## 准备工作

一个正常可以使用的oracle数据库系统，instance正常，database正常。

## 操作步骤

1、shutdown 数据库

2、数据库启动到mount状态

3、创建pfile文件

4、执行nid命令，修改数据库名和实例名

5、修改pfile文件，启动数据库

6、创建spfile文件和口令文件

7、加载监听，修改tnsnames.ora文件

8、检测更改后的信息

9、备份数据库

关键部分的详细步骤如下：

### 步骤一、查看nid帮助信息以及nid使用方法

```shell
SQL> host nid –help

DBNEWID: Release 11.1.0.7.0 - Production on 星期一 9月 27 11:09:09 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

关键字      说明                    (默认值)
----------------------------------------------------
TARGET      用户名/口令              (无)
DBNAME      新的数据库名             (无)
LOGFILE     输出日志                     (无)
REVERT      还原失败的更改            否
SETNAME     仅设置新的数据库名        否
APPEND      附加至输出日志            否
HELP        显示这些消息              否

shutdown 数据库
SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL>
```

### 步骤二、启动数据库到mount状态

```shell
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
SQL>
```

### 步骤三、创建pfile文件

```shell
SQL> create pfile='/opt/oracle/product/11g/dbs/pfile2010wyz ' from spfile;

文件已创建。

SQL>
```

### 步骤四、修改数据库名

```shell
SQL> host nid target=sys/sys dbname=inomc

DBNEWID: Release 11.1.0.7.0 - Production on 星期一 9月 27 11:10:23 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

已连接数据库 MMSGDB (DBID=3129897535)

已连接服务器版本 11.1.0

数据库中的控制文件数:
    /opt/oracle/oradata/mmsgdb/control01.ctl
    /opt/oracle/oradata/mmsgdb/control02.ctl
    /opt/oracle/oradata/mmsgdb/control03.ctl

是否将数据库 ID 和数据库名 MMSGDB 更改为 INOMC? (Y/[N]) => Y

操作继续进行
将数据库 ID 从 3129897535 更改为 1037547743
将数据库名从 MMSGDB 更改为 INOMC
    控制文件 /opt/oracle/oradata/mmsgdb/control01.ctl - 已修改
    控制文件 /opt/oracle/oradata/mmsgdb/control02.ctl - 已修改
    控制文件 /opt/oracle/oradata/mmsgdb/control03.ctl - 已修改
    数据文件 /opt/oracle/oradata/mmsgdb/system01.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/sysaux01.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/undotbs01.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/users01.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/mmsgdata0 - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/y_mmsgdb - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/wyz_mmsgdata0 - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/wyztest.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/wyztest01.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/temp01.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/mmsgdata0 - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/y_mmsgdb - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/wyz_mmsgdata0 - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/wyztesttmp.db - dbid 已更改, 已写入新名称
    数据文件 /opt/oracle/oradata/mmsgdb/wyztesttemp0.db - dbid 已更改, 已写入新名称
    控制文件 /opt/oracle/oradata/mmsgdb/control01.ctl - dbid 已更改, 已写入新名称
    控制文件 /opt/oracle/oradata/mmsgdb/control02.ctl - dbid 已更改, 已写入新名称
    控制文件 /opt/oracle/oradata/mmsgdb/control03.ctl - dbid 已更改, 已写入新名称




NID-00600: 内部错误 - [28] [1013] [0] [0]


在验证时更改数据库名和 ID 失败 - 数据库保持原样。
DBNEWID - 已完成, 但出现验证错误。
```
注意：
* 这里出问题了，原因如下：

因为这个nid命令僵死，当使用nid更改数据库名和实例名的时候，nid僵死的几率很高，出现这个问题的时候，当发现控制文件已经更改了，数据文件、重做日志文件已经更改了之后，就可以强制终止nid操作了，于是就出现了上面的“NID-00600: 内部错误 - [28] [1013] [0] [0]”错误信息。

按理这里应该是出现:

```shell
数据库名已经改变为INOMC
在重启数据库之前修改系统参数文件和创建新口令文件
所以的回滚以及归档的重做日志对当前数据库已经无用
关闭数据库后重启时需要使用resetlogs操作
成功改变数据库名和ID信息
DBNEWID –成功完成
```

对应英文如下：

```shell
Database name changed to TESTDB.
Modify parameter file and generate a new password file before restarting.
Database ID for database TESTDB changed to 2321050327.
All previous backups and archived redo logs for this database are unusable.
Shut down database and open with RESETLOGS option.
Succesfully changed database name and ID.
DBNEWID - Completed succesfully.
```

### 步骤五、修改pfile文件和环境变量

#### 修改pfile

```shell
inomc.__db_cache_size=1207959552   #"inomc"这个名称，原先是mmsgdb，这里凡是带“mmsgdb”字样的，全部被修改成inomc
inomc.__java_pool_size=16777216
inomc.__large_pool_size=16777216
inomc.__oracle_base='/opt/oracle'#ORACLE_BASE set from environment
inomc.__pga_aggregate_target=6744440832
inomc.__sga_target=1610612736
inomc.__shared_io_pool_size=0
inomc.__shared_pool_size=352321536
inomc.__streams_pool_size=0
*.audit_file_dest='/opt/oracle/admin/mmsgdb/adump'
*.audit_trail='NONE'
*.compatible='11.1.0.0.0'
*.control_files='/opt/oracle/oradata/mmsgdb/control01.ctl','/opt/oracle/oradata/mmsgdb/control02.ctl','/opt/oracle/oradata/mmsgdb/co
ntrol03.ctl'
*.db_block_size=8192
*.db_domain=''
*.db_name='inomc'   #原先是mmsgdb，这里修改成inomc
*.diagnostic_dest='/opt/oracle'
*.nls_language='SIMPLIFIED CHINESE'
*.nls_territory='CHINA'
*.open_cursors=300
*.pga_aggregate_target=6728712192
*.processes=150
*.recyclebin='OFF'
*.remote_login_passwordfile='EXCLUSIVE'
*.sga_target=1610612736
*.undo_tablespace='UNDOTBS1'
*.instance_name='inomc'   #新增的信息，因为oracle11g隐式读取这个参数，这里增加，可直接读取
*.service_names='inomc'   #新增的信息，因为oracle11g隐式读取这个参数，这里增加，可直接读取
```

#### 修改环境变量信息.profile文件

将这个文件中的```ORACLE_SID=mmsgdb ```, 修改成 ```ORACLE_SID=inomc ```, 重新source一下这个环境变量文件。

### 步骤六、以pfile文件启动数据库

```shell
SQL> shutdown immediate     #停止数据库
ORA-01507: ??????


ORACLE 例程已经关闭。
SQL> startup nomount         #启动数据库到mount状态
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes


SQL> shutdown immediate
ORA-01507: ??????


ORACLE 例程已经关闭。
SQL> startup pfile='/opt/oracle/product/11g/dbs/pfile2010wyz.ora'  #以pfile文件启动
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
ORA-01589: 要打开数据库则必须使用 RESETLOGS 或 NORESETLOGS 选项  #这里提示报错了，先不管


SQL> create spfile from pfile = '/opt/oracle/product/11g/dbs/pfile2010wyz.ora'
  2  ;

文件已创建。                      #通过pfile文件创建spfile文件

SQL> shutdown immediate      #关闭数据库
ORA-01109: 数据库未打开


已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup mount           #启动数据库到mount状态
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
SQL> alter database open RESETLOGS;      #使用resetlogs启动数据库

数据库已更改。

SQL> select open_mode from v$database;   #查看数据库打开模式

OPEN_MODE
----------
READ WRITE

SQL> show parameter name                   #查看数据库名和实例信息

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
db_file_name_convert                 string
db_name                              string      inomc
db_unique_name                       string      inomc
global_names                         boolean     FALSE
instance_name                        string      inomc
lock_name_space                      string
log_file_name_convert                string
service_names                        string      inomc
SQL>
```
### 步骤七、创建口令文件

#### 查看orapwd帮助信息

```shell
oracle@mmsg:~/product/11g/network/admin> orapwd
Usage: orapwd file=<fname> password=<password> entries=<users> force=<y/n> ignorecase=<y/n> nosysdba=<y/n>

  where
    file - name of password file (required),
    password - password for SYS, will be prompted if not specified at command line,
    entries - maximum number of distinct DBA (optional),
    force - whether to overwrite existing file (optional),
    ignorecase - passwords are case-insensitive (optional),
    nosysdba - whether to shut out the SYSDBA logon (optional Database Vault only).
    
  There must be no spaces around the equal-to (=) character.
```

#### 创建口令文件

```shell
oracle@mmsg:~/product/11g/dbs> orapwd  file=/opt/oracle/product/11g/dbs/orapwinomc password=sys entries=20
```

### 步骤八、事后检查

#### 查看实例信息

```shell
SQL> select instance_name from v$instance;

INSTANCE_NAME
----------------
inomc

SQL>
```

#### 修改tnsnames.ora文件信息

```shell
INOMC =
  (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = mmsg)(PORT = 1521))
      (CONNECT_DATA =
        (SERVER = DEDICATED)
        (SERVICE_NAME = inomc)
      )
  )

```
注：
* 凡是mmsgdb的，修改成inomc

#### reload监听信息

```shell
racle@mmsg:~/product/11g/network/admin> lsnrctl reload

LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 27-9月 -2010 15:20:02

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

正在连接到 (ADDRESS=(PROTOCOL=tcp)(HOST=)(PORT=1521))
命令执行成功
```

### 步骤九、备份数据库

原因是数据库实例名和数据库名发生变更后，之前的所有备份对当前数据库已经没有任何作用了，所以建议备份一下当前修改后的数据库。

# 总结

修改实例名和数据库名与删除实例重建，前者最大的优势是原有数据不会丢失。

至此，数据库名和实例名修改完成。


# 遇见的问题与解决方法

## 表象

数据库连接与启动失败，与数据库建立连接时报ORA-00838错误。

```shell
racle@mmsg:~> sqlplus / as sysdba
Copyright (c) 1982, 2008, Oracle.  All rights reserved.
ORA-00838: Specified value of MEMORY_TARGET is too small, needs to be at least 7968M
oracle@mmsg:~> cd product/11g/dbs

oracle@mmsg:~/product/11g/dbs> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期一 9月 27 14:55:13 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

已连接到空闲例程。

SQL> startup 
ORA-00838: Specified value of MEMORY_TARGET is too small, needs to be at least 7968M
SQL>
```

## 原因

内存自动管理机制中MEMORY_TARGET参数值设置过小。

## 解决方法

当前数据库已经无法启动，也就无法查看当前memory_target值与memory_max_target的值

解决这个问题，只能从pfile文件中着手（因为spfiel文件是二进制文件，不能直接修改）。

### 修改pfile文件，新增一行记录

```*.memory_target=8365053568 ```,这里修改值比7968*1024*1024的值稍大点.

### 以指定pfile文件方式启动数据库

```shell
SQL> startup pfile='/opt/oracle/product/11g/dbs/pfile2010wyz.ora'
ORACLE 例程已经启动。

Total System Global Area 8334446592 bytes
Fixed Size                  2176280 bytes
Variable Size            7147096808 bytes
Database Buffers         1174405120 bytes
Redo Buffers               10768384 bytes
数据库装载完毕。
数据库已经打开。
```

### 以pfile文件创建spfile文件

```shell
SQL> create spfile='/opt/oracle/product/11g/dbs/spfileinomc.ora' from pfile ='/opt/oracle/product/11g/dbs/pfile2010wyz.ora'
  2  ;

文件已创建。
```

### 重启数据库

```shell
SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup       
ORACLE 例程已经启动。

Total System Global Area 8351150080 bytes
Fixed Size                  2161272 bytes
Variable Size            7449085320 bytes
Database Buffers          872415232 bytes
Redo Buffers               27488256 bytes
数据库装载完毕。
数据库已经打开。
SQL>
```
