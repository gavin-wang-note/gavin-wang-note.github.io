---
layout:     post
title:      "Linux stat家族之pidstat"
subtitle:   "Linux pidstat"
date:       2023-01-20
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# pidstat 概述

pidstat是sysstat工具的一个命令，用于监控全部或指定进程的cpu、内存、线程、设备IO等系统资源的占用情况。pidstat首次运行时显示自系统启动开始的各项统计信息，之后运行pidstat将显示自上次运行该命令以后的统计信息。用户可以通过指定统计的次数和时间来获得所需的统计信息。

# pidstat 安装

pidstat 是sysstat软件套件的一部分，sysstat包含很多监控linux系统状态的工具，它能够从大多数linux发行版的软件源中获得。

在Debian/Ubuntu系统中可以使用下面的命令来安装:

```apt-get install sysstat ```

CentOS/Fedora/RHEL版本的linux中则使用下面的命令：

```yum install sysstat ```


# 实践


## 显示所有正在运行的进程（或特定进程）的统计信息

使用 -p ALL 选项查看所有正在运行的进程的性能统计信息，如下所示:

```
root@node166:~# pidstat -p ALL | wc -l
1275
root@node166:~# pidstat -p ALL | head
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:39:51 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:39:51 PM     0         1    0.02    0.05    0.00    0.08    18  systemd
04:39:51 PM     0         2    0.00    0.00    0.00    0.00    29  kthreadd
04:39:51 PM     0         4    0.00    0.00    0.00    0.00     0  kworker/0:0H
04:39:51 PM     0         7    0.00    0.00    0.00    0.00     0  mm_percpu_wq
04:39:51 PM     0         8    0.00    0.03    0.00    0.03     0  ksoftirqd/0
04:39:51 PM     0         9    0.00    0.87    0.00    0.87    30  rcu_sched
04:39:51 PM     0        10    0.00    0.00    0.00    0.00     0  rcu_bh
root@node166:~#
```

默认情况下，这将显示 CPU 使用率。但是，可以将其更改为任何其他性能统计信息，如后面的示例所示。


使用 -p PID 监视特定进程的性能统计信息，如下所示:

```
root@node166:~# pidstat -p  5736
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:41:06 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:41:06 PM     0      5736    2.34    5.06    0.00    7.40    28  ceph-osd
root@node166:~# 
```

## 使用 -C 根据进程名称显示性能统计信息

以下示例将显示匹配特定关键字（例如：ceph-osd）的所有进程的性能统计信息:

```
root@node166:~# pidstat -C "ceph-osd"
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:41:57 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:41:57 PM     0      5736    2.34    5.07    0.00    7.41    28  ceph-osd
04:41:57 PM     0      5741    1.95    3.42    0.00    5.37    15  ceph-osd
04:41:57 PM     0      5745    2.32    4.15    0.00    6.47    10  ceph-osd
04:41:57 PM     0      5749    2.10    3.88    0.00    5.98     0  ceph-osd
04:41:57 PM     0      5751    2.69    5.81    0.00    8.50    15  ceph-osd
04:41:57 PM     0      5753    2.13    4.20    0.00    6.33     8  ceph-osd
root@node166:~# 
```

注意：
   在上面的例子中，选项 -C 代表“命令名称”。即它将使用给定的关键字搜索进程的命令名称。


## 以一定的间隔重复输出

默认情况下，不会重复输出。例如，选项 -u 是显示任务的 CPU 使用统计信息，这是 pidstat 命令给出的默认统计信息。Thsi 将只显示输出一次。


```
root@node166:~# pidstat -p 5753
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:42:54 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:42:54 PM     0      5753    2.15    4.24    0.00    6.39     8  ceph-osd
root@node166:~# 
```

要重复输出，请指定以秒为单位的间隔作为最后一个参数。例如，以下示例将每 1 秒重复输出一次（直到按 Ctrl-C）:

