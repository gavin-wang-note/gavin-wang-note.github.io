---
layout:     post
title:      "S3 分片上传对象报416错误码"
subtitle:   "Multipart upload S3 object, raise HTTP 416"
date:       2022-06-30
author:     "Gavin"
catalog:    true
tags:
    - S3
---



# 概述



python boto上传一个2T大小的对象，产品报HTTP 416 错误码, Requested Range Not Satisfiable， 如下所示：



```
root@node224:~# time python s3_upload.py                                                                                         
[DEBUG]  Enable rgw debug log
{
    "success": ""
} {
    "debug_rgw": "20/20"
}
Traceback (most recent call last):
  File "s3_upload.py", line 118, in <module>
    upload_file_multipart(filepath, keyname, bucket, threadcnt)
  File "s3_upload.py", line 66, in upload_file_multipart
    mp.complete_upload()
  File "/usr/local/lib/python2.7/dist-packages/boto/s3/multipart.py", line 319, in complete_upload
    self.id, xml)
  File "/usr/local/lib/python2.7/dist-packages/boto/s3/bucket.py", line 1807, in complete_multipart_upload
    response.status, response.reason, body)
boto.exception.S3ResponseError: S3ResponseError: 416 Requested Range Not Satisfiable
<?xml version="1.0" encoding="UTF-8"?><Error><Code>InvalidRange</Code><BucketName>test</BucketName><RequestId>tx000000000000000003210-0062bd5539-102b2-default</RequestId><HostId>102b2-default-default</HostId></Error>
real    12m45.518s
user    15m8.592s
sys     11m23.152s
root@node224:~#
```



# 问题过程记录



## 修改参数



```
root@node224:/var/log/ceph# ceph daemon client.radosgw.0 config show | grep multipart
    "rgw_multipart_min_part_size": "5242880",
    "rgw_multipart_part_upload_limit": "600000",
```



这里调整了产品的两个参数，一个是最小分片大小(5MiB)，另外一个是允许的分片数上限(默认10000)




## 测试过程



经过测试，分片上传2T， 50G 和 100G, 50G的成功，100G的就失败了，由此推算出 按8M一个分片上传，单个文件大小介于50G到100G之间，会出现失败，至于文件大小临界点，下文介绍到。



## 问题摸索



按8M一个分片上传，通过上传 50G 、 100G 和 2T文件，开启RGW debug情况下，看到如下信息：


50G：

```
2022-06-30 16:58:45.321050 7f3da254a700 20  bucket index object: .dir.1ed581f4-fc6f-4b86-88e4-b6895841272b.4373.1.54
2022-06-30 16:58:45.323798 7f3da254a700  2 req 23325:0.004960:s3:POST /test/50G.file:init_multipart:completing
2022-06-30 16:58:45.324043 7f3da254a700  2 req 23325:0.005205:s3:POST /test/50G.file:init_multipart:op status=0
2022-06-30 16:58:45.324081 7f3da254a700  2 req 23325:0.005243:s3:POST /test/50G.file:init_multipart:http status=200
2022-06-30 16:58:45.324091 7f3da254a700  1 ====== req done req=0x7f3da25437d0 op status=0 http_status=200 ======
2022-06-30 16:58:47.857037 7f3da254a700 20 CONTENT_LENGTH=8388608
2022-06-30 16:58:47.857060 7f3da254a700 20 CONTENT_TYPE=application/octet-stream
2022-06-30 16:58:47.857063 7f3da254a700 20 HTTP_ACCEPT_ENCODING=identity
2022-06-30 16:58:47.857067 7f3da254a700 20 HTTP_AUTHORIZATION=AWS N2Z4LERBO87Y8G743FZ2:X4b9snKTcsc1uJs5z+N0w/OActc=
2022-06-30 16:58:47.857070 7f3da254a700 20 HTTP_CONTENT_MD5=lplbWNTL9qqpBBtPAMf2rg==
2022-06-30 16:58:47.857077 7f3da254a700 20 HTTP_DATE=Thu, 30 Jun 2022 08:58:47 GMT
2022-06-30 16:58:47.857080 7f3da254a700 20 HTTP_EXPECT=100-Continue
2022-06-30 16:58:47.857082 7f3da254a700 20 HTTP_HOST=172.17.73.178
2022-06-30 16:58:47.857085 7f3da254a700 20 HTTP_USER_AGENT=Boto/2.49.0 Python/2.7.5 Linux/4.14.148-202204291725.git90deb91
2022-06-30 16:58:47.857090 7f3da254a700 20 HTTP_VERSION=1.1
2022-06-30 16:58:47.857093 7f3da254a700 20 QUERY_STRING=uploadId=2~yqR7SqXx1aeg1QMqrrjJMdfNWqqw-cE&partNumber=15
2022-06-30 16:58:47.857108 7f3da254a700 20 REMOTE_ADDR=172.17.73.178
2022-06-30 16:58:47.857110 7f3da254a700 20 REQUEST_METHOD=PUT
2022-06-30 16:58:47.857112 7f3da254a700 20 REQUEST_URI=/test/50G.file
2022-06-30 16:58:47.857116 7f3da254a700 20 SCRIPT_URI=/test/50G.file
2022-06-30 16:58:47.857118 7f3da254a700 20 SERVER_PORT=80
2022-06-30 16:58:47.857122 7f3da254a700  1 ====== starting new request req=0x7f3da25437d0 =====
```



