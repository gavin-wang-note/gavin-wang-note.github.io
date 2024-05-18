---
title: env与printenv的区别
date: 2013-10-06 11:33:00
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: Linux下env与printenv的区别
categories:
    - [Linux]
tags:
    - Linux
---


# Overview

在Linux和UNIX系统中，env和printenv是两个常用的环境变量相关命令。尽管它们都与环境变量打交道，但它们的功能和用途有所不同。本文将详细介绍这两个命令的区别，并提供一些使用场景。

# env命令

env命令用于在执行另一个命令之前设置或修改环境变量。它的基本语法如下：


```shell
env [OPTION] [-] [NAME=VALUE]... [COMMAND [ARG]...]
```

主要特点：

* 设置和修改环境变量：可以在执行其他命令之前设置或修改环境变量。
* 传递环境变量：可以传递一组环境变量给后续执行的命令。
* 忽略继承的环境变量：使用-选项时，env将忽略从父进程继承的环境变量，只使用命令行指定的环境变量。


使用场景：

* 运行特定环境的程序：当你需要在特定环境变量下运行某个程序时，可以使用env来设置这些环境变量。
* 调试：在调试程序时，可能需要临时修改环境变量以观察程序行为的变化。


示例：

```shell
env PATH=/usr/local/bin:$PATH /path/to/program
```

这个命令将设置PATH环境变量，然后执行/path/to/program。

# printenv命令

`printenv`命令用于打印出所有的环境变量及其值，或者指定的环境变量的值。它的基本语法如下：


```shell
printenv [VARIABLE]...
```

主要特点：

* 打印环境变量：打印出所有的环境变量及其值，或者指定的环境变量的值。
* 查看环境变量：用于查看当前环境中设置的变量。


使用场景：

* 查看环境变量：当你需要查看当前环境中的所有环境变量或特定变量的值时。
* 配置和诊断：在配置系统或诊断问题时，查看环境变量可以帮助理解系统的运行状态。


示例：

```shell
printenv
```

这个命令将打印出所有的环境变量及其值。

或者，只打印特定的环境变量：

```shell
printenv PATH
```

这个命令将只打印PATH环境变量的值。

# 总结

`env`和`printenv`虽然都与环境变量相关，但它们的用途和功能有明显区别：

* env用于在执行其他命令之前设置或修改环境变量，常用于运行特定环境的程序或调试。
* printenv用于打印出所有的环境变量及其值，或者指定的环境变量的值，常用于查看环境变量以进行配置和诊断。
