---
title: 《pytest测试指南》-- 章节1-9 pytest 配置文件
date: 2024-05-29 23:00:00
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
summary: 《pytest测试指南》一书 章节1-9 pytest配置文件conftest.py和pytest.ini介绍
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 第9章 pytest配置文件

要建立一个可靠且高效的测试环境，理解和正确使用 `pytest` 的配置文件系统是至关重要的。配置文件在 `pytest` 环境中发挥着核心作用，它们是控制测试行为的神经中枢。这些文件不仅允许团队成员间共享一致的测试设置，还能够帮助自动化简化一些重复的任务，如指定测试目录、添加常用选项以及管理日志输出。更重要的是，合理的配置文件可以使我们的测试更加可预测，让我们对测试流程有着细致的控制，从而提高开发和维护的效率。

`pytest` 支持多种类型的配置文件，旨在满足不同项目的特点和需求。从专用的 `pytest.ini` 文件到可在多个上下文中使用的 `pyproject.toml`，再到更加通用且兼容的 `tox.ini` 和 `setup.cfg`，每种文件都可以在项目的适当位置定义精细的测试配置参数，都可以用来细化和调优你的测试设置。配置文件确立了一个标准，使得在多种环境和机器上跑测试能够产生一致的结果。

通过准确地配置 `pytest`，我们可以设定测试发现规则、管理插件、定义运行参数、控制日志行为，以及多样化地调整其它测试行为。配置文件的存在，不仅使得测试过程更加可预测和稳定，还能提升测试实施的有效性，让团队成员之间实现高效且无缝的协作。

在本章节中，我们将深入探讨 `pytest` 配置文件的各个方面。我们会开始于简要介绍每种配置文件的特点以及它们在 `pytest` 生态中的角色，然后进一步讨论如何优雅地使用它们来提升自动化测试的效果。无论你是已经在使用 `pytest` 还是即将开始自动化测试的旅程，本篇文章都将为你打开一扇通往更高效、更严谨测试实践的大门。

# 9.1 pytest 配置文件分类

`pytest`中配置文件主要有如下几种：


| 配置文件        | 用途                                                                    | 含义                                                                                                             |
|----------------|-------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| `pytest.ini`   | `pytest`的主配置文件。                                           | 当该文件存在时，`pytest`会优先读取该文件中的配置信息。通常用于指定特定于 `pytest`的参数和测试行为选项，改变`pytest`的默认行为。它的位置也定义了`pytest`的根目录，或称`rootdir`。 |
| `pyproject.toml` | Python 项目构建配置，用于存放构建工具配置，`pytest` 也支持从中读取配置。 | 可以将 `pytest` 的配置项放在 `[tool.pytest.ini_options]` 中。 |
| `tox.ini`      | `tox` 工具的配置文件，用于虚拟环境的管理和测试命令配置。                  | 如果 `pytest.ini` 不存在，`pytest` 将读取 `tox.ini` 中的 `[pytest]` 部分，为 `tox` 环境中的测试提供配置。          |
| `setup.cfg`    | `setuptools` 的配置文件，管理包元信息和运行设置。                        | `[tool:pytest]` 部分用于配置 `pytest`，适用于那些希望保持传统并在一个文件中管理所有配置的项目。        |


这个表格提供了 `pytest` 配置文件的简要概览，指出了每种文件的用途和它们为 `pytest` 测试环境提供的配置作用。开发人员可以根据自己项目的需要以及对不同工具的使用偏好，来选择使用哪种配置文件来设定测试参数。

# 9.2 哪些内容可以放在 pytest.ini 文件中

`pytest.ini` 文件中的内容，来自于 ``` pytest --help```， 具体信息，请查阅help，每个参数都有描述说明。

如下是未安装第三方插件情况下，可以写入到`pytest.ini`文件中的参数：

