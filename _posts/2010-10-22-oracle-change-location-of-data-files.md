title:      "Oracle案例--变更数据库中数据文件位置"
subtitle:   "Oracle troubleshoot--Change the location of data files"
date:       2010-10-22
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 变更数据库中数据文件位置

## 适用条件

原存放数据库相关文件磁盘分区空间不足。

注：
*  操作过程中请慎重，防止破坏数据库。

## 操作过程

### 步骤一、查看磁盘空间使用情况

```
mmsg:oracle:mmsgdb > df
Filesystem           1K-blocks      Used Available Use% Mounted on
/dev/sda2             20972152   3111364  17860788  15% /
udev                   4091824       156   4091668   1% /dev
/dev/sda6             25172984  22747280   2425704  91% /home
/dev/sda5             15735128   6036132   9698996  39% /opt
shmfs                  4194304        88   4194216   1% /dev/shm
```

### 步骤二、查看原数据文件位置

```
mmsg:oracle:mmsgdb > sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on Fri Oct 22 11:54:54 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> set wrap off
SQL> set linesize 200
SQL> select * from dba_data_files;
FILE_NAME
---------------------------------------------------------------------------------------------------------------------------
/home/oracle/database/mmsgdb/system01.dbf
/home/oracle/database/mmsgdb/sysaux01.dbf
/home/oracle/database/mmsgdb/undotbs01.dbf
/home/oracle/database/mmsgdb/users01.dbf
/opt/oracle/oradata/mmsgdb/ymmdata01
/opt/oracle/oradata/mmsgdb/cyjdata01
/home/oracle/admin/mmsgdb/mmsgdata/chyjdata01
/home/oracle/admin/mmsgdb/mmsgdata/zzzdata01
/home/oracle/admin/mmsgdb/mmsgdata/skkdata01
/home/oracle/admin/mmsgdb/mmsgdata/zhuzhaozhongdata01
/home/oracle/admin/mmsgdb/mmsgdata/ymdata01

FILE_NAME
---------------------------------------------------------------------------------------------------------------------------
/home/oracle/database/mmsgdb/data11.dbf
/home/oracle/database/mmsgdb/data12.dbf
/home/oracle/database/mmsgdb/data13.dbf
/home/oracle/admin/mmsgdb/mmsgdata/lsjdata01
/home/oracle/admin/mmsgdb/mmsgdata/lxb01
/home/oracle/admin/mmsgdb/mmsgdata/lxb03
/opt/oracle/oradata/MMSGRPT/MMSGNODECDR.DBF
/opt/oracle/oradata/MMSGRPT/MMSGNODEDATA.DBF
/opt/oracle/oradata/MMSGRPT/PRESTAT.DBF
/opt/oracle/oradata/MMSGRPT/MMSGSERVERCDR.DBF
/opt/oracle/oradata/MMSGRPT/MMSGSERVERDATA.DBF

FILE_NAME
---------------------------------------------------------------------------------------------------------------------------
/opt/oracle/oradata/mmsgdb/mmsg.dbf

23 rows selected.
```

大量数据文件在/home路径下，空间严重不足（93%使用率）

### 步骤三、文件路径更改操作执行

关闭数据库

```
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> 
```

启动数据库到mount状态

```
SQL> startup mount
ORACLE instance started.

Total System Global Area  830984192 bytes
Fixed Size                  2148840 bytes
Variable Size             402654744 bytes
Database Buffers          419430400 bytes
Redo Buffers                6750208 bytes
Database mounted. 
```

注：
* 数据库启动到安装状态后，方能进行数据文件的mv操作，否则在未启动到mount状态或者在open状态或者在shutdown状态时，或导致数据库被破坏。
* 当在open状态进行cp操作文件到另外一个位置后，启动数据库到mount状态，然后发布alter database命令，可以成功修改，但是，当open数据库的时候，需要进行介质恢复，修改了多少个数据文件的位置，就需要对多少个数据文件进行介质恢复。

### 步骤四、OS Level mv数据文件到指定位置

```
mv chyjdata01    /opt/oracle/oradata/mmsgdb/chyjdata01  
mv zzzdata01     /opt/oracle/oradata/mmsgdb/zzzdata01
mv skkdata01     /opt/oracle/oradata/mmsgdb/skkdata01 
mv zhuzhaozhongdata01 /opt/oracle/oradata/mmsgdb/zhuzhaozhongdata01
mv ymdata01     /opt/oracle/oradata/mmsgdb/ymdata01           

mmsg:oracle:mmsgdb > cd /home/oracle/database/mmsgdb/
mmsg:oracle:mmsgdb > mv  data11.dbf data12.dbf data13.dbf   /opt/oracle/oradata/mmsgdb/
mmsg:oracle:mmsgdb > cd /home/oracle/admin/mmsgdb/mmsgdata/
mmsg:oracle:mmsgdb > mv lsjdata01 lxb01 lxb03 /opt/oracle/oradata/mmsgdb/
```

