---
title: 《pytest测试指南》-- 附录2 pytest hook介绍
date: 2024-06-08 23:00:00
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
summary: 《pytest测试指南》一书 附录2 pytest hook介绍
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

`pytest` 钩子（hook）函数是 `pytest` 提供的一个强大功能，它允许你在测试生命周期的特定点插入自定义代码。这样，你可以改变 `pytest` 的默认行为、增加额外的日志、生成测试报告或者实现其他复杂的测试设定。

`pytest`插件就是用一个或者多个`hook`函数，也就是钩子函数构成的。如果想要编写新的插件，或者改进现有的插件，都必须通过这个`hook`函数进行。所以想掌握`pytest`插件二次开发，必须搞定`hook`函数。

如下图所示，在`pytest`用例执行过程中，每个过程都有钩子函数的参与：

<img class="shadow" src="/img/in-post/pytest用例执行顺序-uml.png" width="600">

# 2.1 pytest hook分类

pytest中的钩子函数按功能一共分为6类：引导钩子，初始化钩子、用例收集钩子、用例执行钩子、报告钩子、调试钩子。

## 2.1.1 Bootstrapping hooks 引导钩子

引导钩子要求尽早注册插件（内部插件和 setuptools 插件）。

* pytest_load_initial_conftests(early_config,parser,args): 在命令行选项解析之前实现初始conftest文件的加载。

* pytest_load_initial_conftests(early_config, parser, args):在处理命令行参数之前，加载初始的 conftest 文件。

* pytest_cmdline_parse(pluginmanager,args): 返回一个初始化的配置对象,解析指定的args。

* pytest_cmdline_main(config): 要求执行主命令行动作。默认实现将调用configure hooks和runtest_mainloop。 

## 2.1.2 Initialization hooks 初始化钩子

初始化钩子调用插件和conftest.py文件。

* pytest_addoption(parser): 注册argparse样式的选项和ini样式的配置值，这些值在测试运行开始时被调用一次。
* pytest_addhooks(pluginmanager): 在插件注册时调用，以允许通过调用来添加新的挂钩
* pytest_configure(config): 允许插件和conftest文件执行初始配置。
* pytest_unconfigure(config): 在退出测试过程之前调用。
* pytest_sessionstart(session): 在Session创建对象之后，执行收集并进入运行测试循环之前调用。
* pytest_sessionfinish(session,exitstatus): 在整个测试运行完成后调用，就在将退出状态返回系统之前。
* pytest_plugin_registered(plugin,manager):一个新的pytest插件已注册。 

## 2.1.3 Collection hooks 测试用例收集钩子

pytest调用以下钩子函数来收集测试文件及目录。

* pytest_collection(session): 执行给定会话的收集协议。
* pytest_collect_directory(path, parent): 在遍历目录以获取集合文件之前调用。
* pytest_collect_file(path, parent) 为给定的路径创建一个收集器，如果不相关，则创建“无”。
* pytest_pycollect_makemodule(path: py._path.local.LocalPath, parent) 返回给定路径的模块收集器或无。
* pytest_pycollect_makeitem(collector: PyCollector, name: str, obj: object) 返回模块中Python对象的自定义项目/收集器，或者返回None。在第一个非无结果处停止
* pytest_generate_tests(metafunc: Metafunc) 生成（多个）对测试函数的参数化调用。
* pytest_make_parametrize_id(config: Config, val: object, argname: str) 返回val 将由@ pytest.mark.parametrize调用使用的给定用户友好的字符串表示形式，如果挂钩不知道，则返回None val。
* pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]) 在执行收集后调用。可能会就地过滤或重新排序项目。
* pytest_collection_finish(session: Session) 在执行并修改收集后调用。 

## 2.1.4 Test running (runtest) hooks 测试运行钩子

运行测试相关的钩子，接收一个pytest.Item对象。

* pytest_runtestloop(session: Session) 执行主运行测试循环（收集完成后）。
* pytest_runtest_protocol(item: Item, nextitem: Optional[Item]) 对单个测试项目执行运行测试协议。
* pytest_runtest_logstart(nodeid: str, location: Tuple[str, Optional[int], str]) 在运行单个项目的运行测试协议开始时调用。
* pytest_runtest_logfinish(nodeid: str, location: Tuple[str, Optional[int], str])在为单个项目运行测试协议结束时调用。
* pytest_runtest_setup(item: Item) 调用以执行测试项目的设置阶段。
* pytest_runtest_call(item: Item) 调用以运行测试项目的测试（调用阶段）。
* pytest_runtest_teardown(item: Item, nextitem: Optional[Item]) 调用以执行测试项目的拆卸阶段。
* pytest_runtest_makereport(item: Item, call: CallInfo[None]) 被称为为_pytest.reports.TestReport测试项目的每个设置，调用和拆卸运行测试阶段创建一个。
* pytest_pyfunc_call(pyfuncitem: Function) 调用基础测试功能。 

## 2.1.5 Reporting hooks 测试报告钩子

与会话相关，断言相关的测试报告钩子。

* pytest_collectstart(collector: Collector) 收集器开始收集。
* pytest_make_collect_report(collector: Collector) 执行collector.collect()并返回一个CollectReport。
* pytest_itemcollected(item: Item) 我们刚刚收集了一个测试项目。
* pytest_collectreport(report: CollectReport) 收集器完成收集。
* pytest_deselected(items: Sequence[Item]) 要求取消选择的测试项目，例如按关键字。
* pytest_report_header(config: Config, startdir: py._path.local.LocalPath) 返回要显示为标题信息的字符串或字符串列表，以进行终端报告。
* pytest_report_collectionfinish(config: Config, startdir: py._path.local.LocalPath, items: Sequence[Item]) 返回成功完成收集后将显示的字符串或字符串列表。
* pytest_report_teststatus(report: Union[CollectReport, TestReport], config: Config) 返回结果类别，简写形式和详细词以进行状态报告。
* pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: ExitCode, config: Config) 在终端摘要报告中添加一个部分。
* pytest_fixture_setup(fixturedef: FixtureDef[Any], request: SubRequest) 执行夹具设置执行。
* pytest_fixture_post_finalizer(fixturedef: FixtureDef[Any], request: SubRequest) 在夹具拆除之后但在清除缓存之前调用，因此夹具结果fixturedef.cached_result仍然可用（不是 None）
* pytest_warning_captured(warning_message: warnings.WarningMessage, when: Literal[‘config’, ‘collect’, ‘runtest’], item: Optional[Item], location: Optional[Tuple[str, int, str]]) （已弃用）处理内部pytest警告插件捕获的警告。
* pytest_warning_recorded(warning_message: warnings.WarningMessage, when: Literal[‘config’, ‘collect’, ‘runtest’], nodeid: str, location: Optional[Tuple[str, int, str]]) 处理内部pytest警告插件捕获的警告。
* pytest_runtest_logreport(report: TestReport) 处理项目的_pytest.reports.TestReport每个设置，调用和拆卸运行测试阶段产生的结果。
* pytest_assertrepr_compare(config: Config, op: str, left: object, right: object) 返回失败断言表达式中的比较的说明。
* pytest_assertion_pass(item: Item, lineno: int, orig: str, expl: str) （实验性的）在断言通过时调用。 

