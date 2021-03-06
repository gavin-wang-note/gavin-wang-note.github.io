---
layout:     post
title:      "Linux下统计行数性能对比"
subtitle:   "Performance compare when get line numbers from file"
date:       2020-05-28
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

这次使用esrally进行elastic search性能测试，构造了产品自己生成的索引所需要的数据，由于数据比较大，行数有700million+，统计行数碰到了问题，主要是时间问题，统计太耗时，所以，想知道哪个统计效率更高。

本文介绍几种方法，以100million行数的文件，在Linux下统计文件行数，对比下统计性能如何。


# 准备工作

准备一个100million行数的文件：

```
root@host75:~/tmp# ll
total 3018132
drwxr-xr-x 2 root root       4096 May 28 17:39 ./
drwx------ 4 root root       4096 May 28 17:38 ../
-rw-r--r-- 1 root root 3090550784 May 28 17:39 documents-2.json
root@host75:~/tmp# du -sh *
3.3G	documents-2.json
root@host75:~/tmp# cat documents-2.json | head -n 2
{"name": "50_9213603372.65", "bucket": "bucket01", "instance": "null", "meta": {"custom-string": {"name": "1729620399787334", "value": "9600528609211706"}, "mtime": "2020-05-25T18:26:36.457Z", "etag": "e7b592f4a6232de9c7a070e5d7456ab1", "content_type": "application/octet-stream", "tail_tag": "a3a5cefd-376d-421b-6085-08b56886e7c1.4520.288519", "size": "972"}, "owner": {"display_name": "user01", "id": "user01"}, "versioned_epoch": "0"}
{"name": "39_1283951288.80", "bucket": "bucket01", "instance": "null", "meta": {"custom-string": {"name": "5902405182780371", "value": "6086948407181992"}, "mtime": "2020-05-28T12:22:37.787Z", "etag": "e7b351f4a7411de9c7a070e5d2381ab1", "content_type": "application/octet-stream", "tail_tag": "a3a5cefd-376d-421b-7442-08b70241e7c1.4520.567559", "size": "152"}, "owner": {"display_name": "user01", "id": "user01"}, "versioned_epoch": "0"}
root@host75:~/tmp# 
```


# 统计行数性能比较

## 使用wc统计

```
root@host75:~/tmp# time wc -l documents-2.json 
100000000 documents-2.json

real	0m9.857s
user	0m2.767s
sys	0m7.041s
root@host75:~/tmp#
```

## awk


```
root@host75:~/tmp# time awk '{print NR}' documents-2.json | tail -n1
100000000

real	1m16.523s
user	1m5.944s
sys	0m14.584s
root@host75:~/tmp# 
```


```
root@host75:~/tmp# time awk 'END{print NR}' documents-2.json 
100000000

real	0m43.118s
user	0m32.708s
sys	0m10.395s
root@host75:~/tmp#
```


## grep & awk 结合

```
root@host75:~/tmp# time grep -n "" documents-2.json | awk '{{print }}' | tail -n1
100000000:{"name": "23_1479119854.64", "bucket": "bucket01", "instance": "null", "meta": {"custom-string": {"name": "6389993698492958", "value": "9869611550099604"}, "mtime": "2020-05-29T13:24:30.042Z", "etag": "e7b195f4a3730de9c7a070e5d5762ab1", "content_type": "application/octet-stream", "tail_tag": "a3a5cefd-376d-421b-7964-08b62339e7c1.4520.381771", "size": "819"}, "owner": {"display_name": "user01", "id": "user01"}, "versioned_epoch": "0"}

real	1m31.090s
user	1m21.797s
sys	2m8.774s
```

## sed

```
root@host75:~/tmp# time sed -n '$=' documents-2.json 
100000000

real	0m23.395s
user	0m13.503s
sys	0m9.891s
root@host75:~/tmp# 
```


## cat 

```
root@host75:~/tmp# time cat documents-2.json | wc -l
100000000

real	0m22.773s
user	0m3.910s
sys	0m31.834s
root@host75:~/tmp# 
```

说明：

这个方法不建议使用，比较考验CPU能力。


# 总结

由于被统计的文件的数据结构不一样，上述命令统计出来的性能也会有一些差异。本文示例的文档，统计效果比较好的方法是：

wc -l 优于 cat 优于 sed 优于 awk 优于 grep

具体哪个统计方法适合当前被统计文档，可以适当的使用一部分数据作为统计效果看看哪个更优，然后再做抉择使用哪个方法。

