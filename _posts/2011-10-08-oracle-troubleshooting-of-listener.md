---
layout:     post
title:      "Oracle案例之监听"
subtitle:   "Oracle troubleshooting of listener"
date:       2011-10-08
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# 概述

listener，主要用来监听客户端向数据库服务器端提出的连接请求，是基于服务器端的服务，那么它也只存在于数据库服务器端，进行监听器的设置也是在数据库服务器端完成的。

要排除客户端与服务器端的连接问题，首先检查客户端配置是否正确(客户端配置必须与数据库服务器端监听配置一致)，再根据错误提示解决。本文主要介绍在使用oracle过程中，碰到的一些监听故障/问题的记录/汇总。


# ORA-12541: TNS: 没有监听器

显而易见，服务器端的监听器没有启动，另外检查客户端IP地址或端口填写是否正确。启动监听器：

```
$ lsnrctl start
```

# ORA-12500: TNS: 监听程序无法启动专用服务器进程

没有启动Oracle实例服务。启动实例服务。

# ORA-12535: TNS: 操作超时

```
TNS-12154 (ORA-12154)：TNS:could not resolve service name
```

检查输入的服务名与配置的服务名是否一致。另外注意生成的本地服务名文件(Linux/Unix下$ORACLE_HOME/network/admin/tnsnames.ora)里每项服务的首行服务名称前不能有空格。

# ORA-12514: TNS: 监听进程不能解析在连接描述符中给出的 SERVICE_NAME

检查tnsnames.ora里的服务名输入是否正确。该服务名必须与服务器端监听器配置的全局数据库名一致。

# ORA-12514:TNS:：监听程序当前无法识别连接描述符中请求的服务

现象：

（1）在服务端和客户端使用sqlplus user/password@SID均无法连接

（2）在服务端使用sqlplus user/password@SID可以建立连接，客户端使用使用sqlplus user/password@SID无法建立连接。

解决：

（方法1）检查listener.ora以及tnsnames.ora文件。主要是检查文件中的HOST是否为

当前主机名（hostname），如果不是，修改成当前主机名（hostname）或IP地址；

（方法2）在listener.ora文件中添加SID_LIST_LISTENER信息。

创建监听错误

<img class="shadow" src="/img/in-post/oracle-listener-create-error.png" widtgh="1200">
 
这个问题的解决方法如下：

在ORACLE_HOME/network/admin/listener.ora文件中增加"SID_LIST_LISTENER = "这部分内容。

```
LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST=10.164.75.167)(PORT = 1521))
    )
  )
SID_LIST_LISTENER =
    (SID_DESC =
      (GLOBAL_DBNAME = ora11g)       //ora11g是数据库实例名
      (ORACLE_HOME = /opt/oracle/app/product/11.1.0/db_1)    //oracle家目录
      (SID_NAME = ora11g)           
    )
  )
```

注：

Oracle System Identifier (SID)

```
A name that identifies a specific instance of a running pre-release 8.1 Oracle
database. For any database, there is at least one instance referencing the database.
For pre-release 8.1 databases, SID is used to identify the database. The SID is
included in the connect descriptor of a tnsnames.ora file and in the definition of the
listener in the listener.ora file.
```

如果SID值不作人为的修改，该值默认为PLSExtProc，且完全可以正常运行（目前141  上的数据库该值就是PLSExtProc）。因此我觉得可能是如果不指定SID值的话，oracle会自动地去搜索运行的实例，然后找出一个匹配的，但是如果直接指定SID，则省去了搜索的步骤，也就加快了连接速度。不过这种猜想目前尚未得到证实，如果大家对这方面了解的话，希望不吝赐教。

# 启动监听时出错 -- 12514

正确创建监听后，启动监听时监听启动异常，报12514错误。

```
oerr ora 12514
12514, 00000, "TNS:listener does not currently know of service requested in connect descriptor"
// *Cause:  The listener received a request to establish a connection to a
// database or other service. The connect descriptor received by the listener
// specified a service name for a service (usually a database service)
// that either has not yet dynamically registered with the listener or has
// not been statically configured for the listener.  This may be a temporary
// condition such as after the listener has started, but before the database
// instance has registered with the listener.
// *Action:
//  - Wait a moment and try to connect a second time.
//  - Check which services are currently known by the listener by executing:
//    lsnrctl services <listener name>
//  - Check that the SERVICE_NAME parameter in the connect descriptor of the
//    net service name used specifies a service known by the listener.
//  - If an easy connect naming connect identifier was used, check that
//    the service name specified is a service known by the listener.
//  - Check for an event in the listener.log file.
```

解决方法同上。

如果出现TNS错误时，有可能是因为没有加载数据库实例，加载方法如下：

在SQL/PLUS中输入startup force，强制加载数据库实例。

