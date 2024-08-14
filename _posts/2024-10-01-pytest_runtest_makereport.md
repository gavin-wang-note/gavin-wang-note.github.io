---
title: pytest hook系列之pytest_runtest_makereport
date: 2024-10-01 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-17.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_runtest_makereport
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_makereport` 是`pytest` 框架中的一个钩子函数，它在每个测试项执行后生成测试报告时被调用，允许我们在每个测试项的执行报告生成时插入自定义逻辑。通过这个钩子函数，我们可以在测试报告生成过程中添加额外的信息、处理统计数据、生成自定义报告等，从而更好地满足复杂的测试需求。

# 使用场景

1. **添加额外的报告信息**：在生成测试报告时添加额外的信息，例如测试开始和结束时间、日志信息等。
2. **处理统计数据**：在生成测试报告时处理和记录统计数据，例如通过率、失败率等。
3. **生成自定义报告**：在生成测试报告时生成自定义格式的报告，例如 `HTML` 报告、`JSON` 报告等。

# 参数

```python
def pytest_runtest_makereport(item, call):
    # item: 被采集到的测试项对象，包含测试项的所有信息
    # call: 包含有关测试调用的信息，例如调用关键字、异常信息等
    pass
```

- `item`：被采集到的测试项对象，包含测试项的所有信息。
- `call`：包含有关测试调用的信息，例如调用关键字、异常信息等。

# 示例代码

## 案例一：在测试报告中添加开始和结束时间

目标：在测试报告中添加每个测试项的开始和结束时间，并输出到日志文件。

步骤：
1. 使用 `pytest_runtest_setup` 钩子函数记录测试开始时间。
2. 使用 `pytest_runtest_makereport` 钩子函数记录测试结束时间并添加到报告中。

示例代码：

```python
# conftest.py
import pytest
import logging
import time

