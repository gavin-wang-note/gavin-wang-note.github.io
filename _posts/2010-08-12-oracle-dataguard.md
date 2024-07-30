---
layout:     post
title:      "Oracle Dataguard"
subtitle:   "Oracle Dataguard"
date:       2010-08-12
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# dataguard概述

Oracle Dataguard主要实现数据库的容灾，根据archive log进行数据的同步，当主库异常时，自动切换到备库。

# 实践

## 背景

XX行业网关，本期配置了4块服务器（4C8G），分别部署在A地和B地两地，组成两两双机的对等集群。A地和B地两地相距30KM，采用千兆专线拉通，具体拓扑如下图所示：

<img class="shadow" src="/img/in-post/oracle-dg.png" width="1200">

### 数据库容灾方案

在A地和B地业务、数据库和计费服务器均进行合设。平时A地节点作为数据库生产节点，B地节点作为数据库容灾节点，生产节点和容灾节点通过DATAGUARD进行数据同步。

数据库生产节点和容灾节点通过F5实现对业务服务器的统一IP。即在F5上为数据库专门配置一个POOL和VISUAL SERVER。VISUAL SERVER是对外提供的数据库统一IP，将数据库生产节点优先级设置为高优先级，容杂节点设置为低优先级。平时F5会将流量发送高优先级的生产节点处理，当生产节点不可用时会自动发送给低优先级的容灾节点。

## 试验环境

SUSE Linux Enterprise Server 10 SP1 (x86_64) - Kernel 2.6.16.46-0.12-smp (3)

IP规划如下：

|IP | 硬件类型|说明 |
|---------------|---------------|------------------|
|10.137.49.114|   R2+单板 |  primary数据库|
|10.137.49.167|   R2单板  |  standby数据库|

## 软件环境

Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production

## Data guard 操作

### 配置操作

#### 1、 确认primary数据库处于归档模式 

```shell
SQL> archive log list
数据库日志模式             非存档模式
自动存档             禁用
存档终点            /opt/oracle/product/11g/dbs/arch
最早的联机日志序列     1
当前日志序列           2
SQL>
```

如果为非归档模式，请执行下列命令修改

```shell
SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
SQL> ALTER DATABASE ARCHIVELOG;

数据库已更改。

SQL> ALTER DATABASE OPEN;

数据库已更改。

SQL>
```

#### 2、 设置归档日志路径

```shell
SQL> show parameter log_archive_dest

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
log_archive_dest                     string
log_archive_dest_1                   string
log_archive_dest_10                  string
log_archive_dest_2                   string
log_archive_dest_3                   string
log_archive_dest_4                   string
log_archive_dest_5                   string
log_archive_dest_6                   string
log_archive_dest_7                   string
log_archive_dest_8                   string
log_archive_dest_9                   string

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
log_archive_dest_state_1             string      enable
log_archive_dest_state_10            string      enable
log_archive_dest_state_2             string      enable
log_archive_dest_state_3             string      enable
log_archive_dest_state_4             string      enable
log_archive_dest_state_5             string      enable
log_archive_dest_state_6             string      enable
log_archive_dest_state_7             string      enable
log_archive_dest_state_8             string      enable
log_archive_dest_state_9             string      enable

#arch目录请到dbs目录下手工创建
SQL> alter system set log_archive_dest_1=' location=/opt/oracle/diag/arch ' scope=spfile;
系统已更改。

SQL> alter system set log_archive_format=' arch_%t_%s_%r.arc' scope=spfile;

系统已更改。
SQL> 
```

#### 3、 将primary数据库置为FORCE LOGGING模式

通过下列语句： 

```shell
SQL> alter database force logging; 

数据库已更改。

#需要重启数据库，做如下操作：
SQL> shutdown immediate
SQL> startup
SQL> show parameter log_archive_dest
SQL> 
```

#### 4、 primary数据库创建standby数据库控制文件 

```shell
SQL> shutdown immediate
SQL> startup mount
SQL> alter database create standby controlfile as '/opt/oracle/oradata/mmsgdb/backupctl.ctl';  

数据库已更改。

SQL> SQL> alter database open;

数据库已更改。

SQL> alter system archive log current;

系统已更改。

SQL>
```

