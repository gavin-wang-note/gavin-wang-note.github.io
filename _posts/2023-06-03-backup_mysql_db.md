---
layout:     post
title:      "备份 TestLink MySQL数据库"
subtitle:   "Backup TestLink MySQL database"
date:       2023-06-03
author:     "Gavin Wang"
catalog:    true
categories:
    - [shell]
    - [mysql]
tags:
    - shell
    - mysql
---



# 概述

Lab 环境中有一套TestLink（测试用例管理平台）和一套 media wiki（存放大家日常工作中写的总结性、经验性文档），他们共用一套MySQL 数据库(不同的db user)。

为了确保数据不丢失，需要每天备份一次mysql，目前的备份策略是全量备份，并同步到一台NAS服务器指定目录。

设置的crontab job，每天凌晨1点执行备份，并sync到一套NAS服务器，完成备份文件的备份，以及清理掉规定日期前的备份文件。


# 实践

## mysql_backup.sh


```shell
#!/bin/bash
#This script backup the mysql databases and attachments automatically.
 
#variable list
DbName=( 'testlink' 'bugs' 'wikidb' )   # testlink, bugzilla, mediawiki
DbUser=( 'root' 'bugs' 'wikiuser' )
DbPwd=( 'p@ssw0rd' 'bigtera!@#' '111111' )
PicPath=( '/var/www/html/testlink/upload_area/nodes_hierarchy/' '' '/var/www/html/mediawiki/images/' )  # 备份附件等其他目录
BackupPath=/root/mysql_backup/
LogFile=/root/mysql_backup/log_file
 
#check the backup file exists or not
if [ ! -d $BackupPath ]; then
    mkdir $BackupPath
fi

echo "-----------------------------------------"
echo $(date +"%y-%m-%d %H:%M:%S")
echo $(date +"%y-%m-%d %H:%M:%S") >> $LogFile
echo "-----------------------------------------"

for ((i=0;i<${#DbName[@]};i++))
do
    NewFile="$BackupPath"${DbName[$i]}_DB_$(date +%y-%m-%d).tar.gz
    DumpFile="$BackupPath"${DbName[$i]}_DB_$(date +%y-%m-%d).sql
    OldFile="$BackupPath"${DbName[$i]}_DB_$(date +%y-%m-%d --date='1 weeks ago').tar.gz

    #create new backup file weekly
    if [ -f $NewFile ]; then
        echo "New backup file have exists!"
    else
        mysqldump -u${DbUser[$i]} -p${DbPwd[$i]} ${DbName[$i]} > $DumpFile
        tar czvf $NewFile $DumpFile ${PicPath[$i]}
        rm -rf $DumpFile
        echo "[$NewFile] backup completely!" >> $LogFile
    fi

    #remove the obsolete file
    if [ -f $OldFile ]; then
        rm -f $OldFile
        echo "delete the old file: [$OldFile]"
    fi
done
```
