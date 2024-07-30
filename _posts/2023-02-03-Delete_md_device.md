---
layout:     post
title:      "彻底删除Linux下md设备"
subtitle:   "Delete Linux of md deivce"
date:       2023-02-03
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
    - mdadm
---


# 概述

Lab 2U4N设备上SSD盘有soft-raid存在，本文介绍如何清理掉这些md 设备。


# 实践


## 获取相关信息

当前OS中md设备信息：

```shell
root@node123:~# lsblk
NAME        MAJ:MIN RM    SIZE RO TYPE  MOUNTPOINT
sda           8:0    0    3.5T  0 disk  
sdb           8:16   0    3.5T  0 disk  
sdc           8:32   0    3.5T  0 disk  
sdd           8:48   0    3.5T  0 disk  
sde           8:64   0    3.5T  0 disk  
sdf           8:80   0    3.5T  0 disk  
└─md126       9:126  0    3.5T  0 raid0 
  ├─md126p1 259:6    0      8G  0 part  
  ├─md126p2 259:7    0    3.5T  0 part  
  └─md126p3 259:8    0 1007.5K  0 part  
nvme0n1     259:0    0  238.5G  0 disk  
├─nvme0n1p1 259:2    0   1007K  0 part  
├─nvme0n1p2 259:3    0    512M  0 part  /boot/efi
├─nvme0n1p3 259:4    0      8G  0 part  [SWAP]
└─nvme0n1p4 259:5    0    230G  0 part  /
nvme1n1     259:1    0  238.5G  0 disk  
pmem0       259:9    0     16G  0 disk  
pmem1       259:10   0     16G  0 disk  
root@node123:~# 
```


```shell
root@node123:~# mdadm -Ds 
ARRAY /dev/md/ddf0 metadata=ddf UUID=783f1a5c:5a361165:b27fff3b:c518b21a
ARRAY /dev/md126 container=/dev/md/ddf0 member=2 UUID=926ae63a:c3cd5a73:93063a44:eda9c39f
root@node123:~# 
```

```shell
root@node123:~# mdadm -D /dev/md126
/dev/md126:
         Container : /dev/md/ddf0, member 2
        Raid Level : raid0
        Array Size : 3750199296 (3576.47 GiB 3840.20 GB)
      Raid Devices : 1
     Total Devices : 1

             State : clean 
    Active Devices : 1
   Working Devices : 1
    Failed Devices : 0
     Spare Devices : 0

        Chunk Size : 64K

Consistency Policy : none

    Container GUID : 4C534920:20202020:1000005D:10009361:50C1A436:0B5F09A0
                  (LSI      12/07/22 16:09:26)
               Seq : 00000259
     Virtual Disks : 5

    Number   Major   Minor   RaidDevice State
       0       8       80        0      active sync   /dev/sdf
root@node123:~#
```

```shell
root@node123:/etc/mdadm# cat /proc/mdstat 
Personalities : [raid0] [linear] [multipath] [raid1] [raid6] [raid5] [raid4] [raid10] 
md127 : inactive sdf[0](S)
      538968 blocks super external:ddf
       
unused devices: <none>
root@node123:/etc/mdadm# 
```

```shell
root@node123:/etc/mdadm# mdadm -D /dev/md127
/dev/md127:
           Version : ddf
        Raid Level : container
     Total Devices : 1

   Working Devices : 1

    Container GUID : 4C534920:20202020:1000005D:10009361:50C1A436:0B5F09A0
                  (LSI      12/07/22 16:09:26)
               Seq : 00000259
     Virtual Disks : 5

     Member Arrays :

    Number   Major   Minor   RaidDevice

       -       8       80        -        /dev/sdf
root@node123:/etc/mdadm#
```