100G:

```
2022-06-30 15:48:03.980991 7f54d680a700  2 RGWDataChangesLog::ChangesRenewThread: start
2022-06-30 15:48:09.436299 7f54bd7d8700 20 CONTENT_LENGTH=1345746
2022-06-30 15:48:09.436313 7f54bd7d8700 20 CONTENT_TYPE=text/xml
2022-06-30 15:48:09.436314 7f54bd7d8700 20 HTTP_ACCEPT_ENCODING=identity
2022-06-30 15:48:09.436315 7f54bd7d8700 20 HTTP_AUTHORIZATION=AWS KAGC5XL83YICQXP0THTQ:tRoonm2iXmUKxPQPVbGzeQRG9g0=
2022-06-30 15:48:09.436317 7f54bd7d8700 20 HTTP_DATE=Thu, 30 Jun 2022 07:48:08 GMT
2022-06-30 15:48:09.436318 7f54bd7d8700 20 HTTP_HOST=10.16.172.224
2022-06-30 15:48:09.436319 7f54bd7d8700 20 HTTP_USER_AGENT=Boto/2.49.0 Python/2.7.12 Linux/4.14.148-202204291725.git90deb91
2022-06-30 15:48:09.436320 7f54bd7d8700 20 HTTP_VERSION=1.1
2022-06-30 15:48:09.436321 7f54bd7d8700 20 QUERY_STRING=uploadId=2~J7YByyru1yeZVWpAHEc4mqbC-tsTkhT
2022-06-30 15:48:09.436325 7f54bd7d8700 20 REMOTE_ADDR=10.16.172.224
2022-06-30 15:48:09.436325 7f54bd7d8700 20 REQUEST_METHOD=POST
2022-06-30 15:48:09.436326 7f54bd7d8700 20 REQUEST_URI=/test/100G.file
2022-06-30 15:48:09.436328 7f54bd7d8700 20 SCRIPT_URI=/test/100G.file
2022-06-30 15:48:09.436328 7f54bd7d8700 20 SERVER_PORT=80
2022-06-30 15:48:09.436329 7f54bd7d8700  1 ====== starting new request req=0x7f54bd7d1860 =====
```



