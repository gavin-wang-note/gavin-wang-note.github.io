---
layout:     post
title:      "使用edac工具来检测服务器内存故障"
subtitle:   "Use edac to check memory"
date:       2022-06-08
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - edac
---




# 概述



随着虚拟化，Redis,BDB内存数据库等应用的普及，现在越来越多的服务器配置了大容量内存，拿DELL的R620来说在配置双路CPU下，其24个内存插槽，支持的内存高达960GB。对于ECC,REG这些带有纠错功能的内存故障检测是一件很头疼的事情，出现故障，还是可以连续运行几个月甚至几年，但如果运气不好，随时都会挂掉，好在linux中提供了一个edac-utils 内存纠错诊断工具，可以用来检查服务器内存潜在的故障。



# 实战



下面以CentOS为例，介绍下edac-utils 工具的使用。



在使用edac-utils 工具之前，需要先了解服务器的硬件架构，以DELL R620为例，(其它如HP DL360P G8，IBM X3650 M4 机型都使用了 E5-2600 系列CPU，C600 系列芯片组.大致相同)  其CPU内存控制器对应通道，内存槽关系，如下所示。

```
处理器0 (对应一个内存控制器)
通道0：内存插槽A1、A5 和A9
通道1：内存插槽A2、A6 和A10
通道2：内存插槽A3、A7 和A11
通道3：内存插槽A4、A8 和A12

处理器1 (对应一个内存控制器)
通道0：内存插槽B1、B5 和B9
通道1：内存插槽B2、B6 和B10
通道2：内存插槽B3、B7 和B11
通道3：内存插槽B4、B8 和B12
```


## 安装 edac-utils 工具

```
yum install -y libsysfs edac-utils
```





## 行检测命令，可查看纠错提示如下



```
[root@dbhost ~]# edac-util -v
mc0: 0 Uncorrected Errors with no DIMM info
mc0: 0 Corrected Errors with no DIMM info
mc0: csrow0: 0 Uncorrected Errors
mc0: csrow0: CPU_SrcID#0_Channel#0_DIMM#0: 6312 Corrected Errors    A1槽
mc0: csrow1: 0 Uncorrected Errors
mc0: csrow1: CPU_SrcID#0_Channel#0_DIMM#1: 0 Corrected Errors         A5槽
mc0: csrow2: 0 Uncorrected Errors
mc0: csrow2: CPU_SrcID#0_Channel#1_DIMM#0: 0 Corrected Errors         A2槽
mc0: csrow3: 0 Uncorrected Errors
mc0: csrow3: CPU_SrcID#0_Channel#1_DIMM#1: 0 Corrected Errors         A6槽
mc0: csrow4: 0 Uncorrected Errors
mc0: csrow4: CPU_SrcID#0_Channel#2_DIMM#0: 0 Corrected Errors         A3槽
mc0: csrow5: 0 Uncorrected Errors
mc0: csrow5: CPU_SrcID#0_Channel#2_DIMM#1: 0 Corrected Errors         A7槽
mc0: csrow6: 0 Uncorrected Errors
mc0: csrow6: CPU_SrcID#0_Channel#3_DIMM#0: 0 Corrected Errors         A4槽
mc1: 0 Uncorrected Errors with no DIMM info
mc1: 0 Corrected Errors with no DIMM info
mc1: csrow0: 0 Uncorrected Errors
mc1: csrow0: CPU_SrcID#1_Channel#0_DIMM#0: 6459 Corrected Errors     B1槽
mc1: csrow1: 0 Uncorrected Errors
mc1: csrow1: CPU_SrcID#1_Channel#0_DIMM#1: 0 Corrected Errors          B5槽
mc1: csrow2: 0 Uncorrected Errors
mc1: csrow2: CPU_SrcID#1_Channel#1_DIMM#0: 0 Corrected Errors          B2槽
mc1: csrow3: 0 Uncorrected Errors
mc1: csrow3: CPU_SrcID#1_Channel#1_DIMM#1: 0 Corrected Errors          B6槽
mc1: csrow4: 0 Uncorrected Errors
mc1: csrow4: CPU_SrcID#1_Channel#2_DIMM#0: 535 Corrected Errors       B3槽
mc1: csrow5: 0 Uncorrected Errors
mc1: csrow5: CPU_SrcID#1_Channel#2_DIMM#1: 0 Corrected Errors          B7槽
mc1: csrow6: 0 Uncorrected Errors
mc1: csrow6: CPU_SrcID#1_Channel#3_DIMM#0: 0 Corrected Errors          B4槽
[root@dbhost ~]#
```

其中 mc0 表示 表示内存控制器0,  CPU_Src_ID#0表示源CPU0 , Channel#0 表示通道0
DIMM#0 标示内存槽0，Corrected Errors 代表已经纠错的次数，根据前面列出的CPU通
道和内存槽对应关系即可给edac-utils 返回的信息进行编号。
即可得出 A1槽 6312 次纠错，B1槽 6459次纠错，B3槽 535次纠错. 3条内存出现潜在故障，接下来联系供应商进行更换即可。



如果没有侦测到错误，显示信息如下：

```
[root@node163 ~]# edac-util -v
mc0: 0 Uncorrected Errors with no DIMM info
mc0: 0 Corrected Errors with no DIMM info
mc0: csrow0: 0 Uncorrected Errors
mc0: csrow0: mc#0memory#0: 0 Corrected Errors
mc0: csrow10: 0 Uncorrected Errors
mc0: csrow10: mc#0memory#10: 0 Corrected Errors
mc0: csrow12: 0 Uncorrected Errors
mc0: csrow12: mc#0memory#12: 0 Corrected Errors
mc0: csrow14: 0 Uncorrected Errors
mc0: csrow14: mc#0memory#14: 0 Corrected Errors
mc0: csrow2: 0 Uncorrected Errors
mc0: csrow2: mc#0memory#2: 0 Corrected Errors
mc0: csrow4: 0 Uncorrected Errors
mc0: csrow4: mc#0memory#4: 0 Corrected Errors
mc0: csrow6: 0 Uncorrected Errors
mc0: csrow6: mc#0memory#6: 0 Corrected Errors
mc0: csrow8: 0 Uncorrected Errors
mc0: csrow8: mc#0memory#8: 0 Corrected Errors
mc1: 0 Uncorrected Errors with no DIMM info
mc1: 0 Corrected Errors with no DIMM info
edac-util: No errors to report.
[root@node163 ~]# 
```
