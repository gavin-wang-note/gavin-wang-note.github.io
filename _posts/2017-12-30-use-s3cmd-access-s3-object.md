---
layout:     post
title:      "使用s3cmd操作对象"
subtitle:   "use s3cmd to access S3 object"
date:       2017-12-30
author:     "Gavin"
catalog:    true
tags:
    - s3cmd
    - S3
---

# 前言

ceph 天然支持对象存储，经常使用XShell访问server，习惯了在console里做一些操作，那么，如何

# 获取S3 key

ceph提供radosg-admin命令，方便查询S3账号的属性信息，诸如ACL，quota，AKEY，SKEY等等一些信息，如下所示：


```
root@auto-70-1:~# radosgw-admin --uid=user01 user info
{
    "user_id": "user01",
    "display_name": "user01",
    "email": "user01@126.com",
    "suspended": 0,
    "max_buckets": 1000,
    "auid": 0,
    "subusers": [
        {
            "id": "user01:user01",
            "permissions": "full-control"
        }
    ],
    "keys": [
        {
            "user": "user01",
            "access_key": "4B2DT6E0B9C5R6MJ8OEA",
            "secret_key": "XI5ZxYejXiZXUJWtzLDEs4OXiGOYVDuoXVhBYtIa"
        }
    ],
    "swift_keys": [
        {
            "user": "user01",
            "secret_key": "1"
        },
        {
            "user": "user01:user01",
            "secret_key": "1"
        }
    ],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "max_size_kb": -1,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "max_size_kb": -1,
        "max_objects": -1
    },
    "temp_url_keys": []
}

root@auto-70-1:~# 
```


# 配置s3cmd config

通过上面获取到的AKEY和SKEY，就可以进行s3cmd的配置操作了。

```
root@auto-70-1:~# s3cmd --configure

Enter new values or accept defaults in brackets with Enter.
Refer to user manual for detailed description of all options.

Access key and Secret key are your identifiers for Amazon S3
Access Key: 4B2DT6E0B9C5R6MJ8OEA
Secret Key: XI5ZxYejXiZXUJWtzLDEs4OXiGOYVDuoXVhBYtIa

Encryption password is used to protect your files from reading
by unauthorized persons while in transfer to S3
Encryption password: 
Path to GPG program [/usr/bin/gpg]: 

When using secure HTTPS protocol all communication with Amazon S3
servers is protected from 3rd party eavesdropping. This method is
slower than plain HTTP and can't be used if you're behind a proxy
Use HTTPS protocol [No]: 

On some networks all internet access must go through a HTTP proxy.
Try setting it here if you can't conect to S3 directly
HTTP Proxy server name: 

New settings:
  Access Key: 4B2DT6E0B9C5R6MJ8OEA
  Secret Key: XI5ZxYejXiZXUJWtzLDEs4OXiGOYVDuoXVhBYtIa
  Encryption password: 
  Path to GPG program: /usr/bin/gpg
  Use HTTPS protocol: False
  HTTP Proxy server name: 
  HTTP Proxy server port: 0

Test access with supplied credentials? [Y/n] n

Save settings? [y/N] y
Configuration saved to '/root/.s3cfg'
root@auto-70-1:~#
```

# 修改.s3conf

从上面可以看出，会生成用户的配置文件/root/.s3cfg,但是标准的s3是amazon提供的，因此：

```
host_base = s3.amazonaws.com
host_bucket = %(bucket)s.s3.amazonaws.com
```

显然，如果不修改配置文件，就会访问官方正式的amazon s3 服务，而ceph提供的是兼容服务，比如让web service请求发送到ceph集群中的某个主机，或者ceph 集群提供的域名。

因此将上面两行中的s3.amazonaws.com改成集群中的IP或者集群提供的域名.


```:%s/s3.amazonaws.com/192.168.7.105/g ```

至此，就可以通过s3cmd正常访问对象存储了。

# 操作bucket

## 创建Bucket

```
root@auto-70-1:~# s3cmd mb s3://bench
Bucket 's3://bench/' created
root@auto-70-1:~#
```


## 查看当前S3账号下有哪些bucket
```
root@auto-70-1:~# s3cmd ls
2017-12-30 06:54  s3://bench
```
## 上传对象
```
root@auto-70-1:~# s3cmd put /var/log/syslog s3://bench
/var/log/syslog -> s3://bench/syslog  [1 of 1]
 732743 of 732743   100% in    0s    10.42 MB/s  done
```

## 列出bucket下有哪些对象

```
root@auto-70-1:~# s3cmd ls s3://bench
2017-12-30 08:09    732743   s3://bench/syslog
```

