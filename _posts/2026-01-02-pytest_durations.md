---
title: 测试用例持续时间之pytest_durations源码解读
date: 2026-01-02 23:00:00
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
summary: 测试用例持续时间之pytest_durations源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-durations` 是一个 `pytest` 插件，用于测量测试的执行时间，包括测试用例的调用、设置和清理，以及 `fixture` 的设置和销毁。

`pytest_durations`插件默认被`pytest`安装&使用，对应参数如下(使用`pytest -h`命令查看)：

```shell
  --durations=N         Show N slowest setup/test durations (N=0 for all)
  --durations-min=N     Minimal duration in seconds for inclusion in slowest list. Default: 0.005.
```

`pytest_durations`源码下载后解压，目录/文件参考如下：

```shell
root@Gavin:~/pytest_plugin/pytest-durations-1.2.0# ll
total 36
drwxr-xr-x 3 root root 4096 Jul  3 15:09 ./
drwxr-xr-x 9 root root 4096 Jul 13 14:05 ../
-rw-r--r-- 1 root root 1069 Apr 22  2022 LICENSE
-rw-r--r-- 1 root root 4165 Apr 22  2022 PKG-INFO
-rw-r--r-- 1 root root 1358 Apr 22  2022 pyproject.toml
-rw-r--r-- 1 root root 3156 Apr 22  2022 README.md
-rw-r--r-- 1 root root 4088 Apr 22  2022 setup.py
drwxr-xr-x 3 root root 4096 Jul  3 15:08 src/
root@Gavin:~/pytest_plugin/pytest-durations-1.2.0# cd src
root@Gavin:~/pytest_plugin/pytest-durations-1.2.0/src# ll
total 12
drwxr-xr-x 3 root root 4096 Jul  3 15:08 ./
drwxr-xr-x 3 root root 4096 Jul  3 15:09 ../
drwxr-xr-x 2 root root 4096 Jul 15 09:40 pytest_durations/
root@Gavin:~/pytest_plugin/pytest-durations-1.2.0/src# cd pytest_durations/
root@Gavin:~/pytest_plugin/pytest-durations-1.2.0/src/pytest_durations# ll
total 48
drwxr-xr-x 2 root root 4096 Jul 15 09:40 ./
drwxr-xr-x 3 root root 4096 Jul  3 15:08 ../
-rw-r--r-- 1 root root  725 Apr 22  2022 helpers.py
-rw-r--r-- 1 root root  109 Apr 22  2022 __init__.py
-rw-r--r-- 1 root root  866 Apr 22  2022 measure.py
-rw-r--r-- 1 root root 1351 Apr 22  2022 options.py
-rw-r--r-- 1 root root 5664 Apr 22  2022 plugin.py
-rw-r--r-- 1 root root 3244 Apr 22  2022 reporting.py
-rw-r--r-- 1 root root  312 Apr 22  2022 ticker.py
-rw-r--r-- 1 root root   81 Apr 22  2022 types.py
-rw-r--r-- 1 root root 1816 Apr 22  2022 xdist.py
root@Gavin:~/pytest_plugin/pytest-durations-1.2.0/src/pytest_durations#
```

1. **`__init__.py`**:
   - 通常，这个文件用于初始化插件，使 `Python` 知道该目录应该被视为一个包。在 `pytest` 插件中，它可能包含插件的入口点。

2. **`helpers.py`**:
   - 包含一些辅助函数，可能用于生成测试或 `fixture` 的唯一键，或检查 `fixture` 是否是共享的。

3. **`measure.py`**:
   - 包含 `MeasureDuration` 类，这是一个上下文管理器，用于测量代码块的执行时间。

4. **`ticker.py`**:
   - 包含获取当前时间戳的函数，可能用于测量持续时间。

5. **`types.py`**:
   - 定义了插件中使用的数据类型，例如 `MeasurementsT`，这是一个字典类型，用于存储测量结果。

6. **`options.py`**:
   - 可能包含处理命令行选项和配置的代码，例如 `--pytest-durations` 和 `--pytest-durations-min`。

7. **`reporting.py`**:
   - 包含生成报告的逻辑，例如 `get_report_rows` 和 `get_report_max_widths` 函数，用于格式化和显示测量结果。

8. **`plugin.py`**:
   - 这是插件的主要文件，定义了 `PystDurationPlugin` 类，实现了 `pytest` 插件的核心逻辑。它使用其他组件（如 `helpers.py`、`measure.py`、`reporting.py`）来测量测试的执行时间，并在测试结束时生成报告。

9. **`xdist.py`**:
   - 处理与 `pytest-xdist` 插件的集成，确保在分布式测试环境中测量数据的正确收集和合并。

插件的运行和互相调用顺序通常如下：

- 当 `pytest` 命令行工具启动时，它将加载所有可用的插件，包括 `pytest-durations`。
- 如果用户使用了与 `pytest-durations` 相关的命令行选项（如 `--pytest-durations`），`options.py` 将处理这些选项。
- 在 `pytest` 运行期间，`plugin.py` 中的钩子方法将被调用，以测量测试和 `fixture` 的执行时间：
  - `pytest_fixture_setup` 和 `pytest_fixture_post_finalizer` 用于测量 `fixture` 的设置和销毁时间。
  - `pytest_runtest_call`、`pytest_runtest_setup` 和 `pytest_runtest_teardown` 用于测量测试用例的不同阶段的执行时间。
- `measure.py` 中的 `MeasureDuration` 上下文管理器被 `plugin.py` 用于测量指定代码块的执行时间。
- 测量结果将使用 `types.py` 中定义的类型存储。
- 当测试会话结束时，`plugin.py` 中的 `pytest_terminal_summary` 钩子方法将调用 `reporting.py` 中的函数来生成和显示测量结果的报告。
- 如果使用 `pytest-xdist` 进行分布式测试，`xdist.py` 将确保测量结果在不同的工作进程之间正确合并。

**请注意:**

这个顺序是基于源码文件的功能和 `pytest` 插件的一般工作方式推断的。实际的调用顺序可能会根据 `pytest` 的版本和插件的具体实现有所不同。


# 源码解读

## helpers.py文件

`helpers.py` 文件通常包含了一些工具函数，用于在 `pytest-durations` 插件或其他 pytest 插件中辅助处理测试用例和 `fixture` 的信息。

### 导入类型检查

```python
from typing import TYPE_CHECKING
```

这行代码导入了 `TYPE_CHECKING`，它是一个标志，用于在类型检查时（例如使用 `mypy`）导入模块，而不在运行时导入，这样可以避免循环依赖和不必要的性能开销。

### 条件导入

```python
if TYPE_CHECKING:
    from _pytest.fixtures import FixtureDef
    from _pytest.nodes import Item
