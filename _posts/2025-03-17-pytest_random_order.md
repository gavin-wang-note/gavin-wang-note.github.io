---
title: 测试用例随机执行之pytest-random-order源码解读
date: 2025-03-17 22:00:00
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
summary: 测试用例随机执行之pytest-random-order源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-random-order` 是一个 `pytest` 插件，它允许用户自定义测试用例的执行顺序，支持随机执行测试用例，或者将失败的测试用例重新排序到执行队列的前端，这个功能对于揭示测试之间的隐性依赖关系以及开发团队过分依赖测试执行顺序的情况非常有用。

## 主要特性

1. **随机执行测试**:
   - 插件支持将所有测试用例随机执行，打破执行顺序可能带来的依赖问题。

2. **失败测试优先执行**:
   - 通过命令行选项，用户可以让上次失败的测试在当前测试运行中优先执行。

3. **仅执行失败的测试**:
   - 用户可以选择只重新执行上次失败的测试，而跳过其他已通过的测试。

4. **跨会话缓存**:
   - 插件使用 `pytest` 的缓存机制来记录测试状态，实现跨测试运行的信息维护。

5. **灵活的桶类型**:
   - 用户可以指定不同的桶类型来分组测试用例，桶类型包括全局、包、模块、类、父类和自定义类型。

6. **配置和命令行选项**:
   - 插件提供了多种配置选项和命令行参数，允许用户控制随机顺序的行为。

## 工作原理

- **随机化逻辑**: 插件通过 `_shuffle_items` 函数在测试集合中随机分配测试用例到不同的桶中。
- **失败测试处理**: 使用缓存来识别失败的测试，并根据配置决定它们的执行顺序。
- **命令行接口**: 提供了 `--lf`（last failed）、`--ff`（failed first）等选项来控制失败测试的执行策略。
- **缓存操作**: 插件使用 `config.cache` 对象存储和检索测试状态信息，如失败测试列表。

## 使用场景

- **持续集成**: 在 `CI` 环境中，随机化测试顺序有助于发现潜在的隐性错误和依赖。
- **开发调试**: 开发者可以使用失败优先的策略快速定位和修复问题。
- **性能优化**: 通过优先执行失败测试，可以减少等待时间，提高测试效率。

## 集成与扩展

- **与 pytest 集成**: 插件作为 `pytest`的一部分，与 `pytest`的钩子系统和配置系统集成。
- **扩展性**: 插件允许开发者通过自定义函数和命令行选项来扩展其功能。

## 配置选项

- `--random-order`: 启用随机化测试顺序。
- `--random-order-bucket`: 指定测试用例的分组方式。
- `--random-order-seed`: 设置随机化使用的种子。

## 命令行工具

- `--lf`, `--last-failed`: 仅重新执行上次失败的测试。
- `--ff`, `--failed-first`: 先执行上次失败的测试，然后执行其他测试。
- `--cache-show`: 显示缓存内容。
- `--cache-clear`: 清除缓存内容。

`pytest-random-order` 插件为 `pytest` 用户提供了强大的测试顺序控制能力，有助于创建更健壮和可靠的自动化测试套件。



# 安装 pytest-random-order

使用 `pip` 安装 `pytest-random-order`：

```shell
pip install pytest-random-order
```



# 使用示例

在 `pytest` 测试会话中，使用 `--random-order` 参数来随机运行测试：

```shell
pytest --random-order
```

如果希望随机排序但要保持顺序可重复性，可以指定一个种子值：

```shell
pytest --random-order-seed=<seed>
```

比如：

```shell
pytest --random-order --random-order-seed=12345
```

在这个例子中，`12345` 是一个种子值。此后每次使用同一个种子值运行 `pytest` 时，测试的随机顺序将会保持一致，只要测试用例集没有变化。

通常，在测试运行结束时，如果你启用了随机顺序插件，`pytest` 会打印用于该次测试顺序的种子。例如：

```shell
Using --random-order-seed=12345
```

这样当你想要复现测试用例的随机顺序时，就可以通过提供之前生成的种子来执行。这确保了你能够重现同样的顺序，从而方便调试和解决可能出现的顺序依赖问题。

对于希望以固定顺序进行的特定测试，可以使用 `@pytest.mark.order` 标记（需要 `pytest-order` 或相似插件）：

```python
# content of test_pytest_random_order.py
import pytest

@pytest.mark.order(1)
def test_should_run_first():
    # 这个测试将总是首先执行
    pass

def test_random1():
    pass

def test_random2():
    pass

def test_random3():
    pass

