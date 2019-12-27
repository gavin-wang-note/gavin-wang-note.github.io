---
layout:     post
title:      "FTP需求汇总"
subtitle:   "FTP Feature"
date:       2017-10-12
author:     "Gavin"
catalog:    true
tags:
    -FTP
---


# 引言
**vsftpd(very secure FTP daemon)**，如果你想在你的Linux/Unix服务器上搭建一个安全、高性能、稳定性好的FTP服务器，那么vsftpd可能是你的首选应用。
我们的客户对FTP有需求，目前只能通过手动部署、配置的方式来实现客户的要求，工作往往重复。为了规范化FTP配置流程，本文整理一下FTP的需求，以供RD参考。
<br><br>

# 基本配置
默认如下拥有配置项：

## (1)ftp port

支持默认与非默认的修改,针对对安全有特殊要求的用户

```
    listen_port=<port> :设置控制连接的监听端口号，默认为21
    connect_from_port_20=<YES/NO> :若为YES，则强迫FTP－DATA的数据传送使用port 20，默认YES
```

## (2)Listen=yes

独立的VSFTPD服务器

## (3)记录vsftpd的log

```
    log_ftp_protocol=YES (all FTP requests and responses are logged)
    xferlog_enable=yes  （激活上传和下传的日志）
    xferlog_std_format=yes (使用标准的日志格式)  
```

## (4)anon_root

```
    This option represents a directory  which  vsftpd  will  try  to change  into  after  an  anonymous  login.  Failure  is silently ignored.
    Default: (none)
    留给匿名账号使用。
```

## (5)local_umask

```
default 022
```

建议设置成002

## (6) 其他默认配置项

```
    dirmessage_enable=YES
    use_localtime=YES
    secure_chroot_dir=/var/run/vsftpd/empty
    pam_service_name=ftp
    rsa_cert_file=/etc/ssl/private/vsftpd.pem  （这项可有可无，虚拟用户访问FTP Server、PAM认证时使用）
```

# 需求

## 匿名访问

说明：

基于安全考虑，禁止匿名用户启用SSL，即：```allow_anon_ssl=NO```
 

### 场景1、仅有上传权限

#### vsftpd.conf需要修改的内容如下

```
    anon_upload_enable=YES (开放上传权限)
    anon_mkdir_write_enable=YES（可创建目录的同时可以在此目录中上传文件）
    anon_other_write_enable=NO (匿名帐号可以有删除的权限，基于安全考虑，建议设置为NO)
    anon_root=/var/share/ezfs/shareroot/gz/ （设定匿名用户的base_home，要与/etc/passwd 中ftp用户保持一致）
    anon_umask=002
    hide_ids=YES
    no_anon_password=YES （是否询问匿名访问时输入密码）
    write_enable=yes (开放本地用户写的权限)
``` 
   
#### 测试

##### FTP的匿名登录一般有三种：

* 1、用户名：anonymous 密码：Email或者为空
* 2、用户名：FTP 密码：FTP或者为空
* 3、用户名：USER 密码：pass

##### 出现如下错误

```
    500 OOPS: vsftpd: refusing to run with writable root inside chroot()
```

##### 解决方法

Bean 修改了vsftpd的source code，将vsftpd 校验根目录的写权限这部分code注释掉，从而规避这个问题。 记得patch 新的vsftpd deb。


### 场景2、仅有下载权限

vsftpd.conf内容变更如下：

```
    anonymous_enable=YES
    anon_world_readable_only=YES
    anon_root=/var/share/ezfs/shareroot/gz/
    hide_ids=YES
    no_anon_password=YES
    local_enable=YES
```

说明：

要注意文件夹的属性，匿名帐户是其它（other）用户来开启它的读写执行的权限
* （R）读 -- 下载
* （W）写 -- 上传 
* （X）执行 -- 如果不开FTP的目录都进不去

### 场景3、上传、下载权限都有

vsftpd.conf内容变更如下：

```
    anonymous_enable=YES
    anon_umask=002
    anon_upload_enable=YES
    anon_mkdir_write_enable=YES
    anon_other_write_enable=NO
    anon_world_readable_only=YES
    anon_root=/var/share/ezfs/shareroot/gz/
    hide_ids=YES
    no_anon_password=YES
    local_enable=YES
    write_enable=YES
```

### 场景4、约束传输速率

```
    anon_max_rate=51200  （匿名用户的传输比率，单位b/s）
```

作为场景1、2、3的附属配置。


### 场景5、更改文件上传属主

这个作为场景3的附属配置，一旦设置了属主，文件的umask始终是600，这样，ftp用户只有上传权限，无法下载。

