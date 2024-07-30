---
layout:     post
title:      "Oracle审计功能简介"
subtitle:   "Oracle Audit"
date:       2009-04-08
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---



# 关于审计

审计（Audit)，用于监视用户所执行的数据库操作，并且Oracle会将审计跟踪结果存放到OS文件（默认位置为$ORACLE_BASE/admin /$ORACLE_SID/adump/）或数据库（存储在system表空间中的SYS.AUD$表中，可通过视图dba_audit_trail查 看）中。Oracle11g默认情况下审计是开启的。

不管你是否打开数据库的审计功能，以下这些操作系统会强制记录：用管理员权限连接Instance；启动数据库；关闭数据库。

# 和审计相关的两个主要参数

## 1、Audit_sys_operations

```shell
SQL> show parameter Audit_sys_operations

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_sys_operations                 boolean     FALSE
SQL>  
```

默认为false，当设置为true时，所有sys用户（包括以sysdba,sysoper身份登录的用户）的操作都会被记录。audit trail不会写在aud$表中，这个很好理解，如果数据库还未启动aud$不可用，那么像conn /as sysdba这样的连接信息，只能记录在其它地方。如果是windows平台，audti trail会记录在windows的事件管理中，如果是linux/unix平台则会记录在audit_file_dest参数指定的文件中。audit_file_dest参数实际是个路径信息：

```shell
SQL> show parameter audit_file_dest

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_file_dest                      string      /opt/oracle/admin/mmsgdb/adump
SQL>
```

## 2、Audit_trail

None：不做审计；
DB：将audit trail 记录在数据库的审计相关表中，如aud$，审计的结果只有连接信息；
DB,Extended：这样审计结果里面除了连接信息还包含了当时执行的具体语句；
OS：将audit trail 记录在操作系统文件中，文件名由audit_file_dest参数指定；
XML：自oracle 10g里新增的。

注：
这两个参数是static参数，需要重新启动数据库才能生效。

# 审计级别

当开启审计功能后，可在三个级别对数据库进行审计：Statement(语句)、Privilege（权限）、object（对象）。

## Statement

按语句来审计，比如audit table 会审计数据库中所有的create table,drop table,truncate table语句，alter session by mmsg会审计mmsg用户所有的数据库连接。

## Privilege

按权限来审计，当用户使用了该权限则被审计，如执行grant select any table to mmsg，当执行了audit select any table语句后，当用户mmsg 访问了用户wyz的表时（如select * from wyz.table_name）会用到select any table权限，故会被审计。

注:
* 用户是自己表的所有者，所以用户访问自己的表不会被审计。

## Object

按对象审计，只审计on关键字指定对象的相关操作，如aduit alter,delete,drop,insert on mmsg.table by scott; 这里会对mmsg用户的table表进行审计，但同时使用了by子句，所以只会对scott用户发起的操作进行审计。

说明:

* Oracle没有提供对schema中所有对象的审计功能，只能一个一个对象审计，对于后面创建的对象，Oracle则提供on default子句来实现自动审计，比如执行audit drop on default by access;后，对于随后创建的对象的drop操作都会审计。但这个default会对之后创建的所有数据库对象有效，似乎没办法指定只对某个用户创建 的对象有效，想比 trigger可以对schema的DDL进行“审计”，这个功能稍显不足。

# 审计的一些其他选项

by access / by session：
by access 每一个被审计的操作都会生成一条audit trail。 
by session 一个会话里面同类型的操作只会生成一条audit trail，默认为by session。

whenever [not] successful：
whenever successful 操作成功(dba_audit_trail中returncode字段为0) 才审计,
whenever not successful 反之。省略该子句的话，不管操作成功与否都会审计。

# 和审计相关的视图

## dba_audit_trail

保存所有的audit trail，实际上它只是一个基于aud$的视图。其它的视图 dba_audit_session,dba_audit_object,dba_audit_statement都只是dba_audit_trail 的一个子集。

## dba_stmt_audit_opts

可以用来查看statement审计级别的audit options，即数据库设置过哪些statement级别的审计。dba_obj_audit_opts,dba_priv_audit_opts视图功能与之类似.

## all_def_audit_opts

用来查看数据库用on default子句设置了哪些默认对象审计。

# 取消审计

将对应审计语句的audit改为noaudit即可，如audit session whenever successful对应的取消审计语句为noaudit session whenever successful;

# 审计能告诉我们什么

Oracle 数据库审计以一种非常详细的级别捕获用户行为，它可以消除手动的、基于触发器的审计。

假定用户 Joe 具有更新那张表的权限，并按如下所示的方式更新了表中的一行数据：

```shell
update SCOTT.EMP set salary = 12000 where empno = 123456;
```

