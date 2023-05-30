---
layout:     post
title:      "重置ESXi root密码"
subtitle:   "Reset root's password for ESXi"
date:       2019-04-29
author:     "Gavin"
catalog:    true
tags:
    - 虚拟化
    - ESXi
---


# Overview

其他人创建的环境，碰到ESXi root密码无人记得了，上面又有蛮多重要的VM，如何重置ESXi root密码，成为本文介绍的话题。


# 实践

## 使用单用户模式更改密码

* (1) 用Linux光盘启动，如：RHEL5，进入到系统的救援模式。

* (2) 在命令提示符界面下，运行mount /dev/sda5 /mnt/test  #这里的test目录是自己创建的，用于挂载用

* (3) sh-3.2# cp  /mnt/sda5/state.tgz /tmp/

* (4) 进入到/tmp 目录下，依次解压state.tgz local.tgz

```
sh-3.2# tar xvfz state.tgz
sh-3.2# tar xvfz local.tgz
```

* (5) 修改存放用户密码的配置文件，将root用户的密码清除掉（即通过MD5加密的长串字符）

```
sh-3.2# vi etc/shadow
```

* (6) 重要的步骤：

```
sh-3.2# rm -rf state.tgz local.tgz
sh-3.2# tar czvf local.tgz etc
sh-3.2# tar czvf state.tgz local.tgz
sh-3.2# cp statge.tgz /mnt/test
```

* (7) 重启ESXi主机即可
