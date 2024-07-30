---
layout:     post
title:      "gzip vs bzip2 vs xz vs pbzip2 性能对比"
subtitle:   "gzip vs bzip2 vs xz vs pbzip2 performance comparison"
date:       2020-06-03
author:     "Gavin Wang"
catalog:    true
categories:
    - [gzip]
    - [bzip2]
    - [pbzip2]
    - [xz]
tags:
    - gzip
    - bzip2
    - pbzip2
    - xz
---


# 概述

两天前，简单写了篇bzip2 与 pbzip2 压缩哪个更快，当时是处于使用esrally压测Elastic search性能，并没有太多的关注几种压缩工具的性能如何。本文介绍常用的几种压缩命令，分别汇总出各个命令的压缩&解压缩全方面性能对比。



# 准备工作



看了下gzip，bzip2，pbzip2，xz这4个命令的help信息，帮助信息比较相似：



<img class="shadow" src="/img/in-post/compress_help.png" width="1200">



准备了一个测试文件方便测试：



```shell
root@node244:/mnt/disk/compress_test# ll
total 557704
drwxr-xr-x 2 root root      4096 Jun  3 10:34 ./
drwxr-xr-x 5 root root      4096 Jun  3 10:32 ../
-rw-r--r-- 1 root root 571073631 Jun  3 10:33 ceph-client.radosgw.0.log
root@node244:/mnt/disk/compress_test# 
```



结合各个命令的help信息，可以使用简单的shell命令来完成测试工作，例如：



```shell
for i in {1..9}; do echo "============================  Compress Level $i  ==========================="; echo " ----- Compress -----"; time gzip -k -f -$i ceph-client.radosgw.0.log; echo " ----- Compress info -----"; gzip -l -v ceph-client.radosgw.0.log.gz; echo "-----  Uncompress -----"; time gzip -d -f ceph-client.radosgw.0.log.gz; done
```



# 测试过程



## gzip 压缩与解压缩



```shell
root@node244:/mnt/disk/compress_test# for i in {1..9}; do echo "============================  Compress Level $i  ==========================="; echo " ----- Compress -----"; time gzip -k -f -$i ceph-client.radosgw.0.log; echo " ----- Compress info -----"; gzip -l -v ceph-client.radosgw.0.log.gz; echo "-----  Uncompress -----"; time gzip -d -f ceph-client.radosgw.0.log.gz; done
============================  Compress Level 1  ===========================
 ----- Compress -----

real	0m3.389s
user	0m3.261s
sys	0m0.128s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            27542300           571073631  95.2% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.502s
user	0m1.962s
sys	0m0.472s
============================  Compress Level 2  ===========================
 ----- Compress -----

real	0m3.385s
user	0m3.257s
sys	0m0.128s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            27158636           571073631  95.2% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.782s
user	0m1.893s
sys	0m0.444s
============================  Compress Level 3  ===========================
 ----- Compress -----

real	0m3.407s
user	0m3.262s
sys	0m0.144s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            26820084           571073631  95.3% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.403s
user	0m1.919s
sys	0m0.417s
============================  Compress Level 4  ===========================
 ----- Compress -----

real	0m4.302s
user	0m4.150s
sys	0m0.152s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            22196434           571073631  96.1% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.413s
user	0m1.914s
sys	0m0.433s
============================  Compress Level 5  ===========================
 ----- Compress -----

real	0m4.385s
user	0m4.237s
sys	0m0.149s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            20643438           571073631  96.4% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.370s
user	0m1.937s
sys	0m0.349s
============================  Compress Level 6  ===========================
 ----- Compress -----

real	0m5.298s
user	0m5.142s
sys	0m0.156s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            19503464           571073631  96.6% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.367s
user	0m1.910s
sys	0m0.400s
============================  Compress Level 7  ===========================
 ----- Compress -----

real	0m5.518s
user	0m5.402s
sys	0m0.116s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            19396724           571073631  96.6% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.435s
user	0m1.842s
sys	0m0.486s
============================  Compress Level 8  ===========================
 ----- Compress -----

real	0m6.961s
user	0m6.853s
sys	0m0.108s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            18411146           571073631  96.8% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.480s
user	0m1.884s
sys	0m0.399s
============================  Compress Level 9  ===========================
 ----- Compress -----

real	0m7.233s
user	0m7.077s
sys	0m0.156s
 ----- Compress info -----
method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
defla d30eafa2 Jun  3 10:33            18186392           571073631  96.8% ceph-client.radosgw.0.log
-----  Uncompress -----

real	0m2.877s
user	0m1.820s
sys	0m0.456s
root@node244:/mnt/disk/compress_test# 
```