# oracle数据库监听启动失败，报00525，12560等错的解决方法

启动数据库监听，报如下警告：

```
LSNRCTL> start
Starting /opt/oracle/product/11g//bin/tnslsnr: please wait...
TNSLSNR for Linux: Version 11.1.0.7.0 - Production
System parameter file is /opt/oracle/product/11g//network/admin/listener.ora
Log messages written to /opt/oracle/diag/tnslsnr/RAC2/listener/alert/log.xml
Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=RAC2)(PORT=1521)))
Error listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1521)))
TNS-12555: TNS:permission denied
 TNS-12560: TNS:protocol adapter error
  TNS-00525: Insufficient privilege for operation
   Linux Error: 1: Operation not permitted
Listener failed to start. See the error message(s) above...
```

原因分析

TCP监听正常，IPC监听失败，由TNS-12555和TNS-12560错误确定是IPC协议出错，由TNS-00525确定是权限不足，查看/tmp/.oracle目录下无内容，可以确定是因为某种原因，oracle不能在该目录下生成IPC监听的KEY值，导致IPC监听失败.

解决方法

将ICP监听取消，将 (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))这句话注释掉不使用，可以暂时解决该问题。可以使数据库作为客户端来使用

方法二：

修改如下文件夹的权限

```
/tmp/.oracle的权限 
/var/tmp/.oracle的权限 
```

oracle应该有这些目录的权限，用oinstall 

```
chown -R  oracle:oinstall /tmp/.oracle 
chown -R  oracle:oinstall /var/tmp/.oracle 
```

# AIX下监听无法停止

AIX下ORACLE11G（版本：Oracle Database 11g Enterprise Edition Release 11.1.0.6.0 - 64bit Production）监听停止、启动失败

表象:

停止监听

```
% lsnrctl stop
LSNRCTL for IBM/AIX RISC System/6000: Version 11.1.0.6.0 - Production on 17-6月 -2009 19:22:34
Copyright (c) 1991, 2007, Oracle.  All rights reserved.
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=infox2)(PORT=1521)))
TNS-01190: The user is not authorized to execute the requested listener command
```

启动监听

```
% lsnrctl start
LSNRCTL for IBM/AIX RISC System/6000: Version 11.1.0.6.0 - Production on 17-6月 -2009 19:51:21
Copyright (c) 1991, 2007, Oracle.  All rights reserved.
Starting /opt/oracle/app/product/11.1.0/db_1/bin/tnslsnr: please wait...
TNSLSNR for IBM/AIX RISC System/6000: Version 11.1.0.6.0 - Production
System parameter file is /opt/oracle/app/product/11.1.0/db_1/network/admin/listener.ora
Log messages written to /opt/oracle/app/diag/tnslsnr/infox2/listener/alert/log.xml
Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=infox2)(PORT=1521)))
Error listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1521)))
TNS-12555: TNS:permission denied
 TNS-12560: TNS:protocol adapter error
  TNS-00525: Insufficient privilege for operation
   IBM/AIX RISC System/6000 Error: 1: Not owner
Listener failed to start. See the error message(s) above...
```

解决方法

修改ORACLE_HOME目录下lintener.ora文件，例如修改为：

```
LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST=10.164.75.22)(PORT = 1521))
    )
  )
  
SID_LIST_LISTENER =
    (SID_DESC =
      (GLOBAL_DBNAME = smsgrpt)       //实例名
      (ORACLE_HOME = /opt/oracle/app/product/11.1.0/db_1)   // ORACLE_HOME 目录路径
      (SID_NAME = smsgrpt)           
    )
  )
```

注：
oracle版本为Version 11.1.0.6.0的，几乎都会遇见上述监听相关问题，解决方法一般都是增加SID信息。


# 结语

当不得已而为之的时候，删除监听，重新建立一个监听。

测试tns的时候，可以通过tnsping 来进行。

在服务器测试，示例如下：

```
tnsping mmsgdb（这里的mmsgdb是数据库的实例名） 
```

客户端测试如下：

```
tnsping 10.164.75.220/mmsgdb
```

以上是Oracle客户端连接服务器端常见的一些问题，当然不能囊括所有的连接异常。解决问题的关键在于方法与思路，而不是每种问题都有固定的答案。

# TNS-01189案例

表象:

```
oracle@mmsg01:~/product/11g/network/admin> lsnrctl status

LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 31-3?? -2010 18:09:47

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

?y?úá??óμ? (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=mmsg01)(PORT=1521)))
TNS-01189: 监听程序无法验证用户
oracle@mmsg01:~/product/11g/network/admin> lsnrctl stop  

LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 31-3?? -2010 18:09:50

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

?y?úá??óμ? (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=mmsg01)(PORT=1521)))
TNS-01189: 监听程序无法验证用户
oracle@mmsg01:~/product/11g/network/admin> lsnrctl start

LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 31-3?? -2010 18:09:51

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

TNS-01106: 00106 使用名称LISTENER的监听程序已经启动
oracle@mmsg01:~/product/11g/network/admin>
```