# 配置日志记录
logging.basicConfig(filename='test_report.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_runtest_setup(item):
    # 记录测试开始时间
    item.start_time = time.time()

def pytest_runtest_makereport(item, call):
    # 记录测试报告生成时的信息
    if call.when == 'call':
        duration = time.time() - item.start_time
        log_message = f"Test {item.nodeid} completed in {duration:.4f} seconds."
        logging.info(log_message)
        print(log_message)

# 示例测试文件 `tests/test_example.py`
def test_example1():
    time.sleep(1)  # 模拟长时间运行的测试
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_runtest_setup` 钩子函数中记录测试项的开始时间。
- 在 `pytest_runtest_makereport` 钩子函数中记录测试项的结束时间，并添加该信息到日志文件中。

## 案例二：处理测试通过和失败的统计数据

目标：在生成测试报告时处理和记录测试通过和失败的统计数据。

步骤：
1. 使用 `pytest_runtest_makereport` 钩子函数处理测试通过和失败的数据。
2. 在钩子函数中记录统计数据。

示例代码：

```python
# conftest.py
import pytest

passed_tests = []
failed_tests = []

def pytest_runtest_makereport(item, call):
    # 记录测试通过和失败的统计数据
    if call.when == 'call':
        if call.excinfo is None:
            passed_tests.append(item.nodeid)
        else:
            failed_tests.append(item.nodeid)

def pytest_sessionfinish(session, exitstatus):
    # 打印统计数据
    print(f"\nPassed tests: {len(passed_tests)}")
    print(f"Failed tests: {len(failed_tests)}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 5  # 故意的失败用于演示
```

**注释**：
- 在 `pytest_runtest_makereport` 钩子函数中处理测试通过和失败的统计数据，并记录到相应的列表中。
- 在 `pytest_sessionfinish` 钩子函数中打印统计数据，显示测试通过和失败的数量。

## 案例三：生成自定义格式的测试报告

目标：在生成测试报告时生成自定义格式的报告，例如 `HTML` 报告、`JSON` 报告等。

步骤：
1. 使用 `pytest_runtest_makereport` 钩子函数生成自定义格式的测试报告。
2. 在钩子函数中处理并生成报告文件。

示例代码：

```python
# conftest.py
import pytest
import json

test_results = []

def pytest_runtest_makereport(item, call):
    # 收集测试结果
    if call.when == 'call':
        result = {
            'nodeid': item.nodeid,
            'outcome': call.excinfo is None,
            'duration': call.stop - call.start
        }
        test_results.append(result)

def pytest_sessionfinish(session, exitstatus):
    # 生成 JSON 格式的测试报告
    with open('test_report.json', 'w') as f:
        json.dump(test_results, f, indent=4)
    print(f"Generated JSON report with {len(test_results)} test results.")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_runtest_makereport` 钩子函数中收集每个测试项的结果信息，并记录到 `test_results` 列表中。
- 在 `pytest_sessionfinish` 钩子函数中生成 `JSON` 格式的测试报告，并保存到文件中。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
├── test_report.log
└── tests
    └── test_example.py

2 directories, 3 files
root@Gavin:~/test/hook#
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

### 验证输出信息

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如测试执行时间、测试通过和失败的统计数据以及自定义格式的测试报告。

### 控制台输出和日志文件示例

**案例一：在测试报告中添加开始和结束时间**

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

tests/test_example.py::test_example1 Test tests/test_example.py::test_example1 completed in 1.0253 seconds.
PASSED
tests/test_example.py::test_example2 Test tests/test_example.py::test_example2 completed in 0.0006 seconds.
PASSED

=================================================================================================================== 2 passed in 1.05s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  1 13:38 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  571 Oct  1 13:37 conftest.py
drwxr-xr-x 2 root root 4096 Oct  1 13:38 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  1 13:38 .pytest_cache/
-rw-r--r-- 1 root root  194 Oct  1 13:38 test_report.log
drwxr-xr-x 3 root root 4096 Oct  1 13:38 tests/
root@Gavin:~/test/hook# cat test_report.log 
2024-10-01 13:38:09,878 - Test tests/test_example.py::test_example1 completed in 1.0253 seconds.
2024-10-01 13:38:09,880 - Test tests/test_example.py::test_example2 completed in 0.0006 seconds.
root@Gavin:~/test/hook#
```

**案例二：处理测试通过和失败的统计数据**

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
tests/test_example.py::test_example2 FAILED
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
============================================================================================================== 1 failed, 1 passed in 0.11s ==============================================================================================================
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
tests/test_example.py::test_example2 PASSEDGenerated JSON report with 2 test results.


=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  1 13:41 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  587 Oct  1 13:41 conftest.py
drwxr-xr-x 2 root root 4096 Oct  1 13:41 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  1 13:41 .pytest_cache/
-rw-r--r-- 1 root root  279 Oct  1 13:41 test_report.json
drwxr-xr-x 3 root root 4096 Oct  1 13:40 tests/
]root@Gavin:~/test/hook#
```

**生成的 JSON 报告内容**

```json
root@Gavin:~/test/hook# cat test_report.json 
[
    {
        "nodeid": "tests/test_example.py::test_example1",
        "outcome": true,
        "duration": 0.00010061264038085938
    },
    {
        "nodeid": "tests/test_example.py::test_example2",
        "outcome": true,
        "duration": 9.894371032714844e-05
    }
]root@Gavin:~/test/hook#
```

### 详细解释

1. **添加开始和结束时间**
   - 使用 `pytest_runtest_setup` 钩子记录测试项的开始时间，使用 `pytest_runtest_makereport` 钩子记录测试项的结束时间，并将信息存储到日志文件中。
  
2. **处理测试通过和失败的统计数据**
   - 在 `pytest_runtest_makereport` 钩子中，根据测试结果将测试项记录到通过或失败的列表中，使用 `pytest_sessionfinish` 钩子打印统计数据。

3. **生成自定义格式的测试报告**
   - 在 `pytest_runtest_makereport` 钩子中收集测试结果信息，使用 `pytest_sessionfinish` 钩子生成`JSON`格式的测试报告。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的`pytest`版本支持 `pytest_runtest_makereport` 钩子。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，配置文件和测试文件如 `test_example.py` 放在 `tests` 目录你且符合`pytest`命名规则。

3. **清理 pytest 缓存**

   - 通过`pytest --cache-clear`清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行 `pytest`并查看控制台和日志文件输出，确认测试报告生成期间的自定义逻辑执行结果符合预期。


# 总结

通过详细介绍`pytest_runtest_makereport`钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是添加开始和结束时间、处理测试通过和失败的统计数据，还是生成自定义格式的测试报告，都能为你提供强大的工具，增强测试报告的灵活性和可调试性。
