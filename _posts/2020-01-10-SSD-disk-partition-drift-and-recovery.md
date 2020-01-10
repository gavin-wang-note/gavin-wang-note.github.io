---
layout:     post
title:      "SSD盘符漂移导致OSD down场景模拟与恢复"
subtitle:   "SSD disk partition drift and how to recovery it"
date:       2020-01-10
author:     "Gavin"
catalog:    true
tags:
    - ceph
---


# 前言

运维团队反馈一个问题，现象是：

某个OSD对应的cache分区发生了变化，比如原来cache使用的分区是/dev/sde,后来还是这块盘，但分区信息不知何故，变成了/dev/sdf（产品OSD设备并不是根据分区名称来map，而是根据partlabel），最终的现象是这个OSD down了，没法启动.
接到这个现象的反馈后，记录一下这个问题在lab的复现方法。

# 准备工作

## Step1. OSD data盘做RAID5

## Step2. 重新将SSD make as JBOD

在Step1结束后，将在RAID卡上的SSD设置为JBOD

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpSetProp -EnableJBOD -1 -aALL```

## Step3. 创建集群，正常启用OSD，对应osd要选择SSD作为cache

如下为node245上的data与cache 大致的map关系：

```
root@node245:~# lsblk
NAME                      MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda                         8:0    0 447.1G  0 disk 
├─sda1                      8:1    0     8G  0 part 
├─sda2                      8:2    0 439.1G  0 part 
│ ├─g-osd1-0-cache (dm-0) 252:0    0 380.4G  0 dm   /data/cache/g-osd1-0
│ ├─g-osd1-0-ext4m (dm-1) 252:1    0  58.5G  0 dm   
│ │ └─g-osd1-0 (dm-2)     252:2    0  14.6T  0 dm   /data/osd.0
│ └─g-osd1-0-ext4j (dm-3) 252:3    0   256M  0 dm   
└─sda3                      8:3    0  1007K  0 part 
sdb                         8:16   0 447.1G  0 disk 
├─sdb1                      8:17   0     8G  0 part 
├─sdb2                      8:18   0 439.1G  0 part 
│ ├─g-osd2-0-cache (dm-4) 252:4    0   395G  0 dm   /data/cache/g-osd2-0
│ ├─g-osd2-0-ext4m (dm-5) 252:5    0  43.9G  0 dm   
│ │ └─g-osd2-0 (dm-6)     252:6    0    11T  0 dm   /data/osd.1
│ └─g-osd2-0-ext4j (dm-7) 252:7    0   256M  0 dm   
└─sdb3                      8:19   0  1007K  0 part 
sdc                         8:32   0  14.6T  0 disk 
└─sdc1                      8:33   0  14.6T  0 part 
  └─g-osd1-0 (dm-2)       252:2    0  14.6T  0 dm   /data/osd.0
sdd                         8:48   0  10.9T  0 disk 
└─sdd1                      8:49   0  10.9T  0 part 
  └─g-osd2-0 (dm-6)       252:6    0    11T  0 dm   /data/osd.1
sde                         8:64   0 278.9G  0 disk 
├─sde1                      8:65   0   7.6M  0 part 
├─sde2                      8:66   0  95.4G  0 part /
├─sde3                      8:67   0  26.7G  0 part [SWAP]
└─sde4                      8:68   0 156.8G  0 part 
root@node245:~#
```

# 问题复现

说明：

* 本文示例的SSD为E:S为[9:1]，对应的分区信息是sdb， 对应的osd id是1

## Step1. 确认好SSD所在的盘位，直接从设备上拔掉，紧接着再插回去

重新拔插回去的SSD，此时节点的lsblk吐出信息是：

```
root@node245:~# lsblk
NAME                      MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda                         8:0    0 447.1G  0 disk 
├─sda1                      8:1    0     8G  0 part 
├─sda2                      8:2    0 439.1G  0 part 
│ ├─g-osd1-0-cache (dm-0) 252:0    0 380.4G  0 dm   /data/cache/g-osd1-0
│ ├─g-osd1-0-ext4m (dm-1) 252:1    0  58.5G  0 dm   
│ │ └─g-osd1-0 (dm-2)     252:2    0  14.6T  0 dm   /data/osd.0
│ └─g-osd1-0-ext4j (dm-3) 252:3    0   256M  0 dm   
└─sda3                      8:3    0  1007K  0 part 
sdc                         8:32   0  14.6T  0 disk 
└─sdc1                      8:33   0  14.6T  0 part 
  └─g-osd1-0 (dm-2)       252:2    0  14.6T  0 dm   /data/osd.0
