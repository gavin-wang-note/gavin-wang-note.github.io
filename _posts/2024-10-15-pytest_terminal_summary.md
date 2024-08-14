---
title: pytest hook系列之pytest_terminal_summary
date: 2024-10-15 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-20.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_terminal_summary
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_terminal_summary` 是 `pytest` 框架中的一个钩子函数，它在测试会话结束时被触发，用于在测试会话结束时向终端报告中添加自定义的总结信息。通过这个钩子函数，我们可以在测试完成后报告一些有用的信息，例如统计数据、失败原因汇总、性能指标等，从而增强测试报告的可读性和信息量。

# 使用场景

1. **测试结果总结**：在测试会话结束时汇总和报告测试结果，例如通过、失败和跳过的测试用例数量。
2. **失败原因汇总**：列出所有失败的测试用例及其失败原因，方便调试和修复。
3. **性能指标报告**：报告测试执行的性能指标，例如总耗时、平均耗时等。
4. **自定义统计信息**：根据项目特定需求，报告例如覆盖率信息、用例分类统计等。

# 参数

```python
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # terminalreporter: TerminalReporter 对象，用于报告终端输出信息
    # exitstatus: 测试会话的退出状态，表示测试运行的结果
    # config: pytest 的配置对象，包含有关当前测试会话的所有信息
    pass
```

- `terminalreporter`：`TerminalReporter` 对象，用于报告终端输出信息。
- `exitstatus`：测试会话的退出状态，表示测试运行的结果。
- `config`：`pytest` 的配置对象，包含有关当前测试会话的所有信息。

# 示例代码

## 案例一：测试结果总结

目标：在测试会话结束时汇总和报告测试结果，例如通过、失败和跳过的测试用例数量。

步骤：
1. 使用 `pytest_terminal_summary` 钩子函数。
2. 在钩子函数中插入统计信息收集和报告代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在测试结束时汇总报告测试结果"""
    total = len(terminalreporter.stats.get('passed', [])) + \
            len(terminalreporter.stats.get('failed', [])) + \
            len(terminalreporter.stats.get('skipped', []))
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    
    terminalreporter.write_sep("=", "Test Summary")
    terminalreporter.write_line(f"Total: {total}")
    terminalreporter.write_line(f"Passed: {passed}")
    terminalreporter.write_line(f"Failed: {failed}")
    terminalreporter.write_line(f"Skipped: {skipped}")

# 示例测试文件 tests/test_example.py
def test_passed():
    assert 1 + 1 == 2

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

**注释**：
- 使用 `terminalreporter.stats` 获取通过、失败和跳过的测试用例列表，并统计数量。
- 在 `pytest_terminal_summary` 钩子函数中使用 `terminalreporter.write_sep` 和 `terminalreporter.write_line` 输出汇总信息。

## 案例二：失败原因汇总

目标：列出所有失败的测试用例及其失败原因，方便调试和修复。

步骤：
1. 使用 `pytest_terminal_summary` 钩子函数。
2. 在钩子函数中插入失败原因收集和报告代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在测试结束时汇总报告失败原因"""
    terminalreporter.write_sep("=", "Failure Summary")
    for report in terminalreporter.stats.get('failed', []):
        terminalreporter.write_line(f"{report.nodeid}: {report.longrepr}")

# 示例测试文件 tests/test_example.py
def test_passed():
    assert 1 + 1 == 2

def test_failed():
    assert 1 + 1 == 3

def test_another_failed():
    assert 2 + 2 == 5
```

**注释**：
- 使用 `terminalreporter.stats.get('failed', [])` 获取所有失败的测试用例报告列表。
- 在 `pytest_terminal_summary` 钩子函数中使用 `terminalreporter.write_line` 输出每个失败测试用例的节点 ID 和详细的失败信息。

## 案例三：性能指标报告

目标：在测试会话结束时，报告测试执行的性能指标，例如总耗时、平均耗时等。

