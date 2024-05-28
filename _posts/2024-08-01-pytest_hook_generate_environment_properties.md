---
title: 借助pytest hook生成Allure所需的environment.properties文件内容
date: 2024-08-01 13:20:18
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
summary: 借助pytest hook生成Allure所需的environment.properties文件内容，在报告上的overview页面上的ENVIRONMENT位置展示相关自定义信息
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述



为了在使用`pytest`时自动生成一个包含环境和版本信息的`environment.properties`文件，你可以使用`pytest`的钩子函数来在测试会话开始时记录起始时间，以及在测试会话结束时记录终止时间，并计算耗时。然后根据这些信息生成文件。

# pytest hook方案

以下是一个`conftest.py`的示例实现， 借助 `pytest_sessionstart` 和 `pytest_sessionfinish`,代码参考如下：

```python
# Content of conftest.py
import pytest
from datetime import datetime

# 全局变量记录测试开始时间
start_time = datetime.now()

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    global start_time
    start_time = datetime.now()
    # print(f"Testing started at {start_time}")

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    end_time = datetime.now()
    print(f"Testing ended at {end_time}")

    # 计算耗时，包括天数
    duration = end_time - start_time
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    total_time = f"{days}Days {hours}Hours {minutes}Mins {seconds}Sec"

    # 获取环境相关的信息，这些应根据你的实际需要填写或动态获取
    env_info = "IP或域名地址"      # 替换成相关获取函数的调用或逻辑代码
    version_info = "被测版本信息"  # 替换成相关获取函数的调用或逻辑代码

    # 创建 environment.properties 文件并写入收集到的信息
    env_properties = f"""测试环境: {env_info}
被测版本: {version_info}
起始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
终止时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
总计耗时: {total_time}
"""
    with open('environment.properties', 'w') as f:  # 注意这里文件存放的路径，根据实际情况调整
        f.write(env_properties)

    # print(f"Total duration: {total_time}")
```

* 在上述代码中，首先定义了全局变量`start_time`来存储测试会话开始的时间。`pytest_sessionstart`钩子是在测试会话开始的时候调用，此时记录下当前时间。同样地，`pytest_sessionfinish`钩子在整个测试会话结束时被调用，再次获取当前时间，用以计算总的测试持续时间。

* 然后，代入一些需要手动设置的常量变量（如`env_info`和`version_info`）。理想情况下，这些变量可以从配置文件、环境变量、命令行参数或`CI/CD`工具传递的变量中获取。

* 最后，将所有收集到的信息写入`environment.properties`文件中。该文件将在测试会话结束时与测试报告一同生成。如果你希望包含更多的环境信息，你可以按相同的格式将它们添加到文件内容中。


生成的`environment.properties`文件内容参考如下：

```shell
测试环境: IP或域名地址
被测版本: 被测版本信息
起始时间: 2024-08-01 22:51:58
终止时间: 2024-08-01 22:52:02
总计耗时: 0Days 0Hours 0Mins 4Sec
```

# 其他方法

当然，你也可以在类似`run.py`文件中计算用例开始与结束时间，统计代码可参考[这篇文章](https://gavin-wang-note.github.io/2024/07/26/pytest_cases_result_summary/)。

方法多种多样，就看哪种更合适了，如果想多使用`pytest`的特性，可以使用本文的方法。
