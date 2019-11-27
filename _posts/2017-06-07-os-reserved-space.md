---
layout:     post
title:      "操作系统空间预留"
subtitle:   "OS partition reserved space"
date:       2017-06-07
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

在执行df命令查看空间时，发现已使用空间与剩余空间之和，小于总空间，如下图所示：

<img class="shadow" src="/img/in-post/df_space.png" width="600">

图上显示，可用空间81G，已使用8G，加起来是89G，但总空间是94G，少了5G?

这是什么原因呢？


# mkfs 空间预留

原来mkfs的时候，默认携带 -m 参数，即默认预留5%的空间, 94G * 0.05 = 4.7G，大约是5G，与上面的计算吻合（在磁盘换算过程中由于使用的单位不同，这个有约0.02左右的误差是可能的）。 

<img class="shadow" src="/img/in-post/dumpe2fs.png" width="600">

# 意图

默认预留5%的磁盘空间，留给root用户维护系统或者记录系统关键日志的时候使用(比如磁盘使用空间已经100%的情况下的处理)，这也就是导致普通用户无法使用部分磁盘空间的原因了。


# 如果关闭预留空间

以另外一套环境为例：

通过tune2fs 可以关闭文件系统空间的预留

关闭前：

```
root@host244:/# df -PH
Filesystem                                Size  Used Avail Use% Mounted on
/dev/sdc3                                  99G  2.2G   92G   3% /
udev                                       34G   13k   34G   1% /dev
tmpfs                                     6.8G  5.5M  6.8G   1% /run
none                                      5.3M     0  5.3M   0% /run/lock
none                                       34G   37k   34G   1% /run/shm
```

关闭后：

```
root@host244:/# tune2fs -h 
tune2fs 1.42 (29-Nov-2011)
tune2fs: invalid option -- 'h'
Usage: tune2fs [-c max_mounts_count] [-e errors_behavior] [-g group]
	[-i interval[d|m|w]] [-j] [-J journal_options] [-l]
	[-m reserved_blocks_percent] [-o [^]mount_options[,...]] [-p mmp_update_interval]
	[-r reserved_blocks_count] [-u user] [-C mount_count] [-L volume_label]
	[-M last_mounted_dir] [-O [^]feature[,...]]
	[-E extended-option[,...]] [-T last_check_time] [-U UUID]
	[ -I new_inode_size ] device
root@host244:/# tune2fs -m 0 /dev/sdc3 
tune2fs 1.42 (29-Nov-2011)
Setting reserved blocks percentage to 0% (0 blocks)
root@host244:/# df -PH
Filesystem                                Size  Used Avail Use% Mounted on
/dev/sdc3                                  99G  2.2G   97G   3% /
udev                                       34G   13k   34G   1% /dev
tmpfs                                     6.8G  5.5M  6.8G   1% /run
none                                      5.3M     0  5.3M   0% /run/lock
none                                       34G   37k   34G   1% /run/shm
root@host244:/# 
```

