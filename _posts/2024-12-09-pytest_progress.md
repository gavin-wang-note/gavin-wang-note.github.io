---
title: 测试用例进度展示pytest_progress源码解读
date: 2024-12-09 23:00:00
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
summary: 测试用例执行过程中进度的展示，pytest_progress源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_progress` 插件旨在改进 `pytest` 的终端输出，显示测试运行的进度以及测试通过、失败、跳过等统计信息。

本文是对此插件核心代码 `pytest_progress.py` 文件的一点解析。

如需了解此插件的更多信息，请访问[官网](https://pypi.org/project/pytest-progress/)。

# 源码解读

源码下载到本地解压后展示如下：

```shell
root@Gavin:~/pytest_plugin/pytest_progress-1.3.0# ll
total 52
drwxrwxrwx 3 root root 4096 Jul 13 14:05 ./
drwxr-xr-x 9 root root 4096 Jul 13 14:05 ../
-rw-rw-rw- 1 root root 1085 Jun 18 17:22 LICENSE
-rw-rw-rw- 1 root root   89 Jun 18 17:22 MANIFEST.in
-rw-rw-rw- 1 root root 2145 Jun 18 17:29 PKG-INFO
drwxrwxrwx 2 root root 4096 Jun 18 17:29 pytest_progress.egg-info/
-rw-rw-rw- 1 root root 7891 Jun 18 17:25 pytest_progress.py
-rw-rw-rw- 1 root root 1016 Jun 18 17:28 README.rst
-rw-rw-rw- 1 root root   74 Jun 18 17:29 setup.cfg
-rw-rw-rw- 1 root root 1816 Jun 18 17:26 setup.py
-rw-rw-rw- 1 root root  595 Jun 18 17:22 test_progress_report.py
-rw-rw-rw- 1 root root    7 Jun 18 17:26 version.txt
root@Gavin:~/pytest_plugin/pytest_progress-1.3.0#
```
核心文件是`pytest_progress.py`，此文件的解读介绍参见下文。

## 导入模块

```python
import pytest
from _pytest.terminal import TerminalReporter
```

- **`pytest`**：导入 pytest 库。
- **`TerminalReporter`**：导入 pytest 提供的终端报告模块。

## 处理测试收集

```python
def pytest_collection_finish(session):
    terminal_reporter = session.config.pluginmanager.getplugin('terminalreporter')
    if terminal_reporter:
        terminal_reporter.tests_count = len(session.items)
```

- **`pytest_collection_finish(session)`**：在测试收集阶段结束后调用。
- 获取`terminalreporter`插件实例，并记录所有收集到的测试项目数量。
- **`terminal_reporter.tests_count`**：存储测试用例总数。

## 处理xdist

```python
try:
    import xdist
except ImportError:
    pass
else:
    from distutils.version import LooseVersion
    xdist_version = LooseVersion(xdist.__version__)
    if xdist_version >= LooseVersion("1.14"):
        def pytest_xdist_node_collection_finished(node, ids):
            terminal_reporter = node.config.pluginmanager.getplugin('terminalreporter')
            if terminal_reporter:
                terminal_reporter.tests_count = len(ids)
```

- 处理平台扩展 `xdist` 插件，用于分布式测试。
- **`pytest_xdist_node_collection_finished(node, ids)`**：对于每个分布式节点，记录节点上的测试用例数量。

## 添加命令行选项

```python
def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption('--showprogress', '--show-progress',
                    action="count",
                    default=0,
                    dest="progress",
                    help="Prints test progress on the terminal.")

    group.addoption('--skip-summary',
                    action="store_false",
                    default=True,
                    dest="display_summary",
                    help="Skip summary of failures and errors")
```

- **`pytest_addoption(parser)`**：添加命令行选项。
- **`--showprogress`**：用于显示测试进度。
- **`--skip-summary`**：跳过显示失败和错误摘要。

## 配置插件

```python
@pytest.mark.trylast
def pytest_configure(config):
    progress = config.option.progress

    if progress and not getattr(config, 'slaveinput', None):
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        instaprogress_reporter = ProgressTerminalReporter(standard_reporter)

        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(instaprogress_reporter, 'terminalreporter')