```shell
[pytest] ini-options in the first pytest.ini|tox.ini|setup.cfg|pyproject.toml file found:

  markers (linelist):   Markers for test functions
  empty_parameter_set_mark (string):
                        Default marker for empty parametersets
  norecursedirs (args): Directory patterns to avoid for recursion
  testpaths (args):     Directories to search for tests when no files or directories are given on the command line
  filterwarnings (linelist):
                        Each line specifies a pattern for warnings.filterwarnings. Processed after -W/--pythonwarnings.
  usefixtures (args):   List of default fixtures to be used with this project
  python_files (args):  Glob-style file patterns for Python test module discovery
  python_classes (args):
                        Prefixes or glob names for Python test class discovery
  python_functions (args):
                        Prefixes or glob names for Python test function and method discovery
  disable_test_id_escaping_and_forfeit_all_rights_to_community_support (bool):
                        Disable string escape non-ASCII characters, might cause unwanted side effects(use at your own risk)
  console_output_style (string):
                        Console output: "classic", or with additional progress information ("progress" (percentage) | "count" | "progress-even-when-capture-no" (forces progress even when capture=no)
  xfail_strict (bool):  Default for the strict parameter of xfail markers when not given explicitly (default: False)
  tmp_path_retention_count (string):
                        How many sessions should we keep the `tmp_path` directories, according to `tmp_path_retention_policy`.
  tmp_path_retention_policy (string):
                        Controls which directories created by the `tmp_path` fixture are kept around, based on test outcome. (all/failed/none)
  enable_assertion_pass_hook (bool):
                        Enables the pytest_assertion_pass hook. Make sure to delete any previously generated pyc cache files.
  junit_suite_name (string):
                        Test suite name for JUnit report
  junit_logging (string):
                        Write captured log messages to JUnit report: one of no|log|system-out|system-err|out-err|all
  junit_log_passing_tests (bool):
                        Capture log information for passing tests to JUnit report:
  junit_duration_report (string):
                        Duration time to report: one of total|call
  junit_family (string):
                        Emit XML for schema: one of legacy|xunit1|xunit2
  doctest_optionflags (args):
                        Option flags for doctests
  doctest_encoding (string):
                        Encoding used for doctest files
  cache_dir (string):   Cache directory path
  log_level (string):   Default value for --log-level
  log_format (string):  Default value for --log-format
  log_date_format (string):
                        Default value for --log-date-format
  log_cli (bool):       Enable log display during test run (also known as "live logging")
  log_cli_level (string):
                        Default value for --log-cli-level
  log_cli_format (string):
                        Default value for --log-cli-format
  log_cli_date_format (string):
                        Default value for --log-cli-date-format
  log_file (string):    Default value for --log-file
  log_file_level (string):
                        Default value for --log-file-level
  log_file_format (string):
                        Default value for --log-file-format
  log_file_date_format (string):
                        Default value for --log-file-date-format
  log_auto_indent (string):
                        Default value for --log-auto-indent
  pythonpath (paths):   Add paths to sys.path
  faulthandler_timeout (string):
                        Dump the traceback of all threads if a test takes more than TIMEOUT seconds to finish
  addopts (args):       Extra command line options
  minversion (string):  Minimally required pytest version
  required_plugins (args):
                        Plugins that must be present for pytest to run
  render_collapsed (string):
                        row(s) to render collapsed on open.
  max_asset_filename_length (string):
                        set the maximum filename length for assets attached to the html report.
  environment_table_redact_list (linelist):
                        a list of regexes corresponding to environment table variables whose values should be redacted from the report
  initial_sort (string):
                        column to initially sort on.
  generate_report_on_test (bool):
                        the HTML report will be generated after each test instead of at the end of the run.
```

上述参数的详细信息，请查阅第三章“pytest参数详解”的内容，本章节将针对几个常用场景下参数展开介绍。

#  9.3 配置文件pytest.ini

`pytest` 配置文件`pytest.ini`可以改变 `pytest` 的运行方式，它是一个固定的文件（名称固定，只能是 `pytest.ini`），读取配置信息，按指定的方式去运行。

`pytest.ini` 放在项目的根目录下。

简而言之，如果 `pytest.ini` 有该参数值，在执行的时候，先读取配置文件中的参数，然后取其他地方的（主函数/命令行中）。

## 9.3.1 应用场景

`pytest.ini`可用于多种场景，包括但不限制于：

- **预设命令行参数**：设置运行测试时默认使用的命令行参数。
- **自定义测试发现规则**：定义`pytest`查找测试用例时的文件模式和Python类、函数命名规则。
- **增加自定义测试标记**：定义新的标记（markers），为测试用例添加额外的元数据。
- **日志配置**：设定测试中的日志记录行为。
- **修改插件行为**：添加或修改特定`pytest`插件的配置规则。

## 9.3.2 pytest.ini 使用方法

在项目的根目录下创建名为`pytest.ini`的文件，并按照`INI`文件的格式编写所需的配置信息。

**请注意：**

* 整个项目有且仅有一个此文件，且位置、名称固定，不得更改；
* `pytest.ini` 不能使用任何中文符号，包括汉字、空格、引号、冒号等等。
* 在使用命令行参数时，通过`pytest.ini`设置的默认参数优先级高于命令行中直接给出的参数。
* 对于复杂的配置，考虑使用注释来解释特定配置项的目的，提升可维护性。
* 如果还配置了其他的`pytest`配置文件，如`tox.ini`或`pyproject.toml`，请注意它们之间参数设置的优先级和互斥情况。

如下`pytest.ini`文件中示例，中文信息只是注解，方便读者理解，实际使用时需要删除掉。

### 9.3.2.1 预设命令行参数

```ini
# content of pytest.ini
[pytest]
addopts = -vrs --cache-clear --full-trace -p no:warnings
```

上面的配置中，`addopts`选项是向命令行添加参数的好方法。在上面的配置文件中，每次运行pytest时，都会自动包含`-vrs`这三个选项。

`-v` 或 `--verbose`：增加测试运行的详细信息。在使用此选项时，每个测试函数在输出中都会有一行对应的信息，包括它的完整路径和结果。
`-r`：跟随于字符，指定测试结果的详细输出。例如，`-rs` 中的 `s` 和 `r` 是两个不同参数，它们用来控制什么类型的信息被包括在报告总结中，具体含义如下：

  - `s`：输出所有失败的测试用例的原因（如skipped tests）。
  - `r`：输出测试运行总结信息，通常与其他字母结合使用（如`rfE`），分别代表失败（fail）、错误（error）等，`-r` 后面没有跟任何字母，则代表输出所有可能的输出类型。

