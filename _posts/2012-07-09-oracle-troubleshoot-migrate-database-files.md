---
layout:     post
title:      "Oracle案例--迁移数据库控制文件、数据文件、重做日志文件"
subtitle:   "Oracle troubleshoot--Migrate database control files, data files, redo log files"
date:       2012-07-19
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 迁移数据库控制文件、数据文件、重做日志文件


## 适用条件

数据文件、控制文件较大，占用当前磁盘空间，而且当前磁盘剩余空间严重不足。


## 操作步骤

### 首先，移动控制文件

```
        sqlplus / as sysdba 
        create pfile from spfile;  
        shutdown immdiate 
```

### 修改pfile文件中控制文件的位置

如：原先控制文件在/opt/oracle/oradata/mmsgdb/目录下，修改为/home/oradata/mmsgdb/ (这个目录手工建立，并改变属主)

(1) os level级去mv 控制文件 到 新的目录下

(2) startup pfile=‘pfile文件路径’

(3) create spfile from pfile 

注：
* 数据库启动可以指定使用哪个pfile文件，但不能指定使用spfile文件。
  
### 其次，数据文件

```
         shutdown immediate
         os level 级  mv操作
         startup mount
         alter database rename datafile ‘xxxx01.dbf’,’xxxx02.dbf’ to ‘xxxx03.dbf’,’xxx04.dbf’;
         alter database open;  //如果还需要移动重做日志文件，这里可不启动数据库
```

### 再者，重做日志文件

```
        shutdown immediate
        os level nv重做日志文件
        startup mount
        alter database rename file '/opt/oracle/oradata/mmsgdb/redo01.log' to '/home/oradate/redo01.log‘;
        alter database rename file '/opt/oracle/oradata/mmsgdb/redo02.log' to '/home/oradate/redo02.log‘;
        alter database rename file '/opt/oracle/oradata/mmsgdb/redo03.log' to '/home/oradate/redo03.log‘;
        alter database open;
```

