---
layout:     post
title:      "Oracle表空间管理"
subtitle:   "Manager Oracle tablespace"
date:       2013-03-10
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 与表空间相关的视图 

| 段类型                   | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
|V$TABLESPACE 	|控制文件中保存的所有表空间的名称和数量 |
|DBA_TABLESPACES 	|所有表空间的描述信息 |
|USER_TABLESPACES 	|所有用户可访问表空间的描述信息 |
|DBA_TABLESPACE_GROUPS 	|所有表空间组及其所属的表空间信息|
|DBA_SEGMENTS 	|所有表空间中的区间信息 |
|USER_SEGMENTS 	|所有用户表空间中的区间信息 |
|DBA_FREE_SPACE 	|所有表空间中的空闲区间信息 |
|USER_FREE_SPACE 	|所有用户表空间中的空闲区间信息 |
|V$DATAFILE 	|所有数据文件信息 |
|V$TEMPFILE 	|所有临时文件信息 |
|DBA_DATA_FILES 	|显示所有属于表空间的数据文件信息 |
|DBA_TEMP_FILES 	|显示所有属于临时表空间的临时文件信息 |
|V$TABLESPACE 	|控制文件中保存的所有表空间的名称和数量 |
|DBA_TABLESPACES 	|所有表空间的描述信息 |


# 创建表空间

```shell
CREATE TABLESPACE tablespace_name 
DATAFILE  '/path/filename' SIZE integer [K|M] REUSE 
[，'/path/filename' SIZE integer [K|M] REUSE] 
[AUTOEXTEND [ OFF | ON  NEXT integer [ K | M ]  ] [ MAXSIZE [ UNLIMITED | integer [ K | M ] ] ]  ]
[ MINIMUM  EXTENT  integer [ K | M ]  ]
[DEFAULT STORAGE storage ]
[ ONLINE | OFFLINE ]
[ LOGGING | NOLOGGING ]
[ PERMANENT | TEMPORARY ]
[EXTENT MANAGEMENT
[ DICTIONARY | LOCAL [ AUTOALLOCATE | UNIFORM SIZE integer [ K | M ] ]  ]
 ]
```

解释：

1、一个表空间可以拥有多个数据文件，create tablespace时，各个数据文件使用英文状态下的逗号分隔；

2、数据文件是否自动扩展，默认off

3、minimum

4、default storeage 设置默认存储
```shell
        default storage(
        initial 192K
        next 192K
        minextents 1
        pctincrease 0)
```

5、数据文件在线还是脱机，默认online

6、Logging与nologging，区别在于是否忽略日志记录

7、 EXTENT MANAGEMENT，表空间管理方式，分为数据字典管理和本地管理

# 字典管理方式的表空间

表空间中所有存储空间的管理信息都保存在数据字典中，在进行存储空间管理时会产生回退和重做记录

# 本地管理方式的表空间

表空间中所有存储空间的管理信息都保存在数据文件头部的位图中

本地管理方式的表空间具有如下优点:

1、在存储分配过程中不需要访问数据库，可以提高存储分配操作的速度

2、能够避免在表空间的存储管理操作中产生的递归现象

3、不会产生重做和撤销记录

4、简化DBA对表空间的管理操作

5、降低用户对数据字典的依赖性

# 大文件表空间

Bigfile与smallfile文件

这种类型的表空间只能有一个数据文件，且该数据文件允许有4G的数据快，即如果db_block_size=8k的话，最大容量为4G*8K=32T，当然，这个还要看操作系统的限制了。

一般应该不会这样的用的。

理论上的 BFT 可以达到下面所列的值：

```shell
数据块大小(单位：K)   BFT 最大值(单位：T) 
         2k                    8T 
         4k                    16T 
         8k                    32T 
         16k                   64T 
         32k                  128T 
```

# 查询网关默认数据文件类型

```shell
select property_name,property_value from database_properties where property_name='DEFAULT_TBS_TYPE';
```
修改数据库默认的表空间类型为smallfile,就可以为表空间创建多个数据文件了。

