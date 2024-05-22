---
title: 《pytest测试指南》-- 第二章 2-4 Cobbler部署与使用
date: 2024-06-05 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password: Huawei123!
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 第二章 2-4 Cobbler部署与使用
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 4.1 Cobbler介绍

Cobbler是一个开源的Linux发行版的服务器安装和配置自动化工具，在基于PXE(Preboot eXecution Environment)的安装环境中扮演着中心角色，它可以通过网络自动化地配置和部署多种操作系统。Cobbler 利用了一些已有的技术比如Kickstart、DHCP、TFTP和DNS，以实现其功能。它非常适用于需要快速扩展和管理大量系统的数据中心和网络环境，进行大规模的系统安装，适用于多种Linux发行版，特别是基于 RPM 的系统，如 CentOS、Fedora、Red Hat Enterprise Linux (RHEL) 和其他兼容的版本。

**主要特性包括：**

* **自动化安装**：Cobbler 可以帮助系统管理员自动化安装过程，减少手动配置和错误。
* **系统配置和管理**：通过使用模板和脚本，Cobbler 允许预定义和模块化地配置系统，这样可以确保每次安装的一致性和可重复性。
* **模板和脚本**：Cobbler 支持使用脚本和模板来定义系统配置，可以应用于安装过程中的不同阶段。
* **网络引导（PXE）**：Cobbler可设置网络启动服务（如PXE服务），允许从网络引导计算机并自动安装操作系统。
* **数据同步**：Cobbler 提供了命令行工具和API来管理系统数据的同步功能，如同步Kickstart文件、系统镜像文件等。
* **集成支持**：它可以集成Puppet、Ansible或Chef这样的配置管理工具，并且与版本控制系统配合使用。
* **API 访问**：Cobbler 提供了一个丰富的API接口，允许其他系统或工具与其进行交云。
* **Web界面**：Cobbler还提供了Web界面，使得管理和监视安装过程更加直观方便。
* **扩展性**：因为Cobbler是开源的，所以可以很方便地进行定制和扩展。

Cobbler 通过集中管理多个不同的安装源、配置文件和模板，为系统批量安装提供了强大的后端支持。然而，它的设置和配置可能会比较复杂，需要适当的网络和系统管理知识。此外，随着时间的推移，可能会有新版本发布，带来新的功能和改进。在使用Cobbler时，建议查阅最新的官方文档以获取详细信息和最佳实践。

# 4.2 Cobbler工作原理

Cobbler的工作原理简述如下：

* **服务器和服务配置**

  Cobbler 作为服务器运行，它配置了多个服务，包括 DHCP（动态主机配置协议），TFTP（简单文件传输协议），HTTP/FTP 以服务网络引导和安装文件提供。

* **系统镜像管理**

  Cobbler 可以导入多种发行版的镜像，并对它们进行管理。这包括下载系统镜像，添加安装源，以及存储镜像元数据。完成后，Cobbler 能识别可用的操作系统并提供用于安装它们的网络启动服务。

* **安装配置模板（Kickstart/Preseed文件）**

  对于Red Hat及其衍生版发行版系统，Cobbler 使用 Kickstart 文件来自动化安装。这些文件定义了需要自动进行的安装步骤和配置设置。对于Debian/Ubuntu 系统，则使用 Preseed 文件。Cobbler 允许管理员为不同的操作系统和硬件配置创建和管理多个Kickstart和Preseed模板文件。

* **系统配置和部署**：

  Cobbler 可以管理和配置系统数据，包括主机名、IP地址和硬件配置（如网络接口卡）。当一台机器启动网络引导时，Cobbler 会通过 MAC 地址或其他方法识别机器，并提供特定的操作系统映像和相应的自动化安装模板。

* **网络引导和自动化安装**：

  通过PXE（预启动执行环境）技术，无盘或未安装操作系统的机器可以通过网络引导。在引导流程中，Cobbler 的 TFTP 服务器提供一个引导加载程序（如PXELINUX）和所需的内核和初始化镜像文件。加载程序随后会指引机器下载全套的操作系统镜像和Kickstart/Preseed文件，并开始自动化安装过程。

* **管理和监控**：

  Cobbler 提供命令行工具和Web界面，使得管理员可以轻松地管理和监视部署过程。Cobbler 也支持集成到其他自动化工具链中，为复杂的环境和流程提供无缝接入的自动化部署功能。

Cobbler工作流程图参考如下：

<img class="shadow" src="/img/in-post/cobbler/cobbler工作原理图.png" width="800">

上图Cobbler工作流程介绍如下：

**Cobbler服务器的工作流程**

* **启动**：Cobbler服务启动，此过程通常作为系统服务进行，可以使用系统服务命令启动。

* **更新配置**：Cobbler服务器更新其配置，同步`/etc/cobbler/settings`和`/var/lib/cobbler`中的数据，以确保所有相关组件的配置信息都是最新的。

* **复制TFTP文件**：Cobbler将启动文件和其他必要的引导文件复制到TFTP根目录中。这些文件在网络引导过程中非常重要。

* **启动DHCP服务**：Cobbler通常也会管理DHCP服务，确保能够为新启动和即将安装的客户端分配IP地址。如果服务成功启动，流程继续；如果服务启动失败，则会显示错误信息，并需要进行故障排查。

* **DHCP服务**：如果DHCP服务启动成功，它就会等待来自客户机的网络请求，并为其分配IP地址以及PXE引导的相关信息（比如TFTP服务器地址和引导文件路径）。

**PXE客户端的工作流程**

* **PXE启动**：客户机通过网络接口卡（NIC）的PXE支持启动，并发出网络启动的请求。

* **获取IP地址**：PXE客户机向DHCP服务器请求IP地址。Cobbler服务器的DHCP服务响应该请求并提供IP地址及相关的网络启动信息。

* **访问TFTP服务器获取启动文件**：客户机使用从DHCP获取的信息，通过TFTP协议与Cobbler服务器通信，下载启动文件。

* **加载并运行内存引导**：启动文件被加载到客户机的内存中，并开始执行。这通常是一个轻量级的操作系统映像或特定的引导程序，用于启动整个安装过程。

* **Cobbler安装界面**：此时，客户机在引导到安装环境后，通过Cobbler提供的界面进行交互，用户可以在此确认安装选项。

* **根据配置安装**：客户端根据用户确认的安装选项和kickstart文件（自动化安装脚本）开始安装过程；kickstart指定了分区、用户、软件包集等参数。

* **获取安装文件**：根据kickstart文件中定义的路径（通常是一个URL），客户端通过网络获取操作系统的安装文件。

* **操作系统安装**：在kickstart文件的指导下，客户端开始自动安装操作系统。这个过程包括对硬盘的分区、文件系统的创建、软件包的安装和配置等步骤。

通过上述的Cobbler和PXE工作流程，可以看到Cobbler扮演着集中式管理角色，协调网络引导、IP地址分配和操作系统自动化部署等任务，从而实现了大规模自动化部署和管理操作系统的能力。

# 4.3 Cobbler目录结构简介

## 4.3.1 Cobbler配置文件目录

Cobbler配置文件所在目录:/etc/cobbler：

```bash
/etc/cobbler                        # 配置文件目录
/etc/cobbler/settings               # cobbler主配置文件
/etc/cobbler/dhcp.template          # DHCP服务的配置模板
/etc/cobbler/tftpd.template         # tftp服务的配置模板
/etc/cobbler/rsync.template         # rsync服务的配置模板
/etc/cobbler/iso                    # iso模板配置文件目录
/etc/cobbler/pxe                    # pxe模板文件目录
/etc/cobbler/power                  # 电源的配置文件目录
/etc/cobbler/users.conf             # Web服务授权配置文件
/etc/cobbler/users.digest           # web访问的用户名密码配置文件
/etc/cobbler/dnsmasq.template       # DNS服务的配置模板
/etc/cobbler/modules.conf           # Cobbler模块配置文件
```

## 4.3.2 Cobbler数据目录

```shell
/var/lib/cobbler                    # Cobbler数据目录
/var/lib/cobbler/config             # 配置文件
/var/lib/cobbler/kickstarts         # 默认存放kickstart文件
/var/lib/cobbler/loaders            # 存放的各种引导程序
/var/www/cobbler                    # 系统安装镜像目录
/var/www/cobbler/ks_mirror          # 导入的系统镜像列表
/var/www/cobbler/images             # 导入的系统镜像启动文件
/var/www/cobbler/repo_mirror        #  yum源存储目录
```

## 4.3.3 Cobbler日志文

```shell
/var/log/cobbler                    # 日志目录
/var/log/cobbler/install.log        # 客户端系统安装日志
/var/og/cobbler/cobbler.log         # cobbler日志
```



# 4.4 部署Cobbler

## 4.4.1 IP规划

