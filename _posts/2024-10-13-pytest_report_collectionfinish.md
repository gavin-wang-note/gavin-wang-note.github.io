---
title: pytest hook系列之pytest_report_collectionfinish
date: 2024-10-13 23:00:00
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
summary: pytest hook之pytest_report_collectionfinish
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_report_collectionfinish` 是`pytest`框架中的一个钩子函数，用于在测试收集阶段完成后提供自定义的报告信息，它在测试收集阶段完成后被触发。通过这个钩子函数，我们可以在测试收集完成后插入一些有用的信息，例如收集的测试用例数量、收集耗时、特定的测试用例标记信息等，以便更好地了解和调试测试集的状态，从而更好地了解测试集的情况。

# 使用场景

1. **测试用例统计**：统计和报告收集到的测试用例数量、目录结构等信息。
2. **测试用例分类**：对收集到的测试用例进行分类，并提供分类统计信息。
3. **测试用例标记**：统计和报告带有特定标记的测试用例信息。
4. **收集阶段耗时**：记录和报告测试收集阶段的耗时信息。

# 参数

```python
def pytest_report_collectionfinish(config, startdir, items):
    # config: pytest 的配置对象，包含有关当前测试会话的所有信息
    # start_path: 测试收集开始的目录
    # startdir: 测试收集开始的目录(deprecated)
    # items: 收集到的测试用例项列表
    pass
```

- `config`：`pytest` 的配置对象，包含有关当前测试会话的所有信息。
- `start_path`：测试收集开始的目录。
- `startdir`：测试收集开始的目录（废弃中）
- `items`：收集到的测试用例项列表。

# 示例代码

## 案例一：测试用例统计

目标：统计和报告收集到的测试用例数量和目录结构信息。

步骤：
1. 使用 `pytest_report_collectionfinish` 钩子函数。
2. 在钩子函数中插入统计信息收集和返回代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_report_collectionfinish(config, startdir, items):
    """在测试报告中统计并显示收集到的测试用例数量和目录结构信息"""
    num_tests = len(items)
    return [
        f"Collected {num_tests} test{'s' if num_tests != 1 else ''}"
    ]

# 示例测试文件 tests/test_example.py
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert "pytest" in "pytest is fun"
```

**注释**：
- `items` 参数包含收集到的所有测试用例项列表。
- 通过 `len(items)` 统计测试用例数量，并在 `pytest_report_collectionfinish` 钩子函数中返回包含统计信息的字符串列表。

**运行效果**：

```shell
collected 2 items                                                                                                                                                                                                                                       
Collected 2 tests

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED
```

## 案例二：测试用例分类

目标：对收集到的测试用例进行分类，并提供分类统计信息。

步骤：
1. 使用 `pytest_report_collectionfinish` 钩子函数。
2. 在钩子函数中插入测试用例分类和统计代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_report_collectionfinish(config, startdir, items):
    """在测试报告中分类并统计收集到的测试用例信息"""
    tests_by_class = {}
    for item in items:
        test_class = item.cls.__name__ if item.cls else 'NoClass'
        if test_class not in tests_by_class:
            tests_by_class[test_class] = 0
        tests_by_class[test_class] += 1
    
    report_lines = [f"Collected {len(items)} tests"]
    for test_class, count in tests_by_class.items():
        report_lines.append(f"{test_class}: {count} test{'s' if count != 1 else ''}")
    return report_lines

# 示例测试文件 tests/test_example.py
class TestMath:
    def test_addition(self):
        assert 1 + 1 == 2
    
    def test_subtraction(self):
        assert 2 - 1 == 1

def test_string_contains():
    assert "pytest" in "pytest is fun"
```

**注释**：
- `pytest` 的测试项有一个 `cls` 属性来表示测试类。
- 遍历 `items` 生成按类统计的测试用例信息，并在 `pytest_report_collectionfinish` 钩子函数中返回分类统计信息的字符串列表。


**运行效果**：

```shell
collected 3 items                                                                                                                                                                                                                                       
Collected 3 tests
TestMath: 2 tests
NoClass: 1 test

