---
title: pytest hook逐一详解
date: 2999-12-30 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-16.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook逐一详解
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 文章总览

## Initialization hooks called for every plugin

第一篇：pytest hook 之 [pytest_addhooks](https://gavin-wang-note.github.io/2024/09/01/pytest_addhooks/)

第二篇：pytest hook 之 [pytest_plugin_registered](https://gavin-wang-note.github.io/2024/09/02/pytest_plugin_registered/)

第三篇：pytest hook 之 [pytest_addoption](https://gavin-wang-note.github.io/2024/09/03/pytest_addoption/)

第四篇：pytest hook 之 [pytest_configure](https://gavin-wang-note.github.io/2024/09/04/pytest_configure/)

## Bootstrapping hooks called for plugins registered early enough

第五篇：pytest hook 之 [pytest_cmdline_parse](https://gavin-wang-note.github.io/2024/09/05/pytest_cmdline_parse/)

第六篇：pytest hook 之 [pytest_cmdline_preparse](https://gavin-wang-note.github.io/2024/09/06/pytest_cmdline_preparse/)

第七篇：pytest hook 之 [pytest_cmdline_main](https://gavin-wang-note.github.io/2024/09/07/pytest_cmdline_main/)

第八篇：pytest hook 之 [pytest_load_initial_conftests](https://gavin-wang-note.github.io/2024/09/08/pytest_load_initial_conftests/)

## collection hooks

第九篇：pytest hook 之 [pytest_collection](https://gavin-wang-note.github.io/2024/09/09/pytest_collection/)

第十篇：pytest hook 之 [pytest_collection_modifyitems](https://gavin-wang-note.github.io/2024/09/10/pytest_collection_modifyitems/)

第十一篇：pytest hook 之 [pytest_collection_finish](https://gavin-wang-note.github.io/2024/09/11/pytest_collection_finish/)

第十二篇：pytest hook 之 [pytest_ignore_collect](https://gavin-wang-note.github.io/2024/09/12/pytest_ignore_collect/)

第十三篇：pytest hook 之 [pytest_collect_file](https://gavin-wang-note.github.io/2024/09/13/pytest_collect_file/)

第十四篇：pytest hook 之 [pytest_collectstart](https://gavin-wang-note.github.io/2024/09/14/pytest_collectstart/)

第十五篇：pytest hook 之 [pytest_itemcollected](https://gavin-wang-note.github.io/2024/09/15/pytest_itemcollected/)

第十六篇：pytest hook 之 [pytest_collectreport](https://gavin-wang-note.github.io/2024/09/16/pytest_collectreport/)

第十七篇：pytest hook 之 [pytest_deselected](https://gavin-wang-note.github.io/2024/09/17/pytest_deselected/)

第十八篇：pytest hook 之 [pytest_make_collect_report](https://gavin-wang-note.github.io/2024/09/18/pytest_make_collect_report/)

## Python test function related hooks

第十九篇：pytest hook 之 [pytest_pycollect_makemodule](https://gavin-wang-note.github.io/2024/09/19/pytest_pycollect_makemodule/)

第二十篇：pytest hook 之 [pytest_pycollect_makeitem](https://gavin-wang-note.github.io/2024/09/20/pytest_pycollect_makeitem/)

第二十一篇：pytest hook 之 [pytest_pyfunc_call](https://gavin-wang-note.github.io/2024/09/21/pytest_pyfunc_call/)

第二十二篇：pytest hook 之 [pytest_generate_tests](https://gavin-wang-note.github.io/2024/09/22/pytest_generate_tests/)

第二十三篇：pytest hook 之 [pytest_make_parametrize_id](https://gavin-wang-note.github.io/2024/09/23/pytest_make_parametrize_id/)

## runtest related hooks

第二十四篇：pytest hook 之 [pytest_runtestloop](https://gavin-wang-note.github.io/2024/09/24/pytest_runtestloop/)

第二十五篇：pytest hook 之 [pytest_runtest_protocol](https://gavin-wang-note.github.io/2024/09/25/pytest_runtest_protocol/)

第二十六篇：pytest hook 之 [pytest_runtest_logstart](https://gavin-wang-note.github.io/2024/09/26/pytest_runtest_logstart/)

第二十七篇：pytest hook 之 [pytest_runtest_logfinish](https://gavin-wang-note.github.io/2024/09/27/pytest_runtest_logfinish/)

第二十八篇：pytest hook 之 [pytest_runtest_setup](https://gavin-wang-note.github.io/2024/09/28/pytest_runtest_setup/)

第二十九篇：pytest hook 之 [pytest_runtest_call](https://gavin-wang-note.github.io/2024/09/29/pytest_runtest_call/)

第三十篇：pytest hook 之 [pytest_runtest_teardown](https://gavin-wang-note.github.io/2024/09/30/pytest_runtest_teardown/)

第三十一篇：pytest hook 之 [pytest_runtest_makereport](https://gavin-wang-note.github.io/2024/10/01/pytest_runtest_makereport/)

第三十二篇：pytest hook 之 [pytest_runtest_logreport](https://gavin-wang-note.github.io/2024/10/02/pytest_runtest_logreport/)

第三十三篇：pytest hook 之 [pytest_report_to_serializable](https://gavin-wang-note.github.io/2024/10/03/pytest_report_to_serializable/)

第三十四篇：pytest hook 之 [pytest_report_from_serializable](https://gavin-wang-note.github.io/2024/10/04/pytest_report_from_serializable/)

## Fixture related hooks

第三十五篇：pytest hook 之 [pytest_fixture_setup](https://gavin-wang-note.github.io/2024/10/05/pytest_fixture_setup/)

第三十六篇：pytest hook 之 [pytest_fixture_post_finalizer](https://gavin-wang-note.github.io/2024/10/06/pytest_fixture_post_finalizer/)

## test session related hooks

第三十七篇：pytest hook 之 [pytest_sessionstart](https://gavin-wang-note.github.io/2024/10/07/pytest_sessionstart/)

第三十八篇：pytest hook 之 [pytest_sessionfinish](https://gavin-wang-note.github.io/2024/10/08/pytest_sessionfinish/)

第三十九篇：pytest hook 之 [pytest_unconfigure](https://gavin-wang-note.github.io/2024/10/09/pytest_unconfigure/)

## hooks for customizing the assert methods

第四十篇：pytest hook 之 [pytest_assertrepr_compare](https://gavin-wang-note.github.io/2024/10/10/pytest_assertrepr_compare/)

第四十一篇：pytest hook 之 [pytest_assertion_pass](https://gavin-wang-note.github.io/2024/10/11/pytest_assertion_pass/)

## Hooks for influencing reporting (invoked from \_pytest_terminal)

第四十二篇：pytest hook 之 [pytest_report_header](https://gavin-wang-note.github.io/2024/10/12/pytest_report_header/)

第四十三篇：pytest hook 之 [pytest_report_collectionfinish](https://gavin-wang-note.github.io/2024/10/13/pytest_report_collectionfinish/)

第四十四篇：pytest hook 之 [pytest_report_teststatus](https://gavin-wang-note.github.io/2024/10/14/pytest_report_teststatus/)

第四十五篇：pytest hook 之 [pytest_terminal_summary](https://gavin-wang-note.github.io/2024/10/15/pytest_terminal_summary/)

第四十六篇：pytest hook 之 [pytest_warning_recorded](https://gavin-wang-note.github.io/2024/10/16/pytest_warning_recorded/)

## Hooks for influencing skipping

第四十七篇：pytest hook 之 [pytest_markeval_namespace](https://gavin-wang-note.github.io/2024/10/17/pytest_markeval_namespace/)

## error handling and internal debugging hooks

第四十八篇：pytest hook 之 [pytest_internalerror](https://gavin-wang-note.github.io/2024/10/18/pytest_internalerror/)

第四十九篇：pytest hook 之 [pytest_keyboard_interrupt](https://gavin-wang-note.github.io/2024/10/19/pytest_keyboard_interrupt/)

第五十篇：pytest hook 之 [pytest_exception_interact](https://gavin-wang-note.github.io/2024/10/20/pytest_exception_interact/)

第五十一篇：pytest hook 之 [pytest_enter_pdb](https://gavin-wang-note.github.io/2024/10/21/pytest_enter_pdb/)

第五十二篇：pytest hook 之 [pytest_leave_pdb](https://gavin-wang-note.github.io/2024/10/22/pytest_leave_pdb/)


# hook简介

`pytest`是一个强大的测试框架，它提供了一系列的`hook`函数，这些`hook`函数允许你在测试执行的不同阶段进行干预和扩展，以改变或增强测试的行为。

这些`hook`函数通常以`pytest_`为前缀，并在`conftest.py`文件或测试模块中定义。

如下图所示(点击图片可放大)，在`pytest`用例执行过程中，每个过程都有钩子函数的参与：

<img class="shadow" src="/img/in-post/pytest用例执行顺序.png" width="600">

列个大概的过程，如下图所示(点击图片可放大)：

<img class="shadow" src="/img/in-post/pytest-hook过程.jpeg" width="800">


这篇文章是总览，我将逐一介绍`pytest hook`的使用方法。

# pytest有哪些hook

以`pytest 8.0.2`为例，它有如下`hook`函数：

```shell
root@Gavin:/usr/lib/python3/dist-packages/_pytest# cat hookspec.py | grep 'def pytest_' | awk -F '(' '{{print $1}}'
def pytest_addhooks
def pytest_plugin_registered
def pytest_addoption
def pytest_configure
def pytest_cmdline_parse
def pytest_cmdline_preparse
def pytest_cmdline_main
def pytest_load_initial_conftests
def pytest_collection
def pytest_collection_modifyitems
def pytest_collection_finish
def pytest_ignore_collect
def pytest_collect_file
def pytest_collectstart
def pytest_itemcollected
def pytest_collectreport
def pytest_deselected
def pytest_make_collect_report
def pytest_pycollect_makemodule
def pytest_pycollect_makeitem
def pytest_pyfunc_call
def pytest_generate_tests
def pytest_make_parametrize_id
def pytest_runtestloop
def pytest_runtest_protocol
def pytest_runtest_logstart
def pytest_runtest_logfinish
def pytest_runtest_setup
def pytest_runtest_call
def pytest_runtest_teardown
def pytest_runtest_makereport
def pytest_runtest_logreport
def pytest_report_to_serializable
def pytest_report_from_serializable
def pytest_fixture_setup
def pytest_fixture_post_finalizer
def pytest_sessionstart
def pytest_sessionfinish
def pytest_unconfigure
def pytest_assertrepr_compare
def pytest_assertion_pass
def pytest_report_header
def pytest_report_collectionfinish
def pytest_report_teststatus
def pytest_terminal_summary
def pytest_warning_recorded
def pytest_markeval_namespace
def pytest_internalerror
def pytest_keyboard_interrupt
def pytest_exception_interact
def pytest_enter_pdb
def pytest_leave_pdb
root@Gavin:/usr/lib/python3/dist-packages/_pytest# cat hookspec.py | grep 'def pytest_' | awk -F '(' '{{print $1}}' | wc -l
52
root@Gavin:/usr/lib/python3/dist-packages/_pytest#
```
# pytest hook 分类

大致被分为以下几个阶段：初始化、配置、命令行处理、收集、运行测试、测试完成和清理等。下文按钩子的执行顺序与时机进行分类。

## 初始化阶段

```python
   def pytest_addhooks(pluginmanager):
       # 注册新的插件钩子
       pass

   def pytest_plugin_registered(plugin, manager):
       # 每次注册插件后调用
       pass
```

## 配置阶段

```python
   def pytest_addoption(parser, pluginmanager):
       # 添加命令行选项和ini配置文件值
       pass

   def pytest_configure(config):
       # 配置插件和初始化操作
       pass
```

## 命令行处理阶段

```python
   def pytest_cmdline_parse(parser):
       # 解析命令行参数
       pass

   def pytest_cmdline_preparse(config, args):
       # 在默认和插件命令行参数解析之前预处理命令行
       pass

   def pytest_cmdline_main(config):
       # 处理测试运行的主要入口函数
       pass
```

## 初步加载阶段

```python
   def pytest_load_initial_conftests(early_config, parser, args):
       # 最早加载conftest.py文件
       pass
```

## 收集阶段

```python
   def pytest_collection(session):
       # 测试用例收集阶段
       pass

   def pytest_collection_modifyitems(session, config, items):
       # 修改收集的项，如重新排序或添加/移除项目
       pass

   def pytest_collection_finish(session):
       # 收集阶段结束
       pass

   def pytest_ignore_collect(path, config):
       # 决定是否忽略某个收集项目
       pass

   def pytest_collect_file(file_path, parent):
       # 收集文件
       pass

   def pytest_collectstart(collector):
       # 开始收集某个项目
       pass

   def pytest_collectreport(report):
       # 收集归档报告
       pass

   def pytest_make_collect_report(collector):
       # 创建收集报告
       pass

   def pytest_itemcollected(item):
       # 每收集到一个项目时调用
       pass

   def pytest_deselected(items):
       # 项目取消选择时调用
       pass

   def pytest_pycollect_makemodule(module_path, parent):
       # 创建一个模块收集器
       pass

   def pytest_pycollect_makeitem(collector, name, obj):
       # 创建收集项目
       pass
```

## 测试生成阶段


```python

   def pytest_generate_tests(metafunc):
       # 动态生成测试用例
       pass

   def pytest_make_parametrize_id(config, val):
       # 用于生成参数化的测试标识符
       pass
```

## 运行测试阶段


```python
   def pytest_runtestloop(session):
       # 测试运行循环
       pass

   def pytest_runtest_protocol(item, nextitem):
       # 运行单个测试项协议
       pass

   def pytest_runtest_logstart(nodeid, location):
       # 日志记录开始
       pass

   def pytest_runtest_logfinish(nodeid, location):
       # 日志记录结束
       pass

   def pytest_runtest_setup(item):
       # 测试项设置
       pass

   def pytest_pyfunc_call(pyfuncitem):
       # 实际调用测试函数
       pass

   def pytest_runtest_call(item):
       # 执行测试项
       pass

   def pytest_runtest_teardown(item, nextitem):
       # 清理测试项
       pass

   def pytest_runtest_makereport(item, call):
       # 制作测试报告
       pass

   def pytest_runtest_logreport(report):
       # 日志记录测试报告
       pass

   def pytest_report_to_serializable(report):
       # 报告序列化
       pass

   def pytest_report_from_serializable(config, data):
       # 从序列化数据中生成报告
       pass
```

## fixture阶段

```python
   def pytest_fixture_setup(fixturedef, request):
       # 设置fixture
       pass

   def pytest_fixture_post_finalizer(fixturedef, request):
       # fixture最终清理阶段后的操作
       pass
```

## 会话生命周期阶段

```python
   def pytest_sessionstart(session):
       # 会话开始
       pass

   def pytest_sessionfinish(session, exitstatus):
       # 会话结束
       pass

   def pytest_unconfigure(config):
       # 解除配置并清理资源
       pass
```

## 断言阶段


```python
    def pytest_assertrepr_compare(config, op, left, right):
        # 断言比较表示
        pass

    def pytest_assertion_pass(item, lineno, orig, expl):
        # 断言通过
        pass
```

## 报告阶段


```python
    def pytest_report_header(config):
        # 报告前的头部信息
        pass

    def pytest_report_collectionfinish(config, startdir, items):
        # 收集结束时的报告信息
        pass

    def pytest_report_teststatus(report, config):
        # 测试状态的报告
        pass

    def pytest_terminal_summary(terminalreporter, exitstatus):
        # 终端汇总和总结
        pass
```

## 警告和内部错误、交互阶段


```python

    def pytest_warning_recorded(warning_message, nodeid, location):
        # 记录警告
        pass

    def pytest_markeval_namespace(config):
        # 评估mark表达式的命名空间
        pass

    def pytest_internalerror(excrepr, excinfo):
        # 处理内部错误
        pass

    def pytest_keyboard_interrupt(excinfo):
        # 处理键盘中断
        pass

    def pytest_exception_interact(node, call, report):
        # 交互异常
        pass

    def pytest_enter_pdb(config, traceback, excinfo):
        # 进入PDB调试器
        pass

    def pytest_leave_pdb(config, traceback, excinfo):
        # 离开PDB调试器
        pass
```

# 钩子函数解释

* pytest_addhooks: 在插件钩子系统注册新的钩子。
* pytest_plugin_registered: 每次新插件注册时被调用。
* pytest_addoption: 用于增加命令行参数和配置选项。
* pytest_configure: 在测试运行开始时配置所有插件和初始化。
* pytest_cmdline_parse: 解析命令行参数。
* pytest_cmdline_preparse: 在命令行参数解析之前进行预处理。
* pytest_cmdline_main: 处理测试运行的主要入口函数。
* pytest_load_initial_conftests: 最早加载conftest.py文件。
* pytest_collection: 表示开始收集测试用例。
* pytest_collection_modifyitems: 修改或筛选已经收集的测试项。
* pytest_collection_finish: 收集阶段结束时被调用。
* pytest_ignore_collect: 决定是否忽略某个路径的收集。
* pytest_collect_file: 收集指定文件中的测试项。
* pytest_collectstart: 收集一个项目的开始阶段。
* pytest_collectreport: 报告收集结果。
* pytest_make_collect_report: 创建收集的报告对象。
* pytest_itemcollected: 每收集到一个项目时被调用。
* pytest_deselected: 某些项目被取消选择时被调用。
* pytest_pycollect_makemodule: 创建模块收集器。
* pytest_pycollect_makeitem: 创建具体的测试项。
* pytest_generate_tests: 动态生成测试用例。
* pytest_make_parametrize_id: 生成参数化测试用例的标识符。
* pytest_runtestloop: 测试运行循环。
* pytest_runtest_protocol: 运行单个测试项的协议。
* pytest_runtest_logstart: 记录测试开始日志。
* pytest_runtest_logfinish: 记录测试结束日志。
* pytest_runtest_setup: 设置测试用例。
* pytest_pyfunc_call: 实际调用测试函数。
* pytest_runtest_call: 执行测试用例。
* pytest_runtest_teardown: 清理测试用例。
* pytest_runtest_makereport: 制作每个测试阶段的报告。
* pytest_runtest_logreport: 记录测试报告日志。
* pytest_report_to_serializable: 将报告对象转换为可序列化格式。
* pytest_report_from_serializable: 从可序列化格式恢复报告对象。
* pytest_fixture_setup: 设置fixture。
* pytest_fixture_post_finalizer: fixture最终清理阶段后的操作。
* pytest_sessionstart: 会话开始。
* pytest_sessionfinish: 会话结束。
* pytest_unconfigure: 解除配置并清理资源。
* pytest_assertrepr_compare: 断言比较表示。
* pytest_assertion_pass: 断言通过。
* pytest_report_header: 报告前的头部信息。
* pytest_report_collectionfinish: 收集结束时的报告信息。
* pytest_report_teststatus: 测试状态的报告。
* pytest_terminal_summary: 终端汇总和总结。
* pytest_warning_recorded: 记录警告。
* pytest_markeval_namespace: 评估mark表达式的命名空间。
* pytest_internalerror: 处理内部错误。
* pytest_keyboard_interrupt: 处理键盘中断。
* pytest_exception_interact: 交互异常。
* pytest_enter_pdb: 进入PDB调试器。
* pytest_leave_pdb: 离开PDB调试器。


# pytest Hooks 功能、使用场景和注意点

| Hook 名称                    | 功能描述                                                         | 使用场景                                                     | 注意点                                                       |
|------------------------------|------------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| `pytest_addhooks`            | 增加插件所需要的 hooks                                           | 用于自定义插件开发时增加新的 hooks                           | 需要深刻理解 hooks 的管理机制                                 |
| `pytest_plugin_registered`   | 插件被注册时调用                                                 | 可用于记录插件的加载                                         | 确认插件注册逻辑无循环引用                                   |
| `pytest_addoption`           | 增加自定义命令行选项                                             | 用于提供额外的命令行参数                                     | 确保命令行参数的名称和描述具有唯一性                         |
| `pytest_configure`           | 在会话配置时调用                                                 | 用于配置初始化，设置全局变量                                 | 必须在 `pytest_sessionstart` 前调用                       |
| `pytest_cmdline_parse`       | 命令行解析完成后调用                                             | 用于在命令行参数解析后添加自定义逻辑                         | 解析逻辑应兼容所有合法命令行参数                             |
| `pytest_cmdline_preparse`    | 命令行初始解析之前调用                                           | 可在参数解析之前进行预处理                                   | 避免破坏命令行标准参数                                       |
| `pytest_cmdline_main`        | 主命令行解析后立即调用                                           | 可对最终命令行参数进行调整                                   | 确保调整的参数能被预期的函数识别                             |
| `pytest_load_initial_conftests` | 装载初始 `conftest.py` 文件                                     | 用于初始化 `conftest.py` 配置文件                            | 确保 `conftest.py` 文件路径及加载顺序正确                     |
| `pytest_collection`          | 开始收集测试项目调用                                             | 用于收集测试用例前的准备工作                                 | 确保收集逻辑无副作用                                         |
| `pytest_collection_modifyitems` | 收集到测试项目后调用可修改测试集合                             | 用于动态过滤、排序测试用例                                   | 确保修改测试集合的逻辑无副作用                               |
| `pytest_collection_finish`   | 收集测试项目完成后调用                                           | 收集完成后的清理和日志记录                                   | 确保收集完成的状态一致                                       |
| `pytest_ignore_collect`      | 某个路径被忽略时调用                                             | 用于过滤掉不需要的测试文件                                   | 确保过滤路径完全覆盖所需范围                                 |
| `pytest_collect_file`        | 收集文件时调用                                                   | 用于自定义文件收集逻辑                                       | 确保路径处理符合预期                                         |
| `pytest_collectstart`        | 开始收集某个项目时调用                                           | 可用于在特定目录或模块开始时的初始化工作                     | 防止无限循环收集                                             |
| `pytest_itemcollected`       | 每个测试项目被收集到时调用                                       | 用于记录收集到的测试用例                                     | 在收集项目时避免耗时操作                                     |
| `pytest_collectreport`       | 收集报告生成时调用                                               | 用于处理收集报告                                             | 确保报告生成逻辑与期望一致                                   |
| `pytest_deselected`          | 测试项目被过滤掉时调用                                           | 用于记录被过滤掉的测试项目                                   | 防止误删关键测试用例                                         |
| `pytest_make_collect_report` | 创建收集报告时调用                                               | 用于生成自定义收集报告                                       | 确保报告内容充分反映收集过程                                 |
| `pytest_pycollect_makemodule` | 创建 Python 模块收集项目                                         | 用于自定义模块收集逻辑                                       | 确保模块的合法性                                             |
| `pytest_pycollect_makeitem`  | 创建 Python 测试项目                                             | 用于自定义测试项目的创建逻辑                                 | 确保项目收集逻辑满足预期                                     |
| `pytest_pyfunc_call`         | 调用测试函数时调用                                               | 用于自定义测试函数调用行为                                   | 确保调用逻辑没有副作用                                       |
| `pytest_generate_tests`      | 动态生成测试用例                                                 | 用于参数化测试生成测试用例                                   | 确保生成的测试用例符合命名规则                               |
| `pytest_make_parametrize_id` | 生成参数化的 id                                                   | 用于生成更具可读性的参数化 id                                | 保证参数化 id 的唯一性                                       |
| `pytest_runtestloop`         | 测试运行主循环                                                   | 用于修改或增强测试运行循环                                   | 确保自定义逻辑不破坏测试流程                                 |
| `pytest_runtest_protocol`    | 每个测试用例的运行协议                                           | 用于控制单个测试用例的运行过程                               | 确保测试运行协议的完整性                                     |
| `pytest_runtest_logstart`    | 每个测试用例开始时的日志记录                                     | 用于记录测试用例开始执行信息                                 | 确保日志格式与系统一致                                       |
| `pytest_runtest_logfinish`   | 每个测试用例结束时的日志记录                                     | 用于记录测试用例结束执行信息                                 | 确保结束日志与开始日志匹配                                   |
| `pytest_runtest_setup`       | 测试用例运行前                                                 | 用于测试环境的准备工作                                       | 确保所有前置条件都已配置完毕                                 |
| `pytest_runtest_call`        | 测试用例运行时调用                                               | 用于自定义测试用例运行逻辑                                   | 确保运行逻辑没有副作用                                       |
| `pytest_runtest_teardown`    | 测试结束后的清理工作                                             | 用于清理测试环境以及资源回收                                 | 确保清理确实完成且无副作用                                   |
| `pytest_runtest_makereport`  | 生成测试用例的运行报告                                           | 用于生成自定义测试报告                                       | 确保报告内容准确反映测试结果                                 |
| `pytest_runtest_logreport`   | 测试用例完成时的日志记录                                         | 用于记录测试用例的最终状态                                   | 确保日志详细记录测试结果                                     |
| `pytest_report_to_serializable` | 将报告对象序列化                                                 | 用于报告多进程、多主机环境下的传输                           | 确保序列化格式的一致性                                       |
| `pytest_report_from_serializable` | 从序列化对象还原报告                                             | 用于报告多进程、多主机环境下的还原                           | 确保反序列化格式的一致性                                     |
| `pytest_fixture_setup`       | 固件被设置时调用                                                 | 用于自定义固件设置逻辑                                       | 确保固件设置无副作用                                         |
| `pytest_fixture_post_finalizer` | 固件最后一个 finalizer 运行后调用                                | 用于自定义固件后处理逻辑                                     | 确保固件后处理无副作用                                       |
| `pytest_sessionstart`        | 测试会话启动时调用                                               | 用于初始化测试会话                                           | 确保会话启动逻辑的唯一性                                     |
| `pytest_sessionfinish`       | 测试会话结束时调用                                               | 用于清理测试会话资源                                         | 确保所有资源都已被正确释放                                   |
| `pytest_unconfigure`         | 测试会话完全结束时调用                                           | 用于配置文件和内存的最终清理                                 | 确保所有配置和内存都已被正确清理                             |
| `pytest_assertrepr_compare`  | 断言比较时调用                                                   | 用于自定义断言比较信息                                       | 确保断言信息的详细和准确                                     |
| `pytest_assertion_pass`      | 当断言通过时调用                                                 | 用于记录成功断言的日志                                       | 可以选择性记录成功断言                                       |
| `pytest_report_header`       | 生成测试报告的头部信息                                           | 用于自定义测试报告头部                                       | 确保头部信息的清晰和准确                                     |
| `pytest_report_collectionfinish` | 在测试集合完成后生成报告头部信息                                | 增强报告内容，确保收集过程的完整性                          | 确保报告准确反映测试集合的实际状态                           |
| `pytest_report_teststatus`   | 修改或增加测试状态信息                                           | 自定义测试状态，以更好地符合项目需求                         | 确保测试状态与实际一致，避免误导                             |
| `pytest_terminal_summary`    | 生成测试会话的最终总结报告                                       | 统一输出测试结果，提供整体视图                               | 确保报告内容的全面和准确                                     |
| `pytest_warning_recorded`    | 记录测试中出现的警告信息                                         | 收集、记录或处理测试警告                                     | 确保警告信息的完整记录，避免遗漏重要警告                     |
| `pytest_markeval_namespace`  | 自定义标记表达式解析命名空间                                     | 定义新的标记规则和解析逻辑                                   | 确保新规则符合项目的实际需求                                 |
| `pytest_internalerror`       | 捕获 pytest 框架自身的内部错误                                   | 记录和处理 pytest 内部错误                                   | 捕获到内部错误时，确保不会影响其他测试流程                   |
| `pytest_keyboard_interrupt`  | 处理键盘中断事件                                                 | 可用于处理 Ctrl+C 中断并进行善后处理                         | 确保中断事件处理不影响已完成的测试结果                       |
| `pytest_exception_interact`  | 在测试过程中抛出异常时与之交互                                   | 捕获测试中异常，提供交互式调试或日志记录                     | 确保异常信息的详细记录，便于后续分析处理                     |
| `pytest_enter_pdb`           | 进入 pdb 调试模式时调用                                           | 预设调试环境，打印调试信息                                   | 确保调试信息的详细和准确，可以有效指导问题定位               |
| `pytest_leave_pdb`           | 离开 pdb 调试模式时调用                                           | 清理调试状态，记录调试结束信息                               | 确保调试状态的清理正确，避免影响后续测试                     |

