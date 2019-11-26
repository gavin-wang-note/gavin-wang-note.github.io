---
layout:     post
title:      "消息网关组性能数据收集"
subtitle:   "GW performance date parse"
date:       2012-11-12
author:     "Gavin"
catalog:    true
tags:
    - performance
    - perl
---

# 概述

之前在网关测试组，每个迭代版本都需要进行性能测试，每次测试，除去环境部署外，最大的工作就是性能数据的收集以及分析、绘图了。

做成一个小工具，支持组内所有产品，根据配置文件的设定，自动进行数据的收集，通过excel宏，分析性能数据，并绘制成图在excle中展示。

# 代码

具体代码位置，在：

https://github.com/gavin-wang-note/gw_performance.git

已开源。

