---
layout:     post
title:      "oracle RMAN备份与恢复"
subtitle:   "rman backup and recovery"
date:       2011-06-07
author:     "Gavin"
catalog:    true
tags:
    - rman
    - oracle
---


## RMAN简介

 

RMAN 可以用来备份和恢复数据库文件、归档日志和控制文件，也可以用来执行完全或不完全的数据库恢复。RMAN有三种不同的用户接口：COMMAND LINE方式、GUI 方式（集成在OEM 中的备份管理器）、API 方式（用于集成到第三方的备份软件中）。具有如下特点： 

1）功能类似物理备份，但比物理备份强大N倍，从下面的特点可以看到； 

2）可以压缩空块； 

3）可以在块水平上实现增量； 

4）可以把备份的输出打包成备份集，也可以按固定大小分割备份集； 

5）备份与恢复的过程可以自动管理； 

6）可以使用脚本（存在Recovery catalog 中） 

7）可以做坏块监测

 

## RMAN术语

### Backup Sets （备份集合）

  备份集合的特性：包括一个或多个数据文件或归档日志，以oracle专有的格式保存，有一个完全的所有的备份片集合构成，构成一个完全备份或增量备份。

 

### Backup Pieces （备份片）

一个备份集由若干个备份片组成。每个备份片是一个单独的输出文件。一个备份片的大 小是有限制的；如果没有大小的限制， 备份集就只由一个备份片构成。备份片的大小不能 大于使用的文件系统所支持的文件长度的最大值。

 

### Image Copies 镜像备份

  镜像备份是独立文件（数据文件、归档日志、控制文件）的备份。它很类似操作系统级 的文件备份。它不是备份集或备份片，也没有被压缩。

### Full backup Sets 全备份集合

全备份是一个或多个数据文件中使用过的数据块的的备份。没有使用过的数据块是不被备份的，也就是说，oracle 进行备份集合的压缩。

 

### Incremental backup sets 增量备份集合

  增量备份是指备份一个或多个数据文件的自从上一次同一级别的或更低级别的备份以来被修改过的数据块。 与完全备份相同，增量备份也进行压缩。

File multiplexing  多工

多个数据文件可以在一个备份集中。

 

### Recovery catalog resyncing 恢复目录同步

  使用恢复管理器执行 backup、copy、restore 或者 switch 命令时，恢复目录自动进行更 新，但是有关日志与归档日志信息没有自动记入恢复目录。需要进行目录同步。使用 resync catalog命令进行同步。

RMAN> resync catalog；

 

### Incarnation 对应物

  在不完全恢复完成之后，通常需要使用 resetlogs 选项来打开数据库。resetlogs 表示一个 数据库逻辑生存期的结束和另一个数据库逻辑生存期的开始。数据库的逻辑生存期也被称为 一个对应物（incarnation）。每次使用 resetlogs 选项来打开数据库后都会创建一个新的数据库 对应物。

 

## RMAN备份形式

RMAN备份有两种形式：

1、镜像备份（image copies）；

2、备份集备份（backup sets）。

 

### 镜像备份

镜像备份实际就是RMAN利用目标数据库服务进程来完成文件的copy操作，是数据文件、控制文件或者归档日志文件的副本。

RMAN镜像备份的副本无法通过list backup显示，可以通过list copy显示。

本文主要描述备份集备份。

 

### 备份集备份

备份集是通过RMAN创建的逻辑备份对象，一个备份集中可以包括多个控制文件、数据文件、归档文件。

备份集在物理上由多个备份片段组成，每个备份片段就是一个操作系统文件。

 

## RMAN备份类型

利用RMAN进行备份时，可以通过三种方式来对RMAN的备份做分类

### 完全备份(Full Backup)与增量备份(Incremental Backup)

 

全备与增备是针对数据文件而言，控制文件和归档日志文件不能进行增量备份。当然，后两者可以做备份优化。

 

### 打开备份(Open Backup)或关闭备份(Closed Backup)

数据库打开状态下进行备份即是打开备份，数据库关闭状态下(加载状态)进行的备份即关闭备份。

 

### 一致备份(Consistent Backup)与不一致备份(Inconsistent Backup)

数据库打开状态或不干净关闭状态(shutdown abort)进行的备份是不一致备份，利用不一致的备份修复数据库后还需要做数据库的恢复。在数据库干净关闭状态进行的备份是一致备份，利用一致备份修复数据库后不需要做数据库的恢复。