### 9.3.2.2 自定义测试发现规则

```ini
# content of pytest.ini
[pytest]
# Find Test Cases Catalog (可以指定多个)
testpaths = tests
# Test file patterns (可以指定多个模式)
python_files = test_*.py *_tests.py

# Test class patterns (默认以 Test 开头的类)
python_classes = *Test Test*

# Test method patterns (可以指定多个模式，通常以 test_ 开头)
python_functions = test_* *_test check_*
```

`testpaths`：指定测试文件的搜索路径。`pytest` 在运行时只会在指定的路径下查找和运行测试用例，这有助于优化测试的发现过程，尤其是当项目文件夹结构较复杂，包含许多非测试代码的文件时。

`python_files`: 设置文件模式，定义哪些文件被认为是测试文件。默认是 `test_*.py` 或者 `*_test.py`，上面的设置增加了 `*_tests.py` 也作为测试文件识别。

`python_classes`: 设置类模式，定义哪些类包含测试方法。默认是以 `Test` 开头的类，上面的设置扩展到任何包含 `Test` 或者以 `Test` 开头的类。

`python_functions`: 设置方法模式，定义哪些函数被视为测试用例。默认是以 `test_` 开头的函数，上面的设置增加了以 `_test` 结尾和以 `check_` 开头的函数。

如果要搜索的路径比较多，也可以分行书写，参考如下：

```ini
# content of pytest.ini
[pytest]
testpaths = 
    tests
    integration_tests
```

### 9.3.2.3 增加自定义测试标记

```ini
# pytest.ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    smoke: smoke tests cover the main functionality of the program.
    serial: mark tests that should be run serially and not in parallel.
```

在这个例子中，我们定义了三个标记，其中：

* 名为`slow`的标记
    你可以用它来标记那些运行缓慢的测试。现在你可以通过命令`pytest -m "not slow"`来跳过所有标记为慢的测试。
* 名为`smoke`的标记
    你可以用它来标记那些用于冒烟测试的测试。同理，可以通过命令`pytest -m "not smoke"`来跳过所有标记为冒烟测试的测试。
* 名为`serial`的标记
    你可以用它来标记那些只能串行无法并行执行的测试用例。同理，可以通过命令`pytest -m "not serial"`来跳过所有标记为串行测试的测试。

### 9.3.2.4 日志配置

在 `pytest.ini` 文件中，你可以配置日志记录，从而在测试执行过程中掌握更精细的日志信息。日志配置允许你设置日志级别、日志格式以及日志输出文件等。

以下是如何在 `pytest.ini` 中进行日志配置的示例：

```ini
# pytest.ini
[pytest]
log_cli = 1
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format = %Y-%m-%d %H:%M:%S

log_file = automation_log.txt
log_file_level = DEBUG
log_file_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_file_date_format = %Y-%m-%d %H:%M:%S
```

这里的配置做了如下设定：

- `log_cli`: 开启实时日志输出到控制台。
- `log_cli_level`: 设置控制台日志的级别。此处为 `INFO`，即只有 `INFO` 及以上级别的日志会被输出到控制台。
- `log_cli_format`: 定义控制台日志输出的格式，这里包括时间、日志级别、消息内容、文件名和行号。
- `log_cli_date_format`: 设置控制台日志的时间格式。

对于日志文件配置：

- `log_file`: 指定存储日志的文件路径。
- `log_file_level`: 设置日志文件的日志级别。此处为 `DEBUG`，意味着所有级别的日志都会被记录到文件中。
- `log_file_format`: 定义日志文件中每个日志条目的格式。
- `log_file_date_format`: 设置日志文件中时间戳的格式。

通过这些配置，你可以确保所有重要的测试日志记录都按照你希望的方式被捕获和显示，无论是在测试执行的实时输出中还是存储于日志文件中供后期分析使用。

配置完后，当你运行 `pytest` 时，将会看到按照指定格式输出的日志信息，并且所有记录都会保存到指定的文件中，这对于调试和追踪测试问题非常有帮助。

### 9.3.2.5 修改插件行为

在 `pytest` 中，插件是用来扩展框架功能的组件，它们可以添加新的命令行选项、生成报告、配置测试环境等。通过 `pytest.ini` 配置文件，你可以修改插件的默认行为，如启用或禁用插件、改变它们的行为，或是为它们提供必要的配置。

以下是在 `pytest.ini` 中修改插件行为的一些通用方法：

#### 9.3.2.5.1 禁用插件

使用 `addopts` 配置项，利用 `--disable-plugin` 选项可以禁用特定插件：

```ini
[pytest]
addopts = --disable-plugin plugin_name
```

#### 9.3.2.5.2 配置插件选项

某些插件允许通过命令行参数进行配置，这些参数也可以在 `pytest.ini` 中指定：

```ini
[pytest]
addopts = --plugin-option=value
```

#### 9.3.2.5.3 定制插件行为

有的插件从 `pytest.ini` 文件中读取配置选项。例如，`pytest-cov` 插件可以从配置文件中读取覆盖率相关的设置：

```ini
[pytest]
addopts = --cov=my_package --cov-report=html
```

或者，针对特定插件的配置可以放在它自己的段落中：

```ini
[coverage:run]
branch = True

[coverage:report]
omit = 
    */tests/*
    */migrations/*
```

