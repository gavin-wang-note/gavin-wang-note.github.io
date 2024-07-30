---
layout:     post
title:      "Oracle监听"
subtitle:   "Oracle Listener"
date:       2013-02-03
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 监听作用

oracle监听器是Oracle服务器软件的一个组件，它负责管理Oracle数据库和客户端之间的通讯，它在一个特定的网卡端口（默认是TCP 1521端口）上监听连接请求，并将连接转发给数据库，由两个二进制文件组成：tnslsnr和lsnrctl。其中tsnlsnr就是监听器本身，它运行在数据库服务器端，lsnrctl是监听器控制程序，用于在服务器上或远程管理监听器。与监听器相关的还有两个配置文件：sqlnet.ora和listener.ora。tnslsnr启动时就会读取这两个配置文件中的信息，如端口号，数据库服务名。

简而言之，oracle监听主要用来监听客户端向数据库服务器端提出的连接请求，是基于服务器端的服务，那么它也只存在于数据库服务器端，进行监听器的设置也是在数据库服务器端完成的。当conn建立连接以后，listener就没有用了，不会再用到了。

# lsnrctl监听命令详解

监听命令是lsnrctl

Oracle用户登陆终端，输入lsnrctl，如下：

```shell
oracle@mmsg1:~> lsnrctl

LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 11-8月 -2010 10:12:17

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

欢迎来到LSNRCTL, 请键入"help"以获得信息。

LSNRCTL> help
以下操作可用
星号 (*) 表示修改符或扩展命令: 

start                 stop                 status              
services              version             reload              
save_config          trace                spawn               
change_password     quit                 exit                
set*                   show*               
```

## 启动指定的监听

```shell
LSNRCTL>start
```
或者

```shell
oracle@mmsg1:~> lsnrctl start
```

## 停止指定的监听

```shell
LSNRCTL>stop
```

或者

```shell
oracle@mmsg1:~> lsnrctl stop
```

## 查看监听状态

```shell
LSNRCTL>status
```

或者

```shell
oracle@mmsg1:~> lsnrctl status
```

显示监听器的状态。Status命令显示监听器是不是活动的，日志与跟踪文件的位置，监听器已经持续运行了多长时间，以及监听器所监听的任务。

```shell
LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 11-8月 -2010 10:29:05

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.167)(PORT=1521)))
LISTENER 的 STATUS
------------------------
别名                      LISTENER
版本                      TNSLSNR for Linux: Version 11.1.0.7.0 - Production
启动日期                  11-8月 -2010 08:56:47
正常运行时间              0 天 1 小时 32 分 18 秒
跟踪级别                  err
安全性                    ON: Local OS Authentication
SNMP                      OFF
监听程序参数文件          /opt/oracle/product/11g/network/admin/listener.ora
监听程序日志文件          /opt/oracle/diag/tnslsnr/mmsg1/listener/alert/log.xml
监听程序跟踪文件          /opt/oracle/diag/tnslsnr/mmsg1/listener/trace/ora_9828_47108097237856.trc
监听端点概要...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=10.137.49.167)(PORT=1521)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
服务摘要..
服务 "PLSExtProc" 包含 1 个例程。
  例程 "PLSExtProc", 状态 UNKNOWN, 包含此服务的 1 个处理程序...
服务 "mmsgdb" 包含 1 个例程。
  例程 "mmsgdb", 状态 UNKNOWN, 包含此服务的 1 个处理程序...
命令执行成功
oracle@mmsg1:~>
```

列举监听器的服务信息，比如这些服务是否有任何专用的预生成服务器进程或与之相关的调度进程，以及每个服务已有多少连接被接受或拒绝。这种方法用来检查一个监听器是否在监听一个指定服务。


## service

列出服务的一个汇总表及为每个协议服务处理程序所建立和拒绝的连接信息个数。

```shell
LSNRCTL> service  
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.167)(PORT=1521)))
服务摘要..
服务 "PLSExtProc" 包含 1 个例程。
  例程 "PLSExtProc", 状态 UNKNOWN, 包含此服务的 1 个处理程序...
    处理程序:
      "DEDICATED" 已建立:0 已被拒绝:0
         LOCAL SERVER
服务 "mmsgdb" 包含 1 个例程。
  例程 "mmsgdb", 状态 UNKNOWN, 包含此服务的 1 个处理程序...
    处理程序:
      "DEDICATED" 已建立:0 已被拒绝:0
         LOCAL SERVER
命令执行成功
LSNRCTL>
```

## version

显示oracle net软件与协议适配器的版本

```shell
LSNRCTL> version
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.167)(PORT=1521)))
TNSLSNR for Linux: Version 11.1.0.7.0 - Production
        TNS for Linux: Version 11.1.0.7.0 - Production
        Unix Domain Socket IPC NT Protocol Adaptor for Linux: Version 11.1.0.7.0 - Production
        Oracle Bequeath NT Protocol Adapter for Linux: Version 11.1.0.7.0 - Production
        TCP/IP NT Protocol Adapter for Linux: Version 11.1.0.7.0 - Production,,
命令执行成功
LSNRCTL>
```

