---
layout:     post
title:      "在linux中查看端口号是哪个进程在占用"
subtitle:   "Get proccss which used port"
date:       2022-06-02
author:     "Gavin"
catalog:    true
tags:
    - Linux
---



# 概述

今天升级一套存储，碰到了80端口被占用，导致RGW bind 80 port时bind失败，最终导致RGW服务启用失败，造成S3 业务不可用问题。


# 查看端口信息

Linux 上的 /etc/services 文件可以查看到更多关于保留端口的信息。

可以使用以下三种方法查看端口信息。

* ss：可以用于转储套接字统计信息
* netstat：可以显示打开的套接字列表
* lsof：可以列出打开的文件。

以下我们将找出端口号为80,被哪个守护进程所使用。

## 方法1：使用 ss 命令

```
root@node167:/var/log/ceph# ss -tlnp | grep ':80'
LISTEN     0      128          *:8080                     *:*                   users:(("apache2",pid=2771,fd=3),("apache2",pid=2770,fd=3),("apache2",pid=2769,fd=3),("apache2",pid=2768,fd=3),("apache2",pid=2767,fd=3),("apache2",pid=2760,fd=3))
LISTEN     0      128          *:80                       *:*                   users:(("haproxy",pid=2473,fd=4))
```



## 方法2：使用 netstat 命令

```
root@node167:/var/log/ceph# netstat -lntp | grep ':80'
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      2760/apache2    
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      2473/haproxy    
root@node167:/var/log/ceph# 
```

## 方法3：使用 lsof 命令

```
root@node167:/var/log/ceph# lsof -i:80
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
haproxy 2473 root    4u  IPv4   1766      0t0  TCP *:http (LISTEN)
root@node167:/var/log/ceph# 
```

# 此次事故概述


此次碰到的问题，是升级过程中未对新增功能相关port bind做处理，详情如下：

Parts of ceph-client.radosgw.0.log:

```
2022-06-02 17:05:38.709761 7fec78874040  0 deferred set uid:gid to 0:0 (root:root)
2022-06-02 17:05:38.709778 7fec78874040  0 ceph version 12.2.10-903-g0149c5ceafe (0149c5ceafe1c541f0a5044e1c5c9e4fbc71c64e) luminous (stable), process radosgw, pid 104451
2022-06-02 17:05:38.713450 7fec78874040  0 stack NetworkStack max thread limit is 24, switching to this now. Higher thread values are unnecessary and currently unsupported.
2022-06-02 17:05:38.807429 7fec78874040  0 starting handler: civetweb
2022-06-02 17:05:38.808117 7fec78874040  0 civetweb: 0x55d2cd1be0c0: cannot bind to 80: 98 (Address already in use)
2022-06-02 17:05:38.808143 7fec78874040  0 civetweb: 0x55d2cd1be0c0: cannot bind to 443s: 98 (Address already in use)
2022-06-02 17:05:38.808175 7fec78874040 -1 ERROR: failed run
```

Other log:

```
root@node167:/var/log/ceph# netstat -tnlp | grep ':80'
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      2760/apache2    
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      2473/haproxy    
root@node167:/var/log/ceph# cat /etc/ceph/ceph.conf | grep -i 'rgw frontends'
rgw frontends = civetweb port=80+443s ssl_certificate=/etc/ezs3/ssl/ezs3_server.pem num_threads=1024 ssl_cipher_list=HIGH:!aNULL:!MD5:!3DES ssl_protocol_version=4
rgw frontends = civetweb port=80+443s ssl_certificate=/etc/ezs3/ssl/ezs3_server.pem num_threads=1024 ssl_cipher_list=HIGH:!aNULL:!MD5:!3DES ssl_protocol_version=4
root@node167:/var/log/ceph# cat /etc/haproxy/haproxy.cfg
frontend https
        bind *:80
        bind *:443 ssl crt /etc/ezs3/ssl/ezs3_server.pem
        mode http
        option http-keep-alive
        option http-server-close
        timeout http-keep-alive 10s
        option forwardfor
        reqadd X-Forwarded-Proto:\ https
        default_backend rgw_cluster

backend rgw_cluster
        mode http
        balance roundrobin
       server localhost 127.0.0.1:7480 check
root@node167:/var/log/ceph# 
```

这里可以清晰看到，haproxy占用了RGW的80端口， /etc/haproxy/haproxy.cfg中

```
server localhost 127.0.0.1:7480 check
```

是告知ceph.conf中的rgw，你要使用的是7480这个port，而不是/etc/ceph/ceph.conf使用的却是80 port

```
rgw frontends = civetweb port=80+443s ssl_certificate=/etc/ezs3/ssl/ezs3_server.pem num_threads=1024 ssl_cipher_list=HIGH:!aNULL:!MD5:!3DES ssl_protocol_version=4
```

问题的解决方法是修改/etc/ceph/ceph.conf中的80 port为 7480。
