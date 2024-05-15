---
title: python json、ujson、orjson性能大比拼
date: 2019-01-01 10:59:27
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: python json、ujson、orjson性能PK
categories:
    - [python]
tags:
    - python
---

# Overview

之前写过一篇关于ujson的文章[链接](https://gavin-wang-note.github.io/2014/12/06/python_ujson/), 在2018年又出现了个orjson，性能更强悍，趁着元旦假期浅学一下。

# json vs ujson vs orjson

以下是基于功能和性能对比 json（Python标准库），ujson 和 orjson 的简要总结：


| 特性/性能     | `json`                    | `ujson`                                          | `orjson`                                        |
|--------------|--------------------------|--------------------------------------------------|-------------------------------------------------|
| 速度         | 标准                     | 比标准json快，但不是最快                          | 在大多数情况下最快                              |
| 兼容性       | Python标准库，广泛支持    | 高，但可能在细微处有所差别                        | 高，但一些非标准JSON类型（如datetime）处理有特定方式 |
| 定制化支持    | 有限                     | 有限                                              | 多（例如，可以直接序列化datetime）              |
| 安装         | 内置，无需安装             | 需要安装                                          | 需要安装                                        |
| Unicode处理  | 有时可能较慢              | 优化良好                                          | 优化良好                                        |
| 维护和社区支持 | Python社区支持            | 相对较好，但可能不如标净json库                     | 活跃的开发和支持                                |

* json 是 Python 内置的 JSON 处理库，足够通用且易于使用，但可能在处理非常大的数据或者要求高性能的场景中不是最佳选择。
* ujson（Ultra JSON）通过使用 C 语言编写的优化代码来提高性能，是一个速度更快的 JSON 库。但它可能在某些细节（如解析和错误处理）上表现得不如 Python 的标准 json 库那样温和。
* orjson 是当前最快的 JSON 库之一, 特别是在序列化方面。它提供了额外的功能，比如直接序列化 datetime 对象，而不需要先转换为字符串。但可能需要安装 Rust 编译器来编译安装。


# Benchkark

为了比较 json、ujson 和 orjson 的性能，我们可以编写一个 benchmark 脚本来对每种库的序列化（转换成 JSON）和反序列化（从 JSON 转换回来）进行测试。

这是一个基本的测试脚本例子：

```python
import time
import json
import ujson
import orjson
import random
import string

def random_string(length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

data = {
    "name": random_string(10),
    "array": list(range(10000)),
    "nested": {
        "subarray": list(range(100)),
        "value": random_string(100)
    }
}

# 确保所有 json 库都可以对同一份数据进行序列化和反序列化
assert data == json.loads(json.dumps(data))
assert data == ujson.loads(ujson.dumps(data))
assert data == orjson.loads(orjson.dumps(data))

start_time = time.time()
json.dumps(data)
json_dump_time = time.time() - start_time

start_time = time.time()
json.loads(json.dumps(data))
json_load_time = time.time() - start_time

start_time = time.time()
ujson.dumps(data)
ujson_dump_time = time.time() - start_time

start_time = time.time()
ujson.loads(ujson.dumps(data))
ujson_load_time = time.time() - start_time

start_time = time.time()
orjson.dumps(data)
orjson_dump_time = time.time() - start_time

start_time = time.time()
orjson.loads(orjson.dumps(data))
orjson_load_time = time.time() - start_time

print(f"json dump: {json_dump_time:.5f}s, load: {json_load_time:.5f}s")
print(f"ujson dump: {ujson_dump_time:.5f}s, load: {ujson_load_time:.5f}s")
print(f"orjson dump: {orjson_dump_time:.5f}s, load: {orjson_load_time:.5f}s")
```

此脚本分别对 json、ujson 和 orjson 执行序列化（dump）和反序列化（load）操作，然后记录并打印出各操作所需的时间。这将帮助我们了解在处理相同数据量时各库的性能情况。

运行效果参考如下：

```shell
root@Gavin:~/test# python3 benchmark.py 
json dump: 0.00040s, load: 0.00066s
ujson dump: 0.00020s, load: 0.00049s
orjson dump: 0.00005s, load: 0.00018s
root@Gavin:~/test# 
```

安装官方的说法：

ujson是json的3倍性能，orjson是json的6倍性能。

```shell
ujson is 3 times faster than the standard json library
orjson is over 6 times faster than the standard json library
```


请注意：

* 测试结果可能会因环境不同而有所出入。
* 理想情况下，应当在一致的环境下运行多次测试，并计算平均值以获得更精确的性能对比。


# 参考链接

/* 2022年，增加了下文内容：*/

国外有个博主写了一个压测脚本，详细信息请点击[链接](https://dollardhingra.com/blog/python-json-benchmarking/)。

为了防止链接失效，我贴一下对方的测试Code:

```python
import time
import json
import orjson
import ujson


def benchmark(name, dumps, loads):
    start = time.time()
    for i in range(3000000):
        result = dumps(m)
        loads(result)
    print(name, time.time() - start)


if __name__ == "__main__":
    m = {
        "timestamp": 1556283673.1523004,
        "task_uuid": "0ed1a1c3-050c-4fb9-9426-a7e72d0acfc7",
        "task_level": [1, 2, 1],
        "action_status": "started",
        "action_type": "main",
        "key": "value",
        "another_key": 123,
        "and_another": ["a", "b"],
    }

    benchmark("Python", json.dumps, json.loads)
    benchmark("ujson", ujson.dumps, ujson.loads)

    # orjson only outputs bytes, but often we need unicode:
    benchmark("orjson", lambda s: str(orjson.dumps(s), "utf-8"), orjson.loads)

# OUTPUT:
# Python 12.502133846282959
# ujson 4.428200960159302
# orjson 2.3136467933654785
```
