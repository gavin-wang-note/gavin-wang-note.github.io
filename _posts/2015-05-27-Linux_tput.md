---
title: Linux下tput更改终端设置
date: 2015-05-26 13:28:36
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: tput更改终端设置，颜色、移动光标
categories:
    - [Linux]
tags:
    - Linux
---


# Overview

闲着没事，水一篇...

tput命令用于更改终端设置，如设置文本颜色，移动光标位置。


# 设置颜色

```shell
for i in `seq 1 10`; do tput setaf $i; echo "This is in color $i"; done
```

效果图如下所示：

<img class="shadow" src="/img/in-post/tput_setaf.png" width="800">

# 移动光标

tput 是一个终端操作实用程序，它利用 terminfo 数据库操纵终端。你可以使用它来移动光标，清除屏幕或部分区域，以及改变字体样式等。光标移动是 tput 的基本功能之一。
移动光标的tput命令：

* tput cup Y X: 移动光标到屏幕上的位置（Y，X），其中 Y 是行号，X 是列号，计数从0开始。
* tput home: 移动光标到左上角（同0 0）。
* tput cuf N: 将光标向前（右）移动 N 个位置。
* tput cub N: 将光标向后（左）移动 N 个位置。
* tput cuu N: 将光标向上移动 N 行。
* tput cud N: 将光标向下移动 N 行。

# 示例

* 移动光标到特定位置

```shell
# 移动光标到第5行第10列
tput cup 4 9
```

* 将光标移至屏幕左上角（通常认为是0 0，但使用tput时不需要指定0 0）

```shell
tput home
```

* 将光标向右移动5个位置

```shell
tput cuf 5
```

* 将光标向上移动3行

```shell
tput cuu 3
```

# 使用tput移动光标的脚本示例

以下是一个简单的bash脚本示例，演示如何使用tput在屏幕上绘制一个静态的文本框。脚本使用tput来定位光标并画出框的四个角：

```shell
#!/bin/bash
# 定义文本框的大小
width=50
height=10

# 定位到屏幕中央
tput cup $(( ( $(tput lines) - height ) / 2 )) $(( ( $(tput cols) - width ) / 2 ))

# 画上边界
printf '┌'
for (( i = 1; i <= width - 2; i++ )); do
    printf '─'
done
printf '┐'

# 画中间内容
for (( i = 1; i <= height - 2; i++ )); do
    tput cud 1
    tput cub $((width - 1))
    printf '│'
    tput cuf $((width - 2))
    printf '│'
done

# 画下边界
tput cud 1
tput cub $((width - 1))
printf '└'
for (( i = 1; i <= width - 2; i++ )); do
    printf '─'
done
printf '┘'

# 将光标移回原位
tput cup $(( $(tput lines) - 1 )) 0
```

上述代码运行效果如下图所示：

<img class="shadow" src="/img/in-post/tput_setaf2.png" width="800">

# 进阶示例

我们可以结合使用tput和echo命令，在终端中绘制一个框。此示例展示了如何利用tput进行光标控制和绘图：

```shell
# 清屏
clear
# 移动到左上角
tput cup 0 0
echo -n "+"; for i in {1..20}; do echo -n "-"; done; echo "+"
for i in {1..10}
do
    tput cup $i 0
    echo -n "|"
    tput cup $i 22
    echo "|"
done
tput cup 11 0
echo -n "+"; for i in {1..20}; do echo -n "-"; done; echo "+"
```


上述代码运行效果如下图所示：

<img class="shadow" src="/img/in-post/tput_setaf3.png" width="800">


**注意:**

* 上述示例假定你的终端支持某些Unicode字符来绘制边界。如果终端不支持，你可以选择ASCII字符（如-和|）替代。
* 不仅可以用tput改变光标的位置，但也可以用于其他高级终端操作，比如设置前后景色，使文本加粗、下划线、闪烁等特效。了解这些命令可以帮你设计动态的输出或交互式的脚本。