## bzip2的压缩与解压缩



```shell
root@node244:/mnt/disk/compress_test# for i in {1..9}; do echo "============================  Compress Level $i  ==========================="; echo " ----- Compress -----"; time bzip2 -k -f -v -$i ceph-client.radosgw.0.log ceph-client.radosgw.0.log.bz2; echo "-----  Uncompress -----"; time bzip2 -d -f ceph-client.radosgw.0.log.bz2; done
============================  Compress Level 1  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     28.266:1,  0.283 bits/byte, 96.46% saved, 571073631 in, 20203523 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	1m14.986s
user	1m14.115s
sys	0m0.212s
-----  Uncompress -----

real	0m8.986s
user	0m7.820s
sys	0m0.492s
============================  Compress Level 2  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     34.344:1,  0.233 bits/byte, 97.09% saved, 571073631 in, 16627875 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	1m26.956s
user	1m25.741s
sys	0m0.232s
-----  Uncompress -----

real	0m8.858s
user	0m8.241s
sys	0m0.488s
============================  Compress Level 3  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     37.331:1,  0.214 bits/byte, 97.32% saved, 571073631 in, 15297380 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	1m35.014s
user	1m34.232s
sys	0m0.140s
-----  Uncompress -----

real	0m9.019s
user	0m8.451s
sys	0m0.512s
============================  Compress Level 4  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     38.943:1,  0.205 bits/byte, 97.43% saved, 571073631 in, 14664242 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	1m41.031s
user	1m40.805s
sys	0m0.160s
-----  Uncompress -----

real	0m9.702s
user	0m8.491s
sys	0m0.596s
============================  Compress Level 5  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     40.177:1,  0.199 bits/byte, 97.51% saved, 571073631 in, 14214101 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	1m46.857s
user	1m46.109s
sys	0m0.172s
-----  Uncompress -----

real	0m9.378s
user	0m8.565s
sys	0m0.536s
============================  Compress Level 6  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     41.332:1,  0.194 bits/byte, 97.58% saved, 571073631 in, 13816797 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	1m50.821s
user	1m50.619s
sys	0m0.196s
-----  Uncompress -----

real	0m9.688s
user	0m8.611s
sys	0m0.556s
============================  Compress Level 7  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     41.987:1,  0.191 bits/byte, 97.62% saved, 571073631 in, 13601242 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	1m55.011s
user	1m54.842s
sys	0m0.168s
-----  Uncompress -----

real	0m9.197s
user	0m8.560s
sys	0m0.575s
============================  Compress Level 8  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     42.637:1,  0.188 bits/byte, 97.65% saved, 571073631 in, 13393739 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	2m0.052s
user	1m59.319s
sys	0m0.100s
-----  Uncompress -----

real	0m9.232s
user	0m8.650s
sys	0m0.516s
============================  Compress Level 9  ===========================
 ----- Compress -----
  ceph-client.radosgw.0.log:     43.064:1,  0.186 bits/byte, 97.68% saved, 571073631 in, 13261043 out.
bzip2: Input file ceph-client.radosgw.0.log.bz2 already has .bz2 suffix.

real	2m1.284s
user	2m1.072s
sys	0m0.204s
-----  Uncompress -----

real	0m9.246s
user	0m8.667s
sys	0m0.512s
root@node244:/mnt/disk/compress_test# 
```



