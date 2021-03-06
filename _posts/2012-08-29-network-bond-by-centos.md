---
layout:     post
title:      "手动对CentoOS6 or CentoOS7做网卡绑定"
subtitle:   "Network bond for Centos"
date:       2012-08-29
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 前言

一直使用SUSE，今天切换了一个环境做测试，是Centos6.3，发现不会对Centos做bond了，mark一下操作记录, 本操作在Centos6 和 7 都适用.

# 操作步骤

## 1、ifconfig查看网卡信息

```
eth0      Link encap:Ethernet  HWaddr EC:38:8F:79:1B:F0  
          inet addr:172.18.112.11  Bcast:172.18.112.255  Mask:255.255.255.0
          inet6 addr: fe80::ee38:8fff:fe79:1bf0/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:2743 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1958 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:689409 (673.2 KiB)  TX bytes:318047 (310.5 KiB)
          Memory:94d00000-94e00000 

eth1      Link encap:Ethernet  HWaddr EC:38:8F:79:1B:F1  
          inet6 addr: fe80::ee38:8fff:fe79:1bf1/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:38 errors:0 dropped:0 overruns:0 frame:0
          TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:3564 (3.4 KiB)  TX bytes:468 (468.0 b)
          Memory:94c00000-94d00000
```

## 2、备份原网卡信息

进入 ```/etc/sysconfig/network-scripts```，创建backup目录，并将eth0和eth1网卡配置文件信息拷贝到新创建的backup目录下

```
mkdir backup
cp ifcfg-eth0 ifcfg-eth1 ./backup
```

## 3、绑定网卡

修改ifcfg-bond1内容

```/etc/sysconfig/network-scripts ```目录下，创建ifcfg-bond1文件，并添加如下内容：

```
DEVICE=bond1
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
IPADDR=172.18.112.11
NETMASK=255.255.255.0
GATEWAY=172.18.112.1
修改ifcfg-eth0和ifcfg-eth1内容
ifcfg-eth0内容
DEVICE=eth0
MASTER=bond1
SLAVE=yes
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
```

ifcfg-eth1内容

```
DEVICE=eth1
MASTER=bond1
SLAVE=yes
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
```

修改dist.conf文件,增加如下内容

```
vi /etc/modprobe.d/dist.conf
alias bond1 bonding
options bond1 miimon=100 mode=1
```

重启网卡服务

```
/etc/init.d/network restart
```


# 查看绑定的网卡信息

执行ifconfig命令


如果ifconfig查看，并没有发现有bond1网卡信息，可通过如下方法进行解决

```
service NetworkManager stop
service network restart
ifconfig查看bond信息
```

