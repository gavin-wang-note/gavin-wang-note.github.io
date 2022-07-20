---
layout:     post
title:      "分片上传2T大小的一个S3对象"
subtitle:   "Fragment Upload Object which size is 2T"
date:       2022-06-27
author:     "Gavin"
catalog:    true
tags:
    - S3
    - ceph
---


# 概述

客户询问，对于2T大小的一个S3对象，我司产品是否支持。

原本计划使用GUI工具，诸如S3Browser，CloudBerry这样的可视化工具上传一下验证看看，考虑到本地磁盘大小无法容纳2T大小的文件，只能放弃，改成使用python code来上传看看。



# 操作步骤

## 准备一个2T大小的对象文件

``` fallocate -l 2T 2T.file ```

快速生成一个含有大量hole的文件，存放在某个osd的挂载点（物理磁盘，RAID组，空间比较大，放的下这么大的文件了）


##  准备测试脚本


```
#!/usr/bin/env python

import shutil
import math
import string
import io
from io import BytesIO
import os
from os import path
import sys
import traceback
import boto
import boto.s3.connection
from filechunkio import FileChunkIO
import threading
import Queue
import time

class Chunk:
    num = 0
    offset = 0
    len = 0
    def __init__(self, n, o, l):  
        self.num = n
        self.offset = o
        self.len = l

chunksize = 8 << 20

def init_queue(filesize):
    chunkcnt = int(math.ceil(filesize*1.0/chunksize))
    q = Queue.Queue(maxsize = chunkcnt)
    for i in range(0,chunkcnt):
        offset = chunksize*i
        len = min(chunksize, filesize-offset)
        c = Chunk(i+1, offset, len)
        q.put(c)
    return q

def upload_chunk(filepath, mp, q, id):
    while (not q.empty()):
        chunk = q.get()
        fp = FileChunkIO(filepath, 'r', offset=chunk.offset, bytes=chunk.len)
        mp.upload_part_from_file(fp, part_num=chunk.num)
        fp.close()
        q.task_done()

def upload_file_multipart(filepath, keyname, bucket, threadcnt=8):
    enable_debug_log_cmd = "ceph daemon client.radosgw.0 config set debug_rgw 20/20"
    disable_debug_log_cmd = "ceph daemon client.radosgw.0 config set debug_rgw 0/0"
    get_debug_log_cmd = "ceph daemon client.radosgw.0 config get debug_rgw"

    filesize = os.stat(filepath).st_size
    mp = bucket.initiate_multipart_upload(keyname)
    q = init_queue(filesize)
    for i in range(0, threadcnt):
        t = threading.Thread(target=upload_chunk, args=(filepath, mp, q, i))
        t.setDaemon(True)
        t.start()
    q.join()
    print("--  enable rgw debug log")
    res1 = commands.getoutput(enable_debug_log_cmd)
    res2 = commands.getoutput(get_debug_log_cmd)
    print res1, res2
    mp.complete_upload()
    print("--  disable rgw debug log")
    res3 = commands.getoutput(disable_debug_log_cmd)
    res4 = commands.getoutput(get_debug_log_cmd)
    print res3, res4

def download_chunk(filepath, bucket, key, q, id):
    while (not q.empty()):
        chunk = q.get()
        offset = chunk.offset
        len = chunk.len
        resp = bucket.connection.make_request("GET", bucket.name, key.name, headers={"Range":"bytes=%d-%d" % (offset, offset+len)})
        data = resp.read(len)
        fp = FileChunkIO(filepath, 'r+', offset=offset, bytes=len)
        fp.write(data)
        fp.close()
        q.task_done()

def download_file_multipart(key, bucket, filepath, threadcnt=8):
    if type(key) == str:
        key=bucket.get_key(key)
    filesize=key.size
    if os.path.exists(filepath):
        os.remove(filepath)
    os.mknod(filepath)
    q = init_queue(filesize)
    for i in range(0, threadcnt):
        t = threading.Thread(target=download_chunk, args=(filepath, bucket, key, q, i))
        t.setDaemon(True)
        t.start()
    q.join()

access_key = "YGZTOFN14AEVFGFCX5VA"
secret_key = "Dyt9GlnQ8XPexUzd9iEnFNdUuDpY8vuHvde5DVxl"
host = "10.16.72.161"

filepath = "/data/osd.2/2T.file"
keyname = "2T.file"

threadcnt = 8

conn = boto.connect_s3(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
    host = host,
    is_secure=False,
    calling_format = boto.s3.connection.OrdinaryCallingFormat(),
    )

bucket = conn.get_bucket("test")

time1= time.time()
upload_file_multipart(filepath, keyname, bucket, threadcnt)
time2= time.time()
print "upload %s with %d threads use %d seconds" % (keyname, threadcnt, time2-time1)

key = bucket.get_key(keyname)

download_filepath = path.join(".", keyname)
time1= time.time()
download_file_multipart(key, bucket, download_filepath, threadcnt)
time2= time.time()
print "download %s with %d threads use %d seconds" % (keyname, threadcnt, time2-time1)

```

* 说明：
    这里将2T对象，8个thread并发上传, 每个分片大小是8MiB


## 测试结果

脚本output:


```
root@node224:~# python s3_upload.py            
--  enable rgw debug log                       
{                                              
    "success": ""                              
} {                                            
    "debug_rgw": "20/20"                       
}                                              
--  disable rgw debug log                      
{                                              
    "success": ""                              
} {                                            
    "debug_rgw": "0/0"                         
}                                              
upload 1T.file with 32 threads use 8907 seconds
```


存储端对象信息：