```
    chown_uploads=YES
    chown_username=指定一个账号
```

说明:

* chown_uploads=YES 情况下，anon_umask 的设置失效，上传的文件的权限始终是600

* chown_uploads=YES

* * 这种情况下需要设置chown_username，但是你不设置也不会报错，因为系统默认给你设置了个root用户，上传上去的文件所有会是root:ftp。无论你是否设置anon_umask，上传的文件都会是600权限，很恶心，自己能上传但是不能下载。
* * 这种情况可用于公司开发文件上传，只要上传了你就不能修改。

* chown_uploads=NO

* * 这种情况下，通过修改anon_umask文件来控制匿名用户上传文件的权限，不过上传的文件所有者会变为ftp:ftp，也就是说这种情况下匿名用户总是可以修改自己上传的文件的，即使anon_umask=777，也是有权限的。
* * 无论在哪种情况下，上传的文件是不会拥有X，即执行权限。

       

# 普通ftp用户的上传

## 只能上传，无法下载

vsftpd.conf内容变更如下：

```
    anonymous_enable=NO
    local_enable=YES
    write_enable=YES
    download_enable=NO
    log_ftp_protocol=YES
    use_sendfile=NO
    local_umask=002
```

## 普通ftp用户的下载

vsftpd.conf内容变更如下：

```
    anonymous_enable=NO
    local_enable=YES
    write_enable=NO
    download_enable=YES
    log_ftp_protocol=YES
    use_sendfile=NO
    local_umask=002
```

## 普通ftp用户的上传、下载

vsftpd.conf内容变更如下：

```
    anonymous_enable=NO
    local_enable=YES
    write_enable=YES
    log_ftp_protocol=YES
    use_sendfile=NO
    local_umask=002
```
 
## 冻结FTP账号

vsftpd.conf内容增加如下配置项：

```
    userlist_enable=YES
    userlist_deny=YES
    userlist_file=xxxPATH
```

同时，要将被冻结账号信息加入到userlist_file中

### 测试

#### vsftpd.conf中增加

```
    userlist_enable=YES
    userlist_deny=YES
    userlist_file=/etc/vsftpd.deny_list 
```

#### 然后，增加被限制账号到userlist_file中

```
    echo -n "guizhou" > vsftpd.deny_list
```

#### 最后，restart vsftp，使用client 访问FTP server

```
    root@631:~# ftp 172.17.59.5
    Connected to 172.17.59.5.
    220 (vsFTPd 2.3.5)
    Name (172.17.59.5:root): guizhou
    530 Permission denied.
    Login failed.
    ftp>
```


## 约束ftp用户访问目录范围

### 原因

如果不约束住ftp用户的访问目录范围，任其可以访问非base_home下文件，这是非常危险的。

### 约束配置

如果设置为：

```
    chroot_local_user＝YES
    chroot_list_enable=YES(这行可以没有, 也可以有)
    chroot_list_file=/etc/vsftpd.chroot_list
```

那么, 凡是加在文件vsftpd.chroot_list中的用户都是不受限止的用户

即, 可以浏览其主目录的上级目录.

所以, 如果不希望某用户能够浏览其主目录上级目录中的内容,可以如上设置, 然后在文件vsftpd.chroot_list中不添加该用户即可(此时, 在该文件中的用户都是可以浏览其主目录之外的目录的).

或者, 设置如下：

```
    chroot_local_user＝NO
    chroot_list_enable=YES(这行必须要有, 否则文件
    vsftpd.chroot_list不会起作用)
    chroot_list_file=/etc/vsftpd.chroot_list
```

然后把所有不希望有这种浏览其主目录之上的各目录权限的用户添加到文件vsftpd.chroot_list(此时, 在该文件中的用户都是不可以浏览其主目录之外的目录的)

中即可(一行一个用户名).



下图，为这两个参数的详细解释：
<img class="shadow" src="/img/in-post/ftp_parameter_desc.png" width="1200">

#### 测试
按照上面的配置，在限制住用户只能访问bash_home情况下，会出现FTP 500错误码：

```
    root@scaler01:/var/share/ezfs/shareroot# ftp 172.17.59.5
    Connected to 172.17.59.5.
    220 (vsFTPd 2.3.5)
    Name (172.17.59.5:root): guizhou
    331 Please specify the password.
    Password:
    500 OOPS: vsftpd: refusing to run with writable root inside chroot()
    Login failed.
    ftp> 
```

但如果注销掉这三个参数，则会限制住目录，一切OK。

