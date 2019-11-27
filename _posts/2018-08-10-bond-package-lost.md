---
layout:     post
title:      "网卡丢包解决案例"
subtitle:   "Bond lost package"
date:       2018-08-10
author:     "Gavin"
catalog:    true
tags:
    - network
---

# 概述

在lab进行性能测试，网络是配置的bond， active+standby模式，发现流量越大，网卡丢包越多

# 解决方法

经过摸索，最终通过如下方式进行解决：

修改对一个网口的RX size，从512 调整为2048

<img class="shadow" src="/img/in-post/package_lost.png" width="600">