```shell
SQL> alter database set default smallfile tablespace;

Database altered
```

也可以在创建表空间时，指定表空间类型：create smallfile/bigfile  tablespace ...

# 重命名表空间

```shell
SQL> select * from v$tablespace;
       TS# NAME                           INC BIG FLA ENC
---------- ------------------------------ --- --- --- ---
         0 SYSTEM                         YES NO  YES
         1 SYSAUX                         YES NO  YES
         2 UNDOTBS1                       YES NO  YES
         3 TEMP                           NO  NO  YES
         4 USERS                          YES NO  YES
         5 MMSG                           YES NO  YES
         6 MMSG_TMP                       NO  NO  YES
         7 YJH                            YES NO  YES
         8 YJH_TMP                        NO  NO  YES
         9 WYZ                            YES NO  YES
        10 WYZ_TMP                        NO  NO  YES
       TS# NAME                           INC BIG FLA ENC
---------- ------------------------------ --- --- --- ---
        11 WYZTEST                        YES NO  YES
        12 WYZTESTTEMP                    NO  NO  YES
已选择13行。
SQL> alter tablespace wyztest rename to wyztest0;
表空间已更改。
SQL> select * from v$tablespace;
       TS# NAME                           INC BIG FLA ENC
---------- ------------------------------ --- --- --- ---
         0 SYSTEM                         YES NO  YES
         1 SYSAUX                         YES NO  YES
         2 UNDOTBS1                       YES NO  YES
         3 TEMP                           NO  NO  YES
         4 USERS                          YES NO  YES
         5 MMSG                           YES NO  YES
         6 MMSG_TMP                       NO  NO  YES
         7 YJH                            YES NO  YES
         8 YJH_TMP                        NO  NO  YES
         9 WYZ                            YES NO  YES
        10 WYZ_TMP                        NO  NO  YES
       TS# NAME                           INC BIG FLA ENC
---------- ------------------------------ --- --- --- ---
        11 WYZTEST0                       YES NO  YES
        12 WYZTESTTEMP                    NO  NO  YES
已选择13行。
SQL> 
```

# 本地管理表空间

在ALTER TABLESPACE语句中使用ADD DATAFILE子句，可以在本地管理表空间中增加数据文件，代码如下：

```shell
SQL> alter tablespace wyztest 
add datafile '/opt/oracle/oradata/mmsgdb/wyztest01.dbf‘
size 10m
autoextend on next 10m maxsize 100m
表空间已更改。
SQL>
```

# 重置表空间大小

在ALTER database语句中使用resize子句，可以在本地管理表空间中修改数据文件大小，代码如下：

## 改变数据文件大小

```shell
SQL> alter database datafile '/opt/oracle/oradata/mmsgdb/wyztest01.dbf' resize 15m;
数据库已更改。
```

# 修改数据文件增长方式

在ALTER database语句中使用autoextend子句，可以在本地管理表空间中修改数据文件（不）自动扩展，代码如下：

## 修改数据文件的增长方式

```shell
SQL> alter database datafile  '/opt/oracle/oradata/mmsgdb/wyztest.dbf' 
 2  autoextend on next 15m maxsize 150m; 
数据库已更改。
SQL>
```

## 关闭自动表空间自动扩展

```shell
SQL> alter database datafile '/opt/oracle/oradata/mmsgdb/wyztest.dbf' 
  2  autoextend off;
数据库已更改。
SQL> 
```

# 改变数据文件的名称和位置

## 场景一 数据文件属于同一个表空间

1；将包含数据文件的表空间置为脱机状态

```shell
SQL> alter tablespace wyztest offline normal;
表空间已更改。
```

2：os level级重命名表空间下的数据文件名称

```shell
oracle@mmsg37:~/oradata/mmsgdb> mv wyztest01.dbf wyztest00.dbf 
```

3：在数据库内部修改数据文件的名称或者改变数据文件的位置

