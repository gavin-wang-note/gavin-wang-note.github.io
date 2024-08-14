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


# /proc/sysrq-trigger介绍

`/proc/sysrq-trigger` 是 Linux 系统中的一个特殊文件，它允许用户通过向其中写入特定的字符来触发紧急系统请求（也称为 "SysRq" 功能）。这个特性通常用于系统管理员在系统崩溃或无法正常响应时进行紧急操作。以下是对 `/proc/sysrq-trigger` 的一些详细解释：

## 功能

- **紧急重启**：当系统无法通过常规方法重启时，可以使用 `SysRq` 功能来安全地重启系统。

## 使用方法

要使用 `/proc/sysrq-trigger`，你需要向该文件写入特定的字符。这通常通过 `echo` 命令完成。例如，要触发紧急重启，可以执行以下命令：

```shell
echo "b" > /proc/sysrq-trigger
```

## 支持的字符

以下是一些常用的 `SysRq` 功能字符及其作用：

- `b`：立即重启系统，不进行同步或卸载文件系统。
- `c`：终止所有进程，然后执行紧急重启。
- `d`：立即同步所有文件系统，然后打印内核调试信息。
- `e`：发送 `SIGTERM` 信号给所有进程，除了 `init` 进程。
- `g`：打印当前的工作队列。
- `h`：打印帮助信息，列出所有可用的 `SysRq` 功能。
- `i`：使所有网络接口进入混杂模式。
- `j`：将当前的内存信息打印到控制台。
- `k`：立即重启内核（需要内核配置支持）。
- `l`：日志消息级别切换。
- `m`：打印内存信息。
- `n`：清除所有网络接口的网络套接字队列。
- `o`：关闭所有网络接口。
- `p`：打印当前进程列表。
- `q`：发送 `SIGKILL` 信号给所有进程，除了 `init` 进程。
- `r`：重新启动所有网络接口。
- `s`：同步所有文件系统。
- `t`：打印当前的任务列表和状态。
- `u`：重新挂载所有文件系统为只读模式。
- `v`：打印进程的虚拟内存信息。
- `w`：打印当前的未完成的任务列表。
- `x`：关闭所有网络接口的网络套接字队列。

## 注意事项

- 使用 `SysRq` 功能时，需要具有 `root` 权限或相应的 `sudo` 权限。
- 某些 `SysRq` 功能可能需要特定的内核配置才能使用。
- `SysRq` 功能主要用于紧急情况，可能会影响系统的稳定性和数据的完整性。因此，除非绝对必要，否则应谨慎使用。

`SysRq` 功能是 `Linux` 系统中一个强大的工具，可以帮助系统管理员在系统出现问题时快速采取行动。然而，由于其强大的能力，使用时应确保了解其潜在的影响。
