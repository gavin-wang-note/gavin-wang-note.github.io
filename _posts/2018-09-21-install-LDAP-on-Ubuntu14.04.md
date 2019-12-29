---
layout:     post
title:      "Ubuntu 14.04 上部署LDAP&DNS Server"
subtitle:   "Install LDAP$DNS Server on Ubuntu14.04"
date:       2018-09-21
author:     "Gavin"
catalog:    true
tags:
    - LDAP
---


# 安装LDAP

## 安装软件

```sudo apt-get install slapd ldap-utils ```

安装过程中会提示输入设置LDAP管理员账号密码：
<img class="shadow" src="/img/in-post/ldap_password.png" width="1200">
 
这里输入了12345678。

再次确认密码
<img class="shadow" src="/img/in-post/ldap_confirm_passwd.png" width="1200">

# 配置LDAP

打开'/etc/ldap/ldap.conf'文件按照以下内容配置修改:

```
sudo vi /etc/ldap/ldap.conf
#
# LDAP Defaults
#

# See ldap.conf(5) for details
# This file should be world readable but not world writable.

#BASE   dc=example,dc=com
#URI    ldap://ldap.example.com ldap://ldap-master.example.com:666
BASE    dc=bigtera-os,dc=com
URI     ldap://172.16.146.134

#SIZELIMIT      12
#TIMELIMIT      15
#DEREF          never

# TLS certificates (needed for GnuTLS)
TLS_CACERT      /etc/ssl/certs/ca-certificates.crt
```

执行以下命令配置：

```sudo dpkg-reconfigure slapd ```

以下界面选择“NO”后按Enter继续
<img class="shadow" src="/img/in-post/ldap_ dpkg_reconfigure_slapd.png" width="1200">

输入DNS domain 名称。例如bigtera-os.com

输入组织名称，例如bigtera-os
<img class="shadow" src="/img/in-post/ldap_doamin.png" width="1200"> 


输入LDAP管理员的密码
<img class="shadow" src="/img/in-post/ldap_input_passwd.png" width="1200">
 
再次确认输入LDAP管理员密码
<img class="shadow" src="/img/in-post/ldap_input_confirm_passwd.png" width="1200"> 

选择HDB数据库
<img class="shadow" src="/img/in-post/ldap_select_db.png" width="1200">

选择删除LDAP服务时自动删除数据库
<img class="shadow" src="/img/in-post/ldap_remove_db1.png" width="1200">

选择删除之前的数据库
<img class="shadow" src="/img/in-post/ldap_remove_db2.png" width="1200">

选择No后，LDAP服务配置且启动
<img class="shadow" src="/img/in-post/ldap_config_auto_start.png" width="1200">


# 测试LDAP服务

输入"ldapsearch -x"，会看到类似以下输出:

```
wyz@LDAP:~$ ldapsearch -x
# extended LDIF
#
# LDAPv3
# base <dc=bigtera-os,dc=com> (default) with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# bigtera-os.com
dn: dc=bigtera-os,dc=com
objectClass: top
objectClass: dcObject
objectClass: organization
o: bigtera-os
dc: bigtera-os

# admin, bigtera-os.com
dn: cn=admin,dc=bigtera-os,dc=com
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator

# search result
search: 2
result: 0 Success

# numResponses: 3
# numEntries: 2
wyz@LDAP:~$
```

## 查看LDAP版本

```
root@LDAP:~# slapd -V
@(#) $OpenLDAP: slapd  (Ubuntu) (May 31 2017 21:52:16) $
	buildd@lgw01-30:/build/openldap-tnOaja/openldap-2.4.31/debian/build/servers/slapd
```

# LDAP服务器管理

在命令行模式下管理LDAP服务器是相当困难的，所以在这里我使用了一个更简单的GUI管理工具“phpldapadmin”。

## 安装phpldapadmin

执行以下命令安装:
```sudo apt-get install phpldapadmin ```


