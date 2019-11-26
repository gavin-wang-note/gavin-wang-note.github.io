---
layout:     post
title:      "Lunux常用命令"
subtitle:   "Linux command"
date:       2019-11-26
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


#测试中常用的Linux命令汇总

# 概述
在日常测试工作中，产品是部署在Linux系统上的，本文罗列一下在测试过程中，常用到的一些指令

# 批量生成文件

方法1：

```seq 1 10  | xargs -i{} -P 10 touch file_{}  ```

10个并发来touch file


方法2：

```for i in {1..100}; do dd if=/dev/zero of=file_$i bs=1M count=1; done ```

这个没有并发哦~


方法3：

```touch file{0..9}.txt ```

相应的，创建目录、删除目录/文件（夹），都可以以此类推：

```rm -rf file{0..9} ```

```mkdir dir{0..9} ```

```rm -rf dir{0..9} ```



# 
