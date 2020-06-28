---
layout:     post
title:      "Megacli详解"
subtitle:   "Megacli Guide"
date:       2020-05-06
author:     "Gavin"
catalog:    true
tags:
    - Megacli
---



# 概述

通常，我们使用的DELL/HP/IBM三家的机架式PC级服务器阵列卡是从LSI的卡OEM出来的，DELL和IBM两家的阵列卡原生程度较高， 没有做太多封装，可以用原厂提供的阵列卡管理工具进行监控；而HP的阵列卡一般都做过封装了，因此需要使用自身特有的管理工具来监控。
本文以几种常用的阵列卡为例，展示其阵列卡及硬盘监控的方法。

DELL SAS 6/iR卡，全称LSI Logic SAS1068E，只支持RAID 0, RAID 1, RAID 1+0, 不支持RAID 5等高级RAID特性，不支持阵列卡电池。
DELL PERC PERC H700卡，全称LSI Logic MegaRAID SAS 2108，支持各种RAID级别及高级特性，可选配阵列卡电池。
DELL PERC H310 Mini卡 ，全称LSI Logic / Symbios Logic MegaRAID SAS 2008，支持常见RAID级别，不支持高级RAID特性，不支持阵列卡电池。
IBM ServeRAID M5014 SAS/SATA Controller卡，全称LSI Logic / Symbios Logic MegaRAID SAS 2108，支持各种RAID级别及高级特性，可选配阵列卡电池。
IBM ServeRAID-MR10i SAS/SATA Controller卡，全称LSI Logic / Symbios Logic MegaRAID SAS 1078，支持常见RAID级别，不支持高级RAID特性，可选配阵列卡电池，这个卡其实和DELL的PERC 6/i卡是一样的，都是基于LSI MegaRAID SAS 1078基础上OEM出来的。

上面是几种常见的阵列卡型号，更多的可以自行查看官方的技术手册。
下面我们要继续的是，这些阵列卡以及硬盘如何监控，阵列卡的管理也请查看官方技术手册，不在本文讨论范畴。
一般地，支持RAID 5的卡，我们称其为阵列卡，都可以使用LSI官方提供的MegaCli工具来管理，而不支持RAID 5的卡，我们称其为SAS卡，使用lsiutil工具来管理。HP的服务器使用其特有的hpacucli工具来管理。



# 工具概述



## **MegaCli工具**

### MegaCli -adpallinfo -aall — 查看阵列卡信息

-a 参数指定阵列卡的编号，一般服务器上只会配一个阵列卡，因此我们通常指定为 -a0（阵列卡适配器编号，从0开始） 即可，主要关注下面几个信息：

 

| **状态值**                     | **对应含义**                                                 |
| ------------------------------ | ------------------------------------------------------------ |
| Product Name : PERC  H710 Mini | 阵列卡名称                                                   |
| FW Package Build:  21.2.0-0007 | 阵列卡firmware版本号，版本如果太低，建议升级以提高稳定性及性能 |
| BBU : Present                  | 是否有配BBU电池                                              |



### MegaCli -cfgdsply -aall — 查看阵列配置

 

