---
layout:     post
title:      "磁盘健康评估"
subtitle:   "Disk Health Assessment"
date:       2023-01-23
author:     "Gavin Wang"
catalog:    true
categories:
    - [Disk]
tags:
    - Disk 
---

# 概述

Scaler 产品中有一feature，关于DISK的健康健康。

本文概要的介绍一下如何判断磁盘的健康状态。


# 磁盘健康检测操作

## 磁盘在Raid卡上

命令:

```shell 
$ smartctl  -A -d megaraid,{1} {2} 
```

参数：

```shell
{1} --> raid卡上的VD会有一个Device ID
{2} --> 磁盘设备的 disk name 形式是：/dev/sdX
```

举例：

获取设备的 SCSI NAA ID 

```shell
$ udevadm info --query=symlink --name=sdc
disk/by-id/scsi-36001485000764bd02b0e1956937eb1f8 
disk/by-id/scsi-SAVAGO_Gigabyte_MR-3108_00f8b17e9356190e2bd04b7600504801 
disk/by-id/wwn-0x6001485000764bd02b0e1956937eb1f8 disk/by-path/pci-0000:af:00.0-scsi-0:2:2:0
```

再通过 storcli64 筛选符合该 ID 的 VD 组信息, 筛选对应VD信息 

```shell
$ storcli64 /call/vall show all | grep -B100 6001485000764bd02b0e1956937eb1f8
/c0/v2 :
======
--------------------------------------------------------------
DG/VD TYPE  State Access Consist Cache Cac sCC      Size Name 
--------------------------------------------------------------
3/2   RAID5 Optl  RW     Yes     NRWBD -   ON  36.383 TB      
--------------------------------------------------------------

PDs for VD 2 :
============
-------------------------------------------------------------------------------
EID:Slt DID State DG     Size Intf Med SED PI SeSz Model               Sp Type 
-------------------------------------------------------------------------------
56:1     74 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:2     80 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:3     73 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:4     58 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:5     79 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:6     90 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
-------------------------------------------------------------------------------

VD2 Properties :
==============
Strip Size = 128 KB
Number of Blocks = 78134968320
VD has Emulated PD = Yes
Span Depth = 1
Number of Drives Per Span = 6
Write Cache(initial setting) = WriteBack
Disk Cache Policy = Disabled
Encryption = None
Data Protection = Disabled
Active Operations = None
Exposed to OS = Yes
Creation Date = 21-11-2022
Creation Time = 11:11:18 AM
Emulation type = default
Cachebypass size = Cachebypass-64k
Cachebypass Mode = Cachebypass Intelligent
Is LD Ready for OS Requests = Yes
SCSI NAA Id = 6001485000764bd02b0e1956937eb1f8        ----可以看到匹配的SCSI NAA Id,对应的是 VD2，成员盘有6个
```

各个成员盘的 Device ID 便是表格中的 DID 列值，至此可由 smartctl 来确认各个磁盘健康状态

查看磁盘健康信息 

```shell
$ smartctl -A -d megaraid,73 /dev/sdc
smartctl 7.0 2018-12-30 r4883 [x86_64-linux-4.14.148-202207281639.git553ed7f] (local build)
Copyright (C) 2002-18, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000b   100   100   050    Pre-fail  Always       -       0
  2 Throughput_Performance  0x0005   100   100   050    Pre-fail  Offline      -       0
  3 Spin_Up_Time            0x0027   100   100   001    Pre-fail  Always       -       6016
  4 Start_Stop_Count        0x0032   100   100   000    Old_age   Always       -       1002
  5 Reallocated_Sector_Ct   0x0033   100   100   050    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x000b   100   100   050    Pre-fail  Always       -       0
  8 Seek_Time_Performance   0x0005   100   100   050    Pre-fail  Offline      -       0
  9 Power_On_Hours          0x0032   060   060   000    Old_age   Always       -       16152
 10 Spin_Retry_Count        0x0033   120   100   030    Pre-fail  Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       548
191 G-Sense_Error_Rate      0x0032   100   100   000    Old_age   Always       -       0
192 Power-Off_Retract_Count 0x0032   099   099   000    Old_age   Always       -       530
193 Load_Cycle_Count        0x0032   100   100   000    Old_age   Always       -       1070
194 Temperature_Celsius     0x0022   100   100   000    Old_age   Always       -       31 (Min/Max 14/55)
196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       0
197 Current_Pending_Sector  0x0032   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0030   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x0032   200   200   000    Old_age   Always       -       0
220 Disk_Shift              0x0002   100   100   000    Old_age   Always       -       0
222 Loaded_Hours            0x0032   061   061   000    Old_age   Always       -       15639
223 Load_Retry_Count        0x0032   100   100   000    Old_age   Always       -       0
224 Load_Friction           0x0022   100   100   000    Old_age   Always       -       0
226 Load-in_Time            0x0026   100   100   000    Old_age   Always       -       558
240 Head_Flying_Hours       0x0001   100   100   001    Pre-fail  Offline      -       0
```

重点关注几个 RAW_VALUE 

