---
layout:     post
title:      "Oracle导入导出之exp/imp"
subtitle:   "Oracle exp/imp"
date:       2010-03-30
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# 导入导出的作用

EXP和IMP不仅可以用于实现逻辑备份和逻辑恢复,还可以实现下面的功能：

* 1、重新组织表
* 2、在用户之间移动对象
* 3、在数据库之间移动对象
* 4、升级数据库到其他平台
* 5、升级数据库到高版本
* 6、实现逻辑备份和恢复


# exp命令详解

EXP 将数据库部分或全部对象的结构和数据导出,并存储到OS文件中的过程。

## exp命令行选项

```
oracle@GW_8:~> exp help=y

Export: Release 11.1.0.7.0 - Production on 星期五 2月 1 08:42:26 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.

通过输入 EXP 命令和您的用户名/口令, 导出
操作将提示您输入参数: 

     例如: EXP SCOTT/TIGER

或者, 您也可以通过输入跟有各种参数的 EXP 命令来控制导出
的运行方式。要指定参数, 您可以使用关键字: 

     格式:  EXP KEYWORD=value 或 KEYWORD=(value1,value2,...,valueN)
     例如: EXP SCOTT/TIGER GRANTS=Y TABLES=(EMP,DEPT,MGR)
               或 TABLES=(T1:P1,T1:P2), 如果 T1 是分区表

USERID 必须是命令行中的第一个参数。

关键字   说明 (默认值)         关键字      说明 (默认值)
--------------------------------------------------------------------------
USERID   用户名/口令           FULL        导出整个文件 (N)
BUFFER   数据缓冲区大小        OWNER        所有者用户名列表
FILE     输出文件 (EXPDAT.DMP)  TABLES     表名列表
COMPRESS  导入到一个区 (Y)   RECORDLENGTH   IO 记录的长度
GRANTS    导出权限 (Y)          INCTYPE     增量导出类型
INDEXES   导出索引 (Y)         RECORD       跟踪增量导出 (Y)
DIRECT    直接路径 (N)         TRIGGERS     导出触发器 (Y)
LOG      屏幕输出的日志文件    STATISTICS    分析对象 (ESTIMATE)
ROWS      导出数据行 (Y)        PARFILE      参数文件名
CONSISTENT 交叉表的一致性 (N)   CONSTRAINTS  导出的约束条件 (Y)

OBJECT_CONSISTENT    只在对象导出期间设置为只读的事务处理 (N)
FEEDBACK             每 x 行显示进度 (0)
FILESIZE             每个转储文件的最大大小
FLASHBACK_SCN        用于将会话快照设置回以前状态的 SCN
FLASHBACK_TIME       用于获取最接近指定时间的 SCN 的时间
QUERY                用于导出表的子集的 select 子句
RESUMABLE            遇到与空格相关的错误时挂起 (N)
RESUMABLE_NAME       用于标识可恢复语句的文本字符串
RESUMABLE_TIMEOUT    RESUMABLE 的等待时间
TTS_FULL_CHECK       对 TTS 执行完整或部分相关性检查
VOLSIZE              写入每个磁带卷的字节数
TABLESPACES          要导出的表空间列表
TRANSPORT_TABLESPACE 导出可传输的表空间元数据 (N)
TEMPLATE             调用 iAS 模式导出的模板名
```

### 1、BUFFER

该选项用于指定提取行数据时的缓冲区尺寸.通过设置该选项,可以确定导出时数据提起尺寸.该选项只适用于常规选项. 
Exp scott/tiger tables=dept,emp file=a.dmp buffer=81920 

### 2、COMPRESS

该选项用于指定导入管理初始区(INITIAL)的方法.默认值为Y.当设置该选项为Y时,oracle会将INITIAL设置为表段的当前尺寸;当设置该选项为N时,oracle仍然使用表段的原有存储参数(INITIAL和NEXT). 

### 3、CONSISTENT

该选项用于指定是否使用SET TRANSACTION READ ONLY语句确保取得一致时间点的数据,默认值为N .当设置该选项为Y时,所有被导出表会在同一个事务内完成导出.确保取得一致时间点的数据,当设置该选项为N时,每个被导出表会使用独立事务导出.需要注意,导出数据库时,为了避免snapshot too old 错误,不要将选项CONSISTENT设置为Y. 

### 4、CONSTRAINTS

设是否导出表的约束,默认值为Y. 

### 5、DIRECT

该选项用于指定是否使用直接导出方式,默认值为N.当设置该选项为Y时,采用直接导出方式;当设置为N时,采用常规导出方式.需要注意,直接导出方式速度要优于常规导出,但要求客户端和服务端的字符集必须完全一致. 

### 6、FEEDBACK

指定导出行数显示进程框,默认为0,如果设置该选项为10,则每导出10行显示一个园点(.) 

### 7、FILE

该选项用于指定导出文件名 

### 8、FILESIZE

该选项用于指定导出文件的最大尺寸. 

### 9、FLASHBACK_SCN

该选项用于指定导出特定SCN时刻的表数据.FLASHBACK_SCN选项和FLASHBACK_TIME选项不能同时使用. 

```
Exp system/manager tables=scott.dept,scott.emp file=a.dmp 
Flashback_scn=941931 
```

### 10、FLASHBACK_TIME

指定导出特定时刻的数据 

```
Exp system/manager tables=scott.dept,scott.emp file=a.dmp 
Flashback_time="'2004-07-06 15:59:52'"
```

### 11、FULL 

指定数据库导出模式,默认值为N,当设置为Y时,导出除SYS外所有其他方案的对象. 

### 12、GRANTS

该选项用于指定是否导出对象权限信息,默认值为Y. 

### 13、HELP

展示exp相关命令项信息。

### 14、INDEXES

指定是否导出与表和簇相关的索引,默认值为Y 

### 15、LOG

指定导出日志文件的名称,默认情况下不好生成导出日志文件. 

### 16、OBJECT_CONSISTENT

用于指定是否基于对象级设置只读事务导出,默认值为N,当设置该选项为Y时,基于每个对象设置一个只读事务,然后导出相应对象的数据。

### 17、OWNER

指定用于导出模式. 

### 18、PARFILE

指定导出工具要使用的参数文件名.如果经常需要使用EXP工具导出数据,可以将命令行选项放到参数文件中,然后导出时调用该参数文件. 

### 19、QUERY

该选项用于指定WHERE条件子句,从而导出表的部分数据.需要注意,使用直接导出方式时不能指定该选项. 

```
Exp scott/tiger tables=emp query=’WHERE depot=10’ 
```

### 20、RECORDLENGTH

该选项用于指定文件记录的长度,默认值为BUFFER选项值.当需要将导出文件传送到不同OS平台时,可能需要设置该选项.需要注意,该选项的值不能超过64K. 

### 21、RESUMABLE

该选项用于指定是否激活”空间继续分配”特征,默认值为N,为了使用选项RESUMABLE_NAEM和RESUMABLE_TIMEOUT,必须将该选项设置为Y. 

### 22、RESUMABLE_NAME

该选项用于指定”空间继续分配”语句所对应的标识符. 

### 23、RESUMABLE_TIMEOUT

该选项用于指定错误被修正的最大周期(单位:秒),默认值为7200 

### 24、ROWS

该选项用于指定是否导出表行数据,默认值为Y 

### 25、STATISTICS

该选项用于指定导入导出文件时生成优化统计信息的类型.默认值为ESTIMATE. 

### 26、TABLES

该选项用于指定导出表 

### 27、TABLESPACE

该选项用于指定表空间导出模式,使用TABLESPACES选项时,会导出特定表空间上所有表. 

### 28、TRANSPORT_TABLESPACE

该选项用于指定是否导出表空间元数据,默认值为N.当设置为Y时,导出特定表空间的元数据,当设置为N时,不导出表空间的元数据. 

### 29、TRIGGERS

用于指定是否导出触发器,默认为Y 

### 30、TTS_FULL_CHECK

该选项用于指定是否检查被搬移表空间的关联关系,默认值为N 

### 31、USERID

该选项用于指定执行导出操作的用于名,口令和连接字符串.

# imp命令详解

IMP是将OS文件中的对象结构和数据装载到数据库中的过程。

