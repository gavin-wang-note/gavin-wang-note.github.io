---
layout:     post
title:      "S3 单一Bucket下写4K数据性能衰减验证"
subtitle:   "Downsite of S3 4K Objects performance to one Bucket"
date:       2021-10-11
author:     "Gavin"
catalog:    true
tags:
    - performance
    - Linux
---


# 测试环境



## 测试环境信息



**存储端**

| **被测版本** | v8.2-211  (a243210)                                          |
| ------------ | ------------------------------------------------------------ |
| **节点数**   | 6 nodes，NJ Lab 技嘉4U36B设备                                |
| **CPU**      | node1~node3: Intel(R) Xeon(R) Gold 5118 CPU @ 2.30GHz <br />node4~node6:  Intel(R) Xeon(R) Silver 4114 CPU @ 2.20GHz |
| **Memory**   | 256G(16G\*16)                                                |
| **Disk**     | 希捷 SATA  8T\*36    <br />Intel S4510 SSD: 240G\*1     <br />node1~node6： 威刚ADATA SR2000CP NVMe 4T\*1     <br />node1~node3： NVMe P4500/P4600 4T*1 |
| **Network**  | QLogic  Corp. FastLinQ QL41000 Series 10/25/40/50GbE Controller \*2 Ports     <br />Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection \*2 Ports |
| **集群信息** | 2块SATA盘组RAID0，每个node 18个OSD，一块ADATA NVME SSD作为OSD Journal&Cache，加入s3-data-pool<br />node1~node3，每个node的一块P4510/4610 NVME SSD作OSD，加入s3-index-pool<br />配置S3 placement， data pool选择s3-data-pool， index pool选择s3-index-pool<br />对metadata，s3-data-pool 和 s3-data-pool 启用PG split功能，并确保PG均衡<br />UI创建S3 账号，并创建bucket<br />参数调优部分，参考下文“参数调优”章节 |



说明：

​    最初node1~node3上是两块ADATA NVME SSD，后来才和node4~node6互换SSD，对应测试章节为本文的“Lab最终测试”



**客户端**

​    6台VM，CentOS7，走10G网络向存储端的6个radosgw 发起请求。



```
[root@centos-1 ~]# hostnamectl 
   Static hostname: centos-1
         Icon name: computer-vm
           Chassis: vm
        Machine ID: b398080741c04f70b049ebe588c5ffde
           Boot ID: e114313e62ff4e6b9e4d24a711d9ed82
    Virtualization: vmware
  Operating System: CentOS Linux 7 (Core)
       CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-693.el7.x86_64
      Architecture: x86-64
```



 

**cosbench task config**

内容参考如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<workload name="5" description="1200million_4k_data_filling">
<storage type="s3" config="accesskey=YGWTYZEPDQVCPX44F6BA;secretkey=ze7bpgdY81wbHYehpzAaM2Y5RyO5rOh99YbH9NCj;endpoint=http://10.16.172.161/" />

  <workflow>
    <workstage name="1200million_4k_data_filling-init">
        <work name="1200million_4k_data_filling-init" type="init" workers="1" interval="10" division="container" runtime="0" rampup="0" rampdown="0" driver="driver1"  config="cprefix=bigtera;containers=r(1,1)" />
    </workstage>
    <workstage name="1200million_4k_data_filling-write">
        <work name="datafile-write1" type="write" workers="96" interval="10" division="object" totalOps="200000000" rampup="0" rampdown="0" driver="driver1">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=YGWTYZEPDQVCPX44F6BA;secretkey=ze7bpgdY81wbHYehpzAaM2Y5RyO5rOh99YbH9NCj;endpoint=http://10.16.172.161/" />
            <operation type="write" ratio="100" division="object" config="cprefix=bigtera;oprefix=4KB_;containers=s(1,1);objects=r(1,200000000);sizes=c(4)KB;createContainer=false;" id="none" />
        </work>
        <work name="datafile-write2" type="write" workers="96" interval="10" division="object" totalOps="200000000" rampup="0" rampdown="0" driver="driver2">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=YGWTYZEPDQVCPX44F6BA;secretkey=ze7bpgdY81wbHYehpzAaM2Y5RyO5rOh99YbH9NCj;endpoint=http://10.16.172.162/" />
            <operation type="write" ratio="100" division="object" config="cprefix=bigtera;oprefix=4KB_;containers=s(1,1);objects=r(200000001,400000000);sizes=c(4)KB;createContainer=false;" id="none" />
        </work>
        <work name="datafile-write3" type="write" workers="96" interval="10" division="object" totalOps="200000000" rampup="0" rampdown="0" driver="driver3">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=YGWTYZEPDQVCPX44F6BA;secretkey=ze7bpgdY81wbHYehpzAaM2Y5RyO5rOh99YbH9NCj;endpoint=http://10.16.172.163/" />
            <operation type="write" ratio="100" division="object" config="cprefix=bigtera;oprefix=4KB_;containers=s(1,1);objects=r(400000001,600000000);sizes=c(4)KB;createContainer=false;" id="none" />
        </work>
        <work name="datafile-write3" type="write" workers="96" interval="10" division="object" totalOps="200000000" rampup="0" rampdown="0" driver="driver4">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=YGWTYZEPDQVCPX44F6BA;secretkey=ze7bpgdY81wbHYehpzAaM2Y5RyO5rOh99YbH9NCj;endpoint=http://10.16.172.164/" />
            <operation type="write" ratio="100" division="object" config="cprefix=bigtera;oprefix=4KB_;containers=s(1,1);objects=r(600000001,800000000);sizes=c(4)KB;createContainer=false;" id="none" />
        </work>
        <work name="datafile-write3" type="write" workers="96" interval="10" division="object" totalOps="200000000" rampup="0" rampdown="0" driver="driver5">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=YGWTYZEPDQVCPX44F6BA;secretkey=ze7bpgdY81wbHYehpzAaM2Y5RyO5rOh99YbH9NCj;endpoint=http://10.16.172.165/" />
            <operation type="write" ratio="100" division="object" config="cprefix=bigtera;oprefix=4KB_;containers=s(1,1);objects=r(800000001,1000000000);sizes=c(4)KB;createContainer=false;" id="none" />
        </work>
        <work name="datafile-write3" type="write" workers="96" interval="10" division="object" totalOps="200000000" rampup="0" rampdown="0" driver="driver6">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=YGWTYZEPDQVCPX44F6BA;secretkey=ze7bpgdY81wbHYehpzAaM2Y5RyO5rOh99YbH9NCj;endpoint=http://10.16.172.166/" />
            <operation type="write" ratio="100" division="object" config="cprefix=bigtera;oprefix=4KB_;containers=s(1,1);objects=r(1000000001,1200000000);sizes=c(4)KB;createContainer=false;" id="none" />
        </work>
    </workstage>
    </workflow>

