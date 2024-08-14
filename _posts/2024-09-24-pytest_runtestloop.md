---
title: pytest hook系列之pytest_runtestloop
date: 2024-09-24 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-15.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_runtestloop
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtestloop` 是`pytest`框架中的一个钩子函数，允许我们在测试执行主循环期间插入自定义逻辑。通过这个钩子，我们可以在测试运行的整个过程中实现特定的行为，比如在测试套件的初始化配置、执行和清理阶段使用，帮助我们在测试执行的各个阶段插入自定义逻辑，从而满足复杂的测试需求。

# 使用场景

1. **自定义测试执行逻辑**：在测试执行过程中插入特定的行为，如日志记录、资源监控等。
2. **测试执行控制**：通过插入条件判断，动态控制测试的执行和终止。
3. **全局测试状态管理**：在测试执行期间管理全局状态，如统计测试执行时间、动态调整配置等。

# 参数

```python
def pytest_runtestloop(session):
    # session: pytest 的测试会话对象，包含有关当前测试会话的所有信息
    pass
```

- `session`：`pytest` 的测试会话对象，包含有关当前测试会话的所有信息。

# 示例代码

## 案例一：自定义测试执行逻辑

目标：在测试执行过程中记录每个测试用例的执行时间，并在测试结束时输出统计信息。

步骤：

1. 使用 `pytest_runtestloop` 钩子函数。
2. 在钩子函数中记录每个测试用例的执行时间，并在测试结束时输出统计信息。

示例代码：

```python
# conftest.py
import pytest
import time

# 存储每个测试用例的执行时间
test_durations = {}

def pytest_runtestloop(session):
    # 自定义测试执行逻辑
    for item in session.items:
        start_time = time.time()
        # 执行测试用例
        session.config.hook.pytest_runtest_protocol(item=item, nextitem=None)
        end_time = time.time()
        test_durations[item.nodeid] = end_time - start_time

    # 输出每个测试用例的执行时间
    for nodeid, duration in test_durations.items():
        print(f"{nodeid} executed in {duration:.4f} seconds")

    return True  # 表示钩子成功处理

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    time.sleep(1)  # 模拟长时间运行的测试
    assert 2 + 2 == 4
```

**注释**：

- 在 `pytest_runtestloop` 钩子函数中，记录每个测试用例的执行时间，并在测试结束时输出统计信息。

## 案例二：测试执行控制

目标：根据特定条件终止测试执行，例如当某个测试项失败时停止后续测试。

步骤：
1. 使用 `pytest_runtestloop` 钩子函数。
2. 在钩子函数中检测测试项的执行结果，并根据条件终止测试执行。

示例代码：

```python
# conftest.py
import pytest

def pytest_runtestloop(session):
    for item in session.items:
        # 执行测试用例
        result = session.config.hook.pytest_runtest_protocol(item=item, nextitem=None)
        # 示例条件：如果测试用例失败，则终止后续测试
        if not result:
            print(f"Test {item.nodeid} failed. Terminating further test execution.")
            break

    return True  # 表示钩子成功处理

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 5  # 故意失败的测试
```

**注释**：

- 在 `pytest_runtestloop` 钩子函数中，检测测试项的执行结果，并在测试失败时终止后续测试执行。

## 案例三：全局测试状态管理

目标：在测试执行期间动态调整全局状态，例如根据已有的测试结果调整后续测试的配置。

步骤：
1. 使用 `pytest_runtestloop` 钩子函数。
2. 在钩子函数中根据测试结果动态调整后续测试的配置。

示例代码：

```python
# conftest.py
import pytest

@pytest.fixture(scope="session", autouse=True)
def dynamic_config():
    return {"threshold": 10}