## 2.1.6 Debugging/Interaction hooks 调试/交互钩子

有几个钩子可以用于特殊报告或与异常交互。

* pytest_internalerror(excrepr: ExceptionRepr, excinfo: ExceptionInfo[BaseException]) 要求内部错误。返回True以禁止对将INTERNALERROR消息直接打印到sys.stderr的回退处理。
* pytest_keyboard_interrupt(excinfo: ExceptionInfo[Union[KeyboardInterrupt, Exit]]) 要求键盘中断。
* pytest_exception_interact(node: Union[Item, Collector], call: CallInfo[Any], report: Union[CollectReport, TestReport]) 在引发可能可以交互处理的异常时调用。
* pytest_enter_pdb(config: Config, pdb: pdb.Pdb) 调用了pdb.set_trace()。 

# 2.2 常用hook函数介绍

## 2.2.1 pytest_addoption

`pytest_addoption`用于向`pytest`添加自定义的命令行选项，必须在 `conftest.py` 文件或 `pytest` 插件中才能生效。这个钩子在命令行选项解析之前被调用，它允许你通过命令行参数来配置和控制测试的行为。

### 2.2.1.1 使用场景

- 在运行测试时，提供额外的配置选项，例如指定测试环境、设置日志级别、指定测试数据文件等。
- 根据需要动态配置和控制测试的行为，例如启用/禁用特定的测试功能、设置超时时间、指定测试报告的输出路径等。

- 你打算运行一组特定的测试用例，需要一些特殊的环境设置。
- 你希望通过命令行选项指定一些测试所需要的参数，例如数据文件的路径、服务器的地址等。
- 基于命令行参数来动态生成配置，比如数据库连接，服务接口地址等。
- 控制 debug 模式的开启和关闭
- 控制是否生成详细的测试报告
- 根据命令行参数执行不同的测试用例
- 等等

### 2.2.1.2 用法与示例

- 在您的`conftest.py`文件中定义`pytest_addoption`函数，并使用`parser`参数来添加自定义的命令行选项。
- 使用`addoption`方法添加命令行选项，并指定选项的名称、帮助文本、默认值等。

如下所示：

```python
# content of conftest.py

def pytest_addoption(parser):
    parser.addoption("--environment", action="store", default="dev", help="Specify the test environment")
```

```python
# content of test_addoption.py
def test_example(request):
    # 使用request.config.getoption获取命令行选项的值
    environment = request.config.getoption("--environment")
    print(f"Running test in {environment} environment")
    # 测试逻辑...
```

上述用例，如不指定`--environment`参数，默认携带`dev`值；如果携带，则使用指定值。通过这种方式，指定相关测试环境，完成相同用例在不同环境下的运行。示例用例运行结果参考如下：

```shell
# 不携带参数--environment，使用默认值'dev'
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_addoption.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
collected 1 item

Running test in dev environment

 Appendix/appendix-2/test_addoption.py::test_example ✓         100% ██████████

Results (0.02s):
       1 passed
root@Gavin:~/code/Appendix/appendix-2# 
# 携带参数--environment，使用携带值'prod'
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_addoption.py --environment prod
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0

Running test in prod environment

 Appendix/appendix-2/test_addoption.py::test_example ✓        100% ██████████
Results (0.02s):
       1 passed
root@Gavin:~/code/Appendix/appendix-2#
```

再比如用例适配不同的数据库，参考代码如下：

```python
# content of conftest.py
def pytest_addoption(parser):
    parser.addoption("--use-db", action="store_true", default=False,
                     help="Use real database for tests")

# test_module.py
def test_database(pytestconfig):
    if pytestconfig.getoption("use_db"):
        # 连接到真实的数据库
        db = RealDatabase()
    else:
        # 使用模拟的数据库
        db = FakeDatabase()

    # 执行数据库相关的测试...
```

### 2.2.1.3 注意事项

- **命名规范化**：命令行选项的名称应该使用双横线作为前缀，以避免与其他参数或选项冲突。如果配合`pytest_generate_tests`使用，尤其需要注意避免参数冲突。
- **注释与说明**：确保命令行选项的名称和帮助文本清晰明确，以便其他人理解和使用。



## 2.2.2 pytest_load_initial_conftests

`pytest_load_initial_conftests(early_config, parser, args)` hook 允许插件或者测试集合的作者在 module 分发阶段之前动态加载配置文件，这个 hook 会被 `pytest` 自动调用，参数含义如下：

`pytest_load_initial_conftests(config, conftestpath)` 这个 `hook` 会被 `pytest` 自动调用。其中 `config` 是一个配置对象，而 `conftestpath` 是用来定位配置文件的文件路径。

如果 `conftestpath` 没有按照常规方式被解析，那么 `pytest` 会调用 `pytest_addhooks` hook 将配置文件中定义的其他 hooks 转为合法的插件。

- `early_config` 是一个配置对象，用于控制 `pytest` 的行为。
- `parser` 是一个 `argparse.ArgumentParser` 实例，用于解析命令行参数。
- `args` 是命令行参数列表。

典型的使用场景是一个插件需要在调用测试前动态加载特定的配置文件，以为会话或测试集合进行全局配置。该 `hook` 的另一个用途是允许在基于文件系统的 test discovery 过程中正确解析不能直接加载的配置文件。



### 2.2.2.1 使用场景

* **加载配置或插件**：
  * 根据不同的命令行参数加载不同的配置。
  * 根据环境变量或者其他外部条件动态加载配置。
  * 在你没有直接控制的环境中加载特定的插件或设置。
  * 当你需要在测试运行之前注册一个插件，而这个插件是通过命令行参数、环境变量或某些外部条件动态决定的。

* **自定义设置**： 当你希望在测试会话开始前修改一些配置设置。

### 2.2.2.2 用法与示例

下面是一个简单的示例，它展示了如何使用 `pytest_load_initial_conftests` 动态加载不同的`conftest.py`配置文件。

