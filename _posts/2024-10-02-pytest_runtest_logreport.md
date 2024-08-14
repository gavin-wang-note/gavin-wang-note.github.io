---
title: pytest hook系列之pytest_runtest_logreport
date: 2024-10-02 23:00:00
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
summary: pytest hook之pytest_runtest_logreport
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_logreport` 是`pytest`框架中的一个钩子函数，它在每个测试项执行完成后、报告生成时被调用，允许我们在每个测试项执行报告生成时插入自定义逻辑。通过这个钩子函数，我们可以在生成的测试报告中添加额外的信息、处理统计数据、生成自定义报告等，从而更好地满足对测试报告进行自定义和扩展。

# 使用场景

1. **记录测试结果**：在生成测试报告时记录和处理每个测试项的结果信息。
2. **处理统计数据**：在生成测试报告时处理和记录统计数据，例如通过率、失败率等。
3. **生成自定义报告**：在生成测试报告时生成自定义格式的报告，例如`JSON`报告、`HTML`报告等。

# 参数

```python
def pytest_runtest_logreport(report):
    # report: 当前测试项的执行报告对象，包含测试项的所有信息和结果
    pass
```

- `report`：当前测试项的执行报告对象，包含测试项的所有信息和结果。

# 示例代码

## 案例一：记录每个测试项的执行结果

目标：在每个测试项的执行报告中记录测试结果，并在测试会话结束时输出统计信息。

步骤：
1. 使用 `pytest_runtest_logreport` 钩子函数。
2. 在钩子函数中记录每个测试项的结果，并在测试会话结束时输出统计信息。

示例代码：

```python
# conftest.py
import pytest

passed_tests = []
failed_tests = []

def pytest_runtest_logreport(report):
    # 记录测试通过和失败的统计数据
    if report.when == 'call':
        if report.outcome == 'passed':
            passed_tests.append(report.nodeid)
        elif report.outcome == 'failed':
            failed_tests.append(report.nodeid)

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
- 在 `pytest_runtest_logreport` 钩子函数中记录每个测试项的结果信息，并更新通过和失败的列表。
- 在 `pytest_sessionfinish` 钩子函数中打印统计数据，显示测试通过和失败的数量。

## 案例二：生成自定义格式的测试报告

目标：在生成测试报告时生成自定义格式的报告，例如`JSON`报告。

步骤：
1. 使用 `pytest_runtest_logreport` 钩子函数生成测试结果。
2. 在钩子函数中处理并生成 `JSON` 报告文件。

示例代码：

```python
# conftest.py
import pytest
import json

test_results = []

def pytest_runtest_logreport(report):
    # 收集测试结果
    if report.when == 'call':
        result = {
            'nodeid': report.nodeid,
            'outcome': report.outcome,
            'duration': report.duration
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
- 在 `pytest_runtest_logreport` 钩子函数中收集每个测试项的结果信息，并记录到 `test_results` 列表中。
- 在 `pytest_sessionfinish` 钩子函数中生成`JSON`格式的测试报告，并保存到文件中。

## 案例三：在测试报告中添加调试和日志信息

目标：在生成测试报告时添加调试信息和日志信息，帮助开发者进行调试和问题定位。

步骤：
1. 使用 `pytest_runtest_logreport` 钩子函数添加调试和日志信息。
2. 在钩子函数中处理并输出相应的调试和日志信息。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test_debug.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def pytest_runtest_logreport(report):
    # 添加调试和日志信息
    if report.when == 'call':
        log_message = f"Test {report.nodeid} {report.outcome.upper()} with duration {report.duration:.4f} seconds."
        logging.debug(log_message)
        print(log_message)

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_runtest_logreport` 钩子函数中添加调试和日志信息，通过 `logging` 模块记录到日志文件中，并输出到控制台。

## 运行和验证

确保目录结构如下：

```shell

```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

### 验证输出信息

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如每个测试项的结果记录、生成的`JSON`报告和调试信息。

### 控制台输出和日志文件示例

**案例一：记录每个测试项的执行结果**

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

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 FAILED
Passed tests: 1
Failed tests: 1


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

**案例二：生成自定义格式的测试报告**

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

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSEDGenerated JSON report with 2 test results.


=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**生成的 JSON 报告内容**

```json
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  2 13:58 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  573 Oct  2 13:58 conftest.py
drwxr-xr-x 2 root root 4096 Oct  2 13:58 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  2 13:56 .pytest_cache/
-rw-r--r-- 1 root root  286 Oct  2 13:58 test_report.json
drwxr-xr-x 3 root root 4096 Oct  2 13:58 tests/
root@Gavin:~/test/hook# cat test_report.json 
[
    {
        "nodeid": "tests/test_example.py::test_example1",
        "outcome": "passed",
        "duration": 0.0001178579987026751
    },
    {
        "nodeid": "tests/test_example.py::test_example2",
        "outcome": "passed",
        "duration": 6.124901119619608e-05
    }
]root@Gavin:~/test/hook#
```

