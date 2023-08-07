---
layout:     post
title:      "修复memcache 未授权访问漏洞"
subtitle:   "memcache of limit 11211 port"
date:       2017-07-30
author:     "Gavin"
catalog:    true
tags:
    - memchche
    - securite
    - Linux
---


# 背景说明 

memcache 未授权访问漏洞修复，修复方法是通过系统的防火墙来禁止其他ip访问


# patch步骤 

## 1. 检查 

客户端确认端口访问情况，可以看到 11211 可以访问


```
root@wyz-node2:~# telnet 10.10.10.134 11211
Trying 10.10.10.134...
Connected to 10.10.10.134.
Escape character is '^]'.
dd^H^H^H^H^C^C^C^C^C^C^C^C
```

## 2. 存储节点增加iptable（每个节点都要做）

注意其中ip 需要根据实际情况替换
 
```
iptables -I INPUT -p tcp --dport 11211 -j DROP
iptables -I INPUT -s 127.0.0.1 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.17.73.134 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.17.73.135 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 172.17.73.136 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 10.10.10.134 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 10.10.10.135 -p tcp --dport 11211 -j ACCEPT
iptables -I INPUT -s 10.10.10.136 -p tcp --dport 11211 -j ACCEPT
root@wyz:~/docker-file/first# telnet 172.17.73.134 11211
```

## 3. 效果验证 

每个节点做完后，通过 客户端 telnet 11211端口，验证是否可以访问。可以看到已经无法访问了

```
root@wyz:~/docker-file/first# telnet 172.17.73.134 11211

Trying 172.17.73.134...
```