```
root@node166:~# pidstat -p 5753 1
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:43:28 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:43:29 PM     0      5753    8.00   19.00    0.00   27.00     8  ceph-osd
04:43:30 PM     0      5753    7.00   22.00    0.00   29.00     8  ceph-osd
04:43:31 PM     0      5753    8.00   21.00    0.00   29.00     8  ceph-osd
04:43:32 PM     0      5753    8.00   26.00    0.00   34.00     8  ceph-osd
04:43:33 PM     0      5753   10.00   28.00    0.00   38.00     8  ceph-osd
04:43:34 PM     0      5753   10.00   22.00    0.00   32.00     8  ceph-osd
^C
Average:        0      5753    8.50   23.00    0.00   31.50     -  ceph-osd
root@node166:~# 
```

以下将每 15 秒重复输出一次（直到按 Ctrl-C）

```
t@node166:~# pidstat -p 5753 15
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:44:10 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:44:25 PM     0      5753    8.00   21.07    0.00   29.07     8  ceph-osd
04:44:40 PM     0      5753    9.53   23.53    0.00   33.07     8  ceph-osd
04:44:55 PM     0      5753    7.87   21.13    0.00   29.00     8  ceph-osd
04:45:10 PM     0      5753    9.13   23.53    0.00   32.67     8  ceph-osd
^C
Average:        0      5753    8.63   22.32    0.00   30.95     -  ceph-osd
root@node166:~# 
```



## 使用 -d 显示特定进程的 I/O 统计信息

使用选项 -d 报告进程的 I/O 统计信息。它的输出显示了不同的属性，如 PID、磁盘读写速度（以 kB/s 为单位），如下所示。

以下示例每 1 秒显示 PID 23493 的磁盘使用情况。

```
root@node166:~# pidstat -p 5736 -d 1
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:44:51 PM   UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command
04:44:52 PM     0      5736  79916.00      0.00      0.00       0  ceph-osd
04:44:53 PM     0      5736  75820.00      0.00      0.00       0  ceph-osd
04:44:54 PM     0      5736  85052.00      4.00      0.00       0  ceph-osd
04:44:55 PM     0      5736  87100.00      0.00      0.00       0  ceph-osd
04:44:56 PM     0      5736  92204.00      0.00      0.00       0  ceph-osd
04:44:57 PM     0      5736  86064.00      0.00      0.00       0  ceph-osd
^C
Average:        0      5736  84359.33      0.67      0.00       0  ceph-osd
root@node166:~# 
```


## 使用 -r 显示特定进程的分页活动

使用选项 -r 显示给定任务 (PID) 的页面错误和内存利用率。

```
root@node166:~# pidstat -p 5753 -r 1
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)


04:45:52 PM   UID       PID  minflt/s  majflt/s     VSZ     RSS   %MEM  Command
04:45:53 PM     0      5753  36733.00      0.00 7048224 4374012   3.35  ceph-osd
04:45:54 PM     0      5753  39449.00      0.00 7048224 4374012   3.35  ceph-osd
04:45:55 PM     0      5753  48854.00      0.00 7048224 4374044   3.35  ceph-osd
04:45:56 PM     0      5753  37720.00      0.00 7048224 4374060   3.35  ceph-osd
04:45:57 PM     0      5753  46121.00      0.00 7048224 4374060   3.35  ceph-osd
04:45:58 PM     0      5753  46210.00      0.00 7048224 4392352   3.36  ceph-osd
^C
Average:        0      5753  42514.50      0.00 7048224 4377090   3.35  ceph-osd
root@node166:~#
```


## 使用选项 -l 显示命令名称及其参数

默认情况下，pidstat 仅显示命令名称。即没有命令的完整路径及其参数。例如，在命令列中，你只会看到 "python" （它只是程序的名称）。

```
root@node166:~# pidstat -C python
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:46:37 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:46:37 PM     0     11307    0.05    0.03    0.00    0.07    29  python
root@node166:~# 
```