| **状态值**                                                   | **对应含义**                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Memory: 512MB                                                | 阵列卡cache大小，2的N次方，如果不是，说明阵列卡有异常        |
| Number of dedicated  Hotspares: 0                            | 阵列是否有专用/独享热备盘（如果有多个逻辑磁盘组/disk group，则可以指定一个硬盘用于全局热备，那么该disk group上的专用热备盘数量为0也不用担心），除了RAID  1/RAID 1+0一般不指定热备盘以外，其他几个阵列级别建议都要指定热备盘 |
| State : Optimal                                              | 阵列状态，如果不是 Optimal 就要关注了                        |
| Current Cache  Policy: WriteBack, ReadAheadNone, Direct, Write Cache OK if Bad BBU | 阵列读写cache策略，建议写策略设置为FORCE WB，最起码是WB，预读策略可以关掉，意义不大，几乎没影响 |
| Disk Cache Policy :  Disabled                                | 硬盘cache策略，建议关闭，防止意外时数据丢失                  |
| Current Power  Savings Policy: None                          | 节电策略，建议关闭                                           |
| Media Error Count:  0                                        | 三个错误计数器，任何一个值大于100就要立刻引起关注，尤其要关注起增长速度。1T以上SATA盘，计数值不够精确，可能所有盘上该值都会大于0，一般重启就会重新清0，如果重启后还是大于0的话，赶紧报修吧。SAS盘的计数值则比较准确。 |
| Other Error Count:  0                                        |                                                              |
| Predictive Failure  Count: 0                                 |                                                              |
| Firmware state:  Online, Spun Up                             | 查看硬盘状态，如果是unconfigured表示该硬盘未分配加入到阵列中；如果是  unconfigured(bad)表示该盘不但是未分配，而且还坏了，正是“出师未捷身先死”；如果是failed，表示该盘故障无法识别；如果是  rebuilding，表示该盘正在重建数据 |



### MegaCli -adpbbucmd -aall — 查看阵列卡电池信息

 

| **状态值**                                 | **对应含义**                                                 |
| ------------------------------------------ | ------------------------------------------------------------ |
| Temperature: 39 C                          | 查看电池温度，如果相比上一次查看高出不少，就需要关注了，或者可以根据经验设置一个基线值 |
| Battery State:  Optimal                    | 电池状态，如果不是为Optimal，就需要关注了                    |
| Charger Status:  Complete                  | 电池充放电状态                                               |
| isSOHGood: Yes                             | 电池状态，如果不是为Yes，需要关注                            |
| Relative State of  Charge: 93 %            | 当前电量，当电量低于15%，或者电池坏掉时，默认都会将写策略从WB改成WT，除非设定为FORCE WB策略 |
| Max Error = 0 %                            | 电池是否有错误信息                                           |
| Next Learn time:  Tue Oct 14 22:06:50 2014 | 电池充放电时间，注意这是美国时间。另外，新的阵列卡电池很多改成电容式的了，也就不需要重复充放电了 |





## lsiutil工具

lsiutil有交互和非交互两种方式，作为监控，我们肯定选择非交互模式。想要使用交互模式的，可以根据非交互模式自行练习。



### lsiutil -p 1 -a 20,12,0,0 — 查看硬盘计数器

Invalid DWord Count 2,563 — 任何一个值大于0，都需要引起关注

Running Disparity Error Count 2,366

Loss of DWord Synch Count 0

Phy Reset Problem Count 0



###  lsiutil -p 1 -a 21,1,0,0,0 — 查看逻辑卷状态

 

| **状态值**                                | **对应含义**   |
| ----------------------------------------- | -------------- |
| Volume State:  optimal, enabled           | 逻辑卷健康状况 |
| Volume draws from  Hot Spare Pools: 0     | 是否有热备     |
| Volume Size 139392  MB, 2 Members         | 由几块硬盘组成 |
| Primary is PhysDisk  1 (Bus 0 Target 9)   | 物理硬盘1      |
| Secondary is  PhysDisk 0 (Bus 0 Target 3) | 物理硬盘0      |



### lsiutil -p 1 -a 21,2,0,0,0 — 查看物理硬盘状态

 

| **状态值**                                                   | **对应含义**                          |
| ------------------------------------------------------------ | ------------------------------------- |
| PhysDisk 0 is Bus 0  Target 3                                | 编号                                  |
| PhysDisk State:  online                                      | 状态                                  |
| Error Count 13,  Last Error: Command = 28h, Key = 3, ASC/ASCQ = 11h/00h | 错误计数器，大于0的话，就需要引起关注 |



## hpacucli工具

hpacucli工具查看阵列、硬盘、电池信息，其实就只要一条指令：

**hpacucli ctrl all show config detail — 查看阵列详细信息、配置**

