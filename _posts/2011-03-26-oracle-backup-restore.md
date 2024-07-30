---
layout:     post
title:      "Oracle备份与恢复概述"
subtitle:   "Oracle backup and restore"
date:       2011-03-26
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 什么是备份 

所谓备份，就是把数据库复制到转储设备的过程。其中，转储设备是指用于放置数据库拷贝的磁带(sbt)或磁盘(disk)。通常也将存放于转储设备中的数据库的拷贝称为原数据库的备份或转储。

# 备份分类

ORACLE数据库的备份分为物理备份和逻辑备份两种。

## 物理备份

物理备份是将实际组成数据库的操作系统文件从一处拷贝到另一处的备份过程。可以使用 Oracle 的恢复管理器（Recovery Manager，RMAN）或操作系统命令进行数据库的物理备份。

## 逻辑备份

逻辑备份是利用SQL语言从数据库中抽取数据并存于二进制文件的过程。Oracle提供的逻辑备份工具是exp/expdp。数据库逻辑备份是物理备份的补充。


根据在物理备份时数据库的状态，可以将备份分为一致性备份（consistent backup）和不一致性备份（inconsistent backup）两种：

## 一致性备份

一致性备份是当数据库的所有可读写的数据库文件和控制文件具有相同的系统改变号（SCN），并且数据文件不包含当前 SCN 之外的任何改变。在做数据库检查点时，Oracle 使所有的控制文件和数据文件一致。对于只读表空间和脱机的表空间，Oracle 也认为它们是一致的。使数据库处于一致状态的唯一方法是数据库正常关闭（用shutdown normal 或 shutdown immediate 命令关闭）。因此，只有在以下条件下的备份是一致性备份：

数据库正常关闭（用shutdown normal 或 shutdown immediate 命令关闭）。 

## 非一致性备份

不一致性备份是当数据库的可读写的数据库文件和控制文件的系统改变号（SCN）在不一致条件下的备份。对于一个 7*24 工作的数据库来说，由于不可能关机，而数据库数据是不断改变的，因此只能进行不一致备份。在 SCN 号不一致的条件下，数据库必须通过应用重做日志使 SCN 一致的情况下才能启动。因此，如果进行不一致备份，数据库必须设为归档状态，并对重做日志归档才有意义。在以下条件下的备份是不一致性备份： 

数据库处于打开状态； 

数据库处于关闭状态，但是用非正常手段关闭的。例如，数据库是通过 shutdown abort 或机器掉电等等方法关闭的。 

汇总如下图所示：

<img class="shadow" src="/img/in-post/oracle_backup.png" width="600">

# 什么是恢复 

所谓恢复，就是把数据库由存在故障的状态转变为无故障状态的过程。

## 根据出现故障的原因，恢复分为两种类型

### 实例恢复

这种恢复是Oracle实例出现失败后，Oracle自动进行的恢复。 

### 介质恢复

这种恢复是当存放数据库的介质出现故障时所做的恢复。本文后面提到的恢复都是指介质恢复。

装载（restore）物理备份与恢复（recover）物理备份是介质恢复的手段。装载是将备份考回到磁盘，恢复是利用重做日志（物理备份的一部分）修改考回到磁盘的数据文件（物理备份的另一部分），从而恢复数据库的过程。

## 根据数据库的恢复程度，将恢复方法分为两种类型

### 完全恢复

将数据库恢复到数据库失败时数据库的状态。这种恢复是通过装载数据库备份和并应用全部的重做日志做到的。 

### 不完全恢复

将数据库恢复到数据库失败前的某一时刻数据库的状态。这种恢复是通过装载数据库备份和并应用部分的重做日志做到的。进行不完全恢复后必须在启动数据库时用 resetlogs 选项重设联机重做日志。 

例如，在上午10：00，由于磁盘损坏导致数据库中止使用。现在使用两种方法进行数据库的恢复，第一种方法使数据库可以正常使用，且使恢复后与损坏时（10：00）数据库中的数据相同，那么第一种恢复方法就属于完全恢复类型；第二种方法能使数据库正常使用，但只能使恢复后与损坏前（例如9：00）数据库中的数据相同，没能恢复数据库到失败时（10:00）数据库的状态，那么第二种恢复方法就属于不完全恢复类型。

事实上，如果数据库备份是一致性的备份，则装载后的数据库即可使用，从而也可以不用重做日志恢复到数据库备份时的点。这也是一种不完全恢复。 


# 备份与恢复的关系 

备份一个ORACLE数据库，类似于买医疗保险——在遇到疾病之前不会意识到它的重要性，获得保险金的数量取决于保险单的种类。同理，随着制作备份的种类和频繁程度的不同，数据库发生故障后其恢复的可行性、难度与所花费的时间也不同。 

数据库故障是指数据库运行过程中影响数据库正常使用的特殊事件。数据库故障有许多类型，最严重的是介质失败（如磁盘损坏），这种故障如不能恢复将导致数据库中数据的丢失。数据库故障类型有： 

* 语句失败
* 用户进程失败
* 实例失败
* 用户或应用错误操作    #这类错误可能是意外地删除了表中的数据等错误操作。 
* 介质失败              #如硬盘失败，硬盘中的数据丢失。 
* 自然灾害              #如地震、洪水等。 

由于故障类型的不同，恢复数据库的方法也不同。通过装载备份来恢复数据库既是常用的恢复手段，也是恢复介质失败故障的主要方法。 

# 备份与恢复要考虑的问题

备份与恢复要考虑以下的三个问题：

* 备份与恢复策略要考虑的商业、操作、及技术问题
* 灾难恢复计划的组成
* 测试备份与恢复策略的重要性

能够进行什么样的恢复依赖于有什么样的备份。作为 DBA，有责任从以下三个方面维护数据库的可恢复性：

* 使数据库的失效次数减到最少，从而使数据库保持最大的可用性 
* 当数据库不可避免地失效后，要使恢复时间减到最少，从而使恢复的效率达到最高
* 当数据库失效后，要确保尽量少的数据丢失或根本不丢失，从而使数据具有最大的可恢复性

# Oracle的运行方式

oracle数据库有两种运行方式：

* 归档方式（archivelog）
* 非归档方式（noarchivelog）

归档方式的目的是当数据库发生故障时可最大限度的恢复数据库，可以保证不丢失任何已提交的数据；不归档方式只能恢复数据库到最近的回收点（冷备份或是逻辑备份）。我们根据数据库的高可用性和用户可承受丢失的工作量的多少，对于生产数据库，强烈要求采用归档方式；那些正在开发和调试的数据库可以采用不归档方式。

默认情况下，安装oracle数据库是非归档方式，可以修改数据库的运行方式的，具体操作如下：

## 由非归档方式调整成归档方式

```shell
node1:oracle:mmsgdb > sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on Tue Feb 22 11:42:35 2011

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> archive log list
Database log mode              No Archive Mode  #非归档方式
Automatic archival             Disabled
Archive destination            /opt/oracle/product/11g/dbs/arch
Oldest online log sequence     4911
Current log sequence           4913
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup mount
ORA-32004: obsolete and/or deprecated parameter(s) specified
ORACLE instance started.

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size            1342179856 bytes
Database Buffers          251658240 bytes
Redo Buffers                7413760 bytes
Database mounted.
SQL> alter database archivelog;

Database altered.

SQL> alter database open;

Database altered.

SQL> archive log list
Database log mode              Archive Mode   #归档模方式
Automatic archival             Enabled
Archive destination            /opt/oracle/product/11g/dbs/arch
Oldest online log sequence     4911
Next log sequence to archive   4913
Current log sequence           4913
SQL>
```

## 由归档方式调整成非归档方式

```shell
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup mount
ORA-32004: obsolete and/or deprecated parameter(s) specified
ORACLE instance started.

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size            1342179856 bytes
Database Buffers          251658240 bytes
Redo Buffers                7413760 bytes
Database mounted.
SQL> alter database noarchivelog;

Database altered.

SQL> alter database open; 

Database altered.

SQL> archive log list;
Database log mode              No Archive Mode
Automatic archival             Disabled
Archive destination            /opt/oracle/product/11g/dbs/arch
Oldest online log sequence     4911
Current log sequence           4913
SQL>
```

数据库运行在归档方式下，是以消耗一部分性能作代价的，因为日志要归档，系统io比非归档方式要高，但它不会丢失已经提交的任何数据。

注：
* 从归档方式修改到非归档方式后，一定要做一次数据库全冷备份。

# 物理备份与恢复

## 冷备

冷备步骤如下：

### 1、正常关闭数据库

```shell
shutdown immediate
```

### 2、拷贝数据库文件到指定存储位置

这里的数据库文件包括数据文件、控制文件、重做日志文件、spfile文件（可选）。

### 3、启动数据库

```shell
startup
```

冷备的优点是简单、快捷、方便，缺点是备份文件占用空间，且数据只能恢复到备份前状态。日常工作中，可以使用脚本进行数据库的冷备操作，提供一个简单oracle数据库冷备perl脚本：

