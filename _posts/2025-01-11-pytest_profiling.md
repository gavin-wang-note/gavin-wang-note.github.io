---
title: 测试用例性能分析之pytest-profiling源码解读
date: 2025-01-11 22:00:00
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
summary: 测试用例性能分析之pytest-profiling源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-profiling`是`pytest`的性能剖析插件，提供表格和热图输出。它使用 `cProfile` 对测试进行剖析，使用 `pstats` 对测试进行分析；使用 `gprof2dot` 和 `dot` 生成热图。

有如下两个特点：

* 性能分析插件

`pytest`插件`pytest-profiling`是一个性能分析插件，它能够生成详细的热图和支持`gprof`的`C`扩展。该插件通过统一的构建和测试流程确保了其在不同平台上的稳定性和兼容性。

* 生成详细的热图和`C`扩展的`gprof`支持

`pytest`插件`pytest-profiling`通过其内置功能，能够生成详细的热图和`C`扩展的`gprof`支持，显著提升性能分析的效率和准确性。

# 源码目录结构

[官方](https://pypi.org/project/pytest-profiling)下载源码，解压后目录结构如下：

```shell
root@Gavin:~/pytest_plugin/pytest-profiling-1.7.0# ll
total 80
drwxr-xr-x  5  709   28  4096 May 28  2019 ./
drwxr-xr-x 12 root root  4096 Jul 16 09:36 ../
-rw-r--r--  1  709   28  6631 May 28  2019 CHANGES.md
-rw-r--r--  1  709   28  2686 May 28  2019 common_setup.py
drwxr-xr-x  3  709   28  4096 May 28  2019 docs/
-rw-r--r--  1  709   28  1064 May 28  2019 LICENSE
-rw-r--r--  1  709   28    71 May 28  2019 MANIFEST.in
-rw-r--r--  1  709   28 15658 May 28  2019 PKG-INFO
drwxr-xr-x  2  709   28  4096 May 28  2019 pytest_profiling.egg-info/
-rw-r--r--  1  709   28  4028 May 28  2019 pytest_profiling.py
-rw-r--r--  1  709   28  4357 May 28  2019 README.md
-rw-r--r--  1  709   28   158 May 28  2019 setup.cfg
-rw-r--r--  1  709   28  1512 May 28  2019 setup.py
drwxr-xr-x  4  709   28  4096 May 28  2019 tests/
-rw-r--r--  1  709   28     6 May 28  2019 VERSION
root@Gavin:~/pytest_plugin/pytest-profiling-1.7.0# tree 
.
├── CHANGES.md
├── common_setup.py
├── docs
│   └── static
│       └── profile_combined.svg
├── LICENSE
├── MANIFEST.in
├── PKG-INFO
├── pytest_profiling.egg-info
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── PKG-INFO
│   ├── requires.txt
│   ├── SOURCES.txt
│   └── top_level.txt
├── pytest_profiling.py
├── README.md
├── setup.cfg
├── setup.py
├── tests
│   ├── integration
│   │   ├── profile
│   │   │   └── tests
│   │   │       └── unit
│   │   │           ├── test_chdir.py
│   │   │           ├── test_example.py
│   │   │           └── test_long_name.py
│   │   └── test_profile_integration.py
│   └── unit
│       └── test_profile.py
└── VERSION

10 directories, 22 files
root@Gavin:~/pytest_plugin/pytest-profiling-1.7.0#
```

核心文件是`pytest_profiling.py`.

# 源码解读

`pytest-profiling` 插件提供了在 pytest 测试中进行性能分析的功能。它通过 `cProfile` 和 `pstats` 来生成和处理性能分析数据，并可以选择生成 SVG 格式的性能分析图。以下是 `pytest_profiling.py` 文件的详细解析。

## 导入模块

```python
from __future__ import absolute_import

import sys
import os
import cProfile
import pstats
import pipes
import errno
from hashlib import md5

import six
import pytest
```

- **系统和文件操作模块**：`sys`, `os`, `errno`。
- **性能分析模块**：`cProfile`, `pstats`。
- **辅助模块**：`pipes`, `md5` (用于处理文件名)。
- **兼容性模块**：`six` (兼容 `Python` 2 和 3)。

## 常量

```python
LARGE_FILENAME_HASH_LEN = 8
```

- **`LARGE_FILENAME_HASH_LEN`**：用于处理过长文件名的哈希长度。

## 清理文件名

```python
def clean_filename(s):
    forbidden_chars = set('/?<>\:*|"')
    return six.text_type("".join(c if c not in forbidden_chars and ord(c) < 127 else '_'
                                 for c in s))
