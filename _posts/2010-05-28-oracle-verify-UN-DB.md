---
layout:     post
title:      "联通数据库切换验证"
subtitle:   "UN Database switch verification"
date:       2010-05-28
author:     "Gavin"
catalog:    true
tags:
    - oracle
---



# 背景

现状:

数据库与业务分别设立在不同的单板上（suse10 + ora11g)

调整:

把数据库切换到AIX机器上，业务单板不变。

示意图如下：

<img class="shadow" src="/img/in-post/un_to_be.png" width="360" />

数据迁移流程图

<img class="shadow" src="/img/in-post/un_db_change.png" width="600" />
 
# 操作过程

## 数据库A应用数据全表导出

脚本:

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
ACCOUNT=mmsg        #用户名称
PASSWORD=mmsg       #用户密码
SID=mmsgdb          #数据库别名
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

## 导出

1、oracle用户上传fullbak_mmsg.sh脚本，并为fullbak_mmsg.sh脚本增加可执行权限

```chmod +x fullbak_mmsg.sh ```

2、使用oracle用户执行fullbak_mmsg.sh脚本

```sh fullbak_mmsg.sh ```

3、导出过程日志信息片段如下

```
Connected to: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
Export done in ZHS16GBK character set and UTF8 NCHAR character set

About to export the entire database ...
. exporting tablespace definitions
. exporting profiles
. exporting user definitions
. exporting roles
. exporting resource costs
. exporting rollback segment definitions
. exporting database links
. exporting sequence numbers
. exporting directory aliases
. exporting context namespaces
. exporting foreign function library names
. exporting PUBLIC type synonyms
. exporting private type synonyms
. exporting object type definitions
. exporting system procedural objects and actions
. exporting pre-schema procedural objects and actions
. exporting cluster definitions
. about to export SYSTEM's tables via Conventional Path ...
. . exporting table                    DEF$_AQCALL          0 rows exported
. . exporting table                   DEF$_AQERROR          0 rows exported
. . exporting table                  DEF$_CALLDEST          0 rows exported
. . exporting table               DEF$_DEFAULTDEST          0 rows exported
…………………………………………………………………………………………
. . exporting table                 VPNUNITECORPID          1 rows exported
. exporting synonyms
. exporting views
. exporting referential integrity constraints
. exporting stored procedures
. exporting operators
. exporting indextypes
. exporting bitmap, functional and extensible indexes
. exporting posttables actions
. exporting triggers
. exporting materialized views
. exporting snapshot logs
. exporting job queues
. exporting refresh groups and children
. exporting dimensions
. exporting post-schema procedural objects and actions
. exporting user history table
. exporting default and system auditing options
. exporting statistics
Export terminated successfully without warnings.
```

## 可能出现的问题解决方法

### ORA-06550、EXP-00008、PLS-0020、ORA-06512错误

在导出过程中如果出现如下错误：

```
EXP-00008: ORACLE error 6550 encountered
ORA-06550: line 1, column 19:
PLS-00201: identifier 'SYS.DBMS_DEFER_IMPORT_INTERNAL' must be declared
ORA-06550: line 1, column 7:
PL/SQL: Statement ignored
ORA-06512: at "SYS.DBMS_SQL", line 1575
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 97
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 126
ORA-06512: at line 1
. . exporting table                   DEF$_AQERROR
EXP-00008: ORACLE error 6510 encountered
ORA-06510: PL/SQL: unhandled user-defined exception
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 50
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 126
ORA-06512: at line 1
. . exporting table                  DEF$_CALLDEST
EXP-00008: ORACLE error 6550 encountered
ORA-06550: line 1, column 19:
PLS-00201: identifier 'SYS.DBMS_DEFER_IMPORT_INTERNAL' must be declared
ORA-06550: line 1, column 7:
PL/SQL: Statement ignored
ORA-06512: at "SYS.DBMS_SQL", line 1575
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 97
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 126
ORA-06512: at line 1
. . exporting table               DEF$_DEFAULTDEST
EXP-00008: ORACLE error 6510 encountered
ORA-06510: PL/SQL: unhandled user-defined exception
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 50
ORA-06512: at "SYS.DBMS_EXPORT_EXTENSION", line 126
ORA-06512: at line 1
```

请使用如下方法解决：

1、将DBMS_EXPORT_EXTENSION和DBMS_DEFER_IMPORT_INTERNAL执行权限赋予导出用户

```
grant execute on DBMS_EXPORT_EXTENSION to 导出用户;
grant execute on DBMS_DEFER_IMPORT_INTERNAL to 导出用户;
```

2、成功赋予权限后，执行应用全表导出操作

```
sh fullbak_mmsg.sh
```

## 应用全表导入到数据库B

注：
* 在将数据库A中表数据导入到数据库B中 之前，请务必先备份数据库B中数据，备份操作请参考“数据库A应用数据全表导出”部分内容。

### 1、删除原有数据库中所有应用表

注：
* 本段的操作，必须是在正确完成上述应用数据库B中数据的导出工作后进行！

删除原有数据库中所有应用表操作步骤

#### A、准备存储过程

新增一存储过程drop_tbl_table，sql脚本代码如下：

```
create or replace procedure drop_tbl_table(tname in varchar)

is
    v_sql      varchar(100);    -- 动态SQL语句
    v_count    number(10);      -- 数据库中drop过的表数


begin
    v_count := 0;
    
    for v1 in (select * from all_tables where owner = 'MMSG')
    loop
        v_sql := 'drop table ' || v1.table_name;
        v_count := v_count + 1;
        execute immediate v_sql;
    end loop;
    dbms_output.put_line(v_count);
end drop_tbl_table;
/
```

将上述脚本拷贝到文件中，以asc方式上传到oracle数据库某节点下，并将该文件命名为ora_proc_drop_tbl_tables.sql，如下：
 
注：
* ```sql脚本中select * from all_tables where owner = 'MMSG'``` 的 MMSG为表的属主，请根据现网环境选择正确属主，否则会造成误删不相关的表，造成数据丢失。

#### B、创建存储过程

oracle用户成功登录终端，以应用用户（如数据库应用用户mmsg）与数据库建立连接，执行ora_proc_drop_tbl_tables.sql脚本

```
oracle@mmsg:~> cat ora_proc_drop_tbl_tables.sql | sqlplus mmsg/mmsg@mmsgdb

SQL*Plus: Release 11.1.0.7.0 - Production on 星期一 7月 12 18:08:17 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL>   2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19  
过程已创建。

SQL> 从 Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options 断开
oracle@mmsg:~>
```

#### C、执行存储过程

执行存储过程，删除所有应用表。

```
oracle@mmsg:~> sqlplus mmsg/mmsg@mmsgdb

SQL*Plus: Release 11.1.0.7.0 - Production on 星期一 7月 12 17:52:44 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> exec drop_tbl_table(0)

PL/SQL 过程已成功完成。

SQL>
```

注意事项：

* 1、存储过程的执行过程需要一定的时间（尤其应用表数量较多时），请耐心等待。切勿执行退出命令，否则会导致表删除不全。
* 2、存储过程执行完毕后，输入sqlplus中输入如下命令查看表是否删除完毕：
```select  count(0)  from all_tables where owner = 'MMSG'; ```
如果查询结果是0，则 表删除完毕。

## 2、导入

```imp  username/passwd@sid file=XXX.dmp ignore=y commit=y  full=y```

或者

```imp username/passwd@dbname fromuser=XXX touser=XXX file= XXX.dmp ignore=y commit=y full=y ```

其中:
* fromuser  该选项用于指定从导出文件中摘取并导入特定用于的对象；
* touser    该选项用于指定将特定方案对象导入到其他用户。

例如：

```
imp wyz/wyz@iagw fromuser=mmsg touser=wyz file=./fullbak_20100507_091121.dmp ignore=y commit=y log= fullbak_20100506_194731.log
```

如果导入导出的用户名一致，可以直接使用如下命令进行导入：

```
imp mmsg/mmsg@mmsgdb  file=./ fullbak_20100507_091121.dmp  ignore=y commit=y  full=y
```

注：
* .dmp文件必须以bin方式从数据库A ftp到数据库B

## 可能出现的问题解决方法

如果在导入过程中并未出现下列问题，请跳过下列步骤，直接验证导入后数据完整性。


### IMP-00013错误

如果在导入过程中出现IMP-00013错误，如下：

```
% imp wyz/wyz@iagw fromuser=mmsg touser=wyz file=./fullbak_20100506_200334.dmp ignore=y commit=y

Import: Release 11.1.0.6.0 - Production on 星期四 5月 6 20:13:59 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to: Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining,
Oracle Database Vault and Real Application Testing option

Export file created by EXPORT:V11.01.00 via conventional path
IMP-00013: only a DBA can import a file exported by another DBA
IMP-00000: Import terminated unsuccessfully
%
```

原因:

导入用户不具有dba权限

解决方法:

赋予导入用户dba和imp_full_Database权限

操作如下:

```
% sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期五 5月 7 09:54:40 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining,
Oracle Database Vault and Real Application Testing options

SQL> grant dba to wyz;

Grant succeeded.

SQL> grant imp_full_Database to wyz;

Grant succeeded.

SQL> exit
```

### IMP-00003、ORA-01658错误

重新执行导入操作，如果在导入过程中出现如下错误

```
IMP-00003: ORACLE error 1658 encountered
ORA-01658: 无法为表空间 MMSG 中的段创建 INITIAL 区
```

原因:

1、表空间WYZ不足；

2、数据从A数据库导入到B数据库，但是没有使用B数据库对应的表空间。

解决方法如下:

1、请确保被导入数据的数据库所对应的表空间足够大，如果表空间不足，请使用如下方法进行相应的表空间扩展。

Suse平台扩展Oracle表空间操作

当按照安装规划创建的表空间无法适应于当前性能测试需要时，可以通过如下方法扩大相应逻辑卷，增加空间。

Suse操作系统下扩展Oracle表空间一般情况我们通过扩展裸设备大小的操作，而不是通过增加裸设备个数的操作来实现。因为Suse中的裸设备raw**是需要跟lv文件进行绑定的，该绑定操作需要在系统重启的时候执行。而绑定关系是配置在启动文件中的（该部分可以参考安装指南）。如果增加了裸设备还需要修改绑定关系，为了减少操作，我们一般使用修改lv/裸设备大小的方式进行。


假设临时表空间需要扩展表空间，步骤如下：

扩展lv大小。先找出临时表空间用到哪个裸设备，假设为raw2，然后在安装文档或/etc/raw文件中找到raw2对应绑定的lv的名称，假设为/dev/datavg/lvora_temp1，那么可以将该lv增大2G。

```# lvextend -L +2G /dev/datavg/lvora_temp1 ```

datafile是针对一般表空间

当扩展的是临时表空间时，替换成tmpfile

扩展表空间

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
alter database datafile '/opt/oracle/admin/mmsgdb/mmsgdata/mmsgdata01' AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED;
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

### Oracle用imp导入用户表时选择表空间的问题

当前表空间为WYZ，但是提示信息显示无法为表空间 MMSG 中的段创建 INITIAL 区，说明数据虽然导入到了wyz用户下，但是使用的表空间依然是MMSG，而我们所需要的是表空间WYZ，而非MMSG，解决方法如下：

```
% sqlplus / as sysdba

SQL*Plus: Release 11.1.0.6.0 - Production on 星期五 5月 7 11:08:51 2010

Copyright (c) 1982, 2007, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining,
Oracle Database Vault and Real Application Testing options

SQL> grant resource,connect to wyz; 

Grant succeeded.

SQL> grant dba to wyz;     // 赋 DBA 权限

Grant succeeded.

SQL> revoke unlimited tablespace from wyz;  // 撤销此权限

Revoke succeeded.

SQL> alter user wyz quota 0 on system;  //将用户在 System 表空间的配额置为 0

User altered.

SQL> alter user wyz quota unlimited on wyz; //设置用户在 wyz 表空间配额不受限。

User altered.

SQL> exit
```

上述问题解决后，重新执行数据导入操作

## 数据导入

```
imp wyz/wyz@iagw fromuser=mmsg touser=wyz file=./fullbak_20100507_091121.dmp ignore=y commit=y log=imp_20100507_091121.log
```

## 导入验证

日志信息

