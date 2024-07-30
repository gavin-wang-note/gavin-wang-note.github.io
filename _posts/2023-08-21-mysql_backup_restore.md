---
layout:     post
title:      "mysql 备份与恢复详解"
subtitle:   "MySQL backup and restore"
date:       2023-08-20
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
    - [mysql]
tags:
    - python
    - mysql
---


# 概述


MySQL是目前比较流行的关系型数据库管理系统之一，在企业级应用中被广泛使用。无论是研发成员还是数据库管理员，都需要了解MySQL备份与恢复的基本知识。

备份和恢复是为了防止在数据库发生宕机的情况下保证数据不丢失，或者最小程度丢失的解决方法，不仅能够帮助企业保护数据，还能够使系统在不良情况下快速应对，尽可能使其恢复到正常运行状态。MySQL提供了 mysqldump、ibbackup、replication 工具来备份，当然也有一些三方工具，诸如 xtrabacup、LVM快照等。

利用周末时间，整理一下，详细介绍MySQL备份与恢复的操作步骤，并提供一些最佳实践，以帮助读者在保护其MySQL数据库方面走得更远。




# 环境


```shell
root@ubuntu:~# hostnamectl 
   Static hostname: ubuntu
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 2e28c320b7b64edcb7b039f56050833c
           Boot ID: 928ff3a2a9ef430ba5b923b0d119902f
    Virtualization: vmware
  Operating System: Ubuntu 18.04.6 LTS
            Kernel: Linux 5.4.0-84-generic
      Architecture: x86-64
root@ubuntu:~# mysql --version
mysql  Ver 14.14 Distrib 5.7.42, for Linux (x86_64) using  EditLine wrapper
root@ubuntu:~# 
```



并创建了一个名称为 'test'的数据库，存放一张表（user）和一个视图（user_view）：

```shell
mysql> create table user (name VARCHAR(25), age INT(3));
Query OK, 0 rows affected (0.02 sec)

mysql> insert into user(name, age) values('zhangsan', 30);
Query OK, 1 row affected (0.00 sec)

mysql> insert into user(name, age) values('lisi', 31);
Query OK, 1 row affected (0.00 sec)

mysql> insert into user(name, age) values('wangwu', 38);
Query OK, 1 row affected (0.00 sec)

mysql> insert into user(name, age) values('cat', 2);
Query OK, 1 row affected (0.00 sec)

mysql> create view user_view as select * from user;
Query OK, 0 rows affected (0.01 sec)

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| user           |
| user_view      |
+----------------+
2 rows in set (0.00 sec)

mysql> select * from tables;
ERROR 1146 (42S02): Table 'test.tables' doesn't exist
mysql> select * from user;
+----------+------+
| name     | age  |
+----------+------+
| zhangsan |   30 |
| lisi     |   31 |
| wangwu   |   38 |
| cat      |    2 |
+----------+------+
4 rows in set (0.00 sec)

mysql>
```



# 1. MySQL备份


无论哪种数据库，都应该频繁备份，以确保数据库永远处于最新状态。最好能够制定合理的备份策略，实现定期备份、归档备份文件；备份文件要存放双份，且存在于不同的物理介质上。



## 1.1 备份分类

下面的备份分类中，并不是所有都适配了 Mysql 和 Innodb引擎，所以部分是没有真正的方案，也有些是交叉分类的（比如在热备又在逻辑文件中）。



### 1.1.1 按备份类型

- 热备：在数据库运行过程中直接备份
- 冷备：在数据库停止的情况下备份，一般直接复制相关的物理文件即可
- 温备：在数据库运行过程中备份，但对数据库操作有影响，如加个全局读锁以保证备份数据一致性



### 1.1.2 按备份文件

- 逻辑文件：指备份出的文件可读，一般指 SQL 语句（适用库升级，迁移，但恢复时间较长需要执行 SQL 语句）
- 物理文件：指复制数据库的物理文件



### 1.1.3 按备份内容

- 日志备份：主要备份 bin-log 日志，然后 replay 来完成 point-in-time
- 完全备份：对数据库一个完整的备份
- 增量备份：在上次完全备份的基础上对更改部分进行备份（MySQL 没真正的增量备份，一般通过 bin-log 完成，要借助第三方工具才能实现）



也有按 **物理备份 **与 **逻辑备份** 进行分类的，视角不同，实则殊途同归。