## 给phpldapadmin目录创建link目录

```sudo ln -s /usr/share/phpldapadmin/  /var/www/phpldapadmin ```

## 修改config.phhp文件

打开‘/etc/phpldapadmin/config.phhp’文件，替换配置的名称。按照以下显示修改：
建议先备份一下，防止修改错误。

```sudo cp /etc/phpldapadmin/config.php /etc/phpldapadmin/bak_config.php ```

```
$servers = new Datastore();
$servers->newServer('ldap_pla');
$servers->setValue('server','host','172.16.146.134');
$servers->setValue('server','base',array('dc=bigtera-os,dc=com'));
$servers->setValue('login','auth_type','session');
$servers->setValue('login','bind_id','cn=admin,dc=bigtera-os,dc=com');
```

## 重启LDAP服务

```sudo /etc/init.d/apache2 restart ```


## 打开系统80,389端口
```
wyz@LDAP:~$ sudo ufw allow 80
Rules updated
Rules updated (v6)
wyz@LDAP:~$ sudo ufw allow 389
Rules updated
Rules updated (v6)
```

## 登陆LDAP服务端

通过浏览器访问 ```http://IP/phpldapadmin ```
<img class="shadow" src="/img/in-post/ldap_login_page.png" width="1200">

点击登陆按钮进入登陆界面
<img class="shadow" src="/img/in-post/lsap_auth_page.png" width="1200">

输入密码后点击“认证”进入系统会看到下面的界面
<img class="shadow" src="/img/in-post/ldap_login_success.png" width="1200">
 
至此LDAP的管理服务phpldapadmin算是搭建完成了。


# LDAP简称对应

```
o --  organization（组织-公司）
ou -- organization unit（组织单元/部门）
c --  countryName（国家）
dc -- domainComponent（域名组件）
sn -- suer name（真实名称）
cn -- common name（常用名称）
dn -- distinguished name（专有名称）
```

# LDAP 操作

说明：

* 本文简化操作，只以创建用户组和普通用户来进行文档的整理。

## 创建OU

### Create new entry here

如下图所示，点击“Create new entry here”，创建一个新条目：
 
<img class="shadow" src="/img/in-post/ldap_create_new_entry.png" width="1200">

### Create Object
如下图所示，选择“Generic： Organisational Unit”
 
<img class="shadow" src="/img/in-post/ldap_create_object.png" width="1200">

### 选择OU后，如下图所示：
 
<img class="shadow" src="/img/in-post/ldap_select_ou.png" width="1200">

### Create LDAP Entry

输入OU名称，例如“IT”：
<img class="shadow" src="/img/in-post/ldap_create_ou_entry.png" width="1200">
 
### Save the created Entry

点击“Commit”按钮：
<img class="shadow" src="/img/in-post/ldap_save_ou_entry.png" width="1200">


# 创建CN

说明：

* 用phpldapadmin 时，不能添加UID号 和 GID 号，这是phpldapadmin的bug。解决办法是要先用ldapadd，添加用户的uidNumber，gidNumber如：

```
root@LDAP:~# vi lduser1.ldif 
# lduser1, IT, bigtera-os.com
dn: uid=lduser1,ou=IT,dc=bigtera-os,dc=com
uid: lduser1
cn: lduser1
objectClass: account
objectClass: posixAccount
objectClass: top
objectClass: shadowAccount
userPassword: 1
shadowLastChange: 14323
shadowMax: 99999
shadowWarning: 7
loginShell: /bin/bash
uidNumber: 1105
gidNumber: 1105
homeDirectory: /home/lduser1
```

说明：

* 这里添加了一个普通账号，账号名称为lduser1.

使用命令添加：

```
root@LDAP:~# ldapadd -x -D "cn=admin,dc=bigtera-os,dc=com" -W  -f  lduser1.ldif
Enter LDAP Password: 
adding new entry "uid=lduser1,ou=IT,dc=bigtera-os,dc=com"
```