## pbzip2的压缩与解压缩



由于担心不同CPU并发影响测试效果，这里指定了CPU个数为24个，在不带-p参数情况下，默认32个，当前环境虽然有32cores，但并不是每次都能全部参与，有时候是32，有时候是29，有时候是26，所以这里指定一个更低值，确保每次执行都使用相同cores的CPU数。

```shell
@node244:/mnt/disk/compress_test# for i in {1..9}; do echo "============================  Compress Level $i  ==========================="; echo " ----- Compress -----"; time pbzip2 -k -f -v -p24 -$i ceph-client.radosgw.0.log; echo "----- Uncompress -----"; time pbzip2 -p24 -d -f ceph-client.radosgw.0.log.bz2; done
============================  Compress Level 1  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 100 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 20251314 bytes
-------------------------------------------

     Wall Clock: 5.553146 seconds

real	0m5.557s
user	2m10.868s
sys	0m0.600s
----- Uncompress -----

real	0m0.675s
user	0m11.626s
sys	0m0.710s
============================  Compress Level 2  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 200 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 17034671 bytes
-------------------------------------------

     Wall Clock: 6.295284 seconds

real	0m6.299s
user	2m28.521s
sys	0m0.892s
----- Uncompress -----

real	0m0.706s
user	0m12.163s
sys	0m0.780s
============================  Compress Level 3  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 300 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 15336308 bytes
-------------------------------------------

     Wall Clock: 7.094542 seconds

real	0m7.098s
user	2m46.324s
sys	0m1.328s
----- Uncompress -----

real	0m1.047s
user	0m12.899s
sys	0m0.723s
============================  Compress Level 4  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 400 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 15289111 bytes
-------------------------------------------

     Wall Clock: 7.390034 seconds

real	0m7.393s
user	2m53.305s
sys	0m1.428s
----- Uncompress -----

real	0m0.738s
user	0m13.124s
sys	0m0.806s
============================  Compress Level 5  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 500 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 14424635 bytes
-------------------------------------------

     Wall Clock: 7.929576 seconds

real	0m7.933s
user	3m5.904s
sys	0m1.616s
----- Uncompress -----

real	0m0.783s
user	0m14.003s
sys	0m0.780s
============================  Compress Level 6  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 600 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 14320561 bytes
-------------------------------------------

     Wall Clock: 8.235693 seconds

real	0m8.240s
user	3m12.339s
sys	0m2.512s
----- Uncompress -----

real	0m0.770s
user	0m13.975s
sys	0m0.789s
============================  Compress Level 7  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 700 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 14284009 bytes
-------------------------------------------

     Wall Clock: 8.463171 seconds

real	0m8.467s
user	3m17.862s
sys	0m2.209s
----- Uncompress -----

real	0m0.828s
user	0m14.793s
sys	0m0.932s
============================  Compress Level 8  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 800 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 14161949 bytes
-------------------------------------------

     Wall Clock: 9.343830 seconds

real	0m9.348s
user	3m37.798s
sys	0m3.541s
----- Uncompress -----

real	0m0.844s
user	0m15.348s
sys	0m0.937s
============================  Compress Level 9  ===========================
 ----- Compress -----
Parallel BZIP2 v1.1.9     - by: Jeff Gilchrist [http://compression.ca]
[Apr. 13, 2014]               (uses libbzip2 by Julian Seward)
Major contributions: Yavor Nikolov <nikolov.javor+pbzip2@gmail.com>

         # CPUs: 24
 BWT Block Size: 900 KB
File Block Size: 900 KB
 Maximum Memory: 100 MB
-------------------------------------------
         File #: 1 of 1
     Input Name: ceph-client.radosgw.0.log
    Output Name: ceph-client.radosgw.0.log.bz2

     Input Size: 571073631 bytes
Compressing data...
    Output Size: 13295516 bytes
-------------------------------------------

     Wall Clock: 10.434447 seconds

real	0m10.438s
user	4m3.675s
sys	0m4.175s
----- Uncompress -----

real	0m0.796s
user	0m15.991s
sys	0m0.911s
root@node244:/mnt/disk/compress_test#
```



