---
title: 测试用例重复执行插件pytest-repeat源码解读
date: 2024-11-02 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-26.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 测试用例重复执行插件pytest-repeat源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

`pytest-repeat`插件允许用户多次重复运行每个测试函数(测试用例)，本文介绍一下`pytest-repeat`插件源码解读。


下载官方最新版`tar`包解压后展示如下：

```python
root@Gavin:~/pytest_plugin/pytest_repeat-0.9.3# ll
total 60
drwxr-xr-x 3 root root  4096 Jul  2 09:04 ./
drwxr-xr-x 3 root root  4096 Jul  2 09:01 ../
-rw-r--r-- 1 root root  1805 Oct 10  2023 CHANGES.rst
drwxr-xr-x 3 root root  4096 Jul  2 09:01 .github/
-rw-r--r-- 1 root root    85 Oct 10  2023 .gitignore
-rw-r--r-- 1 root root   204 Oct 10  2023 LICENSE
-rw-r--r-- 1 root root  4918 Oct 10  2023 PKG-INFO
-rw-r--r-- 1 root root  1294 Oct 10  2023 pyproject.toml
-rw-r--r-- 1 root root  2134 Oct 10  2023 pytest_repeat.py
-rw-r--r-- 1 root root  3501 Oct 10  2023 README.rst
-rw-r--r-- 1 root root 11002 Oct 10  2023 test_repeat.py
-rw-r--r-- 1 root root   420 Oct 10  2023 tox.ini
```

原以为内容会比较多，解压打开后发现非常的精简，这么强悍的功能，代码量这么少，着实让人意外，但也说明了`pytest hook`的强悍。

核心内容就一个：`pytest_repeat.py`，它是插件源码，而`test_repeat.py`则是测试`pytest_repeat.py`代码的测试代码。

# 核心源码介绍

```python
# Content of pytest_repeat.py
root@Gavin:~/pytest_plugin/pytest_repeat-0.9.3# cat pytest_repeat.py 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
import warnings
from unittest import TestCase

import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--count',
        action='store',
        default=1,
        type=int,
        help='Number of times to repeat each test')

    parser.addoption(
        '--repeat-scope',
        action='store',
        default='function',
        type=str,
        choices=('function', 'class', 'module', 'session'),
        help='Scope for repeating tests')


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'repeat(n): run the given test function `n` times.')


class UnexpectedError(Exception):
    pass


@pytest.fixture()
def __pytest_repeat_step_number(request):
    marker = request.node.get_closest_marker("repeat")
    count = marker and marker.args[0] or request.config.option.count
    if count > 1:
        try:
            return request.param
        except AttributeError:
            if issubclass(request.cls, TestCase):
                warnings.warn(
                    "Repeating unittest class tests not supported")
            else:
                raise UnexpectedError(
                    "This call couldn't work with pytest-repeat. "
                    "Please consider raising an issue with your usage.")


@pytest.hookimpl(trylast=True)
def pytest_generate_tests(metafunc):
    count = metafunc.config.option.count
    m = metafunc.definition.get_closest_marker('repeat')
    if m is not None:
        count = int(m.args[0])
    if count > 1:
        metafunc.fixturenames.append("__pytest_repeat_step_number")

        def make_progress_id(i, n=count):
            return '{0}-{1}'.format(i + 1, n)

        scope = metafunc.config.option.repeat_scope
        metafunc.parametrize(
            '__pytest_repeat_step_number',
            range(count),
            indirect=True,
            ids=make_progress_id,
            scope=scope
        )
root@Gavin:~/pytest_plugin/pytest_repeat-0.9.3#
```

解读内容如下：

* 导入必要的模块：
  - `warnings`：用于发出警告。
  - `TestCase`：来自 `unittest` 模块，用于检查测试是否是 `unittest` 风格的测试。
  - `pytest`：导入 `pytest` 框架。

