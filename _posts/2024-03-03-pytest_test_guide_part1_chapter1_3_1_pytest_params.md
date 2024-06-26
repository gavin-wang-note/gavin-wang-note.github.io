---
title: 《pytest测试指南》-- 章节1-3 pytest参数详解PART1
date: 2024-03-03 21:09:15
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
summary: 《pytest测试指南》一书 章节1-3 pytest参数详解PART1。
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
---

# 概述

`pytest` 提供了丰富的参数，本文以 `pytest 7.4.0` 版本为基础，在未安装任何额外插件情况下，分类阐述参数的使用方法与介绍：

* positional arguments

* general（通用）
* Reporting （报告）
* pytest-warnings （告警）
* collection （信息收集）
* test session debugging and configuration （测试会话调试和配置）
* logging （日志记录）
* [pytest] ini-options （pytest配置文件--pytest.ini|tox.ini|setup.cfg|pyproject.toml ）



说明：

* 对于一些常用参数，在本书后续独立章节详细介绍。
* 本文以 `pytest 7.4.0` 版本下展示的参数进行说明描述，`pytest` 版本不同，参数会有些许差异，所以你应当参照你所使用的 `pytest` 版本的官方文档以获得最准确的信息。
* 参数比较多，内容比较长，拆分成三部分介绍，另外两部分参考如下链接：
[Part2](https://gavin-wang-note.github.io/2024/05/22/pytest_test_guide_part1_chapter1_3_2_pytest_params/)
[Part3](https://gavin-wang-note.github.io/2024/05/23/pytest_test_guide_part1_chapter1_3_3_pytest_params/)



# 3.1 pytest 参数介绍与示例

## 3.1.1 查看pytest所有可用参数

可以使用`pytest -h` 或者 `pytest --help` ，查看所有可用参数：

```shell
root@Gavin:~# pytest -h
usage: pytest [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

general:
  -k EXPRESSION         Only run tests which match the given substring expression. An                             expression is a Python evaluatable expression where all names are                         substring-matched against test names and their parent classes.                           Example: -k 'test_method or test_other' matches all test                                 functions and classes whose name contains 'test_method' or                               'test_other', while -k 'not test_method' matches those that don't                         contain 'test_method' in their names. -k 'not test_method
                        and not test_other' will eliminate the matches. Additionally                             keywords are matched to classes and functions containing extra                           names in their 'extra_keyword_matches' set, as well as functions                         which have names assigned directly to them. The matching is case-                         insensitive.
  -m MARKEXPR           Only run tests matching given mark expression. For example: -m                           'mark1 and not mark2'.
  --markers             show markers (builtin, plugin and per-project ones).
  -x, --exitfirst       Exit instantly on first error or failed test
  --fixtures, --funcargs
                        Show available fixtures, sorted by plugin appearance (fixtures 
                        with leading '_' are only shown with '-v')
  --fixtures-per-test   Show fixtures per test
  --pdb                 Start the interactive Python debugger on errors or 
                        KeyboardInterrupt
  --pdbcls=modulename:classname
                        Specify a custom interactive Python debugger for use with 
                        --pdb.For example: --pdbcls=IPython.terminal.debugger:TerminalPdb
  --trace               Immediately break when running each test
  --capture=method      Per-test capturing method: one of fd|sys|no|tee-sys
  -s                    Shortcut for --capture=no
  --runxfail            Report the results of xfail tests as if they were not marked
  --lf, --last-failed   Rerun only the tests that failed at the last run (or all if 
                        none failed)
  --ff, --failed-first  Run all tests, but run the last failures first. This may re-order
                        tests and thus lead to repeated fixture setup/teardown.
  --nf, --new-first     Run tests from new files first, then the rest of the tests sorted
                        by file mtime
  --cache-show=[CACHESHOW]
                        Show cache contents, don't perform collection or tests. Optional
                        argument: glob (default: '*').
  --cache-clear         Remove all cache contents at start of test run
  --lfnf={all,none}, --last-failed-no-failures={all,none}
                        Which tests to run with no previously (known) failures
  --sw, --stepwise      Exit on test failure and continue from last failing test next
                        time
  --sw-skip, --stepwise-skip
                        Ignore the first failing test but stop on the next failing test.                         Implicitly enables --stepwise.

Reporting:
  --durations=N         Show N slowest setup/test durations (N=0 for all)
  --durations-min=N     Minimal duration in seconds for inclusion in slowest list.
                        Default: 0.005.
  -v, --verbose         Increase verbosity
  --no-header           Disable header
  --no-summary          Disable summary
  -q, --quiet           Decrease verbosity
  --verbosity=VERBOSE   Set verbosity. Default: 0.
  -r chars              Show extra test summary info as specified by chars: (f)ailed,
                        (E)rror, (s)kipped, (x)failed, (X)passed, (p)assed, (P)assed with
                        output, (a)ll except passed (p/P), or (A)ll. (w)arnings are 
                        enabled by default (see
                        --disable-warnings), 'N' can be used to reset the list. (default:
                        'fE').
  --disable-warnings, --disable-pytest-warnings
                        Disable warnings summary
  -l, --showlocals      Show locals in tracebacks (disabled by default)
  --no-showlocals       Hide locals in tracebacks (negate --showlocals passed through
                        addopts)
  --tb=style            Traceback print mode (auto/long/short/line/native/no)
  --show-capture={no,stdout,stderr,log,all}
                        Controls how captured stdout/stderr/log is shown on failed tests.
                        Default: all.
  --full-trace          Don't cut any tracebacks (default is to cut)
  --color=color         Color terminal output (yes/no/auto)
  --code-highlight={yes,no}
                        Whether code should be highlighted (only if --color is also
                        enabled). Default: yes.
  --pastebin=mode       Send failed|all info to bpaste.net pastebin service
  --junit-xml=path      Create junit-xml style report file at given path
  --junit-prefix=str    Prepend prefix to classnames in junit-xml output

pytest-warnings:
  -W PYTHONWARNINGS, --pythonwarnings=PYTHONWARNINGS
                        Set which warnings to report, see -W option of Python itself
  --maxfail=num         Exit after first num failures or errors
  --strict-config       Any warnings encountered while parsing the `pytest` section of
                        the configuration file raise errors
  --strict-markers      Markers not registered in the `markers` section of the 
                        configuration file raise errors
  --strict              (Deprecated) alias to --strict-markers
  -c FILE, --config-file=FILE
                        Load configuration from `FILE` instead of trying to locate one of
                        the implicit configuration files.
  --continue-on-collection-errors
                        Force test execution even if collection errors occur
  --rootdir=ROOTDIR     Define root directory for tests. Can be relative path: 
                        'root_dir', './root_dir', 'root_dir/another_dir/'; 
                        absolute path: '/home/user/root_dir'; path with variables: 
                        '$HOME/root_dir'.

collection:
  --collect-only, --co  Only collect tests, don't execute them
  --pyargs              Try to interpret all arguments as Python packages
  --ignore=path         Ignore path during collection (multi-allowed)
  --ignore-glob=path    Ignore path pattern during collection (multi-allowed)
  --deselect=nodeid_prefix
                        Deselect item (via node id prefix) during collection 
                        (multi-allowed)
  --confcutdir=dir      Only load conftest.py's relative to specified dir
  --noconftest          Don't load any conftest.py files
  --keep-duplicates     Keep duplicate tests
  --collect-in-virtualenv
                        Don't ignore tests in a local virtualenv directory
  --import-mode={prepend,append,importlib}
                        Prepend/append to sys.path when importing test modules and
                        conftest files. Default: prepend.
  --doctest-modules     Run doctests in all .py modules
  --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}
                        Choose another output format for diffs on doctest failure
  --doctest-glob=pat    Doctests file matching pattern, default: test*.txt
  --doctest-ignore-import-errors
                        Ignore doctest ImportErrors
  --doctest-continue-on-failure
                        For a given doctest, continue to run after the first failure

test session debugging and configuration:
  --basetemp=dir        Base temporary directory for this test run. (Warning: this 
                        directory is removed if it exists.)
  -V, --version         Display pytest version and information about plugins. When given
                        twice, also display information about plugins.
  -h, --help            Show help message and configuration info
  -p name               Early-load given plugin module name or entry point 
                        (multi-allowed). To avoid loading of plugins, use the `no:`
                        prefix, e.g. `no:doctest`.
  --trace-config        Trace considerations of conftest.py files
  --debug=[DEBUG_FILE_NAME]
                        Store internal tracing debug information in this log file. 
                        This file is opened with 'w' and truncated as a result, care
                        advised. Default: pytestdebug.log.
  -o OVERRIDE_INI, --override-ini=OVERRIDE_INI
                        Override ini option with "option=value" style, e.g. 
                        `-o xfail_strict=True -o cache_dir=cache`.
  --assert=MODE         Control assertion debugging tools.
                        'plain' performs no assertion debugging.
                        'rewrite' (the default) rewrites assert statements in test 
                        modules on import to provide assert expression information.
  --setup-only          Only setup fixtures, do not execute tests
  --setup-show          Show setup of fixtures while executing tests
  --setup-plan          Show what fixtures and tests would be executed but don't execute 
                        anything

logging:
  --log-level=LEVEL     Level of messages to catch/display. Not set by default, so it
                        depends on the root/parent log handler's effective level, where
                        it is "WARNING" by default.
  --log-format=LOG_FORMAT
                        Log format used by the logging module
  --log-date-format=LOG_DATE_FORMAT
                        Log date format used by the logging module
  --log-cli-level=LOG_CLI_LEVEL
                        CLI logging level
  --log-cli-format=LOG_CLI_FORMAT
                        Log format used by the logging module
  --log-cli-date-format=LOG_CLI_DATE_FORMAT
                        Log date format used by the logging module
  --log-file=LOG_FILE   Path to a file when logging will be written to
  --log-file-level=LOG_FILE_LEVEL
                        Log file logging level
  --log-file-format=LOG_FILE_FORMAT
                        Log format used by the logging module
  --log-file-date-format=LOG_FILE_DATE_FORMAT
                        Log date format used by the logging module
  --log-auto-indent=LOG_AUTO_INDENT
                        Auto-indent multiline messages passed to the logging module.
                        Accepts true|on, false|off or an integer.
  --log-disable=LOGGER_DISABLE
                        Disable a logger by name. Can be passed multiple times.

[pytest] ini-options in the first pytest.ini|tox.ini|setup.cfg|pyproject.toml file found:

  markers (linelist):   Markers for test functions
  empty_parameter_set_mark (string):
                        Default marker for empty parametersets
  norecursedirs (args): Directory patterns to avoid for recursion
  testpaths (args):     Directories to search for tests when no files or directories are
                        given on the command line
  filterwarnings (linelist):
                        Each line specifies a pattern for warnings.filterwarnings. 
                        Processed after -W/--pythonwarnings.
  usefixtures (args):   List of default fixtures to be used with this project
  python_files (args):  Glob-style file patterns for Python test module discovery
  python_classes (args):
                        Prefixes or glob names for Python test class discovery
  python_functions (args):
                        Prefixes or glob names for Python test function and method
                        discovery
  disable_test_id_escaping_and_forfeit_all_rights_to_community_support (bool):
                        Disable string escape non-ASCII characters, might cause unwanted
                        side effects(use at your own risk)
  console_output_style (string):
                        Console output: "classic", or with additional progress 
                        information ("progress" (percentage) | "count" | 
                        "progress-even-when-capture-no" (forces progress even when 
                        capture=no)
  xfail_strict (bool):  Default for the strict parameter of xfail markers when not given
                        explicitly (default: False)
  tmp_path_retention_count (string):
                        How many sessions should we keep the `tmp_path` directories, 
                        according to `tmp_path_retention_policy`.
  tmp_path_retention_policy (string):
                        Controls which directories created by the `tmp_path` fixture are 
                        kept around, based on test outcome. (all/failed/none)
  enable_assertion_pass_hook (bool):
                        Enables the pytest_assertion_pass hook. Make sure to delete any 
                        previously generated pyc cache files.
  junit_suite_name (string):
                        Test suite name for JUnit report
  junit_logging (string):
                        Write captured log messages to JUnit report: one of 
                        no|log|system-out|system-err|out-err|all
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
                        Dump the traceback of all threads if a test takes more than 
                        TIMEOUT seconds to finish
  addopts (args):       Extra command line options
  minversion (string):  Minimally required pytest version
  required_plugins (args):
                        Plugins that must be present for pytest to run

Environment variables:
  PYTEST_ADDOPTS           Extra command line options
  PYTEST_PLUGINS           Comma-separated plugins to load during startup
  PYTEST_DISABLE_PLUGIN_AUTOLOAD Set to disable plugin auto-loading
  PYTEST_DEBUG             Set to enable debug tracing of pytest's internals


to see available markers type: pytest --markers
to see available fixtures type: pytest --fixtures
(shown according to specified file_or_dir or current dir if not specified; fixtures with leading '_' are only shown with the '-v' option
root@Gavin:~#
```

请不要被上面这么多的使用参数吓到，实际常用十之有二。接下来我们将逐一分析每个参数的详细使用方法。



## 3.1.2 分类汇总

在Shell执行`pytest -h`可以看到`pytest`的命令行参数有这9大类（默认状态、未安装其他插件情况下），共130个，汇总如下表所示：

| 序号 | 类别                                     | 中文名                               | 包含命令行参数数量 |
| :--- | :--------------------------------------- | :----------------------------------- | :----------------- |
| 1    | positional arguments                     | 形参                                 | 1                  |
| 2    | general                                  | 通用                                 | 20                 |
| 3    | reporting                                | 报告                                 | 19                 |
| 4    | pytest-warnings                          | pytest警告                           | 8                  |
| 5    | collection                               | 收集                                 | 15                 |
| 6    | test session debugging and configuration | 测试session调试和配置                | 11                 |
| 7    | logging                                  | 日志                                 | 12                 |
| 8    | ini-options                              | pytest.ini/tox.ini/setup.cfg配置文件 | 40                 |
| 9    | environment variables                    | 环境变量                             | 4                  |

# 3.2 pytest help信息介绍

## 3.2.1 positional arguments

### 3.2.1.1 参数 [**file_or_dir**]

用途： 指定一个或多个文件/目录

使用方法：

```shell
pytest [file_or_dir] [file_or_dir] [...]
```



## 3.2.2 general 相关参数

### 3.2.2.1 参数 `-k`

`-k` 允许你运行名称符合某种表达式的测试用例。当使用 `-k` 参数时，你可以指定一个字符串表达式，`pytest` 将遍历项目中的每个测试用例名称，只有那些匹配表达式的测试用例才会被执行。

**使用方法：**

- **特定名称**


如果你只想运行测试名称中包含 "login" 的测试用例，可以执行：

  ```shell
pytest -k "login"
  ```

- **使用逻辑运算符**

`-k` 参数支持逻辑运算符 `AND`、`OR` 和 `NOT`（在 `-k` 参数中分别使用 `and`、`or`、`not` 关键词表示），比如：

若要运行包含 "login" 或 "logout" 的测试用例，可以执行：

  ```shell
pytest -k "login or logout"
  ```

如果想要执行既包含 "login" 又包含 "account" 的测试用例，可以执行：

  ```shell
pytest -k "login and account"
  ```

若要排除所有包含 "skip" 的测试用例，可以执行：

  ```shell
pytest -k "not skip"
  ```

- **结合其他参数**

`-k` 参数可以与其他 `pytest` 命令行选项结合使用，例如 `--ignore` 或 `-v`（用于增加详细程度）。



**请注意：**

- 表达式中的关键词大小写不敏感，且支持中文。

- 确保 `-k` 参数后面的表达式用双引号或单引号括起来以避免由于 shell 的特殊字符处理而导致的问题。

- 使用逻辑运算符时（`and`、`or`、`not`），需要按照 Python 逻辑语法规则进行组合。

`-k` 是一个非常有用的参数，可以快速选择子集的测试进行运行，非常适合在开发过程中对特定功能的测试或者当有大量的测试用例，但只有少数需要频繁运行时使用。



### 3.2.2.2 参数 `-m`

`pytest` 提供的 `-m` 参数允许用户基于标记（mark）来选择运行特定的测试用例。通过使用标记，可以非常灵活地组织测试用例，并据此选择运行特定的一组测试。

使用标记的一个常见场景是对测试用例按照功能、模块或者是测试类型（如冒烟测试、回归测试、测试用例分级别等）进行分组。

**使用方法：**

以下是如何使用 `-m` 参数的几个示例：

* **基本使用**

如果你有一个标记为 `migration` 的测试用例，你可以使用 `-m` 参数来只运行所有带有 `migration` 标记的测试用例。

```shell
pytest -m migration
```

这条命令会执行所有使用了 `@pytest.mark.migration` 装饰器的测试用例。

* **逻辑运算**

与 `-k` 参数类似，`-m` 参数也支持简单的逻辑运算符，如 `and`、`or` 和 `not`。

- 运行标记为 `migration` 或者 `loopdevice` 的测试：

```shell
pytest -m "migration or loopdevice"
```

- 运行同时标记为 `migration` 和 `NAS` 的测试：

```shell
pytest -m "migration and NAS"
```

- 运行未标记为 `migration` 的所有测试：

```shell
pytest -m "not migration"
```

* **结合其他参数**

`-k` 和 `-m`：`-m` 参数可以与 `-k` 参数或其它 `pytest` 参数结合使用，以实现更复杂的测试用例选择。

```shell
pytest -m "not migration" -k "iSCSI"
```

上面的命令将执行所有未被标记为"migration"且名称中包含 "iSCSI" 的测试用例。

* **自定义标记**

可以在 `pytest.ini`、`pyproject.toml`、`tox.ini` 或者 `setup.cfg` 文件中定义自己的标记策略，以避免使用未定义的标记引起的警告。例如，在 `pytest.ini` 中定义 `migraion` 和 `NAS`：

```ini
[pytest]
markers =
    migration: mark cases for migration features (deselect with '-m "not migration"')
    NAS: mark cases for all NAS features (deselect with '-m "not NAS"')
```

这段配置告诉 `pytest` 这些标记是已预定义的，并防止在使用未声明的标记时发出警告。



**请注意：**

`-m` 是一个功能强大的参数，配合标记功能，可以帮助我们灵活地组织和执行测试用例，非常适合管理复杂或大型测试集。

在持续集成/持续部署（CI/CD）环境中，`-m` 参数经常用于指定运行某类测试，例如只运行与当前开发工作相关的测试。



### 3.2.2.3 参数 `--markers`

`pytest` 提供的`--markers` 是一个命令行选项，它提供了显示项目中可用标记（markers）列表的便捷方式。在 `pytest` 中，标记用于分类和选择测试，通常用于为测试用例添加额外的元数据，诸如区分慢速运行的测试、需要特殊硬件的测试或者指定测试与某个特定功能相关等，这些标记可以后续用来选择性地运行特定的测试用例集合。

当你运行 `pytest --markers` 命令时，将会列出所有已注册的标记及其相应的说明（如果有的话），包含内置标记和自定义标记。这些信息通常来源于以下几个地方：

**内置标记：**

`pytest` 具有一些预设（内置）的标记，参考如下：

- `mark.name`: 这里的 `name` 是标记的名称，你可以将这个标记应用到一个测试函数上，然后通过 `-m 'name'` 选项来运行所有带有这个标记的测试。

- `skip`: 这个内置的标记用于不运行那些标记了 `@pytest.mark.skip` 的测试函数。

- `skipif`: 这个标记用作条件跳过，即在满足指定条件时，跳过使用了 `@pytest.mark.skipif` 的测试函数。

- `xfail`: 表示“预期失败”的测试，即这些测试可能由于某种已知的原因无法通过，使用 `@pytest.mark.xfail` 标记。

- `parametrize`: 这个标记允许用户为测试函数提供多组参数，使得同一测试函数可以用不同的数据多次运行。

- `usefixtures`: 通过这个标记可以声明测试用例需要使用的 fixture，即在测试运行前后执行的准备和清理/销毁函数。

- `filterwarnings`: 这个标记用于过滤掉在测试运行期间触发的特定警告。

**自定义标记：**

用户可以在测试文件中通过使用装饰器 `@pytest.mark.<marker_name>` 自定义标记，并且经常在配置文件中对这些标记进行描述。

**配置文件中声明的标记：**

为了避免在使用未声明的标记时遭受警告，用户在 `pytest.ini`、`pyproject.toml`、`tox.ini` 或 `setup.cfg` 等配置文件中声明标记及其说明。

例如，在 `pytest.ini` 文件中定义了两个标记 `slow` 和 `fast`，如下所示：

```ini
[pytest]
markers =
    slow: mark tests as slow (deselect with '-m "not slow"').
    fast: mark tests that run quickly (deselect with '-m "not fast"').
```

那么运行 `pytest --markers` 将列出所有可用的内置标记以及你定义的 `slow` 和 `fast` 标记。

输出结果会类似这样：

```shell
@pytest.mark.slow: mark tests as slow (deselect with '-m "not slow"').
@pytest.mark.fast: mark tests that run quickly (deselect with '-m "not fast"').
@pytest.mark.skip(reason=None): skip the given test function with an optional reason. Explanations may be presented with '-rs' or '-rA'.
...
```

此列表对于维护测试集合、确保标记使用的一致性以及为新成员快速提供项目内标记概览非常有用。它可作为一个参考手册，帮助团队成员理解每个标记的使用意图和上下文。



**请注意：**

使用标记的好处是：增加了测试的灵活性和表达力。

用户可以标记慢速的测试、特定组件的测试、需要特定资源的测试、根据功能特性分类的自定义标记等，然后根据需要选择性地运行或跳过它们，这对于管理大型测试套件特别有用。



### 3.2.2.4 参数 `-x` 或者 `--exitfirst`

`pytest` 的 `-x` 或 `--exitfirst` 参数是用来选择在第一个错误或失败（failure）出现时立即退出测试运行的。这个选项对于那些需要迅速识别出导致测试失败的问题的情况十分有用，它可以帮助开发人员节省时间，因为他们不必等整个测试套件运行完毕就能开始排查问题。

`pytest` 默认行为是运行所有的测试用例，不论它们成功还是失败，并在最后提供一个汇总报告。如果测试套件非常庞大，第一个错误可能在较早的阶段就发生了，但默认情况下你还是得等到所有测试用例运行完成后才会知道。使用 `-x` 选项，你可以在测试出现第一个失败时立刻得到反馈，这允许你更快地开始解决问题。

比如说，如果你有一个包含1000个测试用例的测试套件，并且第5个测试用例失败了，`pytest -x` 会在第5个测试用例失败后立即停止运行，而不是继续执行剩下的995个测试，这样你就可以专注于修复这个第5个测试用例的问题。

**使用方法：**

在命令行中可以这样使用 `-x` 选项：

```shell
pytest -x
```

或使用长形式：

```shell
pytest --exitfirst
```



**请注意：**

在某些情况下，比如在持续集成（CI）环境中运行测试时，你可能不想要这种行为，因为你会希望从单次构建中获得尽可能多的反馈信息。所以 `-x` 参数最适合在开发过程中使用，当你试图找到并修复测试失败的问题时。



### 3.2.2.5 参数 `--fixtures`

`pytest` 的 `--fixtures` 选项用于显示测试中可用的所有fixture的详细信息。在 `pytest` 中，fixtures 是一种功能，它们提供了一种固定的基础设施，可以被不同的测试用例所使用。这些fixture可能负责设置数据库、准备测试数据、启动某些服务、创建临时文件、清理某些设置等等。`--fixtures` 选项会列出所有的fixture及其文档字符串，这有助于开发者了解每个fixture的用途和功能。

而 `--funcargs` 选项在新版本的 `pytest` 中已经弃用了，因此它不会被 认可和使用（recognized and used）。过去，`--funcargs` 是用来展示可用的fixtures，与 `--fixtures` 类似。如果你尝试使用一个旧版本的 `pytest` 版本，`--funcargs` 选项可能仍然存在，但是在当前的 `pytest` 版本中，应该使用 `--fixtures` 来获得相同的结果。

**使用方法：**

 `--fixtures` 选项的示例如下：

```shell
pytest --fixtures
```

这个命令会打印出所有已定义的fixtures，包括它们的名称、所在的测试文件以及配套的文档说明。这对于了解项目中已有的测试资源和如何使用它们来说非常有帮助。

假设你在测试代码中有如下的fixture定义：

```python
# content of conftest.py
import pytest

@pytest.fixture
def smtp_connection():
    """Returns a smtp connection instance"""
    import smtplib
    return smtplib.SMTP("smtp.163.com", 587, timeout=5)

@pytest.fixture
def make_customer_record():
    """Create a test customer record"""
    def _make_customer_record(name):
        return {"name": name, "orders": []}
    return _make_customer_record
```

运行 `pytest --fixtures` 命令后，输出结果会包含类似以下内容的记录：

```python
----------------------- fixtures defined from conftest -------------------------
make_customer_record -- conftest.py:11
    Create a test customer record

smtp_connection -- conftest.py:6
    Returns a smtp connection instance

```

每一个fixture都会携带其注册在 `pytest` 中的名称和提供的文档字符串。

**请注意：**

- 下划线(_)开头的fixtures，需要使用参数 '-v' 来显示。
- 从`pytest` 的 `2.3` 版本起，`--funcargs` 参数已被废弃，其功能已由 `--fixtures` 接替。
- 使用 `--fixtures` 可以帮助你查看所有可用的fixtures及其说明，包括内置的、conftest.py中使用的和其他自定义的fixtures。



### 3.2.2.6 参数 `--fixtures-per-test`

查看每个测试用例实际使用了哪些 fixtures，或是想要查找特定测试用例相关的所有fixtures，你可以简单地在命令行中指定具体的测试用例，配合 `--fixtures-per-test`  选项，来查看测试用例使用了哪些fixtures。除此之外，借助`--setup-show` 选项，来查看每个测试用例的 setup 阶段中使用了哪些 fixtures。关于`--setup-show` 选项，请参考本章节中的“test session debugging and configuration 相关参数”处。

**使用方法：**

```shell
pytest --fixtures-per-test test_show_fixtures.py
```

**示例：**

```python
root@Gavin:~/code/chapter1-3# cat test_show_fixtures.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
This is an example pytest fixture
"""

import pytest


@pytest.fixture()
def run_function():
    """  This is a function doc info  """
    print("Run before function...")
    yield
    print("Run after function...")


def test_case_1(run_function):
    """  Test case 1  """
    print("case 1")


def test_case_2():
    """  Test case 2  """
    print("case 2")


def test_case_3(run_function):
    """  Test case 3  """
    print("case 3")
root@Gavin:~/code/chapter1-3#
```

测试结果：

```python
root@Gavin:~/code/chapter1-3# pytest --fixtures-per-test test_show_fixtures.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3
collected 3 items                                                                         

---------------------------- fixtures used by test_case_1 ----------------------
---------------------------- (test_show_fixtures.py:20) ------------------------
run_function -- test_show_fixtures.py:12
    This is a function doc info  

---------------------------- fixtures used by test_case_3 ----------------------
---------------------------- (test_show_fixtures.py:30) ------------------------
run_function -- test_show_fixtures.py:12
    This is a function doc info  

============================= no tests ran in 0.00s ============================
root@Gavin:~/code/chapter1-3# 
```



### 3.2.2.7 参数 `--pdb`

`pytest` 的 `--pdb` 选项是一个非常实用的调试助手。当使用这个选项运行测试时，如果发生了一个异常（例如测试失败了），`pytest` 将自动进入Python的调试器 `pdb`（Python Debugger）。它允许你在代码中的任何位置进行断点调试，并允许你检查堆栈、变量和执行任意的Python代码。

**使用方法：**

```shell
pytest --pdb test_file.py
```

当你运行以上命令时，如果 `test_file.py` 中的测试发生错误，`pytest` 就会在第一个发生错误的地方立即进入 `pdb` 调试模式。在进入 `pdb` 后，你可以：

- 使用 `list` 或 `l` 命令查看当前的代码。
- 使用 `next` 或 `n` 步过 (step over) 下一行代码。
- 使用 `step` 或 `s` 步入 (step into) 函数或方法。
- 使用 `continue` 或 `c` 继续执行程序直到碰到下一个断点。
- 使用 `quit` 或 `q` 退出调试器。
- 使用 `p` 打印一个表达式的值。

这是一个强大的功能，因为它允许你在测试失败时直接从错误点开始调试，而不需要去手动设置断点。这经常被用于复杂的失败，或是那些仅在特定测试环境下发生的问题。

也可以在命令行中组合 `--pdb` 与其它 `pytest` 选项一起使用，例如 `--maxfail` 可以在一定数量的失败之后停止测试:

```shell
pytest --pdb --maxfail=2 test_file.py
```

此命令告诉 `pytest` 在两个测试失败后停止执行，并且如果有测试失败，则在第一个失败的测试处打开 `pdb`。

**请注意：**

使用 `pytest --pdb` 可以帮助快速定位测试中的问题，特别是在复杂的测试或难以复现的问题时，它是一个极其有用的工具。不过，要记住，如果在自动化测试系统中运行测试，避免使用 `--pdb`, 因为它需要交互式输入，可能导致自动化流程暂停。

请记住，在 `pdb` 调试会话中，你需要了解一些基本的 `pdb` 命令来有效地进行调试。这个功能是Python标准库的一部分，因此无需额外安装即可与 `pytest` 一起使用。



### 3.2.2.8 参数 `--pdbcls`

`pytest` 的 `--pdbcls` 选项允许用户指定一个自定义的调试器类来代替标准的 `pdb` 调试器。它非常有用，尤其是当你需要使用不同的特性或者接口来进行调试时。

**使用方法：**

选项的格式是 `--pdbcls=modulename:classname`，其中：

- `modulename` 对应于包含你希望使用的调试器的 Python 模块的名字。
- `classname` 是模块中的调试器类的名称。

**示例：**

如果你想使用 `ipdb` 作为你的调试器，首先确保你已安装了 `ipdb` 模块：

```shell
pip install ipdb
```

然后，运行 `pytest` 时提供这个参数来使用 `ipdb` 的功能：

```shell
pytest --pdbcls=IPython.terminal.debugger:TerminalPdb
```

在这个例子中：

- `IPython.terminal.debugger` 是含有调试器类的模块名。
- `TerminalPdb` 是在 `IPython` 模块中对应的调试器类名。

使用这个选项时，测试运行时触发的任何异常都会进入由 `--pdbcls` 指定的调试器而不是标准的 `pdb`。这就允许你利用你选择的调试器的所有功能，比如 `ipdb` 提供的更丰富的交互性和更高级的调试工具。

不过，需要注意的是，并不是所有的 Python 调试器都与 `pytest` 兼容，因此在使用前应确保想用的调试器支持该集成。此外，由于 `pytest` 本身可能时不时更新，最好查看官方文档来获取最新的兼容性信息和使用指南。



### 3.2.2.9 参数 `--trace`

`pytest` 的 `--trace` 选项是一个用于启动调试的实用功能，它在测试执行期间提供了一种直接进入调试模式的方式。

使用 `--trace` 选项，当 `pytest` 开始执行一条测试项时，它会自动启动一个调试器。这允许你单步执行代码，检查当前的变量状态，评估表达式等等，就像在典型的调试会话中一样。这个选项在需要理解测试执行流或者排查一个特别复杂的测试失败原因时特别有用。

如下为如何使用 `--trace` 选项的基本示例：

```shell
pytest --trace tests/test_my_feature.py
```

在这个例子中，`pytest` 会执行 `tests/test_my_feature.py` 文件中所有的测试项，但对于每个测试项，它会在测试函数的开头打开调试器。

比较一下 `--pdb` 选项，也用于打开调试器，但仅在测试失败时。相反，无论测试是否失败，`--trace` 都会为每一个测试启动调试器。

这是一个非常给力的工具，但由于它会在每个测试项处停止，如果你有很多测试项，使用它可能不是很高效。通常，仅需针对单个测试或者很小的一组测试使用 `--trace` 选项，以便可以集中精力进行调试。

此外，`--trace` 选项会直接进入 `pdb` 调试器界面，因此对于不熟悉 `pdb` 命令的用户来说，可能需要一点时间去熟悉。

总体来说，`--trace` 选项在调试过程中提供了一种更立即的方法来控制测试的执行和分析。它对于快速定位问题和交互式地探究测试行为非常有帮助。

示例如下：

```python
root@Gavin:~/code/chapter1-3# pytest --trace test_show_fixtures.py 
============================= test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3
collected 3 items

test_show_fixtures.py 
>>>>>>>>>>>>>>>>>>>>>> PDB runcall (IO-capturing turned off) >>>>>>>>>>>>>>
> /root/code/chapter1-3/test_show_fixtures.py(21)test_case_1()
-> print("case 1")
(Pdb) l
 16  	    print("Run after function...")
 17  	
 18  	
 19  	def test_case_1(run_function):
 20  	    """  Test case 1  """
 21  ->	    print("case 1")
 22  	
 23  	
 24  	def test_case_2():
 25  	    """  Test case 2  """
 26  	    print("case 2")
(Pdb) 
```



### 3.2.2.10 参数 `--capture`

在 `pytest` 中，`-s` 或 `--capture=no` 选项用于禁用所有的标准输出 (`stdout`) 和标准错误 (`stderr`) 捕获。通常，`pytest` 会捕获测试运行时产生的所有输出，并且仅当测试失败时才显示它，有助于在出现问题时保持输出的清晰和集中。然而，在某些情况下，你可能希望在测试执行时直接看到输出，而不是等待测试失败。

举个例子，运行以下命令:

```shell
pytest -s test_my_feature.py
```

使用 `-s` 选项，`pytest` 将会运行 `test_my_feature.py` 文件中的测试，并将测试执行过程中的任何输出实时显示。这意味着打印到 `stdout` 或 `stderr` 的任何内容都会立刻显示在控制台上，而不是在测试结束后。

而 `-capture=method` 选项则允许更细粒度的控制。这里的 `method` 可以是以下选项之一：

* `no`: 不捕获输出，这与 `-s` 选项相同。
* `fd`: 使用文件描述符捕获机制。这种方法可以捕获包括系统调用在内的输出，比如打印到 `sys.stdout` 和 `sys.stderr` 的内容。
* `sys`: 只捕获写入 `sys.stdout` 和 `sys.stderr` Python 文件对象的输出。如果代码直接写入到操作系统提供的文件描述符，这些输出将不会被捕获。


例如，使用文件描述符捕获可以通过以下命令实现：

```shell
pytest --capture=fd test_my_feature.py
```

与 `-s` 选项不同，`--capture=fd` 将允许 `pytest` 捕获和控制输出，除非你明确要求显示它们。在实践中，根据具体的测试需求和调试偏好，你可能需要选择是否捕获输出以及如何捕获输出。通常情况下，你可能想要看到更多的输出来理解测试的行为，例如在引入新测试或调试现有测试失败时。



### 3.2.2.11 参数 `-s`

`pytest`中的`-s`参数是禁用捕获输出的简写选项，它的全称是`--capture=no`。在使用`pytest`时，通常测试在运行过程中产生的输出会被捕获，这样可以让测试的结果输出更加清晰，因为只有在测试出现错误或失败时，捕获的输出才会显示出来。当你没有使用`-s`选项时，所有打印到`stdout`（标准输出）或`stderr`（标准错误）的内容在测试过程中是看不到的，它们被`pytest`内部捕获存储起来了。

当使用了`-s`选项后，测试运行中的输出不再被`pytest`捕获，而是直接打印出来。例如：

```shell
pytest -s chapter1-3/
```

这条命令将运行`chapter1-3`目录下的所有测试，所有输出均会实时地显示在控制台上。这包括`print`语句、日志消息以及其他脚本可能输出的任何内容。这非常有助于调试测试脚本，特别是当你需要实时地获取反馈信息时。

假设我们有以下的测试用例：

```python
# test_example.py
def test_example():
    print("Hello, this is a pytest test case!")
    assert 1 == 1
```

运行`pytest -s`后，你将会看到"Hello, this is a pytest test case!"的输出。如果没有`-s`选项，这段输出信息将不会被显示。

需要注意的是，虽然`-s`选项有助于调试，但是如果测试用例本身或被测试的代码需要读取`stdin`的话，那么使用`-s`选项可能会产生问题，因为`pytest`默认会屏蔽掉对`stdin`的访问，以防止测试在等待输入时挂起。



### 3.2.2.12 参数 --runxfail

`pytest` 提供了一种处理预期失败（expected failures）的功能，通过使用 `@pytest.mark.xfail` 装饰器或使用内联的`pytest.mark.skipif`装饰器来标记那些由于某些已知问题而预期会失败的测试。这样做可以让这些测试在执行时不影响整个测试套件的结果。

在某些情况下，虽然我们将测试标记为预期失败，但我们可能想要强制执行这些标记为 `xfail` 的测试，来检查它们是否依然失败，或者是否提早解决了这个问题。这就是 `--runxfail` 参数的用途。当你在运行 `pytest` 时添加了 `--runxfail` 参数，它会执行所有标记为 `xfail` 的测试，就好像它们没有标记 `xfail`。

使用方法如下：

```shell
pytest --runxfail
```

使用 `--runxfail` 的效果包括：

**运行所有标记为 `xfail` 的测试：**

`--runxfail` 使所有使用 `@pytest.mark.xfail` 标记的测试都会执行，不考虑它们的 `xfail` 状态。

**忽略 `xfail` 状态：**

对于测试执行的结果，`--runxfail` 参数会导致 `pytest` 忽略 `xfail` 状态。即使测试预期失败，它们也会被记录为正常的失败或成功。

换言之，`pytest`会像平常一样运行这些测试，但不会特别关注预期失败的标记。如果测试失败了，它会被报告为一个普通的失败；如果测试通过了，它就会被报告为通过，不会有任何`xfail`或`xpass`的结果。

例如，你有以下的测试代码：

```python
# test_example.py
import pytest

@pytest.mark.xfail(reason="This feature is not yet implemented.")
def test_future_feature():
    assert 0

def test_normal_feature():
    assert 1
```

在默认情况下运行`pytest`时，`test_future_feature`会被标记为`xfail`。但是，当你使用`--runxfail`选项运行测试时：

```shell
pytest --runxfail test_example.py
```

此时，`test_future_feature`会被视为普通测试用例执行，如果它失败了，它会被报告为失败，不会考虑`xfail`。

**对bug修复测试：**

这个参数很有用，比如你修复了一个导致多个测试预期失败的bug，现在想要验证这些修复是否有效。而不是移除或者编辑每个 `xfail` 标记，你可以简单的使用 `--runxfail` 来执行这些测试。

**输出结果：**

即使测试是预期失败的，使用 `--runxfail` 后，失败结果会以正常的失败（FAIL）报告，而成功则为正常的成功（PASS）。这意味着 `xfail` 状态不会影响到测试结果的解释。

这个选项在持续集成或者测试环境中也非常有用，你可能想要临时极端地理解哪些 `xfail` 测试在当前环境中实际上是通过的，或者在排查问题的过程中需要确认这些测试的当前状态。不过，在常规的测试运行中，我们通常不加 `--runxfail`，让 `xfail` 的测试保持它们的预期状态。



### 3.2.2.13 参数 `--lf, --last-failed`

`pytest` 提供了一种非常有用的功能来帮助开发者专注于最近失败的测试。通过 `--lf` 或 `--last-failed` 选项，`pytest` 只重新运行最近一次测试运行中失败的那些测试用例。这个选项能够节省时间，特别是处在解决 bug 和测试修复的循环中时，因为你不需要重新运行整个测试套件，只需关注那些失败的测试。

具体使用方法是在命令行中添加该选项：

```shell
pytest --last-failed
```

或者是使用缩写形式：

```shell
pytest --lf
```



**`--lf` 或 `--last-failed` 的行为：**

**执行过滤：**

在你下次执行 `pytest` 时，只有上一次运行中失败的测试会被运行。如果在上一次运行中没有任何测试失败，那么使用 `--last-failed` 将不会运行任何测试。

**节省时间：**

这种方式特别有用，因为它可以帮助你专注于修复那些断言失败或出错的测试，而不必等待那些已经通过的测试再次运行。

**配合其他策略：**

你可以将 `--last-failed` 与其他 `pytest` 选项结合使用，例如 `-vv` 提高输出的详细程度，或者 `--pdb` 在失败的测试上直接进入调试器。

**持久化：**

`pytest` 会在 `.pytest_cache` 目录中存储关于上一次运行哪些测试失败的信息，这样即使你在不同的测试运行之间关闭了你的工作站，`--last-failed` 也能继续工作。

**清除失败记录：**

如果想从头运行所有的测试，或者清理掉失败的记录，你可以运行 `pytest` 而不加任何参数，或者使用 `--clear-last-failed` 来清除失败的缓存记录。

这个功能在测试开发过程中特别高效，能够显著提高开发者处理失败测试的速度。不过，当你确信所有的问题都已经修复完毕，最好进行一次全面测试，以确保没有其他非预期的问题出现。



### 3.2.2.14 参数 `--ff, --failed-first`

`pytest` 的 `--ff` 和 `--failed-first` 选项是用来优化测试运行的。这些选项被设计用于让在上一次运行中失败的测试用例首先执行，这样可以让开发者更快地看到修复这些失败用例是否有效。如果这些之前失败的测试现在都通过了，那么 `pytest` 将继续执行其余的测试用例。

使用这种方式，测试反馈循环更短，特别是在一个有许多测试用例的大型项目中，你可以更快地知道你的更改是否解决了问题而不必等待整个测试套件完成运行。

具体用法如下:

```shell
pytest --failed-first
```

或者使用简写形式:

```shell
pytest --ff
```

在命令执行时，`pytest` 会首先运行上次失败的测试集，如果这些测试通过，则继续执行剩余的测试集。

例如，假设你有一组测试用例，其中某几个在上次运行时失败了，如果你修改了相关代码以解决这些失败的测试，并想要确认这些修改的效果，可以使用 `--ff` 选项运行 `pytest`。这样做不仅可以快速获得关于这些特定测试的反馈，而且一旦这些测试都通过了，剩余的测试也会在之后执行，以确保其他部分的代码仍然是正确的。

就像 `--lf`（`--last-failed`）选项一样，`--ff` 选项依赖于 `.pytest_cache` 目录中存储的信息，它记录了哪些测试在上次运行中失败。如果你想要从头开始运行所有测试用例或者清除失败的历史，可以使用 `--cache-clear` 选项来清空缓存。



### 3.2.2.15 参数  `--nf, --new-first`

`pytest` 的 `--nf` 或 `--new-first` 选项是用于调整测试用例的执行顺序，以便最先运行最新的测试。这个功能特别适用于开发新功能或修复缺陷时，当你添加或修改了测试用例，并希望首先执行这些最新的测试来快速获得反馈。

当使用 `--nf` 或 `--new-first` 选项时，`pytest` 会尝试根据测试用例文件的修改时间来确定测试执行的顺序。较新或最近修改的测试文件中的测试用例会被提前到测试队列的前面。

具体用法如下:

```shell
pytest --new-first
```

或者使用简写形式:

```shell
pytest --nf
```

这与 `--ff`（`--failed-first`）选项不同，后者是将之前失败的测试用例置于队列前面。`--new-first` 选项则关注文件的新旧程度。

例如，假设你在开发一个特性并且添加了一些新的测试用例，或者对现有的一个测试文件进行了显著的修改。使用 `--new-first` 选项可以让你更快地看到这些更改是否成功，因为 `pytest` 将先运行这些新添加或修改的测试用例。

这是一种有助于提高开发效率的测试策略，尤其是当你正在频繁地添加新测试和更改现有测试时。这样可以先关注新的更改，确保它们按预期工作，然后再关注全局的测试情况。

记住，如果希望运行所有测试用例，而不对顺序做特殊处理，你应该运行裸 `pytest` 命令，而不带任何排序相关的选项。



### 3.2.2.16 参数  `--cache-show=[CACHESHOW]`

`pytest` 的 `--cache-show` 选项用于显示缓存内容（默认是`.pytest_cache`目录），可以查看之前测试运行时所保存的信息，这对调试和理解 `pytest` 缓存机制非常有帮助。`pytest` 缓存用于存储跟测试运行相关的数据。例如，`--lf` （--last-failed）和 `--ff`（--failed-first）选项依赖于 `.pytest_cache` 目录中的失败记录来确定失败的测试。



`pytest`的缓存目录结构示例如下：

```shell
root@Gavin:~/code# tree -a .pytest_cache/
.pytest_cache/
├── CACHEDIR.TAG
├── .gitignore
├── README.md
└── v
    └── cache
        ├── lastfailed
        ├── nodeids
        └── stepwise

3 directories, 6 files
root@Gavin:~/code# 
```

说明如下：

* `.pytest_cache/CACHEDIR.TAG`：pytest创建的缓存目录标签。
* `.pytest_cache/.gitignore`：pytest测试框架 `.pytest_cache`的自带的 `.gitignore`文件。
* `.pytest_cache/README.md`： `.pytest_cache`文件夹介绍。
* `.pytest_cache/v/cache/lastfailed`: 上一次运行失败的测试用例。
* `.pytest_cache/v/cache/nodeids`: 上一次运行的所有测试用例（无论测试用例的执行结果通过还是失败）。
* `.pytest_cache/v/cache/stepwise`：测试用例的路径。

如果指定 `--cache-show` 而不带任何参数，它将显示所有缓存的信息。你也可以提供具体的键值来查看特定的缓存信息。

具体用法如下:

```shell
pytest --cache-show
```

这将会打印 `.pytest_cache` 目录中的所有内容，参考如下：

```shell
root@Gavin:~/code# pytest --cache-show
============================== test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
cachedir: /root/code/.pytest_cache
------------------------------ cache values for '*' ----------------------------
cache/lastfailed contains:
  {'chapter1-3/test_example.py::test_assert_failed': True}
cache/nodeids contains:
  ['chapter1-3/test_example.py::test_assert_failed',
   'chapter1-3/test_example.py::test_example',
   'chapter1-3/test_example.py::test_future_feature',
   'chapter1-3/test_example.py::test_normal_feature']
cache/stepwise contains:
  []

============================== no tests ran in 0.00s ===========================
root@Gavin:~/code#
```

如果你想针对特定缓存项获取详细信息，可以指定该项的名称：

```shell
pytest --cache-show=[CACHENAME]
```

在这里，`[CACHENAME]` 应该替换为你希望查看的具体缓存项的名称。

例如：

```shell
pytest --cache-show=chapter1-3/test_example.py
```

这个命令将会显示与 `chapter1-3/test_example.py` 相关的缓存信息，这个键值通常包含了上次运行中失败的测试。

缓存功能可以用来存储和检索测试间需要传递的数据。不过，请注意，过多依赖于测试间的缓存可能会导致测试结果不可靠，因为它们可以含有过时的数据，尤其是在代码改动频繁的情况下。

当你对 `pytest` 缓存机制有了深入理解，并且能够有效利用缓存数据时，`--cache-show` 就成为了一个非常有用的调试工具。



### 3.2.2.17 参数  `--cache-clear`

`pytest` 的 `--cache-clear` 选项用于清除通过 `pytest` 缓存机制存储在本地的所有缓存数据。`pytest` 的缓存系统允许跨多次测试运行间存储和复用数据，这些数据默认存储在 `.pytest_cache` 目录中。使用 `--cache-clear` 可以删除这个目录下的所有内容，从而清空缓存。

使用 `--cache-clear` 选项的场景包括但不限制于：

- 当你想要重新运行失败的测试而不受之前运行影响时。
- 当你要清除由于某些原因可能已经不再准确或有用的缓存数据时。
- 测试过程中某些缓存数据可能导致测试结果不一致，此时清除缓存能够确保每次运行测试都是在干净的状态下开始。

具体的命令如下所示：

```shell
pytest --cache-clear
```

执行这条命令，`pytest` 会先删除 `.pytest_cache` 目录及其内容，然后根据你可能的运行测试命令，开始新的测试运行。

需要注意的是，使用这个选项之后，所有的缓存都会被清除，包括用于 `--lf`（--last-failed）和 `--ff`（--failed-first）选项的失败记录。因此，使用它之前请确保你不需要缓存中的任何数据，或者已经做好了相应的数据备份工作。



### 3.2.2.18 参数  `--lfnf={all,none}, --last-failed-no-failures={all,none}`

`pytest` 的 `--lfnf` 或者全称 `--last-failed-no-failures` 选项用于指定当没有失败的测试时应该执行哪些测试。这个选项通常与 `--last-failed` 选项一起使用，后者会使 `pytest` 只重运行上次运行中失败的测试。

`--last-failed-no-failures` 有两个可能的值：

* `all`：如果在上次的测试中没有任何失败（或者使用了 `--cache-clear` 清空了缓存），则运行所有的测试用例。

* `none`：如果在上次的测试中没有任何失败，则不运行任何测试用例。

这个选项在持续集成流程中非常有用，让你可以先尝试只重运行那些失败的测试用例。如果在某次运行中所有的失败用例都被修复了，根据 `--lfnf` 的设置，你可以选择是运行全部测试保证整体健康，还是什么都不做。

**使用方法：**

如果上次没有失败的测试，运行所有测试：

```shell
pytest --last-failed --last-failed-no-failures=all
```

如果上次没有失败的测试，不运行任何测试：

```shell
pytest --last-failed --last-failed-no-failures=none
```

**请注意：**

这两个选项需要结合使用。如果你没有启用 `--last-failed`，则 `--last-failed-no-failures` 选项没有任何效果。当你期望根据失败用例的存在与否来决定运行策略时，这一选项组合尤其有帮助。



### 3.2.2.19 参数  `--sw, --stepwise`

`pytest` 的 `--stepwise` 选项（缩写为 `--sw`）是一个有用的调试工具，它允许测试在第一个失败的测试处停止。其功能类似于逐步执行（stepwise），可以帮助你快速定位问题。当你在大型测试集中调试单个失败的测试时，这个选项特别有帮助，因为它避免了在修复当前失败的测试之前需要运行所有其他测试的情况。

**使用方法：**

开启 stepwise 模式，当遇到第一个失败的测试时立即停止执行剩余的测试:

```shell
pytest --stepwise
```

**详细说明：**

- 当启用 `--stepwise` 选项时，`pytest` 会开始执行测试，一旦遇到第一个测试失败，它就会停止执行。
- 修复了导致测试失败的问题之后，你可以重新运行带有 `--stepwise` 选项的 `pytest`，它将继续从上一次失败的测试处开始执行，而不是从头开始。
- 如果在 `--stepwise` 模式下所有的测试都通过了，那么 `pytest` 将正常退出。
- 这个选项非常适合那些需要快速迭代和修复单个或一系列测试问题的开发者。
- 请注意，`--stepwise` 模式与 `pytest` 的缓存机制一起工作；它利用缓存来记住上次失败的位置。

可能需要注意的是，如果你的测试依赖于特定的顺序或者有涉及状态的依赖，那么 `--stepwise` 可能不是最好的选择，因为在测试序列中间的某个点开始执行可能会导致意外的副作用。在这种情况下，使用标准的 `--lf`（--last-failed）选项可能更加安全，`--lf` 会重新运行上次运行中失败的所有测试。



### 3.3.3.20 参数  `--sw-skip, --stepwise-skip`

`pytest` 的 `--stepwise-skip` 选项（可缩写为 `--sw-skip`）是结合了 `--stepwise` 功能和忽略跳过（skip）测试的能力。启用这个选项后，`pytest` 会在遇到第一个失败的测试时停止执行，就像 `--stepwise` 那样，但它还将自动跳过任何标记为跳过的测试。

**使用方法：**

在 stepwise 模式下跳过使用 `pytest.mark.skip` 或 `pytest.mark.skipif` 标记的测试：

```shell
pytest --stepwise --stepwise-skip
```

**详细说明：**

- 启用 `--stepwise-skip` 时，`pytest` 开始执行测试并跳过任何明确被标记为需要跳过的测试。
- 一旦遇到第一个测试失败，它就会停止执行后续的测试，就像在标准的 `--stepwise` 模式下那样。
- 当你修复了导致停止的测试失败后，可以再次运行 `pytest` 带上 `--stepwise` 和 `--stepwise-skip` 选项，它将从上次失败的测试处继续执行，并且继续跳过那些被标记为跳过的测试。
- 名为 `--sw-skip` 的缩写形式可以替代 `--stepwise-skip` 使用。
- 类似 `--stepwise`，这个选项在调试一个大型测试套件时非常有用，尤其是当你希望忽略已知将被跳过的测试，将焦点放在需要修复的失败测试上时。
- `--stepwise-skip` 选项创造了一个快速迭代的测试环境，特别是在调试过程中，它绕过了不需要关注的测试，让你可以集中精力在当前失败处一步步前进。
- 这个选项的使用前提是你的测试套件中包含了使用 `pytest.mark.skip` 或 `pytest.mark.skipif` 标记的测试。如果没有这样的跳过标记，它的行为就和标准的 `--stepwise` 选项一样。


[续下文](https://gavin-wang-note.github.io/2024/05/22/pytest_test_guide_part1_chapter1_3_2_pytest_params/)
