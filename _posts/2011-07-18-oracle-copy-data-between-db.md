---
layout:     post
title:      "跨库拷贝数据"
subtitle:   "Copy data between different DB by oracle"
date:       2011-07-18
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 跨库拷贝数据（可用于视图测试）

## 使用场景

创建数据库A与B的脚本是一致的，或互相拷贝的表结构字段是一致的，或者想创建表，且表和另外一个库中的表一样时，我们可以通过如下方法快速将数据库B的表数据拷贝到A的表中。

## 实践 

A数据库假设是一个空的数据库。IP地址是10.164.75.164

B数据库假设是有大量数据的数据库。IP地址是10.168.38.52

将B的数据拷贝到A数据库。

### 步骤一、建立NET服务

在库A上创建到B的NET服务

### 步骤二、创建Database links

以PLSQL登录A数据库。新建Database links，Name填写为远程连接B数据库的代号，

连接到部分填写连接数据库B的相关信息。注意Shared（共享）要勾选。

注意:
* 要先在A数据库的机器上先建立一个本地连接到数据库B，且名字是如下输入框的Database要一致。

<img class="shadow" src="/img/in-post/oracle-conn.png" width="600" />
 

### 步骤三、拷贝数据

Apply【应用】这个数据库链接后，就可以直接按填写的name使用。

例如: ```select * from memberinfo@ora11g ```

就把数据库B的memberinfo表的数据查询出来，将数据库B的memberinfo数据插入数据库A的memberinfo表使用如下语句，注意修改表名。

```insert into memberinfo nologging select * from  memberinfo@ ora11g ```

如果没有在机器上建立本地链接，则会出现以下错误：
 
<img class="shadow" src="/img/in-post/oracle-ora-12154.png" width="300" />

