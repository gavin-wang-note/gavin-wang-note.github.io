---
layout:     post
title:      "bzip2 vs pbzip2 性能对比"
subtitle:   "bzip2 vs pbzip2 performance"
date:       2020-06-01
author:     "Gavin"
catalog:    true
tags:
    - bzip2
    - pbzip2
---


# 概述

近期使用esrally进行Elastic Search性能压测，使用script产生了原始数据，这些原始数据需要被压缩成bz2格式，如果原文件大小很大，压缩起来就非常耗时。本文介绍几种bzip2压缩操作，观察耗时情况。


# 准备测试数据

准备10万笔记录，看看压缩耗时如何：


```
root@node244:/mnt/disk/esrally_data/test# time wc -l documents-2.json 
100000 documents-2.json

real	0m0.025s
user	0m0.005s
sys	0m0.020s
root@node244:/mnt/disk/esrally_data/test# cat documents-2.json | head -n 1
{"name": "08_9837907241.49", "bucket": "bucket01", "instance": "null", "meta": {"custom-string": {"name": "1597699173358823", "value": "5714268441146127"}, "mtime": "2020-05-26T19:21:32.598Z", "etag": "e7b647f4a3959de9c7a070e5d3093ab1", "content_type": "application/octet-stream", "tail_tag": "a3a5cefd-376d-421b-3110-08b41412e7c1.4520.862976", "size": "760"}, "owner": {"display_name": "user01", "id": "user01"}, "versioned_epoch": "0"}
root@node244:/mnt/disk/esrally_data/test# 
```


# 压缩验证


## 使用默认的bzip2压缩指令

```
root@node244:/mnt/disk/esrally_data/test# time bzip2 -k documents-2.json documents-2.json.bz2
bzip2: Input file documents-2.json.bz2 already has .bz2 suffix.

real	0m8.482s
user	0m8.454s
sys	0m0.028s
root@node244:/mnt/disk/esrally_data/test# ll
total 47444
drwxr-xr-x 2 root root     4096 Jun  2 16:01 ./
drwxr-xr-x 5 root root     4096 Jun  2 15:55 ../
-rw-r--r-- 1 root root 43800000 Jun  2 15:55 documents-2.json
-rw-r--r-- 1 root root  4769476 Jun  2 15:55 documents-2.json.bz2
root@node244:/mnt/disk/esrally_data/test# 
```

## bzip2 使用 -1 参数

```
root@node244:/mnt/disk/esrally_data/test# time bzip2 -k -1 documents-2.json documents-2.json.bz2
bzip2: Input file documents-2.json.bz2 already has .bz2 suffix.

real	0m5.411s
user	0m5.390s
sys	0m0.020s
root@node244:/mnt/disk/esrally_data/test# ll
total 48020
drwxr-xr-x 2 root root     4096 Jun  2 16:03 ./
drwxr-xr-x 5 root root     4096 Jun  2 15:55 ../
-rw-r--r-- 1 root root 43800000 Jun  2 15:55 documents-2.json
-rw-r--r-- 1 root root  5357900 Jun  2 15:55 documents-2.json.bz2
root@node244:/mnt/disk/esrally_data/test# 
```


## bzip2 使用 -9 参数

```
root@node244:/mnt/disk/esrally_data/test# time bzip2 -k -9 documents-2.json documents-2.json.bz2
bzip2: Input file documents-2.json.bz2 already has .bz2 suffix.

real	0m8.053s
user	0m8.049s
sys	0m0.004s
root@node244:/mnt/disk/esrally_data/test#
root@node244:/mnt/disk/esrally_data/test# ll
total 47444
drwxr-xr-x 2 root root     4096 Jun  2 16:10 ./
drwxr-xr-x 5 root root     4096 Jun  2 15:55 ../
-rw-r--r-- 1 root root 43800000 Jun  2 15:55 documents-2.json
-rw-r--r-- 1 root root  4769476 Jun  2 15:55 documents-2.json.bz2
```

## pbzip2

```
root@node244:/mnt/disk/esrally_data/test# time pbzip2 documents-2.json -z -k -1 -f  > documents-2.json.bz2

real	0m0.449s
user	0m9.834s
sys	0m0.096s
root@node244:/mnt/disk/esrally_data/test# ll
total 48028
drwxr-xr-x 2 root root     4096 Jun  2 16:09 ./
drwxr-xr-x 5 root root     4096 Jun  2 15:55 ../
-rw-r--r-- 1 root root 43800000 Jun  2 15:55 documents-2.json
-rw-r--r-- 1 root root  5366033 Jun  2 15:55 documents-2.json.bz2
root@node244:/mnt/disk/esrally_data/test# 
```

根据pbzip2的help信息，这里没有携带-p参数，默认会自己根据当前硬件CPU核数，计算使用多少路并发，默认32


# bzip2 vs pbzip2性能对比

使用 Compression Level -9, 压缩比率最大，但耗时会比 -1 要久，此选项是默认选项；

使用pzip2进行压缩，多并发情况下，压缩耗时明显要比bzip2 -1 要快。

孰优孰略，一目了然。

BTW，由于pbzip2只能压缩文件，不能对目录进行压缩，所以如果想使用pbzip2压缩目录，则需要借助tar工具。