sdd                         8:48   0  10.9T  0 disk 
└─sdd1                      8:49   0  10.9T  0 part 
  └─g-osd2-0 (dm-6)       252:6    0    11T  0 dm   /data/osd.1
sde                         8:64   0 278.9G  0 disk 
├─sde1                      8:65   0   7.6M  0 part 
├─sde2                      8:66   0  95.4G  0 part /
├─sde3                      8:67   0  26.7G  0 part [SWAP]
└─sde4                      8:68   0 156.8G  0 part 
sdf                         8:80   0 447.1G  0 disk 
├─sdf1                      8:81   0     8G  0 part 
├─sdf2                      8:82   0 439.1G  0 part 
└─sdf3                      8:83   0  1007K  0 part 
root@node245:~# 
```

此时，发现sdb已经不见了，出现了新的分区sdf：

```
root@node245:~# gdisk /dev/sdf
GPT fdisk (gdisk) version 0.8.8

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): 

Command (? for help): p
Disk /dev/sdf: 937703088 sectors, 447.1 GiB
Logical sector size: 512 bytes
Disk identifier (GUID): 7CB4C196-1B82-4190-B044-C11E96294A62
Partition table holds up to 128 entries
First usable sector is 34, last usable sector is 937703054
Partitions will be aligned on 8-sector boundaries
Total free space is 1679 sectors (839.5 KiB)

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048        16779263   8.0 GiB     8300  **g-osd2-0-journal**
   2        16779264       937701375   439.1 GiB   8300  **g-osd2-0-ssd**
   3              34            2047   1007.0 KiB  8300  