## reload

重新装入监听器，重新读取listener.ora文件，但不关闭监听器。如果该文件发生了变化，重新刷新监听器。

## save_config

当从lsnrctl工具中对listener.ora文件进行了修改时，复制一个叫做listener.bak的listener.ora的文件

## trace

打开监听器的跟踪特性

## change_password

允许用户修改关闭监听器所需要的密码

## quit

退出lsnrctl实用工具

## exit

退出lsnrctl实用工具

# set*

```shell
SNRCTL> set
The following operations are available after set
An asterisk (*) denotes a modifier or extended command:

password                       rawmode                     
displaymode                    trc_file                    
trc_directory                  trc_level                   
log_file                        log_directory               
log_status                     current_listener            
inbound_connect_timeout     startup_waittime            
save_config_on_stop          dynamic_registration        

LSNRCTL>
```

**password**

指定在lsnrctl命令行工具中执行管理任务所需要的密码

## rawmode

指定原始模式，默认为OFF。

## displaymode

指定服务显示模式，默认设置为：NORMAL。

## trc_file

指定监听器跟踪信息的位置。默认设置是$ORACLE_HOME\network\trace\listener.trc

## trc_directory

指定trace文件路径，默认设置为：$ORALCE_BASE/ diag/tnslsnr/hostname/ listener/trace。

## trc_level

跟踪级别 ，OFF - 未启用跟踪功能。OFF 为默认设置。 

其中，0和1  ：off
      2和3  ：err
      4和5  ：user
      6~10   ：admin

示例:

```shell
LSNRCTL> set trc_level 1
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 off
LSNRCTL> set trc_level 2
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 err
命令执行成功
LSNRCTL> set trc_level 3
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 err
命令执行成功
LSNRCTL> set trc_level 4
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 user
命令执行成功
LSNRCTL> set trc_level 5
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 user
命令执行成功
LSNRCTL> set trc_level 6
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 admin
命令执行成功
LSNRCTL> set trc_level 7
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 admin
命令执行成功
LSNRCTL> set trc_level 8
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 admin
命令执行成功
LSNRCTL> set trc_level 9
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 admin
命令执行成功
LSNRCTL> set trc_level 10
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 admin
命令执行成功
LSNRCTL> set trc_level 0
正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.114)(PORT=1521)))
STRAYEAGLE 参数 "trc_level" 设为 off
命令执行成功
```

## log_file

指定监听日志文件名，默认为：$ORACLE_BASE/ diag/tnslsnr/hostname/ listener/alert/log.xml。

## log_directory

指定监听日志文件存放路径，默认为：$ORACLE_BASE/ diag/tnslsnr/hostname/ listener/alert

## log_status

指定一个监听器将把日志信息写到哪里。这个参数在默认的情况下是ON,并默认为%oracle_home%\network\log\listener.log

## current_listener

显示当前监听器名称。

## inbound_connect_timeout

定义监听器在一个会话得到启动时将等待的有效响应时间。默认设置为10秒。

## startup_waittime

定义监听器在响应lsnrctl命令行工具中的一条status命令之前将等待多长时间。

## save_config_on_stop

指定在一个lsnrctl会话期内所发生的修改在退出时是否应该被保存起来。

# show*

```shell
LSNRCTL> show     
The following operations are available after show
An asterisk (*) denotes a modifier or extended command:

rawmode                     displaymode                 
rules                       trc_file                    
trc_directory               trc_level                   
log_file                    log_directory               
log_status                  current_listener            
inbound_connect_timeout     startup_waittime            
snmp_visible                save_config_on_stop         
dynamic_registration        
```

## rawmode

显示关于status和service的较详细信息（当他们设置成on时）值为ON或OFF


## displaymode

把lsnrctl工具的显示模式设置成raw、compact、normal或verbose

服务显示模式为NORMAL


## rules

过滤规则

```shell
LSNRCTL> show rules
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
No filtering rules currently in effect.
The command completed successfully
LSNRCTL>
```

## trc_file

指定监听器跟踪信息的位置。默认设置是$ORACLE_HOME\network\trace\listener.trc

```shell
LSNRCTL> show  trc_file   
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "trc_file" set to ora_4825_47881906824032.trc
The command completed successfully
LSNRCTL>
```

## trc_directory

```shell
LSNRCTL> show trc_directory
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "trc_directory" set to /opt/oracle/diag/tnslsnr/node1/listener/trace
The command completed successfully
LSNRCTL>
```

## trc_level

```shell
LSNRCTL> show trc_level
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "trc_level" set to off
The command completed successfully
LSNRCTL>
```

## log_file

指定一个监听器将把日志信息写到哪里。这个参数在默认的情况下是ON,并默认为%oracle_home%\network\log\listener.log

```shell
LSNRCTL> show log_file
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "log_file" set to /opt/oracle/diag/tnslsnr/node1/listener/alert/log.xml
The command completed successfully
LSNRCTL>
```

## log_directory

```shell
LSNRCTL> show log_directory
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "log_directory" set to /opt/oracle/diag/tnslsnr/node1/listener/alert
The command completed successfully
LSNRCTL> 
log_status
LSNRCTL> show log_status
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "log_status" set to ON
The command completed successfully
LSNRCTL>
```