```

这个条件导入块只在类型检查时执行，它导入了 `FixtureDef` 和 `Item` 类型，这些类型用于指定函数参数的类型注解。

### _get_fixture_key 函数

```python
def _get_fixture_key(fixturedef: "FixtureDef") -> str:
    """Return fixture name."""
    return fixturedef.argname
```

这个函数接收一个 `FixtureDef` 对象作为参数，返回该 fixture 的名称，即 `argname` 属性的值。

### _get_test_key 函数

```python
def _get_test_key(item: "Item") -> str:
    """Return test item name without filename part (class and function names only)."""
```
这个函数接收一个 `Item` 对象作为参数，返回测试项的名称，但不包括文件名部分。它通过以下步骤实现：

- 使用 `split("::", 1)[1]` 移除 `nodeid` 中的文件名部分。
- 使用 `split("[", 1)[0]` 移除 `nodeid` 中的参数部分。

### _is_shared_fixture 函数

```python
def _is_shared_fixture(fixturedef: "FixtureDef") -> bool:
    """Return true if a fixture is shared."""
    return fixturedef.scope != "function"
```

这个函数检查传入的 `FixtureDef` 对象，如果该 `fixture` 的作用域不是 "function"，则返回 `True`，表示这是一个共享 `fixture`。


## ticker.py文件

`ticker.py` 文件是 `pytest-durations` 插件的一部分，它提供了一个用于获取当前时间戳的方法。

### 导入语句

```python
from time import monotonic
```

这里导入了 `Python` 标准库 `time` 模块中的 `monotonic` 函数。`monotonic` 函数返回一个单调递增的时间值，这个值不会受到系统时间变化的影响，因此适合用于测量时间间隔。

### 尝试导入 freezegun

```python
try:
    # if freezegun is installed, use its stored real function
    import freezegun
