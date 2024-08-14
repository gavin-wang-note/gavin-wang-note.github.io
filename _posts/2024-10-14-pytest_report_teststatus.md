---
title: pytest hook系列之pytest_report_teststatus
date: 2024-10-14 23:00:00
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
summary: pytest hook之pytest_report_teststatus
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_report_teststatus` 是`pytest`框架中的一个钩子函数，用于自定义测试结果的状态报告，它在每个测试用例执行完毕后被触发，以确定测试结果的显示状态、简短标记和详细描述。通过这个钩子函数，我们可以修改测试用例的状态显示（例如修改默认的 “PASSED”、“FAILED”、 “SKIPPED”等状态）、结果输出格式和报告统计信息，从而更加符合特定项目的需求或增强报告的可读性。

# 使用场景

1. **自定义状态显示**：根据特定条件或需求，自定义测试结果的状态显示，如用不同的标记或颜色区分结果。
2. **增强报告可读性**：提供更详细的测试结果描述，增加报告信息的可读性和调试性。
3. **项目特定需求**：定制化测试报告，满足特定项目的需求，例如标记特定的测试类型或环境信息。
4. **统计信息**：统计不同类型或不同状态的测试用例数量，生成自定义统计报告。

# 参数

```python
def pytest_report_teststatus(report, config):
    # report: TestReport 对象，包含当前测试用例的结果信息
    # config: pytest 的配置对象，包含有关当前测试会话的所有信息
    pass
```

- `report`：`TestReport` 对象，包含当前测试用例的结果信息。
- `config`：`pytest` 的配置对象，包含有关当前测试会话的所有信息。

# 示例代码

## 案例一：自定义状态显示

目标：根据特定条件自定义测试结果的状态显示和标记。

步骤：
1. 使用 `pytest_report_teststatus` 钩子函数。
2. 在钩子函数中插入自定义状态和标记显示代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_report_teststatus(report, config):
    """自定义测试结果状态显示"""
    if report.when == "call" and report.passed:
        return "passed", "P", "Test Passed!"
    elif report.failed:
        return "failed", "F", "Test Failed!"
    elif report.skipped:
        return "skipped", "S", "Test Skipped!"

# 示例测试文件 tests/test_example.py
def test_passed():
    assert 1 + 1 == 2

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

**注释**：
- 在 `pytest_report_teststatus` 钩子中，自定义测试结果的状态显示、简短标记和详细描述。
- `report.when == "call" and report.passed` 用于检查测试用例是否通过。
- `report.failed` 和 `report.skipped` 则用于检查测试失败和跳过的状态。

## 案例二：增强报告可读性

目标：提供更详细的测试结果描述，增加报告信息的可读性。

步骤：
1. 使用 `pytest_report_teststatus` 钩子函数。
2. 在钩子函数中插入详细描述代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_report_teststatus(report, config):
    """增强测试结果报告的可读性"""
    if report.when == "call" and report.passed:
        return "passed", "P", "Test Passed! Function: {}".format(report.location[2])
    elif report.failed:
        return "failed", "F", "Test Failed! Function: {}".format(report.location[2])
    elif report.skipped:
        return "skipped", "S", "Test Skipped! Reason: {}".format(report.longrepr)

# 示例测试文件 tests/test_example.py
def test_passed():
    assert 1 + 1 == 2

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

**注释**：
- `report.location[2]` 提供测试用例的函数名称。
- `report.longrepr` 提供更详细的失败或跳过原因描述。

## 案例三：项目特定需求

目标：定制化测试报告，满足特定项目需求，例如标记特定的测试类型或环境信息。

步骤：
1. 使用 `pytest_report_teststatus` 钩子函数。
2. 在钩子函数中插入项目特定需求的状态显示代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_report_teststatus(report, config):
    """项目特定需求的测试结果标记"""
    if report.when == "call" and report.passed:
        if "integration" in report.keywords:
            return "integration_passed", "IP", "Integration Test Passed!"
        else:
            return "unit_passed", "UP", "Unit Test Passed!"
    elif report.failed:
        return "failed", "F", "Test Failed! Function: {}".format(report.location[2])
    elif report.skipped:
        return "skipped", "S", "Test Skipped! Reason: {}".format(report.longrepr)

# 示例测试文件 tests/test_example.py
import pytest

@pytest.mark.integration
def test_integration_passed():
    assert 1 + 1 == 2

def test_unit_passed():
    assert 2 + 2 == 4

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

**注释**：
- 使用 `report.keywords` 检查测试用例是否具有特定标记（如 `integration`）。
- 根据测试用例标记，自定义返回不同的状态和标记显示。

## 案例四：统计信息

目标：统计不同类型或不同状态的测试用例数量，生成自定义统计报告。

步骤：
1. 使用 `pytest_report_teststatus` 钩子函数。
2. 在钩子函数中插入统计信息记录代码。

示例代码：

```python
# conftest.py
import pytest