```shell
root@node123:~# cat /etc/mdadm/mdadm.conf
# mdadm.conf
#
# !NB! Run update-initramfs -u after updating this file.
# !NB! This will ensure that initramfs has an uptodate copy.
#
# Please refer to mdadm.conf(5) for information about this file.
#

# by default (built-in), scan all partitions (/proc/partitions) and all
# containers for MD superblocks. alternatively, specify devices to scan, using
# wildcards if desired.
#DEVICE partitions containers

# automatically tag new arrays as belonging to the local system
HOMEHOST <system>

# instruct the monitoring daemon where to send mail alerts
MAILADDR root

# definitions of existing MD arrays
ARRAY metadata=ddf UUID=f6da2fa6:f847cfe8:6efae15e:1ec1cb18
ARRAY container=f6da2fa6:f847cfe8:6efae15e:1ec1cb18 member=0 UUID=9ff807d6:cd51ad98:0fde88a0:bed80d0e
ARRAY container=f6da2fa6:f847cfe8:6efae15e:1ec1cb18 member=1 UUID=be17285a:62edb788:24f8e528:00912e8c
ARRAY container=f6da2fa6:f847cfe8:6efae15e:1ec1cb18 member=2 UUID=b08d0c30:d7aa7ba5:0a22787e:103831d9
ARRAY container=f6da2fa6:f847cfe8:6efae15e:1ec1cb18 member=3 UUID=5159a750:d1c2251f:56b0ef10:4b9a1309
ARRAY container=f6da2fa6:f847cfe8:6efae15e:1ec1cb18 member=4 UUID=70f4a9f0:fdb95f4d:753d57a5:8c2314c0
ARRAY metadata=ddf UUID=471d86af:9306e6d2:bc56f74d:c3b578f9
ARRAY container=471d86af:9306e6d2:bc56f74d:c3b578f9 member=0 UUID=6d0bf5f0:b39ef888:80529401:91f64dcb
ARRAY container=471d86af:9306e6d2:bc56f74d:c3b578f9 member=1 UUID=7cc9f621:c04ac67c:f4b0976a:78fe15f2
ARRAY container=471d86af:9306e6d2:bc56f74d:c3b578f9 member=2 UUID=95994645:864ddcc9:67c2f8ce:9fe93d97
ARRAY container=471d86af:9306e6d2:bc56f74d:c3b578f9 member=3 UUID=91b65356:8b4ec6e8:f64d7f23:63f8bd83
ARRAY container=471d86af:9306e6d2:bc56f74d:c3b578f9 member=4 UUID=c8f2b38c:f32ce54b:9d2ef6ff:4e537329
ARRAY metadata=ddf UUID=783f1a5c:5a361165:b27fff3b:c518b21a
ARRAY container=783f1a5c:5a361165:b27fff3b:c518b21a member=0 UUID=af20c622:b4cab24e:6e79902d:a83f750c
ARRAY container=783f1a5c:5a361165:b27fff3b:c518b21a member=1 UUID=2f4788c1:1dbe4d60:274c34fc:fdad0f1e
ARRAY container=783f1a5c:5a361165:b27fff3b:c518b21a member=2 UUID=926ae63a:c3cd5a73:93063a44:eda9c39f
ARRAY container=783f1a5c:5a361165:b27fff3b:c518b21a member=3 UUID=5bebdf83:dfd7c23d:99bdb41a:3991d212
ARRAY container=783f1a5c:5a361165:b27fff3b:c518b21a member=4 UUID=efc49f2c:f23319c6:b2b4666f:26f9dba6
ARRAY container=783f1a5c:5a361165:b27fff3b:c518b21a member=5 UUID=e05f0b90:235cb256:9d031efe:ac7f6f4f

# This configuration was auto-generated on Thu, 02 Feb 2023 12:52:09 +0800 by mkconf
root@node123:~#
```

# 删除md device

```shell
root@node123:~# mdadm --stop -s /dev/md126
mdadm: stopped /dev/md126
root@node123:~# 
```

```shell
root@node123:~# mdadm --misc --zero-superblock /dev/sdf
mdadm: Couldn't open /dev/sdf for write - not zeroing
root@node123:~# mdadm --zero-superblock /dev/sdf
mdadm: Couldn't open /dev/sdf for write - not zeroing
root@node123:~# 
```


* 说明
通过上面的方法，是无法删除md设备的，即使清空了/etc/mdadm/mdadm.conf也没用，重启机器后md设备又在了。


正确的删除方法是：

## 从/proc/mdstat中获取当前OS下的所有md信息


```shell
root@node122:/var/log/history# cat /proc/mdstat 
Personalities : [raid0] [linear] [multipath] [raid1] [raid6] [raid5] [raid4] [raid10] 
md120 : inactive sda[0]
      3750199296 blocks super external:/md124/3
       
md124 : inactive sda[1](S) sdb[0](S)
      1077936 blocks super external:ddf
       
md127 : inactive sdd[1](S) sdc[0](S)
      1077936 blocks super external:ddf
       
unused devices: <none>
root@node122:/var/log/history# 
```

根据/proc/mdstat中的md信息，逐一stop并清理掉metadata信息，如下：

```shell
root@node123:/etc/mdadm# mdadm -S /dev/md127
mdadm: stopped /dev/md127
root@node123:/etc/mdadm# mdadm --zero-superblock /dev/sdf
root@node123:/etc/mdadm# 
```

这样，即使机器reboot后，也不会再次出现md设备了，干净清理掉。

