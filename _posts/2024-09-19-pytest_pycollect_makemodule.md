---
title: pytest hook系列之pytest_pycollect_makemodule
date: 2024-09-19 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-14.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_pycollect_makemodule
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_pycollect_makemodule` 是`pytest`框架中的一个钩子函数，允许我们自定义测试模块的收集过程。利用这个钩子函数，我们可以在模块被收集时定制其行为，如过滤测试、添加特定的初始化逻辑等。这为我们提供了高度的灵活性，以满足各种复杂的测试需求。

# 什么是pytest_pycollect_makemodule？

`pytest_pycollect_makemodule` 是一个`pytest`提供的钩子函数，它在收集一个`Python`模块时调用。通过这个钩子，我们可以自定义模块的创建过程，并对其进行特殊处理。

# 使用场景

1. **根据文件路径自定义收集器行为**：根据模块文件的位置或名称进行自定义处理。
2. **动态添加测试用例**：在模块收集过程中，动态添加测试用例或修改现有的测试用例。
3. **模块初始化**：在模块被收集时执行特定的初始化逻辑，如设置特定的环境变量或路径。

# 参数

```python
def pytest_pycollect_makemodule(path, parent):
    # path: 模块文件的路径，为 `pathlib.Path` 对象
    # parent: 父收集器对象，通常是一个目录收集器
    pass
```

- `path`：表示模块文件路径的 `pathlib.Path` 对象。
- `parent`：父收集器对象，通常是一个目录收集器，可以通过它访问包含此模块的目录。

# 示例代码

## 案例一：根据文件路径自定义收集器行为

目标：根据模块文件的位置或名称，决定是否进行特殊处理或动态过滤测试用例。

步骤：

1. 使用 `pytest_pycollect_makemodule` 钩子函数。
2. 根据文件路径或名称，决定是否进行特殊处理或过滤。

示例代码：

```python
# conftest.py
import pytest
from pathlib import Path

def pytest_pycollect_makemodule(path, parent):
    # 确保函数被调用
    print(f"pytest_pycollect_makemodule called for: {path}")

    # 确保我们使用 pathlib.Path
    if not isinstance(path, Path):
        path = Path(str(path))

    # 获取文件名（不带扩展名）
    stem = path.stem

    # 根据模块文件路径决定是否特殊处理
    if "special" in stem:
        print(f"Collecting special module: {path}")
        module = pytest.Module.from_parent(parent, path=path)
        return module

    # 返回默认的模块收集器
    print(f"Collecting normal module: {path}")
    return pytest.Module.from_parent(parent, path=path)

# 示例测试文件 `tests/test_special_module.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_normal_module.py`
def test_example2():
    assert 2 + 2 == 4
```

**注释**：

- `pytest_pycollect_makemodule` 钩子函数中，检查模块文件路径是否包含特定关键字（如 "special"），以决定是否进行特殊处理。
- 如果模块包含关键字，打印信息并添加标记；否则，返回默认的模块收集器。


运行效果：

```shell
root@Gavin:~/test/hook# pytest --cache-clear -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... pytest_pycollect_makemodule called for: /root/test/hook/tests/test_normal_module.py
Collecting normal module: /root/test/hook/tests/test_normal_module.py
pytest_pycollect_makemodule called for: /root/test/hook/tests/test_special_module.py
Collecting special module: /root/test/hook/tests/test_special_module.py
collected 2 items                                                                                                                                                                                                                                       

tests/test_normal_module.py::test_example2 PASSED
tests/test_special_module.py::test_example1 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```


## 案例二：动态添加测试用例

目标：在模块收集过程中，动态地添加测试用例以满足特定测试需求。

步骤：

1. 使用 `pytest_pycollect_makemodule` 钩子函数。
2. 动态创建并添加测试用例到模块中。

示例代码：

```python
# conftest.py
import pytest
from pathlib import Path

