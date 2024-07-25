---
title: 测试用例执行顺序之pytest-order源码解读
date: 2025-02-01 22:00:00
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
summary: 测试用例执行顺序之pytest-order源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

今天我们来解读一下`pytest-order`源码，以及使用`pytest-order`中的一个坑的介绍。

The content is a bit long, please read patiently. -\^-\^-

了解这一块的同学可能会提及另外一个插件`pytest-ordering`，这两者之间关系比较密切，准确的说`pytest-order`是`pytest-ordering`的一个分支，但是`pytest-ordering`已经不维护了（多年未更新了,官网有说：This is a fork of pytest-ordering. That project is not maintained anymore, and there are several helpful PRs that are now integrated into pytest-order. ），所以就介绍介绍`pytest-order`吧。


# 源码目录结构

[官网](https://pypi.org/project/pytest-order)下载后解压，目录结构如下：

```shell
root@Gavin:~/pytest_plugin# cd pytest-order-1.2.1/
root@Gavin:~/pytest_plugin/pytest-order-1.2.1# ll
total 80
drwxr-xr-x  7 1001 gdm  4096 Apr  3 03:09 ./
drwxr-xr-x 15 root root 4096 Jul 18 10:16 ../
-rw-r--r--  1 1001 gdm   347 Apr  3 03:08 AUTHORS
-rw-r--r--  1 1001 gdm  9153 Apr  3 03:08 CHANGELOG.md
drwxr-xr-x  3 1001 gdm  4096 Apr  3 03:09 docs/
drwxr-xr-x  4 1001 gdm  4096 Apr  3 03:09 example/
-rw-r--r--  1 1001 gdm  1148 Apr  3 03:08 LICENSE
-rw-r--r--  1 1001 gdm   172 Apr  3 03:08 MANIFEST.in
-rw-r--r--  1 1001 gdm  7640 Apr  3 03:09 PKG-INFO
drwxr-xr-x  2 1001 gdm  4096 Apr  3 03:09 pytest_order/
drwxr-xr-x  2 1001 gdm  4096 Apr  3 03:09 pytest_order.egg-info/
-rw-r--r--  1 1001 gdm  6184 Apr  3 03:08 README.md
-rw-r--r--  1 1001 gdm   165 Apr  3 03:09 setup.cfg
-rw-r--r--  1 1001 gdm  1929 Apr  3 03:08 setup.py
drwxr-xr-x  2 1001 gdm  4096 Apr  3 03:09 tests/
-rw-r--r--  1 1001 gdm   648 Apr  3 03:08 tox.ini
root@Gavin:~/pytest_plugin/pytest-order-1.2.1# cd pytest_order
root@Gavin:~/pytest_plugin/pytest-order-1.2.1/pytest_order# ll
total 56
drwxr-xr-x 2 1001 gdm  4096 Apr  3 03:09 ./
drwxr-xr-x 7 1001 gdm  4096 Apr  3 03:09 ../
-rw-r--r-- 1 1001 gdm    22 Apr  3 03:08 __init__.py
-rw-r--r-- 1 1001 gdm  7545 Apr  3 03:08 item.py
-rw-r--r-- 1 1001 gdm  5241 Apr  3 03:08 plugin.py
-rw-r--r-- 1 1001 gdm  2536 Apr  3 03:08 settings.py
-rw-r--r-- 1 1001 gdm 21385 Apr  3 03:08 sorter.py
root@Gavin:~/pytest_plugin/pytest-order-1.2.1/pytest_order#
```

核心源码在`pytest_order`目录下。

# 源码解读

## 文件item.py 

该文件主要为`pytest-order` 提供基础支持，包括表示和处理测试项的类、按标记顺序排序项目和处理标记。通过这些类与方法，实现了定义和执行测试项顺序的功能。在实际运用中，整体框架便于管理复杂的测试项顺序关系，满足深层次测试需求。


```python
import sys
from typing import Optional, List, Dict, Tuple, Generic, TypeVar

from _pytest.python import Function

from .settings import Scope, Settings


_ItemType = TypeVar("_ItemType", "Item", "ItemGroup")


class Item:
    """Represents a single test item."""

    def __init__(self, item: Function) -> None:
        self.item: Function = item  # 代表一个单一的测试项
        self.nr_rel_items: int = 0  # 表示与其他项相关的数量
        self.order: Optional[int] = None  # 表示其顺序
        self._node_id: Optional[str] = None  # 节点ID

    def inc_rel_marks(self) -> None:
        if self.order is None:
            self.nr_rel_items += 1  # 增加相关项数量

    def dec_rel_marks(self) -> None:
        if self.order is None:
            self.nr_rel_items -= 1  # 减少相关项数量

    @property
    def module_path(self) -> str:
        return self.item.nodeid[: self.node_id.index("::")]  # 获取模块路径

    def parent_path(self, level) -> str:
        return "/".join(self.module_path.split("/")[:level])  # 获取父路径

    @property
    def node_id(self) -> str:
        if self._node_id is None:
            # pytest 4 之前的版本中，nodeid 包含不需要的 ::()
            self._node_id = self.item.nodeid.replace("::()", "")
        return self._node_id
```

### Item 类

`Item` 类表示单一的测试项。包含以下主要属性和方法：
- `item`：测试项本身，是一个 `_pytest.python.Function` 对象.
- `nr_rel_items`：相关项数量。用于管理与此项相关联的其他测试项数量。
- `order`：测试项的执行顺序。
- `node_id`：采用惰性加载的方式获取测试项的节点ID。

```python
class ItemList:
    """Handles a group of items with the same scope."""

    def __init__(
        self,
        items: List[Item],
        settings: Settings,
        scope: Scope,
        rel_marks: List["RelativeMark[Item]"],
        dep_marks: List["RelativeMark[Item]"],
    ) -> None:
        self.items = items  # 项目列表
        self.settings = settings  # 设置
        self.scope = scope  # 范围
        self.start_items: List[Tuple[int, List[Item]]] = []  # 起始项
        self.end_items: List[Tuple[int, List[Item]]] = []  # 结束项
        self.unordered_items: List[Item] = []  # 无序项
        self._start_items: Dict[int, List[Item]] = {}  # 内部起始项字典
        self._end_items: Dict[int, List[Item]] = {}  # 内部结束项字典
        self.all_rel_marks = rel_marks  # 所有关系标记
        self.all_dep_marks = dep_marks  # 所有依赖标记
        self.rel_marks = filter_marks(rel_marks, items)  # 过滤后的关系标记
        self.dep_marks = filter_marks(dep_marks, items)  # 过滤后的依赖标记

    def collect_markers(self, item: Item) -> None:
        self.handle_order_mark(item)
        if item.nr_rel_items or item.order is None:
            self.unordered_items.append(item)

    def handle_order_mark(self, item: Item) -> None:
        if item.order is not None:
            if item.order < 0:
                self._end_items.setdefault(item.order, []).append(item)
            else:
                self._start_items.setdefault(item.order, []).append(item)

    def sort_numbered_items(self) -> List[Item]:
        self.start_items = sorted(self._start_items.items())
        self.end_items = sorted(self._end_items.items())
        sorted_list = []
        index = 0
        for order, items in self.start_items:
            if self.settings.sparse_ordering:
                while order > index and self.unordered_items:
                    sorted_list.append(self.unordered_items.pop(0))
                    index += 1
            sorted_list += items
            index += len(items)
        mid_index = len(sorted_list)
        index = -1
        for order, items in reversed(self.end_items):
            if self.settings.sparse_ordering:
                while order < index and self.unordered_items:
                    sorted_list.insert(mid_index, self.unordered_items.pop())
                    index -= 1
            sorted_list[mid_index:mid_index] = items
            index -= len(items)
        sorted_list[mid_index:mid_index] = self.unordered_items
        return sorted_list

    def print_unhandled_items(self) -> None:
        msg = " ".join(
            [mark.item.node_id for mark in self.rel_marks]
            + [mark.item.node_id for mark in self.dep_marks]
        )
        if msg:
            sys.stdout.write("\nWARNING: cannot execute test relative to others: ")
            sys.stdout.write(msg)
            sys.stdout.write(" - ignoring the marker.\n")
            sys.stdout.flush()

    def number_of_rel_groups(self) -> int:
        return len(self.rel_marks) + len(self.dep_marks)

    def handle_rel_marks(self, sorted_list: List[Item]) -> None:
        self.handle_relative_marks(self.rel_marks, sorted_list, self.all_rel_marks)

    def handle_dep_marks(self, sorted_list: List[Item]) -> None:
        self.handle_relative_marks(self.dep_marks, sorted_list, self.all_dep_marks)

    @staticmethod
    def handle_relative_marks(
        marks: List["RelativeMark[Item]"],
        sorted_list: List[Item],
        all_marks: List["RelativeMark[Item]"],
    ) -> None:
        for mark in reversed(marks):
            if move_item(mark, sorted_list):
                marks.remove(mark)
                all_marks.remove(mark)

    def group_order(self) -> Optional[int]:
        if self.start_items:
            return self.start_items[0][0]
        elif self.end_items:
            return self.end_items[-1][0]
        return None

```

### ItemList 类

`ItemList` 类处理具有相同范围的一组测试项。主要功能是收集并排序测试项，处理排序标记和关闭标记。主要方法与属性有:

- `__init__`: 初始化方法，接受一组测试项及其相关的标记。
- `collect_markers`: 收集测试项的标记并将未排序项追加到列表中。
- `handle_order_mark`: 根据顺序标记将项添加到起始项或结束项字典中。
- `sort_numbered_items`: 根据起始项和结束项将测试项排序。
- `print_unhandled_items`: 打印未被处理的项。
- `number_of_rel_groups`: 返回关系标记组数量。
- `handle_rel_marks`: 处理关系标记。
- `handle_dep_marks`: 处理依赖标记。


#### collect_markers 方法

```python
    def collect_markers(self, item: Item) -> None:
        self.handle_order_mark(item)
        if item.nr_rel_items or item.order is None:
            self.unordered_items.append(item)
```

这个方法主要作用是收集测试用例的标记，并根据这些标记对测试用例进行分类处理。

- 参数：
  item：一个 `Item` 对象，代表单个测试用例。

- 功能：
  调用 handle_order_mark 方法来处理 item 的顺序标记。
  检查 item 的 nr_rel_items（相对标记的数量）和 order 属性：
    如果 item 没有相对标记（`nr_rel_items` 为0）且没有指定顺序（`order` 为 `None`），则将该 `item` 添加到 `unordered_items` 列表中。这些未排序的测试用例将在所有已排序测试用例之后执行。

#### handle_order_mark 方法

```python
    def handle_order_mark(self, item: Item) -> None:
        if item.order is not None:
            if item.order < 0:
                self._end_items.setdefault(item.order, []).append(item)
            else:
                self._start_items.setdefault(item.order, []).append(item)
```

这个方法主要作用是处理单个测试用例的顺序标记。

- 参数：
  `item`：一个 `Item` 对象，代表单个测试用例。

- 功能：
  检查 `item` 的 `order` 属性：
  * 如果 `order` 不为 `None`（即测试用例有指定的执行顺序），则根据 `order` 的值将 `item` 分类到 `_start_items` 或 `_end_items` 字典中：
    如果 `order` 为负数（如 -1，表示最后执行），则将 `item` 添加到 `_end_items` 字典中，以 `order` 值为键。
    如果 `order` 为正数或零（如 1，表示最先执行），则将 `item` 添加到 `_start_items` 字典中，以 `order` 值为键。

- 代码逻辑



* 收集标记：
  遍历所有测试用例，调用 `collect_markers` 方法。
  对每个测试用例，调用 `handle_order_mark` 方法处理其顺序标记。

* 分类存储：
  根据 `order` 值，将测试用例存储在` _start_items`（正数或零）或 `_end_items`（负数）字典中。
  未指定顺序的测试用例存储在 `unordered_items` 列表中。

* 排序执行：
  在实际执行测试用例之前，根据 `_start_items、_end_items` 和 `unordered_items` 中的顺序，构建最终的执行顺序。

**注意事项：**

- 全局性：一旦使用了 `order` 标记，所有测试用例都需要明确指定其顺序，否则可能会影响预期的执行顺序。
- 负数顺序：负数 `order` 值表示测试用例将在其他测试用例之后执行，这在需要在测试结束时执行某些清理操作时非常有用。


#### sort_numbered_items方法

`sort_numbered_items` 方法的作用是将测试用例按照指定的顺序进行排序，既做到灵活地控制测试用例的执行顺序，同时又能保持代码的可读性和可维护性。

```python
    def sort_numbered_items(self) -> List[Item]:
        self.start_items = sorted(self._start_items.items())
        self.end_items = sorted(self._end_items.items())
        sorted_list = []
        index = 0
        for order, items in self.start_items:
            if self.settings.sparse_ordering:
                while order > index and self.unordered_items:
                    sorted_list.append(self.unordered_items.pop(0))
                    index += 1
            sorted_list += items
            index += len(items)
        mid_index = len(sorted_list)
        index = -1
        for order, items in reversed(self.end_items):
            if self.settings.sparse_ordering:
                while order < index and self.unordered_items:
                    sorted_list.insert(mid_index, self.unordered_items.pop())
                    index -= 1
            sorted_list[mid_index:mid_index] = items
            index -= len(items)
        sorted_list[mid_index:mid_index] = self.unordered_items
        return sorted_list
```

逻辑解读如下：

1. **排序起始和结束项**：
   - `self.start_items = sorted(self._start_items.items())`：将具有正数或零顺序标记的测试用例（存储在 `_start_items` 字典中）按顺序值进行排序。
   - `self.end_items = sorted(self._end_items.items())`：将具有负数顺序标记的测试用例（存储在 `_end_items` 字典中）按顺序值进行排序。

2. **初始化排序列表**：
   - `sorted_list = []`：创建一个空列表，用于存储排序后的测试用例。

3. **处理起始项**：
   - 遍历 `self.start_items` 中的每个顺序值和对应的测试用例列表：
     - 如果设置了 `self.settings.sparse_ordering`（稀疏排序），则在将未排序的测试用例插入到当前位置之前，先将它们插入到排序列表中，直到达到当前顺序值。
     - 将当前顺序的测试用例添加到 `sorted_list`。
     - 更新 `index` 值，表示已排序的测试用例数量。

4. **处理中间项**：
   - `mid_index = len(sorted_list)`：记录排序列表的中间索引位置。

5. **处理结束项**：
   - 遍历 `self.end_items` 中的每个顺序值和对应的测试用例列表（逆序遍历）：
     - 如果设置了 `self.settings.sparse_ordering`，则在将未排序的测试用例插入到当前位置之前，先将它们插入到排序列表中，直到达到当前顺序值。
     - 将当前顺序的测试用例插入到 `sorted_list` 的中间位置。
     - 更新 `index` 值，表示已排序的测试用例数量。

6. **添加未排序项**：
   - `sorted_list[mid_index:mid_index] = self.unordered_items`：将未排序的测试用例添加到排序列表的末尾。

7. **返回排序后的列表**：
   - `return sorted_list`：返回排序后的测试用例列表。

#### print_unhandled_items方法

`print_unhandled_items` 方法用于处理和报告未处理的相对标记（`relative marks`），有助于调试和理解测试用例的执行顺序，特别是在处理复杂的依赖关系时。

逻辑大致如下：

1. **构建消息内容**：
   - `msg = " ".join([...])`：通过 `join` 方法将字符串列表连接成一个单独的字符串，每个字符串之间用空格分隔。
   - `(mark.item.node_id for mark in self.rel_marks)`：生成一个迭代器，包含所有相对标记（`RelativeMark` 对象）中的 `item` 的 `node_id`。
   - `(mark.item.node_id for mark in self.dep_marks)`：类似地，生成一个迭代器，包含所有依赖标记中的 `item` 的 `node_id`。

2. **检查消息是否非空**：
   - `if msg:`：如果 `msg` 字符串非空（即存在未处理的标记），则执行以下操作。

3. **输出警告信息**：
   - `sys.stdout.write("\nWARNING: cannot execute test relative to others: ")`：使用 `sys.stdout.write` 输出警告消息的开头部分。
   - `sys.stdout.write(msg)`：输出未处理的测试用例的 `node_id`。
   - `sys.stdout.write(" - ignoring the marker.\n")`：输出警告消息的结尾部分，提示这些标记将被忽略。
   - `sys.stdout.flush()`：刷新标准输出缓冲区，确保警告信息立即显示。

**注意事项：**

- **输出警告**：这个方法仅在存在未处理的相对标记时输出警告信息。如果没有未处理的标记，它不会输出任何内容。
- **即时显示**：通过 `sys.stdout.flush()` 确保警告信息立即显示在控制台上，而不是等待缓冲区自动刷新。


#### number_of_rel_groups方法

此方法用于计算测试用例中相对标记的数量，返回值：int，相对标记组的总数。

```python
    def number_of_rel_groups(self) -> int:
        return len(self.rel_marks) + len(self.dep_marks)
```

这个方法返回 `self.rel_marks`（相对标记列表）和 `self.dep_marks`（依赖标记列表）的长度之和。这些标记用来定义测试用例之间的相对执行顺序。


#### handle_rel_marks方法

此方法处理相对标记。

```python
    def handle_rel_marks(self, sorted_list: List[Item]) -> None:
        self.handle_relative_marks(self.rel_marks, sorted_list, self.all_rel_marks)
```

调用 `handle_relative_marks` 静态方法，传入 `self.rel_marks`（相对标记列表）、`sorted_list`（已排序的测试用例列表）和 `self.all_rel_marks`（所有相对标记列表）。


#### handle_dep_marks方法

此方法处理依赖标记。

```python
    def handle_dep_marks(self, sorted_list: List[Item]) -> None:
        self.handle_relative_marks(self.dep_marks, sorted_list, self.all_dep_marks)
```

这个方法调用` handle_relative_marks` 静态方法，传入 `self.dep_marks`（依赖标记列表）、`sorted_list`（已排序的测试用例列表）和 `self.all_dep_marks`（所有依赖标记列表）。


#### handle_relative_marks方法

`handle_relative_marks`方法用于处理相对标记，确保测试用例按照这些相对关系进行排序，它通过调整测试用例在 `sorted_list` 中的位置来实现这一点。

```python
    @staticmethod
    def handle_relative_marks(
        marks: List["RelativeMark[Item]"],
        sorted_list: List[Item],
        all_marks: List["RelativeMark[Item]"],
    ) -> None:
        for mark in reversed(marks):
            if move_item(mark, sorted_list):
                marks.remove(mark)
                all_marks.remove(mark)
```

逻辑解读如下：

- 遍历 `marks` 列表的逆序列（从最后一个标记开始）。
- 对于每个标记，调用 `move_item` 方法尝试根据相对标记调整 `sorted_list` 中测试用例的顺序。
- 如果 `move_item` 返回 `True`，表示标记被成功处理：
    从 `marks` 列表中移除该标记。
    从 `all_marks` 列表中移除该标记。



#### group_order方法

这个方法用于确定测试用例组的顺序值，基于组内测试用例的相对顺序标记，即确定测试用例组的整体顺序，这在处理多个测试用例需要按特定顺序执行时非常有用。

```python
    def group_order(self) -> Optional[int]:
        if self.start_items:
            return self.start_items[0][0]
        elif self.end_items:
            return self.end_items[-1][0]
        return None
```


逻辑解读如下：

- 检查 `self.start_items`（起始项列表）：
  如果存在起始项，返回第一个起始项的顺序值。
- 检查 `self.end_items`（结束项列表）：
  如果存在结束项，返回最后一个结束项的顺序值。
- 如果两者都不存在，返回 `None`。


### ItemGroup 类

```python
class ItemGroup:
    """
    Holds a group of sorted items with the same group order scope.
    Used for sorting groups similar to Item for sorting items.
    """

    def __init__(
        self, items: Optional[List[Item]] = None, order: Optional[int] = None
    ) -> None:
        self.items: List[Item] = items or []
        self.order = order
        self.nr_rel_items = 0

    def inc_rel_marks(self) -> None:
        if self.order is None:
            self.nr_rel_items += 1

    def dec_rel_marks(self) -> None:
        if self.order is None:
            self.nr_rel_items -= 1

    def extend(self, groups: List["ItemGroup"], order: Optional[int]) -> None:
        for group in groups:
            self.items.extend(group.items)
        self.order = order
```
`ItemGroup`类用于处理具有相同分组顺序范围的一组项目。主要方法与属性有:

- `__init__`: 初始化方法，接受一组项目及其顺序。
- `inc_rel_marks`: 增加相关项目数量。
- `dec_rel_marks`: 减少相关项目数量。
- `extend`: 扩展项目组。

`ItemGroup` 类用于以下目的：

* 分组：将具有相同顺序范围的测试用例组合在一起。
* 顺序管理：通过 `order` 属性管理组的整体执行顺序。
* 相对标记计数：通过 `nr_rel_items` 属性跟踪组内未标记顺序的测试用例数量，这有助于在处理相对顺序时做出决策。

#### 类定义和初始化

```python
class ItemGroup:
    """
    Holds a group of sorted items with the same group order scope.
    Used for sorting groups similar to Item for sorting items.
    """
    def __init__(
        self, items: Optional[List[Item]] = None, order: Optional[int] = None
    ) -> None:
        self.items: List[Item] = items or []
        self.order = order
        self.nr_rel_items = 0
```

- **`__init__` 方法**：类的构造函数，用于初始化 `ItemGroup` 实例。
  - **参数**：
    - `items`：`Optional[List[Item]]`，一个可选的测试用例列表。如果未提供，则默认为空列表。
    - `order`：`Optional[int]`，一个可选的整数，表示组的顺序。如果未提供，则默认为 `None`。
  - **属性**：
    - `self.items`：存储属于该组的测试用例列表。
    - `self.order`：存储该组的顺序值。
    - `self.nr_rel_items`：存储该组中未标记顺序的测试用例数量。

#### 方法

- **`inc_rel_marks` 方法**：

  ```python
  def inc_rel_marks(self) -> None:
      if self.order is None:
          self.nr_rel_items += 1
  ```
  - **功能**：增加未标记顺序的测试用例计数。
  - **参数**：无
  - **返回值**：无（`None`）
  - **逻辑**：如果组的顺序 `self.order` 为 `None`，则增加 `self.nr_rel_items` 的值。

- **`dec_rel_marks` 方法**：

  ```python
  def dec_rel_marks(self) -> None:
      if self.order is None:
          self.nr_rel_items -= 1
  ```
  - **功能**：减少未标记顺序的测试用例计数。
  - **参数**：无
  - **返回值**：无（`None`）
  - **逻辑**：如果组的顺序 `self.order` 为 `None`，则减少 `self.nr_rel_items` 的值。

- **`extend` 方法**：

  ```python
  def extend(self, groups: List["ItemGroup"], order: Optional[int]) -> None:
      for group in groups:
          self.items.extend(group.items)
      self.order = order
  ```
  - **功能**：扩展当前组，包含其他组的测试用例。
  - **参数**：
    - `groups`：`List[ItemGroup]`，要合并的组列表。
    - `order`：`Optional[int]`，新的顺序值，用于更新当前组的顺序。
  - **返回值**：无（`None`）
  - **逻辑**：
    - 遍历 `groups` 列表，将每个组的测试用例列表扩展到当前组的 `self.items` 中。
    - 更新当前组的顺序值为传入的 `order`。


### RelativeMark 类

`RelativeMark` 类代表标记项或项组，并处理两个相关项或组及其关系。此外，函数 `filter_marks` 与 `move_item`，是 `pytest-order` 插件中用于处理测试用例相对顺序的核心部分。

#### RelativeMark 类

```python
class RelativeMark(Generic[_ItemType]):
    """
    Represents a marker for an item or an item group.
    Holds two related items or groups and their relationship.
    """

    def __init__(
        self,
        item: _ItemType,
        item_to_move: _ItemType,
        move_after: bool,
    ) -> None:
        self.item: _ItemType = item
        self.item_to_move: _ItemType = item_to_move
        self.move_after: bool = move_after
```

- **功能**：表示一个测试用例或测试用例组的相对标记。
- **参数**：
  - `item`：`_ItemType`，被标记的测试用例或组。
  - `item_to_move`：`_ItemType`，需要移动的测试用例或组。
  - `move_after`：`bool`，一个布尔值，指示 `item_to_move` 是否应该移动到 `item` 之后。
- **属性**：
  - `self.item`：存储被标记的测试用例或组。
  - `self.item_to_move`：存储需要移动的测试用例或组。
  - `self.move_after`：指示移动方向。

#### filter_marks 函数

```python
def filter_marks(
    marks: List[RelativeMark[_ItemType]], all_items: List[Item]
) -> List[RelativeMark[_ItemType]]:
    result = []
    for mark in marks:
        if mark.item in all_items and mark.item_to_move in all_items:
            result.append(mark)
        else:
            mark.item_to_move.dec_rel_marks()
    return result
```

- **功能**：过滤相对标记，确保标记中的测试用例或组都存在于 `all_items` 列表中。
- **参数**：
  - `marks`：`List[RelativeMark[_ItemType]]`，相对标记列表。
  - `all_items`：`List[Item]`，所有测试用例的列表。
- **返回值**：`List[RelativeMark[_ItemType]]`，过滤后的相对标记列表。
- **逻辑**：
  - 遍历 `marks` 列表。
  - 如果标记中的 `item` 和 `item_to_move` 都在 `all_items` 中，则将该标记添加到结果列表 `result`。
  - 如果 `item_to_move` 不在 `all_items` 中，则调用 `dec_rel_marks` 方法减少其相对标记计数。

#### move_item 函数

```python
def move_item(mark: RelativeMark[_ItemType], sorted_items: List[_ItemType]) -> bool:
    if (
        mark.item not in sorted_items
        or mark.item_to_move not in sorted_items
        or mark.item.nr_rel_items
    ):
        return False
    pos_item = sorted_items.index(mark.item)
    pos_item_to_move = sorted_items.index(mark.item_to_move)
    if mark.item_to_move.order is not None and mark.item.order is None:
        # if the item to be moved has already been ordered numerically,
        # and the other item is not ordered, we move that one instead
        mark.move_after = not mark.move_after
        mark.item, mark.item_to_move = mark.item_to_move, mark.item
        pos_item, pos_item_to_move = pos_item_to_move, pos_item
    mark.item_to_move.dec_rel_marks()
    if mark.move_after:
        if pos_item_to_move < pos_item + 1:
            del sorted_items[pos_item_to_move]
            sorted_items.insert(pos_item, mark.item_to_move)
    else:
        if pos_item_to_move > pos_item:
            del sorted_items[pos_item_to_move]
            pos_item -= 1
            sorted_items.insert(pos_item + 1, mark.item_to_move)
    return True
```

- **功能**：根据相对标记调整测试用例在已排序列表中的位置。
- **参数**：
  - `mark`：`RelativeMark[_ItemType]`，相对标记。
  - `sorted_items`：`List[_ItemType]`，已排序的测试用例或组列表。
- **返回值**：`bool`，指示是否成功移动了测试用例。
- **逻辑**：
  - 检查 `mark.item` 和 `mark.item_to_move` 是否都在 `sorted_items` 中，如果不在或 `mark.item` 有多个相对标记，则返回 `False`。
  - 获取 `mark.item` 和 `mark.item_to_move` 在 `sorted_items` 中的位置。
  - 如果 `mark.item_to_move` 已经有顺序，而 `mark.item` 没有，则交换 `item` 和 `item_to_move`，并更新移动方向。
  - 调用 `dec_rel_marks` 方法减少 `mark.item_to_move` 的相对标记计数。
  - 根据移动方向 `mark.move_after` 调整 `sorted_items` 中的位置。

#### 其他说明

- **相对标记**：`RelativeMark` 类用于定义测试用例或组之间的相对执行顺序。
- **过滤标记**：`filter_marks` 函数确保所有标记的测试用例或组都存在于测试用例列表中，否则减少其相对标记计数。
- **移动测试用例**：`move_item` 函数根据相对标记调整测试用例在排序列表中的位置，确保相对顺序被尊重。

这些功能共同确保测试用例不仅按照它们的绝对顺序执行，而且也尊重它们之间的相对顺序关系。这对于测试用例之间存在依赖关系或特定执行顺序要求的场景非常重要。


## 文件plugin.py

### pytest_configure 函数

```python
def pytest_configure(config: Config) -> None:
    """
    Register the "order" marker and configure the plugin,
    depending on the CLI options.
    """
    provided_by_pytest_order = (
        "Provided by pytest-order. " "See also: https://pytest-order.readthedocs.io/"
    )

    config_line = (
        "order: specify ordering information for when tests should run "
        "in relation to one another. " + provided_by_pytest_order
    )
    config.addinivalue_line("markers", config_line)

    if config.getoption("indulgent_ordering"):
        wrapper = pytest.hookimpl(tryfirst=True)
    else:
        wrapper = pytest.hookimpl(trylast=True)
    OrderingPlugin.pytest_collection_modifyitems = wrapper(  # type:ignore[attr-defined]
        modify_items
    )
    config.pluginmanager.register(OrderingPlugin(), "orderingplugin")
```

- **功能**：在 `pytest` 配置阶段注册 "order" 标记，并根据命令行选项配置插件。
- **参数**：
  - `config`：`Config`，`pytest` 的配置对象。
- **逻辑**：
  - 向配置文件中添加 "order" 标记的说明。
  - 根据是否设置了 `--indulgent-ordering` 选项，决定 `modify_items` 函数的执行顺序（`tryfirst` 或 `trylast`）。
  - 注册 `OrderingPlugin` 插件。

### pytest_addoption 函数

```python
def pytest_addoption(parser: Parser) -> None:
    """Set up CLI option for pytest"""
    group = parser.getgroup("order")
    group.addoption(
        "--indulgent-ordering",
        action="store_true",
        dest="indulgent_ordering",
        help=(
            "Request that the sort order provided by pytest-order be applied "
            "before other sorting, allowing the other sorting to have priority"
        ),
    )
    group.addoption(
        "--order-scope",
        action="store",
        dest="order_scope",
        help=(
            "Defines the scope used for ordering. Possible values are: "
            "'session' (default), 'module', and 'class'. "
            "Ordering is only done inside a scope."
        ),
    )
    group.addoption(
        "--order-scope-level",
        action="store",
        type=int,
        dest="order_scope_level",
        help=(
            "Defines that the given directory level is used as order scope. "
            "Cannot be used with --order-scope. The value is a number "
            "that defines the hierarchical index of the directories used as "
            "order scope, starting with 0 at session scope."
        ),
    )
    group.addoption(
        "--order-group-scope",
        action="store",
        dest="order_group_scope",
        help=(
            "Defines the scope used for order groups. Possible values are: "
            " 'session' (default), 'module', and 'class'. "
            "Ordering is first done inside a group, then between groups."
        ),
    )
    group.addoption(
        "--sparse-ordering",
        action="store_true",
        dest="sparse_ordering",
        help=(
            "If there are gaps between ordinals, they are filled "
            "with unordered tests."
        ),
    )
    group.addoption(
        "--order-dependencies",
        action="store_true",
        dest="order_dependencies",
        help=(
            "If set, dependencies added by pytest-dependency will be ordered "
            "if needed."
        ),
    )
    group.addoption(
        "--order-marker-prefix",
        action="store",
        dest="order_marker_prefix",
        help=(
            "If set, markers starting with the given prefix followed by a number "
            "are handled like order markers with an index."
        ),
    )
```

- **功能**：为 `pytest` 设置命令行选项。
- **参数**：
  - `parser`：`Parser`，`pytest` 的命令行参数解析器。
- **逻辑**：
  - 创建一个名为 "order" 的参数组。
  - 添加多个选项，允许用户控制测试用例的执行顺序和相关行为。

### _get_mark_description 函数

```python
def _get_mark_description(mark: Mark):
    if mark.kwargs:
        return ", ".join([f"{k}={v}" for k, v in mark.kwargs.items()])
    elif mark.args:
        return f"index={mark.args[0]}"
    return mark
```

- **功能**：获取标记的描述。
- **参数**：
  - `mark`：`Mark`，`pytest` 的标记对象。
- **返回值**：`str`，标记的描述。

### pytest_generate_tests 函数

```python
def pytest_generate_tests(metafunc):
    """
    Handle multiple pytest.mark.order decorators.

    Make parametrized tests with corresponding order marks.
    """
    if getattr(metafunc, "function", False):
        if getattr(metafunc.function, "pytestmark", False):
            # Get list of order marks
            marks = metafunc.function.pytestmark
            order_marks = [mark for mark in marks if mark.name == "order"]
            if len(order_marks) > 1:
                # Remove all order marks
                metafunc.function.pytestmark = [
                    mark for mark in marks if mark.name != "order"
                ]
                # Prepare arguments for parametrization with order marks
                args = [
                    pytest.param(_get_mark_description(mark), marks=[mark])
                    for mark in order_marks
                ]
                if "order" not in metafunc.fixturenames:
                    metafunc.fixturenames.append("order")
                metafunc.parametrize("order", args)
```

- **功能**：处理多个 `pytest.mark.order` 装饰器，并生成相应的参数化测试。
- **参数**：
  - `metafunc`：`Metafunc`，`pytest` 的元函数对象。
- **逻辑**：
  - 获取函数的所有标记。
  - 筛选出所有的 "order" 标记。
  - 如果有多个 "order" 标记，将它们参数化，并生成相应的测试用例。

### OrderingPlugin 类

```python
class OrderingPlugin:
    """
    Plugin implementation.

    By putting this in a class, we are able to dynamically register it after
    the CLI is parsed.
    """
```

- **功能**：插件实现。
- **说明**：通过将插件实现放在类中，可以在命令行解析后动态注册它。

### modify_items 函数

```python
def modify_items(session: Session, config: Config, items: List[Function]) -> None:
    sorter = Sorter(config, items)
    items[:] = sorter.sort_items()
```

- **功能**：修改项目列表，根据指定的顺序对测试用例进行排序。
- **参数**：
  - `session`：`Session`，`pytest` 的会话对象。
  - `config`：`Config`，`pytest` 的配置对象。
  - `items`：`List[Function]`，测试用例列表。
- **逻辑**：
  - 创建一个 `Sorter` 对象，传入配置和测试用例列表。
  - 使用 `Sorter` 对象的 `sort_items` 方法对测试用例进行排序，并更新 `items` 列表。

### 功能解释

这些函数和类共同实现了 `pytest-order` 插件的核心功能：
- **命令行选项**：允许用户通过命令行选项控制测试用例的执行顺序。
- **标记处理**：处理 `pytest.mark.order` 装饰器，支持参数化测试。
- **排序**：根据用户指定的顺序对测试用例进行排序。

通过这些功能，`pytest-order` 插件能够灵活地控制测试用例的执行顺序，满足不同的测试需求。


## 文件settings.py

这段代码定义了 `pytest-order` 插件的配置设置，主要用于处理命令行选项和配置文件中的设置，并提供这些设置的访问。

### Scope 枚举类

```python
from enum import Enum

class Scope(Enum):
    CLASS = 1
    MODULE = 2
    SESSION = 3
```

- **功能**：定义了三个枚举值，分别表示测试用例的执行范围。
  - `CLASS`：类级别。
  - `MODULE`：模块级别。
  - `SESSION`：会话级别。

### Settings 类

```python
class Settings:
    """Holds all configuration settings."""
    valid_scopes = {
        "class": Scope.CLASS,
        "module": Scope.MODULE,
        "session": Scope.SESSION,
    }

    def __init__(self, config: Config) -> None:
        self.sparse_ordering: bool = config.getoption("sparse_ordering")
        self.order_dependencies: bool = config.getoption("order_dependencies")
        self.marker_prefix: str = config.getoption("order_marker_prefix")
        scope: str = config.getoption("order_scope")
        if scope in self.valid_scopes:
            self.scope: Scope = self.valid_scopes[scope]
        else:
            if scope is not None:
                warn(
                    "Unknown order scope '{}', ignoring it. "
                    "Valid scopes are 'session', 'module' and 'class'.".format(scope)
                )
            self.scope = Scope.SESSION
        scope_level: int = config.getoption("order_scope_level") or 0
        if scope_level != 0 and self.scope != Scope.SESSION:
            warn(
                "order-scope-level cannot be used together with "
                "--order-scope={}".format(scope)
            )
            scope_level = 0
        self.scope_level: int = scope_level
        group_scope: str = config.getoption("order_group_scope")
        if group_scope in self.valid_scopes:
            self.group_scope: Scope = self.valid_scopes[group_scope]
        else:
            if group_scope is not None:
                warn(
                    "Unknown order group scope '{}', ignoring it. "
                    "Valid scopes are 'session', 'module' and 'class'.".format(
                        group_scope
                    )
                )
            self.group_scope = self.scope
        if self.group_scope.value > self.scope.value:
            warn("Group scope is larger than order scope, ignoring it.")
            self.group_scope = self.scope
        try:
            auto_mark_dep = config.getini("automark_dependency")
            if isinstance(auto_mark_dep, str):
                auto_mark_dep = auto_mark_dep.lower() in (
                    "1",
                    "yes",
                    "y",
                    "true",
                    "t",
                    "on",
                )
        except ValueError:
            auto_mark_dep = False
        self.auto_mark_dep = auto_mark_dep
```

- **功能**：存储所有配置设置。
- **参数**：
  - `config`：`Config`，`pytest` 的配置对象。
- **属性**：
  - `self.sparse_ordering`：布尔值，表示是否启用稀疏排序。
  - `self.order_dependencies`：布尔值，表示是否排序依赖项。
  - `self.marker_prefix`：字符串，表示标记前缀。
  - `self.scope`：`Scope` 枚举值，表示排序的执行范围。
  - `self.scope_level`：整数，表示执行范围的层级。
  - `self.group_scope`：`Scope` 枚举值，表示组排序的执行范围。
  - `self.auto_mark_dep`：布尔值，表示是否自动标记依赖项。

**逻辑**：
1. **初始化**：从配置对象中获取相关选项，并进行相应的处理。
2. **范围验证**：验证 `order_scope` 和 `order_group_scope` 是否有效，如果无效则使用默认值。
3. **范围层级**：处理 `order_scope_level`，但只有在 `scope` 为 `SESSION` 时才有效。
4. **依赖项自动标记**：处理 `automark_dependency` 配置项，决定是否自动标记依赖项。

### 功能解释

- **配置读取**：从 `pytest` 配置中读取相关选项，如排序、依赖项处理等。
- **范围处理**：处理测试用例执行的范围和组排序的范围，确保它们是有效的枚举值。
- **警告**：如果配置项无效或存在冲突，发出警告并使用默认值。

这些设置使得 `pytest-order` 插件能够根据用户的需求灵活地控制测试用例的执行顺序和相关行为。


## 文件sorter.py

### sort_items方法

它负责对测试用例进行排序并返回排序后的测试用例列表。

#### 方法参数和返回值

- **参数**：无
- **返回值**：`List[Function]`，排序后的测试用例列表

#### 方法逻辑

1. **收集标记**：
   - `self.collect_markers()`：收集测试用例的标记，包括顺序标记和依赖标记。

2. **根据作用域进行排序**：
   - 根据配置文件中指定的作用域（会话、模块、类），对测试用例进行分组和排序。

3. **会话作用域**：
   - 如果 `self.settings.scope` 是 `Scope.SESSION`：
     - 检查 `self.settings.scope_level` 是否大于0：
       - 如果是，调用 `directory_item_groups` 函数将测试用例按目录层级分组。
       - 遍历每个分组，创建 `ScopeSorter` 实例对每个分组内的测试用例进行排序，并将排序后的结果添加到 `sorted_list`。
     - 如果不是，创建一个 `ScopeSorter` 实例（指定会话作用域），并调用其 `sort_items` 方法对所有测试用例进行排序。

4. **模块作用域**：
   - 如果 `self.settings.scope` 是 `Scope.MODULE`：
     - 调用 `module_item_groups` 函数将测试用例按模块分组。
     - 遍历每个模块分组，创建 `ScopeSorter` 实例对每个模块内的测试用例进行排序，并将排序后的结果添加到 `sorted_list`。

5. **类作用域**：
   - 如果 `self.settings.scope` 是其他值（默认为类作用域）：
     - 调用 `class_item_groups` 函数将测试用例按类分组。
     - 遍历每个类分组，创建 `ScopeSorter` 实例对每个类内的测试用例进行排序，并将排序后的结果添加到 `sorted_list`。

6. **返回排序后的测试用例列表**：
   - `return [item.item for item in sorted_list]`：从排序后的 `Item` 对象列表中提取测试用例（`Function` 对象），并返回。

### mark_binning方法

`mark_binning` 和 `handle_dependency_mark`这两个方法负责处理测试用例的标记，特别是与依赖和顺序相关的标记。

```python
def mark_binning(
    self,
    item: Item,
    dep_marks: Dict[Tuple[str, Scope, str], List[Item]],
    aliases: Dict[str, List[Item]],
) -> None:
    """
    Collect relevant markers for the given item.
    """
    keys = item.item.keywords.keys()
    has_dependency = "dependency" in keys
    has_order = "order" in keys
    if not has_order and self.settings.marker_prefix:
        for key in keys:
            if key.startswith(self.settings.marker_prefix):
                try:
                    index = int(key[len(self.settings.marker_prefix)])
                    item.order = index
                except ValueError:
                    pass
    if has_dependency or self.settings.auto_mark_dep:
        self.handle_dependency_mark(item, has_order, dep_marks, aliases)
    if has_order:
        self.handle_order_marks(item)
```

- **参数**：
  - `item`：`Item` 对象，代表单个测试用例。
  - `dep_marks`：依赖标记的字典，键是依赖项的名称、作用域和前缀的元组，值是依赖该项的测试用例列表。
  - `aliases`：别名字典，存储测试用例的别名和对应的测试用例列表。

- **功能**：
  - 收集与给定测试用例相关的标记。
  - 检查是否有 `dependency` 或 `order` 标记。
  - 如果没有 `order` 标记但设置了标记前缀，则尝试将其他标记转换为顺序索引。
  - 处理依赖标记。
  - 处理顺序标记。

### handle_dependency_mark 方法

```python
def handle_dependency_mark(
    self,
    item: Item,
    has_order: bool,
    dep_marks: Dict[Tuple[str, Scope, str], List[Item]],
    aliases: Dict[str, List[Item]],
) -> None:
    # always order dependencies if an order mark is present
    # otherwise only if order-dependencies is set
    mark = item.item.get_closest_marker("dependency")
    name_mark = None
    if mark and (self.settings.order_dependencies or has_order):
        dependent_mark = mark.kwargs.get("depends")
        if dependent_mark:
            scope = scope_from_name(mark.kwargs.get("scope", "module"))
            prefix = scoped_node_id(item.node_id, scope)
            for name in dependent_mark:
                dep_marks.setdefault((name, scope, prefix), []).append(item)
                item.inc_rel_marks()
        # we always collect the names of the dependent items, because
        # we need them in both cases
        name_mark = mark.kwargs.get("name")
    # the default name in pytest-dependency is the nodeid or a part
    # of the nodeid, depending on the scope
    if not name_mark:
        name_mark = item.node_id
    aliases.setdefault(name_mark, []).append(item)
```

- **参数**：
  - `item`：`Item` 对象，代表单个测试用例。
  - `has_order`：布尔值，指示是否有顺序标记。
  - `dep_marks`：依赖标记的字典。
  - `aliases`：别名字典。

- **功能**：
  - 处理依赖标记。
  - 获取 `dependency` 标记，并根据其依赖项设置依赖标记。
  - 如果标记存在且 `order_dependencies` 设置为 `True` 或存在顺序标记，则处理依赖项。
  - 获取依赖项的作用域和前缀，并为每个依赖项名称创建依赖标记。
  - 更新别名字典，存储测试用例的别名和对应的测试用例列表。

#### 代码逻辑

1. **收集标记**：
   - `mark_binning` 方法首先检查测试用例是否有 `dependency` 或 `order` 标记。
   - 如果没有 `order` 标记但设置了标记前缀，则尝试将其他标记转换为顺序索引。

2. **处理依赖标记**：
   - `handle_dependency_mark` 方法处理 `dependency` 标记。
   - 获取 `dependency` 标记的参数，如依赖项名称和作用域。
   - 为每个依赖项名称创建依赖标记，并将其添加到 `dep_marks` 字典中。
   - 更新测试用例的相对标记计数。

3. **更新别名字典**：
   - 如果 `dependency` 标记中没有提供名称，则使用测试用例的节点 ID 作为名称。
   - 将测试用例添加到别名字典中，以便后续处理。

### handle_order_marks 方法

`handle_order_marks` 和 `handle_order_mark`，这些方法负责处理 `order` 标记，这些标记用于指定测试用例的执行顺序。

```python
def handle_order_marks(self, item: Item) -> None:
    marks = item.item.iter_markers("order")
    for mark in marks:
        self.handle_order_mark(item, mark)
```

- **参数**：
  - `item`：`Item` 对象，代表单个测试用例。

- **功能**：
  - 获取测试用例上所有的 `order` 标记。
  - 对每个 `order` 标记调用 `handle_order_mark` 方法进行处理。

### handle_order_mark 方法

```python
def handle_order_mark(self, item: Item, mark: Mark) -> None:
    order = mark.args[0] if mark.args else mark.kwargs.get("index")
    if order is not None:
        if isinstance(order, int):
            order = int(order)
        elif order in orders_map:
            order = orders_map[order]
        else:
            warn("Unknown order attribute:'{}'".format(order))
            order = None
    if item.order is None:
        item.order = order
    self.handle_relative_marks(item, mark)
    if order is not None:
        item.nr_rel_items = 0
```

- **参数**：
  - `item`：`Item` 对象，代表单个测试用例。
  - `mark`：`Mark` 对象，代表 `order` 标记。

- **功能**：
  - 从 `order` 标记中提取顺序值。
  - 根据 `mark.args` 或 `mark.kwargs` 中的 `index` 获取顺序值。
  - 如果顺序值是整数，则直接使用。
  - 如果顺序值是字符串且在 `orders_map` 中定义，则将其转换为对应的整数。
  - 如果顺序值未知，则发出警告并设置为 `None`。
  - 如果测试用例之前没有顺序值，则将其设置为当前的顺序值。
  - 调用 `handle_relative_marks` 方法处理相关的相对标记。
  - 如果设置了顺序值，则将测试用例的相对标记计数器重置为0。

详细解读内容如下：

1. **获取 `order` 标记**：
   - `marks = item.item.iter_markers("order")`：获取测试用例上所有的 `order` 标记。

2. **处理每个 `order` 标记**：
   - 遍历每个 `order` 标记，调用 `handle_order_mark` 方法。

3. **提取顺序值**：
   - `order = mark.args[0] if mark.args else mark.kwargs.get("index")`：从标记的参数或关键字参数中获取顺序值。

4. **验证和转换顺序值**：
   - 如果顺序值是整数，则直接使用。
   - 如果顺序值是字符串，则检查是否在 `orders_map` 中定义，如果是，则转换为对应的整数。
   - 如果顺序值未知，则发出警告并将其设置为 `None`。

5. **设置测试用例的顺序值**：
   - 如果测试用例之前没有顺序值，则将其设置为当前的顺序值。

6. **处理相对标记**：
   - `self.handle_relative_marks(item, mark)`：处理测试用例上的相对标记，如 `before` 和 `after`。

7. **重置相对标记计数器**：
   - 如果设置了顺序值，则将测试用例的相对标记计数器 `item.nr_rel_items` 重置为0。这表示该测试用例已经有了明确的顺序，不需要进一步的相对标记处理。

### items_from_label 方法

`items_from_label` 方法用于根据给定的标签（`label`）查找匹配的测试用例项（`Item`），处理测试用例相对顺序标记的关键部分，确保测试用例能够根据指定的顺序执行。

```python
def items_from_label(self, label: str, item: Item, is_cls_mark: bool) -> List[Item]:
    """
    Return the list of matching items from the given label.
    The list contains one item for a single matching test, several items
    in the case of a matching parametrized test, or no item in case of
    an invalid label.
    """
    item_id = item.node_id
    label_len = len(label)
    last_comp = label.split("/")[-1].split("::")[-1]
    items = []
    with suppress(KeyError):
        node_ids = self.node_id_last[last_comp]
        for node_id in node_ids:
            if node_id.endswith(label):
                id_start = node_id[:-label_len]
            elif node_id.endswith("]") and node_id.rpartition("[")[0].endswith(
                label
            ):
                id_start = node_id.rpartition("[")[0][:-label_len]
            else:
                continue
            if is_cls_mark and id_start.count("::") == 2:
                continue
            if item_id.startswith(id_start):
                items.append(self.node_ids[node_id])

    return items
```

#### 方法参数

- `label`：`str`，要匹配的标签。
- `item`：`Item` 对象，当前正在处理的测试用例。
- `is_cls_mark`：`bool`，指示标记是否应用于类级别。

#### 方法返回值

- 返回类型：`List[Item]`，匹配的测试用例项列表。

#### 方法逻辑

1. **初始化变量**：
   - `item_id`：获取当前测试用例的节点 ID。
   - `label_len`：计算标签的长度。
   - `last_comp`：获取标签的最后一部分，这通常是测试用例的名称或部分路径。

2. **初始化结果列表**：
   - `items`：创建一个空列表，用于存储匹配的测试用例项。

3. **处理标签匹配**：
   - 使用 `with suppress(KeyError)` 确保即使 `last_comp` 不存在于 `node_id_last` 字典中也不会抛出异常。
   - 获取与 `last_comp` 相关的所有节点 ID（`node_ids`）。

4. **遍历节点 ID**：
   - 遍历 `node_ids` 中的每个节点 ID。
   - 检查节点 ID 是否以标签结束：
     - 如果是，计算 `id_start` 为节点 ID 减去标签长度。
     - 如果节点 ID 以 "[" 结尾，并且 "[" 之前的部分以标签结束，则从 "[" 之前的部分计算 `id_start`。
   - 如果 `is_cls_mark` 为 `True` 并且 `id_start` 包含两个 `"::"`，则跳过当前节点 ID（只匹配类级别的标记）。
   - 如果当前测试用例的节点 ID（`item_id`）以 `id_start` 开始，则将匹配的测试用例项添加到 `items` 列表中。

5. **返回结果**：
   - 返回包含所有匹配测试用例项的列表。

概况下来就是：

- **标签匹配**：该方法通过标签匹配测试用例，支持精确匹配和部分匹配。
- **参数化测试**：如果标签匹配到多个测试用例（例如参数化测试），则所有匹配的测试用例都会被添加到结果列表中。
- **类级别标记**：如果 `is_cls_mark` 为 `True`，则仅匹配类级别的测试用例。


### items_from_class_label 方法

`items_from_class_label` 方法用于根据类标签查找匹配的测试用例项（`Item`）。

```python
def items_from_class_label(self, label: str, item: Item) -> List[Item]:
    items = []
    item_id = item.node_id
    label_len = len(label)
    for node_id in self.node_ids:
        if node_id.count("::") == 2:
            cls_index = node_id.rindex("::")
            if node_id[:cls_index].endswith(label):
                id_start = node_id[: cls_index - label_len]
                if item_id.startswith(id_start):
                    items.append(self.node_ids[node_id])
    return items
```

#### 方法参数

- `label`：`str`，要匹配的类标签。
- `item`：`Item` 对象，当前正在处理的测试用例。

#### 方法返回值

- 返回类型：`List[Item]`，匹配的测试用例项列表。

#### 方法逻辑

1. **初始化结果列表**：
   - `items`：创建一个空列表，用于存储匹配的测试用例项。

2. **获取当前测试用例的节点 ID**：
   - `item_id`：获取当前测试用例的节点 ID。

3. **计算标签长度**：
   - `label_len`：计算标签的长度。

4. **遍历所有测试用例的节点 ID**：
   - 遍历 `self.node_ids` 字典中的所有节点 ID。

5. **检查节点 ID 是否匹配类标签**：
   - 对于每个节点 ID，检查其是否包含两个 `"::"`，这通常表示它是一个类级别的测试用例。
   - 获取类名称的结束索引 `cls_index`。
   - 检查节点 ID 的前 `cls_index` 部分是否以标签结束：
     - 如果是，计算 `id_start` 为节点 ID 的前 `cls_index - label_len` 部分。
     - 如果当前测试用例的节点 ID（`item_id`）以 `id_start` 开始，则将匹配的测试用例项添加到 `items` 列表中。

6. **返回结果**：
   - 返回包含所有匹配测试用例项的列表。

概括就是：

- **类标签匹配**：该方法通过类标签匹配测试用例，支持精确匹配类级别的测试用例。
- **节点 ID 分析**：通过分析节点 `ID` 来确定测试用例是否属于特定的类。
- **匹配添加**：将所有匹配的测试用例项添加到结果列表中。


### handle_before_or_after_mark 方法

`handle_before_or_after_mark` 方法用于处理测试用例上的 `before` 和 `after` 标记，这些标记定义了测试用例之间的相对执行顺序。

```python
def handle_before_or_after_mark(
    self, item: Item, mark: Mark, marker_name: str, is_after: bool
) -> bool:
    def is_class_mark() -> bool:
        if item.item.cls and item.item.parent:
            return item.item.parent.get_closest_marker("order") == mark
        return False

    def is_mark_for_class() -> bool:
        return "::" not in marker_name and is_class_mark()

    is_cls_mark = is_class_mark()
    items_for_label = self.items_from_label(marker_name, item, is_cls_mark)
    if items_for_label:
        for item_for_label in items_for_label:
            rel_mark = RelativeMark(item_for_label, item, move_after=is_after)
            if is_after or not is_cls_mark:
                self.rel_marks.append(rel_mark)
            else:
                self.rel_marks.insert(0, rel_mark)
            item.inc_rel_marks()
        return True
    else:
        if is_mark_for_class():
            items = self.items_from_class_label(marker_name, item)
            for item_for_label in items:
                rel_mark = RelativeMark(item_for_label, item, move_after=is_after)
                if is_after:
                    self.rel_marks.append(rel_mark)
                else:
                    self.rel_marks.insert(0, rel_mark)
                item.inc_rel_marks()
            return len(items) > 0
    return False
```

#### 方法参数

- `item`：`Item` 对象，当前正在处理的测试用例。
- `mark`：`Mark` 对象，包含 `order` 标记的详细信息。
- `marker_name`：`str`，要匹配的标记名称。
- `is_after`：`bool`，指示是否将当前测试用例放在标记指定的测试用例之后。

#### 方法返回值

- 返回类型：`bool`，指示是否成功处理了标记。

#### 方法逻辑

1. **辅助函数 `is_class_mark`**：
   - 检查 `item` 是否属于类级别的测试用例，并且其父级是否有 `order` 标记。
   - 如果是，则返回 `True`，表示标记应用于类级别。

2. **辅助函数 `is_mark_for_class`**：
   - 检查 `marker_name` 是否不包含 `"::"` 并且 `is_class_mark` 返回 `True`。
   - 如果是，则返回 `True`，表示标记应用于类级别。

3. **初始化变量**：
   - `is_cls_mark`：根据 `is_class_mark` 函数的结果初始化，表示标记是否应用于类级别。
   - `items_for_label`：通过调用 `items_from_label` 方法获取与 `marker_name` 匹配的测试用例列表。

4. **处理标签匹配的测试用例**：
   - 如果 `items_for_label` 不为空：
     - 遍历每个匹配的测试用例 `item_for_label`。
     - 创建 `RelativeMark` 对象，表示 `item_for_label` 和 `item` 之间的相对顺序关系。
     - 根据 `is_after` 的值，将 `RelativeMark` 对象添加到 `self.rel_marks` 列表的末尾或开头。
     - 增加 `item` 的相对标记计数。
     - 返回 `True`。

5. **处理类级别的标记**：
   - 如果 `is_mark_for_class` 返回 `True`：
     - 调用 `items_from_class_label` 方法获取与类标签匹配的测试用例列表。
     - 遍历每个匹配的测试用例 `item_for_label`。
     - 创建 `RelativeMark` 对象，表示 `item_for_label` 和 `item` 之间的相对顺序关系。
     - 根据 `is_after` 的值，将 `RelativeMark` 对象添加到 `self.rel_marks` 列表的末尾或开头。
     - 增加 `item` 的相对标记计数。
     - 返回匹配的测试用例数量大于0的结果。

6. **返回结果**：
   - 如果没有匹配的测试用例或类级别的标记，则返回 `False`。

概要的说就是：

- **相对标记处理**：该方法处理 `before` 和 `after` 标记，确定测试用例之间的相对执行顺序。
- **类级别标记**：特别处理类级别的标记，确保类级别的测试用例能够正确排序。
- **返回结果**：返回一个布尔值，指示是否成功处理了标记，这有助于调试和验证标记处理逻辑。



### handle_relative_marks 方法

`handle_relative_marks` 方法用于处理测试用例上的相对顺序标记，如 `before` 和 `after`。

这些标记定义了测试用例相对于其他测试用例的执行顺序。同时，通过警告机制（且看接下来的`warn_about_unknown_test`），插件能够提醒用户检查标记的使用，提高测试用例的可维护性。

```python
def handle_relative_marks(self, item: Item, mark: Mark) -> bool:
    has_relative_marks = False
    before_marks = mark.kwargs.get("before", ())
    if before_marks and not isinstance(before_marks, (list, tuple)):
        before_marks = (before_marks,)
    for before_mark in before_marks:
        if self.handle_before_or_after_mark(
            item, mark, before_mark, is_after=False
        ):
            has_relative_marks = True
        else:
            self.warn_about_unknown_test(item, before_mark)
    after_marks = mark.kwargs.get("after", ())
    if after_marks and not isinstance(after_marks, (list, tuple)):
        after_marks = (after_marks,)
    for after_mark in after_marks:
        if self.handle_before_or_after_mark(item, mark, after_mark, is_after=True):
            has_relative_marks = True
        else:
            self.warn_about_unknown_test(item, after_mark)
    return has_relative_marks
```

#### 功能解释

- **相对标记处理**：该方法处理 `before` 和 `after` 标记，确定测试用例相对于其他测试用例的执行顺序。
- **警告机制**：如果无法找到与标记名称匹配的测试用例，则发出警告，提示用户检查标记名称是否正确。
- **返回结果**：返回一个布尔值，指示是否成功处理了标记，这有助于调试和验证标记处理逻辑。


#### 方法参数

- `item`：`Item` 对象，当前正在处理的测试用例。
- `mark`：`Mark` 对象，包含 `order` 标记的详细信息。

#### 方法返回值

- 返回类型：`bool`，指示是否在测试用例上发现了相对标记。

#### 方法逻辑

1. **初始化变量**：
   - `has_relative_marks`：布尔值，用于指示是否发现了相对标记。

2. **处理 `before` 标记**：
   - 获取 `mark` 中的 `before` 关键字参数，默认为空元组 `()`。
   - 如果 `before_marks` 不是列表或元组类型，则将其转换为单元素元组。
   - 遍历 `before_marks` 中的每个标记名称：
     - 调用 `handle_before_or_after_mark` 方法，将当前测试用例 (`item`) 与 `before_mark` 进行比较，设置 `is_after=False`。
     - 如果 `handle_before_or_after_mark` 返回 `True`，表示成功处理了 `before` 标记，将 `has_relative_marks` 设置为 `True`。
     - 如果处理失败，则调用 `warn_about_unknown_test` 方法，发出警告。

3. **处理 `after` 标记**：
   - 获取 `mark` 中的 `after` 关键字参数，默认为空元组 `()`。
   - 如果 `after_marks` 不是列表或元组类型，则将其转换为单元素元组。
   - 遍历 `after_marks` 中的每个标记名称：
     - 调用 `handle_before_or_after_mark` 方法，将当前测试用例 (`item`) 与 `after_mark` 进行比较，设置 `is_after=True`。
     - 如果 `handle_before_or_after_mark` 返回 `True`，表示成功处理了 `after` 标记，将 `has_relative_marks` 设置为 `True`。
     - 如果处理失败，则调用 `warn_about_unknown_test` 方法，发出警告。

4. **返回结果**：
   - 返回 `has_relative_marks` 的值，表示是否在测试用例上发现了相对标记。

### warn_about_unknown_test 方法

静态方法 `warn_about_unknown_test`用于在无法识别或匹配测试用例的相对标记时发出警告。

```python
@staticmethod
def warn_about_unknown_test(item: Item, rel_mark: str) -> None:
    sys.stdout.write(
        "\nWARNING: cannot execute '{}' relative to others: "
        "'{}' - ignoring the marker.".format(item.item.name, rel_mark)
    )
```

#### 功能解释

- **警告机制**：当 `pytest-order` 插件在处理测试用例的相对顺序标记时，如果遇到无法识别的标记（例如，标记的测试用例不存在），则会调用这个方法输出警告信息。
- **直接输出**：通过 `sys.stdout.write` 直接输出警告信息，而不是使用 `print` 函数，这样可以避免额外的换行符和缓冲问题。

#### 方法参数

- `item`：`Item` 对象，当前正在处理的测试用例。
- `rel_mark`：`str`，无法识别的相对标记名称。

#### 方法返回值

- 返回类型：`None`，这个方法不返回任何值，而是直接输出警告信息。

#### 方法逻辑

1. **输出警告信息**：
   - 使用 `sys.stdout.write` 直接向标准输出写入警告信息。
   - 格式化字符串，包含当前测试用例的名称 (`item.item.name`) 和无法识别的相对标记名称 (`rel_mark`)。

2. **警告内容**：
   - 警告信息的格式为：
     ```
     WARNING: cannot execute '<test_name>' relative to others: '<rel_mark>' - ignoring the marker.
     ```
   - 其中 `<test_name>` 会被替换为当前测试用例的名称，`<rel_mark>` 会被替换为无法识别的相对标记名称。


#### 使用场景

这个方法通常在以下场景中被调用：

- 在 `handle_before_or_after_mark` 方法中，如果无法找到与 `before` 或 `after` 标记匹配的测试用例。
- 在 `handle_relative_marks` 方法中，处理 `before` 和 `after` 标记时，如果遇到无法识别的标记名称。

通过输出警告信息，插件提醒用户检查测试用例的相对顺序标记，确保所有标记都能正确识别和处理，从而避免测试执行顺序的混乱。

#### 注意事项

- 警告信息是直接输出到控制台的，不会被 `pytest` 的日志系统捕获，因此它们可能不会被一些日志收集工具记录。
- 这个方法不返回任何值，它的目的仅仅是为了通知用户存在未处理的标记。

### collect_markers 方法

`collect_markers` 方法负责收集测试用例的标记，并处理依赖关系和别名。

```python
def collect_markers(self) -> None:
    aliases: Dict[str, List[Item]] = {}
    dep_marks: Dict[Tuple[str, Scope, str], List[Item]] = {}
    for item in self.items:
        self.mark_binning(item, dep_marks, aliases)
    self.resolve_dependency_markers(dep_marks, aliases)
```

#### 功能解释

- **标记收集**：`collect_markers` 方法是 `Sorter` 类中用于初始化和收集测试用例标记的关键步骤。
- **依赖关系处理**：通过 `mark_binning` 方法，插件能够识别测试用例之间的依赖关系，并准备相应的标记。
- **别名处理**：别名用于处理测试用例的命名冲突或重载，确保每个测试用例都可以被唯一标识。


#### 方法参数

- 无参数。

#### 方法返回值

- 返回类型：`None`，这个方法不返回任何值，而是直接修改对象的状态。

#### 方法逻辑

1. **初始化字典**：
   - `aliases`：字典，用于存储别名和对应的测试用例列表。
   - `dep_marks`：字典，用于存储依赖标记和对应的测试用例列表。键是一个元组，包含依赖项的名称、作用域和前缀。

2. **遍历测试用例**：
   - 遍历 `self.items` 中的所有测试用例（`Item` 对象）。

3. **收集标记**：
   - 对于每个测试用例，调用 `mark_binning` 方法：
     - 收集依赖标记并存储到 `dep_marks` 字典中。
     - 收集别名并存储到 `aliases` 字典中。

4. **处理依赖标记**：
   - 调用 `resolve_dependency_markers` 方法，处理依赖标记：
     - 将依赖标记转换为相对标记，并存储到 `self.rel_marks` 列表中。


#### 使用场景

这个方法在 `Sorter` 类的实例化过程中被调用，通常在测试用例开始执行之前。它为后续的排序和依赖关系处理提供了必要的信息。

#### 注意事项

- **字典结构**：`dep_marks` 字典的键是一个元组，包含依赖项的名称、作用域和前缀，这有助于精确地识别依赖关系。
- **方法调用**：`mark_binning` 和 `resolve_dependency_markers` 方法的调用是收集和处理标记的核心，确保所有依赖关系都被正确识别和处理。

### resolve_dependency_markers 方法

`resolve_dependency_markers` 方法负责处理测试用例的依赖标记，并将它们转换为相对标记。

```python
def resolve_dependency_markers(
    self,
    dep_marks: Dict[Tuple[str, Scope, str], List[Item]],
    aliases: Dict[str, List[Item]],
) -> None:
    for (name, _, prefix), items in dep_marks.items():
        if name in aliases:
            for item in items:
                alias = self.matching_alias(aliases[name], item)
                self.dep_marks.append(RelativeMark(alias, item, move_after=True))
        else:
            label = "::".join((prefix, name))
            if label in aliases:
                for item in items:
                    alias = self.matching_alias(aliases[label], item)
                    self.dep_marks.append(
                        RelativeMark(alias, item, move_after=True)
                    )
            else:
                sys.stdout.write(
                    "\nWARNING: Cannot resolve the dependency marker '{}' "
                    "- ignoring it.".format(name)
                )
```

#### 功能解释

- **依赖标记处理**：该方法处理测试用例的依赖标记，确保测试用例按照依赖关系正确执行。
- **别名匹配**：通过 `matching_alias` 方法，找到与当前测试用例最匹配的别名测试用例。
- **相对标记创建**：创建 `RelativeMark` 对象，表示测试用例之间的相对执行顺序。
- **警告机制**：如果无法解析依赖标记，输出警告信息，提醒用户检查标记的正确性。

#### 方法参数

- `dep_marks`：`Dict[Tuple[str, Scope, str], List[Item]]`，一个字典，键是一个包含依赖项名称、作用域和前缀的元组，值是依赖该项的测试用例列表。
- `aliases`：`Dict[str, List[Item]]`，一个字典，存储测试用例的别名和对应的测试用例列表。

#### 方法返回值

- 返回类型：`None`，这个方法不返回任何值，而是直接修改对象的状态。

#### 方法逻辑

1. **遍历依赖标记**：
   - 遍历 `dep_marks` 字典中的每个条目。

2. **检查别名**：
   - 对于每个依赖标记，检查其名称 `name` 是否存在于 `aliases` 字典中。

3. **处理已知别名**：
   - 如果 `name` 存在于 `aliases` 中：
     - 遍历依赖项的测试用例列表 `items`。
     - 对于每个测试用例，调用 `matching_alias` 方法找到匹配的别名测试用例。
     - 创建 `RelativeMark` 对象，表示依赖关系，并将 `move_after` 设置为 `True`（表示依赖项应该在当前测试用例之后执行）。
     - 将 `RelativeMark` 对象添加到 `self.dep_marks` 列表中。

4. **处理未知别名**：
   - 如果 `name` 不存在于 `aliases` 中：
     - 创建完整的标签 `label`，格式为 `"::".join((prefix, name))`。
     - 检查 `label` 是否存在于 `aliases` 中：
       - 如果是，执行与已知别名相同的处理步骤。
       - 如果不是，输出警告信息，提示无法解析依赖标记，并忽略该标记。

5. **输出警告**：
   - 如果无法解析依赖标记，使用 `sys.stdout.write` 输出警告信息。

#### 注意事项

- **别名字典**：`aliases` 字典用于存储测试用例的别名，确保能够正确匹配依赖关系。
- **警告信息**：输出的警告信息直接写入标准输出，不会被 `pytest` 的日志系统捕获，因此可能不会被一些日志收集工具记录。

### matching_alias 方法

`matching_alias` 静态方法用于在多个具有相同别名的测试用例中选择与依赖项最匹配的一个。

```python
@staticmethod
def matching_alias(aliases: List[Item], item: Item) -> Item:
    if len(aliases) == 1:
        return aliases[0]

    # handle the rare case that several tests have the same alias name
    # we use the item that best matches the node id of the dependent item
    max_matching_parts = 0
    node_id_parts = re.split("(::|/)", item.node_id)
    matching_item = aliases[0]
    for alias_item in aliases:
        alias_node_id_parts = re.split("(::|/)", alias_item.node_id)
        nr_matching_parts = 0
        for n, a in zip(node_id_parts, alias_node_id_parts):
            if n != a:
                break
            nr_matching_parts += 1
        if nr_matching_parts > max_matching_parts:
            max_matching_parts = nr_matching_parts
            matching_item = alias_item
    return matching_item
```

#### 功能解释

- **别名匹配**：当多个测试用例具有相同的别名时，该方法通过比较节点 `ID` 来选择最匹配的测试用例。
- **最大匹配度**：通过计算节点 `ID` 的公共部分数量来确定匹配度，并选择匹配度最高的测试用例。

#### 方法参数

- `aliases`：`List[Item]`，一个包含测试用例项（`Item` 对象）的列表，这些测试用例具有相同的别名。
- `item`：`Item` 对象，当前正在处理的测试用例。

#### 方法返回值

- 返回类型：`Item`，最匹配的测试用例项。

#### 方法逻辑

1. **处理单个别名**：
   - 如果 `aliases` 列表中只有一个测试用例，则直接返回这个测试用例。

2. **处理多个别名**：
   - 如果 `aliases` 列表中有多个测试用例：
     - 初始化 `max_matching_parts` 为0，用于存储最大匹配部分的数量。
     - 使用正则表达式将当前测试用例的节点 ID (`item.node_id`) 分割成部分。
     - 初始化 `matching_item` 为 `aliases` 列表中的第一个测试用例。

3. **遍历别名测试用例**：
   - 遍历 `aliases` 列表中的每个测试用例 (`alias_item`)：
     - 使用正则表达式将 `alias_item.node_id` 分割成部分。
     - 初始化 `nr_matching_parts` 为0，用于存储当前别名测试用例与当前测试用例匹配的部分数量。
     - 遍历两个节点 ID 部分的列表（`node_id_parts` 和 `alias_node_id_parts`），比较每个部分是否相同：
       - 如果不相同，则终止当前循环。
       - 如果相同，则增加 `nr_matching_parts`。

4. **更新匹配测试用例**：
   - 如果 `nr_matching_parts` 大于 `max_matching_parts`：
     - 更新 `max_matching_parts` 为 `nr_matching_parts`。
     - 更新 `matching_item` 为当前别名测试用例 (`alias_item`)。

5. **返回最匹配的测试用例**：
   - 返回 `matching_item`，即与当前测试用例匹配度最高的别名测试用例。

#### 注意事项

- **正则表达式**：使用正则表达式 `re.split("(::|/)", node_id)` 来分割节点 ID，这可以处理包含 `::` 或 `/` 的节点 ID。
- **性能考虑**：在有大量测试用例和别名时，匹配过程可能会影响性能，因此在实际应用中需要考虑优化。


### module_item_groups 方法

`module_item_groups` 的函数，其作用是将测试用例按照它们所属的模块分组。

这个方法通常在测试用例的组织和排序过程中被调用，尤其是在需要按模块执行测试用例时。它可以帮助测试框架或测试插件将测试用例组织成模块级别的组，从而实现更灵活的测试执行策略。

```python
def module_item_groups(items: List[Item]) -> Dict[str, List[Item]]:
    """
    Split items into groups per module.
    """
    module_items: OrderedDict[str, List[Item]] = OrderedDict()
    for item in items:
        module_items.setdefault(item.module_path, []).append(item)
    return module_items
```

#### 功能解释

- **模块分组**：该函数将测试用例按照它们所属的模块进行分组，使得同一模块内的测试用例可以一起处理。
- **有序字典**：使用 `OrderedDict` 确保模块的顺序在最终的输出中得以保留。


#### 函数参数

- `items`：`List[Item]`，一个包含 `Item` 对象的列表，每个 `Item` 对象代表一个测试用例。

#### 函数返回值

- 返回类型：`Dict[str, List[Item]]`，一个字典，键是模块路径（字符串），值是该模块下所有测试用例的列表。

#### 函数逻辑

1. **初始化有序字典**：
   - `module_items: OrderedDict[str, List[Item]] = OrderedDict()`：创建一个 `OrderedDict`，用于存储模块路径和对应的测试用例列表。使用有序字典是为了保持模块的顺序。

2. **遍历测试用例**：
   - `for item in items`：遍历传入的测试用例列表。

3. **获取模块路径**：
   - `item.module_path`：获取当前测试用例的模块路径。

4. **设置默认值并添加测试用例**：
   - `module_items.setdefault(item.module_path, []).append(item)`：使用 `setdefault` 方法确保字典中存在与模块路径对应的键。如果不存在，则创建一个空列表作为该键的值。然后将当前测试用例添加到该列表中。

5. **返回结果**：
   - `return module_items`：返回包含模块路径和测试用例列表的字典。

#### 注意事项

- **模块路径**：函数依赖于 `Item` 对象的 `module_path` 属性来获取模块路径，确保每个测试用例的 `module_path` 属性正确设置。
- **性能考虑**：在处理大量测试用例时，该函数的性能是可接受的，因为它只需要遍历一次测试用例列表。但是，如果测试用例数量非常大，可能需要考虑更高效的数据结构或算法。

### directory_item_groups 方法

`directory_item_groups` 函数将测试用例按照它们所在的目录层级分组。

这个方法通常在测试用例的组织和排序过程中被调用，尤其是在需要按目录层级执行测试用例时。它可以帮助测试框架或测试插件将测试用例组织成目录级别的组，从而实现更灵活的测试执行策略。

```python
def directory_item_groups(items: List[Item], level: int) -> Dict[str, List[Item]]:
    """
    Split items into groups per directory at the given level.
    The level is relative to the root directory, which is at level 0.
    """
    module_items: OrderedDict[str, List[Item]] = OrderedDict()
    for item in items:
        module_items.setdefault(item.parent_path(level), []).append(item)
    return module_items
```

#### 功能解释

- **目录分组**：该函数将测试用例按照它们所在的目录层级进行分组，使得同一目录内的测试用例可以一起处理。
- **有序字典**：使用 `OrderedDict` 确保目录的顺序在最终的输出中得以保留。

#### 函数参数

- `items`：`List[Item]`，一个包含 `Item` 对象的列表，每个 `Item` 对象代表一个测试用例。
- `level`：`int`，目录层级的级别。级别是相对于根目录的，根目录级别为0。

#### 函数返回值

- 返回类型：`Dict[str, List[Item]]`，一个字典，键是目录路径（字符串），值是该目录下所有测试用例的列表。

#### 函数逻辑

1. **初始化有序字典**：
   - `module_items: OrderedDict[str, List[Item]] = OrderedDict()`：创建一个 `OrderedDict`，用于存储目录路径和对应的测试用例列表。使用有序字典是为了保持目录的顺序。

2. **遍历测试用例**：
   - `for item in items`：遍历传入的测试用例列表。

3. **获取目录路径**：
   - `item.parent_path(level)`：获取当前测试用例相对于根目录的指定层级级别的目录路径。

4. **设置默认值并添加测试用例**：
   - `module_items.setdefault(item.parent_path(level), []).append(item)`：使用 `setdefault` 方法确保字典中存在与目录路径对应的键。如果不存在，则创建一个空列表作为该键的值。然后将当前测试用例添加到该列表中。

5. **返回结果**：
   - `return module_items`：返回包含目录路径和测试用例列表的字典。

#### 注意事项

- **目录路径**：函数依赖于 `Item` 对象的 `parent_path` 方法来获取目录路径，确保每个测试用例的 `parent_path` 方法正确设置。
- **性能考虑**：在处理大量测试用例时，该函数的性能是可接受的，因为它只需要遍历一次测试用例列表。但是，如果测试用例数量非常大，可能需要考虑更高效的数据结构或算法。

### class_item_groups 方法

`class_item_groups` 函数，其作用是将测试用例按照它们所属的类进行分组。

这个方法通常在测试用例的组织和排序过程中被调用，尤其是在需要按类执行测试用例时。它可以帮助测试框架或测试插件将测试用例组织成类级别的组，从而实现更灵活的测试执行策略。

```python
def class_item_groups(items: List[Item]) -> Dict[str, List[Item]]:
    """
    Split items into groups per class.
    Items outside a class are sorted into a group per module.
    """
    class_items: OrderedDict[str, List[Item]] = OrderedDict()
    for item in items:
        delimiter_index = item.node_id.index("::")
        if "::" in item.node_id[delimiter_index + 2:]:
            delimiter_index = item.node_id.index("::", delimiter_index + 2)
        class_path = item.node_id[:delimiter_index]
        class_items.setdefault(class_path, []).append(item)
    return class_items
```

#### 功能解释

- **类分组**：该函数将测试用例按照它们所属的类进行分组，使得同一类内的测试用例可以一起处理。
- **模块分组**：不属于任何类的测试用例将按照它们所属的模块进行分组。

#### 函数参数

- `items`：`List[Item]`，一个包含 `Item` 对象的列表，每个 `Item` 对象代表一个测试用例。

#### 函数返回值

- 返回类型：`Dict[str, List[Item]]`，一个字典，键是类路径（字符串），值是该类下所有测试用例的列表。

#### 函数逻辑

1. **初始化有序字典**：
   - `class_items: OrderedDict[str, List[Item]] = OrderedDict()`：创建一个 `OrderedDict`，用于存储类路径和对应的测试用例列表。使用有序字典是为了保持类的顺序。

2. **遍历测试用例**：
   - `for item in items`：遍历传入的测试用例列表。

3. **获取类路径**：
   - `delimiter_index = item.node_id.index("::")`：找到测试用例节点ID中第一个 `"::"` 的索引，这通常表示模块和类之间的分隔符。
   - `if "::" in item.node_id[delimiter_index + 2 :]`：检查节点ID中是否还有第二个 `"::"`，这可能表示存在嵌套的类或方法。
   - `delimiter_index = item.node_id.index("::", delimiter_index + 2)`：如果存在第二个 `"::"`，则更新 `delimiter_index` 为第二个 `"::"` 的索引。

4. **提取类路径**：
   - `class_path = item.node_id[:delimiter_index]`：截取节点ID中从开始到第一个 `"::"` 之前的部分作为类路径。

5. **设置默认值并添加测试用例**：
   - `class_items.setdefault(class_path, []).append(item)`：使用 `setdefault` 方法确保字典中存在与类路径对应的键。如果不存在，则创建一个空列表作为该键的值。然后将当前测试用例添加到该列表中。

6. **返回结果**：
   - `return class_items`：返回包含类路径和测试用例列表的字典。

#### 注意事项

- **节点ID格式**：函数依赖于 `Item` 对象的 `node_id` 属性来获取类路径，确保每个测试用例的 `node_id` 属性正确设置，并且遵循 `"模块名::类名::方法名"` 的格式。
- **性能考虑**：在处理大量测试用例时，该函数的性能是可接受的，因为它只需要遍历一次测试用例列表。但是，如果测试用例数量非常大，可能需要考虑更高效的数据结构或算法。

###  ScopeSorter 类

#### 类定义和初始化

```python
class ScopeSorter:
    """
    Sorts the items for the defined scope.
    """
    def __init__(
        self,
        settings: Settings,
        items: List[Item],
        rel_marks: List[RelativeMark[Item]],
        dep_marks: List[RelativeMark[Item]],
        session_scope: bool = False,
    ) -> None:
        self.settings = settings
        self.items = items
        # no need to filter items in session scope
        if session_scope:
            self.rel_marks = rel_marks
            self.dep_marks = dep_marks
        else:
            self.rel_marks = filter_marks(rel_marks, self.items)
            self.dep_marks = filter_marks(dep_marks, self.items)
```

段代码定义了一个名为 `ScopeSorter` 的类，它负责在给定的作用域内对测试用例进行排序。

- **参数**：
  - `settings`：`Settings` 对象，包含排序相关的配置。
  - `items`：`List[Item]`，测试用例列表。
  - `rel_marks`：`List[RelativeMark[Item]]`，相对标记列表。
  - `dep_marks`：`List[RelativeMark[Item]]`，依赖标记列表。
  - `session_scope`：`bool`，指示是否是会话作用域。默认为 `False`。

- **属性**：
  - `self.settings`：存储传入的设置。
  - `self.items`：存储传入的测试用例列表。
  - `self.rel_marks`：存储过滤后的相对标记列表。如果是会话作用域，则直接使用传入的相对标记；否则，使用 `filter_marks` 函数过滤。
  - `self.dep_marks`：存储过滤后的依赖标记列表。处理方式与相对标记相同。

#### sort_items 方法

```python
def sort_items(self) -> List[Item]:
    if self.settings.group_scope.value < self.settings.scope.value:
        if self.settings.scope == Scope.SESSION:
            sorted_list = self.sort_in_session_scope()
        else:  # module scope / class group scope
            sorted_list = self.sort_in_module_scope()
    else:
        sorted_list = self.sort_items_in_scope(self.items, Scope.SESSION).items

    return sorted_list
```

- **功能**：对测试用例进行排序并返回排序后的列表。
- **参数**：无。
- **返回值**：`List[Item]`，排序后的测试用例列表。

**逻辑**：
1. **作用域比较**：
   - 如果 `group_scope` 的值小于 `scope` 的值，表示需要在更细粒度的作用域内进行分组和排序。
   - 根据 `settings.scope` 的值确定是会话作用域还是模块/类作用域，并调用相应的排序方法。

2. **会话作用域**：
   - 如果是会话作用域，调用 `sort_in_session_scope` 方法进行排序。

3. **模块/类作用域**：
   - 如果是模块或类作用域，调用 `sort_in_module_scope` 方法进行排序。

4. **组作用域等于或大于测试用例作用域**：
   - 如果 `group_scope` 的值等于或大于 `scope` 的值，直接在会话作用域内对测试用例进行排序，调用 `sort_items_in_scope` 方法。

5. **返回结果**：
   - 返回排序后的测试用例列表。

##### 功能解释

- **作用域排序**：`ScopeSorter` 类根据配置文件中指定的作用域对测试用例进行分组和排序。
- **细粒度排序**：在模块或类作用域内，测试用例会根据相对和依赖标记进行细粒度的排序。
- **会话作用域排序**：在会话作用域内，测试用例会根据会话级别的相对和依赖标记进行排序。

##### 使用场景

这个类在 `pytest-order` 插件中用于实现测试用例的排序逻辑，确保测试用例按照用户指定的顺序执行，满足不同的测试需求。

##### 注意事项

- **作用域处理**：在处理不同作用域的测试用例时，需要考虑作用域的层次关系，确保测试用例按照正确的顺序执行。
- **标记过滤**：在非会话作用域中，需要过滤相对和依赖标记，以确保只有属于当前作用域的测试用例被考虑在内。

#### sort_in_session_scope 方法

这段代码是 `ScopeSorter` 类中的 `sort_in_session_scope` 方法，它负责在会话作用域内对测试用例进行排序。

```python
def sort_in_session_scope(self) -> List[Item]:
    sorted_list = []
    module_items = module_item_groups(self.items)
    if self.settings.group_scope == Scope.CLASS:
        module_groups = self.sort_class_groups(module_items)
    else:
        module_groups = [
            self.sort_items_in_scope(item, Scope.MODULE)
            for item in module_items.values()
        ]
    sorter = GroupSorter(
        Scope.MODULE, module_groups, self.rel_marks, self.dep_marks
    )
    for group in sorter.sorted_groups()[1]:
        sorted_list.extend(group.items)
    return sorted_list
```

##### 功能解释

- **会话作用域排序**：该方法在会话作用域内对测试用例进行排序，考虑了模块和类的作用域。
- **模块分组**：首先将测试用例按模块分组。
- **类作用域处理**：如果配置要求，还会进一步按类分组并排序。
- **组排序器**：使用 `GroupSorter` 对模块组或类组进行排序。


##### 方法参数

- 无参数。

##### 方法返回值

- 返回类型：`List[Item]`，会话作用域内排序后的测试用例列表。

##### 方法逻辑

1. **初始化排序列表**：
   - `sorted_list = []`：创建一个空列表，用于存储最终排序后的测试用例。

2. **按模块分组**：
   - `module_items = module_item_groups(self.items)`：调用 `module_item_groups` 函数，将测试用例按模块分组。

3. **处理类作用域**：
   - `if self.settings.group_scope == Scope.CLASS`：如果配置的组作用域是类级别：
     - `module_groups = self.sort_class_groups(module_items)`：调用 `sort_class_groups` 方法，对每个模块内的类进行排序，并将结果存储在 `module_groups` 中。
   - 否则：
     - `module_groups = [self.sort_items_in_scope(item, Scope.MODULE) for item in module_items.values()]`：遍历每个模块的测试用例，调用 `sort_items_in_scope` 方法，按模块作用域对测试用例进行排序，并将结果存储在 `module_groups` 中。

4. **创建组排序器**：
   - `sorter = GroupSorter(Scope.MODULE, module_groups, self.rel_marks, self.dep_marks)`：创建 `GroupSorter` 实例，传入模块组列表、相对标记和依赖标记。

5. **排序模块组**：
   - `for group in sorter.sorted_groups()[1]`：调用 `sorted_groups` 方法获取排序后的模块组列表，并遍历这些组。
   - `sorted_list.extend(group.items)`：将每个组内的测试用例添加到 `sorted_list` 中。

6. **返回排序后的列表**：
   - `return sorted_list`：返回会话作用域内排序后的测试用例列表。

##### 注意事项

- **作用域处理**：在处理不同作用域的测试用例时，需要考虑作用域的层次关系，确保测试用例按照正确的顺序执行。
- **性能考虑**：在处理大量测试用例时，排序操作可能会影响性能，因此在实际应用中需要考虑优化。

通过这种方式，`pytest-order` 插件能够灵活地控制测试用例的执行顺序，满足不同的测试需求。



#### sort_in_module_scope 方法

这段代码是 `ScopeSorter` 类中的 `sort_in_module_scope` 方法，它负责在模块作用域内对测试用例进行排序。

```python
def sort_in_module_scope(self) -> List[Item]:
    sorted_list = []
    class_items = class_item_groups(self.items)
    class_groups = [
        self.sort_items_in_scope(item, Scope.CLASS) for item in class_items.values()
    ]
    sorter = GroupSorter(
        Scope.CLASS, class_groups, self.rel_marks, self.dep_marks
    )
    for group in sorter.sorted_groups()[1]:
        sorted_list.extend(group.items)
    return sorted_list
```

##### 功能解释

- **模块作用域排序**：该方法在模块作用域内对测试用例进行排序，考虑了类的作用域。
- **类分组**：首先将测试用例按类分组。
- **类组排序器**：使用 `GroupSorter` 对类组进行排序。

##### 方法参数

- 无参数。

##### 方法返回值

- 返回类型：`List[Item]`，模块作用域内排序后的测试用例列表。

##### 方法逻辑

1. **初始化排序列表**：
   - `sorted_list = []`：创建一个空列表，用于存储最终排序后的测试用例。

2. **按类分组**：
   - `class_items = class_item_groups(self.items)`：调用 `class_item_groups` 函数，将测试用例按类分组。

3. **对每个类进行排序**：
   - `class_groups = [self.sort_items_in_scope(item, Scope.CLASS) for item in class_items.values()]`：遍历每个类的测试用例，调用 `sort_items_in_scope` 方法，按类作用域对测试用例进行排序，并将结果存储在 `class_groups` 中。

4. **创建组排序器**：
   - `sorter = GroupSorter(Scope.CLASS, class_groups, self.rel_marks, self.dep_marks)`：创建 `GroupSorter` 实例，传入类组列表、相对标记和依赖标记。

5. **排序类组**：
   - `for group in sorter.sorted_groups()[1]`：调用 `sorted_groups` 方法获取排序后的类组列表，并遍历这些组。
   - `sorted_list.extend(group.items)`：将每个组内的测试用例添加到 `sorted_list` 中。

6. **返回排序后的列表**：
   - `return sorted_list`：返回模块作用域内排序后的测试用例列表。

##### 注意事项

- **作用域处理**：在处理不同作用域的测试用例时，需要考虑作用域的层次关系，确保测试用例按照正确的顺序执行。
- **性能考虑**：在处理大量测试用例时，排序操作可能会影响性能，因此在实际应用中需要考虑优化。

#### sort_class_groups 方法

这段代码是 `ScopeSorter` 类中的 `sort_class_groups` 方法，它负责在模块内对测试用例按类进行分组和排序。

```python
def sort_class_groups(self, module_items: Dict[str, List[Item]]) -> List[ItemGroup]:
    module_groups = []
    for module_item in module_items.values():
        class_items = class_item_groups(module_item)
        class_groups = [
            self.sort_items_in_scope(item, Scope.CLASS) for item in class_items.values()
        ]
        module_group = ItemGroup()
        sorter = GroupSorter(
            Scope.CLASS, class_groups, self.rel_marks, self.dep_marks
        )
        group_order, class_groups = sorter.sorted_groups()
        module_group.extend(class_groups, group_order)
        module_groups.append(module_group)
    return module_groups
```

##### 功能解释

- **模块内类分组**：该方法在模块内将测试用例按类分组，并进行排序。
- **类组排序**：使用 `GroupSorter` 对类组进行排序，确保测试用例按照指定的顺序执行。

##### 方法参数

- `module_items`：`Dict[str, List[Item]]`，一个字典，键是模块路径，值是该模块下所有测试用例的列表。

##### 方法返回值

- 返回类型：`List[ItemGroup]`，模块内排序后的测试用例组列表。

##### 方法逻辑

1. **初始化模块组列表**：
   - `module_groups = []`：创建一个空列表，用于存储每个模块的测试用例组。

2. **遍历模块内的测试用例**：
   - `for module_item in module_items.values()`：遍历每个模块的测试用例列表。

3. **按类分组**：
   - `class_items = class_item_groups(module_item)`：调用 `class_item_groups` 函数，将模块内的测试用例按类分组。

4. **对每个类进行排序**：
   - `class_groups = [self.sort_items_in_scope(item, Scope.CLASS) for item in class_items.values()]`：遍历每个类的测试用例，调用 `sort_items_in_scope` 方法，按类作用域对测试用例进行排序，并将结果存储在 `class_groups` 中。

5. **创建模块组**：
   - `module_group = ItemGroup()`：创建一个新的 `ItemGroup` 实例，用于存储当前模块的测试用例组。

6. **创建组排序器**：
   - `sorter = GroupSorter(Scope.CLASS, class_groups, self.rel_marks, self.dep_marks)`：创建 `GroupSorter` 实例，传入类组列表、相对标记和依赖标记。

7. **排序类组**：
   - `group_order, class_groups = sorter.sorted_groups()`：调用 `sorted_groups` 方法获取排序后的类组和组顺序值。

8. **扩展模块组**：
   - `module_group.extend(class_groups, group_order)`：使用 `extend` 方法将排序后的类组添加到模块组中，并指定组顺序值。

9. **添加模块组到列表**：
   - `module_groups.append(module_group)`：将当前模块的测试用例组添加到模块组列表中。

10. **返回模块组列表**：
    - `return module_groups`：返回包含所有模块测试用例组的列表。

##### 注意事项

- **作用域处理**：在处理不同作用域的测试用例时，需要考虑作用域的层次关系，确保测试用例按照正确的顺序执行。
- **性能考虑**：在处理大量测试用例时，排序操作可能会影响性能，因此在实际应用中需要考虑优化。

#### sort_items_in_scope 方法

这段代码是 `ScopeSorter` 类中的 `sort_items_in_scope` 方法，它负责在给定的作用域内对测试用例进行排序。

```python
def sort_items_in_scope(self, items: List[Item], scope: Scope) -> ItemGroup:
    item_list = ItemList(
        items, self.settings, scope, self.rel_marks, self.dep_marks
    )
    for item in items:
        item_list.collect_markers(item)

    sorted_list = item_list.sort_numbered_items()

    still_left = 0
    length = item_list.number_of_rel_groups()
    while length and still_left != length:
        still_left = length
        item_list.handle_rel_marks(sorted_list)
        item_list.handle_dep_marks(sorted_list)
        length = item_list.number_of_rel_groups()
    if length:
        item_list.print_unhandled_items()
    return ItemGroup(sorted_list, item_list.group_order())
```

##### 功能解释

- **作用域排序**：该方法在给定的作用域内对测试用例进行排序，考虑了编号、相对和依赖标记。
- **标记处理**：处理测试用例上的相对和依赖标记，确保测试用例按照指定的顺序执行。
- **未处理项警告**：如果存在未处理的相对或依赖标记，打印警告信息。

##### 方法参数

- `items`：`List[Item]`，一个包含 `Item` 对象的列表，每个 `Item` 对象代表一个测试用例。
- `scope`：`Scope`，一个枚举值，表示排序的作用域（例如 `Scope.CLASS` 或 `Scope.MODULE`）。

##### 方法返回值

- 返回类型：`ItemGroup`，包含排序后的测试用例和组顺序值的对象。

##### 方法逻辑

1. **创建 `ItemList` 实例**：
   - `item_list = ItemList(items, self.settings, scope, self.rel_marks, self.dep_marks)`：创建一个 `ItemList` 对象，传入测试用例列表、设置、作用域、相对标记和依赖标记。

2. **收集标记**：
   - `for item in items: item_list.collect_markers(item)`：遍历测试用例列表，为每个测试用例收集标记。

3. **排序编号项**：
   - `sorted_list = item_list.sort_numbered_items()`：调用 `ItemList` 的 `sort_numbered_items` 方法对测试用例进行排序，返回排序后的测试用例列表。

4. **处理相对和依赖标记**：
   - 初始化 `still_left` 和 `length` 变量：
     - `still_left = 0`
     - `length = item_list.number_of_rel_groups()`
   - 进入循环，直到没有剩余的相对或依赖组：
     - 在循环开始时，将 `length` 的值赋给 `still_left`。
     - 调用 `item_list.handle_rel_marks(sorted_list)` 处理相对标记。
     - 调用 `item_list.handle_dep_marks(sorted_list)` 处理依赖标记。
     - 更新 `length` 为当前的相对或依赖组数量。
   - 如果循环结束后 `length` 仍不为0，表示有未处理的相对或依赖标记。

5. **打印未处理的项**：
   - `if length: item_list.print_unhandled_items()`：如果有未处理的相对或依赖标记，调用 `print_unhandled_items` 方法打印警告信息。

6. **返回 `ItemGroup`**：
   - `return ItemGroup(sorted_list, item_list.group_order())`：创建一个 `ItemGroup` 对象，传入排序后的测试用例列表和组顺序值，并返回。

##### 注意事项

- **作用域处理**：在处理不同作用域的测试用例时，需要考虑作用域的层次关系，确保测试用例按照正确的顺序执行。
- **性能考虑**：在处理大量测试用例时，排序和标记处理操作可能会影响性能，因此在实际应用中需要考虑优化。

### scope_from_name 方法

这段代码定义了一个名为 `scope_from_name` 的函数，它用于根据传入的名称字符串返回相应的 `Scope` 枚举值。

```python
def scope_from_name(name: str) -> Scope:
    if name == "module":
        return Scope.MODULE
    if name == "class":
        return Scope.CLASS
    return Scope.SESSION
```

#### 功能解释

- **作用域映射**：这个函数是作用域名称到 `Scope` 枚举值的映射函数，它简化了从字符串名称到枚举值的转换。
- **默认值**：如果传入的名称不是预期的 `"module"` 或 `"class"`，函数会返回 `Scope.SESSION`，这表示会话级别的作用域。

#### 函数参数

- `name`：`str`，一个字符串，表示作用域的名称。

#### 函数返回值

- 返回类型：`Scope`，一个枚举值，表示测试用例的作用域。

#### 函数逻辑

1. **检查名称并返回对应的作用域**：
   - 函数首先检查传入的 `name` 是否等于 `"module"`：
     - 如果是，返回 `Scope.MODULE`。
   - 接下来，检查 `name` 是否等于 `"class"`：
     - 如果是，返回 `Scope.CLASS`。
   - 如果 `name` 既不是 `"module"` 也不是 `"class"`，则默认返回 `Scope.SESSION`。

#### 注意事项

- **枚举值匹配**：函数依赖于精确的字符串匹配来确定返回的 `Scope` 枚举值，因此传入的名称必须是预期的字符串之一。
- **大小写敏感**：由于字符串比较是区分大小写的，传入的名称必须与 `"module"` 或 `"class"` 完全匹配（包括大小写）。

通过这种方式，`scope_from_name` 函数提供了一种简单而直接的方法来将作用域的字符串表示转换为 `Scope` 枚举值，这在 `pytest-order` 插件中用于控制测试用例的执行顺序。


### scoped_node_id 方法

`scoped_node_id` 函数用于根据指定的作用域（`Scope`）从完整的节点 `ID`（`node_id`）中提取相关部分，用于控制测试用例的执行顺序和组织结构。

```python
def scoped_node_id(node_id: str, scope: Scope) -> str:
    if scope == Scope.MODULE:
        return node_id[: node_id.index("::")]
    if scope == Scope.CLASS:
        return node_id[: node_id.rindex("::")]
    return ""
```

#### 功能解释

- **作用域提取**：这个函数根据指定的作用域提取节点 `ID` 的相关部分，使得可以针对不同的作用域进行操作。
- **模块和类作用域**：特别处理模块和类作用域，通过提取节点 `ID` 的相应部分来标识测试用例所属的模块或类。


#### 函数参数

- `node_id`：`str`，完整的节点 `ID`，通常用于唯一标识测试用例。
- `scope`：`Scope`，一个枚举值，表示需要提取的作用域。

#### 函数返回值

- 返回类型：`str`，根据作用域提取的节点 `ID` 部分。

#### 函数逻辑

1. **模块作用域**：
   - 如果 `scope` 是 `Scope.MODULE`：
     - 使用 `node_id.index("::")` 查找第一个 `"::"` 的索引。
     - 返回 `node_id` 从开始到第一个 `"::"` 之前的部分（不包括 `"::"`）。

2. **类作用域**：
   - 如果 `scope` 是 `Scope.CLASS`：
     - 使用 `node_id.rindex("::")` 查找最后一个 `"::"` 的索引。
     - 返回 `node_id` 从开始到最后一个 `"::"` 之前的部分（不包括 `"::"`）。

3. **默认情况**：
   - 如果 `scope` 不是 `Scope.MODULE` 或 `Scope.CLASS`（例如 `Scope.SESSION`），则返回一个空字符串。

#### 注意事项

- **字符串操作**：函数通过字符串切片操作来提取节点 ID 的相关部分，因此 `node_id` 必须是一个有效的字符串。
- **作用域匹配**：函数依赖于 `scope` 参数的匹配来决定如何提取节点 ID，因此传入的 `scope` 必须是正确的枚举值。


### GroupSorter 类

`GroupSorter` 类负责对测试用例组进行排序。

#### 类定义和初始化

```python
class GroupSorter:
    """
    Sorts groups of items.
    """

    def __init__(
        self,
        scope: Scope,
        groups: List[ItemGroup],
        rel_marks: List[RelativeMark[Item]],
        dep_marks: List[RelativeMark[Item]],
    ) -> None:
        self.scope: Scope = scope
        self.groups: List[ItemGroup] = groups
        self.rel_marks: List[RelativeMark[ItemGroup]] = self.collect_group_marks(
            rel_marks
        )
        self.dep_marks: List[RelativeMark[ItemGroup]] = self.collect_group_marks(
            dep_marks
        )
```

- **参数**：
  - `scope`：`Scope`，作用域枚举值，表示排序的作用域。
  - `groups`：`List[ItemGroup]`，测试用例组的列表。
  - `rel_marks`：`List[RelativeMark[Item]]`，相对标记的列表。
  - `dep_marks`：`List[RelativeMark[Item]]`，依赖标记的列表。

- **属性**：
  - `self.scope`：存储传入的作用域。
  - `self.groups`：存储传入的测试用例组列表。
  - `self.rel_marks`：存储转换后的相对标记列表，这些标记是针对测试用例组的。
  - `self.dep_marks`：存储转换后的依赖标记列表，这些标记也是针对测试用例组的。

#### collect_group_marks 方法

```python
def collect_group_marks(
        self, marks: List[RelativeMark[Item]]
    ) -> List[RelativeMark[ItemGroup]]:
    group_marks: List[RelativeMark[ItemGroup]] = []
    for mark in marks:
        group = self.group_for_item(mark.item)
        group_to_move = self.group_for_item(mark.item_to_move)
        if group is not None and group_to_move is not None:
            group_marks.append(RelativeMark(group, group_to_move, mark.move_after))
            group_to_move.inc_rel_marks()
    return group_marks
```

- **功能**：将针对测试用例的相对标记转换为针对测试用例组的相对标记。
- **参数**：
  - `marks`：`List[RelativeMark[Item]]`，原始的相对标记列表。
- **返回值**：`List[RelativeMark[ItemGroup]]`，转换后的相对标记列表。

#### group_for_item 方法

```python
def group_for_item(self, item: Item) -> Optional[ItemGroup]:
    for group in self.groups:
        if item in group.items:
            return group
    return None
```

- **功能**：根据测试用例找到对应的测试用例组。
- **参数**：
  - `item`：`Item`，测试用例。
- **返回值**：`Optional[ItemGroup]`，对应的测试用例组，如果没有找到则返回 `None`。

#### sorted_groups 方法

```python
def sorted_groups(self) -> Tuple[Optional[int], List[ItemGroup]]:
    group_order = self.sort_by_ordinal_markers()
    length = len(self.rel_marks) + len(self.dep_marks)
    if length == 0:
        return group_order, self.groups

    # handle relative markers the same way single items are handled
    still_left = 0
    while length and still_left != length:
        still_left = length
        self.handle_rel_marks(self.rel_marks)
        self.handle_rel_marks(self.dep_marks)
    return group_order, self.groups
```

- **功能**：对测试用例组进行排序，并返回排序后的组和组的顺序值。
- **返回值**：`Tuple[Optional[int], List[ItemGroup]]`，组的顺序值和排序后的测试用例组列表。

#### sort_by_ordinal_markers 方法

```python
def sort_by_ordinal_markers(self) -> Optional[int]:
    start_groups = []
    middle_groups = []
    end_groups = []
    for group in self.groups:
        if group.order is None:
            middle_groups.append(group)
        elif group.order >= 0:
            start_groups.append(group)
        else:
            end_groups.append(group)
    start_groups = sorted(start_groups, key=lambda g: cast(int, g.order))
    end_groups = sorted(end_groups, key=lambda g: cast(int, g.order))
    self.groups = start_groups + middle_groups + end_groups
    if start_groups:
        group_order = start_groups[0].order
    elif end_groups:
        group_order = end_groups[-1].order
    else:
        group_order = None
    return group_order
```

- **功能**：根据序数标记对测试用例组进行排序。
- **返回值**：`Optional[int]`，组的顺序值。

#### handle_rel_marks 方法

```python
def handle_rel_marks(self, marks: List[RelativeMark[ItemGroup]]) -> None:
    for mark in reversed(marks):
        if move_item(mark, self.groups):
            marks.remove(mark)
```

- **功能**：处理相对标记，调整测试用例组的顺序。
- **参数**：
  - `marks`：`List[RelativeMark[ItemGroup]]`，相对标记列表。

#### 功能解释

- **测试用例组排序**：`GroupSorter` 类对测试用例组进行排序，考虑了序数标记和相对标记。
- **序数标记处理**：通过 `sort_by_ordinal_markers` 方法，根据序数标记对测试用例组进行初步排序。
- **相对标记处理**：通过 `handle_rel_marks` 方法，处理相对标记，进一步调整测试用例组的顺序。

#### 注意事项

- **作用域处理**：在处理不同作用域的测试用例组时，需要考虑作用域的层次关系，确保测试用例组按照正确的顺序执行。
- **性能考虑**：在处理大量测试用例组时，排序和标记处理操作可能会影响性能，因此在实际应用中需要考虑优化。

# pytest-order插件的使用与闭坑

## 安装

```shell
pip install pytest-order
```

## 准备测试用例

```python
root@Gavin:~/pytest_plugin/test/pytest_order_example# cat test_a.py 
import pytest

@pytest.mark.order("first")
def test_a1():
    print("Executing test_a1")

@pytest.mark.order("last")
def test_a2():
    print("Executing test_a2")

@pytest.mark.order(after="test_a1")
def test_a3():
    print("Executing test_a3")
root@Gavin:~/pytest_plugin/test/pytest_order_example# cat test_b.py 
import pytest

@pytest.mark.order(1)
def test_b1():
    print("Executing test_b1")

@pytest.mark.order(2, scope="module")
def test_b2():
    print("Executing test_b2")

@pytest.mark.order(3, scope="class")
class TestB3:
    def test_method1(self):
        print("Executing test_b3_method1")

    def test_method2(self):
        print("Executing test_b3_method2")
root@Gavin:~/pytest_plugin/test/pytest_order_example# cat test_c.py 
import pytest

@pytest.mark.order(1)
def test_c1():
    print("Executing test_c1")

@pytest.mark.order(2)
def test_c2():
    print("Executing test_c2")

@pytest.mark.order(3)
def test_c3():
    print("Executing test_c3")
root@Gavin:~/pytest_plugin/test/pytest_order_example#
```

##  测试用例执行

```shell
root@Gavin:~/pytest_plugin/test/pytest_order_example# pytest -v
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'profiling': '1.7.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'sugar': '1.0.0', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3', 'line-profiler': '0.2.1'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/pytest_plugin/test/pytest_order_example
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, sugar-1.0.0, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1
asyncio: mode=Mode.STRICT
collected 10 items                                                                                                                                                                                                                                       

 test_a.py::test_a1 ?                                                                                                                                                                                                                       10% █         
 test_b.py::test_b1 ?                                                                                                                                                                                                                       20% ██        
 test_c.py::test_c1 ?                                                                                                                                                                                                                       30% ███       
 test_b.py::test_b2 ?                                                                                                                                                                                                                       40% ████      
 test_c.py::test_c2 ?                                                                                                                                                                                                                       50% █████     
 test_b.py::TestB3.test_method1 ?                                                                                                                                                                                                           60% ██████    
 test_b.py::TestB3.test_method2 ?                                                                                                                                                                                                           70% ███████   
 test_c.py::test_c3 ?                                                                                                                                                                                                                       80% ████████  
 test_a.py::test_a3 ?                                                                                                                                                                                                                       90% █████████ 
 test_a.py::test_a2 ?                                                                                                                                                                                                                      100% ██████████
=============================================================================================================== sum of all tests durations ===============================================================================================================
0.05s

Results (0.08s):
      10 passed
root@Gavin:~/pytest_plugin/test/pytest_order_example# 
```

从上面记录可以看到，执行顺序是：

```shell
 test_a.py::test_a1                                                                                                                                                                                                                        10% █         
 test_b.py::test_b1                                                                                                                                                                                                                        20% ██        
 test_c.py::test_c1                                                                                                                                                                                                                        30% ███       
 test_b.py::test_b2                                                                                                                                                                                                                        40% ████      
 test_c.py::test_c2                                                                                                                                                                                                                        50% █████     
 test_b.py::TestB3.test_method1                                                                                                                                                                                                            60% ██████    
 test_b.py::TestB3.test_method2                                                                                                                                                                                                            70% ███████   
 test_c.py::test_c3                                                                                                                                                                                                                        80% ████████  
 test_a.py::test_a3                                                                                                                                                                                                                        90% █████████ 
 test_a.py::test_a2   
```

## 坑点

如果没有使用`pytest-order`插件，从测试用例文件命名来看，会先执行`test_a.py`，再执行`test_b.py`，最后执行`test_c.py`，但使用了`pytest-order`插件后,会打乱执行顺序，尤其是使用了`@pytest.mark.order("last")`，它会在当前执行会话中所有的用例都执行结束后，最最后来执行这个标记的测试用例，并非是我们所想的单个测试用例`py`文件中的最后执行，而是在所有测试用例`py`文件的最后执行。
这一点，请牢牢记住，避免多个用例文件之间有环境准备/清理关系，导致`@pytest.mark.order("last")`的用例执行失败。