```python
# content of pytest my_plugin.py

import os
import pytest
import importlib.util

def pytest_addoption(parser):
    # 添加一个命令行选项 --env，用来指明需要哪个环境的配置
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")

def pytest_load_initial_conftests(early_config, parser, args):
    # 获取当前路径
    dirname = os.path.dirname(os.path.abspath(__file__))

    # 解析传入的命令行参数
    options = parser.parse_known_args(args)

    # 根据 --env 参数确定配置文件
    # 注意：要访问 --env 参数需要使用 options.env
    env = options.env
    if env == 'dev':
        config_file_path = 'conftest_dev.py'
    elif env == 'prod':
        config_file_path = 'conftest_prod.py'
    else:
        # 如无有效环境参数，不加载任何额外配置
        raise ValueError(f"Invalid environment option --env={env}, expected 'dev' or 'prod'")

    # 生成配置文件的绝对路径
    conftest_path = os.path.join(dirname, config_file_path)
    
    # 动态加载 conftest 模块
    spec = importlib.util.spec_from_file_location("conftest_module", conftest_path)
    conftest_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conftest_module)

    # 使用 pluginmanager 注册 conftest 模块
    print(f'使用 pluginmanager 注册 conftest 模块: {config_file_path}')
    early_config.pluginmanager.register(conftest_module, name=config_file_path)
```

上面的示例在 `my_plugin.py` 中定义了一些 `pytest` 配置，指定加载的 `conftest.py` 和添加自定义命令行选项。然后在 `pytest_load_initial_conftests` 中动态加载 `conftest.py`，以确保在运行测试时它已经被正确加载和解析。这种方式，你就可以在测试运行之前对测试全局进行自定义配置：

```python
# content of conftest_dev.py

import pytest

def pytest_sessionstart(session):
    print("\ndev 会话开始：这是一条来自 pytest_sessionstart 钩子的信息")

def pytest_sessionfinish(session, exitstatus):
    print("\ndev 会话结束：这是一条来自 pytest_sessionfinish 钩子的信息")
```

```python
# content of conftest_prod.py

import pytest

def pytest_sessionstart(session):
    print("\nprod 会话开始：这是一条来自 pytest_sessionstart 钩子的信息")

def pytest_sessionfinish(session, exitstatus):
    print("\nprod 会话结束：这是一条来自 pytest_sessionfinish 钩子的信息")
```

这样，在设置了这样的配置后，你就可以在测试中访问不同`conftest.py`中的 fixture 了，也可以通过 `--env`在测试期间输出更多的信息。

我们来看一下用例的执行效果：

```shell
root@Gavin:~/code/Appendix/appendix-2# PYTHONPATH=. pytest -s -v -p my_plugin --env=prod test_sample2.py
使用 pluginmanager 注册 conftest 模块: conftest_prod.py
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0

prod 会话开始：这是一条来自 pytest_sessionstart 钩子的信息
collected 6 items

 Appendix/appendix-2/test_sample2.py::test_str_methods ✓        17% █▋        
 Appendix/appendix-2/test_sample2.py::test_list_append ✓        33% ███▍      
 Appendix/appendix-2/test_sample2.py::test_list_pop ✓           50% █████     
 Appendix/appendix-2/test_sample2.py::test_tuple_length ✓       67% ██████▋   
 Appendix/appendix-2/test_sample2.py::test_set_length ✓         83% ████████▍ 
 Appendix/appendix-2/test_sample2.py::test_dict_items ✓        100% ██████████
prod 会话结束：这是一条来自 pytest_sessionfinish 钩子的信息

Results (0.03s):
       6 passed
root@Gavin:~/code/Appendix/appendix-2# PYTHONPATH=. pytest -s -v -p my_plugin --env=dev test_sample2.py
使用 pluginmanager 注册 conftest 模块: conftest_dev.py
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0

dev 会话开始：这是一条来自 pytest_sessionstart 钩子的信息
collected 6 items

 Appendix/appendix-2/test_sample2.py::test_str_methods ✓        17% █▋        
 Appendix/appendix-2/test_sample2.py::test_list_append ✓        33% ███▍      
 Appendix/appendix-2/test_sample2.py::test_list_pop ✓           50% █████     
 Appendix/appendix-2/test_sample2.py::test_tuple_length ✓       67% ██████▋   
 Appendix/appendix-2/test_sample2.py::test_set_length ✓         83% ████████▍ 
 Appendix/appendix-2/test_sample2.py::test_dict_items ✓        100% ██████████
dev 会话结束：这是一条来自 pytest_sessionfinish 钩子的信息

Results (0.03s):
       6 passed
root@Gavin:~/code/Appendix/appendix-2# 
```

可以看出，通过指定参数`--env`携带不同的参数值，使用不同的`conftest.py`文件，以期达到测试用例设计效果。

### 2.2.2.3 注意事项

* **测试和验证**：当使用这个钩子时，确保彻底测试其行为，保证它按照预期注册插件且不造成副作用。
* **参数解析**：确保你的参数解析与 `pytest` 保持一致，并且不会干扰到后面的配置或者插件加载。
* **安全性**：使用 `exec` 执行外部文件时要非常小心，确保文件来源可靠，防止代码注入攻击。
* **名称空间**：适当地管理名称空间，确保加载的配置不会无意中覆盖已有的设置或变量。
* **文件路径**：验证配置文件路径的正确性，并确保在任何环境中其都是可访问的。
* **测试要严格**：变更测试配置是一个风险较高的操作，确保对每个环境进行详尽的测试，验证配置的有效性。
* **回退机制**：提供一个默认配置作为回退，以防某些环境没有专门的配置文件。
* **文档记录**：清晰记录这种动态配置机制的细节，以便项目的其他成员能理解和正确使用它。
* **只用于特殊情况**：通常你不需要在常规的测试中使用这个钩子。只有在你确实需要控制测试前的插件加载或配置时，才会用到。
* **兼容性维护**：如果你的插件或 `conftest.py` 依赖于这个钩子，确保与 `pytest` 版本的兼容性，防止因升级导致的问题。



## 2.2.3 pytest_runtest_logstart

`pytest_runtest_logstart` 钩子专门用于测试执行期间的日志生成，当测试开始执行时，就会调用它。

### 2.2.3.1 使用场景

- **日志记录**：自定义日志记录，比如在测试开始时记录更多上下文信息。
- **性能监测**：用于在测试开始时记录时间戳，从而监控测试执行时间。
- **资源准备**：在测试开始前确保重要资源，例如测试服务器或数据库，是在线并可访问的。
- **通知发送**：发送通知到其他系统，比如开始执行测试用例的通知。

### 2.2.3.2 用法与示例

这个钩子通常定义在 `conftest.py` 文件中，这是一个特殊的文件，`pytest`会自动集成其中的钩子和`fixtures`：