查看：

```
root@LDAP:~# ldapsearch -x  -b "dc=bigtera-os,dc=com"
# extended LDIF
#
# LDAPv3
# base <dc=bigtera-os,dc=com> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# bigtera-os.com
dn: dc=bigtera-os,dc=com
objectClass: top
objectClass: dcObject
objectClass: organization
o: bigtera-os
dc: bigtera-os

# admin, bigtera-os.com
dn: cn=admin,dc=bigtera-os,dc=com
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator

# IT, bigtera-os.com
dn: ou=IT,dc=bigtera-os,dc=com
objectClass: organizationalUnit
objectClass: top
ou: IT

# lduser1, IT, bigtera-os.com
dn: uid=lduser1,ou=IT,dc=bigtera-os,dc=com
uid: lduser1
cn: lduser1
objectClass: account
objectClass: posixAccount
objectClass: top
objectClass: shadowAccount
shadowMax: 99999
shadowWarning: 7
loginShell: /bin/bash
uidNumber: 1105
gidNumber: 1105
homeDirectory: /home/lduser1

# search result
search: 2
result: 0 Success

# numResponses: 5
# numEntries: 4
root@LDAP:~#
```

账号创建好后，如下图所示：
 
<img class="shadow" src="/img/in-post/ldap_show_account.png" width="1200">

至此，就可以正常使用phpldapadmin添加用户和用户组了！


# 创建Posix Group

## Create a child entry

如下图所示，选择cn=admin，对其创建子条目：
<img class="shadow" src="/img/in-post/ldap_create_a_child_entry.png" width="1200">
 

## Create Object

选择“Generic： Posix Group”，如下图所示：
<img class="shadow" src="/img/in-post/ldap_select_posix_group.png" width="1200"> 

输入组名称，如group1：
<img class="shadow" src="/img/in-post/ldap_create_group.png" width="1200">
 
注意：
* 不要选择已经存在的账号！

## Create LDAP Entry
<img class="shadow" src="/img/in-post/ldap_create_ldap_entry.png" width="1200">
 
## Save the entry

点击“Commit”按钮，如下图所示：

<img class="shadow" src="/img/in-post/ldap_save_entry.png" width="1200">
 


## 新增账号

Create a child entry
    选择新创建的OU，创建子条目，如下图所示：
<img class="shadow" src="/img/in-post/ldap_create_new_account.png" width="1200">

## Create Object

输入账号名称信息，比如test01。
说明：
    password加密算法，选择crypt.

<img class="shadow" src="/img/in-post/ldap_crypt.png" width="1200">
 
## Create LDAP Entry
 
<img class="shadow" src="/img/in-post/ldap_create_crypt_user.png" width="1200">

## Save entry
 
<img class="shadow" src="/img/in-post/ldap_save_ou_user.png" width="400">

# Rename user

选择新创建的账号，对其进行修改操作
<img class="shadow" src="/img/in-post/ldap_rename01.png" width="1200">


将cn=test01 修改为 uid=test01
<img class="shadow" src="/img/in-post/ldap_rename02.png" width="1200">
 
点击“Rename”后：
<img class="shadow" src="/img/in-post/ldap_rename03.png" width="1200">
 
修改loginShell，将/bin/sh修改为 /bin/bash：
<img class="shadow" src="/img/in-post/ldap_shell.png" width="1200">
 
点击“Upgrade Object”后，账号信息发送了变化：
<img class="shadow" src="/img/in-post/ldap_show_update.png" width="1200">
 

## Add attribute

说明：

* LDAP的 user, 要加上 displayName 和 mail，因为没有这些attribute， search出来的结果会被filter掉。 标准的LDAP账号，应该是具有这些属性信息的。

### Add new attribute

<img class="shadow" src="/img/in-post/ldap_attribute01.png" width="1200">