</workload>
```



## 参数调优

 

 

### 修改bucket shards，默认128，改成1000

```
radosgw-admin bucket reshard --bucket=bigtera1 --num-shards=1000
```

 说明：

​      此操作，请务必放在修改了s3 placement，并创建好bucket后再执行。



### 调整rgw相关参数

 

```
rgw ecsoc bundle shards = 512
rgw gc max objs = 32
rgw gc obj min wait = 300
rgw gc processor max_time = 300
rgw gc processor period = 300
rgw init timeout = 3000
```

 

### 调整bigterastore cache

默认100万，调整成1000万，尽量避免bigterastore flush cache

```
be_cache_max_objs = 10000000
```

 

说明：

​    建议写入每个node的ceph.conf [osd]处；

​    本文 EC 4+2 灌12亿对象场景，不调整此参数。





### 避免inode耗尽

```
ceph tell osd.* injectargs '--bigterastore_obj_meta_size 1024'
```

 建议写入每个node的ceph.conf [osd]处。

 

### PG相关

 metadata pool 启用PG split，避免OSD数量过多（默认512 PG数太少）和 bucket中objects数量较多情况下出现osd metaata pool full，引发性能衰减；

s3-data-pool启用PG split；

确保metadata pool 和 s3-data-pool的PG分布是均衡的。

 

说明：

以本次测试环境为例，虽然产品有deamon /usr/local/bin/bt-pool-reweight-agent.py 来做reweight PG，但整个执行周期有些慢，迟迟没有调整好，所以手工干预了一下，操作步骤大致如下：

（1）   ceph df 获取要调整的pool id  # 主要是3个pool，一个是metadata pool，一个是s3 data pool 和s3 index pool

（2）   获取pool预期OSD PG分布crush信息 # 以metadata pool id=10为示例：

 

```
crush_reweight_tool -p 10 -o 10_crush.bin -t 1
ceph osd setcrushmap -i 10_crush.bin
```

 

上面是理想状态，-t 1表示每个OSD上分布的PG相差1，比如计算出来的每个OSD 分布的PG数平均值为150，预计调整后的状态是：有的OSD 分布的PG数是151，有的是150，有的是152；

如果-t 1中无法达到预期调整效果，特别是在现有PG分布非常不均衡状态下，放大这个数值，先从差值较大来做调整，然后缩小范围，示例如下：

```
crush_reweight_tool -p 10 -o 10_crush.bin -t 30；
ceph osd setcrushmap -i 10_crush.bin
```

apply下去后：

```
crush_reweight_tool -p 10 -o 10_crush.bin -t 10；
ceph osd setcrushmap -i 10_crush.bin
```

 

然后

```
crush_reweight_tool -p 10 -o 10_crush.bin -t 4；
ceph osd setcrushmap -i 10_crush.bin

crush_reweight_tool -p 10 -o 10_crush.bin -t 2；
ceph osd setcrushmap -i 10_crush.bin

crush_reweight_tool -p 10 -o 10_crush.bin -t 1；
ceph osd setcrushmap -i 10_crush.bin
```

 

类似上面的操作，如果-t 1达不到预计效果，终止调整。



3个Pool的PG调整好后，检查一下PG分布，确保没有问题，具体检查方法，请执行附件提供的脚本：pg_allocate.py，输出参考如下：

```
root@node166:~# ./pg_allocate.py 
dumped all

pool  : 1      10     11     12     13     2      3      4      5      6      7      8      9      | SUM
--------------------------------------------------------------------------------------------------------------