| 分类    | IP                        | netmask       | gateway       | 说明                                                         |
| ------- | ------------------------- | ------------- | ------------- | ------------------------------------------------------------ |
|         | 172.17.75.236             | 255.255.252.0 | 172.17.75.254 | cobbler manager地址                                          |
| cobbler | 172.10.0.1                | 255.255.255.0 | 172.10.0.255  | cobbler dhcp server地址(domain-name-servers)，**对应ESXi PXE网络** |
|         | 10.16.172.236             | 255.255.255.0 |               | 10G网络，cobbler挂载外部ISO镜像地址；也可使用cobbler manager地址（千兆网络） |
| DHCP    | 172.10.0.0                |               |               | DHCP server的subnet                                          |
|         |                           | 255.255.255.0 |               | DHCP option routers                                          |
|         |                           |               | 172.10.0.254  | DHCP option subnet-mask                                      |
|         | 172.10.0.100~172.10.0.200 |               |               | DHCP range dynamic-bootp                                     |

说明：

​    Cobbler必须要有PXE网络，同时推荐OS分区空间要>= 300G,或额外增加一个分区用于ISO挂载使用。只所以占用空间，更多是因为cobbler repo sync后将镜像中文件复制一份出来，建议删除repo，并增加定时任务清理存在的repo，以期保证空间的充足。

## 4.4.2 查看系统信息

```shell
[root@cobbler-236 ~]# cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core) 
[root@cobbler-236 ~]# uname -r
3.10.0-957.el7.x86_64
[root@cobbler-236 ~]# hostname -I
172.17.75.236 
[root@cobbler-236 ~]# 
```

## 4.4.3 配置IP

```shell
[root@cobbler-236 network-scripts]# pwd
/etc/sysconfig/network-scripts
[root@cobbler-236 network-scripts]# ls ifcfg-ens*
ifcfg-ens160  ifcfg-ens192  ifcfg-ens224
[root@cobbler-236 network-scripts]# cat ifcfg-ens160 
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens160
UUID=fad33a53-af8c-48dd-9cb9-46565a8cac98
DEVICE=ens160
ONBOOT=yes
IPADDR0=172.17.75.236
PREFIX=24
DNS1=8.8.8.8
DNS2=114.114.114.114
GATEWAY0=172.17.75.254
[root@cobbler-236 network-scripts]# cat ifcfg-ens192 
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=none
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens192
DEVICE=ens192
ONBOOT=yes
IPADDR=10.16.172.236
PREFIX=24
[root@cobbler-236 network-scripts]# cat ifcfg-ens224
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=none
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens224
DEVICE=ens224
ONBOOT=yes
IPADDR=172.10.0.1
PREFIX=24
[root@cobbler-236 network-scripts]# 
```

重启网络服务，并查看ip地址:


```shell
[root@cobbler-236 network-scripts]# systemctl restart network.service
[root@cobbler-236 network-scripts]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:9e:52:f0 brd ff:ff:ff:ff:ff:ff
    inet 172.17.75.236/22 brd 172.17.75.255 scope global noprefixroute ens160
       valid_lft forever preferred_lft forever
    inet6 fe80::1f1c:2a31:560d:b640/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:9e:aa:8b brd ff:ff:ff:ff:ff:ff
    inet 10.16.172.236/24 brd 10.16.172.255 scope global noprefixroute ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::ddb7:d654:f5be:b66a/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
4: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:9e:3a:2c brd ff:ff:ff:ff:ff:ff
    inet 172.10.0.1/24 brd 172.10.0.255 scope global noprefixroute ens224
       valid_lft forever preferred_lft forever
    inet6 fe80::6934:bda8:2fba:d5bd/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
[root@cobbler-236 network-scripts]# 
```

## 4.4.4 配置 ssh

默认 ssh_config 启用了 DNS 解析，导致每次远程 ssh 时都特别慢

```shell
[root@cobbler-236 ~]# sed -i 's%#UseDNS yes%UseDNS no%' /etc/ssh/sshd_config
[root@cobbler-236 ~]# service sshd restart
```

## 4.4.5 关闭防火墙、selinux等

### 4.4.5.1 关闭防火墙

```shell
systemctl stop firewalld.service        # 停止firewall
systemctl disable firewalld.service     # 禁止firewall开机启动
```

### 4.4.5.2 关闭SELinux

编辑`/etc/selinux/config`文件，将SELINUX的值设置为disabled，下次开机SELinux就不会启动了。接着再执行如下命令,注意 setenforce 后面有空格:

```setenforce 0 ```

查看SELinux状态,执行getenforce命令, Disabled 表示已经关闭了。

## 4.4.6 安装wget

```shell
yum -y install wget
```

## 4.4.7 安装epel源

cobbler由epel源提供，所以需要事先配置epel的yum源。

```wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo ```

这里使用的是阿里的epel源，你也可以直接 ```yum install epel-release ```

## 4.4.8 新增一个分区，增加ISO自动挂载

手动创建一个空的目录/var/www/cobbler，此时新增一个300~500G大小的分区（假如分区是sdb，以此为示例），执行 ```msfs -t xfs /dev/sdb```，并将该分区挂载到这个目录:

1) ```mkfs.xfs /dev/sdb ```

2) ```mount /dev/sdb /var/www/cobbler/```

3) ```使用blkid获取uuid ```

用于/etc/fstab文件的编辑，比如：

```shell
[root@cobbler-236 ~]# blkid 
/dev/mapper/centos-root: UUID="f43b464c-78b9-4877-9c9b-72c5f01eb69d" TYPE="xfs" 
/dev/sda2: UUID="bwMXPE-QMkC-gbwC-vCxn-q7W0-HCss-RBsmtK" TYPE="LVM2_member" 
/dev/sdb: UUID="eaa27ae0-63bd-4d9e-a683-35d785269848" TYPE="xfs" 
/dev/sda1: UUID="5d3aa690-2d88-45c3-b647-1efe372980b6" TYPE="xfs" 
/dev/mapper/centos-swap: UUID="cfcd9e7b-2b02-45fc-a097-21c3f871ea92" TYPE="swap" 
/dev/mapper/centos-home: UUID="82402837-18a5-471f-87f9-d50eb73914df" TYPE="xfs" 
[root@cobbler-236 ~]# 
```

增加如下信息：

```shell
10.16.172.101:/vol/share/Builds/buildwindow/ /mnt/buildwindow nfs rsize=8192,wsize=8192,timeo=14,intr
UUID=eaa27ae0-63bd-4d9e-a683-35d785269848  /var/www/cobbler        xfs     defaults        0 2
```

* /mnt/buildwindow 是挂载点，存放IP地址为10.16.172.101的NAS Server提供的ISO安装镜像文件。
* /var/www/cobbler 为cobbler数据目录，由于涉及到ISO文件的同步，所需空间可适当分配的大一点，比如500G。

## 4.4.9 安装cobbler

```yum -y install cobbler cobbler-web pykickstart debmirror httpd dhcp tftp-server xinetd syslinux ```

## 4.4.10 启动相关服务并设置开机自启

```shell
systemctl start httpd
systemctl enable httpd
systemctl start cobblerd
systemctl enable cobblerd
systemctl start rsyncd
systemctl enable rsyncd
# systemctl enable dhcpd
```

## 4.4.11 检查cobbler配置

通过cobbler自带的命令检查，而后逐一按提示解决。

```cobbler check ```

出现如下提示信息：

```shell
[root@cobbler-236 ~]# cobbler check
The following are potential configuration items that you may want to fix:

1 : The 'server' field in /etc/cobbler/settings must be set to something other than localhost, or kickstarting features will not work.  This should be a resolvable hostname or IP for the boot server as reachable by all machines that will use it.
2 : For PXE to be functional, the 'next_server' field in /etc/cobbler/settings must be set to something other than 127.0.0.1, and should match the IP of the boot server on the PXE network.
3 : SELinux is enabled. Please review the following wiki page for details on ensuring cobbler works correctly in your SELinux environment:
    https://github.com/cobbler/cobbler/wiki/Selinux
4 : change 'disable' to 'no' in /etc/xinetd.d/tftp
5 : Some network boot-loaders are missing from /var/lib/cobbler/loaders, you may run 'cobbler get-loaders' to download them, or, if you only want to handle x86/x86_64 netbooting, you may ensure that you have installed a *recent* version of the syslinux package installed and can ignore this message entirely.  Files in this directory, should you want to support all architectures, should include pxelinux.0, menu.c32, elilo.efi, and yaboot. The 'cobbler get-loaders' command is the easiest way to resolve these requirements.
6 : comment out 'dists' on /etc/debmirror.conf for proper debian support
7 : comment out 'arches' on /etc/debmirror.conf for proper debian support
8 : The default password used by the sample templates for newly installed machines (default_password_crypted in /etc/cobbler/settings) is still set to 'cobbler' and should be changed, try: "openssl passwd -1 -salt 'random-phrase-here' 'your-password-here'" to generate new one
9 : fencing tools were not found, and are required to use the (optional) power management features. install cman or fence-agents to use them

Restart cobblerd and then run 'cobbler sync' to apply changes.
[root@cobbler-236 ~]# 
```