tests/test_example.py::TestMath::test_addition PASSED
tests/test_example.py::TestMath::test_subtraction PASSED
tests/test_example.py::test_string_contains PASSED

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

## 案例三：测试用例标记

目标：统计和报告带有特定标记的测试用例信息。

步骤：
1. 使用 `pytest_report_collectionfinish` 钩子函数。
2. 在钩子函数中插入标记测试用例统计和报告代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_report_collectionfinish(config, startdir, items):
    """在测试报告中统计并显示带有特定标记的测试用例信息"""
    tagged_tests = [item for item in items if 'slow' in item.keywords]
    num_tagged_tests = len(tagged_tests)
    return [
        f"Collected {len(items)} tests",
        f"Number of 'slow' tagged tests: {num_tagged_tests}"
    ]

# 示例测试文件 tests/test_example.py
import pytest

@pytest.mark.slow
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert "pytest" in "pytest is fun"
```

**注释**：
- 使用 `item.keywords` 属性判断测试用例是否带有特定标记（如 `slow`）。
- 统计和报告带有 `slow` 标记的测试用例数量，并在 `pytest_report_collectionfinish` 钩子函数中返回包含这些统计信息的字符串列表。


**运行效果**：

```shell
collected 2 items                                                                                                                                                                                                                                       
Collected 2 tests
Number of 'slow' tagged tests: 1

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED
```
## 案例四：收集阶段耗时

目标：记录和报告测试收集阶段的耗时信息。

步骤：
1. 使用 `pytest_report_collectionfinish` 钩子函数。
2. 在测试收集阶段开始时记录开始时间；在钩子函数中计算并报告收集阶段的耗时。

示例代码：

```python
# conftest.py
import pytest
import time

# 全局变量用于记录测试收集开始时间
collection_start_time = None

def pytest_configure(config):
    global collection_start_time
    collection_start_time = time.time()

def pytest_report_collectionfinish(config, startdir, items):
    """在测试报告中显示测试收集的耗时信息"""
    global collection_start_time
    collection_duration = time.time() - collection_start_time
    return [
        f"Collected {len(items)} tests",
        f"Collection duration: {collection_duration:.2f} seconds"
    ]

# 示例测试文件 tests/test_example.py
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert "pytest" in "pytest is fun"
```

**注释**：
- `pytest_configure` 钩子函数在 `pytest` 配置初始化时触发。我们在该钩子函数中记录测试收集的开始时间。
- 在 `pytest_report_collectionfinish` 钩子函数中，计算测试收集的耗时，并将其与测试用例统计信息一起返回。

**运行效果**：

```shell
collected 2 items                                                                                                                                                                                                                                       
Collected 2 tests
Collection duration: 0.09 seconds

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

# 其他详细考虑

1. **输出信息的格式化**
   - 可以进一步格式化输出信息，使其更加美观和可读。例如，使用表格格式对分类统计数据进行排版。

2. **动态标记**
   - 除了固定标记，还可以增强代码实现动态标记监控。例如，从命令行参数中读取特定标记，或通过配置文件自定义监控的标记类型。

3. **汇总信息**
   - 可以在多个钩子结合使用时汇总输出信息。例如，可以将收集测试数量、分类统计和标签统计信息整合到一起，形成一份综合报告。

# 实现步骤

以下详细步骤确保在适当的钩子函数中插入代码，以实现所需功能：

## 步骤一：编写conftest.py文件

