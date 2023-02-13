---
layout:     post
title:      "Linux stat家族之vmstat"
subtitle:   "Linux vmstat"
date:       2023-01-19
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

* Virtual Meomory Statistics，报告虚拟内存统计信息
* 统计进程信息、内存、交换区、IO、磁盘、CPU 等数据
 

# vmstat主要能看什么性能指标

均是 Linux 系统级别

* 运行状态、不可中断睡眠状态的进程数量
* 内存、交换区、I/O、CPU 信息
* 上下文切换次数、中断次数
* 磁盘 I/O 的详细信息和概要信息
 

# 语法格式

```
[root@node81 ~]# vmstat -h

Usage:
 vmstat [options] [delay [count]]

Options:
 -a, --active           active/inactive memory
 -f, --forks            number of forks since boot
 -m, --slabs            slabinfo
 -n, --one-header       do not redisplay header
 -s, --stats            event counter statistics
 -d, --disk             disk statistics
 -D, --disk-sum         summarize disk statistics
 -p, --partition <dev>  partition specific statistics
 -S, --unit <char>      define display unit
 -w, --wide             wide output
 -t, --timestamp        show timestamp

 -h, --help     display this help and exit
 -V, --version  output version information and exit

For more details see vmstat(8).
```

* options：命令行参数，可选
* delay：间隔多久统计一次数据，可选
* count：统计一次，可选

注意:
  若只传了 delay，则统计次数是无限次，结束统计后会打印本次所有数据的平均值.
 

## 示例

```vmstat 1 ```

每隔 1s 统计打印一次数据，统计无限次



```vmstat 2 5 ```

每隔 2s 统计打印一次数据，共统计 5 次

 

# 命令行参数

| 简  写  | 完整写法           | 是否需要指定一个值  | 作用                                                                                       |
| ------- | ------------------ | ------------------- | ------------------------------------------------------------------------------------------ |
| -a      | --active           |  F                  |  显示活动和非活动内存                                                                      |
| -n      | --one-header       |  F                  |  仅显示一次标题，而不是定期显示                                                            |
| -s      | --stats            |  F                  |  获取内存、CPU、swap、中断次数、上下文切换次数等信息                                       |
| -d      | --disk             |  F                  |  获取磁盘的读写详细信息                                                                    |
| -D      | --disk-sum         |  F                  |  获取磁盘的一些摘要信息                                                                    |
| -P      | --partition device |  T (Device)         |  有关分区的详细统计信息                                                                    |
| -S      | --unit character   |  T (character)      |  输出数值的单位，charactr取值:k,K,m or M(Default is K),k:1000;K:1024;m:1000000;M:1048576   |
| -t      | --timestamp        |  F                  |  加一列，显示当前时间                                                                      |
| -V      | --version          |  F                  |  显示版本信息                                                                              |
| -h      | --help             |  F                  |  帮助信息                                                                                  |



# 统计数据的字段说明 

```
[root@node81 ~]# vmstat 2 2
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 3549024 309900 938184    0    0    47    23  246  293  1  1 98  0  0
 2  0      0 3501380 309908 938184    0    0     0    30 3602 3698  1  6 93  0  0
[root@node81 ~]# 
```

共有 6 个模块

 

## procs：进程状态


| 字段 | 字段说明                       |
| ---- | ------------------------------ |
| r    | 处于 Runnable状态的进程数量    |
| b    | 处于不可中断睡眠状态的进程数量 |
 

## memory：内存信息


| 字段   | 字段说明           |
| ------ | ------------------ |
| swpd   | 已用虚拟内存       |
| free   | 空闲内存           |
| buff   | 用于缓冲区的内存   |
| cache  | 用于缓存的内存     |
| inact  | 不活动的内存量(-a) |
| active | 活动的内存量(-a)   |
 
 

## swap：交换区


| 字段 | 字段说明                       |
| ---- | ------------------------------ |
| si   | 每秒从交换区写到内存的大小     |
| so   | 每秒写入交换区的内存大小       |
 
 

## io：io 读写信息

现在的Linux版本块的大小为1024bytes


| 字段 | 字段说明        |
| ---- | --------------- |
| bi   | 每秒读取的块数  |
| bo   | 每秒写入的块数  |

 

## system：系统信息


| 字段 | 字段说明                  |
| ---- | ------------------------- |
| in   | 每秒中断数，包括时钟中断  |
| cs   | 每秒上下文切换次数        |

 

## CPU：CPU 详细信息

这些是总 CPU 时间的百分比


| 字段 | 字段说明                 |
| ---- | ------------------------ |
| us   | 用户态进程的CPU使用率    |
| sy   | 内核态进程的CPU使用率    |
| id   | 空闲CPU百分比            |
| wa   | 等待IO的CPU使用率        |
| st   | 从虚拟机偷取的CPU百分比  |

 

