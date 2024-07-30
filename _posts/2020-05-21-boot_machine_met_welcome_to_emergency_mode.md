---
layout:     post
title:      "Linux开机启动，进入welcome to emergency mode"
subtitle:   "welcome to emergency mode after boot machine"
date:       2020-05-21
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---


# 概述

Ubuntu 18.04系统, 执行reboot -f后，网络不通，通过IPMI console查看，发现出现 ‘welcome to emergency mode!’，详细信息如下图所示：

```shell
welcome to emergency mode! after logging in, type "journalctl -xb" to view system logs，
"systemctl reboot" to reboot ，"systemctl default" to try again to boot into default mode.
give root password for maintenance(Control-D)
```

<img class="shadow" src="/img/in-post/welcome_to_emergency_mode.png" width="1200">


# 问题解决

按照提示操作：Control-D， systemctl reboot 命令后，依然如此。

考虑到当时产品有停用过ES(ElasticSearch)，由于存在bug，导致ES对应存储挂载点并没有被umount掉，更没有更新/etc/fstab，但是自己使用gdisk命令，重新格式化了这个分区，并dd擦写了上面的部分数据。可能是这个原因, 导致重启系统出现此界面。

想到这里，开始动手检查/etc/fstab内容，果然是有对应一条ES mount 记录：

<img class="shadow" src="/img/in-post/es_disk_mount_point.png" width="1200">

删除掉它，并重启机器。


# 小结

报这个错误多数情况下是因为/etc/fstab文件的错误。注意一下是不是加载了外部硬盘、存储器或者是网络共享空间，在重启时没有加载上导致的。

