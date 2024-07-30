---
layout:     post
title:      "Oracle实例与数据库的区别"
subtitle:   "Different with oracle instance and database"
date:       2010-11-18
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# oracle实例与数据库的区别

ORACLE实例 = 进程 + 进程所使用的内存(SGA)

实例是一个临时性的东西，你也可以认为它代表了数据库某一时刻的状态！

数据库 = 重做文件 + 控制文件 + 数据文件 + 临时文件

数据库是永久的，是一个文件的集合。

# ORACLE实例和数据库之间的关系

1、临时性和永久性

2、实例可以在没有数据文件的情况下单独启动 startup nomount , 通常没什么意义

3、个实例在其生存期内只能装载(alter database mount)和打开(alter database open)一个数据库

4、一个数据库可被许多实例同时装载和打开(即RAC)，RAC环境中实例的作用能够得到充分的体现