def test_random4():
    pass
```

运行结果参考如下：

```shell
root@Gavin:~/pytest_plugin/test# pytest -s -v --random-order-seed=3 test_pytest_random_order.py
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Using --random-order-bucket=module
Using --random-order-seed=3

metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'profiling': '1.7.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3', 'line-profiler': '0.2.1', 'sugar': '1.0.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1, sugar-1.0.0
asyncio: mode=Mode.STRICT
collected 5 items                                                                                                                                                                                                                        

 test_pytest_random_order.py::test_should_run_first ✓                                                                                                                                                                       20% ██        
 test_pytest_random_order.py::test_random1 ✓                                                                                                                                                                                40% ████      
 test_pytest_random_order.py::test_random4 ✓                                                                                                                                                                                60% ██████    
 test_pytest_random_order.py::test_random2 ✓                                                                                                                                                                                80% ████████  
 test_pytest_random_order.py::test_random3 ✓                                                                                                                                                                               100% ██████████
======================================================================================================= sum of all tests durations =======================================================================================================
0.02s

Results (0.05s):
       5 passed
root@Gavin:~/pytest_plugin/test#
```

如果希望分组测试用例，并随后随机化各组内的测试用例顺序，可以使用：

```shell
pytest --random-order --random-order-bucket
```

`--random-order-bucket`参数接受下面几种不同的值：

- `module`：按照模块随机化测试用例顺序。同一个模块的测试用例将首先被收集，然后作为一个整体随机化它们的顺序。
- `class`：按照类随机化测试用例顺序。同一个类的测试用例将首先被收集，然后作为一个整体随机化它们的顺序。
- `package`：按照包（即目录结构）随机化测试用例顺序。同一个包或子包内的测试用例将首先被收集，然后作为一个整体随机化它们的顺序。
- `global`：测试全部随机化。不做任何分组，所有的测试用例被汇集到一起并随机排序。
- `none`：不对测试用例执行顺序做任何干预，即保持 `pytest` 默认的顺序。

例如，如果你想要按照模块来随机化测试用例的执行顺序，你可以在运行 Pytest 时采用如下命令：

```shell
pytest --random-order --random-order-bucket=module
```

另一方面，如果你想要全局随机化测试用例（不考虑模块、类或包的边界），可以使用：

```shell
pytest --random-order --random-order-bucket=global
```



# 注意事项

- **独立性**：确保你的测试没有依赖于特定的执行顺序，可以独立运行。
- **环境清理**：在测试结束后对环境进行彻底清理，以避免状态污染后续的测试。
- **数据隔离**：避免共享数据库或公共文件等资源，这些资源可能不安全地在测试间共享。
- **重现问题**：如果发现测试失败，需要记下当前的种子值，以便能在随后的调试过程中使用相同的顺序来重现问题。

`pytest-random-order` 是一个有价值的工具，对于提高测试的稳健性和可靠性有潜在的好处。然而，它可能暴露那些在某些顺序条件下不易察觉的问题，因此在集成到持续集成流程之前必须谨慎对待。



# 源码介绍



## 目录结构

从[官网](https://pypi.org/project/pytest-random-order/)下载后解压缩，目录结构如下：

```shell
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1# ll
total 60
drwxr-xr-x  5 1001 gdm   4096 Jan 20  2024 ./
drwxr-xr-x 18 root root  4096 Jul 23 15:53 ../
-rw-r--r--  1 1001 gdm   1080 Jan 20  2024 LICENSE
-rw-r--r--  1 1001 gdm    109 Jan 20  2024 MANIFEST.in
-rw-r--r--  1 1001 gdm  11554 Jan 20  2024 PKG-INFO
drwxr-xr-x  2 1001 gdm   4096 Jan 20  2024 pytest_random_order.egg-info/
drwxr-xr-x  2 1001 gdm   4096 Jan 20  2024 random_order/
-rw-r--r--  1 1001 gdm  10452 Jan 20  2024 README.rst
-rw-r--r--  1 1001 gdm    222 Jan 20  2024 setup.cfg
-rw-r--r--  1 1001 gdm   1650 Jan 20  2024 setup.py
drwxr-xr-x  2 1001 gdm   4096 Jan 20  2024 tests/
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1# cd random_order/
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order# ll
total 36
drwxr-xr-x 2 1001 gdm 4096 Jan 20  2024 ./
drwxr-xr-x 5 1001 gdm 4096 Jan 20  2024 ../
-rw-r--r-- 1 1001 gdm 1572 Jan 20  2024 bucket_types.py
-rw-r--r-- 1 1001 gdm 1116 Jan 20  2024 cache.py
-rw-r--r-- 1 1001 gdm  957 Jan 20  2024 config.py
-rw-r--r-- 1 1001 gdm   35 Jan 20  2024 __init__.py
-rw-r--r-- 1 1001 gdm 3478 Jan 20  2024 plugin.py
-rw-r--r-- 1 1001 gdm 4009 Jan 20  2024 shuffler.py
-rw-r--r-- 1 1001 gdm  210 Jan 20  2024 xdist.py
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order#
```

核心文件介绍如下：

1. **`bucket_types.py`**:
   - 这个文件可能定义了不同的测试用例分组（`bucket`）类型。在某些测试策略中，测试用例可能根据某些特征（如功能区域、依赖性等）被分为不同的组，在随机排序时可能需要对这些组内的测试用例执行特定的处理。
2. **`cache.py`**:
   - 此文件可能包含缓存逻辑，用于存储测试执行过程中的中间状态或结果，可能用于加速测试或在并行测试环境中同步状态。
3. **`config.py`**:
   - 这个文件通常包含插件的配置逻辑，可能定义了命令行选项和配置参数，这些参数控制着插件的行为，比如随机种子、是否启用某项功能等。
5. **`plugin.py`**:
   - 这个文件是 `pytest` 插件的主要入口点。它通常包含插件的类定义，该类继承自 `pytest.Plugin`，并定义了插件的钩子实现和注册逻辑。
6. **`shuffler.py`**:
   - 此文件可能包含执行测试用例随机排序逻辑的代码。它可能定义了用于打乱测试用例顺序的算法和数据结构。
7. **`xdist.py`**:
   - 这个文件专门处理与 `pytest-xdist` 插件的集成，确保在并行测试环境中随机排序的行为正确无误。根据之前的解读，`XdistHooks` 类配置了随机种子，以便在分布式测试中保持测试顺序的一致性。

这些文件共同构成了 `pytest-random-order` 插件，它们协同工作以实现测试用例的随机排序功能，并确保在并行测试环境中也能正确执行。



## 源码解读



### xdist.py文件



```python
import pytest


