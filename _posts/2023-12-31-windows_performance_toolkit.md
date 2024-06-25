---
title: Windows Performance Toolkit性能分析
date: 2023-12-31
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
summary: 本文介绍了Windows Performance Toolkit的简单入门使用，尚需更多实战才能使用好这个强悍的工具
categories:
    - [Windows]
    - [performance]
tags:
    - Windows
    - performance
---



# 概述

Windows Performance Toolkit（WPT）是微软提供的一个性能分析工具集，它包括了Windows  Performance Analyzer（WPA）和Windows Performance  Recorder（WPR）这两个核心工具。

简单来说，WPR 就是一个“抓包”工具，用来抓取系统的事件信息，而WPA就是将抓取的信息以图表的形式展示出来便于我们详细分析的工具。WPA分析WPR生成的.ETL文件（Event Trace Log）。

这个工具可以帮助开发者和系统管理员分析和诊断Windows应用程序的性能问题。

想了解更多信息，请查阅官方文档：[官方文档](https://learn.microsoft.com/zh-cn/windows-hardware/test/wpt/windows-performance-toolkit-technical-reference)



# 事件跟踪（ETW）
ETW 支持对内核和应用程序事件进行一致、直接的捕获。 你可以随时启用或禁用事件捕获，而无需重新启动系统或进程。 Windows 性能分析器 (WPA) 呈现 ETW 在一组易于理解的图形和表中收集的信息。

可以捕获并呈现所选事件以非侵入性的方式标识并诊断系统和应用程序性能问题。 可以动态启用或禁用事件跟踪。 Windows Performance Recorder (WPR) 使用 ETW 收集和组织关键系统信息。 WPR 充当会话控制器，启动和停止会话，并选择要记录的 ETW 事件。

WPA 使用所有事件提供程序在 ETW 会话中生成的事件跟踪日志 (ETL) 文件。 内核和应用程序事件可以提供有关系统操作的大量详细信息。 几乎每个影响整体系统性能的内核事件都已定义，并且可用于 WPA。


# 使用WPT步骤

以下是使用Windows Performance Toolkit对程序进行分析的基本步骤：

1. **安装工具**：
   - 确保你的Windows系统已经安装了Performance Toolkit。这通常可以通过Windows的功能选项或者从微软的官方网站[下载](https://learn.microsoft.com/zh-cn/windows-hardware/get-started/adk-install)。
2. **使用Windows Performance Recorder**：
   - 打开WPR，选择“开始记录”或“开始新的记录”来开始捕获性能数据。
   - 选择你想要分析的程序或进程，并设置相关的捕获选项，例如CPU、内存、磁盘、网络等。
   - 运行你的应用程序，执行你想要分析的操作。
3. **停止记录**：
   - 完成操作后，停止WPR的记录过程。WPR会生成一个包含性能数据的ETL（Event Trace Log）文件。
4. **使用Windows Performance Analyzer**：
   - 打开WPA，然后打开刚才WPR生成的ETL文件。
   - WPA会加载性能数据，并提供一个交互式的界面来分析数据。
5. **分析数据**：
   - 使用WPA的各种视图和工具来分析数据。例如，你可以查看CPU使用率、内存使用情况、磁盘I/O、网络流量等。
   - 使用图表、表格和时间线来识别性能瓶颈或异常行为。
6. **诊断问题**：
   - 根据分析结果，识别可能的性能问题，如高CPU使用率、内存泄漏、磁盘瓶颈等。
   - 使用WPA的诊断功能，如堆栈跟踪和代码路径分析，来进一步诊断问题。
7. **优化程序**：
   - 根据分析结果，对程序进行优化，以提高性能和响应速度。
8. **重复测试**：
   - 在优化后，重复上述步骤，以验证性能改进的效果。



# 实践

## 安装WPT

官方下载与当前PC端Windows系统匹配的版本并进行安装，安装界面参考如下：

<img class="shadow" src="/img/in-post/windows/install_windows_ADK.png" width="600">

<img class="shadow" src="/img/in-post/windows/install_windows_ADK_tools.png" width="600">



## WPR录制

WPR界面如下：

<img class="shadow" src="/img/in-post/windows/Record_system_information.png" width="600">



点击上图左下角的”Add Profiles…”按钮可通过后缀为.wprp格式文件进行参数记录配置的导入，其格式为xml，用记事本打开可进行编辑。

设置好相关配置后，点击“Start”开始录制，点击“Save”保存录制数据，然后点击WPR界面左下角的“Open in WPA”，进入WPA进行数据分析。



## WPA分析



### 功能预览

WPA界面全览如下图所示：

<img class="shadow" src="/img/in-post/windows/WPA界面全览.png" width="1200">



### 功能分类

主要分为六部分：

* System Activity
* Computation
* Storage
* Memory
* Video
* Power



#### System Activity（系统活动）

System Activity 主要用于监视和分析系统的各种活动，包括进程、线程、CPU 使用情况、系统响应能力等。这部分工具可以帮助你识别和解决系统性能问题，比如系统延迟、响应慢等。

- **进程和线程分析**：监控和记录系统中所有进程和线程的活动。
- **CPU使用情况**：跟踪 CPU 使用情况，识别消耗 CPU 资源最多的进程和线程。
- **系统延迟**：检测和分析系统调用的延迟，找出可能导致系统慢的瓶颈。



#### Computation（计算性能）

Computation 主要用于分析和优化计算性能。这部分功能重点在于破案破案 CPU 和 GPU 的使用情况，以及应用程序的计算任务的性能。

- **CPU 分析**：记录和分析 CPU 的使用情况，找出影响 CPU 性能的因素。
- **GPU 分析**：监控 GPU 的使用情况，优化图形计算和处理任务。
- **计算任务性能**：评估应用程序的计算任务执行效率，找出计算性能的瓶颈。



#### Storage（存储性能）

Storage 主要用于监控和分析存储设备的性能，包括硬盘、SSD 等。这部分工具可以帮助你检测磁盘 I/O 操作，优化存储性能。

- **磁盘 I/O 分析**：记录和分析读写操作的次数和速度，找出影响存储设备性能的因素。
- **存储性能优化**：通过分析存储设备的读写模式，优化存储设备的使用效率。
- **文件系统分析**：监控和分析文件系统操作，包括文件创建、删除和修改等。



#### Memory（内存性能）

Memory 主要用于监控和分析内存的使用情况，找出影响内存性能的问题。这部分工具可以帮助你优化内存管理，解决内存泄漏和过度占用的问题。

- **内存使用情况**：记录和分析应用程序和系统的内存使用情况，找出占用内存最多的进程。
- **内存泄漏检测**：检测和分析内存泄漏情况，帮助开发者修复内存泄漏问题。
- **内存分页**：监控和分析内存分页操作，优化内存分页效率，减少分页对系统性能的影响。



Video（视频性能）
Video 主要用于分析和优化视频相关的性能。这部分功能包括监控视频播放和渲染性能，找出影响视频效果的问题。

- **视频播放性能**：记录和分析视频播放过程中可能出现的卡顿和延迟，优化视频播放效果。
- **渲染性能**：监控视频及图形的渲染性能，优化渲染效率，减少渲染时间。
- **帧率分析**：检测视频播放的帧率，分析帧率不稳定的原因，优化视频流畅度。



#### Power（电源管理）

Power 主要用于监控和管理系统的电源使用情况。这部分工具可以帮助你优化电源管理策略，延长电池寿命，减少能耗。

- **电池使用情况**：记录和分析系统和应用程序的电池使用情况，找出耗电最大的进程。
- **电源模式分析**：监控和分析不同电源模式（如节能模式、高性能模式）的功耗，优化电源管理策略。
- **睡眠和唤醒分析**：检测和分析系统的睡眠和唤醒事件，找出影响系统稳定性的因素，优化睡眠和唤醒效率。



### 功能简述

#### 系统活动性（System Activity）分析简述

System Activity展开后显示如下内容：

<img class="shadow" src="/img/in-post/windows/System_Activity.png" width="400">



 双击Process图标，展开系统活动性中进程时间线分析窗口：

<img class="shadow" src="/img/in-post/windows/System_Activity_Process.png" width="800">



这里有两种进程，一种是Permanent（持续的），另一种是Transient（短暂的），我们打开这个短暂的分支，观察下FileCoAuth.exe 这个进程。点击搜索图标，输入进程名，点击过滤到输入则可以仅显示符合条件项。

<img class="shadow" src="/img/in-post/windows/WPA_processes.png" width="800">

如上图所示，阴影区域标识对应进程占用的时间片段。

使用相同的方法，我们来看一下线程

<img class="shadow" src="/img/in-post/windows/WPA_thread.png" width="800">

关闭掉不关心的Process信息，查询到Thread中我们关注的FileCoAuth.exe 这个进程：

<img class="shadow" src="/img/in-post/windows/WPA_thread_analiysis.png" width="800">



#### 分页内存池泄漏分析简述

WPA的分页内存，如下图所示：

<img class="shadow" src="/img/in-post/windows/WPA_Memory.png" width="800">

展开后我们看到：

<img class="shadow" src="/img/in-post/windows/WPA_Memory_exp.png" width="400">

如果想查看所有的Menory View，右击点击，添加自己所需的分析识图，如下图所示：

<img class="shadow" src="/img/in-post/windows/WPA_Memory_add_analysis_view.png" width="800">



# 小结

WPT功能非常强大，此篇文章只是安装与入门介绍，尚需多实践才能加深对此工具的使用。

尽管功能强大并且分析工具也可以直观的帮助我们查看日志， 但该工具最大问题在于生成的日志非常庞大，因此需要有足够的空间来缓存日志内容。 

其他无，优点就是太强悍了，O(∩_∩)O哈哈~
