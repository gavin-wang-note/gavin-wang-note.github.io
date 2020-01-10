---
layout:     post
title:      "如何快速知道S3存储性能"
subtitle:   "S3 Radosgw performance"
date:       2019-12-30
author:     "Gavin"
catalog:    true
tags:
    - S3
---


# 前言

当ceph S3集群搭建成功后，想知道当前存储的RGW性能如何， 如何快速评估呢？

本文介绍3种方法：

* s3cmd并发
* rest-bench
* cosbench

# s3cmd 快速评估

详请参考我同事Bean的blog：

```https://bean-li.github.io/s3cmd-put-to-slow/ ```

# Step1. rest-bench

说明：
* rest-bench这个工具，年久失修，在ceph的早期版本开发的（ceph version 0.80.11），运行到最后会crash，好在crash之前，很多的结果已经吐出来的，将就用吧，不用care CORE dump问题

## 安装rest-bench

```
apt-get update
apt-get install rest-bench
```

## Step2. 创建Bucket

本文以s3cmd来创建bucket，当然，也可以通过其他可视化工具（S3 Browser 或者 CloudBerry Explorer for Amazon S3 Freeware）进行Bucket的创建， 如下操作，是在获知S3账号的AKEY和SKEY情况下进行的。

### 准备测试脚本

```
export RGW=localhost:7480
export SECS=10
export SIZE=$((1<<22)) # 4MB object size
export BUCKET=bench
export CONCURRENCY=16
export KEY="4B2DT6E0B9C5R6MJ8OEA"
export SECRET="XI5ZxYejXiZXUJWtzLDEs4OXiGOYVDuoXVhBYtIa"

rest-bench -t $CONCURRENCY -b $SIZE --seconds=$SECS --api-host=$RGW --bucket=$BUCKET --access-key=$KEY --secret=$SECRET --no-cleanup write host=localhost:7480
```

如上脚本，可以放在一个shell script里，也可以直接在ssh console里执行

说明：
* 下列结果，为VM的测试结果，仅做示例

```
 Maintaining 16 concurrent writes of 4194304 bytes for up to 10 seconds or 0 objects
 Object prefix: benchmark_data_auto-70-1_839993
   sec Cur ops   started  finished  avg MB/s  cur MB/s  last lat   avg lat
     0       5         5         0         0         0         -         0
     1      16        20         4   15.9971        16   0.32558  0.209102
     2      16        32        16   31.9936        48  0.805092  0.811289
     3      16        41        25   33.3274        36  0.959682   1.12456
     4      16        42        26   25.9957         4   2.53238    1.1787
     5      16        44        28   22.3966         8   3.08912   1.31648
     6      16        48        32   21.3301        16   3.36158   1.63555
     7      16        57        41   23.4252        36   4.75692   2.15025
     8      16        67        51   25.4964        40   1.14588   2.20246
     9      16        74        58   25.7691        28   1.81314   2.15862
    10      16        79        63   25.1919        20   1.45566   2.13518
    11      16        80        64   23.2657         4   3.54682   2.15723
    12      15        80        65   21.6604         4   3.15252   2.17254
 Total time run:         12.499256
Total writes made:      80
Write size:             4194304
Bandwidth (MB/sec):     25.602 

Stddev Bandwidth:       16.0831
Max bandwidth (MB/sec): 48
Min bandwidth (MB/sec): 0
Average Latency:        2.48922
Stddev Latency:         1.42932
Max latency:            6.14039
Min latency:            0.088134
```


# cosbench

说明：

* 这个工具是Intel 开源的工具，业内也非常认可它，很多厂商都使用它进行S3的性能测试。
* 本文以6节点做配置示例

## controller侧controller.conf内容

```
[controller]
drivers = 6
log_level = INFO
log_file = log/system.log
archive_dir = archive

[driver1]
name = driver1
url = http://10.0.26.91:18088/driver

[driver2]
name = driver2
url = http://10.0.26.92:18088/driver

[driver3]
name = driver3
url = http://10.0.26.93:18088/driver

[driver4]
name = driver4
url = http://10.0.26.94:18088/driver

[driver5]
name = driver5
url = http://10.0.26.95:18088/driver

[driver6]
name = driver6
url = http://10.0.26.96:18088/driver
```

## driver侧driver.conf内容

driver1的driver.conf内容：

```
[driver]
log_level = DEBUG
name = driver1
url = http://10.0.26.91:18088/driver
```

说明：

* 其他node的driver.conf，只是name后面的driver名称（需要与controller.conf匹配）和URL地址的变化，其他没什么变化