osd.0   5      153    115    2      0      2      7      3      3      21     18     8      3      | 340   
osd.1   5      153    115    8      0      4      4      5      5      26     14     7      2      | 348   
osd.2   5      153    113    5      0      3      2      4      5      27     17     6      3      | 343   
osd.3   3      153    113    5      0      3      8      8      5      13     34     5      3      | 353   
osd.4   3      152    114    4      0      1      12     6      7      19     16     6      5      | 345   
osd.5   5      152    115    5      0      2      6      4      2      20     22     3      9      | 345   
osd.6   4      150    115    4      0      2      5      5      3      23     27     5      6      | 349   
osd.7   5      152    113    4      0      3      11     8      7      22     13     7      5      | 350   
osd.8   1      151    114    1      0      4      5      2      7      17     27     1      6      | 336   
osd.9   3      152    115    1      0      7      5      6      5      12     16     2      4      | 328   
osd.10  4      150    113    6      0      4      4      5      3      17     12     7      6      | 331   
osd.11  4      150    115    3      0      5      2      4      9      22     15     0      4      | 333   
osd.12  2      153    114    5      0      6      8      4      6      18     20     3      3      | 342   
osd.13  6      151    115    4      0      7      4      5      5      18     26     8      6      | 355   
osd.14  7      153    113    4      0      3      2      7      2      19     14     9      6      | 339   
osd.15  6      152    114    2      0      7      5      4      6      20     16     11     6      | 349   
osd.16  7      151    113    5      0      3      1      5      3      16     15     4      7      | 330   
osd.17  2      152    113    13     0      7      8      9      3      21     17     4      3      | 352   
osd.18  6      151    112    6      0      4      4      3      3      25     22     2      3      | 341   
osd.19  6      152    113    2      0      3      9      4      5      21     11     1      4      | 331   
osd.20  3      152    112    7      0      7      5      6      5      18     21     5      3      | 344   
osd.21  4      150    114    3      0      5      1      5      3      18     14     4      5      | 326   
osd.22  7      150    114    3      0      5      9      7      3      14     18     4      7      | 341   
osd.23  9      152    115    9      0      4      5      2      6      17     7      5      3      | 334   
osd.24  6      152    114    6      0      4      5      4      2      17     16     6      4      | 336   
osd.25  3      150    112    5      0      4      5      0      6      18     13     5      6      | 327   
osd.26  3      153    113    5      0      3      5      4      4      20     31     3      6      | 350   
osd.27  6      150    113    4      0      4      8      5      6      19     22     3      10     | 350   
osd.28  1      153    113    0      0      4      4      2      3      11     14     7      5      | 317   
osd.29  7      153    113    9      0      7      4      3      3      34     19     5      4      | 361   
osd.30  3      151    114    10     0      7      5      5      2      11     35     4      10     | 357   
osd.31  3      150    115    1      0      5      7      9      2      17     17     5      3      | 334   
osd.32  2      152    114    2      0      5      4      5      4      19     18     7      5      | 337   
osd.33  6      151    115    6      0      7      7      7      2      12     19     3      4      | 339   
osd.34  4      152    115    7      0      8      3      3      7      25     15     3      6      | 348   
osd.35  5      152    112    4      0      6      4      4      8      20     21     2      5      | 343   
osd.36  7      153    115    3      0      4      6      2      4      18     21     7      3      | 343   
osd.37  1      152    114    3      0      1      7      2      5      18     23     3      5      | 334   
osd.38  6      153    115    9      0      2      5      6      2      14     13     4      2      | 331   
osd.39  4      151    114    6      0      6      6      2      6      24     22     2      5      | 348   
osd.40  3      152    115    3      0      4      7      7      6      18     15     4      4      | 338   
osd.41  4      152    114    4      0      3      3      4      4      24     23     4      4      | 343   
osd.42  1      152    113    6      0      4      4      7      4      16     16     6      2      | 331   
osd.43  5      151    115    5      0      7      3      2      2      14     23     5      3      | 335   
osd.44  5      152    112    7      0      3      3      5      11     17     26     8      4      | 353   
osd.45  5      153    115    7      0      5      1      7      7      22     18     5      5      | 350   
osd.46  5      151    114    6      0      2      7      5      8      16     20     4      6      | 344   
osd.47  4      153    114    6      0      6      2      9      3      21     19     2      9      | 348   
osd.48  8      151    114    1      0      4      2      4      5      17     19     1      7      | 333   
osd.49  5      152    114    4      0      4      4      4      4      22     18     2      4      | 337   
osd.50  8      153    115    4      0      6      5      4      1      20     19     4      1      | 340   
osd.51  5      153    115    5      0      4      4      7      6      15     15     3      8      | 340   
osd.52  9      152    114    4      0      4      2      2      6      12     18     6      3      | 332   
osd.53  5      153    113    7      0      5      4      6      1      28     21     3      8      | 354   
osd.54  3      151    114    8      0      5      8      7      7      13     14     3      5      | 338   
osd.55  8      152    113    9      0      2      5      5      4      20     24     12     1      | 355   
osd.56  7      153    113    1      0      3      6      1      7      23     26     6      1      | 347   
osd.57  8      151    115    5      0      6      1      10     10     23     26     5      4      | 364   
osd.58  7      153    113    3      0      5      5      4      3      15     22     6      7      | 343   
osd.59  4      150    115    7      0      5      3      5      10     17     11     5      6      | 338   
osd.60  4      152    115    7      0      6      4      1      2      16     10     2      5      | 324   
osd.61  5      152    113    4      0      7      3      1      8      22     21     8      4      | 348   
osd.62  8      150    113    2      0      4      1      5      2      11     21     4      9      | 330   
osd.63  4      150    113    5      0      1      5      7      5      27     21     3      3      | 344   
osd.64  4      151    115    5      0      6      6      5      7      14     25     5      9      | 352   
osd.65  5      150    113    3      0      7      6      5      3      18     18     6      6      | 340   
osd.66  5      151    112    6      0      4      3      4      4      17     20     3      4      | 333   
osd.67  4      153    113    8      0      7      2      7      3      19     13     5      3      | 337   
osd.68  7      153    115    3      0      6      3      5      0      14     12     2      5      | 325   
osd.69  5      151    114    3      0      8      3      5      3      16     21     3      5      | 337   
osd.70  5      152    113    7      0      3      4      8      5      24     16     2      6      | 345   
osd.71  3      151    112    2      0      8      6      3      7      18     22     5      5      | 342   
osd.72  8      151    112    7      0      4      5      5      5      13     18     8      6      | 342   
osd.73  4      151    114    2      0      13     6      6      3      23     18     5      2      | 347   
osd.74  3      153    114    7      0      3      1      3      6      24     11     6      3      | 334   
osd.75  3      150    115    1      0      9      5      6      4      19     21     1      7      | 341   
osd.76  5      153    115    4      0      5      6      5      3      26     21     4      3      | 350   
osd.77  2      153    114    5      0      12     4      4      7      22     23     4      3      | 353   
osd.78  5      153    114    4      0      2      8      5      5      26     22     7      5      | 356   
osd.79  2      152    113    5      0      5      3      2      5      22     23     9      4      | 345   
osd.80  7      150    113    7      0      5      3      4      2      23     17     3      2      | 336   
osd.81  3      152    114    2      0      4      4      4      4      24     13     4      4      | 332   
osd.82  5      151    112    5      0      6      1      7      7      24     26     4      8      | 356   
osd.83  5      151    112    2      0      7      5      6      6      24     24     5      6      | 353   
osd.84  1      153    114    6      0      4      6      2      4      13     9      9      3      | 324   
osd.85  5      151    112    4      0      4      8      8      6      11     10     7      4      | 330   
osd.86  7      150    112    8      0      4      5      4      2      19     22     4      4      | 341   
osd.87  5      152    115    4      0      5      4      5      3      15     18     7      9      | 342   
osd.88  3      150    112    2      0      4      3      7      4      15     21     1      4      | 326   
osd.89  6      151    114    4      0      7      5      3      4      23     22     4      2      | 345   
osd.90  1      151    114    1      0      0      4      3      3      22     22     8      4      | 333   
osd.91  3      150    115    8      0      3      6      7      3      16     19     5      6      | 341   
osd.92  6      152    115    3      0      4      2      3      5      24     20     4      4      | 342   
osd.93  4      153    114    5      0      6      2      6      8      18     15     5      4      | 340   
osd.94  8      153    115    8      0      3      6      5      4      15     14     6      2      | 339   
osd.95  7      152    114    3      0      4      5      7      6      23     25     2      3      | 351   
osd.96  3      150    115    2      0      4      6      8      7      24     20     5      7      | 351   
osd.97  10     150    115    2      0      3      7      5      5      12     15     5      8      | 337   
osd.98  4      153    115    5      0      5      8      4      6      20     14     5      4      | 343   
osd.99  6      152    115    6      0      2      5      7      2      18     19     4      4      | 340   
osd.100 3      151    113    5      0      8      8      5      6      18     17     5      4      | 343   
osd.101 5      152    113    7      0      3      2      2      9      14     27     11     6      | 351   
osd.102 6      152    113    2      0      2      4      4      4      14     17     5      7      | 330   
osd.103 1      152    112    8      0      6      2      2      3      16     19     6      4      | 331   
osd.104 6      153    113    1      0      2      5      5      8      21     18     3      4      | 339   
osd.105 3      153    113    6      0      7      5      0      5      22     23     5      4      | 346   
osd.106 7      152    115    6      0      3      8      6      6      13     18     2      4      | 340   
osd.107 3      152    114    7      0      12     3      2      7      22     23     6      3      | 354   
osd.108 0      0      0      0      171    0      0      0      0      0      0      0      0      | 171   
osd.109 0      0      0      0      170    0      0      0      0      0      0      0      0      | 170   
osd.110 0      0      0      0      171    0      0      0      0      0      0      0      0      | 171   

