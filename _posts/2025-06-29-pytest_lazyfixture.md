---
title: 测试用例依赖之pytest-lazy-fixture源码解读 
date: 2025-06-29 22:00:00
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
summary: 试用例依赖之pytest-lazy-fixture源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-lazy-fixture` 是一个用于延迟加载 `pytest fixture` 的插件，它使得在使用 `pytest` 编写测试时可以延迟 `fixture` 的创建直至实际需要时(如仅在需要时才加载 `fixture`，而不是在每个测试用例之前都加载)。这在一些特定测试场景下非常有用，尤其是当你需要在测试参数化（`parametrization`）中使用 `fixtures`，但不想在测试参数化声明时立即实例化它们。

本文先介绍一下`pytest-lazy-fixture`的使用，最后再解读其源码。

# pytest-lazy-fixture的使用

## 安装 pytest-lazy-fixture

你可以使用 `pip` 来安装这个插件：

```shell
pip install pytest-lazy-fixture
```

## 主要特性

* 提高测试执行效率：通过延迟加载`fixture`，可以减少不必要的`fixture`加载操作，从而提高测试的执行速度。
* 灵活的条件加载：可以根据不同的条件来决定是否加载`fixture`，从而更好地控制测试用例的行为。
* 无缝集成：`pytest-lazy-fixture`与`pytest`框架无缝集成，使用起来非常方便。
* 兼容性：`pytest-lazy-fixture`与其他`pytest`插件和功能兼容，可以与其他插件一起使用，以满足特定的测试需求。


## 使用场景

* **优化测试性能**：对于一些创建代价较高的`fixture`，使用`pytest-lazy-fixture`可以在不影响测试的情况下，仅在必要时进行创建。
* **处理复杂的fixture依赖**：在`fixture`之间有复杂的依赖关系时，可以根据测试用例的需要动态决定加载哪个 `fixture`。
* **参数化测试**：在使用 `@pytest.mark.parametrize` 时，能够更灵活地处理`fixture`作为参数。
  当你希望使用 `fixtures` 作为参数化测试的一部分，但又不想这些 `fixtures` 在所有测试用例中都被加载时。
  当你使用参数化让测试用例遍历不同的 `fixture` 组合，但是你希望避免不使用的 `fixture` 被初始化。
* **条件性 fixture 使用**：当某些 `fixtures` 的创建过程开销较大，仅在某些特定的测试用例中需要使用时。


## 示例


假设有两个`fixture`，但只希望根据测试用例的不同选择性地使用它们：

```python
# content of test_lazy_fixture_v1.py
import pytest

@pytest.fixture
def expensive_fixture():
    print("Creating expensive fixture")
    return "Expensive Data"

@pytest.fixture
def another_fixture():
    print("Creating another fixture")
    return "Another Data"

@pytest.mark.parametrize("my_fixture", [
    pytest.lazy_fixture('expensive_fixture'),
    pytest.lazy_fixture('another_fixture')
])
def test_example(my_fixture):
    assert my_fixture in ["Expensive Data", "Another Data"]
```

在这个示例中，`test_example` 被参数化以使用两个不同的fixture。通过 `pytest.lazy_fixture`，这些`fixture`会在测试函数实际调用时才初始化，从而实现延迟加载，运行效果如下（由于此插件长期不更新，`pytest 8.0`及以上版本无法使用此插件）：

```shell
root@Gavin:~/pytest_plugin/test# pytest test_lazy_fixture_v1.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.4, pytest-sugar 1.0.0)
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, twisted-1.14.2, rerunfailures-14.0, lazy-fixture-0.6.3, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, picked-0.5.0, assume-2.4.3, anyio-4.3.0, asyncio-0.23.8, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1, sugar-1.0.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                        

 test_lazy_fixture_v1.py ✓✓                                                                                                                                                                                                100% ██████████
======================================================================================================= sum of all tests durations =======================================================================================================
0.05s

Results (0.08s):
       2 passed
root@Gavin:~/pytest_plugin/test#
```

再比如：假设我们有以下两个 `fixtures`：

```python
# content of conftest.py
import pytest

@pytest.fixture
def expensive_fixture():
    print("Setting up an expensive fixture")
    yield "data from expensive setup"
    print("Tearing down an expensive fixture")

@pytest.fixture(params=[1, 2])
def number_fixture(request):
    return request.param