## 1.2 备份的一致性

数据库备份的一致性要求在备份的时候数据在这一时间点上是一致的，比如银行转账，A 转给 B 现金100 RMB，这个事务过程先扣 A 100元，再去 B 加100元，确保前后数据一致，否则会发生恢复数据后金钱对不上的情况。

对于 Innodb 引擎来说，因为其支持 MVCC 功能，所以可以先开启一个事务，然后导出一组相关的表，最后提交来实现一致的备份，当然隔离级别要设置为 REPEATABLE READ

对于 mysqldump 备份工具可以添加 --single-transaction 选项来实现备份一致性（开启事务，设置隔离级别）

下面来说明备份的途径 。



# 2. 备份与恢复常用操作示例



## 2.1 备份 MySQL 



### 2.1.1 备份全部数据库的数据和结构

​                

```shell
mysqldump -uroot -p123456 -A > /data/mysql_dump/mydb.sql
```



### 2.1.2 备份全部数据库的结构（加 -d 参数）

​                

```shell
mysqldump -uroot -p123456 -A -d > /data/mysql_dump/mydb.sql
```



### 2.1.3 备份全部数据库的数据(加 -t 参数)

​                

```shell
mysqldump -uroot -p123456 -A -t > /data/mysql_dump/mydb.sql
```



### 2.1.4 备份单个数据库的数据和结构(,数据库名mydb)

​                

```shell
mysqldump -uroot-p123456 mydb > /data/mysql_dump/mydb.sql
```



### 2.1.5 备份单个数据库的结构

​                

```shell
mysqldump -uroot -p123456 mydb -d > /data/mysql_dump/mydb.sql
```



### 2.1.6 备份单个数据库的数据

​                

```shell
mysqldump -uroot -p123456 mydb -t > /data/mysql_dump/mydb.sql
```



### 2.1.7 备份多个表的数据和结构



数据，结构的单独备份方法与上同。

​                

```shell
mysqldump -uroot -p123456 mydb t1 t2 > /data/mysql_dump/mydb.sql
```



### 2.1.8 一次备份多个数据库

​                

```shell
mysqldump -uroot -p123456 --databases db1 db2 > /data/mysql_dump/mydb.sql
```





## 2.2 还原 MySQL 备份内容



有两种方式还原，第一种是在 MySQL 命令行中，第二种是使用 SHELL 行完成还原



在系统命令行中，输入如下实现还原：

​                

```shell
mysql -uroot -p123456 < /data/mysql_dump/mydb.sql
```



###### 在登录进入mysql系统中,通过source指令找到对应系统中的文件进行还原：

​                

```shell
mysql> source /data/mysql_dump/mydb.sql
```



在 Linux中，通常使用BASH脚本对需要执行的内容进行编写，加上定时执行命令crontab实现日志自动化生成。





# 3. 备份与恢复实践



## 3.1 物理备份与恢复



### 3.1.1 物理备份



MySQL有一种非常简单的备份方法，就是将MySQL中的数据库文件直接复制出来。这是最简单，速度最快的方法。

不过在此之前，建议将数据库进行一次完整逻辑备份（防患于未然，建议做），然后将服务器停止，这样才可以保证在复制期间数据库的数据不会发生数据冲突。如果在复制数据库的过程中还有数据写入，就会造成数据不一致。这种情况在开发环境可以，但是在生产环境中很难允许备份服务器。

**注意：**

此方法不适用于InnoDB存储引擎的表，而对于MyISAM存储引擎的表很方便。同时，还原时MySQL的版本最好相同。



### 3.1.2 物理恢复



物理恢复是将备份文件中的物理文件复制到MySQL服务器的目标目录中。下面是物理恢复的一些步骤：

* 停止MySQL服务
* 复制备份文件到正确的目录
* 启动MySQL服务



下面是在Linux系统中使用命令行恢复MySQL数据库的一些命令：

```shell
service mysql stop

cp 备份文件名 目标目录

service mysql start
```





## 3.2 mysqldump



mysqldump 是属于逻辑备份，也是最常见的备份工具了，缺点在于备份和恢复速度不是特别快，因为是单线程。



### 3.2.1 mysqldump 备份



语法：

```shell
mysqldump [arguments] > dump.sql
```



详细语法，可执行 ``` mysqldump --help``` 进行查看，如下为几个重要的参数介绍：