## imp命令选项
```
oracle@GW_8:~> imp help=y  

Import: Release 11.1.0.7.0 - Production on 星期五 2月 1 08:54:04 2012

Copyright (c) 1982, 2007, Oracle.  All rights reserved.



通过输入 IMP 命令和您的用户名/口令, 导入
操作将提示您输入参数: 

     例如: IMP SCOTT/TIGER

或者, 可以通过输入 IMP 命令和各种参数来控制导入
的运行方式。要指定参数, 您可以使用关键字: 

     格式:  IMP KEYWORD=value 或 KEYWORD=(value1,value2,...,valueN)
     例如: IMP SCOTT/TIGER IGNORE=Y TABLES=(EMP,DEPT) FULL=N
               或 TABLES=(T1:P1,T1:P2), 如果 T1 是分区表

USERID 必须是命令行中的第一个参数。

关键字   说明 (默认值)        关键字      说明 (默认值)
--------------------------------------------------------------------------
USERID   用户名/口令           FULL       导入整个文件 (N)
BUFFER   数据缓冲区大小        FROMUSER    所有者用户名列表
FILE     输入文件 (EXPDAT.DMP)  TOUSER     用户名列表
SHOW     只列出文件内容 (N)     TABLES      表名列表
IGNORE   忽略创建错误 (N)    RECORDLENGTH  IO 记录的长度
GRANTS   导入权限 (Y)          INCTYPE     增量导入类型
INDEXES   导入索引 (Y)         COMMIT       提交数组插入 (N)
ROWS     导入数据行 (Y)        PARFILE      参数文件名
LOG     屏幕输出的日志文件    CONSTRAINTS    导入限制 (Y)
DESTROY                覆盖表空间数据文件 (N)
INDEXFILE              将表/索引信息写入指定的文件
SKIP_UNUSABLE_INDEXES  跳过不可用索引的维护 (N)
FEEDBACK               每 x 行显示进度 (0)
TOID_NOVALIDATE        跳过指定类型 ID 的验证 
FILESIZE               每个转储文件的最大大小
STATISTICS             始终导入预计算的统计信息
RESUMABLE              在遇到有关空间的错误时挂起 (N)
RESUMABLE_NAME         用来标识可恢复语句的文本字符串
RESUMABLE_TIMEOUT      RESUMABLE 的等待时间 
COMPILE                编译过程, 程序包和函数 (Y)
STREAMS_CONFIGURATION  导入流的一般元数据 (Y)
STREAMS_INSTANTIATION  导入流实例化元数据 (N)
VOLSIZE                磁带的每个文件卷上的文件的字节数

下列关键字仅用于可传输的表空间
TRANSPORT_TABLESPACE 导入可传输的表空间元数据 (N)
TABLESPACES 将要传输到数据库的表空间
DATAFILES 将要传输到数据库的数据文件
TTS_OWNERS 拥有可传输表空间集中数据的用户
```

IMP命令行与EXP不一样的有: 

### 1、COMMIT 

该选项用于指定每次数据插入完成之后是否提交数据,默认值为N 

### 2、COMPILE 

该选项用于指定导入包,过程和函数时是否进行编译,默认值为Y 

### 3、CONSTRAINTS 

该选项用于指定是否导入表的约束,默认值为Y 

### 4、DATAFILE 

当设置选项TRANSPORT_TABLESPACE为Y时,该选项用于指定要被搬移到目标数据库的数据文件列表. 

```
IMP ‘sys/admin as sysdba ‘ TRANSPORT_TABLESPACE=Y 
DATAFILE=’g:testtools01.dbf’ 
TTS_OWNERS=RMAN FROMUSER=RMAN TOUSER=SYSTEM 
```

### 5、DESTROY

该选项用于指定导入时是否覆盖已存在的数据文件,默认值为N. 

### 6、FROMUSER 

该选项用于指定从导出文件中摘取并导入特定用于的对象. 

### 7、IGNORE 

该选项用于指定是否忽略对象建立错误信息.默认为N 

### 8、INDEXFILE 

该选项用于指定生成存放索引建立语句的文件名称. 

### 9、SHOW 

该选项用于指定显示导出文件的内容,默认为N 

### 10、SKIP_UNUSABLE_INDEXES 

该选项用于指定导入时是否要跳过不可使用的索引,默认值为N 

### 11、STATSTICS 

该选项用于指定导入时数据库优化器要执行的操作.默认值为ALWAYS 

### 12、STREAMS_CONFIGURATION 

该选项用于指定是否导入流元数据(Stream Matadata),默认值为Y 

### 13、TOID_NOVALIDATE 

该选项用于指定导入对象表时要排除校验的对象类型 

### 14、TOUSER 

该选项用于指定将特定方案对象导入到其他用户. 

### 15、TTS_OWNERS 

当设置TRANSPORT_TABLESPACE=Y时,该选项用于列出用于被搬移表空间数据的数据库用户.

# 实践

## 导出一个完整数据库

```
exp system/password file=XX.dmp log=XX.log full=y
```
     
## 导出数据库定义而不导出数据

```
exp system/password file=XX.dmp log=XX.log full=y rows=n
```
      
## 导出一个或一组指定用户所属的全部表、索引和其他对象

```
exp system/sys file=mmsg log=mmsg owner=mmsg 
```
      
## 导出一个或多个指定表

```
exp mmsg/mmsg file=vaspinfo.dmp log= vaspinfo.log tables= vaspinfo 
exp mmsg/mmsg file=tables.dmp log= tables.log tables= vaspinfo,mmscinfo,miscinfo 
```

## 估计导出文件的大小

### 全部表总字节数

```
SELECT sum(bytes) FROM dba_segments WHERE segment_type = 'TABLE';
```

### MMSG用户所属表的总字节数

```
SELECT sum(bytes) FROM dba_segments WHERE owner = 'MMSG'
AND segment_type = 'TABLE';
``` 

### MMSG用户下的aquatic_animal表的字节数

```
SELECT sum(bytes)  FROM dba_segments 
WHERE owner = 'MMSG'
　　AND segment_type = 'TABLE'
　　AND segment_name = 'AQUATIC_ANIMAL';
```
        
## 导出表数据的子集(oracle8i以上)

```
exp mmsg/mmsg@mmsgdb tables=mmscinfo query=\"where mmscid=910000\“
```
        
## 用多个文件分割一个导出文件

```
exp username/passwd 
file=\(paycheck_1.dmp,paycheck_2.dmp,paycheck_3.dmp,paycheck_4.dmp \)
log=XX.log, filesize=[K][M][G] tables=tables_name 
```

操作如下：

```
exp mmsg/mmsg file=\(1.dmp,2.dmp,3.dmp\) log=test.log filesize=25K tables= mmscinfo,miscinfo,vaspinfo,areainfo 
```
        
## 使用参数文件（详见parfile使用方法）

```
exp system/manager parfile=bible_tables.par
   bible_tables.par参数文件：
　#Export the sample tables used for the Oracle8i Database Administrator's Bible.
　file=bible_tables 
　log=bible_tables 
　tables=(
amy.artist 
　amy.books 
　seapark.checkup 
　seapark.items 
　)
```

示例如下：

建立一个parfile文件，命名为svclogbak.par，内容是一些导出参数，如：

```
   file=svclogbak.dmp                   #导出的文件命名
   log=svclogbak.log                    #导出过程中产生的日志信息
   tables=(mmsgsvclog_0122_1_o_0,    #括号中存放要导出的相关表信息，以英文逗号分隔
     mmsgsvclog_0122_1_o_1,
     mmsgsvclog_0122_1_o_2,
     mmsgsvclog_20100122_1_s)         #如有需要，可增加其它参数，这里仅作示例
```
                                   
使用parfile文件，可以在不同的操作系统中执行，即是任何OS平台都适用的方法。

### 导出 

```exp username/passwd@dbname parfile=svclogbak.par ```

### 导入 

```imp username/passwd@dbname fromuser=XXX touser=XXX file=svclogbak.dmp ignore=y commit=y ```

其中:
fromuser ，该选项用于指定从导出文件中摘取并导入特定用于的对象；
touser     该选项用于指定将特定方案对象导入到其他用户。
如果导入导出的用户名一致，可以直接使用如下命令进行导入：
```imp username/passwd@dbname  file=svclogbak.dmp ignore=y  commit=y ```
或者
``` imp username/passwd  file=svclogbak.dmp ignore=y commit=y```

## 增量导出 

“完全”增量导出(complete)，即备份整个数据库 

```exp system/sys inctype=complete file=wangyunzeng_mmsg.dmp ```
　
“增量型”增量导出(incremental)，即备份上一次备份后改变的数据 

