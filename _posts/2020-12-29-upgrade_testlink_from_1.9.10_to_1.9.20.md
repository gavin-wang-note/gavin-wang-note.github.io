---
layout:     post
title:      "CentOS6.5 testlink-1.9.10升级到1.9.20"
subtitle:   "CentOS6.5 upgrade testlink-1.9.10 to testlink-1.9-20"
date:       2020-12-29
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [shell]
tags:
    - Linux
    - shell
---

# 概述

Lab使用的testlink版本是1.9.10，运行在CentOS6.5上，应大家要求，对testlink进行升级，升级到官方最新1.9.20版本

# 实践

## 设置本地源

## 备份本地源

```cd /etc/yum.repos.d/;mkdir backup_repo; mv *.repo  mirrors-rpmforge* backup_repo/ ```

修改源

```shell
vi redhat.repo
[rhel6-media]
name=local
baseurl=file:///mnt/cdrom
gpgcheck=0
enabled=1
```

## 上传镜像并挂载

上传镜像 'rhel-server-6.6-x86_64-dvd.iso', 并挂载

```cd /mnt;mkdir cdrom;mount /dev/sr0 /mnt/cdrom/ ```

## 使用本地源

```yum clean all;yum makecache ```

## 卸载旧版php

```yum remove php-common ```

## 安装rpm升级包

```rpm -Uvh https://mirror.webtatic.com/yum/el6/latest.rpm ```

## 安装php5.6

```yum install -y php56w php56w-opcache php56w-xml php56w-mcrypt php56w-gd php56w-devel php56w-mysql php56w-intl php56w-mbstring --skip-broken ```

## 查看php版本

```shell
[root@localhost mnt]# php -v
PHP 5.6.40 (cli) (built: Jan 12 2019 09:19:57) 
Copyright (c) 1997-2016 The PHP Group
Zend Engine v2.6.0, Copyright (c) 1998-2016 Zend Technologies
    with Zend OPcache v7.0.6-dev, Copyright (c) 1999-2016, by Zend Technologies
[root@localhost mnt]# 
```


## 升级mysql 5.5 到 mysql 5.6

### 查看升级前版本

```shell
[root@localhost mnt]# yum info mysql-server
Loaded plugins: fastestmirror, refresh-packagekit, security
Loading mirror speeds from cached hostfile
 * webtatic: us-east.repo.webtatic.com
Installed Packages
Name        : mysql-server
Arch        : x86_64
Version     : 5.5.38
Release     : 1.el6.remi
Size        : 45 M
Repo        : installed
From repo   : remi
Summary     : The MySQL server and related files
URL         : http://www.mysql.com
License     : GPLv2 with exceptions and LGPLv2 and BSD
Description : MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
            : client/server implementation consisting of a server daemon (mysqld)
            : and many different client programs and libraries. This package contains
            : the MySQL server and some accompanying files and directories.

[root@localhost mnt]# 
```


### 卸载旧版本mysql

```yum remove mysql mysql-server ```

### 卸载mysql-client

```yum remove mysql-client ```

### 卸载mysql-devel

```yum remove mysql-devel ```



### 添加MySQL的yum安装库

```shell
wget http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
rpm -ivh mysql-community-release-el6-5.noarch.rpm
```

```yum list | grep mysql ```, 这样很多更新的MySQL安装包就都有了。


如有必要，运行下面的命令确保yum安装库是最新的：

```yum update mysql-community-release ```



### 安装mysql

```yum install mysql-server ```

### 启动数据库

```/etc/init.d/mysqld start ```

### 修复mysql

```mysql_upgrade -uroot -pp@ssw0rd ```


## 安装testlink-1.9.20

### 解压testlink-1.9.20
  略

### 备份旧版testlink数据库

#### 先备份，后导入备份库

```mysql -uroot -pp@ssw0rd ```

```create database testlink_bak; ```

#### 导出旧库数据

```mysqldump -uroot -pp@ssw0rd testlink > testlink_backup.sql ```

#### 导入到备份数据库中

```mysql -uroot -pp@ssw0rd testlink_bak < testlink_backup.sql ```

#### 将旧testlink db切换到testlink_bak

Step1. 修改config_db.conf，并重启httpd服务

Step2. 尝试访问旧版testlink报错


```shell
[root@localhost logs]# mysql -ubigtera -p111111 testlink_bak
Warning: Using a password on the command line interface can be insecure.
ERROR 1044 (42000): Access denied for user 'bigtera'@'localhost' to database 'testlink_bak'
```

```shell
mysql -uroot -pp@ssw0rd testlink_bak
```

执行

```shell
GRANT ALL PRIVILEGES ON *.* TO 'bigtera'@'localhost' IDENTIFIED BY '111111';
```


### UI 安装新testlink

#### 安装新版testlink

如果不先修复mysql，在安装过程中会报错：


