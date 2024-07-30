---
layout:     post
title:      "ESXi常用命令"
subtitle:   "ESXi commands"
date:       2019-04-30
author:     "Gavin Wang"
catalog:    true
categories:
    - [ESXi]
tags:
    - 虚拟化
    - ESXi
---


### 概述

本文摘抄ESXi的一些基本命令范例， mark下来备用。




###  看你的esx版本

```shell
vmware -v                      #  看你的esx版本
VMware ESXi 5.0.0 build-469512
```

```shell
esxcfg-info -a                 #  显示所有ESX相关信息
esxcfg-info -w                 #  显示esx上硬件信息
service mgmt-vmware restart    #  重新启动vmware服务
esxcfg-vmknic -l               #  查看宿主机IP地址
 
esxcli hardware cpu list       #  cpu信息 Brand，Core Speed，
esxcli hardware cpu global get #  cpu信息 （CPU Cores）
esxcli hardware memory get     #  内存信息 内存 Physical Memory
esxcli hardware platform get   #  硬件型号，供应商等信息,主机型号,Product Name 供应商,Vendor Name
esxcli hardware clock get      #  当前时间
 
esxcli system version get                           # 查看ESXi主机版本号和build号
esxcli system maintenanceMode set --enable yes      # 将ESXi主机进入到维护模式
esxcli system maintenanceMode set --enable no       # 将ESXi主机退出维护模式
esxcli system settings advanced list -d             # 列出ESXi主机上被改动过的高级设定选项
esxcli system settings kernel list -d               # 列出ESXi主机上被变动过的kernel设定部分
esxcli system snmp get | hash | set | test          # 列出、测试和更改SNMP设定
 
esxcli vm process list                              # 利用esxcli列出ESXi服务器上VMs的World I(运行状态的)
esxcli vm process kill -t soft -w WorldI           # 利用esxcli命令杀掉VM
 
vim-cmd hostsvc/hostsummary          # 查看宿主机摘要信息
vim-cmd vmsvc/get.datastores         # 查看宿主存储空间信息
vim-cmd vmsvc/getallvms              # 列出所有虚拟机
 
vim-cmd vmsvc/power.getstate VMI    # 查看指定VMI虚拟状态
vim-cmd vmsvc/power.shutdown VMI    # 关闭虚拟机
vim-cmd vmsvc/power.off VMI         # 如果虚拟机没有关闭，使用poweroff命令
vim-cmd vmsvc/get.config VMI        # 查看虚拟机配置信息
 
esxcli software vib install -d /vmfs/volumes/datastore/patches/xxx.zip  # 为ESXi主机安装更新补丁和驱动
 
esxcli network nic list         # 列出当前ESXi主机上所有NICs的状态
esxcli network vm list          # 列出虚拟机的网路信息
esxcli storage nmp device list  # 理出当前NMP管理下的设备satp和psp信息
esxcli storage core device vaai status get # 列出注册到PS设备的VI状态
 
esxcli storage nmp satp set --default-psp VMW_PSP_RR --satp xxxx # 利用esxcli命令将缺省psp改成Round Robin
```

查看FC WWN號信息：

```shell
CLI ( SSH, vMA, vCLI)
esxcfg-mpath -b |grep WWNN | sed 's/.*fc //;s/Target.*$//'
```

