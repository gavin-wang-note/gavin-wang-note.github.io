---
layout:     post
title:      "Monkey详解"
subtitle:   "Monkey"
date:       2015-08-21
author:     "Gavin Wang"
catalog:    true
categories:
    - [Monkey]
tags:
    - Monkey
---


# Monkey 是什么？

Monkey 就是SDK中附带的一个工具。



# Monkey 测试的目的？

该工具用于进行压力测试。 然后开发人员结合monkey 打印的日志 和系统打印的日志，结局测试中出现的问题。



# Monkey 测试的特点？

Monkey 测试,所有的事件都是随机产生的，不带任何人的主观性。



# Monkey 命令详解

## 标准的monkey 命令

```[adb shell] monkey [options] <eventcount> ```

例如：

```adb shell monkey -v 500 ```

产生500次随机事件，作用在系统中所有activity（其实也不是所有的activity，而是包含  Intent.CATEGORY_LAUNCHER 或Intent.CATEGORY_MONKEY 的activity）。
上面只是一个简单的例子，实际情况中通常会有很多的options 选项



## 四大类 -- 常用选项 、 事件选项 、 约束选项 、 调试选项

### 常用选项

--help：打印帮助信息

-v：指定打印信息的详细级别，一个 -v增加一个级别 ， 默认级别为 0 。


### 事件选项


-s：指定产生随机事件种子值，相同的种子值产生相同的事件序列。如： -s 200

--throttle：每个事件结束后的间隔时间——降低系统的压力（如不指定，系统会尽快的发送事件序列）。如：--throttle 100

--pct-touch：指定触摸事件的百分比，如：--pct-touch 5% ， 相关的还有以下option：

--pct-motion <percent> （滑动事件）、 --pct-trackball <percent> （轨迹球事件） 、 --pct-nav <percent> （导航事件 up/down/left/right）、 --pct-majornav <percent> (主要导航事件 back key 、 menu key)、 --pct-syskeys <percent> (系统按键事件 Home 、Back 、startCall 、 endCall 、 volumeControl)、 --pct-appswitch <percent> （activity之间的切换）、 --pct-anyevent <percent>（任意事件）


### 约束选项

-p：指定有效的package（如不指定，则对系统中所有package有效），一个-p 对应一个有效package， 如：-p com.ckt -p com.ckt.asura；

-c：activity必须至少包含一个指定的category，才能被启动，否则启动不了；


### 调试选项

--dbg-no-events：初始化启动的activity，但是不产生任何事件。

--hprof：指定该项后在事件序列发送前后会立即生成分析报告  —— 一般建议指定该项。

--ignore-crashes：忽略崩溃

--ignore-timeouts：忽略超时

--ignore-security-exceptions：忽略安全异常

--kill-process-after-error：发生错误后直接杀掉进程

--monitor-native-crashes：跟踪本地方法的崩溃问题

--wait-dbg：知道连接了调试器才执行monkey测试。



# 一个简单的monkey命令：

```adb shell monkey -p com.xy.android.junit -s 500 -v 10000 ```

但是，工作中为了保证测试数量的完整进行，我们一般不会在发生错误时立刻退出压力测试。

monkey 测试命令如下：

```adb shell monkey -p com.xy.android.junit -s 500 --ignore-crashes --ignore-timeouts --monitor-native-crashes -v -v 10000 > E:\monkey_log\java_monkey_log.txt```



# monkey作用的包：com.ckt.android.junit

产生时间序列的种子值：500
忽略程序崩溃 、 忽略超时 、 监视本地程序崩溃 、 详细信息级别为2 ， 产生 10000个事件 。