def pytest_pycollect_makemodule(path, parent):
    # 确保函数被调用
    print(f"pytest_pycollect_makemodule called for: {path}")

    # 确保我们使用 pathlib.Path
    if not isinstance(path, Path):
        path = Path(str(path))

    # 获取文件名（不带扩展名）
    stem = path.stem

    module = pytest.Module.from_parent(parent, path=path)

    if "enhanced" in stem:
        print(f"Enhancing module: {path}")

        # 动态添加测试用例
        def dynamic_test():
            assert True, "This is a dynamically added test case"

        item = pytest.Function.from_parent(module, name="test_dynamic", callobj=dynamic_test)
        
        # 添加动态测试用例到模块的已有收集中
        original_collect = module.collect

        def my_collect():
            items = list(original_collect())
            items.append(item)
            return items

        module.collect = my_collect

    return module

# 示例测试文件 `tests/test_enhanced_module.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_normal_module.py`
def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- `pytest_pycollect_makemodule` 钩子函数中，检测模块文件名包含特定关键字（如 "enhanced"），决定是否增强模块。
- 动态创建一个测试用例并添加到模块中。


运行效果：

```shell
root@Gavin:~/test/hook# pytest --cache-clear -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... pytest_pycollect_makemodule called for: /root/test/hook/tests/test_enhanced_module.py
Enhancing module: /root/test/hook/tests/test_enhanced_module.py
pytest_pycollect_makemodule called for: /root/test/hook/tests/test_normal_module.py
pytest_pycollect_makemodule called for: /root/test/hook/tests/test_special_module.py
collected 4 items                                                                                                                                                                                                                                       

tests/test_enhanced_module.py::test_example1 PASSED
tests/test_enhanced_module.py::test_dynamic PASSED
tests/test_normal_module.py::test_example2 PASSED
tests/test_special_module.py::test_example1 PASSED

=================================================================================================================== 4 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

# 案例三：模块初始化

目标：在模块被收集时，执行特定的初始化逻辑，比如设置环境变量或路径。

步骤：
1. 使用 `pytest_pycollect_makemodule` 钩子函数。
2. 在模块收集时执行初始化逻辑。

示例代码：

```python
# conftest.py
import pytest
import os
from pathlib import Path

def pytest_pycollect_makemodule(path, parent):
    # 确保函数被调用
    print(f"pytest_pycollect_makemodule called for: {path}")

    # 确保我们使用 pathlib.Path
    if not isinstance(path, Path):
        path = Path(str(path))

    # 获取文件名（不带扩展名）
    stem = path.stem

    module = pytest.Module.from_parent(parent, path=path)

    if "config" in stem:
        print(f"Configuring module: {path}")
        # 模块初始化逻辑
        os.environ["CONFIG_PATH"] = str(path)

    return module

# 示例测试文件 `tests/test_config_module.py`
import os

def test_example1():
    config_path = os.getenv("CONFIG_PATH")
    assert config_path.endswith("test_config_module.py")

# 示例测试文件 `tests/test_normal_module.py`
def test_example2():
    assert 2 + 2 == 4
```

**注释**：

- `pytest_pycollect_makemodule` 钩子函数中，根据模块文件名检查是否需要初始化。
- 如果需要初始化，则设置相应的环境变量或路径。

运行效果：

```shell
root@Gavin:~/test/hook# pytest --cache-clear -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... pytest_pycollect_makemodule called for: /root/test/hook/tests/test_config_module.py
Configuring module: /root/test/hook/tests/test_config_module.py
pytest_pycollect_makemodule called for: /root/test/hook/tests/test_enhanced_module.py
pytest_pycollect_makemodule called for: /root/test/hook/tests/test_normal_module.py
pytest_pycollect_makemodule called for: /root/test/hook/tests/test_special_module.py
collected 4 items                                                                                                                                                                                                                                       

tests/test_config_module.py::test_example1 PASSED
tests/test_enhanced_module.py::test_example1 PASSED
tests/test_normal_module.py::test_example2 PASSED
tests/test_special_module.py::test_example1 PASSED

=================================================================================================================== 4 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

# 总结

`pytest_pycollect_makemodule` 是一个非常有用的钩子，允许我们在模块被收集时执行自定义逻辑。通过本文的案例，你可以了解如何使用 `pytest_pycollect_makemodule` 钩子定制模块的收集行为、动态添加测试用例以及在收集时进行模块初始化。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而实现更灵活的测试管理和调试。希望这篇文章能够帮助你更好地理解和使用 `pytest_pycollect_makemodule`。
