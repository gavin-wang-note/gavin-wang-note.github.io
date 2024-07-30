---
layout:     post
title:      "kerberos安装与客户端配置"
subtitle:   "Deploy kerberos"
date:       2023-02-17
author:     "Gavin Wang"
catalog:    true
categories:
    - [kerberos]
tags:
    - kerberos
---

# 概述

由于产品有使用到kerberos做NFS Auth, 近期环境出现异常，也没有文档记录kerberos安装过程，故重新部署并记录文档。



# 环境规划

在部署之前一定要提前规划好角色、域名以及IP地址，否则会出现异常

系统: ubuntu-18.04.6-desktop-amd64.iso，主机名与地址配置:

| 角色  |   全称域名（FQDN） | IP地址  |
| ------- | --------------------------------- |--------------------------------- |
| Kadmin KDC  |  kadminkdc.njqa.com  |  172.17.75.240 |
| kerberos client1 |  kclient241.njqa.com | 172.17.75.241  |
| kerberos client2 |  kclient242.njqa.com | 172.17.75.242  |
| Scaler集群       |  scaler.njqa.com     | 172.17.72.11; 172.17.72.12;172.17.72.13  |


添加域名映射到/etc/hosts文件中，确保集群和kdc以及client可以通过全称域名互相访问（若有DNS服务器更好，可以避免一些奇怪的问题）

多节点集群每个节点都应当配置好hosts，否则不能在集群配置界面配置kerberos服务器为全称域名

```shell
172.17.75.240   kadminkdc.njqa.com      kadminkdc
172.17.75.241   kclient241.njqa.com     kclient241
172.17.75.242   kclient242.njqa.com     kclient242

172.17.72.111   scaler.njqa.com    node111
172.17.72.112   scaler.njqa.com    node112
172.17.72.113   scaler.njqa.com    node113
```

# 集群为多节点情况下需要所有节点都配置映射到一个域名

Kerberos服务器对时间较为敏感，可以在KDC和kerberos client上配置NTP同步时间,Scaler集群自带NTP服务

```shell
apt-get install ntp -y
```

另外若有防火墙需要先将防火墙关闭ufw disable,或者让防火墙允许Kerberos服务通过

# 配置KDC和kadmin

## 安装相关组件 

```shell
apt-get install krb5-kdc krb5-admin-server
```

安装完成后会弹出Kerberos的配置界面，该配置界面也可以使用命令dpkg-reconfigure krb5-kdc来打开


### 填写Realm，Kerberos的Realm为大写，我们使用NJQA.COM

<img class="shadow" src="/img/in-post/kerberos/kerberos-1.png" width="1200">

设置Kerberos server，为我们的Kerberos主机名，按照规划应当填入kadminkdc.njqa.com，图中仅作参考

<img class="shadow" src="/img/in-post/kerberos/kerberos-2.png" width="1200">

设置Administrative server，因为我们只有一台KDC服务器，所以设置为这台Kerberos的主机名，按照规划应当填入kadminkdc.njqa.com ，图中仅作参考

<img class="shadow" src="/img/in-post/kerberos/kerberos-3.png" width="1200">

### 创建Kerberos数据库，里面维护着认证系统中所有主机的密码

krb5_newrealm 按照提示设置密码即可

<img class="shadow" src="/img/in-post/kerberos/kerberos-4.png" width="1200">

### 为Kerberos添加一个管理员帐号，以管理认证系统中的principal，再添加三个principals，两个用于client，另一个用于scaler集群

