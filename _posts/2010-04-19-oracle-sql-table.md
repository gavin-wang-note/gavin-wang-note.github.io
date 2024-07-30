---
layout:     post
title:      "Oracle SQL篇之表"
subtitle:   "Oracle SQL -- Table"
date:       2010-04-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
    - SQL
---


# 查看表结构

```shell
desc tablename
```

# 行数

```shell
rownum
```

# 查询用户执行过哪些sql操作

```shell
select * from v$sqlarea t where t.PARSING_SCHEMA_NAME in ('WYZ') order by t.LAST_ACTIVE_TIME desc
```

# 锁表

```shell
LOCK TABLE table1,table2,table3 IN ROW EXCLUSIVE MODE;
```

# 十进制十六进制转换

```shell
to_char(1212,'xxxx'),to_number('4bc','xxx') from dual
```

# 查看表大小


有两种含义的表大小：一种是分配给一个表的物理空间数量，而不管空间是否被使用。可以这样查询获得字节数：

```shell
select segment_name, bytes 
from user_segments 
where segment_type = 'TABLE'; 
```

或者

```shell
Select Segment_Name,Sum(bytes)/1024/1024 From User_Extents Group By Segment_Name
```

另一种表实际使用的空间。这样查询：

```shell
analyze table AREAINFO compute statistics; 

select   TABLE_NAME,TABLESPACE_NAME, NUM_ROWS ,AVG_ROW_LEN,  NUM_ROWS*AVG_ROW_LEN   
from user_tables 
where table_name = 'AREAINFO';
```

说明：

* 表名称要大写，红色加粗部分。

# 查看每个表空间的大小

```Select Tablespace_Name,Sum(bytes)/1024/1024 From Dba_Segments Group By Tablespace_Name ```

# 快速做表备份

```create table table_name as select *  from table; ```

这个是创建和table表一样的表tablke_name，包含原table表中的数据信息；

```create table table_name as select * from table where 1 = 2; ```

这个是创建和table表一样的表tablke_name，包不包含原table表中的数据信息，即为一张空表。

# 计算一个表占用的空间的大小                                     

```select owner,table_name,NUM_FREELIST_BLOCKS,LAST_ANALYZED,BLOCKS*AAA/1024/1024 "Size M" from dba_tables   where table_name='XXX'; ```

Here:
* AAA is the value of db_block_size;
* XXX is the table name you want to check

或者

```shell
select sum(bytes)/(1024*1024) as "size(M)" from user_segments 
where segment_name=upper('&table_name');
```

# 查询数据库有多少表

```shell
SQL> select * from all_tables；
SQL> select count(0) from all_tables;

  COUNT(0)
----------
      1331

SQL>
```

# 查询表中主键信息

```shell
select cu.* from user_cons_columns cu, user_constraints au 
where 
    cu.constraint_name = au.constraint_name  
and 
   au.constraint_type = 'P' and au.table_name ='RPT_DELAYTIME_20100828';
```

# 查询表的所有索引

```shell
select t.*,i.index_type 
from user_ind_columns t,user_indexes i 
where 
      t.index_name = i.index_name 
and   
      t.table_name = i.table_name 
and 
      t.table_name ='RPT_DELAYTIME_20100828';
```

# 查询表的唯一性约束

```shell
select column_name from user_cons_columns cu, user_constraints au 
where 
 cu.constraint_name = au.constraint_name 
and 
au.constraint_type = 'U' 
and 
au.table_name = 'RPT_DELAYTIME_20100828';
```

# 查找表的外键

```shell
select c.* from user_constraints c 
where 
     c.constraint_type = 'R' 
and 
c.table_name = 'RPT_DELAYTIME_20100828';
```

# 外键约束的列名

```shell
select cl.* from user_cons_columns cl where cl.constraint_name = 外键名称
```

# 引用表的键的列名

```shell
select cl.* from user_cons_columns cl where cl.constraint_name = 外键引用表的键名
```

# 停止外键语句

```shell
alter table T_BME_TASK disable constraints FK_TASKDEFINITION_TASKDEFID;
alter table T_BME_TASKRUNRESULT disable constraints FK_TASKRUNRESULT_TASKID;
alter table T_BME_TASKNOTIFYINFO disable constraints FK_TASKNOTIFYINFO_TASKID;
```

# 启用外键语句

