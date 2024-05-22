---
title: 《pytest测试指南》-- 章节1-4 pytest测试用例标记
date: 2024-05-24 22:19:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 章节1-4 pytest测试用例标记
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 第4章 pytest测试用例标记

# 4.1 标记（markers）

`pytest`标记是`pytest`测试框架中的一个重要特性，它允许开发者在测试用例中添加元数据，以便在运行测试时进行过滤、排序或执行特定的操作。

在`pytest`中，标记是通过在测试函数或类上使用装饰器来实现的。装饰器以“@”符号开头，后面跟着标记名称和可选的参数。标记名称可以是任何有效的标识符，而参数则用于传递额外的信息。

标记可以用于多种目的，例如：

* 过滤测试：通过使用标记，可以只运行带有特定标记的测试用例。例如，可以使用`@pytest.mark.migration`标记来过滤出业务功能为"Migration"的测试用例。
* 排序测试：通过使用标记，可以按照特定的顺序运行测试用例。例如，可以使用`@pytest.mark.priority(1)`标记来将某个测试用例的优先级设置为最高（需安装`pytest-priority`插件）。
* 执行特定操作：通过使用标记，可以在运行测试时执行特定的操作。例如，可以使用`@pytest.mark.skipif(condition)`标记来跳过满足某个条件的测试用例。

在编写测试用例时，建议为每个测试用例添加适当的标记，以便更好地组织和管理测试用例。同时，也可以根据项目需求自定义标记，以满足特定的测试需求。

`pytest`标记可以分为两大类：

- **内置标记：** 这些标记是由`pytest`内置的，可以用于许多目的，例如跳过测试、标记测试为参数化测试，等等。

- **自定义标记：** 这些标记是由用户定义的，可以用于任何目的。

## 4.1.1 内置标记

`pytest`提供了许多内置标记，包括但不限制于：

- `@pytest.mark.skip`: 跳过测试
- `@pytest.mark.xfail`： 标记测试为已知失败
- `@pytest.mark.parametrize`: 把测试变为参数化
- `@pytest.mark.skipif`: 根据条件跳过测试

说明：

关于`pytest.mark.parametrize`，本书后续章节进行独立介绍。

## 4.1.2 自定义标记

除了内置标记，用户还可以创建自己的自定义标记。自定义标记必须以`@pytest.mark.`开头，后跟标记名。例如：

```python
import pytest

@pytest.mark.loopdevice
def test_create_NAS_disk():
    """  Create a NAS Disk  """
    pass
```

这个标记可以用来标记需要存在`loop device`设备情况下才能运行的测试，在执行时，使用标记过滤相应的测试用例：

```shell
pytest testcase/NAS/test_nas_disk.py -m "loopdevice"
```



# 4.2 标记的使用

标记可以通过以下方式使用：

- 将标记添加到测试用例或测试类中，**允许添加多个标记**。
- 使用`pytest`命令行选项过滤测试。
- 与插件交互。



## 4.2.1 -m 参数执行指定标记的用例

此部分内容，在“pytest参数详解” 章节中的 “general 相关参数”部分的"参数 -m"，有详细介绍，这里仅做示例演示。

测试用例集中有一些测试类被标记为 `migration` 的测试用例，测试代码片段如下：

```python
@pytest.mark.NAS
@pytest.mark.migration
class TestNASMigration(ShareFolderManager):
    """  Test case for: NAS Migration  """
    @classmethod
    def setup_class(cls):
        cls.nas_folder_src = 'pytest_nas_src'
        cls.nas_folder_migration = 'pytest_nas_migration'
        cls.nas_folder_mbcs = '中文目录'
        cls.nas_mount_point = 'pytest_nas_migration_mount'
        cls.nas_src_mount_point = 'pytest_migration_src_mount'
        cls.sub_folder_name = 'pytest_sub_folder'
```

可以使用 `-m` 参数来只收集/运行所有带有 `migration` 标记的测试用例，或反向过滤收集/执行不含有被标记为 `migration` 的测试用例。

**收集被标记为 `migration` 的测试用例：**

```shell
pytest --collect-only -m 'migration'
```

**收集未被标记为 `migration` 的测试用例：**

```shell
pytest --collect-only -m 'not migration'
```

说明：

去掉`--collect-only`就表示执行用例。



## 4.2.2 跳过（skip）测试

跳过测试用例是测试过程中的一个重要策略，可以帮助我们更有效率地管理测试工作。在`pytest`中跳过测试用例通常在以下情况之一出现时使用：

* **外部依赖不满足**	：当测试依赖于某个外部资源或服务，例如数据库、网络服务、磁盘资源等，而这些依赖暂时不可用或不满足条件时。
* **环境特定条件**：当测试用例仅适用于特定的操作系统、版本、配置或其他环境条件下，其他环境下不适用或意义不大时。
* **未实现的功能**：当测试面向尚未实现或处于开发中的功能时。
* **长时间运行的测试**：对于非常耗时的测试用例，可能在持续集成中或某些特定场合跳过，以加快测试回馈的速度。
* **已知的失败**：如果一个测试用例因为一个已知的bug而失败，这个bug暂时不会被修复，可能会跳过这个测试用例，避免影响整体测试结果。
* **测试数据不可用**：当测试数据或资源无法访问或者不适用时。
* **版本兼容性**：当测试用例针对特定版本的代码库或依赖库，其他版本应该跳过。
* **权限限制**：某些测试可能需要特定权限，例如管理员权限，但在当前测试环境中不易获得。
* **破坏性测试**：例如涉及到删除重要数据的测试，可能在生产环境或其他敏感环境中被跳过。
* **优先级管理**：基于开发和测试的优先级，可能临时跳过一些低优先级的测试。
* **功能冗余**：如果有功能上的重复测试，为了提高效率，可能会跳过一些重复或冗余的测试用例。
* **条件变化**：例如依赖于特定事件的测试，在不满足条件时跳过。
* **动态资源配额**：在资源有限的情况下，可能会根据当前资源使用情况决定跳过部分测试。
* **实验性特性**：对于尚处于实验阶段的功能，可能会选择性地跳过其对应的测试用例。
* **维护模式**：项目或服务处于维护模式时，可能临时跳过所有测试。
* 其他情况，等等等等。

对测试用例的跳过应该清晰记录理由，并且在合适的时机重新启用这些测试，以确保测试覆盖面不被长时间忽视。

`pytest`常用的跳过有：`@pytest.mark.skip`, `@pytest.mark.skipif`, `pytest.skip`，下面通过几种不同的实现方式对不同层次用例进行跳过操作。

### 4.2.2.1 @pytest.mark.skip

跳过执行某个用例最简洁的方式就是使用`@pytest.mark.skip`装饰器，并且可以设置reason可选参数表明跳过原因，使用装饰器的原因是在不修改测试用例函数代码的情况下就可以达到跳过的目的，其基本语法格式如下：

```python
import pytest

@pytest.mark.skip(reason="提供跳过测试的原因")
def test_function():
    # 此处的测试代码将会被跳过，不会执行
    ...
```

