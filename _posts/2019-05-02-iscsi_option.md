---
layout:     post
title:      "iSCSI 相关操作介绍"
subtitle:   "iSCSI Options"
date:       2019-05-02
author:     "Gavin"
catalog:    true
tags:
    - iSCSI
---


# 概述

本文主要介绍作为initiator端时，如何访问存储端IP_SAN device。

# 实践

## 查看存储scst的一些信息：

```/sys/kernel/scst_tgt/devices/tgtX_X```

## 挂载iscsi卷

```iscsiadm -m discovery -t st -p 10.16.17.191 -l ``` 或者

```iscsiadm -m node -l ```

或者指定target进行挂载：```iscsiadm -m node -T iqn.2016-01.11test:storage  -p 10.16.17.11 -l```


## 查找iSCSI targets主机的target name

```iscsiadm --mode discovery --type sendtargets --portal 192.168.0.9```

注：假设target主机ip为192.168.0.9

## login target

```iscsiadm --mode node --targetname iqn.renyuannetdisk --portal 192.168.0.9:3260 --login```

注：假设target name为iqn.renyuannetdisk，3260为iSCSI服务默认端口


## iSCSI target端设置

initiator客户端执行login命令后，在target服务器端可以发现新通道。把要分配给initiator客户端的卷通过该通道映射给initiator。

## 重启客户端iscsi initiator 服务

```/etc/init.d/open-iscsi restart```

## 查看iscsi targets映射过来的卷

```fdisk -l ```

或 用dmesg 或tail -f /var/log/messages 命令查看

## 创建分区

```fdisk /dev/sdb```

在提示行后输入m查看fdisk命令，输入n新建分区。

注：假设映射过来的卷设备名为sdb

## 格式化分区

```mkfs.ext3 /dev/sdb1```


## 挂载文件系统

```
mkdir /mnt/iscsi

mount /dev/sdb1 /mnt/iscsi
```

## 注销iSCSI initiator登录

不需要时可以注销iSCSI initiator登录，先umount文件系统，再把第四步命令的login参数改成logout执行即可：

```
umount /mnt/iscsi

iscsiadm --mode node --targetname iqn.renyuannetdisk --portal 192.168.0.9:3260 --logout
```


## 删除指定Target

用logout只是暂时登出，发现的target信息会保存在数据库中，下次重启iscsi服务时(service iscsi restart)，仍会找回该Target卷。如果想从数据库中删除该Target，需用以下命令：

查询数据库中Target内容：

```iscsiadm -m node```

## 删除指定的Target：

```iscsiadm -m node -o delete ```

or

```iscsiadm --mode node -o delete --targetname iqn.renyuannetdisk --portal 192.168.0.9:3260 ```

or

```iscsiadm -m node -o delete -T TARGET -p IP:port```


# Initiator name 格式说明：

https://www.ietf.org/rfc/rfc3721.txt 参考 : 1.1.  Constructing iSCSI names using the iqn. Format 



# 客户端发现iSCSI 调测

当客户端尝试登录iSCSI target时，发起discovery and login命令，如果命令执行结果出错，可以通过如下方式来调测：

```strace -f -s 1024 iscsiadm -m discovery -t iqn.2018-08.nose:target-acl2 -p 172.17.75.98```

那server端，是谁在负责处理客户端的连接请求呢？

iscsi-scstd 这个用户态进程负责处理

```
root@node248:~# ps -ef |grep iscsi-scstd | grep -v grep
root      293083       1  0 Sep22 ?        00:00:04 iscsi-scstd
root@node248:~# 

strace -f -p 293083
```

上面的这个指令，在客户端发起连接请求时候，会跟踪出详细连接信息


