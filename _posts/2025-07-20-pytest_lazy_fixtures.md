---
title: 测试用例依赖之pytest-lazy-fixtures源码解读 
date: 2025-07-20 22:00:00
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
summary: 试用例依赖之pytest-lazy-fixtures源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-lazy-fixtures` 是一个 `pytest` 插件，它允许你以惰性（延迟）的方式使用 `fixtures`。这意味着 `fixtures` 将不会在测试开始时立即执行，而是在真正需要它们的时候才进行加载和执行。这种特性对于以下几种情况特别有用：

1. **减少资源消耗**：当 `fixtures` 的设置或拆除过程成本高昂时，延迟它们的执行可以节省资源。

2. **避免不必要的执行**：如果某些 `fixtures` 只在特定条件下需要，惰性加载可以避免在不需要时执行它们。

3. **提高测试速度**：通过延迟非必要的 `fixtures` 加载，可以减少测试套件的整体启动时间。

4. **复杂的测试依赖**：在测试依赖于多个复杂的 `fixtures` 时，可以更灵活地控制它们的加载顺序。

5. **参数化测试**：它支持与参数化测试结合使用，允许更复杂的测试场景定义。

使用 `pytest-lazy-fixtures` 插件，你可以定义一个 `fixture`，然后在测试函数中以惰性方式引用它。当测试运行到需要该 `fixture` 的时候，它才会被加载和执行。

安装 `pytest-lazy-fixtures` 插件非常简单，可以通过 `pip` 进行安装：

```ellh
pip install pytest-lazy-fixtures
```

使用插件后，你可以通过 `lazy_fixture` 函数来引用 `fixtures`，该函数接受一个或多个 `fixture` 名称作为参数，并返回一个或多个 `LazyFixture` 对象。在测试函数中使用这些对象，`pyteset` 会在适当的时候解析并加载相应的 `fixtures`。

例如：

```python
import pytest
from pytest_lazy_fixtures import lazy_fixture

@pytest.mark.usefixtures("db_fixture")
def test_example(lazy_fixture("db_session")):
    # 在这里，db_session fixture 将被延迟加载
    session = lazy_fixture("db_session")  # 获取实际的 fixture 实例
    # 使用 session 进行测试...
```

在这个例子中，`db_session fixture` 只有在 `test_example` 测试函数实际需要它时才会被加载。如果测试函数有多个参数，所有参数都将按需加载。这为测试提供了更高的灵活性和效率。

# 源码解读

## 源码目录结构

从[官网](https://pypi.org/project/pytest-lazy-fixtures)下载解压到本地：

```shell
root@Gavin:~/pytest_plugin/pytest_lazy_fixtures-1.1.1# ll
total 36
drwxr-xr-x  4 root root 4096 Jul 24 13:46 ./
drwxr-xr-x 21 root root 4096 Jul 24 13:46 ../
-rw-r--r--  1 root root 1069 Jul 23 05:39 LICENSE
-rw-r--r--  1 root root 4502 Jan  1  1970 PKG-INFO
-rw-r--r--  1 root root 1666 Jul 23 05:39 pyproject.toml
drwxr-xr-x  2 root root 4096 Jul 24 13:46 pytest_lazy_fixtures/
-rw-r--r--  1 root root 3683 Jul 23 05:39 README.md
drwxr-xr-x  2 root root 4096 Jul 24 13:46 tests/
root@Gavin:~/pytest_plugin/pytest_lazy_fixtures-1.1.1# cd pytest_lazy_fixtures/
root@Gavin:~/pytest_plugin/pytest_lazy_fixtures-1.1.1/pytest_lazy_fixtures# ll
total 32
drwxr-xr-x 2 root root 4096 Jul 24 13:46 ./
drwxr-xr-x 4 root root 4096 Jul 24 13:46 ../
-rw-r--r-- 1 root root   93 Jul 23 05:39 __init__.py
-rw-r--r-- 1 root root  966 Jul 23 05:39 lazy_fixture_callable.py
-rw-r--r-- 1 root root  839 Jul 23 05:39 lazy_fixture.py
-rw-r--r-- 1 root root  864 Jul 23 05:39 loader.py
-rw-r--r-- 1 root root 3322 Jul 23 05:39 normalizer.py
-rw-r--r-- 1 root root  600 Jul 23 05:39 plugin.py
-rw-r--r-- 1 root root    0 Jul 23 05:39 py.typed
root@Gavin:~/pytest_plugin/pytest_lazy_fixtures-1.1.1/pytest_lazy_fixtures# 
```


## lazy_fixture.py文件

```python
from dataclasses import dataclass
from operator import attrgetter
from typing import Optional

import pytest


@dataclass
class LazyFixtureWrapper:
    name: str

    @property
    def fixture_name(self) -> str:
        return self.name.split(".", maxsplit=1)[0]

    def _get_attr(self, fixture) -> Optional[str]:
        splitted = self.name.split(".", maxsplit=1)
        if len(splitted) == 1:
            return fixture
        return attrgetter(splitted[1])(fixture)

    def __repr__(self) -> str:
        return self.name

    def load_fixture(self, request: pytest.FixtureRequest):
        return self._get_attr(request.getfixturevalue(self.fixture_name))

    def __hash__(self) -> int:
        return hash(self.name)


