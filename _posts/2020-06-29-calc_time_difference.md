---
layout:     post
title:      "统计两个时间的时间差"
subtitle:   "Calc time difference"
date:       2020-06-28
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
tags:
    - python
---


# 概述

最近在跑cosbench，由于OS根分区空间满，导致cosbench任务失败，误删了一部分cosbench archive记录，但controller html页面还是能展示这部分数据记录的片段信息，比如任务的提交时间，起始时间与结束时间，而每个cosbench 任务写数据的总量可以从定义的xml中获取到，需要手动计算一下起止时间差，统计总量/时间差，就可以得到这轮任务的平均写速度了。

本文介绍通过script计算前后两个时间差，每次都记不住，这次写下来，避免每次都去查资料重新写script。



# 脚本内容

参考如下：


```python
root@node244:~/75# cat timestamp_calc.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from __future__ import unicode_literals

import sys
from datetime import datetime

if len(sys.argv) == 3:
    start = datetime.strptime(sys.argv[1], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(sys.argv[2], '%Y-%m-%d %H:%M:%S')
    print (end-start).seconds
else:
    print "\nUsage: %s start_time end_time" % sys.argv[0]
    print "  e.g: %s '2020-06-28 09:18:59' '2020-06-28 10:00:33' \n" % sys.argv[0]
    sys.exit(2)

root@node244:~/75#
```


# 运行效果

```shell
root@node244:~/75# python timestamp_calc.py '2020-06-28 10:49:18' '2020-06-28 11:22:53'
2015
root@node244:~/75# 
```

