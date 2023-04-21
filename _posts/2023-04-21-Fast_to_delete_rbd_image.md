---
layout:     post
title:      "快速清除rbd image"
subtitle:   "Fast to delete rbd image"
date:       2023-04-21
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

当集群里出现一个较大的rbd image时，如何快速清理掉它并释放空间，已经存在文章 ：https://cephnotes.ksperis.com/blog/2014/07/04/remove-big-rbd-image/ 做了介绍。
并且对不同的方法做了分析，这里先把结论说下:

| rbd类型    | rbd rm 方法                        | rados -p rm方法                                            |
| ------- | ------------------------- | --------------------------------------------------- |
|未填充很多|	慢|	快|
|已填充很多|	快|	慢 |

在rbd进行删除的时候，即使内部没有对象数据，也一样需要一个个对象去发请求，即使对象不存在，这个可以开日志看到:
在/etc/ceph/ceph.conf中添加

```
[client]
debug_ms=1
log_file=/var/log/ceph/rados.log
```

# 实践

dd写，bs=1M,写了40G的数据：
```
root@pytest-83-19:~# dd if=/dev/zero of=/dev/rbd0 bs=1M count=40960
40960+0 records in
40960+0 records out
42949672960 bytes (43 GB, 40 GiB) copied, 261.264 s, 164 MB/s
```

## rbd image 信息


```
root@pytest-83-19:~# rbd ls
889795de-fafb-4fca-9bf1-9b984e6124d2.img
root@pytest-83-19:~# rbd info rbd/889795de-fafb-4fca-9bf1-9b984e6124d2.img
rbd image '889795de-fafb-4fca-9bf1-9b984e6124d2.img':
	size 600GiB in 614400 objects
	order 20 (1MiB objects)
	used objects: 0
	block_name_prefix: rbd_data.30dc419495cff
	format: 2
	features: layering
	flags: 
	create_timestamp: Fri Apr 21 14:26:48 2023
root@pytest-83-19:~#


```

## 原始的快速删除方法


```
root@pytest-83-19:~# time rados -p rbd ls | grep '^rbd_data.30dc419495cff' | xargs -n 200  rados -p rbd rm

real	2m5.564s
user	0m46.126s
sys	0m4.718s
root@pytest-83-19:~# 
```




## 开启多进程删除的方法

这个比上面那种方法好的是：

* 可以显示当前删除的进度
* 可以指定删除的进程并发数
* 可以显示当时正在删除的对象
* 可以增加一个中断时间降低负载

首先获取一个需要快速删除的rbd的列表:

### 获取prifix

```
root@pytest-83-19:~# rbd info rbd/889795de-fafb-4fca-9bf1-9b984e6124d2.img | grep prefix
	block_name_prefix: rbd_data.30dc419495cff
root@pytest-83-19:~# 
```

### 获取列表

```
root@pytest-83-19:~# rados -p rbd ls |grep rbd_data.30dc419495cff > delobject
```

这里可以看下内容有没有问题，检查确认下:

```
root@pytest-83-19:~# vim delobject 
rbd_data.30dc419495cff.0000000000008e90
rbd_data.30dc419495cff.00000000000047a4
rbd_data.30dc419495cff.000000000000063f
............... 如下内容省略 ..........
```


删除的fast_remove.sh脚本如下：

```
root@node161:~# cat fast_remove.sh 
#!/bin/bash

process=400
objectlistfile="./delobject"
deletepool=san-pool


delete_fun()
  {
      date "+%Y-%m-%d %H:%M:%S"
      rados -p $deletepool rm $1
      #sleep 1
  }


concurrent()
 {
     start=$1 && end=$2 && cur_num=$3
     mkfifo   ./fifo.$$ &&  exec 4<> ./fifo.$$ && rm -f ./fifo.$$
     for ((i=$start; i<$cur_num+$start; i++)); do
         echo "init  start delete process $i" >&4
     done

     for((i=$start; i<=$end; i++)); do
         read -u 4
         {
             # echo -e "-- current delete: [:delete $i/$objectnum  $REPLY]"
             delob=`sed -n "${i}p" $objectlistfile`
             delete_fun $delob
             # echo "delete $delob done"  1>&4  # write to $ff_file
         } &
     done
     wait
 }

objectnum=`cat $objectlistfile | wc -l`
concurrent 1 $objectnum $process
root@node161:~#
```


### 测试结果


如下为Physical node的测试结果：

```
400 并发:
root@node161:~# time rados -p san-pool ls | grep '^rbd_data.3bba6b8b4567' | xargs -n 400  rados -p san-pool rm

real	0m55.853s
user	0m40.324s
sys	0m1.949s
root@node161:~# 


1200 并发:
root@node161:~# time rados -p san-pool ls | grep '^rbd_data.3bba6b8b4567' | xargs -n 1200  rados -p san-pool rm

real	0m53.060s
user	0m38.611s
sys	0m1.221s
root@node161:~# 
```

脚本删除结果（400并发）：

```
400 并发:
2023-04-21 17:55:16
-- current delete: [:delete 40960/40960  delete rbd_data.3bba6b8b4567.00000000000007b1 done]
2023-04-21 17:55:16
2023-04-21 17:55:16

real	1m59.236s
user	30m37.312s
sys	25m4.611s
root@node161:~#


1200 并发：

real	1m30.148s
user	24m40.103s
sys	19m49.270s
root@node161:~# 
```


尝试了VM以及Phsical Machine，多轮次测试验证，脚本删除的效果并不佳.


本文，参考：
``` https://www.cnblogs.com/zphj1987/p/13575449.html ```