```python
# conftest.py
import pytest
import time
import platform
import sys
import subprocess
import os

# 全局变量用于记录测试收集开始时间
collection_start_time = None

def pytest_configure(config):
    global collection_start_time
    collection_start_time = time.time()

def pytest_addoption(parser):
    """添加自定义命令行参数"""
    parser.addoption("--config", action="store", default="default_config.yaml", help="Path to the config file")
    parser.addoption("--show-env", action="store_true", help="Show environment information in the report")
    parser.addoption("--show-version", action="store_true", help="Show version information in the report")
    parser.addoption("--show-params", action="store_true", help="Show run parameters in the report")
    parser.addoption("--show-debug", action="store_true", help="Show debug information in the report")

def get_git_commit():
    """获取当前代码仓库的提交 ID"""
    try:
        commit_id = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
    except Exception:
        commit_id = "N/A"
    return commit_id

def pytest_report_header(config):
    """在测试报告头部添加自定义信息"""
    header = []
    
    if config.getoption("--show-env"):
        # 获取环境信息
        header.extend([
            f"Platform: {platform.platform()}",
            f"Python Version: {sys.version}",
            f"pytest Version: {pytest.__version__}",
        ])
    
    if config.getoption("--show-version"):
        # 获取版本信息
        header.extend([
            f"Application Version: 1.0.0",
            f"Git Commit ID: {get_git_commit()}",
        ])
    
    if config.getoption("--show-params"):
        # 获取运行参数
        config_file = config.getoption("--config")
        header.extend([
            f"Config File: {config_file}",
            f"Command Line Arguments: {config.invocation_params.args}",
        ])
    
    if config.getoption("--show-debug"):
        # 获取调试信息
        header.extend([
            "Debug Information:",
            f"APP_DEBUG_MODE: {os.environ.get('APP_DEBUG_MODE', 'undefined')}",
            f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'undefined')}",
        ])
    
    return header

def pytest_report_collectionfinish(config, startdir, items):
    """在测试报告中显示收集到的测试用例数量和收集耗时信息"""
    global collection_start_time
    collection_duration = time.time() - collection_start_time
    
    tests_by_class = {}
    tagged_tests = [item for item in items if 'slow' in item.keywords]
    num_tagged_tests = len(tagged_tests)
    
    for item in items:
        test_class = item.cls.__name__ if item.cls else 'NoClass'
        if test_class not in tests_by_class:
            tests_by_class[test_class] = 0
        tests_by_class[test_class] += 1
    
    report_lines = [
        f"Collected {len(items)} tests",
        f"Collection duration: {collection_duration:.2f} seconds",
        f"Number of 'slow' tagged tests: {num_tagged_tests}"
    ]
    
    for test_class, count in tests_by_class.items():
        report_lines.append(f"{test_class}: {count} test{'s' if count != 1 else ''}")
    
    return report_lines

# 示例测试文件 tests/test_example.py
import pytest

@pytest.mark.slow
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert "pytest" in "pytest is fun"

class TestMath:
    def test_addition(self):
        assert 1 + 1 == 2
    
    def test_subtraction(self):
        assert 2 - 1 == 1
```

# 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree -l
.
├── clear_pyc.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook#
```

## 执行测试命令

在项目根目录下运行以下命令：

```shell
pytest -s -v --config=custom_config.yaml --show-env --show-version --show-params --show-debug
```


## 验证输出信息

控制台输出应包含所有在 `pytest_report_header` 和 `pytest_report_collectionfinish` 钩子中返回的信息，例如：

```plaintext
root@Gavin:~/test/hook# pytest -s -v --config=custom_config.yaml --show-env --show-version --show-params --show-debug
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
fatal: not a git repository (or any of the parent directories): .git
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Platform: Linux-6.5.0-35-generic-x86_64-with-glibc2.38
Python Version: 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0]
pytest Version: 8.0.2
Application Version: 1.0.0
Git Commit ID: N/A
Config File: custom_config.yaml
Command Line Arguments: ('-s', '-v', '--config=custom_config.yaml', '--show-env', '--show-version', '--show-params', '--show-debug')
Debug Information:
APP_DEBUG_MODE: true
DATABASE_URL: sqlite:///:memory:
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 4 items                                                                                                                                                                                                                                       
Collected 4 tests
Collection duration: 0.10 seconds
Number of 'slow' tagged tests: 1
NoClass: 2 tests
TestMath: 2 tests

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED
tests/test_example.py::TestMath::test_addition PASSED
tests/test_example.py::TestMath::test_subtraction PASSED