class XdistHooks:

    def pytest_configure_node(self, node: pytest.Item) -> None:
        seed = node.config.getoption('random_order_seed')
        node.workerinput['random_order_seed'] = seed
```



这段代码确保在使用 `pytest` 的并行执行插件（`pytest-xdist`）时，每个工作节点（`worker node`）都能够使用相同的随机种子来确定测试用例的执行顺序。

1. **导入 Pytest 模块**:
   - `import pytest`：将 `pytest` 模块导入到当前脚本中，以便使用 `pytest` 提供的类、函数和钩子。

2. **定义 XdistHooks 类**:
   - `class XdistHooks:`：声明了一个名为 `XdistHooks` 的类。这个类可能用于挂载或定义与 `pytest-xdist` 插件相关的特定钩子或功能。

3. **配置节点钩子方法**:
   - `def pytest_configure_node(self, node: pytest.Item) -> None:`：在 `pytest` 中，`pytest_configure_node` 是一个钩子方法，它会在每个工作节点开始工作前被调用。这个方法用于配置节点，传入的 `node` 参数是一个 `pytest` 的 `Item` 对象，代表当前的工作节点或测试用例集合。
   - `-> None` 表示这个方法没有返回值。

4. **获取随机种子配置**:
   - `seed = node.config.getoption('random_order_seed')`：从当前节点的配置中获取 `random_order_seed` 选项的值。这个配置是由用户在使用 Pytest 时通过命令行选项指定的，用于设置随机执行测试用例的种子。

5. **设置工作输入**:
   - `node.workerinput['random_order_seed'] = seed`：将获取到的随机种子 `seed` 设置到 `node.workerinput` 字典中，以 `'random_order_seed'` 作为键。`workerinput` 是一个在 `pytest-xdist` 插件中使用的特殊字典，用于存储需要发送给工作进程的数据。这样，每个工作进程在执行测试用例时都会接收到相同的随机种子，以确保它们可以生成一致的测试执行顺序。

通过这种方式，`pytest-random-order` 插件确保了即使在并行测试环境中，测试用例的执行顺序也能保持随机性，同时在不同的工作进程中保持一致，这对于确保测试结果的可重复性非常重要。



### shuffler.py文件

此文件负责打乱测试项的顺序，可以根据用户定义的约束条件进行定制和集成到 `pytest` 的测试执行流程中，确保测试可以以随机顺序执行，同时尊重特定的用户定义的限制。

```python
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order# cat shuffler.py 
# -*- coding: utf-8 -*-

