---
layout: post
title: "python3 升级pip后找不到pip模块"
subtitle: "No module named 'pip' after upgrade pip"
date: 2023-11-09
author: "Gavin Wang"
catalog: true
summary: 解决"python3 升级pip后找不到pip模块"问题 
categories:
    - [python]
tags:
    - python
---


# 概述



原本未打算写这个文档的，之前碰到过，但是今天运维同事碰到了此问题，想起以前也碰到过，记录一下。

就目前碰到状况而言，此问题只在python3中发生过，并未在python2中遇见。

言归正传，此次使用的python3环境，提示要升级pip版本，按照要求进行了版本的升级，升级失败，再次尝试安装，提示pip缺失，如下图所示：



<img class="shadow" src="/img/in-post/pip_module_error.png" width="1200">


上图提示python “No module named pip”，升级后导致不能使用pip命令。



# 原因


可能是新旧版本冲突或路径空格导致，尚未找到root cause。



# 解决方法


{% note success %}
## 方案1
{% endnote %}


适用于windows/Mac/Linux系统

```shell
python -m ensurepip
```

如下图所示(Windows下结果)：



<img class="shadow" src="/img/in-post/pip_reinstall.png" width="1200">


{% note success %}
## 方案2
{% endnote %}

输入如下命令：          

```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --force-reinstall
```



{% note success %}
## 方案3
{% endnote %}


```shell
apt install --fix-missing python3-pip
```



# 验证安装

```shell
pip show pip
```