## current_listener

```shell
LSNRCTL> show current_listener
Current Listener is LISTENER
LSNRCTL>
```

## inbound_connect_timeout

定义监听器在一个会话得到启动时将等待的有效响应时间。默认设置为60秒。

```shell
LSNRCTL> show inbound_connect_timeout
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "inbound_connect_timeout" set to 60
The command completed successfully
LSNRCTL>
```

## startup_waittime

定义监听器在响应lsnrctl命令行工具中的一条status命令之前将等待多长时间。

```shell
LSNRCTL> show startup_waittime
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "startup_waittime" set to 0
The command completed successfully
LSNRCTL>
snmp_visible
LSNRCTL> show snmp_visible
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "snmp_visible" set to OFF
The command completed successfully
LSNRCTL>
```

## save_config_on_stop

指定在一个lsnrctl会话期内所发生的修改在退出时是否应该被保存起来。

```shell
LSNRCTL> show save_config_on_stop
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.119)(PORT=1521)))
LISTENER parameter "save_config_on_stop" set to OFF
The command completed successfully
LSNRCTL>
```

# 使用监听与数据库建立连接的另一种方式

```shell
sqlplus mmsg/mmsg@10.137.49.119:1521/mmsgdb 
```

# 客户端如何通过监听与server建立连接

sqlnet.ora文件内容 

```shell
NAMES.DIRECTORY_PATH= (TNSNAMES,HOSTNAME)
```

当你输入sqlplus mmsg/mmsg@mmsgdb的时候

1． 查询sqlnet.ora看看名称的解析方式，发现是TNSNAME

2． 则查询tnsnames.ora文件，从里边找mmsgdb的记录，并且找到主机名，端口和service_name

3． 如果listener进程没有问题的话，建立与listener进程的连接。

4． 根据不同的服务器模式如专用服务器模式或者共享服务器模式，listener采取接下去的动作。默认是专用服务器模式，没有问题的话客户端就连接上了数据库的server process。

5． 这时候网络连接已经建立，listener进程的历史使命也就完成了。

# 几种连接用到的命令形式

1.sqlplus / as sysdba 这是典型的操作系统认证，不需要listener进程

2.sqlplus sys/passwd as sysdba 这种连接方式只能连接本机数据库，同样不需要listener进程

3.sqlplus sys/passwd@dbname  as sysdba 这种方式需要listener进程处于可用状态。最普遍的通过网络连接。

以上连接方式使用sys用户或者其他通过密码文件验证的用户都不需要数据库处于可用状态，操作系统认证也不需要数据库可用，普通用户因为是数据库认证，所以数据库必需处于open状态。


# 监听注册

注册就是将数据库作为一个服务注册到监听程序。

客户端不需要知道数据库名和实例名，只需要知道该数据库对外提供的服务名就可以申请连接到数据库。这个服务名可能与实例名一样，也有可能不一样。 

## 当监听的端口非1521时候，如何使得监听进行动态注册

通过修改参数local_listener 进行。

### 方法一

可以设置local_listener=listener，前提条件是将lsnrctl.ora文件中的listener信息添加到tnsnames.ora文件中，因为pmon进程动态注册监听时会通过读取tnsname.ora文件相关信息

```shell
alter system set local_listener=listener;
```

添加lsnrctl.ora文件内容到tnsnames.ora文件中。

### 方法二

可以设置local_listener参数为lister.ora文件中的address和address_list 

```shell
alter system set local_listener = '(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.37)(PORT=1522))';
```

## 如何判断监听是否已注册

通过查看监听当前状态，根据如下红色加粗部分信息判别：

```shell
oracle@GW_8:~> lsnrctl status

LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 01-2月 -2013 11:59:06

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1521)))
LISTENER 的 STATUS
------------------------
别名                      LISTENER
版本                      TNSLSNR for Linux: Version 11.1.0.7.0 - Production
启动日期                  29-1月 -2013 10:05:29
正常运行时间              3 天 1 小时 53 分 36 秒
跟踪级别                  off
安全性                    ON: Local OS Authentication
SNMP                      OFF
监听程序参数文件          /opt/oracle/product/11g/network/admin/listener.ora
监听程序日志文件          /opt/oracle/diag/tnslsnr/GW_8/listener/alert/log.xml
监听端点概要...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=10.41.16.50)(PORT=1521)))
服务摘要..
服务 "mmsgdb" 包含 1 个例程。
  例程 "mmsgdb", 状态 READY, 包含此服务的 1 个处理程序...
服务 "mmsgdb_XPT" 包含 1 个例程。
  例程 "mmsgdb", 状态 READY, 包含此服务的 1 个处理程序...
```

说明：

* 监听分静态注册与动态注册，注册过程由oracle的PMON进程完成，PMON进程仅默认对1521端口的监听进行注册，非1521端口无法自动注册。

# local_listener与remote_listener

<img class="shadow" src="/img/in-post/oracle_listener_remote_listener.png" width="1200">