| **状态值**                                            | **对应含义**                                                 |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| Controller Status:  OK                                | 阵列卡状态                                                   |
| Firmware Version:  1.18                               | firmware版本，太低了建议升级，以提高稳定性及性能             |
| Cache Board  Present: True                            | 是否配备了cache模块                                          |
| Cache Status: OK                                      | cache模块状态                                                |
| Cache Ratio: 100%  Read / 0% Write                    | cache策略，此处只有读cache，不用于写cache，因为没有bbu电池，见下方结果 |
| Drive Write Cache:  Disabled                          | 关闭磁盘cache                                                |
| Total Cache Size:  256 MB                             | cache大小                                                    |
| Total Cache Memory  Available: 208 MB                 | 实际可用cache大小，和理论cache大小不一样，说明cache模块可能有问题 |
| No-Battery Write  Cache: Disabled                     | 关闭FORCEWB策略                                              |
| Battery/Capacitor  Count: 0                           | 阵列卡BBU电池数量为0，也就是没有BBU模块                      |
| Battery/Capacitor  Status: Failed (Replace Batteries) | 阵列卡BBU电池状态，这里显示是错误状态，需要及时更换          |
| Array: A                                              | 第一个乌列阵列，编号从A开始，依次是A、B、C                   |
| Status: OK                                            | 物理阵列状态                                                 |
| Logical Drive: 1                                      | 第一个逻辑卷，编号从1开始                                    |
| Fault Tolerance:  RAID 5                              | 第一个逻辑卷的阵列级别                                       |
| Status: OK                                            | 第一个逻辑卷状态                                             |
| Caching: Enabled                                      | 第一个逻辑卷是否启用了cache策略                              |
| physicaldrive  1I:1:1                                 | 第一块物理硬盘，编号从1开始                                  |
| Status: OK                                            | 第一块物理硬盘状态                                           |
| Firmware Revision:  HPDA                              | 第一块物理硬盘firmware，如果太低，也需要及时升级，HP的硬盘每个批次都有不同的firmware |





# Megacli实践



## 查看有风险的盘



```/opt/MegaRAID/MegaCli/MegaCli64 -LDPDinfo -A0 |grep "Device Id" |awk '{print $3}' |xargs -I {} smartctl -a -d megaraid,{} /dev/sdc |grep -Ei "^187|^188|^197|^198|Reallocated_Sector_Ct" | xargs -I{} echo {} ```

 

## 查看磁盘的smart信息



如果磁盘在RAID卡上：

（1）先获取磁盘的device id

```/opt/MegaRAID/MegaCli/MegaCli64 PDList aall ```

这里的输出，会有ES信息，同时还会有device id

 

（2）根据device id，查询smart信息

 ```smartctl -a -d megaraid,11 /dev/sdc ```

 

这里的11就是磁盘的device id，哪怕后面的/dev/sdc不存在，获取是这颗磁盘不属于sdc，也能输出正确的信息，只要device id是正确的就行。



如果不在RAID卡上，直接```smartctl -a /dev/sdc ```



## 手工配置初始化

```
/opt/MegaRAID/MegaCli/MegaCli64 -LDInit -start –L0 -a0         # 快速初始化

/opt/MegaRAID/MegaCli/MegaCli64 -LDInit -start -full –L0 -a0     # 完全初始化

/opt/MegaRAID/MegaCli/MegaCli64 -LDInit -progdsply -L0 -a0      # 显示初始化的进度

/opt/MegaRAID/MegaCli/MegaCli64 -LDInit -abort -L0 -a0        # 结束完全初始化

/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -Abort -LALL -aALL # 忽略初始化

/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -ProgDsply -LALL -aALL
```



## 设置RAID cache

```
/opt/MegaRAID/MegaCli/MegaCli64 -ldinfo -l1 -a0

/opt/MegaRAID/MegaCli/MegaCli64 -ldsetprop cached -l1 -a0

/opt/MegaRAID/MegaCli/MegaCli64 -ldinfo -l1 -a0

```



## 显示Rebuid进度

