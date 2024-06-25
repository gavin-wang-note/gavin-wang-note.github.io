---
title: Windows Performance Tools介绍
date: 2024-06-25
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 介绍几个Windows Performance Tools，方便未来之需，便于未来Windows下性能测试分析使用
categories:
    - [Windows]
    - [performance]
tags:
    - Windows
    - performance
---

# Overview

介绍几款Windows下的性能分析工具，用于分析PC端应用程序的性能瓶颈所在。

# 工具介绍

* Perfmon（性能监视器）：是Windows自带的性能监控工具，可以通过它来查看CPU、内存、硬盘、网络等系统性能指标的实时数据，也可以将数据保存到文件中进行后续分析。
* Process Explorer：是一个高级的系统任务管理器，可以显示进程信息、线程信息、内存使用情况、CPU使用情况等详细信息，也可以实时监控进程的活动。
* Sysinternals Suite：是一个由微软官方提供的一组系统工具集合，其中包括了很多用于性能监控的工具，例如Process Monitor、DiskMon、TCPView等。
* Windows Performance Toolkit：是一组高级性能监控工具，可用于性能分析和故障排查，包括xperf、WPR、WPA等。

# 工具概览

## Perfmon

Windows自带的，详细使用方法，参考官方[链接](https://techcommunity.microsoft.com/t5/ask-the-performance-team/windows-performance-monitor-overview/ba-p/375481)

## Process Explorer

下载后即可使用，官方下载链接，请点击此处进行[下载](https://learn.microsoft.com/zh-cn/sysinternals/downloads/process-explorer).

<img class="shadow" src="/img/in-post/windows/ProcessExplorer.png" width="800">


## Sysinternals Suite

[官网](https://learn.microsoft.com/zh-cn/sysinternals/)有详细的使用介绍，请查阅官网资料。

## Windows Performance Toolkit

这个工具比较复杂，也非常的强悍，后面再专门介绍。

想了解的读者，请移步[官网](https://learn.microsoft.com/zh-cn/windows-hardware/test/wpt/windows-performance-toolkit-technical-reference)。
