---
title: pytest hook系列之pytest_make_parametrize_id
date: 2024-09-23 23:00:00
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
summary: pytest hook之pytest_make_parametrize_id
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_make_parametrize_id` 是`pytest`框架中的一个钩子函数，允许我们自定义参数化测试用例的`ID`，它在生成参数化测试用例的`ID`时被调用。通过这个钩子函数，我们可以在生成参数化测试用例时为每个参数生成友好且易读的`ID`，从而提高测试结果的可读性和可调试性。

# 使用场景

1. **增强测试报告的可读性**：为每个参数化的测试用例生成易读的 `ID`，使测试报告更加清晰。
2. **参数值的友好展示**：将复杂或不具可读性的参数值转换为易理解的名称。
3. **调试和分析**：在调试和分析测试结果时，利用自定义的 `ID` 更快地定位问题。

# 参数

```python
def pytest_make_parametrize_id(config, val):
    # config: pytest 配置对象，可以从中获取与配置相关的信息
    # val: 参数值，即当前需要生成 `ID` 的参数
    pass
```

- `config`：pytest 配置对象，可以从中获取与配置相关的信息。
- `val`：参数值，即当前需要生成`ID`的参数。

# 示例代码

## 案例一：为简单参数生成友好ID

目标：为简单参数（如整数、字符串等）生成友好且易读的`ID`。

步骤：

1. 使用 `pytest_make_parametrize_id` 钩子函数。
2. 根据参数值生成友好的`ID`。

示例代码：

```python
# conftest.py
def pytest_make_parametrize_id(config, val):
    if isinstance(val, (int, float, str)):
        return f"param_{val}"
    return None  # 使用默认 ID

# 示例测试文件 `tests/test_example.py`
import pytest

@pytest.mark.parametrize("param", [1, 2, 3.5, "hello"])
def test_example(param):
    assert param is not None
```

**注释**：

- 在 `pytest_make_parametrize_id` 钩子函数中，检查参数类型是否为 `int`, `float` 或 `str`，并为其生成友好的`ID`。

## 案例二：为复杂参数生成友好ID

目标：为复杂参数（如字典、对象等）生成友好且易读的`ID`。

步骤：

1. 使用 `pytest_make_parametrize_id` 钩子函数。
2. 检查参数类型并生成相应的友好`ID`。

示例代码：

```python
# conftest.py
def pytest_make_parametrize_id(config, val):
    if isinstance(val, dict):
        return "_".join(f"{k}={v}" for k, v in val.items())
    return None  # 使用默认 ID

# 示例测试文件 `tests/test_complex.py`
import pytest

@pytest.mark.parametrize("param", [{"a": 1, "b": 2}, {"a": 3, "b": 4}])
def test_complex(param):
    assert "a" in param
    assert "b" in param
```

**注释**：
- 在 `pytest_make_parametrize_id` 钩子函数中，检查参数类型是否为 `dict`，并生成以键值对形式展示的 `ID`。

## 案例三：为对象参数生成友好 ID

目标：为对象参数生成友好且易读的`ID`。

步骤：

1. 使用 `pytest_make_parametrize_id` 钩子函数。
2. 检查参数类型并生成相应的友好 `ID`。

示例代码：

```python
# conftest.py
class CustomObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def pytest_make_parametrize_id(config, val):
    if isinstance(val, CustomObject):
        return f"{val.name}-{val.value}"
    return None  # 使用默认 ID

# 示例测试文件 `tests/test_object.py`
import pytest

@pytest.mark.parametrize("param", [CustomObject("obj1", 10), CustomObject("obj2", 20)])
def test_object(param):
    assert isinstance(param, CustomObject)
    assert param.value > 0
```

**注释**：

- 在 `pytest_make_parametrize_id` 钩子函数中，检查参数类型是否为自定义的 `CustomObject`，并生成以 `name` 和 `value` 属性组合的 `ID`。

# 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    ├── test_complex.py
    ├── test_example.py
    └── test_object.py

2 directories, 4 files
root@Gavin:~/test/hook# 
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

## 验证输出信息

根据不同的案例，控制台输出应显示友好且易读的测试用例 `ID`。

## 控制台输出示例

**案例一：为简单参数生成友好 ID**

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

tests/test_example.py::test_example[param_1] PASSED
tests/test_example.py::test_example[param_2] PASSED
tests/test_example.py::test_example[param_3.5] PASSED
tests/test_example.py::test_example[param_hello] PASSED

=================================================================================================================== 4 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**案例二：为复杂参数生成友好 ID**

```plaintext
root@Gavin:~/test/hook# pytest -s -v tests/test_complex.py 
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

tests/test_complex.py::test_complex[a=1_b=2] PASSED
tests/test_complex.py::test_complex[a=3_b=4] PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**案例三：为对象参数生成友好 ID**

```plaintext
root@Gavin:~/test/hook# pytest -s -v tests/test_object.py --cache-clear
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

tests/test_object.py::test_object[obj1-10] PASSED
tests/test_object.py::test_object[obj2-20] PASSED

=================================================================================================================== 2 passed in 0.05s ===================================================================================================================
root@Gavin:~/test/hook#
```

## 详细解释

1. **生成友好 ID**
   - 在 `pytest_make_parametrize_id` 钩子函数中，根据参数的类型生成友好的`ID`，以提高测试报告的可读性。

2. **处理简单参数**
   - 对于简单参数（如整数、浮点数、字符串），直接生成包含参数值的`ID`。

3. **处理复杂参数**
   - 对于复杂参数（如字典），生成以键值对形式展示的`ID`。

4. **处理对象参数**
   - 对于对象参数，生成包含对象属性值的`ID`。

## 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保所使用的是支持 `pytest_make_parametrize_id` 钩子的 pytest 版本。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py`、`test_complex.py`、`test_object.py` 放在 `tests` 目录内且符合 pytest 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台输出，确认生成的测试用例`ID`是否符合预期。

# 总结

通过详细介绍 `pytest_make_parametrize_id` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是为简单参数、复杂参数，还是对象参数生成友好 `ID`，都能为你提供强大的工具，提升测试报告的可读性和可调试性。
