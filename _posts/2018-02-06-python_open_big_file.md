---
layout:     post
title:      "Python文件操作：大文件的读"
subtitle:   "Python open big file"
date:       2018-02-06
author:     "Gavin"
catalog:    true
tags:
    - python
---


# 概述



上一篇介绍了文件的open与 with open的区别，此篇介绍下如何读取大文件，避免MemoryError之类的错误（比如说VM内存4G，读取10GiB大小的文件）。





# 文件读取方式



| method      | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| read()      | 一次性**读取整个文件内容**。推荐使用read(size)方法，size越大运行时间越长 |
| readline()  | 每次**读取一行**内容。内存不够时使用，一般不太用             |
| readlines() | 一次性**读取整个文件内容**，并按行返回到list，方便我们遍历   |



从介绍的几种method来看，read() 与  readlines() 都是读取文件的全部内容，遇到大文件不能按常规方法直接使用。





# 实践



## 读取大文件



准备了一个大小为2067MiB的大文件进行测试：



```
root@scaler80:/mnt/code# du -m ./big_file.txt 
2067	./big_file.txt
```



测试脚本如下：



```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import time
import psutil

# from memory_profiler import profile

def time_diff(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        time_diff= end_time - start_time
        print("Time diff : {}".format('%.4f s' % (time_diff)))

    return wrapper


def get_memory_usage(func):
    def wrapper():
        before_used = float(psutil.swap_memory().free) / 1024 / 1024 / 1024
        func()
        after_used = float(psutil.swap_memory().free) / 1024 / 1024 / 1024
        print("Memory diff : {}".format('%.4f GB' % (after_used - before_used)))
    return wrapper

@time_diff
@get_memory_usage
def open_file_test():
    file_name = r"D:\big_file.txt"
    with open(file_name, "r") as f:
        f.read()


if __name__ == "__main__":
    open_file_test()
```





输出结果：



```
root@scaler80:/mnt/code# python time_diff.py
Memory diff : 1.0151 GB
Time diff : 6.3894 s

root@scaler80:/mnt/code# 
```



从测试效果看，整个读取过程，文件占用了1.0151 GB的内存，耗时6.3894秒。

优化一下看看效果：



```
@time_diff
@get_memory_usage
def open_file_test():
    chunk_size = 1024 * 1024
    file_name = r"D:\big_file.txt"
    with open(file_name, "r") as f:
        f.read(chunk_size)
```



执行效果：



```
root@scaler80:/mnt/code# python time_diff.py
Memory diff : 0.0000 GB
Time diff : 0.1323 s
```





再次优化:



```
def chunked_file_reader(file, block_size=1024 * 1024):
    for chunk in iter(partial(file.read, block_size), ''):
        yield chunk


@time_diff
@get_memory_usage
def open_file_test():
    file_name = r"D:\big_file.txt"
    with open(file_name, "r") as f:
        chunked_file_reader(f)
```



效果如下：



```
root@scaler80:/mnt/code# python time_diff.py
Memory diff : 0.0000 GB
Time diff : 0.1168 s

root@scaler80:/mnt/code# 
```



最后两个优化基本上没差。