```python
# conftest.py

def pytest_runtest_logstart(nodeid, location):
    # 自定义的日志记录或测试前操作
    print(f"开始执行测试: {nodeid}，位置: {location}")
```

- `nodeid`: 是测试的唯一标识，通常包括文件名、类名和测试函数名或参数化标识符。
- `location`: 是一个三元组，包含测试文件的名称、测试所在文件的行号以及测试节点的名称。

假设你想要在每个测试开始前记录当前时间和测试的标识符，可以这样做：

```python
# content of conftest.py

import pytest
from datetime import datetime

def pytest_runtest_logstart(nodeid, location):
    """
    Hook for logging test start information.
    
    :param nodeid: Unique id of the test.
    :param location: Location of the test (file, line, domain).
    """
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{start_time} - Starting test: {nodeid}")
```

每当一个测试用例开始执行时，都会在控制台打印出类似的日志信息，类似如下：

```shell
root@Gavin:~/code/Appendix/appendix-2# pytest  test_sample2.py  | grep Starting
test_sample2.py 2024-01-16 12:34:31 - Starting test: Appendix/appendix-2/test_sample2.py::test_str_methods
.2024-01-16 12:34:31 - Starting test: Appendix/appendix-2/test_sample2.py::test_list_append
.2024-01-16 12:34:31 - Starting test: Appendix/appendix-2/test_sample2.py::test_list_pop
.2024-01-16 12:34:31 - Starting test: Appendix/appendix-2/test_sample2.py::test_tuple_length
.2024-01-16 12:34:31 - Starting test: Appendix/appendix-2/test_sample2.py::test_set_length
.2024-01-16 12:34:31 - Starting test: Appendix/appendix-2/test_sample2.py::test_dict_items
root@Gavin:~/code/Appendix/appendix-2#
```



### 2.2.3.3 注意事项

- 这个钩子不应该用于执行测试用例所需的正常设置，为此目的，应使用 fixtures。
- 在这个钩子中改变的状态不会影响测试用例本身，即：它仅适合于日志和类似非功能性的任务。
- 信息打印须适用于所配置的`pytest`的日志系统，要确保信息被适当地记录而不是丢失。
- 如果有多个插件或`conftest.py`文件实现了这个钩子，需要注意它们会按照`pytest`的插件管理规则进行调用，可能会出现预期之外的情况。
- 当在 CI/CD 系统中使用时，要确保任何输出都符合系统抓取和解析日志的要求。



## 2.2.4 pytest_generate_tests

`pytest_generate_tests` 允许你定义自己的参数化逻辑或自动生成测试用例参数的集合。这个功能特别适用于当你想要在运行时动态地决定参数集合或实现更复杂的参数化规则时。

### 2.2.4.1 使用场景

- **动态参数化**：根据测试环境的不同条件，允许在测试运行时动态地决定测试参数。
- **复杂的参数逻辑**：在进行跨多个参数的组合测试，且参数组合逻辑比较复杂时；或者当`@pytest.mark.parametrize`不够用时，可以使用`pytest_generate_tests`来处理更复杂的参数化需求；或者实现自定义参数化逻辑，比如压缩测试用例范围、随机生成测试数据等。
- **条件参数化**：基于某些条件，诸如用户输入、配置文件或者从外部数据源（如文件、数据库、API等）载入测试数据。
- **跨多个测试目录或文件**：可以在`conftest.py`文件中使用该钩子，从而对整个目录或项目范围内的测试进行参数化。

### 2.2.4.2 用法与示例

- 在 `conftest.py` 文件或测试模块中定义 `pytest_generate_tests` 函数。
- 使用 `metafunc.parametrize` 方法来将参数值和id传入测试函数。

假设你有一个测试函数，它需要根据一组输入进行测试：

```python
def test_example(parameter):
    # 测试代码
    assert parameter < 4
```

你可以使用 `pytest_generate_tests` 来动态地为这个测试生成参数：

```python
# content of test_generate_tests1.py

def pytest_generate_tests(metafunc):
    if "parameter" in metafunc.fixturenames:
        metafunc.parametrize("parameter", [1, 2, 3], scope="function")

def test_example(parameter):
    assert parameter < 4
```

在上述例子中，如果测试函数请求了一个名叫 `parameter` 的fixture参数，该钩子将会使用值列表 `[1, 2, 3]` 参数化 `parameter`。输出结果参考如下：

```shell
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_generate_tests1.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0
collected 3 items

 Appendix/appendix-2/test_generate_tests1.py::test_example[1] ✓       33% ███▍      
 Appendix/appendix-2/test_generate_tests1.py::test_example[2] ✓       67% ██████▋   
 Appendix/appendix-2/test_generate_tests1.py::test_example[3] ✓      100% ██████████

Results (0.02s):
       3 passed
root@Gavin:~/code/Appendix/appendix-2# 
```

也可以写在`conftest.py`文件中，如下面的示例：

假设你想基于不同的输入数据测试一个函数，而这些数据来源于一个外部文件。

```shell
# content of data.json
[
    {"input": 1, "expected": 2},
    {"input": 2, "expected": 4},
    {"input": 3, "expected": 6}
]
```

```python
# content of conftest.py
import json

def pytest_generate_tests(metafunc):
    # 假设所有测试都需要 "input_data" 参数
    if 'input_data' in metafunc.fixturenames:
        # 加载测试数据，这里以从文件加载为例
        with open('data.json', 'r') as f:
            data = json.load(f)
        # parametrize 可以接受一个参数列表和一个id列表
        metafunc.parametrize("input_data", data, ids=[str(d) for d in data])
```

```python
# content of test_generate_tests2.py
def test_my_func(input_data):
    # 这里将根据上面生成的每个输入数据进行测试
    result = my_func(input_data)
    assert result # 或一些有意义的断言
```

执行效果参考如下：

```shell
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_generate_tests2.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0
collected 3 items

 Appendix/appendix-2/test_generate_tests2.py::test_my_func[{'input': 1, 'expected': 2}] ✓        33% ███▍      
 Appendix/appendix-2/test_generate_tests2.py::test_my_func[{'input': 2, 'expected': 4}] ✓        67% ██████▋   
 Appendix/appendix-2/test_generate_tests2.py::test_my_func[{'input': 3, 'expected': 6}] ✓       100% ██████████

Results (0.02s):
       3 passed
root@Gavin:~/code/Appendix/appendix-2#
```

### 2.2.4.3 注意事项