**案例三：在测试报告中添加调试和日志信息**

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

tests/test_example.py::test_example1 PASSEDTest tests/test_example.py::test_example1 PASSED with duration 0.0001 seconds.

tests/test_example.py::test_example2 PASSEDTest tests/test_example.py::test_example2 PASSED with duration 0.0001 seconds.


=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 32
drwxr-xr-x 5 root root 4096 Oct  2 13:59 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  436 Oct  2 13:59 conftest.py
drwxr-xr-x 2 root root 4096 Oct  2 13:59 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  2 13:59 .pytest_cache/
-rw-r--r-- 1 root root 4623 Oct  2 13:59 test_debug.log
drwxr-xr-x 3 root root 4096 Oct  2 13:58 tests/
root@Gavin:~/test/hook# cat test_debug.log 
2024-10-02 13:59:33,783 - Looking for locale `en_US` in provider `faker.providers.address`.
2024-10-02 13:59:33,784 - Provider `faker.providers.address` has been localized to `en_US`.
2024-10-02 13:59:33,785 - Looking for locale `en_US` in provider `faker.providers.automotive`.
2024-10-02 13:59:33,785 - Provider `faker.providers.automotive` has been localized to `en_US`.
2024-10-02 13:59:33,786 - Looking for locale `en_US` in provider `faker.providers.bank`.
2024-10-02 13:59:33,786 - Specified locale `en_US` is not available for provider `faker.providers.bank`. Locale reset to `en_GB` for this provider.
2024-10-02 13:59:33,786 - Looking for locale `en_US` in provider `faker.providers.barcode`.
2024-10-02 13:59:33,786 - Provider `faker.providers.barcode` has been localized to `en_US`.
2024-10-02 13:59:33,787 - Looking for locale `en_US` in provider `faker.providers.color`.
2024-10-02 13:59:33,787 - Provider `faker.providers.color` has been localized to `en_US`.
2024-10-02 13:59:33,788 - Looking for locale `en_US` in provider `faker.providers.company`.
2024-10-02 13:59:33,788 - Provider `faker.providers.company` has been localized to `en_US`.
2024-10-02 13:59:33,788 - Looking for locale `en_US` in provider `faker.providers.credit_card`.
2024-10-02 13:59:33,789 - Provider `faker.providers.credit_card` has been localized to `en_US`.
2024-10-02 13:59:33,789 - Looking for locale `en_US` in provider `faker.providers.currency`.
2024-10-02 13:59:33,789 - Provider `faker.providers.currency` has been localized to `en_US`.
2024-10-02 13:59:33,790 - Looking for locale `en_US` in provider `faker.providers.date_time`.
2024-10-02 13:59:33,790 - Provider `faker.providers.date_time` has been localized to `en_US`.
2024-10-02 13:59:33,790 - Provider `faker.providers.emoji` does not feature localization. Specified locale `en_US` is not utilized for this provider.
2024-10-02 13:59:33,790 - Provider `faker.providers.file` does not feature localization. Specified locale `en_US` is not utilized for this provider.
2024-10-02 13:59:33,790 - Looking for locale `en_US` in provider `faker.providers.geo`.
2024-10-02 13:59:33,791 - Provider `faker.providers.geo` has been localized to `en_US`.
2024-10-02 13:59:33,791 - Looking for locale `en_US` in provider `faker.providers.internet`.
2024-10-02 13:59:33,791 - Provider `faker.providers.internet` has been localized to `en_US`.
2024-10-02 13:59:33,792 - Provider `faker.providers.isbn` does not feature localization. Specified locale `en_US` is not utilized for this provider.
2024-10-02 13:59:33,792 - Looking for locale `en_US` in provider `faker.providers.job`.
2024-10-02 13:59:33,792 - Provider `faker.providers.job` has been localized to `en_US`.
2024-10-02 13:59:33,793 - Looking for locale `en_US` in provider `faker.providers.lorem`.
2024-10-02 13:59:33,793 - Provider `faker.providers.lorem` has been localized to `en_US`.
2024-10-02 13:59:33,795 - Looking for locale `en_US` in provider `faker.providers.misc`.
2024-10-02 13:59:33,795 - Provider `faker.providers.misc` has been localized to `en_US`.
2024-10-02 13:59:33,796 - Looking for locale `en_US` in provider `faker.providers.passport`.
2024-10-02 13:59:33,796 - Provider `faker.providers.passport` has been localized to `en_US`.
2024-10-02 13:59:33,796 - Looking for locale `en_US` in provider `faker.providers.person`.
2024-10-02 13:59:33,797 - Provider `faker.providers.person` has been localized to `en_US`.
2024-10-02 13:59:33,800 - Looking for locale `en_US` in provider `faker.providers.phone_number`.
2024-10-02 13:59:33,800 - Provider `faker.providers.phone_number` has been localized to `en_US`.
2024-10-02 13:59:33,801 - Provider `faker.providers.profile` does not feature localization. Specified locale `en_US` is not utilized for this provider.
2024-10-02 13:59:33,801 - Provider `faker.providers.python` does not feature localization. Specified locale `en_US` is not utilized for this provider.
2024-10-02 13:59:33,801 - Provider `faker.providers.sbn` does not feature localization. Specified locale `en_US` is not utilized for this provider.
2024-10-02 13:59:33,801 - Looking for locale `en_US` in provider `faker.providers.ssn`.
2024-10-02 13:59:33,802 - Provider `faker.providers.ssn` has been localized to `en_US`.
2024-10-02 13:59:33,802 - Provider `faker.providers.user_agent` does not feature localization. Specified locale `en_US` is not utilized for this provider.
2024-10-02 13:59:33,803 - Test tests/test_example.py::test_example1 PASSED with duration 0.0001 seconds.
2024-10-02 13:59:33,804 - Test tests/test_example.py::test_example2 PASSED with duration 0.0001 seconds.
root@Gavin:~/test/hook#
```

### 详细解释

1. **记录测试结果**
   - 使用 `pytest_runtest_logreport` 钩子记录每个测试项的结果信息，并在测试会话结束时打印统计数据。
  
2. **生成自定义格式的测试报告**
   - 在 `pytest_runtest_logreport` 钩子中收集测试结果信息，并在 `pytest_sessionfinish` 钩子生成`JSON`格式的测试报告。

3. **添加调试和日志信息**
   - 在 `pytest_runtest_logreport` 钩子中添加调试和日志信息，通过 `logging` 模块记录到日志文件中，并在控制台输出。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用支持 `pytest_runtest_logreport` 钩子的`pytest`版本。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录你且符合`pytest`命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台和日志文件输出，确认测试报告生成期间的自定义逻辑执行结果符合预期。


# pytest_runtest_makereport 与 pytest_runtest_logreport 的异同点

上一篇文章我介绍了`pytest_runtest_makereport`，那么 `pytest_runtest_makereport` 和 `pytest_runtest_logreport` 这两个钩子函数有哪些异同点呢？

我做了汇集整理，参考如下：

| **特性** | **pytest_runtest_makereport** | **pytest_runtest_logreport** |
|---|---|---|
| **功能概述** | 用于生成每个测试项的执行报告，并允许插入自定义逻辑。 | 监控每个测试项的执行报告生成，并插入额外的日志记录和报告信息。 |
| **触发时机** | 在每个测试项执行后，用于生成执行报告时触发。 | 在每个测试项执行完成后，报告生成时触发。 |
| **传递参数** | `item`：测试项对象。<br>`call`：包含测试调用信息的对象。 | `report`：当前测试项的执行报告对象。 |
| **常见使用场景** | 1. 重写或扩展默认的测试项报告。<br>2. 记录测试的开始时间和结束时间。<br>3. 管理通过和失败的统计数据。 | 1. 添加额外的日志信息到报告中。<br>2. 记录测试结果到外部报告（如 `JSON`, `HTML`）。<br>3. 实现细粒度的日志记录和调试信息。 |
| **关键点差异** | - 主要用于影响或生成报告内容<br>- `item` 和 `call` 提供更多上下文信息。 | - 主要用于记录和监控报告<br>- 使用 `report` 对象直接获取测试项的结果和持续时间。 |
| **是否影响报告生成** | 是，可以影响或重写默认报告内容。 | 否，主要用于记录和添加信息，不影响报告生成。 |

## 示例代码对比

### `pytest_runtest_makereport`

```python
# conftest.py
import pytest
import time
import logging

# 配置日志记录
logging.basicConfig(filename='test_report.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_runtest_setup(item):
    item.start_time = time.time()

def pytest_runtest_makereport(item, call):
    if call.when == 'call':
        duration = time.time() - item.start_time
        log_message = f"Test {item.nodeid} completed in {duration:.4f} seconds."
        logging.info(log_message)
        print(log_message)

# 示例测试文件 `tests/test_example.py`
def test_example1():
    time.sleep(1)
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

### `pytest_runtest_logreport`

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test_debug.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def pytest_runtest_logreport(report):
    if report.when == 'call':
        log_message = f"Test {report.nodeid} {report.outcome.upper()} with duration {report.duration:.4f} seconds."
        logging.debug(log_message)
        print(log_message)

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

通过以上表格及示例代码，我们可以清楚地看到 `pytest_runtest_makereport` 和 `pytest_runtest_logreport` 的异同点。

# 总结

通过详细介绍 `pytest_runtest_logreport` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是记录测试结果、处理统计数据，还是生成自定义格式的测试报告，都能为你提供强大的工具，增强测试报告的灵活性和可调试性。