```

Connected to: Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
Export done in ZHS16GBK character set and UTF8 NCHAR character set

About to export the entire database ...
. exporting tablespace definitions
. exporting profiles
. exporting user definitions
. exporting roles
. exporting resource costs
. exporting rollback segment definitions
. exporting database links
. exporting sequence numbers
. exporting directory aliases
. exporting context namespaces
. exporting foreign function library names
. exporting PUBLIC type synonyms
. exporting private type synonyms
. exporting object type definitions
. exporting system procedural objects and actions
. exporting pre-schema procedural objects and actions
. exporting cluster definitions
. about to export SYSTEM's tables via Conventional Path ...
. . exporting table                    DEF$_AQCALL          0 rows exported
. . exporting table                   DEF$_AQERROR          0 rows exported
. . exporting table                  DEF$_CALLDEST          0 rows exported
. . exporting table               DEF$_DEFAULTDEST          0 rows exported
. . exporting table               DEF$_DESTINATION          0 rows exported
. . exporting table                     DEF$_ERROR          0 rows exported
. . exporting table                       DEF$_LOB          0 rows exported
. . exporting table                    DEF$_ORIGIN          0 rows exported
. . exporting table                DEF$_PROPAGATOR          0 rows exported
. . exporting table       DEF$_PUSHED_TRANSACTIONS          0 rows exported
. . exporting table                  DEF$_TEMP$LOB          0 rows exported
. . exporting table                            OL$
. . exporting table                       OL$HINTS
. . exporting table                       OL$NODES
. . exporting table           QUEST_SOO_AT_APPNAME          0 rows exported
. . exporting table    QUEST_SOO_AT_EXECUTION_PLAN          0 rows exported
. . exporting table        QUEST_SOO_AT_OPERATIONS          0 rows exported
. . exporting table      QUEST_SOO_AT_PARSE_CURSOR          0 rows exported
. . exporting table       QUEST_SOO_AT_PARSE_ERROR          0 rows exported
. . exporting table       QUEST_SOO_AT_PARSE_WAITS          0 rows exported
. . exporting table        QUEST_SOO_AT_SESSION_ID          0 rows exported
. . exporting table         QUEST_SOO_AT_SQL_BINDS          0 rows exported
. . exporting table    QUEST_SOO_AT_SQL_EXECUTIONS          0 rows exported
. . exporting table    QUEST_SOO_AT_SQL_EXEC_ERROR          0 rows exported
. . exporting table         QUEST_SOO_AT_SQL_FETCH          0 rows exported
. . exporting table     QUEST_SOO_AT_SQL_STATEMENT          0 rows exported
. . exporting table   QUEST_SOO_AT_SQL_STMT_PIECES          0 rows exported
. . exporting table         QUEST_SOO_AT_SQL_WAITS          0 rows exported
. . exporting table        QUEST_SOO_AT_TRACE_FILE          0 rows exported
. . exporting table        QUEST_SOO_AT_WAIT_NAMES          0 rows exported
. . exporting table          QUEST_SOO_BUFFER_BUSY          0 rows exported
. . exporting table     QUEST_SOO_EVENT_CATEGORIES       1445 rows exported
. . exporting table            QUEST_SOO_LOCK_TREE          0 rows exported
. . exporting table     QUEST_SOO_PARSE_TIME_TRACK          1 rows exported
. . exporting table           QUEST_SOO_PLAN_TABLE          0 rows exported
. . exporting table       QUEST_SOO_SB_BUFFER_BUSY          0 rows exported
. . exporting table             QUEST_SOO_SB_EVENT          0 rows exported
. . exporting table           QUEST_SOO_SB_IO_STAT          0 rows exported
. . exporting table      QUEST_SOO_SCHEMA_VERSIONS          1 rows exported
. . exporting table              QUEST_SOO_VERSION          1 rows exported
. . exporting table        REPCAT$_AUDIT_ATTRIBUTE          2 rows exported
. . exporting table           REPCAT$_AUDIT_COLUMN          0 rows exported
. . exporting table           REPCAT$_COLUMN_GROUP          0 rows exported
. . exporting table               REPCAT$_CONFLICT          0 rows exported
. . exporting table                    REPCAT$_DDL          0 rows exported
. . exporting table             REPCAT$_EXCEPTIONS          0 rows exported
. . exporting table              REPCAT$_EXTENSION          0 rows exported
. . exporting table                REPCAT$_FLAVORS          0 rows exported
. . exporting table         REPCAT$_FLAVOR_OBJECTS          0 rows exported
. . exporting table              REPCAT$_GENERATED          0 rows exported
. . exporting table         REPCAT$_GROUPED_COLUMN          0 rows exported
. . exporting table      REPCAT$_INSTANTIATION_DDL          0 rows exported
. . exporting table            REPCAT$_KEY_COLUMNS          0 rows exported
. . exporting table           REPCAT$_OBJECT_PARMS          0 rows exported
. . exporting table           REPCAT$_OBJECT_TYPES         28 rows exported
. . exporting table       REPCAT$_PARAMETER_COLUMN          0 rows exported
. . exporting table               REPCAT$_PRIORITY          0 rows exported
. . exporting table         REPCAT$_PRIORITY_GROUP          0 rows exported
. . exporting table      REPCAT$_REFRESH_TEMPLATES          0 rows exported
. . exporting table                 REPCAT$_REPCAT          0 rows exported
. . exporting table              REPCAT$_REPCATLOG          0 rows exported
. . exporting table              REPCAT$_REPCOLUMN          0 rows exported
. . exporting table         REPCAT$_REPGROUP_PRIVS          0 rows exported
. . exporting table              REPCAT$_REPOBJECT          0 rows exported
. . exporting table                REPCAT$_REPPROP          0 rows exported
. . exporting table              REPCAT$_REPSCHEMA          0 rows exported
. . exporting table             REPCAT$_RESOLUTION          0 rows exported
. . exporting table      REPCAT$_RESOLUTION_METHOD         19 rows exported
. . exporting table  REPCAT$_RESOLUTION_STATISTICS          0 rows exported
. . exporting table    REPCAT$_RESOL_STATS_CONTROL          0 rows exported
. . exporting table          REPCAT$_RUNTIME_PARMS          0 rows exported
. . exporting table              REPCAT$_SITES_NEW          0 rows exported
. . exporting table           REPCAT$_SITE_OBJECTS          0 rows exported
. . exporting table              REPCAT$_SNAPGROUP          0 rows exported
. . exporting table       REPCAT$_TEMPLATE_OBJECTS          0 rows exported
. . exporting table         REPCAT$_TEMPLATE_PARMS          0 rows exported
. . exporting table     REPCAT$_TEMPLATE_REFGROUPS          0 rows exported
. . exporting table         REPCAT$_TEMPLATE_SITES          0 rows exported
. . exporting table        REPCAT$_TEMPLATE_STATUS          3 rows exported
. . exporting table       REPCAT$_TEMPLATE_TARGETS          0 rows exported
. . exporting table         REPCAT$_TEMPLATE_TYPES          2 rows exported
. . exporting table    REPCAT$_USER_AUTHORIZATIONS          0 rows exported
. . exporting table       REPCAT$_USER_PARM_VALUES          0 rows exported
. . exporting table        SQLPLUS_PRODUCT_PROFILE          0 rows exported
. about to export OUTLN's tables via Conventional Path ...
. . exporting table                            OL$          0 rows exported
. . exporting table                       OL$HINTS          0 rows exported
. . exporting table                       OL$NODES          0 rows exported
. about to export TSMSYS's tables via Conventional Path ...
. . exporting table                           SRS$          0 rows exported
. about to export MMSG's tables via Conventional Path ...
. . exporting table                       AREAINFO        374 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX          2 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          1 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100428        736 rows exported
. . exporting table      INTERFACEACCOUNT_20100429        302 rows exported
. . exporting table      INTERFACEACCOUNT_20100430          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100501          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100502          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100503          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100504          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100505          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100506          0 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR         10 rows exported
. . exporting table                       MISCINFO          2 rows exported
. . exporting table                MISCROUTERTABLE          8 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          2 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_0        715 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_1        654 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_2        725 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_3        820 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_4        508 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_5        642 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_6        719 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_7        807 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_8        663 rows exported
. . exporting table          MMSGSVCLOG_0428_1_O_9        650 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_0        104 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_1         43 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_2         56 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_3         99 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_4         77 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_5         69 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_6         88 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_7         40 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_8         38 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_9         42 rows exported
. . exporting table        MMSGSVCLOG_20100428_1_S        976 rows exported
. . exporting table        MMSGSVCLOG_20100429_1_S         94 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         16 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          0 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          0 rows exported
. . exporting table               MONTHORDERINFO_2          1 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         24 rows exported
. . exporting table              PORTALLOG20100428         57 rows exported
. . exporting table              PORTALLOG20100429         12 rows exported
. . exporting table              PORTALLOG20100506         15 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          1 rows exported
. . exporting table                      RIGHTINFO        250 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        519 rows exported
. . exporting table                    ROUTERTABLE          5 rows exported
. . exporting table                 RPT_BUSYSERVER        198 rows exported
. . exporting table                  RPT_DELAYTIME          0 rows exported
. . exporting table         RPT_DELAYTIME_20100428        206 rows exported
. . exporting table         RPT_DELAYTIME_20100429         88 rows exported
. . exporting table         RPT_DELAYTIME_20100430          0 rows exported
. . exporting table         RPT_DELAYTIME_20100501          0 rows exported
. . exporting table         RPT_DELAYTIME_20100502          0 rows exported
. . exporting table         RPT_DELAYTIME_20100503          0 rows exported
. . exporting table         RPT_DELAYTIME_20100504          0 rows exported
. . exporting table         RPT_DELAYTIME_20100505          0 rows exported
. . exporting table         RPT_DELAYTIME_20100506          0 rows exported
. . exporting table                  RPT_INTERFACE          0 rows exported
. . exporting table         RPT_INTERFACE_20100428        359 rows exported
. . exporting table         RPT_INTERFACE_20100429         60 rows exported
. . exporting table         RPT_INTERFACE_20100430          0 rows exported
. . exporting table         RPT_INTERFACE_20100501          0 rows exported
. . exporting table         RPT_INTERFACE_20100502          0 rows exported
. . exporting table         RPT_INTERFACE_20100503          0 rows exported
. . exporting table         RPT_INTERFACE_20100504          0 rows exported
. . exporting table         RPT_INTERFACE_20100505          0 rows exported
. . exporting table         RPT_INTERFACE_20100506          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC         50 rows exported
. . exporting table                   RPT_MMSCSUCC         28 rows exported
. . exporting table              RPT_MMSC_20100428          0 rows exported
. . exporting table              RPT_MMSC_20100429          0 rows exported
. . exporting table              RPT_MMSC_20100430          0 rows exported
. . exporting table              RPT_MMSC_20100501          0 rows exported
. . exporting table              RPT_MMSC_20100502          0 rows exported
. . exporting table              RPT_MMSC_20100503          0 rows exported
. . exporting table              RPT_MMSC_20100504          0 rows exported
. . exporting table              RPT_MMSC_20100505          0 rows exported
. . exporting table              RPT_MMSC_20100506          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20100428          0 rows exported
. . exporting table              RPT_VASP_20100429          0 rows exported
. . exporting table              RPT_VASP_20100430          0 rows exported
. . exporting table              RPT_VASP_20100501          0 rows exported
. . exporting table              RPT_VASP_20100502          0 rows exported
. . exporting table              RPT_VASP_20100503          0 rows exported
. . exporting table              RPT_VASP_20100504          0 rows exported
. . exporting table              RPT_VASP_20100505          0 rows exported
. . exporting table              RPT_VASP_20100506          0 rows exported
. . exporting table        SERVICEACCOUNT_20100428         79 rows exported
. . exporting table        SERVICEACCOUNT_20100429        188 rows exported
. . exporting table        SERVICEACCOUNT_20100430          0 rows exported
. . exporting table        SERVICEACCOUNT_20100501          0 rows exported
. . exporting table        SERVICEACCOUNT_20100502          0 rows exported
. . exporting table        SERVICEACCOUNT_20100503          0 rows exported
. . exporting table        SERVICEACCOUNT_20100504          0 rows exported
. . exporting table        SERVICEACCOUNT_20100505          0 rows exported
. . exporting table        SERVICEACCOUNT_20100506          0 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        340 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          2 rows exported
. . exporting table              TMP_ATTACH_RESULT        201 rows exported
. . exporting table                TMP_BASE_RESULT         73 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO         12 rows exported
. . exporting table                  VASPLEVELINFO          2 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP         15 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                    VPNCORP_100          3 rows exported
. . exporting table                    VPNCORP_300          3 rows exported
. . exporting table                  VPNSUBSCRIBER          6 rows exported
. . exporting table                 VPNUNITECORPID          1 rows exported
. about to export MYENUM's tables via Conventional Path ...
. about to export YKLOG's tables via Conventional Path ...
. . exporting table         LOG_ROUTER201003010101          0 rows exported
. . exporting table         LOG_ROUTER201003190101        156 rows exported
. . exporting table         LOG_ROUTER201003230101         68 rows exported
. . exporting table         LOG_ROUTER201003240101        332 rows exported
. . exporting table         LOG_ROUTER201003250101        228 rows exported
. . exporting table         LOG_ROUTER201003260101         64 rows exported
. . exporting table         LOG_ROUTER201003270101        480 rows exported
. . exporting table         LOG_ROUTER201003290101       1073 rows exported
. . exporting table         LOG_ROUTER201003300101         64 rows exported
. . exporting table         LOG_ROUTER201003310101        181 rows exported
. . exporting table         LOG_ROUTER201004010101         62 rows exported
. . exporting table         LOG_ROUTER201004060101         10 rows exported
. . exporting table         LOG_ROUTER201004070101         60 rows exported
. . exporting table         LOG_ROUTER201004080101         47 rows exported
. . exporting table         LOG_ROUTER201004090101        734 rows exported
. . exporting table         LOG_ROUTER201004100101         44 rows exported
. . exporting table         LOG_ROUTER201004110101         16 rows exported
. . exporting table         LOG_ROUTER201004120101        168 rows exported
. . exporting table         LOG_ROUTER201004130101         62 rows exported
. . exporting table         LOG_ROUTER201004140101        116 rows exported
. . exporting table         LOG_ROUTER201004150101         60 rows exported
. . exporting table         LOG_ROUTER201004160101         24 rows exported
. . exporting table         LOG_ROUTER201004210101          1 rows exported
. . exporting table         LOG_ROUTER201004220101          2 rows exported
. . exporting table         LOG_ROUTER201004230101         75 rows exported
. . exporting table         LOG_ROUTER201004240101         27 rows exported
. . exporting table                   NOTIFYRESULT          0 rows exported
. . exporting table                  OPERATERESULT          0 rows exported
. . exporting table                   ROUTERRESULT         50 rows exported
. . exporting table             STATUS_CHECK_TABLE          0 rows exported
. about to export YJH's tables via Conventional Path ...
. . exporting table                  VPNCORP _9999          0 rows exported
. . exporting table                   VPNCORP_8888          0 rows exported
. . exporting table                       AREAINFO        374 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX          2 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          1 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100426        347 rows exported
. . exporting table      INTERFACEACCOUNT_20100427        633 rows exported
. . exporting table      INTERFACEACCOUNT_20100428        809 rows exported
. . exporting table      INTERFACEACCOUNT_20100429        419 rows exported
. . exporting table      INTERFACEACCOUNT_20100430        308 rows exported
. . exporting table      INTERFACEACCOUNT_20100501          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100502          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100503          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100504          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100505         61 rows exported
. . exporting table      INTERFACEACCOUNT_20100506        157 rows exported
. . exporting table      INTERFACEACCOUNT_20100507          0 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR          8 rows exported
. . exporting table                       MISCINFO          2 rows exported
. . exporting table                MISCROUTERTABLE          8 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          2 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          1 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_0         16 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_1         16 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_2          9 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_3          9 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_4          8 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_5         24 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_6         51 rows exported
. . exporting table          MMSGSVCLOG_0506_1_O_0         24 rows exported
. . exporting table          MMSGSVCLOG_0506_1_O_3          8 rows exported
. . exporting table          MMSGSVCLOG_0506_1_O_4         24 rows exported
. . exporting table          MMSGSVCLOG_0506_1_O_5         15 rows exported
. . exporting table          MMSGSVCLOG_0506_1_O_6         15 rows exported
. . exporting table          MMSGSVCLOG_0506_1_O_9          9 rows exported
. . exporting table        MMSGSVCLOG_20100505_1_S         16 rows exported
. . exporting table        MMSGSVCLOG_20100506_1_S         12 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         16 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          0 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          0 rows exported
. . exporting table               MONTHORDERINFO_2          0 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         24 rows exported
. . exporting table              PORTALLOG20100426        184 rows exported
. . exporting table              PORTALLOG20100427        330 rows exported
. . exporting table              PORTALLOG20100428        100 rows exported
. . exporting table              PORTALLOG20100429         75 rows exported
. . exporting table              PORTALLOG20100430         33 rows exported
. . exporting table              PORTALLOG20100505        104 rows exported
. . exporting table              PORTALLOG20100506          8 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          1 rows exported
. . exporting table                      RIGHTINFO        250 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        519 rows exported
. . exporting table                    ROUTERTABLE          5 rows exported
. . exporting table                 RPT_BUSYSERVER         18 rows exported
. . exporting table                  RPT_DELAYTIME          0 rows exported
. . exporting table         RPT_DELAYTIME_20100426         64 rows exported
. . exporting table         RPT_DELAYTIME_20100427        202 rows exported
. . exporting table         RPT_DELAYTIME_20100428        245 rows exported
. . exporting table         RPT_DELAYTIME_20100429        122 rows exported
. . exporting table         RPT_DELAYTIME_20100430         82 rows exported
. . exporting table         RPT_DELAYTIME_20100501          0 rows exported
. . exporting table         RPT_DELAYTIME_20100502          0 rows exported
. . exporting table         RPT_DELAYTIME_20100503          0 rows exported
. . exporting table         RPT_DELAYTIME_20100504          0 rows exported
. . exporting table         RPT_DELAYTIME_20100505         17 rows exported
. . exporting table         RPT_DELAYTIME_20100506         44 rows exported
. . exporting table         RPT_DELAYTIME_20100507          0 rows exported
. . exporting table                  RPT_INTERFACE          0 rows exported
. . exporting table         RPT_INTERFACE_20100426         10 rows exported
. . exporting table         RPT_INTERFACE_20100427        195 rows exported
. . exporting table         RPT_INTERFACE_20100428        385 rows exported
. . exporting table         RPT_INTERFACE_20100429         65 rows exported
. . exporting table         RPT_INTERFACE_20100430          0 rows exported
. . exporting table         RPT_INTERFACE_20100501          0 rows exported
. . exporting table         RPT_INTERFACE_20100502          0 rows exported
. . exporting table         RPT_INTERFACE_20100503          0 rows exported
. . exporting table         RPT_INTERFACE_20100504          0 rows exported
. . exporting table         RPT_INTERFACE_20100505          0 rows exported
. . exporting table         RPT_INTERFACE_20100506         75 rows exported
. . exporting table         RPT_INTERFACE_20100507          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC          6 rows exported
. . exporting table                   RPT_MMSCSUCC          4 rows exported
. . exporting table              RPT_MMSC_20100426          0 rows exported
. . exporting table              RPT_MMSC_20100427         26 rows exported
. . exporting table              RPT_MMSC_20100428          0 rows exported
. . exporting table              RPT_MMSC_20100429          0 rows exported
. . exporting table              RPT_MMSC_20100430          0 rows exported
. . exporting table              RPT_MMSC_20100501          0 rows exported
. . exporting table              RPT_MMSC_20100502          0 rows exported
. . exporting table              RPT_MMSC_20100503          0 rows exported
. . exporting table              RPT_MMSC_20100504          0 rows exported
. . exporting table              RPT_MMSC_20100505          0 rows exported
. . exporting table              RPT_MMSC_20100506          0 rows exported
. . exporting table              RPT_MMSC_20100507          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20100426          0 rows exported
. . exporting table              RPT_VASP_20100427         31 rows exported
. . exporting table              RPT_VASP_20100428          0 rows exported
. . exporting table              RPT_VASP_20100429          0 rows exported
. . exporting table              RPT_VASP_20100430          0 rows exported
. . exporting table              RPT_VASP_20100501          0 rows exported
. . exporting table              RPT_VASP_20100502          0 rows exported
. . exporting table              RPT_VASP_20100503          0 rows exported
. . exporting table              RPT_VASP_20100504          0 rows exported
. . exporting table              RPT_VASP_20100505          0 rows exported
. . exporting table              RPT_VASP_20100506          0 rows exported
. . exporting table              RPT_VASP_20100507          0 rows exported
. . exporting table        SERVICEACCOUNT_20100426        157 rows exported
. . exporting table        SERVICEACCOUNT_20100427        381 rows exported
. . exporting table        SERVICEACCOUNT_20100428        246 rows exported
. . exporting table        SERVICEACCOUNT_20100429        263 rows exported
. . exporting table        SERVICEACCOUNT_20100430        255 rows exported
. . exporting table        SERVICEACCOUNT_20100501          0 rows exported
. . exporting table        SERVICEACCOUNT_20100502          0 rows exported
. . exporting table        SERVICEACCOUNT_20100503          0 rows exported
. . exporting table        SERVICEACCOUNT_20100504          0 rows exported
. . exporting table        SERVICEACCOUNT_20100505         44 rows exported
. . exporting table        SERVICEACCOUNT_20100506         18 rows exported
. . exporting table        SERVICEACCOUNT_20100507          0 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        340 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          2 rows exported
. . exporting table              TMP_ATTACH_RESULT          0 rows exported
. . exporting table                TMP_BASE_RESULT          0 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO         12 rows exported
. . exporting table                  VASPLEVELINFO          2 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP         15 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                    VPNCORP_100          3 rows exported
. . exporting table                    VPNCORP_300          3 rows exported
. . exporting table                  VPNSUBSCRIBER          6 rows exported
. . exporting table                 VPNUNITECORPID          1 rows exported
. about to export WYZ's tables via Conventional Path ...
. . exporting table                       AREAINFO        374 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX          2 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          1 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091223         56 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR         10 rows exported
. . exporting table                       MISCINFO          1 rows exported
. . exporting table                MISCROUTERTABLE          7 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          2 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         16 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          0 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          0 rows exported
. . exporting table               MONTHORDERINFO_2          0 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         22 rows exported
. . exporting table              PORTALLOG20091223         26 rows exported
. . exporting table              PORTALLOG20100106          8 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          2 rows exported
. . exporting table                      RIGHTINFO        251 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        523 rows exported
. . exporting table                    ROUTERTABLE          4 rows exported
. . exporting table                 RPT_BUSYSERVER          1 rows exported
. . exporting table                  RPT_DELAYTIME          0 rows exported
. . exporting table         RPT_DELAYTIME_20091223         16 rows exported
. . exporting table                  RPT_INTERFACE          0 rows exported
. . exporting table         RPT_INTERFACE_20091223         31 rows exported
. . exporting table               RPT_MM7_VASPSUCC          2 rows exported
. . exporting table                   RPT_MMSCSUCC          2 rows exported
. . exporting table              RPT_MMSC_20091223          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20091223          0 rows exported
. . exporting table        SERVICEACCOUNT_20091223         23 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        328 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          2 rows exported
. . exporting table              TMP_ATTACH_RESULT          0 rows exported
. . exporting table                TMP_BASE_RESULT          0 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO         11 rows exported
. . exporting table                  VASPLEVELINFO          2 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP          9 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. about to export MMSC's tables via Conventional Path ...
. . exporting table               ACCESSEDADDRINFO          0 rows exported
. . exporting table                       AREAINFO        375 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX      36122 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         27 rows exported
. . exporting table              CNTADAPTRULETABLE          1 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091031          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091109          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091111          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091112          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091113          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091117          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091118          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091119          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091120          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091121          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091122          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091123          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091124          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091125          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091126          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091127          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091128          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091129          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091130          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091201          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091202          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091203          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091204          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091205          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091206          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091207          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091208          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091209          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091218          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091219          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20091220          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100111          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100119          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100120          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100121          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100122          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100123          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100124          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100125          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100129          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100130          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100131          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100201          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100202          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100203          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100205          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100206          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100207          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100208          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100209          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100210          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100211          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100212          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100213          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100214          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100215          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100216          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100217          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100218          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100219          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100220          0 rows exported
. . exporting table      DELAYTIMEACCOUNT_20100221          0 rows exported
. . exporting table               DETAILSTATUSCODE        242 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                    ENUMSRVINFO          1 rows exported
. . exporting table             EXTEMAILSERVERINFO          7 rows exported
. . exporting table           EXTEMAILSRVLEVELINFO          1 rows exported
. . exporting table                    EXTMMSCINFO          0 rows exported
. . exporting table                  GWACCOUNTINFO          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091031          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091109          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091111          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091112          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091113          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091117          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091118          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091119          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091120          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091121          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091122          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091123          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091124          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091125          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091126          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091127          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091128          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091129          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091130          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091201          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091202          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091203          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091204          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091205          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091206          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091207          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091208          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091209          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091218          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091219          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20091220          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100111          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100119          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100120          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100121          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100122          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100123          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100124          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100125          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100129          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100130          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100131          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100201          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100202          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100203          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100205          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100206          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100207          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100208          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100209          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100210          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100211          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100212          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100213          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100214          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100215          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100216          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100217          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100218          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100219          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100220          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100221          0 rows exported
. . exporting table    GWINTERFACEACCOUNT_20100222          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091031          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091109          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091111          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091112          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091113          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091117          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091118          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091119          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091120          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091121          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091122          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091123          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091124          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091125          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091126          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091127          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091128          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091129          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091130          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091201          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091202          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091203          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091204          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091205          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091206          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091207          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091208          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091209          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091218          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091219          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20091220          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100111          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100119          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100120          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100121          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100122          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100123          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100124          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100125          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100129          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100130          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100131          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100201          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100202          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100203          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100205          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100206          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100207          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100208          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100209          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100210          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100211          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100212          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100213          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100214          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100215          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100216          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100217          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100218          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100219          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100220          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100221          0 rows exported
. . exporting table      GWSERVICEACCOUNT_20100222          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table                        HOLIDAY          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091031          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091109          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091111          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091112          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091113          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091117          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091118          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091119          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091120          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091121          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091122          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091123          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091124          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091125          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091126          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091127          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091128          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091129          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091130          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091201          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091202          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091203          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091204          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091205          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091206          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091207          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091208          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091209          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091218          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091219          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20091220          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100111          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100119          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100120          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100121          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100122          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100123          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100124          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100125          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100129          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100130          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100131          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100201          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100202          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100203          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100205          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100206          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100207          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100208          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100209          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100210          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100211          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100212          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100213          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100214          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100215          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100216          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100217          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100218          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100219          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100220          0 rows exported
. . exporting table    IGDELAYTIMEACCOUNT_20100221          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091031          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091109          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091111          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091112          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091113          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091117          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091118          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091119          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091120          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091121          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091122          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091123          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091124          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091125          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091126          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091127          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091128          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091129          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091130          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091201          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091202          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091203          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091204          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091205          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091206          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091207          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091208          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091209          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091218          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091219          0 rows exported
. . exporting table      INTERFACEACCOUNT_20091220          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100111          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100119          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100120          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100121          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100122          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100123          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100124          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100125          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100129          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100130          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100131          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100201          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100202          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100203          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100205          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100206          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100207          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100208          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100209          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100210          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100211          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100212          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100213          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100214          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100215          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100216          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100217          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100218          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100219          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100220          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100221          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100222          0 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table              LIMITTIMESTRATEGY          0 rows exported
. . exporting table                 MCASSERVERINFO          1 rows exported
. . exporting table                 MCPSSERVERINFO          1 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         36 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR          9 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          4 rows exported
. . exporting table                       MMSCINFO          1 rows exported
. . exporting table                       MMSDINFO          0 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         23 rows exported
. . exporting table                        MODULES         23 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         22 rows exported
. . exporting table              NUMBERPREFIXFOR3G          0 rows exported
. . exporting table               PERSONALIZEDINFO          0 rows exported
. . exporting table                        PPGINFO          2 rows exported
. . exporting table                      PPGROUTER          1 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table               PUSHDRERRMAPPING         87 rows exported
. . exporting table                       PUSHINFO          1 rows exported
. . exporting table                 PUSHRECORDINFO          0 rows exported
. . exporting table                 RCPTSUBSCRIBER          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table               REJECTEDADDRINFO          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091031          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091109          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091111          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091112          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091113          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091117          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091118          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091119          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091120          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091121          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091122          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091123          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091124          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091125          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091126          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091127          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091128          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091129          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091130          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091201          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091202          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091203          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091204          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091205          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091206          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091207          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091208          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091209          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091218          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091219          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20091220          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100111          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100119          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100120          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100121          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100122          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100123          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100124          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100125          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100129          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100130          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100131          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100201          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100202          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100203          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100205          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100206          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100207          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100208          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100209          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100210          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100211          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100212          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100213          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100214          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100215          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100216          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100217          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100218          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100219          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100220          0 rows exported
. . exporting table    RENEWEDPHONENUMBER_20100221          0 rows exported
. . exporting table                  RENTALFEEINFO          2 rows exported
. . exporting table                REPLYCHARGEINFO          0 rows exported
. . exporting table                      RIGHTINFO        460 rows exported
. . exporting table                           ROLE          6 rows exported
. . exporting table                   ROLEMAPRIGHT        997 rows exported
. . exporting table                    ROUTERTABLE          1 rows exported
. . exporting table                 RPT_BUSYSERVER       2361 rows exported
. . exporting table                RPT_MM1_WAPSUCC          6 rows exported
. . exporting table                 RPT_MM3_ESSUCC          0 rows exported
. . exporting table               RPT_MM4_MMSCSUCC          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC         12 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table                RUBBISHMSGLIMIT          2 rows exported
. . exporting table                        SCPINFO          3 rows exported
. . exporting table                      SCPROUTER          3 rows exported
. . exporting table        SERVICEACCOUNT_20091031          0 rows exported
. . exporting table        SERVICEACCOUNT_20091109          0 rows exported
. . exporting table        SERVICEACCOUNT_20091111          0 rows exported
. . exporting table        SERVICEACCOUNT_20091112          0 rows exported
. . exporting table        SERVICEACCOUNT_20091113          0 rows exported
. . exporting table        SERVICEACCOUNT_20091117          0 rows exported
. . exporting table        SERVICEACCOUNT_20091118          0 rows exported
. . exporting table        SERVICEACCOUNT_20091119          0 rows exported
. . exporting table        SERVICEACCOUNT_20091120          0 rows exported
. . exporting table        SERVICEACCOUNT_20091121          0 rows exported
. . exporting table        SERVICEACCOUNT_20091122          0 rows exported
. . exporting table        SERVICEACCOUNT_20091123          0 rows exported
. . exporting table        SERVICEACCOUNT_20091124          0 rows exported
. . exporting table        SERVICEACCOUNT_20091125          0 rows exported
. . exporting table        SERVICEACCOUNT_20091126          0 rows exported
. . exporting table        SERVICEACCOUNT_20091127          0 rows exported
. . exporting table        SERVICEACCOUNT_20091128          0 rows exported
. . exporting table        SERVICEACCOUNT_20091129          0 rows exported
. . exporting table        SERVICEACCOUNT_20091130          0 rows exported
. . exporting table        SERVICEACCOUNT_20091201          0 rows exported
. . exporting table        SERVICEACCOUNT_20091202          0 rows exported
. . exporting table        SERVICEACCOUNT_20091203          0 rows exported
. . exporting table        SERVICEACCOUNT_20091204          0 rows exported
. . exporting table        SERVICEACCOUNT_20091205          0 rows exported
. . exporting table        SERVICEACCOUNT_20091206          0 rows exported
. . exporting table        SERVICEACCOUNT_20091207          0 rows exported
. . exporting table        SERVICEACCOUNT_20091208          0 rows exported
. . exporting table        SERVICEACCOUNT_20091209          0 rows exported
. . exporting table        SERVICEACCOUNT_20091218          0 rows exported
. . exporting table        SERVICEACCOUNT_20091219          0 rows exported
. . exporting table        SERVICEACCOUNT_20091220          0 rows exported
. . exporting table        SERVICEACCOUNT_20100111          0 rows exported
. . exporting table        SERVICEACCOUNT_20100119          0 rows exported
. . exporting table        SERVICEACCOUNT_20100120          0 rows exported
. . exporting table        SERVICEACCOUNT_20100121          0 rows exported
. . exporting table        SERVICEACCOUNT_20100122          0 rows exported
. . exporting table        SERVICEACCOUNT_20100123          0 rows exported
. . exporting table        SERVICEACCOUNT_20100124          0 rows exported
. . exporting table        SERVICEACCOUNT_20100125          0 rows exported
. . exporting table        SERVICEACCOUNT_20100129          0 rows exported
. . exporting table        SERVICEACCOUNT_20100130          0 rows exported
. . exporting table        SERVICEACCOUNT_20100131          0 rows exported
. . exporting table        SERVICEACCOUNT_20100201          0 rows exported
. . exporting table        SERVICEACCOUNT_20100202          0 rows exported
. . exporting table        SERVICEACCOUNT_20100203          0 rows exported
. . exporting table        SERVICEACCOUNT_20100205          0 rows exported
. . exporting table        SERVICEACCOUNT_20100206          0 rows exported
. . exporting table        SERVICEACCOUNT_20100207          0 rows exported
. . exporting table        SERVICEACCOUNT_20100208          0 rows exported
. . exporting table        SERVICEACCOUNT_20100209          0 rows exported
. . exporting table        SERVICEACCOUNT_20100210          0 rows exported
. . exporting table        SERVICEACCOUNT_20100211          0 rows exported
. . exporting table        SERVICEACCOUNT_20100212          0 rows exported
. . exporting table        SERVICEACCOUNT_20100213          0 rows exported
. . exporting table        SERVICEACCOUNT_20100214          0 rows exported
. . exporting table        SERVICEACCOUNT_20100215          0 rows exported
. . exporting table        SERVICEACCOUNT_20100216          0 rows exported
. . exporting table        SERVICEACCOUNT_20100217          0 rows exported
. . exporting table        SERVICEACCOUNT_20100218          0 rows exported
. . exporting table        SERVICEACCOUNT_20100219          0 rows exported
. . exporting table        SERVICEACCOUNT_20100220          0 rows exported
. . exporting table        SERVICEACCOUNT_20100221          0 rows exported
. . exporting table        SERVICEACCOUNT_20100222          0 rows exported
. . exporting table                    SMSNOTEINFO         35 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                    SMTPSTSINFO          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        132 rows exported
. . exporting table                     SUBSCRIBER          4 rows exported
. . exporting table                   SUBSNUMGROUP          0 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        523 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          0 rows exported
. . exporting table              TMP_ATTACH_RESULT          0 rows exported
. . exporting table                TMP_BASE_RESULT          0 rows exported
. . exporting table            TMP_USERPHONENUMBER          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                     USERBWLIST          0 rows exported
. . exporting table                USERPHONENUMBER          0 rows exported
. . exporting table                VASDELIVERGROUP          0 rows exported
. . exporting table                   VASLOCALLIST          0 rows exported
. . exporting table                       VASPINFO          1 rows exported
. . exporting table                  VASPLEVELINFO          1 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICEINFO          1 rows exported
. . exporting table                VASPSERVICE_SUP          7 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table                  VASSWITCHINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                      WAPGWINFO         25 rows exported
. . exporting table                WHITENOTIFYLIST          0 rows exported
. about to export ZJUN's tables via Conventional Path ...
. . exporting table                       AREAINFO        374 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX          2 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          1 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100406          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100427         97 rows exported
. . exporting table      INTERFACEACCOUNT_20100428          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100429        100 rows exported
. . exporting table      INTERFACEACCOUNT_20100430        198 rows exported
. . exporting table      INTERFACEACCOUNT_20100501          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100502          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100503          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100504          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100505          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100506          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100507          0 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR          8 rows exported
. . exporting table                       MISCINFO          2 rows exported
. . exporting table                MISCROUTERTABLE          9 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          2 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_0         15 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_1         59 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_3         74 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_4         24 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_5          9 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_6         24 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_7          5 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_8         40 rows exported
. . exporting table          MMSGSVCLOG_0427_1_O_9         95 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_0         18 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_1         27 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_5         11 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_6         37 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_7         24 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_8          9 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_9         20 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_0        194 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_1        121 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_2        297 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_3        306 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_4        224 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_5        191 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_6        190 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_7        101 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_8        135 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_9        212 rows exported
. . exporting table        MMSGSVCLOG_20100427_1_S         59 rows exported
. . exporting table        MMSGSVCLOG_20100429_1_S         14 rows exported
. . exporting table        MMSGSVCLOG_20100430_1_S        173 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         17 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          0 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          0 rows exported
. . exporting table               MONTHORDERINFO_2          0 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         24 rows exported
. . exporting table              PORTALLOG20100427         79 rows exported
. . exporting table              PORTALLOG20100429         31 rows exported
. . exporting table              PORTALLOG20100430          8 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          1 rows exported
. . exporting table                      RIGHTINFO        249 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        518 rows exported
. . exporting table                    ROUTERTABLE          5 rows exported
. . exporting table                 RPT_BUSYSERVER        184 rows exported
. . exporting table                  RPT_DELAYTIME         37 rows exported
. . exporting table         RPT_DELAYTIME_20100505          0 rows exported
. . exporting table         RPT_DELAYTIME_20100506          0 rows exported
. . exporting table         RPT_DELAYTIME_20100507          0 rows exported
. . exporting table                  RPT_INTERFACE         14 rows exported
. . exporting table         RPT_INTERFACE_20100505          0 rows exported
. . exporting table         RPT_INTERFACE_20100506          0 rows exported
. . exporting table         RPT_INTERFACE_20100507          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC         16 rows exported
. . exporting table                   RPT_MMSCSUCC         14 rows exported
. . exporting table              RPT_MMSC_20100406          0 rows exported
. . exporting table              RPT_MMSC_20100427          0 rows exported
. . exporting table              RPT_MMSC_20100428          0 rows exported
. . exporting table              RPT_MMSC_20100429          0 rows exported
. . exporting table              RPT_MMSC_20100430          0 rows exported
. . exporting table              RPT_MMSC_20100501          0 rows exported
. . exporting table              RPT_MMSC_20100502          0 rows exported
. . exporting table              RPT_MMSC_20100503          0 rows exported
. . exporting table              RPT_MMSC_20100504          0 rows exported
. . exporting table              RPT_MMSC_20100505          0 rows exported
. . exporting table              RPT_MMSC_20100506          0 rows exported
. . exporting table              RPT_MMSC_20100507          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20100406          0 rows exported
. . exporting table              RPT_VASP_20100427          0 rows exported
. . exporting table              RPT_VASP_20100428          0 rows exported
. . exporting table              RPT_VASP_20100429          0 rows exported
. . exporting table              RPT_VASP_20100430          0 rows exported
. . exporting table              RPT_VASP_20100501          0 rows exported
. . exporting table              RPT_VASP_20100502          0 rows exported
. . exporting table              RPT_VASP_20100503          0 rows exported
. . exporting table              RPT_VASP_20100504          0 rows exported
. . exporting table              RPT_VASP_20100505          0 rows exported
. . exporting table              RPT_VASP_20100506          0 rows exported
. . exporting table              RPT_VASP_20100507          0 rows exported
. . exporting table        SERVICEACCOUNT_20100406          0 rows exported
. . exporting table        SERVICEACCOUNT_20100427         56 rows exported
. . exporting table        SERVICEACCOUNT_20100428          0 rows exported
. . exporting table        SERVICEACCOUNT_20100429         53 rows exported
. . exporting table        SERVICEACCOUNT_20100430        114 rows exported
. . exporting table        SERVICEACCOUNT_20100501          0 rows exported
. . exporting table        SERVICEACCOUNT_20100502          0 rows exported
. . exporting table        SERVICEACCOUNT_20100503          0 rows exported
. . exporting table        SERVICEACCOUNT_20100504          0 rows exported
. . exporting table        SERVICEACCOUNT_20100505          0 rows exported
. . exporting table        SERVICEACCOUNT_20100506          0 rows exported
. . exporting table        SERVICEACCOUNT_20100507          0 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        336 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          2 rows exported
. . exporting table              TMP_ATTACH_RESULT          0 rows exported
. . exporting table                TMP_BASE_RESULT          0 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO         13 rows exported
. . exporting table                  VASPLEVELINFO          2 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP         15 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                    VPNCORP_100          3 rows exported
. . exporting table                    VPNCORP_300          3 rows exported
. . exporting table                  VPNSUBSCRIBER          6 rows exported
. . exporting table                 VPNUNITECORPID          1 rows exported
. about to export AUTOTEST's tables via Conventional Path ...
. . exporting table                       AREAINFO        374 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX      36158 rows exported
. . exporting table                 AREANUMBER_BAK        728 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          5 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100202        332 rows exported
. . exporting table      INTERFACEACCOUNT_20100203         28 rows exported
. . exporting table      INTERFACEACCOUNT_20100204        102 rows exported
. . exporting table      INTERFACEACCOUNT_20100205         15 rows exported
. . exporting table      INTERFACEACCOUNT_20100206          7 rows exported
. . exporting table      INTERFACEACCOUNT_20100207          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100208          4 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR         15 rows exported
. . exporting table                       MISCINFO          1 rows exported
. . exporting table                MISCROUTERTABLE          1 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          1 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_0        256 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_1        238 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_2        308 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_3        406 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_4        160 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_5        352 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_6        276 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_7        322 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_8        296 rows exported
. . exporting table          MMSGSVCLOG_0202_1_O_9        428 rows exported
. . exporting table          MMSGSVCLOG_0203_1_O_4         18 rows exported
. . exporting table          MMSGSVCLOG_0203_1_O_6         18 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_1         20 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_2         38 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_3         18 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_4         46 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_5         36 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_6         18 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_7         20 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_8         88 rows exported
. . exporting table          MMSGSVCLOG_0204_1_O_9         28 rows exported
. . exporting table        MMSGSVCLOG_20100202_1_S        536 rows exported
. . exporting table        MMSGSVCLOG_20100203_1_S          4 rows exported
. . exporting table        MMSGSVCLOG_20100204_1_S         42 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         16 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          0 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          0 rows exported
. . exporting table               MONTHORDERINFO_2          0 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         24 rows exported
. . exporting table                NETWORKCODE_BAK         44 rows exported
. . exporting table              PORTALLOG20100202        124 rows exported
. . exporting table              PORTALLOG20100203        158 rows exported
. . exporting table              PORTALLOG20100204        242 rows exported
. . exporting table              PORTALLOG20100205         42 rows exported
. . exporting table              PORTALLOG20100208         74 rows exported
. . exporting table              PORTALLOG20100209         52 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          2 rows exported
. . exporting table                      RIGHTINFO        247 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        515 rows exported
. . exporting table                    ROUTERTABLE          4 rows exported
. . exporting table                 RPT_BUSYSERVER        107 rows exported
. . exporting table                  RPT_DELAYTIME          0 rows exported
. . exporting table         RPT_DELAYTIME_20100202         66 rows exported
. . exporting table         RPT_DELAYTIME_20100203         12 rows exported
. . exporting table         RPT_DELAYTIME_20100204         34 rows exported
. . exporting table         RPT_DELAYTIME_20100205          5 rows exported
. . exporting table         RPT_DELAYTIME_20100206          1 rows exported
. . exporting table         RPT_DELAYTIME_20100207          0 rows exported
. . exporting table         RPT_DELAYTIME_20100208          1 rows exported
. . exporting table                  RPT_INTERFACE          0 rows exported
. . exporting table         RPT_INTERFACE_20100202         75 rows exported
. . exporting table         RPT_INTERFACE_20100203         12 rows exported
. . exporting table         RPT_INTERFACE_20100204         30 rows exported
. . exporting table         RPT_INTERFACE_20100205          0 rows exported
. . exporting table         RPT_INTERFACE_20100206          1 rows exported
. . exporting table         RPT_INTERFACE_20100207          0 rows exported
. . exporting table         RPT_INTERFACE_20100208          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC         10 rows exported
. . exporting table                   RPT_MMSCSUCC         22 rows exported
. . exporting table              RPT_MMSC_20100202          0 rows exported
. . exporting table              RPT_MMSC_20100203          0 rows exported
. . exporting table              RPT_MMSC_20100204          0 rows exported
. . exporting table              RPT_MMSC_20100205          0 rows exported
. . exporting table              RPT_MMSC_20100206          0 rows exported
. . exporting table              RPT_MMSC_20100207          0 rows exported
. . exporting table              RPT_MMSC_20100208          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20100202          0 rows exported
. . exporting table              RPT_VASP_20100203          0 rows exported
. . exporting table              RPT_VASP_20100204          0 rows exported
. . exporting table              RPT_VASP_20100205          0 rows exported
. . exporting table              RPT_VASP_20100206          0 rows exported
. . exporting table              RPT_VASP_20100207          0 rows exported
. . exporting table              RPT_VASP_20100208          0 rows exported
. . exporting table        SERVICEACCOUNT_20100202        131 rows exported
. . exporting table        SERVICEACCOUNT_20100203         20 rows exported
. . exporting table        SERVICEACCOUNT_20100204         66 rows exported
. . exporting table        SERVICEACCOUNT_20100205          5 rows exported
. . exporting table        SERVICEACCOUNT_20100206          6 rows exported
. . exporting table        SERVICEACCOUNT_20100207          0 rows exported
. . exporting table        SERVICEACCOUNT_20100208          4 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        333 rows exported
. . exporting table            SYSTEMPARAMETER_BAK        664 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          0 rows exported
. . exporting table              TMP_ATTACH_RESULT        196 rows exported
. . exporting table                TMP_BASE_RESULT        228 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO          1 rows exported
. . exporting table                  VASPLEVELINFO          1 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP          6 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                    VPNCORP_100          3 rows exported
. . exporting table                    VPNCORP_300          3 rows exported
. . exporting table                  VPNSUBSCRIBER          0 rows exported
. . exporting table                 VPNUNITECORPID          0 rows exported
. about to export AIXTEST's tables via Conventional Path ...
. . exporting table                       AREAINFO        374 rows exported
. . exporting table                   AREAINFO_BAK        748 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX          3 rows exported
. . exporting table                 AREANUMBER_BAK        728 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          1 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100324         72 rows exported
. . exporting table      INTERFACEACCOUNT_20100325        263 rows exported
. . exporting table      INTERFACEACCOUNT_20100326        120 rows exported
. . exporting table      INTERFACEACCOUNT_20100327        359 rows exported
. . exporting table      INTERFACEACCOUNT_20100328        113 rows exported
. . exporting table      INTERFACEACCOUNT_20100329        123 rows exported
. . exporting table      INTERFACEACCOUNT_20100330        751 rows exported
. . exporting table      INTERFACEACCOUNT_20100331        843 rows exported
. . exporting table      INTERFACEACCOUNT_20100401          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100402         42 rows exported
. . exporting table      INTERFACEACCOUNT_20100403          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100404          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100405          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100406          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100407          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100416         86 rows exported
. . exporting table      INTERFACEACCOUNT_20100417          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100420          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100421          0 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR         13 rows exported
. . exporting table                       MISCINFO          2 rows exported
. . exporting table                MISCROUTERTABLE          8 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          2 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_0         92 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_1         46 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_2         60 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_3         16 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_4         46 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_5         46 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_6         48 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_7         20 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_8         78 rows exported
. . exporting table          MMSGSVCLOG_0324_1_O_9        138 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_0        116 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_1         58 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_2         50 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_3         74 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_4         78 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_5         80 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_6         96 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_7         28 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_8         58 rows exported
. . exporting table          MMSGSVCLOG_0325_1_O_9        112 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_0        192 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_1        296 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_2        272 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_3        226 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_4        178 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_5        230 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_6        284 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_7        282 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_8        258 rows exported
. . exporting table          MMSGSVCLOG_0326_1_O_9        238 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_0       2450 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_1       2176 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_2       2734 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_3       2702 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_4       3590 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_5       3924 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_6       3432 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_7       2946 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_8       2482 rows exported
. . exporting table          MMSGSVCLOG_0327_1_O_9       2118 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_0       1614 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_1       1360 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_2       1390 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_3       1684 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_4       1598 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_5       1814 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_6       1758 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_7       1624 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_8       1386 rows exported
. . exporting table          MMSGSVCLOG_0328_1_O_9       1454 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_0       1250 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_1       1344 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_2       1367 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_3       1399 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_4       1208 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_5       1385 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_6       1351 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_7       1630 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_8       1420 rows exported
. . exporting table          MMSGSVCLOG_0329_1_O_9       1267 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_0       1545 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_1       1706 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_2       1470 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_3       1309 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_4       1219 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_5       1456 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_6       1384 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_7       1539 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_8       1401 rows exported
. . exporting table          MMSGSVCLOG_0330_1_O_9       1540 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_0      17978 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_1      18403 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_2      18454 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_3      18122 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_4      17853 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_5      17472 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_6      17510 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_7      17667 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_8      18157 rows exported
. . exporting table          MMSGSVCLOG_0331_1_O_9      18110 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_0         78 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_1        143 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_2         57 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_3         39 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_4         56 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_5        192 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_6         87 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_7        135 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_8        155 rows exported
. . exporting table          MMSGSVCLOG_0401_1_O_9        103 rows exported
. . exporting table          MMSGSVCLOG_0402_1_O_2         36 rows exported
. . exporting table          MMSGSVCLOG_0402_1_O_3         42 rows exported
. . exporting table          MMSGSVCLOG_0402_1_O_6         16 rows exported
. . exporting table          MMSGSVCLOG_0402_1_O_8         16 rows exported
. . exporting table        MMSGSVCLOG_20100324_1_S         86 rows exported
. . exporting table        MMSGSVCLOG_20100325_1_S        108 rows exported
. . exporting table        MMSGSVCLOG_20100326_1_S        404 rows exported
. . exporting table        MMSGSVCLOG_20100327_1_S       4118 rows exported
. . exporting table        MMSGSVCLOG_20100328_1_S       2322 rows exported
. . exporting table        MMSGSVCLOG_20100329_1_S       2076 rows exported
. . exporting table        MMSGSVCLOG_20100330_1_S       2241 rows exported
. . exporting table        MMSGSVCLOG_20100331_1_S      23131 rows exported
. . exporting table        MMSGSVCLOG_20100401_1_S        168 rows exported
. . exporting table        MMSGSVCLOG_20100402_1_S         16 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         16 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          0 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          0 rows exported
. . exporting table               MONTHORDERINFO_2          0 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         24 rows exported
. . exporting table                NETWORKCODE_BAK         44 rows exported
. . exporting table              PORTALLOG20100323         22 rows exported
. . exporting table              PORTALLOG20100324         66 rows exported
. . exporting table              PORTALLOG20100325        200 rows exported
. . exporting table              PORTALLOG20100326         74 rows exported
. . exporting table              PORTALLOG20100327        164 rows exported
. . exporting table              PORTALLOG20100329        176 rows exported
. . exporting table              PORTALLOG20100330        133 rows exported
. . exporting table              PORTALLOG20100331         90 rows exported
. . exporting table              PORTALLOG20100402         64 rows exported
. . exporting table              PORTALLOG20100416         32 rows exported
. . exporting table              PORTALLOG20100420         30 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          1 rows exported
. . exporting table                      RIGHTINFO        250 rows exported
. . exporting table                  RIGHTINFO_BAK        494 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        519 rows exported
. . exporting table               ROLEMAPRIGHT_BAK       1030 rows exported
. . exporting table                    ROUTERTABLE          5 rows exported
. . exporting table                 RPT_BUSYSERVER         56 rows exported
. . exporting table                  RPT_DELAYTIME          0 rows exported
. . exporting table         RPT_DELAYTIME_20100324         24 rows exported
. . exporting table         RPT_DELAYTIME_20100325         86 rows exported
. . exporting table         RPT_DELAYTIME_20100326         36 rows exported
. . exporting table         RPT_DELAYTIME_20100327        122 rows exported
. . exporting table         RPT_DELAYTIME_20100328         40 rows exported
. . exporting table         RPT_DELAYTIME_20100329         37 rows exported
. . exporting table         RPT_DELAYTIME_20100330        246 rows exported
. . exporting table         RPT_DELAYTIME_20100331        242 rows exported
. . exporting table         RPT_DELAYTIME_20100401          0 rows exported
. . exporting table         RPT_DELAYTIME_20100402         11 rows exported
. . exporting table         RPT_DELAYTIME_20100403          0 rows exported
. . exporting table         RPT_DELAYTIME_20100404          0 rows exported
. . exporting table         RPT_DELAYTIME_20100405          0 rows exported
. . exporting table         RPT_DELAYTIME_20100406          0 rows exported
. . exporting table         RPT_DELAYTIME_20100407          0 rows exported
. . exporting table         RPT_DELAYTIME_20100416         18 rows exported
. . exporting table         RPT_DELAYTIME_20100417          0 rows exported
. . exporting table         RPT_DELAYTIME_20100420          0 rows exported
. . exporting table         RPT_DELAYTIME_20100421          0 rows exported
. . exporting table                  RPT_INTERFACE          0 rows exported
. . exporting table         RPT_INTERFACE_20100324         36 rows exported
. . exporting table         RPT_INTERFACE_20100325        116 rows exported
. . exporting table         RPT_INTERFACE_20100326         40 rows exported
. . exporting table         RPT_INTERFACE_20100327        203 rows exported
. . exporting table         RPT_INTERFACE_20100328         63 rows exported
. . exporting table         RPT_INTERFACE_20100329         44 rows exported
. . exporting table         RPT_INTERFACE_20100330        456 rows exported
. . exporting table         RPT_INTERFACE_20100331        229 rows exported
. . exporting table         RPT_INTERFACE_20100401          0 rows exported
. . exporting table         RPT_INTERFACE_20100402         16 rows exported
. . exporting table         RPT_INTERFACE_20100403          0 rows exported
. . exporting table         RPT_INTERFACE_20100404          0 rows exported
. . exporting table         RPT_INTERFACE_20100405          0 rows exported
. . exporting table         RPT_INTERFACE_20100406          0 rows exported
. . exporting table         RPT_INTERFACE_20100407          0 rows exported
. . exporting table         RPT_INTERFACE_20100416         52 rows exported
. . exporting table         RPT_INTERFACE_20100417          0 rows exported
. . exporting table         RPT_INTERFACE_20100420          0 rows exported
. . exporting table         RPT_INTERFACE_20100421          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC          6 rows exported
. . exporting table                   RPT_MMSCSUCC          8 rows exported
. . exporting table              RPT_MMSC_20100324          0 rows exported
. . exporting table              RPT_MMSC_20100325          0 rows exported
. . exporting table              RPT_MMSC_20100326          0 rows exported
. . exporting table              RPT_MMSC_20100327          0 rows exported
. . exporting table              RPT_MMSC_20100328          0 rows exported
. . exporting table              RPT_MMSC_20100329          0 rows exported
. . exporting table              RPT_MMSC_20100330          0 rows exported
. . exporting table              RPT_MMSC_20100331          0 rows exported
. . exporting table              RPT_MMSC_20100401          0 rows exported
. . exporting table              RPT_MMSC_20100402          0 rows exported
. . exporting table              RPT_MMSC_20100403          0 rows exported
. . exporting table              RPT_MMSC_20100404          0 rows exported
. . exporting table              RPT_MMSC_20100405          0 rows exported
. . exporting table              RPT_MMSC_20100406          0 rows exported
. . exporting table              RPT_MMSC_20100407          0 rows exported
. . exporting table              RPT_MMSC_20100416          0 rows exported
. . exporting table              RPT_MMSC_20100417          0 rows exported
. . exporting table              RPT_MMSC_20100420          0 rows exported
. . exporting table              RPT_MMSC_20100421          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20100324          0 rows exported
. . exporting table              RPT_VASP_20100325          0 rows exported
. . exporting table              RPT_VASP_20100326          0 rows exported
. . exporting table              RPT_VASP_20100327          0 rows exported
. . exporting table              RPT_VASP_20100328          0 rows exported
. . exporting table              RPT_VASP_20100329          0 rows exported
. . exporting table              RPT_VASP_20100330          0 rows exported
. . exporting table              RPT_VASP_20100331          0 rows exported
. . exporting table              RPT_VASP_20100401          0 rows exported
. . exporting table              RPT_VASP_20100402          0 rows exported
. . exporting table              RPT_VASP_20100403          0 rows exported
. . exporting table              RPT_VASP_20100404          0 rows exported
. . exporting table              RPT_VASP_20100405          0 rows exported
. . exporting table              RPT_VASP_20100406          0 rows exported
. . exporting table              RPT_VASP_20100407          0 rows exported
. . exporting table              RPT_VASP_20100416          0 rows exported
. . exporting table              RPT_VASP_20100417          0 rows exported
. . exporting table              RPT_VASP_20100420          0 rows exported
. . exporting table              RPT_VASP_20100421          0 rows exported
. . exporting table        SERVICEACCOUNT_20100324         48 rows exported
. . exporting table        SERVICEACCOUNT_20100325        117 rows exported
. . exporting table        SERVICEACCOUNT_20100326         65 rows exported
. . exporting table        SERVICEACCOUNT_20100327        200 rows exported
. . exporting table        SERVICEACCOUNT_20100328         71 rows exported
. . exporting table        SERVICEACCOUNT_20100329         96 rows exported
. . exporting table        SERVICEACCOUNT_20100330        204 rows exported
. . exporting table        SERVICEACCOUNT_20100331        516 rows exported
. . exporting table        SERVICEACCOUNT_20100401          0 rows exported
. . exporting table        SERVICEACCOUNT_20100402         19 rows exported
. . exporting table        SERVICEACCOUNT_20100403          0 rows exported
. . exporting table        SERVICEACCOUNT_20100404          0 rows exported
. . exporting table        SERVICEACCOUNT_20100405          0 rows exported
. . exporting table        SERVICEACCOUNT_20100406          0 rows exported
. . exporting table        SERVICEACCOUNT_20100407          0 rows exported
. . exporting table        SERVICEACCOUNT_20100416         33 rows exported
. . exporting table        SERVICEACCOUNT_20100417          0 rows exported
. . exporting table        SERVICEACCOUNT_20100420          0 rows exported
. . exporting table        SERVICEACCOUNT_20100421          0 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        340 rows exported
. . exporting table            SYSTEMPARAMETER_BAK        662 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          2 rows exported
. . exporting table              TMP_ATTACH_RESULT          0 rows exported
. . exporting table                TMP_BASE_RESULT          0 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO         12 rows exported
. . exporting table                  VASPLEVELINFO          2 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP         15 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                    VPNCORP_100          3 rows exported
. . exporting table                    VPNCORP_300          3 rows exported
. . exporting table                  VPNSUBSCRIBER          6 rows exported
. . exporting table                 VPNUNITECORPID          1 rows exported
. about to export CHYJ's tables via Conventional Path ...
. . exporting table                       AREAINFO        374 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX      36158 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         21 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          5 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100421          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100422          0 rows exported
. . exporting table                    INTERPREFIX         21 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR         10 rows exported
. . exporting table                       MISCINFO          0 rows exported
. . exporting table                MISCROUTERTABLE          0 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          1 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         16 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          0 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          0 rows exported
. . exporting table               MONTHORDERINFO_2          0 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         24 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          1 rows exported
. . exporting table                      RIGHTINFO        250 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        519 rows exported
. . exporting table                    ROUTERTABLE          2 rows exported
. . exporting table                 RPT_BUSYSERVER         19 rows exported
. . exporting table                  RPT_DELAYTIME          0 rows exported
. . exporting table         RPT_DELAYTIME_20100421          0 rows exported
. . exporting table         RPT_DELAYTIME_20100422          0 rows exported
. . exporting table                  RPT_INTERFACE          0 rows exported
. . exporting table         RPT_INTERFACE_20100421          0 rows exported
. . exporting table         RPT_INTERFACE_20100422          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC          0 rows exported
. . exporting table                   RPT_MMSCSUCC          0 rows exported
. . exporting table              RPT_MMSC_20100421          0 rows exported
. . exporting table              RPT_MMSC_20100422          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20100421          0 rows exported
. . exporting table              RPT_VASP_20100422          0 rows exported
. . exporting table        SERVICEACCOUNT_20100421          0 rows exported
. . exporting table        SERVICEACCOUNT_20100422          0 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         13 rows exported
. . exporting table                SYSTEMPARAMETER        340 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          0 rows exported
. . exporting table              TMP_ATTACH_RESULT          0 rows exported
. . exporting table                TMP_BASE_RESULT          0 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO          1 rows exported
. . exporting table                  VASPLEVELINFO          1 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP          6 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                  VPNSUBSCRIBER          0 rows exported
. . exporting table                 VPNUNITECORPID          0 rows exported
. about to export SYC's tables via Conventional Path ...
. . exporting table                       AREAINFO        375 rows exported
. . exporting table                     AREANUMBER        364 rows exported
. . exporting table               AREANUMBERPREFIX          4 rows exported
. . exporting table                BEARERVALUELIST          3 rows exported
. . exporting table                    CARRIERINFO          1 rows exported
. . exporting table               CHARGINGKPCONFIG         28 rows exported
. . exporting table                 CONNECTIONINFO          0 rows exported
. . exporting table                    COUNTRYCODE         22 rows exported
. . exporting table             DATAFILESTATUSCODE          0 rows exported
. . exporting table               DETAILSTATUSCODE        247 rows exported
. . exporting table                     DNSSRVINFO          0 rows exported
. . exporting table                  DRMACCESSCODE          0 rows exported
. . exporting table                     ECTOSIINFO          0 rows exported
. . exporting table                    ENUMSRVINFO          1 rows exported
. . exporting table                  EXP_CACHESTAT          0 rows exported
. . exporting table                    HISTORYFLOW          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100428         37 rows exported
. . exporting table      INTERFACEACCOUNT_20100429        374 rows exported
. . exporting table      INTERFACEACCOUNT_20100430        135 rows exported
. . exporting table      INTERFACEACCOUNT_20100501          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100502          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100503          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100504          0 rows exported
. . exporting table      INTERFACEACCOUNT_20100505        103 rows exported
. . exporting table      INTERFACEACCOUNT_20100506          6 rows exported
. . exporting table      INTERFACEACCOUNT_20100507          0 rows exported
. . exporting table      INTERFACEACCOUNT_20101027        320 rows exported
. . exporting table                    INTERPREFIX         22 rows exported
. . exporting table               IPRANGEPARTITION         93 rows exported
. . exporting table                        MESSAGE          0 rows exported
. . exporting table               MESSAGEREFERENCE          0 rows exported
. . exporting table            MESSAGESENDSCHEDULE         15 rows exported
. . exporting table                     MIBLEAFINT         79 rows exported
. . exporting table                     MIBLEAFSTR          9 rows exported
. . exporting table                       MISCINFO          2 rows exported
. . exporting table                MISCROUTERTABLE          7 rows exported
. . exporting table                      MMBOXTYPE          5 rows exported
. . exporting table           MMINTERFACELEVELINFO          2 rows exported
. . exporting table                       MMSCINFO          2 rows exported
. . exporting table                     MMSCIPINFO          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP00          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP01          1 rows exported
. . exporting table             MMSGMMSCMSGIDMAP02          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP03          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP04          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP05          1 rows exported
. . exporting table             MMSGMMSCMSGIDMAP06          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP07          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP08          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP09          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP10          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP11          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP12          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP13          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP14          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP15          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP16          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP17          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP18          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP19          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP20          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP21          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP22          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP23          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP24          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP25          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP26          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP27          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP28          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP29          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP30          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP31          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP32          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP33          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP34          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP35          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP36          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP37          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP38          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP39          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP40          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP41          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP42          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP43          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP44          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP45          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP46          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP47          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP48          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP49          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP50          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP51          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP52          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP53          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP54          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP55          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP56          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP57          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP58          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP59          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP60          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP61          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP62          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP63          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP64          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP65          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP66          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP67          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP68          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP69          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP70          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP71          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP72          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP73          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP74          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP75          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP76          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP77          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP78          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP79          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP80          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP81          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP82          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP83          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP84          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP85          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP86          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP87          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP88          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP89          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP90          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP91          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP92          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP93          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP94          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP95          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP96          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP97          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP98          0 rows exported
. . exporting table             MMSGMMSCMSGIDMAP99          0 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_0         48 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_1        115 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_2         80 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_3         74 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_4         83 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_5        104 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_6        131 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_7        123 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_8        141 rows exported
. . exporting table          MMSGSVCLOG_0429_1_O_9         63 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_0       1209 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_1       1208 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_2       1253 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_3       1272 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_4       1309 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_5       1377 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_6       1358 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_7       1386 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_8       1343 rows exported
. . exporting table          MMSGSVCLOG_0430_1_O_9       1381 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_0         23 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_1         50 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_2         26 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_3         45 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_4         23 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_5         35 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_6         17 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_7         23 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_8         36 rows exported
. . exporting table          MMSGSVCLOG_0505_1_O_9         18 rows exported
. . exporting table          MMSGSVCLOG_0506_1_O_3          5 rows exported
. . exporting table        MMSGSVCLOG_20100429_1_S         95 rows exported
. . exporting table        MMSGSVCLOG_20100430_1_S       2306 rows exported
. . exporting table        MMSGSVCLOG_20100505_1_S         35 rows exported
. . exporting table        MMSGSVCLOG_20100506_1_S          1 rows exported
. . exporting table        MMSGSVCLOG_20101027_1_S        159 rows exported
. . exporting table                      MMSTARIFF          1 rows exported
. . exporting table                      MODULECMD         18 rows exported
. . exporting table                        MODULES         17 rows exported
. . exporting table                 MONITOREDUSERS          0 rows exported
. . exporting table                MONITORPERFSTAT          1 rows exported
. . exporting table               MONTHORDERINFO_0          0 rows exported
. . exporting table               MONTHORDERINFO_1          2 rows exported
. . exporting table               MONTHORDERINFO_2          1 rows exported
. . exporting table               MONTHORDERINFO_3          0 rows exported
. . exporting table               MONTHORDERINFO_4          0 rows exported
. . exporting table               MONTHORDERINFO_5          0 rows exported
. . exporting table               MONTHORDERINFO_6          0 rows exported
. . exporting table               MONTHORDERINFO_7          0 rows exported
. . exporting table               MONTHORDERINFO_8          0 rows exported
. . exporting table               MONTHORDERINFO_9          0 rows exported
. . exporting table                   NATIVEPREFIX          1 rows exported
. . exporting table                    NETWORKCODE         24 rows exported
. . exporting table              PORTALLOG20100428         86 rows exported
. . exporting table              PORTALLOG20100429        121 rows exported
. . exporting table              PORTALLOG20100430         49 rows exported
. . exporting table              PORTALLOG20100505        114 rows exported
. . exporting table              PORTALLOG20100506        184 rows exported
. . exporting table                PPSNUMBERPREFIX          0 rows exported
. . exporting table                PROHIBITEDRIGHT          0 rows exported
. . exporting table                   REALTIMEFLOW          0 rows exported
. . exporting table                  RENTALFEEINFO          1 rows exported
. . exporting table                      RIGHTINFO        250 rows exported
. . exporting table                           ROLE          4 rows exported
. . exporting table                   ROLEMAPRIGHT        519 rows exported
. . exporting table                    ROUTERTABLE          3 rows exported
. . exporting table                 RPT_BUSYSERVER        214 rows exported
. . exporting table                  RPT_DELAYTIME        105 rows exported
. . exporting table         RPT_DELAYTIME_20100506          1 rows exported
. . exporting table         RPT_DELAYTIME_20100507          0 rows exported
. . exporting table                  RPT_INTERFACE         85 rows exported
. . exporting table         RPT_INTERFACE_20100507          0 rows exported
. . exporting table               RPT_MM7_VASPSUCC         40 rows exported
. . exporting table                   RPT_MMSCSUCC         30 rows exported
. . exporting table              RPT_MMSC_20100428          0 rows exported
. . exporting table              RPT_MMSC_20100429          0 rows exported
. . exporting table              RPT_MMSC_20100430          0 rows exported
. . exporting table              RPT_MMSC_20100501          0 rows exported
. . exporting table              RPT_MMSC_20100502          0 rows exported
. . exporting table              RPT_MMSC_20100503          0 rows exported
. . exporting table              RPT_MMSC_20100504          0 rows exported
. . exporting table              RPT_MMSC_20100505          0 rows exported
. . exporting table              RPT_MMSC_20100506          0 rows exported
. . exporting table              RPT_MMSC_20100507          0 rows exported
. . exporting table              RPT_MMSC_20101027          0 rows exported
. . exporting table              RPT_TERMINALCOUNT          0 rows exported
. . exporting table                   RPT_USECOUNT          0 rows exported
. . exporting table              RPT_USEOFSPSERVER          0 rows exported
. . exporting table              RPT_VASP_20100428          0 rows exported
. . exporting table              RPT_VASP_20100429          0 rows exported
. . exporting table              RPT_VASP_20100430          0 rows exported
. . exporting table              RPT_VASP_20100501          0 rows exported
. . exporting table              RPT_VASP_20100502          0 rows exported
. . exporting table              RPT_VASP_20100503          0 rows exported
. . exporting table              RPT_VASP_20100504          0 rows exported
. . exporting table              RPT_VASP_20100505          0 rows exported
. . exporting table              RPT_VASP_20100506          0 rows exported
. . exporting table              RPT_VASP_20100507          0 rows exported
. . exporting table              RPT_VASP_20101027          0 rows exported
. . exporting table        SERVICEACCOUNT_20100428         24 rows exported
. . exporting table        SERVICEACCOUNT_20100429        227 rows exported
. . exporting table        SERVICEACCOUNT_20100430         96 rows exported
. . exporting table        SERVICEACCOUNT_20100501          0 rows exported
. . exporting table        SERVICEACCOUNT_20100502          0 rows exported
. . exporting table        SERVICEACCOUNT_20100503          0 rows exported
. . exporting table        SERVICEACCOUNT_20100504          0 rows exported
. . exporting table        SERVICEACCOUNT_20100505         80 rows exported
. . exporting table        SERVICEACCOUNT_20100506          5 rows exported
. . exporting table        SERVICEACCOUNT_20100507          0 rows exported
. . exporting table        SERVICEACCOUNT_20101027        237 rows exported
. . exporting table                         SIINFO          0 rows exported
. . exporting table                    SMSNOTEINFO          4 rows exported
. . exporting table              SMSPROTOCOLCONFIG          0 rows exported
. . exporting table                SPECIALCUSTINFO          0 rows exported
. . exporting table                  SUBMITRESINFO        128 rows exported
. . exporting table                    SYSOPERATOR         14 rows exported
. . exporting table                SYSTEMPARAMETER        340 rows exported
. . exporting table                SZXNUMBERPREFIX          0 rows exported
. . exporting table              TERMINALBLACKLIST          2 rows exported
. . exporting table              TMP_ATTACH_RESULT        161 rows exported
. . exporting table                TMP_BASE_RESULT         28 rows exported
. . exporting table                     TMP_RESULT          0 rows exported
. . exporting table                   TMP_RESULTID          0 rows exported
. . exporting table                  TMP_RESULTMEM          0 rows exported
. . exporting table                   TRACEMSGINFO          0 rows exported
. . exporting table                      UAPROFILE          2 rows exported
. . exporting table                       VASPINFO         12 rows exported
. . exporting table                  VASPLEVELINFO          2 rows exported
. . exporting table               VASPPRIORITYINFO          5 rows exported
. . exporting table                VASPRIORITYINFO          5 rows exported
. . exporting table                VASPSERVICE_SUP         15 rows exported
. . exporting table              VASSERVEDAREALIST          1 rows exported
. . exporting table               VASSUBSCRIBEINFO          0 rows exported
. . exporting table              VCARRIERNBRPREFIX          5 rows exported
. . exporting table             VIRTUALCARRIERINFO          1 rows exported
. . exporting table            VIRTUALCARRIERLEVEL          1 rows exported
. . exporting table                    VPNCORP_100          3 rows exported
. . exporting table                    VPNCORP_300          3 rows exported
. . exporting table                  VPNSUBSCRIBER          6 rows exported
. . exporting table                 VPNUNITECORPID          1 rows exported
. exporting synonyms
. exporting views
. exporting referential integrity constraints
. exporting stored procedures
. exporting operators
. exporting indextypes
. exporting bitmap, functional and extensible indexes
. exporting posttables actions
. exporting triggers
. exporting materialized views
. exporting snapshot logs
. exporting job queues
. exporting refresh groups and children
. exporting dimensions
. exporting post-schema procedural objects and actions
. exporting user history table
. exporting default and system auditing options
. exporting statistics
Export terminated successfully without warnings.
``` 