1T



 ```
 2022-06-30 17:29:15.016098 7f0ef6d31700 20 Read xattr: user.rgw.source_zone
 2022-06-30 17:29:15.016102 7f0ef6d31700 15 Encryption mode:
 2022-06-30 17:29:15.049927 7f0ef6530700 20 CONTENT_LENGTH=15728640
 2022-06-30 17:29:15.049948 7f0ef6530700 20 CONTENT_TYPE=application/octet-stream
 2022-06-30 17:29:15.049949 7f0ef6530700 20 HTTP_ACCEPT_ENCODING=identity
 2022-06-30 17:29:15.049951 7f0ef6530700 20 HTTP_AUTHORIZATION=AWS KAGC5XL83YICQXP0THTQ:JIsSkMsbsOSEQCouHX9ZuRFCIWc=
 2022-06-30 17:29:15.049954 7f0ef6530700 20 HTTP_CONTENT_MD5=FLFyNOI3UFQhtkkrjXV1Bw==
 2022-06-30 17:29:15.049955 7f0ef6530700 20 HTTP_DATE=Thu, 30 Jun 2022 09:29:14 GMT
 2022-06-30 17:29:15.049956 7f0ef6530700 20 HTTP_EXPECT=100-Continue
 2022-06-30 17:29:15.049957 7f0ef6530700 20 HTTP_HOST=10.16.172.224
 2022-06-30 17:29:15.049958 7f0ef6530700 20 HTTP_USER_AGENT=Boto/2.49.0 Python/2.7.12 Linux/4.14.148-202204291725.git90deb91
 2022-06-30 17:29:15.049959 7f0ef6530700 20 HTTP_VERSION=1.1
 2022-06-30 17:29:15.049961 7f0ef6530700 20 QUERY_STRING=uploadId=2~1ZV5udTDBC-xcHWguk3Wr4_9U2awOKf&partNumber=4183
 2022-06-30 17:29:15.049969 7f0ef6530700 20 REMOTE_ADDR=10.16.172.224
 2022-06-30 17:29:15.049970 7f0ef6530700 20 REQUEST_METHOD=PUT
 2022-06-30 17:29:15.049971 7f0ef6530700 20 REQUEST_URI=/test/1T.file
 2022-06-30 17:29:15.049972 7f0ef6530700 20 SCRIPT_URI=/test/1T.file
 2022-06-30 17:29:15.049973 7f0ef6530700 20 SERVER_PORT=80
 2022-06-30 17:29:15.049975 7f0ef6530700  1 ====== starting new request req=0x7f0ef6529860 =====
 ```





2T  

```
2022-06-30 14:30:21.497960 7fc3b4ecd700 20  bucket index object: .dir.a36a7e3f-2952-4680-9b9c-8497fa9a2c73.5279.1.70
2022-06-30 14:30:21.500356 7fc3b4ecd700 15 omap_set obj=default.rgw.buckets.non-ec:a36a7e3f-2952-4680-9b9c-8497fa9a2c73.5279.1__multipart_2T.file.2~i1zS2MRnaC6rvPxD36aRh-rsRPnkJHW.meta key=part.00015316
2022-06-30 14:30:21.501809 7fc3b4ecd700  2 req 15319:13.402100:s3:PUT /test/2T.file:put_obj:completing
2022-06-30 14:30:21.501872 7fc3b4ecd700  2 req 15319:13.402162:s3:PUT /test/2T.file:put_obj:op status=0
2022-06-30 14:30:21.501876 7fc3b4ecd700  2 req 15319:13.402167:s3:PUT /test/2T.file:put_obj:http status=200
2022-06-30 14:30:21.501890 7fc3b4ecd700  1 ====== req done req=0x7fc3b4ec6820 op status=0 http_status=200 ======
2022-06-30 14:30:21.501944 7fc3b4ecd700  1 civetweb: 0x55556651f620: 10.16.172.224 - - [30/Jun/2022:14:30:08 +0800] "PUT /test/2T.file?uploadId=2~i1zS2MRnaC6rvPxD36aRh-rsRPnkJHW&partNumber=15316 HTTP/1.1" 200 231 - Boto/2.49.0 Python/2.7.12 Linux/4.14.148-202204291725.git90deb91
2022-06-30 14:30:22.031011 7fc3b2ec9700  5 NOTICE: call to do_aws4_auth_completion
2022-06-30 14:30:22.031098 7fc3b2ec9700  5 NOTICE: call to do_aws4_auth_completion
2022-06-30 14:30:22.139835 7fc3b96d6700 20 CONTENT_LENGTH=134217728
2022-06-30 14:30:22.139849 7fc3b96d6700 20 CONTENT_TYPE=application/octet-stream
2022-06-30 14:30:22.139849 7fc3b96d6700 20 HTTP_ACCEPT_ENCODING=identity
2022-06-30 14:30:22.139851 7fc3b96d6700 20 HTTP_AUTHORIZATION=AWS KAGC5XL83YICQXP0THTQ:eGNkLYW1iOtm1x6l5boBiMy+/Co=
2022-06-30 14:30:22.139853 7fc3b96d6700 20 HTTP_CONTENT_MD5=/enggYKBg25PwO3+3iuHYg==
2022-06-30 14:30:22.139855 7fc3b96d6700 20 HTTP_DATE=Thu, 30 Jun 2022 06:30:21 GMT
2022-06-30 14:30:22.139856 7fc3b96d6700 20 HTTP_EXPECT=100-Continue
2022-06-30 14:30:22.139857 7fc3b96d6700 20 HTTP_HOST=10.16.172.224
2022-06-30 14:30:22.139858 7fc3b96d6700 20 HTTP_USER_AGENT=Boto/2.49.0 Python/2.7.12 Linux/4.14.148-202204291725.git90deb91
2022-06-30 14:30:22.139859 7fc3b96d6700 20 HTTP_VERSION=1.1
2022-06-30 14:30:22.139864 7fc3b96d6700 20 QUERY_STRING=uploadId=2~i1zS2MRnaC6rvPxD36aRh-rsRPnkJHW&partNumber=15335
2022-06-30 14:30:22.139869 7fc3b96d6700 20 REMOTE_ADDR=10.16.172.224
2022-06-30 14:30:22.139870 7fc3b96d6700 20 REQUEST_METHOD=PUT
2022-06-30 14:30:22.139871 7fc3b96d6700 20 REQUEST_URI=/test/2T.file
2022-06-30 14:30:22.139871 7fc3b96d6700 20 SCRIPT_URI=/test/2T.file
2022-06-30 14:30:22.139872 7fc3b96d6700 20 SERVER_PORT=80
2022-06-30 14:30:22.139874 7fc3b96d6700  1 ====== starting new request req=0x7fc3b96cf820 =====
```





