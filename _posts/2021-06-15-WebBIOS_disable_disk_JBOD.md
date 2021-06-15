---
layout:     post
title:      "WebBIOS里取消磁盘的JBOD设置"
subtitle:   "Disable JBOD for disks in WebBIOS"
date:       2021-06-15
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

环境之前有使用过storcli或megacli命令开启了JBOD模式，安装系统后始终无法进入系统，grub 引导出问题，BIOS的设置检查了几次，并未发现异常，boot device也是对的，始终无法解决重灌系统后开机问题。
决定更换OS盘（换成其他的SAS盘），在更换后，碰到了本文要描述的问题：存在部分是RAID部分是JBOD盘，计划OS盘做RAID0,但WebBIOS里查看到此盘无法最RAID。


本文记录如何在WebBIOS取消JBOD模式，仅附图片mark下，避免忘记。

# 处理过程

## 最初盘的状况

<img class="shadow" src="/img/in-post/disk_mix_mode.png" width="1200">


## 取消JBOD

开机启动进入WebBIOS，Controller Properties --> ALter+N + 回车，连续三次，进入'Manage JBOD' 界面，选择对应的JBOD driver，点击'OK'完成取消JBOD mode的设置， 可以按住shift与向下的箭头按钮，多选磁盘的

<img class="shadow" src="/img/in-post/disable_disks_jbod_mode.png" width="1200">