# 验证过程

## 数据完整性验证

应用数据导入到数据库B后，数据完整性验证。

主要操作是查询导入后的数据信息，例如通过PLSQL Developer工具查询相同的表，前后进行数据对比操作。

## TNS配置

使用oracle用户，在MMSG单板侧增加tns信息，即修改 $ORACLE_HOME/network/admin/tnsnames.ora文件

例如：

```
vi $ORACLE_HOME/network/admin/tnsnames.ora

MMSGDB62 =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.71.167.62)(PORT = 1523))
    )
    (CONNECT_DATA =
      (SERVICE_NAME = iagw)
    )
  )
```

注：
* 蓝色部分为增加的TNS信息，请根据实际情况进行增加。


## MMSG与切换后的数据库连接验证

使用MMSG用户登录单板，验证网关与切换后的数据库的连接是否正常

### 操作如下

1、使用tnsping或者sqlplus命令验证

```tnsping  dbname N ```

其中:

* dbname为TNS中增加的数据库的别名
* N 表示一个正整数

2、使用sqlplus命令验证

```
sqlplus  username/passwd@dbname
```

其中:

* username表示切换数据库后应用用户名
* passwd   表示切换数据库后应用用户的密码
* dbname  表示 TNS中增加的数据库名（示例中为MMSGDB62）