=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py:3
  /root/test/hook/tests/test_example.py:3: PytestUnknownMarkWarning: Unknown pytest.mark.slow - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.slow

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================================================= 4 passed, 1 warning in 0.04s ==============================================================================================================
root@Gavin:~/test/hook# 
```

这个输出展示了：

1. **启动时的环境信息**：
   - 平台、`Python` 版本、`pytest` 版本等。

2. **版本信息**：
   - 应用程序版本和 `Git` 提交 `ID`。

3. **运行参数信息**：
   - 配置文件路径和运行时的命令行参数。

4. **调试信息**：
   - 特定的调试环境变量值。

5. **收集阶段的信息**：
   - 收集到的测试用例数量，收集耗时。
   - 特定标记的测试用例数量。
   - 测试用例按类分类的数量。

## 详细解释

1. **添加命令行参数**：
   - 使用 `pytest_addoption` 钩子添加自定义命令行参数，使用户能够选择需要在报告头部显示的信息.`--config`，`--show-env`，`--show-version`，`--show-params` 和 `--show-debug` 被添加为命令行参数供用户选择。

2. **收集测试用例数量**：
   - 在 `pytest_report_collectionfinish` 中，通过 `len(items)` 获取收集到的测试用例的数量，并将其包含在报告中。

3. **分类测试用例**：
   - 为每个测试用例调用 `.cls`，并使用字典记录按类名分类后的测试用例数量。这有助于更好地理解每个测试类中的测试用例分布。

4. **标记信息统计**：
   - 使用特定标记（如 `slow`）统计测试用例数量，通过 `item.keywords` 检查每个测试用例的标记并统计。

5. **收集阶段耗时**：
   - 在 `pytest_configure` 钩子函数中记录测试收集开始时间，在 `pytest_report_collectionfinish` 钩子函数中计算并显示收集阶段耗时。

这样做能够确保我们在测试报告中清楚地了解所有收集到的测试用例信息，有助于全面理解和调试测试集。

## 扩展示例：输出格式的美化和优化

为了使输出更美观和易读，可以在生成报告时增加格式化。例如，添加分隔符和缩进，以提供更好的视觉效果。

### 美化后的conftest.py文件

```python
import pytest
import time
import platform
import sys
import subprocess
import os

collection_start_time = None

def pytest_configure(config):
    global collection_start_time
    collection_start_time = time.time()

def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="default_config.yaml", help="Path to the config file")
    parser.addoption("--show-env", action="store_true", help="Show environment information in the report")
    parser.addoption("--show-version", action="store_true", help="Show version information in the report")
    parser.addoption("--show-params", action="store_true", help="Show run parameters in the report")
    parser.addoption("--show-debug", action="store_true", help="Show debug information in the report")

def get_git_commit():
    try:
        commit_id = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
    except Exception:
        commit_id = "N/A"
    return commit_id

def pytest_report_header(config):
    header = []
    
    if config.getoption("--show-env"):
        header.extend([
            "=== Environment Information ===",
            f"Platform: {platform.platform()}",
            f"Python Version: {sys.version}",
            f"pytest Version: {pytest.__version__}",
        ])
    
    if config.getoption("--show-version"):
        header.extend([
            "=== Version Information ===",
            f"Application Version: 1.0.0",
            f"Git Commit ID: {get_git_commit()}",
        ])
    
    if config.getoption("--show-params"):
        config_file = config.getoption("--config")
        header.extend([
            "=== Run Parameters ===",
            f"Config File: {config_file}",
            f"Command Line Arguments: {config.invocation_params.args}",
        ])
    
    if config.getoption("--show-debug"):
        header.extend([
            "=== Debug Information ===",
            f"APP_DEBUG_MODE: {os.environ.get('APP_DEBUG_MODE', 'undefined')}",
            f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'undefined')}",
        ])
    
    return header

def pytest_report_collectionfinish(config, startdir, items):
    global collection_start_time
    collection_duration = time.time() - collection_start_time
    
    tests_by_class = {}
    tagged_tests = [item for item in items if 'slow' in item.keywords]
    num_tagged_tests = len(tagged_tests)
    
    for item in items:
        test_class = item.cls.__name__ if item.cls else 'NoClass'
        if test_class not in tests_by_class:
            tests_by_class[test_class] = 0
        tests_by_class[test_class] += 1
    
    report_lines = [
        "-" * 40,
        f"Collected {len(items)} tests",
        f"Collection duration: {collection_duration:.2f} seconds",
        f"Number of 'slow' tagged tests: {num_tagged_tests}"
    ]
    
    for test_class, count in tests_by_class.items():
        report_lines.append(f"{test_class}: {count} test{'s' if count != 1 else ''}")
    
    return report_lines