```shell
#/usr/bin/perl

###############################################################
##      作用：数据库备份与还原操作                        ##
##      Create： 2010-12-31                                   ##
###############################################################

## 选择1：冷备
## 选择2：逻辑备份（输入用户名和密码--全表备份或者应用级表备份）
## 选择3：冷恢复
## 选择4：数据导入

#判断当前登录用户，非oracle，退出
my $localuser;      #定义当前登录用户
$localuser = getlogin || (getpwuid($<))[0] || die "Can't find a user here!!!\n";
#print "当前登录用户是$localuser\n";
@foo = @foo[0 .. $#foo];  

##判断oracle用户是否存在
if($localuser eq "oracle")
{
  #当前路径信息
  my $path = `pwd`;
  chomp($path);
  
  @foo = @foo[0 .. $#foo];  
  print '-' x 50,"\n";
  print "请选择操作类型,例如：2 \n";
  print "\n\t1:数据库冷备\t2:数据导出t3:RMAN备份\n";
  print "@foo\n";
  
  chomp ($response = <STDIN>);
  $response = lc($response);
    if($response eq "1")
      {   
      print "\n冷备oracle数据库......\n";
      ##剩余空间检测
      &space;
      chdir "$path";
      #备份执行
      &cool_bak;
      }
    elsif($response eq "2")
      {
        print "\n逻辑备份数据库.\n";
       &logic;
      }
    else
      {
          print "输入非法，操作退出!\n";
          print "@foo\n"; 
      }
  
  #定义子函数
  ##冷备数据库
  sub cool_bak
  {
     #获取时间
     my ($sec,$min,$hour,$day,$month,$year)= localtime(time());
     $year+=1900;
     $month=sprintf("%02d",$month+1);
     $day=sprintf("%02d",$day);
     my $daytime = "$year$month$day$hour$min$sec";
     chomp($daytime);
     
     #备份文件存放路径
     my $path = `pwd`;
     chomp($path);
     
     #目录
     unless (-d "coolbackup")      # 如果目录不存在，创建目录
     {
         mkdir("coolbackup", 0755) || die "Make directory coolbackup error.\n";
     }
     chdir "coolbackup";
     
     
       ##导出当前数据库中系统参数、数据文件、控制文件、重做日志文件等信息
       print "\n";
       print '-' x 50, "\n";
       
       ##检测数据库运行状态，只有在open状态下才能进行参数写文件的备份
       open(SQLPLUS, "|sqlplus  / as sysdba > loginfo.txt") || die "Execute sqlplus error!\n";
       close(SQLPLUS) || die "Execute sql error!\n";
       
       my $login = `cat loginfo.txt  \| head \-n 7 \| grep \-v SQL \| grep \-v Copyright \| sed \'\/\^\$\/d\'`;
       chomp($login);
       if($login=~ m/Connected to:/ || $login=~ m/连接到:/)
       {
         print "\n数据库处于open状态，可以进行下一步备份操作!\n";
         unlink("./loginfo.txt");
       }
       else
       {
         print "\n数据库被关闭，无法进行下一步备份操作！\n";
         print "\n退出当前备份。\n";
         unlink("./loginfo.txt");
         exit;
         print "\n";
       }
       
       print "oracle冷备第一步：写参数、数据文件信息到文件!\n";
       print "开始写入信息到文件......\n";
       print "\n";
       open (SQLPLUS, "|sqlplus -S / as sysdba >/dev/null") || die "Execute sqlplus error!\n";
       print SQLPLUS "set feedback off\nset sqlnumber off\n";
       print SQLPLUS "set colsep \"\;\"\n";
       print SQLPLUS "set wrap off\n";
       print SQLPLUS "set pagesize 0\nset linesize 32767\n";
       print SQLPLUS "set trimspool off\n";
       print SQLPLUS "set sqlblanklines off\n";
       print SQLPLUS "spool tmp.txt\n";
       print SQLPLUS "select * from v\$parameter;\n";
       print SQLPLUS "select * from props\$;\n";
       print SQLPLUS "select * from v\$datafile;\n";
       print SQLPLUS "select * from v\$controlfile;\n";
       print SQLPLUS "select * from v\$logfile;\n";
       print "\n结束写入信息到文件.\n";
       print "\n";
       print "\n";
       
       
       print '-' x 50, "\n";
       print "oracle冷备第二步：关闭数据库，备份相关文件!\n"; 
       print SQLPLUS "set linesize 80\n";
       print SQLPLUS "spool wyztest.txt\n";
       print SQLPLUS "select \'cp \'\||name \|| \' \./\' from v\$datafile;\n";
       print SQLPLUS "select \'cp \'\||name \|| \' \./\' from v\$controlfile;\n";
       print SQLPLUS "select \'cp \'\||member \|| \' \./\' from v\$logfile;\n";
       
       print SQLPLUS "spool off\n";
       
       ##停止数据库
       system("sleep 2");
       system("cp wyztest.txt coolbak.sh");
       system("chmod \+x coolbak.sh");
       print "开始关闭数据库，请稍候......\n";
       print SQLPLUS "shutdown immediate";
       system("sleep 30");
       &ckstatus;
       print "\n数据库已经停止\n";
       
       #备份文件  
       print "\n开始备份文件，请稍候......\n";
       system("sh coolbak.sh");
       print "\n备份文件结束。\n";
       print "\n";
       print "\n";  
       
       ##备份spfile文件
       print "开始备份系统参数文件\n";
       system("cp \$ORACLE_HOME\/dbs\/spfile\* \.\/");
       print "\n完成系统参数文件备份.\n";
       print "\n";
       print "\n";
       
       ##备份orapw文件
       print "开始备份口令文件\n";
       system("cp \$ORACLE_HOME\/dbs\/orapw\* \.\/");
       print "\n完成口令文件备份.\n";
       print "\n";
       print "\n";
             
       print '-' x 50, "\n";
       print "oracle冷备第三步：启动数据库\n";     
       ##启动数据库        
       print "\n开始启动数据库，请稍候......\n";
       print SQLPLUS "startup\n";
       system("sleep 30");
       &ckstatus;
       print "\n数据库已经启动\n";
       close(SQLPLUS) || die "Execute sql error!\n";
       
       ##格式话parameter文件内容
       system("sed 's\/    \/\/g' tmp.txt  \> tmp0.txt");
       system("sed 's\/\^\[ \\t\]\*\/\/\;s\/\[ \\t\]\*\$\/\/' tmp0.txt \> database.parameter");
       unlink("./tmp.txt");
       unlink("./tmp0.txt");
       print "\n";
       print "\n"; 
       
        
       ##节约空间，压缩备份文件
       print '-' x 50, "\n";
       print "oracle冷备第四步：压缩备份文件，节约空间.\n";   
       chdir "$path";
       print "\n开始进行文件压缩......\n";
       print "\n";
       system("tar cvf coolbackup.tar coolbackup");
       system("sleep 2");
       system("gzip coolbackup.tar");
       system("rm -rf coolbackup");
       system("mv coolbackup.tar.gz coolbackup\_$daytime.tar.gz");
       print "\n文件压缩结束.\n";
       print "\noracle冷备结束.\n";
       print '-' x 50, "\n";
      
  }
  
  ##数据库运行状态检测   
  sub ckstatus
  {
     #检测oracle数据库是否运行                                
       ###已连接到空闲例程。|Connected to an idle instance.       
       ###Connected to:  | 连接到:
                                                     
     open(SQLPLUS, "|sqlplus  / as sysdba > loginfo_ch.txt") || die "Execute sqlplus error!\n";
     close(SQLPLUS) || die "Execute sql error!\n";
     
     my $login_ck = `cat loginfo_ck.txt  \| head \-n 7 \| grep \-v SQL \| grep \-v Copyright \| sed \'\/\^\$\/d\'`;
     chomp($login_ck);
     if($login_ck=~ m/Connected to:/ || $login=~ m/连接到:/)
     {
       print "\t检测数据库当前状态.\n";
       print "\t数据库Open!\n";
       print "\t检测数据库状态结束.\n"; 
     }
     else
     {
       print "\t检测数据库当前状态.\n";
       print "\t数据库Closed.\n";
       print "\t检测数据库状态结束.\n";    
     }
     unlink("./loginfo_ck.txt");
  }
  
  ##剩余空间检测
  sub space
  {
     print "\n剩余空间信息检测\n";
     #判断使用空间路径
     #system("cd \$ORACLE_BASE");
     chdir "$ORACLE_BASE";
     my $orabase=`pwd`;
     chomp($orabase);
     my $mu = substr($orabase,1,3);
     
     #df | grep opt  | awk -F " " '{print $2,$3,$4,$5,$6}'
     my $max_tmp = `df \| grep $mu  \| awk \-F \" \" \'\{print \$2\}\'`;
     my $used_tmp = `df \| grep $mu  \| awk \-F \" \" \'\{print \$3\}\'`;
     my $available_tmp = `df \| grep $mu  \| awk \-F \" \" \'\{print \$4\}\'`;
     my $useper = `df \| grep $mu  | awk \-F \" \" \'\{print \$5\}\'`;
     my $mount = `df \| grep $mu  \| awk \-F \" \" \'\{print \$6}\'`;
     
     my $max= substr($max_tmp/1024/1024,0,8);
     my $used = substr($used_tmp/1024/1024,0,8);
     my $available =  substr($available_tmp/1024/1024,0,8);
     
     chomp($max);
     chomp($used);
     chomp($available);
     chomp($useper);
     chomp($mount);
     
     print "\n当前oracle所使用的空间信息如下：\n";
     print "\t挂载点    ：$mount\n";
     print "\t空间大小  ：$max G\n";
     print "\t已用空间  ：$used G\n";
     print "\t剩余空间  ：$available G\n";
     print "\t空间使用率：$useper\n";
     
     if($available < 2)
      {
         print "\n检测结果如下：\n";
         print "\n\t当前剩余空间小于2G，备份空间不足，备份退出\n";
         exit;
      }
     else
      {
         print "\n检测结果如下：\n";
         print "\n\t当前剩余空间大于2G，可以进行oracle冷份\n";
      }
  }

  sub logic
  {
    print "请输入用户名:\n";
    my $user=<STDIN>;
    chomp($user);
    
    print "请输入密码:\n";
    my $passwd = <STDIN>;
    chomp($passwd);
  
    my $sql="exp $user/$passwd file=myexport$daytime.dmp log=myexport$daytime.log";
    print "\n开始数据库逻辑备份.\n";
    system("$sql");
    print "\n结束数据库逻辑备份.\n";
    
  }
}
else
{
  print "\n当前非oracle用户登录，退出!\n";
  print "\n请使用oracle用户执行本脚本.\n"; 
  print "@foo\n"; 
}
```

## 冷备的恢复

冷备的恢复比较简单，比如数据库数据文件损坏，则关闭数据库后，将原先备份的所有文件再拷贝到相应目录下，重启数据库即可。

通常情况下，控制文件有3个，但无论什么时候，实际使用的只有一个控制文件，建议备份控制文件到不同路径下，当其中一个或者两个控制文件损坏后，可以使用第三个好的控制文件替换损坏的控制文件，并正确命名这些控制文件。

# RMAN概述

RMAN（oracle恢复管理器）是数据库的一种备份与恢复工具，具有多种能力完成备份与恢复工作。RMAN有两个版本：OEM的GUI版本和命令行版本。使用OEM的GUI版本，操作简单，但中间的执行过程无法向我们展示，只有一个最终的执行结果，本文不概述这个版本的使用。

RMAN是一种物理备份，可以用RMAN来备份数据文件、控制文件、参数文件、归档日志文件。我们在数据库出现问题的时候可以通过RMAN物理备份恢复到数据库的失效点。

## 准备工作

```shell
SQL> create tablespace RMAN_DATA datafile '/opt/oracle/oradata/mmsgdb/rman_data.dbf'
  2  size 200M
  3  autoextend off
  4  extent management local
  5  uniform;

表空间已创建。

SQL> create temporary tablespace RMAN_TMP tempfile '/opt/oracle/oradata/mmsgdb/rman_tmp.dbf'
  2  size 20M
  3  autoextend off
  4  extent management local
  5  uniform;

表空间已创建。

SQL> create user rman identified by rman
  2  default tablespace RMAN_DATA
  3  temporary tablespace RMAN_TMP;

用户已创建。

SQL> grant connect ,resource,recovery_catalog_owner to rman;

授权成功。

SQL>exit
```

## 启动和连接到RMAN

关于启动RMAN有几个重要说明，如指定目标数据库和规定一个恢复目录等。下面了解三种使用RMAN工具的数据库连接类型。

|数据库连接| 说明|
|-------------------------|-------------------------------------------------|
|目标数据库 |目标数据库是将备份和恢复定为目标的数据库。为了完成任务，要求SYSDAB权限 |
|恢复目录数据库 |恢复目录数据库是个可选数据库，它存储有关备份、恢复的信息和重建数据 |
|辅助数据库 |辅助数据库是备用数据库、复制数据库或辅助实例（备用或TSPITR）|

有两种连接到目标数据库的方法：

* 1、从命令行；
* 2、使用RMAN工具

### 使用命令行

在命令行中指定目标和默认连接，nocatalog是可选的，如果留下空白，则为默认使用nocatalog。

```shell
oracle@mmsg:~> rman target / nocatalog

恢复管理器: Release 11.1.0.7.0 - Production on 星期五 11月 12 12:31:04 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

连接到目标数据库: INOMC (DBID=1037536304)
使用目标数据库控制文件替代恢复目录

RMAN>
```

### 使用RMAN工具

```shell
oracle@mmsg:~> rman

恢复管理器: Release 11.1.0.7.0 - Production on 星期五 11月 12 12:33:11 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

RMAN> connect target 

连接到目标数据库: INOMC (DBID=1037536304)

RMAN>
```

连接到恢复目录相当简单，以下是使用恢复目录的RMAN

#### 命令行

```shell
oracle@mmsg:~> rman target / catalog rman/rman@inomc

恢复管理器: Release 11.1.0.7.0 - Production on 星期五 11月 12 12:34:44 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

连接到目标数据库: INOMC (DBID=1037536304)
连接到恢复目录数据库

RMAN>
```

#### RMAN工具

```shell
oracle@mmsg:~> rman

恢复管理器: Release 11.1.0.7.0 - Production on 星期五 11月 12 12:35:58 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

RMAN> connect target/

连接到目标数据库: INOMC (DBID=1037536304)

RMAN> connect catalog rman/rman@inomc

连接到恢复目录数据库