### 验证如下

```
69 mmsg [mmsg] :/home/mmsg>tnsping mmsgdb62 10

TNS Ping Utility for Linux: Version 11.1.0.7.0 - Production on 07-MAY-2010 14:33:10

Copyright (c) 1997, 2008, Oracle.  All rights reserved.

Used parameter files:


Used TNSNAMES adapter to resolve the alias
Attempting to contact (DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = 10.71.167.62)(PORT = 1523))) (CONNECT_DATA = (SERVICE_NAME = iagw)))
OK (50 msec)
OK (50 msec)
OK (50 msec)
OK (50 msec)
OK (50 msec)
OK (60 msec)
OK (50 msec)
OK (50 msec)
OK (50 msec)
OK (50 msec)
70 mmsg [mmsg] :/home/mmsg>sqlplus wyz/wyz@mmsgdb62

SQL*Plus: Release 11.1.0.7.0 - Production on Fri May 7 14:33:43 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining,
Oracle Database Vault and Real Application Testing options

SQL> select * from modules;

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      1001 OMCAgent
         1 10.137.49.114             52238
OMCAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      2001 ChargeServer
         2 10.137.49.114             52234
ChargeServer

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
         1 MMSServer
         3 10.137.49.114             52233
MMSServer

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
        80 Dispatcher
        88 10.137.49.114             52299
Dispatcher

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      1901 VASPServer
        71 10.137.49.114             52280
VASPServer

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      1811 MMSCServer
        70 10.137.49.114             52288
MMSCServer

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      1101 ENUMDNSAgent
        11 10.137.49.114             52237
EnumDNSAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      5301 VASPClient
        73 10.137.49.114             52298
VASPClient

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      5401 MMSCClient
        74 10.137.49.114             52278
MMSCClient

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      1201 DSMPAgent
        12 10.137.49.114             52281
DSMPAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      2200 LOG2DB
        22 10.137.49.114             52232
LOG2DB

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      4001 SMSAgent
         4 10.137.49.114             52235
SMSAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      8201 BILLAgent
        82 10.137.49.114             52266
BILLAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      8202 VPNBILLAgent
        82 10.137.49.114             52277
VPNBILLAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      8203 DRBILLAgent
        82 10.137.49.114             53398
DRBILLAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
      8901 VPNAgent
        89 10.137.49.114             52222
VPNAgent

  MODULEID MODULENAME
---------- ----------------------------------------------------------------
MODULETYPE MODULEIPADDR         LISTENPORT
---------- -------------------- ----------
MODULEDESC
--------------------------------------------------------------------------------
HOSTNAME                                                                PID
---------------------------------------------------------------- ----------
      PING
----------
                                                                          0
         0


16 rows selected.
```