- 确保使用 `pytest_generate_tests` 时，其应用的范围与你预期一致。如果你将其放在`conftest.py`，它会对整个目录下的测试应用；如果只是在特定的模块中，它仅对那个模块应用。
- 注意性能问题：如果你生成了大量的测试参数组合，测试执行时间可能会大幅增加。
- 确保生成的参数与你的测试函数期望的参数匹配，意即如果`metafunc.parametrize`的参数名不在测试函数的参数列表中，则测试将无法运行。
- 使用复杂数字数据作为参数时，考虑为参数设置ID，使测试结果更易于理解。

- 确保 `pytest_generate_tests` 不会与其他参数化方法（如直接在装饰器中参数化）冲突。
- 牢记 `pytest_generate_tests` 是按照模块作用域运行的，如果在同一模块中有多个测试函数需要参数化，`pytest_generate_tests` 需要能够处理每个测试函数的参数化。
- 由于 `pytest_generate_tests` 在收集阶段就会被调用，你不能在测试函数或fixture内部使用它。



## 2.2.5 pytest_runtest_protocol 

`pytest_runtest_protocol` 允许插件和用户自定义的代码在测试执行期间介入，改变或扩展`pytest`的标准测试执行流程。使用这个钩子，可以控制测试的运行方式、测试报告的生成以及许多其他方面的自定义行为（如自定义测试的执行流程。控制测试报告的生成。根据需要实现特殊的测试逻辑，如条件跳过、重试失败的测试等）。

### 2.2.5.1 使用场景

* **自定义测试执行流程**：当你需要某些测试遵循不同于默认执行流程的顺序或逻辑时，如实现失败重试机制。
* **集成外部服务**：比如，测试开始前需要从外部服务获取一些数据或者状态，并在测试结束后更新外部服务的状态。
* **增强测试报告**：记录更多信息到测试报告中，例如附加日志信息、屏幕截图等。

### 2.2.5.2 用法与示例

首先，你需要创建一个`pytest_runtest_protocol`函数，在测试项目执行时，这个函数将被调用。函数需要接收两个参数：`item`和`nextitem`。`item`是当前正在运行的测试项目，而`nextitem`是队列中的下一个测试项目。

在`pytest`的插件中或是你的测试代码中，你可以定义一个带有`pytest_runtest_protocol` 名称的函数。其基本模板如下：

```python
# conftest.py 或 pytest 插件中
def pytest_runtest_protocol(item, nextitem):
    # 自定义的准备工作
    # ...

    # 执行测试并捕获结果
    outcomes = runtestprotocol(item, nextitem=nextitem, log=True)
    
    # 自定义的清理工作或额外的报告
    # ...

    # 返回True来阻止其他的hook执行
    return True
```

下面是一个简单的示例，这个示例通过`pytest_runtest_protocol` 钩子实现一个简单的测试重试逻辑：

```python
# content of conftest.py
import pytest
from _pytest.runner import runtestprotocol

def pytest_addoption(parser):
    """
    添加一个命令行选项 --retry，用于设置重试次数。
    """
    parser.addoption(
        "--retry", action="store", default=0, type=int,
        help="Number of times to retry a test if it fails."
    )

def pytest_runtest_protocol(item, nextitem):
    """
    重写默认的Pytest测试协议以添加重试功能。
    """
    # 获取命令行参数中的重试次数
    retry_count = item.config.getoption("--retry")
    # 为了记录测试重试的次数
    retries = 0

    while True:
        # 统计重试的次数，如果大于零则为重试。
        if retries > 0:
            print(f"Retrying {item.nodeid} ({retries}/{retry_count})")
        
        # 执行测试并捕获结果
        outcomes = runtestprotocol(item, nextitem=nextitem, log=True)
        # 查找测试执行阶段（call）的报告
        call_reports = [outcome for outcome in outcomes if outcome.when == "call"]
        
        # 如果没有发生失败，或者重试次数已用完，则退出循环
        if not any(call_report.failed for call_report in call_reports) or retries >= retry_count:
            break
        
        # 如果测试失败了，则增加重试次数，并再次执行循环
        retries += 1
        
    # 返回True以阻止Pytest进一步处理剩余的测试协议
    return True
```

对应测试用例：

```python
# content of test_retry.py
def test_case01():
    assert 1== 1


def test_case02():
    assert True == False
```

测试用例`test_case02`故意断言失败，看看是否会按照要求进行重试，执行效果如下（重试2次）：

```shell
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_retry.py --retry=2
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_retry.py --retry=2
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0
collected 2 items

 Appendix/appendix-2/test_retry.py::test_case01 ✓       50% █████     
―――――――――――――――――――――――――――――― test_case02 ―――――――――――――――――――――――――――――――
    def test_case02():
>       assert True == False
E       assert True == False

test_retry.py:6: AssertionError

 Appendix/appendix-2/test_retry.py::test_case02 ⨯      100% ██████████
 Retrying Appendix/appendix-2/test_retry.py::test_case02 (1/2)
―――――――――――――――――――――――――――――― test_case02 ―――――――――――――――――――――――――――――――
    def test_case02():
>       assert True == False
E       assert True == False

test_retry.py:6: AssertionError

 Appendix/appendix-2/test_retry.py::test_case02 ⨯      150% ███████████████
 Retrying Appendix/appendix-2/test_retry.py::test_case02 (2/2)
―――――――――――――――――――――――――――――― test_case02 ――――――――――――――――――――――――――――――
    def test_case02():
>       assert True == False
E       assert True == False

test_retry.py:6: AssertionError

 Appendix/appendix-2/test_retry.py::test_case02 ⨯      200% ████████████████████
======================== short test summary info =========================
FAILED test_retry.py::test_case02 - assert True == False
FAILED test_retry.py::test_case02 - assert True == False
FAILED test_retry.py::test_case02 - assert True == False

Results (0.06s):
       1 passed
       3 failed
         - Appendix/appendix-2/test_retry.py:5 test_case02
         - Appendix/appendix-2/test_retry.py:5 test_case02
         - Appendix/appendix-2/test_retry.py:5 test_case02
root@Gavin:~/code/Appendix/appendix-2#
```

执行第一次失败后，又重试了两次，总计三次，都以失败而结束，但这造成了展示进度百分比的异常。

### 2.2.5.3 注意事项

* **确保兼容性**：如果你覆盖了`pytest_runtest_protocol`，确保你的实现与`pytest`的其他插件兼容，比如测试执行的基础工作流程不被打断，除非你有特别的原因完整重写它。
* **保留测试流程**：你可能要调用默认的`pytest_runtest_protocol`来保留标准的测试流程，除非你有充分的理由全部重新实现它。
* **返回值**：当你的`pytest_runtest_protocol`实现返回True时，会阻止后续同名钩子的执行。这意味着你应该小心这么做，以避免不小心禁用了其它插件可能依赖的功能。
* **理解执行顺序**：钩子的执行顺序与它们在`conftest.py`文件或插件中的注册顺序有关。深入理解这一点对于确保钩子正确执行非常重要。
* **防止无限循环**：在重试逻辑中，确保有基础案例来停止测试，防止出现无限重试的情况。