#### 9.3.2.5.4 覆盖配置

如果你在项目中使用了多个插件，它们各自可能有独立的章节，在 `pytest.ini` 中可以并存，如下所示：

```ini
[pytest]
addopts = --html=report.html

[html]
title = My Project Test Report
description = Detailed test results for My Project.
```

这里 `pytest` 默认选项设定了生成 HTML 报告，并在 `[html]` 部分定制了报告的标题和描述。

## 9.3.3 结合使用 `conftest.py` 和 `pytest.ini`

`conftest.py` 和 `pytest.ini` 可以结合使用，以充分利用 `pytest` 的配置灵活性。`conftest.py` 更适用于编写可以在测试中使用的代码，如fixture和hook功能，而 `pytest.ini` 更适合用于配置固定的配置数据。

当测试项目越来越大时，合理利用这两种配置方式可以帮助维持测试代码的可维护性和可扩展性：

- `conftest.py` 中定义的 fixture 和hook函数可以根据 `pytest.ini` 中的配置被相应地调整和使用。
- `pytest.ini` 提供的测试发现规则可以使 `conftest.py` 中的 fixture 和hook函数在不同的测试场景中灵活应用。
- `conftest.py` 可以根据 `pytest.ini` 中的配置进行调整，例如，根据 `addopts` 中的特定选项来启动或禁用某些测试设置或行为。
- `conftest.py`可以存在多个，`pytest.ini`只能存在一个。

## 9.3.4 使用 pytest.ini 的优势

拥有一个`pytest.ini`文件可以让你:

- 更好地控制测试用例执行的方式，并可以提供给团队统一的测试行为标准。
- 节省时间，因为你不用在命令行中重复输入相同的参数。
- 为项目定制特殊的测试用例发现规则和测试标记，使得测试结果更加准确。

## 9.3.5 小结

`pytest.ini`作为`pytest`的核心配置文件，允许开发人员预先设定测试行为，提升项目的自动化水平，减轻程序员的工作负担。透过对`pytest.ini`的深入理解和合理应用，可以让你更精确地控制自动化测试的行为，简化测试命令的复杂性，构建出高效、可维护并且符合项目特性的测试环境。通过优化配置，`pytest`能够更完美地融入你的开发工作流，辅助你提高软件开发的质量、效率和可靠性。

# 9.4 配置文件pyproject.toml

`pyproject.toml` 是一个配置文件，由 PEP 518 引入，用来替代 `setup.py`。`PyPI` 的旧时代因为规范太松散了，每个项目的结构都五花八门。现在好了，`pyproject.toml` 它在 Python 项目的结构上都有一个推荐风式，统一以前散布在 `setup.py`、`setup.cfg`、`requirements.txt`、`tox.ini` 和其他配置文件中的项目元数据和配置信息，如配置工具链中的打包、构建系统、静态分析工具等。它是一个基于 `TOML`（Tom’s Obvious, Minimal Language）语言的配置文件，其设计简洁明了，易于阅读和编写，目的是为 Python 项目提供统一的配置文件格式。从 Python 3.6 开始，`pyproject.toml` 文件开始被当工具支持，它用来配置测试框架，如 `pytest`。

配置 `pytest` 的 `pyproject.toml` 大致的结构如下所示：

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "-v"
testpaths = [
    "tests",
    "integration_tests"
]
filterwarnings = [
    "ignore::UserWarning",
]
```

以上配置等同于 `pytest.ini` 中的以下内容：

```ini
# pytest.ini
[pytest]
addopts = -v
testpaths =
    tests
    integration_tests
filterwarnings =
    ignore::UserWarning
```

在这个 `pyproject.toml` 示例中:

- `[tool.pytest.ini_options]` 是 `pytest` 使用的配置节。
- `addopts` 用于设置命令行参数（在这个例子里，添加了 `-v` 参数来显示更详细的信息）。
- `testpaths` 列出了 `pytest` 应该搜索测试的路径。
- `filterwarnings` 用于设定警告过滤规则，例如忽略特定类型的警告。

此外，`pyproject.toml` 可以用来配置多个工具的参数：

```toml
# pyproject.toml
[build-system]
requires = ["setuptools", "wheel"]  # 指定构建过程中的依赖
build-backend = "setuptools.build_meta" # 指定构建后端

# 下面是针对 pytest 的配置示例
[tool.pytest.ini_options]
addopts = "-v -s" # 设置 pytest 命令行默认选项
testpaths = [  # 指定测试文件搜索路径
    "tests",
    "integration_tests"
]
python_files = ["test_*.py", "*_tests.py", "test*.py"]  # 识别测试文件的模式
python_classes = ["*Tests", "Test*"]  # 识别测试类的模式
python_functions = ["test_*", "*_test"]  # 识别测试函数的模式

# 以下是其他工具的配置示例
[tool.black]
line-length = 88
include = '\.pyi?$'
exclude = '' # 可以在这里指定排除的文件或目录模式