## workload示例

### 示例1： 36Threads,运行900秒

```
<?xml version="1.0" encoding="UTF-8"?>
<workload name="Bigtera BT-H4400 HCI 1VM 36Threads" description="1GB tests. include writes, reads, mix tests">
<storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161" />

  <workflow>

		<!-- ******************************* -->
  	<!-- 1mch 24wrks 36threads write job -->
		<!-- ******************************* -->

    <workstage name="1mch-23wrks-36threads-write-init">
        <work name="1mch-24wrks-36threads-write-init" type="init" workers="1" interval="10" division="container" runtime="0" rampup="0" rampdown="0" driver="driver1"  config="cprefix=bigterahci;containers=r(1,48)" />
    </workstage>
    
    <workstage name="1mch-24wrks-36threads-write-WRITEJOB">
        <work name="write1-11_7070" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1" >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(1,2);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-11_7071" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(3);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-11_7072" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(4,5);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-11_7073" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(7,8);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
		
        <work name="write2-11_7070" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(9,10);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-11_7071" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(11,12);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-14_7072" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(13,14);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-14_7073" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(15,16);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
		
        <work name="write1-12_7070" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(17,18);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-12_7071" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(19,20);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-12_7072" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(21,22);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-12_7073" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(23,24);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>

        <work name="write2-12_7070" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(25,26);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-12_7071" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(27,28);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-14_7072" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(29,30);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-14_7073" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(31,32);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>

        <work name="write1-13_7070" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(33,34);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-13_7071" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(35,36);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-13_7072" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(37,38);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write1-13_7073" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(39,40);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>

        <work name="write2-13_7070" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(41,42);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-13_7071" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(43,44);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-14_7072" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(45,46);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="write2-14_7073" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(47,48);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
    </workstage>
		
    <workstage name="1mch-24wrks-36threads-write-cleanup">
          <work type="cleanup" workers="1" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(1,48);objects=r(1,10)" />
    </workstage>
    <workstage name="1mch-24wrks-36threads-write-dispose">
          <work type="dispose" workers="1" driver="driver1" config="cprefix=bigterahci;containers=r(1,48)" />
    </workstage>

		<!-- ****************************** -->
  	<!-- 1mch 24wrks 36threads read job -->
		<!-- ****************************** -->

    <workstage name="1mch-24wrks-36threads-read-init">
        <work name="1mch-24wrks-36threads-read-init" type="init" workers="1" interval="10" division="container" runtime="0" rampup="0" rampdown="0" driver="driver1"  config="cprefix=bigterahci;containers=r(1,48)" />
    </workstage>
    
    <workstage name="1mch-24wrks-36threads-read-prepare">
        <work type="prepare" workers="48" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(1,48);objects=r(1,10);content=zero;sizes=c(1)GB" />
    </workstage>
    
    <workstage name="1mch-24wrks-36threads-read-READJOB">
          <work name="read1-11-7070" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(1,2);objects=u(1,10)" />
          </work>
          <work name="read1-11-7071" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(3,4);objects=u(1,10)" />
          </work>
          <work name="read1-11-7072" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(5,6);objects=u(1,10)" />
          </work>
          <work name="read1-11-7073" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(7,8);objects=u(1,10)" />
          </work>

          <work name="read2-11-7070" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(9,10);objects=u(1,10)" />
          </work>
          <work name="read2-11-7071" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(11,12);objects=u(1,10)" />
          </work>
          <work name="read2-14-7072" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(13,14);objects=u(1,10)" />
          </work>
          <work name="read2-14-7073" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(15,16);objects=u(1,10)" />
          </work>
		  
          <work name="read1-12-7070" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(17,18);objects=u(1,10)" />
          </work>
          <work name="read1-12-7071" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(19,20);objects=u(1,10)" />
          </work>
          <work name="read1-12-7072" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(21,22);objects=u(1,10)" />
          </work>
          <work name="read1-12-7073" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(23,24);objects=u(1,10)" />
          </work>

          <work name="read2-12-7070" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(25,26);objects=u(1,10)" />
          </work>
          <work name="read2-12-7071" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(27,28);objects=u(1,10)" />
          </work>
          <work name="read2-14-7072" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(29,30);objects=u(1,10)" />
          </work>
          <work name="read2-14-7073" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(31,32);objects=u(1,10)" />
          </work>
		  
          <work name="read1-13-7070" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(33,34);objects=u(1,10)" />
          </work>
          <work name="read1-13-7071" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(35,36);objects=u(1,10)" />
          </work>
          <work name="read1-13-7072" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(37,38);objects=u(1,10)" />
          </work>
          <work name="read1-13-7073" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(39,40);objects=u(1,10)" />
          </work>

          <work name="read2-13-7070" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(41,42);objects=u(1,10)" />
          </work>
          <work name="read2-13-7071" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(43,44);objects=u(1,10)" />
          </work>
          <work name="read2-14-7072" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(45,46);objects=u(1,10)" />
          </work>
          <work name="read2-14-7073" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                  <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                  <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(47,48);objects=u(1,10)" />
          </work>

    </workstage>
    
    <workstage name="1mch-24wrks-36threads-read-cleanup">
          <work type="cleanup" workers="1" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(1,48);objects=r(1,10)" />
    </workstage>
    <workstage name="1mch-24wrks-36threads-read-dispose">
          <work type="dispose" workers="1" driver="driver1" config="cprefix=bigterahci;containers=r(1,48)" />
    </workstage>

		<!-- ***************************** -->
  	<!-- 1mch 24wrks 36threads mix job -->
		<!-- ***************************** -->

    <workstage name="1mch-24wrks-36threads-mix-init">
        <work name="1mch-24wrks-36threads-mix-init" type="init" workers="1" interval="10" division="container" runtime="0" rampup="0" rampdown="0" driver="driver1"  config="cprefix=bigterahci;containers=r(1,48)" />
    </workstage>
    
    <workstage name="1mch-24wrks-36threads-mix-prepare">
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(1,2);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(3,4);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(5,6);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(7,8);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(9,10);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(11,12);objects=r(1,10);content=zero;sizes=c(1)GB" />
	    <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(13,14);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(15,16);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(17,18);objects=r(1,10);content=zero;sizes=c(1)GB" />
		<work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(19,20);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(21,22);objects=r(1,10);content=zero;sizes=c(1)GB" />
        <work type="prepare" workers="8" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(23,24);objects=r(1,10);content=zero;sizes=c(1)GB" />
    </workstage>

    <workstage name="1mch-24wrks-36threads-mix-MIXJOB">
        <work name="mix1-14_7070" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(25,26);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix1-11_7071" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(27,28);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix1-11-7072" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(1,2);objects=u(1,10)" />
        </work>
        <work name="mix1-14-7073" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(3,4);objects=u(1,10)" />
        </work>
		
        <work name="mix2-11_7070" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(29,30);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix2-11_7071" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(31,32);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix2-11-7072" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(5,6);objects=u(1,10)" />
        </work>
        <work name="mix2-11-7073" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.161"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(7,8);objects=u(1,10)" />
        </work>
		
        <work name="mix1-12_7070" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(33,34);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix1-14_7071" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(35,36);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix1-14-7072" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(9,10);objects=u(1,10)" />
        </work>
        <work name="mix1-12-7073" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(11,12);objects=u(1,10)" />
        </work>

        <work name="mix2-12_7070" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(37,38);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix2-12_7071" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(39,40);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix2-12-7072" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(13,14);objects=u(1,10)" />
        </work>
        <work name="mix2-12-7073" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.162"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(15,16);objects=u(1,10)" />
        </work>

        <work name="mix1-14_7070" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(41,42);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix1-13_7071" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(43,44);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix1-13-7072" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(17,18);objects=u(1,10)" />
        </work>
        <work name="mix1-14-7073" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.164"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(19,20);objects=u(1,10)" />
        </work>

        <work name="mix2-13_7070" type="write" workers="1" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(45,46);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix2-13_7071" type="write" workers="2" interval="10" division="object" runtime="900" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
            <operation type="write" ratio="100" division="object" config="cprefix=bigterahci;oprefix=1GB_;containers=u(47,48);objects=u(1,10);sizes=c(1)GB;createContainer=false;" id="none" />
        </work>
        <work name="mix2-13-7072" workers="1" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(21,22);objects=u(1,10)" />
        </work>
        <work name="mix2-13-7073" workers="2" runtime="900" rampup="10" rampdown="0" interval="10" driver="driver1" >
                <storage type="s3" config="accesskey=EIP2ZTZO4EHL6A50I8FT;secretkey=GFLTkbyVUaisUuSF0g9QgkZUmkGEyp3hOt7W2tpT;endpoint=http://10.0.26.163"/>
                <operation type="read" ratio="100" config="cprefix=bigterahci;oprefix=1GB_;containers=u(23,24);objects=u(1,10)" />
        </work>
    </workstage>
		
    <workstage name="1mch-24wrks-36threads-mix-cleanup">
          <work type="cleanup" workers="1" driver="driver1" config="cprefix=bigterahci;oprefix=1GB_;containers=r(1,48);objects=r(1,10)" />
    </workstage>
    <workstage name="1mch-24wrks-36threads-mix-dispose">
          <work type="dispose" workers="1" driver="driver1" config="cprefix=bigterahci;containers=r(1,48)" />
    </workstage>

	</workflow>
</workload>

```