```

- 这个函数的目的是清洗一个文件名字符串，移除或替换掉一些在特定操作系统中可能引起问题的特殊字符。

- `return`语句中，使用列表推导式来处理输入字符串中的每个字符：

  - 对于每个字符 c，在判断条件中做两个检查：

      1)字符是否不在之前创建的禁止字符集合中;
      2)字符的ASCII码值是否小于127。

    如果这两个条件都满足，则保留原字符；否则使用下划线 `'_'``代替该特殊字符。
- 使用空字符串连接生成的新序列，并返回结果。

在这里使用了库 `six.text_type()` ，这通常是用于确保兼容性的处理方式，在`Python` 2和3之间转换文本类型。不过在`Python 3.x`，可以直接使用原生的字符串类型而不需要这样的转换。


## Profiling 类

```python
class Profiling(object):
    svg = False
    svg_name = None
    profs = []
    combined = None

    def __init__(self, svg, dir=None):
        self.svg = svg
        self.dir = 'prof' if dir is None else dir[0]
        self.profs = []
        self.gprof2dot = os.path.abspath(os.path.join(os.path.dirname(sys.executable), 'gprof2dot'))
        if not os.path.isfile(self.gprof2dot):
            self.gprof2dot = 'gprof2dot'
```

- **`Profiling` 类**：负责性能分析的主要逻辑。
  - **初始化参数**：`svg` 指定是否生成 SVG 格式分析图；`dir` 指定存储分析数据的目录（默认为 `prof`）。
  - **`gprof2dot`**：用于生成性能分析图的工具，默认路径为 `Python` 安装目录。如找不到则假设在 `PATH` 中。

## 会话开始钩子

```python
def pytest_sessionstart(self, session):
    try:
        os.makedirs(self.dir)
    except OSError:
        pass
```

- **`pytest_sessionstart(self, session)`**：在测试会话开始时创建存储目录。

## 会话结束钩子

```python
    def pytest_sessionfinish(self, session, exitstatus):  # @UnusedVariable
        if self.profs:
            combined = pstats.Stats(self.profs[0])
            for prof in self.profs[1:]:
                combined.add(prof)
            self.combined = os.path.abspath(os.path.join(self.dir, "combined.prof"))
            combined.dump_stats(self.combined)
            if self.svg:
                self.svg_name = os.path.abspath(os.path.join(self.dir, "combined.svg"))
                t = pipes.Template()
                t.append("{} -f pstats $IN".format(self.gprof2dot), "f-")
                t.append("dot -Tsvg -o $OUT", "-f")
                t.copy(self.combined, self.svg_name)
```

这段代码是 `pytest-profiling` 插件的 `pytest_sessionfinish` 钩子实现，它是在 `pytest` 测试会话结束时调用的，详细分析如下：

### 钩子函数定义

```python
def pytest_sessionfinish(self, session, exitstatus):  # @UnusedVariable
```

`pytest_sessionfinish` 是一个钩子函数，`session` 参数代表当前的测试会话，`exitstatus` 是会话结束时的退出状态码。`@UnusedVariable` 是一个装饰器，用来标记函数参数未使用，以避免某些IDE或linter的警告。

### 检查是否有性能分析文件

```python
if self.profs:
```

这个条件判断用于检查是否已经收集了性能分析文件（`.prof` 文件）。`self.profs` 是一个列表，存储了所有测试用例生成的性能分析文件的路径。

### 创建综合的性能分析文件

```python
combined = pstats.Stats(self.profs[0])
for prof in self.profs[1:]:
    combined.add(prof)
```

如果存在性能分析文件，首先创建一个 `pstats.Stats` 对象，它将用于合并所有单独的性能分析数据。然后遍历 `self.profs` 列表，从第二个文件开始（因为第一个文件已经被用来初始化 `combined`），将每个文件的性能分析数据添加到 `combined` 对象中。

### 保存综合的性能分析数据

```python
self.combined = os.path.abspath(os.path.join(self.dir, "combined.prof"))
combined.dump_stats(self.combined)
```

