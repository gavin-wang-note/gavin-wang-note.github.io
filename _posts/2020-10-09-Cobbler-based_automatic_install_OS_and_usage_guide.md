---
layout:     post
title:      "基于Cobbler二次开发，实现自动安装ISO文件部署OS"
subtitle:   "Cobbler-based automatic install OS and usage guide"
date:       2020-10-09
author:     "Gavin Wang"
catalog:    true
summary: "基于Cobbler二次开发，实现自动获取ISO文件和部署不同类型的Linux OS"
top: true
categories:
    - [cobbler]
    - [Automation]
tags:
    - cobbler
    - Automation
---


# IP规划



| 分类    | IP                        | netmask       | gateway       | 说明                                                         |
| ------- | ------------------------- | ------------- | ------------- | ------------------------------------------------------------ |
|         | 172.17.75.236             | 255.255.252.0 | 172.17.75.254 | cobbler manager地址                                          |
| cobbler | 172.10.0.1                | 255.255.255.0 | 172.10.0.255  | cobbler dhcp server地址(domain-name-servers)，**对应ESXi PXE网络** |
|         | 10.16.172.236             | 255.255.255.0 |               | cobbler挂载外部ISO镜像地址，也可使用cobbler manager地址      |
| DHCP    | 172.10.0.0                |               |               | DHCP server的subnet                                          |
|         |                           | 255.255.255.0 |               | DHCP option routers                                          |
|         |                           |               | 172.10.0.254  | DHCP option subnet-mask                                      |
|         | 172.10.0.100~172.10.0.200 |               |               | DHCP range dynamic-bootp                                     |



说明：

​    cobbler必须要有PXE网络，同时推荐OS分区空间要>= 300G,或额外增加一个分区用于ISO挂载使用。只所以占用空间，更多是因为cobbler repo sync后将镜像中文件复制一份出来，建议删除repo，并增加定时任务清理存在的repo，以期保证空间的充足。



# 部署cobbler



## 查看系统信息



```shell
[root@cobbler-236 ~]# cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core) 
[root@cobbler-236 ~]# uname -r
3.10.0-957.el7.x86_64
[root@cobbler-236 ~]# hostname -I
172.17.75.236 
[root@cobbler-236 ~]# 
```



## 配置IP



```shell
[root@cobbler-236 network-scripts]# pwd
/etc/sysconfig/network-scripts
[root@cobbler-236 network-scripts]# ls ifcfg-ens*
ifcfg-ens160  ifcfg-ens192
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
    link/ether 00:50:56:9e:8c:1e brd ff:ff:ff:ff:ff:ff
    inet 172.17.75.236/16 brd 172.17.255.255 scope global noprefixroute ens160
       valid_lft forever preferred_lft forever
    inet6 fe80::4d94:54dc:9eb2:2864/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:9e:07:2b brd ff:ff:ff:ff:ff:ff
    inet 172.10.0.1/24 brd 172.10.0.255 scope global noprefixroute ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::ddb7:d654:f5be:b66a/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
[root@cobbler-236 network-scripts]# 
```



## 配置 ssh



默认 ssh_config 启用了 DNS 解析，导致每次远程 ssh 时都特别慢

```shell
[root@cobbler-236 ~]# sed -i 's%#UseDNS yes%UseDNS no%' /etc/ssh/sshd_config
[root@cobbler-236 ~]# service sshd restart
```



## 关闭防火墙、selinux等



### 关闭防火墙



```shell
systemctl stop firewalld.service        # 停止firewall
systemctl disable firewalld.service     # 禁止firewall开机启动
```



### 关闭SELinux



编辑/etc/selinux/config文件，将SELINUX的值设置为disabled，下次开机SELinux就不会启动了。接着再执行如下命令,注意 setenforce 后面有空格:

```shell
setenforce 0
```

查看SELinux状态,执行getenforce命令, Disabled 表示已经关闭了。



## 安装wget

```shell
yum -y install wget
```



## 安装epel源

cobbler由epel源提供，所以需要事先配置epel的yum源。

```wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo ```

这里使用的是阿里的epel源，你也可以直接 ```yum install epel-release ```



## 新增一个分区，增加ISO自动挂载



手动创建一个空的目录/var/www/cobbler，此时新增一个300~500G大小的分区（假如分区是sdb，以此为示例），执行 ```msfs -t xfs /dev/sdb```，并将该分区挂载到这个目录:

