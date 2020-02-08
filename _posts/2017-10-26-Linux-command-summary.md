---
layout:     post
title:      "测试中常用的Linux命令汇总"
subtitle:   "Linux command"
date:       2017-10-26
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

在日常测试工作中，产品是部署在Ubuntu上的，本文罗列一些在测试过程中，常用到的一些指令。

# 批量生成文件

方法1：

```seq 1 10  | xargs -i{} -P 10 touch file_{}  ```

10个并发来touch file


方法2：

```for i in {1..100}; do dd if=/dev/zero of=file_$i bs=1M count=1; done ```

这个没有并发哦~


方法3：

```touch file{0..9}.txt ```

相应的，创建目录、删除目录/文件（夹），都可以以此类推：

```rm -rf file{0..9} ```

```mkdir dir{0..9} ```

```rm -rf dir{0..9} ```

# 查找僵尸进程

```ps -A -ostat,ppid,pid,cmd | grep -e '^[zZ]' ```

# 查看进程运行时间

```ps -A -opid,stime,etime,args | grep XXX ```

# 查看某进程什么时候启动、运行时间

## 启动时间

```ps -eo lstart ```

## 运行多长时间

```ps -eo etime ```

示例:

```ps -eo pid,lstart,etime | grep 5176```

或者

```ps -p `pidof ceph-mon` -o etime,pid,cmd ```


# 查看网卡读写信息

方法1：

```nfsiostat 2 ```

方法2：

```iftop ```

或者：

```iftop -I ethX ```

方法3：

```sar -n DEV 2 ```


# 查看cpu信息

## 查看物理CPU的个数

```cat /proc/cpuinfo |grep "physical id"|sort |uniq|wc -l```
 
## 查看逻辑CPU的个数

```cat /proc/cpuinfo |grep "processor"|wc -l```

或者使用nproc命令查看:

```
root@host245:~# nproc
32
```

## 查看CPU是几核

```cat /proc/cpuinfo |grep "cores"|uniq```

## 查看CPU的主频

```cat /proc/cpuinfo |grep MHz|uniq```

## 查看内存的插槽数，已经使用多少插槽。每条内存多大，已使用内存多大

```dmidecode|grep -P -A5 "Memory\s+Device"|grep Size|grep -v Range```

## 查看内存支持的最大内存容量

```dmidecode|grep -P 'Maximum\s+Capacity'```

## 查看内存的频率

```dmidecode|grep -A16 "Memory Device"```

```dmidecode|grep -A16 "Memory Device"|grep 'Speed'```


# VM热加盘

虚拟机添加硬盘，无需重启，识别新硬盘

```echo '- - -' > /sys/class/scsi_host/host*/scan ```

# 查看sector size

```cat /sys/block/sdX/queue/*block_size```

# 如何确定盘是SSD类型的磁盘

方法1：

```cat /sys/block/sdX/queue/rotational```


方法2：

```lsblk -d -o name,rota```

输出示例如下：

```
root@host245:~/tmp# lsblk -d -o name,rota
NAME ROTA
sda     0
sdb     0
sdc     1
sdd     1
sde     1
sdf     1
sdg     1
sdh     1
sdi     1
sdj     1
sdk     1
sdl     1
```

说明：

* 0 表示是SSD
* 1 表示是HDD或者SAS盘
* 如SSD是在RAID卡上，此方法不适用，需要借助Megacli(e.g:```MegaCli ldpdinfo aall```)来确认

# 查看分区的uuid信息

```
[root@nwos ~]# blkid  /dev/sdb1
/dev/sdb1: UUID="9d7790c6-4fd9-47db-ad16-24d1025d4518" TYPE="ext4" 
```

或者直接使用blkid指令列出所有分区的uuid

<img class="shadow" src="/img/in-post/blkid.png" width="1200">


# 快速创建大文件

```fallocate -l 10G bigfile```

上面这个，只能骗过ls -s, du和df


```truncate -s 10G bigfile ```

上面这个，只能骗过ls -l


```dd of=bigfile bs=1 seek=10G count=0```

上面这个，只能骗过ls -l


# 调出后台运行的命令

比如vi 一个文件，ctrl+z之后，进入后台, 或者在vi期间，session中断了（没有tmux）

```
root@node01:/home/stability_testing/src/testCase/_03_ctdb/testcasebase# vi ctdbManagerTestcaseBase.py 

[1]+  Stopped  

```

ps查看：

```
root@node01:/home/stability_testing/src/testCase/_03_ctdb/testcasebase# ps -ef | grep -i vii
root      393866  399030  0 11:35 pts/2    00:00:00 grep --color=auto -i vii
root@node01:/home/stability_testing/src/testCase/_03_ctdb/testcasebase# ps -ef | grep -i vi
root        1085       2  0 Jun21 ?        00:00:00 [dbu_evict]
root        1111       2  0 Jun21 ?        00:00:12 [arc_user_evicts]
root      394119  399030  0 11:35 pts/2    00:00:00 grep --color=auto -i vi
root      412813  399030  0 10:58 pts/2    00:00:02 vi ctdbManagerTestcaseBase.py
```

如何调出这个vi命令，继续进行vi编辑？