使用这个钩子可以大幅度地提高测试的灵活性和控制力，但也需谨慎使用以避免引入复杂性和不可预见的行为。如有可能，应当避免使用这个钩子来实现简单的任务，因为过度使用钩子可能会增加测试套件的复杂度，并使得问题更难调试。



### 2.2.5.4 与`pytest_runtest_logstart`对比

以下是一个简单表格，对比`pytest_runtest_logstart`和`pytest_runtest_protocol`这两个`pytest`钩子函数的差异：

| 特性                     | `pytest_runtest_logstart`                                    | `pytest_runtest_protocol`                                    |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 钩子类型                 | 日志钩子                                                     | 测试执行钩子                                                 |
| 作用                     | 当测试用例开始时调用，用于日志记录                           | 覆盖pytest默认的测试执行协议                                 |
| 接口参数                 | `nodeid`，`location`: 表示测试项的详细信息                   | `item`，`nextitem`: 当前正在运行的测试项和下一个测试项的钩子函数 |
| 返回值                   | 无                                                           | 可返回True或None。如果返回True，则阻止后续的测试执行钩子继续处理当前测试项。 |
| 调用时机                 | 在测试用例执行的开始，且在任何fixture和测试用例之前          | 在测试项运行时调用，并处理整个测试执行阶段，包括调用`pytest_runtest_setup`、`pytest_runtest_call`<br />和`pytest_runtest_teardown` |
| 用例                     | 可以用来输出测试开始的合适日志顺序，比如在并行测试时保持日志清晰 | 可用于实现自定义的测试执行逻辑，例如根据特定条件跳过测试或更改测试执行的方式 |
| 扩展性                   | 主要用于日志目的，不涉及更改测试执行策略                     | 提供强大的自定义能力，可极大地更改测试执行方式               |
| 对测试结果的影响         | 无                                                           | 有;可以控制整个测试协议，包括结果记录和报告                  |
| 可以中断测试执行流程吗？ | 不能，它主要用于日志记录和其他插件机制。                     | 可以，因为它控制了测试用例的完整生命周期。                   |

此表格反映的是两个钩子的核心差异。`pytest_runtest_logstart`主要用于记录测试开始的信息，而`pytest_runtest_protocol`则是用于控制测试的执行流程。开发者可以通过实现这些钩子来扩展`pytest`的测试运行机制并将其与其他测试工具或流程进行集成。



## 2.2.6 pytest_collection_modifyitems 

`pytest_collection_modifyitems` 允许你在测试用例被搜集后，执行测试之前对这些测试项进行修改或筛选。你可以使用这个钩子来添加标记、添加附加信息、修改测试用例的顺序或者根据某些条件跳过某些测试用例。它有如下几个常用属性：

* `item.nodeid`: 返回一个字符串，表示测试用例的唯一标识符。
* `item.name`: 返回一个字符串，表示测试用例的名称。
* `item.parent`: 返回一个节点对象，表示测试用例所属的父级节点（模块、类或测试集合）。
* `item.function`: 返回一个函数对象，表示测试用例的实际执行函数。
* `item.originalname`: 返回一个字符串，表示测试用例的原始名称。
* `item.location`: 返回一个元组，包含测试用例所在文件的路径和行号。
* `item.keywords`:返回一个包含字符串关键字的集合

### 2.2.6.1 使用场景

- **重新排序测试用例**：改变测试用例的执行顺序，或对测试用例进行排序，例如按照测试用例名称进行字母顺序排序。
- **筛选测试用例**：对测试用例进行过滤，例如根据标签或表达式筛选出特定的测试用例。
- **添加或修改标记**：动态地给测试用例添加pytest标记和附加信息，例如为测试用例添加自定义标记或附加说明。
- **条件化跳过测试**：在运行测试前根据条件跳过某些测试。
- **实现自定义逻辑**：实现复杂的条件逻辑，这些逻辑不能通过静态标记或者命令行参数轻易完成，但任何需要的测试收集后逻辑处理都可以在此实现。

### 2.2.6.2 用法与示例

要使用这个钩子函数，你需要在你的`conftest.py`文件或者自定义的插件中定义一个`pytest_collection_modifyitems`函数，并在该函数中修改`items`列表，这个列表包含了所有搜集到的测试项：

- `conftest.py`文件中定义`pytest_collection_modifyitems`函数，并使用`config`参数来修改测试用例。
- 使用`item.nodeid`属性来获取测试用例的标识符，并对测试用例进行操作。

同时，创建一个名称为`test_collection_modifyitems_v1.py`的文件，测试用例代码如下：

```python
import pytest

def test_b():
    assert True

def test_a():
    assert True

def test_c():
    assert True

def test_slow():
    assert True

@pytest.mark.slow('Slow Tag test case')
def test_d():
    assert True

@pytest.mark.smoke('smoke test case')
def test_e():
    assert True
```

#### 2.2.6.2.1 用例排序

```python
# content of conftest.py
def pytest_collection_modifyitems(config, items):
    # 对测试用例按照名称进行排序
    items.sort(key=lambda item: item.nodeid)
```

#### 2.2.6.2.2 过滤用例

过滤含有特定标记的测试用例：

```python
# content of conftest.py
def pytest_collection_modifyitems(config, items):
    # 对测试用例进行过滤，只保留包含"smoke"标记的测试用例
    items[:] = [item for item in items if 'smoke' in item.keywords]
```

跳过用例名称含有指定关键字的用例：

```python
# 下面的例子演示了如何在conftest.py文件中使用这个钩子
# 跳过所有名字包含'slow'的测试用例
import pytest

def pytest_collection_modifyitems(config, items):
    for item in items.copy():
        if 'slow' in item.name: # item.name指的是测试用例函数名
            # 也可以使用pytest.mark.skip装饰器来跳过
            item.add_marker(pytest.mark.skip(reason="Skipping slow test"))
```

#### 2.2.6.2.3 添加标记

下面这个代码示例将会在所有的测试用例上添加一个名为`smoke`的标记：

```python
# content of conftest.py
import pytest

def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.smoke)
```

或者下面这种，增加多个标记：

```python
import pytest

def pytest_collection_modifyitems(session, config, items):
    for item in items:
        # 为所有未标记为"slow"的测试添加一个"fast"标记
        if "slow" not in item.keywords:
            item.add_marker(pytest.mark.fast)
        
        # 示例：如果测试的名称包含 "special"，给测试添加一个"special"标记
        if "special" in item.name:
            item.add_marker(pytest.mark.special)
```