针对`@pytest.mark.skip`，接下来结合具体示例进行展示其功能。

#### 4.2.2.1.1 跳过测试函数

假如存在如下代码，用于跳过虚拟机环境下的用例执行，示例如下：

```python
root@Gavin:~/code/chapter1-4# cat test_mark_skip.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import pytest


def is_virtual_machine():
    """检查当前系统是否为虚拟机。
       通过检查 /sys/class/dmi/id/product_name 是否包含特定的虚拟机提供商名称来确定。
    """
    try:
        with open('/sys/class/dmi/id/product_name', 'r') as file:
            product_name = file.read().strip().lower()
    except FileNotFoundError:
        return False  # 文件不存在可能意味着无法确定，这里假定为非虚拟机

    # 根据需要添加更多的虚拟机提供商名称...
    vm_providers = ['vmware', 'virtualbox', 'qemu', 'xen', 'kvm']

    return any(vm_provider.lower() in product_name for vm_provider in vm_providers)


# 作用于函数级别的pytest.mark.skip
@pytest.mark.skip(reason="Can only run on physical devices, don't support VM")
def test_on_physical_device():
    assert is_virtual_machine, "[ERROR]  Not a physical machine."
```

将`@pytest.mark.skip`装饰器放在测试用例函数之上，表明仅跳过这个测试用例，执行结果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_mark_skip.py::test_on_physical_device
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-4
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_mark_skip.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)

=============================== 1 skipped in 0.00s =============================
root@Gavin:~/code/chapter1-4#
```



#### 4.2.2.1.2 跳过测试类

在上述文件`test_mark_skip.py`基础上，增加如下内容：

```python
# 作用于类级别的pytest.mark.skip
@pytest.mark.skip(reason="This feature is not supported yet")
class TestNewFeature:
    def test_sftp_settings(self):
        pass

    def test_sftp_upload(self):
        pass

    def test_sftp_download(self):
        pass
```

将`@pytest.mark.skip`装饰器放在测试类之上，使之跳过整个测试类，即此类下的所有测试用例均被跳过，执行结果：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_mark_skip.py::TestNewFeature
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-4
plugins: check-2.2.2, metadata-3.0.0
collected 3 items

test_mark_skip.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
test_mark_skip.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
test_mark_skip.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)

================================ 3 skipped in 0.00s ============================
root@Gavin:~/code/chapter1-4# 
```



### 4.2.2.2 @pytest.mark.skipif

带条件的测试跳过，满足条件就跳过，不满足条件就不跳过，基本语法格式如下：

```python
@pytest.mark.skipif(condition, reason="Optional reason for skipping the test")
def test_function_name():
    # Test code here
```

#### 4.2.2.2.1 跳过测试函数

```python
root@Gavin:~/code/chapter1-4# cat test_mark_skipif.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import pytest


def is_virtual_machine():
    """检查当前系统是否为虚拟机。
       通过检查 /sys/class/dmi/id/product_name 是否包含特定的虚拟机提供商名称来确定。
    """
    try:
        with open('/sys/class/dmi/id/product_name', 'r') as file:
            product_name = file.read().strip().lower()
    except FileNotFoundError:
        return False  # 文件不存在可能意味着无法确定，这里假定为非虚拟机

    # 根据需要添加更多的虚拟机提供商名称...
    vm_providers = ['vmware', 'virtualbox', 'qemu', 'xen', 'kvm']

    return any(vm_provider.lower() in product_name for vm_provider in vm_providers)


# 作用于函数级别的pytest.mark.skipif
@pytest.mark.skipif(is_virtual_machine, reason="Can only run on physical devices, don't support VM")
def test_on_physical_device():
    print("Run case in physical devices")
```

`@pytest.mark.skipif`装饰器作用于测试函数上，执行结果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_mark_skipif.py::test_on_physical_device
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 1 item

test_mark_skipif.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)

=============================== 1 skipped in 0.================================
root@Gavin:~/code/chapter1-4#
```



#### 4.2.2.2.2 跳过测试类

在文件`test_mark_skipif.py`基础之上，添加如下代码：

```python
# 作用于类级别的pytest.mark.skipif
@pytest.mark.skipif(is_virtual_machine, reason="This feature is not supported yet")
class TestNewFeature:
    def test_sftp_settings(self):
        pass

    def test_sftp_upload(self):
        pass

    def test_sftp_download(self):
        pass
```

`@pytest.mark.skipif`装饰器作用于测试类`TestNewFeature`之上，如果不满足条件则跳过整个测试类，执行效果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_mark_skipif.py::TestNewFeature
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 3 items

test_mark_skipif.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
test_mark_skipif.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
test_mark_skipif.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)

============================== 3 skipped in 0.01s =============================
root@Gavin:~/code/chapter1-4#
```

#### 4.2.2.2.3 模块之间共享@pytest.mark.skipif

在大型测试项目中，可以在一个文件中定义所有的执行条件，在需要时引入此模块，实现模块间共享约束条件的作用。

假如存在test_module这个文件夹，文件夹下存在两个测试用例文件：`test_module_skip_a`和`test_module_skip_b`，在测试用例文件`test_module_skip_a`中定义`minversion`，用于表明程序执行所需的python最低版本，示例代码如下：

```python
root@Gavin:~/code/chapter1-4/test_module# cat test_module_skip_a.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys
import pytest

minversion = pytest.mark.skipif(sys.version_info < (3, 13), reason="请使用python 3.13或更改高版本")

@minversion
def test_case_one():
    pass
root@Gavin:~/code/chapter1-4/test_module# cat test_module_skip_b.py 
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from test_module_skip_a import minversion


@minversion
def test_case_two():
    pass
root@Gavin:~/code/chapter1-4/test_module
```

在python版本为3.11.6环境下，执行test_module下的两个测试用例，效果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_module
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-4
collected 2 items

test_module/test_module_skip_a.py::test_case_one SKIPPED (请使用python 3.13或更改高版本)
test_module/test_module_skip_b.py::test_case_two SKIPPED (请使用python 3.13或更改高版本)

=============================== 2 skipped in 0.01s ============================
root@Gavin:~/code/chapter1-4#
```

从结果看出，minversion在两个测试文件中均生效了。




### 4.2.2.3 跳过标记

可以将 `pytest.mark.skip` 和 `pytest.mark.skipif` 赋值给一个标记变量，在不同模块之间共享这个标记变量，这样在有多个模块的测试用例需要用到相同的 `skip` 或 `skipif` ，可以用一个单独的文件去管理这些通用标记，然后适用于整个测试用例集。

示例：

```python
root@Gavin:~/code/chapter1-4# cat test_skipmark_skipifmark.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest


# 标记
skipmark = pytest.mark.skip(reason="不能在Linux上运行")
skipifmark = pytest.mark.skipif(sys.platform == 'linux', reason="不能在linux上运行")


@skipmark
class TestSkipMark(object):
    @skipifmark
    def test_skipifmark1(self):
        print("测试标记1")
  
    def test_skipifmark2(self):
        print("测试标记2")

    @skipmark
    def test_skipmark():
        print("测试标记3")