```shell
--all-databases：  备份所有数据库
--databases：      备份指定数据库
--single-transaction：备份一致性
--add-drop-database：添加语句 DROP DATABASE IF EXISTS（默认是 CREATE DATABASE IF NOT EXISTS）
--hex-blob：binary、blog、bit是十六进制不可见，会以十六进制来展示
```



示例：

```shell
mysqldump -uroot -pp@ssw0rd test > test.sql
```


注意：

* mysqldump 可以导出存储过程，导出触发器，导出事件，导出数据，但不能导出视图
* 如果用户的数据库中还使用了视图，则在用mysqldump备份完数据库后，还需要导出视图的定义，或者备份视图定义的frm文件，并在恢复时进行导入，这样才能保证mysqldump数据库的完全恢复和数据的完整


视图备份与恢复：


```shell
root@ubuntu:~# mysql -uroot -pp@ssw0rd test
mysql: [Warning] Using a password on the command line interface can be insecure.
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 5.7.42-0ubuntu0.18.04.1-log (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| user           |
| user_view      |
+----------------+
2 rows in set (0.00 sec)

mysql> drop view user_view;
Query OK, 0 rows affected (0.01 sec)

mysql> commit;
Query OK, 0 rows affected (0.00 sec)

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| user           |
+----------------+
1 row in set (0.00 sec)

mysql> exit;
Bye
root@ubuntu:~# mysql -uroot -pp@ssw0rd test < view.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
root@ubuntu:~# mysql -uroot -pp@ssw0rd test
mysql: [Warning] Using a password on the command line interface can be insecure.
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 14
Server version: 5.7.42-0ubuntu0.18.04.1-log (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| user           |
| user_view      |
+----------------+
2 rows in set (0.00 sec)

mysql> select * from user_view;
+----------+------+
| name     | age  |
+----------+------+
| zhangsan |   30 |
| lisi     |   31 |
| wangwu   |   38 |
| cat      |    2 |
+----------+------+
4 rows in set (0.00 sec)

mysql> exit;
Bye
root@ubuntu:~# 
```


### 3.2.2 mysqldump 恢复



```shell
mysqldump -uroot -pp@ssw0rd test < test.sql
```





## 3.3 bin-log

bin-log 是 Mysql 的日志文件。



### 3.3.1 备份



先要在 ```/etc/mysql/mysql.conf.d/mysqld.cnf``` 中[mysql] section 下增加下面一句话，之后会自动记录，名字按 name.00001 格式来递增滚动，其中 name 为 自定义的log-bin name，如下所示：



```text
[mysqld]
# 不赋值默认为主机名
log-bin         = /var/log/mysql/mysql-binlog
server-id       = 1
```



重启mysql service后，会在 /var/log/mysql 目录下产生从1 开始的binlog文件：

```shell
root@ubuntu:/var/log/mysql# ll
total 28
drwxr-x---  2 mysql adm    4096 Aug 21 13:23 ./
drwxrwxr-x 13 root  syslog 4096 Aug 21 13:22 ../
-rw-r-----  1 mysql adm    3546 Aug 21 13:23 error.log
-rw-r-----  1 mysql adm    5659 Aug 21 13:16 error.log.1.gz
-rw-r-----  1 mysql mysql   154 Aug 21 13:23 mysql-binlog.000001
-rw-r-----  1 mysql mysql    35 Aug 21 13:23 mysql-binlog.index
root@ubuntu:/var/log/mysql# 
```



**说明：**



这里的mysqld.cnf配置文件中一定要赋值 server-id，否则会报如下错误(来自/var/log/syslog)：



