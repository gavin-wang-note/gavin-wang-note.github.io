---
title: python ujson介绍
date: 2016-12-06 10:59:27
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: python ujson入门
categories:
    - [python]
tags:
    - python
---

ujson 是一个优化后的 JSON 库，由于它使用优化后的 C 库，因此它比 Python 内建的 json 模块具有更高的性能，尤其在处理大数据时，这个优势尤其显著。

# 安装 ujson

可以使用 pip 来安装 ujson：

```bash
pip install ujson
```

# 基本用法

ujson 的基本用法和 Python 内建的 json 模块十分相似。

你可以使用 ujson.dumps() 将 Python 对象转换成 JSON 字符串：

```python
import ujson

data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# 转换为 JSON 字符串
json_str = ujson.dumps(data)
print(json_str)  # 输出: {"name":"John","age":30,"city":"New York"}
```

逆向操作，ujson.loads() 可以把 JSON字符串转换为 Python 对象：

```python
import ujson

# 假设我们有以下 JSON 字符串
json_str = '{"name":"John","age":30,"city":"New York"}'

# 使用 ujson.loads() 解析 JSON 字符串
data = ujson.loads(json_str)
print(data)  # 输出: {'name': 'John', 'age': 30, 'city': 'New York'}
```

在这个例子中，ujson.loads() 方法接收一个 JSON 字符串，并将其抓换回相应的 Python 对象，这里是一个字典。

# 文件操作

ujson 也支持直接从文件读取和写入 JSON 数据。

写入 JSON 数据到文件：

```python
import ujson

data = {
    "name": "Jane",
    "age": 25,
    "city": "Los Angeles"
}

# 写入 JSON 数据到文件
with open('data.json', 'w') as f:
    ujson.dump(data, f)
```

从文件中读取 JSON 数据：

```python
import ujson

# 从文件中读取 JSON 数据
with open('data.json', 'r') as f:
    data = ujson.load(f)
    print(data)  # 输出: {'name': 'Jane', 'age': 25, 'city': 'Los Angeles'}
```

# 性能

虽然 ujson 提供了与内建的 json 模块类似的接口，但它的主要优势在于性能。在处理庞大或复杂的 JSON 数据时，ujson 的读写速度通常要比 json 模块快很多。

# 注意事项

* 尽管 ujson 在性能上有显著优势，但是其对于 JSON 格式的容错能力略逊于内置的 json 模块。
* ujson 默认情况下会以一个紧凑的格式输出 JSON 字符串，去除了不必要的空格和换行。如果需要更可读的格式，可以使用 indent 参数实现格式化输出：

```python

json_str_pretty = ujson.dumps(data, indent=4)
print(json_str_pretty)
```

在写入和读取文件时，你需要确保文件的打开模式（读取为 'r'，写入为 'w'）和处理的数据类型（文本或二进制）相匹配。

# 总结

ujson 是处理 JSON 数据的高性能库，因此尤其适合于性能要求较高的应用，如大数据处理、实时系统等。它易于使用，因此几乎可以无缝替换内置的 json 模块，让开发者可以在不牺牲代码可读性的情况下获得更佳性能。

更多关于ujson信息， 请参考[官方链接](https://pycopy.readthedocs.io/en/latest/library/ujson.html)。
