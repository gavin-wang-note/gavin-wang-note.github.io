---
layout:     post
title:      "记一次根据epoch查找问题触发时间点"
subtitle:   "Base on epoch to find when issue occured"
date:       2022-07-11
author:     "Gavin Wang"
catalog:    true
categories:
    - [ceph]
tags:
    - ceph
---


# 概述

自动化用例执行期间，碰到crushmap中有一个Default pool，还有一个default pool，只是首字母大小写不一样，如下所示：

```shell
root@pytest-83-12:~/workspace@2/src# ceph -s
  cluster:
    id:     5d8a5c28-48e7-4f2b-bab5-fd3d1f576b12
    health: HEALTH_OK
 
  services:
    mon: 3 daemons, quorum zvdtw,sufih,rlxot
    mgr: zvdtw(active), standbys: sufih, rlxot
    mds: cephfs-3/3/3 up  {0=cephfs.1.1.1.11.10=up:active,1=cephfs.1.1.1.11.12=up:active,2=cephfs.1.1.1.11.11=up:active}, 5 up:standby
    osd: 3 osds: 3 up, 3 in
    rgw: 1 daemon active
 
  data:
    pools:   12 pools, 6144 pgs
    objects: 627 objects, 6.20MiB
    usage:   8.17GiB used, 96.7GiB / 105GiB avail
    pgs:     6144 active+clean
 
  io:
    client:   168B/s rd, 0B/s wr, 0op/s rd, 0op/s wr
 
root@pytest-83-12:~/workspace@2/src# ceph osd tree
ID  CLASS WEIGHT  TYPE NAME                  STATUS REWEIGHT PRI-AFF 
-26       0.02119 pool Default                                       
-31             0     host Default_1.1.1.11                          
-25       0.02119     host Default_1.1.1.12                          
  1   hdd 0.02119         osd.1                  up  1.00000 1.00000 
-29             0     host Default_1.1.1.13                          
 -2       0.08488 pool metadata                                      
 -7       0.03555     host metadata_1.1.1.11                         
  0   hdd 0.03555         osd.0                  up  1.00000 1.00000 
-11       0.01575     host metadata_1.1.1.12                         
  1   hdd 0.01575         osd.1                  up  1.00000 1.00000 
-15       0.03358     host metadata_1.1.1.13                         
  2   hdd 0.03358         osd.2                  up  1.00000 1.00000 
-19             0     host metadata_1.1.1.14                         
 -1       0.10237 pool default                                       
 -5       0.04059     host default_1.1.1.11                          
  0   hdd 0.04059         osd.0                  up  1.00000 1.00000 
 -9       0.02119     host default_1.1.1.12                          
  1   hdd 0.02119         osd.1                  up  1.00000 1.00000 
-13       0.04059     host default_1.1.1.13                          
  2   hdd 0.04059         osd.2                  up  1.00000 1.00000 
-17             0     host default_1.1.1.14                          
root@pytest-83-12:~/workspace@2/src# 
```

表面看，ceph集群是健康的，但UI上的一些操作会报错，报错的原因是无法从Default pool中获取到对应的osd.x中的x，即osd的index id无法获取到，进而导致UI上的涉及Pool和OSD的相关动作，都会报错。

# 问题追踪

## 如何确定问题发生的第一时间点？


先获取当前epoch，如下文所示：

