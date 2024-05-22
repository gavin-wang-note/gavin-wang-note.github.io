---
title: 《pytest测试指南》-- 章节1-1 初识pytest
date: 2024-01-21 22:06:17
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg: 
password: 
toc: false
mathjax: false
summary: 《pytest测试指南》一书 章节1-1 初识pytest。
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 1.1 常见几种测试框架对比

笔者在过往工作经历中使用过几种测试框架，涉及unittest，nose，pytest 和 robot framework：

* unittest: Python自带，最基础的单元测试框架；
* nose: 基于unittest开发，易用性好，有许多插件；
* pytest: 同样基于unittest开发，易用性好，信息更详细，插件众多；
* robot framework：一款基于Python语言的关键字驱动测试框架，有界面，功能完善，自带报告及log清晰美观。

简要对比信息参考如下：

| 项目                       | unittest                                                 | nose                                                         | pytest                                                       | robot framework                                              |
| -------------------------- | -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 用例编写                   | 继承unittest.TestCase类需要组织各种testSuite断言种类繁多 | test开头的方法即可                                           | test开头的方法即可                                           | robot格式，文本文件                                          |
| 执行器                     | 自己写run_all_tests+discover+CommandParser+...           | nosetests ...                                                | py.test ...                                                  | pybot ...                                                    |
| 用例发现Discover           | 支持                                                     | 支持                                                         | 支持                                                         | 支持                                                         |
| 跳过用例                   | unittest.skip()unittest.skipIf()raise uniitest.SkipTest  | from nose.plugins.skip import SkipTestraise SkipTest         | @pytest.mark.skipif( condition)@pytest.mark.xfail            | -                                                            |
| Fixtures                   | setUp/tearDown@classmethodsetUpClass...                  | 支持                                                         | @pytest.fixture(session="session", autouse=True)fixture的作用域：function、module、session ，autouse=True使得函数将默认执行 | [Setup] ...[Teardown] ...                                    |
| 用例标签tags               | 借助unittest.skip()+comandParser实现                     | attrib标签from nose.plugins.attrib import attr@attr(speed='slow')def test_big_download(): pass$ nosetests -a speed=slow | @pytest.mark.webtest自定义一个mark，如下，然后 py.test -v -m webtest 只运行标记了webtest的函数， py.test -v -m "not webtest" 来运行未标记webtest的 | [Tags] test level1pybot -i/--include tagName C:\TF-Testpybot -e/--exculde level1 *.robot排除 |
| 超时机制Timeout            | 自己实现                                                 | from nose.tools import timedimport time@timed(1)def test_lean_5():time.sleep(2)pass | pip install pytest-timeout<br />@pytest.mark.timeout(60)或 pytest --timeout=300 | [Timeout] 3 seconds                                          |
| 参数化                     | 结合ddt使用                                              | 结合ddt使用                                                  | @pytest.mark.parametrize("a,b,expected", testdata)def test_timedistance_v0(a, b, expected):diff = a - bassert diff == expected | [Template] 1 2 3                                             |
| 报告                       | HTMLTestRunner                                           | pip install nose-htmloutput<br />Usage: --with-html --html-file=<br />支持allure | pip install -U pytest-html<br />Usage: py.test --html=./report.html<br />支持allure | 支持，默认自动生成                                           |
| 日志log                    | 自己实现                                                 | --nologcapture 不使用log--logging-format=FORMAT使用自定义的格式显示日志--logging-datefmt=FORMAT 和上面类类似，多了日期格式--logging-filter=FILTER日志过滤，一般很少用，可以不关注--logging-clear-handlers 也可以不关注--logging-level=DEFAULT log的等级定义 | pytest test_add.py --resultlog=./log.txtpytest test_add.py --pastebin=all | 支持，默认自动生成                                           |
| 只列出用例collect-only     | 无                                                       | nosetests --collect-only/nosetests -v --with-id              | --collect-only -v                                            | 无                                                           |
| 失败用例重跑rerun failures | 无                                                       | nosetests -v --failed                                        | pip install -U pytest-rerunfailures@pytest.mark.flaky(reruns=5)py.test --rerun=3 | robot --rerunfailed                                          |
| baseline对比               | 无                                                       | 无                                                           | 无                                                           | 无                                                           |
| 并发                       | 改造unittest使用协程并发，或使用线程池+Beautiful Report  | 命令行并发                                                   | pytest-xdist：分发到不用的cpu或机器上                        | 命令行并发                                                   |
| xml报告                    | 无                                                       | --with-xunit                                                 | --xunit-file=... /pytest+Allure                              | --junit-xml=                                                 |
| Selenium支持               | 无                                                       | 无                                                           | pytest-selenium                                              | robotframework-seleniumlibraryrobotframwork-selenium2library |
| APP支持                    | 无                                                       | 无                                                           | pytest-appium                                                | robotframework-appiumlibrary                                 |