```

现在，假设我们想要在单个测试函数中使用 `expensive_fixture`，但仅当 `number_fixture` 的状态为特定值时。

我们可以用 `pytest.mark.parametrize` 和 `pytest-lazy-fixture` 来实现：

```python
# content of test_lazy_fixture_v2.py
import pytest
from pytest_lazyfixture import lazy_fixture

@pytest.mark.parametrize("number,my_fixture", [
    (1, pytest.lazy_fixture('expensive_fixture')), 
    # expensive_fixture 只会在 number_fixture 为 1 时加载
    (2, None),
    # expensive_fixture 不会加载
])
def test_with_conditions(number, my_fixture):
    if number == 1:
        assert my_fixture == "data from expensive setup"
    else:
        assert my_fixture is None
```

在这个例子中，当 `number_fixture` 的值为 1 时，`expensive_fixture` 将被初始化，如果它的值为 2，`expensive_fixture` 则不会被创建，运行结果如下：

```shell
root@Gavin:~/pytest_plugin/test# pytest test_lazy_fixture_v2.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.4, pytest-sugar 1.0.0)
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, twisted-1.14.2, rerunfailures-14.0, lazy-fixture-0.6.3, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, picked-0.5.0, assume-2.4.3, anyio-4.3.0, asyncio-0.23.8, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1, sugar-1.0.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                        

 test_lazy_fixture_v2.py ✓✓                                                                                                                                                                                                100% ██████████
======================================================================================================= sum of all tests durations =======================================================================================================
0.02s

Results (0.05s):
       2 passed
root@Gavin:~/pytest_plugin/test#
```


## 注意事项

* **团队协作**：确定你的团队了解和同意使用 `pytest-lazy-fixture`，因为它增加了测试码的复杂性。
* **调试困难**：由于 `fixture` 的延迟加载，可能会使得问题的调试变得稍微复杂。
* **过度使用避免**：虽然延迟加载 `fixture` 很有用，但不应过度使用，以免影响代码的可读性和维护性。
* **注解加载条件**：确保理解如何和何时 `fixtures` 被初始化，避免在测试中引入隐藏的副作用，增加详细注解方便团队成员理解。

# 源码介绍

## 源码目录结构

从[官网](https://pypi.org/project/pytest-lazy-fixture)下载解压到本地：

```shell
root@Gavin:~/pytest_plugin/pytest-lazy-fixture-0.6.3# ll
total 48
drwxr-xr-x  4 gavin gavin 4096 Feb  2  2020 ./
drwxr-xr-x 22 root  root  4096 Jul 24 15:57 ../
-rw-r--r--  1 gavin gavin 1082 Sep 13  2018 LICENSE
-rw-r--r--  1 gavin gavin  125 Mar 17  2019 MANIFEST.in
-rw-r--r--  1 gavin gavin 3680 Feb  2  2020 PKG-INFO
drwxr-xr-x  2 gavin gavin 4096 Feb  2  2020 pytest_lazy_fixture.egg-info/
-rw-r--r--  1 gavin gavin 5732 Feb  2  2020 pytest_lazyfixture.py
-rw-r--r--  1 gavin gavin 1896 Sep 13  2018 README.rst
-rw-r--r--  1 gavin gavin   94 Feb  2  2020 setup.cfg
-rwxr-xr-x  1 gavin gavin 1639 Feb  2  2020 setup.py*
drwxr-xr-x  2 gavin gavin 4096 Feb  2  2020 tests/
root@Gavin:~/pytest_plugin/pytest-lazy-fixture-0.6.3# 
```

核心文件是`pytest_lazyfixture.py`。

也看的出来，代码已经好几年没有更新了。



## 源码解读

这段代码是 `pytest_lazy_fixtures` 插件的核心部分，它提供了延迟加载 `fixtures` 的功能。以下是对代码的中文注解和详细解释：

### 导入依赖
```python
import copy
import sys
import types
from collections import defaultdict
import pytest
```
- `copy`：用于复制对象。
- `sys`：用于检查 `Python` 版本。
- `types`：用于操作类型相关的操作。
- `defaultdict`：用于创建默认字典。
- `pytest`：导入 `pytest` 模块。

### 定义 PY3 和 string_type
```python
PY3 = sys.version_info[0] == 3
string_type = str if PY3 else basestring
```
- `PY3`：判断是否为 `Python 3`。
- `string_type`：根据 `Python` 版本选择字符串类型。

### Pytest 配置钩子
```python
def pytest_configure():
    pytest.lazy_fixture = lazy_fixture
