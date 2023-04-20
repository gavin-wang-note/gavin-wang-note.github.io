---
layout:     post
title:      "如何查看端口是否被封"
subtitle:   "How to check if a port is blocked"
date:       2023-04-20
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

比如客户现场，PC端无法正常访问SAMBA Folder, 在网络通畅状况下依然无法访问，就需要检查是否防火墙封掉了SAMBA 相关端口。
本文概述如何判断某个端口是否被封。


# 实践

## 使用 telnet 命令进行连接测试

在命令行中输入命令 telnet IP地址 端口号，如果能够连接上，则表明该端口没有被封；如果无法连接，则表明该端口可能被封了。

例如：

```
telnet 192.168.1.100 80
```

如果能够连接上，则输出如下内容：

```
Trying 192.168.1.100...
Connected to 192.168.1.100.
Escape character is '^]'.
```


如果无法连接，则输出如下内容：

```
Trying 192.168.1.100...
telnet: Unable to connect to remote host: Connection refused
```

## 使用 nc 命令进行连接测试

在命令行中输入命令 nc -vz IP地址 端口号，如果能够连接上，则表明该端口没有被封；如果无法连接，则表明该端口可能被封了。

例如：

```
nc -vz 192.168.1.100 80
```

如果能够连接上，则输出如下内容：

```
Connection to 192.168.1.100 80 port [tcp/*] succeeded!
```


如果无法连接，则输出如下内容：

```
nc: connect to 192.168.1.100 port 80 (tcp) failed: Connection refused
```

## 使用网络工具进行检测：

可以使用网络工具（如 Wireshark、tcpdump 等）进行抓包检测
