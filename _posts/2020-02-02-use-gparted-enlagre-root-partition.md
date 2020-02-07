---
layout:     post
title:      "利用gparted扩展根分区"
subtitle:   "Use gparted to enlagre root partition"
date:       2020-02-02
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 前言

lab有一套Jenkins环境，是一台VM环境，最初安装系统的时候，整个系统分区只有20G的容量，后来发现这个容量实在太小，经常因根分区满导致jenkins任务没法正常执行。

后台通过VMware vSphere Client扩大了这个分区空间（扩大到60G）：

```
root@ubuntu-16:~# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk 
sda      8:0    0   20G  0 disk /iso
sdb      8:16   0   60G  0 disk 
├─sdb1   8:17   0   16G  0 part /
├─sdb2   8:18   0    1K  0 part 
└─sdb5   8:21   0    4G  0 part [SWAP]
sr0     11:0    1 1024M  0 rom  
root@ubuntu-16:~# 
```

但这多出的40G，如何分配给根/分区呢？ 

# 环境准备

为此，准备了一个测试环境，进行/分区扩容验证。

安装Ubuntu16.04，系统分区是60G的容量：

```
root@ubuntu16:~# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk 
sda      8:0    0   60G  0 disk 
├─sda1   8:1    0   59G  0 part /
├─sda2   8:2    0    1K  0 part 
└─sda5   8:5    0  975M  0 part [SWAP]
sr0     11:0    1 1024M  0 rom  
root@ubuntu16:~# 
```

成功安装后，关机，通过VMware vSphere Client扩大vdisk空间，从60G扩大到80G：

```
root@ubuntu16:~# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk 
sda      8:0    0   80G  0 disk 
├─sda1   8:1    0   59G  0 part /
├─sda2   8:2    0    1K  0 part 
└─sda5   8:5    0  975M  0 part [SWAP]
sr0     11:0    1  873M  0 rom  
root@ubuntu16:~# 
```

并在根目录下，创建了一个文件，计算md5值：

```
root@ubuntu16:/# echo 'check' > test.txt 
root@ubuntu16:/# md5sum test.txt 
5e9b13ce8f6c99f3f510756be58d15fe  test.txt
root@ubuntu16:/# 
```

# 借助gparted live ISO进行修改

上面的尝试，说明了gparted可以调整分区大小，且支持无损，但是对于/根目录的分区无法调整，但是它提供ISO工具，可以启动后进行调整。

下载了一个gparted-live-0.29.0-1-amd64.iso，下载链接：

链接：https://pan.baidu.com/s/1I_JWP7-HKHfNM44mlt6Vow 提取码：moq4

### 修改VM启动顺序

在将gparted-live-0.29.0-1-amd64.iso作为VM “CD/DVD设备”条件下，重新启动VM，进入BIOS界面，设置操作如下图所示：

<img class="shadow" src="/img/in-post/vm_set_BIOS.png" width="800">

进入Boot页面，使用“-/+”按钮，将“CD-ROM Driver”设置为第一启动顺序，保存后退出，如下图所示：

<img class="shadow" src="/img/in-post/change-boot-order.png" width="800">

### 使用 GParted Live 安装介质启动你的系统

VM重新开机后，会弹出如下界面：

<img class="shadow" src="/img/in-post/boot-gparted.png" width="800">

这里选择 “GParted Live (Default settings)” ，并敲击回车按键。

### 键盘选择

默认情况下，它选择第二个选项，按下回车即可。

<img class="shadow" src="/img/in-post/package_configuration.png" width="800">

### 语言选择

默认情况下，它选择 “33” 美国英语，按下回车即可。

<img class="shadow" src="/img/in-post/language_set.png" width="800">


### 模式选择（图形用户界面或命令行)

默认情况下，它选择 “0” 图形用户界面模式，按下回车即可。

<img class="shadow" src="/img/in-post/mode_select.png" width="800">

### 加载 GParted Live 屏幕

现在，GParted Live 屏幕已经加载，它显示我以前创建的分区列表:

<img class="shadow" src="/img/in-post/gparted_show_all_partitions.png" width="800">

### 删除系统磁盘非根分区