--------------------------------------------------------------------------------------------------------------

SUM   : 512    16384  12288  512    512    512    512    512    512    2048   2048   512    512    |
root@node166:~# 
```

 



 

 ## 可行性验证



### EC 4+2， 2盘组RAID0

2021-09-09

01:52集群异常，是因为忘记调整obj meta size，导致默认值情况下计算的inode耗尽，如下图所示：

<img class="shadow" src="/img/in-post/clip_image001-16316766830863.png" width="600" />

 

当时数据已经写了3.2亿左右，没有截图，早上上班时候，发现此问题，调整了参数，继续灌数据：

<img class="shadow" src="/img/in-post/clip_image002-16316766830874.png" width="600" />

 

从上面图可以看出来，凌晨2点48前后，集群没有流量了：

 
<img class="shadow" src="/img/in-post/clip_image003-16316766829691.png" width="600" />
 

出现了Near full 和backfillfull，此时还是可以继续写入的，只是接着出现了FULL，97%了，导致数据无法写入：

<img class="shadow" src="/img/in-post/clip_image004-16316766829702.png" width="600" />
 

 

早上到Office后，调整了参数，让数据继续灌，不打算终止重新跑，因为只要此刻开始，后面只要写入的数据是平稳的，没有衰减，目的就达到了，持续观察中（下面是灌了4.98亿对象时看到的状况截图）：

<img class="shadow" src="/img/in-post/clip_image005.png" width="600" />

<img class="shadow" src="/img/in-post/clip_image006.png" width="600" />

<img class="shadow" src="/img/in-post/clip_image007.png" width="600" />

<img class="shadow" src="/img/in-post/clip_image008.png" width="600" />

 

后面3个节点，相较前3个节点， NVME SSD比较弱了。

 
 

重做集群（2021-09-11）：


<img class="shadow" src="/img/in-post/clip_image009.png" width="600" />
 

 

写了5.7亿，pool出现 near full，衰减的厉害。

<img class="shadow" src="/img/in-post/clip_image010.png" width="600" />

 

### EC 4+2 2盘RAID0, 但每个node使用10组RAID做OSD

 

2021-09-12

<img class="shadow" src="/img/in-post/clip_image011.png" width="600" />

<img class="shadow" src="/img/in-post/clip_image012.png" width="600" />

 

出现OSD near full，之后写性能下降。

 

### 6盘组RAID0，每个node 6个OSD


2021-09-13

前3个node，用一块 Nvme 做ssd osd pool

 
<img class="shadow" src="/img/in-post/clip_image013.png" width="600" />

<img class="shadow" src="/img/in-post/clip_image014.png" width="600" />

 

还是出现了metadata pool full，与osd full的问题

 

 

2021-09-14 

考虑到上面没有多metadata pool做PG split，PG数量太少，objects数量太多，有可能引发osd metadata near full问题，导致性能下降。

重做环境，继续观察。







# Lab 继续后续测试



## 场景1 Enable Rack Awareness， EC 2+1，空桶状况下上传7.2亿4K小对象

 

### 存储端信息

 灌的object量：

<img class="shadow" src="/img/in-post/image-20210915120446571.png" width="600" />



集群统计信息：

<img class="shadow" src="/img/in-post/image-20210915115732869.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210915120241981.png" width="600" />


### cosbench端统计信息


<img class="shadow" src="/img/in-post/image-20210915120102542.png" width="600" />


<img class="shadow" src="/img/in-post/image-20210915120139930.png" width="600" />


 

### 性能瓶颈

如下为node4~node6的NVME atop信息片断，这3个节点NVME SSD要表node1~node3的NVME SSD弱一个档次。

 

#### node 166

<img class="shadow" src="/img/in-post/clip_image015.png" width="600" />
<img class="shadow" src="/img/in-post/clip_image016.png" width="600" />
<img class="shadow" src="/img/in-post/clip_image017.png" width="600" />

 

#### node 165

 
<img class="shadow" src="/img/in-post/clip_image018.png" width="600" />
<img class="shadow" src="/img/in-post/clip_image019.png" width="600" />

 

#### node 164

 
<img class="shadow" src="/img/in-post/clip_image020.png" width="600" />

 

###  疑问

 

整个过程中没有看到HDD忙，考虑到NVME SSD空间比较大，而且调整过bigterastore object cache size为1000万，总共是108个HDD OSD和 3 个NVME OSD，SSD 能够容纳的对象数是11亿左右(1000万*111个OSD)，上面总共灌了7.2亿对象，这些对象在SSD里，所以没有看到衰减迹象。

下个场景，改变一下测试策略，不再调整object cache size，使用默认值（100万）。

 

 

## 场景2 EC 4+2，空桶状况下上传12亿4k小对象

 

 使用默认的be cache max objs参数，灌12亿对象到单一bucket中，但灌到8亿的时候出现osd near full，再继续灌下去，出现osd full，然后性能开始下降了，所以先记录数据，终止测试，下一轮次依然是12亿的目标，但会将metadata pool 和s3 data pool的PG数放大验证看看。


 

###  统计信息

 

#### 存储UI端

<img class="shadow" src="/img/in-post/image-20210916194250670.png" width="600" />


#### 存储后端


<img class="shadow" src="/img/in-post/image-20210916194313663.png" width="600" />



#### cosbench 统计


<img class="shadow" src="/img/in-post/image-20210916194358253.png" width="600" />


<img class="shadow" src="/img/in-post/image-20210916194428439.png" width="600" />



### 硬件资源开销



如果是在灌了5.4+亿对象后截屏信息


<img class="shadow" src="/img/in-post/image-20210916091341852.png" width="600" />



#### atop信息



node161

<img class="shadow" src="/img/in-post/image-20210916091729055.png" width="600" />



node162

<img class="shadow" src="/img/in-post/image-20210916091738876.png" width="600" />



node163

<img class="shadow" src="/img/in-post/image-20210916091749509.png" width="600" />

node164

<img class="shadow" src="/img/in-post/image-20210916091759035.png" width="600" />



node165

<img class="shadow" src="/img/in-post/image-20210916091809408.png" width="600" />



node166

<img class="shadow" src="/img/in-post/image-20210916091824733.png" width="600" />




#### iostat信息

node161

<img class="shadow" src="/img/in-post/image-20210916091114070.png" width="600" />

 

node162


<img class="shadow" src="/img/in-post/image-20210916091512154.png" width="600" />



node163

<img class="shadow" src="/img/in-post/image-20210916091522315.png" width="600" />





node164


<img class="shadow" src="/img/in-post/image-20210916091545140.png" width="600" />



node165

<img class="shadow" src="/img/in-post/image-20210916091555478.png" width="600" />



node166

<img class="shadow" src="/img/in-post/image-20210916091604747.png" width="600" />





注意点：

在灌了7.6亿对象情况下，发现部分osd的metadata usage 接近near full阈值（0.85），下图是设置bigterastore_obj_meta_size=1024下看到的信息：

<img class="shadow" src="/img/in-post/image-20210916172730569.png" width="600" />



现在调整bigterastore_obj_meta_size=512，执行上面的脚本获取osd的metadata usage并没有发生变化。











### 再次测试

2021-09-16

放大metadata 和 s3-data-pool的PG numbers

{% raw %}```
root@node166:~# ceph osd pool get s3-data-pool pg_num
pg_num: 2048
root@node166:~# ceph osd pool get metadata pg_num
pg_num: 8192
``` {% endraw %}



{% raw %}```
root@node166:~# cat enlarge_pg.sh 
# pool_name='s3-data-pool'
pool_name='metadata'
cur_pg_num=`ceph osd pool get ${pool_name} pg_num |awk -F ':' '{{print $NF}}'`
target_pg_num=`expr ${cur_pg_num} \* 3`

