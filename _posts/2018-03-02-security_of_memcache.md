---
layout:     post
title:      "记一次memcache安全漏洞修复记录"
subtitle:   "security of memcache"
date:       2018-03-02
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [security]
tags:
    - security
---

# 概述

分布式高速缓存系统Memcache存在高危安全漏洞，攻击者可利用该漏洞实施分布式反射拒绝服务（DRDoS）攻击。恶意攻击者向网络服务器发送大量伪造源IP地址的UDP协议数据包，这些源IP地址即为被攻击目标地址。服务器根据Memcache协议内容向源IP地址回复大量数据内容，从而造成被攻击目标网络拥堵进而无法对外提供服务。


# 实践

## 解决方法

增加`iptables`过滤

## 操作步骤

```shell
在/etc/rc.local中增加如下内容：
iptables -I INPUT -p tcp --dport 11211 -j DROP
iptables -I INPUT -s 127.0.0.1 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.20.3.61 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.20.3.62 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 172.20.3.63 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.20.3.64 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.18.12.105 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.18.12.106 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.18.12.107 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.18.12.108 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 172.18.12.109 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 10.10.128.1 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.2 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.3 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.4 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.5 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.6 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.7 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.8 -p tcp --dport 11211 -j Accept
iptables -I INPUT -s 10.10.128.9 -p tcp --dport 11211 -j Accept
```

## 查看是否生效

```iptables -L -n -v ```

清空上面的规则，命令：

```iptables -F ```

