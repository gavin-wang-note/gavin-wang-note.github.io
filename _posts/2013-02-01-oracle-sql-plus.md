---
layout:     post
title:      "Oracle SQL*Plus"
subtitle:   "Oracle SQL*Plus"
date:       2013-02-01
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 前言

Oracle SQL*Plus是连接Oracle常用的工具，本文介绍这个工具的常用命令行。

# Oracle的SQL*Plus工具中清屏

有时候SQL*Plus工具中输出的信息过多，想清除当前的信息，如同Linux系统的清屏操作。

汇总了oracle的SQL*Plus工具的清屏的几个方法，参考如下：

* 方法一：如果在window窗口下sqlplus 中清屏命令：host cls 或是clear screen 或只是4位 clea scre

* 方法二：如果是在dos的窗口下进入sql/plus就要用clear SCR。【不区分大小写的】

* 方法三：在Unix/Linux系统下，使用!clear命令

汇总如下：

## Windows平台

```
host cls
clear screen
clea scre
clear scr
clea scr
```

## Unix/Linux平台

```
clear screen
clea scre
clear scr
clea scr
!clear
```

# SQL*Plus系统环境变量信息以及如何修改这些变量信息

```
show和set命令是两条用于维护SQL*Plus系统变量的命令 
      SQL> show all          --查看所有68个系统变量值 
      SQL> show user         --显示当前连接用户 
      SQL> show error　　　　--显示错误 
      SQL> set heading off  --禁止输出列标题，默认值为ON 
      SQL> set feedback off --禁止显示最后一行的计数反馈信息，默认值为"对6个或更多的记录，回送ON" 
      SQL> set timing on      --默认为OFF，设置查询耗时，可用来估计SQL语句的执行时间，测试性能 
      SQL> set sqlprompt "SQL> "    --设置默认提示符，默认值就是"SQL> " 
      SQL> set linesize 1000         --设置屏幕显示行宽，默认100 
      SQL> set autocommit ON         --设置是否自动提交，默认为OFF 
      SQL> set pause on     --默认为OFF，设置暂停，会使屏幕显示停止，等待按下ENTER键，再显示下一页 
      SQL> set arraysize 1  --默认为15 
      SQL> set long 1000     --默认为80 
```

说明：
* long值默认为80，设置1000是为了显示更多的内容，因为很多数据字典视图中用到了long数据类型，如：

```
SQL> desc user_views
列名                          可空值否   类型
------------------------------- -------- ----
VIEW_NAME                       NOT NULL VARCHAR2(30)
TEXT_LENGTH                              NUMBER
TEXT                                     LONG
```

# SQL*PLUS常用命令列表

命令列表： 

假设当前执行命令为：```select * from tab; ```

```
(a)ppend　　　　      添加文本到缓冲区当前行尾　　　　a  order by tname　
结果：select * from tab order by tname;
（注：a后面跟2个空格）
(c)hange/old/new  在当前行用新的文本替换旧的文本　c/*/tname　　　　结果：select tname from tab;
(c)hange/text　　从当前行删除文本　　　　　　　　 c/tab　　　　　　　结果：select tname from;


del　　　　　　　删除当前行
del n　　　　　　删除第n行


(i)nput 文本　　 在当前行之后添加一行
(l)ist　　　　　 显示缓冲区中所有行
(l)ist n　　　　 显示缓冲区中第 n 行

(l)ist m n　　　 显示缓冲区中 m 到 n 行

run　　　　　　　执行当前缓冲区的命令
/　　　　　　　　执行当前缓冲区的命令
r　　　　　　　　执行当前缓冲区的命令


@文件名　　　　　运行调入内存的sql文件，如： 
SQL> edit s<回车>
如果当前目录下不存在s.sql文件，则系统自动生成s.sql文件，
在其中输入“select * from tab;”，存盘退出。 
SQL> @s<回车>
系统会自动查询当前用户下的所有表、视图、同义词。 


@@文件名　　　　 在.sql文件中调用令一个.sql文件时使用 
save 文件名　　　将缓冲区的命令以文件方式存盘，缺省文件扩展名为.sql
get 文件名　　　 调入存盘的sql文件
start 文件名　　 运行调入内存的sql文件 
spool 文件名　　 把这之后的各种操作及执行结果“假脱机”即存盘到磁盘文件上，默认文件扩展名为.lst
spool　　　　　　显示当前的“假脱机”状态
spool off　　　　停止输出
例：
SQL> spool a
SQL> spool
正假脱机到 A.LST
SQL> spool off
SQL> spool
当前无假脱机 

exit　　　　　　  退出SQL*PLUS
desc 表名　　　　 显示表的结构
show user　　　　显示当前连接用户
show error　　　 显示错误
show all　　　　 显示所有68个系统变量值
edit　　　　　　  打开默认编辑器，Windows系统中默认是notepad.exe，把缓冲区中最后一条SQL语句调入afiedt.buf文件中进行编辑
edit 文件名　　　 把当前目录中指定的.sql文件调入编辑器进行编辑 
clear screen　　 清空当前屏幕显示
```