```exp system/sys inctype=incremental file= wangyunzeng_mmsg.dmp ```
                               
“累计型”增量导出(cumulative)，即备份上一次“完全”导出之后改变的数据 

```exp system/sys inctype=cumulative file= wangyunzeng_mmsg.dmp ```

注：
* 必须为 SYS 或 SYSTEM 才能执行增量导出 

## 导入一个完整数据库

```
imp system/manager file=bible_db log=dible_db full=y ignore=y
```

## 导入一个或一组指定用户所属的全部表、索引和其他对象

```
imp system/manager file=seapark log=seapark fromuser=seapark 
imp  system/manager file=seapark log=seapark fromuser=\(seapark,amy,amyc,Harold\)
```

## 将一个用户所属的数据导入另一个用户

```
imp system/manager file=tank log=tank fromuser=seapark touser=seapark_copy 
imp system/manager file=tank log=tank fromuser=mmsg touser=wyz 
```

## 导入一个表

```
imp mmsg/mmsg file=mmscinfo.dmp log=mmscinfo.log fromuser=seapark TABLES=mmscinfo 
```

## 从多个文件导入

```
imp system/manager file=\(paycheck_1,paycheck_2,paycheck_3,paycheck_4\) log=paycheck, filesize=1G full=y
```

## 使用参数文件

```
 imp system/manager parfile=bible_tables.parbible_tables.par fromuser=mmsg touser=wyz file=mmscinfo.dmp log=mmscinfo.log commit=y
```

## 增量导入

```
imp system./manager inctype= RECTORE FULL=Y FILE=A
```

# parfile使用方法

建立一个parfile文件，命名为svclogbak.par，内容是一些导出参数，如：

```
file=svclogbak.dmp                  #导出的文件命名
log=svclogbak.log                   #导出过程中产生的日志信息
tables=(mmsgsvclog_0122_1_o_0,      #括号中存放要导出的相关表信息，以英文逗号分隔
mmsgsvclog_0122_1_o_1,
mmsgsvclog_0122_1_o_2,
mmsgsvclog_20100122_1_s)            #如有需要，可增加其它参数，这里仅作示例
```

说明：
* 使用parfile文件，可以在不同的操作系统中执行，即是任何OS平台都适用的方法。

## 导出

```
exp username/passwd@dbname parfile=svclogbak.par
```

## 导入

```
imp username/passwd@dbname fromuser=XXX touser=XXX file=svclogbak.dmp ignore=y commit=y
```

其中:
fromuser  该选项用于指定从导出文件中摘取并导入特定用于的对象；
touser  该选项用于指定将特定方案对象导入到其他用户。

如果导入导出的用户名一致，可以直接使用如下命令进行导入：

```
imp username/passwd@dbname  file=svclogbak.dmp ignore=y  commit=y
```

或者

```
imp username/passwd  file=svclogbak.dmp ignore=y commit=y
```

## 表名获取


通过PLSQL Developer工具获取表名

如果用户安装了PLSQL Developer工具，可以直接在该工具上查询相关的SVC表信息：

（1）按住shift键，选中这些表，按住鼠标拖到右侧新建的SQL窗口

<img class="shadow" src="/img/in-post/oracle-dev-table.png" width="600" />

（2）点击“名称”，在SQL窗口中显示所选中的MMSGSVCLOG_X表的名称：
 
<img class="shadow" src="/img/in-post/oracle-dev-table2.png" width="600" />

（3）拷贝这些表名称，修改svclogbak.par文件

将拷贝的表的名称保存在tables=()中的括号中，并保存svclogbak.par文件；

（4）执行导入操作。

## 查询表，从sqlplus中获取

（1）数据库应用用户登录数据库，查询SVC日志表信息：
```
select * from tab where tname like 'MMSGSVCLOG_%';
```

（2）将查询所得的需要备份的MMSGSVCLOG_X表拷贝到svclogbak.par文件中的tables=()中的括号中，并以英文逗号分隔；

（3）执行导入操作。

# 测试验证

## Parfile文件内容

```
# cat svclogbak.par
file=svclogbak.dmp
log=svclogbak.log
tables=(mmsgsvclog_0122_1_o_0,
mmsgsvclog_0122_1_o_1,
mmsgsvclog_0122_1_o_2,
mmsgsvclog_0122_1_o_3,
mmsgsvclog_0122_1_o_4,
mmsgsvclog_0122_1_o_5,
mmsgsvclog_0122_1_o_6,
mmsgsvclog_0122_1_o_7,
mmsgsvclog_0122_1_o_8,
mmsgsvclog_0122_1_o_9,
mmsgsvclog_0123_1_o_0,
mmsgsvclog_0123_1_o_1,
mmsgsvclog_0123_1_o_2,
mmsgsvclog_0123_1_o_3,
mmsgsvclog_0123_1_o_4,
mmsgsvclog_0123_1_o_5,
mmsgsvclog_0123_1_o_6,
mmsgsvclog_0123_1_o_7,
mmsgsvclog_0123_1_o_8,
mmsgsvclog_0123_1_o_9,
mmsgsvclog_0124_1_o_0,
mmsgsvclog_0124_1_o_1,
mmsgsvclog_0124_1_o_2,
mmsgsvclog_0124_1_o_3,
mmsgsvclog_0124_1_o_4,
mmsgsvclog_0124_1_o_5,
mmsgsvclog_0124_1_o_6,
mmsgsvclog_0124_1_o_7,
mmsgsvclog_0124_1_o_8,
mmsgsvclog_0124_1_o_9,
mmsgsvclog_0124_2_o_0,
mmsgsvclog_0124_2_o_4,
mmsgsvclog_0124_2_o_5,
mmsgsvclog_0124_2_o_6,
mmsgsvclog_0124_2_o_7,
mmsgsvclog_0124_2_o_8,
mmsgsvclog_0124_2_o_9,
mmsgsvclog_0125_1_o_0,
mmsgsvclog_0125_1_o_1,
mmsgsvclog_0125_1_o_2,
mmsgsvclog_0125_1_o_3,
mmsgsvclog_0125_1_o_4,
mmsgsvclog_0125_1_o_5,
mmsgsvclog_0125_1_o_6,
mmsgsvclog_0125_1_o_7,
mmsgsvclog_0125_1_o_8,
mmsgsvclog_0125_1_o_9,
mmsgsvclog_0126_1_o_0,
mmsgsvclog_0126_1_o_1,
mmsgsvclog_0126_1_o_2,
mmsgsvclog_0126_1_o_3,
mmsgsvclog_0126_1_o_4,
mmsgsvclog_0126_1_o_5,
mmsgsvclog_0126_1_o_6,
mmsgsvclog_0126_1_o_7,
mmsgsvclog_0126_1_o_8,
mmsgsvclog_0126_1_o_9,
mmsgsvclog_0127_1_o_0,
mmsgsvclog_0127_1_o_1,
mmsgsvclog_0127_1_o_2,
mmsgsvclog_0127_1_o_3,
mmsgsvclog_0127_1_o_4,
mmsgsvclog_0127_1_o_5,
mmsgsvclog_0127_1_o_6,
mmsgsvclog_0127_1_o_7,
mmsgsvclog_0127_1_o_8,
mmsgsvclog_0127_1_o_9,
mmsgsvclog_0128_1_o_3,
mmsgsvclog_0128_1_o_4,
mmsgsvclog_20100122_1_s,
mmsgsvclog_20100123_1_s,
mmsgsvclog_20100124_1_s,
mmsgsvclog_20100124_2_s,
mmsgsvclog_20100125_1_s,
mmsgsvclog_20100126_1_s,
mmsgsvclog_20100127_1_s,
mmsgsvclog_20100128_1_s)
```

## 导出

```
129 node1 [yjh] :/home/yjh/>exp yjh/yjh@mmsgdb parfile=svclogbak.par

Export: Release 11.1.0.7.0 - Production on Thu Jan 28 15:35:11 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
Export done in ZHS16GBK character set and UTF8 NCHAR character set

About to export specified tables via Conventional Path ...
. . exporting table          MMSGSVCLOG_0122_1_O_0        670 rows exported
……………………………………….. ………………………………………..中间数据省略 ……………………………………….. ………………………………………..
. . exporting table        MMSGSVCLOG_20100128_1_S        130 rows exported
Export terminated successfully without warnings.
```

## 文件信息

