---
title: 动态调整pytest日志文件
date: 2024-08-17 16:59:18
author: Gavin Wang
img: "/img/pytest/pytest-10.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 介绍几种方法来动态的调整pytest的日志文件名称
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

如何让pytest用例执行过程中产生的日志按预期要求命名？

比如按天：`pytest_log_2024_08_17.log`(pytest_log_年_月_日.log)

比如按秒: `pytest_log_2024_08_17_21_10_17.log`(pytest_log_年_月_日_时_分_秒.log)

可以在`pytest.ini`文件中配置么？

很不幸，直接在`pytest.ini`文件中使用变量来动态设置日志文件名称（如日期和时间）是不支持的，因为`pytest.ini`不支持脚本或动态变量。

本文探讨几个方法来解决上述问题。

# 方案1. 使用Pytest的--log-file命令行参数

因为不能直接在`pytest.ini`中实现动态名称，那可以写一个简单的`shell`脚本或批处理文件来生成日期时间字符串，并以此运行`pytest`。以下是一个使用`bash shell`的示例：

```shell
#!/bin/bash

# 生成日期字符串变量
DATE_STR=$(date +"%Y%m%d")  # YYYYMMDD格式
DATE_TIME_STR=$(date +"%Y%m%d_%H%M%S")  # YYYYMMDD_HHMMSS格式

# 使用日期字符串运行pytest，仅包含日期
pytest --log-file=pytest_log_${DATE_STR}.log

# 或者，如果你想包含小时、分钟和秒
pytest --log-file=pytest_log_${DATE_TIME_STR}.log
```


在`Windows`中，可以使用类似的批处理命令来实现，如下为示例`PowerShell`脚本：

```powershell
# 获取当前日期和时间
$timestamp = Get-Date -Format "yyyy_MM_dd_HH_mm_ss"

# 运行pytest并指定日志文件名
pytest --log-file=pytest_log_$timestamp.log
```

# 方案2. 使用Pytest的钩子和环境变量

如果不想在运行测试时每次都手动输入日期和时间，另一个方案是使用环境变量结合`conftest.py`文件来管理这个过程。

设置环境变量并运行pytest

在`Unix-like`系统:

```shell
export PYTEST_LOG_NAME=pytest_log_$(date +%Y%m%d_%H%M%S).log
pytest
```

在`Windows`:

```shell
set PYTEST_LOG_NAME=pytest_log_%date:~0,4%_%date:~5,2%_%date:~8,2%_%time:~0,2%_%time:~3,2%_%time:~6,2%.log
pytest
```


conftest.py文件中使用环境变量

```python
# Content of conftest.py
import os
import pytest

def pytest_configure(config):
    # 取环境变量，如果没设置，默认为'pytest_log.log'
    log_name = os.getenv('PYTEST_LOG_NAME', 'pytest_log.log')

    # 设置日志文件名称
    config.option.log_file = log_name
```

这种方式依赖于一个名为PYTEST_LOG_NAME的环境变量，你可以在运行测试之前设置它。


Windows下运行效果如下：

```shell
D:\test>set PYTEST_LOG_NAME=pytest_log_%date:~0,4%_%date:~5,2%_%date:~8,2%_%time:~0,2%_%time:~3,2%_%time:~6,2%.log

D:\test>pytest
================================================= test session starts =================================================
platform win32 -- Python 3.11.4, pytest-8.0.2, pluggy-1.5.0
rootdir: D:\test
plugins: allure-pytest-2.13.2, Faker-24.0.0, assume-2.4.3, base-url-2.1.0, html-4.1.1, metadata-3.1.1, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0, variables-3.1.0
collected 1 item

test_fixture.py .                                                                                                [100%]

================================================== 1 passed in 0.07s ==================================================

D:\test>dir
 驱动器 D 中的卷是 新加卷
 卷的序列号是 8A1A-9CD0

 D:\test 的目录

2024/08/17  17:41    <DIR>          .
2024/08/17  17:38    <DIR>          .pytest_cache
2024/08/17  17:12               255 conftest.py
2024/08/17  17:41                 0 pytest_log_2024_08_17_17_41_32.log
2024/08/17  17:13               135 test_fixture.py
2024/08/17  17:41    <DIR>          __pycache__
               3 个文件            390 字节
               3 个目录 97,900,556,288 可用字节

D:\test>
```


# 方案3. 纯粹使用Pytest的钩子（通过conftest.py）

创建或编辑你的项目中的`conftest.py`文件，使用`pytest`的钩子函数来修改日志文件名称：

```python
# Content of conftest.py
import pytest
from datetime import datetime

def pytest_configure(config):
    # 生成日期和时间字符串
    date_str = datetime.now().strftime("%Y%m%d")  # YYYYMMDD格式
    date_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")  # YYYYMMDD_HHMMSS格式

    # 设置日志文件路径，这里仅使用日期
    config.option.log_file = f'pytest_log_{date_str}.log'

    # 如果你想使用日期和时间
    # config.option.log_file = f'pytest_log_{date_time_str}.log'
```

Windows下运行效果如下：

```shell
D:\test>dir
 驱动器 D 中的卷是 新加卷
 卷的序列号是 8A1A-9CD0

 D:\test 的目录

2024/08/17  17:38    <DIR>          .
2024/08/17  17:38    <DIR>          .pytest_cache
2024/08/17  17:38               484 conftest.py
2024/08/17  17:38                 0 pytest_log_20240817.log
2024/08/17  17:13               135 test_fixture.py
2024/08/17  17:38    <DIR>          __pycache__
               3 个文件            874 字节
               3 个目录 97,900,552,192 可用字节

D:\test>
```


通过在conftest.py中设置config.option.log_file，你可以动态地设置日志文件的路径和名称。根据你的需要，你可以选择使用包含日期的版本或包含日期和时间的版本。

**注意:**

如果你通过命令行或pytest.ini设置了日志文件路径，此方法可能会覆盖那些设置，所以确保这是你期望的行为。这种方式提供了将日期和时间动态嵌入到日志文件名称中的灵活性。


# 方案4. 动态修改pytest.ini文件内容

比较粗暴了一些，直接修改，如果不存在log_file参数项，直接新增；存在则修改。

```python
import time

from configparser import ConfigParser

# 创建ConfigParser对象
config = ConfigParser()

# 读取pytest.ini文件
config.read('pytest.ini')

# 修改log_file配置项
timestamp = time.strftime("%Y%m%d_%H%M%S")
new_log_file = f"pytest_log_{timestamp}.log"

# 设置新的log_file值
config['pytest']['log_file'] = new_log_file

# 写回修改到pytest.ini文件
with open('pytest.ini', 'w') as configfile:
    config.write(configfile)

print(f"Log file has been updated to: {new_log_file}")
```

上述方法，貌似画蛇添足了，直接使用`pytest`参数`--log-file`貌似更好、更安全(万一代码有误修改错了pytest.ini文件内容)。


# 小结

选择哪种方案，根据自己的实际需求调整。