步骤：
1. 使用 `pytest_terminal_summary` 钩子函数。
2. 在钩子函数中插入性能指标计算和报告代码。

示例代码：

```python
# conftest.py
import pytest
import time

test_start_time = None

def pytest_sessionstart(session):
    global test_start_time
    test_start_time = time.time()

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在测试结束时报告性能指标"""
    total_time = time.time() - test_start_time
    num_tests = len(terminalreporter.stats.get('passed', [])) + \
                len(terminalreporter.stats.get('failed', [])) + \
                len(terminalreporter.stats.get('skipped', []))
    avg_time = total_time / num_tests if num_tests > 0 else 0

    terminalreporter.write_sep("=", "Performance Metrics")
    terminalreporter.write_line(f"Total time: {total_time:.2f} seconds")
    terminalreporter.write_line(f"Number of tests: {num_tests}")
    terminalreporter.write_line(f"Average time per test: {avg_time:.2f} seconds")

# 示例测试文件 tests/test_example.py
def test_passed():
    assert 1 + 1 == 2

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

**注释**：
- 在 `pytest_sessionstart` 钩子函数中记录测试会话开始时间。
- 在 `pytest_terminal_summary` 钩子函数中计算并报告总耗时、测试用例数量和平均耗时。

## 案例四：自定义统计信息

目标：根据项目特定需求，在测试会话结束时报告自定义的统计信息，例如覆盖率信息、用例分类统计等。

步骤：
1. 使用 `pytest_terminal_summary` 钩子函数。
2. 在钩子函数中插入自定义统计信息收集和报告代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在测试结束时报告自定义统计信息"""
    num_unit_tests = sum(1 for item in terminalreporter.stats.get('passed', []) if "unit" in item.keywords)
    num_integration_tests = sum(1 for item in terminalreporter.stats.get('passed', []) if "integration" in item.keywords)
    
    terminalreporter.write_sep("=", "Custom Test Statistics")
    terminalreporter.write_line(f"Number of unit tests passed: {num_unit_tests}")
    terminalreporter.write_line(f"Number of integration tests passed: {num_integration_tests}")

# 示例测试文件 tests/test_example.py
import pytest

@pytest.mark.unit
def test_unit_passed():
    assert 1 + 1 == 2

@pytest.mark.integration
def test_integration_passed():
    assert 2 + 2 == 4

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

**注释**：
- 使用 `terminalreporter.stats.get('passed', [])` 获取所有通过的测试用例列表，对其进行统计。
- 使用 `item.keywords` 检查每个测试用例的标记（如 `unit` 和 `integration`）。
- 在 `pytest_terminal_summary` 钩子函数中使用 `terminalreporter.write_line` 输出自定义统计信息。

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

### 执行测试命令

在项目根目录下运行以下命令来查看修改后的测试总结信息：

```shell
pytest -s -v
```

### 验证输出信息

控制台输出应包含自定义的测试结果状态和统计信息。

### 控制台输出示例

**案例一：测试结果总结**

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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
===================================================================================================================== Test Summary ======================================================================================================================
Total: 3
Passed: 1
Failed: 1
Skipped: 1
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_failed - assert (1 + 1) == 3
======================================================================================================== 1 failed, 1 passed, 1 skipped in 0.11s =========================================================================================================
root@Gavin:~/test/hook# 
```

**案例二：失败原因汇总**

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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
==================================================================================================================== Failure Summary ====================================================================================================================
tests/test_example.py::test_failed: def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_failed - assert (1 + 1) == 3
======================================================================================================== 1 failed, 1 passed, 1 skipped in 0.11s =========================================================================================================
root@Gavin:~/test/hook# 
```

**案例三：性能指标报告**

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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================================================== Performance Metrics ==================================================================================================================
Total time: 0.12 seconds
Number of tests: 3
Average time per test: 0.04 seconds
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_failed - assert (1 + 1) == 3
======================================================================================================== 1 failed, 1 passed, 1 skipped in 0.11s =========================================================================================================
root@Gavin:~/test/hook#
```

