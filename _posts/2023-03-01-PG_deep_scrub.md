---
layout:     post
title:      "提升 PG scrub速度"
subtitle:   "Improve ceph PG scrub"
date:       2023-03-01
author:     "Gavin"
catalog:    true
tags:
    - ceph
---


# 概述

本文介绍如何提升ceph PG scrub 速度



# 提升CEPH PG scrub的速度

CEPH会定期（默认每个星期一次）对所有的PGs进行scrub，即通过检测PG中各个osds中数据是否一致来保证数据的安全。

当CEPH更换一块坏硬盘，进行数据修复后，出现了大量的PGs不能及时进行scrub，甚至有些PGs数据不一致，导致CEPH系统报警，如下所示：

```
  cluster:
    id:     8f1c1f24-59b1-11eb-aeb6-f4b78d05bf17
    health: HEALTH_ERR
            6 scrub errors
            Possible data damage: 5 pgs inconsistent
            1497 pgs not deep-scrubbed in time
            1466 pgs not scrubbed in time

  services:
    mon: 5 daemons, quorum ceph101,ceph103,ceph107,ceph109,ceph105 (age 5d)
    mgr: ceph107.gtrmmh(active, since 9d), standbys: ceph101.qpghiy
    mds: cephfs:3 {0=cephfs.ceph106.hggsge=up:active,1=cephfs.ceph104.zhkcjt=up:active,2=cephfs.ceph102.imxzno=up:active} 1 up:standby
    osd: 360 osds: 360 up (since 5d), 360 in (since 5d)

  data:
    pools:   4 pools, 10273 pgs
    objects: 331.80M objects, 560 TiB
    usage:   1.1 PiB used, 4.2 PiB / 5.2 PiB avail
    pgs:     10261 active+clean
             7     active+clean+scrubbing+deep
             5     active+clean+inconsistent

  io:
    client:   223 MiB/s rd, 38 MiB/s wr, 80 op/s rd, 12 op/s wr
```

此时，需要提高对PGs的scrub速度。默认情况下一个OSD近能同时进行一个scrub操作且仅当主机低于0.5时才进行scrub操作。我运维的CEPH系统一个PG对应10个OSDs，每个OSD仅能同时进行一个scrub操作，导致大量scrub操作需要等待，而同时进行的scrub操作数量一般为8个。因此需要在各台存储服务器上对其OSDs进行参数修改，来提高scrub速度。

osd_max_scrubs参数用于设置单个OSD同时进行的最大scrub操作数量；osd_scrub_load参数设置负载阈值。主要修改以上两个参数来提高scrub速度，其默认值为1和0.5。

例如，对ceph101主机中的所有OSDs进行参数修改：

首先，获取ceph101中所有的OSD信息：

```ceph osd dump | grep `grep ceph101 /etc/hosts | perl -ne 'print $1 if m/(\d\S*)/'` | perl -ne 'print "$1\n" if m/(osd.\d+)/' > /tmp/osd.list```

然后，对所有OSD的参数进行批量修改：

```
for i in `cat /tmp/osd.list`
do
    ceph tell $i injectargs --osd_max_scrubs=10 --osd_scrub_load_threshold=10
done
检查修改后的效果

for i in `cat /tmp/osd.list`
do
    echo $i
    ceph daemon $i config show | egrep "osd_max_scrubs|osd_scrub_load"
done
```

对所有的CEPH主机进行上述修改后，同时进行scrub的数量提高了30倍，并且使用top命令可以看到ceph-osd进程对CPU的资源消耗明显上升。


```
  cluster:
    id:     8f1c1f24-59b1-11eb-aeb6-f4b78d05bf17
    health: HEALTH_ERR
            6 scrub errors
            Possible data damage: 5 pgs inconsistent
            1285 pgs not deep-scrubbed in time
            1208 pgs not scrubbed in time
            1 slow ops, oldest one blocked for 37 sec, daemons [osd.124,osd.352] have slow ops.

  services:
    mon: 5 daemons, quorum ceph101,ceph103,ceph107,ceph109,ceph105 (age 5d)
    mgr: ceph107.gtrmmh(active, since 9d), standbys: ceph101.qpghiy
    mds: cephfs:3 {0=cephfs.ceph106.hggsge=up:active,1=cephfs.ceph104.zhkcjt=up:active,2=cephfs.ceph102.imxzno=up:active} 1 up:standby
    osd: 360 osds: 360 up (since 5d), 360 in (since 5d)

  data:
    pools:   4 pools, 10273 pgs
    objects: 331.80M objects, 560 TiB
    usage:   1.1 PiB used, 4.2 PiB / 5.2 PiB avail
    pgs:     10041 active+clean
             152   active+clean+scrubbing+deep
             75    active+clean+scrubbing
             3     active+clean+scrubbing+deep+inconsistent+repair
             2     active+clean+inconsistent

  io:
    client:   65 MiB/s rd, 4.2 MiB/s wr, 21 op/s rd, 2 op/s wr
```

此外，注意：（1）提高scrub的并行数可能对CEPH集群内网的网速要求较高，推荐使用10GE以上交换机。（2）条scrub的并行数，会导致一个OSD对应的硬盘同时并行读取的操作数量较高，当导致磁盘100%被使用时，可能磁盘的利用效率并不高，因此不推荐将 osd_max_scrubs参数调节到10以上。

对两个星期内（当前时间2022-08-03）未进行deep-scrubbed，已经有报警信息的PGs进行操作。

```
ceph pg dump | perl -e 'while (<>) { @_ = split /\s+/; $pg{$_[0]} = $1 if ($_[22] =~ m/2022-07-(\d+)/ && $1 <= 21); } foreach ( sort {$pg{$a} <=> $pg{$b}} keys %pg ) { print "ceph pg deep-scrub $_; sleep 30;\n"; }' > for_deep_scrub.list

sh for_deep_scrub.list
```