results_count = {"passed": 0, "failed": 0, "skipped": 0}

def pytest_report_teststatus(report, config):
    """统计不同状态的测试用例数量"""
    global results_count
    
    if report.when == "call":
        if report.passed:
            results_count["passed"] += 1
            return "passed", "P", "Test Passed!"
        elif report.failed:
            results_count["failed"] += 1
            return "failed", "F", "Test Failed!"
    elif report.skipped:
        results_count["skipped"] += 1
        return "skipped", "S", "Test Skipped!"

def pytest_sessionfinish(session, exitstatus):
    """在会话结束时输出统计信息"""
    print("\nTest Results Summary:")
    print(f"Passed: {results_count['passed']}")
    print(f"Failed: {results_count['failed']}")
    print(f"Skipped: {results_count['skipped']}")

# 示例测试文件 tests/test_example.py
def test_passed():
    assert 1 + 1 == 2

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

**注释**：
- 使用 `results_count` 字典记录通过、失败和跳过的测试用例数量。
- 在 `pytest_report_teststatus` 钩子中更新统计信息。
- 在 `pytest_sessionfinish` 钩子函数中输出统计结果汇总。

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

在项目根目录下运行以下命令来查看修改后的测试结果和统计信息：

```shell
pytest -s -v
```

### 验证输出信息

控制台输出应包含自定义的测试结果状态和统计信息。

### 控制台输出示例

**案例一：自定义状态显示**

```plaintext
root@Gavin:~/test/hook# pytest -s -v
==================================================================================== test session starts ====================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                           

tests/test_example.py::test_passed Test Passed!
tests/test_example.py::test_failed Test Failed!
tests/test_example.py::test_skipped Test Skipped! (Skipping this test)

========================================================================================= FAILURES ==========================================================================================
________________________________________________________________________________________ test_failed ________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================== short test summary info ==================================================================================
Test Failed! tests/test_example.py::test_failed - assert (1 + 1) == 3
========================================================================== 1 failed, 1 passed, 1 skipped in 0.11s ===========================================================================
root@Gavin:~/test/hook# 
```

### 控制台输出示例

**案例二：增强报告可读性**

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

