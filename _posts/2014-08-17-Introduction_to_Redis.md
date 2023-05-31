---
layout:     post
title:      "Redis入门"
subtitle:   "Getting Started with Redis"
date:       2014-08-17
author:     "Gavin"
catalog:    true
tags:
    - Redis
---



# 概述

Gikoo的产品后端使用的数据库是Redis，本文介绍Redis的入门。



# Redis概念


<img class="shadow" src="/img/in-post/redis/overview_of_various_databases.png" width="1200">

Redis是一款高性能的NOSQL系列的非关系型数据库。

## 1.1、什么是NOSQL

NOSQL（NOSQL = Not Only SQL），意即“不仅仅是SQL”，是一项全新的数据库理念，泛指非关系型的数据库。随着互联网Web2.0网站的兴起，传统的关系型数据库在应付Web2.0网站，特别是超大规模和高并发的SNS类型的Web2.0纯动态网站已经显得力不从心，暴露了很多难以克服的问题，而非关系型的数据库则由于其本身的特点得到了非常迅速的发展。NOSQL数据库的产生就是为了解决大规模数据集合多重数据种类带来的挑战，尤其是大数据应用难题。

### 1.1.1、NOSQL和关系型数据库比较

优点：

- 成本：NOSQL数据库简单易部署，基本都是开源软件，不需要像使用oracle那样花费大量成本购买使用，相比关系型数据库价格便宜。
- 查询速度：NOSQL数据库将数据存储于缓存之中，关系型数据库将数据存储在硬盘中，自然查询速度远不及NOSQL数据库。
- 查询数据的格式：NOSQL的存储格式是key，value形式、文档形式、图片形式等等，所以可以存储基础类型以及对象或者是集合等各种格式，而数据库则只支持基础类型。
- 扩展性：关系型数据库有类似join这样的多表查询机制的限制导致扩展很艰难。

缺点：

- 维护的工具和资料有限，因为NOSQL是属于新的技术，不能和关系型数据库十几年的技术同日而语。
- 不提供对SQL的支持，如果不支持SQL这样的工页标准，将产生一定用户的学习和使用成本。
- 不提供关系型数据库对事务的处理。

### 1.1.2、非关系型数据库的优势

性能NOSQL是基于键值对的，可以想象成表中的主键和值的对应关系，而且不需要经过SQL层的解析，所以性能非常高。

可扩展性同样也是因为基于键值对，数据之间没有耦合性，所以非常容易水平扩展。

### 1.1.3、关系型数据库的优势

复杂查询可以用SQL语句方便地在一个表以及多个表之间做非常复杂的数据查询。

事务支持使得对于安全性能很高的数据访问要求得以实现。对于这两类数据库，对方的优势就是就是自己的弱势，反之亦然。

### 1.1.4、总结

关系型数据库与NOSQL数据库并非对立而是互补的关系，即通常情况下使用关系型数据库，在适合使用NOSQL的时候使用NOSQL数据库，让NOSQL数据库对关系型数据库的不足进行弥补。一般会将数据存储在关系型数据库中，在NOSQL数据库中备份存储关系型数据库的数据。

## 1.2、主流的NOSQL产品

### 1.2.1、键值（Key-Value）存储数据库

- 相关产品：Tokyo Cabinet/Tyrant、Redis、Voldemort、Berkeley DB。
- 典型应用：内容缓存，主要用于处理大量数据的高访问负载。
- 数据模型：一系列键值对。
- 优势：快速查询。
- 劣势：存储的数据缺少结构化。

### 1.2.2、列存储数据库

- 相关产品：Cassandra、HBase、Riak。
- 典型应用：分布式的文件系统。
- 数据模型：以列簇式存储，将同一列数据存在一起。
- 优势：查找速度快，可扩展性强，更容易进行分布式扩展。
- 劣势：功能相对局限。

### 1.2.3、文档型数据库

- 相关产品：CouchDB、MongoDB。
- 典型应用：Web应用（与Key-Value类似，Value是结构化的）。
- 数据模型：一系列键值对。
- 优势：数据结构要求不严格。
- 劣势：查询性能不高，而且缺乏统一的查询语法。

### 1.2.4、图形（Graph）数据库

- 相关数据库：Neo4J、InfoGrid、Infinite Graph。
- 典型应用：社交网络。
- 数据模型：图结构。
- 优势：利用图结构相关算法。
- 劣势：需要对整个图做计算才能得出结果，不容易做分布式的集群方案。

