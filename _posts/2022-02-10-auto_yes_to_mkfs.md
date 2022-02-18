---
layout:     post
title:      "自动化交互式格式化文件系统"
subtitle:   "Auto format FS by expect"
date:       2022-02-10
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

#  概述

当格式化文件系统时，尤其是在脚本或代码中做这个操作，一旦出现需要输入'y'的时候，脚本或者代码就会卡住或者timeout，造成程序失败。

本文介绍几种方法，在format时自动填写yes or y，让format持续进行下去.



# 实践


## 方法1

```yes | mkfs.ext4 /dev/sdb```


## 方法2

```echo -e "y\n" | mkfs.ext4 /dev/sdx```

## 方法3

```mkfs.ext4 -F /dev/sdb```


