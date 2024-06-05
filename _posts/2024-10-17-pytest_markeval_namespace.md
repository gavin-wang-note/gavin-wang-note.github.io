---
title: pytest hook系列之pytest_markeval_namespace
date: 2024-10-17 23:00:00
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
summary: pytest hook之pytest_markeval_namespace
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_markeval_namespace` 是 `pytest` 框架中的一个钩子函数，用于在自定义标记表达式的评估过程中向命名空间中注入额外的变量或函数。通过这个钩子函数，我们可以在运行测试时传递更多的信息，并在测试标记表达式的评估过程中灵活地使用这些信息。这个钩子特别适用于需要根据环境或者上下文信息动态更改测试集合的场景。

# 使用场景

1. **动态测试选择**：根据运行时环境或配置，动态选择需要执行的测试。例如，可以根据当前测试环境（如开发、测试、生产）选择不同的测试集合。
2. **方便调试**：在调试过程中，通过自定义标记表达式快速筛选和执行特定的测试用例。
3. **灵活的测试过滤**：可以基于复杂的逻辑自定义测试过滤规则。

# 参数

```python
def pytest_markeval_namespace(config):
    # config: pytest 的配置对象，包含有关当前测试会话的所有信息
    pass
```

- `config`：pytest 的配置对象，包含有关当前测试会话的所有信息。通过这个配置对象，我们可以获取命令行参数、环境变量等各种配置信息，并据此注入自定义的变量或函数。

# 示例代码

## 案例一：动态测试选择

目标：根据命令行参数动态选择需要执行的测试。

步骤：
1. 使用 `pytest_addoption` 钩子增加一个自定义参数，用于指定测试环境。
2. 使用 `pytest_markeval_namespace` 钩子动态注入变量或函数。
3. 根据自定义的变量或函数过滤测试用例。

示例代码：

**增加自定义参数**：

```python
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")

def pytest_markeval_namespace(config):
    # 获取命令行参数
    current_env = config.getoption("--env")
    
    # 向命名空间注入一个函数，用于判断当前环境
    def is_env(env):
        return env == current_env
    
    return {
        'is_env': is_env
    }
```

**示例测试文件**：

```python
# tests/test_example.py
# tests/test_example.py
import pytest

@pytest.mark.skipif("not is_env('dev')", reason="Only run in dev environment")
def test_only_in_dev():
    assert 1 + 1 == 2

@pytest.mark.skipif("not is_env('prod')", reason="Only run in prod environment")
def test_only_in_prod():
    assert 2 + 2 == 4
```

**运行测试**：

在命令行中运行测试并指定环境：

```shell
pytest -s -v --env=dev
```

运行效果参考如下：

```shell
root@Gavin:~/test/hook# pytest -s -v --env=prod
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

tests/test_example.py::test_only_in_dev SKIPPED (Only run in dev environment)
tests/test_example.py::test_only_in_prod PASSED

============================================================================================================= 1 passed, 1 skipped in 0.04s ==============================================================================================================
root@Gavin:~/test/hook# pytest -s -v --env=dev
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

tests/test_example.py::test_only_in_dev PASSED
tests/test_example.py::test_only_in_prod SKIPPED (Only run in prod environment)

============================================================================================================= 1 passed, 1 skipped in 0.03s ==============================================================================================================
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

tests/test_example.py::test_only_in_dev PASSED
tests/test_example.py::test_only_in_prod SKIPPED (Only run in prod environment)

============================================================================================================= 1 passed, 1 skipped in 0.03s ==============================================================================================================
root@Gavin:~/test/hook# 
```

## 案例二：调试过程中使用自定义标记表达式快速筛选测试用例

目标：在调试过程中，通过自定义标记表达式快速筛选和执行特定的测试用例。

步骤：
1. 使用 `pytest_markeval_namespace` 钩子向命名空间注入自定义的调试函数。
2. 在测试用例中使用不同的标记策略。

示例代码：

```python
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")
    parser.addoption("--debug-mode", action="store_true", help="Run tests in debug mode")

def pytest_markeval_namespace(config):
    # 获取命令行参数
    current_env = config.getoption("--env")
    debug_mode = config.getoption("--debug-mode")
    
    # 向命名空间注入函数
    def is_env(env):
        return env == current_env
    
    def is_debug_mode():
        return debug_mode
    
    return {
        'is_env': is_env,
        'is_debug_mode': is_debug_mode
    }