## RMAN report list delete命令详解

### report

```
1. 报告目标数据库的物理结构              RMAN> report schema;

2. 报告最近N天尚未备份的数据文件           RMAN> report need backup days=3;

3. 报告表空间上最近N天未备份的数据文件         RMAN> report need backup days=3 tablespace MMSG;

4. 报告恢复数据文件需要的增量备份个数超过3次的数据文件 RMAN> report need backup incremental 3;

5. 报告备份文件低于2份的所有数据文件         RMAN> report need backup redundancy 2 database;

6. 报告文件报表的恢复需要超过6天的归档日志的数据文件  RMAN> report need backup recovery window of 6 days;

7. 报告数据库所有不可恢复的数据文件          RMAN> report unrecoverable;

8. 报告备份次数超过2次的陈旧备份           RMAN> report obsolete redundancy 2;

9. 报告多余的备份                  RMAN> report obsolete;
```

 

### list

```
list backup;             列出详细备份

list expired backup;         列出过期备份

list backup of database;       列出所有数据文件的备份集

list backup of tablespace MMSG;    列出特定表空间的所有数据文件备份集

list backup of controlfile;      列出控制文件备份集

list backup of archivelog all;    列出归档日志备份集详细信息

list archivelog all;　　　　　　    列出归档日志备份集简要信息

list backup of spfile;        列出SPFILE备份集

list copy of datafile 5;       列出数据文件映像副本

list copy of controlfile;       列出控制文件映像副本

list copy of archivelog all;     列出归档日志映像副本

list incarnation of database;     列出对应物/列出数据库副本

list backup summary;         概述可用的备份（B表示backup、F表示FULL、A表示archive log、S说明备份状态（A　AVAILABLE　　　X EXPIRED )

  

list backup by file;         按备份类型列出备份

​                   按照数据文件备份，归档日志备份，控制文件备份，服务器参数文件备份　列出
```

 

 

### check

```
RMAN> crosscheck backup;               核对所有备份集 

RMAN> crosscheck backup of database;         核对所有数据文件的备份集 

RMAN> crosscheck backup of tablespace MMSG;      核对特定表空间的备份集 

RMAN> crosscheck backup of datafile 4;        核对特定数据文件的备份集 

RMAN> crosscheck backup of controlfile;        核对控制文件的备份集 

RMAN> crosscheck backup of spfile;          核对SPFILE的备份集 

RMAN> crosscheck backup of archivelog sequence 3;   核对归档日志的备份集

RMAN> crosscheck copy;                 核对所有映像副本

RMAN> crosscheck copy of database;          核对所有数据文件的映像副本

RMAN> crosscheck copy of tablespace MMSG;       核对特定表空间的映像副本 

RMAN> crosscheck copy of datafile 6;         核对特定数据文件的映像副本 

RMAN> crosscheck copy of archivelog sequence 4;    核对归档日志的映像副本 

RMAN> crosscheck copy of controlfile;         核对控制文件的映像副本

RMAN> crosscheck backup tag='SAT_BACKUP';

RMAN> crosscheck backup completed after 'sysdate - 2';

RMAN> crosscheck backup completed between 'sysdate - 5' and 'sysdate -2 ';

RMAN> crosscheck backup device type sbt;

RMAN> crosscheck archivelog all;

RMAN> crosscheck archivelog like '%ARC00012.001';

RMAN> crosscheck archivelog from sequence 12;

RMAN> crosscheck archivelog until sequence 522;
```

 

### delete

```
RMAN> delete obsolete;         删除陈旧备份；

RMAN> delete expired backup;      删除EXPIRED备份 

RMAN> delete expired copy;       删除EXPIRED副本

RMAN> delete backupset 19;       删除特定备份集

RMAN> delete backuppiece '/opt/oracle/oradata/backup/test.ora';  删除特定备份片

RMAN> delete backup;          删除所有备份集

RMAN> delete datafilecopy '/opt/oracle/oradata/backup/test.bak'; 删除特定映像副本

RMAN> delete copy;           删除所有映像副本

RMAN> delete archivelog all delete input;

RMAN> delete backupset 22 format = '/opt/oracle/oradata/backup/%u.bak' delete input;

​                    在备份后删除输入对象      

RMAN> delete backupset id;       删除备份集
```

 

 