RMAN>
```

## 通道分配

通道分配是连接RMAN和目标数据库的方法，也是确定I/O设备类型的方法，服务器进程将使用该I/O设备完成备份和重建操作。I/O设备可以是磁盘，也可以是磁带，通道分配可以自动分配也可以手工分配。

### 手工分配通道

只要发布allocate channel，即可执行手工分配通道。

手工分配通道的命令是

```shell
allocate channel channel_name type disk/sbt
allocate channel c1 type disk
```
它用于写入磁盘文件系统，这里的磁盘包括：硬盘、光盘、软盘、U盘等。

```allocate channel c2 type sbt ```
它用于写入磁带。

### 自动分配通道

自动分配通道可以通过在RMAN命令提示符下设置RMAN配置来完成。使用命令configure default device type to configure device完成该任务。当执行backup、restora或者delete命令时，自动使用自动通道分配。

自动通道分配的完整清单如下：

```shell
config device type disk backup|clear|parallelism n;
config default device type to|clear;
config channel device type disk|equal;
config channel n device type disk|equal;
```

下面的示例显示默认设备类型被设置为磁盘，并行数被设置为1，这意味着：如果没有手工分配通道，参数将如下：

```shell
RMAN> show all;
db_unique_name 为 INOMC 的数据库的 RMAN 配置参数为:
CONFIGURE RETENTION POLICY TO REDUNDANCY 1; # default
CONFIGURE BACKUP OPTIMIZATION OFF; # default
CONFIGURE DEFAULT DEVICE TYPE TO DISK; # default
CONFIGURE CONTROLFILE AUTOBACKUP OFF; # default
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '%F'; # default
CONFIGURE DEVICE TYPE DISK PARALLELISM 1 BACKUP TYPE TO BACKUPSET; # default
CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE ARCHIVELOG BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE MAXSETSIZE TO UNLIMITED; # default
CONFIGURE ENCRYPTION FOR DATABASE OFF; # default
CONFIGURE ENCRYPTION ALGORITHM 'AES128'; # default
CONFIGURE COMPRESSION ALGORITHM 'BZIP2'; # default
CONFIGURE ARCHIVELOG DELETION POLICY TO NONE; # default
CONFIGURE SNAPSHOT CONTROLFILE NAME TO '/opt/oracle/product/11g/dbs/snapcf_inomc.f'; # default
```

## RMAN的参数和永久设置

为RMAN设置永久设置参数是通过对每个目标数据库的配置而实现的。

有一些长用的有助于使用RMAN的配置参数设置，在日常操作中，这些设置很有用：

```shell
device type
backup type
compressed backupset
channel disk device
channel tapy device
```

下面详细介绍如何修改或设定每个配置的设置值。

将默认设备设置为磁带，然后是磁盘，使用如下命令：

```shell
RMAN> configure default device type to sbt;

旧的 RMAN 配置参数:
CONFIGURE DEFAULT DEVICE TYPE TO 'SBT_TAPE';
新的 RMAN 配置参数:
CONFIGURE DEFAULT DEVICE TYPE TO 'SBT_TAPE';
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN> configure default device type to disk;

旧的 RMAN 配置参数:
CONFIGURE DEFAULT DEVICE TYPE TO 'SBT_TAPE';
新的 RMAN 配置参数:
CONFIGURE DEFAULT DEVICE TYPE TO DISK;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN>
```

先为图像副本设定默认备份类型，然后为备份集设定默认备份类型，使用如下命令：

该参数和设置值设定备份的类型是图像副本还是备份集。

```shell
RMAN> configure device type disk backup type to copy;

新的 RMAN 配置参数:
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO COPY PARALLELISM 1;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN> configure device type disk backup type to backupset;

旧的 RMAN 配置参数:
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO COPY PARALLELISM 1;
新的 RMAN 配置参数:
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO BACKUPSET PARALLELISM 1;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN>

给解压备份集配置默认设备为磁盘或者磁带，有两个特别的命令：
RMAN> configure device type disk backup type to compressed backupset;

旧的 RMAN 配置参数:
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO BACKUPSET PARALLELISM 1;
新的 RMAN 配置参数:
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO COMPRESSED BACKUPSET PARALLELISM 1;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN> configure device type sbt backup type to compressed backupset;

新的 RMAN 配置参数:
CONFIGURE DEVICE TYPE 'SBT_TAPE' BACKUP TYPE TO COMPRESSED BACKUPSET PARALLELISM 1;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN>
```

## 保留策略

保留策略是为了用于可能的恢复，是备份被保留的时间长度。保留策略由参数RETENTION POLICY确定，使用show all命令可以显示此参数。

```shell
RMAN> show all;

db_unique_name 为 INOMC 的数据库的 RMAN 配置参数为:
CONFIGURE RETENTION POLICY TO REDUNDANCY 1; # default
CONFIGURE BACKUP OPTIMIZATION OFF; # default
CONFIGURE DEFAULT DEVICE TYPE TO DISK;
CONFIGURE CONTROLFILE AUTOBACKUP OFF; # default
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '%F'; # default
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE SBT_TAPE TO '%F'; # default
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO COMPRESSED BACKUPSET PARALLELISM 1;
CONFIGURE DEVICE TYPE 'SBT_TAPE' BACKUP TYPE TO COMPRESSED BACKUPSET PARALLELISM 1;
CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE SBT_TAPE TO 1; # default
CONFIGURE ARCHIVELOG BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE ARCHIVELOG BACKUP COPIES FOR DEVICE TYPE SBT_TAPE TO 1; # default
CONFIGURE MAXSETSIZE TO UNLIMITED; # default
CONFIGURE ENCRYPTION FOR DATABASE OFF; # default
CONFIGURE ENCRYPTION ALGORITHM 'AES128'; # default
CONFIGURE COMPRESSION ALGORITHM 'BZIP2'; # default
CONFIGURE ARCHIVELOG DELETION POLICY TO NONE; # default
CONFIGURE SNAPSHOT CONTROLFILE NAME TO '/opt/oracle/product/11g/dbs/snapcf_inomc.f'; # default

RMAN>
```

RMAN中提供了两种保留策略，分别是：基于时间和基于冗余数量。

### 基于时间的备份保留策略

说的简单些，就是你希望数据库最早能恢复到几天前。比如将恢复时间段设置为7，那么RMAN所保留的备份即是可以保证你将数据库恢复到一周内任何时刻下那些文件。 

设置基于时间的备份保留策略可以通过CONFIGURE命令，例如： 

```shell
configure retention policy to recovery window of n days;
RMAN> configure retention policy to recovery window of 2 days;

旧的 RMAN 配置参数:
CONFIGURE RETENTION POLICY TO REDUNDANCY 1;
新的 RMAN 配置参数:
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 2 DAYS;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN>
```

注：
* n=大于0的正整数 

执行该命令后，RMAN将始终保留那些将数据库恢复到n天前的状态时需要用到的备份，比如，恢复时间段被设置为7天，那么各个数据文件的备份必须满足如下条件： 

```shell
SYSDATE-(SELECT CHECKPOINT_TIME FROM V$DATAFILE)>=7 
任何不满足上述条件的备份都将被RMAN废弃并可通过
DELETE OBSOLETE命令删除。 
基于冗余数量的备份保留策略
基于冗余数量实质即某个数据文件以各种形式（包括备份集和镜像复制）存在的备份的数量。如果某个数据文件的冗余备份数量超出了指定数量，RMAN将废弃最旧的备份。 
同样，基于数量的备份保留策略也是通过CONFIGURE命令设置，例如： 
RMAN>  CONFIGURE RETENTION POLICY TO  REDUNDANCY n ; 
```

同上：n=大于0的正整数 

你也可以通过下列命令设置成不采用任何备份保留策略:

```shell
RMAN>  CONFIGURE RETENTION POLICY TO NONE; 
RMAN的show、report、list、crosscheck、delete命令
show
RMAN> show all;

db_unique_name 为 INOMC 的数据库的 RMAN 配置参数为:
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 2 DAYS;
CONFIGURE BACKUP OPTIMIZATION OFF; # default
CONFIGURE DEFAULT DEVICE TYPE TO DISK;
CONFIGURE CONTROLFILE AUTOBACKUP OFF; # default
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '%F'; # default
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE SBT_TAPE TO '%F'; # default
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO COMPRESSED BACKUPSET PARALLELISM 1;
CONFIGURE DEVICE TYPE 'SBT_TAPE' BACKUP TYPE TO COMPRESSED BACKUPSET PARALLELISM 1;
CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE SBT_TAPE TO 1; # default
CONFIGURE ARCHIVELOG BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
CONFIGURE ARCHIVELOG BACKUP COPIES FOR DEVICE TYPE SBT_TAPE TO 1; # default
CONFIGURE MAXSETSIZE TO UNLIMITED; # default
CONFIGURE ENCRYPTION FOR DATABASE OFF; # default
CONFIGURE ENCRYPTION ALGORITHM 'AES128'; # default
CONFIGURE COMPRESSION ALGORITHM 'BZIP2'; # default
CONFIGURE ARCHIVELOG DELETION POLICY TO NONE; # default
CONFIGURE SNAPSHOT CONTROLFILE NAME TO '/opt/oracle/product/11g/dbs/snapcf_inomc.f'; # default

RMAN>
```

### report

#### 报告目标数据库的物理结构

```shell
RMAN> report schema;

db_unique_name 为 INOMC 的数据库的数据库方案报表

永久数据文件列表
===========================
文件大小 (MB) 表空间           回退段数据文件名称
---- -------- -------------------- ------- ------------------------
1    800      SYSTEM               YES     /opt/oracle/oradata/mmsgdb/system01.dbf
2    500      SYSAUX               NO      /opt/oracle/oradata/mmsgdb/sysaux01.dbf
3    800      UNDOTBS1             YES     /opt/oracle/oradata/mmsgdb/undotbs01.dbf
4    20       USERS                NO      /opt/oracle/oradata/mmsgdb/users01.dbf
5    800      IMAP_DB              NO      /opt/oracle/data/imap_db.dbf
6    1200     IMAPLOGDB            NO      /opt/oracle/data/imaplogdb.dbf
7    600      IMAPSMDB             NO      /opt/oracle/data/imapsmdb.dbf
8    800      IMAPTMDB             NO      /opt/oracle/data/imaptmdb.dbf
9    1000     ALARMDB              NO      /opt/oracle/data/alarmdb.dbf
10   2500     PERFDB               NO      /opt/oracle/data/perfdb.dbf
11   400      NMSGUEST             NO      /opt/oracle/data/nmsguest.dbf
12   1600     PERFDB_IDX           NO      /opt/oracle/data/perfdb_idx.dbf
13   71       MMSG                 NO      /opt/oracle/oradata/mmsgdb/mmsg.dbf
14   200      RMAN_DATA            NO      /opt/oracle/oradata/mmsgdb/rman_data.dbf
15   400      WYZ                  NO      /home/wyz/wyzoradata/wyz.dbf
16   1000     YJH                  NO      /home/yjh/oradata/yjhdata01
17   10       TEST                 NO      /opt/oracle/oradata/mmsgdb/test.dbf

临时文件列表
=======================
文件大小 (MB) 表空间           最大大小 (MB) 临时文件名称
---- -------- -------------------- ----------- --------------------
1    100      TEMP                 32767       /opt/oracle/oradata/mmsgdb/temp01.dbf
2    15       MMSG_TMP             15          /opt/oracle/oradata/mmsgdb/mmsg_tmp.dbf
3    20       RMAN_TMP             20          /opt/oracle/oradata/mmsgdb/rman_tmp.dbf
4    100      WYZ_TMP              200         /home/wyz/wyzoradata/wyz_tmp.dbf
5    500      YJH_TMP              500         /home/yjh/oradata/yjhdata02
6    2        TEST_TMP             2           /opt/oracle/oradata/mmsgdb/test_tmp.dbf

