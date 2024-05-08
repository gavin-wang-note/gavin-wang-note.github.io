---
title: 解决CentOS下cron job 执行pnpm命令报 node 不存在问题
date: 2024-06-17 16:59:18
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 解决CentOS下cron job 执行pnpm命令报 node No such file or directory
categories:
    - [Linux]
tags:
    - Linux
---

# Overview

CentOS 环境下，安装了nodejs和pnpm，但是执行pnpm命令时，提示：

```shell
/usr/bin/env: node: No such file or directory
```

安装过程参考如下：

<img class="shadow" src="/img/in-post/CentOS下安装pnpm.png" width="800">

之后就碰到了上面出现的问题。



# 解决方法

## 1. 将node安装路径下入PATH

将下面内容，写入到~/.bash_profile文件中

```shell
PATH=$PATH::/node-v18/bin/pnpm

export PATH
```

然后执行`source ~/.bash_profile`

## 2. link node

`ln -s /node-v18/bin/node /usr/bin/node`