在这个例子中，`conftest.py` 文件中的`pytest_collection_modifyitems`函数会检查所有收集到的测试项 (`items`) 并在运行测试前做出如下修改：

* 如果一个测试项没有被标记为“slow”，那么将会自动添加一个名为“fast”的标记。
* 如果一个测试项的名称包含“special”，那么将会添加一个名为“special”的标记。

#### 2.2.6.2.4 完整示例

我们来看一个完整的、可以工作的 `pytest_collection_modifyitems` 钩子实现，它按照一个假设的标记 `priority` 来排序测试，让标记为高优先级的测试先运行，如果测试没有标记 `priority`，则按照其在模块中的顺序运行。



下面的示例展示了一个完整的、可以工作的 `pytest_collection_modifyitems` 钩子实现，它按照一个假设的标记 `priority` 来排序测试，让标记为高优先级的测试先运行，如果测试没有标记 `priority`，则按照其在模块中的顺序运行。

首先，创建一个名为 `conftest.py` 的文件（如果它还不存在的话），它应该位于测试集的根目录或所需的子目录中，然后添加以下内容：

```python
# content of conftest.py

def pytest_collection_modifyitems(session, config, items):
    # 编写代码来重新排序 items
    def get_priority(item):
        marker = item.get_closest_marker("priority")
        if marker:
            # 如果测试被标记了 'priority'，则返回其数值
            return marker.args[0]
        else:
            # 如果没有标记 'priority'，我们返回一个预设的高数字保证它们在后面运行
            return float('inf')

    # 对 items 按照 'priority' 标记的值进行排序
    items.sort(key=get_priority)
```

然后，你可以在测试函数中使用 `@pytest.mark.priority` 标记来为特定的测试设置优先级：

```python
# content of test_collection_modifyitems_v2.py

import pytest

def test_no_priority():
    # 这个函数没有显式优先级，将最后运行
    assert True

@pytest.mark.priority(10)
def test_lower_priority():
    # 这个函数的运行优先级低
    assert True

@pytest.mark.priority(1)
def test_high_priority():
    # 这个函数运行优先级最高
    assert True
```

在上面的代码示例中，`test_high_priority` 由于优先级为 1，将首先运行；而 `test_lower_priority` 优先级为 10，将在 `test_high_priority` 后面运行；最后运行的是没有任何 `priority` 标记的 `test_no_priority`。运行结果参考如下：

```shell
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_collection_modifyitems.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0
collected 3 items

 Appendix/appendix-2/test_collection_modifyitems.py::test_high_priority ✓ 33% ███▍     
 Appendix/appendix-2/test_collection_modifyitems.py::test_lower_priority ✓67% ██████▋   
 Appendix/appendix-2/test_collection_modifyitems.py::test_no_priority ✓  100% ██████████

Results (0.02s):
       3 passed
root@Gavin:~/code/Appendix/appendix-2# 
```

### 2.2.6.3 注意事项

- **全局影响性**：此钩子函数应用于整个测试集合，包括子目录中的测试文件，需确保逻辑对所有环境都是通用的，或者根据调用的配置设置进行条件检查。
- **测试独立性**: 确保重新排序后的测试用例依然保持独立性，避免因为执行顺序变化而引发的测试不稳定情况。
- **复杂逻辑**: 如果有复杂的排序逻辑，最好有相应的注释或文档描述。
- **需求变化**: 当项目需求发生变化时，及时更新排序逻辑和优先级标记。
- **标记误用**: 注意避免错误使用标记，比如赋予不恰当的优先级值或在非相关测试上使用该标记。
- **避免冲突**：在有些情况下，此钩子可能不会按预期执行，例如当使用某些插件或配置时。如果遇到问题，请确保你的钩子函数是否正确定义，并验证是否与其他钩子函数或配置产生了冲突。



## 2.2.7 pytest_terminal_summary

`pytest_terminal_summary` 钩子允许用户和插件在执行特定的测试运行阶段插入自己的逻辑，在测试结果汇总信息被打印到终端之后调用。这使得用户或插件开发人员可以添加额外的汇总信息，或者对已有的测试结果进行进一步的处理。

### 2.2.7.1 使用场景

- **自定义测试报告**：在测试报告的末尾添加额外信息，如特定的统计数据或测试运行摘要。
- **分析测试结果**：在所有测试执行完成后，对结果进行进一步的分析或处理，例如计算测试覆盖率或其他指标。
- **集成其他系统**：将测试结果发送到外部监控系统或测试管理工具。
- **提供反馈**：向测试者显示额外的反馈信息，例如性能数据或者特定的警告信息。

### 2.2.7.2 用法与示例

比如给测试报告增加自定义的头部信息，可以使用 `pytest_terminal_summary` 钩子函数来修改`terminal`中的输出，这个钩子函数允许我们在测试报告的末尾添加额外的内容。如果你想要在报告开头添加内容，可以结合 `pytest_report_header` 钩子。

以下是一个简单的 `conftest.py` 文件示例，它演示了如何使用这些钩子函数来向`pytest`报告中添加`header`内容：

```python
# content of conftest.py
import pytest

# 插入定制的头部信息
def pytest_report_header(config):
    return "项目名称: 你的项目名称\n测试环境: 你的开发环境"

# 可以选择在报告总结中添加额外信息
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.ensure_newline()
    terminalreporter.section("定制报告", sep='-', bold=True)
    terminalreporter.line("额外信息可以放在这里")

    if 'my_marker' in config.option.markexpr:
        total = sum(1 for t in terminalreporter.stats.get('passed', []) if 'my_marker' in t.keywords)
        terminalreporter.write('\n')
        terminalreporter.write(f'带有标记 "my_marker" 的测试通过数量：{total}\n')

    # 可以访问 terminalreporter 统计信息
    passed = list(terminalreporter.stats.get('passed', []))  
    failed = list(terminalreporter.stats.get('failed', []))

    terminalreporter.section('Custom Summary')
    # terminalreporter passed 的 when 属性有三状态setup,when,teardown的passed
    passed_no = int(len(passed)/3)
    terminalreporter.line(f'Total passed tests: {passed_no}')
    terminalreporter.line(f'Total failed tests: {len(failed)}')

    if exitstatus == 0:
        terminalreporter.line('All tests passed! Great job! :)', green=True)
```

在上述示例中：