```shell
TestLink setup will now attempt to setup the database:

Creating connection to Database Server:OK!

Database testlink_20 does not exist.
Will attempt to create:
Creating database `testlink_20`:OK!

 ============================================================================== 
 DB Access Error - debug_print_backtrace() OUTPUT START 
 ATTENTION: Enabling more debug info will produce path disclosure weakness (CWE-200) 
            Having this additional Information could be useful for reporting 
            issue to development TEAM. 
 ============================================================================== 
#0  database->exec_query() called at [/var/www/html/testlink-1.9.20/install/installUtils.php:571]
#1  _mysql_assign_grants() called at [/var/www/html/testlink-1.9.20/install/installUtils.php:311]
#2  create_user_for_db() called at [/var/www/html/testlink-1.9.20/install/installNewDB.php:420]
```

创建账户时：

```shell
CREATE USER 'bigtera'@'localhost' IDENTIFIED BY '111111';

ERROR 1558 (HY000): Column count of mysql.user is wrong. Expected 43, found 42. Created with MySQL 50538, now running 50650. Please use mysql_upgrade to fix this error.
```

#### 执行sql

先修改，再执行：

```mysql -uroot -pp@ssw0rd testlink_20 < /var/www/html/testlink-1.9.20/install/sql/mysql/testlink_create_udf0.sql ```



#### 修改新版testlink db，指向testlink这个db

需要重启httpd服务

#### UI访问新版testlink

提示要升级db，执行：

```mysql -uroot -pp@ssw0rd testlink ```

然后执行下面操作：

```shell
alter table platforms add enable_on_design tinyint(1) unsigned NOT NULL default '0';
alter table platforms add enable_on_execution tinyint(1) unsigned NOT NULL default '1';

CREATE OR REPLACE VIEW /*prefix*/latest_exec_by_testplan
AS SELECT tcversion_id, testplan_id, MAX(id) AS id
FROM /*prefix*/executions
GROUP BY tcversion_id,testplan_id;

CREATE TABLE /*prefix*/testplan_platforms (
  id int(10) unsigned NOT NULL auto_increment,
  testplan_id int(10) unsigned NOT NULL,
  platform_id int(10) unsigned NOT NULL,
  active tinyint(1) NOT NULL default '1',
  PRIMARY KEY (id),
  UNIQUE KEY /*prefix*/idx_testplan_platforms(testplan_id,platform_id)
) DEFAULT CHARSET=utf8 COMMENT='Connects a testplan with platforms';


CREATE TABLE /*prefix*/testcase_platforms (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  testcase_id int(10) unsigned NOT NULL DEFAULT '0',
  tcversion_id int(10) unsigned NOT NULL DEFAULT '0',
  platform_id int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (id),
  UNIQUE KEY idx01_testcase_platform (testcase_id,tcversion_id,platform_id),
  KEY idx02_testcase_platform (tcversion_id)
) DEFAULT CHARSET=utf8;

CREATE OR REPLACE VIEW /*prefix*/tcversions_without_platforms
AS SELECT
   NHTCV.parent_id AS testcase_id,
   NHTCV.id AS id
FROM /*prefix*/nodes_hierarchy NHTCV
WHERE NHTCV.node_type_id = 4 AND
NOT(EXISTS(SELECT 1 FROM /*prefix*/testcase_platforms TCPL
           WHERE TCPL.tcversion_id = NHTCV.id));
           
CREATE TABLE /*prefix*/baseline_l1l2_context (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  testplan_id int(10) unsigned NOT NULL DEFAULT '0',
  platform_id int(10) unsigned NOT NULL DEFAULT '0',
  being_exec_ts timestamp NOT NULL,
  end_exec_ts timestamp NOT NULL,
  creation_ts timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY udx1 (testplan_id,platform_id,creation_ts)
) DEFAULT CHARSET=utf8;
```

然后执行如下操作，升级testlink db

```shell
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.10/mysql/DB.1.9.10/step1/db_data_update.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.11/mysql/DB.1.9.11/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.11/mysql/DB.1.9.11/stepZ/z_final_step.sql

mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.12/mysql/DB.1.9.12/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.12/mysql/DB.1.9.12/stepZ/z_final_step.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.13/mysql/DB.1.9.13/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.13/mysql/DB.1.9.13/stepZ/z_final_step.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.14/mysql/DB.1.9.14/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.14/mysql/DB.1.9.14/stepZ/z_final_step.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.15/mysql/DB.1.9.15/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.15/mysql/DB.1.9.15/stepZ/z_final_step.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.16/mysql/DB.1.9.16/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.16/mysql/DB.1.9.16/stepZ/z_final_step.sql

mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.17/mysql/DB.1.9.17/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.17/mysql/DB.1.9.17/stepZ/z_final_step.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.18/mysql/DB.1.9.18/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.18/mysql/DB.1.9.18/stepZ/z_final_step.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.19/mysql/DB.1.9.19/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.19/mysql/DB.1.9.19/stepZ/z_final_step.sql


mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.20/mysql/DB.1.9.20/step1/db_schema_update.sql
mysql -uroot -pp@ssw0rd testlink < /var/www/html/testlink-1.9.20/install/sql/alter_tables/1.9.20/mysql/DB.1.9.20/stepZ/z_final_step.sql
```

至此，升级结束，可以删除旧版本testlink，重命名新版本testlink，并使用UI访问新版本testlink。