原因

解析主机名出错。

主机名为mmsg01，而在/etc/hosts文件中，虽然找到了主机名为mmsg01的记录，但是ifconfig观察之后，发现小网段（192网段）显示的IP信息与/etc/hosts文件中不一致，且/etc/hosts文件中缺少外网段（10网段）的记录。

解决方法

修改/etc/hosts文件，增加小网段和外网段信息，例如：

```
192.168.100.106 mmsg01
10.164.75.102    mmsg01
```

# 机器更换IP后监听启动失败

日志

```
<msg time='2010-04-20T09:56:43.897+08:00' org_id='oracle' comp_id='tnslsnr'
 type='UNKNOWN' level='16' host_id='mmsg'
 host_addr='10.164.74.222'>
 <txt>以 pid=14276 开始
 </txt>
</msg>
<msg time='2010-04-20T09:56:43.898+08:00' org_id='oracle' comp_id='tnslsnr'
 type='UNKNOWN' level='16' host_id='mmsg'
 host_addr='10.164.74.222'>
 <txt>监听: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=10.137.49.114)(PORT=1521)))
 </txt>
</msg>
<msg time='2010-04-20T09:56:43.898+08:00' org_id='oracle' comp_id='tnslsnr'
 type='UNKNOWN' level='16' host_id='mmsg'
 host_addr='10.164.74.222'>
 <txt>监听: (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
 </txt>
</msg>
<msg time='2010-04-20T09:56:44.011+08:00' org_id='oracle' comp_id='tnslsnr'
 type='UNKNOWN' level='16' host_id='mmsg'
 host_addr='10.164.74.222'>
 <txt>Listener completed notification to CRS on start
 </txt>
</msg>
<msg time='2010-04-20T09:56:44.018+08:00' org_id='oracle' comp_id='tnslsnr'
 type='UNKNOWN' level='16' host_id='mmsg'
 host_addr='10.164.74.222'>
 <txt>
TIMESTAMP * CONNECT DATA [* PROTOCOL INFO] * EVENT [* SID] * RETURN CODE
 </txt>
</msg>
```

原因

机器IP更改，导致监听读取lintener.ora文件中HOST失败

解决

修改lintener.ora中host为当前机器IP地址；


修改/etc/host文件，将该文件中的IP地址更换成当前的IP地址（即变化后的IP地址）；

如上修改后重新启动监听

# 停止监听报TNS-01190

表象

```
oracle@mmsg1:~> lsnrctl stop

LSNRCTL for Linux: Version 11.1.0.7.0 - Production on 11-8月 -2010 08:49:50

Copyright (c) 1991, 2008, Oracle.  All rights reserved.

正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.49.167)(PORT=1521)))
TNS-01190: 用户无权执行所请求的监听程序命令
```

原因

Oracle用户未设置监听密码等信息，导致其他用户停止了oracle的监听，并重新启动了监听。

```
oracle@mmsg1:~/product/11g/network/admin> ps -ef | grep oracle
oracle   26896 25801  0 Aug10 pts/2    00:00:00 su oracle
oracle   26897 26896  0 Aug10 pts/2    00:00:00 bash
oracle   26915 26897  0 Aug10 pts/2    00:00:00 bash
oracle   26930 26915  0 Aug10 pts/2    00:00:00 -sh
syc      27829     1  0 Aug10 ?        00:00:00 /opt/oracle/product/11g/bin/tnslsnr LISTENER -inherit
root      9623  9622  0 08:48 ?        00:00:00 login -- oracle              
oracle    9624  9623  0 08:48 pts/1    00:00:00 -bash
oracle    9762  9624  0 08:55 pts/1    00:00:00 ps -ef
oracle    9763  9624  0 08:55 pts/1    00:00:00 grep oracle
```

解决方法

root用户kill掉相关进程id，oracle用户重新启动linstner，并设置监听密码，防止非oracle用户远程启动、停止监听。

# TNS-01201案例Listener cannot find executable

表象

启动监听时候，报TNS-01201错

```
oracle@mmsc101:~/product/11g/network/admin> lsnrctl start

LSNRCTL for Linux: Version 11.1.0.6.0 - Production on 08-OCT-2011 15:38:38

Copyright (c) 1991, 2007, Oracle.  All rights reserved.

Starting /opt/oracle/product/11g/bin/tnslsnr: please wait...

TNSLSNR for Linux: Version 11.1.0.6.0 - Production
System parameter file is /opt/oracle/product/11g/network/admin/listener.ora
Log messages written to /opt/oracle/diag/tnslsnr/mmsc101/listener/alert/log.xml
Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=10.137.73.5)(PORT=1521)))
TNS-01201: Listener cannot find executable /home/oracle/product/11g/bin/oracle for SID sdp

Listener failed to start. See the error message(s) above...
```