## xz的压缩与解压缩



```shell
root@node244:/mnt/disk/compress_test# for i in {0..9}; do echo "============================  Compress Level $i  ==========================="; echo " ----- Compress -----"; rm -rf *.xz; time xz -k -f -v -$i ceph-client.radosgw.0.log; echo " ----- Compress info -----"; xz -l -v ceph-client.radosgw.0.log.xz; echo "----- Uncompress -----"; time xz -d -f ceph-client.radosgw.0.log.xz; done
============================  Compress Level 0  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        17.9 MiB / 544.6 MiB = 0.033    71 MiB/s       0:07             

real	0m7.703s
user	0m7.567s
sys	0m0.136s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    17.9 MiB (18,732,968 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.033
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      18,732,968     571,073,631  0.033  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      18,732,928     571,073,631  0.033  CRC64
----- Uncompress -----

real	0m2.886s
user	0m1.895s
sys	0m0.444s
============================  Compress Level 1  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        17.2 MiB / 544.6 MiB = 0.032    56 MiB/s       0:09             

real	0m9.666s
user	0m9.514s
sys	0m0.152s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    17.2 MiB (18,010,756 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.032
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      18,010,756     571,073,631  0.032  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      18,010,716     571,073,631  0.032  CRC64
----- Uncompress -----

real	0m2.282s
user	0m1.719s
sys	0m0.496s
============================  Compress Level 2  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        16.3 MiB / 544.6 MiB = 0.030    45 MiB/s       0:12             

real	0m12.128s
user	0m11.964s
sys	0m0.164s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    16.3 MiB (17,065,980 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.030
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      17,065,980     571,073,631  0.030  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      17,065,940     571,073,631  0.030  CRC64
----- Uncompress -----

real	0m2.277s
user	0m1.694s
sys	0m0.517s
============================  Compress Level 3  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        16.1 MiB / 544.6 MiB = 0.030    32 MiB/s       0:16             

real	0m16.986s
user	0m16.778s
sys	0m0.208s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    16.1 MiB (16,899,448 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.030
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      16,899,448     571,073,631  0.030  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      16,899,408     571,073,631  0.030  CRC64
----- Uncompress -----

real	0m2.252s
user	0m1.664s
sys	0m0.532s
============================  Compress Level 4  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        16.4 MiB / 544.6 MiB = 0.030    17 MiB/s       0:31             

real	0m31.449s
user	0m31.220s
sys	0m0.228s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    16.4 MiB (17,154,260 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.030
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      17,154,260     571,073,631  0.030  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      17,154,220     571,073,631  0.030  CRC64
----- Uncompress -----

real	0m2.349s
user	0m1.868s
sys	0m0.412s
============================  Compress Level 5  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        15.6 MiB / 544.6 MiB = 0.029    12 MiB/s       0:45             

real	0m45.585s
user	0m45.152s
sys	0m0.420s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    15.6 MiB (16,360,932 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.029
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      16,360,932     571,073,631  0.029  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      16,360,892     571,073,631  0.029  CRC64
----- Uncompress -----

real	0m2.398s
user	0m1.851s
sys	0m0.488s
============================  Compress Level 6  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        15.1 MiB / 544.6 MiB = 0.028   7.1 MiB/s       1:17             

real	1m17.152s
user	1m16.763s
sys	0m0.388s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    15.1 MiB (15,786,352 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.028
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      15,786,352     571,073,631  0.028  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      15,786,312     571,073,631  0.028  CRC64
----- Uncompress -----

real	0m2.302s
user	0m1.752s
sys	0m0.487s
============================  Compress Level 7  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        15.1 MiB / 544.6 MiB = 0.028   6.7 MiB/s       1:20             

real	1m20.962s
user	1m20.478s
sys	0m0.460s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    15.1 MiB (15,862,848 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.028
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      15,862,848     571,073,631  0.028  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      15,862,808     571,073,631  0.028  CRC64
----- Uncompress -----

real	0m2.368s
user	0m1.803s
sys	0m0.497s
============================  Compress Level 8  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        15.4 MiB / 544.6 MiB = 0.028   6.4 MiB/s       1:25             

real	1m25.153s
user	1m24.488s
sys	0m0.660s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    15.4 MiB (16,130,916 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.028
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      16,130,916     571,073,631  0.028  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      16,130,876     571,073,631  0.028  CRC64
----- Uncompress -----

real	0m2.359s
user	0m1.768s
sys	0m0.535s
============================  Compress Level 9  ===========================
 ----- Compress -----
ceph-client.radosgw.0.log (1/1)
  100 %        15.7 MiB / 544.6 MiB = 0.029   5.9 MiB/s       1:32             

real	1m32.645s
user	1m31.211s
sys	0m1.424s
 ----- Compress info -----
ceph-client.radosgw.0.log.xz (1/1)
  Streams:            1
  Blocks:             1
  Compressed size:    15.7 MiB (16,510,384 B)
  Uncompressed size:  544.6 MiB (571,073,631 B)
  Ratio:              0.029
  Check:              CRC64
  Stream padding:     0 B
  Streams:
    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding
         1         1               0               0      16,510,384     571,073,631  0.029  CRC64            0
  Blocks:
    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check
         1         1              12               0      16,510,344     571,073,631  0.029  CRC64
----- Uncompress -----

real	0m2.394s
user	0m1.763s
sys	0m0.500s
root@node244:/mnt/disk/compress_test# 
```



