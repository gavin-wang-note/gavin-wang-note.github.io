---
layout:     post
title:      "修改主机名"
subtitle:   "Modify hostname"
date:       2022-12-28
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

2022年就这么结束了，一年没什么输出，凑个数收个尾，简单mark下Ubuntu下如何更改主机名......


# 实作

## 方法1： 热改

```
 hostname new_host_name
```

简单粗暴有效，重启机器失效。



方法2： 永久修改


方案1: 热改+静态配置文件的修改

```
vim /etc/hosts
vim /etc/hostname
```

然后执行

```
 hostname new_host_name
```

经过上述步骤后，下次重启永久生效


方案2：hostnamectl 指令修改

```
hostnamectl set-hostname {name}
```