## 限制ftp 传输速率

```
local_max_rate=5120000 （本地用户的传输比率，单位b/s ）
```

## 限制IP

要求：

* 支持具体的IP、IP段、域名

调整的内容：

* vsftpd.conf中增加：

```
    tcp_wrappers=YES
```

同时，要修改/etc/hosts.deny  和 /etc/hosts.allow两个文件

/etc/hosts.deny 中增加如下内容：

```
    #vsftpd
    vsftpd:ALL

/etc/hosts.allow
    #vsftpd
    vsftpd:172.17.59.
```

### 测试

在/etc/hosts.deny 中增加如下内容：

```
    #vsftpd
    vsftpd:ALL
```

在/etc/hosts.allow中增加如下内容：

```
    #vsftpd
    vsftpd:172.19.5.
```

client访问ftp server：

```
    root@631:~# ftp 172.17.59.5
    Connected to 172.17.59.5.
    421 Service not available.
    ftp> 
```

vsftpd的log显示：

```
    Thu Oct 12 14:46:44 2017 [pid 2] CONNECT: Client "172.17.59.8", "Connection refused: tcp_wrappers denial."
    Thu Oct 12 14:46:44 2017 [pid 2] FTP response: Client "172.17.59.8", "421 Service not available."
```

说明：

/etc/hosts.allow 内容格式与要求，示例如下：

```
    vsftpd:.hype.com
    vsftpd:172.17.59.
    vsftpd:172.17.0.0/255.255.254.0
```

第一行表示，只有hype.com这个域里的主机允许访问vsftpd服务，注意hype.com前面的那个点(.)；

第二行表示，只有172.17.59这个网段的用户允许访问vsftpd服务，注意0后面的点(.)；

第三行表示，只有172.17.0这个网段的用户允许访问vsftpd服务，注意这里不能写为172.17.0.0/24。

## ftp TLS加密传输
### 未加密传输情况下，直接抓包：

```
    1146	7.562069	172.17.59.8	172.17.59.5	FTP	74	Request: PASS 1
```

<img class="shadow" src="/img/in-post/ftp_tcpdump.png" widtgh="1200">


上面一行为抓包到的内容，可以明确的看出，密码为1，明文的，风险系数较高


### 先确认，vsftpd是否支持SSL认证：

```
    root@scaler01:/etc# ldd /usr/sbin/vsftpd |grep libssl
	libssl.so.1.0.0 => /lib/x86_64-linux-gnu/libssl.so.1.0.0 (0x00007fc154eb4000)
```

出现类似如上信息，表明支持SSL。


### 生成vsftpd.pem 证书

```
    root@scaler01:/etc/ssl/private# openssl req -x509 -nodes -days 365 -newkey rsa:1024 \-keyout /etc/ssl/private/vsftpd.pem \-out /etc/ssl/private/vsftpd.pem
    Generating a 1024 bit RSA private key
    ................++++++
    .............................++++++
    writing new private key to '/etc/ssl/private/vsftpd.pem'
    -----
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:CN
    State or Province Name (full name) [Some-State]:shanghai
    Locality Name (eg, city) []:nanjing
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:bigtera
    Organizational Unit Name (eg, section) []:bigtera
    Common Name (e.g. server FQDN or YOUR name) []:virtualstor
    Email Address []:virtualstor@bigtera.com.cn

```

vsftpd.conf的设置

```
    ssl_enable=YES
    allow_anon_ssl=NO
    force_local_data_ssl=YES
    force_local_logins_ssl=YES
    ssl_tlsv1=YES
    ssl_sslv2=NO
    ssl_sslv3=NO
    rsa_cert_file=/etc/ssl/private/vsftpd.pem
```



### 测试

```
    root@631:~# ftp 172.17.59.5
    Connected to 172.17.59.5.
    220 (vsFTPd 2.3.5)
    Name (172.17.59.5:root): guizhou
    530 Non-anonymous sessions must use encryption.
    Login failed.
    421 Service not available, remote server has closed connection
    ftp> 
```

说明已经启用了认证，client无法访问FTP server。

这里，可以下载flashftp工具，测试一下。
<img class="shadow" src="/img/in-post/ftp_Accept_key.png" widtgh="1200">

在开启SSL认证情况下抓包：
<img class="shadow" src="/img/in-post/ftp_tcp_desc.png" widtgh="1200">

# 参考文档
http://manpages.ubuntu.com/manpages/trusty/man5/vsftpd.conf.5.html

http://os.51cto.com/art/201008/221842_all.htm

http://viong.blog.51cto.com/844766/261354