## 下载对象

```
root@auto-70-1:~# mkdir download
root@auto-70-1:~# cd download
root@auto-70-1:~/download# s3cmd get s3://bench/syslog
s3://bench/syslog -> ./syslog  [1 of 1]
 732743 of 732743   100% in    0s    31.35 MB/s  done
root@auto-70-1:~/download# ls -l
total 716
-rw-r--r-- 1 root root 732743 Dec 30 16:11 syslog
root@auto-70-1:~/download# md5sum syslog 
07e6f89c26d60ec499a203366ba24d55  syslog
root@auto-70-1:~/download# s3cmd info s3://bench/syslog
s3://bench/syslog (object):
   File size: 732743
   Last mod:  Mon, 30 Dec 2017 08:09:39 GMT
   MIME type: binary/octet-stream
   MD5 sum:   07e6f89c26d60ec499a203366ba24d55
   ACL:       user01: FULL_CONTROL
root@auto-70-1:~/download#
```

## 获取bucket空间

```
root@auto-70-1:~# s3cmd du s3://bench
336277063 s3://bench/
root@auto-70-1:~# 
```

说明：
* 单位是byte，336277063大约是330M


## 获取bucket或者对象的stat信息

```
root@auto-70-1:~# s3cmd info s3://bench/syslog
s3://bench/syslog (object):
   File size: 732743
   Last mod:  Mon, 30 Dec 2017 08:09:39 GMT
   MIME type: binary/octet-stream
   MD5 sum:   07e6f89c26d60ec499a203366ba24d55
   ACL:       user01: FULL_CONTROL
root@auto-70-1:~# 
```


## 拷贝或者move数据

### copy object

```
root@auto-70-1:~# s3cmd del s3://bench/benchmark_data_auto-70-1_839993_object9
File s3://bench/benchmark_data_auto-70-1_839993_object9 deleted
root@auto-70-1:~# 
```

### move object

```
root@auto-70-1:~# s3cmd ls s3://bucket01;s3cmd mv s3://bench/benchmark_data_auto-70-1_839993_object8 s3://bucket01; s3cmd ls s3://bench | grep *839993_object8
2017-12-30 08:21    732743   s3://bucket01/syslog
File s3://bench/benchmark_data_auto-70-1_839993_object8 moved to s3://bucket01/benchmark_data_auto-70-1_839993_object8
root@auto-70-1:~# 
```

## 删除S3 object

```
root@auto-70-1:~# s3cmd mb s3://bucket01
Bucket 's3://bucket01/' created
root@auto-70-1:~# s3cmd cp s3://bench/syslog s3://bucket01
File s3://bench/syslog copied to s3://bucket01/syslog
root@auto-70-1:~# s3cmd ls s3://bucket01
2017-12-30 08:21    732743   s3://bucket01/syslog
root@auto-70-1:~# 
```


# 更详细的信息与操作，可参看s3cmd操作手册