```
130 node1 [yjh] :/home/yjh/>ll
总计 150740
-rw-r--r--  1 yjh users  15056896 2010-01-28 15:35 svclogbak.dmp  #导出的文件名称
-rw-r--r--  1 yjh users      7186 2010-01-28 15:35 svclogbak.log   #导出过程中产生的日志
-rw-r--r--  1 yjh users      2156 2010-01-28 14:29 svclogbak.par
```

## 导入

```
155 node1 [mmsg] :/home/mmsg>imp mmsg/mmsg fromuser=yjh touser=mmsg file=svclogbak.dmp ignore=y commit=y

Import: Release 11.1.0.7.0 - Production on Thu Jan 28 15:37:55 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

Export file created by EXPORT:V11.01.00 via conventional path

Warning: the objects were exported by YJH, not by you

import done in ZHS16GBK character set and UTF8 NCHAR character set
. importing YJH's objects into MMSG
. . importing table        "MMSGSVCLOG_0122_1_O_0"        670 rows imported
……………………………………….. ………………………………………..中间数据省略 ……………………………………….. ………………………………………..
. . importing table      "MMSGSVCLOG_20100128_1_S"        122 rows imported
Import terminated successfully without warnings.
```

## 数据库全表导出

### 脚本

#### fullback_system.sh

```
#!/bin/sh

#定义备份时间
backupdate=`date +'%Y%m%d_%H%M%S'`

#定义备份路径
BakPath=/opt/oracle/oracle_table_bak

if [ ! -d $ORACLE_BASE/oracle_table_bak ];then
 mkdir -p $ORACLE_BASE/oracle_table_bak
fi

# 定义oracle用户名和密码
ACCOUNT=system     #用户名称
PASSWORD=sys       #用户密码
SID=mmsgdb         #数据库别名
echo "Please input user name,password and SID to connect to oracle"
#读入用户名
echo "username( system)"
read U_INPUT
if [ "x$U_INPUT" != "x" ]; then
    ACCOUNT=$U_INPUT
fi

#读入密码
echo "password( sys)"
read U_INPUT
if [ "x$U_INPUT" != "x" ]; then
    PASSWORD=$U_INPUT
fi

#读入SID
echo "SID( mmsgdb)"
read U_INPUT
if [ "x$U_INPUT" != "x" ]; then
    SID=$U_INPUT
fi

#系统所在路径
APPHOME=`dirname $0`
if [ $APPHOME = "." ]; then
   APPHOME=`pwd`
fi
cd $APPHOME

#执行导出操作
exp $ACCOUNT/$PASSWORD@$SID file=${ORACLE_BASE}/oracle_table_bak/fullbak_$backupdate.dmp  log=${ORACLE_BASE}/oracle_table_bak/fullbak_$backupdate.log full=y
```

### 导出过程日志

