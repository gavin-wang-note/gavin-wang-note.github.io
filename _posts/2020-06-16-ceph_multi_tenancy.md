---
layout:     post
title:      "ceph S3 多租户"
subtitle:   "ceph multi-tenancy"
date:       2020-06-16
author:     "Gavin Wang"
catalog:    true
categories:
    - [ceph]
tags:
    - ceph
---


# 什么是multi-tenancy

在J版之前，同一个ceph集群中不允许有同名的bucket和S3账号的存在，从J版本开始，引入multi-tenancy功能，使得不同tenant（租户）下的账号和bucket可以同名，为了兼容J之前的版本，提供了一名为空的“legacy” 租户，如果没有指定tenant，则从这个“legacy” tenant去获取账号/bucket信息。



# 查看默认tenant中S3账号信息

```shell
root@node76:/var/log/ezcloudstor# radosgw-admin metadata list user
[
    "admin",
    "user01"
]
```

上述信息中，有两个S3账号，admin账号先忽略，此账号为超级管理员， user01为我创建的一个普通S3账号，此账号信息如下：

```shell
root@node76:/var/log/ezcloudstor# radosgw-admin user info --uid=user01
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
            "access_key": "U3SNDWWAJRSTQU2YZAMG",
            "secret_key": "5l1fg5VgsWo1z9fCd2IvCdrTwGi1asHBqb4b6DTQ"
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
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "bigtera_roles": {
        "cluster_admin": false,
        "deleting": false,
        "migrated": false,
        "s3_admin": false,
        "sds_admin": false,
        "sns": false,
        "sqs": false
    }
}

root@node76:/var/log/ezcloudstor# 
```


直接指定tenant为空，再次查询一下这个S3账号

```shell
root@node76:~# radosgw-admin user info --uid=user01 --tenant=''
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
            "access_key": "U3SNDWWAJRSTQU2YZAMG",
            "secret_key": "5l1fg5VgsWo1z9fCd2IvCdrTwGi1asHBqb4b6DTQ"
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
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "bigtera_roles": {
        "cluster_admin": false,
        "deleting": false,
        "migrated": false,
        "s3_admin": false,
        "sds_admin": false,
        "sns": false,
        "sqs": false
    }
}
```

可以确认一点，当不携带tenant或者指定的tenant为空时，从一个为空的tenant中获取S3账号信息，ceph只所以这么做，是为了兼容J之前的版本。


# 创建不同租户下的相同账号

这里会预先创建两个租户下的同名账号，tenant1下的user01，和tenant2下的user01

```shell
radosgw-admin user create --tenant tenant1 --uid user01 --display-name "tenant1_user01"
radosgw-admin user create --tenant tenant2 --uid user01 --display-name "tenant2_user01"
```

```shell
root@node76:~# radosgw-admin user list
[
    "admin",
    "tenant1$user01",
    "tenant2$user01",
    "user01"
]
root@node76:~# 
```

这里可以看到两个账号，"tenant1$user01" 和 "tenant2$user01"，以符号“$”间隔开，用户名相同，只是属于不同的租户（tenant），不相互冲突。

通过user info，指定tenant，获取到这两个账号的access key 和 secret key，示例如下:

```shell
root@node76:~# radosgw-admin --uid=user01 user info --tenant tenant1
{
    "user_id": "tenant1$user01",
    "display_name": "tenant1_user01",
    "email": "",
    "suspended": 0,
    "max_buckets": 1000,
    "auid": 0,
    "subusers": [],
    "keys": [
        {
            "user": "tenant1$user01",
            "access_key": "SSCBPW100ED03TI0MU51",
            "secret_key": "Tnnjsw7e8A7Gu4qblQlHaka4uoOq5rVVR2cDEfOz"
        }
    ],
    "swift_keys": [],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_raw": false,
        "max_size": -1,
        "max_size_kb": 0,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "bigtera_roles": {
        "cluster_admin": false,
        "deleting": false,
        "migrated": false,
        "s3_admin": false,
        "sds_admin": false,
        "sns": false,
        "sqs": false
    }
}

root@node76:~# 
```

# 对象上传

分别给这两个租户下的同名账号创建相同的bucket，以及上传对象。

node75上，使用tenant1的user01账号；node76上，使用tenant2的user01账号分别创建同名的bucket，以及上传对象到bucket中：

```shell
root@node75:~# cat .s3cfg | grep _key | grep -v kms
access_key = SSCBPW100ED03TI0MU51
secret_key = Tnnjsw7e8A7Gu4qblQlHaka4uoOq5rVVR2cDEfOz
```

```shell
root@node76:~# cat .s3cfg | grep _key | grep -v kms
access_key = 22XOFAUIPFR11C45483R
secret_key = vN5C1bNMcBbprfPm0v3ozKQ4rvvgsZeLuNRoVJ9B
root@node76:~# 
```

尝试创建同名bucket:

```shell
root@node75:~# s3cmd mb s3://tenant-bucket01
Bucket 's3://tenant-bucket01/' created
root@node75:~# 
```

```shell
root@node76:~# s3cmd mb s3://tenant-bucket01
Bucket 's3://tenant-bucket01/' created
root@node76:~# 
```


```shell
root@node76:~# radosgw-admin bucket list
[
    "tenant1/tenant-bucket01",
    "tenant2/tenant-bucket01",
    "bigtera-admin-log-target-bucket"
]
root@node76:~#
```

这里并不需要指定tenant，因为rgw是以key去区分用户数据使用哪一个tenant的，至此，同名的bucket创建成功，可以看到，bucket是以符号"/"间隔开。


开始上传对象到这两个bucket中，分别上传不同的对象:

```shell
root@node75:~# s3cmd put tenant1.png s3://tenant-bucket01
upload: 'tenant1.png' -> 's3://tenant-bucket01/tenant1.png'  [1 of 1]
 8 of 8   100% in    0s   610.87 B/s  done
root@node75:~#
```


```shell
root@node76:~# s3cmd put tenant2.png s3://tenant-bucket01
upload: 'tenant2.png' -> 's3://tenant-bucket01/tenant2.png'  [1 of 1]
 27 of 27   100% in    0s  2019.45 B/s  done
root@node76:~#
```

查看对象上传效果：

```shell
root@node75:~# s3cmd ls s3://tenant-bucket01
2020-06-16 06:58         8   s3://tenant-bucket01/tenant1.png
root@node75:~#
```

```shell
root@node76:~# s3cmd ls s3://tenant-bucket01/
2020-06-16 07:03        27   s3://tenant-bucket01/tenant2.png
root@node76:~#
```


# 总结

本文所示的多租户，解决了如下问题：

* 实现同集群中创建同名bucket和S3账号，即实现租户的数据隔离。

而实际应用要远比本文所示要复杂的多，比如不同tenant之间不同bucket下的数据共享，这就涉及到RGW bucket policy 设置问题了。



