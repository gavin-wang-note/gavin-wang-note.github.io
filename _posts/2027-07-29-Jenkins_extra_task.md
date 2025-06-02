---
title: Jenkins 任务里额外后台执行某个任务，不阻塞当前Jenkins任务
date: 2027-07-29 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: true
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 有个任务要脱离当前Jenkins，但又不能阻塞当前Jenkins的运行，即Jenkins任务结束了，但是这个任务里产生了其他任务可以继续运行
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

#  概述

目前我在 `Jenkins pipeline` 里使用 `shell`，执行 `python run_mkdocs.py &`，从代码记录到的日志来看，服务刚开始启动，然后就没有后续日志了，`ps` 过滤相关进程，并没有看到进程的存在，于是在`Jenkins pipeline` 里执行了如下命令：

`python run_mkdocs.py; sleep 60 &`

在 `sleep` 时间范围内，`ps` 过滤到了相关进程，但是一旦等 `Jenkins` 任务结束，相关进程就消失了。

Why？


# 问题原因分析

在 `Jenkins Pipeline` 中，当执行 `python run_mkdocs.py &; sleep 60` 时，虽然使用了 `&` 符号让 `Python` 脚本在后台运行，但 `Jenkins` 本身是一个自动化构建工具，它会管理任务的生命周期。在 `Pipeline` 中执行这些命令时，`Jenkins` 会将整个 `shell` 会话视为一个任务。在任务执行过程中，`Python` 脚本确实会在后台启动，但是当 `Jenkins` 的构建任务结束（包括 `sleep 60` 这部分任务执行完毕后），它会清理与该任务相关的资源，包括终止由该任务启动的子进程（即 `Python` 脚本进程）。


# 解决方案

在描述解决方案之前，我先说一下尝试了哪些方案。

## nohup

使用 `nohup` 不起作用，如：`nohup python run_mkdocs.py > output.log 2>&1 &`

## 使用 BUILD_ID 变量

在 `Jenkins` 的 `shell` 脚本中，添加`export BUILD_ID=dontKillMe`，然后在后台执行 `Python` 脚本。具体命令如下：

```shell
export BUILD_ID=dontKillMe
nohup python run_mkdocs.py > output.log 2>&1 &
```

## 使用 setsid 命令

`setsid` 命令可以将作业与当前的终端会话分离，从而避免进程在终端关闭时被终止。命令如下：

```shell
setsid python run_mkdocs.py > output.log 2>&1 &
```

## 使用 disown 命令

在启动 `Python` 脚本后，使用 `disown` 命令将其从当前的终端会话中分离。命令如下：

```shell
python run_mkdocs.py > output.log 2>&1 &
```

### 使用 at 命令


`at`命令可以将 `Python` 脚本的执行计划安排在指定时间执行，这样可以避免因 `Jenkins` 构建任务结束而导致的进程终止。命令如下：

```shell
echo "python run_mkdocs.py" | at now
```

**上面方案我都一一尝试了，但是都没有达到预期效果，不过最终还是选择了 `at` 来实现。**


## 经过验证的可行方案

延时执行，就是说 `Jenkins Pipeline` 里帮我新增一个 `at` 任务，这个任务是在未来执行的，我延时了一分钟，参考如下：

```shell
echo "python run_mkdocs.py" | at now + 1 minute
```

因为上述步骤是在整个 `Jenkins Pipeline` 任务的最后，所以这里等待一分钟是足够的，当然，使用者可以根据实际情况调整 `at` 任务的执行时间。


## 其他可行方案

下面方案理论上是可行的，但是由于环境受限，没安装这两个命令，导致我没有验证。

其原理是使用一个固定 `session` ， 如示例中的 `my_session`， 每次进入这个 `session` 来执行命令，从而实现命令的执行与 `Jenkins Task `的分离。 

### 使用 screen 工具

`screen`工具可以创建一个独立的终端会话来运行 `Python` 脚本，即使原终端会话关闭，`screen`会话也会继续运行。命令如下：

```shell
screen -dmS my_session python run_mkdocs.py
```

### 使用 tmux 工具

类似于`screen`，`tmux`也可以在一个独立的会话中运行脚本。命令如下：

```shell
tmux new-session -d -s my_session 'python run_mkdocs.py'
```