```shell
 5  Reallocated_Sector_Ct         ：  reallocated sectors count 重分配扇区计数：硬盘生产过程中，有一部分扇区是保留的。
                                                       当一些普通扇区读/写/验证错误，则重新映射到保留扇区，挂起该异常扇区，并增加计数。随着计数增加，io性能骤降。如果数值不为0，就需要密切关注硬盘健康状况；
                                                       如果持续攀升，则硬盘已经损坏；如果重分配扇区数超过保留扇区数，将不可修复
197 Current_Pending_Sector    ：  待映射扇区数：出现异常的扇区数量，待被映射的扇区数量。 如果该异常扇区之后成功读写，则计数会减小，扇区也不会重新映射。读错误不会重新映射，只有写错误才会重新映射；
194 Temperature_Celsius          ：  硬盘温度
```


## 磁盘不在Raid卡上

命令 

```shell
$ smartctl -A {1}
```

参数：

```shell
{1} --> 设备的 disk name，形式是 /dev/sdX

```

举例：

直接获取磁盘健康状态 

```shell
$ smartctl -A /dev/sdg
smartctl 7.0 2018-12-30 r4883 [x86_64-linux-4.14.148-202207281639.git553ed7f] (local build)
Copyright (C) 2002-18, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 1
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  5 Reallocated_Sector_Ct   0x0032   100   100   000    Old_age   Always       -       0
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       9264
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       243
170 Available_Reservd_Space 0x0033   100   100   010    Pre-fail  Always       -       0
171 Program_Fail_Count      0x0032   100   100   000    Old_age   Always       -       0
172 Erase_Fail_Count        0x0032   100   100   000    Old_age   Always       -       0
174 Unsafe_Shutdown_Count   0x0032   100   100   000    Old_age   Always       -       171
175 Power_Loss_Cap_Test     0x0033   100   100   010    Pre-fail  Always       -       2359 (243 65535)
183 SATA_Downshift_Count    0x0032   100   100   000    Old_age   Always       -       0
184 End-to-End_Error_Count  0x0033   100   100   090    Pre-fail  Always       -       0
187 Uncorrectable_Error_Cnt 0x0032   100   100   000    Old_age   Always       -       0
190 Drive_Temperature       0x0022   063   061   000    Old_age   Always       -       37 (Min/Max 37/39)
192 Unsafe_Shutdown_Count   0x0032   100   100   000    Old_age   Always       -       171
194 Temperature_Celsius     0x0022   100   100   000    Old_age   Always       -       37
197 Pending_Sector_Count    0x0012   100   100   000    Old_age   Always       -       0
199 CRC_Error_Count         0x003e   100   100   000    Old_age   Always       -       0
225 Host_Writes_32MiB       0x0032   100   100   000    Old_age   Always       -       1456731
226 Workld_Media_Wear_Indic 0x0032   100   100   000    Old_age   Always       -       1832
227 Workld_Host_Reads_Perc  0x0032   100   100   000    Old_age   Always       -       6
228 Workload_Minutes        0x0032   100   100   000    Old_age   Always       -       554202
232 Available_Reservd_Space 0x0033   100   100   010    Pre-fail  Always       -       0
233 Media_Wearout_Indicator 0x0032   099   099   000    Old_age   Always       -       0
234 Thermal_Throttle_Status 0x0032   100   100   000    Old_age   Always       -       0/0
235 Power_Loss_Cap_Test     0x0033   100   100   010    Pre-fail  Always       -       2359 (243 65535)
241 Host_Writes_32MiB       0x0032   100   100   000    Old_age   Always       -       1456731
242 Host_Reads_32MiB        0x0032   100   100   000    Old_age   Always       -       108597
243 NAND_Writes_32MiB       0x0032   100   100   000    Old_age   Always       -       2011255
```

## Raid卡上没有建立Raid的盘

扫描所有设备 

```shell
$ smartctl --scan
/dev/sda -d scsi # /dev/sda, SCSI device
/dev/sdb -d scsi # /dev/sdb, SCSI device
/dev/sdc -d scsi # /dev/sdc, SCSI device
/dev/sdd -d scsi # /dev/sdd, SCSI device
/dev/sde -d scsi # /dev/sde, SCSI device
/dev/sdf -d scsi # /dev/sdf, SCSI device
/dev/sdg -d scsi # /dev/sdg, SCSI device
/dev/bus/0 -d megaraid,57 # /dev/bus/0 [megaraid_disk_57], SCSI device
/dev/bus/0 -d megaraid,58 # /dev/bus/0 [megaraid_disk_58], SCSI device
/dev/bus/0 -d megaraid,59 # /dev/bus/0 [megaraid_disk_59], SCSI device
/dev/bus/0 -d megaraid,60 # /dev/bus/0 [megaraid_disk_60], SCSI device
/dev/bus/0 -d megaraid,61 # /dev/bus/0 [megaraid_disk_61], SCSI device
/dev/bus/0 -d megaraid,62 # /dev/bus/0 [megaraid_disk_62], SCSI device
/dev/bus/0 -d megaraid,63 # /dev/bus/0 [megaraid_disk_63], SCSI device
/dev/bus/0 -d megaraid,64 # /dev/bus/0 [megaraid_disk_64], SCSI device
/dev/bus/0 -d megaraid,65 # /dev/bus/0 [megaraid_disk_65], SCSI device
/dev/bus/0 -d megaraid,66 # /dev/bus/0 [megaraid_disk_66], SCSI device
/dev/bus/0 -d megaraid,67 # /dev/bus/0 [megaraid_disk_67], SCSI device
```