root@Gavin:~/code/chapter1-4#

```

执行结果：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_skipmark_skipifmark.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-4
collected 3 items

test_skipmark_skipifmark.py::TestSkipMark::test_skipifmark1 SKIPPED (不能在linux上运行)
test_skipmark_skipifmark.py::TestSkipMark::test_skipifmark2 SKIPPED (不能在Linux上运行)
test_skipmark_skipifmark.py::TestSkipMark::test_skipmark SKIPPED (不能在Linux上运行)

============================== 3 skipped in 0.01================================
root@Gavin:~/code/chapter1-4#
```



### 4.2.3.4 pytest.skip

如果想在测试执行期间（比如setup、teardown期间）强制执行跳过后续步骤，则可以考虑`pytest.skip()`方法，用于表明直接在测试用例里使用`pytest.skip`跳过测试后续步骤，其基本语法格式如下：

```python
pytest.skip(reason="reason for skipping the test")
```

作用：在测试用例执行期间强制跳过不再执行剩余内容。

类似：在Python的循环里面，满足某些条件则break 跳出循环。

示例：

```python
root@Gavin:~/code/chapter1-4# cat test_pytest_skip.py 
import os
import pytest


def test_function():
    n = 1
    while True:
        print(f"这是我第{n}条用例")
        n += 1
        if n == 5:
            pytest.skip("我跑五次了不跑了")


# 使用pytest.skip在测试中跳过
def test_something():
    if os.environ.get("SHELL") == "/bin/bash":
        pytest.skip("Shell是bash，跳过此测试")
    else:
        print("Do something")


def test_type():
    if isinstance([], list):
        pytest.skip(reason="不能是列表，跳过")
    else:
        pass
root@Gavin:~/code/chapter1-4#
```

执行效果：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_pytest_skip.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 2 item

test_pytest_skip.py::test_something SKIPPED (Shell是bash，跳过此测试)
test_pytest_skip.py::test_type SKIPPED (不能是列表，跳过)

============================== 2 skipped in 0.01s ============================
root@Gavin:~/code/chapter1-4#
```

另外，可以为其设置一个布尔型的参数`allow_module_level`（默认为False），表明是否允许在模块中调用这种方法。如果设置为True，则跳过模块中剩余的部分，即这个模块中所有测试方法被跳过。

其语法格式如下：

```python
pytest.skip(reason="", allow_module_level=False)
```

示例：

```python
root@Gavin:~/code/chapter1-4# cat test_pytest_skip_allow_module_level.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest


if sys.platform.startswith("linux"):
    pytest.skip("skipping linux-only tests", allow_module_level=True)


    @pytest.fixture(autouse=True)
    def login():
        print("This is login")


    def test_case01():
        print("I'm test case01")
root@Gavin:~/code/chapter1-4#
```

本机是Linux，其执行结果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_pytest_skip_allow_module_level.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-4
collected 0 items / 1 skipped

=============================== 1 skipped in 0.01s=============================
root@Gavin:~/code/chapter1-4#
```

如果是在Windows上执行，效果如下：

```shell
D:\>pytest -s -v D:\automation\book\code\chapter1-4\test_pytest_skip_allow_module_level.py
============================= test session starts =============================
platform win32 -- Python 2.7.13, pytest-4.6.11, py-1.11.0, pluggy-0.13.1 -- C:\Python27\python.exe
cachedir: .pytest_cache
rootdir: D:\
plugins: repeat-0.9.1, ordering-0.6, progress-1.2.1, allure-pytest-2.8.11
collected 0 items

======================== no tests ran in 0.02 seconds =========================

D:\
```

**请注意：**在测试用例中设置`allow_module_level`参数时，并不会生效，因为此参数是模块级专用参数。

给测试用例增加`allow_module_level=True`语句，由于这个是模块级专用的参数，所以放在某个测试方法中起不到把整个模块也就是文件都跳过的作用，示例如下：

```python
root@Gavin:~/code/chapter1-4# cat test_pytest_skip_allow_module_level_2.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest


@pytest.fixture(autouse=True)
def test_login():
    pytest.skip("skipping linux-only tests", allow_module_level=True)
    print("This is a login test")


def test_case01():
    print("I'm test case01")


def test_case02():
    print("I'm test case02")


def test_case03():
    assert 'linux' in sys.platform, "[ERROR] 本机非Linux系统"  # 当前测试环境是Linux
root@Gavin:~/code/chapter1-4#
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_pytest_skip_allow_module_level_2.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-4
collected 3 items

test_pytest_skip_allow_module_level_2.py::test_case01 SKIPPED (skipping linux-only tests)
test_pytest_skip_allow_module_level_2.py::test_case02 SKIPPED (skipping linux-only tests)
test_pytest_skip_allow_module_level_2.py::test_case03 SKIPPED (skipping linux-only tests)

=============================== 3 skipped in ===================================
root@Gavin:~/code/chapter1-4#
```

从执行结果可以看出，值跳过了对应的测试用例，而不是跳过这个用例下的所有用例，也就是说`allow_module_level=True`这个参数虽然影响范围是文件模块级，但放在具体测试用例函数下就不起作用了。



### 4.2.2.5 跳过测试模块

通过在模块顶部使用`pytestmark`对象，使用`pytest`设置跳过整个模块。考虑到一个模拟的场景，比如说我们只想在虚拟机上跳过测试，你可以这样编写代码：

首先，创建一个名为`conftest.py`的文件，这个文件会包含我们跳过测试所使用的通用函数（如果还没有的话）。

```python
# Content of conftest.py, 为了其他示例，故意命名为'conftest.py_for_module_to_skip'
# 请使用时，自行将'conftest.py_for_module_to_skip'更名为'conftest.py'
# 该函数用于判断当前环境是否为虚拟机，返回布尔值
def is_virtual_machine():
    try:
        with open('/sys/class/dmi/id/product_name', 'r') as file:
            product_name = file.read().strip().lower()
            # 使用更多虚拟机供应商的名称来判断
            return 'vmware' in product_name or 'virtualbox' in product_name
    except FileNotFoundError:
        # 如果文件不存在，我们假设它不是虚拟机
        return False

# 可以设置一个fixture供其他测试使用
def pytest_configure(config):
    config.addinivalue_line('markers', 'skip_in_vm: skip the test if in a virtual machine')
```

然后，在你想要跳过的测试模块文件顶部，设置`pytestmark`变量来跳过整个模块。

```python
# Content of chapter1-4/test_module_to_skip.py
import pytest
from conftest import is_virtual_machine

# 跳过整个模块如果我们在虚拟机上执行测试
pytestmark = pytest.mark.skipif(is_virtual_machine(), reason="跳过虚拟机上的测试")

def test_example_1():
    # 这个测试用例会在虚拟机上被跳过
    assert True

def test_example_2():
    # 这个测试用例同样会在虚拟机上被跳过
    assert True
```

执行效果：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_module_to_skip.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 2 items