### 修改MMSG侧配置文件

注：
* 在修改MMSG侧配置文件前，请先停止正在运行的网关。

## 修改$MMS_HOME/cfg目录下下列文件信息

```
cshrc
mms.cfg
log2db.cfg
vpn.cfg
```

```
vi cshrc
#The SID for accessing the Oracle database must be consistent with the contents in the tnsname.ora configuration file of the Oracle client
setenv ORACLE_SID mmsgdb62   //请根据实际情况进行修改，示例中TNS为mmsgdb62
```

```
vi mms.cfg
//Note: This configuration file is used for setting the database access mode of the MMSC. 
//Other settings are stored in the database. You can set the configuration items on the Web management page.
[Database]
DBName = mmsgdb62
DBUserName =wyz 
DBPassword = wyz
DBType = oracle
DBUrl = jdbc:oracle:thin:@10.71.167.62:1523:iagw
DBJdbcClass=oracle.jdbc.driver.OracleDriver
MMS_LOCAL_FLOATIP = 10.137.49.114
```

```
vi log2db.cfg 
//Log2db configuration file

[Database]
//Database user name
DBUser = wyz

//Database password
DBPassword = wyz

//URL used by the database JDBC
DBUrl = jdbc:oracle:thin:@10.71.167.62:1523:iagw
//DBUrl = jdbc:db2://10.164.78.178:50003/mmsgdb
//DBUrl = jdbc:microsoft:sqlserver://127.0.0.1:1433

//Drive used by the database JDBC
DBDriver = oracle.jdbc.driver.OracleDriver
//DBDriver = com.ibm.db2.jcc.DB2Driver
//DBDriver = com.microsoft.jdbc.sqlserver.SQLServerDriver
```

