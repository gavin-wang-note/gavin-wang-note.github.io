---
layout:     post
title:      "获取系统中所有的pid"
subtitle:   "Get all of pid from OS"
date:       2020-07-08
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [shell]
tags:
    - shell
---

# 概述

Linux进程的pid，会在/proc目录下产生对应pid目录，如果想获取当前系统所有的pid，可以到此目录下去找。

本文介绍几种方法，获取到所有的pid。


# 实践


## 方法1. grep

```ls /proc/ | grep ^[0-9] ```


## 方法2. echo

```(cd /proc && echo +([0-9])) ```

或者

```for d in /proc/*;do [[ $d =~ /proc/[0-9]+ ]] && echo ${d#/proc/};done ```

## 方法3. awk

```ls | awk '{if ($i ~ /^[0-9]/) print $i}' ```

## 方法4. ls 与 echo 结合

```ls -d *[0-9]* ```

或者:

```ls -d * | echo +([0-9]) ```

或者:

```ls -F |grep "/$" | echo +([0-9]) ```

或者:

```ls -l |grep "^d" | echo +([0-9]) ```

或者:

```ls -l |grep "^d" |awk '{print $NF}' |  echo +([0-9]) ```

## 方法5. find 与 echo 结合

```find . -type d -maxdepth 1 |& echo +([0-9]) ```

