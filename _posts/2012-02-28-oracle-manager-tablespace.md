---
layout:     post
title:      "Oracle 管理篇之表空间"
subtitle:   "Manager of oracle tablespace"
date:       2012-02-28
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# 查看表空间

在做报表性能测试的时候，我们一般都需要去查看表空间。如果表空间已经满了，话单文件就堆积了，无法入库了。

```
SQL> select * from v$tablespace;

       TS# NAME                           INC BIG FLA ENC
---------- ------------------------------ --- --- --- ---
         0 SYSTEM                         YES NO  YES
         1 SYSAUX                         YES NO  YES
         2 UNDOTBS1                       YES NO  YES
         3 TEMP                           NO  NO  YES
         4 USERS                          YES NO  YES
         5 SMCRPT_HOME                    YES NO  YES
        14 INFOX_WEB_MAIN_DATA            YES NO  YES
         8 GW_IND_SMPP                    YES NO  YES
         7 GW_IN_SMPP                     YES NO  YES
         9 GW_HIS_SMPP                    YES NO  YES
        15 INFOX_WEB_MAIN_INDEX           YES NO  YES

       TS# NAME                           INC BIG FLA ENC
---------- ------------------------------ --- --- --- ---
        11 CDR                            YES NO  YES
        12 CDR_TEMP                       NO  NO  YES
        13 MMSGYK                         YES NO  YES
        26 INFOX_TEMPLFQ                  NO  NO  YES
        17 TB_SCOTT                       YES NO  YES
        18 INFOX_MAIN_DATA                YES NO  YES
        19 INFOX_MAIN_INDEX               YES NO  YES
        20 INFOX_BACKUP_DATA              YES NO  YES
        23 INFOX_RESEND                   YES NO  YES
        24 INFOX_CONGESTION               YES NO  YES
        25 INFOX_TRAFFIC                  YES NO  YES

       TS# NAME                           INC BIG FLA ENC
---------- ------------------------------ --- --- --- ---
        27 INFOX_TEMP_LFQ                 NO  NO  YES
        28 IMUSE01                        YES NO  YES
        29 BILL                            YES NO  YES
        30 IMUSE01_INDEX                  YES NO  YES
        31 IMUSE01_TEMP                   NO  NO  YES

27 rows selected.
```

但是上述命令呢，我们依然无法查看各个表空间分配了多大的空间，已经使用了多少空间，还剩余多少空间等信息，而且也不直观。

# OEM查看表空间

现提供另外一种方法来查看各个表空间的信息。

## 1、启动OEM

oracle用户登录服务器，执行如下命令：

```
emctl start dbconsole
```

如果服务已经起来了，显示信息如下：

```
oracle@linux:~> emctl start dbconsole
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
        LANGUAGE = (unset),
        LC_ALL = (unset),
        LANG = "AMERICAN_CHINA.ZHS16GBK"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
Oracle Enterprise Manager 11g Database Control Release 11.1.0.6.0
Copyright (c) 1996, 2007 Oracle Corporation.  All rights reserved.
https://linux:1158/em/console/aboutApplication
Starting Oracle Enterprise Manager 11g Database Control ...... started.
------------------------------------------------------------------
Logs are generated in directory /home/oracle/product/11g/linux_infoxdb/sysman/log
```

停止DBCONSOLE服务：

```
oracle@linux:~> emctl stop dbconsole
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
        LANGUAGE = (unset),
        LC_ALL = (unset),
        LANG = "AMERICAN_CHINA.ZHS16GBK"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
Oracle Enterprise Manager 11g Database Control Release 11.1.0.6.0
Copyright (c) 1996, 2007 Oracle Corporation.  All rights reserved.
https://linux:1158/em/console/aboutApplication
Stopping Oracle Enterprise Manager 11g Database Control ...

all attemps to stop oc4j failed... now trying to kill 9
--- Failed to shutdown DBConsole Gracefully ---
 ...  Stopped.
```

启动失败会出现类似如下信息：

```
OC4J Configuration issue. /opt/oracle/app/product/11.1.0/db_1/oc4j/j2ee/OC4J_DBConsole_expsmgw_ora11g not found.
```

## 2、IE登录服务器https://serverip:1158/em

（如果IE登录失败，可以在Internet选项中添加可信任站点，将上述服务器的URL地址添加为可信任站点）

## 3、以系统管理员身份登录
 
<img class="shadow" src="/img/in-post/oracle_oem.png" width="800" />

4、查看表空间信息

主目录 --> 服务器 --> 存储下 表空间

查看各个表空间的详细信息。
 
<img class="shadow" src="/img/in-post/oracle_oem-1.png" width="800" />