```
vi vpn.cfg
[DataBase]
#Database connection information. This parameter is valid only when VpnDbMode is set to 0 indicating to connect to the WEBSMS.
#Oracle database
DBUrl=jdbc:oracle:thin:@10.71.167.62:1523:iagw 
DBDriver=oracle.jdbc.driver.OracleDriver
#DB2 database
#DBUrl=jdbc:db2://10.164.75.87:50001/iagdb1
#DBDriver=com.ibm.db2.jcc.DB2Driver
DBUser=wyz
DBPassword=wyz
```

注：
* 1、蓝色部分信息请根据实际情况进行修改。
* 2、修改后重新source一下cfg目录下cshrc文件
* 3、它配置信息，如后台命令执行的备份脚本等不需要做任何改动，当mms.cfg文件发生修改后，在某时刻后台执行定时任务时候会重新读取这个配置文件，故而相关的定时任务不做任何变动。
* 4、如果在原数据库上进行了数据库的备份策略，请将备份策略在切换后的AIX 11g数据库上重新进行。

### 遇见问题 Get DB Connection is null

如果出现如下错误（Get DB Connection is null），请检查cfg目录下相关配置文件（主要是cfg目录下cshrc、mms.cfg、log2db.cfg三个文件）是否正确修改。

```
91 mmsg [mmsg] :/home/mmsg/mms_home/cfg>Get DB Connection is null
Exception in thread "main" java.lang.NullPointerException
        at com.huawei.mms.common.conf.ModulesData.getModuleNameByID(ModulesData.java:83)
        at com.huawei.mms.common.log.Alarmer.<init>(Alarmer.java:61)
        at com.huawei.mms.common.log.Alarmer.getInstance(Alarmer.java:74)
        at com.huawei.mms.common.dbproxy.DBProxyJDBCImp.query(DBProxyJDBCImp.java:351)
        at com.huawei.mms.common.dbproxy.DBProxyJDBCImp.query(DBProxyJDBCImp.java:271)
        at com.huawei.mms.common.conf.CfgMgr.reload(CfgMgr.java:107)
        at com.huawei.mms.init.HttpAgentData.init(HttpAgentData.java:131)
        at com.huawei.mms.init.MMSCClientInitiator.initCfgData(MMSCClientInitiator.java:155)
        at com.huawei.mms.init.Initiator.initSystem(Initiator.java:97)
        at com.huawei.mms.mm7agent.MMSCClient.main(MMSCClient.java:49)
```

## 启动网关

使用mms start命令启动数据库切换后的网关。

如果在启动过程中出现如下信息，请修改端口号，以server主调度模块为例

```
[05-07 15:22:37 511][INFO][ServerApp][serverapp.cpp 263][-140986064]*****************  Initialize Static Data Successfully!!  ******
**************

[05-07 15:22:37 511][FINE][Platform][mms_acceptor.cpp 85][-140986064]Tcp Server start fail!ip address is:10.137.49.114, port no is:5
2233
[05-07 15:22:37 511][WARNING][ServerApp][serverapp.cpp 492][-140986064]Open Socket Server Failed, Exit System...!ServerIP = 10.137.4
9.114, ListenPort = 52233

[05-07 15:22:37 511][FINE][Platform][appmanager.cpp 173][-140986064]OnInit() return -1
```

### server模块启动失败

```
144 mmsg [mmsg] :/home/mmsg/mms_home/log/server_1/run>netstat -an | grep 52233
tcp        0      0 10.137.49.114:52277     10.137.49.114:52233     ESTABLISHED 
tcp        0      0 10.137.49.114:52233     10.137.49.114:52277     ESTABLISHED
```

解决方法如下

1、server端口信息

```
update  modules  set listenport =52239 where MODULENAME='MMSServer';
```

2、重启server模块

```
mms start 1
```

## 流程验证

网关各个模块启动后，验证流程是否通畅。

注：
* 需要修改portal配置信息，因为数据库已经发生切换。本文不做介绍。


### 下行流程，不支持DR优化

#### 计费话单

```
0507155553800800011020000,008613810243001,,0,822000,008613810243001,,2,1,3,0,0,0,0,1,2,0,1000,800800,910000,822000,7800,121000,,2010
0507155553,20100507155558,,00000,1,1,1,0,0,0,050708001402708220010,
```

#### 统计话单