```shell
root@kdc:~# kadmin.local
Authenticating as principal root/admin@NJQA.COM with password.
kadmin.local:  ank root/admin@NJQA.COM                                                           #管理员账号
WARNING: no policy specified for root/admin@NJQA.COM; defaulting to no policy
Enter password for principal "root/admin@NJQA.COM": 
Re-enter password for principal "root/admin@NJQA.COM": 
Principal "root/admin@NJQA.COM" created.
kadmin.local:  
kadmin.local:  ank host/kclient241.njqa.com@NJQA.COM                                               #Kerberos client1
WARNING: no policy specified for host/kclient241.njqa.com@NJQA.COM; defaulting to no policy
Enter password for principal "host/kclient241.njqa.com@NJQA.COM": 
Re-enter password for principal "host/kclient241.njqa.com@NJQA.COM": 
Principal "host/kclient241.njqa.com@NJQA.COM" created.

kadmin.local:  ank host/kclient242.njqa.com@NJQA.COM                                               #Kerberos client2
WARNING: no policy specified for host/kclient242.njqa.com@NJQA.COM; defaulting to no policy
Enter password for principal "host/kclient242.njqa.com@NJQA.COM": 
Re-enter password for principal "host/kclient242.njqa.com@NJQA.COM": 
Principal "host/kclient242.njqa.com@NJQA.COM" created.

kadmin.local:  ank nfs/scaler.njqa.com@NJQA.COM                                                  #Cluster
WARNING: no policy specified for nfs/scaler.njqa.com@NJQA.COM; defaulting to no policy
Enter password for principal "nfs/scaler.njqa.com@NJQA.COM": 
Re-enter password for principal "nfs/scaler.njqa.com@NJQA.COM": 
Principal "nfs/scaler.njqa.com@NJQA.COM" created.
```

### 为 kadmind 服务创建一个密钥表文件

此命令序列创建一个包含 kadmin/<FQDN> 和 kadmin/changepw 的主体项的特殊密钥表文件。kadmind 服务需要使用这些主体，要更改口令也需要使用这些主体。请注意，当主体实例为主机名时，无论 /etc/resolv.conf 文件中的域名是大写还是小写，都必须以小写字母指定FQDN。

```shell
kadmin.local: ktadd -k /etc/krb5/kadm5.keytab kadmin/kadminkdc.njqa.com@NJQA.COM
Entry for principal kadmin/kadminkdc.example.com@NJQA.COM with kvno 3, encryption type AES-256 CTS mode
          with 96-bit SHA-1 HMAC added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/kadminkdc.example.com@NJQA.COM with kvno 3, encryption type AES-128 CTS mode
          with 96-bit SHA-1 HMAC added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/kadminkdc.example.com@NJQA.COM with kvno 3, encryption type Triple DES cbc
          mode with HMAC/sha1 added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/kadminkdc.example.com@NJQA.COM with kvno 3, encryption type ArcFour
          with HMAC/md5 added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/kadminkdc.example.com@NJQA.COM with kvno 3, encryption type DES cbc mode
          with RSA-MD5 added to keytab WRFILE:/etc/krb5/kadm5.keytab.

kadmin.local: ktadd -k /etc/krb5/kadm5.keytab kadmin/changepw@NJQA.COM
Entry for principal kadmin/changepw@NJQA.COM with kvno 3, encryption type AES-256 CTS mode
          with 96-bit SHA-1 HMAC added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/changepw@NJQA.COM with kvno 3, encryption type AES-128 CTS mode
          with 96-bit SHA-1 HMAC added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/changepw@NJQA.COM with kvno 3, encryption type Triple DES cbc
          mode with HMAC/sha1 added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/changepw@NJQA.COM with kvno 3, encryption type ArcFour
          with HMAC/md5 added to keytab WRFILE:/etc/krb5/kadm5.keytab.
Entry for principal kadmin/changepw@NJQA.COM with kvno 3, encryption type DES cbc mode
          with RSA-MD5 added to keytab WRFILE:/etc/krb5/kadm5.keytab.
kadmin.local:
```

### 运行以下命令（这两个deamon需要保持运行状态）

```shell
krb5kdc
kadmind
```

### 编辑配置文件