def lf(name: str) -> LazyFixtureWrapper:
    """lf is a lazy fixture."""
    return LazyFixtureWrapper(name)
```

### 逻辑说明

- `LazyFixtureWrapper` 类封装了延迟加载 `fixture` 的逻辑，允许用户通过字符串名称引用 `fixture`，并在实际使用时才加载其值。
- `load_fixture` 方法是核心，它使用 `pytest` 的 `request` 对象来获取 `fixture` 的值，并根据需要获取其属性。
- `lf` 函数提供了一个简洁的接口，用于创建 `LazyFixtureWrapper` 实例。

详细介绍如下：

**导入依赖**:
   - 导入 Python 标准库中的 `dataclasses` 模块，用于创建数据类。
   - 导入 `operator` 模块中的 `attrgetter` 函数，用于获取对象的属性。
   - 导入 `typing` 模块中的 `Optional` 类型注解。
   - 导入 `pytest` 模块，用于与 `pytest` 框架集成。

**定义 LazyFixtureWrapper 数据类**:
   - 使用 `@dataclass` 装饰器定义了一个名为 `LazyFixtureWrapper` 的数据类，用于包装延迟加载的 `fixture`。
   - `name`: 一个字符串属性，存储 `fixture` 的名称或其路径（如果需要访问 `fixture` 的属性）。

**fixture_name 属性**:
   - 一个只读属性，返回 `name` 属性的第一部分（通过 `.` 分隔），这通常是 `fixture` 的基本名称。

. **_get_attr 方法**:
   - 一个私有方法，如果 `name` 只包含一个部分，直接返回 `fixture`；如果包含多个部分，使用 `attrgetter` 获取 `fixture` 对象的指定属性。

**`__repr__` 方法**:
   - 定义了类的字符串表示方法，返回 `name` 属性的值。

**load_fixture 方法**:
   - 一个公共方法，接受一个 `request` 参数（`pytest.FixtureRequest` 类型），调用 `request.getfixturevalue` 方法获取 `fixture` 的值，然后使用 `_get_attr` 方法获取最终的属性值。

**`__hash__` 方法**:
   - 定义了类的哈希方法，基于 `name` 属性的哈希值。

**lf 函数**:
   - 一个工厂函数，接受一个字符串参数 `name`，创建并返回一个新的 `LazyFixtureWrapper` 实例。

### 示例

假设有一个 `fixture db_session`，你可能想在测试中引用它，但只在实际需要时才加载它：

```python
def test_query(lf("db_session.my_attribute")):
    # 只有在这一行时，db_session 及其 my_attribute 才会被加载
    my_attribute = lf("db_session.my_attribute").load_fixture(request)
    # 使用 my_attribute 进行测试...
```

在这个例子中，`lf` 函数用于创建一个延迟加载的 `fixture` 引用，只有当 `load_fixture` 被调用时，`db_session` 和它的 `my_attribute` 属性才会被实际加载。这有助于减少不必要的资源消耗和初始化。


## lazy_fixture_callable.py文件

```python
from typing import Callable, Optional, Union

import pytest

from .lazy_fixture import LazyFixtureWrapper


class LazyFixtureCallableWrapper(LazyFixtureWrapper):
    _func: Optional[Callable]
    args: tuple
    kwargs: dict

    def __init__(self, func_or_name: Union[Callable, str], *args, **kwargs):
        if callable(func_or_name):
            self._func = func_or_name
            self.name = func_or_name.__name__
        else:
            self.name = func_or_name
            self._func = None
        self.args = args
        self.kwargs = kwargs

    def get_func(self, request: pytest.FixtureRequest) -> Callable:
        func = self._func
        if func is None:
            func = self.load_fixture(request)
            assert callable(func)
        return func


def lfc(name: Union[Callable, str], *args, **kwargs) -> LazyFixtureCallableWrapper:
    """lfc is a lazy fixture callable."""
    return LazyFixtureCallableWrapper(name, *args, **kwargs)
