---
layout:     post
title:      "CentOS下安装wareshark"
subtitle:   "Install wireshark in CentOS"
date:       2023-01-09
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - wireshark
---


# Overview

How to install wireshare in CentOS? This document briefly describes it.


# Installation on CentOS


```
yum install gcc gcc-c++ bison flex libpcap-devel qt-devel gtk3-devel rpm-build libtool c-ares-devel qt5-qtbase-devel qt5-qtmultimedia-devel qt5-linguist desktop-file-utils
yum install wireshark wireshark-qt
yum install wireshark-gnome
```

启动:在Application/internet下。

启动后提示：

```
Couldn't run /usr/sbin/dumpcap in child process: Permission denied

Are you member of 'wireshark' group? Try running 'usermod -a -G wireshark <username>' as root.

```


同时，也沒有interface列出來。

按照提示增加普通使用者到组以后，还是提示许可证问题。

于是，將/usr/sbin/dumpcap的组改为普用使用者的组，再执行，沒有那个提示了，但是还是沒有interface列出來。


workaround

```
[root@pool-100-0-1-54 windipv6]# sudo usermod -a -G wireshark windipv6

setcap cap_net_raw,cap_net_admin+eip /usr/sbin/dumpcap

```

Reference Link:

```https://linuxtechlab.com/install-wireshark-linux-centosubuntu/```
