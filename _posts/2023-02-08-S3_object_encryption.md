---
layout:     post
title:      "S3 object encryption by awscli"
subtitle:   "S3 object encryption by awscli"
date:       2023-02-08
author:     "Gavin Wang"
catalog:    true
categories:
    - [ceph]
tags:
    - ceph
---

# 概述

本文介绍如何使用awscli 上传、下载S3 object 的加密object.

写此文章的目的在于转换用户过程中，碰到了object加密上传下载，碍于本人对于awscli指令不熟悉，简易记录下来mark下。


# 实战

前提条件：

* 创建了Bucket

本文以bucket01示例。


## 对 bucket设置Default encryption

```shell
aws s3api put-bucket-encryption --bucket=bucket01 --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}' --endpoint-url=http://localhost/ --debug
```


## 获取bucket的encryption信息

```shell
aws s3api get-bucket-encryption --bucket=bucket05 --endpoint-url=https://localhost/
```

## 上传object

```shell
aws s3api put-object --bucket bucket03 --key 2.txt --body /root/2.txt --server-side-encryption aws:kms --no-verify-ssl --endpoint-url=https://localhost/
```


## 下载Object


```shell
aws s3api  get-object --endpoint-url=https://localhost --bucket=bucket01 --key 2.txt output2.txt --server-side-encryption AES256 --no-verify-ssl
```

如果endpoint-url中不想带上https,需要修改如下参数，并重启rgw


`ceph.config`

```shell
[radosgw]
rgw verify ssl = false
rgw crypt require ssl = false
```



参考资料：

* https://ecloud.10086.cn/op-help-center/doc/article/57923
* https://blog.csdn.net/QTM_Gitee/article/details/118052481
* https://advancedweb.hu/encryption-options-for-s3-objects/
* https://repost.aws/questions/QUVIw4-39zSPe_pxZ7m4Ejiw/using-aws-s-3-api-put-object-sse-customer-key-md-5-fails-with-cli