- `pytest_report_header` 钩子函数返回一个字符串或者一个由字符串组成的列表，这些字符串会被添加到测试报告的头部。
- `pytest_terminal_summary` 钩子函数用于在测试报告的结尾增加定制的终端输出。在这个函数中使用了 `terminalreporter` 的 `section` 和 `line` 方法来管理输出的格式。

在运行pytest时，这些钩子函数会自动被调用，并将内容插入到测试报告中相应的位置。通过自定义这些钩子，你可以让测试报告包含所有必要的信息，提供对测试结果更全面的描述。上述用例执行效果参考如下：

```shell
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_sample1.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
项目名称: 你的项目名称
测试环境: 你的开发环境
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0
collected 10 items

 Appendix/appendix-2/test_sample1.py::test_addition ✓       10% █         
 Appendix/appendix-2/test_sample1.py::test_subtraction ✓    20% ██        
 Appendix/appendix-2/test_sample1.py::test_multiplication ✓ 30% ███       
 Appendix/appendix-2/test_sample1.py::test_division ✓       40% ████      
 Appendix/appendix-2/test_sample1.py::test_modulus ✓        50% █████     
 Appendix/appendix-2/test_sample1.py::test_power ✓          60% ██████    
 Appendix/appendix-2/test_sample1.py::test_square_root ✓    70% ███████   
 Appendix/appendix-2/test_sample1.py::test_negative ✓       80% ████████  
 Appendix/appendix-2/test_sample1.py::test_positive ✓       90% █████████ 
 Appendix/appendix-2/test_sample1.py::test_zero ✓          100% ██████████
--------------------------------- 定制报告 -------------------------------
额外信息可以放在这里
============================== Custom Summary ===========================
Total passed tests: 10
Total failed tests: 0
All tests passed! Great job! :)

Results (0.03s):
      10 passed

root@Gavin:~/code/Appendix/appendix-2#
```

### 2.2.7.3 注意事项

* **适当使用接口**：使用 `terminalreporter` 的方法（例如 `write`, `line`, 或者 `section`）来添加内容到终端报告中。避免直接使用 `print` 函数，因为这样可能会干扰 `pytest` 的输出格式。
* **响应状态**：`exitstatus` 参数含有关于测试执行结果的信息（例如，是否有测试失败），你可以使用这个信息来决定是否需要额外的输出或者动作。
* **影响因素**：意识到你的新增输出可能会影响到如何解读测试结果，所以要保持清晰和简洁。在添加自定义的汇总信息时可以加上提示或者装饰，以便于区分 `pytest` 的标准输出。
* **避免干扰**：你的钩子函数不应该覆盖或者干预原有的汇总信息，除非这是你明确的目的。



# 2.3 使用钩子函数

`pytest` 提供了多个钩子函数，用于不同的测试阶段和目的。我们来看一个综合示例：

```python
# content of conftest.py
import pytest
from collections import Counter

# 钩子函数：自定义测试报告头部
def pytest_report_header(config):
    return "项目名称: 示例项目\n测试环境: 开发"

# 钩子函数：每个测试用例执行前调用
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    # 执行前的准备操作
    print(f"开始执行测试: {item.name}")

# 钩子函数：每个测试用例执行后调用
@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    # 执行后的清理操作
    print(f"完成测试: {item.name}")


# 在 pytest_configure 钩子中初始化我们的计数器
def pytest_configure(config):
    # 使用 Pytest 配置对象注册额外的数据字段
    config.test_function_count = Counter()

# 使用 pytest_collection_modifyitems 钩子函数来统计每个模块的测试函数数
def pytest_collection_modifyitems(session, config, items):
    for item in items:
        # 提取测试模块的名字作为统计的键
        module_name = item.module.__name__
        # 计数每个模块的测试函数数量
        config.test_function_count[module_name] += 1

# 在所有测试执行完成后，使用 pytest_terminal_summary 输出总结信息
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # 在 terminal 中打印统计报告
    terminalreporter.section('Test Case Distribution')
    for module, count in config.test_function_count.items():
        terminalreporter.write(f"{module}: {count} test functions\n")
```

执行效果参考如下：

```shell
root@Gavin:~/code/Appendix/appendix-2# pytest -s -v test_sample*.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
项目名称: 示例项目
测试环境: 开发
rootdir: /root/code
configfile: pytest.ini
plugins: sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0
collected 26 items

开始执行测试: test_addition
完成测试: test_addition
 Appendix/appendix-2/test_sample1.py::test_addition ✓            4% ▍         
开始执行测试: test_subtraction

完成测试: test_subtraction
 Appendix/appendix-2/test_sample1.py::test_subtraction ✓         8% ▊
开始执行测试: test_multiplication

完成测试: test_multiplication
 Appendix/appendix-2/test_sample1.py::test_multiplication ✓      12% █▎
 开始执行测试: test_division
................................... 中间内容省略 .................

开始执行测试: test_not_empty_set

完成测试: test_not_empty_set
 Appendix/appendix-2/test_sample3.py::test_not_empty_set ✓       96% █████████▋
 开始执行测试: test_not_empty_tuple

完成测试: test_not_empty_tuple
 Appendix/appendix-2/test_sample3.py::test_not_empty_tuple ✓    100% ██████████▋
=========================== Test Case Distribution ===========================
test_sample1: 10 test functions
test_sample2: 6 test functions
test_sample3: 10 test functions

Results (0.04s):
      26 passed
root@Gavin:~/code/Appendix/appendix-2# 
```



# 2.4 本章小结

在本章中，我们探讨了 `pytest` 框架中的钩子（hooks）机制，它是 `pytest` 的一个重要功能，允许我们自定义和扩展测试的不同阶段。我们了解了钩子的作用，包括它们是如何使我们能够在测试收集、运行、报告等步骤中注入自定义逻辑的。我们学习了在不同的测试阶段可以使用的一些常用钩子，如何在 `conftest.py` 中实现它们，以及如何根据项目的需求调节它们的行为。我们讨论了钩子的用法、使用场景以及一些示例，同时指出在构建和使用钩子时需要考虑的注意事项。

正如我们见到的，通过有效使用钩子，可以实现诸如如下功能：

- 控制测试执行顺序和筛选
- 添加标记或分类以执行特定的测试子集
- 响应测试事件，如设置和拆解操作
- 修改和增强测试报告的输出
- 执行全局资源管理和状态检查

不得不感叹`pytest`的强大，可以用来优化测试流程和结果的呈现，使之更加适合我们的测试需求和环境。无论你是在探究单元测试的细节，还是在构建一个复杂的端到端测试套件，理解和正确应用 `pytest` 钩子都是一个提高测试质量和效率的关键。随着对这些概念的深入掌握，我们可以构建更强大、更灵活的测试套件，并确保我们的测试结果既准确又有洞察力。