for i in {1..256}; do
    cur_pg_num=`ceph osd pool get ${pool_name} pg_num |awk -F ':' '{{print $NF}}'`
    new_pg_num=`expr ${cur_pg_num} + 128`
    ceph osd pool set ${pool_name} pg_num ${new_pg_num}
    ceph osd pool set ${pool_name} pgp_num ${new_pg_num}
    sleep 0.2
    if [[ ${new_pg_num} -eq ${target_pg_num} ]]; then
        break
    fi
done
root@node166:~# 
``` {% endraw %}





当灌到4.4亿的时候，查看了各个osd的matedata usage，发现前3个node与后3个node的用量还是有蛮大差距：


<img class="shadow" src="/img/in-post/image-20210917163813310-16318678940801.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210917163853593.png" width="600" />



```
root@node163:~# ceph daemon osd.48 perf dump bigterastore
{
    "bigterastore": {
        "bt_js_coll_num": 877,
        "bt_js_obj_num": 280268,
        "bt_js_attrs_bytes": 154207729,
        "bt_js_attrs_num": 1610103,
        "bt_js_attrs_rm_num": 0,
        "bt_js_omap_bytes": 5580884,
        "bt_js_omap_num": 92452,
        "bt_js_omap_rm_num": 90618,
        "bt_bc_coll_num": 877,
        "bt_bc_obj_num": 1573011,
        "bt_bc_dirty_obj_num": 1572988,
       "bt_bc_obj_reads": 53,
        "bt_bc_obj_writes": 64191,
        "bt_bc_obj_read_miss": 22,
        "bt_bc_dirty_size": 37119551,
        "bt_bj_transaction_wait_buf": 0,
        "bt_bj_transaction_wait_aio": 0,
        "bt_bj_transaction_in_flight": 0,
        "bt_bj_flusher_s_dispt": 0,
        "bt_bj_flusher_o_dispt": 0,
        "bt_bj_flusher_segments": 0,
        "bt_bj_flusher_objs": 0,
        "bt_bj_segment_head": 2,
        "bt_bj_segment_flushed": 15,
        "bt_bj_segment
        }
}

