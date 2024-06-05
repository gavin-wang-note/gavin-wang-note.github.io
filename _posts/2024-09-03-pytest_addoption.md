---
title: pytest hook系列之pytest_addoption
date: 2024-09-03 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-18.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_addoption
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation

---

# Overview

`pytest_addoption` 是一个钩子函数，允许你向 `pytest` 注册命令行选项、环境变量，或者通过 `ini` 文件定义的配置选项。通过这个钩子，可以在 `pytest` 命令行参数或配置文件中添加自定义选项，以便在测试期间访问这些选项的值。

# 使用场景

* 命令行选项：为测试添加自定义命令行参数，以改变测试行为或传递参数
* 配置文件选项：为 pytest.ini 文件添加新的配置选项，提供灵活的配置方式
* 环境变量：通过命令行参数控制测试期间使用的一些环境变量
* 测试配置管理：通过命令行选项动态地管理和配置测试的行为、路径、URL等


# 参数

* parser: 命令行参数解析器，用于添加新的命令行选项和配置选项(这是一个解析器对象，用于添加和管理命令行参数)
* pluginmanager（可选）：插件管理器实例，可以用来注册和管理插件

parser参数值信息：

* action：指定如何处理参数值。常见的值包括 store_true（存储布尔值），store_false（存储反向布尔值），store_true（存储真值），store_false（存储假值）等。
* default：默认值，可以是任何数据类型
* help：帮助信息，描述该参数的用途


# 示例代码

以下是一个使用 `pytest_addoption` 的示例，展示如何添加和使用自定义的命令行选项和配置选项：

## 定义命令行选项和配置项

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption(
        "--my-option", action="store", default="default_value",
        help="This is a custom command line option for pytest"
    )
    parser.addini("my_config_option", "This is a custom configuration option", default="ini_default_value")
```

## 在测试中访问这些选项

```python
# test_example.py
import pytest

def test_command_line_option(pytestconfig):
    # Accessing the command line option
    my_option = pytestconfig.getoption("--my-option")
    assert my_option == "expected_value"

def test_config_option(pytestconfig):
    # Accessing the ini configuration option
    my_config_option = pytestconfig.getini("my_config_option")
    assert my_config_option == "ini_value"
```

## 详细说明

* `conftest.py`：在 `conftest.py` 文件中通过 `pytest_addoption` 钩子向 `pytest` 添加了一个命令行选项 `--my-option`，以及一个配置选项 `my_config_option`
* `test_example.py`：在测试用例文件 `test_example.py` 中，使用 `pytestconfig` 对象来访问这些选项


# 运行示例

为了测试命令行选项，需要在运行 `pytest` 时传递 `--my-option` 参数：

```shell
pytest --my-option="expected_value"
```

执行效果如下：

```shell
root@Gavin:~/test/hook# pytest --my-option="expected_value"
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                        

test_example.py .F                                                                                                                                                                                                                                 [100%]

======================================================================================================================== FAILURES ========================================================================================================================
___________________________________________________________________________________________________________________ test_config_option ___________________________________________________________________________________________________________________

pytestconfig = <_pytest.config.Config object at 0x7f088db00a50>

    def test_config_option(pytestconfig):
        # Accessing the ini configuration option
        my_config_option = pytestconfig.getini("my_config_option")
>       assert my_config_option == "ini_value"
E       AssertionError: assert 'ini_default_value' == 'ini_value'
E         
E         - ini_value
E         + ini_default_value

test_example.py:11: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_config_option - AssertionError: assert 'ini_default_value' == 'ini_value'
============================================================================================================== 1 failed, 1 passed in 0.10s ===============================================================================================================
root@Gavin:~/test/hook#
```

为了测试配置文件选项，可以在根目录下创建一个 `pytest.ini` 文件，并添加自定义配置：

```ini
# pytest.ini
[pytest]
my_config_option = ini_value
```

然后运行 `pytest`：

```shell
pytest
```

运行效果参考如下：

```shell
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                        

test_example.py F.                                                                                                                                                                                                                                 [100%]

======================================================================================================================== FAILURES ========================================================================================================================
________________________________________________________________________________________________________________ test_command_line_option ________________________________________________________________________________________________________________

pytestconfig = <_pytest.config.Config object at 0x73efac6695d0>

    def test_command_line_option(pytestconfig):
        # Accessing the command line option
        my_option = pytestconfig.getoption("--my-option")
>       assert my_option == "expected_value"
E       AssertionError: assert 'default_value' == 'expected_value'
E         
E         - expected_value
E         + default_value

test_example.py:6: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_command_line_option - AssertionError: assert 'default_value' == 'expected_value'
============================================================================================================== 1 failed, 1 passed in 0.10s ===============================================================================================================
root@Gavin:~/test/hook#
```

同时携带上`--my-option`参数，执行效果如下：

```shell
root@Gavin:~/test/hook# pytest -v --my-option="expected_value"
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                        

test_example.py::test_command_line_option PASSED                                                                                                                                                                                                   [ 50%]
test_example.py::test_config_option PASSED                                                                                                                                                                                                         [100%]

=================================================================================================================== 2 passed in 0.04s ====================================================================================================================
root@Gavin:~/test/hook#
```

这是因为`pytest`在执行过程中，自动读取了`pytest.ini`文件中配置选项，相当于携带了两个参数(`--my-option`和`my_config_option`)。



# 如何使用pytest_addoption来实现多环境配置？

请参考我的另外一篇文章中的示例：[pytest自动化测试执行环境切换的几种解决方案](https://gavin-wang-note.github.io/2024/08/29/pytest_change_env_url_solution/)



# 小结

通过 `pytest_addoption` 钩子，可以灵活地向 `pytest` 添加自定义命令行选项和配置选项。这使得测试框架更加灵活和可配置，适合用于各种复杂测试场景。使用该功能，可以根据具体的配置和需求动态地调整测试行为和环境，极大地增强了测试的可控性和扩展性。
