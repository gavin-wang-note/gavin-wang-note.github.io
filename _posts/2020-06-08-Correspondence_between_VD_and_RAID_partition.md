---
layout:     post
title:      "VD与RAID分区对应关系"
subtitle:   "Correspondence between VD and RAID partition"
date:       2020-06-08
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

环境中创建了VD,lsblk可以看到创建好后的分区信息，如何获取分区与RAID VD之间的对应关系呢，比如/dev/sdc分区，对应RAID组哪个VD？


# 实践

Step1. 获取RAID卡的Vendor Id和Device Id


```
root@ec-node3:~# /opt/MegaRAID/MegaCli/MegaCli64 -adpallinfo -aall | grep -Ei 'Vendor Id|Device Id'
Vendor Id       : 1000
Device Id       : 005d
```

Step2. 获取VD的Target Id


```
root@ec-node3:~# /opt/MegaRAID/MegaCli/MegaCli64 -ldpdinfo  aall | grep 'Target Id'
Virtual Drive: 0 (Target Id: 0)
Virtual Drive: 1 (Target Id: 1)
Virtual Drive: 2 (Target Id: 2)
Virtual Drive: 3 (Target Id: 3)
Virtual Drive: 4 (Target Id: 4)
Virtual Drive: 5 (Target Id: 5)
Virtual Drive: 6 (Target Id: 6)
Virtual Drive: 7 (Target Id: 7)
Virtual Drive: 8 (Target Id: 8)
root@ec-node3:~#
```

Step3. 获取设备前缀信息


```
root@ec-node3:~# lspci -nd 1000:005d
af:00.0 0104: 1000:005d (rev 02)
root@ec-node3:~# 
```

这里的```af:00.0```，就是我们所需的设备前缀信息。


Step4. 根据设备前缀信息以及Target Id，获取对应分区信息

Linux 命令行操作如下：

```
root@ec-node3:~# cd /dev/disk/by-path
root@ec-node3:/dev/disk/by-path# ls -l
total 0
lrwxrwxrwx 1 root root  9 Jun  8 14:39 pci-0000:00:11.5-ata-1 -> ../../sdj
lrwxrwxrwx 1 root root 10 Jun  8 14:39 pci-0000:00:11.5-ata-1-part1 -> ../../sdj1
lrwxrwxrwx 1 root root 10 Jun  8 14:39 pci-0000:00:11.5-ata-1-part2 -> ../../sdj2
lrwxrwxrwx 1 root root 10 Jun  8 14:39 pci-0000:00:11.5-ata-1-part3 -> ../../sdj3
lrwxrwxrwx 1 root root 10 Jun  8 14:39 pci-0000:00:11.5-ata-1-part4 -> ../../sdj4
lrwxrwxrwx 1 root root  9 Jun  8 14:39 pci-0000:00:11.5-ata-2 -> ../../sdk
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:0:0 -> ../../sda
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:0:0-part1 -> ../../sda1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:1:0 -> ../../sdb
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:1:0-part1 -> ../../sdb1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:2:0 -> ../../sdc
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:2:0-part1 -> ../../sdc1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:3:0 -> ../../sdd
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:3:0-part1 -> ../../sdd1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:4:0 -> ../../sde
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:4:0-part1 -> ../../sde1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:5:0 -> ../../sdf
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:5:0-part1 -> ../../sdf1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:6:0 -> ../../sdg
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:6:0-part1 -> ../../sdg1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:7:0 -> ../../sdh
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:7:0-part1 -> ../../sdh1
lrwxrwxrwx 1 root root  9 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:8:0 -> ../../sdi
lrwxrwxrwx 1 root root 10 Jun  8 16:54 pci-0000:af:00.0-scsi-0:2:8:0-part1 -> ../../sdi1
root@ec-node3:/dev/disk/by-path#
{% raw %}root@ec-node3:/dev/disk/by-path# ls -l |grep 'pci-0000:af:00.0-scsi-0:2:2:0' | grep -v part | awk '{{print $NF}}' | awk -F'/' '{{print $NF}}' {% endraw %}
sdc
```

说明：

```pci-0000:af:00.0-scsi-0:2:2:0 ```，这里的 ```0:2:2:0 ```，从左向右数，第二位，2，表示的就是Target Id，```af:00.0 ```为设备前缀信息。


Python Code示例如下:

```
root@ec-node3:~# python
Python 2.7.12 (default, Oct  8 2019, 14:14:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> slot_name = 'af:00.0'
>>> target_id = '2'
>>> import os, re
>>> pattern = re.compile(r':{}-scsi-\d+:\d+:{}:\d+$'.format(slot_name, target_id))
>>> disk_path = None
>>> dev_path = '/dev/disk/by-path'
>>> for disk in os.listdir(dev_path):
...     if pattern.search(disk):
...         path_to_disk = os.readlink(os.path.join(dev_path, disk))
...         disk_path = os.path.normpath(os.path.join(dev_path, path_to_disk))
...         print disk_path
...         break
... 
/dev/sdc
>>> 
```