root@node164:~# ceph daemon osd.56 perf dump bigterastore
{
    "bigterastore": {
        "bt_js_coll_num": 867,
        "bt_js_obj_num": 250467,
        "bt_js_attrs_bytes": 119715269,
        "bt_js_attrs_num": 1249755,
        "bt_js_attrs_rm_num": 0,
        "bt_js_omap_bytes": 4524222,
        "bt_js_omap_num": 74818,
        "bt_js_omap_rm_num": 73086,
        "bt_bc_coll_num": 867,
        "bt_bc_obj_num": 7830607,
        "bt_bc_dirty_obj_num": 7830443,
        "bt_bc_obj_reads": 15,
        "bt_bc_obj_writes": 70003,
        "bt_bc_obj_read_miss": 2,
        "bt_bc_dirty_size": 81089512,
        "bt_bj_transaction_wait_buf": 0,
        "bt_bj_transaction_wait_aio": 0,
        "bt_bj_transaction_in_flight": 37,
        "bt_bj_flusher_s_dispt": 0,
        "bt_bj_flusher_o_dispt": 0,
        "bt_bj_flusher_segments": 0,
        "bt_bj_flusher_objs": 0,
        "bt_bj_segment_head": 12,
        "bt_bj_segment_flushed": 9,
        "bt_bj_segment_trimmed": 6
    }
}
```





Big帮忙确认了一下：

   前3个node的nvme性能比较强悍，object flush&evict比较快，所以HDD的空间消耗也明显比后面3个节点多，前3个node cache object也少于后面的3台，建议各个node统一下NVME SSD。









## Lab最终测试

2021-09-17

说明：

​       如下场景的测试，各个node均有一块ADATA NVME SSD，确保各个node Bigterastore Cache FS inode 均衡，不会因NVME SSD性能不同造成flush/evict不同，引发各个node的Bigterastore Cache FS inode消耗不均衡。



### 一倍放大PG数

每个node使用相同的NVME SSD(ADATA)做OSD的Journal&Cache;

即将原来node161~163上的一块ADATA NVME SSD替换到node164~166上，确保node161~166 6个node都有一块ADATA NVME SSD；

将node164~166上的P4510/4610 NVME SSD，给node161~163使用，做nvme ssd pool as s3 index pool，因为这3个node的CPU更强悍。

虽然Big说不再放大PG数，考虑到对象数据较大，本次测试还是放大了一倍看看效果如何，metadata pool 、s3-data-pool和 s3-index-pool均有放大一倍：


<img class="shadow" src="/img/in-post/image-20210917180327779.png" width="600" />

说明：

​    32768为2副本的metadata pool；

​    24576为4+2EC s3-data-pool；

​    1024为2副本s3-index-pool





整个测试期间，瓶颈在NVME(不是S3 index pool对应的 NVME SSD):



node161

<img class="shadow" src="/img/in-post/image-20210918093146977.png" width="600" />




node162

<img class="shadow" src="/img/in-post/image-20210918092754619.png" width="600" />



node163

<img class="shadow" src="/img/in-post/image-20210918093206742.png" width="600" />




node164

<img class="shadow" src="/img/in-post/image-20210918093216922.png" width="600" />




node165

<img class="shadow" src="/img/in-post/image-20210918093230042.png" width="600" />



node166

<img class="shadow" src="/img/in-post/image-20210918093239165-16319287600391.png" width="600" />





2021-09-18

写了6.2个亿对象

<img class="shadow" src="/img/in-post/image-20210918172307957.png" width="600" />

此时UI统计信息：

<img class="shadow" src="/img/in-post/image-20210918172246927.png" width="600" />





这里有波动，基本上一个小时出现一次，推测是flush/evict造成，尚未找到具体证据。



2021-09-19



<img class="shadow" src="/img/in-post/image-20210919071321059.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919071510301.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919071335003.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919071413716.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919071413716.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919071529108.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919074457366.png" width="600" />

至此之后，性能直线衰减。



停掉cosbench task，此后各个node持续flush/evict object到HDD：

<img class="shadow" src="/img/in-post/image-20210919072945984.png" width="600" />


cosbench停掉10余个小时后：

<img class="shadow" src="/img/in-post/image-20210919212209412.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919212310757.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919212355948.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919212405803.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919212419913.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919212430537.png" width="600" />




各个node 的cache inode消耗：

<img class="shadow" src="/img/in-post/image-20210919073449099.png" width="600" />

各个节点HDD inode消耗：

<img class="shadow" src="/img/in-post/image-20210919074234373.png" width="600" />




说明flush/evich比较慢，停掉cosbench task 大约7个小时候，各个node的osd与cache inode消耗情况如下：

<img class="shadow" src="/img/in-post/image-20210919160536018.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919160704064.png" width="600" />



从这个角度讲，存储能写多少4k的小object，取决于2方面：

1. 产品默认支持计算出来的inode是否能够满足实际需要；

2. ssd flush/evict是否足够快，HDD能够支撑住如此快的flush/evict



考虑到我验证的场景是验证不会随着bucket中对象数的增多而出现衰减，所以考虑重新测试，降低cosbench写速度，避免因写的太快而flush/evict太慢造成osd cache inode提早耗尽出现性能断崖式衰减。







继续在灌了10亿基础上，等待cache inode消耗减低至0.5以下后，写3亿4K小对象，观察有10亿基础数据情况下，这3亿对象写期间性能是否会衰减



<img class="shadow" src="/img/in-post/image-20210919224911546.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210919224922984.png" width="600" />




期间node164 因memory 耗尽出现osd down，始终无法恢复，重启机器与只启用部分osd（18个osd启用15个），无法恢复；第三次重启机器后，只启用了一半的osd，且等待cache inode 消耗降低到1%情况下：

<img class="shadow" src="/img/in-post/image-20210922120820942.png" width="600" />

然后逐步启用余下的osd：

<img class="shadow" src="/img/in-post/image-20210922144652265.png" width="600" />



但osd pg log占用太多memory，只能等PG状态全部是active+clean情况下，才会释放多余的pg log所占用的memory：

<img class="shadow" src="/img/in-post/image-20210922183619848.png" width="600" />



最终还是没法启动所有的osd，只能停用node164上的部分osd，在PG处于如下状态，灌1亿4Kobjects：

<img class="shadow" src="/img/in-post/image-20210923092445769.png" width="600" />





期间NVME 与 HDD 都非常忙，重点是NVME，有做Bigterastore cache，新写入的数据会先到Cache里：

<img class="shadow" src="/img/in-post/image-20210923092826977.png" width="600" />




调整过be_cache_paused_flusher_qsize到32（默认1），cosbench展示的各个driver的OPS波动比较大了，之后又恢复默认值：

<img class="shadow" src="/img/in-post/image-20210923104645353.png" width="600" />


之后碰到cache写满导致osd crash

<img class="shadow" src="/img/in-post/image-20210923120045816.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210923120106531.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210923120134914.png" width="600" />


集群测统计信息：

<img class="shadow" src="/img/in-post/image-20210923120004636.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210923120013254.png" width="600" />


cosbench统计信息：



<img class="shadow" src="/img/in-post/image-20210923120217426.png" width="600" />



各个node的inode消耗情况：

<img class="shadow" src="/img/in-post/image-20210923125119637.png" width="600" />


说明：

   node164 有部分osd down，因memory不足无法启动起来，后来停用了这个node上的一批osd，所以会存在部分cache FS inode消耗明显高很多的状况。



结论：

​    从UI统计折线图看，无需手工放大PG数，产品Enable PG Split所分裂出来的PG数更优异。



#### 使用启用PG Split功能后的PG数，灌4K 1200Million 对象，降低cosbench写速度



```
root@node166:~# ./pg_allocate.py 
dumped all