# 其他方法查看表空间

```
dba_tablespace_usage_metrics
select tablespace_name,tablespace_size/128 as tablespace_size_Mb from dba_tablespace_usage_metrics;
```

说明：

* dba_tablespace_usage_metrics是表，该表只能查询永久性表空间（同时仅包括系统临时表空间，不含应用级临时表空间）相关信息，该表查询获取的表空间大小并不准确，代码中慎用。


## dba_data_files

```
select  tablespace_name,bytes/1024/1024 as tablespace_size_Mb from dba_data_files;
```

说明:

* dba_data_files是表，该表只能查询永久性表空间相关信息。


## dba_temp_files

```
select  tablespace_name,bytes/1024/1024 as tablespace_size_Mb from  dba_temp_files;
```

说明：

* dba_temp_files是表，该表只能查询临时性表空间相关信息。


## dba_free_space
```
select sum(bytes)/1024/1024 from dba_free_space where tablespace_name='WYZ';
```

说明：

* dba_free_space是视图，该视图只能查询永久性表空间相关信息。
 
## dba_temp_free_space

```
select tablespace_name,tablespace_size/1024/1024 from dba_temp_free_space;
```

说明：

* dba_temp_free_space是视图，该视图只能查询临时性表空间相关信息。

# Suse平台扩展Oracle表空间操作

当按照安装规划创建的表空间无法适应于当前性能测试需要时，可以通过如下方法扩大相应逻辑卷，增加空间。

Suse操作系统下扩展Oracle表空间一般情况我们通过扩展裸设备大小的操作，而不是通过增加裸设备个数的操作来实现。因为Suse中的裸设备raw**是需要跟lv文件进行绑定的，该绑定操作需要在系统重启的时候执行。而绑定关系是配置在启动文件中的（该部分可以参考安装指南）。如果增加了裸设备还需要修改绑定关系，为了减少操作，我们一般使用修改lv/裸设备大小的方式进行。

假设临时表空间需要扩展表空间，步骤如下：

扩展lv大小

先找出临时表空间用到哪个裸设备，假设为raw2，然后在安装文档或/etc/raw文件中找到raw2对应绑定的lv的名称，假设为/dev/datavg/lvora_temp1，那么可以将该lv增大2G。

```lvextend -L +2G /dev/datavg/lvora_temp1 ```

datafile是针对一般表空间

当扩展的是临时表空间时，替换成tmpfile

# 扩展表空间

当表空间已经满时，执行数据库操作数据库会报错，例如：

```
ORA-01653: 表 MMSG.TMP_BASE_RESULT 无法通过 8 (在表空间 MMSG 中) 扩展
ORA-06512: 在 "MMSG.LOG2DB_UTIL", line 92
ORA-06512: 在 line 1
需要扩展表空间
ORA－01653
node1:oracle:mmsgdb > oerr ora 01653
01653, 00000, "unable to extend table %s.%s by %s in tablespace %s"
// *Cause:  Failed to allocate an extent of the required number of blocks for 
//          a table segment in the tablespace indicated.
// *Action: Use ALTER TABLESPACE ADD DATAFILE statement to add one or more
//          files to the tablespace indicated.
node1:oracle:mmsgdb >
```

扩展操作命令如下：

```
alter database datafile '/opt/oracle/admin/mmsgdb/mmsgdata/mmsgdata01' AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED；
```

下面的两个命令也可以：

```
alter tablespace mmsg add datafile '/opt/oracle/admin/mmsgdb/mmsgdata/mmsgdata01' size 1024M reuse;
alter database datafile '/opt/oracle/admin/mmsgdb/mmsgdata/mmsgdata01' resize 2048M;
```

扩展后重启实例，查看相关表空间是否已经扩展，

```
select * from dba_tablespace_usage_metrics;
```

# Undo表空间

## 什么是UNDO

Undo是数据库在撤销、回退或者改变数据所需要的数据库维护信息的一种手段。这里的数据库维护信息主要指的是在数据库提交数据之前的记录的改变等事务信息。

## UNDO信息作用

1、当系统发布rollback命令时恢复数据库；

2、提供读一致性。

当系统发布rollback命令时，undo通过记录的信息将数据库中数据恢复到commit之前的状态。在数据恢复期间，undo被用来从undo表空间中撤销任何未提交到数据文件的事务。

对于回滚的数据：

delete         回滚段记录整行记录
update         回滚段记录修改了的字段变化前的数据
insert         回滚段记录插入记录的rawid

如果commit，则回滚段中简单标记事务以提交；

如果rollbak

