---
layout:     post
title:      "彩信网关数据库自动升级与比对（QCC）"
subtitle:   "MMSG Gateway auto upgrade and commpare"
date:       2013-07-05
author:     "Gavin"
catalog:    true
tags:
    - Automation
---

# 概述

原始文件是个ppt，大约是在2013年在网关测试组测试时，写了一个QCC，获奖了哦~~

现在把PPT截图放出来，做了关键信息的屏蔽处理，望见谅~


# MMSG QCC auto upgrade 评审胶片

<img class="shadow" src="/img/in-post/qcc_1.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_2.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_3.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_4.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_5.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_6.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_7.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_8.png" width="1200">

说明：

测试环境准备：包括但不限制于：测试环境准备、产品部署、数据导入等操作

<img class="shadow" src="/img/in-post/qcc_9.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_10.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_11.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_12.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_13.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_14.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_15.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_16.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_17.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_18.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_19.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_20.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_21.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_22.png" width="1200">

说明：

* cfg：存放产品的配置文件信息，方便产品安装与部署
* cls_db.pl：用于清理数据库中对象，包括表、视图、存储过程、package等对象
* compare.pl：用于数据的比对，并将结果保存到文件
* config：存放配置文件信息
* data：存放现网数据，即dmp文件
* exp_date.pl：导出数据
* exp_parameter.pl：导出参数数据
* imp_data.pl：导入现网数据
* main.pl：调用其他的所有的pl脚本
* m_manager：存放XXC的相关升级脚本
* mmsg：存放XXA的相关升级脚本
* package：存放安装包，无需解压的gz或Z包
* sms：存放XXB的相关升级脚本
* syslib：Perl模块，解决AIX平台未安装Config模块无法从配置文件获取信息问题


<img class="shadow" src="/img/in-post/qcc_23.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_24.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_25.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_26.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_27.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_28.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_29.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_30.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_31.png" width="1200">

<img class="shadow" src="/img/in-post/qcc_32.png" width="1200">