| file size | chunk size | content length      |
| --------- | ---------- | ------------------- |
| 50G       | 8M         | 670945(约0.64MiB)   |
| 100G      | 8M         | 1345746(约1.28MiB)  |
| 1T        | 8M         | 64MiB               |
| 1T        | 15M        | 34.133MiB           |
| 2T        | 8M         | 134217728(128MiB)   |





# 总结



如果上传较大文件，为了确保成功率，需做如下调整：

* Client端上传时，放大单个分片大小
* ceph 开放参数`rgw_max_put_param_size` 的设置，配置content buffer 的大小，默认是1MB



但参数`rgw_max_put_param_size` 目前是写死在代码里的，更改ceph的这个参数设置是无效的（有实测）。



最终解决方法是：

​     RD更改了 RGWCompleteMultipart 代码，统一了POST 与 GET传参（int RGWCompleteMultipart_ObjStore::post_params()  和 int RGWCompleteMultipart_ObjStore::get_params()），即让Get也听从传递的参数rgw_max_put_param_size；同时将rgw_max_put_param_size参数默认值放大50倍（默认值是 1 * 1024 * 1024）。


在未修改之前，如果要上传1T大小的对象，单个chunk size=8MiB，最低分片大小是 1 * 1024 * 1024 * 1024 / (1 * 1024 * 1024) = 1GiB (因为rgw_max_put_param_size=1 * 1024 * 1024)




# 资料参考


https://blog.csdn.net/wuyan6293/article/details/82115584



# 结语

8.0 8.2的旧版本，对于分片上传，代码写死为10000片，这限制了分片上传的文件大小。
S3Browser等工具，默认分配大小为8M，按照旧版本的10000片，最大80GB的file大小。
 
当前我们将如下参数改为128000片，S3browser可支持到1000GiB，如果需要上传更大的文件，则需要调整分片上传，每个分片的大小，测试验证后确认每个分配64MB可以传6T的文件。
 
为什么将总分片数限制在128000，而不是更大。原因是BigteraJournal的transaction有个限制MaxTransactionNumOps，最大128K个op，再大会crash。而且标准AWS，支持单个对象最大5TB，再大也就不支持了。
 
```
    self.set(section, 'rgw multipart part upload limit', '128000')
    self.set(section, 'rgw max put param size', '52428800')
```


最终，在上述调整情况下， 上传了一个2T(48MiB分片大小)， 3.6T(64MiB分片大小)， 4T(64MiB分片大小) 和 6T(64MiB分片大小)的单个大小的文件，均上传OK：

<p><img class="shadow" src="/img/in-post/big_object_upload.png" width="1200" /></p>

<p><img class="shadow" src="/img/in-post/ui_shows_big_object.png" width="1200" /></p>
