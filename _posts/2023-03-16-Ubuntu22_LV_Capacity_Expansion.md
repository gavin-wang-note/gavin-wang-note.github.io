---
layout:     post
title:      "LV 扩容"
subtitle:   "LV Capacity Expansion"
date:       2023-03-16
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---


# 概述

前段时间基于Ubuntu22.04 搭建了Jenkins, VM 当时给的 OS disk size是100G, 今天查看环境，无意间发现/空间使用率接近50%。

本文简易概述LV扩容。


# 现象

```shell
root@jenkins:~# df -Ph
Filesystem                         Size  Used Avail Use% Mounted on
tmpfs                              796M  1.2M  794M   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv   48G   22G   25G  47% /
tmpfs                              3.9G     0  3.9G   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
/dev/sda2                          2.0G  126M  1.7G   7% /boot
tmpfs                              796M  4.0K  796M   1% /run/user/0
root@jenkins:~# lsblk
NAME                      MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
fd0                         2:0    1     4K  0 disk 
loop0                       7:0    0  63.3M  1 loop /snap/core20/1822
loop1                       7:1    0  63.3M  1 loop /snap/core20/1828
loop2                       7:2    0  79.9M  1 loop /snap/lxd/22923
loop3                       7:3    0 111.9M  1 loop /snap/lxd/24322
loop4                       7:4    0  49.8M  1 loop /snap/snapd/17950
loop5                       7:5    0  49.8M  1 loop /snap/snapd/18357
sda                         8:0    0   100G  0 disk 
├─sda1                      8:1    0     1M  0 part 
├─sda2                      8:2    0     2G  0 part /boot
└─sda3                      8:3    0    98G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0    49G  0 lvm  /
sr0                        11:0    1  1024M  0 rom  
```

可用空间98G，实际只分配了49G，余下空间想利用起来。




# 实践

1. 查看可用空间

```shell
root@jenkins:~# lvdisplay
  --- Logical volume ---
  LV Path                /dev/ubuntu-vg/ubuntu-lv
  LV Name                ubuntu-lv
  VG Name                ubuntu-vg
  LV UUID                c5tkxV-ZwMC-rVs5-ucVU-gYeQ-B36P-Fgw3JT
  LV Write Access        read/write
  LV Creation host, time ubuntu-server, 2023-01-29 15:41:37 +0800
  LV Status              available
  # open                 1
  LV Size                <49.00 GiB
  Current LE             12543
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
root@jenkins:~# 
```

```shell
root@jenkins:~# fdisk -l /dev/sda
Disk /dev/sda: 100 GiB, 107374182400 bytes, 209715200 sectors
Disk model: Virtual disk    
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: EEA2172F-74FA-41F6-AB3C-D4E8F8F5A991

Device       Start       End   Sectors Size Type
/dev/sda1     2048      4095      2048   1M BIOS boot
/dev/sda2     4096   4198399   4194304   2G Linux filesystem
/dev/sda3  4198400 209713151 205514752  98G Linux filesystem
root@jenkins:~#
```

从上图可以看出磁盘大小(98)大于系统逻辑分区大小(49G)，知道了现在磁盘完全可以提升利用率，就可以直接进行扩容，不需要额外增加硬盘


2. 执行命令扩容

`lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv`

```shell
root@jenkins:~# lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
  Size of logical volume ubuntu-vg/ubuntu-lv changed from <49.00 GiB (12543 extents) to <98.00 GiB (25087 extents).
  Logical volume ubuntu-vg/ubuntu-lv successfully resized.
root@jenkins:~# 
```

注意后面的逻辑分区名字使用lvdisplay命令获取到的

3、执行 命令 `resize2fs /dev/ubuntu-vg/ubuntu-lv` 刷新逻辑卷 

4、执行命令df -h查看效果

```shell
root@jenkins:~# df -Ph
Filesystem                         Size  Used Avail Use% Mounted on
tmpfs                              796M  1.2M  794M   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv   97G   22G   71G  24% /
tmpfs                              3.9G     0  3.9G   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
/dev/sda2                          2.0G  126M  1.7G   7% /boot
tmpfs                              796M  4.0K  796M   1% /run/user/0
root@jenkins:~# 

root@jenkins:~# lsblk
NAME                      MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
fd0                         2:0    1     4K  0 disk 
loop0                       7:0    0  63.3M  1 loop /snap/core20/1822
loop1                       7:1    0  63.3M  1 loop /snap/core20/1828
loop2                       7:2    0  79.9M  1 loop /snap/lxd/22923
loop3                       7:3    0 111.9M  1 loop /snap/lxd/24322
loop4                       7:4    0  49.8M  1 loop /snap/snapd/17950
loop5                       7:5    0  49.8M  1 loop /snap/snapd/18357
sda                         8:0    0   100G  0 disk 
├─sda1                      8:1    0     1M  0 part 
├─sda2                      8:2    0     2G  0 part /boot
└─sda3                      8:3    0    98G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0    98G  0 lvm  /
sr0                        11:0    1  1024M  0 rom  
root@jenkins:~# 
root@jenkins:~#
```

