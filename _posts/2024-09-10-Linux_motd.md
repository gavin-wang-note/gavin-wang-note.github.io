---
title: Linux motd介绍
date: 2024-09-10
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: 每次登录Linux系统时，屏幕上会打印一些信息，这些信息就是Linux motd，本文介绍之
categories:
    - [Linux]
tags:
    - Linux
---

# Overview

**说明：**

  本文以`Ubuntu23`为例，介绍一下`motd`。

我们在使用终端工具透过`ssh`协议访问`Linux Server`时，通常会出现类似如下的资讯：

<img class="shadow" src="/img/in-post/Linux_motd.png" width="800">

那么这些信息是什么？又是如何产生的？

本文将介绍之。

# 什么是motd

`motd`（`Message of the Day`）是`Linux`系统中用于显示系统信息和消息的机制，它在用户登录时自动显示。

这些信息通常由系统命令生成，如`uptime, df, free, who`等。

* `uptime`：显示系统运行时间、用户数、系统负载等。
* `df`：显示磁盘空间使用情况。
* `free`：显示内存和交换空间的使用情况。
* `who`：显示当前登录用户。
等等。

`motd`系统可以配置为动态生成这些信息。在`Ubuntu`系统中，`motd`的内容通常由多个脚本生成，这些脚本位于`/etc/update-motd.d/`目录下。每个脚本负责生成一部分信息，如下所示：

```shell
root@Gavin:/etc/update-motd.d# ll
total 68
drwxr-xr-x   2 root root  4096 Jul 16 09:12 ./
drwxr-xr-x 157 root root 12288 Jul 16 09:12 ../
-rwxr-xr-x   1 root root  1220 Apr 22  2022 00-header*
-rwxr-xr-x   1 root root  1151 Jan  2  2024 10-help-text*
lrwxrwxrwx   1 root root    46 Jun  7 09:16 50-landscape-sysinfo -> /usr/share/landscape/landscape-sysinfo.wrapper*
-rwxr-xr-x   1 root root  5023 Apr 22  2022 50-motd-news*
-rwxr-xr-x   1 root root    84 Oct 11  2023 85-fwupd*
-rwxr-xr-x   1 root root   218 Oct 11  2023 90-updates-available*
-rwxr-xr-x   1 root root   296 Apr 23 21:36 91-contract-ua-esm-status*
-rwxr-xr-x   1 root root   558 Oct  4  2023 91-release-upgrade*
-rwxr-xr-x   1 root root   165 Jan  8  2023 92-unattended-upgrades*
-rwxr-xr-x   1 root root   379 Oct 11  2023 95-hwe-eol*
-rwxr-xr-x   1 root root   111 Oct 11  2023 97-overlayroot*
-rwxr-xr-x   1 root root   142 Oct 11  2023 98-fsck-at-reboot*
-rwxr-xr-x   1 root root   144 Oct 11  2023 98-reboot-required*
root@Gavin:/etc/update-motd.d#
```

# 过程

接下来介绍一下`Ubuntu23`的`motd`，在登录的时候，它执行了哪些脚本？

按照上面图的显示顺序，执行过程参考如下：

```shell
root@Gavin:/etc/update-motd.d# ./00-header 
Welcome to Ubuntu 23.10 (GNU/Linux 6.5.0-44-generic x86_64)
root@Gavin:/etc/update-motd.d# ./10-help-text 

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro
root@Gavin:/etc/update-motd.d# ./50-landscape-sysinfo 

 System information as of Tue Sep 10 10:53:20 AM CST 2024

  System load:  0.06               Processes:              307
  Usage of /:   89.8% of 30.34GB   Users logged in:        1
  Memory usage: 17%                IPv4 address for ens33: 192.168.23.129
  Swap usage:   0%

  => / is using 89.8% of 30.34GB
root@Gavin:/etc/update-motd.d# ./50-motd-news 

 * Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s
   just raised the bar for easy, resilient and secure K8s cluster deployment.

   https://ubuntu.com/engage/secure-kubernetes-at-the-edge
root@Gavin:/etc/update-motd.d# ./90-updates-available 

1 update can be applied immediately.
To see these additional updates run: apt list --upgradable

root@Gavin:/etc/update-motd.d# 
```

# 客制化motd

看到这里，是不是可以定制化自己的`motd`呢？

答案是肯定的，如何订制？

我们来小试一下，增加一下打印当前时间。

