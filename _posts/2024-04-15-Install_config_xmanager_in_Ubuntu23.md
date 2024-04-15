---
layout:     post
title:      "Install&configure xmanager under ubuntu23"
subtitle:   "Install&configure xmanager under ubuntu23"
date:       2024-04-15
author:     "Gavin Wang"
catalog:    true
img:
summary: Install&configure xmanager under ubuntu23
categories:
    - [Linux]
    - [xmanager]
tags:
    - Linux
    - xmanager
---

# 概述

近期有使用到xmanager软件控制Ubuntu，简单记录一下如何在Ubuntu23 上安装&配置xmanager软件。

# 安装&配置过程

## 安装gdm

```shell
apt install gdm3 -y
```

## 配置lightdm

1.新建并编辑配置文件：vi /etc/lightdm/lightdm.conf

粘贴以下内容:

```shell
[SeatDefaults]
greeter-show-manual-login=true
xserver-allow-tcp=true

[XDMCPServer]
Enabled=true
Port=177
```


2.新建并编辑配置文件：nano /etc/lightdm/gdm.schemas

粘贴以下内容：

```shell
<schema>
<key>xdmcp/Enable</key>
<signature>b</signature>
<default>true</default>
</schema>
```


3.安装xubuntu-desktop

xubuntu-desktop用的就是xfce，一个轻量级的unix桌面管理环境，执行以下安装命令：

```shell
apt-get update
apt-get upgrade
apt install xfce4
apt install xubuntu-desktop -y
```


4.关闭防火墙

关闭防火墙：`ufw disable`
或者允许177端口：`ufw allow 177`

5.修改配置Ubuntu文件

修改配置文件：nano /usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf
内容修改后如下：

```shell
[Seat:*]
user-session=ubuntu

[XDMCPServer]
enabled=true

[SeatDefaults]
xserver-allow-tcp=true
```


6.重启XDMCP daemon

重启lightdm ： `service lightdm restart`
查看状态：`systemctl status lightdm.service`


**说明:**

如果没有root权限，有sudo权限，可在相关命令前增加sudo。


进行完上述动作后，在xmanager中新增一个XDMCP，如下图所示：

<img class="shadow" src="/img/in-post/config_xmanager.png" width="400">

然后就可以通过xmanager访问Ubuntu了，和本地访问效果一样。