```

连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
已导出 ZHS16GBK 字符集和 UTF8 NCHAR 字符集

即将导出整个数据库...
. 正在导出表空间定义
. 正在导出概要文件
. 正在导出用户定义
. 正在导出角色
. 正在导出资源成本
. 正在导出回退段定义
. 正在导出数据库链接
. 正在导出序号
. 正在导出目录别名
. 正在导出上下文名称空间
. 正在导出外部函数库名
. 导出 PUBLIC 类型同义词
. 正在导出专用类型同义词
. 正在导出对象类型定义
. 正在导出系统过程对象和操作
. 正在导出 pre-schema 过程对象和操作
. 正在导出簇定义
. 即将导出 SYSTEM 的表通过常规路径...
. . 正在导出表                     DEF$_AQCALL导出了           0 行
. . 正在导出表                    DEF$_AQERROR导出了           0 行
. . 正在导出表                   DEF$_CALLDEST导出了           0 行
. . 正在导出表                DEF$_DEFAULTDEST导出了           0 行
. . 正在导出表                DEF$_DESTINATION导出了           0 行
. . 正在导出表                      DEF$_ERROR导出了           0 行
. . 正在导出表                        DEF$_LOB导出了           0 行
. . 正在导出表                     DEF$_ORIGIN导出了           0 行
. . 正在导出表                 DEF$_PROPAGATOR导出了           0 行
. . 正在导出表        DEF$_PUSHED_TRANSACTIONS导出了           0 行
. . 正在导出表                   DEF$_TEMP$LOB导出了           0 行
. . 正在导出表                             OL$
. . 正在导出表                        OL$HINTS
. . 正在导出表                        OL$NODES
. . 正在导出表            QUEST_SOO_AT_APPNAME导出了           0 行
. . 正在导出表     QUEST_SOO_AT_EXECUTION_PLAN导出了           0 行
. . 正在导出表         QUEST_SOO_AT_OPERATIONS导出了           0 行
. . 正在导出表       QUEST_SOO_AT_PARSE_CURSOR导出了           0 行
. . 正在导出表        QUEST_SOO_AT_PARSE_ERROR导出了           0 行
. . 正在导出表        QUEST_SOO_AT_PARSE_WAITS导出了           0 行
. . 正在导出表         QUEST_SOO_AT_SESSION_ID导出了           0 行
. . 正在导出表          QUEST_SOO_AT_SQL_BINDS导出了           0 行
. . 正在导出表     QUEST_SOO_AT_SQL_EXECUTIONS导出了           0 行
. . 正在导出表     QUEST_SOO_AT_SQL_EXEC_ERROR导出了           0 行
. . 正在导出表          QUEST_SOO_AT_SQL_FETCH导出了           0 行
. . 正在导出表      QUEST_SOO_AT_SQL_STATEMENT导出了           0 行
. . 正在导出表    QUEST_SOO_AT_SQL_STMT_PIECES导出了           0 行
. . 正在导出表          QUEST_SOO_AT_SQL_WAITS导出了           0 行
. . 正在导出表         QUEST_SOO_AT_TRACE_FILE导出了           0 行
. . 正在导出表         QUEST_SOO_AT_WAIT_NAMES导出了           0 行
. . 正在导出表           QUEST_SOO_BUFFER_BUSY导出了           0 行
. . 正在导出表      QUEST_SOO_EVENT_CATEGORIES导出了        1445 行
. . 正在导出表             QUEST_SOO_LOCK_TREE导出了           0 行
. . 正在导出表      QUEST_SOO_PARSE_TIME_TRACK导出了           1 行
. . 正在导出表            QUEST_SOO_PLAN_TABLE导出了           0 行
. . 正在导出表        QUEST_SOO_SB_BUFFER_BUSY导出了           0 行
. . 正在导出表              QUEST_SOO_SB_EVENT导出了           0 行
. . 正在导出表            QUEST_SOO_SB_IO_STAT导出了           0 行
. . 正在导出表       QUEST_SOO_SCHEMA_VERSIONS导出了           1 行
. . 正在导出表               QUEST_SOO_VERSION导出了           1 行
. . 正在导出表         REPCAT$_AUDIT_ATTRIBUTE导出了           2 行
. . 正在导出表            REPCAT$_AUDIT_COLUMN导出了           0 行
. . 正在导出表            REPCAT$_COLUMN_GROUP导出了           0 行
. . 正在导出表                REPCAT$_CONFLICT导出了           0 行
. . 正在导出表                     REPCAT$_DDL导出了           0 行
. . 正在导出表              REPCAT$_EXCEPTIONS导出了           0 行
. . 正在导出表               REPCAT$_EXTENSION导出了           0 行
. . 正在导出表                 REPCAT$_FLAVORS导出了           0 行
. . 正在导出表          REPCAT$_FLAVOR_OBJECTS导出了           0 行
. . 正在导出表               REPCAT$_GENERATED导出了           0 行
. . 正在导出表          REPCAT$_GROUPED_COLUMN导出了           0 行
. . 正在导出表       REPCAT$_INSTANTIATION_DDL导出了           0 行
. . 正在导出表             REPCAT$_KEY_COLUMNS导出了           0 行
. . 正在导出表            REPCAT$_OBJECT_PARMS导出了           0 行
. . 正在导出表            REPCAT$_OBJECT_TYPES导出了          28 行
. . 正在导出表        REPCAT$_PARAMETER_COLUMN导出了           0 行
. . 正在导出表                REPCAT$_PRIORITY导出了           0 行
. . 正在导出表          REPCAT$_PRIORITY_GROUP导出了           0 行
. . 正在导出表       REPCAT$_REFRESH_TEMPLATES导出了           0 行
. . 正在导出表                  REPCAT$_REPCAT导出了           0 行
. . 正在导出表               REPCAT$_REPCATLOG导出了           0 行
. . 正在导出表               REPCAT$_REPCOLUMN导出了           0 行
. . 正在导出表          REPCAT$_REPGROUP_PRIVS导出了           0 行
. . 正在导出表               REPCAT$_REPOBJECT导出了           0 行
. . 正在导出表                 REPCAT$_REPPROP导出了           0 行
. . 正在导出表               REPCAT$_REPSCHEMA导出了           0 行
. . 正在导出表              REPCAT$_RESOLUTION导出了           0 行
. . 正在导出表       REPCAT$_RESOLUTION_METHOD导出了          19 行
. . 正在导出表   REPCAT$_RESOLUTION_STATISTICS导出了           0 行
. . 正在导出表     REPCAT$_RESOL_STATS_CONTROL导出了           0 行
. . 正在导出表           REPCAT$_RUNTIME_PARMS导出了           0 行
. . 正在导出表               REPCAT$_SITES_NEW导出了           0 行
. . 正在导出表            REPCAT$_SITE_OBJECTS导出了           0 行
. . 正在导出表               REPCAT$_SNAPGROUP导出了           0 行
. . 正在导出表        REPCAT$_TEMPLATE_OBJECTS导出了           0 行
. . 正在导出表          REPCAT$_TEMPLATE_PARMS导出了           0 行
. . 正在导出表      REPCAT$_TEMPLATE_REFGROUPS导出了           0 行
. . 正在导出表          REPCAT$_TEMPLATE_SITES导出了           0 行
. . 正在导出表         REPCAT$_TEMPLATE_STATUS导出了           3 行
. . 正在导出表        REPCAT$_TEMPLATE_TARGETS导出了           0 行
. . 正在导出表          REPCAT$_TEMPLATE_TYPES导出了           2 行
. . 正在导出表     REPCAT$_USER_AUTHORIZATIONS导出了           0 行
. . 正在导出表        REPCAT$_USER_PARM_VALUES导出了           0 行
. . 正在导出表         SQLPLUS_PRODUCT_PROFILE导出了           0 行
. 即将导出 OUTLN 的表通过常规路径...
. . 正在导出表                             OL$导出了           0 行
. . 正在导出表                        OL$HINTS导出了           0 行
. . 正在导出表                        OL$NODES导出了           0 行
. 即将导出 TSMSYS 的表通过常规路径...
. . 正在导出表                            SRS$导出了           0 行
. 即将导出 MMSG 的表通过常规路径...
. . 正在导出表                        AREAINFO导出了         374 行
. . 正在导出表                      AREANUMBER导出了         364 行
. . 正在导出表                AREANUMBERPREFIX导出了           2 行
. . 正在导出表                 BEARERVALUELIST导出了           3 行
. . 正在导出表                     CARRIERINFO导出了           1 行
. . 正在导出表                CHARGINGKPCONFIG导出了          28 行
. . 正在导出表                  CONNECTIONINFO导出了           0 行
. . 正在导出表                     COUNTRYCODE导出了          21 行
. . 正在导出表              DATAFILESTATUSCODE导出了           0 行
. . 正在导出表                DETAILSTATUSCODE导出了         247 行
. . 正在导出表                      DNSSRVINFO导出了           0 行
. . 正在导出表                   DRMACCESSCODE导出了           0 行
. . 正在导出表                      ECTOSIINFO导出了           0 行
. . 正在导出表                     ENUMSRVINFO导出了           1 行
. . 正在导出表                   EXP_CACHESTAT导出了           4 行
. . 正在导出表                     HISTORYFLOW导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100319导出了         158 行
. . 正在导出表       INTERFACEACCOUNT_20100320导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100321导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100322导出了          60 行
. . 正在导出表       INTERFACEACCOUNT_20100323导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100324导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100325导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100326导出了         270 行
. . 正在导出表       INTERFACEACCOUNT_20100327导出了         421 行
. . 正在导出表       INTERFACEACCOUNT_20100328导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100329导出了           0 行
. . 正在导出表                     INTERPREFIX导出了          21 行
. . 正在导出表                IPRANGEPARTITION导出了          93 行
. . 正在导出表                         MESSAGE导出了           0 行
. . 正在导出表                MESSAGEREFERENCE导出了           0 行
. . 正在导出表             MESSAGESENDSCHEDULE导出了          15 行
. . 正在导出表                      MIBLEAFINT导出了          79 行
. . 正在导出表                      MIBLEAFSTR导出了           8 行
. . 正在导出表                        MISCINFO导出了           2 行
. . 正在导出表                 MISCROUTERTABLE导出了           7 行
. . 正在导出表                       MMBOXTYPE导出了           5 行
. . 正在导出表            MMINTERFACELEVELINFO导出了           2 行
. . 正在导出表                        MMSCINFO导出了           2 行
. . 正在导出表                      MMSCIPINFO导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP00导出了          30 行
. . 正在导出表              MMSGMMSCMSGIDMAP01导出了          25 行
. . 正在导出表              MMSGMMSCMSGIDMAP02导出了          35 行
. . 正在导出表              MMSGMMSCMSGIDMAP03导出了          27 行
. . 正在导出表              MMSGMMSCMSGIDMAP04导出了          29 行
. . 正在导出表              MMSGMMSCMSGIDMAP05导出了          35 行
. . 正在导出表              MMSGMMSCMSGIDMAP06导出了          29 行
. . 正在导出表              MMSGMMSCMSGIDMAP07导出了          48 行
. . 正在导出表              MMSGMMSCMSGIDMAP08导出了          16 行
. . 正在导出表              MMSGMMSCMSGIDMAP09导出了          30 行
. . 正在导出表              MMSGMMSCMSGIDMAP10导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP11导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP12导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP13导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP14导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP15导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP16导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP17导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP18导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP19导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP20导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP21导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP22导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP23导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP24导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP25导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP26导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP27导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP28导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP29导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP30导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP31导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP32导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP33导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP34导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP35导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP36导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP37导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP38导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP39导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP40导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP41导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP42导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP43导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP44导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP45导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP46导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP47导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP48导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP49导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP50导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP51导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP52导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP53导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP54导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP55导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP56导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP57导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP58导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP59导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP60导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP61导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP62导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP63导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP64导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP65导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP66导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP67导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP68导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP69导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP70导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP71导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP72导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP73导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP74导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP75导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP76导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP77导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP78导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP79导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP80导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP81导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP82导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP83导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP84导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP85导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP86导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP87导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP88导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP89导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP90导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP91导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP92导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP93导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP94导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP95导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP96导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP97导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP98导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP99导出了           0 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_0导出了          55 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_1导出了          37 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_2导出了          20 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_3导出了          34 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_4导出了          41 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_5导出了          70 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_6导出了          18 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_7导出了          51 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_8导出了          32 行
. . 正在导出表           MMSGSVCLOG_0319_1_O_9导出了          35 行
. . 正在导出表           MMSGSVCLOG_0322_1_O_0导出了          25 行
. . 正在导出表           MMSGSVCLOG_0322_1_O_1导出了          11 行
. . 正在导出表           MMSGSVCLOG_0322_1_O_2导出了          17 行
. . 正在导出表           MMSGSVCLOG_0322_1_O_3导出了          13 行
. . 正在导出表           MMSGSVCLOG_0322_1_O_5导出了           9 行
. . 正在导出表           MMSGSVCLOG_0322_1_O_6导出了          30 行
. . 正在导出表           MMSGSVCLOG_0322_1_O_9导出了          16 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_0导出了         903 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_1导出了        1106 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_2导出了        1206 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_3导出了        1173 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_4导出了        1276 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_5导出了        1075 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_6导出了        1178 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_7导出了         981 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_8导出了         974 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_9导出了         781 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_0导出了        2203 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_1导出了        2165 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_2导出了        2334 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_3导出了        2102 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_4导出了        2118 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_5导出了        2256 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_6导出了        2253 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_7导出了        2556 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_8导出了        2443 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_9导出了        2660 行
. . 正在导出表         MMSGSVCLOG_20100319_1_S导出了          91 行
. . 正在导出表         MMSGSVCLOG_20100322_1_S导出了          28 行
. . 正在导出表         MMSGSVCLOG_20100326_1_S导出了        1328 行
. . 正在导出表         MMSGSVCLOG_20100327_1_S导出了        3168 行
. . 正在导出表                       MMSTARIFF导出了           1 行
. . 正在导出表                       MODULECMD导出了          18 行
. . 正在导出表                         MODULES导出了          17 行
. . 正在导出表                  MONITOREDUSERS导出了           0 行
. . 正在导出表                 MONITORPERFSTAT导出了          12 行
. . 正在导出表                MONTHORDERINFO_0导出了           0 行
. . 正在导出表                MONTHORDERINFO_1导出了           0 行
. . 正在导出表                MONTHORDERINFO_2导出了           0 行
. . 正在导出表                MONTHORDERINFO_3导出了           0 行
. . 正在导出表                MONTHORDERINFO_4导出了           0 行
. . 正在导出表                MONTHORDERINFO_5导出了           0 行
. . 正在导出表                MONTHORDERINFO_6导出了           0 行
. . 正在导出表                MONTHORDERINFO_7导出了           0 行
. . 正在导出表                MONTHORDERINFO_8导出了           0 行
. . 正在导出表                MONTHORDERINFO_9导出了           0 行
. . 正在导出表                    NATIVEPREFIX导出了           1 行
. . 正在导出表                     NETWORKCODE导出了          24 行
. . 正在导出表               PORTALLOG20100322导出了          10 行
. . 正在导出表               PORTALLOG20100325导出了          20 行
. . 正在导出表               PORTALLOG20100326导出了         166 行
. . 正在导出表               PORTALLOG20100327导出了          84 行
. . 正在导出表               PORTALLOG20100329导出了           4 行
. . 正在导出表                 PPSNUMBERPREFIX导出了           0 行
. . 正在导出表                 PROHIBITEDRIGHT导出了           0 行
. . 正在导出表                    REALTIMEFLOW导出了           0 行
. . 正在导出表                   RENTALFEEINFO导出了           1 行
. . 正在导出表                       RIGHTINFO导出了         249 行
. . 正在导出表                            ROLE导出了           4 行
. . 正在导出表                    ROLEMAPRIGHT导出了         518 行
. . 正在导出表                     ROUTERTABLE导出了           5 行
. . 正在导出表                  RPT_BUSYSERVER导出了         240 行
. . 正在导出表                   RPT_DELAYTIME导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100319导出了          41 行
. . 正在导出表          RPT_DELAYTIME_20100320导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100321导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100322导出了          13 行
. . 正在导出表          RPT_DELAYTIME_20100323导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100324导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100325导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100326导出了          91 行
. . 正在导出表          RPT_DELAYTIME_20100327导出了         151 行
. . 正在导出表          RPT_DELAYTIME_20100328导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100329导出了           0 行
. . 正在导出表                   RPT_INTERFACE导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100319导出了          79 行
. . 正在导出表          RPT_INTERFACE_20100320导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100321导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100322导出了          31 行
. . 正在导出表          RPT_INTERFACE_20100323导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100324导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100325导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100326导出了         117 行
. . 正在导出表          RPT_INTERFACE_20100327导出了         259 行
. . 正在导出表          RPT_INTERFACE_20100328导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100329导出了           0 行
. . 正在导出表                RPT_MM7_VASPSUCC导出了          46 行
. . 正在导出表                    RPT_MMSCSUCC导出了          28 行
. . 正在导出表               RPT_MMSC_20100319导出了           0 行
. . 正在导出表               RPT_MMSC_20100320导出了           0 行
. . 正在导出表               RPT_MMSC_20100321导出了           0 行
. . 正在导出表               RPT_MMSC_20100322导出了           0 行
. . 正在导出表               RPT_MMSC_20100323导出了           0 行
. . 正在导出表               RPT_MMSC_20100324导出了           0 行
. . 正在导出表               RPT_MMSC_20100325导出了           0 行
. . 正在导出表               RPT_MMSC_20100326导出了           0 行
. . 正在导出表               RPT_MMSC_20100327导出了           0 行
. . 正在导出表               RPT_MMSC_20100328导出了           0 行
. . 正在导出表               RPT_MMSC_20100329导出了           0 行
. . 正在导出表               RPT_TERMINALCOUNT导出了           0 行
. . 正在导出表                    RPT_USECOUNT导出了           0 行
. . 正在导出表               RPT_USEOFSPSERVER导出了           0 行
. . 正在导出表               RPT_VASP_20100319导出了           0 行
. . 正在导出表               RPT_VASP_20100320导出了           0 行
. . 正在导出表               RPT_VASP_20100321导出了           0 行
. . 正在导出表               RPT_VASP_20100322导出了           0 行
. . 正在导出表               RPT_VASP_20100323导出了           0 行
. . 正在导出表               RPT_VASP_20100324导出了           0 行
. . 正在导出表               RPT_VASP_20100325导出了           0 行
. . 正在导出表               RPT_VASP_20100326导出了           0 行
. . 正在导出表               RPT_VASP_20100327导出了           0 行
. . 正在导出表               RPT_VASP_20100328导出了           0 行
. . 正在导出表               RPT_VASP_20100329导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100319导出了          81 行
. . 正在导出表         SERVICEACCOUNT_20100320导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100321导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100322导出了          16 行
. . 正在导出表         SERVICEACCOUNT_20100323导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100324导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100325导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100326导出了         170 行
. . 正在导出表         SERVICEACCOUNT_20100327导出了         268 行
. . 正在导出表         SERVICEACCOUNT_20100328导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100329导出了           0 行
. . 正在导出表                          SIINFO导出了           0 行
. . 正在导出表                     SMSNOTEINFO导出了           4 行
. . 正在导出表               SMSPROTOCOLCONFIG导出了           0 行
. . 正在导出表                 SPECIALCUSTINFO导出了           0 行
. . 正在导出表                   SUBMITRESINFO导出了         128 行
. . 正在导出表                     SYSOPERATOR导出了          13 行
. . 正在导出表                 SYSTEMPARAMETER导出了         335 行
. . 正在导出表                 SZXNUMBERPREFIX导出了           0 行
. . 正在导出表               TERMINALBLACKLIST导出了           2 行
. . 正在导出表               TMP_ATTACH_RESULT导出了           0 行
. . 正在导出表                 TMP_BASE_RESULT导出了           0 行
. . 正在导出表                      TMP_RESULT导出了           0 行
. . 正在导出表                    TMP_RESULTID导出了           0 行
. . 正在导出表                   TMP_RESULTMEM导出了           0 行
. . 正在导出表                    TRACEMSGINFO导出了           0 行
. . 正在导出表                       UAPROFILE导出了           2 行
. . 正在导出表                        VASPINFO导出了          13 行
. . 正在导出表                   VASPLEVELINFO导出了           2 行
. . 正在导出表                VASPPRIORITYINFO导出了           5 行
. . 正在导出表                 VASPRIORITYINFO导出了           5 行
. . 正在导出表                 VASPSERVICE_SUP导出了          15 行
. . 正在导出表               VASSERVEDAREALIST导出了           1 行
. . 正在导出表                VASSUBSCRIBEINFO导出了           0 行
. . 正在导出表               VCARRIERNBRPREFIX导出了           5 行
. . 正在导出表              VIRTUALCARRIERINFO导出了           1 行
. . 正在导出表             VIRTUALCARRIERLEVEL导出了           1 行
. . 正在导出表                     VPNCORP_100导出了           3 行
. . 正在导出表                     VPNCORP_300导出了           3 行
. . 正在导出表                   VPNSUBSCRIBER导出了           6 行
. . 正在导出表                  VPNUNITECORPID导出了           1 行
. 即将导出 YJH 的表通过常规路径...
. . 正在导出表                        AREAINFO导出了         374 行
. . 正在导出表                      AREANUMBER导出了         364 行
. . 正在导出表                AREANUMBERPREFIX导出了           2 行
. . 正在导出表                 BEARERVALUELIST导出了           3 行
. . 正在导出表                     CARRIERINFO导出了           1 行
. . 正在导出表                CHARGINGKPCONFIG导出了          28 行
. . 正在导出表                  CONNECTIONINFO导出了           0 行
. . 正在导出表                     COUNTRYCODE导出了          21 行
. . 正在导出表              DATAFILESTATUSCODE导出了           0 行
. . 正在导出表                DETAILSTATUSCODE导出了         247 行
. . 正在导出表                      DNSSRVINFO导出了           0 行
. . 正在导出表                   DRMACCESSCODE导出了           0 行
. . 正在导出表                      ECTOSIINFO导出了           0 行
. . 正在导出表                     ENUMSRVINFO导出了           1 行
. . 正在导出表                   EXP_CACHESTAT导出了           0 行
. . 正在导出表                     HISTORYFLOW导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100322导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100323导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100324导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100326导出了          20 行
. . 正在导出表       INTERFACEACCOUNT_20100327导出了         135 行
. . 正在导出表       INTERFACEACCOUNT_20100328导出了           0 行
. . 正在导出表       INTERFACEACCOUNT_20100329导出了           0 行
. . 正在导出表                     INTERPREFIX导出了          21 行
. . 正在导出表                IPRANGEPARTITION导出了          93 行
. . 正在导出表                         MESSAGE导出了           0 行
. . 正在导出表                MESSAGEREFERENCE导出了           0 行
. . 正在导出表             MESSAGESENDSCHEDULE导出了          15 行
. . 正在导出表                      MIBLEAFINT导出了          79 行
. . 正在导出表                      MIBLEAFSTR导出了           9 行
. . 正在导出表                        MISCINFO导出了           2 行
. . 正在导出表                 MISCROUTERTABLE导出了           9 行
. . 正在导出表                       MMBOXTYPE导出了           5 行
. . 正在导出表            MMINTERFACELEVELINFO导出了           2 行
. . 正在导出表                        MMSCINFO导出了           2 行
. . 正在导出表                      MMSCIPINFO导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP00导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP01导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP02导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP03导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP04导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP05导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP06导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP07导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP08导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP09导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP10导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP11导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP12导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP13导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP14导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP15导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP16导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP17导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP18导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP19导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP20导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP21导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP22导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP23导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP24导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP25导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP26导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP27导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP28导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP29导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP30导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP31导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP32导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP33导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP34导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP35导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP36导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP37导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP38导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP39导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP40导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP41导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP42导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP43导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP44导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP45导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP46导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP47导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP48导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP49导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP50导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP51导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP52导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP53导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP54导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP55导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP56导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP57导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP58导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP59导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP60导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP61导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP62导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP63导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP64导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP65导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP66导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP67导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP68导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP69导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP70导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP71导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP72导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP73导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP74导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP75导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP76导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP77导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP78导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP79导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP80导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP81导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP82导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP83导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP84导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP85导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP86导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP87导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP88导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP89导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP90导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP91导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP92导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP93导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP94导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP95导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP96导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP97导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP98导出了           0 行
. . 正在导出表              MMSGMMSCMSGIDMAP99导出了           0 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_0导出了           5 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_1导出了          10 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_3导出了           9 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_5导出了           9 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_7导出了           5 行
. . 正在导出表           MMSGSVCLOG_0326_1_O_8导出了           5 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_0导出了          56 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_1导出了          47 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_2导出了          30 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_3导出了          65 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_4导出了          10 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_5导出了          24 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_6导出了          48 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_7导出了          30 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_8导出了          76 行
. . 正在导出表           MMSGSVCLOG_0327_1_O_9导出了          96 行
. . 正在导出表         MMSGSVCLOG_20100326_1_S导出了           7 行
. . 正在导出表         MMSGSVCLOG_20100327_1_S导出了          82 行
. . 正在导出表                       MMSTARIFF导出了           1 行
. . 正在导出表                       MODULECMD导出了          18 行
. . 正在导出表                         MODULES导出了          17 行
. . 正在导出表                  MONITOREDUSERS导出了           0 行
. . 正在导出表                 MONITORPERFSTAT导出了           0 行
. . 正在导出表                MONTHORDERINFO_0导出了           0 行
. . 正在导出表                MONTHORDERINFO_1导出了           0 行
. . 正在导出表                MONTHORDERINFO_2导出了           0 行
. . 正在导出表                MONTHORDERINFO_3导出了           0 行
. . 正在导出表                MONTHORDERINFO_4导出了           0 行
. . 正在导出表                MONTHORDERINFO_5导出了           0 行
. . 正在导出表                MONTHORDERINFO_6导出了           0 行
. . 正在导出表                MONTHORDERINFO_7导出了           0 行
. . 正在导出表                MONTHORDERINFO_8导出了           0 行
. . 正在导出表                MONTHORDERINFO_9导出了           0 行
. . 正在导出表                    NATIVEPREFIX导出了           1 行
. . 正在导出表                     NETWORKCODE导出了          24 行
. . 正在导出表               PORTALLOG20100322导出了          10 行
. . 正在导出表               PORTALLOG20100326导出了          10 行
. . 正在导出表               PORTALLOG20100327导出了          52 行
. . 正在导出表                 PPSNUMBERPREFIX导出了           0 行
. . 正在导出表                 PROHIBITEDRIGHT导出了           0 行
. . 正在导出表                    REALTIMEFLOW导出了           0 行
. . 正在导出表                   RENTALFEEINFO导出了           1 行
. . 正在导出表                       RIGHTINFO导出了         249 行
. . 正在导出表                            ROLE导出了           4 行
. . 正在导出表                    ROLEMAPRIGHT导出了         518 行
. . 正在导出表                     ROUTERTABLE导出了           5 行
. . 正在导出表                  RPT_BUSYSERVER导出了          67 行
. . 正在导出表                   RPT_DELAYTIME导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100322导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100323导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100324导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100326导出了           5 行
. . 正在导出表          RPT_DELAYTIME_20100327导出了          33 行
. . 正在导出表          RPT_DELAYTIME_20100328导出了           0 行
. . 正在导出表          RPT_DELAYTIME_20100329导出了           0 行
. . 正在导出表                   RPT_INTERFACE导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100322导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100323导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100324导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100326导出了           6 行
. . 正在导出表          RPT_INTERFACE_20100327导出了          85 行
. . 正在导出表          RPT_INTERFACE_20100328导出了           0 行
. . 正在导出表          RPT_INTERFACE_20100329导出了           0 行
. . 正在导出表                RPT_MM7_VASPSUCC导出了           8 行
. . 正在导出表                    RPT_MMSCSUCC导出了           6 行
. . 正在导出表               RPT_MMSC_20100322导出了           0 行
. . 正在导出表               RPT_MMSC_20100323导出了           0 行
. . 正在导出表               RPT_MMSC_20100324导出了           0 行
. . 正在导出表               RPT_MMSC_20100326导出了           0 行
. . 正在导出表               RPT_MMSC_20100327导出了           0 行
. . 正在导出表               RPT_MMSC_20100328导出了           0 行
. . 正在导出表               RPT_MMSC_20100329导出了           0 行
. . 正在导出表               RPT_TERMINALCOUNT导出了           0 行
. . 正在导出表                    RPT_USECOUNT导出了           0 行
. . 正在导出表               RPT_USEOFSPSERVER导出了           0 行
. . 正在导出表               RPT_VASP_20100322导出了           0 行
. . 正在导出表               RPT_VASP_20100323导出了           0 行
. . 正在导出表               RPT_VASP_20100324导出了           0 行
. . 正在导出表               RPT_VASP_20100326导出了           0 行
. . 正在导出表               RPT_VASP_20100327导出了           0 行
. . 正在导出表               RPT_VASP_20100328导出了           0 行
. . 正在导出表               RPT_VASP_20100329导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100322导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100323导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100324导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100326导出了           5 行
. . 正在导出表         SERVICEACCOUNT_20100327导出了          44 行
. . 正在导出表         SERVICEACCOUNT_20100328导出了           0 行
. . 正在导出表         SERVICEACCOUNT_20100329导出了           0 行
. . 正在导出表                          SIINFO导出了           0 行
. . 正在导出表                     SMSNOTEINFO导出了           4 行
. . 正在导出表               SMSPROTOCOLCONFIG导出了           0 行
. . 正在导出表                 SPECIALCUSTINFO导出了           0 行
. . 正在导出表                   SUBMITRESINFO导出了         128 行
. . 正在导出表                     SYSOPERATOR导出了          13 行
. . 正在导出表                 SYSTEMPARAMETER导出了         335 行
. . 正在导出表                 SZXNUMBERPREFIX导出了           0 行
. . 正在导出表               TERMINALBLACKLIST导出了           2 行
. . 正在导出表               TMP_ATTACH_RESULT导出了           0 行
. . 正在导出表                 TMP_BASE_RESULT导出了           0 行
. . 正在导出表                      TMP_RESULT导出了           0 行
. . 正在导出表                    TMP_RESULTID导出了           0 行
. . 正在导出表                   TMP_RESULTMEM导出了           0 行
. . 正在导出表                    TRACEMSGINFO导出了           0 行
. . 正在导出表                       UAPROFILE导出了           2 行
. . 正在导出表                        VASPINFO导出了          13 行
. . 正在导出表                   VASPLEVELINFO导出了           2 行
. . 正在导出表                VASPPRIORITYINFO导出了           5 行
. . 正在导出表                 VASPRIORITYINFO导出了           5 行
. . 正在导出表                 VASPSERVICE_SUP导出了          15 行
. . 正在导出表               VASSERVEDAREALIST导出了           1 行
. . 正在导出表                VASSUBSCRIBEINFO导出了           0 行
. . 正在导出表               VCARRIERNBRPREFIX导出了           5 行
. . 正在导出表              VIRTUALCARRIERINFO导出了           1 行
. . 正在导出表             VIRTUALCARRIERLEVEL导出了           1 行
. . 正在导出表                     VPNCORP_100导出了           3 行
. . 正在导出表                     VPNCORP_300导出了           3 行
. . 正在导出表                   VPNSUBSCRIBER导出了           6 行
. . 正在导出表                  VPNUNITECORPID导出了           1 行
. 正在导出同义词
. 正在导出视图
. 正在导出引用完整性约束条件
. 正在导出存储过程
. 正在导出运算符
. 正在导出索引类型
. 正在导出位图, 功能性索引和可扩展索引
. 正在导出后期表活动
. 正在导出触发器
. 正在导出实体化视图
. 正在导出快照日志
. 正在导出作业队列
. 正在导出刷新组和子组
. 正在导出维
. 正在导出 post-schema 过程对象和操作
. 正在导出用户历史记录表
. 正在导出默认值和系统审计选项
. 正在导出统计信息
成功终止导出, 没有出现警告。
```
 