test_module_to_skip.py::test_example_1 SKIPPED (跳过虚拟机上的测试)
test_module_to_skip.py::test_example_2 SKIPPED (跳过虚拟机上的测试)

============================== 2 skipped in 0.01s =============================
root@Gavin:~/code/chapter1-4#
```

在上述例子中，我们定义了一个`pytestmark`，它是`pytest.mark.skipif`的一个实例。这个标记将从`conftest.py`调用`is_virtual_machine`函数来检查当前环境是否为虚拟机。如果是的话，整个`test_module_to_skip.py`模块中的所有测试用例都将被跳过，并且在`pytest`的输出中，你将看到出于何种原因测试被跳过的信息。

这种方式可以确保在特定条件下（在这个例子中是运行在虚拟机上）整个模块的测试用例被统一地跳过，从而避免了在每个独立测试用例上重复设置跳过条件。



### 4.2.2.6 跳过指定目录或路径

在`pytest`中，跳过指定文件或目录的测试可以通过多种方法实现。虽然这段内容与`pytest skip`关联性不大，准确的讲，在`pytest`中称之为“忽略”（ignore），跳过（`skip`） 与 忽略（`ignore`）这在`pytest`中是两个完全不同的概念与用法，请务必注意。通过“忽略”（`ignore`），使用不同于`skip`的方式跳过指定目录或路径，实现测试用例的跳过，故而依然归类此内容到本章节中。

**请注意：**

熟悉`pytest`的用户可能知道，在早期版本使用`@pytest.mark.ignore` 、`pytest.ignore` 和 `collect_ignore` 来忽略测试用例，但自`pytest 6.0`版本起被废弃，因此在`pytest 6.0`及之后的版本中，推荐使用`@pytest.mark.skip()`来替代`@pytest.mark.ignore()`，因为在语义上，它们更为相近。而且，`pytest`建议尽可能地使用标准库提供的装饰器，而不是自定义的装饰器。

#### 4.2.2.6.1 使用命令行参数

最简单的方法是在运行`pytest`时使用命令行参数来指定要跳过的文件或目录。这不需要修改任何测试代码，只需要在运行测试时指定相应的参数。例如：

```bash
pytest -k "not name_of_test_file_to_skip"   # 跳过指定名称的文件
pytest --ignore=path/to/directory_to_skip/  # 跳过指定目录
```

其中 `-k` 参数允许你表达一个表达式来选择测试，而 `--ignore` 参数直接告诉`pytest`忽略某个文件或目录。

#### 4.2.2.6.2 在`conftest.py`中用代码跳过

如果你希望通过编辑代码来控制哪些测试被跳过，可以在项目的`conftest.py`文件中使用`pytest`的`hook`函数来实现。假设我们有一个目录结构如下：

```plaintext
code/
|-- chapter1-4/
    |-- test_module_to_skip.py
    |-- test_mark_skipif.py
    |-- test_mark_skip.py
    |-- test_to_skip.py
    |-- conftest.py
```

并希望跳过`test_module_to_skip.py` 和 `test_to_skip.py` 文件中的测试，可以在`conftest.py`中添加以下钩子函数：

```python
# Content of conftest.py
import pytest

# pytest_collection_modifyitems 钩子允许修改测试项的集合
def pytest_collection_modifyitems(config, items):
    # 你想要跳过的测试文件路径
    skip_files = ["test_module_to_skip.py", "test_to_skip.py"]
    for item in items.copy():
        # 判断当前的测试项是否应该被跳过
        if any(item.location[0].endswith(path) for path in skip_files):
            # 将该测试标记为跳过，并给出原因
            marker = pytest.mark.skip(reason="跳过指定的测试文件")
            item.add_marker(marker)
```

执行效果：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 13 items

test_mark_skip.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)
test_mark_skip.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
test_mark_skip.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
test_mark_skip.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)
test_mark_skipif.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)
test_mark_skipif.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
test_mark_skipif.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
test_mark_skipif.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)
test_module_to_skip.py::test_example_1 SKIPPED (跳过虚拟机上的测试)
test_module_to_skip.py::test_example_2 SKIPPED (跳过虚拟机上的测试)
test_to_skip.py::test_addition SKIPPED (跳过指定的测试文件)
test_to_skip.py::test_my_fixture SKIPPED (跳过指定的测试文件)
test_to_skip.py::test_sum SKIPPED (跳过指定的测试文件)

=============================== 13 skipped in 0.03s ============================
root@Gavin:~/code/chapter1-4#
```

通过这种方式，任何在`skip_files`列表中的测试文件都会被跳过。当`pytest`运行时，它会调用`pytest_collection_modifyitems`钩子并应用这些更改。

注意：`item.location[0]`给出的是测试项的文件路径，你可以根据需要自定义匹配路径的规则。

如果你要跳过一个目录下的所有测试文件，可以进行类似的操作，只需在循环中检查文件路径是否以你想要跳过的目录开始。如果是，就将那些测试项标记为跳过。

除此之外，还可以在`conftest.py`文件中使用`collect_ignore_glob`来定义要忽略的文件或目录。`pytest`的collect_ignore_glob是一个用于定制测试收集行为的特性，它允许你使用Unix shell样式的通配符来排除测试目录或模块，以忽略特定的测试文件或目录。当`pytest`进行测试收集时，它将检查每个目录和文件，如果它们与`collect_ignore_glob`中的通配符匹配，那么这些目录或文件将被忽略。

下面是一个示例代码，展示了如何使用`collect_ignore_glob`来排除特定的测试文件：


```python
# conftest.py
def pytest_configure(config):
    # 添加 collect_ignore_glob 配置选项
    config.addinivalue_line("pytest_plugins", "collect_ignore_glob")

# 在pytest_plugins/collect_ignore_glob.py文件中定义 collect_ignore_glob
collect_ignore_glob = ["tests/**/*.py"]
```
在上面的示例中，我们定义了一个`collect_ignore_glob`列表，其中包含了一个通配符模式`"tests/**/*.py"`。这意味着`pytest`将忽略`tests`目录下所有以`.py`结尾的文件。

**请注意：**`collect_ignore_glob`需要在`pytest_plugins`模块中定义，并且需要使用特殊的插件加载机制。在示例中，我们将`collect_ignore_glob`定义在一个名为`pytest_plugins/collect_ignore_glob.py`的文件中，并通过`pytest_plugins`插件加载机制来加载它。

使用上述配置后，当`pytest`运行测试时，它将忽略`tests`目录下所有以`.py`结尾的文件。你可以根据需要自定义`collect_ignore_glob`中的通配符模式，以排除特定的测试文件或目录。



### 4.2.2.7 pytest中几个被废弃的skip

**pytest.ignore**

从`pytest 4.4`版本开始，`pytest.ignore` 被废弃，先被`pytest.mark.ignore`代替，`pytest.mark.ignore`被废弃后被`pytest.mark.skip`。

**pytest.mark.ignore**

`pytest.mark.ignore` 在 `pytest 6.0`版本中已经被废弃。这个标记主要用于告诉 `pytest` 跳过一个特定的测试，被 `pytest.mark.skip` 代替。