```shell
root@pytest-83-12:~# ceph osd dump
epoch 716
fsid 5d8a5c28-48e7-4f2b-bab5-fd3d1f576b12
created 2022-07-09 12:52:54.101136
modified 2022-07-10 15:34:46.768843
flags sortbitwise,recovery_deletes,purged_snapdirs
crush_version 278
full_ratio 0.95
backfillfull_ratio 0.9
nearfull_ratio 0.85
require_min_compat_client jewel
min_compat_client jewel
require_osd_release luminous
pool 1 '.rgw.root' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 5 flags hashpspool stripe_width 0 application rgw
pool 2 'default.rgw.control' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 15 flags hashpspool stripe_width 0 application rgw
pool 3 '.ezs3' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 17 flags hashpspool,nodelete stripe_width 0 application internal
pool 4 'default.rgw.meta' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 17 flags hashpspool stripe_width 0 application rgw
pool 5 'default.rgw.log' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 19 flags hashpspool stripe_width 0 application rgw
pool 6 'data' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 1024 pgp_num 1024 last_change 76 flags hashpspool,nodelete stripe_width 0 application cephfs
pool 7 'default.rgw.buckets.data' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 1024 pgp_num 1024 last_change 22 flags hashpspool,nodelete stripe_width 0 application rgw
pool 8 '.ezs3.central.log' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 25 flags hashpspool,nodelete stripe_width 0 application internal
pool 9 '.ezs3.statistic' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 28 flags hashpspool,nodelete stripe_width 0 application internal
pool 10 'metadata' replicated size 2 min_size 1 crush_rule 1 object_hash rjenkins pg_num 1024 pgp_num 1024 last_change 76 flags hashpspool,nodelete stripe_width 0 application cephfs
pool 11 'default.rgw.buckets.index' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 34 flags hashpspool stripe_width 0 application rgw
pool 12 'rbd' replicated size 2 min_size 1 crush_rule 0 object_hash rjenkins pg_num 1024 pgp_num 1024 last_change 71 flags hashpspool,nodelete stripe_width 0 application rbd
max_osd 5
osd.0 up in weight 1 recovery_weight 1 up_from 706 up_thru 706 down_at 704 last_clean_interval [395,705) 1.1.1.11:6800/834186 1.1.1.11:6808/1834186 1.1.1.11:6809/1834186 1.1.1.11:6810/1834186 exists,up 89da3846-5336-4b17-8dfd-b919e4371e4c
osd.1 up in weight 1 recovery_weight 1 up_from 232 up_thru 706 down_at 227 last_clean_interval [37,229) 1.1.1.12:6801/15674 1.1.1.12:6806/1015674 1.1.1.12:6807/1015674 1.1.1.12:6808/1015674 exists,up 5933b7c5-bbd8-4e74-984b-9f6961799a5b
osd.2 up in weight 1 recovery_weight 1 up_from 403 up_thru 706 down_at 0 last_clean_interval [0,0) 1.1.1.13:6800/755654 1.1.1.13:6801/755654 1.1.1.13:6802/755654 1.1.1.13:6803/755654 exists,up d50d1d3b-ee0c-4e34-9e09-c187fc7bbec4
```

当前epoch是716


## 查询epoch=716的crush map中是否存在Default

```shell
root@pytest-83-12:/home/btadmin# i=716;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt
got osdmap epoch 716
osdmaptool: osdmap file 'osdmap.716'
osdmaptool: exported crush map to crush.716
root@pytest-83-12:/home/btadmin# cat crush.716.txt |grep Default
host Default_1.1.1.12 {
host Default_1.1.1.13 {
host Default_1.1.1.11 {
pool Default {
	item Default_1.1.1.12 weight 0.021
	item Default_1.1.1.13 weight 0.000
	item Default_1.1.1.11 weight 0.000
root@pytest-83-12:/home/btadmin# 
```

发现epoch716里含有；利用二分法，对半分，来查找：

```shell
root@pytest-83-12:/home/btadmin# i=358;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 358
osdmaptool: osdmap file 'osdmap.358'
osdmaptool: exported crush map to crush.358
host Default_1.1.1.12 {
host Default_1.1.1.13 {
host Default_1.1.1.11 {
pool Default {
	item Default_1.1.1.12 weight 0.021
	item Default_1.1.1.13 weight 0.041
	item Default_1.1.1.11 weight 0.041
root@pytest-83-12:/home/btadmin# 
```

epoch 358里也含有，继续二分法找:

```shell
root@pytest-83-12:/home/btadmin# i=179;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 179
osdmaptool: osdmap file 'osdmap.179'
osdmaptool: exported crush map to crush.179
host Default_1.1.1.12 {
host Default_1.1.1.13 {
host Default_1.1.1.11 {
pool Default {
	item Default_1.1.1.12 weight 0.021
	item Default_1.1.1.13 weight 0.041
	item Default_1.1.1.11 weight 0.041
root@pytest-83-12:/home/btadmin# 
```

```shell
root@pytest-83-12:/home/btadmin# i=89;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 89
osdmaptool: osdmap file 'osdmap.89'
osdmaptool: exported crush map to crush.89
root@pytest-83-12:/home/btadmin# systemctl restart ceph.target;systemctl restart ceph-radosgw@radosgw.0.service;systemctl restart ezrpc.service;systemctl restart httpd.service
Failed to restart httpd.service: Unit httpd.service not found.
root@pytest-83-12:/home/btadmin# 
```

发现epoch 89里并没有涵盖Default pool，说明在epoch 89~179之间的某个epoch，继续缩小范围(查找89~179的中间值，134)：

```shell
root@pytest-83-12:/home/btadmin# i=134;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 134
osdmaptool: osdmap file 'osdmap.134'
osdmaptool: exported crush map to crush.134
host Default_1.1.1.12 {
host Default_1.1.1.13 {
pool Default {
	item Default_1.1.1.12 weight 0.021
	item Default_1.1.1.13 weight 0.041
host Default_1.1.1.11 {
root@pytest-83-12:/home/btadmin# 
```