```


这段代码提供了一种方式来延迟调用 `fixtures` 或任意可调用对象，直到它们真正需要被使用时。

### 逻辑说明

- `LazyFixtureCallableWrapper` 类封装了延迟调用 `fixture` 或任意可调用对象的逻辑。
- 如果提供的名称是一个可调用对象，它将被直接存储；如果是一个字符串，则在需要时通过 `pytest` 的 `fixture` 系统加载。
- `get_func` 方法用于获取实际的函数对象，如果之前没有提供函数，则通过加载 `fixture` 获取。
- `lfc` 函数提供了一个简洁的接口，用于创建 `LazyFixtureCallableWrapper` 实例。

详细介绍如下：

**导入依赖**:
   - 导入 `Callable`, `Optional`, `Union` 等类型注解，用于注解函数和方法的参数和返回值。
   - 导入 `pytest` 模块，用于与 `pytest` 框架集成。
   - 从 `lazy_fixture` 模块导入 `LazyFixtureWrapper` 类。

**定义 LazyFixtureCallableWrapper 类**:
   - `LazyFixtureCallableWrapper` 类继承自 `LazyFixtureWrapper`。

**类属性**:
   - `_func`: 用于存储延迟调用的函数或 None。
   - `args`: 存储传递给延迟调用函数的位置参数。
   - `kwargs`: 存储传递给延迟调用函数的关键字参数。

**构造函数**:
   - 接受 `func_or_name` 参数，它可以是一个可调用对象或一个字符串名称。
   - 如果 `func_or_name` 是可调用的，将其存储在 `_func` 中，并使用 `__name__` 属性作为 `name`。
   - 如果 `func_or_name` 不是可调用的，假定它是一个 fixture 名称，存储在 `name` 中，并将 `_func` 设置为 None。
   - `args` 和 `kwargs` 分别存储构造函数的位置参数和关键字参数。

**get_func 方法**:
   - 接受一个 `request` 参数（`pytest.FixtureRequest` 类型）。
   - 如果 `_func` 是 None，则使用 `load_fixture` 方法加载 `fixture`，并断言加载的结果是可调用的。
   - 返回加载的函数或之前存储的 `_func`。

**lfc 函数**:
   - 一个工厂函数，接受 `name` 参数（可以是函数或字符串名称），以及任意数量的位置参数和关键字参数。
   - 创建并返回一个新的 `LazyFixtureCallableWrapper` 实例。


### 示例

假设有一个 `fixture db_session`，你可能想延迟调用它，直到实际需要执行数据库操作：

```python
def test_query(lfc(db_session)):
    # 只有在这一行时，db_session 才会被加载和调用
    db = lfc(db_session).get_func(request)
    result = db.execute("SELECT * FROM table")
    # 使用 result 进行测试...
```

在这个例子中，`lfc` 函数用于创建一个延迟调用的 `fixture` 引用，只有当 `get_func` 被调用时，`db_session` 才会被实际加载和调用。这有助于减少不必要的初始化和延迟执行。


## loader.py文件

```python
import pytest

from .lazy_fixture import LazyFixtureWrapper
from .lazy_fixture_callable import LazyFixtureCallableWrapper


def load_lazy_fixtures(value, request: pytest.FixtureRequest):
    if isinstance(value, LazyFixtureCallableWrapper):
        return value.get_func(request)(
            *load_lazy_fixtures(value.args, request),
            **load_lazy_fixtures(value.kwargs, request),
        )
    if isinstance(value, LazyFixtureWrapper):
        return value.load_fixture(request)
    # we need to check exact type
    if type(value) is dict:  # noqa: E721
        return {load_lazy_fixtures(key, request): load_lazy_fixtures(value, request) for key, value in value.items()}
    # we need to check exact type
    elif type(value) in {list, tuple, set}:
        return type(value)([load_lazy_fixtures(value, request) for value in value])
    return value
```

递归地加载延迟加载的 `fixtures`。


### 代码逻辑

- `load_lazy_fixtures` 函数负责处理延迟加载的 `fixtures`，包括 `LazyFixtureWrapper` 和 `LazyFixtureCallableWrapper` 实例。
- 它递归地加载 `value` 中的 `fixtures`，无论是作为位置参数、关键字参数，还是嵌套在字典、列表、元组或集合中。
- 函数使用类型检查（`isinstance`）来确定如何处理 `value`，对于 `dict`、`list`、`tuple` 和 `set`，它使用确切的类型检查（`type`），以避免错误地处理继承自这些类型的自定义类型。

详细信息描述如下：

**导入依赖**:
   - 导入 `pytest` 模块，用于与 `pytest` 框架集成。
   - 从 `lazy_fixture` 模块导入 `LazyFixtureWrapper` 类，用于包装延迟加载的 `fixture`。
   - 从 `lazy_fixture_callable` 模块导入 `LazyFixtureCallableWrapper` 类，用于包装延迟调用的 `fixture`。

**load_lazy_fixtures 函数**:
   - 函数接受两个参数：`value`，可能是延迟加载的 `fixture` 或其他值；`request`，`pytest` 的 `FixtureRequest` 对象，用于访问 `fixtures`。
   - 函数首先检查 `value` 是否是 `LazyFixtureCallableWrapper` 的实例。如果是，调用 `get_func` 方法获取实际的函数，并使用 `load_lazy_fixtures` 递归加载 `args` 和 `kwargs`，然后调用该函数。
   - 接下来，检查 `value` 是否是 `LazyFixtureWrapper` 的实例。如果是，调用 `load_fixture` 方法加载 `fixture`。
   - 然后，检查 `value` 是否是字典（`dict`）的确切类型。如果是，递归地加载字典的键和值。
   - 检查 `value` 是否是列表（`list`）、元组（`tuple`）或集合（`set`）的确切类型。如果是，递归地加载这些可迭代对象中的每个元素，并返回相应的类型。
   - 如果 `value` 不是上述任何一种类型，直接返回 `value`。

### 示例

假设你有一些延迟加载的 `fixtures` 和一个需要这些 `fixtures` 的测试函数：

```python
def test_example(lfc(db_session)):
    # 加载 fixtures 并执行测试逻辑
    session = load_lazy_fixtures(lfc(db_session), request)
    # 使用 session 进行测试...