import random
from collections import OrderedDict, namedtuple

from random_order.cache import FAILED_FIRST_LAST_FAILED_BUCKET_KEY

"""
`bucket` is a string representing the bucket in which the item falls based on user's chosen
bucket type.

`disabled` is either a falsey value to mark that the item is ready for shuffling (shuffling is not disabled),
or a truthy value in which case the item won't be shuffled among other items with the same key.

In some cases it is important for the `disabled` to be more than just True in order
to preserve a distinct disabled sub-bucket within a larger bucket and not mix it up with another
disabled sub-bucket of the same larger bucket.
"""
ItemKey = namedtuple('ItemKey', field_names=('bucket', 'disabled', 'x'))
ItemKey.__new__.__defaults__ = (None, None)


def _shuffle_items(items, bucket_key=None, disable=None, seed=None, session=None):
    """
    Shuffles a list of `items` in place.

    If `bucket_key` is None, items are shuffled across the entire list.

    `bucket_key` is an optional function called for each item in `items` to
    calculate the key of bucket in which the item falls.

    Bucket defines the boundaries across which items will not
    be shuffled.

    `disable` is a function that takes an item and returns a falsey value
    if this item is ok to be shuffled. It returns a truthy value otherwise and
    the truthy value is used as part of the item's key when determining the bucket
    it belongs to.
    """

    if seed is not None:
        random.seed(seed)

    # If `bucket_key` is falsey, shuffle is global.
    if not bucket_key and not disable:
        random.shuffle(items)
        return

    def get_full_bucket_key(item):
        assert bucket_key or disable
        if bucket_key and disable:
            return ItemKey(bucket=bucket_key(item, session), disabled=disable(item, session))
        elif disable:
            return ItemKey(disabled=disable(item, session))
        else:
            return ItemKey(bucket=bucket_key(item, session))

    # For a sequence of items A1, A2, B1, B2, C1, C2,
    # where key(A1) == key(A2) == key(C1) == key(C2),
    # items A1, A2, C1, and C2 will end up in the same bucket.
    buckets = OrderedDict()
    for item in items:
        full_bucket_key = get_full_bucket_key(item)
        if full_bucket_key not in buckets:
            buckets[full_bucket_key] = []
        buckets[full_bucket_key].append(item)

    # Shuffle inside a bucket

    bucket_keys = list(buckets.keys())

    for full_bucket_key in buckets.keys():
        if full_bucket_key.bucket == FAILED_FIRST_LAST_FAILED_BUCKET_KEY:
            # Do not shuffle the last failed bucket
            continue

        if not full_bucket_key.disabled:
            random.shuffle(buckets[full_bucket_key])

    # Shuffle buckets

    # Only the first bucket can be FAILED_FIRST_LAST_FAILED_BUCKET_KEY
    if bucket_keys and bucket_keys[0].bucket == FAILED_FIRST_LAST_FAILED_BUCKET_KEY:
        new_bucket_keys = list(buckets.keys())[1:]
        random.shuffle(new_bucket_keys)
        new_bucket_keys.insert(0, bucket_keys[0])
    else:
        new_bucket_keys = list(buckets.keys())
        random.shuffle(new_bucket_keys)

    items[:] = [item for bk in new_bucket_keys for item in buckets[bk]]
    return


def _get_set_of_item_ids(items):
    s = {}
    try:
        s = set(item.nodeid for item in items)
    finally:
        return s