```
- 在 `pytest` 配置阶段，将 `lazy_fixture` 函数注册为 `pytest` 的一个钩子。

### pytest 测试用例设置钩子
```python
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if hasattr(item, '_request'):
        item._request._fillfixtures = types.MethodType(
            fillfixtures(item._request._fillfixtures), item._request
        )
```
- 在每个测试用例的 `setup` 阶段，替换 `_request._fillfixtures` 方法，以便处理延迟加载的 `fixtures`。

### 填充 fixtures 方法
```python
def fillfixtures(_fillfixtures):
    def fill(request):
        item = request._pyfuncitem
        fixturenames = getattr(item, "fixturenames", None)
        if fixturenames is None:
            fixturenames = request.fixturenames

        if hasattr(item, 'callspec'):
            for param, val in sorted_by_dependency(item.callspec.params, fixturenames):
                if val is not None and is_lazy_fixture(val):
                    item.callspec.params[param] = request.getfixturevalue(val.name)
                elif param not in item.funcargs:
                    item.funcargs[param] = request.getfixturevalue(param)

        _fillfixtures()
    return fill
```
- 替换原始的 `_fillfixtures` 方法，用于填充延迟加载的 `fixtures`。

### Pytest fixture 设置钩子
```python
@pytest.hookimpl(tryfirst=True)
def pytest_fixture_setup(fixturedef, request):
    val = getattr(request, 'param', None)
    if is_lazy_fixture(val):
        request.param = request.getfixturevalue(val.name)
```
- 在 fixture 设置阶段，处理延迟加载的 `fixtures`。

### Pytest 测试用例调用钩子
```python
def pytest_runtest_call(item):
    if hasattr(item, 'funcargs'):
        for arg, val in item.funcargs.items():
            if is_lazy_fixture(val):
                item.funcargs[arg] = item._request.getfixturevalue(val.name)
```
- 在测试用例调用阶段，处理 `funcargs` 中的延迟加载 `fixtures`。

### pytest 收集测试项钩子
```python
@pytest.hookimpl(hookwrapper=True)
def pytest_pycollect_makeitem(collector, name, obj):
    global current_node
    current_node = collector
    yield
    current_node = None
```
- 在收集测试项时，设置当前节点。

### 参数化测试 ID 生成钩子
```python
def pytest_make_parametrize_id(config, val, argname):
    if is_lazy_fixture(val):
        return val.name
```
- 为参数化测试生成 ID，处理延迟加载 `fixtures` 的情况。

### pytest 生成测试用例钩子
```python
@pytest.hookimpl(hookwrapper=True)
def pytest_generate_tests(metafunc):
    yield

    normalize_metafunc_calls(metafunc, 'funcargs')
    normalize_metafunc_calls(metafunc, 'params')
```
- 在生成测试用例时，规范化 `metafunc`。

### 规范化 metafunc 调用
```python
def normalize_metafunc_calls(metafunc, valtype, used_keys=None):
    newcalls = []
    for callspec in metafunc._calls:
        calls = normalize_call(callspec, metafunc, valtype, used_keys)
        newcalls.extend(calls)
    metafunc._calls = newcalls
```
- 规范化 `metafunc` 中的调用规范，处理延迟加载 `fixtures`。

### 复制 metafunc
```python
def copy_metafunc(metafunc):
    copied = copy.copy(metafunc)
    copied.fixturenames = copy.copy(metafunc.fixturenames)
    copied._calls = []

    try:
        copied._ids = copy.copy(metafunc._ids)
    except AttributeError:
        # pytest>=5.3.0
        pass

    copied._arg2fixturedefs = copy.copy(metafunc._arg2fixturedefs)
    return copied
