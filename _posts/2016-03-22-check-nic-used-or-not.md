---
layout:     post
title:      "查看网卡对应网口是否已使用"
subtitle:   "Check NIC port user or not"
date:       2016-03-22
author:     "Gavin"
catalog:    true
tags:
    - network
---


# 应用场景

在安装完操作系统进行网卡配置IP地址时，往往不知道操作系统哪几个网卡口插了网线，在不去查看具体设备情况下，可通过本文确认哪个网卡口上插了网线。


如下图所示，存在4个网卡，在配置IP地址时，需要事先确认要去配置哪个网卡。
 
<img class="shadow" src="/img/in-post/net_info.png" width="600">


# 查看过程

## 查看所有网卡信息

```
root@host181:~# ifconfig -a
eth0      Link encap:Ethernet  HWaddr 0c:c4:7a:47:44:a4  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
          Interrupt:16 Memory:df600000-df620000 

eth1      Link encap:Ethernet  HWaddr 00:e0:ed:43:8c:4e  
          inet addr:10.16.17.181  Bcast:10.16.17.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:464590 errors:651 dropped:689 overruns:0 frame:651
          TX packets:68621 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:44648440 (44.6 MB)  TX bytes:47221831 (47.2 MB)

eth2      Link encap:Ethernet  HWaddr 0c:c4:7a:47:44:a5  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
          Interrupt:17 Memory:df500000-df520000 

eth3      Link encap:Ethernet  HWaddr 00:e0:ed:43:8c:4f  
          inet addr:10.10.10.181  Bcast:10.10.10.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:63671255 errors:651 dropped:4061 overruns:0 frame:651
          TX packets:79242899 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:49119827886 (49.1 GB)  TX bytes:47106704400 (47.1 GB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:30775317 errors:0 dropped:0 overruns:0 frame:0
          TX packets:30775317 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:17379972836 (17.3 GB)  TX bytes:17379972836 (17.3 GB)
```

## 查看各个网卡的Link detected信息

```
root@host181:~# ethtool eth0 | grep 'Link detected'
	Link detected: no
root@host181:~# ethtool eth1 | grep 'Link detected'
	Link detected: yes
root@host181:~# ethtool eth2 | grep 'Link detected'
	Link detected: no
root@host181:~# ethtool eth3 | grep 'Link detected'
	Link detected: yes
root@host181:~#
```

如上所示，Link detected值为yes的，表示该网卡有连接线，被启用，据此可以去进行eth0和eth3网卡的IP配置。