```/opt/MegaRAID/MegaCli/MegaCli64 -PDRbld -ShowProg -physdrv[20:2] -aALL ```



## 查看E S

```/opt/MegaRAID/MegaCli/MegaCli64 -PDList -aAll -NoLog | grep -Ei "(enclosure|slot)" ```



## 查看所有硬盘的状态

```/opt/MegaRAID/MegaCli/MegaCli64 -PDList -aAll -NoLog  ```

如果有热备，则 Firmware State会显示为hotspace



## 查看copyback进度



```/opt/MegaRAID/MegaCli/MegaCli64 -PDCpyBk -ShowProg -PhysDrv[33:3] -a0 ```

## 查看所有Virtual Disk的状态



```/opt/MegaRAID/MegaCli/MegaCli64 -LdPdInfo -aAll -NoLog```

RAID Level对应关系：

```
RAID Level : Primary-1, Secondary-0, RAID Level Qualifier-0	RAID 1
RAID Level : Primary-0, Secondary-0, RAID Level Qualifier-0	RAID 0
RAID Level : Primary-5, Secondary-0, RAID Level Qualifier-3	RAID 5
RAID Level : Primary-1, Secondary-3, RAID Level Qualifier-0	RAID 10

```



## 在线做Raid

```
/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r0 [0:11] WB NORA Direct CachedBadBBU -strpsz64 -a0 -NoLog
/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r5 [12:2,12:3,12:4,12:5,12:6,12:7] WB Direct -a0 
```

## 让硬盘LED灯闪烁（定位）

```
    1、  MegaCli  -AdpSetProp UseDiskActivityforLocate -1 -a0 
    2、  MegaCli  -PdLocate  -start  –physdrv[E:S]  -a0  让硬盘LED灯闪烁
    3、  MegaCli  -PdLocate  -stopt  –physdrv[E:S]  -a0 停掉硬盘LED灯
```

## 清除Foreign状态

```/opt/MegaRAID/MegaCli/MegaCli64 -CfgForeign -Clear -a0 ```

## 查看RAID阵列中掉线的盘

```/opt/MegaRAID/MegaCli/MegaCli64 -pdgetmissing -a0 ```

## 替换坏掉的模块

```/opt/MegaRAID/MegaCli/MegaCli64 -pdreplacemissing -physdrv[12:10] -Array5 -row0 -a0 ```

## 手动开启rebuid

```/opt/MegaRAID/MegaCli/MegaCli64 -pdrbld -start -physdrv[12:10] -a0 ```



## 设置HotSpare


```
/opt/MegaRAID/MegaCli/MegaCli64 -pdhsp -set [-Dedicated [-Array2]] [-EnclAffinity] [-nonRevertible] -PhysDrv[4:11] -a0
/opt/MegaRAID/MegaCli/MegaCli64 -pdhsp -set [-EnclAffinity] [-nonRevertible] -PhysDrv[32：1}] -a0
```



## 关闭Rebuild

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpAutoRbld -Dsbl -a0 ```



## 设置rebuild的速率

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpSetProp RebuildRate -30 -a0 ```



## 查看RAID组成员

```/opt/MegaRAID/MegaCli/MegaCli64  -LdPdInfo -aAll ```



## 强制修改RAID卡由write through到write back 方法



```opt/MegaRAID/MegaCli/MegaCli64 -LDSetProp CachedBadBBU -Lall -aALL ```

一般在没有BBU情况下， 要执行如下命令进行修改：

```
/opt/MegaRAID/MegaCli/MegaCli64 -ldsetprop WB -lall -aall;

/opt/MegaRAID/MegaCli/MegaCli64 -LDSetProp CachedBadBBU -Lall -aALL;

/opt/MegaRAID/MegaCli/MegaCli64 ldinfo lall aall
```



## 查raid卡信息 

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL ```



##  查看电池信息

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -aAll ```

## 查看raid卡日志

```/opt/MegaRAID/MegaCli/MegaCli64 -FwTermLog -Dsply -aALL ```



## 显示适配器个数