#### 5、 创建primary数据库客户端初始化参数文件 

注：
* 主要此处修改项较多，为了方便，我们首先创建并修改pfile，然后再通过pfile重建spfile，你当然也可以通过alter system set命令直接修改spfile内容，不过，麻烦。 

```shell
SQL> create pfile from spfile;

文件已创建。
```

将该初始化参数文件复制一份，做为standby数据库的客户端初始化参数文件 

```shell
SQL> host
oracle@mmsg:~> cp /opt/oracle/product/11g/dbs/initmmsgdb.ora  /opt/oracle/product/11g/dbs/bakinitmmsgdb.ora
```

备份已有的spfile文件

```shell
oracle@mmsg:~> cd $ORACLE_HOME/dbs
oracle@mmsg:~/product/11g/dbs> cp spfilemmsgdb.ora bak_spfilemmsgdb.ora
```

修改客户端初始化参数文件，增加下列内容 

```shell
*.DB_UNIQUE_NAME=uqn_primary              //自定义一个unique_name名字
*.LOG_ARCHIVE_CONFIG='DG_CONFIG=(uqn_primary,uqn_standby)'  //此处为主备服务器的unique_name
*.LOG_ARCHIVE_DEST_2='SERVICE=standby ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=uqn_standby'
*.LOG_ARCHIVE_DEST_STATE_1=ENABLE
*.LOG_ARCHIVE_DEST_STATE_2=ENABLE
*.LOG_ARCHIVE_MAX_PROCESSES=30

#--------配置standby角色的参数用于角色转换
*.FAL_SERVER=standby                        //这里为net service name
*.FAL_CLIENT=primary
*.STANDBY_FILE_MANAGEMENT=AUTO
```

上述新增内容中的注释部分不需要，请添加时去掉。

初始化参数参考 

对于primary数据库，需要定义几个primary角色的初始化参数控制redo传输服务，还有几个附加的standby角色的参数需要添加以控制接收redo数据库并应用(switchover/failover后primary/standby角色可能互换，所以建议对于两类角色 相关的 初始化参数都进行配置)。

下列参数为primary角色相关的初始化参数： 

|参数 | 说明|
|-----------|-----------------------------------------------------------------------|
|DB_NAME | 注意保持同一个Data Guard中所有数据库DB_NAME相同。 例如：DB_NAME=mmsgdb|
|DB_UNIQUE_NAME |为每一个数据库指定一个唯一的名称，该参数一经指定不会再发生变化，除非你主动修改它。 例如：DB_UNIQUE_NAME= uqn_mmsgdb |
|LOG_ARCHIVE_CONFIG |该参数通过DG_CONFIG属性罗列同一个Data Guard中所有DB_UNIQUE_NAME(含primary db及standby db)，以逗号分隔 例如：LOG_ARCHIVE_CONFIG='DB_CONFIG= uqn_primary, uqn_standby)' |
|CONTROL_FILES | 没啥说的，控制文件所在路径。|
|LOG_ARCHIVE_DEST_n | 归档文件的生成路径 。该参数非常重要，并且属性和子参数也特别多(这里不一一列举，后面用到时单独讲解;如果你很好奇，建议直接查询oracle官方文档。Data guard白皮书第14章专门介绍了该参数各属性及子参数的功能和设置)。 例如： LOG_ARCHIVE_DEST_1= 'LOCATION= /opt/oracle/diag/arch VALID_FOR=(ALL_LOGFILES,ALL_ROLES) DB_UNIQUE_NAME= uqn_primary' |
|LOG_ARCHIVE_DEST_STATE_n | 指定参数值为ENABLE，允许redo传输服务传输redo数据到指定的路径。 该参数共拥有4个属性值，功能各不相同。|
|REMOTE_LOGIN_PASSWORDFILE | 推荐设置参数值为EXCLUSIVE或者SHARED，注意保证相同Data Guard配置中所有db服务器sys密码相同。|
|LOG_ARCHIVE_FORMAT | 指定归档文件格式。 |
|LOG_ARCHIVE_MAX_PRODUCESSES | 指定归档进程的数量(1-30)，默认值通常是4 。 |

