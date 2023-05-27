---
layout:     post
title:      "blocktrace跟踪磁盘"
subtitle:   "Monitor disk by blocktrace"
date:       2023-01-30
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

通过blocktrace命令，跟踪磁盘，获取磁盘的D2C，C2C信息，判断磁盘IO响应时延分布状况，进而判断磁盘是否出现了硬件瓶颈

# 示例

```
blktrace -d /dev/sdX -o - |blkparse -i -
```