## 1.3、什么是Redis

Redis使用C语言开发的一个开源的高性能键值对（Key-Value）数据库，官方提供测试数据，50个并发执行的100000个请求，读的速度是110000次/s，写的速度是81000次/s，且Redis通过提供多种键值数据类型来适应不同场景下的存储需求，摸钱为止Redis支持的键值数据类型如下：

- 字符串类型：string
- 哈希类型：hash
- 列表类型：list
- 集合类型：set
- 有序集合类型：sortedset

### 1.3.1、Redis的应用场景

- 缓存（数据查询、短连接、新闻内容、商品内容等等）；
- 聊天室的在线好友列表；
- 任务队列（秒杀、抢购、12306等等）；
- 应用排行榜；
- 网站访问统计；
- 数据过期处理（可以精确到毫秒）；
- 分布式集群架构中的session分离。

# 2、下载安装

1、官网：https://redis.io

2、中文网：www.redis.net.cn/download/

3、解压直接可以使用：

```java
redis.windows.conf：配置文件
redis-cli.exe：redis的客户端
redis-server.exe：redis的服务器端
```

# 3、命令操作

## 3. 1、Redis的数据结构

<img class="shadow" src="/img/in-post/redis/redis-struct.png" width="1200">

```java
redis存储的是key-value格式的数据，其中key都是字符串，value有5种不同的数据结构。

value 的数据结构：
    1）字符串类型 string
    2）哈希类型 hash ： map格式
    3）列表类型 list ： linkedlist格式
    4）集合类型 set ： （与list相比不允许重复元素）
    5）有序集合类型 sortedset ： 不允许重复元素，且元素有顺序
```

## 3.2、字符串类型 string

```java
1、存储：set key value
2、获取：get key
3、删除：del key
```

## 3.3、哈希类型 hash

```java
1、存储：hset key field value
2、获取：
    hget key field：获取指定的field对应的value
    hgetall key：获取所有的field和value
3、删除：hdel key field
```

## 3.4、列表类型 list

列表类型list：可以添加一个元素到列表的头部（左边）或者尾部（右边）。

```java
1、存储：
    lpush key value：将元素加入列表左边。
    rpush key value：将元素加入列表右边。
2、获取：get key
    lrange key start end：范围获取
3、删除：del key
    lpop key：删除列表最左边的元素，并将元素返回。
    rpop key：删除列表最右边的元素，并将元素返回。
```

## 3.5、集合类型 set

集合类型set：不允许重复元素。

```java
1、存储：sadd key value
2、获取：smembers key：获取set集合中所有元素
3、删除：srem key value：删除set集合中的某个元素
```

## 3.6、有序集合类型

有序集合类型sortedset：不允许重复元素，且元素有顺序。

```java
1、存储：zadd key score value
2、获取：zrange key start end
3、删除：zrem key value
```

## 3.7、通用命令

```java
1、keys * ：查询所有的键
2、type key：获取键对应的value的类型
3、del key：删除指定的key value
```

# 4、持久化操作

1、Redis是一个内存数据库，当Redis服务器重启，或者电脑重启，数据会丢失，我们可以将Redis内存中的数据持久化保存到硬盘中的文件中。

2、Redis的持久化机制：

- RDB：默认方式，不需要进行配置，默认就是用这种机制。在一定的间隔时间中，检测key的变化情况，然后持久化数据。

  ```java
  使用步骤：
  1、编辑redis.windows.conf文件；
      # after 900 sec (15 min) if at least 1 key changed
      save 900 1
      # after 300 sec (5 min) if at least 10 key changed
      save 300 10
      # after 60 sec (15 min) if at least 10000 key changed
      save 60 10000
  
  2、重新启动redis服务器，并指定配置文件名称。
      D:\redis-2.8.9|redis-server.exe redis.windows.conf
  ```

- AOF：日志记录的方式，记录每一条命令的操作。可以每一次命令操作后，持久化数据。

  ```java
  使用步骤：
  1、编辑redis.windows.conf文件
      appendonly on （关闭aof） --> appendonly yes （开启aof）
  
      # appendfsync always ：每一次操作都进行持久化
      appendfsync everysec ：每隔一秒进行一次持久化
      # appendfsync no ：不进行持久化
  ```

