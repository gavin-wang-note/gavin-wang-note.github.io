---
layout:     post
title:      "Delay the first auto start VM in PVE"
subtitle:   "How to delay the first auto start virtual machinevm guest system in proxmox ve pve"
date:       2021-12-13
author:     "Gavin Wang"
catalog:    true
categories:
    - [PVE]
tags:
    - PVE
    - proxmox ve
---


# 概述



一直以来，认为PVE提供的“延时启动”是针对宿主机完成启动后的XX设定的时间后VM自动启动，直到看到如下链接的内容中：
https://dannyda.com/2020/06/24/how-to-delay-the-first-auto-start-virtual-machinevm-guest-system-in-proxmox-ve-pve/

明确说明PVE VM boot delay并不是我们所想的：宿主机启动后XX秒再启动VM，而是：定义此VM启动与后续VM启动之间的间隔。说明第一台VM启动，依然存在失败问题（存储尚未ready，VM开始启动）。






# UI 设定的“延时启动”

UI展示VM开机自启动，这里的设置来自qm指令

```shell
root@node165:/etc/systemd/system/multi-user.target.wants# qm list
      VMID NAME                 STATUS     MEM(MB)    BOOTDISK(GB) PID       
       100 Scaler186            stopped    4096              32.00 0         
       101 scaler182            stopped    131072            64.00 0         
       103 Scaler103            running    131072            64.00 65598     
       106 Scaler106            running    131072            64.00 266948    
root@node165:/etc/systemd/system/multi-user.target.wants# qm set 106 -startup up=300
update VM 106: -startup up=300

root@node165:/etc/systemd/system/multi-user.target.wants#
```

做了上面的变更后，UI对应VM里的启动试验也跟着变（只是证明一下UI上的设定，来自指令qm set vmid -startup up=xx）。




# 如何正确设置VM的启动时延？



## 方法1：使用 --startall-onboot-delay 设置



指令参考如下：

```shell
pvenode config set --startall-onboot-delay XXX

--startall-onboot-delay <integer> (0 - 300) ( default = 0 ) Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.
```



这个参数的设定，上限是300秒，如果想调整成更大的数值，可以修改如下文件(示例设置为400秒):

```shell
root@node165:/etc/pve# grep -nri 400
nodes/node165/config:1:startall-onboot-delay: 400
```



## 方法2：修改 pve-guests.service pve-guests，增加sleep



```shell
cat /etc/systemd/system/multi-user.target.wants/pve-guests.service pve-guests
```



会看到如下部分的内容（有省略）：



```shell
[Service]
Environment="PVE_LOG_ID=pve-guests"
ExecStartPre=-/usr/share/pve-manager/helpers/pve-startall-delay
```




在如上内容中，增加如下内容（注意两个ExecStartPre的顺序）：

```shell
[Service]
Environment="PVE_LOG_ID=pve-guests"
ExecStartPre=/bin/sleep 400
ExecStartPre=-/usr/share/pve-manager/helpers/pve-startall-delay
```

