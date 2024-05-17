---
title: Jmeter导入外部脚本报错
date: 2024-05-17 09:57:46
author: Gavin Wang
img: "/img/Jmeter/Jmeter.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: Jmeter导入外部脚本报错处理过程
categories:
    - [Jmeter]
    - [Automation]
tags:
    - Jmeter
    - Automation
---

# Overview

今天使用Jmeter 5.6.3版本导入外部脚本时报错。

爆粗内容文本信息如下：

```shell
Problem loading XML from:'D:\接口并发.jmx'. 
Cause:
CannotResolveClassException: kg.apc.jmeter.vizualizers.CorrectedResultCollector

 Detail:com.thoughtworks.xstream.converters.ConversionException: 
---- Debugging information ----
cause-exception     : com.thoughtworks.xstream.converters.ConversionException
cause-message       : 
first-jmeter-class  : org.apache.jmeter.save.converters.HashTreeConverter.unmarshal(HashTreeConverter.java:66)
class               : org.apache.jmeter.save.ScriptWrapper
required-type       : org.apache.jmeter.save.ScriptWrapper
converter-type      : org.apache.jmeter.save.ScriptWrapperConverter
path                : /jmeterTestPlan/hashTree/hashTree/hashTree[7]/hashTree[3]/kg.apc.jmeter.vizualizers.CorrectedResultCollector
line number         : 279
version             : 5.6.3
-------------------------------
```

图示如下：

<img class="shadow" src="/img/in-post/Jmeter/jmeter_import_error.png" width="800">


# 问题解决过程

## 问题原因

缺少jar包，但由于不知道具体缺少哪些/哪个，去官网下载Jmeter插件管理器，让管理器自动检测导入jmx文件时必要的jar包，然后点击install自动下载。

## 解决过程

### Jmeter插件管理器下载

访问`https://jmeter-plugins.org/install/Install/`进行jar包下载，如下图所示：

<img class="shadow" src="/img/in-post/Jmeter/download_jmeter_pligins-manager-jar.png" width="800">

### 存放下载的jar包

将插件jar包放入Jmeter安装路径下`\lib\ext`，如我的安装路径：`C:\apache-jmeter-5.6.3\lib\ext`


### 重载脚本

重新启动Jmeter，将脚本拖入，会提示install，并进行install动作。

<img class="shadow" src="/img/in-post/Jmeter/install_jmeter_lib.png" width="800">


Install结束后会自动重启Jmeter，并导入脚本。
