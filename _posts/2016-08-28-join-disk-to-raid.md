---
layout:     post
title:      "磁盘加入RAID组"
subtitle:   "HDD join RAID5"
date:       2016-08-28
author:     "Gavin Wang"
catalog:    true
categories:
    - [RAID]
tags:
    - RAID
---


# 背景

测试场景中含有容灾测试，其中涉及到拔盘测试，本文以该场景为例，指导如何恢复RAID组到正常状态。

# 新盘加入

从RAID组中拔掉一块硬盘，重新插入一块新盘，无需执行任何megacli命令，新盘会自动加入RAID组，并处于rebuild状态，直至rebuild完成后，RAID组恢复正常。


# 旧盘加入

从RAID组中拔掉一块硬盘，再重新插入这块被拔下来的磁盘，RAID组的校验机制检测到这块盘曾经是RAID组成员，之前叛变了，现在又先回归组织，需要进行身份验证，所以这块旧盘会被标记成unconfig（good）状态，需要做两个动作，来完成再加入RAID，分别是：

1、标记硬盘状态为config(good)

2、导入到RAID组

## 具体操作步骤如下：

（1）获取被加入RAID组磁盘的Enclosure Device ID 和Slot Number

```/opt/MegaRAID/MegaCli/MegaCli64 -LdPdInfo -aALL```

<img class="shadow" src="/img/in-post/hdd_join_raid.png" width="800">

（2）标记磁盘为unconfig（good）状态

如上图所示，坏了的磁盘，状态应该是unconfig（good），这里截图仅供参考。

假如Enclosure Device ID 为8，Slot Number为2的磁盘坏了的话，执行如下命令：

```/opt/MegaRAID/MegaCli/MegaCli64 -PDMakeGood -PhysDrv[8:2] -a0```

将磁盘设置为good状态。

（3）导入RAID组

执行

```/opt/MegaRAID/MegaCli/MegaCli64 -CfgForeign -import -a0```

命令，将步骤2中标记的盘导入raid组。

## 查看RAID组rebuild进度

```/opt/MegaRAID/MegaCli/MegaCli64 -pdrbld -showprog -physdrv[8:2] -aALL```