## RMAN备份

### 备份整个数据库

```
run {

allocate channel c1 type disk;

backup

full

tag full_db_backup

format "/opt/oracle/mmsg.load/db_t%t_s%s_p%p"

(database);

release channel c1;

}
```

 

### 备份指定的数据文件

```
backup datafile '/opt/oracle/oradata/mmsgdb/test.dbf';
```

 

### 备份表空间

```
backup tablespace MMSG;
```

 

### 备份控制文件

方法1：

```
configure controlfile autobackup on;
```

方法2：

```
backup current controlfile;
```

方法3:

```
backup database include current controlfile;
```

 

### 备份归档日志

```
backup archivelog all;
```

 

### 增量备份

建立一个增量级别为0的全库备份：

```
 backup INCREMENTAL LEVEL=0 database;
```

建立一个增量级别为1的数据库表空间的备份：

```
 backup incremental level=1 tablespace MMSG;
```

 

注：

Rman默认创建的增量备份是Differential方式，如果要建立Cumulative方式的增量备份，在执行BACKUP命令时显式指定即可，例如：

```
RMAN> BACKUP INCREMENTAL LEVEL=2 CUMULATIVE DATABASE;
```

 

### 冗余备份

步骤一：显示指定copies数量

```
RMAN> backup copies 2 tablespace MMSG;
```

步骤二：在批处理中增加set backup copies参数：

```
RMAN> run

{

set backup copies 1;

allocate channel c1 device type disk;

backup tablespace MMSG;

}
```

步骤三：通过configure设定预备份Duplexed方式

 

## RMAN恢复

### 恢复spfile文件

```
RMAN> startup nomount

RMAN> set dbid=1037536304

RMAN> restore spfile from autobackup; #这里confile autobackup必须设置成on

RMAN> startup force
```

 

### 表空间的恢复

```
RMAN> shutdown immediate

RMAN>startup mount

RMAN>restore tablespace "TEST"; #TEST为要恢复的表空间名

RMAN>recover tablespace "TEST";

RMAN>alter database open;
```

 

### 数据文件的恢复

这个操作类似于表空间的恢复

```
RMAN>shutdown immediate

RMAN>startup mount

RMAN>restorer datafile datafilepath; #或者是restore datafile datafile_num;

RMAN>recover datafile datafilepath;  #或者是recover datafile datafile_num;

RMAN>alter database open
```

 

### 全库的恢复

```
RMAN>shutdown immediate

RMAN>startup mount

RMAN> run

2> {

3> allocate channel c1 device type disk;

4> restore database;

5> }
```

 

### 控制文件的恢复

**1****、损坏部分控制文件** 

  步骤一：使用dbv命令检测控制文件是否被损坏，如：dbv file=control02.ctl blocksize=16384

  步骤二：cp好的控制文件，并重命名

**2****、所有控制文件均被损坏**

  损坏所有的控制文件或者人为的删除所有的控制文件，通过备份复制已经不能解决问题，只能重新建立新的控制文件。

  保留dba用户执行 alter database backup controlfile to trace 产生的重建控制文件的命令

  步骤一:

  关闭数据库，修改trace文件中创建control文件部分，dba用户执行脚本重创控制文件;

  步骤二 :

重启数据库

 

  如果数据库运行在归档模式下，且有控制文件的备份(CONFIGURE CONTROLFILE AUTOBACKUP ON)，可以使用有可用的控制文件的备份，则可以使用restore controlfile from ‘备份的控制文件路径+文件名’来完成控制文件的恢复操作

  1、数据库启动到非安装状态(nomount)

  2、RMAN恢复

 

```
 RMAN> run {

   allocate channel c1 device type disk;

   restore controlfile from ‘/opt/oracle/rman/back_c-1037536304-20101123-07’;

   release channel c1;

   }
```

 

### 重做日志文件的恢复

```
SQL> shutdown immediate

数据库已经关闭。

已经卸载数据库。

ORACLE 例程已经关闭。

SQL> startup mount

SQL> recover database using backup controlfile until cancel;

SQL> alter database open resetlogs;
```

 

### 归档日志文件的恢复

```
RMAN>shutdown immediate

RMAN>startup mount

RMAN> run

2> {

3> allocate channel c1 device type disk;

4> restore archivelog all;

5> }
```

 

