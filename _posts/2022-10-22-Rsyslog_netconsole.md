---
layout:     post
title:      "使用rsyslog 配置netconsole记录dmesg"
subtitle:   "rsyslog to config netconsole for dmesg"
date:       2022-10-22
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - netconsole
---


# Overview


ENV Info：

```
Server ：127.71.57.11
Log Reciver： 127.71.57.13
```

OS Info：

```
root@pytest-11:~# hostnamectl 
   Static hostname: pytest-11
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 61c34f4154784f019254f8033d92d9cf
           Boot ID: 4be228ed0f824e40bb0a2155928f4c60
    Virtualization: qemu
  Operating System: Ubuntu 16.04.7 LTS
            Kernel: Linux 4.14.148-202207281639.git553ed7f
      Architecture: x86-64
root@pytest-11:~#
```


# Practices


## Shell script

```
root@pytest-11:~# cat net_console.sh 
#!/bin/bash
senddev=bond0
receive_ip=127.71.57.13
receive_port=6666
mac=
gateway=$(ip -4 -o route get $receip|/usr/bin/cut -f 3 -d ' ')
if echo $gateway|/bin/grep -q '^[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+$'
then
    mac=$(ip -4 neigh show $gateway|/usr/bin/cut -f 5 -d ' ')
else
    /bin/ping -c 2 $receip > /dev/null
    mac=$(ip -4 neigh show $receip|/usr/bin/cut -f 5 -d ' ')
fi
if [[ x$mac = x"" ]]; then
    exit 0
fi
echo 7 > /proc/sys/kernel/printk
/sbin/modprobe -r netconsole
/sbin/modprobe netconsole netconsole=@/$senddev,$receive_port@$receive_ip/$mac
```

* Description

* * Script run in Server.



## Configuration of the Log Receiver

If not config this, log will record in kern.log by efault.


### Create a 'xxx.conf' file

```
root@pytest-83-13:/etc/rsyslog.d# cat net-console.conf 
$ModLoad imudp
$UDPServerRun 6666
$template NetconleFile,"/var/log/%fromhost-ip%.log"
if $fromhost-ip startswith '172.17.' then ?NetconleFile
& ~
root@pytest-83-13:/etc/rsyslog.d# 
```

### Restart rsyslog service

```systemctl restart rsyslog```


# How to use

## Add Executable Permissions

```chmod +x net_console.sh````

## Write to boot-up


```echo /root/net_console.sh >> /etc/rc.local```


## Run script to config netconsole

```bash net_console.sh```


## Check dmesg

```dmesg|grep console```, output like the fallowing:

```
Jan  9 18:36:29 pytest-11 kernel: [ 2639.892808] console [netcon0] enabled
Jan  9 18:36:29 pytest-11 kernel: [ 2639.892872] netconsole: network logging started
Jan  9 18:36:30 pytest-11 kernel: [ 2641.324336] netpoll: netconsole: local port 6665
Jan  9 18:36:30 pytest-11 kernel: [ 2641.324388] netpoll: netconsole: local IPv4 address 127.71.57.11
Jan  9 18:36:30 pytest-11 kernel: [ 2641.324438] netpoll: netconsole: interface 'eth0'
Jan  9 18:36:30 pytest-11 kernel: [ 2641.324484] netpoll: netconsole: remote port 6666
Jan  9 18:36:30 pytest-11 kernel: [ 2641.324532] netpoll: netconsole: remote IPv4 address 127.71.57.13
Jan  9 18:36:30 pytest-11 kernel: [ 2641.324587] netpoll: netconsole: remote ethernet address ff:ff:ff:ff:ff:ff
Jan  9 18:36:30 pytest-11 kernel: [ 2641.324646] netpoll: netconsole: eth0 doesn't exist, aborting
Jan  9 18:38:13 pytest-11 kernel: [ 2743.844684] netpoll: netconsole: local port 6665
Jan  9 18:38:13 pytest-11 kernel: [ 2743.844735] netpoll: netconsole: local IPv4 address 127.71.57.11
Jan  9 18:38:13 pytest-11 kernel: [ 2743.844777] netpoll: netconsole: interface 'eth0'
Jan  9 18:38:13 pytest-11 kernel: [ 2743.844811] netpoll: netconsole: remote port 6666
```


## Check if the receiving end has received log messages

```
root@pytest-83-13:/var/log# cat /var/log/127.71.57.11.log 
Jan 10 10:47:17 pytest-11.local [56833.474232] memory_corrupted,adsjkfjlasjdkf
root@pytest-83-13:/var/log# 
```

* Description

* * As above log is simulated by injecting messages to Kernel with the help of syslog-tool tool (self-developed).
* * Of course, it can be simulated by restarting the Server side (too heavy action), or simulating the NIC down/up. e.g:

```
Jan 10 10:54:17 pytest-11.local [57253.352107] bond1: link status definitely down for interface ens19, disabling it
Jan 10 10:54:17 pytest-11.local [57253.352950] bond1: now running without any active interface!
Jan 10 10:54:30 pytest-11.local [57266.124671] 8021q: adding VLAN 0 to HW filter on device ens19
Jan 10 10:54:30 pytest-11.local [57266.143120] bond1: link status definitely up for interface ens19, 0 Mbps full duplex
Jan 10 10:54:30 pytest-11.local [57266.143728] bond1: making interface ens19 the new active one
Jan 10 10:54:30 pytest-11.local [57266.145527] bond1: first active interface up!
```