RMAN>
```

#### 报告最近N天尚未备份的数据文件

```shell
RMAN> report need backup days=3;

文件报表的恢复需要超过 3 天的归档日志
文件天数据 名称
---- ----- -----------------------------------------------------
1    101   /opt/oracle/oradata/mmsgdb/system01.dbf
2    101   /opt/oracle/oradata/mmsgdb/sysaux01.dbf
3    101   /opt/oracle/oradata/mmsgdb/undotbs01.dbf
4    101   /opt/oracle/oradata/mmsgdb/users01.dbf
5    52    /opt/oracle/data/imap_db.dbf
6    52    /opt/oracle/data/imaplogdb.dbf
7    52    /opt/oracle/data/imapsmdb.dbf
8    52    /opt/oracle/data/imaptmdb.dbf
9    52    /opt/oracle/data/alarmdb.dbf
10   52    /opt/oracle/data/perfdb.dbf
11   52    /opt/oracle/data/nmsguest.dbf
12   52    /opt/oracle/data/perfdb_idx.dbf
13   30    /opt/oracle/oradata/mmsgdb/mmsg.dbf
14   25    /opt/oracle/oradata/mmsgdb/rman_data.dbf
15   24    /home/wyz/wyzoradata/wyz.dbf
16   23    /home/yjh/oradata/yjhdata01

RMAN>
```

#### 报告表空间上最近N天未备份的数据文件

```shell
RMAN> report need backup days=3 tablespace MMSG;

文件报表的恢复需要超过 3 天的归档日志
文件天数据 名称
---- ----- -----------------------------------------------------
13   30    /opt/oracle/oradata/mmsgdb/mmsg.dbf

RMAN>
```

#### 报告恢复数据文件需要的增量备份个数超过3次的数据文件

```shell
RMAN> report need backup incremental 3; 

恢复时需要超过3增量的文件报表
文件增量名称
---- ------------ ----------------------------------------------

RMAN>
```

#### 报告备份文件低于2份的所有数据文件

```shell
RMAN> report need backup redundancy 2 database; 

文件冗余备份少于2个
文件 #bkps 名称
---- ----- -----------------------------------------------------
1    0     /opt/oracle/oradata/mmsgdb/system01.dbf
2    0     /opt/oracle/oradata/mmsgdb/sysaux01.dbf
3    0     /opt/oracle/oradata/mmsgdb/undotbs01.dbf
4    0     /opt/oracle/oradata/mmsgdb/users01.dbf
5    0     /opt/oracle/data/imap_db.dbf
6    0     /opt/oracle/data/imaplogdb.dbf
7    0     /opt/oracle/data/imapsmdb.dbf
8    0     /opt/oracle/data/imaptmdb.dbf
9    0     /opt/oracle/data/alarmdb.dbf
10   0     /opt/oracle/data/perfdb.dbf
11   0     /opt/oracle/data/nmsguest.dbf
12   0     /opt/oracle/data/perfdb_idx.dbf
13   0     /opt/oracle/oradata/mmsgdb/mmsg.dbf
14   0     /opt/oracle/oradata/mmsgdb/rman_data.dbf
15   0     /home/wyz/wyzoradata/wyz.dbf
16   0     /home/yjh/oradata/yjhdata01
17   1     /opt/oracle/oradata/mmsgdb/test.dbf

RMAN>
```

#### 报告文件报表的恢复需要超过6天的归档日志的数据文件

```shell
RMAN> report need backup recovery window of 6 days; 

必须备份以满足 6 天恢复窗口所需的文件报表
文件天数据 名称
---- ----- -----------------------------------------------------
1    101   /opt/oracle/oradata/mmsgdb/system01.dbf
2    101   /opt/oracle/oradata/mmsgdb/sysaux01.dbf
3    101   /opt/oracle/oradata/mmsgdb/undotbs01.dbf
4    101   /opt/oracle/oradata/mmsgdb/users01.dbf
5    52    /opt/oracle/data/imap_db.dbf
6    52    /opt/oracle/data/imaplogdb.dbf
7    52    /opt/oracle/data/imapsmdb.dbf
8    52    /opt/oracle/data/imaptmdb.dbf
9    52    /opt/oracle/data/alarmdb.dbf
10   52    /opt/oracle/data/perfdb.dbf
11   52    /opt/oracle/data/nmsguest.dbf
12   52    /opt/oracle/data/perfdb_idx.dbf
13   30    /opt/oracle/oradata/mmsgdb/mmsg.dbf
14   25    /opt/oracle/oradata/mmsgdb/rman_data.dbf
15   24    /home/wyz/wyzoradata/wyz.dbf
16   23    /home/yjh/oradata/yjhdata01

RMAN>
```

#### 报告数据库所有不可恢复的数据文件

```shell
RMAN> report unrecoverable; 

由于操作无法被恢复, 文件的报表需要备份
备份请求名称的文件类型
---- ----------------------- -----------------------------------

RMAN>
```

#### 报告备份次数超过2次的陈旧备份

```shell
RMAN> report obsolete redundancy 2;

未找到已废弃的备份

RMAN>
```

#### 报告多余的备份

```shell
RMAN> report obsolete;

RMAN 保留策略将应用于该命令
将 RMAN 保留策略设置为 2 天的恢复窗口
未找到已废弃的备份

RMAN>
```

### list

```shell
list backup;                        列出详细备份
list expired backup;                列出过期备份
list backup of database;            列出所有数据文件的备份集
list backup of tablespace MMSG;    列出特定表空间的所有数据文件备份集
list backup of controlfile;            列出控制文件备份集
list backup of archivelog all;        列出归档日志备份集详细信息
list archivelog all;　　　　　　       列出归档日志备份集简要信息
list backup of spfile;                 列出SPFILE备份集
list copy of datafile 5;               列出数据文件映像副本
list copy of controlfile;              列出控制文件映像副本
list copy of archivelog all;           列出归档日志映像副本
list incarnation of database;         列出对应物/列出数据库副本
list backup summary;                概述可用的备份
     　　　　　　　　　　　                B表示backup
     　　　　　　　　　　　                F表示FULL
     　　　　　　　　　　　                A表示archive log
     　　　　　　　　　　　                S说明备份状态（A　AVAILABLE　　　X EXPIRED )
     
list backup by file;    按备份类型列出备份
                       按照数据文件备份，归档日志备份，控制文件备份，服务器参数文件备份　列出
```

### check

```shell
RMAN> crosscheck backup;                            核对所有备份集  
RMAN> crosscheck backup of database;                  核对所有数据文件的备份集  
RMAN> crosscheck backup of tablespace MMSG;         核对特定表空间的备份集  
RMAN> crosscheck backup of datafile 4;                 核对特定数据文件的备份集  
RMAN> crosscheck backup of controlfile;                 核对控制文件的备份集  
RMAN> crosscheck backup of spfile;                     核对SPFILE的备份集   
RMAN> crosscheck backup of archivelog sequence 3;   核对归档日志的备份集 
RMAN> crosscheck copy;                                核对所有映像副本
RMAN> crosscheck copy of database;                    核对所有数据文件的映像副本 
RMAN> crosscheck copy of tablespace MMSG;           核对特定表空间的映像副本  
RMAN> crosscheck copy of datafile 6;                   核对特定数据文件的映像副本  
RMAN> crosscheck copy of archivelog sequence 4;      核对归档日志的映像副本   
RMAN> crosscheck copy of controlfile;                  核对控制文件的映像副本
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

```shell
RMAN> delete obsolete;                 删除陈旧备份；
RMAN> delete expired backup;           删除EXPIRED备份   
RMAN> delete expired copy;             删除EXPIRED副本
RMAN> delete backupset 19;             删除特定备份集
RMAN> delete backuppiece '/opt/oracle/oradata/backup/test.ora';   删除特定备份片
RMAN> delete backup;                   删除所有备份集
RMAN> delete datafilecopy '/opt/oracle/oradata/backup/test.bak';  删除特定映像副本
RMAN> delete copy;                      删除所有映像副本
RMAN> delete archivelog all delete input;
RMAN> delete backupset 22 format = '/opt/oracle/oradata/backup/%u.bak' delete input;
                                          在备份后删除输入对象             
RMAN> delete backupset id;              删除备份集
```

# 操作示例

## 列出数据库中所以文件的备份的信息

```shell
RMAN> list backup of database;


备份集列表
===================


BS 关键字  类型 LV 大小       设备类型 经过时间 完成时间  
------- ---- -- ---------- ----------- ------------ ----------
812     Full    2.44M      DISK        00:00:01     18-11月-10
        BP 关键字: 813   状态: AVAILABLE  已压缩: YES  标记: TAG20101118T115451
段名:/opt/oracle/product/11g/dbs/0rltadgb_1_1
  备份集 812 中的数据文件列表
  文件 LV 类型 Ckp SCN    Ckp 时间   名称
  ---- -- ---- ---------- ---------- ----
  13      Full 3978913    18-11月-10 /opt/oracle/oradata/mmsgdb/mmsg.dbf

BS 关键字  类型 LV 大小       设备类型 经过时间 完成时间  
------- ---- -- ---------- ----------- ------------ ----------
863     Full    1.02M      DISK        00:00:00     18-11月-10
        BP 关键字: 864   状态: AVAILABLE  已压缩: YES  标记: TAG20101118T143745
段名:/opt/oracle/product/11g/dbs/0tltan1p_1_1
  备份集 863 中的数据文件列表
  文件 LV 类型 Ckp SCN    Ckp 时间   名称
  ---- -- ---- ---------- ---------- ----
  17      Full 3983755    18-11月-10 /opt/oracle/oradata/mmsgdb/test.dbf

RMAN>
```

## 列出指定表空间备份信息

```shell
RMAN> list backup of tablespace 'MMSG';


备份集列表
===================


BS 关键字  类型 LV 大小       设备类型 经过时间 完成时间  
------- ---- -- ---------- ----------- ------------ ----------
812     Full    2.44M      DISK        00:00:01     18-11月-10
        BP 关键字: 813   状态: AVAILABLE  已压缩: YES  标记: TAG20101118T115451
段名:/opt/oracle/product/11g/dbs/0rltadgb_1_1
  备份集 812 中的数据文件列表
  文件 LV 类型 Ckp SCN    Ckp 时间   名称
  ---- -- ---- ---------- ---------- ----
  13      Full 3978913    18-11月-10 /opt/oracle/oradata/mmsgdb/mmsg.dbf
```

## 列出指定的数据文件备份信息

```shell
RMAN> list backup of datafile '/opt/oracle/oradata/mmsgdb/test.dbf';


备份集列表
===================


BS 关键字  类型 LV 大小       设备类型 经过时间 完成时间  
------- ---- -- ---------- ----------- ------------ ----------
863     Full    1.02M      DISK        00:00:00     18-11月-10
        BP 关键字: 864   状态: AVAILABLE  已压缩: YES  标记: TAG20101118T143745
段名:/opt/oracle/product/11g/dbs/0tltan1p_1_1
  备份集 863 中的数据文件列表
  文件 LV 类型 Ckp SCN    Ckp 时间   名称
  ---- -- ---- ---------- ---------- ----
  17      Full 3983755    18-11月-10 /opt/oracle/oradata/mmsgdb/test.dbf

RMAN>
```

## 删除整个数据库的备份

