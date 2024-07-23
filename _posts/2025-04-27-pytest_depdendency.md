---
title: 测试用例依赖之pytest-dependency源码解读
date: 2025-04-27 22:00:00
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
summary: 试用例依赖之pytest-dependency源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述



`pytest-dependency` 是一个 `pytest` 插件，它允许你定义测试用例之间的依赖关系。这个插件特别适用于那些测试需要按特定顺序执行的情况，比如当一个测试用例的结果依赖于另一个测试用例是否成功完成时。

## 关键特性

1. **测试依赖关系**:
   - 允许你指定某些测试用例必须在其他测试用例之后执行。

2. **显式依赖声明**:
   - 通过装饰器或命令行参数显式声明测试之间的依赖关系。

3. **灵活的执行顺序**:
   - 根据定义的依赖关系，动态调整测试执行的顺序。

4. **错误处理**:
   - 如果依赖的测试用例失败，则依赖它的测试用例将被适当地处理（如跳过或标记为失败）。

5. **命令行接口**:
   - 提供命令行选项来控制依赖测试的行为。

## 使用方式

1. **安装**:
   - 通常可以通过 `pip` 安装：`pip install pytest-dependency`

2. **定义依赖关系**:
   - 使用 `pytest.mark.dependency` 装饰器来标记测试函数，定义它们的依赖关系。

3. **运行测试**:
   - 运行 `pytest` 时，插件会自动处理测试用例的执行顺序，确保依赖关系得到满足。

## 示例代码

```python
import pytest

@pytest.mark.dependency()
def test_a():
    print("Running test A")

@pytest.mark.dependency(depends=["test_a"])
def test_b():
    print("Running test B")

@pytest.mark.dependency(depends=["test_b"])
def test_c():
    print("Running test C")
```

在这个示例中：
- `test_a` 是一个基础测试，没有依赖。
- `test_b` 依赖于 `test_a`，只有在 `test_a` 执行后才能运行。
- `test_c` 依赖于 `test_b`。



执行效果参考：

```shell
root@Gavin:~/pytest_plugin/test# pytest -s -v test_pytest_dependency.py 
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'profiling': '1.7.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3', 'line-profiler': '0.2.1', 'sugar': '1.0.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1, sugar-1.0.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                        
Running test A

 test_pytest_dependency.py::test_a ✓                                                                                                                                                                                        33% ███▍      Running test B

 test_pytest_dependency.py::test_b ✓                                                                                                                                                                                        67% ██████▋   Running test C

 test_pytest_dependency.py::test_c ✓                                                                                                                                                                                       100% ██████████
======================================================================================================= sum of all tests durations =======================================================================================================
0.02s

Results (0.05s):
       3 passed
root@Gavin:~/pytest_plugin/test# 
```



## 命令行选项

- `--dependency`: 允许你指定一个文件，列出所有测试用例及其依赖关系。



## 使用场景

- **数据库测试**: 当测试需要在数据库中创建数据，并且后续测试依赖于这些数据时。
- **集成测试**: 在集成测试中，某些测试步骤可能依赖于之前步骤的结果。
- **资源清理**: 某些测试需要在执行前清理资源，或者在执行后进行资源恢复。



## 限制和注意事项

- 确保依赖关系清晰且正确定义，否则可能导致测试执行顺序混乱。
- 过于复杂的依赖关系可能使测试维护变得困难。

`pytest-dependency` 插件为需要控制测试执行顺序的场景提供了一种解决方案，使得测试用例可以根据实际的依赖关系进行组织和执行。



# 源码介绍



## 目录结构

