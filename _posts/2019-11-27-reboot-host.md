---
layout:     post
title:      "魔法键重启Linux机器"
subtitle:   "reboot Linux machine by magic key"
date:       2019-11-27
author:     "Gavin Wang"
catalog:    true
cover:      true
categories:
    - [Linux]
tags:
    - Linux
---

# 前言

本文介绍魔法键重启Linux机器， very magical.

# 概述

重启Linux机器，无非通过下列几种常见命令：

```reboot ```

```reboot -f ```

```poweroff ```

说明：

如果上面的指令，在机器重启、关机期间卡住了，怎么办？看下面ipmi指令。


# IPMI指令

说明：

需要安装ipmitool工具, 这个也不是本文重点哦。


## 硬关机，直接切断电源

```ipmitool -I lan -H 192.168.1.2 -U IPMI的管理员账号 -P 密码 power off ```

## 软关机

即如同轻按一下开机扭，对于linux，服务器将halt，power status 为off

```ipmitool -I lan -H 192.168.1.2 -U IPMI的管理员账号 -P 密码 power soft ```

## 硬开机

```ipmitool -I lan -H 192.168.1.2 -U IPMI的管理员账号 -P 密码 power on ```

## 硬重启

```ipmitool -I lan -H 192.168.1.2 -U IPMI的管理员账号 -P 密码 power reset ```


# 魔法键

重点来了~~~

上面的指令大家都知道，本文要讲的，是一个Magic key，可以做到强制重启哦，非常的神奇，一切卡死都不是事~~

命令如下：

```echo "b" > /proc/sysrq-trigger ```

