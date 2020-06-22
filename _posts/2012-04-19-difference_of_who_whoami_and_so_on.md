---
layout:     post
title:      "who与whoami与who an i与w的区别"
subtitle:   "Difference of who, whoami, who am i and w"
date:       2012-04-19
author:     "Gavin"
catalog:    true
tags:
    - Megacli
---



# 概述

本文介绍who， w， whoami 和 who am i的区别


# 实际输出

当前是root用户：

```
root@node77:~# w
 18:20:21 up  7:57,  3 users,  load average: 1.06, 1.51, 1.82
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    1.6.72.76        10:28    4.00s  1.89s  0.02s w
root     pts/1    10.10.10.76      15:27    2:30m  0.09s  0.09s -bash
root     pts/2    172.17.74.95     18:13    6:21   0.09s  0.09s -bash
root@node77:~# 
root@node77:~# 
root@node77:~# 
root@node77:~# who
root     pts/0        2012-04-19 10:28 (1.6.72.76)
root     pts/1        2012-04-19 15:27 (10.10.10.76)
root     pts/2        2012-04-19 18:13 (172.17.74.95)
root@node77:~# 
root@node77:~# who am i
root     pts/0        2012-04-19 10:28 (1.6.72.76)
root@node77:~# 
root@node77:~# 
root@node77:~# whoami
root
```

切换到test01用户：

```
root@node77:~# su - test01
test01@node77:~$ who am i
root     pts/0        2012-04-19 10:28 (1.6.72.76)
test01@node77:~$ 
test01@node77:~$ whoami
test01
test01@node77:~$
```


# 具体区别

w:         Show who is logged on and what they are doing
who:       Show who is logged on
whoami:    Print effective userid(EUID)
who am i： Print effective userid(UID), even use sudo to switch users