## 数据库全表导入

```
imp username/password@sid  file=XXX.dmp  ignore=y  commit=y  full=y
```

例如：

```
imp system/sys@mmsgdb  file=./fullbak_20100329_104203.dmp ignore=y  commit=y  full=y
```

注：
* .dmp文件必须以bin方式从节点一1 ftp到节点2

## 应用数据库全表导出

### 脚本

```
#!/bin/sh

#定义备份时间
backupdate=`date +'%Y%m%d_%H%M%S'`

#定义备份路径
BakPath=/opt/oracle/oracle_table_bak

if [ ! -d $ORACLE_BASE/oracle_table_bak ];then
 mkdir -p $ORACLE_BASE/oracle_table_bak
fi

# 定义oracle用户名和密码
ACCOUNT=mmsg     #用户名称
PASSWORD=mmsg       #用户密码
SID=mmsgdb         #数据库别名
echo "Please input user name,password and SID to connect to oracle"
#读入用户名
echo "username(mmsg)"
read U_INPUT
if [ "x$U_INPUT" != "x" ]; then
    ACCOUNT=$U_INPUT
fi

#读入密码
echo "password(mmsg)"
read U_INPUT
if [ "x$U_INPUT" != "x" ]; then
    PASSWORD=$U_INPUT
fi

#读入SID
echo "SID( mmsgdb)"
read U_INPUT
if [ "x$U_INPUT" != "x" ]; then
    SID=$U_INPUT
fi

#系统所在路径
APPHOME=`dirname $0`
if [ $APPHOME = "." ]; then
   APPHOME=`pwd`
fi
cd $APPHOME

#执行导出操作
exp $ACCOUNT/$PASSWORD@$SID file=${ORACLE_BASE}/oracle_table_bak/fullbak_$backupdate.dmp  log=${ORACLE_BASE}/oracle_table_bak/fullbak_$backupdate.log full=y
```
           