1) ```mkfs.xfs /dev/sdb ```

2) ```mount /dev/sdb /var/www/cobbler/```

3) ```使用blkid获取uuid ```

用于/etc/fstab文件的编辑,比如：

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

```shell
10.16.172.101:/vol/share/Builds/buildwindow/ /mnt/buildwindow nfs rsize=8192,wsize=8192,timeo=14,intr
UUID=eaa27ae0-63bd-4d9e-a683-35d785269848  /var/www/cobbler        xfs     defaults        0 2
```



## 安装cobbler



```shell
yum -y install cobbler cobbler-web pykickstart debmirror httpd dhcp tftp-server xinetd syslinux
```



## 启动相关服务并设置开机自启



```shell
systemctl start httpd
systemctl enable httpd
systemctl start cobblerd
systemctl enable cobblerd
systemctl start rsyncd
systemctl enable rsyncd
# systemctl enable dhcpd
```



## 检查cobbler配置



通过cobbler自带的命令检查，而后逐一按提示解决。

```shell
cobbler check
```

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



## 安装其他包



```shell
yum -y install fence-agents
yum -y install perl-JSON-PP
```



## 重启cobblerd并同步检查



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



## 通过cobbler来管理dhcp



```shell
[root@cobbler-236 ~]# sed -i 's#manage_dhcp: 0#manage_dhcp: 1#' /etc/cobbler/settings
```



## 配置DHCP服务



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





# 部署Nginx



## 安装Nginx



`yum -y install nginx`



安装的版本为：

```shell
[root@cobbler-236 ~]# nginx -v
nginx version: nginx/1.16.1
[root@cobbler-236 ~]# 
```



如果要卸载的话，执行 ```yum -y remove nginx   ```



## 设置开机启动



```systemctl enable nginx```



其他指令参考如下：

```shell
service nginx start      # 启动 nginx 服务
service nginx stop       # 停止 nginx 服务
service nginx restart    # 重启 nginx 服务
service nginx reload     # 重新加载配置，一般是在修改过 nginx 配置文件时使用。
```



## 配置Nginx

由于Nginx默认使用80端口，而80端口又被cobbler web占用，需要修改Nginx的默认端口，以及Nginx的其他配置，下文结束修改/etc/nginx/nginx.conf。



### 1. 修改Nginx启用账号

默认是nginx这个账号启用nginx服务的，需要改成root

```shell
user root;
```



### 2. 修改默认端口

下面改成81：

```shell
        listen       81 default_server;
        listen       [::]:81 default_server;
```

​      

### 3. 指定location

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



### 4. autoinit.sh配置文件的存放


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





# 手动安装实践



## 安装CentOS7



### 1. 导入镜像：

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



### 2. 编辑kickstart文件

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



### 3. 修改kickstart文件为自定义的CentOS-7-x86_64.cfg

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



### 4. 重启xinetd服务

systemctl restart xinetd





### 5. 安装系统系统后，自动设定IP地址

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

说明：

​    上面bond信息仅供参考，并未执行成功，即未正常形成bond关系。



安装参考：

https://blog.csdn.net/admin_root1/article/details/84965608





## Ububtu 安装

这个以我们产品为示例。



### 1. 挂载镜像
```shell
cd /var/www/cobbler/ks_mirror
mkdir Scaler-8.0-latest
mount /mnt/buildwindow/xenial/virtualstor_scaler_8.0/builds/2020-09-25_00_33_00/VirtualStor\ Scaler-v8.0-413-xenial~202009250033~5f910ea.iso /var/www/cobbler/ks_mirror/Scaler-8.0-latest
```



### 2. 导入镜像
```shell
cobbler import --path=/var/www/cobbler/ks_mirror/Scaler-8.0-latest --name=Scaler-8.0-latest-x86_64  --arch=x86_64
```



### 3. 新增system config


<img class="shadow" src="/img/in-post/cobbler/image-20200925172717405.png" width="1200">

<img class="shadow" src="/img/in-post/cobbler/image-20200925172726750.png" width="1200">



00:50:56:9e:4c:12 是被安装系统所在VM的PXE网络对应的mac地址



<img class="shadow" src="/img/in-post/cobbler/image-20200925172807485.png" width="1200">

<img class="shadow" src="/img/in-post/cobbler/image-20200925172816714.png" width="1200">

<img class="shadow" src="/img/in-post/cobbler/image-20200925172829380.png" width="1200">


