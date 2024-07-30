---
layout:     post
title:      "UID与EUID区别"
subtitle:   "Difference of UID and EUID"
date:       2012-03-22
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - UID
    - EUID
---


# 概述

Linux系统中每个进程都有2个ID，分别为用户ID（UID）和有效用户ID（EUID），UID（实际用户）是一个重要的环境变量，可用于检查当前脚本是以超级用户（root）还是普通用户的身份运行。

UID与EUID，两者之间有什么区别，本文介绍之。


# UID与EUID的区别

## 从理论上介绍一下两者区别

实际用户(UID)

实际用户ID是指运行这个进程的用户uid。这个用户uid会被设置为父进程的实际用户ID，并且在系统调用中都不会发生改变。一般情况下，登录进程会将用户登录那个shell的实际用户ID设置为 登录用户的uid，并且这个用户所有进程的实际用户ID都会继承这个值。 超级用户可能会把实际用户 ID设置修改为任意值，但是其他用户不可以。

有效用户

有效用户ID是当前进程所使用的用户ID。 权限认证一般是使用这个值。 初始时，这个ID等于实际用户ID。


## 通过实例展示UID与EUID的区别

先来看一段perl脚本

```shell
test01@node77:/home$ cat id.pl 
#!/usr/bin/perl

use warnings;
use strict;

printf "uid: %-20s euid: %-20s\n",$<,$>;
printf "gid: %-20s egid: %-20s\n",$(, $);

test01@node77:/home$ 
```

说明:

perl里面的特殊变量$<、$>表示uid euid; $(、$)表示gid egid。只是，$(和$)会存储一个列表，第一位表示的才是gid和egid，这个是perl的设置，不在本文讨论范围。


在root用户下执行，效果如下：

```shell
root@node77:/home# perl id.pl 
uid: 0                    euid: 0                   
gid: 0 0                  egid: 0 0                 
root@node77:/home# 
```


非root用户下执行，效果如下：

```shell
test01@node77:/home$ perl id.pl 
uid: 1000                 euid: 1000                
gid: 1000 1000            egid: 1000 1000           
test01@node77:/home$ 
```


说明：

第一次运行的时候，使用的是超级权限(root)，所以uid=0，gid=0；

第二次运行的时候，使用的是普通用户，uid=1000，gid=1000，由于没有使用setgid对gid进行改变，所以uid=gid。


# 总结

* 有效用户ID(euid)代表它的属主，限制进程的权限
* 在没有seteuid的情况下，uid=euid，guid同理
* 当进程以root权限调用setuid()后，root权限会被丢弃，所以root权限下，使用setuid()更加安全

