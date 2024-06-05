---
title: 跨终端情况下，重新使用原来的vim
subtitle: Stunning linux commands
date: 2024-05-31 11:25:29
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: ps能够看到vim进程，但jobs无作业，如何在跨终端情况下，重新使用原来的vim
categories:
    - [Linux]
    - [vim]
tags:
    - Linux
    - vim
---


# 背景

`Linux`系统，使用`vim`打开了几个文件，后来`XShell`工具重连了，但`vim`进程还在，使用`jobs`命令无法查看到`vim`的`job`信息。

# 原因分析

`jobs`命令是查看**当前终端的后台作业（进程），是获取本次bash进程下子进程的后台作业**。

当本次终端退出后，后台作业变成孤儿进程，孤儿进程由系统父进程接管。

当再次连接终端时，原作业与当前终端，不存在关系父子关系，故看不到进程。

但是原作业，会在系统中一直运行，直到完成或被停止。

这就是为什么终端退出后，`jobs`看不到的原因了。

# 如何继续使用原来的vim，继续访问原文件？

## 操作过程

1. 先查询出相关进程的id

```shell
root@Gavin:~# ps -ef |grep -i vim
root        6221    3866  0 May29 pts/5    00:00:00 vim hookspec.py
root        7158    2172  0 May30 pts/2    00:00:00 vim 2999-12-30-pytest_hook.md
root       23588   21024  0 09:09 pts/12   00:00:00 grep --color=auto -i vim
root@Gavin:~# jobs
root@Gavin:~# jobs -l
root@Gavin:~# jobs -r
```

2. 使用reptyr

如果没有安装，根据不同的Linux系统进行安装：

```shell
apt-get install reptyr  # 对于 Ubuntu/Debian
yum install reptyr  # 对于 CentOS/RHEL
```

然后使用如下命令重新打开原来的`vim`进程：

```shell
reptyr 6221
```

其中6221为对应`vim`的`pid`。

# 结语

推荐`tmux`命令，详见我的另外一篇博文:[令人惊艳的Linux工具](https://gavin-wang-note.github.io/2015/03/09/amazing_linux_commands/)