```shell
Aug 21 13:18:29 ubuntu mysql-systemd-start[2327]: Please take a look at https://wiki.debian.org/Teams/MySQL/FAQ for tips on fixing common upgrade issues.
Aug 21 13:18:29 ubuntu mysql-systemd-start[2327]: Once the problem is resolved, restart the service.
Aug 21 13:18:29 ubuntu systemd[1]: mysql.service: Control process exited, code=exited status=1
Aug 21 13:18:29 ubuntu systemd[1]: mysql.service: Failed with result 'exit-code'.
Aug 21 13:18:29 ubuntu systemd[1]: Failed to start MySQL Community Server.
Aug 21 13:18:29 ubuntu systemd[1]: mysql.service: Service hold-off time over, scheduling restart.
Aug 21 13:18:29 ubuntu systemd[1]: mysql.service: Scheduled restart job, restart counter is at 1.
Aug 21 13:18:29 ubuntu systemd[1]: Stopped MySQL Community Server.
Aug 21 13:18:29 ubuntu systemd[1]: Starting MySQL Community Server...
Aug 21 13:18:29 ubuntu mysql-systemd-start[2335]: ERROR: Unable to start MySQL server:
Aug 21 13:18:29 ubuntu mysql-systemd-start[2335]: 2023-08-21T20:18:29.151581Z 0 [ERROR] You have enabled the binary log, but you haven't provided the mandatory server-id. Please refer to the proper server start-up parameters documentation
Aug 21 13:18:29 ubuntu mysql-systemd-start[2335]: 2023-08-21T20:18:29.151958Z 0 [ERROR] Aborting
```



备份命令：



```shell
root@ubuntu:/var/log/mysql# mysqlbinlog mysql-binlog.000001 > backup.sql
```





### 3.3.2 恢复



使用 Mysql 自带的 mysqlbinlog 命令，其作用将二进制的记录转成可见的文本格式（即 SQL 语句），然后交给 mysql 执行可恢复数据，主要参数如下：



```text
root@ubuntu:~# mysqlbinlog [option] log_file
--start-position：指定某个起始偏移量来恢复（事务区间）
--stop-positon：指定某个结束偏移量来恢复（事务区间）
--start-datetime: 指定起始时间(日期区间，e.g:2023-08-21 12:10:36)
--stop-datetime: 指定终止时间(日期区间，e.g:2023-08-21 19:29:00)
```



恢复命令：

要先登录对应数据库，在mysql里执行source xx.sql进行恢复，参考如下：



```shell
root@ubuntu:~# mysql -uroot -pp@ssw0rd test
mysql: [Warning] Using a password on the command line interface can be insecure.
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.42-0ubuntu0.18.04.1-log (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> source /var/log/mysql/backup.sql
Query OK, 0 rows affected (0.00 sec)

................... 省略 ...................

ERROR 1050 (42S01): Table 'user_view' already exists
Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

mysql> 
```



**注意：**

在备份bin-log之前，先 FLUSH LOGS，会自动滚动文件，备份滚动后的文件即可：

```shell
mysql> flush logs;
Query OK, 0 rows affected (0.01 sec)

mysql> 
```



此后，会在目录下生成一个全新数字开始的bin-log文件：

```shell
root@ubuntu:/var/log/mysql# ll
total 40
drwxr-x---  2 mysql adm    4096 Aug 21 13:50 ./
drwxrwxr-x 13 root  syslog 4096 Aug 21 13:22 ../
-rw-r--r--  1 root  root   7037 Aug 21 13:45 backup.sql
-rw-r-----  1 mysql adm    3802 Aug 21 13:46 error.log
-rw-r-----  1 mysql adm    5659 Aug 21 13:16 error.log.1.gz
-rw-r-----  1 mysql mysql  3586 Aug 21 13:50 mysql-binlog.000001
-rw-r-----  1 mysql mysql   154 Aug 21 13:50 mysql-binlog.000002
-rw-r-----  1 mysql mysql    70 Aug 21 13:50 mysql-binlog.index
root@ubuntu:/var/log/mysql# 
```







## 3.4 冷备

Innodb 冷备是最简单的，通常只需写个脚本来复制 MySQL 的文件，然后将这些文件放到对应数据库的目录下即可实现数据恢复：

- .frm结构文件
- .idb独立表空间文件
- redo重做日志文件
- 共享表空间文件
- my.cnf配置文件

缺点是：冷备文件比逻辑文件大，因为存放了很多其他数据，而且不能轻易跨平台（SQL 是标准语句，可跨平台）



### 3.4.1 备份

首先关闭数据库，然后执行下面的命令



#### 3.4.1.1 查看mysql数据存放的目录

```shell
# 	 /var/lib/mysql/data
mysql> show variables like "%datadir%";
+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| datadir       | /var/lib/mysql/ |
+---------------+-----------------+
1 row in set (0.00 sec)

mysql>


$cd /var/lib/mysql/
$tar -zcvf mysqlDataBacku.tar.gz  data/
```





#### 3.4.1.2 备份物理文件