[tool.isort]
profile = "black"
```

在这个示例中：

- `[build-system]` 部分指定了你的项目为了正确构建所需要的依赖和后端。
- `[tool.pytest.ini_options]` 用于指定 `pytest` 的配置，类似于你在 `pytest.ini` 文件中所做的配置。
- `[tool.black]` 和 `[tool.isort]` 部分分别为代码格式化工具 black 和 `isort `提供了配置信息。



`pyproject.toml` 的优势在于可以集中管理项目的构建、打包、测试等流程配置，简化项目的维护工作，并且易于协作和共享。此外，`TOML` 的格式比`setup.py`更容易阅读和编辑，并且避免了执行任意 Python 代码造成的安全风险。此外，将项目依赖隔离在 `pyproject.toml` 文件中也意味着可以在没有安装任何项目依赖的情况下构建分发包，这为构建提供了一个更干净的环境。

要在 `pyproject.toml` 文件中启用 `pytest` 配置，将文件放置在项目的根目录下，`pytest` 会自动检测和应用这些配置。请注意，从 `pytest 6.0` 版本开始支持在 `pyproject.toml` 文件中配置 `pytest`。

项目开发者应该参考各工具的官方文档来确定最佳实践和所支持的 `pyproject.toml` 配置选项，以充分利用这个强大工具。

# 9.5 配置文件tox.ini

`tox.ini` 是一个配置文件，用于 `tox` 自动化测试工具。`tox` 旨在为 Python 项目提供一个简单的方式进行自动化测试，包括测试包的安装、运行测试用例以及检查编码风格等，它创建隔离的 Python 环境来进行这些任务，这些测试环境可以基于不同的 Python 版本，以及不同的依赖包配置。。

`tox.ini` 文件通常位于项目的根目录中，由 `tox` 自动识别，并包含了创建测试环境、安装依赖、运行命令和测试的详细指令。这个文件使用 `INI` 格式，并被分割成多个部分，每个部分代表一种特定的环境或设置。

`tox.ini`文件结构分为三部分：

* [tox] 部分：定义全局 `tox` 配置，如要创建的环境列表 `envlist` 和是否独立构建项目 `isolated_build`。
* [testenv] 部分：用于配置默认测试环境的选项，它可以指定用于每个环境的依赖 `deps` 和测试命令 `commands`。当没有特定环境时，这将作为默认环境配置。
* [testenv:envname] 部分：用于定义特定测试环境的选项，比如代码风格检查 `flake8`。它可以覆盖 `[testenv]` 中的配置。环境名称（如 `flake8`）会放在 `testenv:` 后面。

以下是一个基本的 `tox.ini` 配置文件示例：

```ini
# tox.ini 文件示例

[tox]
envlist = py36, py37, py38  # 定义 tox 应该创建和测试的环境列表
isolated_build = True

[testenv]
deps = pytest  # 指定运行测试所需的依赖包
commands = pytest  # 指定运行测试所用的命令

[testenv:flake8]
deps = flake8  # 指定 Flake8 环境所需的依赖
commands = flake8 project_directory  # 指定运行 Flake8 所用的命令
```

在这个例子中：

- `[tox]` 部分定义了不同的测试环境（`envlist`），指定了 `tox` 应该要创建的环境列表。示例中的环境列表包含 Python 3.6 和 3.7 的测试环境以及一个 `flake8` 风格检查环境。
- `[testenv]` 部分是默认的测试环境配置。在该范围内定义了安装依赖（`deps`）和执行的命令（`commands`）。这里使用了 `pytest` 作为测试运行器。
- `[testenv:flake8]` 是一个特定环境的配置，覆盖了 `[testenv]` 部分的设置。`flake8` 环境仅用于运行 `Flake8` 代码风格检查。环境名称（比如 `flake8`）后跟随 `:` 号。

再来看一个更实际的 `tox.ini` 示例，可能涵盖多个不同的 Python 版本，并且还包括了代码风格检查：

```ini
[tox]
envlist = py36, py37, py38, flake8

[testenv]
deps =
    pytest
    pytest-cov
commands =
    pytest --cov=your_package_name tests/

[testenv:flake8]
deps = flake8
commands = flake8 your_package_name tests/
```

在这个示例中：

- `envlist` 包含了三个 Python 版本的测试环境和一个代码风格检查环境。
- 在每个 `testenv` 中，`pytest` 和 `pytest-cov` 被设置为依赖，测试命令包含了生成覆盖率报告。
- 在 `flake8` 环境中，指定了 `flake8` 作为依赖，并且 `commands` 为执行 `flake8` 的命令。

通过上述 `tox.ini` 文件配置，`tox` 可以自动切换到不同的环境来运行同一套测试用例，并且执行代码风格检查。我们仅需在命令行运行 `tox` 命令，就可以执行所有环境的测试。这极大地简化了开发人员的测试工作，并可以轻松集成到持续集成（CI）流程中。

如果项目中同时存在 `tox.ini` 和 `pytest.ini` 文件，`tox` 将使用 `tox.ini` 文件中的配置来创建测试环境，在这些环境中运行 `pytest` 时则使用 `pytest.ini` 中的配置。通过这种方式，你可以为项目构建一个简洁的自动化测试流程，使得将新的测试变得更容易，并确保在每次提交或部署之前验证代码质量。

# 9.6 配置文件 setup.cfg

`setup.cfg` 是一个 `INI` 格式的配置文件，它通常用于存储 Python 包的元数据和配置信息，可以被多个工具使用，包括 `setuptools`、wheel 和 `pytest`。在使用 `setuptools` 构建和分发 Python 包时，`setup.cfg` 可以包含 `setup.py` 脚本中相同的元数据和选项。除了与包构建相关的设置，`setup.cfg` 也可以用于配置 `pytest`，虽然 `pytest` 建议使用独立的 `pytest.ini` 文件或 `pyproject.toml` 文件进行配置。

## 9.6.1 setup.cfg 文件的结构

`setup.cfg` 文件可以包含多个不同的部分，用于配置不同的工具或任务。对于 `pytest`，相关配置应放在 `[tool:pytest]` 部分。

## 9.6.2 pytest 配置示例

以下是如何在 `setup.cfg` 文件中配置 `pytest` 的示例：

```ini
# setup.cfg 文件中的 pytest 配置示例