以下参数为standby角色相关的参数，建议在Primary数据库 的初始化参数中也进行设置，这样在role transition后(Primary转为Standby)也能正常运行： 

|参数 | 说明|
|--------------|-------------------------------------------------------|
|FAL_SERVER | 指定一个数据库SID，通常该库为primary角色。 例如：FAL_SERVER=primary |
|FAL_CLIENT | 指定一个数据库SID，通常该库为standby角色。 例如：FAL_CLIENT=standby
提示：FAL是Fetch Archived Log的缩写 |
|DB_FILE_NAME_CONVERT 	| 在做duplicate复制和传输表空间的时候这类参数讲过很多遍，该参数及上述内容中同名参数功能，格式等完全相同。 |
|LOG_FILE_NAME_CONVERT 	| 同上 |
|STANDBY_FILE_MANAGEMENT | 如果primary数据库数据文件发生修改（如新建，重命名等）则按照本参数的设置在standby中做相应修改。设为AUTO表示自动管理。设为MANUAL表示需要手工管理。例如：STANDBY_FILE_MANAGEMENT=AUTO |

注意：
* 上面列举的这些参数仅只是对于primary/standby两角色可能会相关的参数，还有一些基础性参数比如*_dest,*_size等数据库相关的参数在具体配置时也需要根据实际情况做出适当修改。


通过pfile重建spfile 

```shell
SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup pfile='/opt/oracle/product/11g/dbs/initmmsgdb.ora'
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
数据库已经打开。
SQL>

SQL> create spfile='/opt/oracle/product/11g/dbs/spfilemmsgdb.ora' from pfile='/opt/oracle/product/11g/dbs/initmmsgdb.ora';

文件已创建。

SQL>
SQL> shutdown immediate
```

#### 6、 复制数据文件到standby服务器(方式多样，不详述) 

注:
* 要先停止primary和standby服务器上的oracle数据库，然后复制所有数据文件，备份的控制文件及客户端初始化参数文件（数据文件、口令文件、pfile文件、控制文件）到standby数据库（同时，建议先备份一下standby数据库侧的数据文件、控制文件、参数文件和口令文件） ，具体文件列表信息如下：

```shell
#控制文件
backupctl.ctl
control01.ctl
control02.ctl
control03.ctl
#重做日志文件
redo01.log
redo02.log
redo03.log
#数据文件
sysaux01.dbf
system01.dbf
temp01.dbf
undotbs01.dbf
users01.dbf
#口令文件
orapwmmsgdb
参数文件
initmmsgdb.ora
```

还需要到STANDBY服务器上执行下面的操作。

