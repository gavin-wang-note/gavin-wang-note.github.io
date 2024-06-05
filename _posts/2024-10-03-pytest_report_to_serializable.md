---
title: pytest hook系列之pytest_report_to_serializable
date: 2024-10-03 23:00:00
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
summary: pytest hook之pytest_report_to_serializable
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_report_to_serializable` 是`pytest`框架中的一个钩子函数，允许我们将测试报告转换为可序列化的数据结构，例如，将报告对象转换为字典。通过这个钩子函数，我们可以将测试报告转换为`JSON`等格式，从而方便在不同环境中传输和处理测试结果。

# 使用场景

1. **生成 JSON 测试报告**：将测试报告转换为`JSON`格式，便于通过`HTTP API`等方式传输和处理。
2. **跨系统集成**：将测试报告转换为可序列化的数据结构，便于在不同系统之间集成和传输。
3. **自定义报告格式**：根据需要生成自定义格式的报告，便于分析和展示测试结果。

#### 参数

```python
def pytest_report_to_serializable(config, report):
    # config: pytest 配置对象，可以获取一些配置相关的信息
    # report: 当前测试项的执行报告对象，包含测试项的所有信息和结果
    pass
```

- `config`：`pytest`配置对象，可以获取一些配置相关的信息。
- `report`：当前测试项的执行报告对象，包含测试项的所有信息和结果。

# 示例代码

## 案例一：将测试报告转换为 JSON 格式

目标：在测试执行完成后，将测试报告转换为`JSON`格式并保存到文件中。

步骤：
1. 使用 `pytest_report_to_serializable` 钩子将测试报告转换为`JSON`格式。
2. 在测试会话结束时，将转换好的`JSON`数据写入文件。

示例代码：

```python
# conftest.py
import pytest
import json

# 存储所有的测试报告
test_reports = []

# 将测试报告转换为字典（可序列化的格式）
def pytest_report_to_serializable(config, report):
    return {
        'nodeid': report.nodeid,
        'outcome': report.outcome,
        'longrepr': str(report.longrepr) if report.failed else '',
        'sections': report.sections,
        'duration': report.duration,
    }

# 通过 pytest 的 logreport 钩子将报告追加到列表中
def pytest_runtest_logreport(report):
    # 检查call阶段报告
    if report.when == 'call':
        serialized_report = pytest_report_to_serializable(None, report)
        test_reports.append(serialized_report)
        print(f"Collected report for {report.nodeid}")  # 调试信息

# 在测试会话结束时，将收集的报告写入 JSON 文件
def pytest_sessionfinish(session, exitstatus):
    print(f"Collected {len(test_reports)} reports.")  # 调试信息
    # 将转换后的测试报告保存为 JSON 文件
    with open('test_report_serializable.json', 'w') as f:
        json.dump(test_reports, f, indent=4)
    print(f"Generated JSON report with {len(test_reports)} test results.")


# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 5  # 故意的失败用于演示
```

**注释**：
- 在 `pytest_report_to_serializable` 钩子中，将测试报告对象转换为字典格式。
- 在 `pytest_sessionfinish` 钩子结束时，将转换后的测试报告写入`JSON`文件中。

## 案例二：通过 HTTP 传输测试结果

目标：在测试执行完成后，通过`HTTP`将测试结果发送到远程服务器。

步骤：
1. 使用 `pytest_report_to_serializable` 钩子将测试报告转换为`JSON`格式。
2. 在测试会话结束时，通过`HTTP POST`请求将`JSON`数据发送到远程服务器。

示例代码：

```python
# conftest.py
import pytest
import json
import requests

test_reports = []

def pytest_report_to_serializable(config, report):
    # 将测试报告转换为字典（可序列化的格式）
    serialized_report = {
        'nodeid': report.nodeid,
        'outcome': report.outcome,
        'longrepr': str(report.longrepr) if report.failed else '',
        'sections': report.sections,
        'duration': report.duration,
    }
    test_reports.append(serialized_report)
    return serialized_report

