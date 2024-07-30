---
layout:     post
title:      "perf检查ceph-osd CPU使用率高问题"
subtitle:   "perf check ceph-osd high CPU"
date:       2019-05-06
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [ceph]
tags:
    - perf
    - ceph
---



# 前言 

今天早晨 QA 发现 LAB里的一套集群环境里，124~128集群里面，128节点ceph-osd cpu load重，CPU使用率是 200%~400% 之间。

<img class="shadow" src="/img/in-post/perf-1.png" width="1200">

我用strace 粗略地看了下，没看出什么端倪。只能上perf了。


# 排查 

## perf top 

首先用perf top查看下：

<img class="shadow" src="/img/in-post/perf-2.png" width="1200">


CPU消耗大户是ceph-osd，其中用户态的operator<< 操作罪魁祸首，其中operator<<看起来是运算符重载，应该是和日志打印相关。

## perf record 

找到ceph-osd的进程ID 4966， 用如下指令采集下：

```shell
perf record -e cpu-clock -g -p 4966
```

```shell
-g 选项是告诉perf record额外记录函数的调用关系
-e cpu-clock 指perf record监控的指标为cpu周期
-p 指定需要record的进程pid
```

我们观测的对象是ceph-osd。运行10秒中左右，ctrl+C中断掉perf record:


```shell
root@converger-128:~# perf record -e cpu-clock -g -p 4966
^C[ perf record: Woken up 7 times to write data ]
[ perf record: Captured and wrote 5.058 MB perf.data (17667 samples) ]
root@converger-128:~#
```


在root目录下会产生出来 perf.data文件。

## perf report

用如下指令查看dump 出来的perf.data

```shell
perf report -i perf.data
```

输出如下：

<img class="shadow" src="/img/in-post/perf-3.png" width="1200">


我们把operator<<展开：

<img class="shadow" src="/img/in-post/perf-4.png" width="1200">

我们看到，大部分operator<<的调用是由gen_preﬁx函数产生的。

# 分析

这部分代码代码在：

```shell
osd/ReplicatedBackend.cc
------------------------------
#define dout_subsys ceph_subsys_osd
#define DOUT_PREFIX_ARGS this
#undef dout_prefix
#define dout_prefix _prefix(_dout, this)
static ostream& _prefix(std::ostream *_dout, ReplicatedBackend *pgb) {
  return *_dout << pgb->get_parent()->gen_dbg_prefix();          
}
```

原因是128集群之前有人分析ceph-osd.4，ceph.conf 里面debug osd = 0/20, 尽管不会往磁盘里面打印日志，但是因为OSD crash的时候，需要dump 级别为20 的debug log，因此，大量的osd debug log会暂存在内存的环形buﬀer 中，因此，gen_preﬁx函数被大量的调用，消耗了太多的CPU资源实时修改ceph-osd debug_osd的级别，并修改ceph.conf 永久生效，发现ceph-osd CPU使用正常。

```shell
root@converger-128:/etc/ceph# ceph daemon osd.5 config set debug_osd 0
{
    "success": ""
}
root@converger-128:/etc/ceph# ceph daemon osd.4 config set debug_osd 0
{
    "success": ""
}
```

<img class="shadow" src="/img/in-post/perf-5.png" width="1200">

# 其他 


perf工具我们产品并不自带，如果大家需要的话，需要自行编译。我们buildman上面，进入linux-kernel

```shell
jenkins@buildman-trusty:~/jobs/virtualstor_scaler_7.0/workspace/linux-kernel/tools/perf$
```

执行make，即可得到perf 可执行文件。
（当然了，之所以这么顺利，是因为我们的buildman 已经编译出了内核。）