```
root@auto-70-1:~# s3cmd -h
Usage: s3cmd [options] COMMAND [parameters]

S3cmd is a tool for managing objects in Amazon S3 storage. It allows for
making and removing "buckets" and uploading, downloading and removing
"objects" from these buckets.

Options:
  -h, --help            show this help message and exit
  --configure           Invoke interactive (re)configuration tool.
  -c FILE, --config=FILE
                        Config file name. Defaults to /root/.s3cfg
  --dump-config         Dump current configuration after parsing config files
                        and command line options and exit.
  -n, --dry-run         Only show what should be uploaded or downloaded but
                        don't actually do it. May still perform S3 requests to
                        get bucket listings and other information though (only
                        for file transfer commands)
  -e, --encrypt         Encrypt files before uploading to S3.
  --no-encrypt          Don't encrypt files.
  -f, --force           Force overwrite and other dangerous operations.
  --continue            Continue getting a partially downloaded file (only for
                        [get] command).
  --skip-existing       Skip over files that exist at the destination (only
                        for [get] and [sync] commands).
  -r, --recursive       Recursive upload, download or removal.
  -P, --acl-public      Store objects with ACL allowing read for anyone.
  --acl-private         Store objects with default ACL allowing access for you
                        only.
  --delete-removed      Delete remote objects with no corresponding local file
                        [sync]
  --no-delete-removed   Don't delete remote objects.
  -p, --preserve        Preserve filesystem attributes (mode, ownership,
                        timestamps). Default for [sync] command.
  --no-preserve         Don't store FS attributes
  --exclude=GLOB        Filenames and paths matching GLOB will be excluded
                        from sync
  --exclude-from=FILE   Read --exclude GLOBs from FILE
  --rexclude=REGEXP     Filenames and paths matching REGEXP (regular
                        expression) will be excluded from sync
  --rexclude-from=FILE  Read --rexclude REGEXPs from FILE
  --include=GLOB        Filenames and paths matching GLOB will be included
                        even if previously excluded by one of
                        --(r)exclude(-from) patterns
  --include-from=FILE   Read --include GLOBs from FILE
  --rinclude=REGEXP     Same as --include but uses REGEXP (regular expression)
                        instead of GLOB
  --rinclude-from=FILE  Read --rinclude REGEXPs from FILE
  --bucket-location=BUCKET_LOCATION
                        Datacentre to create bucket in. Either EU or US
                        (default)
  -m MIME/TYPE, --mime-type=MIME/TYPE
                        Default MIME-type to be set for objects stored.
  -M, --guess-mime-type
                        Guess MIME-type of files by their extension. Falls
                        back to default MIME-Type as specified by --mime-type
                        option
  --add-header=NAME:VALUE
                        Add a given HTTP header to the upload request. Can be
                        used multiple times. For instance set 'Expires' or
                        'Cache-Control' headers (or both) using this options
                        if you like.
  --encoding=ENCODING   Override autodetected terminal and filesystem encoding
                        (character set). Autodetected: UTF-8
  --verbatim            Use the S3 name as given on the command line. No pre-
                        processing, encoding, etc. Use with caution!
  --list-md5            Include MD5 sums in bucket listings (only for 'ls'
                        command).
  -H, --human-readable-sizes
                        Print sizes in human readable form (eg 1kB instead of
                        1234).
  --progress            Display progress meter (default on TTY).
  --no-progress         Don't display progress meter (default on non-TTY).
  --enable              Enable given CloudFront distribution (only for
                        [cfmodify] command)
  --disable             Enable given CloudFront distribution (only for
                        [cfmodify] command)
  --cf-add-cname=CNAME  Add given CNAME to a CloudFront distribution (only for
                        [cfcreate] and [cfmodify] commands)
  --cf-remove-cname=CNAME
                        Remove given CNAME from a CloudFront distribution
                        (only for [cfmodify] command)
  --cf-comment=COMMENT  Set COMMENT for a given CloudFront distribution (only
                        for [cfcreate] and [cfmodify] commands)
  -v, --verbose         Enable verbose output.
  -d, --debug           Enable debug output.
  --version             Show s3cmd version (0.9.9.91) and exit.

Commands:
  Make bucket
      s3cmd mb s3://BUCKET
  Remove bucket
      s3cmd rb s3://BUCKET
  List objects or buckets
      s3cmd ls [s3://BUCKET[/PREFIX]]
  List all object in all buckets
      s3cmd la 
  Put file into bucket
      s3cmd put FILE [FILE...] s3://BUCKET[/PREFIX]
  Get file from bucket
      s3cmd get s3://BUCKET/OBJECT LOCAL_FILE
  Delete file from bucket
      s3cmd del s3://BUCKET/OBJECT
  Synchronize a directory tree to S3
      s3cmd sync LOCAL_DIR s3://BUCKET[/PREFIX] or s3://BUCKET[/PREFIX] LOCAL_DIR
  Disk usage by buckets
      s3cmd du [s3://BUCKET[/PREFIX]]
  Get various information about Buckets or Files
      s3cmd info s3://BUCKET[/OBJECT]
  Copy object
      s3cmd cp s3://BUCKET1/OBJECT1 s3://BUCKET2[/OBJECT2]
  Move object
      s3cmd mv s3://BUCKET1/OBJECT1 s3://BUCKET2[/OBJECT2]
  Modify Access control list for Bucket or Files
      s3cmd setacl s3://BUCKET[/OBJECT]
  Sign arbitrary string using the secret key
      s3cmd sign STRING-TO-SIGN
  Fix invalid file names in a bucket
      s3cmd fixbucket s3://BUCKET[/PREFIX]
  List CloudFront distribution points
      s3cmd cflist 
  Display CloudFront distribution point parameters
      s3cmd cfinfo [cf://DIST_ID]
  Create CloudFront distribution point
      s3cmd cfcreate s3://BUCKET
  Delete CloudFront distribution point
      s3cmd cfdelete cf://DIST_ID
  Change CloudFront distribution point parameters
      s3cmd cfmodify cf://DIST_ID

See program homepage for more information at
http://s3tools.org

root@auto-70-1:~# 
```

