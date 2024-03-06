---
title: Some tools to troubleshoot Linux performance problems
date: 2024-01-31 23:02:00
author: Gavin Wang
img: "/img/performance.jpg"
top: false
hide: false
cover: true
coverImg:
password:
toc: true
mathjax: false
summary: This article introduces a few commonly used performance analysis tools for Linux, just to throw a wrench in the works.
categories:
    - [performance]
    - [Linux]
tags:
    - performance
    - Linux
---


# Overview

In this article, you'll learn how to collect information about your Linux system's performance.

Performance is one of those things that many system administrators dread. Sometimes you don't even think about it when things are running well. Then, suddenly you get a call from an end user, or even worse, lots of end users, that the application you're responsible for "feels slow." Or maybe it's outright unavailable. Now you have to go into troubleshooting mode.

Where do you start, though? In this article, I'll walk through some basics, but first, I'll take a step back. It's important to have some baseline information about your system before trying to identify problems. Maybe your system is doing something it shouldn't be, and that is contributing to the high load. Or perhaps it's doing exactly what it always has, and it's just under some additional load. Performance troubleshooting starts before a problem occurs by keeping good documentation and historical performance data.

This article summarizes three utilities that provide great initial performance information, command of top, free and vmstat.


# Start at the atop

The first go-to performance troubleshooting tool is atop. The atop utility gives you a great, constantly updated process and performance dashboard. What's the load of Network?How much memory is in use? What's the CPU load average? What's the Disks load average?What's the load average? What processes are using the most resources? All of this is ready at a moment's notice in atop.

<img class="shadow" src="/img/in-post/atop-overview.png" width="1200">

In addition, you can filter atop, such as searching for processes (type the letter p and then the process id you want to filter), or even viewing the utilization of each kernel in the system (type the letter l and adjust the number of CPU stats), as well as viewing the memory consumption of each process or service in the system, which is very powerful.


# free

This free tool shows the current memory consumption of your system, but free is a little brother to atop.

```shell
root@Gavin:~# free
               total        used        free      shared  buff/cache   available
Mem:         6021396      902228     4167908        1916     1220796     5119168
Swap:        4194300           0     4194300
root@Gavin:~#
```

> **Field descriptions:**

* total: Indicates the total physical memory size.
* used: Indicates how much memory has been used.
* free: the amount of free memory.
* Shared: the total amount of memory shared by multiple processes.
* Buffers/cached: the size of the disk cache.


> **Usage Introduction:**

Syntax: `free [-hbkmotV][-s <interval seconds>]`

Additional Note: The free directive displays memory usage, including physical memory, virtual swap file memory, shared memory segments, and buffers used by the system core.

> **Parameters:**

* -b Displays memory usage in Bytes.
* -k Shows memory usage in kilobytes (KB).
* -m Shows memory usage in MB.
* -h Display memory usage in a more user-friendly way.
* -o Do not display buffer reconciliation columns.
* -s <interval seconds> Continuously observe memory usage.
* -t Display memory sum column.
* -V Display version information.   


Remember that the Linux kernel will take available memory and allocate it to disk buffers and cache. Linux will release those resources when the system needs them, so if free suggests that you have no available memory, be sure to check that buffers/cache column before you conclude that you're out of memory.


# vmstat

Using vmstat is another great way to look at your memory consumption.

```shell
root@Gavin:~# vmstat 2 5
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 4165148  52340 1168620    0    0   172   108  111    0  0  1 99  0  0
 1  0      0 4165148  52340 1168620    0    0     0     0   48   76  0  0 100  0  0
 1  0      0 4165148  52340 1168620    0    0     0     0   45   70  0  0 100  0  0
 1  0      0 4165148  52348 1168612    0    0     0     8   54   86  0  0 100  0  0
 1  0      0 4165148  52348 1168620    0    0     0     0   46   73  0  0 100  0  0
root@Gavin:~# 
```

It breaks down the buffers and cache, and you'll also get information about your swap utilization. Swapping is generally a sign that your system is exhausting its higher-performing memory, and it must resort to swapping to disk. This process can have a devastating effect on some applications.


# Nmon

Nmon (Nigel's Monitor) is a free tool provided by IBM to monitor the resources of AIX and Linux systems. The tool can collect the server system resource consumption and output a specific file , and can use excel analysis tool (nmon analyser) for statistical analysis of data.

Open source performance monitoring tool for monitoring linux system resource consumption information , and can output the results to a file , and then through the nmon_analyser tool to generate data files and graphical results.

## Run nmon

You can run nmon like this:

```shell
nmon
```

<img class="shadow" src="/img/in-post/nmon.png" width="1200">

In the interactive window above, you can use the nmon shortcut to display different system resource statistics:
|Command | Remarks  |
|------------|---------------|
|q | Stop and exit Nmon  |
|h | View help  |
|c | View CPU statistics  |
|m | View memory statistics  |
|d | View hard disk statistics  |
|k | View kernel statistics  |
|n | View network statistics  |
|n | View NFS statistics  |
|j | View file system statistics  |
|t | View high-consumption processes  |
|V | View virtual memory statistics  |
|v | Detailed Mode  |

After pressing c, m, d, the following figure shows the consumption of CPU, memory and disk intuitively, press q to exit.


## data collection

When performance testing, you need to analyze the change of system resources in a period of time according to the execution of the test scenario, then you need nmon to collect the data and save it, the following parameters are commonly used:

* -f parameter: generate a file, file name = host name + current time.nmon
* -T parameter: show processes with high resource utilization.
* -s parameter: -s 10 means collect data every 10 seconds.
* -c parameter: -s 10 means collect data every 10 seconds.
* -m parameter: Specify the file storage directory



If you collect every 5 seconds, a total of 12 times, that is 1 minute of data (the generated file is marked in red):

```shell
root@Gavin:~# nmon -f -s 5 -c 12 -m /root/
```

The generated files are referenced below:

```shell
root@Gavin:~# ls -l Gavin_240131_1034.nmon 
-rw-r--r-- 1 root root 148714 Jan 31 10:34 Gavin_240131_1034.nmon
root@Gavin:~# 
```

The file name consists of:

Hostname_last-two-doubles-of-year-month-date_hour-minute.nmon

If you want to shut down the nmon process after data collection, you need to get the pid of nmon.


The collected data cannot be viewed directly, and the nmon_analyser tool is required to generate data files and graphical results.

Download link:[Download](https://sourceforge.net/projects/nmon/)