```shell
RMAN> delete backup;

分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=1066 设备类型=DISK

备份片段列表
BP 关键字  BS 关键字  Pc# Cp# 状态      设备类型段名称
------- ------- --- --- ----------- ----------- ----------
472     461     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873889_s16_p1
473     462     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873904_s17_p1
474     463     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873908_s18_p1
475     464     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873911_s19_p1
476     465     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873918_s20_p1
477     466     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873919_s21_p1
478     467     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873920_s22_p1
479     468     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873921_s23_p1
480     469     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873937_s24_p1
481     470     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873940_s25_p1
482     471     1   1   AVAILABLE   DISK        /opt/oracle/mmsg.load/db_t734873941_s26_p1

是否确定要删除以上对象 (输入 YES 或 NO)? yes
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873889_s16_p1 RECID=16 STAMP=734873889
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873904_s17_p1 RECID=17 STAMP=734873905
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873908_s18_p1 RECID=18 STAMP=734873908
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873911_s19_p1 RECID=19 STAMP=734873911
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873918_s20_p1 RECID=20 STAMP=734873918
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873919_s21_p1 RECID=21 STAMP=734873919
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873920_s22_p1 RECID=22 STAMP=734873920
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873921_s23_p1 RECID=23 STAMP=734873922
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873937_s24_p1 RECID=24 STAMP=734873937
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873940_s25_p1 RECID=25 STAMP=734873940
已删除备份片段
备份片段句柄=/opt/oracle/mmsg.load/db_t734873941_s26_p1 RECID=26 STAMP=734873942
11 对象已删除


RMAN>
```

## 删除表空间的备份

```shell
RMAN> delete backup of tablespace 'MMSG';

使用通道 ORA_DISK_1

备份片段列表
BP 关键字  BS 关键字  Pc# Cp# 状态      设备类型段名称
------- ------- --- --- ----------- ----------- ----------
813     812     1   1   AVAILABLE   DISK        /opt/oracle/product/11g/dbs/0rltadgb_1_1

是否确定要删除以上对象 (输入 YES 或 NO)? y
已删除备份片段
备份片段句柄=/opt/oracle/product/11g/dbs/0rltadgb_1_1 RECID=27 STAMP=735393291
1 对象已删除


RMAN>
```

## 删除指定的数据文件备份

```shell
RMAN> delete backup of datafile '/opt/oracle/oradata/mmsgdb/test.dbf';

使用通道 ORA_DISK_1

备份片段列表
BP 关键字  BS 关键字  Pc# Cp# 状态      设备类型段名称
------- ------- --- --- ----------- ----------- ----------
839     837     1   1   AVAILABLE   DISK        /opt/oracle/product/11g/dbs/0sltam4j_1_1

是否确定要删除以上对象 (输入 YES 或 NO)? y
已删除备份片段
备份片段句柄=/opt/oracle/product/11g/dbs/0sltam4j_1_1 RECID=28 STAMP=735402132
1 对象已删除


RMAN>
```

## 删除陈旧备份

```shell
RMAN> delete obsolete ; 

RMAN 保留策略将应用于该命令
将 RMAN 保留策略设置为 2 天的恢复窗口
使用通道 ORA_DISK_1
未找到已废弃的备份

RMAN>
```

注：
* 当使用RMAN执行备份操作时，RMAN会根据备份冗余策略确定陈旧备份。

# RMAN备份形式


RMAN备份有两种形式：

* 1、镜像备份（image copies）
* 2、备份集备份（backup sets）

## 镜像备份

镜像备份实际就是RMAN利用目标数据库服务进程来完成文件的copy操作，是数据文件、控制文件或者归档日志文件的副本。

RMAN镜像备份的副本无法通过list backup显示，可以通过list copy显示。


## 备份集备份

备份集是通过RMAN创建的逻辑备份对象，一个备份集中可以包括多个控制文件、数据文件、归档文件。

备份集在物理上由多个备份片段组成，每个备份片段就是一个操作系统文件。

# RMAN备份类型 

利用RMAN进行备份时，可以通过三种方式来对RMAN的备份做分类:

## 完全备份(Full Backup)与增量备份(Incremental Backup) 

全备与增备是针对数据文件而言，控制文件和归档日志文件不能进行增量备份。当然，后两者可以做备份优化。 

## 打开备份(Open Backup)或关闭备份(Closed Backup) 

数据库打开状态下进行备份即是打开备份，数据库关闭状态下(加载状态)进行的备份即关闭备份。

## 一致备份(Consistent Backup)与不一致备份(Inconsistent Backup) 

数据库打开状态或不干净关闭状态(shutdown abort)进行的备份是不一致备份，利用不一致的备份修复数据库后还需要做数据库的恢复。在数据库干净关闭状态进行的备份是一致备份，利用一致备份修复数据库后不需要做数据库的恢复。 


# RMAN备份

## 备份整个数据库

```shell
oracle@mmsg:~> rman target/

恢复管理器: Release 11.1.0.7.0 - Production on 星期日 10月 24 15:37:56 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

连接到目标数据库: INOMC (DBID=1037536304)

RMAN> connect catalog rman/rman@inomc

连接到恢复目录数据库


RMAN> register database;

注册在恢复目录中的数据库
正在启动全部恢复目录的 resync
完成全部 resync

RMAN>
RMAN> run { 
2>  allocate channel c1 type disk; 
3>  backup 
4>  full 
5>  tag full_db_backup 
6>  format "/opt/oracle/mmsg.load/db_t%t_s%s_p%p" 
7>  (database); 
8>  release channel c1; 
9>  }

释放的通道: ORA_DISK_1
分配的通道: c1
通道 c1: SID=1066 设备类型=DISK

启动 backup 于 12-11月-10
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00010 名称=/opt/oracle/data/perfdb.dbf
输入数据文件: 文件号=00016 名称=/home/yjh/oradata/yjhdata01
输入数据文件: 文件号=00015 名称=/home/wyz/wyzoradata/wyz.dbf
输入数据文件: 文件号=00012 名称=/opt/oracle/data/perfdb_idx.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873889_s16_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:15
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00006 名称=/opt/oracle/data/imaplogdb.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873904_s17_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:03
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00009 名称=/opt/oracle/data/alarmdb.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873908_s18_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:03
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00001 名称=/opt/oracle/oradata/mmsgdb/system01.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873911_s19_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:07
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00003 名称=/opt/oracle/oradata/mmsgdb/undotbs01.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873918_s20_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:01
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00005 名称=/opt/oracle/data/imap_db.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873919_s21_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:01
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00008 名称=/opt/oracle/data/imaptmdb.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873920_s22_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:01
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00002 名称=/opt/oracle/oradata/mmsgdb/sysaux01.dbf
输入数据文件: 文件号=00014 名称=/opt/oracle/oradata/mmsgdb/rman_data.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873921_s23_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:15
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00007 名称=/opt/oracle/data/imapsmdb.dbf
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
输入数据文件: 文件号=00004 名称=/opt/oracle/oradata/mmsgdb/users01.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873937_s24_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:03
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00011 名称=/opt/oracle/data/nmsguest.dbf
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873940_s25_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:01
通道 c1: 正在启动全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
备份集内包括当前控制文件
备份集内包括当前的 SPFILE
通道 c1: 正在启动段 1 于 12-11月-10
通道 c1: 已完成段 1 于 12-11月-10
段句柄=/opt/oracle/mmsg.load/db_t734873941_s26_p1 标记=FULL_DB_BACKUP 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 12-11月-10

释放的通道: c1
```

## 备份指定的数据文件

```shell
RMAN> backup datafile '/opt/oracle/oradata/mmsgdb/test.dbf';

启动 backup 于 18-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00017 名称=/opt/oracle/oradata/mmsgdb/test.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/0tltan1p_1_1 标记=TAG20101118T143745 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10

RMAN>
```

## 备份表空间

```shell
RMAN> backup tablespace MMSG;

启动 backup 于 18-11月-10
分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=1065 设备类型=DISK
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/0rltadgb_1_1 标记=TAG20101118T115451 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10

RMAN>
```

## 备份控制文件

1、最简单的方式就是通过configure命令修改CONTROLFILE AUTOBACKUP为on

```shell
RMAN> configure controlfile autobackup on;

新的 RMAN 配置参数:
CONFIGURE CONTROLFILE AUTOBACKUP ON;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN>
```

2、在自动备份打开的情况下，对数据库的任何备份，都会自动备份控制文件。

3、手工执行备份命令

```shell
RMAN> backup current controlfile;

启动 backup 于 18-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
备份集内包括当前控制文件
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/0ultau5s_1_1 标记=TAG20101118T163923 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10

RMAN>
```

4、执行backup操作时，指定include current controlfile参数

```shell
RMAN> backup database include current controlfile;

启动 backup 于 18-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00010 名称=/opt/oracle/data/perfdb.dbf
输入数据文件: 文件号=00016 名称=/home/yjh/oradata/yjhdata01
输入数据文件: 文件号=00015 名称=/home/wyz/wyzoradata/wyz.dbf
输入数据文件: 文件号=00012 名称=/opt/oracle/data/perfdb_idx.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/0vltaue2_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:07
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00006 名称=/opt/oracle/data/imaplogdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/10ltauea_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00009 名称=/opt/oracle/data/alarmdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/11ltaueb_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00001 名称=/opt/oracle/oradata/mmsgdb/system01.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/12ltauec_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00003 名称=/opt/oracle/oradata/mmsgdb/undotbs01.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/13ltauer_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00005 名称=/opt/oracle/data/imap_db.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/14ltaues_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00008 名称=/opt/oracle/data/imaptmdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/15ltauet_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00007 名称=/opt/oracle/data/imapsmdb.dbf
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
输入数据文件: 文件号=00004 名称=/opt/oracle/oradata/mmsgdb/users01.dbf
输入数据文件: 文件号=00017 名称=/opt/oracle/oradata/mmsgdb/test.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/16ltauev_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:03
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00002 名称=/opt/oracle/oradata/mmsgdb/sysaux01.dbf
输入数据文件: 文件号=00014 名称=/opt/oracle/oradata/mmsgdb/rman_data.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/17ltauf2_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00011 名称=/opt/oracle/data/nmsguest.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/18ltaufh_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
备份集内包括当前控制文件
备份集内包括当前的 SPFILE
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/19ltaufi_1_1 标记=TAG20101118T164346 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10


RMAN> backup datafile  '/opt/oracle/oradata/mmsgdb/test.dbf' include current controlfile;

启动 backup 于 18-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00017 名称=/opt/oracle/oradata/mmsgdb/test.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1altauil_1_1 标记=TAG20101118T164613 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
备份集内包括当前控制文件
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1bltauim_1_1 标记=TAG20101118T164613 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10

RMAN>

RMAN> backup tablespace MMSG include current controlfile;

启动 backup 于 18-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1cltaujq_1_1 标记=TAG20101118T164650 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
备份集内包括当前控制文件
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1dltaujs_1_1 标记=TAG20101118T164650 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10

RMAN>
```

## 备份归档日志文件

归档日志备份对于数据库的介质恢复非常重要，归档日志文件被破坏虽然不像控制文件被破坏后数据库崩溃那么严重，但归档日志文件的备份还是非常重要的。备份了归档日志文件后，可以将数据库恢复到备份之前的任何一个时刻。

备份归档日志文件方法有两种：

### 利用BACKUP ARCHIVELOG命令备份

```shell
RMAN> backup archivelog all;

启动 backup 于 18-11月-10
当前日志已存档
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的归档日志备份集
通道 ORA_DISK_1: 正在指定备份集内的归档日志
输入归档日志线程=1 序列=48 RECID=28 STAMP=735350892
输入归档日志线程=1 序列=49 RECID=29 STAMP=735411706
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1eltavfr_1_1 标记=TAG20101118T170147 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
完成 backup 于 18-11月-10

RMAN>
```

### 在backup过程中，使用plus archivelog参数