def _disable(item, session):
    if hasattr(item, 'get_closest_marker'):
        marker = item.get_closest_marker('random_order')
    else:
        marker = item.get_marker('random_order')
    if marker:
        is_disabled = marker.kwargs.get('disabled', False)
        if is_disabled:
            # A test item can only be disabled in its parent context -- where it is part of some order.
            # We use parent name as the key so that all children of the same parent get the same disabled key.
            return item.parent.name
    return False
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order#
```



1. **导入和 `ItemKey` 命名元组**:
   - 导入 `random` 模块用于打乱顺序，以及 `OrderedDict` 和 `namedtuple` 从 `collections` 模块。
   - 定义了一个 `ItemKey` 命名元组，用于表示每个测试项的键，包括 `bucket`（桶）、`disabled`（是否禁用打乱）和 `x`。这个键用于确定测试项属于哪个组。

2. **`_shuffle_items` 函数**:
   - 这个函数负责就地（in place）打乱 `items` 列表。
   - 如果 `bucket_key` 是 `None`，则整个列表中的项将被打乱。
   - `bucket_key` 是一个可选的函数，用于计算每个测试项所属的桶的键。
   - 桶定义了项不会跨越的边界，即同一桶内的项不会与桶外的项混合打乱。
   - `disable` 是一个函数，它接受一个测试项并返回一个假值（`falsy value`）如果该项可以被打乱，或者返回一个真值（`truthy value`），真值将作为测试项键的一部分，用于确定它属于哪个桶。
   - 如果提供了 `seed`，则使用该种子设置随机数生成器，以确保结果的可重复性。
   - 如果 `bucket_key` 和 `disable` 都未提供，则进行全局打乱。
   - 使用嵌套函数 `get_full_bucket_key` 确定每个测试项的完整桶键。
   - 使用 `OrderedDict` 叫做 `buckets` 的字典来分组测试项。
   - 在各自的桶内打乱测试项，但对最后一个失败的桶不进行打乱。
   - 打乱桶的顺序，但保持最后一个失败的桶（如果有）在首位。

3. **`_get_set_of_item_ids` 函数**:
   - 这个实用函数接收测试项列表并返回它们的 `node ID` 集合。

4. **`_disable` 函数**:
   - 根据 `random_order` 标记的存在和其 `disabled` 关键字参数的值，确定是否禁用对给定测试项的打乱。
   - 如果 `disabled` 为真，则返回父项的名称作为禁用键，确保同一父项下的所有子项使用相同的禁用键。

5. **注释和文档**:
   - 代码包含广泛的注释和文档字符串，解释了函数和 `ItemKey` 命名元组的目的和行为。

6. **打乱逻辑**:
   - 打乱过程被精心设计，以尊重特定的边界（桶）和条件（禁用状态），确保测试顺序以受控的方式随机化。

7. **种子设置**:
   - 设置随机种子的选项对于在调试期间或需要复制特定测试结果时重现测试结果至关重要。

8. **桶处理**:
   - 桶的概念允许自定义测试项如何分组和打乱，提供了在定义打乱行为时的灵活性。



### plugin.py文件

`plugin.py` 文件是 `pytest-random-order` 插件的主要入口点，负责插件的配置和主要逻辑。

```python
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order# cat plugin.py 
import random
import sys
import traceback
import warnings

import pytest

from random_order.bucket_types import bucket_type_keys, bucket_types
from random_order.cache import process_failed_first_last_failed
from random_order.config import Config
from random_order.shuffler import _disable, _get_set_of_item_ids, _shuffle_items
from random_order.xdist import XdistHooks


def pytest_addoption(parser):
    group = parser.getgroup('pytest-random-order options')
    group.addoption(
        '--random-order',
        action='store_true',
        dest='random_order_enabled',
        help='Randomise test order (by default, it is disabled) with default configuration.',
    )
    group.addoption(
        '--random-order-bucket',
        action='store',
        dest='random_order_bucket',
        default=Config.default_value('module'),
        choices=bucket_types,
        help='Randomise test order within specified test buckets.',
    )
    group.addoption(
        '--random-order-seed',
        action='store',
        dest='random_order_seed',
        default=Config.default_value(str(random.randint(1, 1000000))),
        help='Randomise test order using a specific seed.',
    )


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'random_order(disabled=True): disable reordering of tests within a module or class'
    )

    if config.pluginmanager.hasplugin('xdist'):
        config.pluginmanager.register(XdistHooks())

    if hasattr(config, 'workerinput'):
        # pytest-xdist: use seed generated on main.
        seed = config.workerinput['random_order_seed']
        if hasattr(config, 'cache'):
            assert config.cache is not None
            config.cache.set('random_order_seed', seed)
        config.option.random_order_seed = seed


def pytest_report_header(config):
    plugin = Config(config)
    if not plugin.is_enabled:
        return "Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>"
    return (
        'Using --random-order-bucket={plugin.bucket_type}\n'
        'Using --random-order-seed={plugin.seed}\n'
    ).format(plugin=plugin)


