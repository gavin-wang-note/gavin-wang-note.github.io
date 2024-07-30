---
layout:     post
title:      "EXT3/4 FS 长度"
subtitle:   "Lenth of EXT3/4"
date:       2017-04-20
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---

# 概述

本文介绍如何测试出EXT3/4 文件系统的长度上限。

# 脚本

```shell
LENTH=`for i in {1..255};do for x in a;do echo -n $x;done;done`
touch $LENTH
```

当增加到256时，touch报错，File name too long

linux系统下ext3文件系统内给文件/目录命名，最长只能支持127个中文字符，英文则可以支持255个字符
