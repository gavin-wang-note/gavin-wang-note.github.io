---
layout:     post
title:      "自动关闭ssh会话"
subtitle:   "Auto close ssh session"
date:       2016-05-29
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - ssh
---

# 概述

有时候需要远程登录到客户现场环境，通过`xshell`之类的终端工具访问后台，由于客户现场有安全方面的严格要求，不得持续保留ssh会话，即：当问题摸清之后，需要退出远程，关闭ssh连接。但难免百密一疏导致遗漏，引发客户埋怨。如何来解决这个问题呢？


# 实践

以`xshell ssh`登录`linux`后台，在一定时间内没有任何操作，自动中断这个会话。

解决方法：

### step 1、vi /etc/profile

增加 `TMOUT=60`

这里表示60秒内无操作，自动终止`ssh session`。


### step 2、source /etc/profile


### step 3、echo $TMOUT