将合并后的性能分析数据保存到一个名为 `combined.prof` 的文件中。使用 `os.path.abspath` 确保文件路径是绝对路径，并且使用 `os.path.join` 构建正确的文件路径。`combined.dump_stats` 方法用于将性能分析数据写入到文件。

### 生成 SVG 图形（如果启用）

```python
if self.svg:
    self.svg_name = os.path.abspath(os.path.join(self.dir, "combined.svg"))
    t = pipes.Template()
    t.append("{} -f pstats $IN".format(self.gprof2dot), "f-")
    t.append("dot -Tsvg -o $OUT", "-f")
    t.copy(self.combined, self.svg_name)
```

如果用户通过命令行选项启用了 SVG 图形生成（`--profile-svg`），则执行以下步骤：

1. 设置 ·SVG· 文件的路径。
2. 创建一个 `pipes.Template` 对象，用于构建命令行命令。
3. 使用 `append` 方法添加两个命令：第一个命令使用 `gprof2dot` 工具将性能分析数据转换为 `dot` 格式，第二个命令使用 `dot` 工具将 `dot` 格式转换为 ·SVG· 图形。
4. 使用 `copy` 方法执行构建的命令行命令，将 `combined.prof` 作为输入，生成 `combined.svg` 文件。

这段代码通过调用外部工具 `gprof2dot` 和 `dot` 来生成性能分析的可视化 `SVG` 图形，这可以帮助用户更直观地理解性能瓶颈。

注意，这需要 `gprof2dot` 和 `Graphviz` 的 `dot` 工具在系统上可用。


## 终端报告摘要钩子

```python
    def pytest_terminal_summary(self, terminalreporter):
        if self.combined:
            terminalreporter.write("Profiling (from {prof}):\n".format(prof=self.combined))
            pstats.Stats(self.combined, stream=terminalreporter).strip_dirs().sort_stats('cumulative').print_stats(20)
        if self.svg_name:
            terminalreporter.write("SVG profile in {svg}.\n".format(svg=self.svg_name))
```

这段代码是 `pytest-profiling` 插件的 `pytest_terminal_summary` 钩子实现，它在 `pytest` 测试运行结束后，在终端报告摘要时调用的，详细解析如下：

### 钩子函数定义
```python
def pytest_terminal_summary(self, terminalreporter):
```

`pytest_terminal_summary` 是一个钩子函数，`terminalreporter` 参数是一个报告器对象，它提供了一些方法来输出信息到终端。

### 检查是否存在综合的性能分析文件

```python
if self.combined:
```

这个条件判断用于检查是否已经生成了综合的性能分析文件（`combined.prof`）。如果存在，说明在测试会话中有性能分析数据被收集和合并。

### 输出性能分析摘要到终端

```python
terminalreporter.write("Profiling (from {prof}):\n".format(prof=self.combined))
```

如果存在综合的性能分析文件，使用 `terminalreporter.write` 方法输出一行文本到终端，指示性能分析数据的来源。

### 打印性能分析数据

```python
pstats.Stats(self.combined, stream=terminalreporter).strip_dirs().sort_stats('cumulative').print_stats(20)
```

接着，使用 `pstats.Stats` 类创建一个性能分析统计对象，传入综合的性能分析文件路径和 `terminalreporter` 作为输出流。然后调用几个方法来格式化和打印性能分析数据：

- `strip_dirs()`：从文件路径中移除前缀目录，使得输出更加简洁。
- `sort_stats('cumulative')`：根据累积时间对函数进行排序。
- `print_stats(20)`：打印前 20 行的性能分析数据，每行显示一个函数的信息。

### 检查是否存在 SVG 图形文件

```python
if self.svg_name:
```

如果用户启用了 SVG 图形生成，并且已经成功生成了 `SVG` 文件，`self.svg_name` 将包含该文件的路径。

### 输出 SVG 图形文件路径到终端

```python
terminalreporter.write("SVG profile in {svg}.\n".format(svg=self.svg_name))
```
如果存在 `SVG` 文件路径，使用 `terminalreporter.write` 方法输出一行文本到终端，指示 `SVG` 图形文件的位置。


## 捕获性能数据钩子