通过 storcli64 获取没有建立 Raid 盘的 DID，然后直接获取健康信息；传参时候，用 /dev/bus/0 代替 disk name,获取磁盘健康信息 

```shell
$ smartctl -A -d megaraid,66 /dev/bus/0
......
```

这里可以发现对比前面 disk name 参数有所改变，因为对于没有建立Raid的盘，系统层级没有与之对应的 sdX，所以用 /dev/bug/0 来代替这个参数，/dev/bus/0 也就是总线设备路径



# 附加

## 定位系统层级盘符对应的Raid组

1、JBOD盘

JBOD磁盘，通过SN（Serial Number）来定位盘符 

#通过 smartctl 获取 /dev/sda 的 SN

```shell
$ smartctl -a /dev/sda
=== START OF INFORMATION SECTION ===
Device Model     :     TOSHIBA MG05ACA800E
Serial Number    :      29Q1KOBBFUUD          --------通过此标识来定位JBOD磁盘信息
LU WWN Device Id :       5 000039 91b703090
Firmware Version :       GX2A
User Capacity    :      8,001,563,222,016 bytes [8.00 TB]
Sector Sizes     :     512 bytes logical, 4096 bytes physical
Rotation Rate    :      7200 rpm
```

查看Raid卡上该磁盘信息 


```shell
$ storcli64 /call/eall/sall show all
......
Drive /c0/e55/s1 Device attributes :
==================================
SN                = 29Q1KOBBFUUD             --------可以得到这个SN对应的磁盘槽位是/c0/e55/s1
Manufacturer Id   = ATA     
Model Number      = TOSHIBA MG05ACA800E
NAND Vendor       = NA
WWN               = 500003991b703090
Firmware Revision = GX2A
......
```

2、普通Raid组磁盘，通过 scsi_id 定位

获取硬盘 scsi_id 

```shell
$ udevadm info --query=symlink --name=sdc
disk/by-id/scsi-36001485000764bd02b0e1956937eb1f8    ----取这个 scsi_3 后面内容(截取部分 grep过滤即可)    
disk/by-id/scsi-SAVAGO_Gigabyte_MR-3108_00f8b17e9356190e2bd04b7600504801        
disk/by-id/wwn-0x6001485000764bd02b0e1956937eb1f8 disk/by-path/pci-0000:af:00.0-scsi-0:2:2:0
```

storcli64 获取对应 Raid 组信息 

```shell
$ storcli64 /call/vall show all | grep -B100 6001485000764bd02b0e1956937eb1f8
/c0/v2 :
======
--------------------------------------------------------------
DG/VD TYPE  State Access Consist Cache Cac sCC      Size Name 
--------------------------------------------------------------
3/2   RAID5 Optl  RW     Yes     NRWBD -   ON  36.383 TB      
--------------------------------------------------------------

PDs for VD 2 :
============
-------------------------------------------------------------------------------
EID:Slt DID State DG     Size Intf Med SED PI SeSz Model               Sp Type 
-------------------------------------------------------------------------------
56:1     74 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:2     80 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:3     73 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:4     58 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:5     79 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
56:6     90 Onln   3 7.276 TB SATA HDD N   N  512B TOSHIBA MG05ACA800E U  -    
-------------------------------------------------------------------------------

VD2 Properties :
==============
Strip Size = 128 KB
Number of Blocks = 78134968320
VD has Emulated PD = Yes
Span Depth = 1
Number of Drives Per Span = 6
Write Cache(initial setting) = WriteBack
Disk Cache Policy = Disabled
Encryption = None
Data Protection = Disabled
Active Operations = None
Exposed to OS = Yes
Creation Date = 21-11-2022
Creation Time = 11:11:18 AM
Emulation type = default
Cachebypass size = Cachebypass-64k
Cachebypass Mode = Cachebypass Intelligent
Is LD Ready for OS Requests = Yes
SCSI NAA Id = 6001485000764bd02b0e1956937eb1f8             ----对应该 SCSI NAA Id 的VD，VD成员盘信息如表格所示
```

新建RAID或者换盘重建RAID时，在满足一定磁盘数量后会进行后台初始化，后台初始化会对全盘进行数据校验，十分耗时，若想终止后台初始化可参考以下命令，先执行命令1，再执行命令2

后台初始化相关命令:

1、禁止后台初始化 `/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -dsbl -L0 -a0`

2、结束正在进行的后台初始化 `/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -abort -L0 -a0`

3、查看后台初始化的设置 `/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -getsetting -L0 -a0`

4、显示后台初始化进度 `/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -progdsply -L0 -a0`



