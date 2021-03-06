---
layout:     post
title:      "HDD损坏了么？"
subtitle:   "Is my hdd wrecked?"
date:       2021-06-03
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

今天同事使用产品对HDD做分区的时候，发现程序抛异常，寻求帮助。

# 过程

由于是一个新安装OS的环境，对现有的HDD除了操作系统之外都可以做格式化处理，尝试格式化一下，出现了如下错误：

```
root@scaler:/home/btadmin# sgdisk -z /dev/sdb
GPT data structures destroyed! You may now partition the disk using fdisk or
other utilities.
```

上面是一个正常分区擦除分区信息的吐出信息，下面是一个异常的：

```
root@scaler:/home/btadmin# sgdisk -z /dev/sdd
Warning! Read error 5; strange behavior now likely!
Warning! Read error 5; strange behavior now likely!
Creating new GPT entries.
Warning! GPT main header not overwritten! Error is 5
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
GPT data structures destroyed! You may now partition the disk using fdisk or
other utilities.
```

尝试分区：

```
root@scaler:~# gdisk /dev/sdd
GPT fdisk (gdisk) version 1.0.1

Warning! Read error 5; strange behavior now likely!
Warning! Read error 5; strange behavior now likely!
Partition table scan:
  MBR: not present
  BSD: not present
  APM: not present
  GPT: not present

Creating new GPT entries.

Command (? for help): p  
Disk /dev/sdd: 7811891200 sectors, 3.6 TiB
Logical sector size: 512 bytes
Disk identifier (GUID): 21979075-7523-49C5-A52B-E8055AE1625F
Partition table holds up to 128 entries
First usable sector is 34, last usable sector is 7811891166
Partitions will be aligned on 2048-sector boundaries
Total free space is 2014 sectors (1007.0 KiB)

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048      7811891166   3.6 TiB     8300  Linux filesystem

Command (? for help): e
b	back up GPT data to a file
c	change a partition's name
d	delete a partition
i	show detailed information on a partition
l	list known partition types
n	add a new partition
o	create a new empty GUID partition table (GPT)
p	print the partition table
q	quit without saving changes
r	recovery and transformation options (experts only)
s	sort partitions
t	change a partition's type code
v	verify disk
w	write table to disk and exit
x	extra functionality (experts only)
?	print this menu

Command (? for help): w

Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): y
OK; writing new GUID partition table (GPT) to /dev/sdd.
Unable to save backup partition table! Perhaps the 'e' option on the experts'
menu will resolve this problem.
Warning! An error was reported when writing the partition table! This error
MIGHT be harmless, or the disk might be damaged! Checking it is advisable.

Command (? for help): 
```

从上面可以明显看出sdd这个分区有异常，继续查看vd与pd信息：

```
Virtual Drive: 3 (Target Id: 3)
Name                :
RAID Level          : Primary-0, Secondary-0, RAID Level Qualifier-0
Size                : 3.637 TB
Sector Size         : 512
Is VD emulated      : No
Parity Size         : 0
State               : Offline
Strip Size          : 64 KB
Number Of Drives    : 2
Span Depth          : 1
Default Cache Policy: WriteBack, ReadAheadNone, Direct, No Write Cache if Bad BBU
Current Cache Policy: WriteBack, ReadAheadNone, Direct, No Write Cache if Bad BBU
Default Access Policy: Read/Write
Current Access Policy: Read/Write
Disk Cache Policy   : Disabled
Encryption Type     : None
PI type: No PI

Is VD Cached: No
Number of Spans: 1
Span: 0 - Number of PDs: 2

PD: 0 Information
Enclosure Device ID: 8
Slot Number: 5
Drive's position: DiskGroup: 3, Span: 0, Arm: 0
Enclosure position: 1
Device Id: 15
WWN: 5000c5007995214d
Sequence Number: 2
Media Error Count: 0
Other Error Count: 0
Predictive Failure Count: 0
Last Predictive Failure Event Seq Number: 0
PD Type: SATA

Raw Size: 1.819 TB [0xe8e088b0 Sectors]
Non Coerced Size: 1.818 TB [0xe8d088b0 Sectors]
Coerced Size: 1.818 TB [0xe8d00000 Sectors]
Sector Size:  512
Logical Sector Size:  512
Physical Sector Size:  512
Firmware state: Online, Spun Up
Commissioned Spare : No
Emergency Spare : No
Device Firmware Level: SN03
Shield Counter: 0
Successful diagnostics completion on :  N/A
SAS Address(0): 0x50015b207898e72d
Connected Port Number: 0(path0) 
Inquiry Data:             Z1X3E91SST2000NM0033-9ZM175                     SN03    
FDE Capable: Not Capable
FDE Enable: Disable
Secured: Unsecured
Locked: Unlocked
Needs EKM Attention: No
Foreign State: None 
Device Speed: 6.0Gb/s 
Link Speed: 6.0Gb/s 
Media Type: Hard Disk Device
Drive:  Not Certified
Drive Temperature :39C (102.20 F)
PI Eligibility:  No 
Drive is formatted for PI information:  No
PI: No PI
Drive's NCQ setting : N/A
Port-0 :
Port status: Active
Port's Linkspeed: 6.0Gb/s 
Drive has flagged a S.M.A.R.T alert : No




PD: 1 Information
Enclosure Device ID: 8
Slot Number: 6
Drive's position: DiskGroup: 3, Span: 0, Arm: 1
Enclosure position: 1
Device Id: 14
WWN: 5000c500798ecb5a
Sequence Number: 3
Media Error Count: 0
Other Error Count: 0
Predictive Failure Count: 0
Last Predictive Failure Event Seq Number: 0
PD Type: SATA

Raw Size: 1.819 TB [0xe8e088b0 Sectors]
Non Coerced Size: 1.818 TB [0xe8d088b0 Sectors]
Coerced Size: 1.818 TB [0xe8d00000 Sectors]
Sector Size:  512
Logical Sector Size:  512
Physical Sector Size:  512
Firmware state: Failed
Commissioned Spare : Yes
Emergency Spare : Yes
Device Firmware Level: SN03
Shield Counter: 0
Successful diagnostics completion on :  N/A
SAS Address(0): 0x50015b207898e730
Connected Port Number: 0(path0) 
Inquiry Data:             Z1Y2CKNFST2000NM0033-9ZM175                     SN03    
FDE Capable: Not Capable
FDE Enable: Disable
Secured: Unsecured
Locked: Unlocked
Needs EKM Attention: No
Foreign State: None 
Device Speed: 6.0Gb/s 
Link Speed: 6.0Gb/s 
Media Type: Hard Disk Device
Drive:  Not Certified
Drive Temperature : N/A
PI Eligibility:  No 
Drive is formatted for PI information:  No
PI: No PI
Drive's NCQ setting : N/A
Port-0 :
Port status: Active
Port's Linkspeed: 6.0Gb/s 
Drive has flagged a S.M.A.R.T alert : No
```