如上各问题的解决方法如下所示：

1、修改/etc/cobbler/settings文件，将默认server的127.0.0.1替换为本机IP地址(cobbler地址)

```sed -i 's#^server: 127.0.0.1#server: 172.10.0.1#' /etc/cobbler/settings ```

2、修改/etc/cobbler/settings文件，将默认next_server的127.0.0.1替换为本机IP地址

```sed -i 's#^next_server: 127.0.0.1#next_server: 172.10.0.1#' /etc/cobbler/settings ```


3、将/etc/xinetd.d/tftp中disable改为no

```disable = no ```

4、执行 ```cobbler get-loaders ``` 命令即可

可能会出现timeout，没关系，多执行几次，直到成功为止（会出现TASK COMPLETE）。

5、注释/etc/debmirror.conf文件中的@dists="sid";一行

```sed -i 's/@dists="sid";/#@dists="sid";/' /etc/debmirror.conf ```

6、注释/etc/debmirror.conf文件中的@arches="i386";一行

```sed -i 's/@arches="i386";/#@arches="i386";/' /etc/debmirror.conf ```

7、 防止循环装系统，适用于服务器第一启动项是PXE启动。
```sed -i 's/pxe_just_once: 0/pxe_just_once: 1/' /etc/cobbler/settings ```

8、设置新系统默认的root密码

执行  ```openssl passwd -1 -salt $(openssl rand -hex 4) ``` 生成密码，并用其替换/etc/cobbler/settings文件中default_password_crypted参数的值；

```shell
[root@cobbler-236 ~]# openssl passwd -1 -salt $(openssl rand -hex 4)
Password: 
$1$2a25cee5$NK/O/uGlcl3tue7mc/Iy5/
[root@cobbler-236 ~]# 
```

```shell
vi /etc/cobbler/settings

default_password_crypted: "$1$2a25cee5$NK/O/uGlcl3tue7mc/Iy5/"
```

## 4.4.12 安装其他包

```shell
yum -y install fence-agents
yum -y install perl-JSON-PP
```

## 4.4.13 重启cobblerd并同步检查

```shell
systemctl restart cobblerd
cobbler sync
cobbler check
```


如果出现如下信息，表明check ok：

```shell
[root@cobbler-236 ~]# cobbler check
No configuration problems found.  All systems go.
[root@cobbler-236 ~]# 
```

## 4.4.14 通过cobbler来管理dhcp

```shell
[root@cobbler-236 ~]# sed -i 's#manage_dhcp: 0#manage_dhcp: 1#' /etc/cobbler/settings
```

## 4.4.15 配置DHCP服务

```vi /etc/cobbler/dhcp.template ```

```shell
subnet 172.10.0.0 netmask 255.255.255.0 {
     option routers             172.10.0.254;
     option domain-name-servers 172.10.0.1;
     option subnet-mask         255.255.255.0;
     range dynamic-bootp        172.10.0.100 172.10.0.200;
     default-lease-time         21600;
     max-lease-time             43200;
     next-server                $next_server;
     class "pxeclients" {
          match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
          if option pxe-system-type = 00:02 {
                  filename "ia64/elilo.efi";
          } else if option pxe-system-type = 00:06 {
                  filename "grub/grub-x86.efi";
          } else if option pxe-system-type = 00:07 {
                  filename "grub/grub-x86_64.efi";
          } else if option pxe-system-type = 00:09 {
                  filename "grub/grub-x86_64.efi";
          } else {
                  filename "pxelinux.0";
          }
     }

}
```

然后重启cobbler服务并同步配置

```shell
systemctl restart cobblerd
cobbler sync
```

# 4.5 部署Nginx

## 4.5.1 安装Nginx

`yum -y install nginx`

安装的版本为：

```shell
[root@cobbler-236 ~]# nginx -v
nginx version: nginx/1.16.1
[root@cobbler-236 ~]# 
```

如果要卸载的话，执行 ```yum -y remove nginx   ```

## 4.5.2 设置开机启动

```systemctl enable nginx```

其他指令参考如下：

```shell
service nginx start      # 启动 nginx 服务
service nginx stop       # 停止 nginx 服务
service nginx restart    # 重启 nginx 服务
service nginx reload     # 重新加载配置，一般是在修改过 nginx 配置文件时使用。
```

## 4.5.3 配置Nginx

由于Nginx默认使用80端口，而80端口又被cobbler web占用，需要修改Nginx的默认端口，以及Nginx的其他配置，下文结束修改/etc/nginx/nginx.conf。

### 4.5.1 修改Nginx启用账号

默认是nginx这个账号启用nginx服务的，需要改成root

```shell
user root;
```

### 4.5.2 修改默认端口

下面改成81：

```shell
        listen       81 default_server;
        listen       [::]:81 default_server;
```

### 4.5.3 指定location

```shell
        location / {
            root /var/www/html;
            autoindex on;
        }
```

同时，执行如下命令：

```shell
cd /var/www
rm -rf html
ln -s /var/lib/tftpboot /var/www/html
```

/etc/nginx/nginx.conf内容参考如下：

<img class="shadow" src="/img/in-post/cobbler/image-20200927163055922.png" width="1200">

### 4.5.4 autoinit.sh配置文件的存放


autiinit.sh脚本，作用于通过PXE网络安装OS最后时刻，修改apache2.conf，修改ssh_config，重置avahi扫描网络所需的配置信息（避免节点avahi config中配置的IP是PXE网络的IP，而非预期设定的public或storage或class网络），内容参考如下：


```shell
#!/bin/sh
sed -i 's/KeepAlive On/KeepAlive Off/' /etc/apache2/apache2.conf;
sed -i.bak 's/^#\ \ \ StrictHostKeyChecking ask/\ \ \ \ StrictHostKeyChecking no/' /etc/ssh/ssh_config
python -c "from ezs3.utils import start_web_ui,start_freenode_service;start_web_ui();start_freenode_service()"
python -c "from ezs3.config import Ezs3CephConfig; Ezs3CephConfig()"
sed -i '/\/root\/autoinit.sh/d' /etc/rc.local
```

将autoinit.sh脚本，复制到 /var/lib/tftpboot/netconf/目录下：

```shell
cp autoinit.sh /var/lib/tftpboot/netconf/
```



# 4.6 手动安装实践

## 4.6.1 安装CentOS7

### 4.6.1.1 导入镜像

以官方CentOS为示例，先在cobbler对应vm上挂载iso，然后ssh到后端执行：

```mount /dev/cdrom  /mnt/ ```

在导入期间，可以在后端查看导入进程信息：

```shell
[root@cobbler-236 ~]# ps -ef |grep rsync
root      4661     1  0 Sep13 ?        00:00:00 /usr/bin/rsync --daemon --no-detach
root     14477 12531 21 23:09 ?        00:00:02 rsync -a /mnt/ /var/www/cobbler/ks_mirror/centos-7-x86_64 --progress
root     14478 14477  0 23:09 ?        00:00:00 rsync -a /mnt/ /var/www/cobbler/ks_mirror/centos-7-x86_64 --progress
root     14479 14478 35 23:09 ?        00:00:04 rsync -a /mnt/ /var/www/cobbler/ks_mirror/centos-7-x86_64 --progress
root     14497 12822  0 23:10 pts/3    00:00:00 grep --color=auto rsync
[root@cobbler-236 ~]# 
```

如果rsync进程消失，表明import结束：

```shell
[root@localhost network-scripts]# ps -ef | grep rsync
root      4854     1  0 Sep16 ?        00:00:00 /usr/bin/rsync --daemon --no-detach
root     11284  9927  0 11:12 pts/0    00:00:00 grep --color=auto rsync
[root@localhost network-scripts]# 
```

导入完成后生成的文件夹

```shell
[root@cobbler-236 ks_mirror]# pwd
/var/www/cobbler/ks_mirror
[root@cobbler-236 ks_mirror]# ll
total 0
drwxrwxr-x  8 root root 254 Nov 26  2018 centos-7-x86_64
drwxr-xr-x. 2 root root  62 Sep 17 11:12 config
[root@cobbler-236 ks_mirror]# 
```

### 4.6.1.2 编辑kickstart文件

vi /var/lib/cobbler/kickstarts/CentOS-7-x86_64.cfg