```

**示例测试文件**：

```python
# tests/test_example.py
import pytest

@pytest.mark.skipif("not is_env('dev')", reason="Only run in dev environment")
def test_only_in_dev():
    assert 1 + 1 == 2

@pytest.mark.skipif("not is_env('prod')", reason="Only run in prod environment")
def test_only_in_prod():
    assert 2 + 2 == 4

@pytest.mark.skipif("not is_debug_mode()", reason="Only run in debug mode")
def test_debug_mode():
    assert "debug" == "debug"
```

**运行测试**：

运行测试，指定 `dev` 环境和启用调试模式:

```shell
root@Gavin:~/test/hook# pytest tests --env=dev --debug-mode -v
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

tests/test_example.py::test_only_in_dev PASSED                                                                                                                                                                                                    [ 33%]
tests/test_example.py::test_only_in_prod SKIPPED (Only run in prod environment)                                                                                                                                                                   [ 66%]
tests/test_example.py::test_debug_mode PASSED                                                                                                                                                                                                     [100%]

============================================================================================================= 2 passed, 1 skipped in 0.04s ==============================================================================================================
root@Gavin:~/test/hook# 
```


运行测试，指定 `prod` 环境:

```shell
root@Gavin:~/test/hook# pytest tests --env=prod -v
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

tests/test_example.py::test_only_in_dev SKIPPED (Only run in dev environment)                                                                                                                                                                     [ 33%]
tests/test_example.py::test_only_in_prod PASSED                                                                                                                                                                                                   [ 66%]
tests/test_example.py::test_debug_mode SKIPPED (Only run in debug mode)                                                                                                                                                                           [100%]

============================================================================================================= 1 passed, 2 skipped in 0.04s ==============================================================================================================
root@Gavin:~/test/hook# 
```

**详细解释:**

**pytest_addoption**：
  使用 `pytest_addoption` 添加了两个自定义的命令行选项 `--env` 和 `--debug-mode`，用于指定测试环境和调试模式。
**pytest_markeval_namespace**：
  钩子函数 `pytest_markeval_namespace` 中，获取命令行参数并注入 `is_env` 和 `is_debug_mode` 函数到 `pytest` 的命名空间中。
标记表达式中引用自定义函数：
  在测试文件中，使用字符串形式引用 `is_env('dev')、is_env('prod') `和 `is_debug_mode()`，确保 `pytest` 能在运行时解析和调用这些函数，根据条件选择性地执行测试用例。

## 案例三：灵活的测试过滤

目标：基于复杂的逻辑自定义测试过滤规则。

步骤：
1. 使用 `pytest_markeval_namespace` 钩子向命名空间注入一个复杂的过滤函数。
2. 在测试用例中基于过滤函数定义标记表达式。

示例代码：

```python
# conftest.py
import pytest
import os

def pytest_markeval_namespace(config):
    # 注入一个自定义函数，判断是否存在某个环境变量
    def has_env_var(var_name):
        return os.getenv(var_name) is not None

    return {
        'has_env_var': has_env_var
    }
```

**示例测试文件**：

```python
# tests/test_env_var_example.py
# tests/test_env_var_example.py
import pytest

@pytest.mark.skipif("not has_env_var('CI')", reason="Only run in CI environment")
def test_only_in_ci():
    assert 3 + 3 == 6
```

**运行测试**：

**CI 环境变量被设置**:

```plaintext
root@Gavin:~/test/hook# CI=true pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_env_var_example.py .                                                                                                                                                                                                                   [100%]

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```



**未设置 CI 环境变量**:

```plaintext
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_env_var_example.py s                                                                                                                                                                                                                   [100%]

================================================================================================================== 1 skipped in 0.02s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**详细解释**:

* **pytest_markeval_namespace**：
 钩子函数 `pytest_markeval_namespace` 被用来向`pytest`的运行时命名空间注入自定义函数 `has_env_var`，用于判断是否存在某个环境变量。
* **标记表达式中引用自定义函数**：
 在测试文件中，使用字符串形式引用 `has_env_var('CI')`。确保 `pytest` 能在运行时解析和调用这些函数，并根据条件选择性地执行测试用例。


# 小结

通过 `pytest_markeval_namespace` 钩子，我们可以在 `pytest` 的标记表达式求值上下文中注入自定义的变量或函数，从而实现灵活的测试选择、调试与过滤。希望这些内容对你有所帮助，使你能够更好地利用此钩子函数来优化你的测试流程和报告。