总体来说：

* unittest比较基础，二次开发方便，适合高手使用；
* pytest/nose更加方便快捷，效率更高，适合小白及追求效率的公司；
* robot framework由于有界面及美观的报告，易用性更好，灵活性及可定制性略差。



# 1.2 初识pytest

## 1.2.1 pytest是什么

`pytest` 是一种功能强大的测试框架，使用Python编程语言开发。它使得编写简单和可扩展的测试代码变得轻松。`pytest` 支持自动发现和运行测试，提供了丰富的参数、断言机制和插件支持。许多开发人员和公司都使用 `pytest` 作为编写和执行单元测试、集成测试以及功能、性测试的首选工具。

以下是 `pytest` 的一些关键特性：

**简单的测试编写：**

- 使用极简的`assert`语句，你可以不需要记住复杂的断言，直接对比期望和实际结果。
- 不需要编写类或方法，普通函数就可以是测试函数。

**自动测试发现：**

- `pytest` 可以自动发现以 `test_` 开头或`_test`结尾的文件和函数作为测试用例。

**详细的测试结果报告：**

- `pytest` 提供详细的错误报告，当测试失败时，会显示哪一行代码失败以及失败的详细信息。

**支持fixtures：**

- 通过使用`fixtures`，`pytest` 可以为测试提供创建/销毁和管理资源（如数据库连接、临时的文件等）。这种机制提供了可重用的功能以及设置和清除条件。

**参数化测试：**

- 使用 `pytest.mark.parametrize` 装饰器可以轻松地对单个测试实现多个参数组合的测试。

**插件系统：**

- `pytest` 有一个广泛的插件生态系统，你可以使用其他开发者写的插件或自己编写插件来扩展其功能。

**可集成性：**

- `pytest` 可与许多其他测试和开发工具集成，如测试覆盖率工具 `coverage.py`，持续集成服务等。



## 1.2.2 pytest框架结构

`pytest` 的框架结构包含若干核心组件以及配合这些组件使用的各种插件。下面详细介绍其主要组成部分：

###  1.2.2.1 测试发现与执行

**发现机制**：
`pytest` 会自动发现测试文件和测试函数。默认情况下，`pytest` 认为所有匹配 `test_*.py` 或 `*_test.py` 的文件是测试文件，并且这些文件中以 `test_` 开头的函数是测试函数。

**执行机制**：
当你运行 `pytest` 命令时，它会调用内部的测试发现机制，寻找所有可用的测试案例，并按照一定顺序执行它们。如果有测试失败，`pytest` 会提供详细的断言失败报告。

###  1.2.2.2 插件系统

`pytest` 具有丰富的插件架构，允许通过安装第三方插件或创建自定义插件来扩展其功能。有许多官方和社区提供的插件，如：

- `pytest-django`：用于Django项目的专有测试工具。
- `pytest-asyncio`：为asyncio代码提供测试支持。
- `pytest-xdist`：支持分布式测试和并行测试执行。
- `pytest-cov`：集成覆盖率报告。
- `pytest-allure`：结合allure生成漂亮的可视化html测试报告。

