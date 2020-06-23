---
layout:     post
title:      "快速获取Lab中哪些IPMI IP地址被使用"
subtitle:   "Fast to get IPMI IPs which are in used"
date:       2020-06-23
author:     "Gavin"
catalog:    true
tags:
    - fping
    - Linux
---


# 概述

Lab里有一大批设备，每个设备都配置了IPMI地址，虽然Office提供了一个在线的excel供大家编辑，但未必每个人都会定期去更新它（因为设备偶尔有进有出），时间久了就会发现excel记录太旧了。

本文不是介绍如何定期更新excel，而是如何快速获取哪些IPMI地址在使用。


# 实践

## 利用ping获取哪些地址被使用

```
#!/bin/bash

for ip in 1.72.5.{1..255};
do
    ping $ip -c 2 &> /dev/null
    if [ $? -eq 0 ]; then
        echo "($ip) is alive"
    fi
done

```

看看执行耗时：

```
root@node77:~# time bash ping.sh 2>&1 >/dev/null

real	12m47.366s
user	0m0.161s
sys	0m0.627s
root@node77:~# 
```

在这个脚本中，每个ping是顺次独立执行的，即每个IP地址都会被ping到，每执行有ping，都会有一段最低2秒的时延（-c 2），很明显，把255给都ping一遍，起码255*2s的时间，效率太低了。


## shell 改进

改进上述脚本的操作，使用并发，要想并发，可将循环体放在()&中，将命令放在()，使其中的命令可作为shell的子shell来执行，而&脱离当前线程，在后台继续执行，改进后如下：

```
#!/bin/bash

for ip in 1.72.5.{1..255};
do
(
    ping $ip -c 2 &> /dev/null
    if [ $? -eq 0 ]; then
        echo "($ip) is alive"
    fi
)&

wait

done
```

看看执行耗时：

```
root@node77:~# time bash ping2.sh 2>&1 >/dev/null

real	12m31.581s
user	0m0.326s
sys	0m0.849s
root@node77:~# 
```


从时间上看，基本没差啊，整体上时间还是非常的久，有没有更好的办法？答案是肯定的，使用fping，但fping Linux系统不自带，需要自行安装，安装地址参考如下： ```https://pkgs.org/download/fping ```


## 使用fping

fping类似于ping，但比ping强大的多。与ping要等待某一主机连接超时或发回反馈信息不同，fping给一个主机发送完数据包后，马上给下一个主机发送数据包，实现多主机同时ping。

看一下官方解释：

```
NAME
       fping - send ICMP ECHO_REQUEST packets to network hosts

SYNOPSIS
       fping [ options ] [ systems... ] fping6 [ options ] [ systems... ]

DESCRIPTION
       fping is a program like ping which uses the Internet Control Message Protocol (ICMP) echo request to determine if a target host is responding.  fping differs from ping in that you can specify any number of targets on the command line, or specify a file
       containing the lists of targets to ping.  Instead of sending to one target until it times out or replies, fping will send out a ping packet and move on to the next target in a round-robin fashion.  In the default mode, if a target replies, it is noted and
       removed from the list of targets to check; if a target does not respond within a certain time limit and/or retry limit it is designated as unreachable. fping also supports sending a specified number of pings to a target, or looping indefinitely (as in ping
       ). Unlike ping, fping is meant to be used in scripts, so its output is designed to be easy to parse.

       The binary named fping6 is the same as fping, except that it uses IPv6 addresses instead of IPv4.
```

测试一下fping的效果：

```
root@node77:~# time fping -s -a -q -g 1.72.5.0/24
1.72.5.111
1.72.5.114
1.72.5.115
1.72.5.116
1.72.5.117
1.72.5.118
1.72.5.124
1.72.5.125
1.72.5.126
1.72.5.127
1.72.5.128
1.72.5.181
1.72.5.182
1.72.5.183
1.72.5.195
1.72.5.196
1.72.5.197
1.72.5.199
1.72.5.202
1.72.5.204
1.72.5.205
1.72.5.206
1.72.5.207
1.72.5.208
1.72.5.209
1.72.5.210
1.72.5.211
1.72.5.212
1.72.5.213
1.72.5.214
1.72.5.215
1.72.5.216
1.72.5.217
1.72.5.218
1.72.5.220
1.72.5.221
1.72.5.222
1.72.5.223
1.72.5.229
1.72.5.231
1.72.5.233
1.72.5.234
1.72.5.235
1.72.5.249
1.72.5.251
1.72.5.252
1.72.5.253
1.72.5.254
1.72.5.53
1.72.5.141
1.72.5.144
1.72.5.151
1.72.5.152
1.72.5.153
1.72.5.154
1.72.5.160
1.72.5.165
1.72.5.166
1.72.5.167
1.72.5.169
1.72.5.174
1.72.5.175
1.72.5.176
1.72.5.177

     254 targets
      64 alive
     190 unreachable
       0 unknown addresses

     190 timeouts (waiting for response)
     840 ICMP Echos sent
      64 ICMP Echo Replies received
     714 other ICMP received

 0.15 ms (min round trip time)
 0.38 ms (avg round trip time)
 2.00 ms (max round trip time)
       22.798 sec (elapsed real time)


real	0m22.801s
user	0m0.007s
sys	0m0.077s
root@node77:~# 
```

效率非常的高，不足23秒，而且输出的IP地址就是alive的，并增加了汇总信息，非常的直观。