# 测试结果



## Compression Size



Unit:bytes



| **Compress Level**  | **gzip** |   **bzip2**  | **pbzip2**  | **xz** |
|--------------|------------------|-------------------|-----------------|------------------|
| 0 | - | - | - | 18,732,968 |
| 1 | 27542300 | 20203523 | 20251314 | 18,010,756 |
| 2 | 27158636 | 16627875 | 17034671 | 17,065,980 |
| 3 | 26820084 | 15297380 | 15336308 | 16,899,448 |
| 4 | 22196434 | 14664242 | 15289111 | 17,154,260 |
| 5 | 20643438 | 14214101 | 14424635 | 16,360,932 |
| 6 | 19503464 | 13816797 | 14320561 | 15,786,352 |
| 7 | 19396724 | 13601242 | 14284009 | 15,862,848 |
| 8 | 18411146 | 13393739 | 14161949 | 16,130,916 |
| 9 | 18186392 | 13261043 | 13295516 | 16,510,384 |





## Compression Time


先从压缩时间开始，下列图表显示了从1到9的每个压缩级别完成压缩所花费的时间。


Unit: seconds



| **Compress Level** | **gzip** | **bzip2** | **pbzip2** | **xz**    |
| ------------------ | -------- | --------- | ---------- | --------- |
| 0                  | -        | -         | -          | 0m7.703s  |
| 1                  | 0m3.389s | 1m14.986s | 0m5.557s   | 0m9.666s  |
| 2                  | 0m3.385s | 1m26.956s | 0m6.299s   | 0m12.128s |
| 3                  | 0m3.407s | 1m35.014s | 0m7.098s   | 0m16.986s |
| 4                  | 0m4.302s | 1m41.031s | 0m7.393s   | 0m31.449s |
| 5                  | 0m4.385s | 1m46.857s | 0m7.933s   | 0m45.585s |
| 6                  | 0m5.298s | 1m50.821s | 0m8.240s   | 1m17.152s |
| 7                  | 0m5.518s | 1m55.011s | 0m8.467s   | 1m20.962s |
| 8                  | 0m6.961s | 2m0.052s  | 0m9.348s   | 1m25.153s |
| 9                  | 0m7.233s | 2m1.284s  | 0m10.438s  | 1m32.645s |





