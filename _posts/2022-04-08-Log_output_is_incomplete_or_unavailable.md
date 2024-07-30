---
layout:     post
title:      "解决 Log output is incomplete or unavailable 问题"
subtitle:   "Log output is incomplete or unavailable"
date:       2022-04-08
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---


# 概述

今天碰到客户反馈通过systemctl status 查看某daemon状态时，显示如下图所示：

<img class="shadow" src="/img/in-post/daemon_journal_log_warn.jpg" width="1200">

客户询问，这个warn是否有影响？

#  根因

客户现场的这个daemon已经长久运行有些年头了，journal会统计log大小，到了某种程度就自动删掉。

# 解决方法

放大journal，比如：

`journalctl --vacuum-size=1G`

示例的意思是：最大可存放1GB journal。

