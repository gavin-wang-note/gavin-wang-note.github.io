i---
layout:     post
title:      "S3 placement to create bucket"
subtitle:   "S3 placement to create bucket"
date:       2019-07-01
author:     "Gavin"
catalog:    true
tags:
    - python
---


s3_placement_create_bucket.py

```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys
import json
import boto
import boto.s3.connection

from ezs3.command import do_cmd


def connect_s3(access_key, secret_key, host):
    print("Connection to S3")
    conn = boto.connect_s3(
           aws_access_key_id=access_key,
           aws_secret_access_key=secret_key,
           host=host,
           calling_format = boto.s3.connection.OrdinaryCallingFormat(),
          )

    return conn


def check_s3_placement(s3_placement):
    s3_placement_set = set()

    res = do_cmd("radosgw-admin zone get --rgw-zone=default").strip()
    res = json.loads(res)

    for each_key in res['placement_pools']:
        s3_placement_set.add(each_key['key'])

    if s3_placement not in s3_placement_set:
        print("[ERROR]  Not exist this S3 placement, please create it first.")
        sys.exit(1)

def create_bucket(conn, bucket_name, s3_placement):
    print("Start to create bucket :({}) in S3 placement : ({})".format(bucket_name, s3_placement))
    try:
        bucket = conn.create_bucket(bucket_name, location=':{}'.format(s3_placement))
    except:
        bucket = conn.get_bucket(bucket_name)

    return bucket

if __name__ == "__main__":
    access_key ='7T0GOCXVGOJXFI4IQJH2'
    secret_key = 'uLqJD5hrkMqtgg0lNQWTWLGod7415L0mB5BIxZEX'
    host = '172.17.75.97'
    bucket_name = 'seg_bucket_test'
    s3_placement = 'new_s3_placement'


    conn = connect_s3(access_key, secret_key, host)
    check_s3_placement(s3_placement)
    create_bucket(conn, bucket_name, s3_placement)

```
