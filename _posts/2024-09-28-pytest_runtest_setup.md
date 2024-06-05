---
title: pytest hook系列之pytest_runtest_setup
date: 2024-09-28 23:00:00
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
summary: pytest hook之pytest_runtest_setup
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_setup` 是`pytest`框架中的一个钩子函数，它在每个测试项开始执行前被调用，允许我们在每个测试项开始执行前插入自定义逻辑。通过这个钩子，我们可以在测试项开始前进行特定的设置或初始化操作，如环境变量设置、资源初始化等，从而为测试的准备和环境配置提供支持。

# 使用场景

1. **测试项准备**：在每个测试项开始前进行准备操作，如数据初始化、配置加载等。
2. **环境设置**：在测试项开始前设置环境变量、配置文件等。
3. **初始化资源**：在测试项开始前初始化所需的资源，如数据库连接、文件句柄等。

# 参数

```python
def pytest_runtest_setup(item):
    # item: 被采集到的测试项对象，包含测试项的所有信息
    pass
```

- `item`：被采集到的测试项对象，包含测试项的所有信息。

# 具体场景案例、步骤、示例代码与注释

## 案例一：在测试项开始前加载配置文件

目标：在每个测试项开始前加载特定的配置文件，并将其内容存储在环境变量中供测试项使用。

步骤：
1. 使用 `pytest_runtest_setup` 钩子函数。
2. 在钩子函数中加载配置文件并设置环境变量。

示例代码：

```python
# conftest.py
import pytest
import json
import os

def pytest_runtest_setup(item):
    # 在测试项开始前加载配置文件
    with open('config.json') as f:
        config = json.load(f)
    os.environ["CONFIG"] = json.dumps(config)
    print(f"Loaded configuration for test: {item.nodeid}")

# 示例配置文件 `config.json`
{
    "database": "test_db",
    "host": "localhost"
}

# 示例测试文件 `tests/test_example.py`
def test_example():
    config = json.loads(os.getenv("CONFIG"))
    assert config["database"] == "test_db"
    assert config["host"] == "localhost"
```

**注释**：
- 在 `pytest_runtest_setup` 钩子函数中，加载配置文件 `config.json` 并设置环境变量 `CONFIG`，以便测试项中使用该配置。

## 案例二：在测试项开始前初始化数据库连接

目标：在每个测试项开始前初始化数据库连接，并在测试项中使用该连接。

步骤：
1. 使用 `pytest_runtest_setup` 钩子函数。
2. 在钩子函数中初始化数据库连接并传递给测试项。

示例代码：

```python
# conftest.py
import pytest
import sqlite3

def pytest_runtest_setup(item):
    # 在测试项开始前初始化数据库连接
    item.db_connection = sqlite3.connect(':memory:')
    print(f"Initialized database connection for test: {item.nodeid}")

# 示例测试文件 `tests/test_example.py`
def test_example(request):
    db_connection = request.node.db_connection
    cursor = db_connection.cursor()
    cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)')
    cursor.execute('INSERT INTO test (value) VALUES ("test_value")')
    db_connection.commit()
    
    cursor.execute('SELECT value FROM test WHERE id=1')
    result = cursor.fetchone()
    assert result[0] == "test_value"
```

**注释**：
- 在 `pytest_runtest_setup` 钩子函数中，初始化数据库连接并将其附加到测试项对象。测试项中通过 `request.node.db_connection` 获取该连接并使用。

## 案例三：在测试项开始前设置特定的标志

目标：在每个测试项开始前设置特定的标志，并在测试项中检查该标志。

步骤：
1. 使用 `pytest_runtest_setup` 钩子函数。
2. 在钩子函数中设置特定的标志。

示例代码：

```python
# conftest.py
import pytest

def pytest_runtest_setup(item):
    # 在测试项开始前设置特定的标志
    item.test_marker = "start"
    print(f"Setting marker for test: {item.nodeid}")

# 示例测试文件 `tests/test_example.py`
def test_example(request):
    assert request.node.test_marker == "start"
```

**注释**：
- 在 `pytest_runtest_setup` 钩子函数中，设置特定的标志 `test_marker`，以便测试项中检查该标志。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree 
.
├── config.json
├── conftest.py
└── tests
    └── test_example.py

2 directories, 3 files
root@Gavin:~/test/hook#
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

### 验证输出信息

根据不同的案例，控制台输出应显示测试项开始前的自定义逻辑执行结果，如配置加载信息、数据库连接初始化信息和标志设置信息。

### 控制台输出示例

**案例一：在测试项开始前加载配置文件**

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
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example Loaded configuration for test: tests/test_example.py::test_example
PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook
```

**案例二：在测试项开始前初始化数据库连接**

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
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example Initialized database connection for test: tests/test_example.py::test_example
PASSED

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：在测试项开始前设置特定的标志**

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
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example Setting marker for test: tests/test_example.py::test_example
PASSED

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

### 详细解释

1. **加载配置文件**
   - 在 `pytest_runtest_setup` 钩子函数中，加载配置文件 `config.json` 并设置环境变量 `CONFIG`，以便测试项中使用该配置。
  
2. **初始化数据库连接**
   - 在 `pytest_runtest_setup` 钩子函数中，初始化数据库连接并将其附加到测试项对象。测试项中通过 `request.node.db_connection` 获取该连接并使用。

3. **设置特定的标志**
   - 在 `pytest_runtest_setup` 钩子函数中，设置特定的标志 `test_marker`，以便测试项中检查该标志。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的 pytest 版本支持 `pytest_runtest_setup` 钩子。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，配置文件 `config.json` 和测试文件如 `test_example.py` 放在 `tests` 目录你且符合 pytest 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台输出，确认测试项开始前的自定义逻辑执行结果符合预期。

# 总结

通过详细介绍 `pytest_runtest_setup` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是加载配置文件、初始化数据库连接，还是设置特定的标志，都能为你提供强大的工具，增强测试的准备和环境配置能力。
