---
layout:     post
title:      "将megaraid卡磁盘改为JBOD模式"
subtitle:   "Enable JBOD for megacli RAID Card"
date:       2019-09-29
author:     "Gavin"
catalog:    true
tags:
    - JBOD
---


# 前言

目前lab里HDD基本上都是通过LSI RAID卡做RAID来使用，但有些时候也想测试单盘，但不想做RAID0，于是需要启用JBOD模式来识别每一块单盘。

megaraid 卡使用 JBOD 模式，磁盘可以直接被系统识别，使用 smartctl 查看 SMART 信息（smartcl -d megaraid,N <device> 参数查看做过RAID磁盘的 SMART 信息）和 直连 SAS 卡一样。

如果 LSI megaraid 卡没有启用JBOD模式，磁盘必须做RAID操作，才能被系统识别到 。

没有启动JBOD模式，没法使用megacli设置磁盘为JBOD 。


# 查看 JBOD 是否启用

```
root@node244:~# /opt/MegaRAID/MegaCli/MegaCli64 -AdpGetProp -enablejbod -aALL
                                     
Adapter 0: JBOD: Enabled

Exit Code: 0x00
root@node244:~# 
```

```Enabled ``` 表明已经启用了JBOD模式；如果没有开启，先启用该特性：

```
root@node244:~# /opt/MegaRAID/MegaCli/MegaCli64 -h
......
......
MegaCli -AdpSetProp -EnableJBOD -val -aN|-a0,1,2|-aALL 
       val - 0=Disable JBOD mode. 
             1=Enable JBOD mode.

root@node244:~# /opt/MegaRAID/MegaCli/MegaCli64 -AdpSetProp -EnableJBOD -1 -aALL
                                     
Adapter 0: Set JBOD to Enable success.

Exit Code: 0x00
root@node244:~# 

```


# 将对应盘设置为JBOD

```
root@node244:~# /opt/MegaRAID/MegaCli/MegaCli64 -PDMakeJBOD -PhysDrv[E:S] -aALL
```

如果想批量设置，类似如下：

```
for i in {0..11}; do /opt/MegaRAID/MegaCli/MegaCli64 -PDMakeJBOD -PhysDrv[E:${i}] -aALL; done
```

注意要替换掉E，这里的E就是 ```Enclosure Device ID```；0..11是值disk的Slot Number

对于```Enclosure Device ID``` 和 ```Slot Number ```,可以通过```/opt/MegaRAID/MegaCli/MegaCli64 pdlist aall ```进行获取:

```
root@node244:~# /opt/MegaRAID/MegaCli/MegaCli64 pdlist aall | grep -Ei "Enclosure Device ID|Slot Number"
Enclosure Device ID: 9
Slot Number: 0
Enclosure Device ID: 9
Slot Number: 1
Enclosure Device ID: 9
Slot Number: 2
Enclosure Device ID: 9
Slot Number: 3
Enclosure Device ID: 9
Slot Number: 4
Enclosure Device ID: 9
Slot Number: 5
Enclosure Device ID: 9
Slot Number: 6
Enclosure Device ID: 9
Slot Number: 7
Enclosure Device ID: 9
Slot Number: 8
Enclosure Device ID: 9
Slot Number: 9
Enclosure Device ID: 9
Slot Number: 10
Enclosure Device ID: 9
Slot Number: 11
root@node244:~# 
```

# 查看盘是否被设置为JBOD模式

```
root@node244:~# /opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL -Nolog|grep '^Firm'
Firmware state: Online, Spun Up
Firmware state: JBOD
Firmware state: JBOD
Firmware state: Online, Spun Up
Firmware state: Unconfigured(bad)
Firmware state: Online, Spun Up
Firmware state: Online, Spun Up
Firmware state: Online, Spun Up
Firmware state: Online, Spun Up
Firmware state: Online, Spun Up
Firmware state: Online, Spun Up
Firmware state: Online, Spun Up
root@node244:~# 
```

说明：
* Unconfigured(bad) 是一块坏盘
* Online, Spun Up 的是RAID组成员，做了RAID，因为当前环境是先创建了RAID5，然后对剩下的盘做的JBOD模式