* `pytest_addoption` 函数：
  - 这个函数用于向 `pytest` 添加命令行选项。
  - `--count`：用于设置每个测试重复的次数，默认为 1。
  - `--repeat-scope`：用于设置重复测试的作用域，可以是 `function、class、module` 或 `session`，默认为 `function`。

* `pytest_configure` 函数：
  - 这个函数在 `pytest` 配置阶段被调用。
  - `config.addinivalue_line`：向配置文件中添加一个标记，允许使用 `repeat` 标记来指定测试函数重复的次数。

* `UnexpectedError` 类：
  - 自定义异常，用于在插件中抛出特定的错误。

* `__pytest_repeat_step_number` 函数：
  - 这是一个 `pytest fixture`，用于生成重复测试的步数。
  - `marker`：获取测试节点上最近的 `repeat` 标记。
  - `count`：获取标记参数或配置中的 `count` 选项。
  - 如果 `count` 大于 1，尝试返回 `request.param`，如果失败则发出警告或抛出异常。

* `pytest.hookimpl(trylast=True)` 装饰器：
  - 这个装饰器用于注册 `pytest` 的钩子实现，`trylast=True` 表示这个实现应该在其他实现之后尝试。

* `pytest_generate_tests` 函数：
  - 这个函数用于生成测试参数。
  - `count`：从配置中获取重复次数。
  - `m`：获取测试定义上的 `repeat` 标记。
  - 如果存在 `repeat` 标记，则使用标记中的值作为 `count`。
  - 如果 `count` 大于 1，将 `__pytest_repeat_step_number` 添加到 `fixture` 名称列表中，并使用 `parametrize` 方法来生成重复的测试参数。

* `make_progress_id` 函数：
  - 这是一个辅助函数，用于生成测试进度的标识符。

* `scope` 变量：
  - 根据配置中的 `repeat_scope` 选项设置参数化的作用域。

* `parametrize` 方法：
  - 用于为 `__pytest_repeat_step_number fixture` 生成参数，参数是从 0 到 `count-1` 的整数范围。
  - `ids` 参数使用 `make_progress_id` 函数生成测试的标识符。
  - `scope` 参数设置参数化的作用域。

从源码看，`pytest-repeat`插件有如下特性：

* 支持用例指定运行次数（`--count`参数）
* 支持用例执行范围（`--repeat-scope`参数，默认`function`级别）
* 支持`mark`标记的使用（`@pytest.mark.repeat(N)`，如`@pytest.mark.repeat(3)`表示重复三次，可放在测试用例`function`层，也可放在`suit`层，即`class`层）
* 不支持`Python Unittest`测试用例的`repeat`，但`Python Unittest`测试用例还是会正常执行（即执行一次，和是否携带`--count`参数无关，携带了则有个`warning`）

如果对于`parametrize` 方法不了解的，可以查看下图介绍，更详细信息请另行查询资料：

<img class="shadow" src="/img/in-post/paramerize参数介绍.png" width="1200">


# 问题答疑解惑

## 问题1：用例既有mark.repeat标记，又指定了--count参数，到底哪个有效？

以具体示例说话：

```python
# Content of test_repeat_example.py 
import pytest

def test_case_without_mark():
    pass

@pytest.mark.repeat(5)
def test_case_mark_repeat_five():
    pass

@pytest.mark.repeat(2)
def test_case_mark_repeat_twice():
    pass
```

运行效果：

```shell
root@Gavin:~/pytest_plugin/test# pytest -s -v --count=3
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-42-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 10 items                                                                                                                                                                                                                                       

test_repeat_example.py::test_case_without_mark[1-3] PASSED
test_repeat_example.py::test_case_without_mark[2-3] PASSED
test_repeat_example.py::test_case_without_mark[3-3] PASSED
test_repeat_example.py::test_case_mark_repeat_five[1-5] PASSED
test_repeat_example.py::test_case_mark_repeat_five[2-5] PASSED
test_repeat_example.py::test_case_mark_repeat_five[3-5] PASSED
test_repeat_example.py::test_case_mark_repeat_five[4-5] PASSED
test_repeat_example.py::test_case_mark_repeat_five[5-5] PASSED
test_repeat_example.py::test_case_mark_repeat_twice[1-2] PASSED
test_repeat_example.py::test_case_mark_repeat_twice[2-2] PASSED

=================================================================================================================== 10 passed in 0.05s ===================================================================================================================
root@Gavin:~/pytest_plugin/test#
```