[tool:pytest]
addopts = -v -ra
testpaths =
    tests
    integration_tests
python_files = test_*.py
python_classes = *Tests
python_functions = test_*
```

在此配置中：

- `addopts` 用于为 `pytest` 运行添加默认的命令行选项。在这个例子中，`-v` 表示详细模式，而 `-ra` 用于显示额外的测试摘要信息，包括所有测试（除了通过的测试）。
- `testpaths` 列出了 `pytest` 应搜索测试文件的路径。这里指定了 `tests` 和 `integration_tests` 目录。
- `python_files` 指定了 `pytest` 应识别为测试文件的模式。此设置将所有匹配 `test_*.py` 模式的文件识别为包含测试的 Python 文件。
- `python_classes` 指定了哪些 Python 类应当被视为包含测试方法的测试类。默认情况下，`pytest` 将识别任何类名包含 `Test` 的 Python 类。
- `python_functions` 指定了哪些函数应当被视为测试。在这个例子中，任何使用 `test_` 前缀的函数都将作为测试用例运行。

当使用 `setup.cfg` 为 `pytest` 配置时，请确保将配置项放置在正确的节下，且文件位于合适的目录结构中。通常，这意味着你的 `setup.cfg` 文件应该位于项目的根目录。

## 9.6.3 setuptools 和 pytest 结合的完整配置示例

一个包含 `setuptools` 元数据和 `pytest` 配置的 `setup.cfg` 完整示例可能如下：

```ini
# setuptools 配置
[metadata]
name = example_package
version = 0.1.0
description = An example package
long_description = file: README.md

[options]
packages = find:
install_requires =
    requests
    numpy

# pytest 配置
[tool:pytest]
addopts = -v -s --cov=example_package --cov-report=term-missing
testpaths = 
    tests
python_files = test_*.py *_test.py

# 其他工具配置
[flake8]
max-line-length = 120
exclude =
    .git,
    __pycache__,
    build,
    dist
```

此配置中：

- `[metadata]` 和 `[options]` 部分由 `setuptools` 使用，包含了包名、版本、描述，以及依赖信息。
- `[tool:pytest]` 部分是` pytest` 的配置，其中 `--cov=example_package` 是 `pytest-cov` 插件的配置，用于生成测试覆盖率报告。
- `[flake8]` 是 `flake8` 插件的配置示例，它定义了代码风格检查的规则。

在项目根目录中包含这样一个 `setup.cfg` 文件可以让你集中管理项目设置，包括打包和测试相关的配置，同时为多个工具提供了配置，无需单独分散的配置文件。这种方式可以使项目结构更加简洁、维护更为方便。

# 9.7 pytest配置文件读取顺序

## 9.7.1 配置文件读取顺序

`pytest` 在寻找和读取配置文件时，遵循一定的优先级顺序。这些配置文件中可以定义测试行为和多个相关配置参数。如果存在多个配置文件，`pytest` 会按照如下优先级顺序读取它们：

1. `pytest.ini`: 这是 `pytest` 专用的配置文件，当存在时，它会被 `pytest` 首先读取。如果你的项目中有 `pytest.ini` 文件，它会覆盖其他配置文件中的设置。

2. `pyproject.toml`: 作为现代工具的配置文件标准（由 PEP 518 提出），如果项目根目录下有 `pyproject.toml` 文件，并且它包含了 `[tool.pytest.ini_options]` 部分，那么 `pytest` 会读取这部分内容作为配置。

3. `tox.ini`: 如果没有 `pytest.ini` 或 `pyproject.toml`（包含 `[tool.pytest.ini_options]` 部分），`pytest` 会查找 `tox.ini` 文件。如果 `tox.ini` 中有 `[pytest]` 部分，`pytest` 将会读取这部分配置。

4. `setup.cfg`: 如果以上三个文件都不存在，`pytest` 会查找 `setup.cfg` 文件进行配置。`pytest` 的配置需要放在 `[tool:pytest]` 部分。

注意事项：

- `pytest` 一旦找到一个配置文件并从中读取配置，就不会继续查找其他配置文件。
- 配置参数不会从不同的配置文件中合并；`pytest` 只会采用找到的第一个配置文件中的参数。
- 通常情况下，建议使用一个配置文件，这样可以避免配置分散和潜在的冲突。
- 即使在多个配置文件中定义了相同的配置项，`pytest` 也只会应用它在优先级最高的配置文件中找到的设置。



## 9.7.2 覆盖默认的配置文件读取顺序

我们在第三章节**pytest参数详解**一文中有介绍过`--override-ini` 选项，这里借助此选项来覆盖默认的配置文件读取顺序。

通过 `--override-ini` 选项，我们可以指定一个自定义的配置文件作为`pytest`的配置文件，而不是使用默认的配置文件。这对于需要在不同的环境或测试场景中使用不同的配置文件非常有用。

以下是使用 `--override-ini` 选项来覆盖默认配置文件读取顺序的步骤：

* 找到你想要用作配置文件的自定义配置文件

这可以是任何有效的`pytest`配置文件，如 `pytest.ini`、`pytest.cfg` 或其他支持的配置文件。

* 指定自定义配置文件路径

在运行`pytest`命令时，使用 `--override-ini` 选项并指定你的自定义配置文件的路径。例如：

```shell
pytest --override-ini path/to/custom_config.ini
```

自此，`pytest`将使用你指定的自定义配置文件作为配置文件，而不是使用默认的配置文件。这样，你可以根据需要更改和自定义`pytest`的行为和设置。

**请注意：**

使用 `--override-ini` 选项会完全覆盖默认的配置文件读取顺序。因此，在使用这个选项时，确保你的自定义配置文件包含了所有必要的配置选项，以避免配置丢失或不完整。另外，此选项设置的只是临时值，运行当前的`pytest`命令时有效，不会改变配置文件的值，下一次运行`pytest`时还是会读取配置文件的设置。



# 9.8 pytest的warning处理机制

在使用`pytest`进行测试时，可能会遇到一些警告信息，这些警告有时是有用的，因为它们可以提示潜在的问题。然而，某些情况下，你可能需要忽略特定的警告。`pytest`提供了几种方法来处理警告信息。

## 9.8.1 使用pytest配置文件忽略特定警告

你可以在`pytest.ini`文件中添加一个`filterwarnings`选项来忽略特定的警告：

```ini
# pytest.ini
[pytest]
filterwarnings =
    ignore::UserWarning
    ignore::DeprecationWarning