```

在这个例子中，`lfc(db_session)` 创建了一个延迟加载的 `fixture` 引用。`load_lazy_fixtures` 函数用于在需要时加载这个 `fixture`，并可以处理更复杂的参数，如字典、列表等，确保所有延迟加载的 `fixtures` 都被正确加载。


## normalizer.py文件

```python
import copy
from typing import Any, Dict, List, Tuple

import pytest

from .lazy_fixture import LazyFixtureWrapper
from .lazy_fixture_callable import LazyFixtureCallableWrapper


def _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, value) -> Tuple[List[str], Dict[str, Any]]:
    if isinstance(value, LazyFixtureCallableWrapper):
        extra_fixturenames_args, arg2fixturedefs_args = _get_fixturenames_closure_and_arg2fixturedefs(
            fm,
            metafunc,
            value.args,
        )
        extra_fixturenames_kwargs, arg2fixturedefs_kwargs = _get_fixturenames_closure_and_arg2fixturedefs(
            fm,
            metafunc,
            value.kwargs,
        )
        return [*extra_fixturenames_args, *extra_fixturenames_kwargs], {
            **arg2fixturedefs_args,
            **arg2fixturedefs_kwargs,
        }
    if isinstance(value, LazyFixtureWrapper):
        if pytest.version_tuple >= (8, 0, 0):
            fixturenames_closure, arg2fixturedefs = fm.getfixtureclosure(metafunc.definition.parent, [value.name], {})
        else:  # pragma: no cover
            # TODO: add tox
            _, fixturenames_closure, arg2fixturedefs = fm.getfixtureclosure([value.name], metafunc.definition.parent)

        return fixturenames_closure, arg2fixturedefs
    extra_fixturenames, arg2fixturedefs = [], {}
    # we need to check exact type
    if type(value) is dict:  # noqa: E721
        value = list(value.values())
    # we need to check exact type
    if type(value) in {list, tuple, set}:
        for val in value:
            ef, arg2f = _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, val)
            extra_fixturenames.extend(ef)
            arg2fixturedefs.update(arg2f)
    return extra_fixturenames, arg2fixturedefs


def normalize_metafunc_calls(metafunc, used_keys=None):
    newcalls = []
    for callspec in metafunc._calls:
        calls = _normalize_call(callspec, metafunc, used_keys)
        newcalls.extend(calls)
    metafunc._calls = newcalls


def _copy_metafunc(metafunc):
    copied = copy.copy(metafunc)
    copied.fixturenames = copy.copy(metafunc.fixturenames)
    copied._calls = []
    copied._arg2fixturedefs = copy.copy(metafunc._arg2fixturedefs)
    return copied


def _normalize_call(callspec, metafunc, used_keys):
    fm = metafunc.config.pluginmanager.get_plugin("funcmanage")

    used_keys = used_keys or set()
    params = callspec.params.copy() if pytest.version_tuple >= (8, 0, 0) else {**callspec.params, **callspec.funcargs}
    valtype_keys = params.keys() - used_keys

    for arg in valtype_keys:
        value = params[arg]
        fixturenames_closure, arg2fixturedefs = _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, value)

        if fixturenames_closure and arg2fixturedefs:
            extra_fixturenames = [fname for fname in fixturenames_closure if fname not in params]

            newmetafunc = _copy_metafunc(metafunc)
            newmetafunc.fixturenames = extra_fixturenames
            newmetafunc._arg2fixturedefs.update(arg2fixturedefs)
            newmetafunc._calls = [callspec]
            fm.pytest_generate_tests(newmetafunc)
            normalize_metafunc_calls(newmetafunc, used_keys | {arg})
            return newmetafunc._calls

        used_keys.add(arg)
    return [callspec]