```shell
# Centos7
# This kickstart file should only be used with EL > 5 and/or Fedora > 7.
# For older versions please use the sample.ks kickstart file.
 
#platform=x86, AMD64, or Intel EM64T
# System authorization information
auth --useshadow --passalgo=sha512
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all --initlabel
# Use text mode install
text
# Firewall configuration
firewall --disable
# Run the Setup Agent on first boot
firstboot --disable
ignoredisk --only-use=sda
# System keyboard
keyboard us
# System language
lang en_US
# Use network installation
url --url=$tree
# If any cobbler repo definitions were referenced in the kickstart profile, include them here.
$yum_repo_stanza
# Network information
$SNIPPET('network_config')
# Reboot after installation
reboot
 
#Root password
rootpw --iscrypted $default_password_crypted
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
skipx
# System timezone
timezone Asia/Shanghai
# Install OS instead of upgrade
install
# Clear the Master Boot Record
zerombr
# Allow anaconda to partition the system as needed
part /boot --fstype="xfs" --size=300 --ondisk=sda
part swap --fstype="swap" --size=2048 --ondisk=sda
part / --fstype="xfs" --grow --size=1 --ondisk=sda
 
%pre
 
$SNIPPET('log_ks_pre')
$SNIPPET('kickstart_start')
$SNIPPET('pre_install_network_config')
# Enable installation monitoring
$SNIPPET('pre_anamon')
%end
 
 
%packages
 
@^minimal
@core
kexec-tools
%end
 
 
%post
 
systemctl disable postfix.service
%end
```

### 4.6.1.3 修改kickstart文件为自定义的CentOS-7-x86_64.cfg

cobbler profile edit --name=CentOS-7-x86_64 --kickstart=/var/lib/cobbler/kickstarts/CentOS-7-x86_64.cfg


用cobbler profile report查看，Kickstart前后信息已经改变

```shell
[root@cobbler-236 kickstarts]# cobbler profile report
Name                           : centos-7-x86_64
TFTP Boot Files                : {}
Comment                        : 
DHCP Tag                       : default
Distribution                   : centos-7-x86_64
Enable gPXE?                   : 0
Enable PXE Menu?               : 1
Fetchable Files                : {}
Kernel Options                 : {}
Kernel Options (Post Install)  : {}
Kickstart                      : /var/lib/cobbler/kickstarts/sample_end.ks
Kickstart Metadata             : {}
Management Classes             : []
Management Parameters          : <<inherit>>
Name Servers                   : []
Name Servers Search Path       : []
Owners                         : ['admin']
Parent Profile                 : 
Internal proxy                 : 
Red Hat Management Key         : <<inherit>>
Red Hat Management Server      : <<inherit>>
Repos                          : []
Server Override                : <<inherit>>
Template Files                 : {}
Virt Auto Boot                 : 1
Virt Bridge                    : xenbr0
Virt CPUs                      : 2
Virt Disk Driver Type          : raw
Virt File Size(GB)             : 5
Virt Path                      : 
Virt RAM (MB)                  : 4096
Virt Type                      : kvm

[root@cobbler-236 kickstarts]# cobbler profile edit --name=CentOS-7-x86_64 --kickstart=/var/lib/cobbler/kickstarts/CentOS-7-x86_64.cfg
[root@cobbler-236 kickstarts]# cobbler profile report
Name                           : CentOS-7-x86_64
TFTP Boot Files                : {}
Comment                        : 
DHCP Tag                       : default
Distribution                   : centos-7-x86_64
Enable gPXE?                   : 0
Enable PXE Menu?               : 1
Fetchable Files                : {}
Kernel Options                 : {}
Kernel Options (Post Install)  : {}
Kickstart                      : /var/lib/cobbler/kickstarts/CentOS-7-x86_64.cfg
Kickstart Metadata             : {}
Management Classes             : []
Management Parameters          : <<inherit>>
Name Servers                   : []
Name Servers Search Path       : []
Owners                         : ['admin']
Parent Profile                 : 
Internal proxy                 : 
Red Hat Management Key         : <<inherit>>
Red Hat Management Server      : <<inherit>>
Repos                          : []
Server Override                : <<inherit>>
Template Files                 : {}
Virt Auto Boot                 : 1
Virt Bridge                    : xenbr0
Virt CPUs                      : 2
Virt Disk Driver Type          : raw
Virt File Size(GB)             : 5
Virt Path                      : 
Virt RAM (MB)                  : 4096
Virt Type                      : kvm

[root@cobbler-236 kickstarts]# 
```

### 4.6.1.4 重启xinetd服务

```systemctl restart xinetd```

### 4.6.1.5 安装系统系统后，自动设定IP地址

```shell
[root@cobbler-236 ~]# cobbler system add --name=CentOS-7-x86_64 --mac=00:50:56:9e:ee:2e  --profile=CentOS-7-X86_64  --ip-address=172.17.73.76 --subnet=255.255.252.0 --gateway=172.17.75.254 --interface=eth0 --static=1 --hostname=wyz_au01 --name-servers="114.114.114.114 8.8.8.8"
[root@cobbler-236 ~]# cobbler system list
   CentOS-7-x86_64
[root@cobbler-236 ~]# cobbler sync
task started: 2020-09-17_165512_sync

```

网络组bond：

4个网口：

```shell
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=eth0 --mac=00:50:56:9e:ee:2e --interface-type=bond_slave --interface-master=bond0
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=eth1 --mac=00:50:56:9e:ee:2e --interface-type=bond_slave --interface-master=bond0
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=bond0 --interface-type=bond --bonding-opts="mode=active-backup miimon=100" --ip-address=172.17.73.76 --subnet=255.255.252.0 --gateway=172.17.75.254 --static=1

cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=eth2 --mac=00:50:56:9e:cc:0c --interface-type=bond_slave --interface-master=bond1
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=eth3 --mac=00:50:56:9e:cc:0c --interface-type=bond_slave --interface-master=bond1
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=bond1 --interface-type=bond --bonding-opts="mode=active-backup miimon=100" --ip-address=10.1.1.76 --subnet=255.255.255.0 --static=1
```

2个网口：

```shell
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=eth0 --mac=00:50:56:9e:ee:2e --interface-type=bond_slave --interface-master=bond0
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=eth1 --mac=00:50:56:9e:cc:0c --interface-type=bond_slave --interface-master=bond1
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=bond0 --interface-type=bond --bonding-opts="mode=active-backup miimon=100" --ip-address=172.17.73.76 --subnet=255.255.252.0 --gateway=172.17.75.254 --static=1
cobbler system edit --name=CentOS-7-x86_64 --profile=CentOS-7-X86_64 --interface=bond1 --interface-type=bond --bonding-opts="mode=active-backup miimon=100" --ip-address=10.1.1.76 --subnet=255.255.255.0 --static=1
```

## 4.6.2 Ububtu 安装

这个以公司存储软件产品为示例。

### 4.6.2.1 挂载镜像

```shell
cd /var/www/cobbler/ks_mirror
mkdir Scaler-8.0-latest
mount /mnt/buildwindow/xenial/virtualstor_scaler_8.0/builds/2020-09-25_00_33_00/VirtualStor\ Scaler-v8.0-413-xenial~202009250033~5f910ea.iso /var/www/cobbler/ks_mirror/Scaler-8.0-latest
```

### 4.6.2.2 导入镜像

```shell
cobbler import --path=/var/www/cobbler/ks_mirror/Scaler-8.0-latest --name=Scaler-8.0-latest-x86_64  --arch=x86_64
```

### 4.6.2.3 新增system config

<img class="shadow" src="/img/in-post/cobbler/image-20200925172717405.png" width="1200">

<img class="shadow" src="/img/in-post/cobbler/image-20200925172726750.png" width="1200">

`00:50:56:9e:4c:12` 是被安装系统所在VM的PXE网络对应的mac地址

<img class="shadow" src="/img/in-post/cobbler/image-20200925172807485.png" width="1200">

<img class="shadow" src="/img/in-post/cobbler/image-20200925172816714.png" width="1200">

<img class="shadow" src="/img/in-post/cobbler/image-20200925172829380.png" width="1200">

其他页面未截图，表明使用默认设置。然后重启vm，自动进入安装界面，如下图所示：

<img class="shadow" src="/img/in-post/cobbler/install_selection.png" width="1200">


# 4.7 自动化安装脚本的使用


## 4.7.1 必要的安装包


```shell
yum -y install python3
yum -y install python3-pip
yum -y install vim
yum -y install nfs-utils
yum -y install net-tools
yum -y install tmux
pip3 install pyVmomi
```

## 4.7.2 相关脚本/模板准备

对于Ubuntu下的Scaler版本，无需任何手工干预，其preseed文件目前是基于ISO自动生成，并存放于 ```/var/lib/tftpboot/netconf ```对应版本（安装脚本**PXE_MAP**处定义的版本信息）目录下，参考如下：