except ImportError:
    pass
else:
    freezegun.configure(extend_ignore_list=[__name__])
```

这段代码尝试导入 `freezegun` 库，这是一个流行的 `Python` 测试库，允许开发者在测试中“冻结”时间。如果 `freezegun` 已安装，它将使用 `freezegun` 的时间替代 `monotonic` 函数的时间。`freezegun.configure` 调用配置 `freezegun` 忽略当前模块（`__name__`），这意味着 `pytest-durations` 插件的时间测量将不受 `freezegun` 的影响。

### get_current_ticks 函数

```python
def get_current_ticks():
    """Return uniformly increasing value in seconds."""
    return monotonic()
```

这个函数是一个简单的封装器，它调用 `monotonic` 函数并返回结果。它的作用是提供一个统一的接口来获取当前时间的单调递增值，这个值以秒为单位。在正常的测试环境中，这将返回自某个固定点以来经过的时间。如果 `freezegun` 被安装并配置，这个函数将返回 `freezegun` 提供的时间值。



## measure.py文件

`measure.py` 文件定义了一个用于测量代码块执行时间的上下文管理器 `MeasureDuration`。

### 导入语句

```python
from typing import Type, TYPE_CHECKING
from pytest_durations.ticker import get_current_ticks
```

这里导入了必要的类型注解和 `get_current_ticks` 函数，后者用于获取当前的滴答数（通常是单调时钟值，用于测量时间间隔）。

### 类定义

```python
class MeasureDuration:
```

定义了一个名为 `MeasureDuration` 的类，它是一个上下文管理器，用于测量代码块的执行时间。

### 类属性

```python
start: float  # monotonic clock value of block entrance
end: float  # monotonic clock value of block exit
duration: float  # duration of block execution in seconds
```

这些属性分别用于存储代码块开始时的单调时钟值、结束时的值，以及计算出的执行时间（以秒为单位）。

### __enter__ 方法

```python
def __enter__(self) -> "MeasureDuration":
    """Store block entrance time."""
    self.start = get_current_ticks()
    self.duration = 0.0
    return self
```

当使用 `with` 语句进入上下文时，此方法被调用。它记录了代码块开始执行的时间，并将 `duration` 属性初始化为 0.0。然后返回 `MeasureDuration` 实例本身。

### __exit__ 方法

```python
def __exit__(self, exc_type: Type[Exception], exc_val: Exception, exc_tb: "TracebackType") -> None:
    """Store block exit time and calculate its duration."""
    self.end = get_current_ticks()
    self.duration += self.end - self.start
    return None
```

当使用 `with` 语句退出上下文时，此方法被调用。它记录了代码块结束执行的时间，并通过当前时钟值减去开始时的时钟值来计算持续时间，然后更新 `duration` 属性。这个方法的返回值为 `None`，表示不抑制任何异常。


## options.py文件

`options.py` 文件是 `pytest-durations` 插件的一部分，它定义了如何向 pytest 添加命令行选项，并在 `pytest` 配置阶段注册插件。

### 导入语句

```python
from typing import NoReturn, TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.config import PytestPluginManager, Config
    from _pytest.config.argparsing import Parser
