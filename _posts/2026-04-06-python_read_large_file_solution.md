---
layout:     post
title:      python read a large file solution
date:       2026-04-06
author:     "Gavin Wang"
catalog:    true
img:
summary: python读取大文件解决方案
categories:
    - [python]
tags:
    - python
---

# Overview

在使用python处理大型文件时，直接使用 `with open` 读取整个文件到内存中可能会导致内存错误或性能问题。

为了解决这些问题，我们可以采纳多种策略，比如逐行读取、分块读取、使用生成器、内存映射等。

# Solution

## 逐行读取文件

逐行读取文件是最常见且简单的处理大文件的方法，这种方法在读取时内存占用较少。

### 示例代码

```python
def read_large_file_line_by_line(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            # 处理每一行
            process_line(line)

def process_line(line):
    # 示例处理函数，可以根据需要修改
    print(line.strip())

# 示例调用
read_large_file_line_by_line('large_file.txt')
```

耗时：

```shell
real	0m5.560s
user	0m0.127s
sys	0m2.420s
root@Gavin:~/tmp/test# 
```

## 分块读取文件

如果每行的大小也很大，或者你想更精细地控制文件读取，分块读取是一个有效的方法。

### 示例代码

```python
def read_large_file_in_chunks(file_path, chunk_size=1024):
    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            # 处理每个块
            process_chunk(chunk)

def process_chunk(chunk):
    # 示例处理函数，可以根据需要修改
    print(chunk)

# 示例调用
read_large_file_in_chunks('large_file.txt', chunk_size=4096)
```

耗时：

```shell
real	0m2.893s
user	0m0.013s
sys	0m0.385s
root@Gavin:~/tmp/test# 
```


## 使用生成器

使用生成器函数可以在读取文件的过程中生成一部分内容，这减少了内存使用并提高了处理效率。

### 示例代码

```python
def read_file_as_generator(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line

def process_using_generator(file_path):
    for line in read_file_as_generator(file_path):
        # 处理每一行
        process_line(line)

def process_line(line):
    # 示例处理函数，可以根据需要修改
    print(line.strip())

# 示例调用
process_using_generator('large_file.txt')
```

耗时：

```shell
real	0m4.693s
user	0m0.276s
sys	0m1.666s
root@Gavin:~/tmp/test# 
```

## 内存映射文件（Memory-Mapped Files）

内存映射文件是一种将文件内容直接映射到进程地址空间的方法，这样你可以像访问内存一样访问文件内容。对于非常大的文件，这种方法特别有效。

### 示例代码

```python
import mmap

def read_large_file_with_mmap(file_path):
    with open(file_path, 'r+b') as file:
        # 创建内存映射对象
        mmapped_file = mmap.mmap(file.fileno(), 0)
        
        # 对文件内容的操作
        while True:
            line = mmapped_file.readline()
            if not line:
                break
            # 处理每一行
            process_line(line.decode('utf-8').strip())
        mmapped_file.close()

def process_line(line):
    # 示例处理函数，可以根据需要修改
    print(line)

# 示例调用
read_large_file_with_mmap('large_file.txt')
```

耗时：

```shell
real	0m5.525s
user	0m0.184s
sys	0m2.591s
root@Gavin:~/tmp/test#
```

## 多进程处理大文件

通过多进程来处理大文件可以加速文件的处理过程。这种方法尤其适用于具有多核的系统。

### 示例代码

```python
from multiprocessing import Process, Queue

def worker(file_path, chunk_size, start, end, queue):
    with open(file_path, 'r') as file:
        file.seek(start)
        chunk = file.read(min(chunk_size, end - start)).splitlines()
        queue.put(chunk)

def process_large_file_with_multiprocessing(file_path, chunk_size=1024, num_workers=4):
    file_size = os.path.getsize(file_path)
    chunk_starts = [i for i in range(0, file_size // 1024, chunk_size)]
    processes = []
    queue = Queue()

    for i in range(len(chunk_starts)):
        start = chunk_starts[i]
        end = chunk_starts[i+1] if i+1 < len(chunk_starts) else file_size
        p = Process(target=worker, args=(file_path, chunk_size, start, end, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not queue.empty():
        chunk = queue.get()
        for line in chunk:
            process_line(line)

def process_line(line):
    # 示例处理函数，可以根据需要修改
    print(line.strip())

# 示例调用
process_large_file_with_multiprocessing('large_file.txt', chunk_size=10000, num_workers=4)
```

耗时：

```shell
real	0m0.048s
user	0m0.042s
sys	0m0.020s
```

# 总结

处理大文件时，可以选择逐行读取、分块读取、使用生成器、内存映射以及多进程处理等方法。每种方法都有其适用的场景，你可以根据具体需求和系统性能选择最适合的方法来处理大文件。