Command (? for help): 
```

可以看出，sdf分区的partlabel就是之前的名称（g-osd2-0-journal && g-osd2-0-ssd），只是分区信息发生了变化。
虽然不知道现场是如何发生分区突然名称更换（也许是被人为触碰，也许是被插拔，也是是其他原因，总之root cause不确定），但是碰到这种情况，如何恢复环境，先恢复业务，解决客户投诉燃眉之急，然后再来查找root cause或针对产品进行改进、优化，能够更好的适配类似问题的发生，使得能够自动恢复，减少人为干预。

## Step2. 将插拔回去的SSD make为JBOD

在Step1里，盘插回去后，这块盘的状态是unconfig good，需要make as JBOD

```/opt/MegaRAID/MegaCli/MegaCli64 -PDMakeJBOD -PhysDrv[9:1] -a0 ```

## Step3. 确认当前dm信息

```
root@node245:~# mount
/dev/sde2 on / type ext4 (rw,errors=remount-ro)
proc on /proc type proc (rw,noexec,nosuid,nodev)
sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)
none on /sys/fs/cgroup type tmpfs (rw)
none on /sys/fs/fuse/connections type fusectl (rw)
none on /sys/kernel/debug type debugfs (rw)
none on /sys/kernel/security type securityfs (rw)
udev on /dev type devtmpfs (rw,mode=0755)
devpts on /dev/pts type devpts (rw,noexec,nosuid,gid=5,mode=0620)
tmpfs on /run type tmpfs (rw,noexec,nosuid,size=10%,mode=0755)
none on /run/lock type tmpfs (rw,noexec,nosuid,nodev,size=5242880)
none on /run/shm type tmpfs (rw,nosuid,nodev)
none on /run/user type tmpfs (rw,noexec,nosuid,nodev,size=104857600,mode=0755)
none on /sys/fs/pstore type pstore (rw)
rpc_pipefs on /run/rpc_pipefs type rpc_pipefs (rw)
systemd on /sys/fs/cgroup/systemd type cgroup (rw,noexec,nosuid,nodev,none,name=systemd)
/dev/mapper/g-osd1-0 on /data/osd.0 type ext4 (rw,noatime,nodelalloc,journal_path=/dev/mapper/g-osd1-0-ext4j)
/dev/mapper/g-osd1-0-cache on /data/cache/g-osd1-0 type ext4 (rw,noatime,nodelalloc)
/dev/mapper/g-osd2-0 on /data/osd.1 type ext4 (rw,noatime,nodelalloc,journal_path=/dev/mapper/g-osd2-0-ext4j)
/dev/mapper/g-osd2-0-cache on /data/cache/g-osd2-0 type ext4 (rw,noatime,nodelalloc)
1.1.1.245,1.1.1.244,1.1.1.243:/ on /var/share/ezfs type ceph (wsize=4194304,mount_timeout=15,noshare,mds_namespace=1)
root@node245:~# dmsetup status
g-osd2-0-ext4m: 0 92012544 linear 
g-osd2-0-cache: 0 828385280 linear 
g-osd2-0-ext4j: 0 524288 linear 
g-osd1-0: 0 31374440415 ext4meta 
g-osd2-0: 0 23530829791 ext4meta 
g-osd1-0-ext4m: 0 122683392 linear 
g-osd1-0-cache: 0 797714432 linear 
g-osd1-0-ext4j: 0 524288 linear 
root@node245:~# 
```

这里发现，g-osd2-0对应的ext4m，ext4j之类的信息依然存在于dm设备中

##Step4.  接触dm设备里map关系

```
root@node245:~# umount /dev/mapper/g-osd2-0-cache
root@node245:~# dmsetup remove g-osd2-0-cache
root@node245:~# umount /data/osd.1
root@node245:~# dmsetup remove g-osd2-0
root@node245:~# dmsetup remove g-osd2-0-ext4m
root@node245:~# dmsetup remove g-osd2-0-ext4j
root@node245:~# dmsetup table
g-osd1-0: 0 31374440415 ext4meta SSD:252:1 HDD:8:33
g-osd1-0-ext4m: 0 122683392 linear 8:2 797714432
g-osd1-0-cache: 0 797714432 linear 8:2 0
g-osd1-0-ext4j: 0 524288 linear 8:2 920397824
root@node245:~# 
```

## Step5.  重新挂载dm设备

```
root@node245:~# bt-mount.py 
root@node245:~# 
root@node245:~# 
root@node245:~# 
root@node245:~# lsblk
NAME                      MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda                         8:0    0 447.1G  0 disk 
├─sda1                      8:1    0     8G  0 part 
├─sda2                      8:2    0 439.1G  0 part 
│ ├─g-osd1-0-cache (dm-0) 252:0    0 380.4G  0 dm   /data/cache/g-osd1-0
│ ├─g-osd1-0-ext4m (dm-1) 252:1    0  58.5G  0 dm   
│ │ └─g-osd1-0 (dm-2)     252:2    0  14.6T  0 dm   /data/osd.0
│ └─g-osd1-0-ext4j (dm-3) 252:3    0   256M  0 dm   
└─sda3                      8:3    0  1007K  0 part 
sdc                         8:32   0  14.6T  0 disk 
└─sdc1                      8:33   0  14.6T  0 part 
  └─g-osd1-0 (dm-2)       252:2    0  14.6T  0 dm   /data/osd.0
sdd                         8:48   0  10.9T  0 disk 
└─sdd1                      8:49   0  10.9T  0 part 
  └─g-osd2-0 (dm-6)       252:6    0    11T  0 dm   /data/osd.1