```

这里导入了必要的类型注解，并且在类型检查时导入了 `PytestPluginManager`、`Config` 和 `Parser` 类型。

### 默认值定义

```python
DEFAULT_DURATIONS = 30
DEFAULT_DURATIONS_MIN = 0.005
```
定义了两个默认值：`DEFAULT_DURATIONS` 是显示最慢测试数量的默认值，`DEFAULT_DURATIONS_MIN` 是包含在最慢测试列表中的最小持续时间（秒）。

### pytest_addoption 函数

```python
def pytest_addoption(parser: "Parser", pluginmanager: "PytestPluginManager") -> NoReturn:
```

这个函数在 `pytest` 命令行解析阶段被调用，用于添加自定义选项。

```python
group = parser.getgroup("pytest-durations")
```

创建或获取一个选项组，用于组织 `pytest-durations` 插件的命令行选项。

```python
group.addoption(
    "--pytest-durations",
    metavar="N",
    type=int,
    default=DEFAULT_DURATIONS,
    help=f"Show N slowest setup/test durations (N=0 to disable plugin). Default {DEFAULT_DURATIONS}",
)
```

添加一个命令行选项 `--pytest-durations`，允许用户指定显示的最慢测试数量。

```python
group.addoption(
    "--pytest-durations-min",
    metavar="N",
    type=float,
    default=DEFAULT_DURATIONS_MIN,
    help=f"Minimal duration in seconds for inclusion in slowest list. Default {DEFAULT_DURATIONS_MIN}",
)
```

添加另一个命令行选项 `--pytest-durations-min`，允许用户指定包含在最慢测试列表中的最小持续时间。

### pytest_configure 函数

```python
def pytest_configure(config: "Config") -> NoReturn:
```
这个函数在 `pytest` 配置阶段被调用，用于根据命令行选项配置插件。

```python
if not config.getoption("--pytest-durations"):
    return
```

如果用户没有指定 `--pytest-durations` 选项或将其设置为 0，表示禁用插件，则不进行进一步配置。

```python
from pytest_durations.plugin import PytestDurationPlugin
```

导入插件的实现。

```python
pluginmanager = config.pluginmanager
```

获取插件管理器。

```python
if pluginmanager.hasplugin("xdist"):
    from pytest_durations.xdist import PytestDurationXdistMixin
    PytestDurationPlugin = type("PytestDurationPlugin", (PytestDurationPlugin, PytestDurationXdistMixin), {})
```

检查是否使用了 `pytest-xdist` 插件，如果使用了，则将 `PytestDurationPlugin` 与 `PytestDurationXdistMixin` 混合，以支持分布式测试。

```python
pluginmanager.register(PytestDurationPlugin())
```

注册 `PytestDurationPlugin` 插件。


## reporting文件

`reporting.py` 文件是 `pytest-durations` 插件的一部分，它定义了如何生成和格式化测试持续时间的报告。

### 类型别名和常量

```python
ReportRowT = Tuple[str, str, str, str, str, str]
TimeValuesT = Tuple[str, int, float, float, float, float]