```
- 复制 `metafunc` 对象。

### 规范化调用规范
```python
def normalize_call(callspec, metafunc, valtype, used_keys):
    fm = metafunc.config.pluginmanager.get_plugin('funcmanage')

    used_keys = used_keys or set()
    valtype_keys = set(getattr(callspec, valtype).keys()) - used_keys

    for arg in valtype_keys:
        val = getattr(callspec, valtype)[arg]
        if is_lazy_fixture(val):
            try:
                _, fixturenames_closure, arg2fixturedefs = fm.getfixtureclosure([val.name], metafunc.definition.parent)
            except ValueError:
                # 3.6.0 <= pytest < 3.7.0; `FixtureManager.getfixtureclosure` returns 2 values
                fixturenames_closure, arg2fixturedefs = fm.getfixtureclosure([val.name], metafunc.definition.parent)
            except AttributeError:
                # pytest < 3.6.0; `Metafunc` has no `definition` attribute
                fixturenames_closure, arg2fixturedefs = fm.getfixtureclosure([val.name], current_node)

            extra_fixturenames = [fname for fname in fixturenames_closure
                                  if fname not in callspec.params and fname not in callspec.funcargs]

            newmetafunc = copy_metafunc(metafunc)
            newmetafunc.fixturenames = extra_fixturenames
            newmetafunc._arg2fixturedefs.update(arg2fixturedefs)
            newmetafunc._calls = [callspec]
            fm.pytest_generate_tests(newmetafunc)
            normalize_metafunc_calls(newmetafunc, valtype, used_keys | set([arg]))
            return newmetafunc._calls

        used_keys.add(arg)
    return [callspec]
```
- 处理单个调用规范，提取延迟加载的 `fixtures`。

### 根据依赖关系排序参数
```python
def sorted_by_dependency(params, fixturenames):
    free_fm = []
    non_free_fm = defaultdict(list)

    for key in _sorted_argnames(params, fixturenames):
        val = params.get(key)

        if key not in params or not is_lazy_fixture(val) or val.name not in params:
            free_fm.append(key)
        else:
            non_free_fm[val.name].append(key)

    non_free_fm_list = []
    for free_key in free_fm:
        non_free_fm_list.extend(
            _tree_to_list(non_free_fm, free_key)
        )

    return [(key, params.get(key)) for key in (free_fm + non_free_fm_list)]
```
- 根据依赖关系对参数进行排序。

### 获取排序后的参数名称
```python
def _sorted_argnames(params, fixturenames):
    argnames = set(params.keys())

    for name in fixturenames:
        if name in argnames:
            argnames.remove(name)
        yield name

    if argnames:
        for name in argnames:
            yield name
```
- 获取排序后的参数名称列表。

### 将树形结构转换为列表
```python
def _tree_to_list(trees, leave):
    lst = []
    for l in trees[leave]:
        lst.append(l)
        lst.extend(
            _tree_to_list(trees, l)
        )
    return lst
```
- 将树形结构转换为列表。

### 创建延迟加载的 fixture 包装器
```python
def lazy_fixture(names):
    if isinstance(names, string_type):
        return LazyFixture(names)
    else:
        return [LazyFixture(name) for name in names]
```
- 创建延迟加载的 `fixture` 包装器。

### 判断是否为延迟加载的 fixture
```python
def is_lazy_fixture(val):
    return isinstance(val, LazyFixture)
```
- 判断一个值是否是延迟加载的 `fixture`。

### LazyFixture 类
```python
class LazyFixture(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{} "{}">'.format(self.__class__.__name__, self.name)

    def __eq__(self, other):
        return self.name == other.name
```
- `LazyFixture` 类表示延迟加载的 `fixture`。
- 包含 `name` 属性和 `__repr__` 方法用于表示对象。
- `__eq__` 方法用于比较两个 `LazyFixture` 对象是否相等。



# 结语



`pytest-lazy-fixture` 是一个 `pytest` 插件，它提供了延迟加载 `fixtures` 的功能，使得 `fixtures` 只有在实际被测试用例使用时才会被初始化。这种机制可以减少不必要的初始化，提高测试的执行效率，特别是在 `fixtures` 准备阶段耗时较长或资源消耗较大的情况下非常有用。

以下是该插件的几个关键点：
- **延迟加载**：`fixtures` 仅在需要时才加载，减少初始化时间。
- **提高效率**：避免在所有测试用例中重复加载和初始化相同的 `fixtures`。
- **灵活性**：允许测试用例按需加载 `fixtures`，适应不同的测试场景。
- **易于使用**：通过简单的 `API` 为测试用例提供延迟加载 fixtures 的能力。

总的来说，`pytest-lazy-fixture` 插件为 `pytest` 用户提供了一种灵活且高效的方式来管理测试中的 `fixtures`，使得测试更加高效和易于维护。