```

以上配置会忽略所有的`UserWarning`和`DeprecationWarning`警告。你还可以采用更精确的方法，仅忽略某个库或模块发出的警告：

```ini
# pytest.ini
[pytest]
filterwarnings =
    ignore::UserWarning:module_name.*
    ignore::DeprecationWarning:another_module.*
```

## 9.8.2 使用pytest配置文件禁用warnings插件方式

你可以在`pytest.ini`文件中`addopts`参数下添加`-p no:warnings`选项来禁用所有警告：

```shell
[pytest]
addopts = -p no:warnings
```

## 9.8.3 在命令行中使用`-W`选项

你也可以在命令行中使用`-W`（或`--pythonwarnings`）选项运行`pytest`，这可以用来忽略特定的警告。

例如，忽略所有`DeprecationWarning`：

```bash
pytest -W ignore::DeprecationWarning
```

或者，仅忽略来自特定模块的`DeprecationWarning`：

```bash
pytest -W ignore::DeprecationWarning:module_name.*
```

## 9.8.4 在代码中使用`warnings`模块处理警告

Python的`warnings`模块同样可以用来控制警告的显示，可以在测试代码中添加特定的警告过滤器：

```python
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
```

将这段代码放在测试的配置文件或者在某个夹具(fixture)中，可以在运行测试之前忽略掉特定类型的警告。

## 9.8.5 使用`pytest.mark.filterwarnings`忽略特定测试的警告

如果你只想忽略特定测试发出的警告，可以使用`pytest.mark.filterwarnings`装饰器：

```python
import pytest

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_example():
    # ...
```

以上代码在运行`test_example`函数时忽略`DeprecationWarning`警告。

**注意**：一般来说，警告是编程语言或者框架用来让你知道代码中潜在问题的一种方式。在决定忽略警告之前，首先应当考虑修复产生警告的原因。只有当你确信这个警告是可以安全忽略的时候，才应该选择忽略警告。

## 9.8.6 忽略所有告警

在`pytest`中忽略所有警告可以通过几种方法来实现。以下是常见的几种方式：

### 9.8.6.1 命令行参数

使用命令行参数是一种快速简便的方法：

```bash
pytest -p no:warnings
```

这将在运行时关闭所有警告的显示。

### 9.8.6.2 pytest.ini配置

在你的`pytest.ini`文件中配置警告的过滤以忽略所有警告：

```ini
[pytest]
addopts = -p no:warnings
```

这样设置后，每次使用`pytest`时都会应用此选项。

### 9.8.6.3 环境变量

设置环境变量`PYTHONWARNINGS`，这个变量会影响Python解释器的警告过滤系统：

```bash
export PYTHONWARNINGS="ignore"
```

在运行`pytest`前设置这个变量，可以忽略所有的Python警告。

### 9.8.6.4 在测试代码中使用`warnings`模块

如果你想在代码中显式地忽略警告，可以使用Python的`warnings`模块。例如，你可以在测试的配置文件（如`conftest.py`）或者在测试执行前运行的某个代码段中，添加以下代码：

```python
import warnings
warnings.filterwarnings("ignore")
```

这将在整个测试会话中忽略所有警告。

记住，虽然有时候忽略警告风险不大，但是最佳实践还是审查和解决这些警告，而不是简单地将它们隐藏。这是因为警告经常是代码潜在问题的指示器，解决这些问题可以帮助避免将来的错误和不稳定。特别是`DeprecationWarning`，通常意味着被使用的某个功能在未来的版本中可能会被移除或更改，因此应当特别关注。

## 9.8.7 禁用 warning 实践


示例参考参考如下：

```python
# content of test_pytest_warning.py
import pytest
import warnings