## Step1、使用jobs命令
`
```
root@node01:/home/stability_testing/src/testCase/_03_ctdb/testcasebase# jobs
[1]+  Stopped                 vi ctdbManagerTestcaseBase.py
```

这里看到[1]+，如果有多个后台运行，展示类似如下：

```
[root@pcmxexweb etc]# jobs

[1]-  Stopped                 find / -name xml

[2]+  Stopped                 vi /etc/hosts
```

## Step2、执行fs X，调出来

X表示中括号里的数值，比如：

```fg 1```

则调出find命令


# 查看所有网口的Link Detected 状态

```ifconfig -a | grep 'Link encap:' | grep -v lo | awk '{{print $1}}' | xargs -I{} -t ethtool {} | grep 'Link detected' ```

输出示例：

```
ethtool bond0 
	Link detected: yes
ethtool bond1 
	Link detected: yes
ethtool enp129s0f0 
	Link detected: yes
ethtool enp129s0f1 
	Link detected: no
ethtool enp130s0f0 
	Link detected: yes
ethtool enp130s0f1 
	Link detected: no
ethtool eth0 
	Link detected: yes
ethtool eth1 
	Link detected: no
```


# 格式化对齐输出

对于cat的一些内容，显示总是不对齐

解决方法

使用\|column -t， 如：

```cat dev | column - ```

输出示例：

<img class="shadow" src="/img/in-post/cat_format.png" width="1200">


# 查看top 10 CPU、内存的占用

## CPU占用最多的前10个进程： 

```ps auxw|head -1;ps auxw|sort -rn -k3|head -10 ```

## 内存消耗最多的前10个进程

```ps auxw|head -1;ps auxw|sort -rn -k4|head -10 ```

## 虚拟内存使用最多的前10个进程

```ps auxw|head -1;ps auxw|sort -rn -k5|head -10 ```


# 统计代码行数

## find 加 wc

```find . -type f -iname "*.py" -print0 | xargs -0 wc -l```

这个指令比较原始，会含有注释、空格等的总计行数.


## 使用cloc进行统计

示例如下：

```cloc /bigtera/nose_framework/src/```

<img class="shadow" src="/img/in-post/code_colc.png" width="1200">


## pylint

```pylint /home/xxx/src```

<img class="shadow" src="/img/in-post/code_pylint.png" width="1200">


# 列出目录的4种方法

方法1：

```ls -d */```

方法2：

```ls -F | grep '/$'```


方法3：

```ls -l | grep '^d'```

方法4：

```find . -type d -maxdepth 1 -print```


# 查看时区

方法1 date

输出示例:

```
root@host245:~/tmp# date +"%Z %z"
CST +0800
```

或者 date -R

```
root@host245:~/tmp# date -R
Wed, 27 Nov 2019 16:59:38 +0800
root@host245:~/tmp# 
```

说明：
* 重点在+0800，表示时区是东八区


方法2 timedatectl

输出示例:

```
root@host245:~/tmp# timedatectl | grep 'Timezone'
        Timezone: Asia/Shanghai (CST, +0800)
```


# 修改时区

当系统安装好后，发现系统时区不对，如何修改呢？

方法1

```tzselect ```


方法2

```timeconfig ```

说明:
* 仅限于RedHat Linux 和 CentOS

方法3

```dpkg-reconfigure tzdata ```

说明:
* 适用于Debian


根据提示，选择不同的时区信息，设置成功后，需要复制文件：

```cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime```

# 清空cache

在跑fio进行读测试之前，一定要进行一次cache的清空，否则会影响fio性能测试结果的。
cache分3种：
1： pagecache； 2：dentries 和 inodes； 3：所有cache

## 清空内存缓存

```
echo 1 > /proc/sys/vm/drop_caches
```

## 清空 pagecache

```
sync
echo 1 > /proc/sys/vm/drop_caches
```

或者

```
sync
sysctl -w vm.drop_caches=1
```

## 清空 dentries 和 inodes

```
sync
echo 2 > /proc/sys/vm/drop_caches
```

或者

```
sync
sysctl -w vm.drop_caches=2
```


## 清空所有缓存（pagecache、dentries 和 inodes）

```
sync
echo 3 > /proc/sys/vm/drop_caches
```

或者

```
sync
sysctl -w vm.drop_caches=3
```

# 清空arp表


```arp -n|awk '/^[1-9]/{print "arp -d " $1}'|sh -x ```

然后 off  和 on 对应的网卡

```
[root@localhost sbull]# ip link set arp off dev eth0
[root@localhost sbull]# ip link set arp on dev eth0
```

最后再查看下arp表信息

```
[root@localhost sbull]# arp -n
```

# 查看当前主机是物理机还是虚拟机

```dmidecode -s system-product-name ```

示例：

物理服务器

```
[root@JX-P-L-KVM-231 ~]# dmidecode -s system-product-name
# SMBIOS implementations newer than version 2.7 are not
# fully supported by this version of dmidecode.
PowerEdge R930
```


KVM 虚拟主机

```
[root@JX-V-L-PHP-237 ~]# dmidecode -s system-product-name
KVM
```

VMware vSphere 虚拟主机

```
[root@ZE-T1 ~]# dmidecode -s system-product-name
VMware Virtual Platform
```

阿里云主机

```
[root@zdc ~]# dmidecode -s system-product-name
HVM domU
```