```
0507155553800800011020000,008613810243001,,0,822000,008613810243001,,2,1,3,0,0,0,0,1,2,0,0100,800800,910000,822000,7800,121000,,2010
0507155553,20100507155553,,00000,1,1,1,0,0,0,,,1,
0507155553800800011020000,008613810243001,,0,822000,008613810243001,,3,1,3,0,0,0,0,1,2,0,1000,800800,910000,822000,7800,121000,,2010
0507155553,20100507155558,,00000,1,1,1,0,0,0,,1,1,
```

#### Vaspserver日志片段

```
Begin to dispose message from SP!
[2010-05-07 15:55:53.335] [FINEST] [vaspserver_1901] [Tools.java:615] [ ] [Receive SOAP Message] 
HttpRequest Content:
15:55:53.334(Tools.java:362) byte[719] @3682584 {
    [HEX]    0  1  2  3  4  5  6  7-  8  9  a  b  c  d  e  f | 0123456789abcdef
  ----------------------------------------------------------------------------
  00000000: 3c 3f 78 6d 6c 20 76 65.72 73 69 6f 6e 3d 22 31 | <?xml version="1
  00000010: 2e 30 22 20 65 6e 63 6f.64 69 6e 67 3d 22 55 54 | .0" encoding="UT
  00000020: 46 2d 38 22 3f 3e 3c 65.6e 76 3a 45 6e 76 65 6c | F-8"?><env:Envel
  00000030: 6f 70 65 20 78 6d 6c 6e.73 3a 65 6e 76 3d 22 68 | ope xmlns:env="h
  00000040: 74 74 70 3a 2f 2f 73 63.68 65 6d 61 73 2e 78 6d |
 ttp://schemas.xm
  00000050: 6c 73 6f 61 70 2e 6f 72.67 2f 73 6f 61 70 2f 65 | lsoap.org/soap/e
  00000060: 6e 76 65 6c 6f 70 65 2f.22 3e 3c 65 6e 76 3a 48 | nvelope/"><env:H
  00000070: 65 61 64 65 72 3e 3c 6d.6d 37 3a 54 72 61 6e 73 | eader><mm7:Trans
  00000080: 61 63 74 69 6f 6e 49 44.20 78 6d 6c 6e 73 3a 6d | actionID xmlns:m
  00000090: 6d 37 3d 22 68 74 74 70.3a 2f 2f 77 77 77 2e 33 | m7="http://www.3
  000000a0: 67 70 70 2e 6f 72 67 2f.66 74 70 2f 53 70 65 63 | gpp.org/ftp/Spec
  000000b0: 73 2f 61 72 63 68 69 76.65 2f 32 33 5f 73 65 72 | s/archive/23_ser
  000000c0: 69 65 73 2f 32 33 2e 31.34 30 2f 73 63 68 65 6d | ies/23.140/schem
  000000d0: 61 2f 52 45 4c 2d 36 2d.4d 4d 37 2d 31 2d 30 22 | a/REL-6-MM7-1-0"
  000000e0: 20 65 6e 76 3a 6d 75 73.74 55 6e 64 65 72 73 74 |  env:mustUnderst
  000000f0: 61 6e 64 3d 22 31 22 3e.74 69 64 31 30 30 30 30 | and="1">tid10000
  00000100: 30 30 30 30 3c 2f 6d 6d.37 3a 54 72 61 6e 73 61 | 0000</mm7:Transa
  00000110: 63 74 69 6f 6e 49 44 3e.3c 2f 65 6e 76 3a 48 65 | ctionID></env:He
  00000120: 61 64 65 72 3e 3c 65 6e.76 3a 42 6f 64 79 3e 3c | ader><env:Body><
  00000130: 53 75 62 6d 69 74 52 65.71 20 78 6d 6c 6e 73 3d | SubmitReq xmlns=
  00000140: 22 68 74 74 70 3a 2f 2f.77 77 77 2e 33 67 70 70 | "http://www.3gpp
  00000150: 2e 6f 72 67 2f 66 74 70.2f 53 70 65 63 73 2f 61 | .org/ftp/Specs/a
  00000160: 72 63 68 69 76 65 2f 32.33 5f 73 65 72 69 65 73 | rchive/23_series
  00000170: 2f 32 33 2e 31 34 30 2f.73 63 68 65 6d 61 2f 52 | /23.140/schema/R
  00000180: 45 4c 2d 36 2d 4d 4d 37.2d 31 2d 30 22 3e 3c 4d | EL-6-MM7-1-0"><M
  00000190: 4d 37 56 65 72 73 69 6f.6e 3e 36 2e 33 2e 30 3c | M7Version>6.3.0<
  000001a0: 2f 4d 4d 37 56 65 72 73.69 6f 6e 3e 3c 53 65 6e | /MM7Version><Sen
  000001b0: 64 65 72 49 64 65 6e 74.69 66 69 63 61 74 69 6f | derIdentificatio
  000001c0: 6e 3e 3c 56 41 53 50 49.44 3e 38 32 32 30 30 30 | n><VASPID>822000
  000001d0: 3c 2f 56 41 53 50 49 44.3e 3c 56 41 53 49 44 3e | </VASPID><VASID>
  000001e0: 37 38 30 30 3c 2f 56 41.53 49 44 3e 3c 2f 53 65 | 7800</VASID></Se
  000001f0: 6e 64 65 72 49 64 65 6e.74 69 66 69 63 61 74 69 | nderIdentificati
}

[2010-05-07 15:55:53.337] [FINER] [vaspserver_1901] [HttpAgentForSoap.java:167] [ ] [SP to Server] 
Decoder soap message to mm7 message success, detail is:
MessageType = MM7-Submit.req
TransactionID = tid100000000
MM7Version = 6.3.0
To = [13810243001]
DeliveryReport = YES
Subject = This is a test.
VASPID = 822000
VASID = 7800
ServiceCode = 121000
Content: Content-Type=application/vnd.wap.multipart.mixed

[2010-05-07 15:55:53.337] [FINER] [vaspserver_1901] [VASPServerCheckTools.java:224] [ ] [VASPServer] 
MM7 Message will be sended to server!
[2010-05-07 15:55:53.338] [FINEST] [vaspserver_1901] [SocketConnection.java:612] [ ] [Send Message] 
 Send message to module[1]
15:55:53.338(Tools.java:374) byte[105000] @25068634 {
    [HEX]    0  1  2  3  4  5  6  7-  8  9  a  b  c  d  e  f | 0123456789abcdef
  ----------------------------------------------------------------------------
  00000000: 49 d9 00 00 00 76 17 40.00 00 4b e3 c7 89 01 51 | I....v.@..K....Q
  00000010: 00 47 07 6d 00 00 00 00.00 03 00 01 10 01 00 00 | .G.m............
  00000020: 00 00 00 02 8c c0 98 74.69 64 31 30 30 30 30 30 | .......tid100000
  00000030: 30 30 30 00 d5 02 06 36.86 80 96 54 68 69 73 20 | 000....6...This 
  00000040: 69 73 20 61 20 74 65 73.74 2e 00 97 31 33 38 31 | is a test...1381
  00000050: 30 32 34 33 30 30 31 00.d7 31 32 31 30 30 30 00 | 0243001..121000.
  00000060: d9 37 38 30 30 00 d8 38.32 32 30 30 30 00 ed 37 | .7800..822000..7
  00000070: 38 30 30 00 b4 01      .                        | 800...          
}

[2010-05-07 15:55:53.341] [FINEST] [vaspserver_1901] [SocketConnection.java:539] [ ] [Receive Message] 
Receive message from module[1], binary stream:
15:55:53.340(Tools.java:374) byte[200] @18818021 {
    [HEX]    0  1  2  3  4  5  6  7-  8  9  a  b  c  d  e  f | 0123456789abcdef
  ----------------------------------------------------------------------------
  00000000: 00 00 00 64 17 41 00 00.4b e3 c7 89 01 51 00 03 | ...d.A..K....Q..
  00000010: 00 01 10 01 00 01 00 47.07 6d 00 00 00 00 00 00 | .......G.m......
  00000020: 00 02 8c c1 98 74 69 64.31 30 30 30 30 30 30 30 | .....tid10000000
  00000030: 30 00 d5 02 06 30 8b 30.35 30 37 31 35 35 35 35 | 0....0.050715555
  00000040: 33 38 30 30 38 30 30 30.31 31 30 32 00 bc 02 03 | 380080001102....
  00000050: e8 be 0f ea 7f e5 8f 91.e9 80 81 e6 88 90 e5 8a | ................
  00000060: 9f 00                  .                        | ..              
}

[2010-05-07 15:55:53.341] [FINER] [vaspserver_1901] [TransactionMgr.java:157] [ ] [Message Process Interval] 
MessageType: MM7-Submit.req; SourceModuleID: 1901; TargetModuleID: 1; Interval: 4
[2010-05-07 15:55:53.341] [FINER] [vaspserver_1901] [MM7MessageSenderMgr.java:357] [ ] [SP to Server] 
Get response from MMSGserver, detail: 
MessageType = MM7-Submit.res
TransactionID = tid100000000
MM7Version = 6.3.0
MessageID = 050715555380080001102
StatusCode = 1000
StatusText = 发送成功

[2010-05-07 15:55:53.342] [FINER] [vaspserver_1901] [HttpAgentForSoap.java:456] [ ] [SP to Server] 
Get response from server or dispatcher, detail:
MessageType = MM7-Submit.res
TransactionID = tid100000000
MM7Version = 6.3.0
MessageID = 050715555380080001102
StatusCode = 1000
StatusText = 发送成功
```

#### SVC日志片段

```
[2010-05-07 15:55:53 339][LgTp:FRSMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:2][SessID:0110000000001100507155553][MsgID:050715555380080001102][TransID:tid100000000][ExMsgID:][MPRP:MM7][MsgType:MM7_SUBMIT_REQ][AfrAtrbt:RCV][AfrStat:OK]; SV:NULL; MsgCls:NULL; DR:YES; RR:NULL; MsgSz:0 Byte(s); VASPID:822000; VASID:7800; SrvCd:121000; DispMsgID:;
[2010-05-07 15:55:53 340][LgTp:SRVMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:2][SessID:0110000000001100507155553][MsgID:050715555380080001102][TransID:tid100000000][ExMsgID:][MPRP:MM7][MsgType:MM7_SUBMIT_RES][AfrAtrbt:SND][AfrStat:OK]; MM7RspStat:SUCCESS; DispMsgID:;
[2010-05-07 15:55:53 345][LgTp:OFLWVR][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SessID:0110000000001100507155553][MsgID:050715555380080001102][ExMsgID:][FlwCls:NORMAL]; FlwOvrStat:SUBMIT_OK; FlwOvrStatCode:0100; DtlCd:STAT_SUBMIT_SUCCESS; DlvrTimer:0 Second(s);
[2010-05-07 15:55:53 346][LgTp:ENTRLS][SessID:0110000000001100507155553][MsgID:050715555380080001102][ExMsgID:][EntAct:SUBMIT_SESSION_RELEASE]; RealFlwCls:NORMAL;
[2010-05-07 15:55:53 346][LgTp:SRVMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:-1][SessID:0110000000002100507155553][MsgID:050715555380080001102][TransID:0110000000002100507155553001][ExMsgID:][MPRP:MM7][MsgType:MM7_SUBMIT_REQ][AfrAtrbt:SND][AfrStat:OK]; SV:NULL; MsgCls:PRSL; DR:YES; RR:NO; MsgSz:0 Byte(s); VASPID:800100; VASID:7788; SrvCd:822001;
[2010-05-07 15:55:53 470][LgTp:SRVMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:0][SessID:0110000000002100507155553][MsgID:050715555380080001102][TransID:0110000000002100507155553001][ExMsgID:050708001402708220010][MPRP:MM7][MsgType:MM7_SUBMIT_RES][AfrAtrbt:RCV][AfrStat:OK]; MM7RspStat:SUCCESS;ResOriginStat:1000;
[2010-05-07 15:55:58 638][LgTp:SRVMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:2][SessID:0110000000002100507155553][MsgID:050715555380080001102][TransID:tid00001003][ExMsgID:050708001402708220010][MPRP:MM7][MsgType:MM7_DELIVERY_REPORT_REQ][AfrAtrbt:RCV][AfrStat:OK]; FtchStat:RETRIEVED;
[2010-05-07 15:55:58 638][LgTp:SRVMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:2][SessID:0110000000002100507155553][MsgID:050715555380080001102][TransID:tid00001003][ExMsgID:050708001402708220010][MPRP:MM7][MsgType:MM7_DELIVERY_REPORT_RES][AfrAtrbt:SND][AfrStat:OK]; MM7RspStat:SUCCESS;
[2010-05-07 15:55:58 638][LgTp:TFLWVR][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SessID:0110000000002100507155553][MsgID:050715555380080001102][ExMsgID:050708001402708220010][FlwCls:NORMAL]; FlwOvrStat:DELIVER_OK; FlwOvrStatCode:1000; DtlCd:STAT_FRWRD_SNDR_ADDR_IN_FRWRD_RCVR_USER_BLKLST; RealFlwCls:NORMAL;
[2010-05-07 15:55:58 638][LgTp:SRVMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:-1][SessID:0110000000002100507155553][MsgID:050715555380080001102][TransID:0110000000002100507155553303][ExMsgID:050708001402708220010][MPRP:MM7][MsgType:MM7_DELIVERY_REPORT_REQ][AfrAtrbt:SND][AfrStat:SNDING]; FtchStat:RETRIEVED; DispMsgID:;
[2010-05-07 15:55:58 657][LgTp:SRVMSG][AfOrgn:][Sndr:7800121000][Rcvr:+8613810243001][FwdAddr:][SqncNum:0][SessID:0110000000002100507155553][MsgID:050715555380080001102][TransID:0110000000002100507155553303][ExMsgID:050708001402708220010][MPRP:MM7][MsgType:MM7_DELIVERY_REPORT_RES][AfrAtrbt:RCV][AfrStat:OK]; MM7RspStat:SUCCESS;
[2010-05-07 15:55:58 657][LgTp:ENTRLS][SessID:0110000000002100507155553][MsgID:050715555380080001102][ExMsgID:050708001402708220010][EntAct:DELIVER_SESSION_RELEASE]; RealFlwCls:NORMAL;
[2010-05-07 15:55:58 657][LgTp:ENTRLS][MsgID:050715555380080001102][ExMsgID:][EntAct:ORIGINMSG_RELEASE];
```

#### CS日志片段

```
m_ucAreaFlag  = 0 
m_ucRoamingStatus  = 255 
m_strIMSI =  
m_strVisitedSGSN =  
m_addrXMmsSenderAddress end: 

m_strXMmsSenderActaulProperties =  
m_strXMmsResulText = 处理成功 
m_listRecipientAddress Start: 
 m_strXMmsTransactionIDofPPS  = 011000000999910050715555300011 

m_addrXMmsRecipientAddress Start:
m_strAddress  = +8613810243001 
m_iAddressType = 0 
m_iAddressSendType = 0
```

#### Mmscclient日志片段