**pytest collect_ignore**

 这个特性允许你指定哪些文件或目录在 `pytest` 执行测试收集时被忽略，`collect_ignore` 通常是一个列表，其中包含要忽略的文件或目录的路径,这些路径可以是相对路径或绝对路径。在`pytest 6.0`中被弃用，并在`pytest` 7.0中被完全移除。

**pytest.importorskip**

`pytest.importorskip` 是旧版 `pytest` 的一个内置函数，用于导入并返回请求的模块信息，如果导入的模块不存在，则跳过当前测试。从`pytest 5.0`版本开始，这个函数被标记为废弃，并在`pytest 6.0`版本中被移除。替代`pytest.importorskip`的方法是使用`pytest.mark.skipif`装饰器，这个装饰器允许你根据特定条件来跳过测试。



## 4.2.3 标记用例为预期失败

标记用例为预期失败，通常用于以下场景：

* 预期失败的测试用例：有时候，我们可能会编写一些明知会失败的测试用例，以便在后续的版本中验证是否已经修复了问题。在这种情况下，我们可以使用 `pytest.mark.xfail` 来标记这些测试用例。

* 尚未开发完成的功能：当我们在自动化脚本开发过程中遇到尚未开发完成的功能时，我们可以使用 `pytest.mark.xfail` 来标记这个测试用例。这样，虽然这个用例会失败，但是测试报告中会显示 `XFAIL` 状态，而不是显示错误追踪。


### 4.2.3.1 使用@pytest.mark.xfail标记用例
`@pytest.mark.xfail`是一个装饰器，可以用来标记一个测试用例，表示期望这个用例执行失败。当使用这个装饰器标记一个用例时，该用例会正常执行，只是在失败时不再显示堆栈信息。最终的结果有两个：用例执行失败时，结果标记为`XFAIL`（符合预期的失败）；用例执行成功时，结果标记为`XPASS`（不符合预期的成功），这可能是一个好消息，因为它意味着问题可能已经被解决了。

下面是如何使用`pytest.mark.xfail`的示例：

```python
import pytest

@pytest.mark.xfail(reason="这个功能还未实现")
def test_some_feature_not_implemented():
    # 这个测试用例预期会失败，因为功能尚未实现
    assert not implemented_feature()

@pytest.mark.xfail
def test_should_fail_due_to_known_bug():
    # 这个测试预期会失败，因为有一个已知的bug
    assert broken_functionality()
```

在运行测试时，`pytest`会识别出这些标记并适当地处理它们。如果你的测试与预期一样失败了，`pytest`会报告`xfail`（预期的失败），但是不会让整个测试会话失败。如果测试意外地通过了，则会报告为`xpass`（预期失败但通过了）。

你也可以为特定条件添加`xfail`，比如仅在特定的操作系统上标记为预期失败：

```python
import sys

@pytest.mark.xfail(sys.platform == "win32", reason="在Windows上有一个已知的bug")
def test_fail_on_windows():
    # Windows特定请况下预期失败的测试用例
    assert windows_specific_functionality()
```

在这个例子中，测试只有在Windows平台上运行时才标记为预期失败。

要在`pytest`的命令行选项中包括这些标记的原因，你可以运行：

```shell
pytest -rx
```

选项`-r`可以与不同的字符一起使用来指定要显示的测试结果类型。在这个例子中`x`代表显示预期失败的测试结果。如果你想看到这些测试的详细原因，你可以使用：

```shell
pytest -rxX
```

这里`X`代表显示预期失败的测试但通过了的原因。



### 4.2.3.2 使用pytest.xfail()标记用例

通过使用`pytest.xfail()`方法标记用例在执行过程中直接将结果标记为`XFAIL`，并跳过后续部分，即该用例中的后续代码不会被执行。常应用于如下场景：

* 功能未开发完毕
* 用例对应业务有Bug
* 用例的执行需要前置条件或操作（前置条件或操作失败，后续动作无需执行）

`pytest.xfail()`语法格式如下：

```python
pytest.xfail(reason="XFAIL reason")
```

`reason)`是一个可选参数，表明失败原因，建议携带上，方便回溯。

代码示例：

```python
root@Gavin:~/code/chapter1-4# cat test_pytest_xfail.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


class TestPytestXfail():
    def test_no_dev(self):
        pytest.xfail(reason="This Feature is not ready")
        print('This is test case1')
        assert 2 == 1

    def test_assert_in(self):
        print("This is test case2")
        assert 'a' in 'apple'

    def test_eq(self):
        print("This is test case3")
        assert 1 == 1

    def test_with_xfail(self):
        with pytest.xfail(reason="Use 'pytest.xfail' by with to mark case xfail"):
            assert 1 + 1 == 3
root@Gavin:~/code/chapter1-4#
```

上述测试用例，有两个测试用例使用了`pytest.xfail`，一个直接标记，一个使用上下文，2个`PASSED`，两个`XFAIL`执行效果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -s -v test_pytest_xfail.py 
============================== test session starts=============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-4
collected 4 items

test_pytest_xfail.py::TestPytestXfail::test_no_dev XFAIL (This Feature is not ready)
test_pytest_xfail.py::TestPytestXfail::test_assert_in This is test case2
PASSED
test_pytest_xfail.py::TestPytestXfail::test_eq This is test case3
PASSED
test_pytest_xfail.py::TestPytestXfail::test_with_xfail XFAIL (Use 'pytest.xfail' by with to mark case xfail)

=========================== 2 passed, 2 xfailed in 0.0 ========================
root@Gavin:~/code/chapter1-4#
```



虽然`pytest.xfail` 和 `with pytest.xfail` 用于标记预期失败的测试，但它们的使用方式和适用场景有所不同。

**直接使用 `pytest.xfail`**：

这种方式通常在测试函数内部使用。当你在测试过程中遇到某个条件，认为剩余的测试步骤应该被标记为预期失败时，可以调用 `pytest.xfail("reason")`。一旦调用 `pytest.xfail`，当前测试会立即标记为预期失败（xfail），不会继续执行后续代码。

示例：

```python
def test_function():
    if some_condition:
        pytest.xfail("known issue with some condition")
    # 更多测试代码...
```

**使用 `with pytest.xfail`**：

这种方式是使用上下文管理器，在特定的代码块内部使用。当你想要仅对测试中的特定部分标记为预期失败时，可以使用这种方式。在 `with` 块内的代码被执行，如果在这个块内发生异常，整个测试会被标记为预期失败；如果 `with` 块中的代码成功执行（没有异常），测试会被标记为预期失败但通过（xfail but passed）。

示例：
```python
def test_function():
    with pytest.xfail("known issue in part of the test"):
        # 只有这部分代码块内的测试是预期失败的
        # 这里的代码...
    # 这部分代码依然会正常执行和检验