_SUM_COLUMN_IDX = 5
_SORT_COLUMN_IDX = 5
_COLUMNS_ORDER = (5, 0, 1, 4, 2, 3)
_GRAND_TOTAL_STR = "grand total"
```

- `ReportRowT` 是报告行的类型别名，表示一个元组，包含六个字符串元素：名称、调用次数、最小时间、最大时间、平均时间和总时间。
- `TimeValuesT` 是时间值的类型别名，表示一个元组，包含名称、时间列表长度、最小时间、最大时间、中位数时间和总时间。
- `_SUM_COLUMN_IDX` 和 `_SORT_COLUMN_IDX` 是列索引，用于在排序和选择时引用总时间列。
- `_COLUMNS_ORDER` 是列的顺序，定义了报告行中各列的显示顺序。
- `_GRAND_TOTAL_STR` 是报告中总计行的标签。

### 报告生成函数

```python
def get_report_rows(
    measurements: Dict[str, List[float]],
    duration_min: float = -1.0,
    durations: int = 0,
) -> List[ReportRowT]:
```

这个函数生成测试持续时间的报告行。它接受一个字典 `measurements`，其中包含测试名称和对应的时间列表，以及两个可选参数：`duration_min`（最小持续时间阈值）和 `durations`（要显示的持续时间数量）。

### 报告行生成辅助函数

```python
def _get_report_header_row() -> ReportRowT:
```

生成报告的标题行。

```python
def _get_report_footer_row(time_values: List[TimeValuesT]) -> ReportRowT:
```

生成报告的总计行，使用 `time_values` 列表计算总计。

```python
def _get_report_timing_rows(time_values: List[TimeValuesT]) -> List[ReportRowT]:
```

生成报告中的时间测量行，基于 `time_values` 列表。

### 报告列宽函数

```python
def get_report_max_widths(report_rows: Collection[ReportRowT]) -> Tuple[int, int, int, int, int, int]:
```

这个函数计算报告中每列的最大宽度，以便在格式化报告时保持列的对齐。

### 报告数据格式化

在 `_get_report_footer_row` 和 `_get_report_timing_rows` 函数中，使用 `timedelta` 对象将时间值格式化为更易读的格式（例如，将秒转换为 `1 day, 3:45:00`）。


## types.py文件

`types.py` 文件定义了 `pytest-durations` 插件中使用的一个类型别名，用于类型注解。

### 类型别名

```python
MeasurementsT = Dict[str, Dict[str, List[float]]]
```

- `MeasurementsT` 是一个类型别名，表示一个字典，其键是一个字符串（通常是测试函数或测试集合的名称），值是另一个字典。
- 内部字典的键也是一个字符串（可能表示 "call" 或其他相关的时间度量类别），值是一个浮点数列表，代表各个时间度量。

这个类型别名用于在整个插件中保持类型一致性，使得时间度量数据的存储和传递更加清晰和规范。通过使用 `MeasurementsT`，开发者可以轻松地识别和操作与测试相关的所有时间度量数据。

例如，`MeasurementsT` 可以用于存储以下数据结构：

```python
{
    "test_function_1": {
        "call": [0.1, 0.2, 0.15],  # 测试函数1的调用时间列表
    },
    "test_function_2": {
        "call": [0.3, 0.25],       # 测试函数2的调用时间列表
    },
    # ... 更多测试函数的时间度量
}
```

在这个例子中，`MeasurementsT` 存储了不同测试函数的调用时间列表，这可以用于后续的性能分析和报告生成。

## xdist.py文件

`xdist.py` 文件是 `pytest-durations` 插件的一部分，专门处理与 `pytest-xdist` 插件的集成，后者用于并行测试执行。

### 类型导入

```python
from typing import Union, NoReturn, Optional, Any, TYPE_CHECKING
```

导入了必要的类型注解。

### 类型检查条件导入

```python
if TYPE_CHECKING:
    from _pytest.config import ExitCode
    from _pytest.main import Session
    from xdist.workermanage import WorkerController
    from pytest_durations.types import MeasurementsT
```

在类型检查时导入了一些额外的类型，以确保类型兼容性。

### 常量定义

```python
_WORKEROUTPUT_KEY = "pytest_durations"
```

定义了一个常量，用作在 `pytest-xdist` 的工作进程之间传递测量数据的键。

### PytestDurationXdistMixin 类

```python
class PytestDurationXdistMixin:
```

这个类定义了一个混入（`mixin`），提供了在分布式测试环境中合并测量数据的方法。

### 成员变量

```python
measurements: "MeasurementsT"
```

类变量 `measurements` 用于存储测试的测量数据，其类型为之前在 `types.py` 中定义的 `MeasurementsT`。

### 钩子方法

```python
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(self, session: "Session", exitstatus: Union[int, "ExitCode"]) -> None:
```

在测试会话结束时调用，用于将测量数据发送到主进程。

```python
def pytest_testnodedown(self, node: "WorkerController", error: Optional[Any]) -> NoReturn:
```

在 `pytest-xdist` 的工作节点（`worker node`）完成测试并断开连接时调用，用于合并该节点的测量数据。

### 数据合并方法

```python
def _extend_measurements(self, src: "MeasurementsT") -> NoReturn:
```

私有方法，用于将源字典 `src` 中的测量数据合并到 `self.measurements` 中。如果目标类别（`category`）不存在，它会创建新的类别并复制数据；如果已存在，它会将新值追加到现有列表的末尾。


## plugin.py文件

`plugin.py` 文件是 `pytest-durations` 插件的核心，定义了插件的主要行为和与 `pytest` 的交互。

### 导入和类型注解

文件开始处导入了必要的模块和类型注解，包括 `pytest` 的钩子（`hook`）和插件的其他组件。

### 类型检查条件导入

```python
if TYPE_CHECKING:
    # 导入用于类型检查的额外类型
