---
layout:     post
title:      "Oracle案例--错误码之ORA-01578,ORA-01110"
subtitle:   "Oracle error code troubleshoot--ORA-01578,ORA-01110"
date:       2010-09-28
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# ORA-01578 和 ORA-01110数据库坏块的处理


## 表象

当Oracle数据库出现坏块时，Oracle会在警告日志文件(alert_SID.log)中记录坏块的信息: 

```shell
ORA-01578: ORACLE data block corrupted (file # 7, block # ) 
ORA-01110: data file : '/oracle1/oradata/V920/oradata/V816/users01.dbf' 
```

其中，file #代表坏块所在数据文件的绝对文件号，block #代表坏块是数据文件上的第几个数据块。出现这种情况时，应该首先检查是否是硬件及操作系统上的故障导致Oracle数据库出现坏块。在排除了数据库以外的原因后，再对发生坏块的数据库对象进行处理。

## 解决过程

步骤一、确定发生坏块的数据库对象

以下为引用的内容：

```shell
SELECT tablespace_name, segment_type, owner, segment_name FROM dba_extents 
WHERE file_id = 1
AND block_id  between block_id AND block_id+blocks-1;
```

步骤二、确立修复方法

如果发生坏块的对象是一个索引，那么可以直接把索引DROP掉后，再根据表里的记录进行重建；

如果发生坏块的表的记录可以根据其它表的记录生成的话，那么可以直接把这个表DROP掉后重建；

如果有数据库的备份，则恢复数据库的方法来进行修复；

如果表里的记录没有其它办法恢复，那么坏块上的记录就丢失了，只能把表中其它数据块上的记录取出来，然后对这个表进行重建。

步骤三、找出坏块

用Oracle提供的DBMS_REPAIR包标记出坏块: 

```shell
exec DBMS_REPAIR.SKIP_CORRUPT_BLOCKS(' ',''); 
```

步骤四、备份表

使用Create table as select命令将表中其它块上的记录保存到另一张表上以下为引用的内容：

```shell
create table corrupt_table_bak as select * from corrupt_table; 
```

步骤五、删除旧表

用DROP TABLE命令删除有坏块的表以下为引用的内容：

```drop table corrup_tatble;  ```

步骤六、重命名表

用alter table rename命令恢复原来的表以下为引用的内容：

```alter table corrupt_table_bak rename to corrupt_table; ```

步骤七、创建索引等

如果表上存在索引，则要重建表上的索引。

