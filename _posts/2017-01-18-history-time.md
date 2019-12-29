---
layout:     post
title:      "History命令打印时间"
subtitle:   "Record time in out put ot history"
date:       2017-01-18
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 前言

排查问题的时候，可能需要追踪出现问题的原因，尤其是怀疑有误操作或者受到攻击的时候，history命令只会展示出命令本身。

# 方法

vim /etc/bash.bashrc 添加如下信息：

```HISTTIMEFORMAT="%Y-%m-%d-%H:%M:%S: " ```

重新登录后，执行history结果如下：

```
  409  2017-01-18-11:50:55: cp b c
  410  2017-01-18-11:50:55: ceph df
  411  2017-01-18-11:51:01: history
  412  2017-01-18-11:52:24: strace -e trace=file history
  413  2017-01-18-11:53:02: which history
```

