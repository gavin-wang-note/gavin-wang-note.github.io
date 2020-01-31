---
layout:     post
title:      "Oracle pfile和spfile"
subtitle:   "Oracle pfile and spfile"
date:       2012-05-02
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 参数文件的定义、作用

oracle数据库通过一系列参数来对数据库进行配置。这些参数是以键－值对的形式来表 示的，如：

```
MAXLOGFILES=50
BACKGROUND_DUMP_DEST=C:\DUMP
```

其中，等号左边是参数名，右边是对应的参数的值，值的类型有多种，典型的如数字和 字符串.

参数文件就是存储这些参数的地方，oracle在启动时会从参数文件中读取相关的配置。

# 参数文件的分类

在9i之前，参数文件只有一种，它是文本格式的，称为pfile，在9i及以后的版本中，新 增了服务器参数文件,称为spfile,它是二进制格式的。这两种参数文件都是用来存储参 数配置以供oracle读取的，但也有不同点，注意以下几点：

（1）pfile是文本文件，spfile是二进制文件；

（2）对于参数的配置，pfile可以直接以文本编辑器打开手工配置，而spfile不行，必 须在数据库启动后，通过sql命令进行在线修改。

（3）pfile配置改变后，要使用其生效，必须重新启动数据库，spfile的配置生效时限 和作用域可以由修改参数的sql命令指定，可以立即生效，也可以不立即生效。当然有些 参数的修改必须重启数据库才能生效；

（4）可用sql命令由pfile创建spfile,也可以由spfile创建pfile；

（5）如果是手动创建数据库而不是通过DBCA，则开始创建数据库时，你只能定义pfile 。因为它是文本格式的；

（6）oracle数据库只使用一个参数文件，要么是pfile,要么是spfile，即么如何判断 数据库当前使用的是哪一个参数文件呢？一种方法是能过create pfile来鉴别，如果当 前使用的不spfile,则相应格式的create pfile会产生错误。另一种方法是show  parameter  spfile命令，用来显示spfile的位置，如果显示的值为空，则表示使用的是pfile。


# 参数文件的动作原理

oracle实例在启动时，会去读取参数文件中的配置，这个过程是这样的：

数据库的startup命令中可以指定以哪个pfile来启动，但是请注意，只能指定pfile,不 能指定spfile。

当使用不带pfile 子句的startup 命令时，Oracle 将从平台指定的默认位置上的服务器 参数文件（spfile） 中读取初始化参数。Oracle查找spfile或者创通的init.ora的顺序 是：在平台指定的默认位置上，Oracle首先查找名为spfile$ORACLE_SID.ora的文件，如 果没有就查找spfile.ora文件，还没有的话，就找init$ORACLE_SID.ora文件。

在$ORACLE_BASE\admin\db_name\spfile下，你很可能可以看到一个类似这样init.ora.1 92003215317]名字的文件，这就是初始化参数文件，只是跟上了时间戳。对于Oracle920 ,缺省的就使用spfile启动，但是这个spfile不是凭空而来，而是根据这个文件创建而来 ，你可以去掉这个长后缀，就是标准的pfile文件了。

对于Windows NT 和Windows 2000  ，其位置是：$ORACLE_HOME\database\spfile$ORACLE_SID.ora

对于LINUX，可以通过show parameter spfile。

```
SQL> show parameter spfile

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
spfile                               string      /opt/oracle/product/11g/dbs/sp
                                                 filemmsgdb.ora
```

数据库在启动后，参数的配置值可以通过查询数据字典v$parameter得到。

# 参数文件的修改方法

分为手动修改和在线修改。

手动修改用于修改pfile，直接用文本编辑打开pfile修改。要使用修改生效，须重启数据库。
在线修改是在数据库运行时，用alter system命令进行修改，命令如下：

```
sql>alter system set job_queue_processed=50 scope=MEMORY;
```

注意，scope=MEMORY表示应用范围，取值如下：

SPFILE:修改只对SPFILE有效，不影响当前实例，需要重启数据库才能生效；

MEMORY:修改只对内存有效，即只对当前实例有效，且立即生效，但不会保存到SPFILE, 数据库重启后此配置丢失；

BOTH:顾名思义，包含以上两种，立即生效，且永久生效。

对于ALTER SYSTEM的参数修改命令，请注意以下几点：

（1）如果当前实例使用的是pfile而非spfile,则scope=spfile或scope=both会产生错 误；

（2）如果实例以pfile启动，则scope的默认值为MEMORY,若以spfile启动，则默认值为 BOTH；

（3）可以使用DEFERRED表示所作修改只适用于将来的会话，还可以使用COMMENT写入注 释，如：ALTER SYSTEM SET JOB_QUEUE_PROCESSES=50 SCOPE=BOTH DEFERRED COMMENT=" 注释"

（4）删除参数的方法如下：```ALTER SYSTEM SET PARAMETER='';```

# 创建参数文件

对于pfile，你可以用文本编辑器直接手工编辑一个，也可以使用create pfile命令 从spfile创建，如：```CREATE PFILE='/opt/oracle/product/11g/dbs/pfilemmsgdb.ora' FROM  SPFILE='/opt/oracle/product/11g/dbs/spfilemmsgdb.ora '```,或者从当前实例所使用的spfile创建：```create  pfile='/opt/oracle/product/11g/dbs/pfilemmsgdb.ora ' from spfile```。