```shell
RMAN> backup database plus archivelog;


启动 backup 于 18-11月-10
当前日志已存档
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的归档日志备份集
通道 ORA_DISK_1: 正在指定备份集内的归档日志
输入归档日志线程=1 序列=48 RECID=28 STAMP=735350892
输入归档日志线程=1 序列=49 RECID=29 STAMP=735411706
输入归档日志线程=1 序列=50 RECID=30 STAMP=735411902
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1fltavlv_1_1 标记=TAG20101118T170503 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
完成 backup 于 18-11月-10

启动 backup 于 18-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00010 名称=/opt/oracle/data/perfdb.dbf
输入数据文件: 文件号=00016 名称=/home/yjh/oradata/yjhdata01
输入数据文件: 文件号=00015 名称=/home/wyz/wyzoradata/wyz.dbf
输入数据文件: 文件号=00012 名称=/opt/oracle/data/perfdb_idx.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1gltavme_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:07
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00006 名称=/opt/oracle/data/imaplogdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1hltavml_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00009 名称=/opt/oracle/data/alarmdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1iltavmm_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00001 名称=/opt/oracle/oradata/mmsgdb/system01.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1jltavmo_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00003 名称=/opt/oracle/oradata/mmsgdb/undotbs01.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1kltavn7_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00005 名称=/opt/oracle/data/imap_db.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1lltavn8_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00008 名称=/opt/oracle/data/imaptmdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1mltavn9_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00007 名称=/opt/oracle/data/imapsmdb.dbf
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
输入数据文件: 文件号=00004 名称=/opt/oracle/oradata/mmsgdb/users01.dbf
输入数据文件: 文件号=00017 名称=/opt/oracle/oradata/mmsgdb/test.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1nltavna_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00002 名称=/opt/oracle/oradata/mmsgdb/sysaux01.dbf
输入数据文件: 文件号=00014 名称=/opt/oracle/oradata/mmsgdb/rman_data.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1oltavnb_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00011 名称=/opt/oracle/data/nmsguest.dbf
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1pltavnr_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
备份集内包括当前控制文件
备份集内包括当前的 SPFILE
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1qltavns_1_1 标记=TAG20101118T170518 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10

启动 backup 于 18-11月-10
当前日志已存档
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的归档日志备份集
通道 ORA_DISK_1: 正在指定备份集内的归档日志
输入归档日志线程=1 序列=51 RECID=31 STAMP=735411966
通道 ORA_DISK_1: 正在启动段 1 于 18-11月-10
通道 ORA_DISK_1: 已完成段 1 于 18-11月-10
段句柄=/opt/oracle/product/11g/dbs/1rltavnv_1_1 标记=TAG20101118T170607 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 18-11月-10

RMAN>
```

## 增量备份

当数据库运行在非归档模式下，只有在数据库干净的关闭情况下，才可进行数据的一致性增量备份；当数据库运行在归档模式下，无论数据库关闭还是启动，均可以对数据库进行增量备份。

建立增量备份，就是在备份过程中增加参数INCREMENTAL LEVEL=n。

例如：建立一个增量级别为0的全库备份。

```shell
RMAN> backup INCREMENTAL LEVEL=0 database;

启动 backup 于 19-11月-10
分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=1068 设备类型=DISK
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00010 名称=/opt/oracle/data/perfdb.dbf
输入数据文件: 文件号=00016 名称=/home/yjh/oradata/yjhdata01
输入数据文件: 文件号=00015 名称=/home/wyz/wyzoradata/wyz.dbf
输入数据文件: 文件号=00012 名称=/opt/oracle/data/perfdb_idx.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/1vltdh86_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:07
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00006 名称=/opt/oracle/data/imaplogdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/20ltdh8e_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00009 名称=/opt/oracle/data/alarmdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/21ltdh8f_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00001 名称=/opt/oracle/oradata/mmsgdb/system01.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/22ltdh8g_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00003 名称=/opt/oracle/oradata/mmsgdb/undotbs01.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/23ltdh8v_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00005 名称=/opt/oracle/data/imap_db.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/24ltdh90_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00008 名称=/opt/oracle/data/imaptmdb.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/25ltdh91_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00007 名称=/opt/oracle/data/imapsmdb.dbf
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
输入数据文件: 文件号=00004 名称=/opt/oracle/oradata/mmsgdb/users01.dbf
输入数据文件: 文件号=00017 名称=/opt/oracle/oradata/mmsgdb/test.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/26ltdh93_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00002 名称=/opt/oracle/oradata/mmsgdb/sysaux01.dbf
输入数据文件: 文件号=00014 名称=/opt/oracle/oradata/mmsgdb/rman_data.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/27ltdh94_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:15
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00011 名称=/opt/oracle/data/nmsguest.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/28ltdh9j_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
通道 ORA_DISK_1: 正在启动压缩的增量级别 0 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
备份集内包括当前控制文件
备份集内包括当前的 SPFILE
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/29ltdh9k_1_1 标记=TAG20101119T161710 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 19-11月-10

RMAN>
```

再例如：建立一个增量级别为1的数据库表空间的备份

```shell
RMAN> backup incremental level=1 tablespace MMSG;

启动 backup 于 19-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的增量级别 1 数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/2bltdhds_1_1 标记=TAG20101119T162012 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 19-11月-10

RMAN>
```

注：

* Rman默认创建的增量备份是Differential方式，如果要建立Cumulative方式的增量备份，在执行BACKUP命令时显式指定即可，例如：```RMAN>  BACKUP INCREMENTAL LEVEL=2 CUMULATIVE DATABASE; ```


## 冗余备份

RMAN提供了一种更谨慎的备份策略：Duplexed 方式备份，实质就是在生成备份集的同时，向指定位置生成指定份数(最大不超过4份)的备份集副本。防止灾难行的事故导致数据库损坏或者备份数据丢失，提高备份的可用性。

### 显示指定copies数量

```shell
RMAN> backup copies 2 tablespace MMSG;

启动 backup 于 19-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10, 有 2 个副本和标记 TAG20101119T163829
段 handle=/opt/oracle/product/11g/dbs/2cltdig5_1_1 comment=NONE
段 handle=/opt/oracle/product/11g/dbs/2cltdig5_1_2 comment=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 19-11月-10

RMAN>
```

### 在批处理中增加set backup copies参数

```shell
RMAN> run
2> {
3> set backup copies 1;
4> allocate channel c1 device type disk;
5> backup tablespace MMSG;
6> }

正在执行命令: SET BACKUP COPIES

分配的通道: c1
通道 c1: SID=1069 设备类型=DISK

启动 backup 于 19-11月-10
使用通道 ORA_DISK_1
通道 ORA_DISK_1: 正在启动压缩的全部数据文件备份集
通道 ORA_DISK_1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
通道 ORA_DISK_1: 正在启动段 1 于 19-11月-10
通道 ORA_DISK_1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/product/11g/dbs/2dltdj5h_1_1 标记=TAG20101119T164953 注释=NONE
通道 ORA_DISK_1: 备份集已完成, 经过时间:00:00:01
完成 backup 于 19-11月-10

RMAN>
```

### 通过configure设定预备份Duplexed方式

```shell
RMAN> configure datafile backup copies for device type disk to 1;

新的 RMAN 配置参数:
CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE DISK TO 1;
已成功存储新的 RMAN 配置参数
正在启动全部恢复目录的 resync
完成全部 resync

RMAN>
```

# RMAN恢复

## 恢复spfile文件

```shell
oracle@mmsg:~> rman target/

恢复管理器: Release 11.1.0.7.0 - Production on 星期四 11月 18 18:14:15 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

已连接到目标数据库 (未启动)

RMAN> connect catalog rman/rman@inomc

RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-04004: 来自恢复目录数据库的警告: ORA-12514: TNS: 监听程序当前无法识别连接描述符中请求的服务

RMAN> startup nomount

启动失败: ORA-01078: failure in processing system parameters
LRM-00109: ???????????????? '/opt/oracle/product/11g/dbs/initinomc.ora'

在没有参数文件的情况下启动 Oracle 实例以检索 spfile
Oracle 实例已启动

系统全局区域总计     158662656 字节

Fixed Size                     2157784 字节
Variable Size                 83886888 字节
Database Buffers              67108864 字节
Redo Buffers                   5509120 字节

RMAN> restore spfile from autobackup;

启动 restore 于 18-11月-10
使用目标数据库控制文件替代恢复目录
分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=96 设备类型=DISK

RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-03002: restore 命令 (在 11/18/2010 18:14:46 上) 失败
RMAN-06495: 必须用 SET DBID 命令明确指定 DBID

RMAN> set dbid=1037536304

正在执行命令: SET DBID

RMAN> restore spfile from autobackup;

启动 restore 于 18-11月-10
使用通道 ORA_DISK_1

通道 ORA_DISK_1: 寻找以下日期的 AUTOBACKUP: 20101118
通道 ORA_DISK_1: 已找到的 AUTOBACKUP: c-1037536304-20101118-00
通道 ORA_DISK_1: 正在从 AUTOBACKUP c-1037536304-20101118-00 还原 spfile
通道 ORA_DISK_1: 从 AUTOBACKUP 还原 SPFILE 已完成
完成 restore 于 18-11月-10

RMAN> startup force

Oracle 实例已启动
数据库已装载
数据库已打开

系统全局区域总计    8351150080 字节

Fixed Size                     2161272 字节
Variable Size               7784629640 字节
Database Buffers             536870912 字节
Redo Buffers                  27488256 字节

RMAN>
```

注：
* RMAN的参数confile autobackup必须设置为on，这样才能恢复spfile文件。

## 口令文件恢复

由于RMAN不支持口令文件的备份，所以，无法通过RMAN进行口令文件的恢复，通过orapw命令重新建立口令文件即可。

```shell
oracle@mmsg:~/product/11g/dbs> orapwd
Usage: orapwd file=<fname> password=<password> entries=<users> force=<y/n> ignorecase=<y/n> nosysdba=<y/n>

  where
    file - name of password file (required),
    password - password for SYS, will be prompted if not specified at command line,
    entries - maximum number of distinct DBA (optional),
    force - whether to overwrite existing file (optional),
    ignorecase - passwords are case-insensitive (optional),
    nosysdba - whether to shut out the SYSDBA logon (optional Database Vault only).
    
  There must be no spaces around the equal-to (=) character.


表空间的恢复
RMAN> shutdown immediate

数据库已关闭
数据库已卸装
Oracle 实例已关闭

RMAN>
RMAN> startup mount

Oracle 实例已启动
数据库已装载

系统全局区域总计    8351150080 字节

Fixed Size                     2161272 字节
Variable Size               7784629640 字节
Database Buffers             536870912 字节
Redo Buffers                  27488256 字节

RMAN> restore tablespace TEST;

RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-00558: 分析输入命令时出错
RMAN-01009: 语法错误: 找到 "test": 应为: "double-quoted-string, identifier, single-quoted-string" 中的一个
RMAN-01007: 在第 1 行第 20 列, 文件: standard input

RMAN> restore tablespace "TEST";

启动 restore 于 23-11月-10
使用目标数据库控制文件替代恢复目录
分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=1089 设备类型=DISK

通道 ORA_DISK_1: 正在开始还原数据文件备份集
通道 ORA_DISK_1: 正在指定从备份集还原的数据文件
通道 ORA_DISK_1: 将数据文件 00017 还原到 /opt/oracle/oradata/mmsgdb/test.dbf
通道 ORA_DISK_1: 正在读取备份片段 /opt/oracle/rman/full_bak_2hltdnio_1_1
通道 ORA_DISK_1: 段句柄 = /opt/oracle/rman/full_bak_2hltdnio_1_1 标记 = TAG20101119T180505
通道 ORA_DISK_1: 已还原备份片段 1
通道 ORA_DISK_1: 还原完成, 用时: 00:00:04
完成 restore 于 23-11月-10

RMAN> recover tablespace "TEST"; 

启动 recover 于 23-11月-10
使用通道 ORA_DISK_1

正在开始介质的恢复
介质恢复完成, 用时: 00:00:03

完成 recover 于 23-11月-10

RMAN> alter database open 
2> ;

数据库已打开

RMAN>    
```