**案例四：自定义统计信息**

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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================================================ Custom Test Statistics =================================================================================================================
Number of unit tests passed: 0
Number of integration tests passed: 0
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_failed - assert (1 + 1) == 3
======================================================================================================== 1 failed, 1 passed, 1 skipped in 0.11s =========================================================================================================
root@Gavin:~/test/hook#
``` 

### 详细解释和总结

1. **测试结果总结**（案例一）：
   - 使用 `terminalreporter.stats` 获取通过、失败和跳过的测试用例数量。
   - 通过 `terminalreporter.write_sep` 和 `terminalreporter.write_line` 输出汇总信息，提供测试结果一目了然的总结。

2. **失败原因汇总**（案例二）：
   - 列出每个失败的测试用例及其详细的失败原因，方便开发者在测试会话结束后查看和修复问题。
   - 使用 `report.nodeid` 获取测试用例的路径和名称，使用 `report.longrepr` 获取详细的失败信息。

3. **性能指标报告**（案例三）：
   - 通过记录测试会话的开始时间和结束时间，计算总耗时。
   - 统计测试用例数量并计算平均耗时，提升对测试性能的认识。

4. **自定义统计信息**（案例四）：
   - 根据项目需求，统计特定类型（如单元测试、集成测试）的测试用例数量，将统计结果输出在测试会话结束时的总结报告中。
   - 使用 `item.keywords` 检查并统计带有特定标记的测试用例。

# 扩展和优化

1. **颜色显示**：
   - 使用外部库（如 `colorama`）为控制台输出添加颜色，使测试结果和统计信息显得更加直观和美观。

2. **详细失败信息**：
   - 在提供失败原因汇总时，增加更多调试信息，例如堆栈跟踪、上下文环境变量等，帮助快速定位和修复问题。

## 具体扩展示例

### 扩展：使用colorama进行颜色显示

```python
# conftest.py
import pytest
from colorama import Fore, Style, init
import coverage

init(autoreset=True)  # 自动重置颜色

cov = None

def pytest_configure(config):
    global cov
    """在 pytest 配置时，启动覆盖率插件"""
    cov = coverage.Coverage()
    cov.start()

