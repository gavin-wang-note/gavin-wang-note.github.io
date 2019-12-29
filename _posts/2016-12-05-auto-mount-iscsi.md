---
layout:     post
title:      "iSCSI自动挂载"
subtitle:   "auto mount iSCSI"
date:       2016-06-12
author:     "Gavin"
catalog:    true
tags:
    - iSCSI
---


# 概要

本篇介绍了iscsiadm常见命令和iSCSI自动挂载的方法。

iscsiadm工具用于Linux连接以太网上的iSCSI设备，我们的系统中内置本工具，如果是其他OS，可能需要先安装相应包。


# 安装

Ubuntu

```
apt-get install open-iscsi
apt-get install open-iscsi-utils
```

CentOS

```
yum install iscsi-initiator-utils
```

安装完成后应该会自动启动，如果没有使用service iscsi start


# 使用

常见步骤如下：

```iscsiadm -m discovery -t sendtargets -p {ip_address:port} ```
* 发现给定IP的target，port可不加，默认是3260，sendtargets可简写为st

```iscsiadm -m node -T { target-name } -p { ip_address:port } -l ```
* 挂载iSCSI 设备

```iscsiadm -m node -T { target-name } -p { ip_address:port } -u ```
* 卸载iSCSI 设备

其他常见命令：

* 查看iSCSI状态
```
iscsiadm -m session # 查看当前登录的session，可以带参数-P 3查看到详细信息，包括target和sdX的对应关系！
iscsiadm -m node # 查看当前已经discovery到的target
```

* 删除iSCSI设备

```iscsiadm -m node -o delete -T { target-name } -p { ip_address:port } ```

* * 可以灵活选用-p和-T，比如iscsiadm -m node -T iqn.2016-12.bigtera.com:test -l表示挂载当前discovery到的名字是iqn.2016-12.bigtera.com:test的target，所有的IP都会被挂载到；同理，如果是iscsiadm -m node -p 192.168.1.1 -u，表示卸载192.168.1.1上的所有target；如果既没有-p，也没有-T，表示挂载/卸载所有session。


# 开机自动挂载

## Step1. 修改 "/etc/iscsi/iscsid.conf"

把 node.startup 改成 automatic。(如果已经discovery了的话需要先删除target，如上述命令"删除iSCSI设备")

## Step2. 重新发现

```iscsiadm -m discovery -t sendtargets -p ip ```

## Step3. 配置文件检查

检查类似如下config中的startup是否是automatic，对于不同的release版本位置有所不同，举例：

### For Ubuntu:

```/etc/iscsi/nodes/iqnname/192.168.0.1:servername.iscsiTargetName/default ```

### For Centos:

```/var/lib/iscsi/nodes/iqn.2001-06.com.test\:storage/192.168.0.14\,3260\,1/default ```

可以针对不同的session设置不同的startup策略(manual/automatic)。