```shell
[root@cobbler-236 netconf]# ll
total 32
drwxr-xr-x  2 root root   72 Dec 27  2020 6.1
drwxr-xr-x  2 root root  186 Mar  4  2021 7.0
drwxr-xr-x  3 root root 4096 May 16  2021 8.0
drwxr-xr-x 19 root root  311 Apr  6  2021 8.0_centos
drwxr-xr-x  2 root root   35 Oct 22  2020 8.0_converger_one_1.0
drwxr-xr-x  3 root root   22 Jan 16  2023 8.0_kylin
drwxr-xr-x  2 root root 8192 Mar 17  2021 8.0_u3
drwxr-xr-x 17 root root  313 Nov 18  2020 8.0_u3_centos
drwxr-xr-x  4 root root 4096 Nov  8  2022 8.2
drwxr-xr-x  9 root root  117 Apr  1  2021 8.2_centos
drwxr-xr-x  5 root root 4096 Apr 17  2023 8.3
drwxr-xr-x 25 root root 4096 Dec  5  2022 8.3_centos
-rwxr-xr-x  1 root root  405 Sep 27  2020 autoinit.sh
[root@cobbler-236 netconf]#  cd 8.3
[root@cobbler-236 8.3]# ll
total 21
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-11
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-12
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-13
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-14
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-15
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-16
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-17
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-18
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-19
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-20
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-21
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-22
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-23
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-24
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-25
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-26
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-FC-57
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-FC-58
-rw-r--r-- 1 root root 551 May  4  2023 interfaces_pytest-83-FC-59
[root@cobbler-236 netconf]# cd ../8.3_centos/
[root@cobbler-236 8.3_centos]# ll
total 0
drwxr-xr-x 2 root root 104 Aug  5  2021 8.3-74
drwxr-xr-x 2 root root 104 Aug  5  2021 8.3-75
drwxr-xr-x 2 root root  84 Aug  5  2021 8.3-76
drwxr-xr-x 2 root root  84 Aug  5  2021 8.3-node76
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-11
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-12
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-13
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-14
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-15
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-16
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-17
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-18
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-19
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-20
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-21
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-22
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-23
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-24
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-25
drwxr-xr-x 2 root root  84 Jul 30  2022 pytest-83-26
[root@cobbler-236 8.3_centos]# cd pytest-83-11/
[root@cobbler-236 pytest-83-11]# ll
total 16
-rw-r--r-- 1 root root 206 Aug  1  2022 ifcfg-bond0
-rw-r--r-- 1 root root 165 Aug  1  2022 ifcfg-bond1
-rw-r--r-- 1 root root  79 Aug  1  2022 ifcfg-ens192
-rw-r--r-- 1 root root  79 Aug  1  2022 ifcfg-ens224
[root@cobbler-236 pytest-83-11]# 
```

而对于CentOS Scaler来说，需要先将 ```centos-ezs3-auto-8.0.ks ``` 这个模板，事先存放在```/var/lib/cobbler/templates ```目录下，当前ks文件，支持CentOS下的Scaler-8.0&Scaler-8.2&Scaler-8.3版本的安装，如果将来有其他版本的CentOS，可能需要额外调整安装脚本或新增ks文件。

## 4.7.3 配置文件准备

此工具支持物理机和虚拟机的批量部署，虚拟机则支持ESXi和PVE两个虚拟化平台下的VM批量安装，在设置配置文件时有些许差异。

我们先来看一个完整的安装VM的参考示例，如下（可以在“vms”中以{}形式，增加其他安装节点）：

```shell
{
    "ostype":"ubuntu",    # 表示是Ubuntu系统
    "version":"8.3",      # 表示的是安装Scaler 8.3版本的ISO
    "isopath":"latest",   # 表示安装最新的Scaler 8.3 ISO
    "vmyesno":"yes",      # yes表示是VM；no表示是物理机
    "esxuser":"root",     # ESXi的超级用户名
    "esxpass":"password", # ESXi超级用户对应的密码
    "disknum":2,          # 表示给VM分配2块虚拟化磁盘（不含OS disk的磁盘数）
    "disksize":50,        # 每个磁盘空间大小是50G，单位是GiB哦
    "osdisk":"yes",       # 此块磁盘是OS disk
    "osdisksize":60,      # OS disk size是60G
    "vms":[
        {
            "hostname":"cobbler-83",    # 要安装的VM的hostname
            "esxhost":"172.17.75.184",  # ESXi宿主机IP
            "datastore":"rdqa02",       # "vmyesno":"no"
            "os_disk":"/dev/sda",       # 操作系统对应的分区名称
            "disknum":6,                # 给VM分配6块磁盘，不含OS disk，这里会覆盖上一层的“disknum":2参数值
            "disksize":30,              # 每个分区大小是30G，里会覆盖上一层的"disksize":50参数值
            "netconf":[                 # VM的网络配置信息，OS安装好后自动生成相关网络配置文件
                {
                    "iface":"bond0",
                    "slave":[
                        "ens160"
                    ],
                    "bond_mode":"active-backup",
                    "address":"172.17.73.81",
                    "netmask":"255.255.252.0",
                    "gateway":"172.17.75.254",
                    "dns-nameservers":"114.114.114.114"
                },
                {
                    "iface":"bond1",
                    "slave":[
                        "ens192"
                    ],
                    "bond_mode":"active-backup",
                    "address":"1.1.1.81",
                    "netmask":"255.255.255.0"
                }
            ]
        }
    ]
}
```

如果是部署在物理设备上（"vmyesno":"no"），需要对应物理机配置IPMI相关信息：

```shell
{
    "ostype":"centos",    # 表明安装的是CentOS 版本的 Scaler产品
    "version":"8.3",      # 安装Scaler 8.3版本
    "isopath":"latest",   # 可以指定具体ISO版本所在的路径；latest表示安装最新版本
    "vmyesno":"no",       # 表明ISO被安装到物理机器上
    "ipmiuser":"ADMIN",   # IPMI超级管理员账号
    "ipmipass":"ADMIN",   # IPMI超级管理员账号的密码
    "vms":[
        {
            "hostname":"node246",        # ISO安装好后，对应物理机的hostname
            "ipmiaddr":"172.17.75.212",  # 物理机所在的IPMI IP地址
            "os_disk":"/dev/sda",        # 指定OS分区
            "pxeint":"eth1",             # 指定PXE网络网口信息，由于Lab网络固定，基本不需修改
            "netconf":[                  # 被安装物理机的网络配置信息，3个网络，一个千兆，两个10G
                {
                    "iface":"bond0",
                    "slave":[
                        "enp5s0f0"
                    ],
                    "bond_mode":"active-backup",
                    "address":"172.17.73.246",
                    "netmask":"255.255.252.0",
                    "gateway":"172.17.75.254",
                    "dns-nameservers":"114.114.114.114"
                },
                {
                    "iface":"bond1",
                    "slave":[
                        "enp130s0f0"
                    ],
                    "bond_mode":"active-backup",
                    "address":"10.16.172.246",
                    "netmask":"255.255.255.0"
                },
                {
                    "iface":"bond2",
                    "slave":[
                        "enp130s0f1"
                    ],
                    "bond_mode":"active-backup",
                    "address":"10.10.10.246",
                    "netmask":"255.255.255.0"
                }
            ]
        }
    ]
}
```

如果指定具体安装版本，参考如下：

```shell
"isopath":"/mnt/buildwindow/xenial/virtualstor_scaler_8.3/builds/dana/VirtualStor Scaler-v8.3-439-xenial~202304190031~0e01482.iso",
```

目前支持安装的版本信息（对应配置文件中的"version"字段）：

```shell
PXE_MAP = {
    "6.1": {
        "buildpath":     "precise/virtualstor_scaler_6.1/",
        "pxeint":        ["eth0", "eth1", "eth2"]
    },
    "6.3": {
        "buildpath":     "precise/virtualstor_scaler_6.3/",
        "pxeint":        ["eth0", "eth1", "eth2"]
    },
    "7.0": {
        "buildpath":     "trusty/virtualstor_scaler_7.0/",
        "pxeint":        ["eth0", "eth1", "eth2"]
    },
    "7s": {
        "buildpath":     "trusty/virtualstor_7s/",
        "pxeint":        ["eth0", "eth1", "eth2"]
    },
    "8.0": {
        "buildpath":     "xenial/virtualstor_scaler_8.0/scaler",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.0_centos": {
        "buildpath":     "centos7/virtualstor_scaler_8.0/scaler",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.0_converger_one_1.0": {
        "buildpath":     "buster/virtualstor_converger_one_1.0/",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.2": {
        "buildpath":     "xenial/virtualstor_scaler_8.2/scaler",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.2_centos": {
        "buildpath":     "centos7/virtualstor_scaler_8.2/scaler",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.3": {
        "buildpath":     "xenial/virtualstor_scaler_8.3/scaler",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.3_centos": {
        "buildpath":     "centos7/virtualstor_scaler_8.3/scaler",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "master": {
        "buildpath":     "xenial/virtualstor_scaler_master/scaler",
        "pxeint":        ["ens160", "ens192", "ens224"]
    }
}
```