sde                         8:64   0 278.9G  0 disk 
├─sde1                      8:65   0   7.6M  0 part 
├─sde2                      8:66   0  95.4G  0 part /
├─sde3                      8:67   0  26.7G  0 part [SWAP]
└─sde4                      8:68   0 156.8G  0 part 
sdf                         8:80   0 447.1G  0 disk 
├─sdf1                      8:81   0     8G  0 part 
├─sdf2                      8:82   0 439.1G  0 part 
│ ├─g-osd2-0-cache (dm-4) 252:4    0   395G  0 dm   /data/cache/g-osd2-0
│ ├─g-osd2-0-ext4m (dm-5) 252:5    0  43.9G  0 dm   
│ │ └─g-osd2-0 (dm-6)     252:6    0    11T  0 dm   /data/osd.1
│ └─g-osd2-0-ext4j (dm-7) 252:7    0   256M  0 dm   
└─sdf3                      8:83   0  1007K  0 part 
root@node245:~# 
root@node245:~# 
root@node245:~# mount
/dev/sde2 on / type ext4 (rw,errors=remount-ro)
proc on /proc type proc (rw,noexec,nosuid,nodev)
sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)
none on /sys/fs/cgroup type tmpfs (rw)
none on /sys/fs/fuse/connections type fusectl (rw)
none on /sys/kernel/debug type debugfs (rw)
none on /sys/kernel/security type securityfs (rw)
udev on /dev type devtmpfs (rw,mode=0755)
devpts on /dev/pts type devpts (rw,noexec,nosuid,gid=5,mode=0620)
tmpfs on /run type tmpfs (rw,noexec,nosuid,size=10%,mode=0755)
none on /run/lock type tmpfs (rw,noexec,nosuid,nodev,size=5242880)
none on /run/shm type tmpfs (rw,nosuid,nodev)
none on /run/user type tmpfs (rw,noexec,nosuid,nodev,size=104857600,mode=0755)
none on /sys/fs/pstore type pstore (rw)
rpc_pipefs on /run/rpc_pipefs type rpc_pipefs (rw)
systemd on /sys/fs/cgroup/systemd type cgroup (rw,noexec,nosuid,nodev,none,name=systemd)
/dev/mapper/g-osd1-0 on /data/osd.0 type ext4 (rw,noatime,nodelalloc,journal_path=/dev/mapper/g-osd1-0-ext4j)
/dev/mapper/g-osd1-0-cache on /data/cache/g-osd1-0 type ext4 (rw,noatime,nodelalloc)
1.1.1.245,1.1.1.244,1.1.1.243:/ on /var/share/ezfs type ceph (wsize=4194304,mount_timeout=15,noshare,mds_namespace=1)
/dev/mapper/g-osd2-0 on /data/osd.1 type ext4 (rw,noatime,nodelalloc,journal_path=/dev/mapper/g-osd2-0-ext4j)
/dev/mapper/g-osd2-0-cache on /data/cache/g-osd2-0 type ext4 (rw,noatime,nodelalloc)
root@node245:~# root@node245:~# umount /dev/mapper/g-osd2-0-cache
ode245:~# dmsetup remove g-osd2-0-ext4j
root@node245:~# dmsetup table
g-osd1-0: 0 31374440415 ext4meta SSD:252:1 HDD:8:33
g-osd1-0-ext4m: 0 122683392 linear 8:2 797714432
g-osd1-0-cache: 0 797714432 linear 8:2 0
g-osd1-0-ext4j: 0 524288 linear 8:2 920397824
root@node245:~# 
```

说明：
* 经过上面的操作，对应dm map关系恢复，mount point也在

## Step6.  启动OSD
```
root@node245:~# /etc/init.d/ceph start osd.1
=== osd.1 === 
Starting Ceph osd.1 on 1.1.1.245...
starting osd.1 at :/0 osd_data /data/osd.1 /dev/disk/by-partlabel/g-osd2-0-journal
root@node245:~# 

```