def pytest_sessionfinish(session, exitstatus):
    global cov
    """在测试会话结束时停止覆盖率收集并保存数据"""
    if cov:
        cov.stop()
        cov.save()

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在测试结束时汇总报告统计信息和失败原因"""
    total = len(terminalreporter.stats.get('passed', [])) + \
            len(terminalreporter.stats.get('failed', [])) + \
            len(terminalreporter.stats.get('skipped', []))
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    
    terminalreporter.write_sep("=", f"{Fore.CYAN}Test Summary")
    terminalreporter.write_line(f"{Fore.GREEN}Passed: {passed}")
    terminalreporter.write_line(f"{Fore.RED}Failed: {failed}")
    terminalreporter.write_line(f"{Fore.YELLOW}Skipped: {skipped}")
    
    terminalreporter.write_sep("=", f"{Fore.RED}Failure Summary")
    for report in terminalreporter.stats.get('failed', []):
        terminalreporter.write_line(f"{Fore.RED}{report.nodeid}: {report.longrepr}")

    terminalreporter.write_sep("=", f"{Fore.BLUE}Coverage Summary")
    if cov and cov.get_data().measured_files():
        cov.report(file=terminalreporter._tw)
    else:
        terminalreporter.write_line(f"{Fore.RED}No coverage data to report.")

# 示例测试文件 tests/test_example.py
import pytest

@pytest.mark.unit
def test_unit_passed():
    assert 1 + 1 == 2

@pytest.mark.integration
def test_integration_passed():
    assert 2 + 2 == 4

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

在控制台运行测试，将显示彩色的测试结果和失败原因，加大可读性。

## 进阶扩展：提高信息丰富度和可读性

除了之前提到的基础功能和简单扩展（如颜色显示），我们还可以增加更多实用和高级的功能，例如覆盖率报告、详细统计、测试趋势分析等。这些功能可以帮助开发团队更加全面地了解测试结果，从而做出更好的质量决策。

### 扩展：覆盖率报告和详细统计

通过集成测试覆盖率工具（如 `coverage.py`），我们可以在测试会话结束时显示覆盖率信息和详细统计。这有助于对代码的覆盖率有全面的认识，从而发现未覆盖的代码路径。

### 覆盖率和详细统计示例

**首先，确保安装了 `pytest-cov` 插件和 `coverage` 工具**：

```shell
pip install pytest-cov coverage
```

#### 增强版conftest.py内容

```python
# conftest.py
import pytest
from colorama import Fore, Style, init
import coverage

init(autoreset=True)  # 自动重置颜色

def pytest_configure(config):
    """在 pytest 配置时，启动覆盖率插件"""
    config.option.cov = ['my_project']  # 替换为你项目的主模块
    config.option.cov_report = 'term-missing'

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在测试结束时汇总报告统计信息、失败原因和覆盖率信息"""
    total = len(terminalreporter.stats.get('passed', [])) + \
            len(terminalreporter.stats.get('failed', [])) + \
            len(terminalreporter.stats.get('skipped', []))
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    
    terminalreporter.write_sep("=", f"{Fore.CYAN}Test Summary")
    terminalreporter.write_line(f"{Fore.GREEN}Passed: {passed}")
    terminalreporter.write_line(f"{Fore.RED}Failed: {failed}")
    terminalreporter.write_line(f"{Fore.YELLOW}Skipped: {skipped}")
    
    terminalreporter.write_sep("=", f"{Fore.RED}Failure Summary")
    for report in terminalreporter.stats.get('failed', []):
        terminalreporter.write_line(f"{Fore.RED}{report.nodeid}: {report.longrepr}")
    
    terminalreporter.write_sep("=", f"{Fore.BLUE}Coverage Summary")
    cov = coverage.Coverage()
    cov.load()
    cov.report(file=terminalreporter._tw)
```

#### 示例测试文件 `tests/test_example.py`

```python
import pytest

@pytest.mark.unit
def test_unit_passed():
    assert 1 + 1 == 2

@pytest.mark.integration
def test_integration_passed():
    assert 2 + 2 == 4

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

#### 验证输出信息

确保目录结构如下，并将新版本的 `conftest.py` 和 `tests/test_example.py` 放置在正确的位置，在项目根目录下运行以下命令来执行测试，并启用覆盖率报告:

```shell
pytest --cov=your_project --cov-report=term-missing -s -v
```

#### 控制台输出示例

**控制台输出应包括测试结果、失败原因和覆盖率报告**：

```plaintext
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
=================================================================================================================== Test Summary ===================================================================================================================
Passed: 1
Failed: 1
Skipped: 1
================================================================================================================= Failure Summary ==================================================================================================================
tests/test_example.py::test_failed: def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================================================= Coverage Summary =================================================================================================================
Name                                                                                      Stmts   Miss  Cover
-------------------------------------------------------------------------------------------------------------
.......................... 省略 ...............................
conftest.py                                                                                  23     21     9%
tests/test_example.py                                                                         7      0   100%
-------------------------------------------------------------------------------------------------------------
TOTAL                                                                                     23089  14678    36%
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_failed - assert (1 + 1) == 3
======================================================================================================== 1 failed, 1 passed, 1 skipped in 0.93s =========================================================================================================
root@Gavin:~/test/hook# 
```

#### 详细解释和总结

