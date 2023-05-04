---
layout:     post
title:      "评测USB接口速度"
subtitle:   "How to get USB speed"
date:       2023-04-28
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述


今天同事咨询硬件USB版本是多少，查询了下资料，发现lsusb这个指令可以捞到，mark it.


# 信息

如果没有安装，执行

```apt-get install usbutils ```
or 

```yum install usbutils ```


output:

```
[root@bigtera etc]# hostnamectl 
   Static hostname: bigtera
         Icon name: computer-server
           Chassis: server
        Machine ID: b3315f4c3ab849a7ae5ffc905a73e45a
           Boot ID: 39bbd8a659fa4465bb4189bc6e4af69a
  Operating System: Kylin Linux Advanced Server V10 (Sword)
            Kernel: Linux 4.19.90-24.4.v2101.ky10.aarch64
      Architecture: arm64
[root@bigtera etc]# lsusb -t
/:  Bus 08.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/1p, 5000M
/:  Bus 07.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/1p, 480M
/:  Bus 06.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/1p, 5000M
    |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/4p, 5000M
/:  Bus 05.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/1p, 480M
    |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/4p, 480M
/:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=ohci-pci/2p, 12M
/:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=ohci-pci/2p, 12M
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
    |__ Port 1: Dev 2, If 0, Class=Human Interface Device, Driver=usbhid, 480M
    |__ Port 1: Dev 2, If 1, Class=Human Interface Device, Driver=usbhid, 480M
[root@bigtera etc]#
```

说明:

* 12M --> USB V1.0
* 480M --> USB V2.0
* 5000M --> USB V3.0