delete         把回滚段整行记录写入数据文件中
update         把回滚段记录修改了的字段变化前的数据写回去
insert         把回滚段记录插入记录的rawid删除掉


当一个用户在访问数据时，Undo记录通过维护访问数据的前镜像数据来保证当有其他用户改变相同数据时数据库的读一致性。

（consisitent reads) Oralce的查询集是根据时间点来判定的。Oracle内部通过系统改变号SC作为相对时间点的标准，任何对数据库的改变都会产生SCN，对数据块的数据改变的时候会把该改变所对应的SCN记录在块中。假设查询开始的时候SCN为T，则在查询所扫描的数据块中，如果数据块的COMMIT SCN小鱼T，则查询接受该数据，如果COMMIT SCN大于T或者说还没有产生COMMIT SCN，则查询会尝试去回滚段中查找数据。这保证了数据的读取时间点的一致性。

# 系统回滚段和延迟回滚段

SYSTEM回滚段是创建在系统表空间中，主要用于系统级的事务和分配普通事务于其他回滚段上。当手工创建数据后需要创建普通回滚段之前必须首先创建系统回滚段。按oracle文档说，当普通事务异常多的事情可能会使用系统回滚段的情况。正常情况下，系统回滚段主要用于两个方面：一是系统事务，例如针对数据字典的操作的truncate table 和 drop table。如果truncate or drop table的过程中没有成果，则系统会根据系统回滚段中的数据字典操作信息对该DDL操作进行回退。

另一个方面，就是延迟回滚段(Deferred Rollback Segment)。延迟回滚段表示，当我们使一个表空间OFFLINE之后，由于表空间不可用，这个时候若有事务数据位于该空间并执行回滚命令，在client看起来该事务已经回滚，但对于数据块来说回滚并没有真正完成，这个时候数据库将该回滚信息写入系统回滚段（这就是延迟回滚段），等表空间重新ONLINE的时候，数据块从系统回滚段中将回滚信息写入表空间。


# 相关参数

```
SQL> show parameter undo

NAME                            TYPE          VALUE
------------------------------------        -----------       ------------------------------
undo_management                    string        AUTO
undo_retention                        integer      900
undo_tablespace                       string       UNDOTBS1
SQL>
```

# undo_management

undo管理方式。undo_management设置为AUTO时，系统使用撤销表空间来管理回滚段；

undo_management设置为MENUAL时，系统使用回滚段。

Oracle推荐使用撤销表空间管理回滚段，当undo_management设置为AUTO时，必须指定一个UNDO表空间。UNDO表空间可以在数据库安装时候创建，也可在数据库安装完成后创建。

当数据库启动的时，oracle会自动选择第一个可用的undo表空间或者是rollbak_segment，如果没有可用的undo表空行和rollbak_segment，系统选择system rollback_segment，这种情况是不被推荐使用的。当系统运行在没有undo的情况下，系统产生一条告警信息记录告警日志。

# undo_retention

系统提交后，回滚段的数据保留多长时间，单位是秒。

# undo_tablespace

指定数据库使用哪一个撤销表空间。

## 查询回退率

```
SELECT NAME, VALUE FROM v$sysstat WHERE NAME IN ('user commits', 'transaction rollbacks');
```

# UNDO TABLESPACE

UNDO TABLESPACE变的很大，我们不能缩小，这个时候我们需要考虑创建新的UNDO TABLESPACE，然后切换到这个新创建的UNDO表空间。这时即使UNDO表空间有事务也可以切换，只不过不能立即删除该表空间，切换之后等到原来的表空间中所有的事务处理完毕，并且达到undo_retention的时间后，就可以drop原来的UNDO表空间。

# 表空间碎片

一个碎片表空间具有很多不连续的自由空间块，碎片会导致性能与空间问题，性能受到影响是因为oracle不得不扫描更多的对象区间，并有可能跨越多个物理磁盘，当数据进行磁盘碎片整理时，对象可以从多个区间压缩为一个区间，减少扫描数据时的内部oracle开销。

相反，一个碎片表空间影响对象存储，具有许多小的自由空间块延伸跨越多个表空间，一些对象可能不会被创建，而如果所有表空间是连续的，空间将足够用于创建该对象。通过表空间磁盘碎片整理，重新组织数据使所有小的自由块形成一个自由块。

当对象如表或索引随表的创建、删除、增大或减小尺寸时，会发生碎片。由于oracle只能在表空间中的、一个连续的自由空间内创建一个区间，会开始出现一些小的自由空间。当删除一个对象时，它的自由空间很有可能处于表空间中分散的地点，只能在那个自由空间中创建另一个相等或小一些的对象。

通过如下命令可以检查表空间的碎片，可以检查在指定的表空间中有多少自由空间段，以及它们的大小。