```shell
vim /etc/krb5.conf

[logging]
        default = FILE:/var/log/krb5.log
        kdc = FILE:/var/log/krb5kdc.log
        admin_server = FILE:/var/log/kadmind.log


[libdefaults]
        default_realm = NJQA.COM
        dns_lookup_kdc = true
        dns_lookup_realm = true
        ticket_lifetime = 24000 
        clock_skew = 300
        kdc_timesync = 1
        ccache_type = 4
        forwardable = true
        proxiable = true


[realms]
        NJQA.COM = {
                kdc = kdc
                admin_server = kdc
        }

[domain_realm]
        .NJQA.COM = NJQA.COM
        NJQA.COM = NJQA.COM


vim /etc/krb5kdc/kdc.conf

[kdcdefaults]
    kdc_ports = 750,88

[realms]
    NJQA.COM = {
        database_name = /var/lib/krb5kdc/principal
        admin_keytab = FILE:/etc/krb5kdc/kadm5.keytab
        acl_file = /etc/krb5kdc/kadm5.acl
        key_stash_file = /etc/krb5kdc/stash
        kdc_ports = 750,88
        max_life = 10h 0m 0s
        max_renewable_life = 7d 0h 0m 0s
        master_key_type = des3-hmac-sha1
        supported_enctypes = aes256-cts:normal arcfour-hmac:normal des3-hmac-sha1:normal des-cbc-crc:normal des:normal des:v4 des:norealm des:onlyrealm des:afs3                                                 
        default_principal_flags = +preauth
    }

```

* /etc/krb5.conf中原本内容删除，替换成上面的内容
* /etc/krb5kdc/kdc.conf中将supported_enctypes前面的#去掉，并增加多种认证方式


### 配置acl

将步骤3中添加的3个principal添加进acl文件中


```shell
vim /etc/krb5kdc/kadm5.acl

# This file Is the access control list for krb5 administration.
# When this file is edited run service krb5-admin-server restart to activate
# One common way to set up Kerberos administration is to allow any principal 
# ending in /admin  is given full administrative rights.
# To enable this, uncomment the following line:
*/admin                   *
root/admin@NJQA.COM       *
host/admin@NJQA.COM       *
nfs/admin@NJQA.COM        *
```

### 添加日志和存取principal的权限

若不修改此项，日志记录和存取principal时会有问题

在ReadWriteDirectories项添加路径/etc/krb5kdc /var/log以增加权限

```shell
vim /lib/systemd/system/krb5-admin-server.service

[Unit]
Description=Kerberos 5 Admin Server


[Service]
Type=simple
ExecStart=/usr/sbin/kadmind -nofork $DAEMON_ARGS
EnvironmentFile=-/etc/default/krb5-admin-server
InaccessibleDirectories=-/etc/ssh -/etc/ssl/private  /root
ReadOnlyDirectories=/
ReadWriteDirectories=-/var/tmp /tmp /var/lib/krb5kdc -/var/run /run /etc/krb5kdc /var/log        #后两项需要添加上
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
vim /lib/systemd/system/krb5-kdc.service

[Unit]
Description=Kerberos 5 Key Distribution Center


[Service]
Type=forking
PIDFile=/var/run/krb5-kdc.pid
ExecReload=/bin/kill -HUP $MAINPID
EnvironmentFile=-/etc/default/krb5-kdc
ExecStart=/usr/sbin/krb5kdc -P /var/run/krb5-kdc.pid $DAEMON_ARGS
InaccessibleDirectories=-/etc/ssh -/etc/ssl/private  /root
ReadOnlyDirectories=/
ReadWriteDirectories=-/var/tmp /tmp /var/lib/krb5kdc -/var/run /run /etc/krb5kdc /var/log
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
Restart=on-abnormal


[Install]
WantedBy=multi-user.target
```

修改完成后使用systemctl daemon-reload命令重新加载



### 重启服务

```systemctl restart krb5-admin-server.service krb5-kdc.service```


# 配置Kerberos client

## 安装相关组件

```apt-get install krb5-user```，在配置界面填写的内容与Kerberos主机填写内容相同，即Server、Client与Kerberos的krb5.conf是相同的
可以将KDC的krb5.conf拷贝到Client端

```shell
root@kclient241:/etc/apt# scp 172.17.75.240:/etc/krb5.conf /etc/krb5.conf
The authenticity of host '172.17.75.240 (172.17.75.240)' can't be established.
ECDSA key fingerprint is SHA256:LnlXsXoJenNd6t5MXyebncsPsgRHJwsHrd+nMt4AHNE.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '172.17.75.240' (ECDSA) to the list of known hosts.
root@172.17.75.240's password: 
krb5.conf                                                                                       100%  542   779.2KB/s   00:00
```