### 导出过程日志

```
oracle@mmsg:~> sh fullbak_mmsg.sh 
Please input user name,password and SID to connect to oracle
username(mmsg)

password(mmsg)

SID( mmsgdb)


Export: Release 11.1.0.7.0 - Production on 星期一 3月 29 11:50:28 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


连接到: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
EXP-00023: 必须是 DBA 才能执行完整数据库或表空间导出操作
(2)U(用户), 或 (3)T(表): (2)U >   #直接按回车键

导出权限 (yes/no): yes >    #直接按回车键

导出表数据 (yes/no): yes >  #直接按回车键

压缩区 (yes/no): yes >      #直接按回车键

已导出 ZHS16GBK 字符集和 UTF8 NCHAR 字符集
. 正在导出 pre-schema 过程对象和操作
. 正在导出用户 MMSG 的外部函数库名
. 导出 PUBLIC 类型同义词
. 正在导出专用类型同义词
. 正在导出用户 MMSG 的对象类型定义
即将导出 MMSG 的对象...
. 正在导出数据库链接
. 正在导出序号
. 正在导出簇定义
. 即将导出 MMSG 的表通过常规路径...
. . 正在导出表                        AREAINFO导出了         374 行
. . 正在导出表                      AREANUMBER导出了         364 行
. . 正在导出表                AREANUMBERPREFIX导出了           2 行
. . 正在导出表                 BEARERVALUELIST导出了           3 行
. . 正在导出表                     CARRIERINFO导出了           1 行
. . 正在导出表                CHARGINGKPCONFIG导出了          28 行
. . 正在导出表                  CONNECTIONINFO导出了           0 行
. . 正在导出表                     COUNTRYCODE导出了          21 行
. . 正在导出表              DATAFILESTATUSCODE导出了           0 行
. . 正在导出表                DETAILSTATUSCODE导出了         247 行
……………………………………….. ………………………………………..中间数据省略 ……………………………………….. ………………………………………..
. . 正在导出表                   VPNSUBSCRIBER导出了           6 行
. . 正在导出表                  VPNUNITECORPID导出了           1 行
. 正在导出同义词
. 正在导出视图
. 正在导出存储过程
. 正在导出运算符
. 正在导出引用完整性约束条件
. 正在导出触发器
. 正在导出索引类型
. 正在导出位图, 功能性索引和可扩展索引
. 正在导出后期表活动
. 正在导出实体化视图
. 正在导出快照日志
. 正在导出作业队列
. 正在导出刷新组和子组
. 正在导出维
. 正在导出 post-schema 过程对象和操作
. 正在导出统计信息
导出成功终止, 但出现警告。
#这里告警，是因为只有DBA用户才能进行全表导出操作，根据提示信息按回车 进行下一步操作就可以了，不影响实际使用。
oracle@mmsg:~>
```

