---
title: pytest hook系列之pytest_report_header
date: 2024-10-12 23:00:00
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
summary: pytest hook之pytest_report_header
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_report_header` 是`pytest`框架中的一个钩子函数，用于在测试报告的头部添加自定义信息，它在生成测试报告的头部时被触发。通过这个钩子函数，我们可以在测试报告的起始部分插入一些有用的自定义信息，如环境配置、版本信息、测试运行参数等，以便为测试结果提供更多的背景和上下文，从而帮助更好地理解和诊断测试结果。

# 使用场景

1. **环境信息**：在报告头部添加环境配置信息，如操作系统、Python 版本、依赖库版本等。
2. **版本信息**：在报告头部添加版本信息，如应用程序版本、代码仓库的提交 ID 等。
3. **运行参数**：在报告头部添加测试运行时的参数信息，如命令行参数、配置文件路径等。
4. **调试信息**：在报告头部添加调试信息，以便更好地分析和诊断测试结果。

# 参数

```python
def pytest_report_header(config, start_path, startdir):
    # config: pytest 的配置对象，包含有关当前测试会话的所有信息
    # start_path: The starting dir.
    # startdir: The starting dir (deprecated)
    pass
```

- `config`：pytest 的配置对象，包含有关当前测试会话的所有信息。
- `start_path`：测试收集开始的目录。
- `startdir`：测试收集开始的目录（废弃中）

# 示例代码

## 案例一：环境信息

目标：在测试报告头部添加环境配置信息，如操作系统、Python 版本、依赖库版本等。

步骤：
1. 使用 `pytest_report_header` 钩子函数。
2. 在钩子函数中插入环境信息收集和返回代码。

示例代码：

```python
# conftest.py
import pytest
import platform
import sys

def pytest_report_header(config):
    """在测试报告头部添加环境配置信息"""
    return [
        f"Platform: {platform.platform()}",
        f"Python Version: {sys.version}",
        f"pytest Version: {pytest.__version__}",
    ]

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：
- 使用 `platform.platform()` 获取操作系统平台信息。
- 使用 `sys.version` 获取 Python 版本信息。
- 使用 `pytest.__version__` 获取 pytest 版本信息。
- 在 `pytest_report_header` 钩子函数中返回一个包含这些信息的列表。

## 案例二：版本信息

目标：在测试报告头部添加版本信息，如应用程序版本、代码仓库的提交 ID 等。

步骤：
1. 使用 `pytest_report_header` 钩子函数。
2. 在钩子函数中插入版本信息收集和返回代码。

示例代码：

```python
# conftest.py
import pytest
import subprocess

def get_git_commit():
    """获取当前代码仓库的提交 ID"""
    try:
        commit_id = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
    except Exception:
        commit_id = "N/A"
    return commit_id

def pytest_report_header(config):
    """在测试报告头部添加版本信息"""
    return [
        f"Application Version: 1.0.0",
        f"Git Commit ID: {get_git_commit()}",
    ]

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：
- 使用 `subprocess.check_output` 命令获取当前代码仓库的提交 ID，并通过 `strip()` 和 `decode()` 方法处理输出。
- 在 `pytest_report_header` 钩子函数中返回一个包含应用程序版本和 Git 提交 ID 的列表。

## 案例三：运行参数

目标：在测试报告头部添加测试运行时的参数信息，如命令行参数、配置文件路径等。

步骤：
1. 使用 `pytest_report_header` 钩子函数。
2. 在钩子函数中插入运行参数收集和返回代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="default_config.yaml", help="Path to the config file")

def pytest_report_header(config):
    """在测试报告头部添加运行参数信息"""
    config_file = config.getoption("--config")
    return [
        f"Config File: {config_file}",
        f"Command Line Arguments: {config.invocation_params.args}",
    ]

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：
- 使用 `pytest_addoption` 钩子为测试运行添加自定义命令行参数选项（如 `--config`）。
- 在 `pytest_report_header` 钩子函数中使用 `config.getoption` 获取自定义命令行参数的值，并将其添加到返回信息中。

## 案例四：调试信息

目标：在测试报告头部添加调试信息，以便更好地分析和诊断测试结果。

步骤：
1. 使用 `pytest_report_header` 钩子函数。
2. 在钩子函数中插入调试信息收集和返回代码。

示例代码：

```python
# conftest.py
import pytest
import os