```

###  _get_fixturenames_closure_and_arg2fixturedefs方法

`_get_fixturenames_closure_and_arg2fixturedefs` 函数递归地处理输入值，以提取与 `pytest fixtures` 相关的信息。这个函数的目的是找出所有由延迟加载的 `fixtures` 引用所隐含的 `fixtures` 名称，并收集它们的详细信息。

代码逻辑：

- 函数首先检查 `value` 是否是 `LazyFixtureCallableWrapper` 或 `LazyFixtureWrapper` 的实例，并相应地递归处理。
- 对于 `LazyFixtureCallableWrapper`，处理附加的位置参数和关键字参数。
- 对于 `LazyFixtureWrapper`，调用 `fm.getfixtureclosure` 获取 `fixtures` 的名称闭包和详细信息。
- 对于字典、列表、元组或集合，递归地处理其中的每个元素，以提取所有相关的 `fixtures` 信息。
- 函数通过递归和类型检查，确保所有可能包含 `fixtures` 引用的地方都被检查并处理。

详细介绍如下：

1. **函数签名**:
   - `def _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, value)`: 定义了函数及其参数：
     - `fm`: `pytest` 的 `funcmanage` 插件实例，用于管理 `fixtures`。
     - `metafunc`: 代表当前测试函数的元数据的对象。
     - `value`: 可能是 `LazyFixtureWrapper` 或 `LazyFixtureCallableWrapper` 的实例，或者是要检查的值。

2. **返回类型注解**:
   - `-> Tuple[List[str], Dict[str, Any]]`: 函数返回一个元组，包含一个字符串列表（`fixtures` 名称的闭包）和一个字典（`fixtures` 的详细信息）。

3. **处理 LazyFixtureCallableWrapper**:
   - 如果 `value` 是 `LazyFixtureCallableWrapper` 的实例，递归地处理 `args` 和 `kwargs`，合并结果并返回。

4. **处理 LazyFixtureWrapper**:
   - 如果 `value` 是 `LazyFixtureWrapper` 的实例，根据 `pytest` 的版本使用不同的方法从 `fm` 获取 `fixtures` 的名称闭包和详细信息。

5. **版本兼容处理**:
   - 根据 `pytest` 的版本（8.0.0 及以上），使用不同的参数顺序调用 `fm.getfixtureclosure`。

6. **返回 fixtures 信息**:
   - 对于 `LazyFixtureWrapper`，返回获取的 `fixtures 名称闭包和详细信息。

7. **处理字典**:
   - 如果 `value` 是字典的确切类型，将值转换为列表并递归处理。

8. **处理列表、元组、集合**:
   - 如果 `value` 是列表、元组或集合的确切类型，遍历每个元素，递归调用 `_get_fixturenames_closure_and_arg2fixturedefs`，并更新结果。

9. **返回空结果**:
   - 如果 `value` 不是上述任何类型，返回空列表和空字典作为默认结果。


### _copy_metafunc方法

这个函数的作用是创建一个与传入的 `metafunc` 对象相似但某些属性被重新初始化或复制的新对象。这种复制操作在一些需要对对象进行修改但又不想影响原始对象的场景中可能会用到。

逐步解释：

1. `copied = copy.copy(metafunc)`：使用 `copy.copy` 函数创建了 `metafunc` 的浅复制，并将其存储在 `copied` 变量中。

2. `copied.fixturenames = copy.copy(metafunc.fixturenames)`：复制了 `metafunc` 对象的 `fixturenames` 属性。

3. `copied._calls = []`：将 `copied` 对象的 `_calls` 属性初始化为一个空列表。

4. `copied._arg2fixturedefs = copy.copy(metafunc._arg2fixturedefs)`：复制了 `metafunc` 对象的 `_arg2fixturedefs` 属性。

5. 最后，函数返回复制后的 `copied` 对象。


### _normalize_call方法

`_normalize_call` 函数用于处理 `pytest` 的调用规范（`callspec`）和元数据（`metafunc`）。

代码逻辑如下：

- 函数的主要目的是处理 `callspec` 中的参数，特别是那些可能是延迟加载 `fixtures` 的参数。
- 它通过 `_get_fixturenames_closure_and_arg2fixturedefs` 函数来提取 `fixtures` 信息，并根据这些信息创建新的测试用例。
- 如果参数值包含延迟加载的 `fixtures`，会创建 `metafunc` 的副本并更新其属性，然后生成新的测试。
- 函数递归地处理 `metafunc`，以确保所有相关的 `fixtures` 都被正确处理。

1. **函数定义**:
   - `def _normalize_call(callspec, metafunc, used_keys)`: 定义了函数，接受三个参数：`callspec`（调用规范），`metafunc`（元数据函数），`used_keys`（已使用的关键字参数集合）。

2. **获取 funcmanage 插件**:
   - `fm = metafunc.config.pluginmanager.get_plugin("funcmanage")`: 从 `pytest` 的插件管理器中获取 `funcmanage` 插件的实例。

3. **初始化 used_keys**:
   - `used_keys = used_keys or set()`: 如果 `used_keys` 未提供或为 `None`，则初始化为一个新的空集合。

4. **复制 params**:
   - `params = callspec.params.copy()`: 复制 `callspec` 中的 `params` 字典。对于 `pytest 8.0.0` 及以上版本，`params` 已经包含了所有参数；对于更低版本，还需要合并 `callspec.funcargs`。

5. **计算 valtype_keys**:
   - `valtype_keys = params.keys() - used_keys`: 找出 `params` 中尚未使用的关键字参数键。

6. **遍历 valtype_keys**:
   - 遍历 `valtype_keys` 中的每个参数名 `arg`。

7. **提取 fixtures 信息**:
   - `fixturenames_closure, arg2fixturedefs = _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, value)`: 对于每个参数值 `value`，调用 `_get_fixturenames_closure_and_arg2fixturedefs` 函数来获取 `fixtures` 名称闭包和详细信息。