### 步骤五、执行修改操作

```
SQL> alter database rename file '/home/oracle/admin/mmsgdb/mmsgdata/chyjdata01','/home/oracle/admin/mmsgdb/mmsgdata/zzzdata01',
  2  '/home/oracle/admin/mmsgdb/mmsgdata/skkdata01','/home/oracle/admin/mmsgdb/mmsgdata/zhuzhaozhongdata01',
  3  '/home/oracle/admin/mmsgdb/mmsgdata/ymdata01'
  4  to '/opt/oracle/oradata/mmsgdb/chyjdata01','/opt/oracle/oradata/mmsgdb/zzzdata01','/opt/oracle/oradata/mmsgdb/skkdata01',
  5  '/opt/oracle/oradata/mmsgdb/zhuzhaozhongdata01','/opt/oracle/oradata/mmsgdb/ymdata01';

Database altered.

SQL> alter database rename file
  2  '/home/oracle/database/mmsgdb/data11.dbf','/home/oracle/database/mmsgdb/data12.dbf',
  3  '/home/oracle/database/mmsgdb/data13.dbf','/home/oracle/admin/mmsgdb/mmsgdata/lsjdata01',
  4  '/home/oracle/admin/mmsgdb/mmsgdata/lxb01','/home/oracle/admin/mmsgdb/mmsgdata/lxb03'
  5  to
  6  '/opt/oracle/oradata/mmsgdb/data11.dbf','/opt/oracle/oradata/mmsgdb/data12.dbf',
  7  '/opt/oracle/oradata/mmsgdb/data13.dbf','/opt/oracle/oradata/mmsgdb/lsjdata01',
  8  '/opt/oracle/oradata/mmsgdb/lxb01','/opt/oracle/oradata/mmsgdb/lxb03';

Database altered.

SQL> alter database open;

Database altered.
```

### 步骤六、查看修改后的数据文件位置

```
SQL> select * from dba_data_files;

FILE_NAME
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/home/oracle/database/mmsgdb/system01.dbf
/home/oracle/database/mmsgdb/sysaux01.dbf
/home/oracle/database/mmsgdb/undotbs01.dbf
/home/oracle/database/mmsgdb/users01.dbf
/opt/oracle/oradata/mmsgdb/ymmdata01
/opt/oracle/oradata/mmsgdb/cyjdata01
/opt/oracle/oradata/mmsgdb/chyjdata01
/opt/oracle/oradata/mmsgdb/zzzdata01
/opt/oracle/oradata/mmsgdb/skkdata01
/opt/oracle/oradata/mmsgdb/zhuzhaozhongdata01
/opt/oracle/oradata/mmsgdb/ymdata01

FILE_NAME
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/opt/oracle/oradata/mmsgdb/data11.dbf
/opt/oracle/oradata/mmsgdb/data12.dbf
/opt/oracle/oradata/mmsgdb/data13.dbf
/opt/oracle/oradata/mmsgdb/lsjdata01
/opt/oracle/oradata/mmsgdb/lxb01
/opt/oracle/oradata/mmsgdb/lxb03
/opt/oracle/oradata/MMSGRPT/MMSGNODECDR.DBF
/opt/oracle/oradata/MMSGRPT/MMSGNODEDATA.DBF
/opt/oracle/oradata/MMSGRPT/PRESTAT.DBF
/opt/oracle/oradata/MMSGRPT/MMSGSERVERCDR.DBF
/opt/oracle/oradata/MMSGRPT/MMSGSERVERDATA.DBF

FILE_NAME
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/opt/oracle/oradata/mmsgdb/mmsg.dbf

23 rows selected.
SQL> exit
Disconnected from Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
mmsg:oracle:mmsgdb >
```

### 步骤七、查看更改数据文件路径后的空间使用情况

```
256 mmsg [wyz] :/home >df
文件系统               1K-块        已用     可用 已用% 挂载点
/dev/sda2             20972152   3111392  17860760  15% /
udev                   4091824       156   4091668   1% /dev
/dev/sda6             25172984  17642036   7530948  71% /home
/dev/sda5             15735128   9672944   6062184  62% /opt
shmfs                  4194304        88   4194216   1% /dev/shm
```

至此，永久性数据库文件路径更改完毕。

至于临时文件的更改位置，操作和永久性文件操作方法一致，或者删除临时文件，重新创建既可，因为临时文件不存放任何数据，仅用于排序操作；对于控制文件，则需要独立创建控制文件或通过控制文件多工方式来进行转移位置，具体操作详见《oracle本地磁盘数据文件更改到lv上》中“变更控制文件位置”部分操作。