```shell
alter table T_BME_TASK enable constraints FK_TASKDEFINITION_TASKDEFID;
alter table T_BME_TASKRUNRESULT enable constraints FK_TASKRUNRESULT_TASKID;
alter table T_BME_TASKNOTIFYINFO enable constraints FK_TASKNOTIFYINFO_TASKID;
```

# 查询表的所有列及其属性

```shell
select t.*,c.COMMENTS from user_tab_columns t,user_col_comments c
 where 
t.table_name = c.table_name 
and 
t.column_name = c.column_name 
and 
t.table_name =  'RPT_DELAYTIME_20100828';
```

# 修改表名

```shell
SQL> alter table old_table_name rename to new_table_name;
```

# 查询/搜索出前N条记录

```shell
select * from table_name where rownum <N;
select * from systemparameter where rownum <30
```

# 如何获得某张表对应的表空间信息

```shell
oracle@mmsg:~> sqlplus mmsg/mmsg@mmsgdb   //应用级用户登录oracle数据库

SQL*Plus: Release 11.1.0.7.0 - Production on 星期四 7月 1 17:34:15 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> select tablespace_name from user_tables where table_name like 'VPNCORP_30%';

TABLESPACE_NAME
------------------------------------------------------------
MMSG

SQL>
```

# oracle如何区分 64-bit/32bit 版本？

```shell
oracle@linux:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期四 7月 1 17:48:20 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> select * from v$version;

BANNER
--------------------------------------------------------------------------------
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
PL/SQL Release 11.1.0.7.0 - Production
CORE    11.1.0.7.0      Production
TNS for Linux: Version 11.1.0.7.0 - Production
NLSRTL Version 11.1.0.7.0 - Production

SQL>
```

# 分辨某个用户是从哪台机器登陆ORACLE的

```shell
SQL> SELECT machine,terminal FROM V$SESSION;
MACHINE                                                          TERMINAL
---------------------------------------------------------------- ------------------------------
linux                                                            pts/2
linux                                                            pts/2
linux                                                            pts/1
linux                                                            pts/1
linux                                                            pts/1
linux                                                            pts/2
linux                                                            pts/1
linux                                                            pts/1
linux                                                            pts/1

已选择9行。

SQL>
```

# 查看最大会话数

```shell
SQL> select * from v$parameter where name like 'proc%';
SQL> show parameter processes

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
aq_tm_processes                      integer     0
db_writer_processes                  integer     1
gcs_server_processes                 integer     0
global_txn_processes                 integer     1
job_queue_processes                  integer     1000
log_archive_max_processes            integer     4
processes                            integer     1000
SQL>

SQL> select * from v$license;  

SESSIONS_MAX SESSIONS_WARNING SESSIONS_CURRENT SESSIONS_HIGHWATER  USERS_MAX CPU_COUNT_CURRENT CPU_CORE_COUNT_CURRENT CPU_SOCKET_COUNT_CURRENT
------------ ---------------- ---------------- ------------------ ---------- ----------------- ---------------------- ------------------------
CPU_COUNT_HIGHWATER CPU_CORE_COUNT_HIGHWATER CPU_SOCKET_COUNT_HIGHWATER
------------------- ------------------------ --------------------------
           0                0               83                482          0                 8                      8                   2
                  8                        8                          2

SQL> 
```

其中sessions_highwater纪录曾经到达的最大会话数
* session数，session=processe*1.1 + 5

# 查看系统被锁的事务时间

```shell
SQL> select * from v$locked_object;

未选定行

SQL>
```

# 查得数据库的SID

```shell
SQL> select name from v$database;

NAME
------------------
MMSGDB

SQL>
```

# 获取SQL语句执行耗时时间

```shell
SQL> set timing on
SQL> select instance_number,instance_name,status from v$instance;

INSTANCE_NUMBER INSTANCE_NAME                    STATUS
--------------- -------------------------------- ------------------------
              1 mmsgdb                           OPEN

已用时间:  00: 00: 00.00
SQL>
```

# 将查询（select）的结果导入到一个文件中

