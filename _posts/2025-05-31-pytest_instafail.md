---
title: 测试用例依赖之pytest-instafail源码解读
date: 2025-05-31 22:00:00
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
summary: 试用例依赖之pytest-instafail源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述



`pytest-instafail` 插件能够在测试运行时立即显示失败的测试而不是等待整个测试会话完成。这对于长时间运行的测试会话特别有用，因为你能更快地获得失败的反馈，并开始针对性地解决问题。

# 安装 pytest-instafail

通过 `pip` 安装 `pytest-instafail`：

```sh
pip install pytest-instafail
```

# 主要特性

- **实时反馈**：测试失败时会立即显示输出，而不是在全部测试执行完毕后统一显示。
- **节省时间**：开发者可以在等待全部测试执行完毕前就开始分析和修复出现的问题。
- **易于集成**：只需通过简单的命令行参数启用，无需对已有的测试用例进行任何修改。

# 使用场景

- **开发过程中**：在开发过程中快速发现测试失败，以便能够快速修复，减少等待时间。
- **持续集成**：在 `CI` 系统中使用，可以更早地在日志中看到失败的测试，而不必等到整个测试流程完成。
- **集成测试或系统测试**：这些测试往往运行时间较长，有时候甚至需要数小时，实时反馈能够显著提高效率。

# 示例和注解

安装 `pytest-instafail` 后，你可以在命令行中使用 `--instafail` 参数来启动它：

```sh
pytest --instafail
```

当你运行此命令时，每当单个测试失败，你会立即在控制台上看到输出，包括失败的断言和堆栈跟踪。

不需要在你的测试代码中添加特定的装饰器或标记，`pytest-instafail` 将自动应用于所有测试。

# 注意事项

- **输出管理**：如果测试用例很多且失败率较高，实时输出可能导致大量的日志信息，这有时会使得控制台输出看起来比较混乱。
- **日志记录**：在 `CI` 工具中使用时，需要确保实时输出不会干扰或覆盖测试结束后的完整报告。
- **与其他插件的潜在冲突**：一些修改测试输出行为的插件可能与 `pytest-instafail` 冲突。

`pytest-instafail` 是提高实时测试反馈效率的好工具，它可以帮助你尽可能快地发现问题，并开始进行故障排除。然而，对于某些情况，可能需要调整 `CI` 系统的日志收集配置，以确保失败的测试输出不会被误解或忽略。



# 源码说明



## 目录结构

