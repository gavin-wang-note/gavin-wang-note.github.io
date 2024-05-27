---
title: Python中的序列化与反序列化
date: 2021-03-31 23:00:00
author: Gavin Wang
img: ""
top: true
hide: false
cover: true
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: Python中的序列化与反序列化
categories:
    - [python]
tags:
    - python
---

# Python中的序列化与反序列化

序列化是指将数据结构或对象状态转换成可存储或可传输的格式的过程。反过来，反序列化是将序列化的数据恢复成原有的数据结构或对象状态。

在`Python`中，序列化通常使用`pickle`模块实现，但也可以使用`json、yaml`或`xml`等格式。


# 为什么需要序列化？

* 数据持久性：序列化允许程序将对象状态保存到文件或数据库中，随后可以从文件或数据库中恢复。
* 跨平台数据交换：通过将数据序列化为如JSON这样的通用格式，可以实现不同编程语言之间的数据交换。


# 使用pickle进行序列化与反序列化

`pickle`是`Python`的标准库之一，提供了一个简单的序列化和反序列化`Python`对象的接口。

```python
import pickle

# 定义一个简单的字典作为示例
data = {"a": 1, "b": 2, "c": 3}

# 序列化：将Python对象转换为二进制格式
with open("data.pickle", "wb") as f:
    pickle.dump(data, f)

# 反序列化：从二进制文件中恢复Python对象
with open("data.pickle", "rb") as f:
    loaded_data = pickle.load(f)
    print(loaded_data)  # 输出: {'a': 1, 'b': 2, 'c': 3}
```

**注意：**

`pickle`序列化的数据是`Python`特有的，不适合作为跨语言的数据交换格式。

# 使用json进行序列化与反序列化

`JSON（JavaScript Object Notation）`是一种轻量级的数据交换格式，易于阅读和编写，同时也易于机器解析和生成。`Python`内置的`json`模块可以轻松地处理`JSON`数据。

```python
import json

# 定义一个简单的字典作为示例
data = {"a": 1, "b": 2, "c": 3}

# 序列化：将Python对象转换为JSON格式的字符串
json_str = json.dumps(data)
print(json_str)  # 输出: {"a": 1, "b": 2, "c": 3}

# 反序列化：从JSON格式的字符串恢复Python对象
loaded_data = json.loads(json_str)
print(loaded_data)  # 输出: {'a': 1, 'b': 2, 'c': 3}
```

**优点：**

`JSON`格式是跨平台和语言的，适合用于`Web`开发和服务间的数据交换。

# 约束和限制

* 使用`pickle`时，只有`Python`才能理解`pickle`格式的数据，这对于需要与其他语言交换数据的应用来说是个限制。
* 尽管`json`适合跨语言交换数据，但它不能直接序列化复杂的`Python`对象，如自定义类的实例。


# 安全提示

使用`pickle`加载不信任的数据是不安全的，因为`pickle`在反序列化时，可能会执行序列化数据中包含的任意代码。因此，仅在可信环境中使用`pickle`序列化数据。


# 思维导图

<img class="shadow" src="/img/in-post/Python序列化和反序列化.png" width="800">

<img class="shadow" src="/img/in-post/Python_Serialization_Deserialization.png" width="800">


# 总结

序列化和反序列化是编程中重要的概念，允许程序开发者以一种格式存储对象，以便于后续恢复或在网络中传输。`Python`提供了多种方式进行序列化，选择哪一种取决于具体的应用场景和需求。对于需要跨平台交换数据的情景，建议使用`json`或其他通用数据格式。