```shell
oracle@mmsg:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期五 7月 2 16:55:52 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> spool test.txt
SQL> select sessions_current,sessions_highwater from v$license;

SESSIONS_CURRENT SESSIONS_HIGHWATER
---------------- ------------------
              38                 53

SQL> select instance_number,instance_name,status from v$instance;

INSTANCE_NUMBER INSTANCE_NAME                    STATUS
--------------- -------------------------------- ------------------------
              1 mmsgdb                           OPEN

SQL> show parameter spfile

NAME                                 TYPE
------------------------------------ ----------------------
VALUE
------------------------------
spfile                               string
/opt/oracle/product/11g/dbs/sp
filemmsgdb.ora
SQL> show parameter license

NAME                                 TYPE
------------------------------------ ----------------------
VALUE
------------------------------
license_max_sessions                 integer
0
license_max_users                    integer
0
license_sessions_warning             integer
0
SQL> quit  
从 Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options 断开
oracle@mmsg:~> more test.txt 
SQL> select sessions_current,sessions_highwater from v$license;

SESSIONS_CURRENT SESSIONS_HIGHWATER                                             
---------------- ------------------                                             
              38                 53                                             

SQL> select instance_number,instance_name,status from v$instance;

INSTANCE_NUMBER INSTANCE_NAME                    STATUS                         
--------------- -------------------------------- ------------------------       
              1 mmsgdb                           OPEN                           

SQL> show parameter spfile

NAME                                 TYPE                                       
------------------------------------ ----------------------                     
VALUE                                                                           
------------------------------                                                  
spfile                               string                                     
/opt/oracle/product/11g/dbs/sp                                                  
filemmsgdb.ora                                                                  
SQL> show parameter license

NAME                                 TYPE                                       
------------------------------------ ----------------------                     
VALUE                                                                           
------------------------------                                                  
license_max_sessions                 integer                                    
0                                                                               
license_max_users                    integer                                    
0                                                                               
license_sessions_warning             integer                                    
0                                                                               
SQL> quit
```

注：
* 相当于边操作边记录操作信息，并将信息追加到指定文件中，指定的文件路径可设置。

# 查询重复记录

```shell
select count(*),ACCOUNTKEY,APPLYTIME  from userdb.account 
group by ACCOUNTKEY,APPLYTIME
having count(*)>1
```

# 删除重复记录

```shell
delete from userdb.account t1 where t1.id != 
(select max(id) from userdb.account t2 where t1.ACCOUNTKEY=t2.ACCOUNTKEY and t1.APPLYTIME=t2.APPLYTIME)
```

# 字符串里加回车

```shell
select 'Welcome  to visit'||chr(10)||'www.CSD N.NET' from dual
```

# 使select语句使查询结果自动生成序号

```shell
select rownum，COL from table;
```

# 插入全年日期

```shell
create table BSYEAR (d date)；                   
　　insert into BSYEAR                                         
　　select to_date('20030101'，'yyyy mmdd')+rownum-1 
　　from all_objects                                             
　　where rownum <= to_char(to_date('20031231'，'yyyymmdd')，'ddd')；
```

# 触发器

## 查询当前触发器

```shell
SQL> set wrap off
SQL> col status format a15
SQL> col OBJECT_NAME format a20
SQL> Select object_name,status  From user_objects Where object_type='TRIGGER';
```

## 禁止、恢复触发器

### 禁止触发器

```shell
alter table accounttype disable all triggers;
```

### 恢复触发器

```shell
alter table accounttype enable all triggers;
```

# 查询当前用户下所有视图

```shell
SQL> Select object_name From user_objects Where object_type='VIEW';
```

# 查询当前用户下所有存储过程

```shell
Select object_name  From user_objects Where object_type='PROCEDURE'
```

# 查询job

## 查询所有job

```shell
SQL> col LOG_USER format a10
SQL> col PRIV_USER format a10
SQL> col SCHEMA_USER format a10
SQL> select job, LOG_USER,SCHEMA_USER,PRIV_USER from dba_jobs;
```

或者从user_jobs中获取数据。

## 查询当天跑的job

```shell
select * from all_jobs where last_date>=trunc(sysdate) 
```

## 查询某一job执行了多少小时

```shell
select  total_time/1000/60/60  from user_jobs
```

# 查询function

```shell
select object_name from user_objects  where object_type='FUNCTION';
```

# 查询sequence

```shell
SELECT OBJECT_NAME FROM USER_OBJECTS WHERE OBJECT_TYPE='FUNCTION'
```

# 查询oracle package内容

```shell
SQL> desc all_source
Name                                      Null?    Type
----------------------------------------- -------- ----------------------------
OWNER                                              VARCHAR2(30)
NAME                                               VARCHAR2(30)
TYPE                                               VARCHAR2(12)
LINE                                               NUMBER
TEXT                                               VARCHAR2(4000)
SQL>select text from all_source where name='DBMS_OUTPUT' and type='PACKAGE'
```