其他页面未截图，表明使用默认设置。



然后重启vm，自动进入安装界面。




# 自动化安装脚本的使用


## 必要的安装包


```shell
yum -y install python3
yum -y install python3-pip
yum -y install vim
yum -y install nfs-utils
yum -y install net-tools
yum -y install tmux
pip3 install pyVmomi
```



## 相关脚本/模板准备



对于Ubuntu Scaler，无需任何手工干预，其preseed文件目前是自动生成，存放于 ```/var/lib/tftpboot/netconf ```对应版本（安装脚本**PXE_MAP**处定义的版本信息）目录下，参考如下：

```shell
[root@cobbler-236 netconf]# ls -l
total 8
drwxr-xr-x 2 root root 4096 Oct  3 18:15 8.0
drwxr-xr-x 3 root root   31 Sep 29 16:06 8.0_centos
-rwxr-xr-x 1 root root  405 Sep 27 10:59 autoinit.sh
[root@cobbler-236 netconf]# 
[root@cobbler-236 netconf]# ls -lR
.:
total 8
drwxr-xr-x 2 root root 4096 Oct  3 18:15 8.0
drwxr-xr-x 3 root root   31 Sep 29 16:06 8.0_centos
-rwxr-xr-x 1 root root  405 Sep 27 10:59 autoinit.sh

./8.0:
total 68
-rw-r--r-- 1 root root 557 Oct  2 22:09 interfaces_cobbler-80
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-11
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-12
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-13
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-14
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-15
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-16
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-17
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-18
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-19
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-20
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-21
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-22
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-23
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-24
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-25
-rw-r--r-- 1 root root 555 Oct  9 16:02 interfaces_pytest-80-26

./8.0_centos:
total 0
drwxr-xr-x 2 root root 84 Sep 29 16:06 cobbler-centos-80

./8.0_centos/cobbler-centos-80:
total 16
-rw-r--r-- 1 root root 206 Oct  9 16:37 ifcfg-bond0
-rw-r--r-- 1 root root 165 Oct  9 16:37 ifcfg-bond1
-rw-r--r-- 1 root root  79 Oct  9 16:37 ifcfg-ens160
-rw-r--r-- 1 root root  79 Oct  9 16:37 ifcfg-ens192
[root@cobbler-236 netconf]#
```



而对于CentOS Scaler来说，需要先将 ```centos-ezs3-auto-8.0.ks ``` 这个模板，事先存放在```/var/lib/cobbler/templates ```目录下，当前ks文件，仅支持8.0的CentOS下Scaler的安装，如果将来有其他版本的CentOS，可能需要额外调整安装脚本/新增ks文件。





## VM配置文件准备



参考示例如下（可以在“vms”中以{}形式，增加其他节点信息）：

```shell
{
    "ostype":"ubuntu",
    "version":"8.0",
    "isopath":"latest",
    "vmyesno":"yes",
    "esxuser":"root",
    "esxpass":"p@ssw0rd",
    "disknum":2,
    "disksize":50,
    "osdisk":"yes",
    "osdisksize":60,
    "vms":[
        {
            "hostname":"cobbler-80",
            "esxhost":"172.17.75.184",
            "datastore":"rdqa02",
            "os_disk":"/dev/sda",
            "disknum":6,
            "disksize":30,
            "netconf":[
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





对于配置文件中版本信息：



```shell
    "8.0": {
        "buildpath":     "xenial/virtualstor_scaler_8.0/",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.0_centos": {
        "buildpath":     "centos7/virtualstor_scaler_8.0/",
        "pxeint":        ["ens160", "ens192", "ens224"]
    },
    "8.0_converger1": {
        "buildpath":     "buster/virtualstor_converger_one_1.0/",
        "pxeint":        ["ens160", "ens192", "ens224"]
    }
```



* 8.0 表示版本为8.0的Ubuntu类型的Scaler
* 8.0_centos 表示版本为8.0的CentOS类型的Scaler
* 8.0_converger1 表示版本为8.0的ConvergerOne

上述值目前写死在code中，所以json格式的配置文件中```"version":```的取值要去适配自己要安装的什么产品类型的ISO。





# 其他



如何判断ks文件有效性



```shell
# yum install pykickstart
```

After installing the package, you can validate a Kickstart file using the following command:

```shell
$ ksvalidator /path/to/kickstart.ks
```



参考：

https://docs.centos.org/en-US/centos/install-guide/Kickstart2/