def pytest_runtestloop(session):
    # 初始化全局状态
    global_state = {"passed": 0, "failed": 0, "threshold": 10}

    for item in session.items:
        # 执行测试用例
        session.config.hook.pytest_runtest_protocol(item=item, nextitem=None)
        
        # 检查测试结果并更新全局状态
        if item in session.config.cache.get("failed", set()):
            global_state["failed"] += 1
        else:
            global_state["passed"] += 1

        # 根据全局状态动态调整后续测试的配置
        if global_state["failed"] > global_state["threshold"]:
            print(f"Test failures exceeded threshold. Adjusting further test configuration.")
            global_state["threshold"] = 20  # 示例：动态调整阈值

    return True  # 表示钩子成功处理

# 示例测试文件 `tests/test_example.py`
@pytest.mark.parametrize("x", [0, 1, 2, 3, 4])
def test_example(x):
    assert x % 2 == 0  # 偶数通过，奇数失败
```

**注释**：

- 在 `pytest_runtestloop` 钩子函数中，初始化并更新全局状态，根据测试结果动态调整后续测试的配置。

# 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

## 验证输出信息

根据不同的案例，控制台输出应显示自定义逻辑的结果，如每个测试用例的执行时间、测试终止信息及全局状态调整信息。

## 控制台输出示例

**案例一：自定义测试执行逻辑**

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
tests/test_example.py::test_example2 PASSEDtests/test_example.py::test_example1 executed in 0.0200 seconds
tests/test_example.py::test_example2 executed in 1.0139 seconds


=================================================================================================================== 2 passed in 1.05s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**案例二：测试执行控制**

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

======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example2 _____________________________________________________________________________________________________________________

    def test_example2():
>       assert 2 + 2 == 5  # 故意失败的测试
E       assert (2 + 2) == 5

tests/test_example.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example2 - assert (2 + 2) == 5
============================================================================================================== 1 failed, 1 passed in 0.12s ==============================================================================================================
root@Gavin:~/test/hook# 
```

**案例三：全局测试状态管理**

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
collected 5 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example[0] PASSED
tests/test_example.py::test_example[1] FAILED
tests/test_example.py::test_example[2] PASSED
tests/test_example.py::test_example[3] FAILED
tests/test_example.py::test_example[4] PASSED

======================================================================================================================= FAILURES ========================================================================================================================
____________________________________________________________________________________________________________________ test_example[1] ____________________________________________________________________________________________________________________

x = 1

    @pytest.mark.parametrize("x", [0, 1, 2, 3, 4])
    def test_example(x):
>       assert x % 2 == 0  # 偶数通过，奇数失败
E       assert (1 % 2) == 0

tests/test_example.py:5: AssertionError
____________________________________________________________________________________________________________________ test_example[3] ____________________________________________________________________________________________________________________

x = 3

    @pytest.mark.parametrize("x", [0, 1, 2, 3, 4])
    def test_example(x):
>       assert x % 2 == 0  # 偶数通过，奇数失败
E       assert (3 % 2) == 0

tests/test_example.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example[1] - assert (1 % 2) == 0
FAILED tests/test_example.py::test_example[3] - assert (3 % 2) == 0
============================================================================================================== 2 failed, 3 passed in 0.15s ==============================================================================================================
root@Gavin:~/test/hook# 
```

## 详细解释

1. **自定义测试执行逻辑**
   - 在 `pytest_runtestloop` 钩子函数中，记录每个测试用例的执行时间，并在测试结束时输出统计信息。

2. **测试执行控制**
   - 在 `pytest_runtestloop` 钩子函数中，检测测试项的执行结果，并在测试失败时终止后续测试执行。

3. **全局测试状态管理**
   - 在 `pytest_runtestloop` 钩子函数中，初始化并更新全局状态，根据测试结果动态调整后续测试的配置。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保所使用的是支持 `pytest_runtestloop` 钩子的 `pytest` 版本。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录内且符合 `pytest` 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行 `pytest` 并查看控制台输出，确认自定义逻辑的结果符合预期。

# 总结

通过详细介绍 `pytest_runtestloop` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是自定义测试执行逻辑、测试执行控制，还是全局测试状态管理，都能为你提供强大的工具，满足各种复杂的测试需求。
