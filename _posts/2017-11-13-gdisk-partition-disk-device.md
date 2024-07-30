---
layout:     post
title:      "gdisk分区"
subtitle:   "gdisk to partition disk device"
date:       2017-11-13
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [gdisk]
tags:
    - Linux
    - gdisk
---

# 引言

对磁盘分区除了使用parted，还可以使用gdisk工具，不过gdisk只支持GPT格式的分区表，不过目前来说已经很少用到MBR了（由于其有2T的size限制）。

# 操作示例

需求1： 将sdb分成三个区，第一个分区是32G，第二个分区也是32G，剩下的是第三个分区

步骤：

```shell
  gdisk /dev/sdb
  > o (y)     # 重建GPT分区表
  > n         # 分第一个分区，分区序号都使用默认即可，选择合适的开始扇区和结束扇区，这里结束扇区用+{offset}表示
  > <Enter>
  > 1M
  > +32G
  > <Enter>
  > n         # 分第二个分区，在选择起始扇区时默认是紧接着上个分区
  > <Enter>
  > <Enter>
  > +32G
  > <Enter>
  > n         # 分第三个分区时都使用默认即可
  > <Enter>
  > <Enter>
  > <Enter>
  > <Enter>
  > w (y)     # 最后别忘了要写入才能生效
```

需求2： 删除第二个分区，将第三个分区的分区名改为osd-data

步骤：

```shell
gdisk /dev/sdb
> d         # 删除分区
> 2
> c         # 修改分区名
> 3
> osd-data
> w (y)
```

# 非交互式

顺便介绍另一个工具sgdisk，相较于gdisk，它不需要交互式配置，只需要把所有参数一次给齐，因此更适合脚本使用。

比如上述示例如果用sgdisk，只需要如下两行代码：

```shell
sgdisk -Z /dev/sdb # 清空分区表 
sgdisk /dev/sdb -n 1:1M:+32G -n 2:0:+32G -N 3
```

提示

对于MPIO的场景，使用parted分区会和multipath有冲突，有可能导致OSD建立失败，因此墙裂建议使用GPT分区。