``` shell
oracle@mmsg1:~> cd /opt/oracle/oradata/ora11g
oracle@mmsg1:~/oradata/ora11g> rm -rf control0*
oracle@mmsg1:~/oradata/ora11g> mv backupctl.ctl  control01.ctl
oracle@mmsg1:~/oradata/ora11g> cp control01.ctl control02.ctl
oracle@mmsg1:~/oradata/ora11g> cp control01.ctl control03.ctl
oracle@mmsg1:~> cd $ORACLE_HOME/dbs 
# 替换口令（如果sys密码不同）和pfile文件
oracle@mmsg1:~/product/11g/dbs> ftp 10.137.49.114
Connected to 10.137.49.114.
220-Welcome to Pure-FTPd.
220-You are user number 1 of 50 allowed.
220-IPv6 connections are also welcome on this server.
220 You will be disconnected after 15 minutes of inactivity.
Name (10.137.49.114:root): oracle
331 User oracle OK. Password required
Password:
230-User oracle has group access to:  dba      oinstall
230 OK. Current directory is /opt/oracle
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd ~/product/11g/dbs
250 OK. Current directory is /opt/oracle/product/11g/dbs
ftp> ls
229 Extended Passive mode OK (|||60900|)
150 Accepted data connection
-rw-r-----    1 oracle   oinstall     2560 Aug  9 15:16 bak_spfilemmsgdb.ora
-rw-r--r--    1 oracle   oinstall      908 Aug  9 15:00 bakinitmmsgdb.ora
-rw-rw----    1 oracle   oinstall     1552 Aug  9 16:16 hc_mmsgdb.dat
-rw-r--r--    1 oracle   oinstall     2774 Sep 11  2007 init.ora
-rw-r--r--    1 oracle   oinstall    12920 May  3  2001 initdw.ora
-rw-r--r--    1 oracle   oinstall     1262 Aug  9 16:14 initmmsgdb.ora
-rw-r-----    1 oracle   oinstall       24 Aug  9 12:38 lkMMSGDB
-rw-r-----    1 oracle   oinstall     1536 Aug  9 13:31 orapwmmsgdb
-rw-r-----    1 oracle   oinstall     3584 Aug  9 16:18 spfilemmsgdb.ora
226-Options: -l 
226 9 matches total
ftp> asc
200 TYPE is now ASCII
ftp> get initmmsgdb.ora
local: initmmsgdb.ora remote: initmmsgdb.ora
229 Extended Passive mode OK (|||11762|)
150 Accepted data connection
100% |*****************************************************************************************|  1300       3.44 MB/s    --:-- ETA
226-File successfully transferred
226 0.000 seconds (measured here), 25.62 Mbytes per second
1300 bytes received in 00:00 (31.72 KB/s)
ftp> bin
200 TYPE is now 8-bit binary
ftp> get orapwmmsgdb
local: orapwmmsgdb remote: orapwmmsgdb
229 Extended Passive mode OK (|||59851|)
150 Accepted data connection
100% |*****************************************************************************************|  1536       6.28 MB/s    00:00 ETA
226-File successfully transferred
226 0.000 seconds (measured here), 34.13 Mbytes per second
1536 bytes received in 00:00 (36.22 KB/s)
ftp> by
221-Goodbye. You uploaded 0 and downloaded 3 kbytes.
221 Logout.
```

#### 7、 修改standby数据库参数文件

```shell
*.DB_UNIQUE_NAME=uqn_standby
*.LOG_ARCHIVE_CONFIG='DG_CONFIG=(uqn_primary,uqn_standby)'
*.LOG_ARCHIVE_DEST_2='SERVICE=primary ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=uqn_primary'
*.LOG_ARCHIVE_DEST_STATE_1=ENABLE
*.LOG_ARCHIVE_DEST_STATE_2=ENABLE
*.LOG_ARCHIVE_MAX_PROCESSES=30

#--------配置standby角色的参数用于角色转换
*.FAL_SERVER=primary
*.FAL_CLIENT=standby
*.STANDBY_FILE_MANAGEMENT=AUTO
```

#### 8、 修改listener及tns信息

配置primary数据库和standby数据库的listener及net service names(方式多样，不详述)

```shell
SID_LIST_LISTENER =
(SID_LIST =
   (SID_DESC =
      (SID_NAME = PLSExtProc)
      (ORACLE_HOME = /opt/oracle/product/11g)
      (PROGRAM = extproc)
  )
    (SID_DESC =
        (GLOBAL_DBNAME = mmsgdb)
        (ORACLE_HOME = /opt/oracle/product/11g)
        (SID_NAME = mmsgdb)           
     )
  )

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.49.114)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )
```

上面为primary数据库的listener信息，standby数据库同理。其中"SID_LIST_LISTENER = "内容为新增信息，红色部分为primary数据库ip地址。


配置primary数据库和standby数据库的tnsnames.ora文件，修改成如下信息

```shell
PRIMARY =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.49.114)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = mmsgdb)
    )
  )
  
STANDBY =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.49.167)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = mmsgdb)
    )
  )
```

完成之后重启primary数据库和standby数据库的listener，并测试监听: 