* 8.3 表示版本为8.0的Ubuntu类型的Scaler
* 8.3_centos 表示版本为8.0的CentOS类型的Scaler
* 8.0_converger_one_1.0 表示版本为8.0的ConvergerOne

上述值目前写死在code中，所以json格式的配置文件中```"version":```的取值要去适配自己要安装的什么产品类型的ISO。随着产品版本的拓展，需适时修改此版本映射关系表。

## 4.7.4 批量部署脚本代码说明

脚本目录结构如下：

```shell
.
├── batch_install.py
├── cone_server.py
├── esxi_server.py
├── logger_batch_install.py
└── tools
    ├── alarm.py
    ├── cli.py
    ├── cluster.py
    ├── datacenter.py
    ├── __init__.py
    ├── interactive_wrapper.py
    ├── pchelper.py
    ├── README.md
    ├── serviceutil.py
    ├── tasks.py
    └── vm.py

2 directories, 15 files
```

文件说明如下：

* `batch_install.py`：执行总入口，负责调用`esxi_server.py`和`cone_server.py`中提供的接口，完成Cobbler相关配置的设定，ISO的挂载，pressed文件的生成，安装ISO，以及安装检查。
* `cone_server.py`：基于`proxmoxer`，实现PVE虚拟化平台下VM的配置与批量安装。
* `esxi_server.py`：基于`pyVim`和`pyVmomi`，实现VMWare ESXi虚拟化平台下VM的配置与批量安装。
* `logger_batch_install.py`：封装的日志记录器，记录整个安装过程的详细日志。
* `tool`： pyvmomi-community-samples samples.tools，为`esxi_server.py`提供基础功能的调用。

由于代码体量比较多，这里借助`pyreverse`生成类图，就不做代码细节介绍了，类图参考如下：

```shell
[root@cobbler-236 batch_install]# pyreverse -ASmy -o png *
```

<img class="shadow" src="/img/in-post/cobbler/packages.png" width="800">

<img class="shadow" src="/img/in-post/cobbler/classes.png" width="800">


## 4.7.5 安装过程

如下，根据在PVE虚拟化平台下批量部署VM的过程日志，来介绍一下完整的自动批量部署ISO过程。

### 4.7.5.1 创建VM

如果VM存在（ESXi根据对应宿主机下VM名称判断；PVE则根据对应宿主机下VM id判断），先删除再创建

```shell
2023-05-04 13:29:22,213 batch_install.py[line:494 ] [WARNING] Virtual machine [pytest-83-11] already exists, delete then create it again
2023-05-04 13:29:33,962 batch_install.py[line:494 ] [WARNING] Virtual machine [pytest-83-12] already exists, delete then create it again
.....................................  省略................................
2023-05-04 13:32:52,216 batch_install.py[line:494 ] [WARNING] Virtual machine [pytest-83-FC-58] already exists, delete then create it again
2023-05-04 13:33:03,935 batch_install.py[line:494 ] [WARNING] Virtual machine [pytest-83-FC-59] already exists, delete then create it again
```

### 4.7.5.2 获取被安装VM的PXE网络IP地址

```shell
2023-05-04 13:33:17,492 batch_install.py[line:350 ] [DEBUG] Get mac address
2023-05-04 13:33:24,579 batch_install.py[line:408 ] [DEBUG] PXE info of pytest-83-11 : ens224 --> 9A:06:4A:A6:A1:07
2023-05-04 13:33:24,579 batch_install.py[line:408 ] [DEBUG] PXE info of pytest-83-11 : ens224 --> 9A:06:4A:A6:A1:07
.....................................  省略................................
2023-05-04 13:33:24,585 batch_install.py[line:408 ] [DEBUG] PXE info of pytest-83-FC-59 : ens224 --> 5A:A4:89:66:00:67
2023-05-04 13:33:24,585 batch_install.py[line:408 ] [DEBUG] PXE info of pytest-83-FC-59 : ens224 --> 5A:A4:89:66:00:67
```

### 4.7.5.3 自动生成网络配置文件和pressed文件

如果是Ubuntu，根据ISO自动生成pressed文件；如果是CentOS或Kylin，读取默认目录下配置好的ks文件。

```shell
2023-05-04 13:33:24,585 batch_install.py[line:543 ] [INFO ] Start to generate Ubuntu netconf for pytest-83-11, file path : (/var/lib/tftpboot/netconf/8.3/interfaces_pytest-83-11)
2023-05-04 13:33:24,594 batch_install.py[line:569 ] [INFO ] Generate netconf for pytest-83-11: /var/lib/tftpboot/netconf/8.3/interfaces_pytest-83-11
2023-05-04 13:33:25,660 batch_install.py[line:644 ] [INFO ] Generate preseed for pytest-83-11: /var/lib/tftpboot/preseed/8.3/ubuntu-ezs3-pytest-83-11.seed
2023-05-04 13:33:25,661 batch_install.py[line:543 ] [INFO ] Start to generate Ubuntu netconf for pytest-83-12, file path : (/var/lib/tftpboot/netconf/8.3/interfaces_pytest-83-12)
2023-05-04 13:33:25,662 batch_install.py[line:569 ] [INFO ] Generate netconf for pytest-83-12: /var/lib/tftpboot/netconf/8.3/interfaces_pytest-83-12
2023-05-04 13:33:25,690 batch_install.py[line:644 ] [INFO ] Generate preseed for pytest-83-12: /var/lib/tftpboot/preseed/8.3/ubuntu-ezs3-pytest-83-12.seed
2023-05-04 13:33:25,691 batch_install.py[line:543 ] [INFO ] Start to generate Ubuntu netconf for pytest-83-13, file path : (/var/lib/tftpboot/netconf/8.3/interfaces_pytest-83-13)
.....................................  省略................................
2023-05-04 13:33:26,203 batch_install.py[line:569 ] [INFO ] Generate netconf for pytest-83-FC-59: /var/lib/tftpboot/netconf/8.3/interfaces_pytest-83-FC-59
2023-05-04 13:33:26,230 batch_install.py[line:644 ] [INFO ] Generate preseed for pytest-83-FC-59: /var/lib/tftpboot/preseed/8.3/ubuntu-ezs3-pytest-83-FC-59.seed
```

### 4.7.5.4 清理cobbler repos

为了防止cobbler server空间被耗尽，需清除repos来释放空间。

```shell
2023-05-04 13:33:26,231 batch_install.py[line:1526] [INFO ] Start to clean cobbler repos to release disk space
2023-05-04 13:33:26,537 batch_install.py[line:1110] [DEBUG] cobbler repo list, res is : ()
2023-05-04 13:33:26,537 batch_install.py[line:1532] [INFO ] End to clean cobbler repos to release disk space
```

### 4.7.5.5 挂载ISO镜像

```shell
2023-05-04 13:33:26,538 batch_install.py[line:1132] [DEBUG] version : (8.3)
2023-05-04 13:33:26,552 batch_install.py[line:1201] [INFO ] Mount ISO by command : (mount '/mnt/buildwindow/xenial/virtualstor_scaler_8.3/scaler/2023-04-29/VirtualStor Scaler-v8.3-506-xenial~202304290434~7fa3878.iso' /var/www/cobbler/ks_mirror/Scaler-8.3-latest)
2023-05-04 13:33:26,559 batch_install.py[line:1211] [INFO ] Start to mount /mnt/buildwindow/xenial/virtualstor_scaler_8.3/scaler/2023-04-29/VirtualStor Scaler-v8.3-506-xenial~202304290434~7fa3878.iso to /var/www/cobbler/ks_mirror/Scaler-8.3-latest
2023-05-04 13:33:26,573 batch_install.py[line:1170] [INFO ] Check mount path : (/var/www/cobbler/ks_mirror/Scaler-8.3-latest)
2023-05-04 13:33:26,580 batch_install.py[line:1174] [INFO ] Mount ISO : (/mnt/buildwindow/xenial/virtualstor_scaler_8.3/scaler/2023-04-29/VirtualStor Scaler-v8.3-506-xenial~202304290434~7fa3878.iso) success
```

### 4.7.5.6 删除陈旧的cobbler system信息