但是，当使用选项 -l 时，它将显示命令的完整路径及其所有参数，如下所示:

```
root@node166:~# pidstat -C python -l
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:47:17 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:47:17 PM     0     11307    0.05    0.03    0.00    0.07     1  python /usr/local/bin/ezs3-app start 
root@node166:~# 
```

为了定期获取任务的统计信息，只需传递你希望查看统计信息的秒数:

```
root@node166:~# pidstat -C ceph-osd -l 1
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:48:20 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:48:21 PM     0      5736    5.77   12.50    0.00   18.27    28  /usr/bin/ceph-osd -f --cluster ceph --id 16 --setuser root --setgroup root 
04:48:21 PM     0      5741    8.65   17.31    0.00   25.96    15  /usr/bin/ceph-osd -f --cluster ceph --id 14 --setuser root --setgroup root 
04:48:21 PM     0      5745    8.65   21.15    0.00   29.81    10  /usr/bin/ceph-osd -f --cluster ceph --id 12 --setuser root --setgroup root 
04:48:21 PM     0      5749    8.65   21.15    0.00   29.81     0  /usr/bin/ceph-osd -f --cluster ceph --id 13 --setuser root --setgroup root 
04:48:21 PM     0      5751    6.73   16.35    0.00   23.08    15  /usr/bin/ceph-osd -f --cluster ceph --id 15 --setuser root --setgroup root 
04:48:21 PM     0      5753   11.54   31.73    0.00   43.27     8  /usr/bin/ceph-osd -f --cluster ceph --id 17 --setuser root --setgroup root 

04:48:21 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:48:22 PM     0      5736    4.00    8.00    0.00   12.00    28  /usr/bin/ceph-osd -f --cluster ceph --id 16 --setuser root --setgroup root 
04:48:22 PM     0      5741    7.00   21.00    0.00   28.00    15  /usr/bin/ceph-osd -f --cluster ceph --id 14 --setuser root --setgroup root 
04:48:22 PM     0      5745    7.00   21.00    0.00   28.00    10  /usr/bin/ceph-osd -f --cluster ceph --id 12 --setuser root --setgroup root 
04:48:22 PM     0      5749   10.00   25.00    0.00   35.00     0  /usr/bin/ceph-osd -f --cluster ceph --id 13 --setuser root --setgroup root 
04:48:22 PM     0      5751    8.00   18.00    0.00   26.00    15  /usr/bin/ceph-osd -f --cluster ceph --id 15 --setuser root --setgroup root 
04:48:22 PM     0      5753    8.00   27.00    0.00   35.00     8  /usr/bin/ceph-osd -f --cluster ceph --id 17 --setuser root --setgroup root 

04:48:22 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:48:23 PM     0      5736    5.00   14.00    0.00   19.00    28  /usr/bin/ceph-osd -f --cluster ceph --id 16 --setuser root --setgroup root 
04:48:23 PM     0      5741    8.00   21.00    0.00   29.00    15  /usr/bin/ceph-osd -f --cluster ceph --id 14 --setuser root --setgroup root 
04:48:23 PM     0      5745    7.00   22.00    0.00   29.00    10  /usr/bin/ceph-osd -f --cluster ceph --id 12 --setuser root --setgroup root 
04:48:23 PM     0      5749    9.00   25.00    0.00   34.00     0  /usr/bin/ceph-osd -f --cluster ceph --id 13 --setuser root --setgroup root 
04:48:23 PM     0      5751    9.00   18.00    0.00   27.00    15  /usr/bin/ceph-osd -f --cluster ceph --id 15 --setuser root --setgroup root 
04:48:23 PM     0      5753    9.00   30.00    0.00   39.00     8  /usr/bin/ceph-osd -f --cluster ceph --id 17 --setuser root --setgroup root 
^C

Average:      UID       PID    %usr %system  %guest    %CPU   CPU  Command
Average:        0      5736    4.93   11.51    0.00   16.45     -  /usr/bin/ceph-osd -f --cluster ceph --id 16 --setuser root --setgroup root 
Average:        0      5741    7.89   19.74    0.00   27.63     -  /usr/bin/ceph-osd -f --cluster ceph --id 14 --setuser root --setgroup root 
Average:        0      5745    7.57   21.38    0.00   28.95     -  /usr/bin/ceph-osd -f --cluster ceph --id 12 --setuser root --setgroup root 
Average:        0      5749    9.21   23.68    0.00   32.89     -  /usr/bin/ceph-osd -f --cluster ceph --id 13 --setuser root --setgroup root 
Average:        0      5751    7.89   17.43    0.00   25.33     -  /usr/bin/ceph-osd -f --cluster ceph --id 15 --setuser root --setgroup root 
Average:        0      5753    9.54   29.61    0.00   39.14     -  /usr/bin/ceph-osd -f --cluster ceph --id 17 --setuser root --setgroup root 
root@node166:~# 
```
## 定期显示输出 X 次

