---
title: Linux下一次性任务(at和batch命令)
date: 2015-04-06 23:01:57
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: Linux下at和batch实现一次性任务执行
categories:
    - [Linux]
tags:
    - Linux
---

# Overview

我们知道，在Linux中可以使用cron实现周期性任务，但如果我有一个一次性任务，该如何做呢？

也许你会说，可以使用nohup或者tmux里执行类似这样的指令达到预期目的：

```shell
sleep 7200; ./do_st.sh
```

即根据当前时间，计算一下预期需要等到多久，再执行具体命令。

Hmm，太trick了...

今天介绍另外一种方式，使用`at`命令。

# `at` 介绍

在 Linux 中，你可以使用 `at` 命令来安排一次性的定时任务。`at` 命令允许你在将来的某个时间点执行一个命令或一组命令。


##  安装

对于基于 `Debian` 的系统（如 `Ubuntu`）：

```shell
sudo apt-get update
sudo apt-get install at
```

对于基于 `Red Hat` 的系统（如 `CentOS` 或 `Fedora`）：

```shell    
sudo yum install at
···

或者，如果你使用的是 dnf：

```shell
sudo dnf install at
···

## 使用 `at` 命令安排任务

假设你想在 5 分钟后运行以下命令：
       
```shell
echo "Hello, World!" > /tmp/hello.txt
```

你可以这样做：

```shell
echo "echo 'Hello, World!' > /tmp/hello.txt" | at now + 5 minutes
```

这里，`echo` 命令用于将待执行的命令传递给 `at`, `now + 5 minutes` 指定了任务的执行时间。


## 查看已安排的任务

使用 `atq` 命令查看已安排的任务及其作业号：

```shell 
atq
```

输出可能如下所示：

```shell
Job 1 at 2015-04-06 15:00
```

## 取消已安排的任务

如果你想取消一个已安排的任务，可以使用 `atrm` 命令，后面跟上作业号：

```shell
atrm 1
```

这里，1 是你想取消的任务的作业号。

## 使用 `at` 的交互模式

我们还可以将 `at` 命令与 `-t` 选项一起使用，以指定确切的日期和时间：

```shell
at -t 2015-04-06 15:00
```

然后，你会进入一个提示符，可以输入要安排的命令。输入完成后，按 `Ctrl + D` 保存并退出。

## 使用 batch 命令

`batch`命令是 `at` 的一个变体，它会在系统负载较低时运行任务。这可以用于不紧急的任务：

```shell
echo "echo 'Hello, World!' > /tmp/hello.txt" | batch
```

或者，使用交互模式：

```shell        
batch
```

然后输入命令，完成后按 `Ctrl + D` 保存并退出。


# 应用场景示例

## 使用at的场景和示例

### 安排一次性任务


你想在明天的某个特定时间运行一个脚本:

```shell
at 9:00 PM tomorrow <<END
/path/to/your/script.sh
END
```

### 发送提醒邮件

你想要在一周后的今天发送一封提醒邮件给自己:

```shell 
echo "This is a reminder for the meeting next week." | at now + 1 week
```

### 系统维护

你需要在夜间执行系统维护任务，比如运行 `apt-get update` 和 `apt-get upgrade`。

```shell  
echo "sudo apt-get update && sudo apt-get upgrade -y" | at 2:00 AM
```

### 定时备份

你想要每天凌晨2点自动运行备份脚本:

```shell
echo "/path/to/backup.sh" | at 2:00 AM
```

### 定时关机

你需要在特定时间自动关闭系统:

```shell 
echo "sudo shutdown -h now" | at 5:00 PM
```

## 使用 batch 的场景和示例

### 低优先级数据处理

你有一项数据处理任务，不需要立即完成，可以在系统负载较低时运行:

```shell  
echo "/path/to/data_processing.sh" | batch
```

### 夜间运行的低优先级任务

你想要在夜间系统负载较低时运行一个长时间的计算任务:

```shell
echo "/path/to/long_computation.sh" | batch -t 23:00
```

### 系统清理任务

你需要定期清理日志文件和临时文件，这可以在夜间进行，以减少对系统性能的影响:

```shell        
echo "/path/to/system_cleanup.sh" | batch
```

### 定期数据库维护

数据库需要定期维护，比如每周日的凌晨1点运行数据库清理脚本:

```shell
echo "/path/to/db_maintenance.sh" | batch -t 01:00
```

### 非紧急的文件传输

你需要在网络负载较低时进行文件传输，比如在夜间:

```shell
echo "rsync -avz /source/ /destination/" | batch
```

**注意**

* `at` 和 `batch` 命令通常在后台运行，不会显示命令的输出。如果你想查看输出，可以将输出重定向到文件中，如上例所示。
* `at` 和 `batch` 命令的具体行为可能会因系统和配置的不同而有所差异。在使用这些命令时，你应该检查你的系统文档以了解它们的具体用法和选项。此外，出于安全考虑，确保你了解这些命令的权限和潜在风险。

# Overall

使用 `at` 命令安排一次性定时任务是一种简单而有效的方法，适用于需要在将来某个时间点执行的任务。