```shell
alter tablespace tablespace_name 
rename datafile  ‘xxxxx’ to ‘xxxx’;
改变名称
SQL> alter tablespace wyztest 
  2  rename datafile 
  3  '/opt/oracle/oradata/mmsgdb/wyztest01.dbf' to
  4  '/opt/oracle/oradata/mmsgdb/wyztest00.dbf';
alter tablespace wyztest     //这里报错，是因为当初没有执行o slevel的命名操作，必须要执行第二步的重命名操作。
*
第 1 行出现错误:
ORA-01525: 重命名数据文件时出错
ORA-01141: 重命名数据文件 7 时出错 - 未找到新文件
'/opt/oracle/oradata/mmsgdb/wyztest00.dbf'
ORA-01110: 数据文件 7: '/opt/oracle/oradata/mmsgdb/wyztest01.dbf'
ORA-27037: 无法获得文件状态
Linux-x86_64 Error: 2: No such file or directory
Additional information: 3
SQL> /
表空间已更改。
```

更改位置

```shell
 alter tablespace wyztest 
Rename datafile '/opt/oracle/oradata/mmsgdb/wyztest01.dbf’ to
‘/home/oradata/mmsgdb/wyztest02.dbf’   //前提条件是/home/oradata/mmsgdb/目录存在，且oracle对该目录具有可操作权限
```

4：将表空间置为联机状态

```shell
SQL> alter tablespace wyztest online;
表空间已更改。
SQL> 
```

5：备份控制文件

## 场景二 要改变的数据文件属于多个表空间

1：关闭数据库

2：os level级重命名或者移动数据文件

3：加载数据库到mount状态 startup mount

4：在数据库内部更改数据文件名称或者位置（alter datafile rename datafile ‘xxxxx01  ‘xxxx02’ to ‘yyyy01’ ‘yyyy02’;） //to 之后的文件必须存在，也就是 os level级的操作是必须做的

5：open数据库 alter database open;

6：备份控制文件


# 设置只读表空间

ALTER TABLESPACE…READ ONLY语句设置只读表空间

【例】将表空间wyztest设置为只读表空间：

```shell
SQL> alter tablespace  wyztest read only;
```

ALTER TABLESPACE…READ WRITE语句可以将只读表空间设置为可读写状态

【例】将表空间wyztest设置为可读写状态：

```shell
SQL> alter tablespace  wyztest read  write;
```

# 删除表空间

删除表空间的时候可以清除表空间的内容以及表空间对应的数据文件

适用情况 
1：不小心给不需要的表空间增加了数据文件；
2：设置的数据文件较大，想删除后重新创建；
```shell
   drop tablesapce tablespacename  including contents;
   drop tablespace tablespacename including contents and datafiles;
```

## A：所在表空间只有一个数据文件

只要简单地删除表空间即可：

```shell
drop tablespace tablespace_name including contents;
```

## B：如果表空间有多个数据文件

1、不再需要表空间中的内容，或者可以很容易重新产生表空间的内容，可以使用

```drop tablespace tablespace_name including contents;``` 命令来从Oracle数据字典删除表空间、数据文件和表空间的内容。

Oracle不会再访问该表空间中的任何内容, 然后重新创建表空间并重新导入数据。

2、需要保留该表空间中的其它数据文件中的内容

必须首先export导出该表空间中的所有内容。为了确定表空间中包含哪些内容，运行：

```shell
select owner,segment_name,segment_type 
from dba_segments 
where tablespace_name='<name of tablespace>'
```

export出你想保留的内容。如果export结束，就可以使用drop tablespace tablespace_name including contents; ，这样永久删除表空间的内容，使用操作系统命令物理删除数据文件，按所需数据文件重新创建表空间，把数据import至表空间。

这里要区别于```alter databade datafile ‘/opt/oracle/oradata/mmsgdb/wyztest.dbf’offline drop ```操作
。
Offline drop 将数据文件脱机，而不是删除对应的数据文件，数据库不会再访问这部分数据文件的内容，但它仍然是表空间的一部分。这个数据文件在控制文件中标记为offline状态，在数据库启动时不会将它与控制文件中的SCN比较，跳过对offline 的数据文件的读取操作，这里控制文件保留这个数据文件的入口，方便后续的介质恢复（归档模式下）