```

使用哪种方法取决于你的具体测试场景和你想要的测试行为。直接使用 `pytest.xfail` 适合于测试一开始就知道会失败的情况，而 `with pytest.xfail` 更适合于只有测试的一部分可能会失败的场景。

### 4.2.3.3 pytest.param参数化标记用例为失败

`pytest.param`方法可用于为`pytest.mark.parameterize`或者参数化的·fixture·指定一个具体的实参，通过关键字参数marks接收一个或一组标记，用于标记这轮测试的用例。

关于`pytest.mark.parameterize`与`fixture`，将在后续章节中一一详细介绍。

在以下的示例中，我们将编写一个使用 `@pytest.mark.parametrize` 装饰器的测试用例，该用例会运行三个不同的测试参数，使用 `pytest.param` 来分别为每个参数指定一个特殊的标记(`xfail`, `skip`, `skipif`)。这样可以在参数化的测试用例中区分不同情况下的预期结果和行为。

```python
root@Gavin:~/code/chapter1-4# cat test_xfail_param.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys
import pytest

# 假设我们正在测试一个简单的加法函数
def add(a, b):
    return a + b

# 使用parametrize装饰器确保每个测试用例都会运行
@pytest.mark.parametrize("input_a, input_b, expected", [
   
    # 一个预期会失败的用例
    pytest.param(1, 1, 3, marks=pytest.mark.xfail(reason="This is a known bug with integers.")),
    
    # 一个将被直接跳过的用例
    pytest.param(2, 2, 4, marks=pytest.mark.skip(reason="Skipping this test for now.")),
    
    # 一个将被条件性跳过的用例（此处假设False为我们的条件）
    pytest.param(3, 3, 6, marks=pytest.mark.skipif(False, reason="This test will only be skipped if the condition is True."))
])
def test_add(input_a, input_b, expected):
    assert add(input_a, input_b) == expected, f"Expected {input_a} + {input_b} to equal {expected}"
```

每个 `pytest.param` 在这里用于定义一组参数以及应用于这组参数的特定标记 (`xfail`, `skip`, `skipif`)：

- `pytest.mark.xfail`: 预期测试会失败。
- `pytest.mark.skip`: 无条件跳过测试。
- `pytest.mark.skipif`: 基于某个条件结果跳过测试。在示例中条件被设置为 `False`，因此测试不会被跳过。如果需要根据条件跳过测试，请替换为具体的条件，如 `sys.platform == "linux"`。

上述用例执行效果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -rA -s -v test_xfail_param.py 
=============================== test session sta===============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-4
collected 3 items

test_xfail_param.py::test_add[1-1-3] XFAIL (This is a known bug with integers.)
test_xfail_param.py::test_add[2-2-4] SKIPPED (Skipping this test for now.)
test_xfail_param.py::test_add[3-3-6] PASSED
================================ PASSE=========================================
================================ short test summary info ======================
PASSED test_xfail_param.py::test_add[3-3-6]
SKIPPED [1] test_xfail_param.py:12: Skipping this test for now.
XFAIL test_xfail_param.py::test_add[1-1-3] - This is a known bug with integers.
==================== 1 passed, 1 skipped, 1 xfailed in 0.02s ==================
root@Gavin:~/code/chapter1-4#
```

### 4.2.3.4 `xfail`标记失效

通过`pytest`的命令行参数`--runxfail`参数执行用例让`xfail`标记（`@pytest.mark.xfail`和`pytest.xfail`标记）失效，是这些用例像正常用例一样被执行。

执行上文中测试用例`test_xfail_param.py`，效果如下：

```shell
root@Gavin:~/code/chapter1-4# pytest -rA -s -v --runxfail test_xfail_param.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-4
collected 3 items

test_xfail_param.py::test_add[1-1-3] FAILED
test_xfail_param.py::test_add[2-2-4] SKIPPED (Skipping this test for now.)
test_xfail_param.py::test_add[3-3-6] PASSED

================================= FAILURES ====================================
_________________________________ test_add[1-1-3] _____________________________

input_a = 1, input_b = 1, expected = 3

    @pytest.mark.parametrize("input_a, input_b, expected", [
    
        # 一个预期会失败的用例
        pytest.param(1, 1, 3, marks=pytest.mark.xfail(reason="This is a known bug with integers.")),
    
        # 一个将被直接跳过的用例
        pytest.param(2, 2, 4, marks=pytest.mark.skip(reason="Skipping this test for now.")),
    
        # 一个将被条件性跳过的用例（此处假设False为我们的条件）
        pytest.param(3, 3, 6, marks=pytest.mark.skipif(False, reason="This test will only be skipped if the condition is True."))
    ])
    def test_add(input_a, input_b, expected):
>       assert add(input_a, input_b) == expected, f"Expected {input_a} + {input_b} to equal {expected}"
E       AssertionError: Expected 1 + 1 to equal 3
E       assert 2 == 3
E        +  where 2 = add(1, 1)

test_xfail_param.py:24: AssertionError
=================================== PASSES ==================================
=================================== short test summary info =================
PASSED test_xfail_param.py::test_add[3-3-6]
SKIPPED [1] test_xfail_param.py:12: Skipping this test for now.
FAILED test_xfail_param.py::test_add[1-1-3] - AssertionError: Expected 1 + 1 to equal 3
================= 1 failed, 1 passed, 1 skipped in 0.06s ====================
root@Gavin:~/code/chapter1-4#
```

从执行结果可以看出，用例被正常执行，忽略了`xfail`标记。



### 4.2.3.5 各种不同失败执行方式的差异

在下表中，将展示使用`pytest`时，各种不同失败执行方式的差异：

| 特性               | 描述                                 | 使用场景                                                   | 命令行参数或装饰器                           |
| ------------------ | ------------------------------------ | ---------------------------------------------------------- | -------------------------------------------- |
| 立即停止测试       | 遇到第一个错误时停止                 | 快速定位第一个问题                                         | `-x` 或 `--exitfirst`                        |
| 重试失败的用例     | 失败的测试用例自动重试指定次数       | 适用于偶发性失败的用例或不稳定的环境                       | `--reruns`，需要`pytest-rerunfailures`插件   |
| 仅运行失败的用例   | 只重新运行上次测试中失败的测试用例   | 修复失败的测试用例后，仅重新检查这些用例                   | `--lf` 或 `--last-failed`                    |
| 优先运行失败的用例 | 先运行上次失败的测试，然后运行其他的 | 当有较多的测试用例需要运行，希望快点得到上次失败用例的结果 | `--ff` 或 `--failed-first`                   |
| 预期失败的用例     | 标记为预期失败的测试                 | 当你已经知道测试会失败，临时忽略该失败                     | `@pytest.mark.xfail`                         |
| 跳过测试           | 明确跳过某个测试                     | 对于特定条件下无需执行或尚未实现的测试                     | `@pytest.mark.skip` 或 `@pytest.mark.skipif` |
| 自定义失败输出     | 添加自定义信息到测试用例失败的输出   | 用于提供更多的上下文信息，如日志、截图等                   | `pytest_exception_interact` 钩子             |

这个表格为你使用`pytest`管理测试用例时提供一个概览，并帮助你选择对应的策略来处理不同的失败情况。



# 4.3 其他标记

