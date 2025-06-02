---
title: 日志模块DEBUG日志
date: 2026-12-19 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 三方模块大量DEBUG日志记录，容易湮灭有效日志
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

在使用`pytest`期间，由于安装了一些三方模块，诸如`matplotlib，faker，pyppeteer， asyncio，websockets`等，在`pytest`记录日志文件时，如果日志级别是`DEBUG`，发现最后生成的日志内容中有不少三方模块产生的`DEBUG`日志，比如说执行了一个测试用例，结果本用例记录的内容10来行，但其他三方模块`DEBUG`日志大几千行。

# 现象

如下面记录到的`pytest`在执行用例过程中产生的日志文件内容：

```ini
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'IHDR' 57 9
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'pHYs' 78 351
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'IDAT' 78 364
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'IHDR' 16 13
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'sBIT' 41 4
2026-12-19 23:19:57 [PngImagePlugin.py:778 ] [DEBUG] b'sBIT' 41 4 (unknown)
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'pHYs' 57 9
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'IDAT' 78 364
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing BlpImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing BmpImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing BufrStubImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing CurImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing DcxImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing DdsImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing FitsStubImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing FlifImagePlugin
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing FpxImagePlugin: No module named 'FpxImagePlugin'
```

上面只是一小部分，实际上会出现大量重复内容，造成日志文件内容爆长且`size`较大。

# 解决方法

如果`pytest`记录日志级别是`INFO`的，上面三方模块的`DEBUG`日志就不会被记录到，但仅有`INFO`级别日志是不够的，有时还是需要`DEBUG`级别的日志的。如何对三方模块的`DEBUG log`进行抑制，是本文要解决的内容。

比如上面记录到的:

```ini
2026-12-19 23:19:57 [PngImagePlugin.py:198 ] [DEBUG] STREAM b'IDAT' 78 364
2026-12-19 23:19:57 [Image.py:405 ] [DEBUG] Importing BlpImagePlugin
```

这里出现了两个`py`文件：`PngImagePlugin.py`和`Image.py`，说明是这两个文件产生了`DEBUG log`，那我们要先找到这两个文件:

```ini
/usr/local/lib64/python3.12/site-packages/PIL/Image.py
/usr/local/lib64/python3.12/site-packages/PIL/PngImagePlugin.py
```

说明这两个文件隶属于`PIL`模块，是`PIL`模块产生了`DEBUG`日志了，找到了文件了，就好进行抑制了。

# DEBUG LOG 抑制方法

在`conftest.py`文件中进行抑制，代码参考如下：

```python
import logging

logging.getLogger('PIL').setLevel(logging.INFO)
```

下图模块也是相同的解决方法:

```python
import logging

# 设置log level为INFO，避免pytest记录到下述模块的DEBUG日志
logging.getLogger('faker').setLevel(logging.INFO)
logging.getLogger('matplotlib').setLevel(logging.INFO)
logging.getLogger('asyncio').setLevel(logging.INFO)
logging.getLogger('pyppeteer').setLevel(logging.INFO)
logging.getLogger('websockets').setLevel(logging.INFO)
logging.getLogger('PIL').setLevel(logging.INFO)
```