```python
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        prof_filename = os.path.abspath(os.path.join(self.dir, clean_filename(item.name) + ".prof"))
        try:
            os.makedirs(os.path.dirname(prof_filename))
        except OSError:
            pass
        prof = cProfile.Profile()
        prof.enable()
        yield
        prof.disable()
        try:
            prof.dump_stats(prof_filename)
        except EnvironmentError as err:
            if err.errno != errno.ENAMETOOLONG:
                raise

            if len(item.name) < LARGE_FILENAME_HASH_LEN:
                raise

            hash_str = md5(item.name.encode('utf-8')).hexdigest()[:LARGE_FILENAME_HASH_LEN]
            prof_filename = os.path.join(self.dir, hash_str + ".prof")
            prof.dump_stats(prof_filename)
        self.profs.append(prof_filename)
```

这段代码是 `pytest-profiling` 插件中用于捕获单个测试用例性能数据的 `pytest_runtest_protocol` 钩子函数，其作用是在每个测试用例执行前后，捕获其性能数据并保存到文件中。这样，用户就可以在测试结束后查看每个测试用例的性能分析数据，从而识别潜在的性能瓶颈。通过在测试用例执行前后启用和禁用性能分析，确保了性能数据的准确性。同时，对于文件名太长的问题，通过使用哈希值作为文件名的一部分，确保了文件能够被正确创建和保存。


### 钩子函数定义

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(self, item, nextitem):
```
`pytest_runtest_protocol` 是一个钩子函数，它在每个测试用例执行前和执行后被调用。
`item` 是当前测试用例的 `Item` 对象，`nextitem` 是下一个要执行的测试用例的 `Item` 对象。`hookwrapper=True` 参数表示这个钩子函数可以作为一个上下文管理器使用。

### 创建性能分析文件名

```python
prof_filename = os.path.abspath(os.path.join(self.dir, clean_filename(item.name) + ".prof"))
```

为当前测试用例创建一个唯一的性能分析文件名，并确保文件路径是绝对路径。`clean_filename` 函数用于清理测试用例名称中的非法字符。

### 创建性能分析文件目录

```python
try:
    os.makedirs(os.path.dirname(prof_filename))
except OSError:
    pass
```

尝试创建存储性能分析文件的目录。如果目录已经存在，忽略 `OSError` 异常。

### 创建性能分析对象并启用

```python
prof = cProfile.Profile()
prof.enable()
```

创建一个 `cProfile.Profile` 对象，并启用性能分析。

### 使用 `yield` 语句

```python
yield
```

使用 `yield` 语句暂停当前钩子函数的执行，允许测试用例 `item` 被执行。测试用例执行完成后，控制流将返回到这个 `yield` 语句。

### 禁用性能分析并保存数据

```python
prof.disable()
try:
    prof.dump_stats(prof_filename)
except EnvironmentError as err:
    if err.errno != errno.ENAMETOOLONG:
        raise

    if len(item.name) < LARGE_FILENAME_HASH_LEN:
        raise

    hash_str = md5(item.name.encode('utf-8')).hexdigest()[:LARGE_FILENAME_HASH_LEN]
    prof_filename = os.path.join(self.dir, hash_str + ".prof")
    prof.dump_stats(prof_filename)
```

测试用例执行完成后，禁用性能分析并尝试将性能数据保存到之前创建的文件中。如果发生 `EnvironmentError`，并且错误代码不是 `ENAMETOOLONG`（文件名太长），则重新抛出异常。如果是文件名太长的问题，则使用测试用例名称的 `MD5` 哈希值作为文件名的一部分，重新尝试保存性能数据。

### 将性能分析文件路径添加到列表

```python
self.profs.append(prof_filename)
```

将当前测试用例的性能分析文件路径添加到 `self.profs` 列表中，以便在测试会话结束时可以合并和处理这些文件。


## 插件行为控制钩子

```python
def pytest_addoption(parser):
    """pytest_addoption hook for profiling plugin"""
    group = parser.getgroup('Profiling')
    group.addoption("--profile", action="store_true",
                    help="generate profiling information")
    group.addoption("--profile-svg", action="store_true",
                    help="generate profiling graph (using gprof2dot and dot -Tsvg)")
    group.addoption("--pstats-dir", nargs=1,
                    help="configure the dump directory of profile data files")


def pytest_configure(config):
    """pytest_configure hook for profiling plugin"""
    profile_enable = any(config.getvalue(x) for x in ('profile', 'profile_svg'))
    if profile_enable:
        config.pluginmanager.register(Profiling(config.getvalue('profile_svg'),
                                                config.getvalue('pstats_dir')))