### 损坏非当前联机日志

步骤一 启动数据库，报错：ORA-00313和ORA-00312

步骤二 查看v$log视图

步骤三  用CLEAR命令重建该日志文件 

```
SQL> alter database clear logfile group 3;
```

​      如果是该日志组还没有归档，则需要用

   

```
  SQL>alter database clear unarchived logfile group 3;
```

步骤四  打开数据库，并备份数据库 

```
 SQL> alter database open;
```

 

### 损坏当前联机日志

一、数据库正常关闭，日志文件中没有未决的事务需要实例恢复，当前日志组的损坏，可以直接使用alter database clear unarchived logfile group N;命令来重建

```
  SQL> alter database clear unarchived logfile group 2;

  SQL> alter database open;
```

 

二、日志组中有活动事务，需要介质恢复，日志组需要用来数据同步，有两种解决方法：

1、通过不完全恢复，保持数据库数据一致性，这种方法要求数据库运行在归档方式下，且有可用的数据文件的备份

  步骤一 启动数据库，报错：ORA-00313 ，ORA-00312， ORA-27037

  步骤二 模拟当前日志组中日志文件损坏 SQL> select * from v$log;

  步骤三 拷贝有效的备份，进行不完全恢复（包括所有的控制文件、数据文件、redo文件）

  步骤四 数据库启动到mount状态，进行不完全恢复：

```
      SQL> startup mount

      SQL> recover database until cancel;

      SQL> alter database open resetlogs;
```

 注：这个时候是不能用rman进行恢复的！

 

2、通过强制性恢复，这种方法会导致数据的不一致性，推荐使用方法一

  步骤一 模拟当前日志组中日志成员被损坏 SQL> select * from v$log;

  步骤二 修改pfile文件，增加隐性参数

 

```
 vi /opt/oracle/admin/mmsgdb/pfile/init.ora.232011183420

  \#add for test by wangyunzeng

  _allow_resetlogs_corruption=TRUE
```

 

步骤三 通过pfile文件启动数据库

步骤四 进行介质恢复 

```
SQL> recover database until cancel;
```

​      出现如下信息时，选择cancel命令  指定日志:

```
 {<RET>=suggested | filename | AUTO | CANCEL}
 cancel
```

  步骤五 resetlogs方式启动数据库

```
SQL> alter database open resetlogs;
```

  步骤六 关闭数据库，去掉pfile文件中隐性参数，重启数据库（直接执行startup命令即可）

  步骤七 备份整个数据库  物理冷备或者物理热备或者RMAN备份都行。

 

  步骤八 导入数据   如果有相关的exp导出的数据，可以执行imp导入操作，毕竟数据发生丢失。

 

  步骤九 表数据分析  建议执行一下表分析 

```
SQL> ANALYZE TABLE time VALIDATE STRUCTURE CASCADE;
```

 

### 临时数据文件的恢复

临时数据文件不包含有效数据，发生丢失后删除原先临时数据文件并进行重建就可以了。

 

## RMAN实战

### 实战1

要求

1 、每天夜间1点执行；

2 、数据库全备，同时备份控制文件及归档日志文件，备份文件保存至：/opt/oracle/rman目录下，并在完成归档日志文件备份后，自动删除已备份的归档日志；

3 、备份保留7天，过期则自动删除；

4 、保留操作日志备查；

 

RMAN脚本

```
oracle@mmsg:~/rman> more back_full.rman

run

{

configure retention policy to recovery window of 7 days;

configure controlfile autobackup on;

configure controlfile autobackup format for device type disk to '/opt/oracle/rman/full_bak_%F';

allocate channel c1 device type disk format '/opt/oracle/rman/full_bak_%U';

backup database skip inaccessible filesperset 10 plus archivelog filesperset 20 delete all input;

release channel c1;

}

allocate channel for maintenance device type disk;

crosscheck backupset;

delete noprompt obsolete;
```

 

SKIP 选项 说明

SKIP INACCESSIBLE ：表示跳过不可读的文件。我们知道一些offline的数据文件只要存在于磁盘上就仍然可被读取，但是可能有些文件已经被删除或移到它处造成不可读，加上这个参数就会跳过这些文件；

SKIP OFFLINE ：跳过offline的数据文件；

SKIP READONLY ：跳过那些所在表空间为read-only的数据文件；

 

命令执行