```
[2010-05-07 15:55:53.321] [FINER] [mmscclient_5401] [ConnectionManager.java:333] [ ] [Update SocketConnection's Load] 
Update module[1]'s state to 0
[2010-05-07 15:55:53.347] [FINEST] [mmscclient_5401] [SocketConnection.java:539] [ ] [Receive Message] 
Receive message from module[1], binary stream:
15:55:53.346(Tools.java:374) byte[297] @16747636 {
    [HEX]    0  1  2  3  4  5  6  7-  8  9  a  b  c  d  e  f | 0123456789abcdef
  ----------------------------------------------------------------------------
  00000000: 00 00 00 c5 17 40 00 00.ff ff ff ff ff ff 00 03 | .....@..........
  00000010: 00 01 10 01 00 01 00 4a.15 19 00 00 00 00 ff ff | .......J........
  00000020: ff ff 8c c0 98 30 31 31.30 30 30 30 30 30 30 30 | .....01100000000
  00000030: 30 32 31 30 30 35 30 37.31 35 35 35 35 33 30 30 | 0210050715555300
  00000040: 31 00 f1 30 35 30 37 31.35 35 35 35 33 38 30 30 | 1..0507155553800
  00000050: 38 30 30 30 31 31 30 32.00 ea 38 32 32 30 30 30 | 80001102..822000
  00000060: 00 eb 37 38 30 30 00 ec.31 32 31 30 30 30 00 d5 | ..7800..121000..
  00000070: 02 06 30 d8 38 30 30 31.30 30 00 d9 37 37 38 38 | ..0.800100..7788
  00000080: 00 85 04 4b e3 c7 89 97.2b 38 36 31 33 38 31 30 | ...K....+8613810
  00000090: 32 34 33 30 30 31 00 d7.38 32 32 30 30 31 00 96 | 243001..822001..
  000000a0: 54 68 69 73 20 69 73 20.61 20 74 65 73 74 2e 00 | This is a test..
  000000b0: 8a 80 88 06 80 04 4b e3.c7 c5 86 80 90 81 d6 03 | ......K.........
  000000c0: 0d e2 b0               .                        | ...             
}

[2010-05-07 15:55:53.347] [FINER] [mmscclient_5401] [MMSCProcessor.java:56] [ ] [MMSG to MMSC] 
Begin to dispose message from MMSGserver!
[2010-05-07 15:55:53.348] [FINER] [mmscclient_5401] [MMSCProcessor.java:124] [ ] [MMSG to MMSC] 
PDU message detail is:
MessageType = MM7-Submit.req
TransactionID = 0110000000002100507155553001
MM7Version = 6.3.0
To = [+8613810243001]
Date = 2010-05-07 15:55:53 +0800
DeliveryReport = YES
Expiry = 2010-05-07 15:56:53 +0800
MessageClass = Personal
ReadReply = NO
Subject = This is a test.
MMSCID = 910000
VASPID = 800100
VASID = 7788
ServiceCode = 822001
MMSGMessageID = 050715555380080001102
RealVASPID = 822000
RealVASID = 7800
RealServiceCode = 121000

[2010-05-07 15:55:53.348] [FINER] [mmscclient_5401] [MMSCProcessor.java:240] [ ] [MMSG to MMSC] 
MMSC Don't Support DR Optimization
[2010-05-07 15:55:53.348] [FINER] [mmscclient_5401] [MMSCProxyHTTPImp.java:461] [ ] [MMSG to MMSC] 
MMSCURL(soap) is: http://10.137.48.60:1190/mmsc
[2010-05-07 15:55:53.382] [FINEST] [mmscclient_5401] [MMSCProxyHTTPImp.java:778] [ ] [MMSG to MMSC] 
Get response from MMSC, detail:
<?xml version="1.0"?><env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"><env:Header><mm7:TransactionID xmlns:mm7="http://www.3gpp.org/ftp/Specs/archive/23_series/23.140/schema/REL-6-MM7-1-0">0110000000002100507155553001</mm7:TransactionID></env:Header><env:Body><SubmitRsp xmlns="http://www.3gpp.org/ftp/Specs/archive/23_series/23.140/schema/REL-6-MM7-1-0"><MM7Version>6.3.0</MM7Version><Status><StatusCode>1000</StatusCode></Status><MessageID>050708001402708220010</MessageID></SubmitRsp></env:Body></env:Envelope> 

[2010-05-07 15:55:53.382] [FINER] [mmscclient_5401] [MMSCProxyHTTPImp.java:1140] [ ] [MMSCProxyHTTPImp] 
get response from MMSC, detail:
MessageType = MM7-Submit.res
TransactionID = 0110000000002100507155553001
MM7Version = 6.3.0
MessageID = 050708001402708220010
StatusCode = 1000

[2010-05-07 15:55:53.443] [FINEST] [mmscclient_5401] [MMSCProcessor.java:665] [ ] [insert data successful. MMSGMessageID = 050715555380080001102, MMSCMessageID = 050708001402708220010 tableName:MMSGMMSCMsgIDMap04 , current time is: Fri May 07 15:55:53 CST 2010] 
[2010-05-07 15:55:53.469] [FINER] [mmscclient_5401] [MMSCProcessor.java:449] [ ] [MMSCProxyHTTPImp] 
Send response to Server, detail:
MessageType = MM7-Submit.res
TransactionID = 0110000000002100507155553001
MM7Version = 6.3.0
MessageID = 050708001402708220010
StatusCode = 1000
```

### 上行流程

#### SVC日志片段

```
[2010-05-07 16:00:16 177][LgTp:FRSMSG][AfOrgn:][Sndr:+8613810243001][Rcvr:7800121000][FwdAddr:][SqncNum:3][SessID:0120000000003100507160016][MsgID:050716001680080001203][TransID:tid00001004][ExMsgID:][MPRP:MM7][MsgType:MM7_DELIVER_REQ][AfrAtrbt:RCV][AfrStat:OK]; SV:NULL; MsgCls:NULL; DR:NULL; RR:NULL; Expiry:-1 Second(s); MsgSz:0 Byte(s); VASPID:; VASID:; SrvCd:; DlvrType:; SessType:Normal;
[2010-05-07 16:00:16 177][LgTp:SRVMSG][AfOrgn:][Sndr:+8613810243001][Rcvr:7800121000][FwdAddr:][SqncNum:3][SessID:0120000000003100507160016][MsgID:050716001680080001203][TransID:tid00001004][ExMsgID:][MPRP:MM7][MsgType:MM7_DELIVER_RES][AfrAtrbt:SND][AfrStat:OK]; MM7RspStat:SUCCESS;
[2010-05-07 16:00:16 182][LgTp:OFLWVR][Sndr:+8613810243001][Rcvr:7800121000][FwdAddr:][SessID:0120000000003100507160016][MsgID:050716001680080001203][ExMsgID:][FlwCls:NORMAL]; FlwOvrStat:SUBMIT_OK; FlwOvrStatCode:0400; DtlCd:STAT_SUBMIT_SUCCESS; DlvrTimer:0 Second(s);
[2010-05-07 16:00:16 182][LgTp:ENTRLS][SessID:0120000000003100507160016][MsgID:050716001680080001203][ExMsgID:][EntAct:SUBMIT_SESSION_RELEASE]; RealFlwCls:NORMAL;
[2010-05-07 16:00:16 183][LgTp:SRVMSG][AfOrgn:][Sndr:+8613810243001][Rcvr:7800121000][FwdAddr:][SqncNum:-1][SessID:0120000000004100507160016][MsgID:050716001680080001203][TransID:0120000000004100507160016001][ExMsgID:][MPRP:MM7][MsgType:MM7_DELIVER_REQ][AfrAtrbt:SND][AfrStat:SNDING]; SV:SHOW; MsgCls:PRSL; DR:NO; RR:NO; Expiry:100 Second(s); MsgSz:0 Byte(s); VASPID:822000; VASID:7800; SrvCd:121000; DlvrType:NORMAL; SessType:Normal;
[2010-05-07 16:00:16 203][LgTp:SRVMSG][AfOrgn:][Sndr:+8613810243001][Rcvr:7800121000][FwdAddr:][SqncNum:0][SessID:0120000000004100507160016][MsgID:050716001680080001203][TransID:0120000000004100507160016001][ExMsgID:][MPRP:MM7][MsgType:MM7_DELIVER_RES][AfrAtrbt:RCV][AfrStat:OK]; MM7RspStat:SUCCESS;ResOriginStat:1000;
[2010-05-07 16:00:16 203][LgTp:TFLWVR][Sndr:+8613810243001][Rcvr:7800121000][FwdAddr:][SessID:0120000000004100507160016][MsgID:050716001680080001203][ExMsgID:][FlwCls:NORMAL]; FlwOvrStat:DELIVER_OK; FlwOvrStatCode:1100; DtlCd:STAT_FRWRD_SNDR_ADDR_IN_FRWRD_RCVR_USER_BLKLST; RealFlwCls:NORMAL;
[2010-05-07 16:00:16 207][LgTp:ENTRLS][SessID:0120000000004100507160016][MsgID:050716001680080001203][ExMsgID:][EntAct:DELIVER_SESSION_RELEASE]; RealFlwCls:NORMAL;
[2010-05-07 16:00:16 207][LgTp:ENTRLS][MsgID:050716001680080001203][ExMsgID:][EntAct:ORIGINMSG_RELEASE];
```

### 批价鉴权

验证了AOMT和MOAT批价鉴权流程，流程通畅。

### 二次确认流程

#### 工具日志片段

```
[2010-05-08 16:19:54:447]  收到HTTP主动请求 AuthPriceReq, TransactionID=8008000000000007
[2010-05-08 16:19:54:447]  返回响应 AuthPriceResp, hRet = 0
[2010-05-08 16:19:59:447]  开始发送OnDemandReq
[2010-05-08 16:19:59:447]  收到响应OnDemandRes, hRet = 0
```

#### 计费话单

```
0507161533800800011060000,008613810243001,,0,008613810243001,822000,,5,1,4,0,3,0,0,1,2,0,1100,910000,800800,822000,7800,121000,,2010
0507161533,20100507161538,,00000,1,6,0,0,0,0,,
```

#### 统计话单

```
0507161533800800011060000,008613810243001,,0,008613810243001,822000,,0,1,4,0,3,0,0,1,2,0,0400,910000,800800,822000,7800,121000,,2010
0507161533,20100507161538,,00000,1,6,0,0,0,0,,1,1,
0507161533800800011060000,008613810243001,,0,008613810243001,822000,,5,1,4,0,3,0,0,1,2,0,1100,910000,800800,822000,7800,121000,,2010
0507161533,20100507161538,,00000,1,6,0,0,0,0,,,1,
```

### 支持DR优化

流程正常

#### Mmsclient日志片段

```
[2010-05-07 16:18:18.985] [FINEST] [mmscclient_5401] [SocketConnection.java:539] [ ] [Receive Message] 
Receive message from module[1], binary stream:
16:18:18.985(Tools.java:374) byte[297] @15430449 {
    [HEX]    0  1  2  3  4  5  6  7-  8  9  a  b  c  d  e  f | 0123456789abcdef
  ----------------------------------------------------------------------------
  00000000: 00 00 00 c5 17 40 00 00.ff ff ff ff ff ff 00 03 | .....@..........
  00000010: 00 01 10 01 00 02 00 4a.15 19 00 00 00 00 ff ff | .......J........
  00000020: ff ff 8c c0 98 30 31 32.30 30 30 30 30 30 30 30 | .....01200000000
  00000030: 31 32 31 30 30 35 30 37.31 36 31 38 31 38 30 30 | 1210050716181800
  00000040: 31 00 f1 30 35 30 37 31.36 31 38 31 38 38 30 30 | 1..0507161818800
  00000050: 38 30 30 30 31 32 30 37.00 ea 38 32 32 30 30 30 | 80001207..822000
  00000060: 00 eb 37 38 30 30 00 ec.31 32 31 30 30 30 00 d5 | ..7800..121000..
  00000070: 02 06 30 d8 38 30 30 31.30 30 00 d9 37 37 38 38 | ..0.800100..7788
  00000080: 00 85 04 4b e3 cc ca 97.2b 38 36 31 33 38 31 30 | ...K....+8613810
  00000090: 32 34 33 30 30 31 00 d7.38 32 32 30 30 31 00 96 | 243001..822001..
  000000a0: 54 68 69 73 20 69 73 20.61 20 74 65 73 74 2e 00 | This is a test..
  000000b0: 8a 80 88 06 80 04 4b e3.cd 06 86 80 90 81 d6 03 | ......K.........
  000000c0: 0d e2 b0               .                        | ...             
}

[2010-05-07 16:18:18.986] [FINER] [mmscclient_5401] [MMSCProcessor.java:56] [ ] [MMSG to MMSC] 
Begin to dispose message from MMSGserver!
[2010-05-07 16:18:18.986] [FINER] [mmscclient_5401] [MMSCProcessor.java:124] [ ] [MMSG to MMSC] 
PDU message detail is:
MessageType = MM7-Submit.req
TransactionID = 0120000000012100507161818001
MM7Version = 6.3.0
To = [+8613810243001]
Date = 2010-05-07 16:18:18 +0800
DeliveryReport = YES
Expiry = 2010-05-07 16:19:18 +0800
MessageClass = Personal
ReadReply = NO
Subject = This is a test.
MMSCID = 910000
VASPID = 800100
VASID = 7788
ServiceCode = 822001
MMSGMessageID = 050716181880080001207
RealVASPID = 822000
RealVASID = 7800
RealServiceCode = 121000

[2010-05-07 16:18:18.986] [FINER] [mmscclient_5401] [MMSCProcessor.java:231] [ ] [MMSG to MMSC] 
MMSC Support DR Optimization
[2010-05-07 16:18:18.986] [FINER] [mmscclient_5401] [MMSCProxyHTTPImp.java:461] [ ] [MMSG to MMSC] 
MMSCURL(soap) is: http://10.137.48.60:1190/mmsc
[2010-05-07 16:18:19.022] [FINEST] [mmscclient_5401] [MMSCProxyHTTPImp.java:778] [ ] [MMSG to MMSC] 
Get response from MMSC, detail:
<?xml version="1.0"?><env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"><env:Header><mm7:TransactionID xmlns:mm7="http://www.3gpp.org/ftp/Specs/archive/23_series/23.140/schema/REL-6-MM7-1-0">050716181880080001207</mm7:TransactionID></env:Header><env:Body><SubmitRsp xmlns="http://www.3gpp.org/ftp/Specs/archive/23_series/23.140/schema/REL-6-MM7-1-0"><MM7Version>6.3.0</MM7Version><Status><StatusCode>1000</StatusCode></Status><MessageID>050708224000108220010</MessageID></SubmitRsp></env:Body></env:Envelope> 

[2010-05-07 16:18:19.023] [FINER] [mmscclient_5401] [MMSCProxyHTTPImp.java:1140] [ ] [MMSCProxyHTTPImp] 
get response from MMSC, detail:
MessageType = MM7-Submit.res
TransactionID = 050716181880080001207
MM7Version = 6.3.0
MessageID = 050708224000108220010
StatusCode = 1000

[2010-05-07 16:18:19.023] [FINER] [mmscclient_5401] [MMSCProcessor.java:449] [ ] [MMSCProxyHTTPImp] 
Send response to Server, detail:
MessageType = MM7-Submit.res
TransactionID = 0120000000012100507161818001
MM7Version = 6.3.0
MessageID = 050708224000108220010
StatusCode = 1000
```

#### 要求包月计费

```
[2010-05-08 17:04:28:277]  收到HTTP主动请求 AuthPriceReq, TransactionID=8008000000000003
[2010-05-08 17:04:28:277]  返回响应 AuthPriceResp, hRet = 0
[2010-05-08 17:04:28:480]  收到HTTP主动请求 RequireMonthFeeReq, TransactionID=8008000000000004
[2010-05-08 17:04:28:480]  返回响应 RequireMonthFeeReq, hRet = 0
```

#### 计费话单

```
0507170006800800012030000,008613810243001,,0,822000,008613810243001,,2,1,3,0,3,0,0,1,2,0,1000,800800,910000,822000,7800,121000,,2010
0507170006,20100507170007,,00000,1,1,1,0,0,0,042803088220010000035,
```

#### 统计话单

```
0507170006800800012030000,008613810243001,,0,822000,008613810243001,,2,1,3,0,3,0,0,1,2,0,0100,800800,910000,822000,7800,121000,,2010
0507170006,20100507170006,,00000,1,1,1,0,0,0,,,1,
0507170006800800012030000,008613810243001,,0,822000,008613810243001,,3,1,3,0,3,0,0,1,2,0,1000,800800,910000,822000,7800,121000,,2010
0507170006,20100507170007,,00000,1,1,1,0,0,0,,1,1,
```

#### 业务日志查询

<img class="shadow" src="/img/in-post/oracle-un-query.png" width="1200" />