### 应用数据库全表导入

```
imp  username/passwd@sid file=XXX.dmp ignore=y commit=y  full=y
```

或者

```
imp username/passwd@dbname fromuser=XXX touser=XXX file= XXX.dmp ignore=y commit=y full=y
```

其中
* fromuser  该选项用于指定从导出文件中摘取并导入特定用于的对象；
* touser 该选项用于指定将特定方案对象导入到其他用户。

例如：

```
imp mmsg/mmsg@mmsgdb fromuser=mmsg touser=yjh  file=./fullbak_20100329_104203.dmp ignore=y commit=y  full=y
```

如果导入导出的用户名一致，可以直接使用如下命令进行导入：

```
imp mmsg/mmsg@mmsgdb  file=./fullbak_20100329_104203.dmp ignore=y commit=y  full=y
```

注：
* .dmp文件必须以bin方式从节点1 ftp到节点2


### 在AIX6.1上验证结果

```
% imp mmsg/mmsg@iagw file=fullbak_20100329_115026.dmp  ignore=y commit=y  full=y

Import: Release 11.1.0.6.0 - Production on 星期一 3月 29 23:33:09 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to: Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining,
Oracle Database Vault and Real Application Testing option

Export file created by EXPORT:V11.01.00 via conventional path
import done in ZHS16GBK character set and AL16UTF16 NCHAR character set
export server uses UTF8 NCHAR character set (possible ncharset conversion)
. importing MMSG's objects into MMSG
. . importing table                     "AREAINFO"        374 rows imported
. . importing table                   "AREANUMBER"        364 rows imported
……………………………………….. ………………………………………..中间数据省略 ……………………………………….. ………………………………………..
. . importing table                "VPNSUBSCRIBER"          6 rows imported
. . importing table               "VPNUNITECORPID"          1 rows imported
Import terminated successfully without warnings.
```