epoch 134含有，说明在epoch 89~134之间的某个epoch，继续缩小范围（取89~134的中间值111）：

```shell
root@pytest-83-12:/home/btadmin# i=111;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 111
osdmaptool: osdmap file 'osdmap.111'
osdmaptool: exported crush map to crush.111
root@pytest-83-12:/home/btadmin# 
```


epoch 111不含有，说明在epoch 111~134之间的某个epoch，继续缩小范围（取111~134的中间值122）：

```shell
root@pytest-83-12:/home/btadmin# i=122;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 122
osdmaptool: osdmap file 'osdmap.122'
osdmaptool: exported crush map to crush.122
root@pytest-83-12:/home/btadmin# 
```


epoch 122不含有，说明在epoch 122~134之间的某个epoch，继续缩小范围（取122~134的中间值128）：

```shell
root@pytest-83-12:/home/btadmin# i=128;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 128
osdmaptool: osdmap file 'osdmap.128'
osdmaptool: exported crush map to crush.128
host Default_1.1.1.12 {
root@pytest-83-12:/home/btadmin# 
```

epoch 128含有了，说明在epoch 122~128之间的某个epoch，这样范围逐步缩小了，接下来就是挨个从(122,128)之间找123~127 epoch

```shell
root@pytest-83-12:/home/btadmin# i=127;ceph osd getmap $i -o osdmap.$i;osdmaptool --export-crush crush.$i  osdmap.$i;crushtool -d crush.$i -o crush.$i.txt;cat crush.$i.txt |grep Default
got osdmap epoch 127
osdmaptool: osdmap file 'osdmap.127'
osdmaptool: exported crush map to crush.127
root@pytest-83-12:/home/btadmin# 
```

很巧，epoch 127不含，说明epoch 128是第一次出现Default pool，那就追epoch 128:

```shell
root@pytest-83-12:/var/log/ceph# zgrep -n "osd crush link" ceph.audit.log.2.gz |grep 'Default'
316910:2022-07-09 13:47:44.051329 mon.klavr mon.1 1.1.1.12:6789/0 208638 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.12"}]: dispatch
316937:2022-07-09 13:47:44.130734 mon.gfbvr mon.0 1.1.1.11:6789/0 724 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.12"}]: dispatch
317003:2022-07-09 13:47:45.108711 mon.gfbvr mon.0 1.1.1.11:6789/0 731 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.12"}]': finished
317129:2022-07-09 13:47:47.106794 mon.klavr mon.1 1.1.1.12:6789/0 208785 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.13"}]: dispatch
317140:2022-07-09 13:47:47.182459 mon.gfbvr mon.0 1.1.1.11:6789/0 755 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.13"}]: dispatch
317153:2022-07-09 13:47:47.248437 mon.gfbvr mon.0 1.1.1.11:6789/0 760 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.13"}]': finished
317338:2022-07-09 13:47:49.261214 mon.klavr mon.1 1.1.1.12:6789/0 208913 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.11"}]: dispatch
317348:2022-07-09 13:47:49.336716 mon.gfbvr mon.0 1.1.1.11:6789/0 788 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.11"}]: dispatch
317548:2022-07-09 13:47:50.338830 mon.gfbvr mon.0 1.1.1.11:6789/0 793 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.11"}]': finished
root@pytest-83-12:/var/log/ceph# 
```