```

- **`pytest_configure(config)`**：在 pytest 配置阶段调用插件。
- 检查是否启用进度显示，如果启用则替换默认的 `terminal reporter`。

## 定义ProgressTerminalReporter类

```python
class ProgressTerminalReporter(TerminalReporter):
    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)
        self._tw = reporter._tw
        self.tests_count = 0
        self.tests_taken = 0
        self.pass_count = 0
        self.fail_count = 0
        self.skip_count = 0
        self.xpass_count = 0
        self.xfail_count = 0
        self.error_count = 0
        self.rerun_count = 0
        self.executed_nodes = []
        self.passed_nodes = []
        self.failed_nodes = []
        self.rerun_nodes = []

    def append_rerun(self, report):
        ...
    def append_pass(self, report):
        ...
    def append_failure(self, report):
        ...
    def append_error(self):
        ...
    def append_skipped(self, report):
        ...
```

- **`__init__`**：初始化测试统计信息变量。
- **`append_rerun`**：处理测试重试情况。
- **`append_pass`**：处理测试通过情况。
- **`append_failure`**：处理测试失败情况。
- **`append_error`**：处理测试错误情况。
- **`append_skipped`**：处理测试跳过情况。

## 报告测试状态

```python
    @pytest.mark.tryfirst
    def pytest_report_teststatus(self, report):
        if report.passed and report.when == "call":
            if report.nodeid not in self.executed_nodes:
                self.append_pass(report)
                self.executed_nodes.append(report.nodeid)

        elif hasattr(report, 'rerun'):
            self.append_rerun(report)

        elif report.failed:
            if report.nodeid not in self.executed_nodes:
                self.append_failure(report)
                self.executed_nodes.append(report.nodeid)

        elif report.skipped:
            if report.nodeid not in self.executed_nodes:
                self.append_skipped(report)
                self.executed_nodes.append(report.nodeid)

        if report.when in ("teardown"):
            status = (self.tests_taken, self.tests_count, self.pass_count, self.fail_count,
                      self.skip_count, self.xpass_count, self.xfail_count, self.error_count, self.rerun_count)
            msg = "%d of %d completed, %d Pass, %d Fail, %d Skip, %d XPass, %d XFail, %d Error, %d ReRun" % (status)
            self.write_sep("_", msg)
```

- **`pytest_report_teststatus(self, report)`**：在每个测试用例完成后调用，更新测试状态统计信息，并在终端显示。

## 其他报告函数

```python
    def pytest_collectreport(self, report):
        TerminalReporter.pytest_collectreport(self, report)
        if report.failed:
            self.rewrite("")
            self.print_failure(report)

    def pytest_runtest_logreport(self, report):
        TerminalReporter.pytest_runtest_logreport(self, report)
        if (report.failed or report.outcome == "rerun") and not hasattr(report, 'wasxfail'):
            if self.verbosity <= 0:
                self._tw.line()
            self.print_failure(report)

    def summary_failures(self):
        if self.config.option.display_summary:
            super().summary_failures()

    def summary_errors(self):
        if self.config.option.display_summary:
            super().summary_errors()

    def print_failure(self, report):
        if self.config.option.tbstyle != "no":
            if self.config.option.tbstyle == "line":
                line = self._getcrashline(report)
                self.write_line(line)
            else:
                msg = self._getfailureheadline(report)
                if not hasattr(report, 'when'):
                    msg = "ERROR collecting " + msg
                elif report.when == "setup":
                    msg = "ERROR at setup of " + msg
                elif report.when == "teardown":
                    msg = "ERROR at teardown of " + msg
                self.write_sep("_", msg)
                if not self.config.getvalue("usepdb"):
                    self._outrep_summary(report)
```

- **`pytest_collectreport(self, report)`**：收集阶段调用，显示收集报告错误。
- **`pytest_runtest_logreport(self, report)`**：记录测试日志，显示运行中的失败。
- **`summary_failures(self)`** 和 **`summary_errors(self)`**：在配置启用时显示测试失败和错误的摘要。
- **`print_failure(self, report)`**：打印详细的测试失败信息。

# 总结

`pytest_progress` 插件的主要功能是增强 `pytest` 的终端输出，包括：
- **进度显示**：在测试运行过程中显示进度信息。
- **统计信息**：显示各类测试状态的统计信息（通过、失败、重新运行等）。
- **改进的报告输出**：即时显示收集和执行阶段的错误。

通过这些增强功能，`pytest_progress` 提高了测试运行的可见性，使开发人员可以更快速地了解测试进度和结果。
