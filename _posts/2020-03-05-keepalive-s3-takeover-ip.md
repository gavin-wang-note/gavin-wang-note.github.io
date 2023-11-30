---
layout:     post
title:      "基于Keepalive测试S3浮动IP切换对业务中断时间"
subtitle:   "Base on keepalive to test S3"
date:       2020-03-05
author:     "Gavin"
catalog:    true
tags:
    - keepalive
---


# 前言

最近产品基于keepalive增加了S3 takeover IP，业务透过这个takeover IP访问业务，当takeover IP对应的主机网络故障或宕机，以期能够减少宕机或断网对业务中断的影响。

如何测试验证呢？

本文增加一个script，来进行业务中断耗时的验证

# 测试代码

```
#!/usr/bin/env python
# -*- coding:UTF-8 -*_

import sys
import time
import boto
import logging
import boto.s3.connection
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Value, JoinableQueue as Queue, Lock, Event

from ezs3.log import EZLog

EZLog.init_handler(logging.INFO, "./s3_ha.log")
logger = EZLog.get_logger("s3ha")

pool = ThreadPool(processes=20)


def connect_s3(access_key, secret_key, host):
    logger.info("Connection to S3")
    conn = boto.connect_s3(
           aws_access_key_id=access_key,
           aws_secret_access_key=secret_key,
           host=host,
           calling_format = boto.s3.connection.OrdinaryCallingFormat(),
          )

    return conn


def create_bucket(conn, bucket_name):
    logger.info("Start to create bucket :(%s)", bucket_name)
    try:
        bucket = conn.create_bucket(bucket_name)
    except:
        bucket = conn.get_bucket(bucket_name)

    return bucket


def input_object(bucket, thread_idx, max_time):
    logger.info("Start to input object")
    for i in xrange(20000):
        key_name = str(thread_idx) + "_" + str(i) + '_' + str(time.time())
        start_time = time.time()
        key = bucket.new_key(key_name)
        key.set_contents_from_string(key_name)
        end_time = time.time()
        cost_time = end_time - start_time
        if cost_time > float(max_time):
            logger.warn("Put object : (%s) done, but cost : (%s)s", key_name, cost_time)


def thread_pool_input_object(max_time):
    results = []
    for i in xrange(20):
        results.append(pool.apply_async(input_object, (bucket, i, max_time)))

    for (idx, result) in enumerate(results):
        try:
            r = result.get()
        except:
            logger.exception("Failed to put s3 object")


def multi_procress_pool_input_object(max_time):
    worker_num = 20
    workq = Queue()
    put_finish_event = Event()
    tasks = []
    for i in xrange(worker_num):
        t = Process(
            target=input_object, args=(bucket, i, max_time)
        )
        t.daemon = True
        t.start()
        tasks.append(t)

    workq.join()
    put_finish_event.set()
    for t in tasks:
        t.join()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "\nusage: {} max_time\n  e.g: {} 2\n  Des: max_time is a second time\n".format(sys.argv[0], sys.argv[0])
        sys.exit(2)

    max_time = sys.argv[1]

    access_key='4X4A784SUI49J7FETC2J'
    secret_key='OOxHdJyDKU71j0jdNcmX5Tool3R12q4ixPa8rNvR'
    host = '1.1.1.1'
    bucket_name = 's3habucket01'

    conn = connect_s3(access_key, secret_key, host)
    bucket = create_bucket(conn, bucket_name)
    # thread_pool_input_object(max_time)
    multi_procress_pool_input_object(max_time)
```


这里由于import了产品的函数，脚本不具有通用性，修改了一下:

```
root@node244:~# cat s3_ha.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*_

import sys
import time
import boto
import logging
from logging import handlers
import boto.s3.connection
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Value, JoinableQueue as Queue, Lock, Event



class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level)) # 设置日志级别
        sh = logging.StreamHandler() # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8') # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str) # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

pool = ThreadPool(processes=20)
log = Logger(filename='s3_ha.log')

def connect_s3(access_key, secret_key, host):
    log.logger.info("Connection to S3")
    conn = boto.connect_s3(
           aws_access_key_id=access_key,
           aws_secret_access_key=secret_key,
           host=host,
           is_secure=False,
           calling_format = boto.s3.connection.OrdinaryCallingFormat(),
          )

    return conn


def create_bucket(conn, bucket_name):
    log.logger.info("Start to create bucket : (%s)", bucket_name)
    try:
        bucket = conn.create_bucket(bucket_name)
    except:
        bucket = conn.get_bucket(bucket_name)

    return bucket


def input_object(bucket, thread_idx, max_time):
    log.logger.info("Start to input object")
    for i in xrange(100000):
        key_name = str(thread_idx) + "_" + str(i) + '_' + str(time.time())
        start_time = time.time()
        key = bucket.new_key(key_name)
        key.set_contents_from_string(key_name)
        end_time = time.time()
        cost_time = end_time - start_time
        # log.logger.info("--  start_time is : (%s), end_time is : (%s), cost_time is : (%s), max_time is : (%s)", start_time, end_time, cost_time, max_time)
        if cost_time > float(max_time):
            log.logger.warn("Put object : (%s) done, but cost : (%s)s", key_name, cost_time)


def thread_pool_input_object(max_time):
    results = []
    for i in xrange(20):
        results.append(pool.apply_async(input_object, (bucket, i, max_time)))

    for (idx, result) in enumerate(results):
        try:
            r = result.get()
        except:
            log.logger.exception("Failed to put s3 object")


def multi_procress_pool_input_object(max_time):
    worker_num = 20
    workq = Queue()
    put_finish_event = Event()
    tasks = []
    for i in xrange(worker_num):
        t = Process(
            target=input_object, args=(bucket, i, max_time)
        )
        t.daemon = True
        t.start()
        tasks.append(t)

    workq.join()
    put_finish_event.set()
    for t in tasks:
        t.join()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "\nusage: {} max_time\n  e.g: {} 2\n  Des: max_time is a second time\n".format(sys.argv[0], sys.argv[0])
        sys.exit(2)

    max_time = sys.argv[1]

    access_key='9QK0PJ5S6TKZLEBN1QO0'
    secret_key='iJCIMyq8Ps47SyTIUjG4Z3EAdAZ69fjfQch66VRk'
    host = '1.6.72.80'
    bucket_name = 's3habucket01'

    conn = connect_s3(access_key, secret_key, host)
    bucket = create_bucket(conn, bucket_name)
    # thread_pool_input_object(max_time)
    multi_procress_pool_input_object(max_time)

root@node244:~#
```

