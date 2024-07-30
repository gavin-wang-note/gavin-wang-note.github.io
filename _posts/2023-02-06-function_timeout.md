---
layout:     post
title:      "Python下使用function timeout"
subtitle:   "function timeout"
date:       2023-02-06
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
    - [Automation]
tags:
    - python
    - Automation 
---


# 概述

今天在编写S3 multipart upload相关test case时，碰到一个Quota相关场景，即上传S3 Object超过了Bucket Quota 的设定，导致thread hang住，无法退出。
一般情况下，无Quota下，程序正常上传Object并退出，但碰到这种有Quota场景的，一旦超额，用例对应multipart upload function 卡住。
为此，本文介绍如果给function增加timeout，正常退出，且不影响后续程序的运行。


#  实践

直接上解决方法.

如下，为多线程中的使用


```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from func_timeout import func_set_timeout
import time
import func_timeout

@func_set_timeout(1)
def task():
    while True:
        print('hello world')
        time.sleep(1)


if __name__ == '__main__':
    try:
        task()
    except func_timeout.exceptions.FunctionTimedOut:
        print('task func_timeout')

``` 

Program output:

```shell
hello world
task func_timeout
``` 

这样就可以不用中断主程序，可以继续执行后面的任务，也可以在超时后加上重试等功能，这就看自己需要了。


对应的测试用例基类：

```python
    if option in ['upload']:
        try:
            self.upload_file_multipart(file_path, object_name, bucket, thread_cnt)
        except func_timeout.exceptions.FunctionTimedOut:
            logging.debug("--  Upload failed by FunctionTimedOut")
``` 

被 call function 头部增加装饰器 `func_set_timeout`

```python

    @func_set_timeout(5)
    def upload_file_multipart(self, file_path, object_name, bucket, thread_cnt):
        filesize = os.stat(file_path).st_size
        mp = bucket.initiate_multipart_upload(object_name)
        q = self.init_queue(filesize)
        for i in range(0, thread_cnt):
            t = threading.Thread(target=self.upload_chunk, args=(file_path, mp, q, i))
            t.setDaemon(True)
            t.start()
        q.join()
        mp.complete_upload()
``` 

如上，完美解决掉thread hang死问题。


参考：

https://zhuanlan.zhihu.com/p/39743129