```shell
oracle@mmsg:~/product/11g/network/admin> lsnrctl stop
oracle@mmsg:~/product/11g/network/admin> lsnrctl start
oracle@mmsg:~/product/11g/network/admin> tnsping primary 10

TNS Ping Utility for Linux: Version 11.1.0.7.0 - Production on 10-8月 -2010 11:14:02

Copyright (c) 1997, 2008, Oracle.  All rights reserved.

已使用的参数文件:


已使用 TNSNAMES 适配器来解析别名
Attempting to contact (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.49.114)(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = mmsgdb)))
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
oracle@mmsg:~/product/11g/network/admin> tnsping standby 10

TNS Ping Utility for Linux: Version 11.1.0.7.0 - Production on 10-8月 -2010 11:14:08

Copyright (c) 1997, 2008, Oracle.  All rights reserved.

已使用的参数文件:


已使用 TNSNAMES 适配器来解析别名
Attempting to contact (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.49.167)(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = mmsgdb)))
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)
OK (0 毫秒)

oracle@mmsg:~/product/11g/network/admin> 
```

执行ping操作，primary和standby互ping一下ip地址，如果能ping通，则继续执行下面的操作，如果ping不通，请检查配置。

#### 9、 启动standby数据库

```shell
oracle@mmsg1:~/product/11g/dbs> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期二 8月 10 14:47:21 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

已连接到空闲例程。

SQL> create spfile from pfile='/opt/oracle/product/11g/dbs/initmmsgdb.ora';

文件已创建。

SQL>

启动standby数据库到mount状态
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
SQL> alter database recover managed standby database disconnect from session; 

数据库已更改。

SQL>
```

### 查看同步情况

#### 方法一

##### 首先连接到primary数据库

```shell
SQL> show parameter instance_name

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
instance_name                        string      mmsgdb
SQL> alter system switch logfile;

系统已更改。

SQL> select max(sequence#) from v$archived_log; 

MAX(SEQUENCE#)
--------------
             5

SQL> 
```

##### 连接到standby数据库 

```shell
SQL> alter database recover managed standby database disconnect from session; 

数据库已更改。

SQL> show parameter instance_name

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
instance_name                        string      mmsgdb
SQL> select max(sequence#) from v$archived_log;

MAX(SEQUENCE#)
--------------
             5
SQL>

MAX(SEQUENCE#)值一致，同步成功。
```

#### 方法二

在standby服务器，执行如下操作：

```shell
SQL> SELECT SEQUENCE#, FIRST_TIME, NEXT_TIME FROM V$ARCHIVED_LOG ORDER BY SEQUENCE#;

 SEQUENCE# FIRST_TIME     NEXT_TIME
---------- -------------- --------------
         2 09-8月 -10     10-8月 -10
         3 10-8月 -10     10-8月 -10
         4 10-8月 -10     10-8月 -10
         5 10-8月 -10     10-8月 -10
```

在primary服务器，执行归档操作：

```shell
SQL> ALTER SYSTEM SWITCH LOGFILE; 

系统已更改。

SQL>
```

返回standby服务器

```shell
SQL> SELECT SEQUENCE#, FIRST_TIME, NEXT_TIME FROM V$ARCHIVED_LOG ORDER BY SEQUENCE#;

 SEQUENCE# FIRST_TIME     NEXT_TIME
---------- -------------- --------------
         2 09-8月 -10     10-8月 -10
         3 10-8月 -10     10-8月 -10
         4 10-8月 -10     10-8月 -10
         5 10-8月 -10     10-8月 -10
         6 10-8月 -10     10-8月 -10

SQL> SELECT SEQUENCE#,APPLIED FROM V$ARCHIVED_LOG ORDER BY SEQUENCE#;

 SEQUENCE# APPLIED
---------- ---------
         2 YES
         3 YES
         4 YES
         5 YES
         6 YES

SQL>
```

发现有一条新的记录,说明同步是正常的。


## 容灾关闭

关闭数据库一定要先关闭primary数据库，然后再去关闭standby数据库。

primary数据库

```shell
SQL> shutdown immediate
```

standby数据库

```shell
SQL> alter database recover managed standby database cancel;

数据库已更改。

SQL> shutdown immediate
```

### 主备切换

注：
* 主备切换必须先主切备，在备切主。

#### 1、 primary切换到standby 数据库

在primary数据库做如下操作