1. **集成 `pytest-cov` 插件**：
   - 安装 `pytest-cov` 插件以便启用覆盖率报告，并在 `pytest_configure` 钩子函数中配置覆盖范围和输出格式。
   - 在测试命令中使用 `--cov` 和 `--cov-report` 选项开启覆盖率显示。

2. **统计测试结果**：
   - 在 `pytest_terminal_summary` 钩子函数中统计通过、失败和跳过的测试用例数量，并使用 `terminalreporter.write_sep` 和 `terminalreporter.write_line` 输出测试总结。

3. **显示失败原因**：
   - 列出所有失败的测试用例及其详细失败信息，以方便调试和问题修复。使用 `report.nodeid` 和 `report.longrepr` 获取相应的测试用例路径和失败详细信息。

4. **显示覆盖率报告**：
   - 使用 `coverage.py` 工具加载覆盖率数据，并在 `pytest_terminal_summary` 钩子函数中调用 `cov.report` 将覆盖率信息输出到终端。

# 高级功能

- **趋势分析**：
    - 将每次测试执行的结果保存下来，例如保存到服务器或数据库中，以便后续做趋势分析，查看测试结果的变化情况。
  
- **图形报告**：
    - 使用图表工具（如 `Matplotlib、Plotly`）根据收集的 `JSON` 数据生成测试报告的可视化图表，提升数据的直观性。
  
- **邮件通知**：
    - 在测试完成后，自动发送测试结果和报告至开发团队，确保所有成员及时收到测试结果。

# 具体示例：图形报告生成

## 使用 Matplotlib 生成测试报告图表

**确保安装必要的库**：

```shell
pip install matplotlib
```

## 生成图形报告并保存总结

**调整conftest.py生成图表**

通过进一步扩展，我们将生成测试报告的图形表示，并保存总结信息到 `JSON` 文件。我们将使用 `matplotlib` 库来生成测试结果的图表。

## 示例：使用matplotlib生成测试报告图表

