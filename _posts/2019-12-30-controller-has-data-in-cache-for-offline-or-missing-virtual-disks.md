---
layout:     post
title:      "解决因RAID卡提示VD有cache而无法创建RAID问题"
subtitle:   "Resolve controller has data in cache for offline or missing virtual disks"
date:       2019-12-30
author:     "Gavin Wang"
catalog:    true
categories:
    - [Megacli]
    - [RAID]
tags:
    - RAID
    - Megacli 
---

# 前言

单盘组的RAID0做的OSD，设备上直接把这块盘拔掉，然后重新插回去，本想看看重做RAID0后，UI rescan or reformat OSD是否OK的，结果在重做RAID0期间碰到了本文的问题，记录一下。

# 现象

单盘RAID0被拔掉后，这块SATA盘的“Firmware State” 是 “Unconfigured(bad), Spun Up”，于是尝试make good it:

```shell
root@node247:~# /opt/MegaRAID/MegaCli/MegaCli64 -PDMakeGood -PhysDrv[0:5] -a0
                                     
Adapter: 0: EnclId-0 SlotId-5 state changed to Unconfigured-Good.

Exit Code: 0x00
```

尝试对它重建建RAID0，结果失败，RAID卡event log显示：

导出的RAID卡的event log：

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpEventLog -GetEvents -f event.log -A0 ```

```shell
seqNum: 0x000153dc
Time: Mon Dec 30 10:12:20 2019

Code: 0x000000da
Class: 0
Locale: 0x40
Event Description: Foreign Configuration Detected
Event Data:
===========
None
```


直接Display event log：

```/opt/MegaRAID/MegaCli/MegaCli64 -FwTermLog -Dsply -aALL ```

```shell
12/30/19 10:13:10: C0:EVT#87008-12/30/19 10:13:10: 218=Foreign Configuration Detected
12/30/19 10:13:11: C0:pii addBvdInfo rsvd2=1 <- bvd ld=0
12/30/19 10:13:11: C0:createMegaraidCfg: cfg:4422ac20 forCfg=441cd7e0 merge:0 import:0 other_pinned_vds:c02e1240 
12/30/19 10:13:11: C0:**** PinnedCacheDataStructures->pinned_cache_present
12/30/19 10:13:11: C0:0x00000002
12/30/19 10:13:11: C0:sscPinnedWindowInfo.ssd_window_pinned 0 
12/30/19 10:13:11: C0:createMegaraidCfg - V ld 0  targetId 1  LdMapTargetIdToLd fe totLd:1 
12/30/19 10:13:11: C0:createMegaraidCfg - VI number_pinned_vds_found_during_import 1 targetId 1 
12/30/19 10:13:11: C0:createMegaraidCfg - pii createMR1 rsvd2=1 <- forcfg ld=0 import:0 OldTargetId:1 merge:0 cfg->logDrvCount:0 ldCount:7 
12/30/19 10:13:11: C0:NumberOfVdsWithPinnedCache: number_of_pinned_vds = 1
```

均提示，侦测到PD Foreign 状态 ```Foreign Configuration Detected ```

# 解决方法

清理Foreign状态

```shell
root@node247:~# /opt/MegaRAID/MegaCli/MegaCli64 -CfgForeign -Clear -a0
                                     
Failed to clear Foreign configuration 0 on controller 0.

FW error description: 
 The current operation is not allowed because the controller has data in cache for offline or missing virtual disks.  

Exit Code: 0x54
root@node247:~# 
```

很遗憾，报错了，究其原因，是VD直接被拔掉，VD对应的PD里还有一些cache，这些cache需要先清理掉。

再次解决之：

```shell
root@node247:~# /opt/MegaRAID/MegaCli/MegaCli64  -DiscardPreservedCache -L1 -a0 
                                     
Adapter #0

Virtual Drive(Target ID 01): Preserved Cache Data Cleared.

Exit Code: 0x00
root@node247:~# /opt/MegaRAID/MegaCli/MegaCli64 -CfgForeign -Clear -aALL
                                     
Foreign configuration 0 is cleared on controller 0.

Exit Code: 0x00
root@node247:~# 
```

这里成功清理了对应VD的cache（虽然VD已经不存在了，但要记住这个RAID0在损坏前的VD id，这里是1），之后就可以成功创建RAID0了

