---
layout:     post
title:      "iSCSI多路径配置"
subtitle:   "Config iSCSI multipath"
date:       2019-12-27
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - iSCSI
---

# 概述

配置iSCSI多路径，可以增加HA（高可用性）

本文以Ubuntu 14.04为示例，在安装了multipath-tools工具后，以此节点作为client去挂载iSCSI设备，将multipath默认active-standy修改为rond-robing


# iSCSI多路径配置（client端）

## 未设置多路径之前

```
root@host245:~# multipath -ll
2ea63c7c4f3aa5c5d dm-0 Bigtera ,VirtualStor_Scal
size=10T features='0' hwhandler='0' wp=rw
|-+- policy='round-robin 0' prio=1 status=active
| `- 11:0:0:0 sdd 8:48  active ready running
|-+- policy='round-robin 0' prio=1 status=enabled
| `- 14:0:0:0 sdg 8:96  active ready running
|-+- policy='round-robin 0' prio=1 status=enabled
| `- 15:0:0:0 sdh 8:112 active ready running
|-+- policy='round-robin 0' prio=1 status=enabled
| `- 13:0:0:0 sdf 8:80  active ready running
`-+- policy='round-robin 0' prio=1 status=enabled
  `- 12:0:0:0 sde 8:64  active ready running
```

## 修改multipath.conf 

```
root@host245:~# cat /etc/multipath.conf 
blacklist {
        devnode "^(rbd)[0-9]*"
        devnode "^zd[0-0]*"
#       devnode "*"
}

defaults {
        getuid_callout  "/lib/udev/scsi_id --whitelisted --replace-whitespace --device=/dev/%n"
        path_grouping_policy  multibus
        path_selector         "round-robin 0"
        failback               immediate
        rr_min_io_req          32
}
root@host245:~# 
```

说明：

从path_grouping_policy开始，之后的4行为新增内容

## 重启multipath-tool

```
root@host245:~# /etc/init.d/multipath-tools restart
```

## 查看设置后效果

```
root@host245:~# multipath -ll
2ea63c7c4f3aa5c5d dm-0 Bigtera ,VirtualStor_Scal
size=10T features='0' hwhandler='0' wp=rw
`-+- policy='round-robin 0' prio=1 status=active
  |- 11:0:0:0 sdd 8:48  active ready running
  |- 12:0:0:0 sde 8:64  active ready running
  |- 13:0:0:0 sdf 8:80  active ready running
  |- 14:0:0:0 sdg 8:96  active ready running
  `- 15:0:0:0 sdh 8:112 active ready running
root@host245:~# 
```

## 确认sdX与iSCSI target关系

现在是多路径了，如何分别出sdX对应哪个iSCSI target呢？

比如下面的sdf

```
root@host243:~# lsblk
NAME                       MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
sda                          8:0    0  14.6T  0 disk  
├─sda1                       8:1    0     8G  0 part  
└─sda2                       8:2    0  14.6T  0 part  /data/osd.2
sdb                          8:16   0 278.9G  0 disk  
├─sdb1                       8:17   0   7.5M  0 part  
├─sdb2                       8:18   0  95.4G  0 part  /
├─sdb3                       8:19   0  26.7G  0 part  [SWAP]
└─sdb4                       8:20   0 156.8G  0 part  
sdc                          8:32   0  10.9T  0 disk  
└─sdc1                       8:33   0  10.9T  0 part  
sdd                          8:48   0     5T  0 disk  
└─26a53c128cb536936 (dm-0) 252:0    0     5T  0 mpath 
sde                          8:64   0     5T  0 disk  
└─26a53c128cb536936 (dm-0) 252:0    0     5T  0 mpath 
sdf                          8:80   0     5T  0 disk  
└─26a53c128cb536936 (dm-0) 252:0    0     5T  0 mpath 
sdg                          8:96   0     5T  0 disk  
└─26a53c128cb536936 (dm-0) 252:0    0     5T  0 mpath 
sdh                          8:112  0     5T  0 disk  
└─26a53c128cb536936 (dm-0) 252:0    0     5T  0 mpath
```

方法如下：

step1、先获取 Host Number