如何在数据库中跟踪这种行为呢？在 Oracle 9i 数据库及其较低版本中，审计只能捕获“谁”执行此操作，而不能捕获执行了“什么”内容。例如，它让您知道 Joe 更新了 SCOTT 所有的表EMP，但它不会显示他更新了该表中员工号为 123456 的薪水列。它不会显示更改前的薪水列的值。要捕获如此详细的更改，你将不得不编写你自己的触发器来捕获更改前的值，或使用 LogMiner 将它们从存档日志中检索出来。

细粒度审计(FGA) ，是在 Oracle 9i 中引入的，能够记录 SCN 号和行级的更改以重建旧的数据，但是它们只能用于 select 语句，而不能用于 DML（Data Manipulation Language，数据操纵语言命令） ，如 update 、insert 和delete 语句。因此，对于 Oracle 数据库 10g 之前的版本，使用触发器虽然对于以行级跟踪用户初始的更改是没有吸引力的选择，但它也是唯一可靠的方法。


# 举例详解

## 准备工作

```shell
SQL> show parameter audit

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_file_dest                      string      /opt/oracle/admin/mmsgdb/adump
audit_sys_operations                 boolean     FALSE
audit_syslog_level                   string
audit_trail                          string      DB
SQL> show parameter spfile

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
spfile                               string      /opt/oracle/product/11g/dbs/sp
                                                 filemmsgdb.ora
SQL> alter system set audit_sys_operations=TRUE scope=spfile;

系统已更改。

SQL> alter system set audit_trail=db,extended scope=spfile;

系统已更改。

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。


SQL> startup force
ORACLE 例程已经启动。

Total System Global Area 1603411968 bytes
Fixed Size                  2160112 bytes
Variable Size             620759568 bytes
Database Buffers          973078528 bytes
Redo Buffers                7413760 bytes
数据库装载完毕。
数据库已经打开。
SQL> show parameter audit

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_file_dest                      string      /opt/oracle/admin/mmsgdb/adump
audit_sys_operations                 boolean     TRUE
audit_syslog_level                   string
audit_trail                          string      DB, EXTENDED
SQL>
```

## 开始审计

```shell
SQL> create table wyz_test as select * from mmsg.vpncorp_300;

表已创建。

SQL>

SQL> audit all on wyz_test;

审计已成功。

SQL> select * from wyz_test;

SHORTNUMBE MEMBERID              A
---------- --------------------- -
66666      13810243003           0
66101      13810243001           1
66102      13810243002           0

SQL> insert into wyz_test(SHORTNUMBER,MEMBERID,ADMINFLAG) values (88888,13951775214,0);

已创建 1 行。
SQL> delete from  wyz_test;

已删除4行。

SQL> commit;

提交完成。

SQL>select OS_USERNAME,username,USERHOST,TERMINAL,TIMESTAMP,OWNER,obj_name,ACTION_NAME,sessionid,os_process,sql_text from dba_audit_trail;

sql> audit select table by u_test by access;
```

如果在命令后面添加by user则只对user的操作进行审计,如果省去by用户,则对系统中所有的用户进行审计(不包含sys用户).

# 撤销审计

```shell
SQL> noaudit all on wyz_test;
审计未成功。
```

# 关闭数据库审计功能

执行此任务可以关闭Oracle的审计功能。

在Oracle11g中，创建数据库时默认会打开审计功能，默认的audit会记录session登录数据库的信息、数据库关闭/启动和用户授权等信息。有可能大量审计记录将写满系统表空间，导致数据库异常。

## (1)登录数据库

以oracle用户登录，连接数据库。

```shell
$ sqlplus "/ as sysdba"
```

## (2)参数检测

检查是否进行审计。

```shell
SQL> show parameter audit_trail
NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_trail                          string      DB
```

若audit_trail的值为DB表示进行审计，并将审计记录存储在数据库中，默认记录在sys.aud$表中。详细的审计记录信息可以查看DBA_AUDIT_TRAIL和DBA_COMMON_AUDIT_TRAIL这两个数据字典视图。

```shell
SQL> select action_name, count(*) from dba_audit_trail group by action_name;
ACTION_NAME                    COUNT(*)
---------------------------- ----------
LOGOFF                             2137
LOGON                              1839
CREATE ROLE                           1
ALTER USER                            1
SET ROLE                             16
SYSTEM GRANT                         24
CREATE USER                           9
ALTER DATABASE                        6
```

## (3)修改参数

从表中可以看出LOGOFF记录了数据库关闭的2137条相关记录。

```shell
SQL> truncate table sys.aud$;
SQL> alter system set audit_trail=none scope=spfile;
重新启动数据库。
SQL> shutdown immediate
SQL> startup
```