def pytest_collection_modifyitems(session, config, items):
    failure = None

    session.random_order_bucket_type_key_handlers = []
    process_failed_first_last_failed(session, config, items)

    item_ids = _get_set_of_item_ids(items)

    plugin = Config(config)

    try:
        seed = plugin.seed
        bucket_type = plugin.bucket_type
        if bucket_type != 'none':
            _shuffle_items(
                items,
                bucket_key=bucket_type_keys[bucket_type],
                disable=_disable,
                seed=seed,
                session=session,
            )

    except Exception as e:
        # See the finally block -- we only fail if we have lost user's tests.
        _, _, exc_tb = sys.exc_info()
        failure = 'pytest-random-order plugin has failed with {0!r}:\n{1}'.format(
            e, ''.join(traceback.format_tb(exc_tb, 10))
        )
        if not hasattr(pytest, "PytestWarning"):
            config.warn(0, failure, None)
        else:
            warnings.warn(pytest.PytestWarning(failure))

    finally:
        # Fail only if we have lost user's tests
        if item_ids != _get_set_of_item_ids(items):
            if not failure:
                failure = 'pytest-random-order plugin has failed miserably'
            raise RuntimeError(failure)
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order#
```



以下是对该代码的解读：

1. **导入依赖**:
   - 导入了 `random`、`sys`、`traceback`、`warnings` 等 Python 标准库模块，以及 `pytest`。
   - 从 `random_order` 包中导入了相关的模块和类。

2. **添加命令行选项**:
   - `pytest_addoption` 函数用于向 Pytest 添加自定义命令行选项，允许用户控制随机顺序的行为。

3. **配置插件**:
   - `pytest_configure` 函数在 Pytest 配置阶段被调用，用于注册插件和处理与 `pytest-xdist` 的集成。

4. **报告头部信息**:
   - `pytest_report_header` 函数用于在测试报告的头部添加关于插件状态的信息。

5. **修改测试集合**:
   - `pytest_collection_modifyitems` 函数在测试项集合构建阶段被调用，用于修改测试项的顺序。

6. **详细解读**:

```python
def pytest_addoption(parser):
```
   - 为插件添加命令行选项，包括启用随机顺序、指定桶类型和设置随机种子。

```python
def pytest_configure(config):
```
   - 在 Pytest 配置阶段注册配置项和钩子，特别是与 `pytest-xdist` 的集成。

```python
def pytest_report_header(config):
```
   - 在测试报告的头部输出插件的配置信息，例如使用的桶类型和随机种子。

```python
def pytest_collection_modifyitems(session, config, items):
```
   - 核心函数，用于修改测试项的顺序：
     - `session.random_order_bucket_type_key_handlers` 用于存储桶类型处理器。
     - `process_failed_first_last_failed` 处理失败的测试项，确保它们按照特定的顺序执行。
     - `_get_set_of_item_ids` 获取测试项的 `ID` 集合，用于后续检查。
     - `Config` 类用于封装插件的配置。
     - `_shuffle_items` 根据配置的桶类型和种子打乱测试项。
     - 如果在打乱过程中出现异常，会捕获异常并记录失败信息。
     - 无论是否发生异常，都会检查测试项集合是否发生了意外的变更。

7. **错误处理**:
   - 在 `pytest_collection_modifyitems` 函数中，如果插件执行失败，并且用户的测试项丢失，则会抛出 `RuntimeError`。

8. **警告**:
   - 如果插件发生错误，但测试项没有丢失，会通过 `PytestWarning` 发出警告。

`plugin.py` 文件体现了 `pytest` 插件的典型结构，包括命令行选项、配置、报告和测试项集合的修改。通过这些钩子函数，插件能够介入 `pytest` 的执行流程，并实现自定义的测试顺序随机化逻辑。





### config.py文件

`config.py` 文件包含了 `pytest-random-order` 插件的配置管理逻辑。

```python
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order# cat config.py 
class Config:

    @classmethod
    def default_value(cls, value):
        return "default:" + str(value)

    def __init__(self, config):
        self._config = config

    @property
    def bucket_type(self):
        if not self.is_enabled:
            return 'none'
        else:
            return self._remove_default_prefix(self._config.getoption('random_order_bucket'))

    @property
    def is_enabled(self):
        return (
            self._config.getoption('random_order_enabled') or
            any(
                not self._config.getoption(name).startswith('default:')
                for name in ('random_order_bucket', 'random_order_seed')
            )
        )

    @property
    def seed(self):
        return self._remove_default_prefix(self._config.getoption('random_order_seed'))

    def _remove_default_prefix(self, value):
        if value.startswith('default:'):
            return value[len('default:'):]
        return value
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order#
```



以下是对该文件中代码的解读：

1. **Config 类定义**:
   - `Config` 类用于封装和提供插件配置的访问方法。

2. **默认值方法**:
   - `@classmethod` 装饰的 `default_value` 类方法用于生成带有默认前缀的字符串，这有助于识别配置项是否使用了默认值。

3. **构造函数**:
   - `__init__(self, config)` 构造函数接收一个 `pytest` 配置对象，并将其存储为实例变量 `_config`。

4. **bucket_type 属性**:
   - `@property` 装饰的 `bucket_type` 属性用于获取桶类型配置。如果插件未启用，则返回 `'none'`；否则，调用 `_remove_default_prefix` 方法去除默认值前缀，并返回桶类型的值。

5. **is_enabled 属性**:
   - `@property` 装饰的 `is_enabled` 属性用于检查插件是否启用。如果 `--random-order-enabled` 选项被设置为 `True`，或者 `--random-order-bucket` 和 `--random-order-seed` 选项的值不以 `'default:'` 前缀开头，则认为插件已启用。

6. **seed 属性**:
   - `@property` 装饰的 `seed` 属性用于获取随机种子配置。调用 `_remove_default_prefix` 方法去除默认值前缀，并返回种子的值。

7. **去除默认前缀方法**:
   - `_remove_default_prefix` 方法用于去除配置值中的 `'default:'` 前缀。如果值以该前缀开头，则去除它并返回剩余部分；否则，直接返回原始值。

8. **配置逻辑**:
   - 该类中的配置逻辑确保插件能够正确地从 `pytest` 配置中读取和解析选项，同时提供了一种机制来识别和处理默认值。

`config.py` 文件的代码体现了插件配置管理的典型模式，包括处理默认值、检查插件启用状态和获取配置选项的值。通过 `Config` 类，插件能够灵活地管理其配置，并在 `pytest` 的测试执行流程中应用这些配置。



### cache.py文件



`cache.py` 文件利用 `pytest` 的缓存机制来处理失败测试的重试逻辑。

```python
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order# cat cache.py 
"""
This module is called "cache" because it builds on the "cache" plugin:

    https://docs.pytest.org/en/latest/cache.html

"""

