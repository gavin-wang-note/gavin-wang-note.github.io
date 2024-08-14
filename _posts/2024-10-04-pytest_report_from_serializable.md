---
title: pytest hook系列之pytest_report_from_serializable
date: 2024-10-04 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-19.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_report_from_serializable
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_report_from_serializable` 是一个`pytest`提供的钩子函数，用于将可序列化的测试报告数据还原为`pytest`的内部报告对象(将`JSON`或其他格式的报告数据中恢复测试报告)。这个钩子通常与 `pytest_report_to_serializable` 配合使用，可以实现测试报告的持久化和恢复。

# 使用场景

1. **测试报告持久化与恢复**：将测试报告持久化为`JSON`等格式后，可以使用这个钩子将其恢复为`pytest`的内部报告对象。
2. **跨系统集成**：在不同系统之间传递测试报告数据，使用这个钩子可以实现从序列化数据到内部对象的转换。
3. **自定义报告处理**：根据具体需求，自定义测试报告的存储和恢复过程，便于后续处理和分析。

# 参数

```python
def pytest_report_from_serializable(config, data):
    # config: pytest 配置对象，可以获取一些配置相关的信息
    # data: 可序列化的测试报告数据，通常是一个字典
    pass
```

- `config`：`pytest` 配置对象，可以获取一些配置相关的信息。
- `data`：可序列化的测试报告数据，通常是一个字典。

# 示例代码

## 案例一：将 JSON 报告数据还原为内部报告对象

目标：将持久化的`JSON`格式的测试报告数据恢复为`pytest`的内部报告对象，并进行处理。

步骤：
1. 使用 `pytest_report_from_serializable` 钩子将`JSON`报告数据还原为内部报告对象。
2. 在测试执行完成后，使用还原的报告对象进行统计和分析。

完整示例代码

```python
# content of conftest.py
import pytest
import json
from _pytest.reports import TestReport

test_reports = []

def pytest_report_to_serializable(config, report):
    # 将测试报告转换为自定义格式（这里以示例格式展示）
    return {
        'nodeid': report.nodeid,
        'outcome': report.outcome,
        'longrepr': str(report.longrepr) if report.failed else '',
        'sections': report.sections,
        'duration': report.duration,
        'location': report.location,
        'keywords': list(report.keywords)
    }

def pytest_runtest_logreport(report):
    # 检查call阶段报告，并将其序列化保存到列表中
    if report.when == 'call':
        serialized_report = pytest_report_to_serializable(None, report)
        test_reports.append(serialized_report)
        print(f"Collected report for {report.nodeid}")  # 调试信息

def report_from_serializable(data):
    # 手动将字典数据转换为 TestReport 对象
    return TestReport(
        nodeid=data['nodeid'],
        location=data['location'],
        keywords=set(data['keywords']),
        outcome=data['outcome'],
        longrepr=data['longrepr'],
        sections=data['sections'],
        duration=data['duration'],
        when='call'  # 基于我们的序列化与日志阶段之一的假设
    )

def pytest_report_from_serializable(config, data):
    return report_from_serializable(data)

def pytest_sessionfinish(session, exitstatus):
    # 将转换后的自定义格式测试报告保存为 JSON 文件
    with open('test_report_serializable.json', 'w') as f:
        json.dump(test_reports, f, indent=4)
    
    print(f"Generated JSON report with {len(test_reports)} test results.")
    
    # 从 JSON 文件中读取测试报告数据并还原
    with open('test_report_serializable.json', 'r') as f:
        serialized_reports = json.load(f)
    
    restored_reports = [pytest_report_from_serializable(None, data) for data in serialized_reports]

    # 处理还原后的报告对象
    passed_count = sum(1 for report in restored_reports if report.outcome == 'passed')
    failed_count = sum(1 for report in restored_reports if report.outcome == 'failed')
    
    print(f"Restored reports: {len(restored_reports)}")
    print(f"Passed tests: {passed_count}")
    print(f"Failed tests: {failed_count}")
```

```python
# tests/test_example.py
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 5  # 故意的失败用于演示
```

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook#
```

在项目根目录下运行以下命令：

```shell
pytest -s -v --cache-clear
```

### 期望的输出

**控制台输出**

```plaintext
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSEDCollected report for tests/test_example.py::test_example1

tests/test_example.py::test_example2 FAILEDCollected report for tests/test_example.py::test_example2
Generated JSON report with 2 test results.
Restored reports: 2
Passed tests: 1
Failed tests: 1


======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example2 _____________________________________________________________________________________________________________________

    def test_example2():
>       assert 2 + 2 == 5  # 故意的失败用于演示
E       assert (2 + 2) == 5

tests/test_example.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example2 - assert (2 + 2) == 5
============================================================================================================== 1 failed, 1 passed in 0.12s ==============================================================================================================
root@Gavin:~/test/hook#
```

**生成的 JSON 报告内容**

```json
root@Gavin:~/test/hook# cat test_report_serializable.json 
[
    {
        "nodeid": "tests/test_example.py::test_example1",
        "outcome": "passed",
        "longrepr": "",
        "sections": [],
        "duration": 0.0002457569935359061,
        "location": [
            "tests/test_example.py",
            0,
            "test_example1"
        ],
        "keywords": [
            "test_example1",
            "test_example.py",
            "tests",
            "hook",
            ""
        ]
    },
    {
        "nodeid": "tests/test_example.py::test_example2",
        "outcome": "failed",
        "longrepr": "def test_example2():\n>       assert 2 + 2 == 5  # \u6545\u610f\u7684\u5931\u8d25\u7528\u4e8e\u6f14\u793a\nE       assert (2 + 2) == 5\n\ntests/test_example.py:5: AssertionError",
        "sections": [],
        "duration": 0.0002567050396464765,
        "location": [
            "tests/test_example.py",
            3,
            "test_example2"
        ],
        "keywords": [
            "test_example2",
            "test_example.py",
            "tests",
            "hook",
            ""
        ]
    }
]root@Gavin:~/test/hook#
```

### 详细解释

1. **持久化测试报告**：
   - 使用 `pytest_runtest_logreport` 收集测试报告，并使用 `pytest_report_to_serializable` 将其转换为可序列化的格式。
   - 在 `pytest_sessionfinish` 钩子中，将收集到的测试报告保存为`JSON `文件。

2. **恢复测试报告**：
   - 在 `pytest_sessionfinish` 钩子中，从`JSON`文件中读取测试报告数据，并使用 `pytest_report_from_serializable` 钩子将其还原为`pytest`的内部报告对象。
   - 对还原后的报告对象进行统计和分析。

通过上述步骤，我们可以实现测试报告的持久化与恢复，从而满足不同的测试需求和分析需求。希望这些内容能帮助你更好地理解和使用 `pytest_report_from_serializable` 钩子函数。