```shell
SQL> startup
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
数据库已经打开。
SQL> alter system switch logfile; //主备切换做好做一次归档

系统已更改。

SQL> alter database commit to switchover to standby with session shutdown;

数据库已更改。

SQL> shutdown immediate
ORA-01507: 未装载数据库


ORACLE 例程已经关闭。
SQL> startup nomount               
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
SQL> alter database mount standby database;

数据库已更改。

SQL> alter database recover managed standby database disconnect from session;

数据库已更改。

SQL>
```

#### 2、 standby 切换到 primary

```shell
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
SQL> alter database commit to switchover to primary with session shutdown;
alter database commit to switchover to primary with session shutdown
*
第 1 行出现错误:
ORA-16139: 需要介质恢复


SQL> shutdown immediate
ORA-01109: 数据库未打开


已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
数据库已经打开。
SQL> 
```

至此，primary与standby数据库已经切换完成

如果想再去切换回来，请重复上述操作，注意primary和standby数据库已经发生了变化，以前的primary现在为standby数据库了。


### 切换的最大可用模式

#### 1、 首先应当在standby数据库创建standby redolog

```shell
SQL> startup mount
SQL> alter  database recover managed standby database cancel;
alter  database recover managed standby database cancel
*
第 1 行出现错误:	
ORA-16136: 受管备用恢复未激活

注：
此时只是暂时redo应用，并不是停止Standby数据库，standby仍会保持接收只不过不会再应用接收到的归档，直到你再次启动redo应用为止。

SQL> alter database add standby logfile group 4 '/opt/oracle/oradata/mmsgdb/stdREDO01.LOG' size 500M;  

数据库已更改。

SQL> alter database add standby logfile group 5 '/opt/oracle/oradata/mmsgdb/stdREDO02.LOG' size 500M;

数据库已更改。

SQL> alter database add standby logfile group 6 '/opt/oracle/oradata/mmsgdb/stdREDO03.LOG' size 500M;

数据库已更改。

SQL> alter database add standby logfile group 7 '/opt/oracle/oradata/mmsgdb/stdREDO04.LOG' size 500M;


数据库已更改。

SQL> SQL> ALTER DATABASE RECOVER MANAGED STANDBY DATABASE USING CURRENT LOGFILE DISCONNECT FROM SESSION;     //启动实时应用

数据库已更改。

SQL> 
```

注：
* 1、standy redelog的组数参考公式：（online redolog组数+1）*数据库线程数：单机线程数为1，RAC一般为2
* 2、stabdby redolog的组成员数和大小也尽量和online redolog一样

检查standby redolog是否已经添加成功

```shell
SQL> select group#,thread#,sequence#,archived,status from v$standby_log;

    GROUP#    THREAD#  SEQUENCE# ARC STATUS
---------- ---------- ---------- --- ----------
         4          0          0 YES UNASSIGNED
         5          0          0 YES UNASSIGNED
         6          0          0 YES UNASSIGNED
         7          0          0 YES UNASSIGNED

SQL>
```

#### 2、 standby数据库重新启动恢复管理模式

```shell
SQL> alter database recover managed standby database disconnect from session;
alter database recover managed standby database disconnect from session
*
第 1 行出现错误:
ORA-01153: 激活了不兼容的介质恢复


SQL> 
```

#### 3、 修改primary数据库参数

设置standby数据库为最大性能模式（primary库优先）

```shell
SQL> alter system set log_archive_dest_2='SERVICE=STANDBY SYNC LGWR AFFIRM NET_TIMEOUT=10' SCOPE=SPFILE;

系统已更改。

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             385878544 bytes
Database Buffers         1207959552 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。

SQL> alter database set standby database to maximize availability;

数据库已更改。

SQL> alter database open;

数据库已更改。

SQL>
```

#### 4、 primary数据库侧，查看保护模式

```shell
SQL> select protection_mode ,protection_level from v$database;

PROTECTION_MODE      PROTECTION_LEVEL
-------------------- --------------------
MAXIMUM AVAILABILITY RESYNCHRONIZATION

SQL>
显示当前为最大可用模式。
```

#### 5、 主（primary）备（standby）切换

如果要使得主备库可以切换，则应如步骤1~4同理在主备库做相应修改。