def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


# @pytest.mark.filterwarnings("ignore:api v1") 这里先注释掉，根据用例需要再放开注释
# @pytest.mark.filterwarnings("ignore::UserWarning")
def test_one():
    assert api_v1() == 1

```

如果不禁用warning，运行效果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest test_pytest_warnning.py 
============================== test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-8
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_pytest_warnning.py .                                             [100%]

============================== warnings summary =============================
test_pytest_warnning.py::test_one
  /root/code/chapter1-8/test_pytest_warnning.py:6: UserWarning: api v1, should use functions from v2
    warnings.warn(UserWarning("api v1, should use functions from v2"))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
====================== 1 passed, 1 warning in 0.01s =========================
root@Gavin:~/code/chapter1-8#
```

### 9.8.7.1 命令行方式禁用warnings的方式

#### 9.8.7.1.1 禁用所有warnings

```shell
# 禁用所有warnings，通常不使用，禁用范围过大
pytest --disable-warnings
```

#### 9.8.7.1.2 使用-W选项忽略warning

 :: 表示具体的警告类名称   :表示匹配告警中`msg`的子串。

```shell
pytest -W ignore::UserWarning
pytest -W "ignore:api v1"   # 这里的 "api v1"，为上面示例代码中 'warnings.warn(UserWarning("api v1, should use functions from v2"))' 的子串
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest --disable-warnings test_pytest_warnning.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-8
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_pytest_warnning.py .                                               [100%]

============================ 1 passed, 1 warning in 0.01s =====================
root@Gavin:~/code/chapter1-8# 
root@Gavin:~/code/chapter1-8# pytest -W ignore::UserWarning test_pytest_warnning.py 
============================ test session starts ===============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-8
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_pytest_warnning.py .                                              [100%]

=============================== 1 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-8# pytest -W "ignore:api v1"
=============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-8
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_pytest_warnning.py .                                              [100%]

================================ 1 passed in 0.01s =============================
root@Gavin:~/code/chapter1-8#
```

### 9.8.7.2 使用装饰器@pytest.mark.filterwarnings

在示例代码测试函数前使用如下装饰器来消除告警：

```python
# : 表示匹配告警信息中的msg的子串
@pytest.mark.filterwarnings("ignore:api v1") 

# :: 表示匹配告警信息中的告警类的类名，例如给出代码示例中的告警即可使用如下方式过滤告警
@pytest.mark.filterwarnings("ignore::UserWarning")
```

### 9.8.7.3 pytest.ini中使用ignore

在`pytest.ini`中进行告警过滤，该文件需要存放到项目根目录，示例参考如下：

```shell
[pytest]
filterwarnings =
    ignore::UserWarning
    ignore::urllib3.exceptions.InsecureRequestWarning
```

如上几种方式均可达到禁用`pytest warning`效果，用户可按照自己的喜好选择某种禁用告警方式。



# 9.9 本章小结

在本章中，我们学习了`pytest`的配置文件以及相关的配置文件读取顺序和处理方法。`pytest`提供了几种不同类型的配置文件，让我们能够根据需要自定义测试框架的行为和设置。

我们首先介绍了`pytest`的默认配置文件 `pytest.ini`，它是一个基本的配置文件，可以在项目根目录下进行配置。我们可以使用它来设置全局的`pytest`选项和插件，以及定义全局的fixture和标记。

其次，我们了解了项目级别的配置文件 `pyproject.toml` 和 `tox.ini`。这些配置文件可以用于更复杂的项目结构和测试环境，以定义项目级别的`pytest`选项和插件，以及其他项目相关的配置。

我们还介绍了用户级别的配置文件 `pytest.ini` 和 `pytest.cfg`，它们位于用户主目录下，用于定义用户级别的`pytest`选项和插件。这些配置文件可以覆盖项目级别的配置，以满足个人偏好和需求。

在配置文件的读取顺序方面，我们了解了`pytest`的默认读取顺序。`pytest`会按照一定的顺序搜索和读取配置文件，包括项目级别和用户级别的配置文件。我们还介绍了如何使用 `--override-ini` 选项来覆盖默认的配置文件读取顺序，以适应特定的需求。

最后，我们详细讨论了相关的warning处理方法。当`pytest`检测到配置文件中存在无效的选项或错误的格式时，会生成相应的warning提示。我们可以通过设置 `filterwarnings` 选项来控制是否显示warning信息，以及如何处理这些warning消息。

总结而言，`pytest`的配置文件提供了一种灵活和可定制化的方式来配置和管理测试框架的行为和设置。通过合理使用不同类型的配置文件，可以满足不同项目和个人的需求。同时，了解配置文件的读取顺序和处理方法，可以帮助我们更好地理解和解决相关的warning问题。
