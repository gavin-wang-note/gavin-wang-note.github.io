---
layout:     post
title:      "Oracle管理篇之几种name"
subtitle:   "Oracle different name"
date:       2010-10-17
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 概述

在修改数据名、修改数据库实例名等操作过程中，需要清楚几种name。

本章节汇集并概述一下oracle 11g中目前显示的几种name信息。

# Oracle中几种name信息

```shell
oracle@mmsg37:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期日 10月 17 01:37:10 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> show parameter name

NAME                                 TYPE        VALUE
--------------------------  ----------- ------------------------------
db_file_name_convert             string
db_name                             string       mmsgdb
db_unique_name                     string       mmsgdb
global_names                       boolean      FALSE
instance_name                      string       mmsgdb
lock_name_space                    string
log_file_name_convert             string
service_names                       string      mmsgdb
SQL>
```

# 数据库名

## 体现方式db_name

数据库名就是一个数据库的标识，具有唯一性，如果一个机器上安装多个数据库，每个数据库名均不同。在数据库安装完成或者创建完成之后，db_name写入参数文件中：
*.db_name='mmsgdb'

在创建数据库时就应该考虑好数据库名，在创建完数据库之后，可以修改数据库名，不过在此之前需要修改二进制的控制文件。一般的不建议修改数据库名。


## 数据库名的作用

数据库名是在安装数据库、创建新的数据库、创建数据库控制文件、修改数据结构、备份与恢复数据库时都需要使用到的。

有很多Oracle安装文件目录是与数据库名相关的，如：

```shell
$ORACLE_BASE /oradata/DB_NAME/
$ORACLE_BASE/admin/DB_NAME/
$ORACLE_BASE/cfgtoollogs/dbca/DB_NAME/
$ORACLE_BASE /diag/rdbms/DB_NAME/
```

发布变更数据库结构的alter database 语句时，后面指定数据库名，如果数据库名和参数文件中不一致，发布语句报错；

控制文件孙损坏，数据库不能加载控制文件时，在非安装模式下创建控制文件，create controlfile命令中指定数据库名；

数据库的备份与恢复时，也会使用到数据库名。

## 查看当前数据库名


方法一：```select name from v$database; ```

方法二：```show parameter name，找到参数db_name 对应的strings类型值；```

方法三：直接查看参数文件（spfile文件为二进制，通过strings命令查看）

## 修改数据库名

简介一下在安装了数据库之后修改数据库名的步骤

### 1、关闭数据库

### 2、以nomount方式启动数据库

### 3、通过spfile文件创建pfile文件

### 4、修改pfile文件中db_name参数值

### 5、创建控制文件，重置重做日志文件（reset redolog）

### 6、指定pfile文件启动数据库，并创建spfile文件

### 7、重启数据库


# 数据库实例名

据库实例名是用于和操作系统进行联系的标识，就是说数据库和操作系统之间的交互用的是数据库实例名。数据库实例名也写入参数：instance_name。

数据库名可以和实例名相同，也可以不同。一般情况下，数据库名和实例名一一对应，RAC集群环境中，一个数据库名对应多个实例名。

## 查看数据库的实例名

方法一：```show parameter instance_name ```

方法二：```select instance_name from v$instance；```

## ORACLE_SID

数据库实例名和ORACLE_SID，两者虽然都表示为数据库实例名，但仍然有区别。

Instance_name是数据库参数，ORACLE_SID是操作系统环境变量。

ORACLE_SID与操作系统交互，从操作系统的角度访问数据库，需要ORACLE_SID，且ORACLE_SID必须与instance_name一致，否则访问数据库时会报错。

## db_domain

db_domain是数据库域名，只要用于分布式数据库中。

比如：国家民政部系统的分布式数据库为：

江苏节点：js.civil
江苏南京节点：nj.js.civil
浙江节点：zj.civil
浙江湖州：hz.zj.civil

当北京需要连接湖州数据库时，发布sqlplus命令，sqlplus user/passwd@name.db_domain。比如：sqlplus mmsg/mmsg@mmsgdb_119.hz.zj.civil, 这就是域名。

## 查看域名信息
方法一：select value from v$parameter where name = 'db_domain';
方法二 ：show parameter db_domain
方法三：直接查看spfile文件

# 全局数据库名

全局数据库名=数据库名+数据库域名，即如前面提到的mmsgdb_119.hz.zj.civil

对应参数global_names。

# 数据库服务名

对应参数service_names，从9i开始引入。

如果数据库有全局数据库名，则数据库服务名和数据库服务名一致，如果没有db_domain，则instance_names与数据库名一致。

## 查看数据库服务名

方法一：```show parameter service_names```

方法二：```select value from v$parameter where name = 'service_name'; ```