<img class="shadow" src="/img/in-post/compression_time.png" width="1200">


从折线图可以看出，随着压缩级别的提高，bzip2需要花费更长的时间才能完成，pbzip2和gzip的变化不大，而压缩级别为3后，xz的增长非常明显。



## Compression Ratio



Unit: %



| **Compress Level** | **gzip** | **bzip2** | **pbzip2** | **xz** |
| ------------------ | -------- | --------- | ---------- | ------ |
| 0                  | -        | -         | -          | 3.3    |
| 1                  | 4.8      | 3.54      | 3.55       | 3.3    |
| 2                  | 4.8      | 2.91      | 2.98       | 3.0    |
| 3                  | 4.7      | 2.68      | 2.69       | 3.0    |
| 4                  | 3.9      | 2.57      | 2.68       | 3.0    |
| 5                  | 3.6      | 2.49      | 2.53       | 2.9    |
| 6                  | 3.4      | 2.42      | 2.51       | 2.8    |
| 7                  | 3.4      | 2.38      | 2.50       | 2.8    |
| 8                  | 3.2      | 2.35      | 2.48       | 2.8    |
| 9                  | 3.2      | 2.32      | 2.33       | 2.9    |



<img class="shadow" src="/img/in-post/compression_ratio.png" width="1200">



compression ratio，越小越好，比如说源文件大小是100MiB，ratio为5%，则压缩后文件大小为5MiB。

从折线图看到趋势是：压缩级别越高，压缩率越低，说明文件被压缩的更小了。在这种情况下，xz始终提供比较平稳的压缩率（但从压缩时间图所示，xz在压缩级别3之后花费更长的时间才能获得这个效果），紧跟其后的是pbzip2和bzip2，gzip在压缩级别为3后，压缩率有所下降。




## Compression Speed



Unit:MiB/s



| **Compress Level** | **gzip** | **bzip2** | **pbzip2** | **xz** |
| ------------------ | -------- | --------- | ---------- | ------ |
| 0                  | -        | -         | -          | 70.702 |
| 1                  | 160.702  | 7.263     | 98.006     | 56.344 |
| 2                  | 160.892  | 6.263     | 86.461     | 44.906 |
| 3                  | 159.853  | 5.732     | 76.728     | 32.063 |
| 4                  | 126.597  | 5.391     | 73.667     | 17.318 |
| 5                  | 124.200  | 5.097     | 68.652     | 11.947 |
| 6                  | 102.797  | 4.914     | 66.094     | 7.059  |
| 7                  | 98.698   | 4.735     | 64.322     | 6.727  |
| 8                  | 78.239   | 4.536     | 58.260     | 6.396  |
| 9                  | 75.296   | 4.490     | 52.176     | 5.879  |



<img class="shadow" src="/img/in-post/compression_speed.png" width="1200">





## Decompression Time



Unit: seconds



| Decompress Level | **gzip** | **bzip2** | **pbzip2** | **xz**   |
| ---------------- | -------- | --------- | ---------- | -------- |
| 0                | -        | -         | -          | 0m2.886s |
| 1                | 0m2.502s | 0m8.986s  | 0m0.675s   | 0m2.282s |
| 2                | 0m2.782s | 0m8.858s  | 0m0.706s   | 0m2.277s |
| 3                | 0m2.403s | 0m9.019s  | 0m1.047s   | 0m2.252s |
| 4                | 0m2.413s | 0m9.702s  | 0m0.738s   | 0m2.349s |
| 5                | 0m2.370s | 0m9.378s  | 0m0.783s   | 0m2.398s |
| 6                | 0m2.367s | 0m9.688s  | 0m0.770s   | 0m2.302s |
| 7                | 0m2.435s | 0m9.197s  | 0m0.828s   | 0m2.368s |
| 8                | 0m2.480s | 0m9.232s  | 0m0.844s   | 0m2.359s |
| 9                | 0m2.877s | 0m9.246s  | 0m0.796s   | 0m2.394s |