测试用例有三个，一个没做任何`mark.repeat`标记，一个标记为重复执行5次(`@pytest.mark.repeat(2)`)，一个则标记重复运行2次(`@pytest.mark.repeat(2)`)，传递的重复执行参数(`--count=3`)则是3，从实际执行效果来看：

* 未做`mark.repeat`标记的，按`--count`参数值重复用例执行
* 已做`mark.repeat`标记的，按用例中`mark.repeat(N)`中`N`次数执行，不受参数`--count`的影响。


## 问题2: 指定count参数后，是否会影响scope

比较关心`count`参数与`fixture scope`是否冲突，引发每个用例的执行都会执行`fixture`？

依然以示例解释，参考如下：

```python
# Content of test_repeat_scopes.py
import pytest

# 会话级别的 fixture
@pytest.fixture(scope="session")
def session_resource():
    print("Setup session resource")
    yield
    print("Teardown session resource")

# 模块级别的 fixture
@pytest.fixture(scope="module")
def module_resource():
    print("Setup module resource")
    yield
    print("Teardown module resource")

# 类级别的 fixture
@pytest.fixture(scope="class")
def class_resource():
    print("Setup class resource")
    yield
    print("Teardown class resource")

# 函数级别的 fixture
@pytest.fixture(scope="function")
def function_resource():
    print("Setup function resource")
    yield
    print("Teardown function resource")

# 使用不同作用域的 fixture 的测试类
class TestScopes:
    def test_session_scope(self, session_resource):
        print("Running test_session_scope")

    def test_module_scope(self, module_resource):
        print("Running test_module_scope")

    def test_class_scope(self, class_resource):
        print("Running test_class_scope")

    def test_function_scope(self, function_resource):
        print("Running test_function_scope")
```

用例执行效果，参考如下：

```shell
root@Gavin:~/pytest_plugin/test# pytest -s -v test_repeat_scopes.py --count=2
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-42-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 8 items                                                                                                                                                                                                                                        

test_repeat_scopes.py::TestScopes::test_session_scope[1-2] Setup session resource
Running test_session_scope
PASSED
test_repeat_scopes.py::TestScopes::test_session_scope[2-2] Running test_session_scope
PASSED
test_repeat_scopes.py::TestScopes::test_module_scope[1-2] Setup module resource
Running test_module_scope
PASSED
test_repeat_scopes.py::TestScopes::test_module_scope[2-2] Running test_module_scope
PASSED
test_repeat_scopes.py::TestScopes::test_class_scope[1-2] Setup class resource
Running test_class_scope
PASSED
test_repeat_scopes.py::TestScopes::test_class_scope[2-2] Running test_class_scope
PASSED
test_repeat_scopes.py::TestScopes::test_function_scope[1-2] Setup function resource
Running test_function_scope
PASSEDTeardown function resource

test_repeat_scopes.py::TestScopes::test_function_scope[2-2] Setup function resource
Running test_function_scope
PASSEDTeardown function resource
Teardown class resource
Teardown module resource
Teardown session resource


=================================================================================================================== 8 passed in 0.04s ====================================================================================================================
root@Gavin:~/pytest_plugin/test#
```

得到如下资讯：

* 每个测试用例都会被执行指定的`count`数
* `pytest-repeat scope`不同，对应的`fixture`执行的次数亦不同，如`scope=session`，则无论执行`--count`是多少，对应的的`fixture`只执行一次。


# 小结

`pytest-repeat`此插件用于指定测试用例执行次数，常用于验证测试用例的健壮性，或复现某些比较难以复现的问题。