其他标记需要安装三方插件，如用例超时限制`pytest-timeout`，`finction-timeout`，用例重复次数`pytest-repeat`等，将在`pytest`插件章节中进行讲述。



# 4.4 测试实践

## 4.4.1 不想被 pytest 执行的文件

与CI工具结合，因`pipline`有规定的文件名称，而这些文件能`pytest`执行时搜索到，因此需要忽略这些文件。

## 4.4.2 问题的解法

### 4.4.2.1 方案一：利用`--ignore` 来排除

#### 4.4.2.1.1 命令行方式

可以指定 file 或是 folder

```shell
pytest --ignore test_nothing.py
pytest --ignore test_nothing/
```

#### 4.4.2.1.2 pytest.ini文件

利用`adopts` 将命令行相关参数加入`pytest.ini`文件。

使用 `--ignore`，参考如下：

```shell
[pytest]
addopts = --ignore=test_nothing.py
```

使用`--ignore-glob`来匹配Unix shell-style的文件，参考如下：

```shell
--ignore-glob='*_01.py'
```

就可以排除像是 `test_01.py` , `pytest_01.py` 任何以 `01.py` 结尾的文件。

### 4.4.2.2 方案二：conftest.py过滤

这里介绍`conftest.py`中利用`collect_ignore_glob`方法，忽略目录或文件。在代码根目录下，创建conftest.py并添加如下内容（如果文件存在则追加内容）：

```python
# Content of conftest.py
collect_ignore_glob = ["*test_pytest_*.py"]
```

这样，在收集用例阶段，自动忽略文件名称含有`test_pytest_`的`py`文件，执行效果如下：

```shell
root@Gavin:~/code# pytest -s -v chapter1-4/
============================ test session starts ==============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 21 items

chapter1-4/test_import_or_skip.py::test_import_pexpect import pexpect test
PASSED
chapter1-4/test_mark_skip.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)
chapter1-4/test_mark_skip.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skip.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skip.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)
chapter1-4/test_mark_skipif.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::test_environ_variable PASSED
chapter1-4/test_mark_skipif.py::test_pytest_version SKIPPED (Test requires Python 3.12 or higher)
chapter1-4/test_module_to_skip.py::test_example_1 SKIPPED (跳过虚拟机上的测试)
chapter1-4/test_module_to_skip.py::test_example_2 SKIPPED (跳过虚拟机上的测试)
chapter1-4/test_skipmark_skipifmark.py::TestSkipMark::test_skipifmark1 SKIPPED (不能在linux上运行)
chapter1-4/test_skipmark_skipifmark.py::TestSkipMark::test_skipifmark2 SKIPPED (不能在Linux上运行)
chapter1-4/test_skipmark_skipifmark.py::TestSkipMark::test_skipmark SKIPPED (不能在Linux上运行)
chapter1-4/test_to_skip.py::test_addition SKIPPED (跳过指定的测试文件)
chapter1-4/test_to_skip.py::test_my_fixture SKIPPED (跳过指定的测试文件)
chapter1-4/test_to_skip.py::test_sum SKIPPED (跳过指定的测试文件)
chapter1-4/test_module/test_module_skip_a.py::test_case_one SKIPPED (请使用python 3.13或更改高版本)
chapter1-4/test_module/test_module_skip_b.py::test_case_two SKIPPED (请使用python 3.13或更改高版本)

============================= 2 passed, 19 skipped in 0.03s ===================
root@Gavin:~/code# 
```

如果`conftest.py`文件中删除了`collect_ignore_glob`设置，执行效果如下：

```shell
root@Gavin:~/code# pytest -s -v chapter1-4/
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 32 items / 1 skipped

chapter1-4/test_import_or_skip.py::test_import_pexpect import pexpect test
PASSED
chapter1-4/test_mark_skip.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)
chapter1-4/test_mark_skip.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skip.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skip.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::test_on_physical_device SKIPPED (Can only run on physical devices, don't support VM)
chapter1-4/test_mark_skipif.py::TestNewFeature::test_sftp_settings SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::TestNewFeature::test_sftp_upload SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::TestNewFeature::test_sftp_download SKIPPED (This feature is not supported yet)
chapter1-4/test_mark_skipif.py::test_environ_variable PASSED
chapter1-4/test_mark_skipif.py::test_pytest_version SKIPPED (Test requires Python 3.12 or higher)
chapter1-4/test_module_to_skip.py::test_example_1 SKIPPED (跳过虚拟机上的测试)
chapter1-4/test_module_to_skip.py::test_example_2 SKIPPED (跳过虚拟机上的测试)
chapter1-4/test_pytest_mark_xfail.py::test_some_feature_not_implemented XPASS (这个功能还未实现)
chapter1-4/test_pytest_mark_xfail.py::test_should_fail_due_to_known_bug XFAIL
chapter1-4/test_pytest_mark_xfail.py::test_fail_on_linux An error occurred while running grep: Command '['grep', '-n', 'FollowSymLinks', '/etc/apache2/apache2.conf']' returned non-zero exit status 2.
XFAIL (在Linux上有一个已知的bug)
chapter1-4/test_pytest_skip.py::test_something SKIPPED (Shell是bash，跳过此测试)
chapter1-4/test_pytest_skip.py::test_type SKIPPED (不能是列表，跳过)
chapter1-4/test_pytest_skip_allow_module_level_2.py::test_case01 SKIPPED (skipping linux-only tests)
chapter1-4/test_pytest_skip_allow_module_level_2.py::test_case02 SKIPPED (skipping linux-only tests)
chapter1-4/test_pytest_skip_allow_module_level_2.py::test_case03 SKIPPED (skipping linux-only tests)
chapter1-4/test_pytest_xfail.py::test_os_type XPASS
chapter1-4/test_pytest_xfail.py::test_mount_point PASSED
chapter1-4/test_pytest_xfail.py::test_example XFAIL (这是一个预期失败的测试用例)
chapter1-4/test_skipmark_skipifmark.py::TestSkipMark::test_skipifmark1 SKIPPED (不能在linux上运行)
chapter1-4/test_skipmark_skipifmark.py::TestSkipMark::test_skipifmark2 SKIPPED (不能在Linux上运行)
chapter1-4/test_skipmark_skipifmark.py::TestSkipMark::test_skipmark SKIPPED (不能在Linux上运行)
chapter1-4/test_to_skip.py::test_addition SKIPPED (跳过指定的测试文件)
chapter1-4/test_to_skip.py::test_my_fixture SKIPPED (跳过指定的测试文件)
chapter1-4/test_to_skip.py::test_sum SKIPPED (跳过指定的测试文件)
chapter1-4/test_module/test_module_skip_a.py::test_case_one SKIPPED (请使用python 3.13或更改高版本)
chapter1-4/test_module/test_module_skip_b.py::test_case_two SKIPPED (请使用python 3.13或更改高版本)

============= 3 passed, 25 skipped, 3 xfailed, 2 xpassed in 0.04s =============
root@Gavin:~/code#
```

可以看出，所有用例都被执行，包括设置之前被跳过的含`test_pytest_`的`py`文件。