```shell
root@pytest-83-12:/var/log/ceph# zgrep -n "osd crush link" ceph.audit.log.2.gz |grep '13:47:'
313387:2022-07-09 13:47:09.208853 mon.klavr mon.1 1.1.1.12:6789/0 206827 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.12"}]: dispatch
313402:2022-07-09 13:47:09.286625 mon.gfbvr mon.0 1.1.1.11:6789/0 445 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.12"}]: dispatch
313478:2022-07-09 13:47:10.259098 mon.gfbvr mon.0 1.1.1.11:6789/0 454 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.12"}]': finished
313778:2022-07-09 13:47:12.168383 mon.klavr mon.1 1.1.1.12:6789/0 206954 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.13"}]: dispatch
313787:2022-07-09 13:47:12.258398 mon.gfbvr mon.0 1.1.1.11:6789/0 474 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.13"}]: dispatch
313898:2022-07-09 13:47:13.336983 mon.gfbvr mon.0 1.1.1.11:6789/0 485 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.13"}]': finished
314138:2022-07-09 13:47:15.325649 mon.klavr mon.1 1.1.1.12:6789/0 207164 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.11"}]: dispatch
314146:2022-07-09 13:47:15.402601 mon.gfbvr mon.0 1.1.1.11:6789/0 510 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.11"}]: dispatch
314194:2022-07-09 13:47:16.406330 mon.gfbvr mon.0 1.1.1.11:6789/0 515 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=pytest-sds-pool"], "name": "pytest-sds-pool_1.1.1.11"}]': finished
316910:2022-07-09 13:47:44.051329 mon.klavr mon.1 1.1.1.12:6789/0 208638 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.12"}]: dispatch
316937:2022-07-09 13:47:44.130734 mon.gfbvr mon.0 1.1.1.11:6789/0 724 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.12"}]: dispatch
317003:2022-07-09 13:47:45.108711 mon.gfbvr mon.0 1.1.1.11:6789/0 731 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.12"}]': finished
317129:2022-07-09 13:47:47.106794 mon.klavr mon.1 1.1.1.12:6789/0 208785 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.13"}]: dispatch
317140:2022-07-09 13:47:47.182459 mon.gfbvr mon.0 1.1.1.11:6789/0 755 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.13"}]: dispatch
317153:2022-07-09 13:47:47.248437 mon.gfbvr mon.0 1.1.1.11:6789/0 760 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.13"}]': finished
317338:2022-07-09 13:47:49.261214 mon.klavr mon.1 1.1.1.12:6789/0 208913 : audit [INF] from='client.5074 1.1.1.12:0/4225613905' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.11"}]: dispatch
317348:2022-07-09 13:47:49.336716 mon.gfbvr mon.0 1.1.1.11:6789/0 788 : audit [INF] from='client.5074 -' entity='client.admin' cmd=[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.11"}]: dispatch
317548:2022-07-09 13:47:50.338830 mon.gfbvr mon.0 1.1.1.11:6789/0 793 : audit [INF] from='client.5074 -' entity='client.admin' cmd='[{"prefix": "osd crush link", "args": ["pool=Default"], "name": "Default_1.1.1.11"}]': finished
root@pytest-83-12:/var/log/ceph# 
```

这里能够看出，13:47时，有创建一个Default pool.

既然找到时间点了，找一下自动化用例，那个时刻在做什么：

```shell
2022-07-09 13:47:42 [pool.py:67  ] [ INFO] [Success]  Get all OSD success which state is UP and IN, osd_up_in is : ([0, 1, 2])
2022-07-09 13:47:42 [pool.py:169 ] [ INFO] [Action]   Assign osd : (0 1 2) into pool : (Default)
2022-07-09 13:47:42 [connectionpool.py:243 ] [DEBUG] Resetting dropped connection: localhost
```

在assign OSD into Default pool，找到这里，就找到那个时间点被执行到的用例：

```shell
2022-07-09 13:47:00 [test_01_SDS_admin_account_settings.py:46  ] [ INFO] ------------------------  Testsuite setup  ------------------------
2022-07-09 13:47:00 [test_01_SDS_admin_account_settings.py:47  ] [ INFO] [SetUp]     Class setup to create pool : (pytest-sds-pool), VS : (pytest-sds-vs)
2022-07-09 13:47:00 [virtual_storage.py:306 ] [ INFO] [Action]   Start to get all nodes information
2022-07-09 13:47:00 [connectionpool.py:243 ] [DEBUG] Resetting dropped connection: localhost
2022-07-09 13:47:00 [connectionpool.py:396 ] [DEBUG] https://localhost:8080 "GET /vs/Default/host HTTP/1.1" 200 139
.......................................... 省略 .......................................
2022-07-09 13:50:06 [bigtera_cluster.py:1422] [ INFO] [Check]    Success, ctdb health is OK
2022-07-09 13:50:06 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2022-07-09 13:50:06 [conftest.py:18  ] [ INFO] Current test case name : (test_01_test_ads_admin_login)
2022-07-09 13:50:06 [test_01_SDS_admin_account_settings.py:24  ] [ INFO] [Check]    Start to check cluster health, file name : (/root/workspace@2/src/testcase/Function_Test/case_02_Accounts/test_01_SDS_admin_account_settings.py)
2022-07-09 13:50:06 [bigtera_cluster.py:1408] [ INFO] [Check]    Check ctdb health status from file of : (/root/workspace@2/src/common/bigtera_cluster.pyc)
2022-07-09 13:50:06 [command.py:102 ] [DEBUG] command 'ctdb status | grep pnn | sed 's/(THIS NODE)//g' | awk '{print $NF}' | grep OK | wc -l' (timeout=0, force=False)
2022-07-09 13:50:06 [command.py:177 ] [DEBUG] command 'ctdb status | grep pnn | sed 's/(THIS NODE)//g' | awk '{print $NF}' | grep OK | wc -l' returns '3

```

至此找出是哪个用例的执行，触发了bug。

