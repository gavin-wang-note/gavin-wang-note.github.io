---
layout:     post
title:      "使用 tmpwatch/tmpreaper 删除旧文件"
subtitle:   "tmpwatch/tmpreaper to delete old files"
date:       2023-04-17
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

inux系统中我们常常会把一些临时文件或者没有什么用处的文件放置在/tmp下，还有一些进程也会将临时数据放到/var或者/tmp。这些文件如长时间不去处理日积月累可能造成磁盘空间爆满，也浪费磁盘资源。tmpwatch是一款非常实用的空间清理工具，可以帮助我们自动清理/tmp和/var空间的部分目录。

tmpwatch 能够循环地删除指定目录下指定时间内没有被访问的文件，这一命令常常用于清理临时文件目录，比如 /tmp 或者 /var/tmp 这类目录。它只清除指定目录下的空目录、普通文件和符号链接文件，也不会影响其他目录，而且会避开那些属于root用户的系统相关关键文件的。

默认设置下，tmpwatch 命令依据文件的 atime （access time）而非mtime （modify time）来删除文件。如果你想改变它的删除依据，可以在使用这个命令时加上你想修改的参数。



* 注意：

千万不要在根目录底下运行 tmpwatch 或者 tmpreaper 命令，因为系统可没有任何机制阻止你在根目录下运行此命令。


# tmpwatch使用说明#

tmpwatch参数说明

```
 -u, --atime 基于访问时间来删除文件，默认的。
 -m, --mtime 基于修改时间来删除文件。
 -c, --ctime 基于创建时间来删除文件，对于目录，基于mtime。
 -M, --dirmtime 删除目录基于目录的修改时间而不是访问时间。
 -a, --all 删除所有的文件类型，不只是普通文件，符号链接和目录。
 -d, --nodirs 不尝试删除目录，即使是空目录。
 -d, --nosymlinks 不尝试删除符号链接。
 -f, --force 强制删除。
 -q, --quiet 只报告错误信息。
 -s, --fuser 如果文件已经是打开状态在删除前，尝试使用“定影”命令。默认不启用。
 -t, --test 仅作测试，并不真的删除文件或目录。
 -U, --exclude-user=user 不删除属于谁的文件。
 -v, --verbose 打印详细信息。
 -x, --exclude=path 排除路径，如果路径是一个目录，它包含的所有文件被排除了。如果路径不存在，它必须是一个绝对路径不包含符号链接。
 -X, --exclude-pattern=pattern 排除某规则下的路径。
```


# tmpwatch 命令的关键选项和参数

* atime (File Last Access Time)：文件最后一次被访问的时间；
* mtime (File Last Modify Time)：文件内容最后一次被修改的时间；
* ctime (File Last Change Time)：文件元数据最后一次被修改的时间，即文件相关属性被修改的时间，多数情况下 mtime 和 ctime 值相同，但是诸如文件所有者、权限、所属组这类不涉及内容的属性被修改时则只会影响 ctime；
* dirmtime (Directory Last modification time)：目录最后一次被修改的时间。

这些时间参数用来设置删除文件的条件阈值：

* d：单位为天；
* h：单位为小时；
* m：单位为分钟；
* s：单位为秒。

# 用 tmpwatch 命令删除一段时间内没有被访问的文件

如前所述，tmpwatch 命令的默认选项是 atime，而默认的单位参数则是h，所以如果你确实要按以小时为单位计算的访问时间来删除文件，那么你不用加任何特殊的选项或则参数后缀，可以直接是用这个命令。如下例所示，即为删除 /tmp 目录下过去5小时内没有被访问的文件：

``` tmpwatch 5 /tmp ```
 


下面这个示例是删除 /home/btadmin/Downloads 目录下过去十小时内没有修改过内容的文件，注意，如果要按 mtime 来删除文件，需要在命令中加上-m 的选项：

``` tmpwatch -m 10 /home/btadmin/Downloads ```



## 删除以其他单位计算的某段时间内没有被访问的文件


如果你要以天为单位，则需要加上 d 的后缀，如下为删除30天内没有被访问的文件：

``` tmpwatch 30d /home/btadmin/Downloads ```
 


## 删除一段时间内未被使用的所有文件


如果你想不仅仅删除普通文件、符号链接文件、空目录文件，而是想删除指定目录下某段时间内没有被访问的所有文件，则需要加上选项 -a，如下为删除指定目录下12小时未被修改内容的所有文件：

``` tmpwatch -am 12 /tmp ```
 

## 将某些目录排除在删除操作外


如下命令可以让那些十小时内没有被修改过内容的目录不被删除：

``` tmpwatch -am 10 --nodirs /home/btadmin/Downloads ```
 


## 将特定路径排除在删除操作外


下面的命令删除 /home/btadmin/Downloads 目录下所有十小时内没有修改内容的文件，但是 /home/btadmin/Downloads/Builds 路径下却不受影响，即该路径下十小时内没修改的文件也不会被删除：

```tmpwatch -am 10 --exclude=/home/btadmin/Downloads/Builds /home/btadmin/Downloads ```

## 将特定格式的文件排除在删除操作外

下面所示的命令为删除指定文件下的所有10小时内未被改动的文件，除了pdf 格式的文件：

``` tmpwatch -am 10 --exclude-pattern='*.pdf' /home/btadmin/Downloads ```
 


## 预演 tmpwatch 的效果


下面这条命令即是对 tmpwatch 的功能效果进行预演：

``` tmpwatch -t 5h /home/btadmin/Downloads ```
 


## 用 tmpwatch 设置一个定时任务周期性地执行删除操作

要完成这个任务，会在 /etc/cron.daily/tmpreaper 目录下留下一个 cronjob 文件，这个文件是按照 /etc/timereaper.conf 的设定工作的，你可以按自己的需求设置它。

如下所示的设置，能在每天上午10点时删除指定目录下，十五天没被访问的文件：

``` crontab -e0 10 * * * /usr/sbin/tmpwatch 15d /home/btadmin/Downloads ```
 

### 默认定时任务配置
安装后会在/etc/cron.daily/目录下生成一个tmpwatch文件，crontab每天会调用执行一次。内容如下：

```
[roota@redhat6 ~]# cat /etc/cron.daily/tmpwatch 
#! /bin/sh
flags=-umc
/usr/sbin/tmpwatch "$flags" -x /tmp/.X11-unix -x /tmp/.XIM-unix \
        -x /tmp/.font-unix -x /tmp/.ICE-unix -x /tmp/.Test-unix \
        -X '/tmp/hsperfdata_*' -X '/tmp/.hdb*lock' -X '/tmp/.sapstartsrv*.log' \
        -X '/tmp/pymp-*' 10d /tmp
/usr/sbin/tmpwatch "$flags" 30d /var/tmp
for d in /var/{cache/man,catman}/{cat?,X11R6/cat?,local/cat?}; do
    if [ -d "$d" ]; then
        /usr/sbin/tmpwatch "$flags" -f 30d "$d"
    fi
done
```

从配置可以看出tmpwatch排查了/tmp 和 /var 下的一些目录，/tmp保留10d内访问修改过的文件，/var保留30d，其他都删除。


# 总结

tmpwatch是空间清理的利器，但在测试和使用时也需要注意安全。重要数据切记不要放到/tmp下，尽管其他非特权用户没有权限删除但tmpwatch可以。
