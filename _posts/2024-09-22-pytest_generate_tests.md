---
title: pytest hook系列之pytest_generate_tests
date: 2024-09-22 23:00:00
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
summary: pytest hook之pytest_generate_tests
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview


`pytest_generate_tests` 是 pytest 框架中的一个钩子函数，它在测试收集阶段被调用，用于生成基于参数化的动态测试用例。通过这个钩子，我们可以实现对测试用例的参数化处理，使测试用例能够覆盖更多的输入组合，从而提高测试覆盖率和测试的灵活性。

# 使用场景

1. **参数化测试**：根据不同的参数组合生成多个测试用例，测试更多的输入组合和边界情况。
2. **动态数据驱动测试**：从外部数据源（如配置文件、数据库等）中读取数据，生成动态测试用例。
3. **组合测试场景**：根据多个参数的笛卡尔积生成测试用例组合，全面覆盖测试场景。

# 参数

```python
def pytest_generate_tests(metafunc):
    # metafunc: pyfuncitem对象, 包含pytest收集函数测试用例的所有相关信息
    pass
```

- `metafunc`：这是收集的测试函数对象，包含所有有关测试函数的信息，包括名称、参数等。

# 示例代码

## 案例一：基本参数化测试

目标：根据提供的参数组合生成多个测试用例，测试不同的输入组合。

步骤：

1. 使用 `pytest_generate_tests` 钩子函数。
2. 在钩子函数中调用 `metafunc.parametrize` 方法为测试函数生成多个参数化的测试用例。

示例代码：

```python
# conftest.py
import pytest

def pytest_generate_tests(metafunc):
    if "param" in metafunc.fixturenames:
        metafunc.parametrize("param", [1, 2, 3])

# 示例测试文件 `tests/test_example.py`
def test_example(param):
    assert param in [1, 2, 3]
```

**注释**：

- 在 `pytest_generate_tests` 钩子函数中，检查是否需要参数化 `param`，并提供一个参数列表 `[1, 2, 3]` 进行参数化。

## 案例二：从外部数据源动态生成测试用例

目标：从外部数据源（如配置文件或数据库）中读取数据，生成动态测试用例。

步骤：

1. 使用 `pytest_generate_tests` 钩子函数。
2. 从外部数据源读取参数并生成测试用例。

示例代码：

```python
# conftest.py
import pytest
import json

def pytest_generate_tests(metafunc):
    if "config_value" in metafunc.fixturenames:
        with open('config.json') as f:
            config_data = json.load(f)
        metafunc.parametrize("config_value", config_data["values"])

# 示例配置文件 `config.json`
{
    "values": [10, 20, 30]
}

# 示例测试文件 `tests/test_config.py`
def test_config(config_value):
    assert config_value in [10, 20, 30]
```

**注释**：

- 在 `pytest_generate_tests` 钩子函数中，从 `config.json` 文件读取配置数据，并生成测试用例。
- 在 `config.json` 文件中，定义测试用例的参数值。

## 案例三：组合测试场景生成

目标：根据多个参数的笛卡尔积生成测试用例，全面覆盖测试场景。

步骤：

1. 使用 `pytest_generate_tests` 钩子函数。
2. 生成多个参数的笛卡尔积组合，并生成测试用例。

示例代码：

```python
# conftest.py
import pytest

def pytest_generate_tests(metafunc):
    if "x" in metafunc.fixturenames and "y" in metafunc.fixturenames:
        q = [x for x in range(2)]
        p = [y for y in range(3)]
        metafunc.parametrize("x, y", [(i, j) for i in q for j in p])

# 示例测试文件 `tests/test_combination.py`
def test_combination(x, y):
    assert x in range(2)
    assert y in range(3)
```

**注释**：

- 在 `pytest_generate_tests` 钩子函数中，生成两个参数 `x` 和 `y` 的笛卡尔积组合，并使用 `metafunc.parametrize` 方法生成测试用例。


## 运行和验证

在项目根目录下运行以下命令：

```sh
pytest -s -v
```

# 验证输出信息

根据不同的案例，控制台输出应包含参数化生成的测试用例，显示测试用例在不同参数组合下的执行结果。

# 示范输出

**案例一：基本参数化测试**

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

tests/test_example.py::test_example[1] PASSED
tests/test_example.py::test_example[2] PASSED
tests/test_example.py::test_example[3] PASSED

=================================================================================================================== 3 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**案例二：动态生成测试用例**

```plaintext
root@Gavin:~/test/hook# pytest -s  -v --cache-clear
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

tests/test_config.py::test_config[10] PASSED
tests/test_config.py::test_config[20] PASSED
tests/test_config.py::test_config[30] PASSED

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：组合测试场景生成**

```plaintext
root@Gavin:~/test/hook# rm -rf config.json 
root@Gavin:~/test/hook# vim conftest.py 
root@Gavin:~/test/hook# rm -rf tests/test_config.py 
root@Gavin:~/test/hook# vim tests/test_combination.py
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
collected 6 items                                                                                                                                                                                                                                       

tests/test_combination.py::test_combination[0-0] PASSED
tests/test_combination.py::test_combination[0-1] PASSED
tests/test_combination.py::test_combination[0-2] PASSED
tests/test_combination.py::test_combination[1-0] PASSED
tests/test_combination.py::test_combination[1-1] PASSED
tests/test_combination.py::test_combination[1-2] PASSED

=================================================================================================================== 6 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

## 详细解释

1. **参数化测试**
   - 在 `pytest_generate_tests` 钩子函数中，通过检查是否需要参数化特定的参数，并使用 `metafunc.parametrize` 方法生成多个测试用例。

2. **动态数据驱动测试**
   - 在 `pytest_generate_tests` 钩子函数中，从外部数据源（如配置文件）读取数据，并使用 `metafunc.parametrize` 方法生成测试用例。

3. **组合测试场景生成**
   - 在 `pytest_generate_tests` 钩子函数中，生成多个参数的笛卡尔积组合，并使用 `metafunc.parametrize` 方法生成测试用例，以全面覆盖测试场景。

## 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保所使用的是支持 `pytest_generate_tests` 钩子的 pytest 版本。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py`、`test_config.py`、`test_combination.py` 放在 `tests` 目录内且符合 pytest 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行 pytest 并检查控制台输出，确认参数化生成的测试用例在不同参数组合下的执行结果。

# 总结

通过详细介绍 `pytest_generate_tests` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是基本参数化测试、动态数据驱动测试，还是组合测试场景生成，都能为你提供强大的工具，满足各种复杂的测试需求。
