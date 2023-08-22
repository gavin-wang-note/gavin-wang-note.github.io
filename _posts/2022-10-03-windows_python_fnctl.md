---
layout:     post
title:      "Windows下python fnctl"
subtitle:   "python fnctl under Windows OS"
date:       2022-10-03
author:     "Gavin"
catalog:    true
tags:
    - python
---


# 概述


fcntl函数是linux下的一个文件锁函数，用以加密文件，给文件上锁，防止文件同时被多个进程操作。但是在windows下执行时发现并没有这个函数，不支持，所以就去找了各种方法来代替。


# 解决方法

有位网友，借助 pywin32 来解决这个问题， 参考链接：https://www.jianshu.com/p/4a0fa333c562

本文介绍另外一种方法，直接将linux下fnctl.py文件，放在python安装路径下的lib目录下，如我的环境： C:\Python27\Lib\ 下。

# fnctl.py文件内容

```
F_GETFD = 0
F_SETFD = 0
FD_CLOEXEC = 0
LOCK_EX = 1
LOCK_UN = 0

def fcntl(fd, op, arg=0):
    return 0


def ioctl(fd, op, arg=0, mutable_flag=True):
    if mutable_flag:
        return 0
    else:
        return ""


def flock(fd, op):
    return


def lockf(fd, operation, length=0, start=0, whence=0):
    return
```


如上文件内容做记录保留下来，防止哪天OS损坏，有地方可以找到。

