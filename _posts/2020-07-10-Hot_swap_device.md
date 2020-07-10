---
layout:     post
title:      "热插拔设备"
subtitle:   "Hot swap device"
date:       2020-07-10
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

测试中碰到破坏RAID或下线磁盘的场景，需要从设备上拔盘，然后等产品侦测到对应Disk或VD异常后，再插回去，验证程序侦测及时性是否存在问题。

由于要频繁的进出机房进行设备的拔出与插回操作，比较麻烦，是否有更便捷的方式进行操作呢？

本文介绍同事推荐的，在有热交换驱动器情况下，scsi热插拔指令（scsi remove-single-device，scsi add-single-device），移除和回插某块设备。

# 实践

## 移除设备

{% raw %}```
echo 'scsi remove-single-device 0 0 17 0' > /proc/scsi/scsi
```{% endraw %}

## 添加设备

{% raw %}```
echo 'scsi add-single-device 0 0 17 0' > /proc/scsi/scsi
```{% endraw %}

其中，0 0 17 0 为对应磁盘的信息，参考如下：

```
root@node75:~# lsscsi 
[0:0:0:0]    enclosu GIGABYTE S451 series      000a  -        
[0:0:1:0]    enclosu GIGABYTE S451 series      000a  -        
[0:0:17:0]   disk    ATA      INTEL SSDSC2KG48 0142  /dev/sdh 
[0:2:0:0]    disk    AVAGO    Gigabyte MR-3108 4.68  /dev/sdb 
[0:2:1:0]    disk    AVAGO    Gigabyte MR-3108 4.68  /dev/sde 
[0:2:2:0]    disk    AVAGO    Gigabyte MR-3108 4.68  /dev/sdc 
[0:2:3:0]    disk    AVAGO    Gigabyte MR-3108 4.68  /dev/sdd 
[1:0:0:0]    disk    ATA      INTEL SSDSC2KG24 0100  /dev/sdf 
[2:0:0:0]    disk    ATA      INTEL SSDSC2KG24 0100  /dev/sdg 
root@node75:~#
```


* 第一列：SCSI设备id，这四个字段分别对应信息为：hostadapter id，SCSI channel on hostadapter，vd target ID， LUN
* 第二列：设备类型
* 第3，4，5列：设备厂商，型号，版本信息  (Vendor,Model,Rev)
* 最后一列：Rev，设备主节点名，可以理解为设备在系统中的名称，如果是磁盘，则为/dev/sdxxx

单独展示一下这里的第三列，第四列，第五列信息：

| **第三列**                     | **第四列**         | **第五列**                               |
| ------------------------------ | ------------------------------------------------------------ |
| AVAGO  | Gigabyte MR-3108   | 4.68    |

分别对应着Vendor，Model， Rev，参考如下：


```
root@node75:/proc/scsi# lsscsi -c
Attached devices: 
Host: scsi0 Channel: 00 Target: 00 Lun: 00
  Vendor: GIGABYTE Model: S451 series      Rev: 000a
  Type:   Enclosure                        ANSI SCSI revision: 05
Host: scsi0 Channel: 00 Target: 01 Lun: 00
  Vendor: GIGABYTE Model: S451 series      Rev: 000a
  Type:   Enclosure                        ANSI SCSI revision: 05
Host: scsi0 Channel: 00 Target: 17 Lun: 00
  Vendor: ATA      Model: INTEL SSDSC2KG48 Rev: 0142
  Type:   Direct-Access                    ANSI SCSI revision: 06
Host: scsi0 Channel: 02 Target: 00 Lun: 00
  Vendor: AVAGO    Model: Gigabyte MR-3108 Rev: 4.68
  Type:   Direct-Access                    ANSI SCSI revision: 05
Host: scsi0 Channel: 02 Target: 01 Lun: 00
  Vendor: AVAGO    Model: Gigabyte MR-3108 Rev: 4.68
  Type:   Direct-Access                    ANSI SCSI revision: 05
Host: scsi0 Channel: 02 Target: 02 Lun: 00
  Vendor: AVAGO    Model: Gigabyte MR-3108 Rev: 4.68
  Type:   Direct-Access                    ANSI SCSI revision: 05
Host: scsi0 Channel: 02 Target: 03 Lun: 00
  Vendor: AVAGO    Model: Gigabyte MR-3108 Rev: 4.68
  Type:   Direct-Access                    ANSI SCSI revision: 05
Host: scsi1 Channel: 00 Target: 00 Lun: 00
  Vendor: ATA      Model: INTEL SSDSC2KG24 Rev: 0100
  Type:   Direct-Access                    ANSI SCSI revision: 05
Host: scsi2 Channel: 00 Target: 00 Lun: 00
  Vendor: ATA      Model: INTEL SSDSC2KG24 Rev: 0100
  Type:   Direct-Access                    ANSI SCSI revision: 05
root@node75:/proc/scsi#
```

热插拔磁盘后，对应的kern log信息片断参考如下:

```
Jul  9 13:46:46 node75 kernel: [ 8752.867575] sd 0:0:17:0: SCSI device is removed
Jul  9 13:46:46 node75 kernel: [ 8752.867895] [830035]: scst: scst_unregister_device:1188:Detached from scsi0, channel 0, id 17, lun 0, type 0
Jul  9 13:46:46 node75 kernel: [ 8752.868087] print_req_error: I/O error, dev sda, sector 0
Jul  9 13:46:46 node75 kernel: [ 8752.875385] sd 0:0:17:0: [sda] Synchronizing SCSI cache
Jul  9 13:46:46 node75 kernel: [ 8752.875497] sd 0:0:17:0: [sda] Synchronize Cache(10) failed: Result: hostbyte=DID_BAD_TARGET driverbyte=DRIVER_OK
Jul  9 13:46:46 node75 kernel: [ 8752.895282] megaraid_sas 0000:af:00.0: scanning for scsi0...
Jul  9 13:46:48 node75 kernel: [ 8754.164633] scsi 0:0:17:0: Direct-Access     ATA      INTEL SSDSC2KG48 0142 PQ: 0 ANSI: 6
Jul  9 13:46:48 node75 kernel: [ 8754.166811] sd 0:0:17:0: Attached scsi generic sg2 type 0
Jul  9 13:46:48 node75 kernel: [ 8754.166818] sd 0:0:17:0: [sdh] 937703088 512-byte logical blocks: (480 GB/447 GiB)
Jul  9 13:46:48 node75 kernel: [ 8754.166821] sd 0:0:17:0: [sdh] 4096-byte physical blocks
Jul  9 13:46:48 node75 kernel: [ 8754.166838] [830035]: scst: scst_register_device:1102:Attached to scsi0, channel 0, id 17, lun 0, type 0
Jul  9 13:46:48 node75 kernel: [ 8754.167729] sd 0:0:17:0: [sdh] Write Protect is off
Jul  9 13:46:48 node75 kernel: [ 8754.167731] sd 0:0:17:0: [sdh] Mode Sense: 9b 00 10 08
Jul  9 13:46:48 node75 kernel: [ 8754.168049] sd 0:0:17:0: [sdh] Write cache: enabled, read cache: enabled, supports DPO and FUA
Jul  9 13:46:48 node75 kernel: [ 8754.174319]  sdh: sdh1 sdh2
Jul  9 13:46:48 node75 kernel: [ 8754.176615] sd 0:0:17:0: [sdh] Attached SCSI disk
Jul  9 13:46:48 node75 kernel: [ 8754.739509] blk_partition_remap: fail for partition 2
Jul  9 13:46:48 node75 kernel: [ 8754.739514] EXT4-fs error (device sda2): ext4_find_entry:1455: inode #2: comm ezrpcd: reading directory lblock 0
Jul  9 13:46:52 node75 kernel: [ 8758.867351] sd 0:0:17:0: SCSI device is removed
Jul  9 13:46:52 node75 kernel: [ 8758.867648] [830035]: scst: scst_unregister_device:1188:Detached from scsi0, channel 0, id 17, lun 0, type 0
Jul  9 13:46:52 node75 kernel: [ 8758.872546] sd 0:0:17:0: [sdh] Synchronizing SCSI cache
Jul  9 13:46:52 node75 kernel: [ 8758.872627] sd 0:0:17:0: [sdh] Synchronize Cache(10) failed: Result: hostbyte=DID_BAD_TARGET driverbyte=DRIVER_OK
Jul  9 13:46:52 node75 kernel: [ 8758.897329] megaraid_sas 0000:af:00.0: scanning for scsi0...
Jul  9 13:46:57 node75 kernel: [ 8763.163262] scsi 0:0:17:0: Direct-Access     ATA      INTEL SSDSC2KG48 0142 PQ: 0 ANSI: 6
Jul  9 13:46:57 node75 kernel: [ 8763.165348] sd 0:0:17:0: Attached scsi generic sg2 type 0
Jul  9 13:46:57 node75 kernel: [ 8763.165372] [830035]: scst: scst_register_device:1102:Attached to scsi0, channel 0, id 17, lun 0, type 0
Jul  9 13:46:57 node75 kernel: [ 8763.166274] sd 0:0:17:0: [sdh] 937703088 512-byte logical blocks: (480 GB/447 GiB)
Jul  9 13:46:57 node75 kernel: [ 8763.166279] sd 0:0:17:0: [sdh] 4096-byte physical blocks
Jul  9 13:46:57 node75 kernel: [ 8763.166558] sd 0:0:17:0: [sdh] Write Protect is off
Jul  9 13:46:57 node75 kernel: [ 8763.166561] sd 0:0:17:0: [sdh] Mode Sense: 9b 00 10 08
Jul  9 13:46:57 node75 kernel: [ 8763.166893] sd 0:0:17:0: [sdh] Write cache: enabled, read cache: enabled, supports DPO and FUA
Jul  9 13:46:57 node75 kernel: [ 8763.175450]  sdh: sdh1 sdh2
Jul  9 13:46:57 node75 kernel: [ 8763.177604] sd 0:0:17:0: [sdh] Attached SCSI disk
```

BTW，本示例中，0:0:17:0: [sdh] 是一块SSD，做成JBOD模式，当JBOD对应盘正常在设备上运行时，是不支持Megacli/storcli下线磁盘指令的，一旦执行报错信息参考如下:


```
root@node75:~# storcli64 /c0/e1/s17 set offline
Controller = 0
Status = Failure
Description = No drive found!

Detailed Status :
===============

-----------------------------------------
Drive      Status  ErrCd ErrMsg
-----------------------------------------
/c0/e1/s17 Failure   255 Drive not found
-----------------------------------------


root@node75:~#
```