8. **处理额外的 fixtures**:
   - 如果 `fixturenames_closure` 和 `arg2fixturedefs` 都不为空，表示找到了额外的 `fixtures`：
     - 从 `fixturenames_closure` 中筛选出尚未在 `params` 中的 `fixtures` 名称。
     - 创建 `metafunc` 的副本 `newmetafunc`。
     - 更新 `newmetafunc` 的 `fixturenames` 和 `_arg2fixturedefs`。
     - 设置 `newmetafunc._calls` 为当前的 `callspec`。
     - 调用 `fm.pytest_generate_tests(newmetafunc)` 来生成新的测试。
     - 递归调用 `normalize_metafunc_calls` 来进一步处理 `newmetafunc`。
     - 返回 `newmetafunc._calls`。

9. **更新 used_keys**:
   - `used_keys.add(arg)`: 将当前处理的参数名 `arg` 添加到 `used_keys` 集合中。

10. **返回 callspec**:
    - 如果没有额外的 `fixtures` 需要处理，或者在处理过程中没有找到新的 `fixtures`，返回原始的 `callspec` 列表。


### normalize_metafunc_calls方法

`normalize_metafunc_calls`函数用于处理 `pytest` 的元数据函数（`metafunc`）和调用规范（`callspec`）。

代码逻辑如下：

- 函数的目的是规范化 `metafunc` 中的调用规范，特别是处理延迟加载的 `fixtures`。
- 它通过 `_normalize_call` 函数来处理每个 `callspec`，这可能会生成新的调用规范，特别是当参数值包含延迟加载的 `fixtures` 时。
- 处理后的调用规范被收集到 `newcalls` 列表中，并最终替换 `metafunc` 的原始 `_calls` 列表。

详细解释如下：

1. **函数定义**:
   - `def normalize_metafunc_calls(metafunc, used_keys=None)`: 定义了函数，接受两个参数：
     - `metafunc`: 一个 `pytest` 测试函数的元数据对象，包含有关测试函数的信息，如参数和 `fixtures`。
     - `used_keys`: 一个可选参数，表示已经使用的关键字参数的集合。如果没有提供，它将被初始化为 `None`。

2. **初始化新调用列表**:
   - `newcalls = []`: 创建一个新的空列表 `newcalls`，用于存储处理后的调用规范。

3. **遍历原始调用规范**:
   - `for callspec in metafunc._calls`: 遍历 `metafunc` 中的 `_calls` 属性，这是一个包含所有调用规范的列表。

4. **处理每个调用规范**:
   - `calls = _normalize_call(callspec, metafunc, used_keys)`: 对每个 `callspec` 调用 `_normalize_call` 函数，传入当前的 `callspec`、`metafunc` 和 `used_keys`。这将处理延迟加载的 fixtures 并生成新的调用规范。

5. **扩展新调用列表**:
   - `newcalls.extend(calls)`: 将 `_normalize_call` 函数返回的新调用规范列表扩展到 `newcalls` 列表中。

6. **更新元数据函数的调用规范**:
   - `metafunc._calls = newcalls`: 用处理后的 `newcalls` 列表更新 `metafunc` 的 `_calls` 属性。


## normalizer.py文件