插件可以通过钩子（hook）函数来扩展 `pytest` 的行为。这些钩子会在测试运行的各个阶段被调用。

###  1.2.2.3 配置文件

`pytest` 允许使用配置文件来定制测试行为。最常见的配置文件是 `pyproject.toml`、`pytest.ini`、`setup.cfg` 和 `tox.ini`。在这些文件中，可以设置不同的选项和插件参数。

###  1.2.2.4 fixture

`pytest` 使用 `fixture` 来设置测试前的环境和上下文。`fixture` 通过特殊的装饰器 `@pytest.fixture` 定义，并可以在测试函数中通过参数引用。

###  1.2.2.5 标记（Marking）

使用 `@pytest.mark` 装饰器，可以对测试进行分类标记，例如跳过某些测试 (`@pytest.mark.skip`), 或者为测试添加自定义标签以便于根据标签选择性运行测试。

###  1.2.2.6 测试收集器（Collector）

`pytest` 有一个测试收集器，其职责是搜集所有需要执行的测试案例。它会递归地搜索测试文件夹，并识别出测试用例。

###  1.2.2.7 测试会话（Session）

从测试收集到测试执行的全部过程，发生在一个 `pytest` 会话中。在这个会话中，可以访问到所有测试案例以及相关配置。

### 1.2.2.8 会话钩子（Session Hooks）

这些钩子在整个测试会话过程中被调用，能让插件在测试过程的关键点插入动作。例如：`pytest_sessionstart`, `pytest_sessionfinish`。

###  1.2.2.9 命令行工具（CLI）

`pytest` 提供了命令行工具与用户交互，通过它可以传递不同的参数和选项来控制测试执行的行为，例如指定测试的路径、选择性地运行标记的测试、设置并行测试数量等。

### 1.2.2.10 结果报告

`pytest` 提供了丰富的结果报告系统，包括控制台输出和（通过插件）XML、HTML等格式的报告。

### 1.2.2.11 记录/日志

`pytest` 支持通过 Python 的 logging 模块来记录测试信息，使得调试更加容易。

### 1.2.2.12 结构示例

```shell
pytest/
├── _src/
│   ├── config/          # 配置处理
│   ├── hooks/           # 钩子定义
│   ├── common/          # 公共类/函数的封装
│   ├── testcase/        # 测试用例，纯测试基类中函数的调用，完成业务流程的构造
│   ├── testcasebase/    # 测试用例对应的基类
│   ├── fixtures.py      # 处理fixtures的模块
│   ├── run.py          # 控制测试收集和执行的主运行入口
│   └── ...
├── pytest.ini           # pytest配置文件（如果存在）
└── conftest.py          # 局部插件和fixture定义（如果存在）
```

`pytest` 的框架结构做到了灵活和强大，支持自定义测试行为，并且提供了丰富的默认选项，使其非常适合各种规模和复杂度的Python项目。因其可扩展性、简洁性和易用性而广受欢迎，是Python社区中常用的测试工具之一。

## 1.2.3 pytest的优点和特点

pytest是python的⼀种免费和开源的测试框架，设计的目的是让测试尽可能简单，它的API易于使用，可以通过命令行或者IDE进行测试，全功能且非常成熟，使⽤起来更简洁，效率更⾼。它主要有以下一些特点：