```shell
root@ubuntu:~# cd /var/lib/mysql/
root@ubuntu:/var/lib/mysql# 
root@ubuntu:/var/lib/mysql# tar -zcvf mysql_cool_backup.tar.gz  /data/
```



### 3.4.2 恢复



```shell
# 1. 恢复只需将上面的包解压到对应数据库的数据存放目录下
# 2. 恢复前将原数据备份一下
# 3. 重启mysql即可

root@ubuntu:~# cd /var/lib/mysql/
root@ubuntu:/var/lib/mysql# mv /data/ /data_tmp
root@ubuntu:/var/lib/mysql# tar -zxvf mysql_cool_backup.tar.gz
```





## 3.5 XtraBackup

Innodb 官方有提供热备工具 ibbackup 的收费软件。

不过可以借用 XtraBackup 开源的热备工具，备份和恢复速度比 mysqldump 快，具体的安装过程这里不说明了（```apt install percona-xtrabackup```）。



### 3.5.1 全量备份



#### 3.5.1.1 备份



```shell

root@ubuntu:~# innobackupex 
	--defaults-file=/etc/mysql/my.cnf  # 有数据存放地址
	--user=root 
	--password="123456" 
	--databases=test
	--backup /mysqlBackup/		 # 目录下生成日期命名的目录
```



#### 3.5.1.2 备份一致性



备份一致性，回滚未提交的事务及同步已经提交的事务至数据文件使数据文件处于一致性



```shell
root@ubuntu:~# innobackupex --apply-log /mysqlBackup/2023-08-20_20-39-19/
```



#### 3.5.1.3 恢复



要保证原数据目录是空的，因为目录里有binlog日志



```shell
root@ubuntu:~# innobackupex 
	--defaults-file=/etc/mysql/my.cnf 
	--copy-back /mysqlBackup/2023-08-20_20-39-19/
```





### 3.5.2 增量备份



当数据量比较大的时候（10G），每次都全量备份不太实际，可采用业务比较闲（比如周末）全量备份，其余时间增量备份的策略



原理：

- 首先执行完全备份，并记录下此时检查点 LSN
- 随后的增量备份中，比较表空间每页 LSN 是否大于上次备份的检查点 LSN，是则备份该页并更新当前检查点 LSN





#### 3.5.2.1 全量备份



```shell
root@ubuntu:~# innobackupex 
	--defaults-file=/etc/mysql/my.cnf
	--user=root
	--password="123456"
	--backup /mysqlBackup/
```





#### 3.5.2.2 增量备份



```shell
root@ubuntu:~# innobackupex 
 	--defaults-file=/etc/mysql/my.cnf 
 	--user=root 
 	--password=123456 
 	--incremental /backup/ 			# 增量备份文件目录
	--incremental-basedir=/mysqlBackup/2023-08-20_22-09-29/		# 上次全备或增量备份的目录
```





#### 3.5.2.3 恢复



保证原数据目录为空

```shell
root@ubuntu:~# innobackupex 
	--apply-log /mysqlBackup/2023-08-20_22-09-29/
	--incremental-dir=/mysqlBackup/2023-08-20_22-09-29/
```







# 备份脚本





## shell 脚本



