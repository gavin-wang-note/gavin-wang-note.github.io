---
layout:     post
title:      "python 读取yaml文件抛UnicodeDecodeError异常"
subtitle:   "python 读取yaml文件抛UnicodeDecodeError异常"
date:       2024-06-12
author:     "Gavin Wang"
catalog:    true
img: "/medias/featureimages/173.jpg"
summary: python读取yaml文件注意点
categories:
    - [python]
tags:
    - python
---

# 概述

读取yaml配置文件，在Linux上运行OK，但相同代码在Windows上运行报错：

```shell
ImportError while loading conftest 'D:\workspace\API\conftest.py'.
conftest.py:6: in <module>
    from utils.config import CONFIG
utils\config.py:16: in <module>
    CONFIG=read_config()
utils\config.py:13: in read_config
    config = yaml.safe_load(file)
C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\yaml\__init__.py:125: in safe_load
    return load(stream, SafeLoader)
C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\yaml\__init__.py:79: in load
    loader = Loader(stream)
C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\yaml\loader.py:34: in __init__
    Reader.__init__(self, stream)
C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\yaml\reader.py:85: in __init__
    self.determine_encoding()
C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\yaml\reader.py:124: in determine_encoding
    self.update_raw()
C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\yaml\reader.py:178: in update_raw
    data = self.stream.read(size)
E   UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 208: illegal multibyte sequence
```

# 解决过程

源码内容参考如下：

```python
root@Gavin:~/automation/API/utils# cat config.py 
import os
import yaml

def get_config_path():
    # 根据项目结构返回config.yaml的路径。假定此文件位于与configs目录平行的utils目录中
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, 'configs', 'config.yaml')

def read_config():
    # 读取配置文件并返回配置数据
    config_path = get_config_path()
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

CONFIG=read_config()
root@Gavin:~/automation/API/utils# 
```

Linux下运行正常，Windows运行抛如上所示的异常。

解决方法是：

修改rb模式读取指定文件，即修改 `with open(config_path, 'r') as file:` 为 `with open(config_path, 'rb') as file:`

参考如下：

```python
root@Gavin:~/automation/API/utils# cat config.py 
import os
import yaml

def get_config_path():
    # 根据项目结构返回config.yaml的路径。假定此文件位于与configs目录平行的utils目录中
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, 'configs', 'config.yaml')

def read_config():
    # 读取配置文件并返回配置数据
    config_path = get_config_path()
    with open(config_path, 'rb') as file:
        config = yaml.safe_load(file)
    return config

CONFIG=read_config()
root@Gavin:~/automation/API/utils# 
```

# 说明

默认情况下，`Python` 在不同操作系统上可能会使用不同的文件编码。例如，`Linux` 通常使用 `UTF-8`，而 `Windows` 通常使用 `GBK` 或其他编码。

在最初的代码中，使用 `r` 模式打开文件可能会导致在 `Windows` 上发生 `UnicodeDecodeError`，因为文件内容可能并不是以 `Windows` 默认的编码（例如 `GBK`）存储的。为了避免这个问题，你需要明确指定文件打开时使用的编码。

除了上面的修改方法外，也可以指定编码：

修改 `with open(config_path, 'r') as file:` 为 `with open(config_path, 'r', encoding='utf-8') as file:` 可以更明确地指定文件的编码。

另外：

使用 `rb`（以二进制模式读取文件）可以避免编码问题，因为此模式下，文件内容不会被解码。但是，文件内容作为二进制数据传递给 `yaml.safe_load` 并不是一个好办法，因为 `yaml.safe_load` 期望的是字符数据而非字节数据。

