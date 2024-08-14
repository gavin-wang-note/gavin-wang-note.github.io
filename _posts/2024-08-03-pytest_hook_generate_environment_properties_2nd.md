---
title: 借助pytest hook生成Allure所需的environment.properties文件内容，第二版
date: 2024-08-03 13:20:18
author: Gavin Wang
img: "/img/pytest/pytest-11.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 两天前写过一篇文章，借助pytest hook生成Allure所需的environment.properties文件内容，在报告上的overview页面上的ENVIRONMENT位置展示相关自定义信息，此次更换其他`hook`实现，并增加了用例相关统计信息
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

[上一版](https://gavin-wang-note.github.io/2024/08/01/pytest_hook_generate_environment_properties/)是在`conftest.py`中借助 `pytest_sessionstart` 和 `pytest_sessionfinish`, 本次使用`pytest_configure`,`pytest_sessionfinish`和`pytest_runtest_logreport`三个hook实现。

不废言，直接上代码：

```python
# Content of conftest.py
import os
import pytest
from datetime import datetime
from zoneinfo import ZoneInfo

from utils.config import CONFIG

# 测试环境信息，根据你的实际情况进行修改
BASE_URL = CONFIG['orangehrm_base_url']
TEST_ENVIRONMENT_IP = BASE_URL.split('/')[1:][1]    # 被测环境的IP
PRODUCT_VERSION = BASE_URL.split('/')[1:][2]        # 被测产品的版本

# 初始化统计信息
test_stats = {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0, 'errors': 0, 'broken': 0}

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """
    pytest统计每个测试阶段（setup/call/teardown）的执行结果。
    """
    if report.when == 'call':  # 'call' 阶段代表测试用例的执行阶段
        test_stats['total'] += 1
        if report.passed:
            test_stats['passed'] += 1
        elif report.failed:
            if report.when == "call":
                test_stats['failed'] += 1
        elif report.skipped:
            test_stats['skipped'] += 1
        elif report.broken:
            test_stats['broken'] += 1

def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束时的操作，主要用于统计完成的测试结果信息。
    """
    tz = ZoneInfo("Asia/Shanghai")
    start_time = session.config.start_time # 测试开始时间
    end_time = datetime.now(tz=tz) # 测试结束时间
    duration = end_time - start_time

    # 获取已声明的alluredir命令行参数值
    allure_dir = session.config.getoption('--alluredir')
    if not allure_dir:
        print('Allure results directory not found. Ensure you are using "--alluredir" option with pytest.')
        return


    env_data = {
        'Environment IP': TEST_ENVIRONMENT_IP,
        'Product Version': PRODUCT_VERSION,
        'Test Start Time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
        'Test End Time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
        'Test Duration (seconds)': str(duration.total_seconds()),
        'Total Cases': str(test_stats['total']),
        'Passed Cases': str(test_stats['passed']),
        'Failed Cases': str(test_stats['failed']),
        'Skipped Cases': str(test_stats['skipped']),
        'Brokend Cases': str(test_stats['broken']),
    }

    # 写入环境信息
    if allure_dir:
        with open(os.path.join(allure_dir, 'environment.properties'), 'w') as env_file:
            for key, value in env_data.items():
                env_file.write(f'{key}={value}\n')

# 在配置中添加开始时间
def pytest_configure(config):
    tz = ZoneInfo("Asia/Shanghai")
    config.start_time = datetime.now(tz=tz)
```

生成的`environment.properties`文件内容参考如下：

```shell
Environment IP=192.168.23.130
Product Version=orangehrm-5.6
Test Start Time=2024-08-03 22:54:16
Test End Time=2024-08-03 22:54:17
Test Duration (seconds)=1.165052
Total Cases=9
Passed Cases=9
Failed Cases=0
Skipped Cases=0
Brokend Cases=0
```