Add DisplayName attribute
 
<img class="shadow" src="/img/in-post/ldap_attribute02.png" width="1200">
 

Add email attribute

<img class="shadow" src="/img/in-post/ldap_attribute03.png" width="1200">
 

其他账号的创建，请参考“新增账号”章节。

# phpldapadmin存在的问题

## Can't create a new entry

现象

创建新实体的时候，UI右方会显示Error, trying to get a non-existant value(appearance, password_hash)

<img class="shadow" src="/img/in-post/ldap_issue1.png" width="1200">

解决方法

将password_hash在/usr/share/phpldapadmin/lib/TemplateRender.php(第2469行)更改为password_hash_custom。

## 创建账号的时候，无法选择gid

现象

本文在创建CN章节有提到，操作方法请参考本文“创建CN”这章节内容。

解决方法

后台创建账号，再在phpldapadmin web界面创建group 和 账号。


## Virtual Stor LDAP 账号导入测试

<img class="shadow" src="/img/in-post/ldap_issue2.png" width="1200">
<img class="shadow" src="/img/in-post/ldap_issue3.png" width="1200">
<img class="shadow" src="/img/in-post/ldap_issue4.png" width="1200">

 
# 总结

搭建的步骤按照文章的内容一步一步来操作，看似很简单，但是希望在看本教程的时候，看懂每一步再下手，不要盲目的去重复上面的事情，只有这样才能事半功倍。



# 参考文档

```
    https://my.oschina.net/u/2496664/blog/801996
    https://my.oschina.net/guol/blog/338362
    https://www.zhukun.net/archives/7980
    http://www.topjishu.com/8781.html
```

# 附录

## 搭建DNS Server

### 参考文档

https://help.ubuntu.com/14.04/serverguide/dns.html

这里简单记录一下内容。

### Caching Nameserver

```
root@LDAP:~# cat /etc/bind/named.conf.options
options {
	directory "/var/cache/bind";

	// If there is a firewall between you and nameservers you want
	// to talk to, you may need to fix the firewall to allow multiple
	// ports to talk.  See http://www.kb.cert.org/vuls/id/800113

	// If your ISP provided one or more IP addresses for stable 
	// nameservers, you probably want to use them as forwarders.  
	// Uncomment the following block, and insert the addresses replacing 
	// the all-0's placeholder.

	// forwarders {
	// 	0.0.0.0;
	// };

       forwarders {
                8.8.8.8;
                172.16.146.134;
           };
	//========================================================================
	// If BIND logs error messages about the root key being expired,
	// you will need to update your keys.  See https://www.isc.org/bind-keys
	//========================================================================
	dnssec-validation auto;

	auth-nxdomain no;    # conform to RFC1035
	listen-on-v6 { any; };
};
```

### Primary Master

```
root@LDAP:~# cat /etc/bind/named.conf.local
//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";


zone "bigtera-os.com" {
	type master;
        file "/etc/bind/db.bigtera-os.com";
};

zone "146.16.172.in-addr.arpa" {
        type master;
        file "/etc/bind/db.172";
};
root@LDAP:~#
```

```
root@LDAP:~# cat /etc/bind/db.bigtera-os.com 
;
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	bigtera-os.com. root.bigtera-os.com. (
			      2		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
	IN	A	172.16.146.134
;
@	IN	NS	ns.bigtera-os.com.
@	IN	A	172.16.146.134
@	IN	AAAA	::1
ns	IN	A	172.16.146.134
www	IN	A	172.16.146.134
root@LDAP:~#
```

```
root@LDAP:~# cat  /etc/bind/named.conf.local 
//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";


zone "bigtera-os.com" {
	type master;
        file "/etc/bind/db.bigtera-os.com";
};

zone "146.16.172.in-addr.arpa" {
        type master;
        file "/etc/bind/db.172";
};
root@LDAP:~#
```