# 示例测试文件 tests/test_example.py
import pytest

@pytest.mark.slow
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert "pytest" in "pytest is fun"

class TestMath:
    def test_addition(self):
        assert 1 + 1 == 2
    
    def test_subtraction(self):
        assert 2 - 1 == 1
```

### 进一步优化的输出格式

通过增加分隔线和分类标题，使输出格式更加美观和易读。例如，添加 "===" 标记和 "-" 分隔线，有助于更好地突出不同信息的类别。

### 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree -l
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook# 
```
**重新执行命令**
在项目根目录下运行以下命令来查看改进后的输出格式：

```shell
pytest -s -v --config=custom_config.yaml --show-env --show-version --show-params --show-debug
```

#### 验证输出信息

控制台输出应包含所有在 `pytest_report_header` 和 `pytest_report_collectionfinish` 钩子中返回的信息，并体现美化后的格式。

#### 预期输出示例

```plaintext
root@Gavin:~/test/hook# pytest -s -v --config=custom_config.yaml --show-env --show-version --show-params --show-debug
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
fatal: not a git repository (or any of the parent directories): .git
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Platform: Linux-6.5.0-35-generic-x86_64-with-glibc2.38
Python Version: 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0]
pytest Version: 8.0.2
Application Version: 1.0.0
Git Commit ID: N/A
Config File: custom_config.yaml
Command Line Arguments: ('-s', '-v', '--config=custom_config.yaml', '--show-env', '--show-version', '--show-params', '--show-debug')
Debug Information:
APP_DEBUG_MODE: true
DATABASE_URL: sqlite:///:memory:
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 4 items                                                                                                                                                                                                                                       
Collected 4 tests
Collection duration: 0.10 seconds
Number of 'slow' tagged tests: 1
NoClass: 2 tests
TestMath: 2 tests

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED
tests/test_example.py::TestMath::test_addition PASSED
tests/test_example.py::TestMath::test_subtraction PASSED

=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py:3
  /root/test/hook/tests/test_example.py:3: PytestUnknownMarkWarning: Unknown pytest.mark.slow - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.slow

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================================================= 4 passed, 1 warning in 0.04s ==============================================================================================================
root@Gavin:~/test/hook# 
```

### 详细解释和总结

1. **`pytest_configure` 钩子**：
   - 在 `pytest_configure` 钩子函数中记录开始收集测试用例的时间，这样我们可以在 `pytest_report_collectionfinish` 钩子中计算收集过程的持续时间。

2. **通过命令行参数控制信息显示**：
   - 使用 `pytest_addoption` 钩子添加自定义命令行选项，使用户可以选择需要显示的信息（例如环境信息、版本信息、运行参数和调试信息）。

3. **信息格式化**：
   - 在 `pytest_report_header` 钩子中返回包含不同类别信息的字符串列表，使用 "===" 和 "-" 分隔线来美化输出格式，使信息更加可读。

4. **输出收集统计信息**：
   - 在 `pytest_report_collectionfinish` 钩子中，统计收集到的测试用例数量、分类统计信息和标记统计信息，并计算和显示收集过程的持续时间。

### 扩展功能和优化

- **动态标记统计**：
  - 可以进一步增强代码，使其支持动态标记统计。例如，让用户通过命令行参数输入需要统计的标记类型。

- **更多统计信息**：
  - 可以记录并展示更多统计信息，比如每个目录下测试文件的数量、每个测试类包含多少测试用例等。

- **更友好的输出格式**：
  - 通过使用外部库来美化输出，例如 `tabulate` 库可以将输出格式化为表格形式，进一步提升可读性。

# 小结

通过 `pytest_report_header` 和 `pytest_report_collectionfinish` 钩子，我们可以在测试报告的头部和收集完成信息中添加自定义信息。这些信息有助于对测试环境和配置信息进行详细记录，提高报告的可读性和可维护性。