FAILED_FIRST_LAST_FAILED_BUCKET_KEY = '<failed_first_last_failed>'


def process_failed_first_last_failed(session, config, items):
    if not hasattr(config, 'cache'):
        return

    if not config.getoption('failedfirst'):
        return

    last_failed_raw = config.cache.get('cache/lastfailed', None)
    if not last_failed_raw:
        return

    # Get the names of last failed tests
    last_failed = []
    for key in last_failed_raw.keys():
        parts = key.split('::')
        if len(parts) == 3:
            last_failed.append(tuple(parts))
        elif len(parts) == 2:
            last_failed.append((parts[0], None, parts[1]))
        else:
            raise NotImplementedError()

    def assign_last_failed_to_same_bucket(item, key):
        if item.nodeid in last_failed_raw:
            return FAILED_FIRST_LAST_FAILED_BUCKET_KEY
        else:
            return key

    session.random_order_bucket_type_key_handlers.append(assign_last_failed_to_same_bucket)
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order# 
```



以下是对该文件中代码的解读：

1. **模块说明**:
   - 该模块建立在 `pytest` 的 "cache" 插件之上，用于在测试运行之间存储和访问信息。

2. **失败测试处理**:
   - 定义了一个特殊的桶键 `FAILED_FIRST_LAST_FAILED_BUCKET_KEY`，用于标识应该首先执行的失败测试。

3. **处理失败测试的函数**:
   - `process_failed_first_last_failed` 函数用于处理上一次测试运行中失败的测试项，确保它们在下一次测试运行中首先被执行。

4. **缓存访问**:
   - 函数首先检查配置对象 `config` 是否具有 `cache` 属性，这是 `pytest` 缓存插件提供的功能。

5. **检查 `--failed-first` 选项**:
   - 如果没有启用 `--failed-first` 选项（`config.getoption('failedfirst')`），函数将不执行任何操作。

6. **获取上次失败的测试**:
   - 使用 `config.cache.get('cache/lastfailed', None)` 获取上次测试运行中失败的测试项的缓存信息。

7. **解析失败测试的名称**:
   - 遍历 `last_failed_raw` 字典的键，解析出失败测试的路径和测试用例名称，并将它们存储在 `last_failed` 列表中。

8. **分配失败测试到桶**:
   - 定义了一个内部函数 `assign_last_failed_to_same_bucket`，它根据测试项的 `nodeid` 是否存在于 `last_failed_raw` 中，决定将测试项分配到特殊的失败测试桶，或者使用其原始的键。

9. **添加桶类型处理器**:
   - 将 `assign_last_failed_to_same_bucket` 函数添加到 `session.random_order_bucket_type_key_handlers` 列表中，这个列表中的函数将用于确定每个测试项的桶键。

通过这种方式，`cache.py` 文件实现了在测试执行顺序随机化的同时，保证失败的测试能够按照用户配置的选项（如 `--failed-first`）优先执行。这有助于开发者更快地定位和修复测试失败的问题。





### bucket_types.py文件

`bucket_types.py` 文件定义了 `pytest-random-order` 插件中用于确定测试项如何分组（即放入哪个桶）的逻辑。

```python
root@Gavin:~/pytest_plugin/pytest-random-order-1.1.1/random_order# cat bucket_types.py 
import functools
import os.path
from collections import OrderedDict

