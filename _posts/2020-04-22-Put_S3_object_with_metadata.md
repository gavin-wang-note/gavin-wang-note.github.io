---
layout:     post
title:      "Put S3 objects with metadata"
subtitle:   "Put S3 objects with metadata"
date:       2020-04-22
author:     "Gavin"
catalog:    true
tags:
    - python
---



```
#!/usr/bin/env python
# -*- coding:UTF-8 -*_

from __future__ import unicode_literals

import time
import boto
import logging
import boto.s3.connection

from random import choice
from string import digits
from multiprocessing.pool import ThreadPool

from ezs3.log import EZLog

EZLog.init_handler(logging.INFO, "./s3_ha.log")
logger = EZLog.get_logger("s3")

pool = ThreadPool(processes=100)


def rand_alpha(length=16):
    return ''.join([choice(digits) for i in xrange(length)])


def connect_s3(access_key, secret_key, host):
    logger.info("Connection to S3")
    conn = boto.connect_s3(
           aws_access_key_id=access_key,
           aws_secret_access_key=secret_key,
           host=host,
           is_secure=False,
           calling_format = boto.s3.connection.OrdinaryCallingFormat(),
          )

    return conn


def create_bucket(conn, bucket_name):
    logger.info("Start to create bucket :(%s)", bucket_name)
    try:
        # bucket = conn.get_bucket(bucket_name)
        bucket = conn.create_bucket(bucket_name)
    except:
        bucket = conn.get_bucket(bucket_name)

    return bucket


def input_object(bucket):
    logging.info("Start to input object")
    for i in xrange(100000000):
        key_name = str(i) + '_' + str(time.time())
        key = bucket.new_key(key_name)

        meta_name = rand_alpha()
        meta_value = rand_alpha()
        # key.metadata = { 'name':'xyz', 'meta2':'value2'}
        key.metadata = {meta_name:meta_value}

        key.set_contents_from_string(key_name)
        if i % 1000000 == 0 and i > 0:
            logger.info("Put done one million object")


def thread_pool_input_object():
    results = []
    for i in xrange(1):
        results.append(pool.apply_async(input_object, (bucket,)))

    for (idx, result) in enumerate(results):
        try:
            r = result.get()
        except:
            logger.exception('Failed to put s3 object')


if __name__ == "__main__":
    access_key='8MHV7BB286YXKE9FFF9X'
    secret_key='hstEN5QEODmENh2Vf5KHCGwOwj61XV1KfbkQxJaC'
    host = '10.16.172.76'
    bucket_name = 's3habucket01'

    conn = connect_s3(access_key, secret_key, host)
    bucket = create_bucket(conn, bucket_name)
    thread_pool_input_object()
```