* 支持多种测试类型：pytest能够支持不同类型的测试，包括单元测试、集成测试、功能测试、性能测试等，可以和Selenium，requests，Appium结合实现web自动化，接口自动化，APP自动化，并能很好的和Jenkins结合进行持续集成。
* 可扩展性：pytest具有很好的可扩展性，支持自定义 assertion、插件和测试套件运行。除此之外，pytest有很多非常强大的第三方插件，并且这些插件能够实现很多实用的操作。多年来，已经有大量的第三方插件扩展和增强它的功能，当然也可以自定义pytest插件。
* 灵活的执行策略：pytest支持灵活的用例执行策略，可以并行运行多个测试，从而减少了测试套件的执行时间；可以将某些测试跳过；对某些预期失败的用例标记成失败；支持重复执行失败的用例等等。
* 强大的配置与fixture：pytest支持参数化（数据驱动）；pytest强大的fixture在不改变被装饰函数的前提下对函数进行功能增强。
* 完美与Allure结合： pytest可以和Allure结合生成非常美观的可视化TTML测试报告。
* 兼容性好：pytest支持python 2.x 和 python 3.x，并且与python的标准库和其他常用的python包兼容。在pytest框架下可以执行Unittest框架和 nose框架的用例。
* 社区支持强大：pytest有一个活跃的社区，提供大量的文档、教程和插件，使得pytest的使用更加容易和高效。

## 1.2.4 pytest的官网及资料地址

pytest官网及帮助文档网址： https://docs.pytest.org/en/latest/。
pypi网址：https://pypi.org/project/pytest/。
GitHub网址： https://github.com/pytest-dev/pytest/。

# 1.3 关于nose 与 pytest

nose和pytest都是Python编程语言的测试框架，它们用于编写和运行测试。

**nose** 是一个相对较老的测试框架，它因简单易用而受欢迎。nose使用插件可以扩展其功能，并且很容易收集测试，只要遵循简单的命名规则即可。

**pytest** 是后来出现的测试框架，但它很快在许多Python开发者中变得流行。pytest提供了一个更丰富的断言模型、更好的支持fixtures的机制、丰富的插件生态系统以及更多的灵活性来定制测试行为。

至于为何nose项目不再活跃，原因包括：

* **开发停滞与技术进步**：随着pytest等新的、功能更全面的测试框架的出现，nose的开发逐渐减缓，最终停止。开发人员和社区成员往往更喜欢那些依旧积极发展和解决新问题的工具。
* **社区支持的转移**：Python社区对nose的支持逐渐转向对pytest的支持，因为pytest提供更先进的功能和改进的用户体验。
* **官方的决定**：nose的维护者们决定停止维护该项目，这可能是因为资源限制、个人兴趣变化或者pytest已经能够提供更好的替代方案。
* **nose2的出现**：应注意，nose的一些原始开发者开始工作在nose的后继项目nose2上，这是一个和nose类似的、但更加现代化的工具，它试图解决nose的一些局限性，并且提供一个更好的平台以支持新特性和测试模式。

总之，软件工具和库的可持续性往往会受到社区支持、维护者参与度、以及新技术的影响。面对pytest这样功能强大、更符合当下需求的框架，nose自然而然地被边缘化，并最终进入了维护模式。

# 1.4 部署pytest

## 1.4.1 环境说明

由于笔者个人习惯问题，直接在`Ubuntu23.10 Server`下借助vim进行测试用例的编写，准备环境如下：

```shell
root@Gavin:~# uname -a
Linux Gavin 6.5.0-13-generic #13-Ubuntu SMP PREEMPT_DYNAMIC Fri Nov  3 12:16:05 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
root@Gavin:~# python3 --version
Python 3.11.6
root@Gavin:~#
```

当然，可根据个人习惯，在windows下安装`python`和`pytest`，借助`python IDE`（如PyCharm）进行用例编写。

## 1.4.2 pytest安装

执行如下命令，安装pytest：

```shell
apt install python3-pytest -y
```

查看安装的版本信息：

```shell
root@Gavin:~# pytest --version
pytest 7.4.0
root@Gavin:~# 
```

或者

```shell
root@Gavin:~# pip show pytest
Name: pytest
Version: 7.4.0
Summary: pytest: simple powerful testing with Python
Home-page: https://docs.pytest.org/en/latest/
Author: Holger Krekel, Bruno Oliveira, Ronny Pfannschmidt, Floris Bruynooghe, Brianna Laugher, Florian Bruhin and others
Author-email: 
License: MIT
Location: /usr/lib/python3/dist-packages
Requires: iniconfig, packaging, pluggy
root@Gavin:~#
```

