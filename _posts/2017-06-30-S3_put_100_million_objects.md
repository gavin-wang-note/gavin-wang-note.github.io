---
layout:     post
title:      "Put 1Million S3 objects to bucket"
subtitle:   "Put 1Million S3 objects to bucket"
date:       2017-06-30
author:     "Gavin"
catalog:    true
tags:
    - python
---


# Script

S3-1million-testing.py

```
import boto
import boto.s3.connection

access_key='JZKZIF7XY46DXA71ZWJZ'
secret_key='PAMM0M1lW2UhollmLOhTIsPUspYtys8acczxa9QS'

if __name__ == "__main__":
    conn = boto.connect_s3(
           aws_access_key_id=access_key,
           aws_secret_access_key=secret_key,
           host="172.16.146.184",
           calling_format = boto.s3.connection.OrdinaryCallingFormat(),
          )
    bucket = conn.get_bucket("my-bucket")
    print bucket.name
    
    for i in range(0,10000):
        for j in range(1,101):
            key_name=str(i* 100 + j) + '.txt'
            key = bucket.new_key(key_name)
            key.set_contents_from_string(key_name)
        print "put %d objects done"%((i+1)*100)
```