tests/test_example.py::test_passed Test Passed! Function: test_passed
tests/test_example.py::test_failed Test Failed! Function: test_failed
tests/test_example.py::test_skipped Test Skipped! Reason: ('/root/test/hook/tests/test_example.py', 10, 'Skipped: Skipping this test') (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================================================ short test summary info ================================================================================================================
Test Failed! Function: test_failed tests/test_example.py::test_failed - assert (1 + 1) == 3
======================================================================================================== 1 failed, 1 passed, 1 skipped in 0.11s =========================================================================================================
root@Gavin:~/test/hook#
```

**案例三：项目特定需求**

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
collected 4 items                                                                                                                                                                                                                                       

tests/test_example.py::test_integration_passed Integration Test Passed!
tests/test_example.py::test_unit_passed Unit Test Passed!
tests/test_example.py::test_failed Test Failed! Function: test_failed
tests/test_example.py::test_skipped Test Skipped! Reason: ('/root/test/hook/tests/test_example.py', 14, 'Skipped: Skipping this test') (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:11: AssertionError
=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py:3
  /root/test/hook/tests/test_example.py:3: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.integration

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================================ short test summary info ================================================================================================================
Test Failed! Function: test_failed tests/test_example.py::test_failed - assert (1 + 1) == 3
===================================================================================== 1 failed, 1 skipped, 1 warning, 1 integration_passed, 1 unit_passed in 0.11s ======================================================================================
root@Gavin:~/test/hook#
```

**案例四：统计信息**

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

tests/test_example.py::test_passed Test Passed!
tests/test_example.py::test_failed Test Failed!
tests/test_example.py::test_skipped SKIPPED (Skipping this test)
Test Results Summary:
Passed: 1
Failed: 1
Skipped: 0


======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:7: AssertionError
================================================================================================================ short test summary info ================================================================================================================
Test Failed! tests/test_example.py::test_failed - assert (1 + 1) == 3
======================================================================================================== 1 failed, 1 passed, 1 skipped in 0.11s =========================================================================================================
root@Gavin:~/test/hook#
```

### 详细解释和总结

1. **自定义状态显示**（案例一）：
   - 通过 `pytest_report_teststatus` 钩子函数自定义测试结果状态、简短标记和详细描述，使测试输出更符合项目需求和开发者习惯。
   - 例如，将通过状态标记为 `P`，失败标记为 `F`，跳过标记为 `S`。

2. **增强报告可读性**（案例二）：
   - 提供更详细的测试结果描述，包括具体的失败原因、测试用例函数名等，帮助开发者快速了解测试结果。
   - 使用 `report.location[2]` 获取测试用例的函数名称，将其包含在返回描述中。

3. **项目特定需求**（案例三）：
   - 根据项目需求自定义测试报告，例如使用 `report.keywords` 检查特定标记（如 `integration`）。
   - 根据测试用例标记，自定义返回不同的状态和标记显示。这可以让特定类型的测试用例（如单元测试、集成测试）在报告中更加显眼。

4. **统计信息**（案例四）：
   - 使用全局字典 `results_count` 统计通过、失败和跳过的测试用例数量，将统计信息输出到控制台总结中。
   - 在 `pytest_sessionfinish` 钩子函数中输出统计结果汇总，帮助开发者了解整体测试状态。

### 扩展功能和优化

- **颜色显示**：
  - 通过使用外部库（如 `colorama`）增强输出，增加颜色显示，使测试结果更具可读性和美观性。

- **动态状态标记**：
  - 实现根据自定义逻辑动态生成状态标记，例如根据测试执行时间或运行环境生成不同的标记。

- **详细失败信息**：
  - 在测试失败时，提供更详细的错误信息，例如堆栈跟踪、上下文环境变量等，帮助快速定位问题。

### 具体扩展示例

#### 扩展：使用colorama进行颜色显示

```python
# conftest.py
import pytest
from colorama import Fore, Style, init

init(autoreset=True)  # 自动重置颜色

def pytest_report_teststatus(report, config):
    """使用颜色自定义测试结果状态显示"""
    if report.when == "call" and report.passed:
        return "passed", f"{Fore.GREEN}P{Style.RESET_ALL}", f"{Fore.GREEN}Test Passed!{Style.RESET_ALL}"
    elif report.failed:
        return "failed", f"{Fore.RED}F{Style.RESET_ALL}", f"{Fore.RED}Test Failed!{Style.RESET_ALL}"
    elif report.skipped:
        return "skipped", f"{Fore.YELLOW}S{Style.RESET_ALL}", f"{Fore.YELLOW}Test Skipped!{Style.RESET_ALL}"

# 示例测试文件 tests/test_example.py
def test_passed():
    assert 1 + 1 == 2

def test_failed():
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

在控制台运行测试，将显示彩色的测试结果状态，增强可读性。

### 进一步步骤

- **综合使用**：
  - 可以将以上案例综合使用，以满足项目不同层面需求的测试报告，例如同时自定义状态显示、增强报告可读性并输出统计信息。

- **配置文件**：
  - 提供配置文件（如 `pytest.ini`），使用户可以通过配置文件启用或禁用特定功能，提高灵活性和可维护性。

# 总结

通过 `pytest_report_teststatus` 钩子函数，我们可以自定义测试结果的状态显示、简短标记和详细描述，从而增强报告的可读性和项目的特定需求。本文详细介绍了钩子的使用场景、参数及具体案例，并提供了完整的示例代码和详细解释，帮助读者更好地理解和应用这个功能。