```
oracle@mmsg:~/rman> rman target / msglog /opt/oracle/rman/bak.log cmdfile=/opt/oracle/rman/back_full.rman
```

 

```
oracle@mmsc103:~/rmanbak> more backup.pl

#!/usr/bin/perl

###    作用：rman定时任务脚本       ###

#获取系统当前时间

my ($sec,$min,$hour,$day,$month,$year)= localtime(time());

$year+=1900;

$month=sprintf("%02d",$month+1);

$day=sprintf("%02d",$day);

$hour=sprintf("%02d",$hour);

$min=sprintf("%02d",$min);

$sec=sprintf("%02d",$sec);

my $daytime = "$year$month$day$hour$min$sec";

system("/opt/oracle/product/11g/bin/rman  cmdfile = '/opt/oracle/rmanbak/everydaybak.rman' msglog=/opt/oracle/rmanbak/everydaybak_$

daytime.log");
```

 

设置crontab

每天凌晨1点执行数据库的备份

```
0 1 * * * su - oracle -c /opt/oracle/rmanbak/backup.pl
```

 

### 实战2

1、备份整个数据库，包括控制文件以及归档日志；

2、清除3天前备份的归档日志。

 

RMAN脚本

```
oracle@mmsc103:~/rmanbak> more everydaybak.rman

#script.:fullbakup.rman

# creater:wangyunzeng

# date:2011-03-11

# desc:backup all database datafile in archive with rman

# connect database

connect target rman/rman;

connect catalogrman/rman@mmsgdb;

#start backup database

run

{

 allocate channel t1 type disk; 

configure controlfile autobackup format for device type disk to '/opt/oracle/rmanbak/controlfile_bak_%F';            

backup database format 'fullbak_%s_%p_%u'  (archivelog all );

crosscheck backupset;

delete noprompt obsolete;

delete noprompt archivelog until time "sysdate -3";

release channel t1;     

}

#end
```

 

 

## RMAN常见问题解决方法

### RMAN命令输入后终端无反应，一直处于等待状态，且长时间如此

原因：操作系统也有一个rman命令，这里执行的是os的rman而非Oracle的

解决：oracle用户设置环境变量 export PATH=$ORACLE_HOME:$PATH

 

### RMAN无法进行备份操作/查看备份信息/配置信息

RMAN-03002: list 命令 (在 03/05/2011 09:28:03 上) 失败

RMAN-06004: 恢复目录数据库发生 ORACLE 错误: RMAN-20001: target database not found in recovery catalog

 

RMAN-03002: backup 命令 (在 03/05/2011 09:28:32 上) 失败

RMAN-03014: 恢复目录的隐式重新同步失败

RMAN-06004: 恢复目录数据库发生 ORACLE 错误: RMAN-20001: 在恢复目录中未找到目标数据库

 

原因：RMAN未注册。

解决方法：注册RMAN。

```
RMAN> register database;           
```

​           

 

### RMAN备份文件异常删除

  原因：RMAN备份的文件存放在某个目录下，该文件没有通过rman命令delete删除，而是在操作系统侧执行rm操作，导致再去删除这个备份文件时无法删除掉。

解决：

```
RMAN> list backupset by backup summary;

RMAN> crosscheck backupset;

RMAN> delete backupset;
```

 

 

## 与RMAN备份相关的动态性能表

V$ARCHIVED_LOG ：   本视图包含了所有归档重做日志文件的创建情况，备份情况以及其他信息。

V$BACKUP_CORRUPTION ：这个视图显示了RMAN在哪些备份集中发现了损坏的数据坏。在你使用BACKUP VALIDATE命令对备份集进行检查时如果发现了损坏的数据块，RMAN将在这个视图中写入记录。

V$COPY_CORRUPTIO ：  本视图显示了哪些镜像复制备份文件已经被损坏。

V$BACKUP_DATAFILE ： 本视图通常用来获取每个数据文件中非空白数据块的数量，从而帮助你创建出大小基本相等的备份集。另外，在视图中也包含了数据文件中损坏的数据块的信息。

V$BACKUP_REDOLOG ：  本视图显示了在现有的备份集中有哪些归档重做日志文件。

V$BACKUP_SET ：    本视图显示了已经创建的备份集的信息。

V$BACKUP_PIECE ：   本视图显示了已经创建的备份片段的信息。

 

 
