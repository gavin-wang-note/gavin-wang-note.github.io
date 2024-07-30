---
layout:     post
title:      "移除pool时提示'must unset nodelete flag'"
subtitle:   "Remove pool raise 'you must unset nodelete flag for the pool first'"
date:       2022-08-25
author:     "Gavin Wang"
catalog:    true
categories:
    - [ceph]
tags:
    - ceph
---

# 概述

UI移除pool时没有发生报错，执行ceph df时却发现有一个pool残留，没有被清理掉，但UI上已经不显示这个pool了。尝试手工删除之，发生错误，如下文所述。



# 现象

```shell
[root@node224 ~]# ceph df
GLOBAL:
    SIZE        AVAIL       RAW USED     %RAW USED 
    7.72TiB     7.39TiB       343GiB          4.34 
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS 
    .rgw.root                     1      1.09KiB         0       2.55TiB           4 
    default.rgw.control           2           0B         0       2.51TiB           8 
    default.rgw.meta              3      3.30KiB         0       2.22TiB          19 
    default.rgw.log               4           0B         0       2.58TiB         192 
    .ezs3                         5      4.52KiB         0       2.80TiB           2 
    data                          6           0B         0       2.54TiB           0 
    default.rgw.buckets.data      7       166GiB      5.84       2.61TiB     1068754 
    .ezs3.central.log             8       765KiB         0       2.69TiB         296 
    .ezs3.statistic               9      15.4MiB         0       2.91TiB         168 
    metadata                      10     12.1MiB         0       3.46TiB          26 
    default.rgw.buckets.index     11          0B         0       2.80TiB         512 
    rbd                           12         19B         0       2.58TiB           3 
    pool-vs0fs1-data              44          0B         0       3.44TiB           0 
[root@node224 ~]# ceph osd pool rm pool-vs0fs1-data pool-vs0fs1-data --yes-i-really-really-mean-it
Error EPERM: pool deletion is disabled; you must first set the mon_allow_pool_delete config option to true before you can destroy a pool
[root@node224 ~]# 
```

修改参数后：

```shell
[root@node224 ~]# ceph tell mon.* injectargs '--mon_allow_pool_delete true'
Error EINVAL: injectargs: failed to parse arguments: true
mon_allow_pool_delete = 'true' (not observed, change may require restart) 
mon.zjohe: injectargs: failed to parse arguments: true
mon_allow_pool_delete = 'true' (not observed, change may require restart) 
Error EINVAL: injectargs: failed to parse arguments: true
mon_allow_pool_delete = 'true' (not observed, change may require restart) 
mon.uzhal: injectargs: failed to parse arguments: true
mon_allow_pool_delete = 'true' (not observed, change may require restart) 
Error EINVAL: injectargs: failed to parse arguments: true
mon_allow_pool_delete = 'true' (not observed, change may require restart) 
mon.emrqu: injectargs: failed to parse arguments: true
mon_allow_pool_delete = 'true' (not observed, change may require restart) 
[root@node224 ~]# 
[root@node224 ~]# 
[root@node224 ~]# 
[root@node224 ~]# ceph osd pool rm pool-vs0fs1-data pool-vs0fs1-data --yes-i-really-really-mean-it
Error EPERM: pool deletion is disabled; you must unset nodelete flag for the pool first
[root@node224 ~]# 
```

解决方法：

```shell
[root@node224 ~]# ceph osd pool set pool-vs0fs1-data nodelete false
set pool 44 nodelete to false
[root@node224 ~]# ceph osd pool rm pool-vs0fs1-data pool-vs0fs1-data --yes-i-really-really-mean-it
pool 'pool-vs0fs1-data' removed
[root@node224 ~]# 
```