```shell
2023-05-04 13:33:26,894 batch_install.py[line:1110] [DEBUG] cobbler distro list, res is : (   Scaler-8.3-latest-hwe-x86_64
   Scaler-8.3-latest-x86_64
)
2023-05-04 13:33:26,894 batch_install.py[line:1252] [INFO ] Has been imported the ISO before, now destroy cobbler configuration then create
2023-05-04 13:33:27,211 batch_install.py[line:1110] [DEBUG] cobbler system list, res is : (   Scaler-8.3-latest-pytest-83-11-x86_64
   Scaler-8.3-latest-pytest-83-12-x86_64
   Scaler-8.3-latest-pytest-83-13-x86_64
   Scaler-8.3-latest-pytest-83-14-x86_64
   Scaler-8.3-latest-pytest-83-15-x86_64
   Scaler-8.3-latest-pytest-83-16-x86_64
   Scaler-8.3-latest-pytest-83-17-x86_64
   Scaler-8.3-latest-pytest-83-18-x86_64
   Scaler-8.3-latest-pytest-83-19-x86_64
   Scaler-8.3-latest-pytest-83-20-x86_64
   Scaler-8.3-latest-pytest-83-21-x86_64
   Scaler-8.3-latest-pytest-83-22-x86_64
   Scaler-8.3-latest-pytest-83-23-x86_64
   Scaler-8.3-latest-pytest-83-24-x86_64
   Scaler-8.3-latest-pytest-83-25-x86_64
   Scaler-8.3-latest-pytest-83-26-x86_64
   Scaler-8.3-latest-pytest-83-FC-57-x86_64
   Scaler-8.3-latest-pytest-83-FC-58-x86_64
   Scaler-8.3-latest-pytest-83-FC-59-x86_64
)
2023-05-04 13:33:33,166 batch_install.py[line:1257] [DEBUG] Delete system and profile
2023-05-04 13:33:33,166 batch_install.py[line:1261] [INFO ] Delete system : (Scaler-8.3-latest-pytest-83-11-x86_64)
2023-05-04 13:33:33,493 batch_install.py[line:1261] [INFO ] Delete system : (Scaler-8.3-latest-pytest-83-12-x86_64)
.....................................  省略................................
2023-05-04 13:33:39,126 batch_install.py[line:1263] [INFO ] Delete profile : (Scaler-8.3-latest-x86_64)
2023-05-04 13:33:40,491 batch_install.py[line:1275] [INFO ] Delete distro : (Scaler-8.3-latest-x86_64)
2023-05-04 13:33:40,877 batch_install.py[line:1522] [INFO ] cobbler sync
2023-05-04 13:33:45,189 batch_install.py[line:1365] [INFO ] Import ISO, command is : (cobbler import --path=/var/www/cobbler/ks_mirror/Scaler-8.3-latest --name=Scaler-8.3-latest --arch=x86_64)
2023-05-04 13:35:04,907 batch_install.py[line:1110] [DEBUG] cobbler distro list, res is : (   Scaler-8.3-latest-hwe-x86_64
   Scaler-8.3-latest-x86_64
)
```

### 4.7.5.7 import ISO

```shell
2023-05-04 13:35:04,908 batch_install.py[line:1376] [INFO ] Import ISO : (/mnt/buildwindow/xenial/virtualstor_scaler_8.3/scaler/2023-04-29/VirtualStor Scaler-v8.3-506-xenial~202304290434~7fa3878.iso) success
2023-05-04 13:35:04,908 batch_install.py[line:1221] [DEBUG] Start to view profile kickstart --> Scaler-8.3-latest-x86_64
2023-05-04 13:35:05,241 batch_install.py[line:1231] [DEBUG] View profile kickstart --> Scaler-8.3-latest-x86_64 success
2023-05-04 13:35:05,241 batch_install.py[line:1397] [INFO ] Create and edit system configuration, profile name :(Scaler-8.3-latest-x86_64)
2023-05-04 13:35:05,507 batch_install.py[line:1110] [DEBUG] cobbler system list, res is : ()
2023-05-04 13:35:05,507 batch_install.py[line:1412] [DEBUG] pxe_mac 9A:06:4A:A6:A1:07, pxe_nic ens224, pub_mac 9A:06:4A:A6:A1:07, pub_nic ens224, sto_mac 9A:06:4A:A6:A1:07, sto_nic ens224
# Create cobbler system
2023-05-04 13:35:05,518 batch_install.py[line:1482] [DEBUG] Create cobbler system : (cobbler system add --name=Scaler-8.3-latest-pytest-83-11-x86_64 --profile=Scaler-8.3-latest-x86_64 --hostname=pytest-83-11 --ksmeta='os_disk_path=/dev/sda country=en_US enable_debugger=1 keep_netboot=1' --kopts='interface=9A:06:4A:A6:A1:07' --kickstart=/var/lib/cobbler/kickstarts/ubuntu-ezs3-pytest-83-11.seed --interface=ens224 --mac=9A:06:4A:A6:A1:07 --template-files=/var/lib/cobbler/templates/sources.list.template=/etc/apt/sources.list)
2023-05-04 13:35:05,853 batch_install.py[line:1491] [DEBUG] Edit cobbler system : (cobbler system edit --name=Scaler-8.3-latest-pytest-83-11-x86_64 --profile=Scaler-8.3-latest-pytest-83-11-x86_64 --interface=ens224 --mac=9A:06:4A:A6:A1:07)
2023-05-04 13:35:06,395 batch_install.py[line:1110] [DEBUG] cobbler system list, res is : (   Scaler-8.3-latest-pytest-83-11-x86_64
)
2023-05-04 13:35:06,395 batch_install.py[line:1502] [INFO ] Add cobbler system : (Scaler-8.3-latest-pytest-83-11-x86_64) success
2023-05-04 13:35:06,395 batch_install.py[line:1221] [DEBUG] Start to view system kickstart --> Scaler-8.3-latest-pytest-83-11-x86_64
2023-05-04 13:35:06,698 batch_install.py[line:1231] [DEBUG] View system kickstart --> Scaler-8.3-latest-pytest-83-11-x86_64 success
2023-05-04 13:35:06,699 batch_install.py[line:1412] [DEBUG] pxe_mac 82:9C:DB:B2:C7:2A, pxe_nic ens224, pub_mac 82:9C:DB:B2:C7:2A, pub_nic ens224, sto_mac 82:9C:DB:B2:C7:2A, sto_nic ens224
2023-05-04 13:35:06,705 batch_install.py[line:1482] [DEBUG] Create cobbler system : (cobbler system add --name=Scaler-8.3-latest-pytest-83-12-x86_64 --profile=Scaler-8.3-latest-x86_64 --hostname=pytest-83-12 --ksmeta='os_disk_path=/dev/sda country=en_US enable_debugger=1 keep_netboot=1' --kopts='interface=82:9C:DB:B2:C7:2A' --kickstart=/var/lib/cobbler/kickstarts/ubuntu-ezs3-pytest-83-12.seed --interface=ens224 --mac=82:9C:DB:B2:C7:2A --template-files=/var/lib/cobbler/templates/sources.list.template=/etc/apt/sources.list)
2023-05-04 13:35:07,009 batch_install.py[line:1491] [DEBUG] Edit cobbler system : (cobbler system edit --name=Scaler-8.3-latest-pytest-83-12-x86_64 --profile=Scaler-8.3-latest-pytest-83-12-x86_64 --interface=ens224 --mac=82:9C:DB:B2:C7:2A)
.....................................  省略................................
2023-05-04 13:35:26,792 batch_install.py[line:1482] [DEBUG] Create cobbler system : (cobbler system add --name=Scaler-8.3-latest-pytest-83-FC-59-x86_64 --profile=Scaler-8.3-latest-x86_64 --hostname=pytest-83-FC-59 --ksmeta='os_disk_path=/dev/sda country=en_US enable_debugger=1 keep_netboot=1' --kopts='interface=5A:A4:89:66:00:67' --kickstart=/var/lib/cobbler/kickstarts/ubuntu-ezs3-pytest-83-FC-59.seed --interface=ens224 --mac=5A:A4:89:66:00:67 --template-files=/var/lib/cobbler/templates/sources.list.template=/etc/apt/sources.list)
2023-05-04 13:35:27,086 batch_install.py[line:1491] [DEBUG] Edit cobbler system : (cobbler system edit --name=Scaler-8.3-latest-pytest-83-FC-59-x86_64 --profile=Scaler-8.3-latest-pytest-83-FC-59-x86_64 --interface=ens224 --mac=5A:A4:89:66:00:67)
2023-05-04 13:35:27,615 batch_install.py[line:1110] [DEBUG] cobbler system list, res is : (   Scaler-8.3-latest-pytest-83-11-x86_64
   Scaler-8.3-latest-pytest-83-12-x86_64
   Scaler-8.3-latest-pytest-83-13-x86_64
   Scaler-8.3-latest-pytest-83-14-x86_64
   Scaler-8.3-latest-pytest-83-15-x86_64
   Scaler-8.3-latest-pytest-83-16-x86_64
   Scaler-8.3-latest-pytest-83-17-x86_64
   Scaler-8.3-latest-pytest-83-18-x86_64
   Scaler-8.3-latest-pytest-83-19-x86_64
   Scaler-8.3-latest-pytest-83-20-x86_64
   Scaler-8.3-latest-pytest-83-21-x86_64
   Scaler-8.3-latest-pytest-83-22-x86_64
   Scaler-8.3-latest-pytest-83-23-x86_64
   Scaler-8.3-latest-pytest-83-24-x86_64
   Scaler-8.3-latest-pytest-83-25-x86_64
   Scaler-8.3-latest-pytest-83-26-x86_64
   Scaler-8.3-latest-pytest-83-FC-57-x86_64
   Scaler-8.3-latest-pytest-83-FC-58-x86_64
   Scaler-8.3-latest-pytest-83-FC-59-x86_64
)
2023-05-04 13:35:27,615 batch_install.py[line:1502] [INFO ] Add cobbler system : (Scaler-8.3-latest-pytest-83-FC-59-x86_64) success
```