```

### Category 类

```python
class Category:
    # 定义了测量类别的常量
    FIXTURE_SETUP = "fixture"
    TEST_CALL = "test"
    TEST_SETUP = "setup"
    TEST_TEARDOWN = "teardown"

    @classmethod
    def report_items(cls) -> Iterable[Tuple[str, str]]:
        # 生成报告项的元组，包括类别名称和显示名称
```

### PystDurationPlugin 类

```python
class PytestDurationPlugin:
    # 插件的主要类，实现了 `pytest` 插件的逻辑
```

这个类包含了测量测试和 `fixture` 执行时间的逻辑，以及生成报告的方法。

### 成员变量

```python
measurements: "MeasurementsT"
shared_fixture_duration: float
last_fixture_teardown_start: float
```

- `measurements`：存储测量数据的字典。
- `shared_fixture_duration`：共享 `fixture` 设置的累计时间。
- `last_fixture_teardown_start`：共享 `fixture` 销毁开始的时间戳。

### 钩子方法

类中定义了多个 `pytest` 钩子方法，这些方法在 `pytest` 的不同阶段被调用：

- `pytest_fixture_setup`：测量 `fixture` 设置的执行时间。
- `pytest_fixture_post_finalizer`：计算 `fixture` 销毁的执行时间。
- `pytest_runtest_call`：测量测试执行的时间。
- `pytest_runtest_setup`：测量测试准备时间，排除共享 `fixture` 的时间。
- `pytest_runtest_teardown`：测量测试清理时间，排除共享 `fixture` 的时间。
- `pytest_terminal_summary`：在终端总结中添加持续时间报告。

### 上下文管理器

```python
@contextmanager
def _measure(self, category: str, key: str) -> Iterable["MeasureDuration"]:
    # 上下文管理器，用于测量代码块的执行时间
```

这个上下文管理器 `_measure` 用于测量指定类别和键的代码块的执行时间，并在测量完成后将结果添加到 `measurements` 字典中。


# 小结

- `helpers.py` 中的这些函数提供了一种方法来处理和识别 `pytest` 中的 `fixtures` 和测试用例。通过这些工具函数，插件可以更容易地获取和操作测试相关的数据，例如，用于收集测试用例的持续时间数据。这些函数通常在插件的其它部分被调用，以辅助实现插件的主要功能。
- `MeasureDuration` 类提供了一个简单的上下文管理器，用于测量任何代码块的执行时间。通过重写 `__enter__` 和 `__exit__` 方法，它能够在代码块执行前后获取时间戳，并计算出执行时间。这个类可以在性能测试和分析中非常有用，帮助开发者了解代码块的执行效率。
- `ticker.py` 文件的作用是提供一个稳定的接口来获取当前时间，以便在测试中测量持续时间。通过考虑 `freezegun` 的存在，它确保了即使在时间被冻结的情况下，插件也能正常工作。这使得 `pytest-durations` 插件更加灵活和可靠，可以在不同的测试环境中使用。
- `options.py` 文件提供了命令行选项的添加和插件的配置逻辑。通过这些选项，用户可以控制插件的行为，例如显示最慢的测试数量和设置最小持续时间阈值。如果使用了 `pytest-xdist` 插件，它还会自动调整以支持分布式测试环境。
- `reporting.py` 文件包含了生成 `pytest-durations` 插件报告所需的所有逻辑。它提供了灵活的方式来选择和排序报告中的数据，并能够以一种格式化的方式展示这些数据。通过这些函数，插件能够生成一个清晰的性能报告，帮助用户识别测试中的性能瓶颈。
- `xdist.py` 文件确保了当使用 `pytest-xdist` 进行分布式测试时，`pytest-durations` 插件能够正确地收集和合并来自不同工作进程的测量数据。通过 `PytestDurationXdistMixin` 类，插件可以在测试会话结束时将数据发送到主进程，并在工作节点断开连接时合并数据，从而提供完整的测试持续时间报告。
- `plugin.py` 文件实现了 `pytest-durations` 插件的主要功能，包括测量测试和 `fixture` 的执行时间，以及在测试结束后生成详细的持续时间报告。通过使用 `pytest` 的钩子系统，插件能够在 `pytest` 的生命周期中插入自己的逻辑，从而提供对测试性能的深入洞察。