从[官网](https://pypi.org/project/pytest-dependency/)下载源码后解压，目录结构如下：

```shell
root@Gavin:~/pytest_plugin/pytest-dependency-0.6.0# ll
total 64
drwxr-xr-x  5 gavin gavin  4096 Jan  1  2024 ./
drwxr-xr-x 19 root  root   4096 Jul 23 16:47 ../
-rw-r--r--  1 gavin gavin  5481 Jan  1  2024 CHANGES.rst
drwxr-xr-x  3 gavin gavin  4096 Jan  1  2024 doc/
-rw-r--r--  1 gavin gavin 11358 Dec 31  2023 LICENSE.txt
-rw-r--r--  1 gavin gavin   197 Jan  1  2024 MANIFEST.in
-rw-r--r--  1 gavin gavin    38 Jan  1  2024 _meta.py
-rw-r--r--  1 gavin gavin  3647 Jan  1  2024 PKG-INFO
-rw-r--r--  1 gavin gavin  1911 Jan  1  2024 README.rst
-rwxr-xr-x  1 gavin gavin  6075 Jan  1  2024 setup.py*
drwxr-xr-x  2 gavin gavin  4096 Jan  1  2024 src/
drwxr-xr-x  2 gavin gavin  4096 Jan  1  2024 tests/
root@Gavin:~/pytest_plugin/pytest-dependency-0.6.0# cd src
root@Gavin:~/pytest_plugin/pytest-dependency-0.6.0/src# ll
total 16
drwxr-xr-x 2 gavin gavin 4096 Jan  1  2024 ./
drwxr-xr-x 5 gavin gavin 4096 Jan  1  2024 ../
-rw-r--r-- 1 gavin gavin 6341 Jan  1  2024 pytest_dependency.py
root@Gavin:~/pytest_plugin/pytest-dependency-0.6.0/src# 
```



此插件的核心文件为`pytest_dependency.py`。



## 源码解读



### 类DependencyItemStatus



```python
class DependencyItemStatus(object):
    """Status of a test item in a dependency manager.
    """

    Phases = ('setup', 'call', 'teardown')

    def __init__(self):
        self.results = { w:None for w in self.Phases }

    def __str__(self):
        l = ["%s: %s" % (w, self.results[w]) for w in self.Phases]
        return "Status(%s)" % ", ".join(l)

    def addResult(self, rep):
        self.results[rep.when] = rep.outcome

    def isSuccess(self):
        return list(self.results.values()) == ['passed', 'passed', 'passed']
```



 `DependencyItemStatus` 类用于跟踪单个测试项在依赖管理中的执行状态的容器（跟踪每个测试项在不同阶段的执行状态，并据此决定是否可以执行依赖于这些测试项的其他测试，确保测试的执行顺序符合定义的依赖关系）。

1. **类定义**:
   - `class DependencyItemStatus(object)`: 定义了一个名为 `DependencyItemStatus` 的类，它继承自 Python 的基类 `object`。

2. **类属性**:
   - `Phases`: 一个元组，包含测试执行的三个阶段：`'setup'`（测试前的准备阶段）、`'call'`（测试调用阶段）、`'teardown'`（测试后的清理阶段）。

3. **构造函数**:
   - `__init__(self)`: 构造函数初始化一个字典 `self.results`，用于存储每个测试阶段的执行结果。初始时，每个阶段的结果都被设置为 `None`。

4. **字符串表示**:
   - `__str__(self)`: 定义了对象的字符串表示形式，方便打印和调试。它通过遍历 `self.results` 字典，将每个阶段及其结果格式化为字符串，并用逗号分隔。

5. **添加结果**:
   - `addResult(self, rep)`: 一个方法，接受一个 `rep` 参数（代表测试报告对象），并将报告中指定阶段的结果（`rep.outcome`）存储在 `self.results` 字典中。`rep.when` 属性指示了测试报告对应的阶段。

6. **检查是否成功**:
   - `isSuccess(self)`: 一个方法，检查所有测试阶段是否都成功执行。如果 `self.results` 字典中的所有值都是 `'passed'`，则返回 `True`，表示测试项成功通过了所有阶段。



### 类DependencyManager的getManager方法



获取或创建一个 `DependencyManager` 对象，该对象管理测试项的依赖关系。



```python
    @classmethod
    def getManager(cls, item, scope):
        """Get the DependencyManager object from the node at scope level.
        Create it, if not yet present.
        """
        node = item.getparent(cls.ScopeCls[scope])
        if not node:
            return None
        if not hasattr(node, 'dependencyManager'):
            node.dependencyManager = cls(scope)
        return node.dependencyManager
```



代码解读如下：

1. **类方法装饰器**:
   - `@classmethod` 表示这是一个类方法，它可以通过类而不是类的实例来调用。

2. **方法定义**:
   - `def getManager(cls, item, scope)`: 定义了一个名为 `getManager` 的类方法，接收三个参数：
     - `cls`: 类方法的第一个参数，表示类本身。
     - `item`: 表示当前的测试项（test item），通常是 `pytest` 的 `Item` 对象。
     - `scope`: 表示作用域级别，用于确定依赖管理器应该附加到哪个级别的测试节点。

3. **获取依赖管理器**:
   - `node = item.getparent(cls.ScopeCls[scope])`: 调用 `item.getparent` 方法获取父节点，`cls.ScopeCls[scope]` 确定要获取的父节点类型，这里 `ScopeCls` 可能是一个类属性，定义了不同作用域对应的节点类型。

4. **检查节点是否存在**:
   - `if not node:`: 如果没有找到父节点，则返回 `None`。

5. **检查依赖管理器是否已创建**:
   - `if not hasattr(node, 'dependencyManager'):`: 使用 `hasattr` 函数检查父节点是否已经有了 `dependencyManager` 属性。

6. **创建依赖管理器**:
   - `node.dependencyManager = cls(scope)`: 如果没有 `dependencyManager`，创建一个新的 `DependencyManager` 实例，并将其赋值给父节点的 `dependencyManager` 属性。

7. **返回依赖管理器**:
   - `return node.dependencyManager`: 返回父节点的 `dependencyManager` 属性，即 `DependencyManager` 对象。

#### 代码逻辑

- 这个方法的目的是确保在指定作用域级别（如模块、类、函数等）的测试项的父节点上有一个 `DependencyManager` 对象。
- 如果这个对象不存在，它会被创建并附加到父节点上。
- 这允许插件在不同的测试执行阶段跟踪和管理依赖关系。

#### 示例用法

假设你正在编写一个测试用例，并且需要确保某些测试在其他测试之前执行：

```python
import pytest

@pytest.mark.dependency()
def test_a():
    # 测试逻辑
    pass

@pytest.mark.dependency(depends=["test_a"])
def test_b():
    # 测试逻辑，依赖于 test_a 的成功执行
    pass

# 在测试运行时，pytest-dependency 插件会使用 DependencyManager 来管理 test_a 和 test_b 的执行顺序
```

在这个例子中，`test_b` 依赖于 `test_a`。`pytest-dependency` 插件会使用 `DependencyManager` 来确保 `test_a` 在 `test_b` 之前执行。如果 `test_a` 失败，`test_b` 将不会被执行。



### 类DependencyManager的addResult方法

个方法用于将测试结果添加到依赖管理器中，以便跟踪和管理测试项的依赖关系。

```python
    def addResult(self, item, name, rep):
        if not name:
            # Old versions of pytest used to add an extra "::()" to
            # the node ids of class methods to denote the class
            # instance.  This has been removed in pytest 4.0.0.
            nodeid = item.nodeid.replace("::()::", "::")
            if self.scope == 'session' or self.scope == 'package':
                name = nodeid
            elif self.scope == 'module':
                name = nodeid.split("::", 1)[1]
            elif self.scope == 'class':
                name = nodeid.split("::", 2)[2]
            else:
                raise RuntimeError("Internal error: invalid scope '%s'"
                                   % self.scope)
        status = self.results.setdefault(name, DependencyItemStatus())
        logger.debug("register %s %s %s in %s scope",
                     rep.when, name, rep.outcome, self.scope)
        status.addResult(rep)
```



- 这个方法的目的是确保测试结果被正确地记录和管理，以便依赖管理器可以根据这些结果来决定测试项是否可以执行。
- 它首先处理旧版本的 `pytest` 中可能出现的节点 `ID` 格式问题。
- 然后，根据作用域级别确定测试项的名称，并获取或创建对应的状态对象。
- 最后，将测试结果添加到状态对象中，并记录一条调试日志。

代码详细解读如下：

1. **方法定义**:
   - `def addResult(self, item, name, rep)`: 定义了一个名为 `addResult` 的方法，接收四个参数：
     - `self`: 类实例的引用。
     - `item`: 表示当前的测试项（`test item`），通常是 `pytest` 的 `Item` 对象。
     - `name`: 测试项的名称或标识符。
     - `rep`: 测试报告对象，包含测试执行的结果和状态。

2. **处理旧版本的 pytest**:
   - `if not name:`: 如果 `name` 参数为空，说明可能需要从 `item.nodeid` 构造名称。
   - `nodeid = item.nodeid.replace("::()::", "::")`: 替换旧版本的 pytest 中类方法的节点 ID 中的 `"::()::"` 为 `"::"`。

3. **确定作用域和名称**:
   - 根据 `self.scope` 的值（表示作用域级别），确定 `name` 的值：
     - `'session'` 或 `'package'`: 使用完整的 `nodeid` 作为名称。
     - `'module'`: 使用 `nodeid` 分割后第二部分作为名称。
     - `'class'`: 使用 `nodeid` 分割后第三部分作为名称。
   - 如果作用域不是以上任何一个，抛出 `RuntimeError`，表示内部错误。

4. **获取或创建状态对象**:
   - `status = self.results.setdefault(name, DependencyItemStatus())`: 使用 `name` 作为键，在 `self.results` 字典中获取对应的 `DependencyItemStatus` 对象。如果不存在，则创建一个新的 `DependencyItemStatus` 实例并设置到字典中。

5. **记录日志**:
   - `logger.debug(...)`: 使用日志记录器记录一条调试信息，说明正在注册测试结果。

6. **添加测试结果**:
   - `status.addResult(rep)`: 调用 `DependencyItemStatus` 对象的 `addResult` 方法，将测试报告对象 `rep` 的结果添加到状态对象中。



### 类DependencyManager的checkDepend方法

这个方法用于检查测试项是否满足其依赖条件。

- 这个方法的目的是确保测试项在执行前，其所依赖的其他测试项已经成功执行。
- 它通过检查 `self.results` 字典来确定依赖项的执行状态。
- 如果所有依赖项都成功执行，则当前测试项可以继续执行；否则，将跳过当前测试项，并记录相应的日志信息。

```python
    def checkDepend(self, depends, item):
        logger.debug("check dependencies of %s in %s scope ...",
                     item.name, self.scope)
        for i in depends:
            if i in self.results:
                if self.results[i].isSuccess():
                    logger.debug("... %s succeeded", i)
                    continue
                else:
                    logger.debug("... %s has not succeeded", i)
            else:
                logger.debug("... %s is unknown", i)
                if _ignore_unknown:
                    continue
            logger.info("skip %s because it depends on %s", item.name, i)
            pytest.skip("%s depends on %s" % (item.name, i))
```



代码详细解读如下：

1. **方法定义**:
   - `def checkDepend(self, depends, item)`: 定义了一个名为 `checkDepend` 的方法，接收三个参数：
     - `self`: 类实例的引用。
     - `depends`: 一个列表，包含当前测试项 `item` 依赖的测试名称。
     - `item`: 当前的测试项（`test item`），通常是 `pytest` 的 `Item` 对象。

2. **记录日志**:
   - `logger.debug(...)`: 使用日志记录器记录一条调试信息，说明正在检查测试项的依赖关系。

3. **遍历依赖项**:
   - `for i in depends`: 遍历 `depends` 列表中的每个依赖项名称。

4. **检查依赖项状态**:
   - `if i in self.results`: 检查依赖项名称是否在 `self.results` 字典中，即是否已有该测试项的执行结果。
   - `if self.results[i].isSuccess()`: 调用 `DependencyItemStatus` 对象的 `isSuccess` 方法，检查依赖项是否成功执行。

5. **处理依赖项成功的情况**:
   - `logger.debug("... %s succeeded", i)`: 如果依赖项成功执行，记录一条调试信息，并继续检查下一个依赖项。

6. **处理依赖项未成功的情况**:
   - `logger.debug("... %s has not succeeded", i)`: 如果依赖项未成功执行，记录一条调试信息。

7. **处理未知依赖项**:
   - `else:`: 如果依赖项名称不在 `self.results` 字典中，表示这是一个未知的依赖项。
   - `logger.debug("... %s is unknown", i)`: 记录一条调试信息，说明依赖项未知。
   - `if _ignore_unknown: continue`: 如果全局变量 `_ignore_unknown` 为 `True`，则跳过当前依赖项，继续检查下一个。

8. **记录依赖项不满足的日志**:
   - `logger.info("skip %s because it depends on %s", item.name, i)`: 记录一条信息日志，说明由于依赖项不满足，将跳过当前测试项。

9. **跳过测试项**:
   - `pytest.skip("%s depends on %s" % (item.name, i))`: 使用 `pytest` 的 `skip` 函数跳过当前测试项，原因为依赖项不满足。





### depends方法

此函数用于在 `pytest` 测试中动态地声明测试依赖关系。

```python
def depends(request, other, scope='module'):
    """Add dependency on other test.

    Call pytest.skip() unless a successful outcome of all of the tests in
    other has been registered previously.  This has the same effect as
    the `depends` keyword argument to the :func:`pytest.mark.dependency`
    marker.  In contrast to the marker, this function may be called at
    runtime during a test.

    :param request: the value of the `request` pytest fixture related
        to the current test.
    :param other: dependencies, a list of names of tests that this
        test depends on.  The names of the dependencies must be
        adapted to the scope.
    :type other: iterable of :class:`str`
    :param scope: the scope to search for the dependencies.  Must be
        either `'session'`, `'package'`, `'module'`, or `'class'`.
    :type scope: :class:`str`

    .. versionadded:: 0.2

    .. versionchanged:: 0.5.0
        the scope parameter has been added.
    """
    item = request.node
    manager = DependencyManager.getManager(item, scope=scope)
    manager.checkDepend(other, item)
```

#### 函数定义与参数
- `def depends(request, other, scope='module')`: 定义了 `depends` 函数，它接收三个参数：
  - `request`: 当前测试的 `request` fixture 的值，它提供了对当前测试项的访问。
  - `other`: 一个可迭代对象，包含当前测试依赖的测试名称列表。这些名称需要根据 `scope` 调整。
  - `scope`: 一个字符串，指定搜索依赖项的作用域。可以是 `'session'`、`'package'`、`'module'` 或 `'class'`。默认值为 `'module'`。

#### 函数功能
- 函数的作用是为当前测试项添加依赖关系。它会检查所有在 `other` 中列出的测试是否之前已经成功执行。如果没有，则调用 `pytest.skip()` 跳过当前测试。

#### 函数逻辑
1. **获取当前测试项**:
   - `item = request.node`: 从 `request` fixture 中获取当前测试项的节点。

2. **获取依赖管理器**:
   - `manager = DependencyManager.getManager(item, scope=scope)`: 调用 `DependencyManager` 类的 `getManager` 类方法获取或创建一个依赖管理器。这个管理器与指定作用域相关联。

3. **检查依赖关系**:
   - `manager.checkDepend(other, item)`: 使用依赖管理器的 `checkDepend` 方法检查 `other` 中列出的依赖项是否都已成功执行。如果所有依赖项都成功，则继续执行当前测试；否则，记录日志并跳过当前测试。

#### 版本历史
- `.. versionadded:: 0.2`: 表示 `depends` 函数从版本 0.2 开始引入。
- `.. versionchanged:: 0.5.0`: 表示在版本 0.5.0 中添加了 `scope` 参数。



### pytest_addoption和pytest_configure方法

这部分定义了如何将插件的配置选项添加到 `pytest` 中，并处理这些参数选项。

```python
def pytest_addoption(parser):
    parser.addini("automark_dependency", 
                  "Add the dependency marker to all tests automatically", 
                  type="bool", default=False)
    parser.addoption("--ignore-unknown-dependency", 
                     action="store_true", default=False, 
                     help="ignore dependencies whose outcome is not known")


def pytest_configure(config):
    global _automark, _ignore_unknown
    _automark = config.getini("automark_dependency")
    _ignore_unknown = config.getoption("--ignore-unknown-dependency")
    config.addinivalue_line("markers", 
                            "dependency(name=None, depends=[]): "
                            "mark a test to be used as a dependency for "
                            "other tests or to depend on other tests."
```

#### 代码解读

1. **添加配置选项**:
   - `def pytest_addoption(parser)`: 这是一个钩子函数，当 `pytest` 启动时会被调用，允许插件向 `pytest`添加额外的命令行选项和配置文件选项。

2. **自动标记依赖**:
   - `parser.addini("automark_dependency", "Add the dependency marker to all tests automatically", type="bool", default=False)`: 添加一个配置项 `automark_dependency`，这是一个布尔值，用于控制是否自动为所有测试添加依赖标记。默认值为 `False`。

3. **忽略未知依赖**:
   - `parser.addoption("--ignore-unknown-dependency", action="store_true", default=False, help="ignore dependencies whose outcome is not known")`: 添加一个命令行选项 `--ignore-unknown-dependency`，当启用时，会忽略那些结果未知的依赖项。这通过 `store_true` 动作设置为 `True`，并且有默认值 `False`。

4. **配置钩子**:
   - `def pytest_configure(config)`: 这是另一个钩子函数，在 `pytest`配置阶段被调用，允许插件进行进一步的配置。

5. **全局变量**:
   - `global _automark, _ignore_unknown`: 声明全局变量 `_automark` 和 `_ignore_unknown`，这些变量将被用于控制插件的行为。

6. **获取配置值**:
   - `_automark = config.getini("automark_dependency")`: 从 `pytest`配置中获取 `automark_dependency` 的值，并将其存储在全局变量 `_automark` 中。
   - `_ignore_unknown = config.getoption("--ignore-unknown-dependency")`: 获取命令行选项 `--ignore-unknown-dependency` 的值，并将其存储在全局变量 `_ignore_unknown` 中。

7. **添加标记说明**:
   - `config.addinivalue_line("markers", "dependency(name=None, depends=[]): mark a test to be used as a dependency for other tests or to depend on other tests.")`: 向 `pytest`的配置文件中添加关于 `dependency` 标记的说明。这个标记用于标记测试项作为其他测试的依赖项，或者声明当前测试依赖于其他测试项。

#### 功能说明

- **automark_dependency**: 如果设置为 `True`，则插件会自动为所有测试添加依赖标记，无需手动添加。
- **ignore_unknown_dependency**: 如果启用，插件会忽略那些结果未知的依赖项，不会因为未知依赖而跳过测试。

#### 示例用法

在命令行中，你可以这样使用这些选项：

```bash
pytest --ignore-unknown-dependency
pytest -o automark_dependency=true
```

这些选项允许用户在运行测试之前，通过命令行或配置文件来控制插件的行为，使得测试的依赖管理更加灵活和方便。



### pytest_runtest_makereport方法

使用 `pytest` 的钩子（`hook`）机制来处理测试结果，并将其存储在依赖管理器中。

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store the test outcome if this item is marked "dependency".
    """
    outcome = yield
    marker = item.get_closest_marker("dependency")
    if marker is not None or _automark:
        rep = outcome.get_result()
        name = marker.kwargs.get('name') if marker is not None else None
        for scope in DependencyManager.ScopeCls:
            manager = DependencyManager.getManager(item, scope=scope)
            if (manager):
                manager.addResult(item, name, rep)
```



#### 代码解读

1. **钩子装饰器**:
   - `@pytest.hookimpl(tryfirst=True, hookwrapper=True)`: 这个装饰器将函数注册为 Pytest 的钩子。`tryfirst=True` 表示该钩子会在其他钩子之前执行，`hookwrapper=True` 表示该钩子会包装其他钩子的执行。

2. **函数定义**:
   - `def pytest_runtest_makereport(item, call)`: 定义了名为 `pytest_runtest_makereport` 的钩子函数，它接收两个参数：
     - `item`: 当前测试项（`test item`）。
     - `call`: 一个封装了测试调用的 `pytest.CallInfo` 对象。

3. **生成器和产出**:
   - `outcome = yield`: 使用 `yield` 挂起函数执行，并将结果存储在 `outcome` 变量中。这是 `hookwrapper=True` 用法的一部分，允许你在其他钩子执行完成后获取结果。

4. **获取测试结果**:
   - `rep = outcome.get_result()`: 从 `outcome` 对象获取生成的测试结果。

5. **检查依赖标记**:
   - `marker = item.get_closest_marker("dependency")`: 获取当前测试项上最近的 `dependency` 标记。如果没有标记，则 `marker` 为 `None`。

6. **处理自动标记**:
   - `if marker is not None or _automark`: 检查是否存在 `dependency` 标记或者全局变量 `_automark` 是否为 `True`。如果是，则继续处理。

7. **获取标记名称**:
   - `name = marker.kwargs.get('name') if marker is not None else None`: 如果存在 `dependency` 标记，则获取其 `name` 参数的值；否则，将 `name` 设置为 `None`。

8. **获取作用域和依赖管理器**:
   - `for scope in DependencyManager.ScopeCls`: 遍历 `DependencyManager.ScopeCls`，这通常是一个包含不同作用域级别的类属性。
   - `manager = DependencyManager.getManager(item, scope=scope)`: 对于每个作用域级别，获取或创建依赖管理器。

9. **添加测试结果**:
   - `if (manager)`: 如果依赖管理器存在，则调用其 `addResult` 方法，传入当前测试项、名称和测试结果对象。

#### 代码逻辑

- 该钩子函数在每个测试项执行完毕后被调用，用于收集和存储测试结果。
- 它首先检查测试项是否有 `dependency` 标记或是否启用了自动标记功能。
- 然后，对于每个作用域级别，获取依赖管理器，并将其测试结果添加到管理器中。



### pytest_runtest_setup方法

定义了一个名为 `pytest_runtest_setup` 的钩子函数，该函数在每个测试项的设置阶段被调用，用于检查测试项的依赖关系。

```python
def pytest_runtest_setup(item):
    """Check dependencies if this item is marked "dependency".
    Skip if any of the dependencies has not been run successfully.
    """
    marker = item.get_closest_marker("dependency")
    if marker is not None:
        depends = marker.kwargs.get('depends')
        if depends:
            scope = marker.kwargs.get('scope', 'module')
            manager = DependencyManager.getManager(item, scope=scope)
            manager.checkDepend(depends, item)
```



#### 代码解读

1. **钩子函数定义**:
   - `def pytest_runtest_setup(item)`: 定义了一个钩子函数，它接收一个参数 `item`，表示当前的测试项（`test item`）。

2. **检查依赖标记**:
   - `marker = item.get_closest_marker("dependency")`: 获取当前测试项上最近的 `dependency` 标记。如果没有标记，则 `marker` 为 `None`。

3. **处理依赖关系**:
   - `if marker is not None`: 如果存在 `dependency` 标记，则进一步处理依赖关系。

4. **获取依赖项**:
   - `depends = marker.kwargs.get('depends')`: 从标记的关键字参数中获取 `depends` 参数，这是一个包含当前测试依赖的测试名称列表。

5. **检查依赖项是否为空**:
   - `if depends`: 如果 `depends` 列表不为空，即当前测试项有依赖项。

6. **获取作用域**:
   - `scope = marker.kwargs.get('scope', 'module')`: 从标记的关键字参数中获取 `scope` 参数，确定依赖项的作用域。如果没有指定，则默认为 `'module'`。

7. **获取依赖管理器**:
   - `manager = DependencyManager.getManager(item, scope=scope)`: 获取或创建一个依赖管理器，该管理器与指定作用域相关联。

8. **检查依赖项是否成功**:
   - `manager.checkDepend(depends, item)`: 使用依赖管理器的 `checkDepend` 方法检查 `depends` 列表中的每个依赖项是否都已成功执行。如果所有依赖项都成功，则继续执行当前测试；否则，跳过当前测试。

#### 代码逻辑

- 该钩子函数在每个测试项的设置阶段被调用，用于确保测试项的所有依赖项都已成功执行。
- 它首先检查测试项是否有 `dependency` 标记。
- 然后，获取依赖项和作用域，并获取相应的依赖管理器。
- 最后，调用依赖管理器的 `checkDepend` 方法来检查依赖项的状态。如果依赖项未成功，将跳过当前测试。




# 结语

`pytest-dependency` 是一个强大的 `pytest` 插件，它为测试用例提供了灵活的依赖管理功能：

1. **声明依赖**：允许测试用例显式地声明它们依赖于其他测试用例的执行结果。
2. **控制执行顺序**：确保测试用例按照正确的依赖关系顺序执行。
3. **动态标记**：支持在运行时动态地为测试用例添加依赖标记。
4. **自动重试失败的测试**：可以配置插件以自动重新执行失败的测试用例。
5. **跨会话缓存**：利用  `pytest`的缓存机制来维护测试执行的状态，实现跨测试运行的信息维护。
6. **灵活的配置选项**：通过命令行和配置文件选项，提供对插件行为的细粒度控制。

总的来说，`pytest-dependency` 插件使得自动化测试更加健壮和可靠，特别适合复杂的测试场景，其中测试用例之间存在明确的执行依赖。
