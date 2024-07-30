---
layout:     post
title:      "三种方式修改CentOS hostname"
subtitle:   "Modify hostname for Centos with different method"
date:       2020-01-16
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---

# 三种方法修改Centos hostname

在CentOS7中，有三种定义的主机名:静态的（static）、瞬态的（transient）、灵活的（pretty）。“静态”主机名也称为内核主机名，是系统在启动时从/etc/hostname自动初始化的主机名。“瞬态”主机名是在系统运行时临时分配的主机名，例如，通过DHCP或mDNS服务器分配。静态主机名和瞬态主机名都遵从作为互联网域名同样的字符限制规则。而另一方面，“灵活”主机名则允许使用自由形式（包括特殊/空白字符）的主机名，以展示给终端用户。

本文介绍修改Centos7的hostname的几种方法。

## 方法1: hostnamectl

通过hostnamectl来修改主机名，hostnamectl吐出来的示例信息如下：

```shell
[root@localhost ~]# hostnamectl
   Static hostname: localhost.localdomain
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 39568e567fd24d9d8bacf3010f9b0ac4
           Boot ID: 23efb67f65454f52bbf810e807267c05
    Virtualization: kvm
  Operating System: CentOS Linux 7 (Core)
       CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-957.el7.x86_64
      Architecture: x86-64
[root@localhost ~]# 
```

修改主机名

```shell
[root@localhost ~]# hostnamectl set-hostname host76 --static
[root@localhost ~]# 
```

查看修改后的效果：

```shell
[root@localhost ~]# 
[root@localhost ~]# hostnamectl
   Static hostname: host76
Transient hostname: localhost.localdomain
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 39568e567fd24d9d8bacf3010f9b0ac4
           Boot ID: 23efb67f65454f52bbf810e807267c05
    Virtualization: kvm
  Operating System: CentOS Linux 7 (Core)
       CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-957.el7.x86_64
      Architecture: x86-64
[root@localhost ~]# hostname
host76
```


## 方法2: 修改/etc/hostname

直接修改/etc/hostname文件，将里面的内容删掉，直接替换成自己需要的主机名称：

```shell
[root@localhost ~]# vi /etc/hostname
```

```shell
[root@localhost ~]# cat /etc/hostname 
host76
```

## 方法3: nmtui

还可以通过nmtui进入图形界面来修改主机名。将光标通过键盘的上下键移动到“设定系统主机名”菜单处，按下回车键。

<img class="shadow" src="/img/in-post/nmtui.png" width="200">

此时，屏幕出现“设定主机名”选项卡，输入需要设定的主机名，通过键盘方向键将光标移动到“确定”处，回车键确定即可完成主机名的修改。