## 数据文件的恢复

这个操作类似于表空间的恢复

```shell
RMAN>shutdown immediate
RMAN>startup mount
RMAN>restorer datafile datafilepath;  #或者是restore datafile datafile_num; 
RMAN> recover datafile datafilepath;  #或者是recover datafile datafile_num;
RMAN> alter database open
```

## 归档模式下，数据文件丢失的恢复

### 模拟场景与测试准备工作

1、先创建表空间TEST，创建test用户，默认表空间为TEST；

2、以test用户登陆数据库，创建表test，并向表test中insert几条记录

```shell
insert into test(id) values (1);
insert into test(id) values (2);
insert into test(id) values (3);
insert into test(id) values (4);
insert into test(id) values (5);
insert into test(id) values (6);
insert into test(id) values (7);
commit;
```

3、将TEST表空间对应的数据文件mv或者rm操作

4、停止数据库后，再次启动数据库。

```shell
oracle@mmsg:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期二 11月 23 11:17:32 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.

已连接到空闲例程。

SQL> startup
ORACLE 例程已经启动。

Total System Global Area 8351150080 bytes
Fixed Size                  2161272 bytes
Variable Size            7784629640 bytes
Database Buffers          536870912 bytes
Redo Buffers               27488256 bytes
数据库装载完毕。
ORA-01157: 无法标识/锁定数据文件 17 - 请参阅 DBWR 跟踪文件
ORA-01110: 数据文件 17: '/opt/oracle/oradata/mmsgdb/test.dbf'
```

5、查询数据库当前状态

```shell
SQL> select instance_name,status from v$instance;

INSTANCE_NAME    STATUS
---------------- ------------
inomc            MOUNTED

SQL>
```

### RMAN恢复操作

```shell
oracle@mmsg:~> rman  target/

恢复管理器: Release 11.1.0.7.0 - Production on 星期二 11月 23 11:18:24 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

已连接到目标数据库: INOMC (DBID=1037536304, 未打开)

RMAN> connect catalog rman/rman@inomc

RMAN-00571: ===========================================================
RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
RMAN-00571: ===========================================================
RMAN-04004: 来自恢复目录数据库的警告: ORA-01033: ORACLE 正在初始化或关闭

RMAN> restore datafile '/opt/oracle/oradata/mmsgdb/test.dbf';

启动 restore 于 23-11月-10
使用目标数据库控制文件替代恢复目录
分配的通道: ORA_DISK_1
通道 ORA_DISK_1: SID=1087 设备类型=DISK

通道 ORA_DISK_1: 正在开始还原数据文件备份集
通道 ORA_DISK_1: 正在指定从备份集还原的数据文件
通道 ORA_DISK_1: 将数据文件 00017 还原到 /opt/oracle/oradata/mmsgdb/test.dbf
通道 ORA_DISK_1: 正在读取备份片段 /opt/oracle/rman/full_bak_2hltdnio_1_1
通道 ORA_DISK_1: 段句柄 = /opt/oracle/rman/full_bak_2hltdnio_1_1 标记 = TAG20101119T180505
通道 ORA_DISK_1: 已还原备份片段 1
通道 ORA_DISK_1: 还原完成, 用时: 00:00:01
完成 restore 于 23-11月-10

RMAN> recover datafile '/opt/oracle/oradata/mmsgdb/test.dbf';

启动 recover 于 23-11月-10
使用通道 ORA_DISK_1

正在开始介质的恢复
介质恢复完成, 用时: 00:00:02

完成 recover 于 23-11月-10

RMAN> alter database open;

数据库已打开

RMAN>
oracle@mmsg:~> sqlplus test/test@inomc

SQL*Plus: Release 11.1.0.7.0 - Production on 星期二 11月 23 11:20:07 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> select * from test;

        ID
----------
         1
         2
         3
         4
         5
         6
         7

已选择7行。

SQL>
```

## 全库的恢复

```shell
RMAN>shutdown immediate
RMAN>startup mount
RMAN> run
2> {
3> allocate channel c1 device type disk;
4> restore database;
5> }
```

## 控制文件的恢复

1、数据库启动到非安装状态(nomount)

2、RMAN恢复

```shell
RMAN> run {
2> allocate channel c1 device type disk;
3> restore controlfile from ‘/opt/oracle/rman/back_c-1037536304-20101123-07’;
4> release channel c1;
5> }
```

## 重做日志文件的恢复

```shell
SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
SQL> startup mount
ORACLE 例程已经启动。

Total System Global Area 8351150080 bytes
Fixed Size                  2161272 bytes
Variable Size            7784629640 bytes
Database Buffers          536870912 bytes
Redo Buffers               27488256 bytes
数据库装载完毕。
SQL> recover database using backup controlfile until cancel;
ORA-00279: 更改 4265765 (在 11/23/2010 15:01:28 生成) 对于线程 1 是必需的
ORA-00289: 建议: /opt/oracle/archivelog/1_63_730813273.dbf
ORA-00280: 更改 4265765 (用于线程 1) 在序列 #63 中


指定日志: {<RET>=suggested | filename | AUTO | CANCEL}
………………………………………………………………………………………………
…………………………………………………………………………………………………
SQL> alter database open resetlogs;

数据库已更改。

SQL>
```

## 归档日志文件的恢复

```shell
RMAN>shutdown immediate
RMAN>startup mount
RMAN> run
2> {
3> allocate channel c1 device type disk;
4> restore archivelog all;
5> }
```

# 综合实践

## 场景1 定时备份数据库到既定目录下，并自动删除过期备份归档日志

### 要求

* 1 、每天夜间1点执行； 
* 2 、数据库全备，同时备份控制文件及归档日志文件，备份文件保存至：/opt/oracle/rman目录下，并在完成归档日志文件备份后，自动删除已备份的归档日志； 
* 3 、备份保留7天，过期则自动删除； 
* 4 、保留操作日志备查； 

### RMAN脚本

```shell
oracle@mmsg:~/rman> more back_full.rman 
run
{
configure retention policy to recovery window of 7 days;
configure controlfile autobackup on;
configure controlfile autobackup format for device type disk to '/opt/oracle/rman/full_bak_%F';
allocate channel c1 device type disk format '/opt/oracle/rman/full_bak_%U';
backup database skip inaccessible filesperset 10 plus archivelog filesperset 20 delete  all input;
release channel c1; 
}
allocate channel for maintenance device type disk;
crosscheck backupset;
delete noprompt obsolete;
```

|SKIP 选项| 说明|
|-------------------|-------------------------------------------------|
|SKIP INACCESSIBLE |表示跳过不可读的文件。我们知道一些offline的数据文件只要存在于磁盘上就仍然可被读取，但是可能有些文件已经被删除或移到它处造成不可读，加上这个参数就会跳过这些文件|
|SKIP OFFLINE |跳过offline的数据文件|
|SKIP READONLY |跳过那些所在表空间为read-only的数据文件|


### 命令执行

```shell
oracle@mmsg:~/rman> rman target / msglog /opt/oracle/rman/bak.log cmdfile=/opt/oracle/rman/back_full.rman
```

### 日志

