---
layout:     post
title:      "systemtap部署与实战"
subtitle:   "Install systemtap and how to use it"
date:       2022-10-26
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - shell
---

# 概述

本文介绍如何借助systemtap给磁盘注入时延，验证产品慢盘检测功能。

# 安装与部署

## 安装Linux debug symbols

挂载安装Virtual Scaler ISO到机器上，然后从后台运行以下命令：

```
mkdir /mnt/cdrom
mount /dev/cdrom /mnt/cdrom
cd /mnt/cdrom/pools/extra
dpkg -i linux-image-4.14.148-dbg_4.14.148-202009221212.git33a12c4_amd64.deb
```

* 此处.deb 请替换成ISO中相应版本的文件，类似linux-image-4.14.148-dbg_***.deb。

## 其他package的安装

直接运行安装包下的install_systemtap.sh:

```
chmod a+x install_systemtap.sh;
./ install_systemtap.sh
```

或

```
dpkg -i zlib1g-dev_1%3a1.2.8.dfsg-2ubuntu4.3_amd64.deb;
dpkg -i liblzma-dev_5.1.1alpha+20120614-2ubuntu2_amd64.deb;
dpkg -i libelf1_0.170-0.4ubuntu0.1_amd64.deb;
dpkg -i libelf-dev_0.170-0.4ubuntu0.1_amd64.deb;
dpkg -i libdw1_0.170-0.4ubuntu0.1_amd64.deb;
dpkg -i libdw-dev_0.170-0.4ubuntu0.1_amd64.deb;
dpkg -i libasm1_0.170-0.4ubuntu0.1_amd64.deb;
dpkg -i libasm-dev_0.170-0.4ubuntu0.1_amd64.deb;
dpkg -i libasprintf-dev_0.19.7-2ubuntu3.1_amd64.deb;
dpkg -i elfutils_0.170-0.4ubuntu0.1_amd64.deb;
```

Centos:

```
yum install elfutils-devel
https://sourceware.org/systemtap/wiki/SystemTapOnCentOS
```

解压systemtap并编译安装

```
tar zxvf systemtap-4.3.tar.gz
cd systemtap-4.3/
./configure --prefix=/usr/;
make && make install
```

测试systemtap是否安装成功

如果安装成功，运行以下命令稍候会打印hello world: 

```
stap -e 'probe kernel.function("sys_open") {log("hello world") exit()}'

```

# 输出当前读写磁盘的进程

创建disk.stp文件，输入以下内容：

```
#!/usr/bin/env stap 
#
# Copyright (C) 2007 Oracle Corp.
#
# Get the status of reading/writing disk every 5 seconds,
# output top ten entries 
#
# This is free software,GNU General Public License (GPL);
# either version 2, or (at your option) any later version.
#
# Usage:
#  ./disktop.stp
#

global io_stat,device
global read_bytes,write_bytes

probe vfs.read.return {
  if (returnval()>0) {
    if (devname!="N/A") {/*skip read from cache*/
      io_stat[pid(),execname(),uid(),ppid(),"R"] += returnval()
      device[pid(),execname(),uid(),ppid(),"R"] = devname
      read_bytes += returnval()
    }
  }
}

probe vfs.write.return {
  if (returnval()>0) {
    if (devname!="N/A") { /*skip update cache*/
      io_stat[pid(),execname(),uid(),ppid(),"W"] += returnval()
      device[pid(),execname(),uid(),ppid(),"W"] = devname
      write_bytes += returnval()
    }
  }
}

probe timer.ms(5000) {
  /* skip non-read/write disk */
  if (read_bytes+write_bytes) {

    printf("\n%-25s, %-8s%4dKb/sec, %-7s%6dKb, %-7s%6dKb\n\n",
           ctime(gettimeofday_s()),
           "Average:", ((read_bytes+write_bytes)/1024)/5,
           "Read:",read_bytes/1024,
           "Write:",write_bytes/1024)

    /* print header */
    printf("%8s %8s %8s %25s %8s %4s %12s\n",
           "UID","PID","PPID","CMD","DEVICE","T","BYTES")
  }
  /* print top ten I/O */
  foreach ([process,cmd,userid,parent,action] in io_stat- limit 10)
    printf("%8d %8d %8d %25s %8s %4s %12d\n",
           userid,process,parent,cmd,
           device[process,cmd,userid,parent,action],
           action,io_stat[process,cmd,userid,parent,action])

  /* clear data */
  delete io_stat
  delete device
  read_bytes = 0
  write_bytes = 0  
}

probe end{
  delete io_stat
  delete device
  delete read_bytes
  delete write_bytes
}

```

给该文件运行的权限并执行：

```
chmod a+x disk.stp
./disk.stp

```

输出如下结果： 

<img class="shadow" src="/img/in-post/disk_stp.png" width="1200">


# 模拟磁盘延迟

推荐将RAID设置成write back模式。

使用oceanfile以512k的bs来写数据: ```oceanfile -d . -p 40 -a 8,20,100,100 -s 10M -b 512K  -i 1```

创建以下systemtap文件inject_ka.stp, 并输入以下内容：
 

```
global cnt = 0 ;
probe module("sd_mod").function("sd_init_command") !,
      kernel.function("sd_init_command")
{
    device = kernel_string(@choose_defined($cmd, $SCpnt)->request->rq_disk->disk_name)
    if(device == @1)
    {
        mdelay($2);
        if(cnt % 100 == 0)
        { 
             printf("%s inject delay %4d times %7d\n", device,$2, cnt)
        }
        cnt++ ;
    }
    #printf("device %s sd_init_command\n", device);
}

 


probe begin{
  println("inject_scsi_delay module begin");
}

```


以如下格式运行：

```
#stap -g -DMAXSKIPPED=99999999 inject_ka.stp sdb 10
```

或

```
#stap -p4 -DMAXSKIPPED=99999999 -m ik -g inject_ka.stp sdb 10
#staprun ik.ko
```

运行之后，sdc盘的svctm就会在当前数值基本上增加10.

 
<img class="shadow" src="/img/in-post/sdc_svctm.png" width="1200">

参考：

https://sourceware.org/systemtap/examples/io/iostat-scsi.stp
https://sourceware.org/systemtap/examples/io/iostat-scsi.txt