也可以在给定的时间间隔内获取特定次数的报告，以获取如下所示的过程列表。

添加次数作为最后一个参数（在以秒为单位的间隔之后）。

例如，下面将显示输出 5 次（以 2 秒的固定间隔）。在报告结束时，它还将显示“平均值”值。

```
root@node166:~# pidstat 2 5
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:50:06 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:50:08 PM     0         9    0.00    1.46    0.00    1.46    23  rcu_sched
04:50:08 PM     0       258    0.00    0.49    0.00    0.49    23  kcompactd0
04:50:08 PM     0       259    0.00    0.49    0.00    0.49    15  kcompactd1
04:50:08 PM     0       292    0.00    6.34    0.00    6.34    22  kswapd0
04:50:08 PM     0       305    0.00    5.37    0.00    5.37    37  kswapd1
04:50:08 PM     0       720    0.00    0.49    0.00    0.49     0  jbd2/sdg2-8
04:50:08 PM   114      2695    0.49    0.00    0.00    0.49    38  memcached
04:50:08 PM     0      2730    6.83    3.41    0.00   10.24     2  ceph-mon
04:50:08 PM     0      2922    0.49    0.49    0.00    0.98    16  ezrpcd
04:50:08 PM     0      3103    0.49    0.00    0.00    0.49     8  bt-monitord
04:50:08 PM     0      5736    4.39   13.66    0.00   18.05    28  ceph-osd
04:50:08 PM     0      5741    6.83   20.00    0.00   26.83    15  ceph-osd
04:50:08 PM     0      5745    8.78   22.44    0.00   31.22    10  ceph-osd
04:50:08 PM     0      5749    8.78   26.34    0.00   35.12     0  ceph-osd
04:50:08 PM     0      5751    9.27   18.05    0.00   27.32    15  ceph-osd
04:50:08 PM     0      5753    9.76   29.76    0.00   39.51     8  ceph-osd
04:50:08 PM     0      6076    8.78    8.78    0.00   17.56     3  node_exporter
04:50:08 PM     0      7890    2.44    0.00    0.00    2.44    19  prometheus
04:50:08 PM     0     30461    0.49    0.00    0.00    0.49    30  bt-ipmi-agent.p
04:50:08 PM     0     33930    3.41    0.98    0.00    4.39    38  bt-exporter
04:50:08 PM     0     35428   13.17    0.98    0.00   14.15    13  bt-ceph-exporte
04:50:08 PM    33     66962    5.37    1.46    0.00    6.83    12  apache2
04:50:08 PM     0    115886    0.49    0.00    0.00    0.49     6  sshd
04:50:08 PM     0    121221    0.00    0.49    0.00    0.49    32  ctdbd
04:50:08 PM     0    121679    3.41    0.49    0.00    3.90     6  eziscsi-rbd-cle
04:50:08 PM     0    121790   18.05    3.90    0.00   21.95     1  btnas-agent
04:50:08 PM     0    121955    2.44    0.98    0.00    3.41    36  eziscsid.py
04:50:08 PM     0    122237    0.49    0.49    0.00    0.98    38  ezqosd
04:50:08 PM     0    147875    0.98    1.46    0.00    2.44    35  pidstat
04:50:08 PM     0    597911    0.49    0.00    0.00    0.49    11  ssh
04:50:08 PM     0    654077    0.49    0.98    0.00    1.46    36  ezs3-agent.py
04:50:08 PM     0    654597    0.49    0.00    0.00    0.49    28  bt-haproxy-agen

04:50:08 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:50:10 PM     0         9    0.00    1.00    0.00    1.00    19  rcu_sched
04:50:10 PM     0       292    0.00    7.50    0.00    7.50    23  kswapd0
04:50:10 PM     0       305    0.00    5.00    0.00    5.00    13  kswapd1
04:50:10 PM   109      2145    0.50    0.00    0.00    0.50     6  dbus-daemon
04:50:10 PM   114      2695    0.00    0.50    0.00    0.50    39  memcached
04:50:10 PM     0      2730    2.50    0.50    0.00    3.00     2  ceph-mon
04:50:10 PM     0      2783    0.50    0.00    0.00    0.50    12  ceph-mgr
04:50:10 PM     0      3103    0.50    0.50    0.00    1.00     9  bt-monitord
04:50:10 PM     0      5736    5.50   13.00    0.00   18.50    28  ceph-osd
04:50:10 PM     0      5741    7.50   20.00    0.00   27.50    15  ceph-osd
04:50:10 PM     0      5745    8.00   23.50    0.00   31.50    10  ceph-osd
04:50:10 PM     0      5749    9.00   24.50    0.00   33.50     0  ceph-osd
04:50:10 PM     0    125343    0.50    0.00    0.00    0.50     0  ganesha.nfsd
04:50:10 PM     0    147875    1.00    1.50    0.00    2.50    35  pidstat
04:50:10 PM     0    564344    0.50    0.50    0.00    1.00    33  radosgw

04:50:10 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
04:50:12 PM     0         9    0.00    1.50    0.00    1.50    23  rcu_sched
04:50:16 PM     0    654597    0.50    0.00    0.00    0.50    29  bt-haproxy-agen
==============================   中间省略 ============================

Average:      UID       PID    %usr %system  %guest    %CPU   CPU  Command
Average:        0         9    0.00    1.19    0.00    1.19     -  rcu_sched
Average:        0       258    0.00    0.10    0.00    0.10     -  kcompactd0
Average:        0       259    0.00    0.20    0.00    0.20     -  kcompactd1
Average:        0       292    0.00    6.27    0.00    6.27     -  kswapd0
Average:        0       305    0.00    5.27    0.00    5.27     -  kswapd1
Average:        0       718    0.00    0.10    0.00    0.10     -  kworker/0:1H
Average:        0       720    0.00    0.10    0.00    0.10     -  jbd2/sdg2-8
Average:      109      2145    0.20    0.00    0.00    0.20     -  dbus-daemon
Average:      110      2163    0.10    0.10    0.00    0.20     -  avahi-daemon
Average:      114      2695    0.10    0.10    0.00    0.20     -  memcached
Average:        0      2730    4.68    1.89    0.00    6.57     -  ceph-mon
Average:        0      2783    0.10    0.00    0.00    0.10     -  ceph-mgr
Average:        0      2922    0.20    0.10    0.00    0.30     -  ezrpcd
Average:        0      3103    0.50    0.20    0.00    0.70     -  bt-monitord
Average:        0      5224    0.10    0.00    0.00    0.10     -  sshd
Average:        0      5736    5.77   14.53    0.00   20.30     -  ceph-osd
Average:        0      5741    7.46   19.60    0.00   27.06     -  ceph-osd
Average:        0      5745    8.56   22.39    0.00   30.95     -  ceph-osd
Average:        0      5749    9.15   25.17    0.00   34.33     -  ceph-osd
Average:        0      5751    8.76   18.71    0.00   27.46     -  ceph-osd
Average:        0      5753   10.35   28.96    0.00   39.30     -  ceph-osd
Average:        0      6076   10.45    8.36    0.00   18.81     -  node_exporter
Average:        0      7890    2.99    0.10    0.00    3.08     -  prometheus
Average:        0     11307    0.00    0.10    0.00    0.10     -  python
Average:        0     29221    0.10    0.00    0.00    0.10     -  bt-disk-monitor
Average:        0     29625    0.00    0.10    0.00    0.10     -  bt-recovery-qos
Average:        0     30461    0.30    0.00    0.00    0.30     -  bt-ipmi-agent.p
Average:        0     33930    5.17    3.28    0.00    8.46     -  bt-exporter
Average:        0     35428    2.99    0.20    0.00    3.18     -  bt-ceph-exporte
Average:       33     66962    2.69    0.40    0.00    3.08     -  apache2
Average:        0     67124    0.00    0.10    0.00    0.10     -  kworker/14:3
Average:        0     94898    0.00    0.10    0.00    0.10     -  kworker/u80:2
Average:        0    115823    0.00    0.10    0.00    0.10     -  ssh
Average:        0    115886    0.10    0.00    0.00    0.10     -  sshd
Average:        0    121221    0.00    0.20    0.00    0.20     -  ctdbd
Average:        0    121679    0.70    0.10    0.00    0.80     -  eziscsi-rbd-cle
Average:        0    121682    0.10    0.10    0.00    0.20     -  ezfs-recycle-fl
Average:        0    121790    7.56    1.79    0.00    9.35     -  btnas-agent
Average:        0    121955    2.79    0.80    0.00    3.58     -  eziscsid.py
Average:        0    122237    0.30    0.20    0.00    0.50     -  ezqosd
Average:        0    122253    0.50    0.00    0.00    0.50     -  bt-rbd-qos-agen
Average:        0    122916    0.10    0.00    0.00    0.10     -  sshd
Average:        0    123274    0.00    0.10    0.00    0.10     -  kworker/6:2
Average:        0    125343    0.10    0.10    0.00    0.20     -  ganesha.nfsd
Average:        0    147875    0.80    1.49    0.00    2.29     -  pidstat
Average:        0    471784    0.00    0.10    0.00    0.10     -  kworker/26:0
Average:        0    564344    0.10    0.10    0.00    0.20     -  radosgw
Average:        0    597911    0.10    0.00    0.00    0.10     -  ssh
Average:        0    654077    0.30    0.30    0.00    0.60     -  ezs3-agent.py
Average:        0    654597    0.20    0.00    0.00    0.20     -  bt-haproxy-agen
Average:        0    655087    0.10    0.00    0.00    0.10     -  ssh
root@node166:~#
```