```shell
oracle@mmsg:~/rman> more bak.log 

恢复管理器: Release 11.1.0.7.0 - Production on 星期五 11月 19 18:04:46 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

连接到目标数据库: INOMC (DBID=1037536304)

RMAN> run
2> {
3> configure retention policy to recovery window of 7 days;
4> configure controlfile autobackup on;
5> configure controlfile autobackup format for device type disk to '/opt/oracle/rman/full_bak_%F';
6> allocate channel c1 device type disk format '/opt/oracle/rman/full_bak_%U';
7> backup database skip inaccessible filesperset 10 plus archivelog filesperset 20 delete  all input;
8> release channel c1; 
9> }
10> allocate channel for maintenance device type disk;
11> crosscheck backupset;
12> delete noprompt obsolete;
13> 
使用目标数据库控制文件替代恢复目录
旧的 RMAN 配置参数:
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 2 DAYS;
新的 RMAN 配置参数:
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
已成功存储新的 RMAN 配置参数

旧的 RMAN 配置参数:
CONFIGURE CONTROLFILE AUTOBACKUP OFF;
新的 RMAN 配置参数:
CONFIGURE CONTROLFILE AUTOBACKUP ON;
已成功存储新的 RMAN 配置参数

新的 RMAN 配置参数:
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/opt/oracle/rman/full_bak_%F';
已成功存储新的 RMAN 配置参数

分配的通道: c1
通道 c1: SID=1065 设备类型=DISK

启动 backup 于 19-11月-10
当前日志已存档
通道 c1: 正在启动压缩的归档日志备份集
通道 c1: 正在指定备份集内的归档日志
输入归档日志线程=1 序列=49 RECID=29 STAMP=735411706
输入归档日志线程=1 序列=50 RECID=30 STAMP=735411902
输入归档日志线程=1 序列=51 RECID=31 STAMP=735411966
输入归档日志线程=1 序列=52 RECID=32 STAMP=735437813
输入归档日志线程=1 序列=53 RECID=33 STAMP=735501889
通道 c1: 正在启动段 1 于 19-11月-10
通道 c1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/rman/full_bak_2fltdni1_1_1 标记=TAG20101119T180449 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:15
通道 c1: 正在删除归档日志
归档日志文件名=/opt/oracle/archivelog/1_49_730813273.dbf RECID=29 STAMP=735411706
归档日志文件名=/opt/oracle/archivelog/1_50_730813273.dbf RECID=30 STAMP=735411902
归档日志文件名=/opt/oracle/archivelog/1_51_730813273.dbf RECID=31 STAMP=735411966
归档日志文件名=/opt/oracle/archivelog/1_52_730813273.dbf RECID=32 STAMP=735437813
归档日志文件名=/opt/oracle/archivelog/1_53_730813273.dbf RECID=33 STAMP=735501889
完成 backup 于 19-11月-10

启动 backup 于 19-11月-10
通道 c1: 正在启动压缩的全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00010 名称=/opt/oracle/data/perfdb.dbf
输入数据文件: 文件号=00007 名称=/opt/oracle/data/imapsmdb.dbf
输入数据文件: 文件号=00013 名称=/opt/oracle/oradata/mmsgdb/mmsg.dbf
输入数据文件: 文件号=00016 名称=/home/yjh/oradata/yjhdata01
输入数据文件: 文件号=00015 名称=/home/wyz/wyzoradata/wyz.dbf
输入数据文件: 文件号=00012 名称=/opt/oracle/data/perfdb_idx.dbf
输入数据文件: 文件号=00006 名称=/opt/oracle/data/imaplogdb.dbf
通道 c1: 正在启动段 1 于 19-11月-10
通道 c1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/rman/full_bak_2gltdnih_1_1 标记=TAG20101119T180505 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:07
通道 c1: 正在启动压缩的全部数据文件备份集
通道 c1: 正在指定备份集内的数据文件
输入数据文件: 文件号=00009 名称=/opt/oracle/data/alarmdb.dbf
输入数据文件: 文件号=00001 名称=/opt/oracle/oradata/mmsgdb/system01.dbf
输入数据文件: 文件号=00003 名称=/opt/oracle/oradata/mmsgdb/undotbs01.dbf
输入数据文件: 文件号=00005 名称=/opt/oracle/data/imap_db.dbf
输入数据文件: 文件号=00008 名称=/opt/oracle/data/imaptmdb.dbf
输入数据文件: 文件号=00002 名称=/opt/oracle/oradata/mmsgdb/sysaux01.dbf
输入数据文件: 文件号=00011 名称=/opt/oracle/data/nmsguest.dbf
输入数据文件: 文件号=00014 名称=/opt/oracle/oradata/mmsgdb/rman_data.dbf
输入数据文件: 文件号=00004 名称=/opt/oracle/oradata/mmsgdb/users01.dbf
输入数据文件: 文件号=00017 名称=/opt/oracle/oradata/mmsgdb/test.dbf
通道 c1: 正在启动段 1 于 19-11月-10
通道 c1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/rman/full_bak_2hltdnio_1_1 标记=TAG20101119T180505 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:25
完成 backup 于 19-11月-10

启动 backup 于 19-11月-10
当前日志已存档
通道 c1: 正在启动压缩的归档日志备份集
通道 c1: 正在指定备份集内的归档日志
输入归档日志线程=1 序列=54 RECID=34 STAMP=735501938
通道 c1: 正在启动段 1 于 19-11月-10
通道 c1: 已完成段 1 于 19-11月-10
段句柄=/opt/oracle/rman/full_bak_2iltdnji_1_1 标记=TAG20101119T180538 注释=NONE
通道 c1: 备份集已完成, 经过时间:00:00:01
通道 c1: 正在删除归档日志
归档日志文件名=/opt/oracle/archivelog/1_54_730813273.dbf RECID=34 STAMP=735501938
完成 backup 于 19-11月-10

启动 Control File and SPFILE Autobackup 于 19-11月-10
段 handle=/opt/oracle/rman/full_bak_c-1037536304-20101119-00 comment=NONE
完成 Control File and SPFILE Autobackup 于 19-11月-10

释放的通道: c1

分配的通道: ORA_MAINT_DISK_1
通道 ORA_MAINT_DISK_1: SID=1065 设备类型=DISK

交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/0tltan1p_1_1 RECID=29 STAMP=735403065
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/0ultau5s_1_1 RECID=30 STAMP=735410365
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/0vltaue2_1_1 RECID=31 STAMP=735410627
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/10ltauea_1_1 RECID=32 STAMP=735410634
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/11ltaueb_1_1 RECID=33 STAMP=735410635
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/12ltauec_1_1 RECID=34 STAMP=735410636
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/13ltauer_1_1 RECID=35 STAMP=735410651
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/14ltaues_1_1 RECID=36 STAMP=735410652
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/15ltauet_1_1 RECID=37 STAMP=735410653
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/16ltauev_1_1 RECID=38 STAMP=735410655
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/17ltauf2_1_1 RECID=39 STAMP=735410658
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/18ltaufh_1_1 RECID=40 STAMP=735410673
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/19ltaufi_1_1 RECID=41 STAMP=735410675
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1altauil_1_1 RECID=42 STAMP=735410773
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1bltauim_1_1 RECID=43 STAMP=735410775
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1cltaujq_1_1 RECID=44 STAMP=735410810
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1dltaujs_1_1 RECID=45 STAMP=735410813
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1eltavfr_1_1 RECID=46 STAMP=735411707
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1fltavlv_1_1 RECID=47 STAMP=735411903
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1gltavme_1_1 RECID=48 STAMP=735411918
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1hltavml_1_1 RECID=49 STAMP=735411925
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1iltavmm_1_1 RECID=50 STAMP=735411927
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1jltavmo_1_1 RECID=51 STAMP=735411928
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1kltavn7_1_1 RECID=52 STAMP=735411943
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1lltavn8_1_1 RECID=53 STAMP=735411944
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1mltavn9_1_1 RECID=54 STAMP=735411945
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1nltavna_1_1 RECID=55 STAMP=735411946
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1oltavnb_1_1 RECID=56 STAMP=735411948
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1pltavnr_1_1 RECID=57 STAMP=735411963
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1qltavns_1_1 RECID=58 STAMP=735411965
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1rltavnv_1_1 RECID=59 STAMP=735411967
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1sltb3li_1_1 RECID=60 STAMP=735415987
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/c-1037536304-20101118-00 RECID=61 STAMP=735415990
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1ultcmae_1_1 RECID=62 STAMP=735467855
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/1vltdh86_1_1 RECID=63 STAMP=735495431
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/20ltdh8e_1_1 RECID=64 STAMP=735495438
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/21ltdh8f_1_1 RECID=65 STAMP=735495439
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/22ltdh8g_1_1 RECID=66 STAMP=735495440
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/23ltdh8v_1_1 RECID=67 STAMP=735495455
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/24ltdh90_1_1 RECID=68 STAMP=735495456
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/25ltdh91_1_1 RECID=69 STAMP=735495458
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/26ltdh93_1_1 RECID=70 STAMP=735495459
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/27ltdh94_1_1 RECID=71 STAMP=735495460
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/28ltdh9j_1_1 RECID=72 STAMP=735495475
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/29ltdh9k_1_1 RECID=73 STAMP=735495477
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/2bltdhds_1_1 RECID=74 STAMP=735495612
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/2cltdig5_1_1 RECID=75 STAMP=735496710
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/2cltdig5_1_2 RECID=76 STAMP=735496710
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/2dltdj5h_1_1 RECID=77 STAMP=735497394
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/product/11g/dbs/2eltdj89_1_1 RECID=78 STAMP=735497481
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/rman/full_bak_2fltdni1_1_1 RECID=79 STAMP=735501889
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/rman/full_bak_2gltdnih_1_1 RECID=80 STAMP=735501905
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/rman/full_bak_2hltdnio_1_1 RECID=81 STAMP=735501914
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/rman/full_bak_2iltdnji_1_1 RECID=82 STAMP=735501938
交叉校验备份片段: 找到为 'AVAILABLE'
备份片段句柄=/opt/oracle/rman/full_bak_c-1037536304-20101119-00 RECID=83 STAMP=735501940
已交叉检验的 55 对象

RMAN 保留策略将应用于该命令
将 RMAN 保留策略设置为 7 天的恢复窗口
未找到已废弃的备份

恢复管理器完成。
```
### 执行定时任务

设置crontab（略）。

## 场景2 备份整个数据库，并清除3天天备份的归档日志

### 要求

1、备份整个数据库，包括控制文件以及归档日志；
2、清除3天前备份的归档日志。

### RMAN脚本

```shell
oracle@mmsc103:~/rmanbak> more everydaybak.rman
#script:fullbakup.rman
# creater:wangyunzeng
# date:2011-03-11
# desc:backup all database datafile in archive with rman
# connect database
connect target rman/rman;
connect catalog rman/rman@mmsgdb;

#start backup database
run
{
  allocate channel t1 type disk;   
configure controlfile autobackup format for device type disk to '/opt/oracle/rmanbak/controlfile_bak_%F';                        
backup database format 'fullbak_%s_%p_%u'   (archivelog all );
crosscheck backupset;
delete noprompt obsolete;
delete noprompt archivelog until time "sysdate -3";
release channel t1;          
}
#end
```

### Perl脚本

```shell
oracle@mmsc103:~/rmanbak> more backup.perl 
#!/use/bin/perl
##################################################
###        作用：rman定时任务脚本              ###
###        日期：2011-03-11                    ###
###        作者：王运增                        ###
##################################################

#获取系统当前时间
my ($sec,$min,$hour,$day,$month,$year)= localtime(time());
$year+=1900;
$month=sprintf("%02d",$month+1);
$day=sprintf("%02d",$day);
$hour=sprintf("%02d",$hour);
$min=sprintf("%02d",$min);
$sec=sprintf("%02d",$sec);
my $daytime = "$year$month$day$hour$min$sec";

system("/opt/oracle/product/11g/bin/rman   cmdfile = '/opt/oracle/rmanbak/everydaybak.rman' msglog=/opt/oracle/rmanbak/everydaybak_$
daytime.log");

oracle@mmsc103:~/rmanbak>
```

### 设定定时任务

```shell
mmsc103:~ # crontab -e

      # DO NOT EDIT THIS FILE - edit the master and reinstall.
      # (/tmp/temp.txt installed on Wed Jan  5 17:42:07 2011)
      # (Cron version V5.0 -- $Id: crontab.c,v 1.12 2004/01/23 18:56:42 vixie Exp $)
      0 1 * * * su - oracle -c /opt/oracle/rmanbak/backup.perl
```

# 附录

## 术语

### Backup Sets （备份集合）

备份集合的特性：包括一个或多个数据文件或归档日志，以oracle专有的格式保存，有一个完全的所有的备份片集合构成，构成一个完全备份或增量备份。


### Backup Pieces （备份片）

一个备份集由若干个备份片组成。每个备份片是一个单独的输出文件。一个备份片的大 小是有限制的；如果没有大小的限制，  备份集就只由一个备份片构成。备份片的大小不能 大于使用的文件系统所支持的文件长度的最大值。

### Image Copies 镜像备份

镜像备份是独立文件（数据文件、归档日志、控制文件）的备份。它很类似操作系统级 的文件备份。它不是备份集或备份片，也没有被压缩。

### Full backup Sets 全备份集合

全备份是一个或多个数据文件中使用过的数据块的的备份。没有使用过的数据块是不被备份的，也就是说，oracle  进行备份集合的压缩。

### Incremental backup sets 增量备份集合

增量备份是指备份一个或多个数据文件的自从上一次同一级别的或更低级别的备份以来被修改过的数据块。  与完全备份相同，增量备份也进行压缩。

### File multiplexing   多工
多个数据文件可以在一个备份集中。

### Recovery catalog resyncing  恢复目录同步

使用恢复管理器执行 backup、copy、restore 或者 switch 命令时，恢复目录自动进行更 新，但是有关日志与归档日志信息没有自动记入恢复目录。需要进行目录同步。使用 resync catalog命令进行同步。
```    RMAN> resync catalog；```

### Incarnation  对应物

在不完全恢复完成之后，通常需要使用  resetlogs  选项来打开数据库。resetlogs  表示一个 数据库逻辑生存期的结束和另一个数据库逻辑生存期的开始。数据库的逻辑生存期也被称为 一个对应物（incarnation）。每次使用  resetlogs  选项来打开数据库后都会创建一个新的数据库 对应物。


## 与RMAN备份相关的动态性能表

|动态性能表名| 说明|
|--------------------------|----------------------------------------------------------|
|V$ARCHIVED_LOG |本视图包含了所有归档重做日志文件的创建情况，备份情况以及其他信息|
|V$BACKUP_CORRUPTION |这个视图显示了RMAN在哪些备份集中发现了损坏的数据坏。在你使用BACKUP VALIDATE命令对备份集进行检查时如果发现了损坏的数据块，RMAN将在这个视图中写入记录|
|V$COPY_CORRUPTIO |本视图显示了哪些镜像复制备份文件已经被损坏|
|V$BACKUP_DATAFILE |本视图通常用来获取每个数据文件中非空白数据块的数量，从而帮助你创建出大小基本相等的备份集。另外，在视图中也包含了数据文件中损坏的数据块的信息|
|V$BACKUP_REDOLOG |本视图显示了在现有的备份集中有哪些归档重做日志文件|
|V$BACKUP_SET |本视图显示了已经创建的备份集的信息|
|V$BACKUP_PIECE |本视图显示了已经创建的备份片段的信息|


### 获得正在进行的镜像复制操作的状态信息

```shell
Select  sid,serial#, context ,sofar,totalwork,totalwork,
round(sofar / totalwork *  100 ,  2 )
from v$session_longops where  opname  like  'RMAN::aggregate';
```

### 获得rman用来完成备份操作的服务进程的SID与SPID信息  

```shell
select  sid, spid, client_info 
from  v$process p, v$session s 
where  p.addr = s.paddr 
and  client_info  like   '%id=rman%';
```

### 查询数据文件，临时文件与表空间对应及数据文件序号

```shell
select  ts.tablespace_name, df.file_name, df.file_id, tf.file_name 
from  dba_tablespaces ts, dba_data_files df, dba_temp_files tf 
where  ts.tablespace_name = df.tablespace_name(+) 
and  ts.tablespace_name = tf.tablespace_name(+);
```