```
select A.TABLESPACE_NAME,B.FILE_NAME,A.BYTES
from dba_free_space A,dba_data_files B
where A.TABLESPACE_NAME = '&tablespace_name' and
A.FILE_ID=B.FILE_ID
order by bytes desc;
```

当运行这段sql代码，服务器会提示输入表空间名：

输入 tablespace_name 的值:  

终端上显示如下：
 
<img class="shadow" src="/img/in-post/oracle_sql.png" width="600" />

PLSQL Developer工具显示如下：

<img class="shadow" src="/img/in-post/oracle_dev.png" width="600" />

对每一个不同的file_name，应该各有一条记录。如果没有，表空间就是碎片的。在含有碎片的表空间中表在导入导出过程中会成为用户不可用的，即数据无效。在依赖导入与导入表空间进行表空间碎片整理时，应该输入命令 alter tablespace tablespace_name coalesce。

如果自由空间的两个大块彼此毗邻，这条命令使它们组成一个更大的块，如果这条命令没用，必须使用导入导出以整理表空间碎片。

另一个需要整理表空间的原因是：是否表空间内对象含有多个区间的情况。在大多数情况下，如果对象多于5个区间，应该加以关注，

因为在这点之后，性能受到显著影响。

如下sql代码查询哪些对象具有多于5个区间：

```
select owner,segment_name, extents from dba_segments
where extents > 5 
and owner not in ('SYS','SYSTEM')
order BY EXTENTS;
```

在开始进行碎整理时，先确认已经知会到所有可能受影响的人，因为在这个操作过程中，表空间中的表将不可用。如果可能，计划在没有人使用这些表的情况下进行碎片整理。

使用导入导出整理一个表空间的碎片，遵循的步骤如下：

1、导出表空间下所有表，确认已设置了commpress=y；
2、手工删除表空间中所有的表；
3、合并表空间中的自由空间，使用alter tablespace tablespace_name coalesce命令完成。
所有的自由空间被合并成一个块，或者与表空间的数据文件一样多的块，因为表空间中不含有对象。

# 说说临时表空间Temp的异常胀大

笔者接到一个做开发上线的兄弟电话，说正在试运行的系统存储过程突然变慢，而且偶然发现数据库的Temp表空间突然增加到20多G。这位兄弟不知道是不是与存储过程突然变慢有关，而且应该如何处理。----转载

## 1、从Temporary Tablespace谈起
 
表空间（Tablespace）、段对象（Segment）、分区（Extent）和数据块（Block）是Oracle逻辑层面上最重要的几个概念。其中，表空间是各个逻辑层面顶层概念，也是与Oracle物理结构文件可以建立关系的重要环节。

```
SQL> select tablespace_name, contents, logging from dba_tablespaces;

TABLESPACE_NAME               CONTENTS LOGGING
------------------------------ --------- ---------
SYSTEM                        PERMANENT LOGGING
UNDOTBS1                      UNDO     LOGGING
SYSAUX                        PERMANENT LOGGING
TEMP                          TEMPORARY NOLOGGING
USERS                         PERMANENT LOGGING
EXAMPLE                       PERMANENT NOLOGGING

6 rows selected

```

表空间从类型上有若干分类的方式，一种是按照“文件file”的大小，区别为small file tablespace和big file tablespace。另一种是按照表空间用途而定的。此种分类方法可以将表空间划分为持久化表空间（Permanent Tablespace）、Undo表空间和临时表空间（Temporary Tablespace）。

Temporary临时表空间是Oracle一种内部空间调控的产物。根据Oracle官方文档中的介绍，Temporary表空间主要是针对session会话自身的操作使用的。

当一个会话通过SQL或者PL/SQL将数据集合获取，进行大面积的sort或者group by操作时，会话会严重的消耗PGA资源。PGA是针对会话自身特有信息的一块内存区域，用于保存会话自身特有、无法与其他会话共享的信息。如果数据集很大，这样对内存PGA的资源消耗就会很大。Oracle在这个时候，就会采用类似操作系统虚拟内存技术的方法，从硬盘上借一块空间给PGA置换使用，缓解PGA的不足。

使用Temporary表空间的时候，是系统自动完成的临时段segment对象创建和销毁。这个过程对用户会话而言是透明的。

临时表空间对应的文件就是临时文件temp file，在Oracle中可以使用dba_temp_files视图进行查询。

```
SQL> col file_name for a50;
SQL> select file_name, bytes/1024/1024, AUTOEXTENSIBLE from dba_temp_files;
 
FILE_NAME                                         BYTES/1024/1024 AUTOEXTENSIBLE

-------------------------------------------------- ---------------
D:\ORACLE\PRODUCT\10.2.0\ORADATA\ORCL\TEMP01.DBF              123YES
```

