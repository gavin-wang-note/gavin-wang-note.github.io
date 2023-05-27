---
layout:     post
title:      "开启kernel debug"
subtitle:   "Open Kernel Debug"
date:       2019-07-04
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

有时候需要查看更详细的kernel堆栈信息，本文介绍如何开启kernel debug。

# 实践 

```
echo 'module ceph +p' > /sys/kernel/debug/dynamic_debug/control
echo 'module libceph +p' > /sys/kernel/debug/dynamic_debug/control
```