```
root@host243:~# multipath -ll
26a53c128cb536936 dm-0 Bigtera ,VirtualStor_Scal
size=5.0T features='0' hwhandler='0' wp=rw
`-+- policy='round-robin 0' prio=1 status=active
  |- 39:0:0:0 sdf 8:80  active ready running
  |- 38:0:0:0 sdh 8:112 active ready running
  |- 40:0:0:0 sdg 8:96  active ready running
  |- 37:0:0:0 sde 8:64  active ready running
  `- 36:0:0:0 sdd 8:48  active ready running
```

如上文所示， ```39:0:0:0```， 这里的39，就是Host Number， 同理，下面的38,40,37,36都是Host Number，分别对应不同的sdX分区

step2、根据Host Number，确认连接到哪个target

```
root@host243:~# iscsiadm -m session -P 3
iSCSI Transport Class version 2.0-870
version 2.0-873
Target: iqn.2019-12.com:lenove
	Current Portal: 10.16.172.109:3260,1
	Persistent Portal: 10.16.172.109:3260,1
		**********
		Interface:
		**********
		Iface Name: default
		Iface Transport: tcp
		Iface Initiatorname: iqn.1993-08.org.debian:01:f077d70d498
		Iface IPaddress: 10.16.172.243
		Iface HWaddress: <empty>
		Iface Netdev: <empty>
		SID: 10
		iSCSI Connection State: LOGGED IN
		iSCSI Session State: LOGGED_IN
		Internal iscsid Session State: NO CHANGE
		*********
		Timeouts:
		*********
		Recovery Timeout: 120
		Target Reset Timeout: 30
		LUN Reset Timeout: 30
		Abort Timeout: 15
		*****
		CHAP:
		*****
		username: <empty>
		password: ********
		username_in: <empty>
		password_in: ********
		************************
		Negotiated iSCSI params:
		************************
		HeaderDigest: None
		DataDigest: None
		MaxRecvDataSegmentLength: 262144
		MaxXmitDataSegmentLength: 1048576
		FirstBurstLength: 262144
		MaxBurstLength: 1048576
		ImmediateData: Yes
		InitialR2T: No
		MaxOutstandingR2T: 1
		************************
		Attached SCSI devices:
		************************
		Host Number: 40	State: running
		scsi40 Channel 00 Id 0 Lun: 0
			Attached scsi disk sdg		State: running
	Current Portal: 10.16.172.105:3260,1
	Persistent Portal: 10.16.172.105:3260,1
		**********
		Interface:
		**********
		Iface Name: default
		Iface Transport: tcp
		Iface Initiatorname: iqn.1993-08.org.debian:01:f077d70d498
		Iface IPaddress: 10.16.172.243
		Iface HWaddress: <empty>
		Iface Netdev: <empty>
		SID: 6
		iSCSI Connection State: LOGGED IN
		iSCSI Session State: LOGGED_IN
		Internal iscsid Session State: NO CHANGE
		*********
		Timeouts:
		*********
		Recovery Timeout: 120
		Target Reset Timeout: 30
		LUN Reset Timeout: 30
		Abort Timeout: 15
		*****
		CHAP:
		*****
		username: <empty>
		password: ********
		username_in: <empty>
		password_in: ********
		************************
		Negotiated iSCSI params:
		************************
		HeaderDigest: None
		DataDigest: None
		MaxRecvDataSegmentLength: 262144
		MaxXmitDataSegmentLength: 1048576
		FirstBurstLength: 262144
		MaxBurstLength: 1048576
		ImmediateData: Yes
		InitialR2T: No
		MaxOutstandingR2T: 1
		************************
		Attached SCSI devices:
		************************
		Host Number: 36	State: running
		scsi36 Channel 00 Id 0 Lun: 0
			Attached scsi disk sdd		State: running
	Current Portal: 10.16.172.107:3260,1
	Persistent Portal: 10.16.172.107:3260,1
		**********
		Interface:
		**********
		Iface Name: default
		Iface Transport: tcp
		Iface Initiatorname: iqn.1993-08.org.debian:01:f077d70d498
		Iface IPaddress: 10.16.172.243
		Iface HWaddress: <empty>
		Iface Netdev: <empty>
		SID: 7
		iSCSI Connection State: LOGGED IN
		iSCSI Session State: LOGGED_IN
		Internal iscsid Session State: NO CHANGE
		*********
		Timeouts:
		*********
		Recovery Timeout: 120
		Target Reset Timeout: 30
		LUN Reset Timeout: 30
		Abort Timeout: 15
		*****
		CHAP:
		*****
		username: <empty>
		password: ********
		username_in: <empty>
		password_in: ********
		************************
		Negotiated iSCSI params:
		************************
		HeaderDigest: None
		DataDigest: None
		MaxRecvDataSegmentLength: 262144
		MaxXmitDataSegmentLength: 1048576
		FirstBurstLength: 262144
		MaxBurstLength: 1048576
		ImmediateData: Yes
		InitialR2T: No
		MaxOutstandingR2T: 1
		************************
		Attached SCSI devices:
		************************
		Host Number: 37	State: running
		scsi37 Channel 00 Id 0 Lun: 0
			Attached scsi disk sde		State: running
	Current Portal: 10.16.172.108:3260,1
	Persistent Portal: 10.16.172.108:3260,1
		**********
		Interface:
		**********
		Iface Name: default
		Iface Transport: tcp
		Iface Initiatorname: iqn.1993-08.org.debian:01:f077d70d498
		Iface IPaddress: 10.16.172.243
		Iface HWaddress: <empty>
		Iface Netdev: <empty>
		SID: 8
		iSCSI Connection State: LOGGED IN
		iSCSI Session State: LOGGED_IN
		Internal iscsid Session State: NO CHANGE
		*********
		Timeouts:
		*********
		Recovery Timeout: 120
		Target Reset Timeout: 30
		LUN Reset Timeout: 30
		Abort Timeout: 15
		*****
		CHAP:
		*****
		username: <empty>
		password: ********
		username_in: <empty>
		password_in: ********
		************************
		Negotiated iSCSI params:
		************************
		HeaderDigest: None
		DataDigest: None
		MaxRecvDataSegmentLength: 262144
		MaxXmitDataSegmentLength: 1048576
		FirstBurstLength: 262144
		MaxBurstLength: 1048576
		ImmediateData: Yes
		InitialR2T: No
		MaxOutstandingR2T: 1
		************************
		Attached SCSI devices:
		************************
		Host Number: 38	State: running
		scsi38 Channel 00 Id 0 Lun: 0
			Attached scsi disk sdh		State: running
	Current Portal: 10.16.172.106:3260,1
	Persistent Portal: 10.16.172.106:3260,1
		**********
		Interface:
		**********
		Iface Name: default
		Iface Transport: tcp
		Iface Initiatorname: iqn.1993-08.org.debian:01:f077d70d498
		Iface IPaddress: 10.16.172.243
		Iface HWaddress: <empty>
		Iface Netdev: <empty>
		SID: 9
		iSCSI Connection State: LOGGED IN
		iSCSI Session State: LOGGED_IN
		Internal iscsid Session State: NO CHANGE
		*********
		Timeouts:
		*********
		Recovery Timeout: 120
		Target Reset Timeout: 30
		LUN Reset Timeout: 30
		Abort Timeout: 15
		*****
		CHAP:
		*****
		username: <empty>
		password: ********
		username_in: <empty>
		password_in: ********
		************************
		Negotiated iSCSI params:
		************************
		HeaderDigest: None
		DataDigest: None
		MaxRecvDataSegmentLength: 262144
		MaxXmitDataSegmentLength: 1048576
		FirstBurstLength: 262144
		MaxBurstLength: 1048576
		ImmediateData: Yes
		InitialR2T: No
		MaxOutstandingR2T: 1
		************************
		Attached SCSI devices:
		************************
		Host Number: 39	State: running
		scsi39 Channel 00 Id 0 Lun: 0
			Attached scsi disk sdf		State: running
```

比如上文中的 ```Persistent Portal: 10.16.172.106:3260,1 ```，对应的Host Number是39(```Host Number: 39 State: running ```)，对应的分区信息是sdf(```Attached scsi disk sdf          State: running ```)，说明访问sdf这个device，是通过10.16.172.106 这个IP进行访问的。