# 4.5 信息汇总

## 4.5.1 标记使用对比信息汇总

| 标记类型                   | 描述                  | 内置/自定义 |
| -------------------------- | --------------------- | ----------- |
| `@pytest.mark.skip`        | 跳过测试              | 内置        |
| `@pytest.mark.xfail`       | 标记测试为已知失败    | 内置        |
| `@pytest.mark.parametrize` | 把测试变为参数化      | 内置        |
| `@pytest.mark.skipif`      | 根据条件跳过测试      | 内置        |
| `@pytest.mark.mark_name`   | 自定义`mark_name`标记 | 自定义      |



## 4.5.2 `pytest` 中跳过和忽略测试用例的区别

### 4.5.2.1 跳过测试用例

跳过测试用例是指在测试执行期间有条件或无条件地跳过一个或多个测试。跳过的测试用例仍然会被收集，并在测试报告中标记为已跳过，并给出跳过原因。

### 4.5.2.2 忽略测试用例

忽略测试用例是指在测试收集阶段就完全不收集某些测试用例，因此它们不会出现在测试报告中。

### 4.5.2.3 `pytest` 中跳过和忽略测试用例的方法

| 方法                  | 描述                                                        | 什么时候使用                                       |
| --------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| `@pytest.mark.skip`   | 无条件地跳过装饰的测试函数。                                | 当测试不可用、正在开发中或出于其他原因需要跳过时。 |
| `pytest.skip()`       | 在测试代码中动态地调用以跳过测试。                          | 当在运行时检测到需要跳过测试的条件时。             |
| `@pytest.mark.skipif` | 有条件地跳过装饰的测试函数。                                | 当测试收集时，如果给定的条件为真，则跳过测试。     |
| `--ignore`或`-k`      | 提供命令行参数指定忽略某个/些文件或目录                     | 当测试收集时，直接跳过被忽略的文件/目录。          |
| `config.py`           | 定义夹具（fixture）和钩子函数（hook functions）忽略相关用例 | 当fixture被使用时，或hook函数触发时。              |

#### 4.5.2.3.1 比较

- **跳过**：
  - 测试会被收集。
  - 测试会被标记为已跳过。
  - 跳过的原因将会被报告。
  - 在命令行使用 `-k`或 `--keyword` 时，跳过的测试不会被执行。

- **忽略**：
  - 测试不会被收集。
  - 测试不会出现在测试报告中。
  - 测试的忽略原因不会被报告。
  - 在命令行使用 `-k`或 `--keyword` 时，忽略的测试仍然会被考虑，因为它们根本没有被执行。

#### 4.5.2.3.2 小结

跳过和忽略是跳过测试的两种不同方式：

- **跳过**：有条件或无条件地跳过测试，但测试仍然会被收集并标记为已跳过。
- **忽略**：在测试收集阶段就完全忽略测试，因此测试不会出现在测试报告中。



# 4.6 各种跳过的用法和差异对比

下表比较了各种跳过的用法和差异：

| 特性                     | `@pytest.mark.skip`                                          | `pytest.skip`                                                | `@pytest.mark.skipif`                                        | `config.py`                                                  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 使用位置                 | 作为装饰器，放在测试函数或类上                               | 测试函数体内部，通常是某个条件语句的一部分                   | 作为装饰器，放在测试函数或类上，但带有额外的条件判断         | /                                                            |
| 用例                     | @pytest.mark.skip()                                          | @pytest.mark.skipif()                                        | pytest.skip(reason="xxx")                                    | /                                                            |
| 类                       | @pytest.mark.skip()                                          | @pytest.mark.skipif()                                        | /                                                            |                                                              |
| 模块                     | pytestmark = pytest.mark.skip()                              | pytestmark = pytest.mark.skipif()                            | pytest.skip(allow_module_level=True)                         | /                                                            |
| 文件按或目录             | /                                                            | /                                                            | /                                                            | hook函数实现                                                 |
| 调用时机                 | 在测试收集(phases of test collection)阶段就确定是否跳过测试  | 测试执行时(runtime)在函数体内部确定是否跳过当前执行的测试    | 在测试收集阶段就根据条件确定是否跳过测试                     | 在测试收集阶段就根据条件确定是否跳过测试                     |
| 接收参数                 | 可选的 `reason` 参数，用来说明跳过测试的原因                 | `reason` 参数，用来提供跳过测试的原因。`allow_module_level` 参数可用于指示是否允许在模块层面跳过测试 | 一个布尔表达式和可选的 `reason` 参数，布尔表达式为 `True` 时跳过测试 | /                                                            |
| 是否提供跳过的理由       | 是，通过 `reason` 参数                                       | 是，通过 `reason` 参数                                       | 是，通过 `reason` 参数                                       | /                                                            |
| 是否根据条件跳过         | 否                                                           | 否                                                           | 是，通过传递给装饰器的测试表达式                             | 是，任何定义在 `conftest.py` 中的夹具（fixture）和钩子函数（hook functions） |
| 是否针对模块可导入性跳过 | 否                                                           | 否                                                           | 否                                                           | 否                                                           |
| 示例代码                 | ```@pytest.mark.skip(reason="功能未实现") def test_feature(): # ... ``` | ```def test_feature(): if not condition: pytest.skip(reason="条件不满足") # ... ``` | ``` @pytest.mark.skipif(sys.version_info < (3, 6), reason="需要Python 3.6以上") def test_feature(): # ... ``` | 由于示例代码篇幅过长，请查阅本章节“**跳过指定目录或路径**”方法二的介绍。 |

上面的表格提供了每个装饰器/函数的用法描述、调用时机、接收的参数、是否需要提供跳过的理由、是否根据

条件跳过以及是否与模块的可导入性有关的信息，并给出了每种方法的具体代码示例。这将有助于你根据测试需求选择合适的方法以跳过测试。



# 4.7 本章小结

本章主要介绍了`pytest`测试框架中测试用例标记的概念、使用方法和实例应用等方面。我们详细介绍了标记选项的基本使用方法，包括对于一个或多个测试用例进行标记、选择标记的测试用例进行运行、标记选项的细节参数设置等。

通过本章的学习，我们了解到`pytest`测试用例标记能够帮助开发人员更加灵活和高效地运行测试用例。例如，我们可以根据不同的标记选项选择不同的测试用例进行运行，以节省时间和提高编码效率。标记也可以用于标识特定的测试目的或需求，以便更好地组织和管理我们的测试用例。

需要注意的是，`pytest`测试用例标记并不是万能的解决方案。如果我们过度使用标记，可能会导致测试用例变得复杂和难以维护，降低测试用例的可读性和可扩展性。因此，我们需要根据测试用例的实际需求和测试目的，谨慎使用测试用例标记，并根据需要进行调整和优化。

总之，`pytest`测试用例标记是`pytest`测试框架中的一个重要特性，通过本文的介绍和实例演示，我们可以更深入了解`pytest`测试框架中的测试用例标记，进一步提高我们代码测试的质量和效率，从而更好地满足我们的测试目的和需求。