def pytest_report_header(config):
    """在测试报告头部添加调试信息"""
    debug_env_vars = {
        "APP_DEBUG_MODE": os.environ.get("APP_DEBUG_MODE", "undefined"),
        "DATABASE_URL": os.environ.get("DATABASE_URL", "undefined"),
    }
    return [
        "Debug Information:",
        f"APP_DEBUG_MODE: {debug_env_vars['APP_DEBUG_MODE']}",
        f"DATABASE_URL: {debug_env_vars['DATABASE_URL']}",
    ]

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：
- 使用 `os.environ.get` 函数获取调试相关的环境变量（如 `APP_DEBUG_MODE` 和 `DATABASE_URL`）。
- 在 `pytest_report_header` 钩子函数中将这些环境变量的信息添加到返回的列表中。

## 运行和验证

确保目录结构如下：

```shell
```

在项目根目录下运行以下命令：

```shell
pytest -s -v --cache-clear
```

### 验证输出信息

根据具体的案例，控制台输出应包含自定义的报告头部信息，如环境配置信息、版本信息、运行参数和调试信息等。

### 控制台输出示例

**案例一：环境信息**

会在屏幕上显示`Platform、Python Version和pytest Version`信息，参考如下：

```plaintext
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Platform: Linux-6.5.0-35-generic-x86_64-with-glibc2.38
Python Version: 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0]
pytest Version: 8.0.2
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example PASSED

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例二：版本信息**

```plaintext
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
fatal: not a git repository (or any of the parent directories): .git
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Application Version: 1.0.0
Git Commit ID: N/A
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example PASSED

=================================================================================================================== 1 passed in 0.05s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：运行参数**

```plaintext
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Config File: default_config.yaml
Command Line Arguments: ('-s', '-v')
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例四：调试信息**

```plaintext
root@Gavin:~/test/hook# export APP_DEBUG_MODE=DEBUG
root@Gavin:~/test/hook# export DEBUG DATABASE_URL='192.168.1.211'
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Debug Information:
APP_DEBUG_MODE: DEBUG
DATABASE_URL: 192.168.1.211
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

### 详细解释

当然，接下来继续详细解释每个案例的实现和应用场景。

### 详细解释

1. **添加环境信息**（案例一）：
   - 使用 `platform.platform()` 函数获取操作系统平台信息。
   - 使用 `sys.version` 获取 `Python` 解释器版本信息。
   - 使用 `pytest.__version__` 获取当前 pytest 的版本信息。
   - 在 `pytest_report_header` 钩子函数中返回包含这些信息的字符串列表，这些字符串将被插入到测试报告的头部。

2. **添加版本信息**（案例二）：
   - 使用 `subprocess` 模块获取当前代码仓库的 `Git` 提交 `ID`。`subprocess.check_output(['git', 'rev-parse', 'HEAD'])` 命令用于获取当前的提交哈希值。
   - 捕获获取 `Git` 提交 `ID` 过程中可能出现的异常，并提供默认值 "N/A" 以防止异常中断流程。
   - 在 `pytest_report_header` 钩子函数中返回包含应用程序版本和 `Git` 提交 `ID` 的字符串列表，这些信息将被插入测试报告的头部。

3. **添加运行参数**（案例三）：
   - 使用 `pytest_addoption` 钩子为 `pytest` 命令行添加自定义选项，例如配置文件路径选项 `--config`。
   - 在 `pytest_report_header` 钩子函数中使用 `config.getoption` 获取命令行传递的配置文件路径参数。
   - 使用 `config.invocation_params.args` 获取所有的命令行参数，方便在报告头部显示执行测试时的完整命令行。
   - 返回包含配置文件路径和命令行参数的字符串列表，这些信息将被插入测试报告的头部。

4. **添加调试信息**（案例四）：
   - 使用 `os.environ.get` 函数获取特定环境变量（如 `APP_DEBUG_MODE` 和 `DATABASE_URL`）的值。如果变量未设置则返回默认值 "undefined"。
   - 在 `pytest_report_header` 钩子函数中返回包含环境变量值的字符串列表，这些信息将被插入测试报告的头部。

### 实现步骤

这些步骤确保在适当的钩子函数中插入代码来实现所需功能。

#### 步骤一：编写 `pytest_report_header` 钩子函数

```python
import pytest
import platform
import sys
import subprocess
import os

def pytest_report_header(config):
    """在测试报告头部添加自定义信息"""
    # 获取环境信息
    environment_info = [
        f"Platform: {platform.platform()}",
        f"Python Version: {sys.version}",
        f"pytest Version: {pytest.__version__}",
    ]
    
    # 获取版本信息
    try:
        commit_id = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
    except Exception:
        commit_id = "N/A"
    version_info = [
        f"Application Version: 1.0.0",
        f"Git Commit ID: {commit_id}",
    ]
    
    # 获取运行参数
    config_file = config.getoption("--config") if "--config" in config.invocation_params.args else "default_config.yaml"
    run_params_info = [
        f"Config File: {config_file}",
        f"Command Line Arguments: {config.invocation_params.args}",
    ]
    
    # 获取调试信息
    debug_info = [
        "Debug Information:",
        f"APP_DEBUG_MODE: {os.environ.get('APP_DEBUG_MODE', 'undefined')}",
        f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'undefined')}",
    ]
    
    # 合并所有信息
    return environment_info + version_info + run_params_info + debug_info

def pytest_addoption(parser):
    """添加自定义命令行参数"""
    parser.addoption("--config", action="store", default="default_config.yaml", help="Path to the config file")
```

