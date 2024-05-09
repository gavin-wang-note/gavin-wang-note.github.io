---
layout:     post
title:      "Linux ncdu命令"
subtitle:   "Linux command之ncdu"
date:       2016-09-15
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---


# Overview

我们知道，在`Linux`下查看空间使用情况的命令，有`df，du，lsblk`等，今天介绍另外一个命令：`ncdu`。

# 篇外篇之df, du, lsblk

在介绍之前，简单介绍一下`df，du，lsblk`

## df

该命令用于显示磁盘空间的使用情况，可以查看文件系统的总空间、已用空间和可用空间等信息。

使用方法如下：

```bash   
df -h
```

该命令的-h选项表示以易读的格式显示信息（如以`K、M、G`为单位），默认以块为单位显示。

## du

该命令用于显示文件或目录的磁盘使用情况。常用的选项有`-a，-sh`。

使用方法如下：


```bash  
du -sh /path/to/directory
```

* -s表示仅显示目录的总计大小，而不显示目录下各个文件的信息；
* -h表示以易读的格式显示磁盘使用大小。


## lsblk

该命令列出所有可用的块设备，并且可以查看磁盘的使用情况。

使用方法如下：

```bash
lsblk
```

这将列出所有已连接的块设备和其分区，以及它们的容量、分区大小、文件系统类型等信息。


# 言归正传之ncdu命令

`ncdu（NCurses Disk Usage）`是一个基于文本的交互式磁盘使用情况分析器。它以一种更人性化和直观的方式展示了磁盘空间的使用情况，使用户能够更容易地识别无用的大文件，从而释放磁盘空间。


## 安装

大多数`Linux`发行版可以直接通过包管理器安装`ncdu`。例如，在基于`Debian`的系统（如`Ubuntu`）上，可以使用以下命令安装：


```bash 
apt-get install ncdu
```

## 基本使用

运行`ncdu`时，你没有提供任何目录作为参数，它将分析当前目录：


```bash
ncdu
```

如果你提供了特定的目录作为参数，它将分析那个目录：


```bash  
ncdu /path/to/directory
```

## 导航

* 键盘方向：使用方向键在菜单和选项之间移动。
* v：在子目录上按v可以查看选定目录的使用情况。
* q：退出当前分析视图，返回上一级或退出程序。

## 查看信息

* `ncdu`显示一个列表，其中通常包括目录、文件、大小、数量、总计和已访问百分比。

* 通过按回车或.（点）键，可以选择不同的项目以进一步分析。

## 排序

默认情况下，`ncdu`按总大小排序。用户还可以按其他标准排序。

* 按大小或名称：+（加号）
* 按大小顺序反转排序：-（减号）
* 按数量排序（如文件数量或块数量）：*（星号）


## 硬链接

默认情况下，`ncdu计`算硬链接，这可以更准确地显示磁盘使用情况。如果要禁用硬链接仅查看占用空间，可以尝试添加`-x`或`--exclude-links`选项：

```bash
ncdu -x /path/to/directory
```

## 版本历史记录

如果你的`ncdu`版本支持，可以查看历史记录，以查看在不同时间段进行的分析结果的差异和比较。


```bash
ncdu -t -o /path/to/directory
```

## 显示隐藏文件

`ncdu`默认情况下不包括以点（.）开头的隐藏文件，要包括，可使用-a：

```bash   
ncdu -a /path/to/directory
```

## 输出

`ncdu`可以在分析结束后生成一个文本文件，其中包含在终端中列出的所有数据项：

```bash
ncdu /path/to/directory --no-color --exclude "^/$" --include "/.*" --prefixProbability "f" --pruneOperator ">" --prune "^/dev" > ncdu-output.txt
```

# Overall

`ncdu`是一个非常有用的工具，甚至被一些专家视为比传统的`du`命令更优秀的文件系统分析工具。学习如何使用`ncdu`可以帮助你更有效地管理磁盘空间。