从[官网](https://pypi.org/project/pytest-instafail/)下载源码解压：

```shell
root@Gavin:~/pytest_plugin/pytest-instafail-0.5.0# ll
total 56
drwxr-xr-x  3  501 staff 4096 Apr  1  2023 ./
drwxr-xr-x 20 root root  4096 Jul 23 17:41 ../
-rw-r--r--  1  501 staff 1651 Apr  1  2023 CHANGES.rst
-rw-r--r--  1  501 staff 1438 Apr  1  2023 LICENSE
-rw-r--r--  1  501 staff   98 Apr  1  2023 MANIFEST.in
-rw-r--r--  1  501 staff 2144 Apr  1  2023 PKG-INFO
drwxr-xr-x  2  501 staff 4096 Apr  1  2023 pytest_instafail.egg-info/
-rw-r--r--  1  501 staff 3231 Apr  1  2023 pytest_instafail.py
-rw-r--r--  1  501 staff 1001 Apr  1  2023 README.rst
-rw-r--r--  1  501 staff   75 Apr  1  2023 setup.cfg
-rw-r--r--  1  501 staff 1434 Apr  1  2023 setup.py
-rw-r--r--  1  501 staff 9109 Apr  1  2023 test_instafail.py
root@Gavin:~/pytest_plugin/pytest-instafail-0.5.0# 
```



核心文件`pytest_instafail.py`。



## 源码解读



### pytest_addoption方法



```python
import pytest
from _pytest.terminal import TerminalReporter


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group._addoption(
        '--instafail', action="store_true", dest="instafail", default=False,
        help=(
            "show failures and errors instantly as they occur (disabled by "
            "default)."
        )
    )
```



这段代码是 `pytest` 插件中添加命令行选项的典型例子，特别是用于自定义终端报告的行为。



#### 代码说明

1. **导入依赖**:
   - `import pytest`: 导入 `pytest`模块，以便使用 `pytest`提供的功能。
   - `from _pytest.terminal import TerminalReporter`: 从 `pytest` 的内部模块中导入 `TerminalReporter` 类，这可能用于自定义终端报告的输出。

2. **添加命令行选项**:
   - `def pytest_addoption(parser)`: 这是一个钩子函数，当 `pytest`启动时会被调用，允许插件向 `pytest` 添加额外的命令行选项。

3. **创建选项组**:
   - `group = parser.getgroup("terminal reporting", "reporting", after="general")`: 使用 `parser` 创建一个新的命令行选项组，名为 "terminal reporting"，并将其归类在 "reporting" 下，位置在 "general" 组之后。

4. **添加新选项**:
   - `group._addoption(...)`: 向 "terminal reporting" 组添加一个新的命令行选项 `--instafail`：
     - `action="store_true"`: 这个选项是一个开关，当它被设置时，会存储 `True`。
     - `dest="instafail"`: 设置选项的目的地，即选项的属性名，这里是 `instafail`。
     - `default=False`: 设置选项的默认值为 `False`。
     - `help=(...)`: 提供选项的帮助信息，说明其作用。

5. **选项的作用**:
   - `--instafail` 选项允许用户在测试执行过程中即时显示失败和错误。如果测试用例失败或抛出错误，这些信息会立即在终端上显示，而不是等到所有测试用例执行完毕后才显示。

6. **即时反馈**:
   - 启用 `--instafail` 选项后，`pytest`会在测试运行时提供即时反馈，这有助于快速发现和解决问题，提高调试效率。

#### 示例用法

在命令行中使用 `--instafail` 选项运行 `pytest`：

```bash
pytest --instafail
```

这将使得 `pytest`在测试执行过程中，一旦发生失败或错误，就会立即在终端上显示相关信息，而不是等待所有测试完成后。



### pytest_configure方法



```python
@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if hasattr(config, 'workerinput'):
        return  # xdist worker, we are already active on the master
    if config.option.instafail and config.pluginmanager.hasplugin('terminalreporter'):
        # Get the standard terminal reporter plugin...
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        instafail_reporter = InstafailingTerminalReporter(standard_reporter)

        # ...and replace it with our own instafailing reporter.
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(instafail_reporter, 'terminalreporter')
```



#### 代码说明

1. **钩子装饰器**:
   - `@pytest.hookimpl(trylast=True)`: 这个装饰器将函数注册为 `pytest` 的钩子，`trylast=True` 参数表示这个钩子将在其他钩子之后尝试执行。

2. **配置钩子函数**:
   - `def pytest_configure(config)`: 定义了一个钩子函数，它接收一个参数 `config`，表示 `pytest`的配置对象。

3. **检查是否为 xdist 工作进程**:
   - `if hasattr(config, 'workerinput'):`: 如果配置对象有 `workerinput` 属性，表示当前运行的是 `pytest-xdist` 插件的工作进程，因此不需要执行主进程特有的配置。

4. **检查 `--instafail` 选项**:
   - `if config.option.instafail`: 检查是否启用了 `--instafail` 选项。

5. **检查 `terminalreporter` 插件**:
   - `config.pluginmanager.hasplugin('terminalreporter')`: 检查 `pytest`是否加载了 `terminalreporter` 插件。

6. **获取并替换终端报告器**:
   - `standard_reporter = config.pluginmanager.getplugin('terminalreporter')`: 获取标准的终端报告器插件实例。
   - `instafail_reporter = InstafailingTerminalReporter(standard_reporter)`: 创建 `InstafailingTerminalReporter` 类的实例，传入标准的终端报告器作为参数，这可能是一个自定义类，用于实现即时失败反馈的功能。

7. **注销并注册新的报告器**:
   - `config.pluginmanager.unregister(standard_reporter)`: 注销标准的终端报告器。
   - `config.pluginmanager.register(instafail_reporter, 'terminalreporter')`: 注册新的即时失败报告器，替换原来的终端报告器。

#### 代码逻辑

- 该钩子函数在 `pytest`配置阶段被调用，用于根据 `--instafail` 选项配置即时失败反馈功能。
- 如果启用了 `--instafail` 并且 `pytest`加载了 `terminalreporter` 插件，它会创建一个新的报告器实例，该实例能够提供即时的失败和错误反馈。
- 然后，它注销了原来的终端报告器，并注册了新的报告器，这样在测试执行过程中，任何失败或错误都会立即显示在终端上。

`pytest`将使用自定义的 `InstafailingTerminalReporter` 报告器来立即显示测试过程中的失败和错误，而不是在所有测试完成后统一报告。这有助于开发者快速定位问题，提高调试效率。



### 类InstafailingTerminalReporter



```python
class InstafailingTerminalReporter(TerminalReporter):
    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)
        self._tw = reporter._tw

    def pytest_collectreport(self, report):
        # Show errors occurred during the collection instantly.
        TerminalReporter.pytest_collectreport(self, report)
        if report.failed:
            if self.isatty:
                self.rewrite('')  # erase the "collecting"/"collected" message
            self.print_failure(report)

    def pytest_runtest_logreport(self, report):
        # Show failures and errors occurring during running a test
        # instantly.
        TerminalReporter.pytest_runtest_logreport(self, report)
        if report.failed and not hasattr(report, 'wasxfail'):
            if self.verbosity <= 0:
                self._tw.line()
            self.print_failure(report)

    def summary_failures(self):
        # Prevent failure summary from being shown since we already
        # show the failure instantly after failure has occurred.
        pass

    def summary_errors(self):
        # Prevent error summary from being shown since we already
        # show the error instantly after error has occurred.
        pass

    def print_failure(self, report):
        if self.config.option.tbstyle != "no":
            if self.config.option.tbstyle == "line":
                line = self._getcrashline(report)
                self.write_line(line)
            else:
                msg = self._getfailureheadline(report)
                if report.when == "collect":
                    msg = "ERROR collecting " + msg
                elif report.when == "setup":
                    msg = "ERROR at setup of " + msg
                elif report.when == "teardown":
                    msg = "ERROR at teardown of " + msg
                self.write_sep("_", msg)
                if not self.config.getvalue("usepdb"):
                    self._outrep_summary(report)
```



这段代码是自定义的一个报告类，它继承自`TerminalReporter`，用于在测试过程中即时显示错误和失败信息。

1. **初始化**：
   - `__init__(self, reporter)`：构造函数接受一个`reporter`对象作为参数，并调用父类的构造函数来初始化配置。
   - `self._tw = reporter._tw`：将传入的reporter对象中的`_tw`（可能是某种文本写入器）保存为实例变量。

2. **收集报告处理**：
   - `pytest_collectreport(self, report)`：当收集阶段结束时被调用。
     - 如果报告中有失败，则立即显示这些错误。

3. **运行测试日志报告处理**：
   - `pytest_runtest_logreport(self, report)`：当某个测试用例执行完成并生成日志报告时被调用。
     - 如果报告显示有失败且没有设置预期失败属性（`xfail`），则在终端输出相应的失败信息。

4. **摘要方法重写**：
   - `summary_failures()` 和 `summary_errors()` 方法被重写为`pass`，以防止默认行为，在每个测试结束后不展示汇总的错误和故障列表，因为本类已经实现了即时显示功能。

5. **打印故障信息**：
   - `print_failure(self, report)`：根据配置选项确定如何展示错误或故障消息。如果启用了`traceback`风格的输出，则会打印出错误的堆栈跟踪；否则会输出一些概要信息，并判断是在哪个阶段发生的错误（例如`collect、setup、teardown`）。

6. 获取关键行或标题的方法:
    - 私有方法如 `_getcrlshline(report)` 和 `__getfailureheadline(report)`

整体来看，这个自定义的`Reporter`类在遇到任何类型的异常或者断言失败时能够提供更直观的反馈给用户。这有助于开发者快速定位问题所在，并及时进行调试修复。




# 结语



`pytest-instafail` 是一个 `pytest` 插件，它提供了即时反馈功能，在测试运行过程中立即显示失败和错误信息。

1. **实时性**：当测试用例执行失败或发生错误时，它会立刻在终端输出相关信息。
2. **详细报告**：根据配置的不同，它可以提供详细的堆栈跟踪或者错误摘要。
3. **优化体验**：通过即时展示问题而不是等到所有测试结束后再汇总，可以帮助开发者更快地定位并解决问题。
4. **自定义程度高**：用户可以通过配置选项来控制插件的行为（例如是否使用 `pdb、traceback` 的风格等）。

这个插件特别适合需要快速迭代开发的场景，因为它可以减少开发者等待整个测试套件运行完成的时间。