def pytest_sessionfinish(session, exitstatus):
    # 将转换后的测试报告通过 HTTP POST 请求发送到远程服务器
    url = 'http://example.com/api/test_report'
    response = requests.post(url, json=test_reports)
    if response.status_code == 200:
        print(f"Successfully sent test report to {url}")
    else:
        print(f"Failed to send test report to {url} with status code {response.status_code}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_report_to_serializable` 钩子中，将测试报告对象转换为字典格式，并保存到 `test_reports` 列表中。
- 在 `pytest_sessionfinish` 钩子结束时，通过`HTTP POST`请求将`JSON`数据发送到指定的远程服务器。

## 案例三：生成自定义格式的测试报告

目标：在测试执行完成后，将测试报告转换为自定义格式并保存到文件中。

步骤：
1. 使用 `pytest_report_to_serializable` 钩子将测试报告转换为自定义格式。
2. 在测试会话结束时，将转换好的自定义数据写入文件。

示例代码：

```python
# conftest.py
import pytest

test_reports = []

def pytest_report_to_serializable(config, report):
    # 将测试报告转换为自定义格式（这里以示例格式展示）
    return {
        'test_id': report.nodeid,
        'status': report.outcome,
        'error': str(report.longrepr) if report.failed else None,
        'details': report.sections,
        'time_taken': report.duration,
    }

def pytest_runtest_logreport(report):
    # 检查call阶段报告，并将其序列化保存到列表中
    if report.when == 'call':
        serialized_report = pytest_report_to_serializable(None, report)
        test_reports.append(serialized_report)

def pytest_sessionfinish(session, exitstatus):
    # 将转换后的自定义格式测试报告保存为文本文件
    with open('custom_test_report.txt', 'w') as f:
        for report in test_reports:
            f.write(f"Test ID: {report['test_id']}\n")
            f.write(f"Status: {report['status']}\n")
            if report['error']:
                f.write(f"Error: {report['error']}\n")
            f.write(f"Details: {report['details']}\n")
            f.write(f"Duration: {report['time_taken']:.4f} seconds\n")
            f.write("\n")
    print(f"Generated custom test report with {len(test_reports)} test results.")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_report_to_serializable` 钩子中，将测试报告对象转换为自定义格式的字典。
- 在 `pytest_sessionfinish` 钩子结束时，将转换后的自定义格式测试报告写入文本文件中。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

### 验证输出信息

根据不同的案例，控制台和文件输出应包含自定义逻辑的结果，如生成的`JSON`报告、通过`HTTP`传输的测试结果和自定义格式的测试报告。

### 控制台输出和文件示例

**案例一：生成 JSON 格式的测试报告**

```plaintext
root@Gavin:~/test/hook# pytest -s -v --cache-clear
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
Collected 2 reports.
Generated JSON report with 2 test results.


======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example2 _____________________________________________________________________________________________________________________

    def test_example2():
>       assert 2 + 2 == 5
E       assert (2 + 2) == 5

tests/test_example.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example2 - assert (2 + 2) == 5
============================================================================================================== 1 failed, 1 passed in 0.10s ==============================================================================================================
root@Gavin:~/test/hook# 
```

**生成的 JSON 报告内容**

```json
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  3 14:33 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root 1184 Jun  3 14:33 conftest.py
drwxr-xr-x 2 root root 4096 Jun  3 14:33 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  3 14:33 .pytest_cache/
-rw-r--r-- 1 root root  502 Jun  3 14:33 test_report_serializable.json
drwxr-xr-x 3 root root 4096 Jun  3 14:22 tests/
root@Gavin:~/test/hook# cat test_report_serializable.json 
[
    {
        "nodeid": "tests/test_example.py::test_example1",
        "outcome": "passed",
        "longrepr": "",
        "sections": [],
        "duration": 8.914095815271139e-05
    },
    {
        "nodeid": "tests/test_example.py::test_example2",
        "outcome": "failed",
        "longrepr": "def test_example2():\n>       assert 2 + 2 == 5\nE       assert (2 + 2) == 5\n\ntests/test_example.py:5: AssertionError",
        "sections": [],
        "duration": 0.00018477503908798099
    }
]root@Gavin:~/test/hook#
```

**案例二：通过 HTTP 传输测试结果**

```plaintext
root@Gavin:~/test/hook# pytest -s -v --cache-clear
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

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSEDFailed to send test report to http://example.com/api/test_report with status code 404


=================================================================================================================== 2 passed in 0.90s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：生成自定义格式的测试报告**

```plaintext
root@Gavin:~/test/hook# pytest -s -v --cache-clear
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

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSEDGenerated custom test report with 2 test results.


=================================================================================================================== 2 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

**生成的自定义格式测试报告内容**

```plaintext
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  3 14:38 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root 1283 Jun  3 14:38 conftest.py
-rw-r--r-- 1 root root  198 Jun  3 14:38 custom_test_report.txt
drwxr-xr-x 2 root root 4096 Jun  3 14:38 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  3 14:38 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  3 14:35 tests/
root@Gavin:~/test/hook# cat custom_test_report.txt 
Test ID: tests/test_example.py::test_example1
Status: passed
Details: []
Duration: 0.0001 seconds

Test ID: tests/test_example.py::test_example2
Status: passed
Details: []
Duration: 0.0001 seconds

root@Gavin:~/test/hook#
```

### 详细解释

1. **生成 JSON 格式**
   - 使用 `pytest_report_to_serializable` 钩子将测试报告转换为`JSON`格式，并在 `pytest_sessionfinish` 钩子中将`JSON`数据写入文件，便于持久化和后续处理。

2. **HTTP 传输测试结果**
   - 使用 `pytest_report_to_serializable` 钩子将测试报告转换为`JSON`格式，并在 `pytest_sessionfinish` 钩子中通过`HTTP POST`请求将测试结果发送到远程服务器。这样可以实现测试结果的集中管理和远程分析。

3. **生成自定义格式的测试报告**
   - 使用 `pytest_report_to_serializable` 钩子将测试报告转换为自定义格式，并在 `pytest_sessionfinish` 钩子中将自定义格式的测试报告写入文件。这个方法允许我们根据具体需求生成特定格式的报告，便于进一步的分析和展示。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的`pytest`版本支持 `pytest_report_to_serializable` 钩子。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录内且符合`pytest`命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台和文件输出，确认测试报告生成期间的自定义逻辑执行结果符合预期。

### 总结

通过详细介绍 `pytest_report_to_serializable` 钩子的使用场景、参数及应用示例，你可以更好地理解和使用这个钩子函数。无论是生成`JSON`格式的报告、通过`HTTP`传输测试结果，还是生成自定义格式的报告，都能为你提供强大的工具，增强测试报告的灵活性和可调试性。希望这些内容对你有所帮助