pool  : 1      10     12     13     14     2      3      4      5      6      7      8      9      | SUM
--------------------------------------------------------------------------------------------------------------
osd.0   8      152    5      113    0      2      5      6      4      17     21     8      5      | 346   
osd.1   4      151    7      112    0      4      4      5      5      17     16     4      2      | 331   
osd.2   5      153    6      112    0      4      2      6      8      23     19     3      4      | 345   
osd.3   2      153    7      113    0      2      6      7      5      15     21     4      6      | 341   
osd.4   4      151    1      114    0      5      9      5      4      13     19     7      2      | 334   
osd.5   4      153    4      115    0      3      8      3      3      16     21     3      3      | 336   
osd.6   7      152    3      115    0      1      3      4      3      21     25     6      3      | 343   
osd.7   7      153    6      115    0      5      4      6      4      23     19     8      4      | 354   
osd.8   3      152    3      112    0      1      5      4      6      13     23     2      5      | 329   
osd.9   6      150    1      114    0      6      3      4      4      25     14     3      3      | 333   
osd.10  6      152    4      113    0      2      3      5      0      21     11     8      2      | 327   
osd.11  3      150    3      114    0      9      5      4      7      22     16     2      5      | 340   
osd.12  4      152    6      115    0      7      8      4      3      18     23     4      4      | 348   
osd.13  4      153    2      113    0      7      6      4      5      22     17     9      6      | 348   
osd.14  6      151    9      115    0      3      8      6      1      22     21     9      2      | 353   
osd.15  7      151    1      114    0      4      3      8      5      18     21     5      10     | 347   
osd.16  4      153    8      115    0      7      2      9      5      14     12     6      8      | 343   
osd.17  4      151    6      114    0      6      8      5      5      14     23     6      7      | 349   
osd.18  7      150    6      112    0      3      7      4      2      23     21     1      5      | 341   
osd.19  5      153    6      114    0      4      5      8      8      17     16     6      4      | 346   
osd.20  1      152    4      115    0      5      3      2      4      12     16     5      5      | 324   
osd.21  5      150    4      113    0      4      3      5      6      25     21     2      9      | 347   
osd.22  5      152    8      114    0      8      2      6      6      15     19     1      7      | 343   
osd.23  5      151    6      112    0      9      3      5      6      21     25     5      5      | 353   
osd.24  3      153    11     114    0      2      9      6      8      24     24     5      2      | 361   
osd.25  4      151    5      114    0      6      4      4      3      14     26     5      6      | 342   
osd.26  4      151    3      115    0      3      9      5      3      20     21     4      9      | 347   
osd.27  3      153    1      114    0      5      9      2      3      20     22     6      4      | 342   
osd.28  5      153    4      115    0      6      5      5      6      19     17     5      6      | 346   
osd.29  6      151    6      114    0      5      2      3      4      22     24     6      0      | 343   
osd.30  5      151    6      114    0      6      7      4      6      15     21     4      3      | 342   
osd.31  2      152    1      113    0      4      1      4      7      16     16     7      6      | 329   
osd.32  3      153    7      114    0      8      6      9      10     20     18     2      5      | 355   
osd.33  6      150    4      114    0      7      3      2      3      21     18     2      6      | 336   
osd.34  3      153    2      114    0      3      3      4      4      14     13     5      7      | 325   
osd.35  4      151    5      113    0      7      3      5      5      18     17     6      4      | 338   
osd.36  4      151    7      115    0      4      5      3      5      20     20     2      5      | 341   
osd.37  2      153    4      114    0      4      5      3      2      20     11     5      4      | 327   
osd.38  3      153    1      115    0      4      4      4      8      16     14     6      4      | 332   
osd.39  3      151    9      115    0      2      3      1      3      17     26     4      6      | 340   
osd.40  4      151    6      115    0      0      7      5      4      28     20     2      4      | 346   
osd.41  5      151    7      114    0      3      4      2      5      20     19     10     4      | 344   
osd.42  3      151    6      112    0      5      6      4      4      16     12     7      1      | 327   
osd.43  0      150    5      115    0      5      4      6      2      23     16     4      7      | 337   
osd.44  4      151    6      114    0      3      4      6      6      13     19     4      3      | 333   
osd.45  6      150    7      114    0      7      4      7      3      21     23     4      8      | 354   
osd.46  7      152    5      113    0      4      6      5      6      32     15     5      6      | 356   
osd.47  10     151    5      112    0      4      2      5      3      12     26     5      1      | 336   
osd.48  8      153    5      114    0      4      6      4      4      24     21     4      3      | 350   
osd.49  3      151    6      113    0      6      2      2      11     11     19     6      5      | 335   
osd.50  2      153    4      113    0      6      4      4      6      13     20     4      5      | 334   
osd.51  7      150    2      113    0      3      10     5      5      23     17     2      3      | 340   
osd.52  7      151    5      113    0      4      12     1      3      18     26     5      3      | 348   
osd.53  4      152    3      114    0      6      6      5      3      17     16     6      9      | 341   
osd.54  5      152    6      115    0      6      6      5      4      22     20     4      7      | 352   
osd.55  3      151    6      113    0      1      3      2      6      28     20     4      8      | 345   
osd.56  4      153    3      112    0      5      5      6      7      23     16     4      4      | 342   
osd.57  8      153    5      114    0      4      4      8      8      14     15     1      5      | 339   
osd.58  6      152    5      114    0      4      7      5      3      22     16     7      4      | 345   
osd.59  5      153    9      114    0      2      3      4      7      23     21     5      3      | 349   
osd.60  6      152    5      115    0      6      3      1      4      18     25     5      5      | 345   
osd.61  4      153    7      113    0      4      6      2      5      13     17     4      5      | 333   
osd.62  5      150    4      112    0      5      3      2      6      12     19     6      1      | 325   
osd.63  4      150    3      115    0      5      4      11     5      14     20     7      4      | 342   
osd.64  7      153    9      114    0      8      3      2      7      15     15     5      3      | 341   
osd.65  2      153    4      115    0      3      3      3      3      15     24     3      8      | 336   
osd.66  7      153    4      114    0      2      2      6      3      17     11     7      5      | 331   
osd.67  7      151    4      114    0      6      3      7      5      23     19     4      5      | 348   
osd.68  9      153    7      113    0      3      5      6      3      21     24     9      2      | 355   
osd.69  1      152    4      114    0      4      8      1      5      24     14     2      8      | 337   
osd.70  6      150    5      114    0      1      6      6      4      16     20     2      4      | 334   
osd.71  7      152    7      113    0      5      6      2      7      22     17     6      7      | 351   
osd.72  4      152    3      114    0      4      8      5      6      9      18     9      6      | 338   
osd.73  7      153    5      113    0      12     5      5      2      23     18     6      6      | 355   
osd.74  2      151    9      114    0      2      3      2      3      26     13     2      1      | 328   
osd.75  6      153    3      113    0      7      6      1      4      14     15     4      6      | 332   
osd.76  5      153    2      114    0      4      8      8      3      23     22     3      2      | 347   
osd.77  6      153    6      115    0      10     5      5      8      20     25     3      4      | 360   
osd.78  4      151    3      113    0      0      6      6      3      19     23     5      4      | 337   
osd.79  5      151    7      115    0      6      6      5      5      26     18     5      2      | 351   
osd.80  6      151    6      114    0      8      6      5      2      28     24     4      5      | 359   
osd.81  4      150    4      113    0      4      5      4      7      21     12     6      5      | 335   
osd.82  5      150    5      114    0      10     2      5      3      23     21     2      8      | 348   
osd.83  3      152    4      113    0      7      3      6      2      22     21     4      3      | 340   
osd.84  5      152    7      114    0      5      5      7      7      12     10     3      4      | 331   
osd.85  6      150    6      114    0      7      4      5      6      12     9      6      5      | 330   
osd.86  5      153    7      114    0      8      3      5      4      23     19     6      5      | 352   
osd.87  9      151    2      113    0      6      4      6      5      12     18     9      9      | 344   
osd.88  6      152    3      114    0      3      4      5      3      19     19     1      4      | 333   
osd.89  5      152    4      114    0      3      6      6      6      18     27     4      5      | 350   
osd.90  6      151    1      112    0      4      3      5      6      20     21     5      3      | 337   
osd.91  3      152    4      114    0      7      9      5      8      24     24     4      7      | 361   
osd.92  3      153    6      114    0      4      5      2      6      23     22     3      3      | 344   
osd.93  5      150    3      113    0      4      4      6      5      22     18     10     6      | 346   
osd.94  7      153    2      114    0      2      2      4      7      15     15     5      3      | 329   
osd.95  5      152    4      114    0      4      3      5      4      17     27     2      2      | 339   
osd.96  5      150    5      114    0      4      2      4      4      22     15     4      7      | 336   
osd.97  6      152    3      115    0      4      5      5      3      12     14     4      2      | 325   
osd.98  2      153    3      114    0      2      3      12     5      18     23     3      5      | 343   
osd.99  1      151    6      113    0      7      1      4      2      19     23     5      3      | 335   
osd.100 3      151    5      112    0      7      5      3      8      24     13     3      6      | 340   
osd.101 9      150    0      114    0      5      5      8      3      20     19     8      3      | 344   
osd.102 4      151    5      112    0      3      7      5      1      13     20     9      6      | 336   
osd.103 3      152    5      115    0      3      1      3      2      21     13     5      6      | 329   
osd.104 7      153    4      114    0      5      5      7      6      14     24     3      8      | 350   
osd.105 2      153    3      115    0      6      3      3      7      20     15     1      6      | 334   
osd.106 1      151    3      114    0      3      4      6      7      17     18     9      7      | 340   
osd.107 5      152    3      115    0      11     6      5      3      21     22     3      2      | 348   
osd.108 0      0      0      0      170    0      0      0      0      0      0      0      0      | 170   
osd.109 0      0      0      0      171    0      0      0      0      0      0      0      0      | 171   
osd.110 0      0      0      0      171    0      0      0      0      0      0      0      0      | 171   