通常，在系统创建的时候，Oracle会创建临时表空间Temp作为系统默认临时表空间Temporary Tablespace。而且，通常Temp表空间都是设置为支持自动拓展的。

## 2、问题分析

回到那位兄弟的问题，简单归纳出来就是“系统中出现批作业缓慢的现象，发现临时表空间暴增”。

从上面我们对于Temp表空间的分析介绍，我们可以初步认为临时表空间的暴增是一个结果，而不是一个原因。或者说，至少是某个原因的结果。

什么意思呢？首先，Oracle文件有自动膨胀autoextend的功能，但是却没有自动缩减的能力。临时表空间容纳的对象，都是系统创建、管理的临时段对象。当会话结束、SQL命令结果返回的时候，临时表空间的内容是可以回收的。所以，Temp表空间的自动膨胀大小结果不是一个累积的效果，而是一个峰值效果。

Temp表空间增加到20G，说明在系统运行的某个阶段，由于会话并发或者其他的原因，引起系统内部排序、分组等PGA高消耗操作剧烈增加，瞬时超过了Temp原有的大小。从而引发Oracle进行Temp表空间的自动拓展，拓展到当前的大小。之后会话操作结束，临时段segment对象被回收，但是文件大小不会重新回收。所以导致了Temp表空间膨胀的事实。

那么，有什么样的原因可能导致出现瞬时Temp空间消耗高峰呢？几种可能的情况如下：

### 系统本身特点

我们说最大使用Temp表空间的就是sort和group by操作。对一些OLAP、DSS系统而言，无论是进行报表生成还是数据整理汇总析取，都伴随着海量数据的sort或者group by。一般情况下的PGA设置是无法满足如此巨大的空间需求的，必然要消耗相当的Temp表空间。根据笔者的了解，一些数据仓库性质的系统对Temp的消耗达到几十上百G是很常见的；

### 应用本身对SQL处理量失控

SQL是一种描述性语言，修改一条记录和修改一千万条记录的语句结构可能都是相同的。但是，对系统而言，两者的差异是天壤之别。比如，当我们尝试将获取到数据集合bulk collect到一个数组时候，要关注到可能的数据量规模。如果数据集合较小，一切都好说。但是如果数据集合达到百万级以上，那么瞬时百万条数据全部请求存放在PGA中，进而引起Temp的过量使用；

### 第三方工具的使用

很多第三方工具，特别是带有数据分析处理的软件，通过专门的业务实体层封装SQL语句。一些时候，这种封装SQL进行连接、汇总时也会带来大量的Temp消耗。

## 3、问题解决
经过沟通，确认系统发生的变更情况。在最近一段时间，系统安装了BO相关组件，多用户在反复同时生成报表的时候，可能会出现Temp消耗高峰的情况。

同时，观察应用系统的部分代码，存在SQL处理量未受控的情况，建议开发组根据工作进度情况进行重构处理。

至于说特定SQL执行时间过长，通过诊断（或者AWR、ASH）确定了问题SQL，进行执行计划修正后问题解决。

最后说说对当前系统临时表空间的处理。在使用BO的前提下，临时表空间胀大的情况也许是不可避免的。所以建议开发组从几个方面着手：
1、借助AWR报告，确定究竟是BO造成的临时表空间使用量过高还是应用本身问题；
2、如果确定是BO本身问题，可以确定一个基本的峰值。将临时表空间文件设置一个增长上限，不要关闭autoextend开关；
3、如果是应用本身的问题，也不要轻易关闭autoextend开关。因为如果Temp表空间需要资源而无法分配，那么前端应用会产生异常报错；
4、不断诊断和重构应用代码，加入处理量控制代码，力图做到每次处理的数据量存在可控上限。防止出现瞬时处理量胀大的情况；

## 4、结论

这个案例，告诉我们两点思考之处：

### 1、分清主次因果

数据库诊断调优是一项综合性强的技术。我们看到的大多是问题的表象，甚至是很奇怪的表象。这时候，我们就需要分析问题的根源，理清主次矛盾、孰因孰果，定位到问题的核心；

### 2、分清轻重远近

很多性能问题的根源不是某个或者某几个SQL造成的，而是和开发过程中一些习惯和细节问题日积月累起来。这种情况下，修改重构是一个过程，不可能一蹴而就。所以，调优要从远近轻重的角度制定方案。首先让应用跑起来，支持生产。之后才是将问题一点点的解决。Oracle推出的outline等技术也就是这个含义。

