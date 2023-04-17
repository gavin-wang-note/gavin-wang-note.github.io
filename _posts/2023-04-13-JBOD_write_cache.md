---
layout:     post
title:      "查看JBOD Write Cache Policy"
subtitle:   "JBOD Write Cache Policy"
date:       2023-04-13
author:     "Gavin"
catalog:    true
tags:
    - JBOD
---

# 概述

在在验证JBOD启用Write Cache时，服务器强制掉电是否出现文件系统错误，需要先检查JBOD是否启用了Write Cache。
故本文介绍查看JBOD Write Policy，至于服务器掉电是否引发文件系统错误的验证，参考我同事的一篇文章：
https://bean-li.github.io/check-hardware-data-loss


# 实践

## 显示JBOD Write Cache信息

```
root@node216:~# hdparm -W /dev/sdj

/dev/sdj:
 write-caching =  1 (on)
root@node216:~# hdparm -W 0 /dev/sdj

/dev/sdj:
 setting drive write-caching to 0 (off)
 write-caching =  0 (off)
root@node216:~# hdparm -W 1 /dev/sdj

/dev/sdj:
 setting drive write-caching to 1 (on)
 write-caching =  1 (on)
root@node216:~#
```


## 显示硬盘的相关设置

```
hdparm /dev/sda
/dev/sda:
IO_support = 0 (default 16-bit)
readonly = 0 (off)
readahead = 256 (on)
geometry = 19457［柱面数］/255［磁头数］/63［扇区数］, sectors = 312581808［总扇区数］, start = 0［起始扇区数］
```

## 显示硬盘的柱面、磁头、扇区数

```
hdparm -g /dev/sda
/dev/sda:
geometry = 19457［柱面数］/255［磁头数］/63［扇区数］, sectors = 312581808［总扇区数］, start = 0［起始扇区数］
```

## 测试硬盘的读取速度

```
hdparm -T /dev/sda
/dev/sda:
 Timing cached reads:   4684 MB in  2.00 seconds = 2342.92 MB/sec
```

## 测试硬盘缓存的读取速度

```
hdparm -T /dev/xvda
/dev/xvda:
Timing cached reads: 11154 MB in 1.98 seconds = 5633.44 MB/sec
```

## 检测硬盘的电源管理模式

```
hdparm -C /dev/sda
/dev/sda:
drive state is: standby [省电模式]
```

## 查询并设置硬盘多重扇区存取的扇区数，以增进硬盘的存取效率

```
hdparm -m /dev/sda
hdparm -m    #参数值为整数值如8 /dev/sda
```

## 附：硬盘坏道修复方法

```
检查：smartctl -l selftest /dev/sda
卸载：umount /dev/sda*
修复：badblocks /dev/sda
```