解决过程

1、查询错误码信息

```
oracle@mmsc101:~/product/11g/network/admin> oerr TNS 01201
01201, 00000, "Listener cannot find executable %s for SID %s"
// *Cause:  The executable for the Oracle dedicated server process cannot be
// found.
// *Action: Check the appropriate SID_DESC in LISTENER.ORA to make sure that
// the ORACLE_HOME component is pointing to a valid location. If this component
// is not set, then check the value of the ORACLE_HOME environment variable.
// *Comment: This error is reported only on UNIX platforms.
oracle@mmsc101:~/product/11g/network/admin> 
```

2、确定一下当前ORACLE_HOME目录

```
oracle@mmsc101:~> echo  $ORACLE_HOME
/opt/oracle/product/11g
```

3、 检查下监听配置文件

```
oracle@mmsc101:~/product/11g/bin> more  /opt/oracle/product/11g/network/admin/listener.ora
# listener.ora Network Configuration File: /home/oracle/product/11g/network/admin/listener.ora
# Generated by Oracle configuration tools.

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.73.5)(PORT = 1521))
    )
  )
SID_LIST_LISTENER =
    (SID_DESC =
      (GLOBAL_DBNAME = sdp)
      (ORACLE_HOME = /home/oracle/product/11g)
      (SID_NAME = sdp)
    )
  )

                      
SID_LIST_LISTENER_RM =
(SID_LIST =
        (SID_DESC =
                (ORACLE_HOME = /opt/oracle/product/11g)
                (SID_NAME= sdp)
                (GLOBAL_DBNAME=sdp)
        )
)

LISTENER_RM =
(
        DESCRIPTION =
          (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.73.5)(PORT = 1523))
)
```

发现监听文件中SID_LIST_LISTENER配置ORACLE_HOME为/home/oracle/product/11g，与实际不符，进行修改。

4、修改监听配置文件

```
oracle@mmsc101:~/product/11g/bin> 


oracle@mmsc101:~/product/11g/network/admin> vi listener.ora 

# listener.ora Network Configuration File: /home/oracle/product/11g/network/admin/listener.ora
# Generated by Oracle configuration tools.

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.73.5)(PORT = 1521))
    )
  )
SID_LIST_LISTENER =
    (SID_DESC =
      (GLOBAL_DBNAME = sdp)
      (ORACLE_HOME = /opt/oracle/product/11g)
      (SID_NAME = sdp)
    )
  )



SID_LIST_LISTENER_RM =
(SID_LIST =
        (SID_DESC =
                (ORACLE_HOME = /opt/oracle/product/11g)
                (SID_NAME= sdp)
                (GLOBAL_DBNAME=sdp)
        )
)

LISTENER_RM =
(
        DESCRIPTION =
          (ADDRESS = (PROTOCOL = TCP)(HOST = 10.137.73.5)(PORT = 1523))
)
```

5、报错后启动监听                                                                              

```
oracle@mmsc101:~/product/11g/network/admin> lsnrctl start

LSNRCTL for Linux: Version 11.1.0.6.0 - Production on 08-OCT-2011 15:42:42

Copyright (c) 1991, 2007, Oracle.  All rights reserved.

Starting /opt/oracle/product/11g/bin/tnslsnr: please wait...

TNSLSNR for Linux: Version 11.1.0.6.0 - Production
System parameter file is /opt/oracle/product/11g/network/admin/listener.ora
Log messages written to /opt/oracle/diag/tnslsnr/mmsc101/listener/alert/log.xml
Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=10.137.73.5)(PORT=1521)))

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.137.73.5)(PORT=1521)))
STATUS of the LISTENER
------------------------
Alias                     LISTENER
Version                   TNSLSNR for Linux: Version 11.1.0.6.0 - Production
Start Date                08-OCT-2011 15:42:42
Uptime                    0 days 0 hr. 0 min. 0 sec
Trace Level               off
Security                  ON: Local OS Authentication
SNMP                      OFF
Listener Parameter File   /opt/oracle/product/11g/network/admin/listener.ora
Listener Log File         /opt/oracle/diag/tnslsnr/mmsc101/listener/alert/log.xml
Listening Endpoints Summary...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=10.137.73.5)(PORT=1521)))
Services Summary...
Service "sdp" has 1 instance(s).
  Instance "sdp", status UNKNOWN, has 1 handler(s) for this service...
The command completed successfully
oracle@mmsc101:~/product/11g/network/admin>
```