```

这段代码定义了 `pytest-profiling` 插件的两个主要钩子函数：`pytest_addoption` 和 `pytest_configure`。这些函数在 `pytest` 测试框架的配置和初始化阶段被调用，实现用户通过命令行选项控制 `pytest-profiling` 插件的行为，包括是否生成性能分析信息、是否生成 `SVG` 图形以及性能分析数据文件的输出目录。通过在 `pytest_configure` 钩子中注册 `Profiling` 类的实例，插件能够在测试执行过程中捕获和处理性能数据。详细解读内容如下：

### pytest_addoption 钩子函数

```python
def pytest_addoption(parser):
    """pytest_addoption hook for profiling plugin"""
    group = parser.getgroup('Profiling')
    group.addoption("--profile", action="store_true",
                    help="generate profiling information")
    group.addoption("--profile-svg", action="store_true",
                    help="generate profiling graph (using gprof2dot and dot -Tsvg)")
    group.addoption("--pstats-dir", nargs=1,
                    help="configure the dump directory of profile data files")
```

- 这个函数被调用时，`pytest` 会要求插件提供其选项配置。`parser` 对象用于添加命令行选项。
- `getgroup('Profiling')` 创建或获取一个选项组，所有与性能分析相关的命令行选项都将添加到这个组中。
- `addoption` 方法用于添加新的命令行选项：
  - `--profile`：一个布尔选项，当设置时，会生成性能分析信息。
  - `--profile-svg`：一个布尔选项，当设置时，除了生成性能分析信息外，还会生成性能分析的 `SVG` 图形，这需要 `gprof2dot` 和 `dot` 工具。
  - `--pstats-dir`：一个需要一个参数的选项，用于配置性能分析数据文件的输出目录。

### pytest_configure 钩子函数

```python
def pytest_configure(config):
    """pytest_configure hook for profiling plugin"""
    profile_enable = any(config.getvalue(x) for x in ('profile', 'profile_svg'))
    if profile_enable:
        config.pluginmanager.register(Profiling(config.getvalue('profile_svg'),
                                                config.getvalue('pstats_dir')))
```

- 这个函数在所有命令行选项被解析之后、测试开始执行之前被调用。
- `config.getvalue(x)` 方法用于获取特定命令行选项的值。
- `profile_enable` 变量是一个布尔值，当 `--profile` 或 `--profile-svg` 选项被设置时，它为 `True`。
- 如果启用了性能分析，`register` 方法被调用来注册 `Profiling` 类的实例。`Profiling` 类是 `pytest-profiling` 插件的主要逻辑类，负责生成和处理性能分析数据。
  - `config.getvalue('profile_svg')` 传递给 `Profiling` 类的构造函数，指示是否需要生成 SVG 图形。
  - `config.getvalue('pstats_dir')` 传递给 `Profiling` 类的构造函数，指示性能分析数据文件的输出目录。


# 结语

1. **插件集成**：`pytest-profiling` 通过 `pytest` 的钩子系统（如 `pytest_addoption` 和 `pytest_configure`）与 `pytest` 框架紧密集成，允许用户通过命令行选项控制插件的行为。

2. **性能数据收集**：插件在测试执行期间通过 `cProfile` 模块收集性能数据，并将这些数据保存到单独的文件中，每个测试用例对应一个 `.prof` 文件。

3. **灵活的配置**：用户可以通过命令行选项轻松配置插件，包括是否生成性能分析报告、是否生成 `SVG` 性能图，以及性能数据文件的输出目录。

4. **性能分析报告**：插件提供了详细的性能分析报告，包括函数级别的调用次数、时间消耗等，帮助用户识别性能瓶颈。

5. **可视化支持**：通过生成 `SVG` 图形，插件增强了性能数据的可读性和直观性，使得性能分析结果更加易于理解。

6. **错误处理**：源码中展示了对潜在错误的处理，例如文件名太长时的处理逻辑，确保了插件的健壮性。

总之，`pytest-profiling` 插件是测试和性能分析领域中一个实用的工具，它不仅提供了性能数据的收集和报告功能，还通过可视化手段增强了用户体验。通过源码解读，我们可以看到插件的设计思路、实现细节以及与 `pytest` 框架的交互方式，这对于希望深入了解 `pytest` 插件开发或性能分析技术的开发者来说是非常有价值的。
