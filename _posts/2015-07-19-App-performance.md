---
layout:     post
title:      "APP性能数据收集操作指南"
subtitle:   "APP performance autotest"
date:       2015-07-19
author:     "Gavin"
catalog:    true
tags:
    - APP
    - performance
    - Automation
---



# 功能描述

集成monkey功能， android测试工作中常用测试脚本，以及在手工测试app端功能时，自动收集相关数据，并生成HTML报告。

```需要源码的，请发我163邮箱```
 

**monkey****稳定性测试：**

  （1）monkey各参数从配置文件中读取，基本涵盖monkey所有参数，可随时调整/修改配置项值；

  （2）获取logcat、traces、monkey日志，出现问题时可通知日志进行问题初步分析；

  （3）捕获JAVA异常日志，提取异常日志写入error文件，并统计异常日志

  

**performance** **数据收集：**

  （1）获取终端设备硬件信息（Results Summary）

  （2）app平均启动时间

  （3）获取cpu、cpu load、memory、flow上下行（WIFI）信息

  （4）处理获取数据，写入文本文件，同时入库（SQLIte）

  （5）绘曲线图，并生成HTML测试报告

 

 

**其他脚本：**

  （1）批量备份/安装/卸载APP；

  （2）kill 5037进程

  （3）获取全局cpu、mem信息并绘曲线图

  （4）获取当前activity

  （5）获取安装包名称（package_name）

  （6）获取安装包详细信息

  （7）截屏，传到本地PC

  （8）屏幕操作过程录制（要求sdk version>=19）

  

# 实现方法

 1、采用python脚本来驱动测试；

 2、调用android SDK adb与monkey命令，进行数据采集和稳定性测试；

 3、采集数据写入文件和数据库；

 4、附带android其他小脚本，便于测试过程中使用；

 5、根据实际情况修改配置文件后进行数据采集，生成静态HTML报告，数据一目了然

 

# 目录结构

代码目录结构：

<img class="shadow" src="/img/in-post/app_performance_code_tree.png" width="400">

 

 

# 性能数据收集使用指南

## 测试准备

### 1、配置文件

只需保证配置文件内容正确即可。

配置文件存放在src/config/目录下，名称是：config.ini。配置文件各参数介绍，请参考下图：

<img class="shadow" src="/img/in-post/config_ini.png" width="1200">

 

### 2、SQLIte数据库表设计说明

<img class="shadow" src="/img/in-post/table_desc.png" width="1200">



### 3、创建表SQL语句

<img class="shadow" src="/img/in-post/sqlite_create_tab.png" width="1200">

 

 

### 4、涉及的第三方模块

| 模块名称    | 安装命令                    | 模块说明     |
| ----------- | --------------------------- | ------------ |
| progressbar | pip  install progressbar    | 进度条       |
| configobj   | pip install configobj       | 读取配置文件 |
| matplotlib  | pip  install matplotlib     | 绘图使用     |
| dateuti     | pip install python-dateutil | 绘图使用     |
| numpy       | pip  install numpy          | 绘图使用     |
|             |                             |              |

 

 

## 性能数据收集代码执行

  执行src目录下run_performance.py，即可进行性能数据的收集工作，在数据收集期间，请手工进行app端的功能测试，这样的数据采集才具有意义。

 

## Monkey稳定性测试

src目录下，执行run_monkey.py，可调用monkey命令进行稳定性测试，产生的日志信息记录在report目录下。

 

**说明：**

  可在进行monkey稳定性过程中，进行性能数据收集操作，这样采集的数据为monkey稳定性测试期间被测app的性能数据。

 

 

## 测试报告查看

测试报告在report目录下Performance_Results.html文件，部分截图如下：

<img class="shadow" src="/img/in-post/app_performance_html_view.png" width="1200">