显示类似如上信息，表明安装`pytest`成功，版本为7.4.0。

# 1.5 pytest入门

## 1.5.1 基本用法

在`pytest`中，你的测试文件通常以`test_`开头，测试函数以`test_`开头。如下是一个基本的测试示例：

```python
# content of test_example.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add('space', 'ship') == 'spaceship'
```

要运行测试，你只需在命令行中执行`pytest`：

```bash
root@Gavin:~# pytest
```

`pytest`将自动发现所有符合命名约定的测试函数和文件，并执行它们。

## 1.5.2 参数化测试

`pytest`允许你通过一个名为`pytest.mark.parametrize`的装饰器来参数化测试：

```python
# content of test_parametrize.py
import pytest


def add(a, b):
    return a + b


@pytest.mark.parametrize("a,b,expected", [(2, 3, 5), (4, 5, 9), ('a', 'b', 'ab')])
def test_add_param(a, b, expected):
    assert add(a, b) == expected
```

通过以上方式，你可以确保`test_add_param`函数被上述三组参数调用三次。

## 1.5.3 测试预期的异常

有些时候，我们期望函数在特定情况下抛出异常， `pytest` 允许我们测试这种行为。

```python
# content of test_exception.py
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def test_divide_exception():
    with pytest.raises(ValueError):
        divide(1, 0)
```

`divide()` 函数在分母为零时抛出 `ValueError`。我们使用 `pytest.raises` 上下文管理器来测试这个行为。

## 1.5.4 使用 fixture 处理测试前后的准备和清理

`fixture` 允许你设置一个代码状态，该状态可以被一个或多个测试共享。可以用来初始化数据库、测试数据或其它资源。

```python
# content of test_fixtures.py
import pytest

@pytest.fixture
def resource_setup():
    # Setup for test (e.g. establish database connection)
    db_conn = setup_database()  
    yield db_conn
    # Teardown for test (e.g. close database connection)
    teardown_database(db_conn)

def setup_database():
    # Dummy function to illustrate setup
    return "database_connection"

def teardown_database(conn):
    # Dummy function to illustrate teardown
    print(f"Closing {conn}")

def test_db(resource_setup):
    assert resource_setup == "database_connection"
```

在这个场景中，`resource_setup` fixture 负责建立和销毁测试所需的资源（在这个例子中是数据库连接）。`test_db()` 函数把 fixture 作为参数使用，确保了执行测试时资源已正确设置。

注意，实际代码中 `setup_database()` 和 `teardown_database()` 函数会涉及真正的数据库操作，这里仅用字符串和打印语句举例。

## 1.5.5 跳过测试或有条件地跳过测试

在某些情况下，可能需要跳过某个测试，比如当一个外部资源不可用时。

```python
# content of test_skip.py
import sys
import pytest

def add(a, b):
    return a + b

@pytest.mark.skip(reason="This function is not yet implemented.")
def test_to_be_skipped():
    # This test will be skipped
    assert add(3, 4) == 7

@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_skip_if():
    # This test will be skipped on Python versions lower than 3.6
    assert add(3, 4) == 7
```

`@pytest.mark.skip` 装饰器表明测试应被跳过，而 `@pytest.mark.skipif` 装饰器用于条件性地跳过测试。



# 1.6 本章小结

在本章节中，开篇对比了几种常见的测试框架，并着重介绍了`pytest`这个流行的测试框架。我们讲解了`pytest`的优点，包括易于学习和使用、丰富的插件和扩展、具有灵活的设置和配置选项、支持测试用例的参数化运行等等。本文还提供了有关如何安装和部署`pytest`的指南，介绍了如何组织测试用例、使用`fixture`和参数化测试用例等pytest的一些核心概念和最佳实践。

总的来说，`pytest`提供了一个清晰的测试编写方法和强大的功能，使编写和维护测试变得更简单。这些特性在提高测试的覆盖率和精确度方面发挥着关键作用。

