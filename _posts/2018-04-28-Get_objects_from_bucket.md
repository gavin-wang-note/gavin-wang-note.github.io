---
layout:     post
title:      "List 3 object from Bucket"
subtitle:   "List S3 object fomr Bucket"
date:       2018-04-28
author:     "Gavin"
catalog:    true
tags:
    - python
---

# Script

```
#!/usr/bin/python
# coding: utf8

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.bucket import Bucket
from boto.s3.key import Key
import time

ACCESS_KEY = "85P6XN20EO05YX88ID9E"
SECRET_ACCESS_KEY = "zzYU77LbdRGOCndXDFhQKw6a949p1Xj5qBjgjRgh"
HOST = "172.17.59.45"
BUCKET_NAME = "account0bucket0" 
PREFIX = "NODE98-1952364"

# create s3 connection
def s3_con(ACCESS_KEY, SECRET_ACCESS_KEY, host, port=80):
    conn = S3Connection(ACCESS_KEY,
        SECRET_ACCESS_KEY,
        host = host,
        port = 80,
        calling_format = OrdinaryCallingFormat(),
        is_secure = False
    )

    return conn


def list_objects(conn, bucket_name, prefix, loop_times=None):
    # List all objects with a prefix under a bucket
    loop_times = 100 if loop_times is None else loop_times

    bucket = conn.get_bucket(bucket_name)

    cost_time_list = []
    for i in xrange(loop_times):
        start_time = time.time()
        match_objs = []
        for obj in bucket.list(prefix=prefix):
            match_objs.append(obj)
    
        match_counts = len(match_objs)
        end_time = time.time()

        time_stamp = end_time - start_time
        cost_time_list.append(time_stamp)
        print "match counts: %d  cost time(s) : %.2f" %(match_counts, time_stamp)


    return cost_time_list


def Get_Max(list):
    return max(list)


def Get_Min(list):
    return min(list)


def Get_Average(list):
    sum = 0
    for item in list:
        sum += item
    return sum/len(list)



def run_app():
    conn = s3_con(ACCESS_KEY, SECRET_ACCESS_KEY, HOST)
    
    cost_time_list = list_objects(conn, BUCKET_NAME, PREFIX, loop_times=100)

    max_time = Get_Max(cost_time_list)
    mix_time = Get_Min(cost_time_list)
    avg_time = Get_Average(cost_time_list)

    print "max: {}  min: {}  avg: {}".format(max_time, mix_time, avg_time)


if __name__ == "__main__":
    run_app()

```