bucket_type_keys = OrderedDict()


def bucket_type_key(bucket_type):
    """
    Registers a function that calculates test item key for the specified bucket type.
    """

    def decorator(f):

        @functools.wraps(f)
        def wrapped(item, session):
            key = f(item)

            if session is not None:
                for handler in session.random_order_bucket_type_key_handlers:
                    key = handler(item, key)

            return key

        bucket_type_keys[bucket_type] = wrapped
        return wrapped

    return decorator


@bucket_type_key('global')
def get_global_key(item):
    return None


@bucket_type_key('package')
def get_package_key(item):
    if not hasattr(item, "module"):
        return os.path.split(item.location[0])[0]
    return item.module.__package__


@bucket_type_key('module')
def get_module_key(item):
    return item.location[0]


@bucket_type_key('class')
def get_class_key(item):
    if not hasattr(item, "cls"):
        return item.location[0]
    if item.cls:
        return item.module.__name__, item.cls.__name__
    else:
        return item.module.__name__


@bucket_type_key('parent')
def get_parent_key(item):
    return item.parent


@bucket_type_key('grandparent')
def get_grandparent_key(item):
    return item.parent.parent


@bucket_type_key('none')
def get_none_key(item):
    raise RuntimeError('When shuffling is disabled (bucket_type=none), item key should not be calculated')


bucket_types = bucket_type_keys.keys()
```



代码解读如下：

1. **导入依赖**:
   - 导入了 `functools` 用于修饰函数，`os.path` 用于路径操作，以及 `OrderedDict` 用于存储桶类型键函数。

2. **bucket_type_keys**:
   - `bucket_type_keys` 是一个 `OrderedDict`，用于存储桶类型名称到其对应的键生成函数的映射。

3. **bucket_type_key 装饰器**:
   - `bucket_type_key` 是一个装饰器工厂，它接收一个桶类型名称 `bucket_type`，返回一个新的装饰器。
   - 这个装饰器接收一个函数 `f`，这个函数用于计算测试项的键。
   - 装饰器通过 `functools.wraps` 保留了原始函数的名称和文档字符串。
   - 装饰器内部定义了一个包装函数 `wrapped`，它在计算键时会应用会话（`session`）中的处理器。

4. **桶类型函数**:
   - 文件中定义了多个函数，每个函数对应一种桶类型，用于计算测试项的键：
     - `get_global_key`: 全局桶，所有测试项共享一个键，返回 `None`。
     - `get_package_key`: 包桶，测试项按 `Python` 包分组。
     - `get_module_key`: 模块桶，测试项按 `Python` 模块分组。
     - `get_class_key`: 类桶，测试项按 `Python` 类分组。
     - `get_parent_key`: 父项桶，测试项按父项分组。
     - `get_grandparent_key`: 祖父项桶，测试项按祖父项分组。
     - `get_none_key`: 当禁用随机打乱时调用，通常会抛出运行时错误。

5. **桶类型集合**:
   - `bucket_types` 包含了所有可用的桶类型名称的集合。

6. **会话处理器**:
   - 在 `wrapped` 函数中，如果会话（`session`）对象不为空，它会遍历 `session.random_order_bucket_type_key_handlers` 中的处理器，并更新键的值。

7. **装饰器应用**:
   - 每个桶类型函数都用 `@bucket_type_key('bucket_type_name')` 装饰器标记，这样插件就知道如何根据桶类型计算测试项的键。

8. **错误处理**:
   - 当桶类型为 `none` 时，即插件被禁用时，`get_none_key` 函数将抛出一个 `RuntimeError`，因为此时不应该计算测试项的键。

通过这些机制，`bucket_types.py` 允许插件用户通过命令行选项指定测试项的分组方式，从而控制随机打乱的范围和行为。



# 结语

`pytest-random-order` 插件为 `pytest` 用户提供了强大的测试顺序控制能力，有助于创建更健壮和可靠的自动化测试套件。