## 使用 -T 显示选定进程及其子进程的统计信息

使用选项 -T 指定 CHILD 或 TASKS。在这种情况下，将报告 TASKS 或任务及其所有子项的统计数据。你也可以指定 ALL。

-T 的可能值：CHILD、TASKS 或 ALL。

```
root@node166:~# pidstat -T CHILD | head 
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:51:31 PM   UID       PID    usr-ms system-ms  guest-ms  Command
04:51:31 PM     0         1    538800    414470         0  systemd
04:51:31 PM     0         2         0       580         0  kthreadd
04:51:31 PM     0         8        10      8020         0  ksoftirqd/0
04:51:31 PM     0         9         0    224970         0  rcu_sched
04:51:31 PM     0        11         0       240         0  migration/0
04:51:31 PM     0        12         0        50         0  watchdog/0
04:51:31 PM     0        15        50         0         0  watchdog/1
root@node166:~# 
```

## 使用 -t 以树格式显示依赖进程的统计信息

使用选项 -t，你可以以树格式显示输出，如下所示。

```
root@node166:~# pidstat -t -C "ceph-osd"
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

04:52:06 PM   UID      TGID       TID    %usr %system  %guest    %CPU   CPU  Command
04:52:06 PM     0      5736         -    2.42    5.29    0.00    7.71    28  ceph-osd
04:52:06 PM     0         -      5736    0.01    0.00    0.00    0.01    28  |__ceph-osd
04:52:06 PM     0         -      5815    0.00    0.00    0.00    0.00     0  |__ceph-osd
04:52:06 PM     0      5741         -    2.07    3.75    0.00    5.82    15  ceph-osd
04:52:06 PM     0         -      5741    0.01    0.00    0.00    0.01    15  |__ceph-osd
04:52:06 PM     0         -      6056    0.00    0.00    0.00    0.00    23  |__ceph-osd
04:52:06 PM     0      5745         -    2.43    4.48    0.00    6.92    10  ceph-osd
04:52:06 PM     0         -      5745    0.01    0.00    0.00    0.01    10  |__ceph-osd
04:52:06 PM     0         -      6006    0.00    0.00    0.00    0.00    36  |__ceph-osd
04:52:06 PM     0      5749         -    2.23    4.26    0.00    6.49     0  ceph-osd
04:52:06 PM     0         -      5749    0.01    0.00    0.00    0.01     0  |__ceph-osd
04:52:06 PM     0         -      6078    0.00    0.00    0.00    0.00    13  |__ceph-osd
04:52:06 PM     0      5751         -    2.80    6.07    0.00    8.87    15  ceph-osd
04:52:06 PM     0         -      5751    0.01    0.00    0.00    0.01    15  |__ceph-osd
04:52:06 PM     0         -      6005    0.00    0.00    0.00    0.00    16  |__ceph-osd
04:52:06 PM     0      5753         -    2.30    4.67    0.00    6.97     8  ceph-osd
04:52:06 PM     0         -      5753    0.01    0.00    0.00    0.01     8  |__ceph-osd
04:52:06 PM     0         -      5861    0.00    0.00    0.00    0.00    27  |__ceph-osd
root@node166:~# 

```