这里显示VD 3 是Offline状态，且[8:6]这块盘Firmware state为Failed, 要再确认下，VD3对应的是哪个分区：


## Step1. 获取RAID卡的Vendor Id和Device Id

```
root@scaler:~# /opt/MegaRAID/MegaCli/MegaCli64 -adpallinfo -aall | grep -Ei 'Vendor Id|Device Id'
Vendor Id       : 1000
Device Id       : 005b
```

## Step2. 获取VD的Target Id

```
root@scaler:~# /opt/MegaRAID/MegaCli/MegaCli64 -ldpdinfo  aall | grep 'Target Id'
Virtual Drive: 0 (Target Id: 0)
Virtual Drive: 1 (Target Id: 1)
Virtual Drive: 2 (Target Id: 2)
Virtual Drive: 3 (Target Id: 3)
Virtual Drive: 4 (Target Id: 4)
```


## Step3. 获取设备前缀信息

```
root@scaler:~# lspci -nd 1000:005b
02:00.0 0104: 1000:005b (rev 05)
root@scaler:~# 
```

这里的02:00.0，就是我们所需的设备前缀信息。


## Step4. 根据设备前缀信息以及Target Id，获取对应分区信息

Linux 命令行操作如下：

{% raw %}
```
root@scaler:~# cd /dev/disk/by-path
root@scaler:/dev/disk/by-path# ls -l |grep 'pci-0000:02:00.0-scsi-0:2:2:0' | grep -v part | awk '{{print $NF}}' | awk -F'/' '{{print $NF}}' 
sdc
root@scaler:/dev/disk/by-path# ls -l
total 0
lrwxrwxrwx 1 root root  9 Jun  2 16:39 pci-0000:00:1f.2-ata-1 -> ../../sdf
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-1-part1 -> ../../sdf1
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-1-part2 -> ../../sdf2
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-1-part3 -> ../../sdf3
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-1-part4 -> ../../sdf4
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-1-part5 -> ../../sdf5
lrwxrwxrwx 1 root root  9 Jun  2 16:39 pci-0000:00:1f.2-ata-2 -> ../../sdg
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-2-part1 -> ../../sdg1
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-2-part2 -> ../../sdg2
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-2-part3 -> ../../sdg3
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-2-part4 -> ../../sdg4
lrwxrwxrwx 1 root root 10 Jun  2 16:39 pci-0000:00:1f.2-ata-2-part5 -> ../../sdg5
lrwxrwxrwx 1 root root  9 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:0:0 -> ../../sda
lrwxrwxrwx 1 root root 10 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:0:0-part1 -> ../../sda1
lrwxrwxrwx 1 root root  9 Jun  2 16:48 pci-0000:02:00.0-scsi-0:2:1:0 -> ../../sdb
lrwxrwxrwx 1 root root 10 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:1:0-part1 -> ../../sdb1
lrwxrwxrwx 1 root root  9 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:2:0 -> ../../sdc
lrwxrwxrwx 1 root root 10 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:2:0-part1 -> ../../sdc1
lrwxrwxrwx 1 root root 10 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:2:0-part2 -> ../../sdc2
lrwxrwxrwx 1 root root 10 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:2:0-part3 -> ../../sdc3
lrwxrwxrwx 1 root root 10 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:2:0-part4 -> ../../sdc4
lrwxrwxrwx 1 root root  9 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:3:0 -> ../../sdd
lrwxrwxrwx 1 root root  9 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:4:0 -> ../../sde
lrwxrwxrwx 1 root root 10 Jun  2 16:50 pci-0000:02:00.0-scsi-0:2:4:0-part1 -> ../../sde1
root@scaler:/dev/disk/by-path# 
root@scaler:/dev/disk/by-path# ls -l |grep 'pci-0000:02:00.0-scsi-0:2:3:0' | grep -v part | awk '{{print $NF}}' | awk -F'/' '{{print $NF}}' 
sdd
root@scaler:/dev/disk/by-path# 
```{% endraw %}

出现坏盘的，对应RAID组为VD 3，正好是sdd这个分区，说明HDD有损坏了，需要进行更换。