# 退出SQL，进入OS命令模式

使用英文输入法中的感叹号”!”，即可从SQL模式退出到Linux/Unix命令行模式下。

```
SQL> show parameter processes

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
aq_tm_processes                      integer     0
db_writer_processes                  integer     1
gcs_server_processes                 integer     0
global_txn_processes                 integer     1
job_queue_processes                  integer     1000
log_archive_max_processes            integer     4
processes                            integer     1000
SQL> !
oracle@GW_8:~> exit
exit
```

在SQL模式下执行linux/unix命令
在linux/unix命令前，增加host命令，即可在不退出SQL模式下执行Linux/Unix命令.

```
SQL> host ls -l
total 5902
-rw-r--r--  1 oracle oinstall  371339 2012-11-28 15:49 14_45.html
-rw-r--r--  1 oracle oinstall  369040 2012-11-28 15:50 15_00.html
-rw-r--r--  1 oracle oinstall  368320 2012-11-28 15:51 15_15.html
-rw-r--r--  1 oracle oinstall  369926 2012-11-28 16:06 15_30.html
-rw-r--r--  1 oracle oinstall  379080 2012-11-28 16:03 15_45.html
-rw-r--r--  1 oracle oinstall  375061 2012-11-28 16:16 16_00.html
-rw-r--r--  1 oracle oinstall  374294 2012-11-28 16:35 16_15.html
-rw-r--r--  1 oracle oinstall  335887 2012-11-28 17:43 16_30.html
-rw-r--r--  1 oracle oinstall  410141 2012-11-28 14:36 9i.html
-rw-r--r--  1 oracle oinstall  401129 2012-11-28 14:41 9j.html
drwxr-x---  3 oracle oinstall      72 2012-10-11 15:17 admin
-rw-r--r--  1 oracle oinstall   16384 2013-01-08 09:53 a_tab.dmp
-rw-r--r--  1 oracle oinstall 2242560 2012-11-28 16:18 awrlog.tar
drwxr-xr-x  2 oracle oinstall      48 2012-10-11 13:58 bin
drwxr-x---  5 oracle oinstall     120 2012-10-11 15:35 cfgtoollogs
-rw-r--r--  1 oracle oinstall     475 2013-01-05 14:18 createuser.sql
drwxr-xr-x  2 oracle oinstall     208 2012-11-13 14:57 dbscript
drwxr-xr-x  2 oracle oinstall     208 2012-12-03 10:05 dbscript_zzz
drwx------  2 oracle oinstall     256 2012-10-11 14:08 Desktop
drwxrwxr-x 11 oracle oinstall     264 2012-10-11 15:17 diag
drwx------  2 oracle oinstall      80 2012-10-11 13:58 Documents
drwxr-xr-x  4 oracle oinstall     224 2012-10-11 15:01 install
drwxr-xr-x  2 oracle oinstall     216 2012-10-27 10:54 jc
drwxr-xr-x  2 oracle oinstall      48 2012-11-22 17:24 mmsgdpzsscripts
drwxr-xr-x  5 oracle oinstall     120 2013-01-28 19:16 mmsgrptscripts
drwxr-xr-x  2 oracle oinstall     184 2012-11-13 15:15 nss
drwxrwxrwx  3 oracle oinstall     200 2013-01-25 14:25 oradata
drwxr-xr-x  3 oracle oinstall      72 2012-10-24 15:24 oradiag_oracle
drwxrwx---  6 oracle oinstall     224 2012-12-05 08:59 oraInventory
drwxr-xr-x  3 oracle oinstall      72 2012-10-11 15:02 product
drwxr-xr-x  2 oracle oinstall      80 2012-10-11 13:58 public_html
drwxr-xr-x  2 oracle oinstall     248 2012-12-05 14:25 qmg
drwxr-xr-x  2 oracle oinstall     200 2012-10-24 10:54 zhy

SQL>
```

