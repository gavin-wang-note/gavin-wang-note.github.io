---
layout:     post
title:      "网络时延--Linux模拟复杂网络环境下的传输（netem和tc）"
subtitle:   "Network Lagency -- By netem and tc to limit Linux network"
date:       2018-07-10
author:     "Gavin"
catalog:    true
tags:
    - network
---

# 概述

在进行网络服务的测试时，有时需要模拟一些异常的网络情况，例如网络延时长、丢包、网络地址连接不通等。
在Linux下，可以通过tc工具来模拟各种网络情况；通过iptables禁止访问某个网络地址。


# netem与tc介绍

netem 是 Linux 2.6 及以上内核版本提供的一个网络模拟功能模块。该功能模块可以用来在性能良好的局域网中，模拟出复杂的互联网传输性能，诸如低带宽、传输延迟、丢包等等情况。

使用 Linux 2.6 (或以上) 版本内核的很多发行版 Linux 都开启了该内核功能，比如Fedora、Ubuntu、Redhat、OpenSuse、CentOS、Debian等等。

tc 是 Linux 系统中的一个工具，全名为traffic control（流量控制）。tc 可以用来控制 netem 的工作模式，也就是说，想要使用 netem ，则需要内核开启了 netem，而且安装了 tc工具。

tc控制的是发包动作，不能控制收包动作。它直接对物理接口生效，如果控制了物理的eth0，那么逻辑网卡（比如eth0:1）也会受到影响，反之则不行，控制逻辑网卡是无效的。


# 模拟延迟传输

将 eth0 网卡的传输设置为延迟100毫秒发送

```
$ tc  qdisc  add  dev  eth0  root  netem  delay  100ms  
```

如果设置出现：

```
root@auto-70-2:~#  tc qdisc add dev bond0 root netem
RTNETLINK answers: File exists
```

说明之前设置过，解决方法：

```
ip addr flush dev bond0
```

真实的情况下，延迟值不会这么精确，会有一定的波动，下面命令模拟带有波动性的延迟值：

```
 $ tc  qdisc  add  dev  eth0  root  netem  delay  100ms  10ms
```

该命令将 eth0 网卡的传输设置为延迟 100ms ± 10ms （90 ~ 110 ms 之间的任意值）发送。

由于各个包的延迟值不通，也会在一定程度上打乱发包的次序。


还可以更进一步加强这种波动的随机性，将 eth0 网卡的传输设置为 100ms ，同时，大约有30%的包会延迟 ± 10ms 发送：

```
 $ tc  qdisc  add  dev  eth0  root  netem  delay  100ms  10ms  30%
```

# 模拟网络丢包

将 eth0 网卡的传输设置为随机丢掉 1% 的数据包。

```
 $ tc  qdisc  add  dev  eth0  root  netem  loss  1%  
```

也可以设置丢包的成功率，将 eth0 网卡的传输设置为随机丢掉 1% 的数据包，成功率为30% ：

```
 $ tc  qdisc  add  dev  eth0  root  netem  loss  1%  30%
```

# 模拟包重复

将 eth0 网卡的传输设置为随机产生 1% 的重复数据包。

```
 $ tc  qdisc  add  dev  eth0  root  netem  duplicate 1% 
```

# 模拟数据包损坏

将 eth0 网卡的传输设置为随机产生 0.2% 的损坏的数据包。 (内核版本需在2.6.16以上）

```
 $ tc  qdisc  add  dev  eth0  root  netem  corrupt  0.2% 
```

# 模拟数据包乱序

将 eth0 网卡的传输设置为:有25%的数据包（50%相关）会被立即发送，其他的延迟10秒。

```
 $ tc  qdisc  change  dev  eth0  root  netem  delay  10ms   reorder  25%  50%
```

# 实例

step1：使用ifconfig命令查看你的网卡信息，如:eth0

step2：将网卡加入监控列表 

       ```$ sudo tc qdisc add dev eth0 root netem```
step3：
       设置丢包率 

       ```$ sudo tc qdisc change dev eth0 root netem loss 0.5% ```

       设置重发

       ```$ sudo tc qdisc change dev eth0 root netem duplicate 1% ```

      设置发乱序包

       ```$ sudo tc qdisc change dev eth0 root netem gap 5 delay 10ms```


如果想让网络恢复正常，只需要删除监控，或将设置的值相应归0即可。

例如，设置延时
```$ sudo tc qdisc add dev eth0 root netem delay 4s```

取消延时

```$ sudo tc qdisc del dev eth0 root netem delay 4s```


# 禁止访问一个IP

如果要禁止访问一个IP，不使用tc，而是用iptables。iptalbes可以简单理解为linux下的防火墙，控制网络访问。

1、禁止访问10.237.0.1


```
$ iptables -A OUTPUT -d 10.237.0.1 -j REJECT
```


2、查看规则

```
$ iptables -L OUTPUT -n
Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
REJECT     all  --  0.0.0.0/0            10.237.0.1        reject-with icmp-port-unreachable
```

3、查看规则号

```
$ iptables -L OUTPUT -n --line-numbers
Chain OUTPUT (policy ACCEPT)
num  target     prot opt source               destination         
1    REJECT     all  --  0.0.0.0/0            10.237.0.1        reject-with icmp-port-unreachable
```

4、删除规则

```
$ iptables -D OUTPUT 1
```