```python
import copy
from typing import Any, Dict, List, Tuple

import pytest

from .lazy_fixture import LazyFixtureWrapper
from .lazy_fixture_callable import LazyFixtureCallableWrapper


def _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, value) -> Tuple[List[str], Dict[str, Any]]:
    if isinstance(value, LazyFixtureCallableWrapper):
        extra_fixturenames_args, arg2fixturedefs_args = _get_fixturenames_closure_and_arg2fixturedefs(
            fm,
            metafunc,
            value.args,
        )
        extra_fixturenames_kwargs, arg2fixturedefs_kwargs = _get_fixturenames_closure_and_arg2fixturedefs(
            fm,
            metafunc,
            value.kwargs,
        )
        return [*extra_fixturenames_args, *extra_fixturenames_kwargs], {
            **arg2fixturedefs_args,
            **arg2fixturedefs_kwargs,
        }
    if isinstance(value, LazyFixtureWrapper):
        if pytest.version_tuple >= (8, 0, 0):
            fixturenames_closure, arg2fixturedefs = fm.getfixtureclosure(metafunc.definition.parent, [value.name], {})
        else:  # pragma: no cover
            # TODO: add tox
            _, fixturenames_closure, arg2fixturedefs = fm.getfixtureclosure([value.name], metafunc.definition.parent)

        return fixturenames_closure, arg2fixturedefs
    extra_fixturenames, arg2fixturedefs = [], {}
    # we need to check exact type
    if type(value) is dict:  # noqa: E721
        value = list(value.values())
    # we need to check exact type
    if type(value) in {list, tuple, set}:
        for val in value:
            ef, arg2f = _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, val)
            extra_fixturenames.extend(ef)
            arg2fixturedefs.update(arg2f)
    return extra_fixturenames, arg2fixturedefs


def normalize_metafunc_calls(metafunc, used_keys=None):
    newcalls = []
    for callspec in metafunc._calls:
        calls = _normalize_call(callspec, metafunc, used_keys)
        newcalls.extend(calls)
    metafunc._calls = newcalls


def _copy_metafunc(metafunc):
    copied = copy.copy(metafunc)
    copied.fixturenames = copy.copy(metafunc.fixturenames)
    copied._calls = []
    copied._arg2fixturedefs = copy.copy(metafunc._arg2fixturedefs)
    return copied


def _normalize_call(callspec, metafunc, used_keys):
    fm = metafunc.config.pluginmanager.get_plugin("funcmanage")

    used_keys = used_keys or set()
    params = callspec.params.copy() if pytest.version_tuple >= (8, 0, 0) else {**callspec.params, **callspec.funcargs}
    valtype_keys = params.keys() - used_keys

    for arg in valtype_keys:
        value = params[arg]
        fixturenames_closure, arg2fixturedefs = _get_fixturenames_closure_and_arg2fixturedefs(fm, metafunc, value)

        if fixturenames_closure and arg2fixturedefs:
            extra_fixturenames = [fname for fname in fixturenames_closure if fname not in params]

            newmetafunc = _copy_metafunc(metafunc)
            newmetafunc.fixturenames = extra_fixturenames
            newmetafunc._arg2fixturedefs.update(arg2fixturedefs)
            newmetafunc._calls = [callspec]
            fm.pytest_generate_tests(newmetafunc)
            normalize_metafunc_calls(newmetafunc, used_keys | {arg})
            return newmetafunc._calls

        used_keys.add(arg)
    return [callspec]
```

对代解析如下：

### 导入依赖

- `import copy`：导入 `Python` 标准库中的 `copy` 模块，用于复制对象。
- `from typing import Any, Dict, List, Tuple`：导入类型注解，用于函数返回类型和参数类型。
- `import pytest`：导入 `pytest` 模块，用于与 `pytest` 框架集成。
- `from .lazy_fixture import LazyFixtureWrapper` 和 `from .lazy_fixture_callable import LazyFixtureCallableWrapper`：从同一包中导入 `LazyFixtureWrapper` 和 `LazyFixtureCallableWrapper` 类。

### _get_fixturenames_closure_and_arg2fixturedefs 函数

- 功能：获取与延迟加载的 `fixture` 相关的 `fixtures` 名称闭包和 `fixtures` 定义。
- 参数：
  - `fm`：`pytest` 的 `funcmanage` 插件实例。
  - `metafunc`：代表当前测试函数的元数据对象。
  - `value`：可能是延迟加载的 `fixture` 或其他值。
- 返回值：一个元组，包含 `fixtures` 名称的列表和 `fixtures` 定义的字典。

### normalize_metafunc_calls 函数

- 功能：规范化 `metafunc` 中的调用规范，处理延迟加载的 `fixtures`。
- 参数：
  - `metafunc`：`pytest` 测试函数的元数据对象。
  - `used_keys`：一个可选参数，表示已经使用的关键字参数的集合。
- 逻辑：遍历 `metafunc._calls` 中的每个 `callspec`，调用 `_normalize_call` 函数处理，并更新 `metafunc._calls`。

### _copy_metafunc 函数

- 功能：复制 `metafunc` 对象，创建一个新的元数据对象。
- 参数：`metafunc`。
- 返回值：一个新的 `metafunc` 副本。

### _normalize_call 函数

- 功能：处理单个调用规范，提取延迟加载的 `fixtures` 并生成新的调用规范。
- 参数：
  - `callspec`：当前的调用规范。
  - `metafunc`：`pytest` 测试函数的元数据对象。
  - `used_keys`：表示已经使用的关键字参数的集合。
- 逻辑：
  - 获取 `funcmanage` 插件实例。
  - 复制 `params` 字典，并计算未使用的关键字参数键（`valtype_keys`）。
  - 遍历 `valtype_keys`，对于每个参数值 `value`，调用 `_get_fixturenames_closure_and_arg2fixturedefs` 函数获取 `fixtures` 名称闭包和定义。
  - 如果获取到额外的 `fixtures` 名称和定义，创建 `metafunc` 的副本，更新其 `fixturenames` 和 `_arg2fixturedefs`，生成新的调用规范并返回。
  - 如果没有额外的 `fixtures`，将当前的 `callspec` 添加到 `used_keys` 并返回。

### 代码逻辑总结

- 这段代码通过递归和类型检查，确保所有可能包含延迟加载 `fixtures` 的参数都被检查并处理。
- `_get_fixturenames_closure_and_arg2fixturedefs` 函数是核心，它负责提取 `fixtures` 信息。
- `normalize_metafunc_calls` 和 `_normalize_call` 函数处理调用规范，生成新的测试用例。
- `_copy_metafunc` 函数用于创建 `metafunc` 的副本，以便在生成新测试时保持原始 `metafunc` 不变。