说明:

* 如果只考虑运行多长时间，则xml中需要定义 ```runtime="900" ```，表示运行900秒
* 如果要考虑在对应bucket里生成一定数量的object，则需要改成 ```totalOps="500000" ```，这里的500000表示50万个object

### 示例2： 60Threads,顺序写固定数量的object

```
<?xml version="1.0" encoding="UTF-8"?>
<workload name="SEG_phyical_round1_60threads_ONLY_W" description="1VM 60threads w24work WR">
<storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63" />

  <workflow>
		<!-- ******************************* -->
  	<!-- 1mch 20wrks 60threads write job -->
		<!-- ******************************* -->

    <workstage name="1mch-20wrks-60threads-write-init">
        <work name="1mch-20wrks-60threads-write-init" type="init" workers="1" interval="10" division="container" runtime="0" rampup="0" rampdown="0" driver="driver1"  config="cprefix=seg;containers=r(1,1)" />
    </workstage>

    <workstage name="1mch-20wrks-60threads-write-WRITEJOB">
        <work name="write1-11_7070" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1" >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(1,500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-11_7071" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(500001,1000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-11_7072" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(1000001,1500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-11_7073" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(1500001,2000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-11_7070" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(2000001,2500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-11_7071" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(2500001,3000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-11_7072" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.63"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(3000001,3500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-11_7073" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.64"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(3500001,4000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-12_7070" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.64"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(4000001,4500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-12_7071" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.64"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(4500001,5000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-12_7072" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.64"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(5000001,5500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-12_7073" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.64"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(5500001,6000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-12_7070" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.64"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(6000001,6500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-12_7071" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.64"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(6500001,7000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-12_7072" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.65"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(7000001,7500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-12_7073" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.65"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(7500001,8000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-13_7070" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.65"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(8000001,8500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-13_7071" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.65"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(8500001,9000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write1-13_7072" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.65"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(9000001,9500000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2-13_7072" type="write" workers="8" interval="10" division="object" totalOps="500000" rampup="0" rampdown="0" driver="driver1"  >
            <auth type="none" config=""/>
            <storage type="s3" config="accesskey=DJL9ZF20DDPEGYCCY902;secretkey=K7DMecYvlsfU9jf6K6bDTc3afnPwwnWmbQyZ1aK8;endpoint=http://10.10.172.65"/>
            <operation type="write" ratio="100" division="object" config="cprefix=seg;oprefix=1_10KB_;containers=s(1,1);objects=r(9500001,10000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
    </workstage>

<!--
    <workstage name="1mch-20wrks-60threads-write-cleanup">
          <work type="cleanup" workers="1" driver="driver1" config="cprefix=seg;oprefix=1_10KB_;containers=r(1,1);objects=r(1,10)" />
    </workstage>
    <workstage name="1mch-20wrks-60threads-write-dispose">
          <work type="dispose" workers="1" driver="driver1" config="cprefix=seg;containers=r(1,1)" />
    </workstage>
-->

	</workflow>
</workload>
```

## cosbench的补充说明

container selector用 "s", object selector用 "r", 然后container数量跟object的"数量"要"互质"

示例:

``` 
<operation type="write" ratio="100" division="object" config="cprefix=tmo;oprefix=round2_10KB_;containers=s(8,10);objects=r(25001,50000);sizes=c(10240)B;createContainer=false;" id="none" />
```

10-8+1 = 3
50000-25001+1 = 25000
3跟25000数量

然后如果是设置timeout就要保证Dataset够大，不会写到重复的

如果是设置totalOps那設定的值照这个示例就是 3 * 25000 = 75000

如果contrainers和objects用range/sequential的selector时，最终生成的object个数为他们的最小公倍数，比如containers=s(1,10);objects=s(1,20)，这样最后的object个数时20，而不是200，所以要灌全200个object，有两个方法：

* 1. 在prepare workstage里会每个object都写到（不管使用的是何种division），因此利用prepare workstage来灌object
* 2. 如果是normal workstage的话，需要contrainers和objects的个数互为质数(relatively-prime)