<img class="shadow" src="/img/in-post/decompression_time.png" width="1200">


由于数值比较小，从折线图上直接看不出什么效果，从表格中可以看出，当文件的压缩级别越高，解压相应的压缩文件耗时越低。xz的解压缩时间几乎是一条直线，非常平稳，gbip2次之，当gbzip2解压比xz更快。

从Compression time, Compression Ratio，结合当前的Decompress Time看，总体上推荐gbzip2进行文件的压缩与解压缩操作。



## Decompression Speed



Unit: MiB/s



| Decompress Level | **gzip** | **bzip2** | **pbzip2** | **xz** |
| ---------------- | -------- | --------- | ---------- | ------ |
| 0                | -        | -         | -          | 6.202  |
| 1                | 10.498   | 2.144     | 28.612     | 7.537  |
| 2                | 9.310    | 1.790     | 23.011     | 7.159  |
| 3                | 10.644   | 1.618     | 13.970     | 7.149  |
| 4                | 8.773    | 1.441     | 19.757     | 6.982  |
| 5                | 8.307    | 1.445     | 17.569     | 6.505  |
| 6                | 7.858    | 1.360     | 17.737     | 6.560  |
| 7                | 7.598    | 1.410     | 16.452     | 6.558  |
| 8                | 7.080    | 1.384     | 16.002     | 6.528  |
| 9                | 6.028    | 1.368     | 15.929     | 6.558  |



<img class="shadow" src="/img/in-post/decompression_speed.png" width="1200">



# 性能差异和比较

默认情况下，当未指定压缩级别时，gzip 使用 -6，bzip2 和 pbzip2 使用 -9，xz 使用 -6。

根据测试结果，原因非常明确：对于 gzip 和 xz -6 作为默认压缩方法提供良好的压缩级别，但完成时间不会太长，损失一个平衡点，因为较高的压缩级别需要更长的时间来处理压缩。另一方面，pbzip2 最好使用默认压缩级别为 9，如手册页中建议的那样，此处的结果证实了这一点，压缩比增加，但所采用的时间几乎相同，在级别 1 到 9 之间相差不到一秒；但反观bzip2，使用不同的压缩级别，压缩耗时还是有蛮大幅度变化的。

一般来说，xz 达到最佳压缩级别，非常的平稳，然后是 bzip2和pbzip2，然后是 gzip。为了达到更好的压缩，但是xz通常需要最长的完成，其次是pbzip2，然后是gzip，最差的是bzip2，耗时太久。

xz 的默认压缩级别为 6，而 pbzip2 在压缩级别 9 时仅花费比 gzip 稍长一点的时间，并且压缩量更好，而 pbzip2 和 xz 之间的差异小于 pbzip2 和 gzip 之间的差异，因此 pbzip2 成为压缩的优先选择。

根据这些测试结果，pbzip2是压缩的良好中间地带，gzip只是压缩的更快一点，而xz可能并不真正值得使用，尤其使用更高的文件压缩级别（>=6），因为它需要更长的时间来完成压缩操作。

然而，使用 bzip2 解压缩比 xz 或 gzip 或 pbzip2 需要更长的时间，xz 处于解压缩文件的良好中间地带，而 gbzip2 则是解压缩最快的。


# 选择哪种压缩方式？


那么我该选择哪种压缩/解压缩方式？这完全取决于应用目的了，需要因地制宜选择所需的压缩/解压缩方法。


* 如果是交互式的压缩文件，可以使用pxz，这个指令可以看到压缩进度；
* 如果只是想尽可能快的压缩和解压缩文件，很少考虑压缩比情况下，gzip是一个很好的选择；
* 如果只想要一个更好的压缩比，以节约磁盘空间，并愿意话费更多的时间去加压缩它，那么xz只比较好的选择，其次是pbzip2