## plugin.py文件

```python
import pytest

from .lazy_fixture import LazyFixtureWrapper
from .loader import load_lazy_fixtures
from .normalizer import normalize_metafunc_calls


@pytest.hookimpl(tryfirst=True)
def pytest_fixture_setup(fixturedef, request):
    val = getattr(request, "param", None)
    if val is not None:
        request.param = load_lazy_fixtures(val, request)


def pytest_make_parametrize_id(config, val, argname):
    if isinstance(val, LazyFixtureWrapper):
        return val.name


@pytest.hookimpl(hookwrapper=True)
def pytest_generate_tests(metafunc):
    yield

    normalize_metafunc_calls(metafunc)
```

代码详细解析：

### 导入依赖

- `import pytest`：导入 `pytest` 模块，用于与 `pytest` 框架集成。
- `from .lazy_fixture import LazyFixtureWrapper`：从同一包中导入 `LazyFixtureWrapper` 类，用于包装延迟加载的 `fixture`。
- `from .loader import load_lazy_fixtures`：从 `loader` 模块导入 `load_lazy_fixtures` 函数，用于加载延迟加载的 `fixtures`。
- `from .normalizer import normalize_metafunc_calls`：从 `normalizer` 模块导入 `normalize_metafunc_calls` 函数，用于规范化 `metafunc` 中的调用规范。

### pytest_fixture_setup 钩子函数

- `@pytest.hookimpl(tryfirst=True)`：装饰器，将函数注册为 `pytest` 的钩子，`tryfirst=True` 表示尽可能早地执行此钩子。
- 功能：在 fixture 设置阶段被调用，用于处理延迟加载的 `fixtures`。
- 参数：
  - `fixturedef`：`fixture` 的定义。
  - `request`：包含测试函数和 `fixture` 请求的上下文。
- 逻辑：
  - 获取 `request` 的 `param` 属性，如果存在，则使用 `load_lazy_fixtures` 函数加载延迟加载的 `fixtures`，并将结果重新赋值给 `request.param`。

### pytest_make_parametrize_id 钩子函数

- 功能：用于生成参数化测试的 ID。
- 参数：
  - `config`：`pytest` 的配置对象。
  - `val`：参数值。
  - `argname`：参数名称。
- 逻辑：
  - 如果 `val` 是 `LazyFixtureWrapper` 的实例，返回其名称 `name` 作为参数化测试的 `ID`。

### pytest_generate_tests 钩子函数

- `@pytest.hookimpl(hookwrapper=True)`：装饰器，将函数注册为 `pytest` 的钩子，`hookwrapper=True` 表示此钩子会包装其他钩子的执行。
- 功能：在生成测试用例时被调用，用于处理延迟加载的 `fixtures`。
- 参数：
  - `metafunc`：代表当前测试函数的元数据对象。
- 逻辑：
  - 使用 `yield` 挂起函数执行，等待其他钩子执行完毕后再继续。
  - 调用 `normalize_metafunc_calls` 函数处理 `metafunc`，确保所有延迟加载的 `fixtures` 被正确处理。

### 代码逻辑总结

- 这段代码通过 `pytest` 的钩子机制，实现了对延迟加载 `fixtures` 的支持。
- `pytest_fixture_setup` 钩子在 `fixture` 设置阶段加载延迟加载的 `fixtures`，并更新 `request.param`。
- `pytest_make_parametrize_id` 钩子为参数化测试生成 ID，特别处理 `LazyFixtureWrapper` 实例。
- `pytest_generate_tests` 钩子在生成测试用例时规范化 `metafunc`，确保所有延迟加载的 `fixtures` 被正确处理。

# 结语

`pytest_lazy_fixtures` 是一个 `pytest` 插件，它允许你以惰性方式加载 `fixtures`，即直到真正需要它们时才进行加载。这可以减少测试的初始化时间，并降低资源消耗，特别是在处理复杂的或耗时的 `fixture` 时非常有用。

1. **编写测试**：在你的测试模块中，使用 `lf` 或 `lfc` 函数来引用 `fixtures`，而不是直接使用 `pytest.fixture` 装饰器。

2. **使用 LazyFixtureWrapper**：`lf` 函数返回一个 `LazyFixtureWrapper` 对象，它包装了 `fixture` 的名称，并在运行时才加载它。

3. **使用 LazyFixtureCallableWrapper**：`lfc` 函数允许你延迟调用 `fixtures`，并且可以传递参数和关键字参数。

4. **运行测试**：使用 `pytest` 运行测试，插件会自动处理延迟加载的 `fixtures`。

5. **配置 pytest**：如果需要，你可以在 `conftest.py` 或测试模块中配置插件，例如设置默认的 `fixtures`。

通过使用 `pytest_lazy_fixtures` 插件，你可以使测试套件更加高效，特别是在处理多个或复杂的 `fixtures` 时。它提供了一种灵活的方式来组织和执行测试，同时保持了测试的清晰性和可维护性。