# 数据来源

主要来自这三个文件:

```
/proc/meminfo
/proc/stat
/proc/*/stat
```


```
[root@node81 ~]# vmstat
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 3379916 312036 942032    0    0    43    21  246  294  1  1 98  0  0
[root@node81 ~]# vmstat 1 2
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 3376784 312060 942032    0    0    43    21  246  294  1  1 98  0  0
 0  0      0 3376712 312060 942040    0    0     0     0 1082 1554  0  0 100  0  0
[root@node81 ~]# 
```

上面这些信息主要来自 /proc/stat 

 

```
[root@node81 ~]# vmstat -s
     12295904 K total memory
      7668944 K used memory
      7718024 K active memory
       457556 K inactive memory
      3372716 K free memory
       312164 K buffer memory
       942080 K swap cache
      6161404 K total swap
            0 K used swap
      6161404 K free swap
        50128 non-nice user cpu ticks
           22 nice user cpu ticks
        86934 system cpu ticks
      7102823 idle cpu ticks
        25004 IO-wait cpu ticks
            0 IRQ cpu ticks
         3045 softirq cpu ticks
            0 stolen cpu ticks
      3105928 pages paged in
      1531600 pages paged out
            0 pages swapped in
            0 pages swapped out
     17847205 interrupts
     21369346 CPU context switches
   1674110880 boot time
        92634 forks
[root@node81 ~]# 
```

上面这些信息的分别来自于 /proc/meminfo 、 /proc/stat 和 /proc/vmstat 

 

```
[root@node81 ~]# vmstat -d
disk- ------------reads------------ ------------writes----------- -----IO------
       total merged sectors      ms  total merged sectors      ms    cur    sec
fd0        0      0       0       0      0      0       0       0      0      0
sda    25592    955 1207050   96572  16120  31009  665696  290943      0     60
sdb    65035   1359 3634310  342617  59749 236139 2398312 7186627      0    110
sr0       18      0    2056      41      0      0       0       0      0      0
sdc      267      0    3888     359      0      0       0       0      0      0
sdd      512      0   16360     901      0      0       0       0      0      0
sde      832      0 1314536   11707      0      0       0       0      0      6
sdf      469      0   14288     692      0      0       0       0      0      0
sdg      267      0    3888     356      0      0       0       0      0      0
sdh      267      0    3888     399      0      0       0       0      0      0
sdi      267      0    3888     402      0      0       0       0      0      0
sdj      267      0    3888     355      0      0       0       0      0      0
sdk      267      0    3888     317      0      0       0       0      0      0
dm-0     162      0    8328     238      0      0       0       0      0      0
dm-1     205      0   10400     481      0      0       0       0      0      0
dm-2     525      0 1308576   11293      0      0       0       0      0      5
[root@node81 ~]# 
```

上面这些信息主要来自于 /proc/diskstats 

 

# 其他用法

## 打印活动内存和不活动内存量


```
[root@node81 ~]# vmstat -a 1 2
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free  inact active   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 3351248 457672 7736448    0    0    42    21  246  294  1  1 98  0  0
 0  0      0 3349100 457676 7738260    0    0     0    32 1482 1945  1  0 99  0  0
[root@node81 ~]# 
```

这里有 'inact' & 'active'关键字。
 

## 以 MB 单位输出结果


```
[root@node81 ~]# vmstat -S M 1 2
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0   3259    305    920    0    0    42    21  246  294  1  1 98  0  0
 1  0      0   3259    305    920    0    0     0     0 1445 1936  0  0 99  0  0
[root@node81 ~]# 
```


## 以 MB 单位输出各事件计数器和内存的统计信息

```
[root@node81 ~]# vmstat -s -S M
        12007 M total memory
         7527 M used memory
         7570 M active memory
          447 M inactive memory
         3254 M free memory
          305 M buffer memory
          920 M swap cache
         6016 M total swap
            0 M used swap
         6016 M free swap
        50984 non-nice user cpu ticks
           22 nice user cpu ticks
        88723 system cpu ticks
      7244100 idle cpu ticks
        25046 IO-wait cpu ticks
            0 IRQ cpu ticks
         3074 softirq cpu ticks
            0 stolen cpu ticks
      3106216 pages paged in
      1534792 pages paged out
            0 pages swapped in
            0 pages swapped out
     18194132 interrupts
     21812846 CPU context switches
   1674110880 boot time
        93251 forks
[root@node81 ~]#
```



# 注意事项

* vmstat 不需要特殊权限
* vmstat 报告旨在帮助确定系统瓶颈，所以它不会将自己视为正在运行的进程
* 当前所有的 Linux 块都是 1024 字节， 旧内核可能报告的块为 512 字节，2048 字节或 4096 字节