这里系统磁盘对应分区是sda，下面有swap分区（sda2， sda5），需要删除sda2和sda5，因为只有连续的分区才能合并（未分配的分区中间间隔着sda2和sda5）。

### 合并分区

选择根分区，点击“Resize/Move”，将20G空闲空间合并到sda1分区。

### 重新创建swap分区，并格式化为linux-swap

这里新建一个分区，文件系统选择linux-swap，并格式化为swap分区

### 生效设置

进行了上面的操作后，点击“Apply”等待生效，gparted处理过程如下图所示：

<img class="shadow" src="/img/in-post/gparted_apply.png" width="800">

成功后，会在界面上显示”complete“字样

然后VM断连GParted Live 安装介质，重启启动VM，VM在启动过程中会出现如下信息(稍微等待一点时间即可，无需人工干预)：

<img class="shadow" src="/img/in-post/vm_start_status.png" width="800">

### 效果确认

最终效果如下：

```
root@ubuntu16:~# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk 
sda      8:0    0   80G  0 disk 
├─sda1   8:1    0   79G  0 part /
└─sda2   8:2    0    1G  0 part 
sr0     11:0    1 1024M  0 rom  
root@ubuntu16:~# 
root@ubuntu16:/# cat test.txt 
check
root@ubuntu16:/# md5sum test.txt 
5e9b13ce8f6c99f3f510756be58d15fe  test.txt
root@ubuntu16:/# 
```

文件md5值，在扩容前后一样.

# 是否还有其他方法？

网上有人说在OS里安装gparted，直接执行gparted来扩展分区，下文将验证其可行性。

## 安装gparted

因为要使用gparted来进行根分区的扩容，需要安装gparted；如果已经安装了，忽略此步骤。

```apt-get install gparted ```


如果后面使用XManager还有问题，可以在此ubuntu节点上安装如下一个工具：

```apt install x11-xserver-utils ```


## 通过XManager访问此节点

需要找一台Windows安装XManager，非本文重点，忽略。

### XManager上创建一个XStart

新建一个XStart，输入此节点的IP地址、root账号和密码，以及需要执行的命令（gparted），保存即可。之后点击这个新建的XStart，会出现有一个auth文件没有，关掉后重新打开这个XStart再次登录即可。

如果直接在终端执行gparted命令时，会出现如下错误：

```
root@ubuntu16:/# gparted

(gpartedbin:2462): Gtk-WARNING **: cannot open display:
```

### 查看进入gparted界面效果

成功通过XStart进入可视化界面后，会看到已经使用的空间都带有锁标记，如下图所示：

<img class="shadow" src="/img/in-post/gparted_lock.png" width="1200">

这时是不能对分区进行操作的，网上有人说需要先卸载（unmount）或者停止（swapoff），然后才能进行Resize操作。

#### 尝试swapoff

```
root@ubuntu16:/# swapoff -a
root@ubuntu16:/# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk
sda      8:0    0   80G  0 disk
├─sda1   8:1    0   59G  0 part /
└─sda5   8:5    0  975M  0 part
sr0     11:0    1  873M  0 rom
root@ubuntu16:/#
```

上面显示已经swapoff了，此时重新进入gparted界面，显示如下：

<img class="shadow" src="/img/in-post/swapoff_root_lock.png" width="1200">

尝试对根分区进行容量扩展，发现没法扩展；尝试先umount，发现也没法umount掉这个根分区，因为会显示为Busy（其实想想，如果umount掉了，系统都没法使用了吧，更不用谈当前gparted操作了），从这里，基本上
把swapoff和umount两条路给堵死了，说明行不通。

还有人说用制作Ubuntu启动U盘试用模式下进行的，不过我的环境是虚机，就没尝试这个方法。

先还原环境吧，swapon回来；

```
root@ubuntu16:/# swapon -a
root@ubuntu16:/# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk
sda      8:0    0   80G  0 disk
├─sda1   8:1    0   59G  0 part /
└─sda5   8:5    0  975M  0 part [SWAP]
sr0     11:0    1  873M  0 rom
root@ubuntu16:/#
```

## 结论

直接通过gparted，只能对非根分区进行扩容/缩容，如果想对根分区进行扩容/缩容，可以通过gparted live ISO进行。

