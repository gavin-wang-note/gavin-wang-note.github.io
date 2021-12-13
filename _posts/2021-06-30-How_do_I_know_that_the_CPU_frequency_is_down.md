---
layout:     post
title:      "如何知道CPU降频了呢"
subtitle:   "How do I know that the CPU frequency is down"
date:       2021-06-30
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

最近碰到过几次服务器出现CPU降频的问题，其中两次是硬件BIOS固件的bug，不小心踩到了（概率很低，但有幸被我碰到，巨坑），后来从硬件厂商那获取到了高阶版本，刷了高阶版本的固件解决掉了；

还有一次是设备两路电源线被同事拔掉了一根，只剩下一路了，供电不足，导致CPU主动降频；

今天RD在tuning performance时，再次碰到了CPU降频问题，问题是tuning performance过程中ganesha 跑到 1000 多 %，很凶，造成服务器机体温度升高，整个Lab平均温度达到31度，增加空调紧急降温后恢复正常。


由于碰到过多次，本文汇总下如何判断CPU发生了降频，避免忘记（其实今天没看出来哪里降频了，所以才写了此文XD）。


# 查看CPU降频的方法

## lscpu

<img class="shadow" src="/img/in-post/lscpu.png" width="1200">


如上图所示：

```
CPU MHz:               2579.700
CPU max MHz:           3000.0000
CPU min MHz:           800.0000
```

这里有CPU当前HZ（CPU MHz）信息和min MHz（CPU min MHz），如果CPU MHz的值是小于CPU min MHz的值，说明CPU被降频了。


## atop中查看cruf


借助atop命令（公司产品有安装），查看CPU的curf（ARM平台，华为鲲鹏服务器，这里的值为'？'，不知道为什么【需要打流量？？】，X86是OK的）

<img class="shadow" src="/img/in-post/atop_cruf.png" width="1200">


如果curf（current frequency）只有几十MHz(正常情况下是XGHz)，CPU铁定是被降频了，此时观察atop中众多process，几乎清一色的只消耗1%的process


# 总结

CPU降频的原因，目前碰到的：

（1）硬件设备温度过高

（2）BIOS固件的bug

（3）供电不足