```/opt/MegaRAID/MegaCli/MegaCli64 -adpCount ```



## 显示适配器时间 

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpGetTime –aALL ```



## 显示所有适配器信息 

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aAll ```



## 显示所有逻辑磁盘组信息

```/opt/MegaRAID/MegaCli/MegaCli64 -LDInfo -LALL -aAll  ```



## 显示所有的物理信息 

```/opt/MegaRAID/MegaCli/MegaCli64 -PDList -aAll ```



## 查看充电状态

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuStatus -aALL |grep 'Charger Status' ```



## 显示BBU状态信息

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuStatus -aALL ```



## 显示BBU容量信息

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuCapacityInfo -aALL ```



## 显示BBU设计参数

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuDesignInfo -aALL ```



## 显示当前BBU属性

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuProperties -aALL```



## 显示Raid卡型号，Raid设置，Disk相关信息

```/opt/MegaRAID/MegaCli/MegaCli64-cfgdsply -aALL ```



## 磁盘状态的变化，从拔盘，到插盘的过程中

Device             : Normal --> Damage --> Rebuild --> Normal

Virtual Drive      : Optimal --> Degraded --> Degraded --> Optimal

Physical Drive     : Online --> Failed Unconfigured --> Rebuild --> Online



## 查看物理磁盘状态

```/opt/MegaRAID/MegaCli/MegaCli64 -PDRbld -ShowProg -PhysDrv [Enclosure Device ID:Slot Number] -a0```

Rebuild 中的物理磁盘状态中会显示："Firmware state: Rebuild"



## 以文本进度条样式显示 Rebuild 进度

```/opt/MegaRAID/MegaCli/MegaCli64-pdrbld -progdsply -physdrv[E:S] -aALL ```

屏幕显示类似下面的内容：

```
Rebuild progress of physical drives...
Enclosure:Slot         Percent Complete           Time Elps
     032 :05   #######################87 %################*******  01:59:07

```



## 查看 RAID 卡 Rebuild 参数

```/opt/MegaRAID/MegaCli/MegaCli64-AdpAllinfo -aALL | grep -i rebuild ```

返回结果类似下面这样

```
Rebuild Rate                             : 30%
Auto Rebuild                             : Enabled
Rebuild Rate                             : Yes
Force Rebuild                            : Yes
```

## 设置 RAID 卡 Rebuild 比例为60%

```/opt/MegaRAID/MegaCli/MegaCli64-AdpSetProp { RebuildRate -60} -aALL ```



## 删除全局热备

```/opt/MegaRAID/MegaCli/MegaCli64-PDHSP -Rmv -PhysDrv[E:S] -a0 ```



## 将物理盘下线和上线

```/opt/MegaRAID/MegaCli/MegaCli64 -PDOffline/Online -PhysDrv [E:S] -a0 ```

## 在线添加磁盘

```/opt/MegaRAID/MegaCli/MegaCli64-LDRecon -Start -r5 -Add -PhysDrv[E:S] -L1 -a0```



## 删除阵列

```/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdDel -L1 -a0 ```

## 查看磁盘缓存策略

```/opt/MegaRAID/MegaCli/MegaCli64-LDGetProp -DskCache -LALL -aALL ```

or 

```/opt/MegaRAID/MegaCli/MegaCli64 -LDGetProp -Cache -LALL -aALL```



## 查看raid卡event log

```/opt/MegaRAID/MegaCli/MegaCli64 -AdpEventLog -GetEvents -f event.log -A0 ```

## 查看Megacli的log

```/opt/MegaRAID/MegaCli/MegaCli64 -fwtermlog -dsply -aALL``` ，关注里面的error/fail/warn等多个关键字


## 查看raid卡时间 



```/opt/MegaRAID/MegaCli/MegaCli64 -AdpGetTime -A0 ; date ```


## Stop 一致性检查

```/opt/MegaRAID/MegaCli/MegaCli64 -LDCC -stop -lall -aall ```



# 参考文档

```https://kamaok.org.ua/?p=2507 ```