## 通过我们创建的管理员帐号登录后获取Server的krb5.keytab

如下

```shell
root@kclient241:~# kadmin
Authenticating as principal root/admin@NJQA.COM with password.
Password for root/admin@NJQA.COM: 
kadmin:  ktadd -k /etc/krb5.keytab host/kclient241.njqa.com@NJQA.COM
Entry for principal host/kclient241.njqa.com@NJQA.COM with kvno 2, encryption type aes256-cts-hmac-sha1-96 added to keytab WRFILE:/etc/krb5.keytab.
Entry for principal host/kclient241.njqa.com@NJQA.COM with kvno 2, encryption type arcfour-hmac added to keytab WRFILE:/etc/krb5.keytab.
Entry for principal host/kclient241.njqa.com@NJQA.COM with kvno 2, encryption type des3-cbc-sha1 added to keytab WRFILE:/etc/krb5.keytab.
Entry for principal host/kclient241.njqa.com@NJQA.COM with kvno 2, encryption type des-cbc-crc added to keytab WRFILE:/etc/krb5.keytab.
kadmin:  q
```

## 使用kinit申请TGT验证认证配置是否成功，kinit执行完成后使用klist查看凭证已拿到

```shell
root@kclient241:~# kinit -kt /etc/krb5.keytab host/kclient241.njqa.com@NJQA.COM
root@kclient241:~# klist
Ticket cache: FILE:/tmp/krb5cc_0
Default principal: host/kclient241.njqa.com@NJQA.COM

Valid starting       Expires              Service principal
2023-01-31T15:32:50  2023-01-31T22:12:50  krbtgt/njqa.COM@NJQA.COM
```

如果这里有问题请检查hostname、hosts、krb5.conf、各个principal是否正确，krb5.keytab是否存在，还有最容易忽略的时间是否统一可以手动校准也可以使用NTP、Chrony等时间同步服务来做


## 在kclient242上按照1-3步骤也操作一遍


# 配置Scaler集群

注意：
1.	提前配置好集群的node的hostname以及hosts
1.	多节点集群中每个节点都需要配置好hosts


在虚拟存储器的配置界面找到Kerberos配置，点击...配置kerberos，其中kerberos服务器建议使用全称域名配置


<img class="shadow" src="/img/in-post/kerberos/kerberos-5.png" width="1200">


配置好Kerberos后添加principal

<img class="shadow" src="/img/in-post/kerberos/kerberos-6.png" width="1200">

<img class="shadow" src="/img/in-post/kerberos/kerberos-7.png" width="1200">

在虚拟存储器的NAS页面中创建共享文件夹，在NFS菜单中选择krb5、krb5i或krb5p，创建基于Kerberos认证的共享文件夹

<img class="shadow" src="/img/in-post/kerberos/kerberos-8.png" width="1200">

然后在Kerberos client端mount共享文件夹

使用nfs4挂载krb5的共享文件夹

mount时使用主机名、ip地址或全称域名均可

```shell
root@kclient241:~# mount -t nfs -o vers=4.2 node111:/vol/folder01 /mnt/folder01/
root@kclient241:~# mount |grep node111
node111:/vol/folder01 on /mnt/folder01 type nfs4 (rw,relatime,vers=4.2,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=krb5,clientaddr=172.17.75.241,local_lock=none,addr=172.17.72.111)
root@kclient241:~# 
```

使用nfs3挂载krb5i的共享文件夹

```shell
root@kclient241:~# mount -t nfs -o vers=3 node111:/vol/folder02 /mnt/folder02/
root@kclient241:~# mount |grep node111
node111:/vol/folder01 on /mnt/folder01 type nfs4 (rw,relatime,vers=4.2,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=krb5,clientaddr=172.17.75.241,local_lock=none,addr=172.17.72.111)
node111:/vol/folder02 on /mnt/folder02 type nfs (rw,relatime,vers=3,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=krb5i,mountaddr=172.17.72.111,mountvers=3,mountport=47733,mountproto=udp,local_lock=none,addr=172.17.72.111)
root@kclient241:~# 
```