## 使用 -h 在一行上水平显示所有统计信息

如果要求 pidstat 报告多个统计数据，它会显示一个又一个统计数据。在下面的示例中，它将首先显示选项“r”的性能统计信息，然后是选项“u”，最后是选项“d”。

```
pidstat -rud
```

但是，如果希望单个进程的所有这些统计信息都显示在一行中，请使用选项 -h，如下所示:

```
root@node166:~# pidstat -rud -h | head
Linux 4.14.148-202302151035.git6a5dacc (node166) 	04/17/2023 	_x86_64_	(40 CPU)

#      Time   UID       PID    %usr %system  %guest    %CPU   CPU  minflt/s  majflt/s     VSZ     RSS   %MEM   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command
 1681721616     0         1    0.02    0.05    0.00    0.07    21      3.08      0.00  191392   11888   0.01     22.63      5.89      2.57       8  systemd
 1681721616     0         2    0.00    0.00    0.00    0.00    28      0.00      0.00       0       0   0.00      0.00      0.00      0.00       0  kthreadd
 1681721616     0         8    0.00    0.03    0.00    0.03     0      0.00      0.00       0       0   0.00      0.00      0.00      0.00       0  ksoftirqd/0
 1681721616     0         9    0.00    0.88    0.00    0.88     8      0.00      0.00       0       0   0.00      0.00      0.00      0.00       0  rcu_sched
 1681721616     0        11    0.00    0.00    0.00    0.00     0      0.00      0.00       0       0   0.00      0.00      0.00      0.00       0  migration/0
 1681721616     0        12    0.00    0.00    0.00    0.00     0      0.00      0.00       0       0   0.00      0.00      0.00      0.00       0  watchdog/0
 1681721616     0        15    0.00    0.00    0.00    0.00     1      0.00      0.00       0       0   0.00      0.00      0.00      0.00       0  watchdog/1
root@node166:~# 
```