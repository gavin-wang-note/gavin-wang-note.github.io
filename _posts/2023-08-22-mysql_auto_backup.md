---
layout: post
title: "mysql 增量备份"
subtitle: "MySQL incremental backup"
date: 2023-08-22
author: "Gavin Wang"
catalog: true
summary: MySQL数据库增量备份
categories: 
    - [python]
    - [mysql]
tags:
    - python
    - mysql
---



# 概述


本文介绍使用python开发一自动备份MySQL数据库工具，完成MySQL数据库定期备份动作。




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



说明：

本文只是示例，所以创建的数据库test中表、视图无论结构还是数据量，都非常小，仅做示例使用。





# 备份策略



* 借助innobackupex实现数据库的备份动作
* 每天凌晨两点自动进行备份
* 每周日进行一次全量备份，其他周天则进行增量备份
* 备份目录保留30天



如下图所示：


<img class="shadow" src="/img/in-post/backup_mysql.bmp" width="1200">





# 备份脚本



``` mysql_backup.py ``` 内容如下：



```python
root@ubuntu:~# cat mysql_backup.py 
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import os
import sys
import commands 
import time
import logging
import subprocess

# Set log format
log_file = "/var/log/backup_mysql.log"
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s:%(message)s',
                            level=logging.INFO, filename=log_file, filemode='a')

mysql_username = 'root'
mysql_password = 'p@ssw0rd'
incremental_backup_path = '/backup/mysql/incremental'
incremental_backup_base_path = '/backup/mysql/base/'
keep_days = 30
mysql_cnf = "/etc/mysql/my.cnf"


def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info("Creating backup folder %s", path)
    else:
        logging.info("Path %s exists, no need to create it", path)


def juge_weekday():
    cur_day = datetime.datetime.now().strftime("%Y-%m-%d")
    weeks = datetime.datetime.fromtimestamp(time.mktime(time.strptime(cur_day, "%Y-%m-%d"))).weekday() + 1

    return weeks


def full_backup_database(db='mysql'):
    complete_ok = False
    backup_base_path = ''
    full_backup_cmd = "innobackupex  --defaults-file={} --user={} --password={} " \
                      "--databases={} --backup {}".format(mysql_cnf, mysql_username,
                                                          mysql_password, db,
                                                          incremental_backup_base_path)

    logging.info("Start to full backup database : (%s)", db)

    output =  commands.getoutput(full_backup_cmd).strip()

    if 'completed OK' in output:
        complete_ok = True

    for each_line in output.split("\n"):
        if 'Backup created in directory' in each_line:
            backup_base_path = each_line.split()[-1].replace("'", '')

    if not os.path.exists(backup_base_path):
        logging.error("Not find backup base path, exit!!!")
        sys.exit(1)

    if complete_ok:
        logging.info("Full backup database : (%s) success", db)
    else:
        logging.error("Full backup database : (%s) failed, please view log : (%s)", db, output)
        sys.exit(1)


def get_latest_subdir():
    all_subdirs = [incremental_backup_base_path + os.sep + d for d in os.listdir(incremental_backup_base_path) if os.path.isdir(incremental_backup_base_path + os.sep + d)]
    if len(all_subdirs):
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        return latest_subdir
    else:
        logging.error("Not get apply log path!")
        return

def apply_log(backup_base_path, db='mysql'):
    complete_ok = False
    apply_cmd = "innobackupex --apply-log {}".format(backup_base_path)

    logging.info("Start to apply log")

    output =  commands.getoutput(apply_cmd).strip()
    if 'completed OK' in output:
        complete_ok = True

    if complete_ok:
        logging.info("Apply log : (%s) success", backup_base_path)
    else:
        logging.error("Apply log : (%s) failed, please view log : (%s)", backup_base_path, output)
        sys.exit(1)


def incremental_backup(backup_base_path, db='mysql'):
    complete_ok = False
    incremental_cmd = "innobackupex --defaults-file={} --user={}" \
                      "--password={} --databases={} --incremental {} " \
                      "--incremental-basedir={}".format(mysql_cnf, mysql_username,
                                                        mysql_password, db,
                                                        incremental_backup_path,
                                                        backup_base_path)

    logging.info("Start incremental backup database")

    output =  commands.getoutput(incremental_cmd).strip()
    if 'completed OK' in output:
        complete_ok = True

    if complete_ok:
        logging.info("Incremental backup database : (%s) success", db)
    else:
        logging.error("Incremental backup database : (%s) failed, please view log : (%s)", db, output)
        sys.exit(1)

    logging.info("Success to backup database : (%s)", db)


def del_old_backup(path):
    old_folder = subprocess.Popen("find {}  -maxdepth 3  -mindepth 2 -mtime +{} -type d".format(path, keep_days),stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()
    if None not in old_folder:  # Find the folder
        logging.info('Now delete file : (%s)', old_folder)

        # str_old_folder = old_folder[0].decode("utf-8", errors="ignore")
        str_old_folder = old_folder[0]
        logging.info("%s", str_old_folder)
        list_lid_folder = str_old_folder.split('\n')

        for folder in list_lid_folder:
            if folder.strip():
                logging.info("Delete %s", folder)
                os.system("rm -rf {}".format(folder))
    else: #old_folder like this ('', None) if not find folders
        logging.info("No folders find under [{}] to delete, skip".format(path))


def loop_backup_mysql(db):
    weeks = juge_weekday()
    apply_log_path = get_latest_subdir()

    if apply_log_path:
        if weeks == 7:
            full_backup_database(db)
            new_apply_log_path = get_latest_subdir()
            if apply_log_path == new_apply_log_path:
                apply_log(apply_log_path, db)
            else:
                apply_log(new_apply_log_path, db)
        else:
            new_apply_log_path = get_latest_subdir()
            if apply_log_path == new_apply_log_path:
                incremental_backup(apply_log_path, db)
            else:
                incremental_backup(new_apply_log_path, db)
    else:
        # First time to backup, so run full backup
        full_backup_database(db)
        apply_log_path = get_latest_subdir()


if __name__ == '__main__':
    logging.info("-" * 80)
    # If path not exist, create it
    if not os.path.exists(incremental_backup_base_path):
        mkdir_if_not_exists(incremental_backup_base_path)

    if not os.path.exists(incremental_backup_path):
        mkdir_if_not_exists(incremental_backup_path)

    # Backup database
    db = 'test'
    loop_backup_mysql(db)

    # Delete old folders
    del_old_backup(incremental_backup_path)
    del_old_backup(incremental_backup_base_path)

root@ubuntu:~#
```



**说明：**

* 日志记录/var/log/backup_mysql.log 文件中
* '/backup/mysql/base/' 存放全量备份的数据库备份信息
*  '/backup/mysql/incremental' 存放增量数据库的备份信息
* 判断当前日期是星期几，如果结果是7表明为周日，则进行全量备份，否则进行增量备份
* 无论是全量备份还是增量备份，备份目录下只保留30天的备份记录，过期目录将被清理掉（先备份后清理）





# 定时任务设置



```shell
0 2 * * * python /usr/local/bin/mysql_backup.py 
```



每天凌晨两点执行备份操作，备份脚本自动识别当前日期是星期几，如果是星期日，则进行全量备份；否则进行增量备份。





# 恢复



建议手工进行恢复，参考命令如下：

```shell
root@ubuntu:~# innobackupex 
	--apply-log /mysql_backup/2023-08-21_23-19-39/
	--incremental-dir=/mysql_backup/2023-08-21_23-19-39/
```




