---
layout:     post
title:      "CentOS7设置netconsole"
subtitle:   "Base on CentOS7 to confie netconsole"
date:       2022-06-08
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - netconsole
---



# Netconsole简述



将内核打印的日志信息通过UDP方式发送至另一台服务器。

本文概述的是基于CentOS7的配置设定，Ubuntu的设定会右差别，请参考之前的另外一篇博文。



# 配置内核日志发送端（Client端）



说明：

   这里的client端，表明的是当前哪台机器要将kernel log上报到rsyslog server去。



## 写入/rtc/rc.local中，开机自动设置



```
dmesg -n 7
modprobe configfs
modprobe netconsole
```



## 配置netconsole



Server端，配置远程接收ip地址、远程接收端口（默认514）、远程接收MAC（可选）、本地发送设备名、本地发送端口



vi /etc/sysconfig/netconsole

```
# 取消SYSLOGPORT、SYSLOGPORT、SYSLOGMACADDR注释并添加相关参数
#--------------------------------------------------------
#也可执行如下命令插入所需的ip、port、mac
#端口为接收端服务器rsyslog服务的接收端口
ip="192.168.1.161"
echo -e "SYSLOGADDR=$ip\nSYSLOGPORT=514\nSYSLOGMACADDR=$(ping -c 1 $ip>/dev/null&&arp|grep $ip|tr -s ' '|cut -f3 -d ' ')">>/etc/sysconfig/netconsole
```



## 配置/etc/sysconfig/netconsole 中DEV设备



vi /etc/sysconfig/netconsole

修改上述配置文件中的 DEV的值，如果配置了bond，需设置为bondX;否则设置为具体网口名称。



## 重启netconsole服务


```
systemctl restart netconsole
```



## 启用netconsole自启动

```
systemctl enable netconsole
```



# 配置内核日志接收端（Server端）



## 修改rsyslog配置文件接收来自UDP的日志



vi /etc/rsyslog.conf

```
#取消$ModLoad imudp和$UDPServerRun 514注释并修改514为需要监听接收udp的端口
#或者执行如下命令
sed -i 's/^#$Mod.*udp$/$ModLoad imudp/g;s/^#$UDP.*/$UDPServerRun 514/g' /etc/rsyslog.conf	#端口替换为自己所需要的
```



## 重启rsyslog服务

```
systemctl restart rsyslog

```



## 检查是否正常监听指定端口

```
lsof -i:514
```


如下所示即为正常监听中:

```
[root@centos-7 ~]# lsof -i:514
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
rsyslogd 1735 root    3u  IPv4  43816      0t0  UDP *:syslog 
rsyslogd 1735 root    4u  IPv6  43817      0t0  UDP *:syslog 
[root@centos-7 ~]# 
```



# 查看来自远程服务器发送的内核日志



在Client端，尝试down与up某个网口，然后在Server端，执行

```
tail -f /var/log/messages
```

来跟踪日志，检查Client端的kernel log是否将kernel log 上报到当然rsyslog server的messages 文件中