```shell
root@Gavin:/etc# vim /etc/update-motd.d/99-custom
root@Gavin:/etc# chmod a+x /etc/update-motd.d/99-custom
root@Gavin:/etc# 
```

`/etc/update-motd.d/99-custom`文件内容参考如下：

```shell
#!/bin/sh
echo "Current Date and Time: $(date)"
```

下次再登录，展示效果参考如下：

```shell
Xshell 7 (Build 0065)
Copyright (c) 2020 NetSarang Computer, Inc. All rights reserved.

Type `help' to learn how to use Xshell prompt.
[C:\~]$ 

Connecting to 192.168.23.129:22...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.

Welcome to Ubuntu 23.10 (GNU/Linux 6.5.0-44-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Tue Sep 10 11:27:31 AM CST 2024

  System load:  0.05               Processes:              317
  Usage of /:   89.8% of 30.34GB   Users logged in:        1
  Memory usage: 18%                IPv4 address for ens33: 192.168.23.129
  Swap usage:   0%

  => / is using 89.8% of 30.34GB

 * Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s
   just raised the bar for easy, resilient and secure K8s cluster deployment.

   https://ubuntu.com/engage/secure-kubernetes-at-the-edge

1 update can be applied immediately.
To see these additional updates run: apt list --upgradable


Current Date and Time: Tue Sep 10 11:27:31 CST 2024
Last login: Tue Sep 10 11:25:48 2024 from 192.168.23.1
cd ~
root@Gavin:~# cd ~
root@Gavin:~# 
```

当然，你也可以在现有文件中增加一些内容，丰富打印信息，比如`00-header`文件中，增加当前主机名，参考如下：

添加如下内容：

```shell
# printf "Welcome to %s (%s %s %s)\n" "$DISTRIB_DESCRIPTION" "$(uname -o)" "$(uname -r)" "$(uname -m)"

HOSTNAME=$(hostname)
printf "Welcome to %s's %s (%s %s %s)\n" "$HOSTNAME" "$DISTRIB_DESCRIPTION" "$(uname -o)" "$(uname -r)" "$(uname -m)"
```

打印效果：

```shell
Welcome to Gavin's Ubuntu 23.10 (GNU/Linux 6.5.0-44-generic x86_64)
```


# 禁用motd

如何禁用`motd`？

方法多种多样！

## 方案1： 禁用动态 Motd

```shell
root@Gavin:/etc# systemctl -l | grep motd
  motd-news.timer                                                                                  loaded active     waiting   Message of the Day
  update-notifier-motd.timer                                                                       loaded active     waiting   Check to see whether there is a new version of Ubuntu available
root@Gavin:/etc#
```


如果你的系统使用 `dynamic motd`（动态 `motd`），你可能需要禁用相关的服务。这通常涉及到 `motd-news、motd-news-scripts` 或类似的包。

禁用动态 Motd 服务：

```shell
systemctl disable motd-news.service
```

然后停止服务：

```shell
systemctl stop motd-news.service
```

如果你不确定是否安装了这些服务，可以使用以下命令检查：

```shell
dpkg -l | grep motd
```

如果这些服务存在，你可以选择卸载它们：

```shell
apt-get remove motd-news motd-news-scripts
```

## 方案2：禁用 /etc/update-motd.d/ 脚本

这个方法简单粗暴，直接移除或删除`/etc/update-motd.d/`目录下文件，比如：

```shell
mv /etc/update-motd.d/* /tmp/
```

## 禁用 Plymouth 启动界面

`Plymouth` 是显示启动画面和 `motd` 的程序。你可以通过编辑 `grub` 配置来禁用它。

打开终端，然后输入以下命令来编辑 `grub` 配置文件：

```shell
vim /etc/default/grub
```

找到包含 `GRUB_CMDLINE_LINUX_DEFAULT` 的行，确保没有 `splash` 这个选项。这行可能看起来像这样：

```shell
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
```

确保没有 `splash` 或 `plymouth.ignore-serial-consoles` 这样的参数。如果存在，删除它们，然后保存文件。

更新 `grub` 配置：

```shell
update-grub
```

重启系统以应用更改。

**请注意**

这些步骤可能会因 `Ubuntu` 的不同版本而略有不同。如果你的系统是最新版本，或者你使用的是特定的发行版，可能需要进行相应的调整。在进行任何更改之前，建议备份相关文件和配置。