```python
# conftest.py
import pytest
from colorama import Fore, Style, init
import json
import matplotlib.pyplot as plt
import coverage

init(autoreset=True)  # 自动重置颜色

cov = None

def pytest_configure(config):
    global cov
    """在 pytest 配置时，启动覆盖率插件"""
    cov = coverage.Coverage()
    cov.start()
    config._test_summary = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'by_module': {},
        'failures': []
    }

def pytest_sessionfinish(session, exitstatus):
    global cov
    """在测试会话结束时停止覆盖率收集并保存数据"""
    if cov:
        cov.stop()
        cov.save()

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    global cov
    """在测试结束时汇总报告统计信息、失败原因和覆盖率信息，并保存报告和结果图表"""
    summary = config._test_summary
    stats = terminalreporter.stats

    summary['total'] = sum(len(stats.get(stat, [])) for stat in ['passed', 'failed', 'skipped'])
    summary['passed'] = len(stats.get('passed', []))
    summary['failed'] = len(stats.get('failed', []))
    summary['skipped'] = len(stats.get('skipped', []))
    
    for stat in ['passed', 'failed', 'skipped']:
        for report in stats.get(stat, []):
            module = report.location[0]
            if module not in summary['by_module']:
                summary['by_module'][module] = {'passed': 0, 'failed': 0, 'skipped': 0}
            summary['by_module'][module][stat] += 1
            
            if stat == 'failed':
                summary['failures'].append({
                    'name': report.nodeid,
                    'reason': str(report.longrepr)
                })

    terminalreporter.write_sep("=", f"{Fore.CYAN}Test Summary")
    terminalreporter.write_line(f"{Fore.GREEN}Passed: {summary['passed']}")
    terminalreporter.write_line(f"{Fore.RED}Failed: {summary['failed']}")
    terminalreporter.write_line(f"{Fore.YELLOW}Skipped: {summary['skipped']}")
    
    terminalreporter.write_sep("=", f"{Fore.RED}Failure Summary")
    for report in stats.get('failed', []):
        terminalreporter.write_line(f"{Fore.RED}{report.nodeid}: {report.longrepr}")
    
    terminalreporter.write_sep("=", f"{Fore.BLUE}Coverage Summary")
    if cov and cov.get_data().measured_files():
        cov.report(file=terminalreporter._tw)
    else:
        terminalreporter.write_line(f"{Fore.RED}No coverage data to report.")
    
    terminalreporter.write_sep("=", f"{Fore.MAGENTA}Module-wise Summary")
    for module, counts in summary['by_module'].items():
        terminalreporter.write_line(f"{module}: Passed: {counts['passed']}, Failed: {counts['failed']}, Skipped: {counts['skipped']}")
    
    # 生成图表并保存为文件
    labels = ['Passed', 'Failed', 'Skipped']
    sizes = [summary['passed'], summary['failed'], summary['skipped']]
    colors = ['green', 'red', 'yellow']
    
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Test Results Distribution')
    plt.savefig('test_results_distribution.png')
    plt.close()

    # 保存总结为 JSON 文件
    with open('test_summary_report.json', 'w') as f:
        json.dump(summary, f, indent=4)

# 示例测试文件 tests/test_example.py
import pytest

@pytest.mark.unit
def test_unit_passed():
    assert 1 + 1 == 2

@pytest.mark.integration
def test_integration_passed():
    assert 2 + 2 == 4

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

## 运行和验证

在项目根目录下运行以下命令来执行测试，启用覆盖率报告并生成图表：

```shell
pytest --cov=your_project --cov-report=term-missing -s -v
```

**控制台输出示例**：

```plaintext
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
=================================================================================================================== Test Summary ===================================================================================================================
Passed: 1
Failed: 1
Skipped: 1
================================================================================================================= Failure Summary ==================================================================================================================
tests/test_example.py::test_failed: def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================================================= Coverage Summary =================================================================================================================
Name                                                                                      Stmts   Miss  Cover
-------------------------------------------------------------------------------------------------------------
.....................
conftest.py                                                                                  58     55     5%
tests/test_example.py                                                                         7      0   100%
-------------------------------------------------------------------------------------------------------------
TOTAL                                                                                     23124  14712    36%
=============================================================================================================== Module-wise Summary ================================================================================================================
tests/test_example.py: Passed: 1, Failed: 1, Skipped: 1
```

### 验证图表和 JSON 文件

**生成的饼图 `test_results_distribution.png` 示例**：

<img class="shadow" src="/img/in-post/test_results_distribution.png" width="600">


**生成的 JSON 总结报告 `test_summary_report.json` 内容示例**：

```json
root@Gavin:~/test/hook# cat test_summary_report.json 
{
    "total": 3,
    "passed": 1,
    "failed": 1,
    "skipped": 1,
    "by_module": {
        "tests/test_example.py": {
            "passed": 1,
            "failed": 1,
            "skipped": 1
        }
    }
}root@Gavin:~/test/hook#
```

### 详细解释和总结

通过这些扩展和优化，我们提供了更加丰富和详细的测试报告信息：

1. **分类统计和详细报告**：
   - 通过分类统计和详细记录失败原因，帮助开发者更快速识别和解决问题。

2. **图形表示**：
   - 使用 `matplotlib` 生成测试结果分布的饼图，直观展示通过、失败和跳过的测试用例比例。

3. **输出到文件**：
   - 将测试总结信息和失败原因保存到 `JSON` 文件中，便于后续分析和报告生成。

# 总结

通过上述扩展，我们利用 `pytest_terminal_summary` 钩子极大地增强了测试报告的丰富性、可读性和实用性。这些详细的测试报告和图形表示，可以帮助开发团队更好地理解测试结果，做出更好的质量决策。希望这些内容对你有所帮助，使你能够更好地优化和扩展你的测试流程和报告。