#### 步骤二：编写测试文件

```python
# tests/test_example.py
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert "pytest" in "pytest is fun"
```

### 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook# 
root@Gavin:~/test/hook# tree
.
├── conftest.py
├── custom_config.yaml
└── tests
    └── test_example.py

2 directories, 3 files
root@Gavin:~/test/hook# 
```

#### 执行测试命令

在项目根目录下运行以下命令：

```shell
pytest -s -v --config=custom_config.yaml
```

#### 验证输出信息

控制台输出应包含所有在 `pytest_report_header` 钩子中返回的自定义信息，示例如下：

```plaintext
root@Gavin:~/test/hook# export DATABASE_URL=sqlite:///:memory:
root@Gavin:~/test/hook# export APP_DEBUG_MODE=true
root@Gavin:~/test/hook# pytest -s -v --config=custom_config.yaml
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
Config File: default_config.yaml
Command Line Arguments: ('-s', '-v', '--config=custom_config.yaml')
Debug Information:
APP_DEBUG_MODE: true
DATABASE_URL: sqlite:///:memory:
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

在以上输出中，可以看到测试报告头部包含了平台信息、`Python` 版本、`pytest` 版本、应用程序版本、`Git` 提交 `ID`、配置文件、命令行参数以及调试信息。这些信息有助于提供测试环境和配置的背景，从而便于问题的排查和分析。

### 进一步的考虑

1. **信息来源的多样性**：
   - 可以扩展 `pytest_report_header` 钩子函数，从更多的来源收集信息，例如从配置文件、环境变量、外部服务获取的信息等。

2. **可配置性**：
   - 提供选项让用户选择需要在报告头部显示哪些信息，以提高灵活性。例如，可以为自定义钩子增加配置选项，以便用户根据需要开启或关闭特定信息。

3. **信息格式化**：
   - 确保输出的格式清晰、统一，使格式化后的信息便于阅读和理解。例如，可以对输出字符串进行对齐和分组，以增加可读性。

### 扩展示例：提供选项选择信息

我们可以进一步扩展 `conftest.py`，增加配置选项以便用户根据需要选择显示哪些信息。

#### 增强版本的`conftest.py`内容

```python
import pytest
import platform
import sys
import subprocess
import os

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

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

### 配置和运行示例

可以通过以下不同的命令行选项运行测试，以查看不同的报告头部信息：

#### 只显示环境信息

```shell
pytest -s -v --show-env
```

#### 只显示版本信息

```shell
pytest -s -v --show-version
```

#### 显示全部信息

```shell
pytest -s -v --show-env --show-version --show-params --show-debug --config=custom_config.yaml
```

#### 输出信息参考如下

```shell
root@Gavin:~/test/hook# pytest -s -v --show-env
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Platform: Linux-6.5.0-35-generic-x86_64-with-glibc2.38
Python Version: 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0]
pytest Version: 8.0.2
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# pytest -s -v --show-version
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
fatal: not a git repository (or any of the parent directories): .git
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
Application Version: 1.0.0
Git Commit ID: N/A
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# pytest -s -v --show-env --show-version --show-params --show-debug --config=custom_config.yaml
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
Command Line Arguments: ('-s', '-v', '--show-env', '--show-version', '--show-params', '--show-debug', '--config=custom_config.yaml')
Debug Information:
APP_DEBUG_MODE: true
DATABASE_URL: sqlite:///:memory:
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

### 详细解释（补充）

- **`pytest_addoption` 钩子**：
  - 增加自定义的命令行选项，使用户可以通过命令行参数选择需要显示的信息。
  - 例如，增加了 `--show-env`, `--show-version`, `--show-params`, `--show-debug`，分别对应环境信息、版本信息、运行参数和调试信息。

- **`pytest_report_header` 的增强版本**：
  - 根据用户通过命令行选项选择的信息，动态决定要在头部报告中添加哪些信息。
  - 使用 `config.getoption` 方法获取命令行参数，根据用户选择的选项动态构建头部信息列表。

# 总结

通过 `pytest_report_header` 钩子，我们可以在测试报告的头部添加自定义的信息，如环境配置信息、版本信息、运行参数和调试信息等。这些信息有助于对于测试环境和配置信息进行详细记录，提高报告的可读性和可维护性。