### 4.7.5.8 检查ks文件准确性

这一步是为了防止产品发生变化，导致ks文件发生变化，避免生成的pressed文件或指定的ks文件与最新版本不匹配，做防呆用。

```shell
2023-05-04 13:35:27,615 batch_install.py[line:1221] [DEBUG] Start to view system kickstart --> Scaler-8.3-latest-pytest-83-FC-59-x86_64
2023-05-04 13:35:27,916 batch_install.py[line:1231] [DEBUG] View system kickstart --> Scaler-8.3-latest-pytest-83-FC-59-x86_64 success
```

### 4.7.5.9 cobbler sync

cobbler相关配置都设定好后，需要同步一下，告知cobbler后续需使用最新的cobbler system， repo等信息进行镜像安装。

```shell
2023-05-04 13:35:27,916 batch_install.py[line:1522] [INFO ] cobbler sync
```

### 4.7.5.10 机器上电

机器上电后自动进入安装界面。

```shell
2023-05-04 13:35:30,225 batch_install.py[line:986 ] [INFO ] COne, start to power on VM [pytest-83-11] to install ISO.
2023-05-04 13:35:30,432 batch_install.py[line:1019] [DEBUG] Power on VM : (['pytest-83-11']) from COne
2023-05-04 13:35:30,579 batch_install.py[line:986 ] [INFO ] COne, start to power on VM [pytest-83-12] to install ISO.
2023-05-04 13:35:30,779 batch_install.py[line:1019] [DEBUG] Power on VM : (['pytest-83-12']) from COne
.....................................  省略................................
2023-05-04 13:35:36,538 batch_install.py[line:986 ] [INFO ] COne, start to power on VM [pytest-83-FC-59] to install ISO.
2023-05-04 13:35:36,711 batch_install.py[line:1019] [DEBUG] Power on VM : (['pytest-83-FC-59']) from COne
```

### 4.7.5.11 等待安装结束

这个过程会持续比较久，如果宿主机比较清闲，安装速度会快一些，Lab中这套虚拟化环境，安装一个节点基本上要在1个小时左右。

```shell
2023-05-04 13:35:36,818 batch_install.py[line:1022] [INFO ] All nodes are reset, please wait for install finished...
2023-05-04 13:36:31,834 batch_install.py[line:1089] [DEBUG] 0 nodes finished.
2023-05-04 13:37:57,539 batch_install.py[line:1089] [DEBUG] 0 nodes finished.
.....................................  省略................................
2023-05-04 14:34:45,375 batch_install.py[line:1089] [DEBUG] 1 nodes finished.
2023-05-04 14:36:09,120 batch_install.py[line:1089] [DEBUG] 1 nodes finished.
2023-05-04 14:37:32,798 batch_install.py[line:1089] [DEBUG] 1 nodes finished.
2023-05-04 14:38:56,536 batch_install.py[line:1089] [DEBUG] 1 nodes finished.
2023-05-04 14:40:20,953 batch_install.py[line:1089] [DEBUG] 1 nodes finished.
2023-05-04 14:41:45,710 batch_install.py[line:1089] [DEBUG] 1 nodes finished.
2023-05-04 14:43:09,449 batch_install.py[line:1089] [DEBUG] 1 nodes finished.
2023-05-04 14:44:28,045 batch_install.py[line:1089] [DEBUG] 5 nodes finished.
2023-05-04 14:45:46,545 batch_install.py[line:1089] [DEBUG] 5 nodes finished.
2023-05-04 14:47:03,842 batch_install.py[line:1089] [DEBUG] 6 nodes finished.
2023-05-04 14:48:21,427 batch_install.py[line:1089] [DEBUG] 6 nodes finished.
2023-05-04 14:49:39,573 batch_install.py[line:1089] [DEBUG] 6 nodes finished.
2023-05-04 14:50:55,579 batch_install.py[line:1089] [DEBUG] 7 nodes finished.
2023-05-04 14:52:08,954 batch_install.py[line:1089] [DEBUG] 9 nodes finished.
2023-05-04 14:53:22,245 batch_install.py[line:1089] [DEBUG] 9 nodes finished.
2023-05-04 14:54:34,275 batch_install.py[line:1089] [DEBUG] 10 nodes finished.
2023-05-04 14:55:46,306 batch_install.py[line:1089] [DEBUG] 10 nodes finished.
2023-05-04 14:56:58,327 batch_install.py[line:1089] [DEBUG] 10 nodes finished.
2023-05-04 14:58:09,815 batch_install.py[line:1089] [DEBUG] 11 nodes finished.
2023-05-04 14:59:20,536 batch_install.py[line:1089] [DEBUG] 11 nodes finished.
2023-05-04 15:00:28,697 batch_install.py[line:1089] [DEBUG] 13 nodes finished.
2023-05-04 15:01:34,496 batch_install.py[line:1089] [DEBUG] 14 nodes finished.
2023-05-04 15:02:37,547 batch_install.py[line:1089] [DEBUG] 17 nodes finished.
2023-05-04 15:03:37,894 batch_install.py[line:1089] [DEBUG] 19 nodes finished.
2023-05-04 15:03:37,894 batch_install.py[line:1096] [INFO ] All nodes are installed!
```

通过`curl`发起HTTP请求到被安装OS的某个服务，校验此服务的API是否有响应，如果响应状态码为预期状态码，则认为此节点已经成功安装好了。每次均间隔1分钟检查一次，如果超过2个小时依然有节点没有回预期的响应状态码，则认为安装超时，自动退出安装。



## 4.7.6 与Jenkins的结合

在创建Jenkins pipeline project时，设置`String parameter`，如下图所示：

<img class="shadow" src="/img/in-post/cobbler/jenkins_bat_install_parameter.png" width="800">

定义一个变量`BAT_INSTALL`，指向批量安装脚本所在路径与携带的配置文件。除此之外，还需在`pipeline script`中指明`BAT_INSTALL` Server IP地址：

```shell
        /* Install VM by PVE */
        stage("Initialize") {
                steps {
                    script {
                            sh """
                            #!/bin/bash -xe
                            echo "Call batch_install_vs.py to install ISO."
                            sshpass -p 1 ssh -p 22 172.17.75.236 -l root \${BAT_INSTALL}
                            """
                        }
                }
            }
```

当然，你也可以定义一个`String parameter`变量作为`BAT_INSTALL_SERVER`，然后在`pipeline script`中使用这个变量。

由于Cobbler Server 与 Jenkins Server是不同的机器，直接`sshpass`会失败，所以呢，还需要建立Cobbler Server 与 Jenkins Server之间的ssh互信关系。

至此，当Jenkins Server触发CI构建时，自动调用Cobbler Server上的批量安装脚本进行ISO的安装。



# 4.8 本章小结

本章节中，我们详细介绍了搭建cobbler及示例自动部署coentos和自动化批量部署分布式存储软件ISO包的过程，以及如何支持物理设备、ESXi和PVE虚拟化设备下的批量部署，并与Jenkins结合实现每天自动、批量部署最新产品ISO。

我们首先介绍了cobbler工具的概念和作用。cobbler是一个自动化部署系统，可以帮助我们快速部署操作系统和其他软件。我们了解了cobbler的基本原理和核心功能，并学习了如何安装和配置cobbler。

接着，我们详细讨论了示例自动部署coentos的过程。我们了解了如何准备coentos ISO镜像文件，并通过cobbler进行自动化部署。我们学习了如何创建和配置cobbler profile、kickstart文件和DHCP设置，以实现自动化部署过程。

我们进一步探讨了自动化批量部署分布式存储软件ISO包的方法。我们了解了如何准备存储软件的ISO镜像文件，并通过cobbler进行批量部署。我们学习了如何创建和配置cobbler profile、kickstart文件和DHCP设置，以及如何与Jenkins结合实现每天自动、批量部署最新产品ISO。