```shell
root@ubuntu:~# cat backup_mysql_db.sh 
#!/bin/bash

#保存备份个数，备份30天数据
number=30

#备份保存路径
backup_dir=/root/mysql_backup

#日期
dd=`date +%Y-%m-%d-%H-%M-%S`

#备份工具
tool=mysqldump

# 被备份的DB信息
username=root
password=123456
database_name=test

if [ ! -d $backup_dir ]; then
    mkdir -p $backup_dir;
fi

$tool -u $username -p$password $database_name > $backup_dir/$database_name-$dd.sql

echo "create $backup_dir/$database_name-$dd.dupm" >> $backup_dir/log.txt

#找出需要删除的备份
delfile=`ls -l -crt $backup_dir/*.sql | awk '{print $9 }' | head -1`

#判断现在的备份数量是否大于$number
count=`ls -l -crt $backup_dir/*.sql | awk '{print $9 }' | wc -l`

if [ $count -gt $number ];then
    #删除最早生成的备份，只保留number数量的备份
    rm $delfile
    #写删除文件日志
    echo "delete $delfile" >> $backup_dir/log.txt
fi

root@ubuntu:~# 
```



执行结果：



```shell
root@ubuntu:~# bash backup_mysql_db.sh 
mysqldump: [Warning] Using a password on the command line interface can be insecure.
root@ubuntu:~# cd mysqlbackup/
root@ubuntu:~/mysql_backup# ll
total 20
drwxr-xr-x 2 root root 4096 Aug 21 14:27 ./
drwx------ 7 root root 4096 Aug 21 14:27 ../
-rw-r--r-- 1 root root  110 Aug 21 14:27 log.txt
-rw-r--r-- 1 root root 3067 Aug 21 14:27 test-2023-08-21-14-27-33.sql
root@ubuntu:~/mysql_backup# 
```







## python脚本



```python
#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import logging
import pymysql
import datetime
import subprocess

# log format
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s:%(message)s',level=logging.INFO)

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
MYSQL_HOST = 'XXX.XXX.XXX.XXX'
MYSQL_USERNAME = 'XXX'
MYSQL_PORT = 3306
MYQSL_PASSWORD = 'XXX'
DISABLED_DATABASES = {'information_schema', 'mysql', 'performance_schema', 'sys'}
BACKUP_PATH = '/backup/mysql/'
# Getting current datetime to create seprate backup folder.
DATETIME = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
TODAYBACKUPPATH = BACKUP_PATH + MYSQL_HOST + '/' + DATETIME
DAY = 30


def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info("Creating backup folder %s", path)
    else:
        logging.info("Path %s exists, no need to create it", path)


def create_mysql_conn(db="mysql"):
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USERNAME,
                           password=MYQSL_PASSWORD, db='mysql')
    return conn


def read_all_databases():
    logging.info('Get all of database names from MySQL')

    conn = create_mysql_conn()
    cursor = conn.cursor()
    cursor.execute('show databases')
    res = cursor.fetchall()
    databases = {item[0] for item in res}
    databases = list(databases - DISABLED_DATABASES)
    cursor.close()
    conn.close()

    logging.info('End to get all of database nemes, now get %s', databases)

    return databases


def backup_database(database):
    logging.info('Start to bakcup database {}...'.format(database))

    command = 'mysqldump -h%s -u%s -p%s %s | gzip > %s/%s.sql.gz' % (
        MYSQL_HOST, MYSQL_USERNAME, MYQSL_PASSWORD, database, TODAYBACKUPPATH, database)

    try:
        subprocess.call(command, shell=True)
    except Exception as ex:
        logging.error('Raise error during backup database, backend return : (%s)', str(ex))

    logging.info('End to backup database %s', database)


def del_old_backup(path):
    old_folder = subprocess.Popen("find {}  -maxdepth 3  -mindepth 2 -mtime +{} -type d".format(path, DAY),stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()

    logging.info('Now delete file : (%s)', old_folder)

    str_old_folder = old_folder[0].decode("utf-8", errors="ignore")
    logging.info("%s", str_old_folder)
    list_lid_folder = str_old_folder.split('\n')

    for folder in list_lid_folder:
        if folder.strip():
            logging.info("Delete %s", folder)
            os.system("rm -rf {}".format(folder))


def backup():
    mkdir_if_not_exists(TODAYBACKUPPATH)
    databases = read_all_databases()
    for database in databases:
        backup_database(database)
    del_old_backup(BACKUP_PATH)


if __name__ == '__main__':
    backup()
```





# 备份MySQL的最佳实践



以下是最佳实践建议，可帮助在备份MySQL数据库时避免一些问题：



1、多种备份方式的组合使用

当备份MySQL数据库时，应使用多种备份方式的组合方式，以确保备份的完整性和稳定性。例如，使用逻辑备份和物理备份的组合，或使用热备和冷备的组合。

备份文件应保留在不同的地方（比如不同的存储主机上），以防止灾难性损失。



2、频繁备份

MySQL数据库应该经常备份，以尽可能减小数据损失。具体的备份频率应该根据业务需要来决定。



3、备份验证

备份文件在完成备份后应该加以验证，这将确保备份的文件完整无损且未被损坏。



4、备份恢复测试

应定期测试备份恢复演示，这将帮助确保备份可以成功地恢复，并且可以提供可靠的备份源。

演示环境尽量是另外一套测试环境，务必避免在生产环境上验证。





# 结语


MySQL备份和恢复是保护和维护数据的最基本的方法之一， 结合业务本身，制定合理、合规的备份策略进行备份，保护企业宝贵数据，确保它们用于处于安全保护状态。

