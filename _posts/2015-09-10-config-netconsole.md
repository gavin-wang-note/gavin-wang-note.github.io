---
layout:     post
title:      "Netconsole ：输出kernel log到远端机器"
subtitle:   "Netconsole config"
date:       2015-09-10
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - Netconsole
---

# 为什么需要netconsole

很多时候，很难抓到kernel panic，因为不知道如何复现。 更惨的是，一旦系统重启，系统的log中因为内核异常可能没有记录下有用的信息。这时候netconsole就可以跳出来帮忙了。

比如出现CPU soft lockup的问题，重启之后，从kernel.log中并未找到明显的线索，使用netconsole，让kernel log输出到另一台机器上，这样的话，如果本地不能写磁盘文件，kernel的printk还可以通过网络，将打印的内容记录在另一台机器上。

netconsole是一个内核模块，我们存储的内核将netconsole以module的形式编进了内核，允许将其作为模块加

```root@node-191:~# grep NETCONSOLE /boot/config-3.14.35-server CONFIGNETCONSOLE=m CONFIGNETCONSOLE_DYNAMIC=y ```

Ubuntu的wiki给出了一个很好的页面，介绍netconsole介绍的很详细：```https://wiki.ubuntu.com/Kernel/Netconsole ```

# Linux server端运行时配置

Netconsole can be loaded as one of?kernel modules? manually after boot or auto during boot depending on this module config. See?kernel modules?for configuring it to load at boot. For loading manually any time after boot:

```
# set log level for kernel messages
dmesg -n 7
modprobe configfs
modprobe netconsole
mount none -t configfs /sys/kernel/config
# 'netconsole' dir is auto created if the module is loaded 
mkdir /sys/kernel/config/netconsole/target1
cd /sys/kernel/config/netconsole/target1
# set local IP address
echo 192.168.0.111 > local_ip
# set destination IP address
echo 192.168.0.17 > remote_ip
# find destination MAC address
arping `cat remote_ip` -f |grep -o ..:..:..:..:..:.. > remote_mac
echo 1 > enabled

```

# To verify

netconsole should now be configured. To verify, run ```dmesg |tail``` and you should see "netconsole: network logging started". Check available log levels by running ```dmesg -h```.


# 接收端配置（可以选择一台虚拟机）

```
nc -u -l 6666
or
nc -u -l -p 6666
```

* 说明：
* * Ubuntu 14.4按照上面的设置无效, 具体设置，参考：
```http://blog.51cto.com/7938217/1662524 ```

* * shell脚本运行在被测试节点，kern log信息会被sync到有设置conf的节点（该节点重启rsyslog服务）

