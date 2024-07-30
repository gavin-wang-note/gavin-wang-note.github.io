---
layout:     post
title:      "替换文件中空行"
subtitle:   "Delete space line with awk/tr/sed/grep"
date:       2014-06-07
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - awk
    - sed
    - tr
    - grep
---

# 概述

本文主要描述，如果在Linux下，使用命令行方式，对文本文件中的空行进行替换操作

# vi模式

真正删除空行，可以使用vim

通过命令模式删除空行。vim在命令模式下(在vim里输入英文字符:进入命令模式)输入： %s/^n//g 。意思是全局替换所有以回车开头的字符，替换为空。
如果有多个连续的空行，想保留一行。则只需在命令行模式输入下行即可：%s/^n$//g


# Linux pipline方式
主要是删除方法，使用grep，awk，sed，tr，xargs等命令进行处理

## grep

```grep -v '^$' filename ```

或

```grep -vE "^[[:blank:]]*$" filename ```


## sed

```sed '/^$/d'  filename ```

或

```sed -n '/./p' filename ```

或

```sed '/^[[:blank:]]*$/d' filename ```


## awk

$0表示一行

```awk '/./ {print}' filename ```

或

```awk '!/^[[:blank:]]*$/{print $0}' filename ```

或

```awk '{if($0!="") print}' ```


## tr

```tr -s "\n" ```