--------------------------------------------------------------------------------------------------------------

SUM   : 512    16384  512    12288  512    512    512    512    512    2048   2048   512    512    |
root@node166:~# ceph df
GLOBAL:
    SIZE        AVAIL       RAW USED     %RAW USED 
    1.55PiB     1.55PiB      3.73GiB             0 
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS 
    .rgw.root                     1      1.07KiB         0        354TiB           4 
    default.rgw.control           2           0B         0        295TiB           8 
    default.rgw.meta              3      2.13KiB         0        295TiB          15 
    default.rgw.log               4           0B         0        295TiB         192 
    .ezs3                         5           0B         0        322TiB           1 
    data                          6           0B         0        443TiB           0 
    default.rgw.buckets.data      7           0B         0        525TiB           0 
    .ezs3.central.log             8       130KiB         0        354TiB           4 
    .ezs3.statistic               9      44.4MiB         0        354TiB         760 
    metadata                      10          0B         0        740TiB           0 
    default.rgw.buckets.index     12          0B         0        322TiB           0 
    s3-data-pool                  13          0B         0        985TiB           0 
    s3-index-pool                 14          0B         0       5.13TiB        1134 
root@node166:~# 

```





经过几天持续的灌入，后期（大约最后一亿的对象）由于cosbench task部分workers与部分driver还在持续运行中，如下图所示：

<img class="shadow" src="/img/in-post/image-20210929134618041.png" width="600" />




部分workers已经结束，但对应driver的部分worker下的mission还在持续运行中：

<img class="shadow" src="/img/in-post/image-20210929134755657.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210929134818421.png" width="600" />



导致cosbench客户端压力不足，整体性能衰减，不应理解为产品问题。



最终灌12亿对象的效果如下：



存储端：

<img class="shadow" src="/img/in-post/image-20210929203936269.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210929204018898.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210929204227169.png" width="600" />

​    由于测试到尾声的时候，cosbench task对应driver里有部分的workers结束，有的整个driver结束，导致后期cosbench 压测的压力不足，所以性能衰减，可以参考28号6:00之前的数据，整体看有衰减，但衰减波动幅度不大。





只看前11亿数据：

<img class="shadow" src="/img/in-post/image-20210930053341048.png" width="600" />

<img class="shadow" src="/img/in-post/image-20210930053415952.png" width="600" />


cosbench task信息：


<img class="shadow" src="/img/in-post/image-20210930192626096.png" width="600" />



cosbench绘制不了折线图了，这里以driver1显示的速度做标记，最初是500ops，跑到结束的时候大约300+，平均下来400+的ops：

<img class="shadow" src="/img/in-post/image-20210930194736058.png" width="600" />


## 基础数据10亿下灌一亿4k



PG split功能开启，创建s3-data-pool&s3-index-pool，PG分布均衡，做了上面的参数优化

单一bucket，存在10.2亿数据，持续灌1亿4K对象



开始是有10.2亿数据：

<img class="shadow" src="/img/in-post/Base on 102 Million, start to write 10 Million-start.png" width="600" />

然后灌1亿对象：


<img class="shadow" src="/img/in-post/image-20211009122645425.png" width="600" />

<img class="shadow" src="/img/in-post/Base on 102 Million, start to write 10 Million-end.png" width="600" />




cosbench task信息：

<img class="shadow" src="/img/in-post/image-20211009122521049.png" width="600" />


# 结束语



* metadata pool， s3 data pool 需要启用PG Split功能

* 确保 metadata pool， s3 data pool，s3 index pool PG分布均衡

* 无需人为再次放大metadata pool，s3 data pool, s3 index pool 的 pg_num&pgp_num，放大后并不能提升性能，反而出现间歇性的性能衰减

* 集群中各个节点的硬件规格一致，特别在有NVME SSD做OSD Bigterastore Cache情况下，NVME SSD 规格要一致

  *  如存在有Bigterastore Cache对应SSD性能弱情况下，使得性能弱的SSD所在disk inode的消耗过多（cosbench写的快，但flush/evict慢），会提早出现pool full问题造成性能断崖式衰减

* 针对客户POC性能测试场景，测试时需区别对待

  * 关注性能指标，有明确OPS要求的场景

    * 如要求OPS为5000的，建议空桶状态下测试，可适当放大cosbench work对应workers数量来压测，比如workers=48

    * 如要求bucket中有一定数据量，比如bucket下已有5亿对象，确保Bigterastroe Cache所在文件系统的inode消耗处于比较低的水位（e.g:df -f /data/cache/osd-name*）情况下压测，避免在inode处于高消耗状态下压测更多数据，这样只会引发pool full造成断崖式性能下跌

  * 关注持续稳定不出现性能衰减场景

    * 如要求业务不中断情况下，持续从0~10亿不出现性能衰减，则使用较小的cosbench workers来压测
      Lab的这套6节点环境验证过如下workers值：

       * workers=96，每个driver可以达到1500+ OPS

       * workers=8，每个driver可以达到1000 OPS左右

       * workers=2，每个driver可以达到200 OPS左右

       * workers=3，每个driver可以达到400 OPS左右

       * workers=4，每个driver可以达到500 OPS左右

         所以Lab里测试0~12亿对象，持续写验证不出现性能瓶颈的场景，使用的是workers=4来验证，在cosbench写入速度与flush/evict object 到HDD之间寻找一个平衡点，避免因cosbench写的太快，flush/evict太慢造成Bigterastore Cache所在文件系统的inode过早被消耗殆尽而出现性能断崖式衰减

* 暂无法根据现有硬件来推算出集群单一bucket中最大能支持存放多少S3 objects

