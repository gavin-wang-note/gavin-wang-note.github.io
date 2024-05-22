---
title: 《pytest测试指南》-- 章节1-10 pytest常用插件介绍
date: 2024-05-30 23:00:00
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
summary: 《pytest测试指南》一书 章节1-10 pytest常用插件详解
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 第10章 pytest插件

`pytest` 的一个强大特性是支持插件，可以使用插件来扩展或改变`pytest`的行为，这使得`pytest`能够适用于各种不同的场景和需求。

许多插件可以通过Python的包管理工具pip安装。要使用一个插件，你需要先安装它，然后你可以在命令行中通过`pytest`运行您的测试，插件将自动被识别和加载。比如：

```shell
pip install pytest-cov
```

上述命令安装了`pytest-cov`插件，它用于生成测试覆盖报告。

目前在`Github`上（截止到2024-01-03），搜索`pytest-plugin`关键字，已经有952个插件了：

<img class="shadow" src="/img/in-post/GitHub-pytest-plugins.png" width="800">

`pytest`社区非常活跃，未来插件还会持续增加。

# 10.1 插件分类

## 10.1.1 内置插件

`pytest` 本身附带了许多有用的内置插件，比如：

- `mark`: 用于标记测试函数。
- `fixture`: 提供了一个强大的机制来定义初始化代码和清理代码。
- `skip`: 允许你跳过某些测试。
- `parametrize`: 允许以不同的参数多次运行同一个测试函数。

这些内置插件通常足以满足基本的测试需求。

## 10.1.2 第三方插件

社区为`pytest`开发了大量的第三方插件，这些插件可以通过pip进行安装。这包括但不限制于：

- `pytest-django`: 用于Django项目的测试。
- `pytest-flask`: 专门用于Flask应用的测试。
- `pytest-asyncio`: 用于测试异步io程序。
- `pytest-xdist`: 提供了分布式测试执行的能力，可以在多个CPU上并行运行测试。

## 10.1.3 自开发的插件

自己根据需求开发的插件。

# 10.2 查看可用的插件

如果想知道哪些插件在本地环境中是可用的，可以通过该命令：

```shell
pytest --trace-config
```

在测试头部信息中会显示激活的插件，它还会在加载本地插件时打印出`conftest.py文件`。

# 10.3 加载/禁用插件

我们可以阻止插件加载或使用它们（`NAME`为插件名称）:

```shell
pytest -p no:<NAME>
```

这样，后续`pytest`会话中就没办法进行插件的加载/使用了。

如果想无条件地禁用一个项目的插件，可以在项目配置文件`pytest.ini`中添加这个选项即可：

```shell
[pytest]
addopts = -p no:<NAME>
```

# 10.4 pytest启动时插件发现顺序

* 通过扫描命令行中的选项并阻止加载该插件（即使是内置插件也可以通过这种方式阻止）。这发生在正常的命令行解析之前，禁用方式：`-p no:name`。
* 通过加载所有内置插件。
* 通过扫描命令行选项并加载指定的插件。这发生在正常的命令行解析之前，使用方式：`-p name`。
* 通过加载通过`setuptools` 入口点注册的所有插件。
* 通过加载通过`PYTEST_PLUGINS`环境变量
* 通过加载`conftest.py`命令行调用推断的所有文件：
  * 如果没有指定测试路径，则使用当前目录作为测试路径
  * 如果存在，则加载`conftest.py`并`test*/conftest.py`相对于第一个测试路径的目录部分。加载文件后`conftest.py` ，加载其 `pytest_plugins`变量中指定的所有插件（如果存在）。
  * 请注意，`pytest` 在工具启动时不会`conftest.py`在更深的嵌套子目录中找到文件。`conftest.py`将文件保存在顶级测试或项目根目录中通常是个好主意。

- 通过递归加载 文件中`pytest_plugins`变量指定的所有插件`conftest.py`。

# 10.5 pytest常用插件介绍

## 10.5.1 进度条相关插件

### 10.5.1.1 pytest-sugar

`pytest-sugar` 插件改变 `pytest` 控制台的输出，增加了一些用户体验上的优化，使其更美观易读。这些改动涉及进度条和颜色编码的测试输出，它们能够提供一个更易读且视觉上更友好的界面来帮助快速识别测试状态。插件还会以不同颜色标记测试的不同状态，比如通过、失败、跳过。

这个插件不仅让测试结果的视觉表现变得更加友好，还在某种程度上提供了一些额外的信息，比如哪些测试较快、哪些较慢等。

#### 10.5.1.1.1 安装 pytest-sugar

要安装 `pytest-sugar`，你可以使用以下 pip 命令：

```shell
pip install pytest-sugar
```

安装成功后，`pytest-sugar` 会自动集成到 `pytest`，当你下次运行测试时，就会看到新的输出格式。

#### 10.5.1.1.2 pytest-sugar的参数

执行`pytest -h`会看到多出来两个参数：

```shell
  --old-summary         Show tests that failed instead of one-line tracebacks
  --force-sugar         Force pytest-sugar output even when not in real terminal
```

`--old-summary` 参数

当你运行`pytest`时，如果测试失败，`pytest-sugar`会在每次测试完成后显示一个彩色的进度条和一个简洁的一行跟踪信息。使用 `--old-summary` 参数可以改变这个行为，使`pytest`在测试会话结束时展示更传统的、详细的测试失败摘要，而不是默认的一行跟踪信息。

这个参数可能对那些想一次性在测试结束时看到所有失败测试详细信息的用户有用，而不是在每个测试后立即查看简短的跟踪信息。

`--force-sugar` 参数

正常情况下，`pytest-sugar`只有在检测到它运行在一个真实的终端中时才会启用，这意味着如果输出被重定向到文件或者通过某些工具查看时，你可能不会看到它特别的输出格式。

使用 `--force-sugar` 参数可以强制`pytest-sugar`输出其特色格式化的输出，即使`pytest`没有在一个真实的终端中运行。这可以用于某些情况下，即使在非终端环境中，你也希望享受`pytest-sugar`提供的美化输出效果。

当你运行`pytest`用例时，简单地在命令后添加这些参数就可以启用它们的特定功能。例如：

```shell
pytest --old-summary
pytest --force-sugar
```

如果需要同时使用这两个参数：

```shell
pytest --old-summary --force-sugar
```

记住，这些参数对任何不使用`pytest-sugar`插件的标准`pytest`命令无效，因此，要使用它们，你需要确保已经安装了`pytest-sugar`插件。

#### 10.5.1.1.3 使用 pytest-sugar

当你运行 `pytest` 测试时，`pytest-sugar` 会自动启动，并以新的、增强的界面格式显示测试结果。下面是一个简单 `pytest` 测试案例和它使用 `pytest-sugar` 的输出样例。

例如，你的测试代码 `test_math.py` 可能这样写：

```python
# content of test_math.py

def test_add():
    assert 1 + 1 == 2

def test_subtract():
    assert 2 - 1 == 1

def test_multiply():
    # This will fail
    assert 2 * 2 == 5

def test_divide():
    assert 4 / 2 == 2
```

你会看到一个动态进度条，每个测试项前面会有一个✓或✖表示测试是否通过，。

#### 10.5.1.1.4 pytest-sugar 输出界面

使用 `pytest-sugar` 运行这些测试，你可以使用以下命令：

```shell
pytest test_math.py
```

输出将与传统 `pytest` 输出有所不同，传统的 `pytest` 输出可能只显示测试的点状态，例如`.` 表示通过，而 `F` 表示失败。使用 `pytest-sugar` 后，每个测试项结果会有以下变化：

- ✓ 绿色：测试通过
- ✖ 红色：测试失败
- s 黄色：测试跳过

测试失败时，`pytest-sugar` 会展示详细的差异对比，在最后以红色的方式突出显示，能清楚地看到实际值与期待值之间的不同。

如下为运行效果：

没安装 `pytest-sugar` 之前：

<img class="shadow" src="/img/in-post/no-pytest-sugar.png" width="800">

安装 `pytest-sugar` 之后：

<img class="shadow" src="/img/in-post/use-pytest-sugar.png" width="800">



#### 10.5.1.1.5 禁用 pytest-sugar

如果由于某些原因你想禁用 `pytest-sugar` 的输出效果，你可以在运行 `pytest` 时加上 `-p no:sugar` 参数：

```shell
pytest -p no:sugar test_math.py
```

这将告诉 `pytest` 在这次测试中不加载 `pytest-sugar` 插件。

#### 10.5.1.1.6 注意事项

`pytest-sugar` 对用户的测试体验做了增强，但它不改变 `pytest` 的内核工作方式。若要在 CI/CD 管道中使用或者需要集成到更复杂的测试环境中，确保 `pytest-sugar` 的输出不会与其他工具冲突。比如，某些工具可能会解析标准输出来检查测试结果，这时候 `pytest-sugar` 的自定义输出可能会导致解析问题。



### 10.5.1.2 pytest-pgogress

`pytest-progress` 插件用于在测试运行时显示进度。这个插件通过在控制台输出的方式，给出更多的实时反馈，比如测试的当前状态和剩余时间估算。

此插件的使用，带来或展示：

- 在 `pytest` 运行期间，实时显示测试进度，包括已经完成的、正在进行的和剩余的测试数量。
- 有助于在运行较长时间的测试集时，了解进度和剩余的工作量。

#### 10.5.1.2.1 安装 pytest-progress

你可以使用 `pip` 来安装 `pytest-progress` 插件：

```sh
pip install pytest-progress
```

#### 10.5.1.2.2 使用 pytest-progress

安装好 `pytest-progress` 插件之后，`pytest`命令多出来一个参数：

```shell
  --show-progress       Prints test progress on the terminal.
```

需要你在执行 `pytest` 时携带上次参数才能看到新的进度条显示。使用此插件时，对于每个测试用例的开始和结束，以及测试用例的数量和完成百分比，都会通过控制台实时显示。

#### 10.5.1.2.3 pytest-progress 输出界面

<img class="shadow" src="/img/in-post/use-pytest-progress.png" width="800">

每个用例执行都会更新进度，并展示用例总数，当前执行到第多少个用例，以及`Pass,Fail,Skip,XPass,XFail,Error, ReRun`的数量信息，方便用户实时看到进度。

#### 10.5.1.2.4 注意事项

- 由于 `pytest-progress` 的输出是实时的，如果在 CI 系统中使用，可能需要特别注意输出格式，因为一些 CI 系统可能不支持动态更新的进度条等实时输出特性。
- `pytest-progress` 插件的确切特性和配置可能会随着版本的更新而有所变化，因此请根据其文档或 `GitHub` 上的项目主页来获取最新和最准确的信息。

`pytest-progress` 为长时间运行的测试集提供了更良好的用户体验，特别是在需要等待较长时间以观察测试结果和进度的场合。

## 10.5.2 用例执行顺序相关插件

### 10.5.2.1 pytest-order

`pytest-order` 插件允许你自定义测试执行的顺序，此插件对于确保测试的执行顺序与特定的依赖或需求相匹配特别有用。你可以使用它来确保特定的测试总是首先运行，或者某些测试在其他测试之后运行。

#### 10.5.2.1.1 功能特点

* 指定测试用例执行顺序：通过用 `pytest.mark.order` 标记测试用例，你可以指定测试执行的特定顺序。
* 依赖控制：你可以使用 `pytest.mark.depends` 来指定测试依赖于其他特定测试的成功执行。
* 更细粒度的顺序控制：也提供了按照类和模块层级的顺序控制。例如，你可以指定一个类中的所有测试在另一个类之前或之后执行。
* 高度可配置性：插件可以配置为按照数字顺序、字母顺序或者标记顺序进行排序。

#### 10.5.2.1.2 使用场景

- **复杂环境的设置和清理**：当测试需要先设置复杂环境且清理代价很高时，你可能希望先执行这些需要该环境的所有测试。
- **顺序依赖的测试**：对于一系列操作需要顺序执行的集成测试，例如先创建资源再修改和删除它们的测试。
- **回归测试**：优先运行以前失败过的测试用例或最有可能失败的测试用例。

#### 10.5.2.1.3 安装 pytest-order

要安装 `pytest-order`，可以使用 `pip`：

```sh
pip install pytest-order
```

#### 10.5.2.1.4 初级排序示例

安装 `pytest-order` 插件之后，您可以使用 `order` 标记为您的测试函数和方法设定执行顺序。标记接受一个整数作为参数（也可以是负数的，比如-1），代表该测试的执行位置：

```python
# content of test_pytest_order_v1.py
import pytest

@pytest.mark.order(2)
def test_foo():
    assert True

@pytest.mark.order(1)
def test_bar():
    assert True

@pytest.mark.order(3)
def test_baz():
    assert True
```

在这个例子中，虽然 `test_foo` 被定义在最前面，但由于使用 `pytest.mark.order` 标记并传递了顺序参数，`test_bar` 将会首先执行，其次是 `test_foo`，然后是 `test_baz`。运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_pytest_order_v1.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0
collecting ... /root/code/chapter1-10/test_pytest_order_v1.py:3: PytestUnknownMarkWarning: Unknown pytest.mark.order - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
  @pytest.mark.order(2)
/root/code/chapter1-10/test_pytest_order_v1.py:7: PytestUnknownMarkWarning: Unknown pytest.mark.order - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
  @pytest.mark.order(1)
/root/code/chapter1-10/test_pytest_order_v1.py:11: PytestUnknownMarkWarning: Unknown pytest.mark.order - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
  @pytest.mark.order(3)
collected 3 items

 chapter1-10/test_pytest_order_v1.py::test_foo ✓                  33% ███▍      
 chapter1-10/test_pytest_order_v1.py::test_bar ✓                  67% ██████▋   
 chapter1-10/test_pytest_order_v1.py::test_baz ✓                 100% ██████████

Results (0.01s):
       3 passed
root@Gavin:~/code/chapter1-10#
```

上面有告警：`PytestUnknownMarkWarning: Unknown pytest.mark.order - is this a typo?`，如果想消除此告警，可以在`pytest.ini`文件中增加如下内容：

```ini
markers =
    order: test case order
```

再执行上述用例：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_pytest_order_v1.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0
collected 3 items

 chapter1-10/test_pytest_order_v1.py::test_foo ✓                 33% ███▍      
 chapter1-10/test_pytest_order_v1.py::test_bar ✓                 67% ██████▋   
 chapter1-10/test_pytest_order_v1.py::test_baz ✓                100% ██████████

Results (0.01s):
       3 passed
root@Gavin:~/code/chapter1-10#
```

#### 10.5.2.1.5 高级排序示例

`pytest-order` 还支持更细致的排序控制，你可以使用它来让一组测试在另一组测试之后运行：

```python
# content of test_pytest_order_v2.py
import pytest

# 排在 "group_two" 测试之前的 "group_one" 测试
@pytest.mark.order(before="group_two")
class TestGroupOne:
    def test_one(self):
        assert True

    def test_two(self):
        assert True

# 排在 "group_one" 测试之后的 "group_two" 测试
@pytest.mark.order(after="group_one")
class TestGroupTwo:
    def test_three(self):
        assert True

    def test_four(self):
        assert True
```

运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_pytest_order_v2.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0
collected 4 items

 chapter1-10/test_pytest_order_v2.py::TestGroupOne.test_one ✓         25% ██▌       
 chapter1-10/test_pytest_order_v2.py::TestGroupOne.test_two ✓         50% █████     
 chapter1-10/test_pytest_order_v2.py::TestGroupTwo.test_three ✓       75% ███████▌  
 chapter1-10/test_pytest_order_v2.py::TestGroupTwo.test_four ✓       100% ██████████

Results (0.02s):
       4 passed
root@Gavin:~/code/chapter1-10# 
```

#### 10.5.2.1.6 Q/A？

Q：存在一个诸多个目录及其子目录下的用例集合中，有一些用例使用`pytest.mark.order`设置了顺序，这些用例是否一定在最后才被执行？

A：不一定。`pytest.mark.order` 装饰的测试用例的执行取决于你为 `order` 装饰器传递的参数。

如果你设置 `pytest.mark.order` 的参数为一个特别大的值，那么相应的测试用例将会在最后执行。例如：

```python
import pytest

@pytest.mark.order(10000)
def test_something():
    assert True
```

上述代码中，因为 `test_something` 的 `order` 参数被设置为了非常大的一个数字，它将在其他没有使用 `order` 裰饰器，或者具有较小 `order` 参数值的测试用例之后执行。

相反，如果你设置它为 `-1` 或任意负数，它通常会在最后执行，因为在 `pytest-order` 中，负数视为低于没有 `order` 设置的测试用例的顺序级别。例如：

```python
import pytest

@pytest.mark.order(-1)
def test_something():
    assert True
```

这样，`test_something` 用例会在没有使用 `order` 修饰，以及具有正的 `order` 值的测试用例之后执行。然而，如果有其他测试用例也被设置了相同或者更大的负数作为 `order` 参数的值，则这些测试之间的执行顺序将由它们的顺序值决定。

如果你没有为 `order` 提供参数或提供 `0` 或较小的值，那么这个装饰的测试不一定会在最后执行。没有提供 `order` 值的测试用例将按照 `pytest` 的默认行为（通常是测试文件、函数名等的字典顺序）进行排序。

总之，确保一个测试用例执行顺序在最后，你需要为 `pytest.mark.order` 提供一个足够高的值（相对于其他用例的 `order` 值），或者一个负数。如果在多个目录和不同的模块中运行测试，`pytest-order` 会尽其所能整个会话中保持给定的顺序，只要正确地为 `order` 设置了值。

#### 10.6.2.1.7 注意事项

- 测试顺序应当被谨慎使用，因为它可能会掩盖测试之间不适当的依赖，降低测试的独立性和可靠性。
- 如果可能，最好使得测试用例彼此独立，从而可以任意顺序执行。这通常是更健壮的测试策略。
- 除了使用插件外，还可以通过自定义 `pytest` 的测试收集钩子（hook），如 `pytest_collection_modifyitems`，以编程方式改变测试的运行顺序，请参考本书相关章节中对“hook”的介绍。

### 10.5.2.2 pytest-ording

`pytest-ordering` 是一个较早期的插件，也用于控制测试用例的执行顺序。对于某些情况下不得不按照特定顺序运行的测试，这个插件可以很有帮助。请注意，`pytest-ordering` 与 `pytest-order` 是不同的插件。但这个插件已经多年不维护了，比较老旧，但依然被最新版的`pytest`所支持（比如`pytest 7.4.0`）。

#### 10.5.2.2.1 安装 `pytest-ordering`

你可以使用 `pip` 安装 `pytest-ordering` 插件：

```sh
pip install pytest-ordering
```

#### 10.5.2.2.2 使用场景

- **测试有依赖条件**：如果某些测试需要依赖其他测试的结果或需要以特定的先后顺序执行。
- **使能关键测试先执行**：例如，先运行最关键的集成测试，这样一旦发生失败，可以尽快反馈信息。
- **性能优化**：测试套件具有许多测试用例，特定的执行顺序可以减少设置/清理环境的次数，从而减少总测试时间。

#### 10.5.2.2.3 示例代码

使用 `pytest-ordering` 时，你可以利用提供的装饰器如 `run(order=N)` 来指定测试执行顺序。

```python
# content of test_pytest_ordering.py
import pytest

@pytest.mark.run(order=2)
def test_foo():
    assert True

@pytest.mark.run(order=1)
def test_bar():
    assert True

@pytest.mark.run(order=3)
def test_baz():
    assert True
```

在这个例子中，三个测试函数因为各自的 `order=N` 裰饰器所设置的顺序而依次执行，执行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_pytest_ordering.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, ordering-0.6
collected 3 items

 chapter1-10/test_pytest_ordering.py::test_bar ✓                        33% ███▍      
 chapter1-10/test_pytest_ordering.py::test_foo ✓                        67% ██████▋   
 chapter1-10/test_pytest_ordering.py::test_baz ✓                       100% ██████████

Results (0.02s):
       3 passed
root@Gavin:~/code/chapter1-10#
```

#### 10.5.2.2.4 注意事项

- **测试的独立性**：测试应该尽量独立运行。过度依赖顺序执行的测试可能会掩盖代码中的问题。
- **维护**：依赖特定执行顺序的测试让维护和理解测试套件变得复杂，特别是对于新加入项目的开发者来说。
- **可移植性**：依赖顺序的测试可能会使得测试套件在某些环境下（特别是并行执行时）运行失败。
- **使用最新版本**：这些插件会继续更新和改进，确认你使用的是最新版本的插件。

#### 10.5.2.2.5 `pytest-ordering` 和 `pytest-order` 的区别

| 特性/插件          | pytest-ordering                            | pytest-order                                                 |
| ------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| 排序标记           | `@pytest.mark.run(order=n)`                | `@pytest.mark.order(n)`                                      |
| 指定首尾顺序的方法 | 使用整数索引，没有专门的首尾标记           | 可以用`first`和`last`来标记在最前或最后运行的测试            |
| 详细排序控制       | 主要通过数字索引来控制排序                 | 提供了除了数字排序外，更详细的排序控制，如按照指定测试后运行等 |
| 依赖控制           | 不提供显示的依赖关系功能                   | 支持依赖关系排序，可以指定某些测试在其他测试之后执行         |
| 标记冲突处理       | 没有明确指导如何处理多个排序标记冲突       | 允许为同一测试指定多个排序参数，并提供规则解决可能的序号冲突 |
| 灵活性/可用性      | 提供基础的顺序控制功能，可能不再活跃维护   | 更为活跃地维护，提供了更灵活的顺序控制功能                   |
| 兼容性和维护情况   | 缺少维护和文档更新，停更多年               | 有定期的更新和维护，以及与最新`pytest`版本的兼容性           |
| 社区使用           | 可能较少使用，新用户建议查看目前的维护状态 | 在社区中有较广泛的使用和支持                                 |

综合比较，推荐使用`pytest-order`插件。

## 10.5.3 用例运行相关插件

### 10.5.3.1 失败重试

`pytest-rerunfailures` 插件为 `pytest` 添加了重新运行失败或错误的测试用例的能力。这在处理间歇性失败的测试（被称为 "flaky" 测试）时特别有用，它们可能由于许多因素（如网络延迟、资源加载问题、并发问题等）偶尔失败。

#### 10.5.3.1.1 主要特性

- **自动重试**：能够自动重新运行未通过的测试。
- **重试次数**：可以定义要重新运行每个失败测试的次数。
- **重试延迟**：可以在重试之间设置延迟。
- **有条件的重试**：可以根据失败原因有选择地重试测试。
- **与其他插件兼容**：可以与如 `pytest-xdist` 的并行测试执行插件共同使用。

#### 10.5.3.1.2 使用场景

- **处理间歇性错误**：网络请求或集成测试中的间歇性错误。
- **外部资源波动**：依赖于外部服务或资源的测试可能受到这些资源的可用性或响应速度的影响。
- **并发问题**：并发环境中可能出现的竞争条件或其他并发问题。
- **加载时间差异**：例如，UI 测试中的元素加载时间可能因环境而异。

#### 10.5.3.1.3 安装 pytest-rerunfailures

通过 pip 安装：

```sh
pip install -U pytest-rerunfailures
```

#### 10.5.3.1.4 代码示例和注解

使用命令行选项自动重试所有失败的测试：

```sh
pytest --reruns 2 --reruns-delay 1
```

在此例中，失败的测试将被自动重新运行最多两次，并在每次重试前设置 1 秒的延迟。

对特定测试使用 `@pytest.mark.flaky` 重试：

```python
# content of test_rerunfailures.py
import random
import pytest

# 无条件地在每个错误或失败的测试后重试最多两次
@pytest.mark.flaky(reruns=2)
def test_example_fail_twice():
    """这个测试有一个随机因素，它可能会失败，我们将尝试重跑两次。"""
    assert random.choice([True, False])

# 在特定条件下重试
@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_example_with_condition():
    """这个测试在特定条件下失败，我们将重试5次，并在重试间增加延迟。"""
    value = random.randint(0, 5)
    assert value > 2

# 没有使用rerunfailures装饰器的测试
def test_always_passes():
    """这个测试总是通过，不涉及重跑逻辑。"""
    assert True
```

如果期间有测试失败，`pytest-rerunfailures` 插件会按照指定的 `reruns` 数量对失败的测试进行重试。对于带有 `@pytest.mark.flaky` 装饰器的测试，如 `test_example_fail_twice` 和 `test_example_with_condition`，将遵循装饰器中定义的重试规则。

`test_always_passes` 是一个普通的测试，不涵盖重跑逻辑，所以如果它失败了，它不会自动重试。

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_rerunfailures.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, ordering-0.6
collected 3 items

 chapter1-10/test_rerunfailures.py::test_example_fail_twice ✓         33% ███▍      
 chapter1-10/test_rerunfailures.py::test_example_with_condition ✓     67% ██████▋   
 chapter1-10/test_rerunfailures.py::test_always_passes ✓             100% ██████████

Results (0.02s):
       3 passed
root@Gavin:~/code/chapter1-10# pytest -s -v test_rerunfailures.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, ordering-0.6
collected 3 items
―――――――――――――――――――――――――――― test_example_fail_twice ―――――――――――――――――――――――――――

    @pytest.mark.flaky(reruns=2)
    def test_example_fail_twice():
        """这个测试有一个随机因素，它可能会失败，我们将尝试重跑两次。"""
>       assert random.choice([True, False])
E       assert False
E        +  where False = <bound method Random.choice of <random.Random object at 0x1472850>>([True, False])
E        +    where <bound method Random.choice of <random.Random object at 0x1472850>> = random.choice

test_rerunfailures.py:8: AssertionError

 chapter1-10/test_rerunfailures.py::test_example_fail_twice ⨯       33% ███▍      
 chapter1-10/test_rerunfailures.py::test_example_with_condition ✓   67% ██████▋   
 chapter1-10/test_rerunfailures.py::test_always_passes ✓           100% ██████████

Results (0.05s):
       2 passed
       1 failed
         - chapter1-10/test_rerunfailures.py:5 test_example_fail_twice
       2 rerun
root@Gavin:~/code/chapter1-10# pytest -s -v test_rerunfailures.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, ordering-0.6
collected 3 items

 chapter1-10/test_rerunfailures.py::test_example_fail_twice R✓       33% ███▍      
 chapter1-10/test_rerunfailures.py::test_example_with_condition ✓    67% ██████▋   
 chapter1-10/test_rerunfailures.py::test_always_passes ✓            100% ██████████

Results (0.02s):
       3 passed
       1 rerun
root@Gavin:~/code/chapter1-10#
```

从执行结果看，用例`test_example_fail_twice`第一次执行成功，第二次失败，第三次成功。再来看一下携带参数的效果：

```shell
root@Gavin:~/code/chapter1-10# pytest --reruns 2 --reruns-delay 1 test_rerunfailures.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, ordering-0.6
collected 3 items

 chapter1-10/test_rerunfailures.py::test_example_fail_twice ✓         33% ███▍      
 chapter1-10/test_rerunfailures.py::test_example_with_condition R✓    67% ██████▋   
 chapter1-10/test_rerunfailures.py::test_always_passes ✓             100% ██████████

Results (1.03s):
       3 passed
       1 rerun
root@Gavin:~/code/chapter1-10#
```

#### 10.5.3.1.5 注意事项

- **遮掩问题**：自动重试有可能掩盖根本问题，而这些问题可能需要修复。
- **增加测试时间**：重试失败的测试会增加总体的测试执行时间。
- **与CI集成**：在持续集成系统中使用时需要考虑到测试时间延长问题。
- **可能的资源清理**：在重试前可能需要清理由前一次测试运行留下的资源，避免 "脏" 环境影响后续测试。
- **并行测试**：在并行测试中使用时要特别小心，重试可能不会按预期工作。

`pytest-rerunfailures` 插件很适合用在不稳定或易受环境影响的测试上，但最好还是尽量让测试保持稳定和可预测，并且对 flaky 测试进行额外的调查和分析，以防在一个确定性的环境中隐藏问题。记住，过度依赖自动重试可能会降低持续集成反馈的价值，并使得问题难以被察觉和解决。

### 10.5.3.2 重复运行

`pytest-repeat` 插件用于重复运行同一个测试多次，这个插件常用在某些特定的测试场景中，比如压力测试、稳定性测试或帮助识别和调试偶尔出现的错误。

#### 10.5.3.2.1 安装 pytest-repeat

使用 `pip` 安装 `pytest-repeat`:

```shell
pip install pytest-repeat
```

#### 10.5.3.2.2 主要特性

- **重复运行测试**：允许开发者指定一个测试用例或整个测试套件需要重复运行的次数。
- **与其他标记结合**：可以与其他`pytest`标记结合使用，例如只重复失败的测试。
- **简单的命令行选项**：提供简洁的命令行选项来指定重复的次数，使其易于使用。

#### 10.5.3.2.3 使用场景

- **性能测试**：重复运行特定的测试用例以监视性能变化。
- **稳定性和健壮性测试**：验证代码的稳定性，尤其在更改底层逻辑或环境时。
- **找出偶发性错误**：重复测试以查找硬件或网络引起的偶发性错误。
- **加载测试**：通过连续运行测试来检查系统在持续负载下的表现。

#### 10.5.3.2.4 代码示例和注解

假设有一个`test_repeat_v1.py`文件，包括以下的测试：

```python
# content of test_repeat_v1.py
def test_repeat_example():
    # 这里是你的测试逻辑
    assert 1 + 1 == 2
```

要连续运行这个测试5次，可以在命令行使用：

```sh
pytest test_repeat_v1.py --count=5
```

每次运行结束后，`pytest` 会立即重启测试，直到达到指定次数，运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_repeat_v1.py --count=5
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
collected 5 items

 chapter1-10/test_repeat_v1.py::test_repeat_example[1-5] ✓           20% ██        
 chapter1-10/test_repeat_v1.py::test_repeat_example[2-5] ✓           40% ████      
 chapter1-10/test_repeat_v1.py::test_repeat_example[3-5] ✓           60% ██████    
 chapter1-10/test_repeat_v1.py::test_repeat_example[4-5] ✓           80% ████████  
 chapter1-10/test_repeat_v1.py::test_repeat_example[5-5] ✓          100% ██████████

Results (0.02s):
       5 passed
root@Gavin:~/code/chapter1-10#
```

该插件同样支持在代码中使用装饰器：

```python
# content of test_repeat_v2.py
import pytest

@pytest.mark.repeat(10)
def test_repeat_example():
    # 这个测试将会运行10次
    assert 1 + 1 == 2
```

使用上面的装饰器，`pytest` 会将 `test_repeat_example` 测试重复执行10次，运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_repeat_v2.py
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
collected 10 items

 chapter1-10/test_repeat_v2.py::test_repeat_example[1-10] ✓             10% █         
 chapter1-10/test_repeat_v2.py::test_repeat_example[2-10] ✓             20% ██        
 chapter1-10/test_repeat_v2.py::test_repeat_example[3-10] ✓             30% ███       
 chapter1-10/test_repeat_v2.py::test_repeat_example[4-10] ✓             40% ████      
 chapter1-10/test_repeat_v2.py::test_repeat_example[5-10] ✓             50% █████     
 chapter1-10/test_repeat_v2.py::test_repeat_example[6-10] ✓             60% ██████    
 chapter1-10/test_repeat_v2.py::test_repeat_example[7-10] ✓             70% ███████   
 chapter1-10/test_repeat_v2.py::test_repeat_example[8-10] ✓             80% ████████  
 chapter1-10/test_repeat_v2.py::test_repeat_example[9-10] ✓             90% █████████ 
 chapter1-10/test_repeat_v2.py::test_repeat_example[10-10] ✓           100% ██████████

Results (0.02s):
      10 passed
root@Gavin:~/code/chapter1-10# 
```

#### 10.5.3.2.5 注意事项

- **掩盖问题**：重复运行测试有可能掩盖较为偶发的问题或者导致测试结果不稳定。
- **资源使用**：重复运行会消耗更多的计算资源和测试时间，尤其对于测试数量和测试本身的复杂性。
- **测试隔离**：确保测试之间没有依赖关系，每次运行都是独立的和干净的环境。

`pytest-repeat` 提供了一种简单直接的方式来实现某些特定类型的测试，但其使用应该谨慎且目标明确，避免滥用。


### 10.5.3.3 并行运行

`pytest-xdist` 是一个功能强大的 `pytest` 插件，它使得测试能够并行运行，同时还提供了分布式测试和循环测试的其他机制。

#### 10.5.3.3.1 安装 pytest-xdist

使用 `pip` 安装 `pytest-xdist`：

```shell
pip install pytest-xdist
```

#### 10.5.3.3.2 主要特性

- **并行测试**：可以在多个CPU上同时运行测试，显著减少测试的运行时间。
- **分布式测试**：支持在多个远程机器上分布式运行测试。
- **加载均衡**：当多个测试节点（workers）可用时，`pytest-xdist` 会智能地分配测试用例以优化运行时间。
- **循环测试**：可以持续循环运行测试直到出现错误，对于发现偶发性测试失败很有用。

#### 10.5.3.3.3 使用场景

- **大型测试套件**：当有很多测试用例时，使用 `pytest-xdist` 可以并行运行，节省时间。
- **持续集成/快速反馈**：把并行测试集成到持续集成流程中，可以更快地获得构建和测试的反馈。
- **资源密集测试**：对于需要大量计算资源的测试，比如算法性能测试，在多个机器上分布式运行可以获得更好的资源利用。

#### 10.5.3.3.4 分布式执行用例的设计原则

- **独立运行**：用例之间是独立的，用例之间没有依赖关系，用例可以完全独立运行
- **随机执行**：用例执行没有顺序，随机顺序都能正常执行
- **不影响其他用例**：每个用例都能重复运行，运行结果不会影响其他用例

#### 10.5.3.3.5 代码示例和注解

##### 10.5.3.3.5.1 指定CPU数并行测试

以下命令将使用4个 CPU 进行测试：

```sh
pytest -n 4
```

这意味着 `pytest` 将并行启动4个测试节点（workers），把测试用例均匀地分散到这些节点上运行。

我们来看一个示例：

```python
# content of test_pytest_xdist_cases.py
import time
import pytest


# 下面我们定义了30个独立的测试用例
@pytest.mark.parametrize('num', range(1, 31))
def test_number_1(num):
    time.sleep(0.5)  # 模拟执行过程
    assert num == num  # 这里的断言总是为真
```

如果不并行运行：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_pytest_xdist_cases.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
collected 30 items

 chapter1-10/test_pytest_xdist_cases.py::test_number_1[1] ✓              3% ▍         
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[2] ✓              7% ▋         
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[3] ✓              10% █         
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[4] ✓              13% █▍        
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[5] ✓              17% █▋        
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[6] ✓              20% ██        
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[7] ✓              23% ██▍       
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[8] ✓              27% ██▋       
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[9] ✓              30% ███       
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[10] ✓             33% ███▍      
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[11] ✓             37% ███▋      
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[12] ✓             40% ████      
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[13] ✓             43% ████▍     
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[14] ✓             47% ████▋     
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[15] ✓             50% █████     
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[16] ✓             53% █████▍    
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[17] ✓             57% █████▋    
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[18] ✓             60% ██████    
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[19] ✓             63% ██████▍   
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[20] ✓             67% ██████▋   
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[21] ✓             70% ███████   
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[22] ✓             73% ███████▍  
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[23] ✓             77% ███████▋  
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[24] ✓             80% ████████  
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[25] ✓             83% ████████▍ 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[26] ✓             87% ████████▋ 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[27] ✓             90% █████████ 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[28] ✓             93% █████████▍
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[29] ✓             97% █████████▋
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[30] ✓            100% ██████████

Results (15.12s):
      30 passed
root@Gavin:~/code/chapter1-10#
```

30个用例耗时了15.12秒，如果并行运行：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v -n 4 test_pytest_xdist_cases.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
4 workers [30 items]    collecting ... 
scheduling tests via LoadScheduling

 chapter1-10/test_pytest_xdist_cases.py::test_number_1[1] ✓             3% ▍         
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[5] ✓             10% █         
[gw2] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[3] ✓             7% ▋         
[gw1] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[7] ✓             13% █▍        
[gw3] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[2] ✓             17% █▋        
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[6] ✓             20% ██        
[gw2] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[8] ✓             23% ██▍       
[gw3] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[4] ✓             27% ██▋       
[gw1] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[9] ✓             30% ███       
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[11] ✓            33% ███▍      
[gw2] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[10] ✓            37% ███▋      
[gw1] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[12] ✓            40% ████      
[gw3] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[13] ✓            43% ████▍     
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[15] ✓            50% █████     
[gw1] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[16] ✓            47% ████▋     
[gw2] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[14] ✓            53% █████▍    
[gw3] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[17] ✓            57% █████▋    
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[19] ✓            63% ██████▍   
[gw1] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[18] ✓            60% ██████    
[gw2] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[20] ✓            67% ██████▋   
[gw3] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[21] ✓            70% ███████   
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[23] ✓            73% ███████▍  
[gw1] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[22] ✓            77% ███████▋  
[gw2] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[24] ✓            80% ████████  
[gw3] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[25] ✓            83% ████████▍ 
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[28] ✓            87% ████████▋ 
[gw3] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[26] ✓            93% █████████▍
[gw1] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[27] ✓            90% █████████ 
[gw2] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[29] ✓            97% █████████▋
[gw0] PASSED test_pytest_xdist_cases.py 
 chapter1-10/test_pytest_xdist_cases.py::test_number_1[30] ✓           100% ██████████
[gw1] PASSED test_pytest_xdist_cases.py 

Results (4.44s):

      30 passed
root@Gavin:~/code/chapter1-10#
```

并行运行后，发现从顺次运行的15.12秒降低到了4.44秒，时间节约了不少。

##### 10.5.3.3.5.2 循环运行直到出现错误

如果要持续循环运行测试直到出现错误：

```sh
pytest --looponfail
```

这会启动一个持续测试的会话，它会监视你的项目文件。当文件改变时，它将只重新运行之前失败的测试而不是运行完整的测试套件，使得开发循环变得更快速响应。具体来说，当开启这个模式后，每当你保存一个文件时，`pytest` 会重新运行上次失败的测试，常用于：

- 开发一个特定的功能或修复一个bug时，你可能需要频繁运行测试来核实代码的改动。
- 在处理一个具体的失败用例时，你可能希望一边调整代码一边立即查看测试的结果。

我们来看一个示例，考虑有下述的失败测试用例：

```python
# content of test_pytest_xdist_looponfail.py
def test_always_fails():
    assert False, "This test always fails"

def test_always_passes():
    assert True, "This test always passes"
```

运行测试：

```shell
pytest -s -v --looponfail test_pytest_xdist_looponfail.py
```

开始时，两个测试都会被执行，其中 `test_always_fails` 会失败。在 `--looponfail` 模式下，`pytest` 将监视所有相关的文件变动。如果你修复了 `test_always_fails`（例如把 `assert False` 改为 `assert True`），并保存了文件，`pytest` 会立即重新运行该测试。

**请注意：**

- 监听文件变动意味着这个模式在某些情况下可能会增加CPU的使用。
- `--looponfail` 模式下，会话一直开启直到你手动终止（如使用 Ctrl + C）。
- 在进行较大范围的变动或重构时，可能需要暂时关闭这个模式，以避免过多的重运行。

##### 10.5.3.3.5.3 指定如何分配测试用例给并行的worker进程

 `pytest-xdist`默认是无序执行的，可以通过 `--dist` 参数来控制顺序。`pytest-xdist` 的 `--dist=loadscope` 参数是一个分布模式选项，这个参数的主要目的是在并行测试时，根据测试用例定义的 scope 来分配测试到不同的进程。

当使用 `pytest-xdist` 并行测试并指定 `--dist=loadscope` 参数时，测试用例会根据其 scope 被分组，然后将整个组分配给相同的进程进行执行。scope 可以是 `function`、`class`、`module` 或 `session`。

- `function` 范围的 scope 指的是每个测试函数都单独运行，在 pytest-xdist 中无需特定处理。
- `class` 范围的 scope 表示一个类中所有的测试函数都在一个进程中运行。
- `module` 范围的 scope 指的是同一个模块中的所有测试函数都在一个进程中运行。
- `session` 范围的 scope 要求在整个测试会话中只运行一次，所以它们不受 `loadscope` 影响。

使用 `--dist=loadscope` 非常适合以下情况：

- 当测试类或模块中的测试需要共享设施或状态时（比如共享的 `class` 或 `module` scope 的 fixtures）。
- 当希望减少 fixture 的设置和清理次数时，因为它们只在特定的进程中初始化一次。

**示例用法：**

在命令行中使用 `pytest-xdist` 进行测试执行，并指定 `--dist=loadscope` 参数：

```sh
pytest -n NUM --dist=loadscope
```

其中 `NUM` 是你要启动的 worker 进程数量。

**代码示例：**

假设我们有一个模块 `test_pytest_xdist_loadcope.py` 和一些装饰了 `@pytest.mark.parametrize` 和 `@pytest.fixture` 的测试函数，并且希望它们按照模块进行排序：

```python
# content of test_pytest_xdist_loadscope.py
import pytest

@pytest.fixture(scope='module')
def module_fixture():
    return "data for module"

@pytest.mark.parametrize('input_value', ['a', 'b'])
def test_one(module_fixture, input_value):
    assert module_fixture and input_value

@pytest.mark.parametrize('input_value', [1, 2])
def test_two(module_fixture, input_value):
    assert module_fixture and input_value
```

运行测试：

```sh
pytest -n 2 --dist=loadscope test_pytest_xdist_loadcope.py
```

这个命令会使用两个进程，根据 `module` scope 将 `test_pytest_xdist_loadscope.py` 中的所有测试用例分配给一个进程，因此 `module_fixture` 只会初始化一次，并用于该文件中的所有测试。

**请注意：**

- **资源管理**：使用 `loadscope` 时，重要的是要管理好所有在作用域中共享的资源，避免状态污染或资源泄漏。
- **测试独立性**：尽管使用了 `loadscope`，最好的做法仍然是尽量确保测试彼此独立，特别是在考虑并发情况时。
- **性能权衡**：如果每个测试类或模块的测试数量不均匀，使用 `loadscope` 有可能导致某些 worker 饱和而其他worker空闲，这可能会降低总体的测试运行效率。因此，平衡测试数量在这种情况下是值得考虑的。

分布模式 `loadscope` 对于测试执行时间的提升效果取决于测试用例的分布情况，如果模块或类包含很多测试用例，则 `loadscope` 会更高效。如果模块或类中只有少数测试用例，可能不会注意到显著的性能提升。

##### 10.5.3.3.5.4 同一个文件里的测试用例被分配给同一个 worker 进程

当使用 `--dist=loadfile` 参数时，`pytest-xdist` 将确保同一个文件里的测试用例会被分配给同一个 worker 进程。测试用例不会跨文件分配。这样做的好处是测试文件之间如果有依赖关系（比如一个文件的测试执行可能会改变环境状态并影响另一个文件的测试），这可以保证单独一个文件内的测试用例之间的依赖不会因为并行测试而中断。

如果你的测试文件较大，测试用例数量较多，并且你希望相关的测试尽可能在同一个进程中执行，以减少进程启动和环境初始化的开销，那么使用 `--dist=loadfile` 参数会非常适合。

在命令行运行 `pytest` 并使用 `--dist=loadfile` 参数：

```shell
pytest -n NUM --dist=loadfile
```

这里的 `NUM` 是并行进程的数量。例如，如果你有 `4` 个测试文件和 `4` 个worker进程，每个测试文件将由单独的worker执行。

代码示例：

设想有以下两个测试文件：`test_pytest_xdist_loadfile_v1.py` 和 `test_pytest_xdist_loadfile_v2.py`，每个文件包含数个测试用例。

```python
# content of test_pytest_xdist_loadfile_v1.py
def test_a():
    pass

def test_b():
    pass
# content of test_pytest_xdist_loadfile_v2.py
def test_c():
    pass

def test_d():
    pass
```

运行测试：

```shell
pytest -n 2 --dist=loadfile
```

上面的命令会启动两个worker进程来并行运行测试。使用 `--dist=loadfile` 保证 `test_pytest_xdist_loadfile_v1.py` 中的所有测试 (`test_a` 和 `test_b`) 将在同一个进程中执行，`test_pytest_xdist_loadfile_v2.py` 中的所有测试 (`test_c` 和 `test_d`) 同样会在同一个进程中执行（可能是另一个进程）。运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v -n 2 --dist=loadfile test_pytest_xdist_loadfile_v*
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
2 workers [4 items]     collecting ... 
scheduling tests via LoadFileScheduling

 chapter1-10/test_pytest_xdist_loadfile_v2.py::test_c ✓                   25% ██▌       
[gw1] PASSED test_pytest_xdist_loadfile_v2.py 
 chapter1-10/test_pytest_xdist_loadfile_v2.py::test_d ✓                  100% ██████████
[gw1] PASSED test_pytest_xdist_loadfile_v2.py 
 chapter1-10/test_pytest_xdist_loadfile_v1.py::test_a ✓                   50% █████     
[gw0] PASSED test_pytest_xdist_loadfile_v1.py 
 chapter1-10/test_pytest_xdist_loadfile_v1.py::test_b ✓                   75% ███████▌  
[gw0] PASSED test_pytest_xdist_loadfile_v1.py 

Results (0.30s):

       4 passed
root@Gavin:~/code/chapter1-10#
```

**请注意：**

- `--dist=loadfile` 会尽可能地将同一个文件的测试用例保持在同一个进程中执行，但并不对跨文件的测试用例依赖提供保护。
- 如果有文件级别的固定或会话级固定，它们将分别在每个worker中运行，这可能导致额外的设置和清理操作。
- 确保你的测试文件之间确实彼此独立，即一个文件中的测试不会依赖或影响另一个文件中的测试状态，除非你有相应的固定来重置这些状态。

#### 10.5.3.3.6 注意事项

- **测试隔离**：当使用 `pytest-xdist` 时，需要确保测试用例能独立运行，不要保留任何共享状态或数据。
- **资源竞争**：并行测试可能会导致资源（如数据库或文件系统）出现争抢情况，需确保测试优雅地处理这些情况。
- **日志和输出**：并行运行时的日志会混合在一起，这可能会使得问题排查变得复杂。
- **调试**：常规调试技术（如使用断点）可能在并行环境下不起作用。

#### 10.5.3.3.7 Q/A？

**Q：如何让scope=session的fixture在test session中仅仅执行一次？**

`pytest-xdist`是让每个worker进程执行属于自己的测试用例集下的所有测试用例

这意味着在不同进程中，不同的测试用例可能会调用同一个scope范围级别较高（例如session）的fixture，该fixture则会被执行多次，这不符合scope=session的预期。

如何解决？

**A：且看下面示例**

在当前目录下`conftest.py`文件中存在`scope="session"`的`fixture`，内容如下：

```python
# content of conftest.py
import os
import pytest

output_file = "xdist_session_scope_test.txt"
if os.path.exists(output_file):
    os.remove(output_file)

@pytest.fixture(scope="session")
def session_fixture():
    print("\nSetting up the session fixture")
    os.system(f"echo 1 >> {output_file}")
    yield
    print("\nTearing down the session fixture")
    os.system(f"echo 2 >> {output_file}")
```

存在如下测试示例代码：

```python
# content of test_pytest_xdist_session_cases.py
def test_example1(session_fixture):
    assert True

def test_example2(session_fixture):
    assert True

def test_example3(session_fixture):
    assert True
```

在并行执行`test_pytest_xdist_session_cases.py`中用例时，观察到：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v -n 4 test_pytest_xdist_session_cases.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
4 workers [3 items]     collecting ... 
scheduling tests via LoadScheduling

 chapter1-10/test_pytest_xdist_session_cases.py::test_example2 ✓          33% ███▍      
[gw1] PASSED test_pytest_xdist_session_cases.py 
 chapter1-10/test_pytest_xdist_session_cases.py::test_example1 ✓          67% ██████▋   
[gw0] PASSED test_pytest_xdist_session_cases.py 
 chapter1-10/test_pytest_xdist_session_cases.py::test_example3 ✓         100% ██████████
[gw2] PASSED test_pytest_xdist_session_cases.py 

Results (0.40s):

       3 passed
root@Gavin:~/code/chapter1-10# cat xdist_session_scope_test.txt 
1
1
1
2
2
2
root@Gavin:~/code/chapter1-10#
```

4个并发进程执行了三个测试用例，虽然`fixture`的`scope="session"`，但是`session_fixture`被调用了三次，而我们实际期望的是在`scope="session"`的`fixture`只被调用一次，为什么？

在标准的 `pytest` 中，一个 `scope=session` 的 `fixture` 在整个测试会话中只会被调用一次，无论有多少测试用例或测试模块，这个 `fixture` 都只会在会话开始时设置一次，然后在会话结束时终止。然而，当使用 `pytest-xdist` 插件进行多进程执行时，情况就有所不同。每个进程会创建它自己的测试会话，在这种情况下，一个 `scope=session` 的 `fixture` 实际上对于每个进程中的会话来说都是唯一的。所以，尽管 fixture 的作用域是 `session`，但因为存在多个进程（与之相对应的是多个独立的测试会话），每个进程中的会话将分别调用一次这个 `fixture`。

这意味着，如果你有四个进程在运行测试，每个进程都会创建自己的会话，并分别实例化一次 `scope=session` 的 `fixture`，总共执行四次（前提条件是进程有被分配到具体测试用例，比如上面的测试用例文件中只有3个测试用例，产生4个进程来执行，有一个进程未被分配到测试用例，故而不会实例化一次 `scope=session` 的 `fixture`）。每个会话中的测试用例将使用它们所在进程中的 `fixture` 实例。

如果你的测试环境或 fixture 有全局的数据存储需求或者需要跨进程同步，这时候就需要格外小心，因为每个进程都会有自己的环境实例。为了避免数据竞争或状态污染的问题，你可能需要采用额外的同步机制，或者重构测试以确保它们能在多进程环境下正确执行。

虽然`pytest-xdist`没有内置的支持来确保会话范围的夹具(fixture)仅执行一次，但是可以通过使用锁定文件进行进程间通信来实现，比如下面的示例只需要执行一次login（因为它是只需要执行一次来定义配置选项）：

* 当第一次请求这个fixture时，则会利用`FileLock`仅产生一次`fixture`数据。
* 当其他进程再次请求这个fixture时，则会从文件中读取数据。

需安装`filelock`库：

```shell
pip install filelock
```

修改`conftest.py`文件，内容如下：

```python
import os
import pytest
from filelock import FileLock

output_file = "xdist_session_scope_test.txt"
lock_file = f"{output_file}.lock"

if os.path.exists(output_file):
    os.remove(output_file)

# 获取预期的worker数量
def get_expected_num_workers(config):
    # 如果使用了pytest-xdist进行分布式测试
    if hasattr(config, 'slaveinput'):
        # sum()返回config.slaveinput的键数量，键名看起来像 gw0, gw1, ...
        return len(config.slaveinput.keys())
    elif hasattr(config, 'workerinput'):
        # 处理pytest-xdist 2.0及以上版本
        print(f"{config.workerinput.keys()}")
        return config.workerinput['workercount']
    elif hasattr(config.option, 'numprocesses'):
        # 如果存在numprocesses选项则直接返回其值
        num = config.option.numprocesses
        if num == "auto":
            # 如果numprocesses被设置为"auto"，xdist将自动选择进程数量
            # 在这种情况下，不能确定确切的数量，因此我们返回None
            # 而不是具体的数字，调用者需要处理这种情况
            return None
        return int(num)
    else:
        # 单进程测试
        return 1


@pytest.fixture(scope="session")
def session_fixture(request):
    worker_id = getattr(request.config, 'workerinput', {}).get('workerid')
    is_master = not worker_id or worker_id == "gw0"

    # Setup部分
    if is_master:
        # 主节点初始化资源
        with FileLock(lock_file):
            if not os.path.exists(output_file):
                # 主节点会创建文件并初始化
                print("\nSetting up the session fixture")
                with open(output_file, "w") as f:
                    f.write("Setup complete.\n")

    yield  # 从这里开始，将会执行你的测试用例

    # Teardown部分
    with FileLock(lock_file):
        with open(output_file, "a") as f:
            f.write("Teardown call.\n")

        with open(output_file, "r") as f:
            lines = f.readlines()

        teardown_calls = [line for line in lines if "Teardown call." in line]
        num_teardown_calls = len(teardown_calls)
        expected_num_workers = get_expected_num_workers(request.config)

        # 当expected_num_workers为None时，暂时无法执行实际的worker数量检查
        if expected_num_workers is None:
            return  # 或者使用其他的方式来处理这种情况

        # 仅在该worker是最后一个完成的时候执行teardown
        if num_teardown_calls == expected_num_workers:
            print("\nTearing down the session fixture")
            # 在此处执行Teardown操作
            with open(output_file, "a") as f:
                f.write("Teardown complete.\n")
```

再来执行上述测试文件`test_pytest_xdist_session_cases.py`：

```shell
root@Gavin:~/code/chapter1-10# export PYTEST_XDIST_WORKER_COUNT=2
root@Gavin:~/code/chapter1-10# pytest -s -v -n ${PYTEST_XDIST_WORKER_COUNT} test_pytest_xdist_session_cases.py
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
2 workers [3 items]     collecting ... 
scheduling tests via LoadScheduling

 chapter1-10/test_pytest_xdist_session_cases.py::test_example2 ✓          33% ███▍      
[gw1] PASSED test_pytest_xdist_session_cases.py 
 chapter1-10/test_pytest_xdist_session_cases.py::test_example1 ✓          67% ██████▋   
[gw0] PASSED test_pytest_xdist_session_cases.py 
 chapter1-10/test_pytest_xdist_session_cases.py::test_example3 ✓         100% ██████████
[gw0] PASSED test_pytest_xdist_session_cases.py 

Results (0.29s):

       3 passed
root@Gavin:~/code/chapter1-10# cat xdist_session_scope_test.txt
Setup complete.
Teardown call.
Teardown call.
Teardown complete.
root@Gavin:~/code/chapter1-10#
```

这里通过指定环境变量`PYTEST_XDIST_WORKER_COUNT`的方式来并行执行用例与获取此环境变量值判断是否是最后一个进程再执行用例，美中不足是当`PYTEST_XDIST_WORKER_COUNT`设置过大时没有执行`teardown`动作。

再举一个例子，在并发运行的测试用例中，使用同一个login session，参考示例如下：

```python
# content of conftest.py
import pytest
from filelock import FileLock


@pytest.fixture(scope="session")
def login():
    with FileLock("session.lock"):
        # 下面请根据自己项目需要补充代码或相关session函数的调用
        account = "admin"
        password = "1"
        session = ""

        # 接口自动化
        # 发起一个登录请求，将session返回都可以这样写

    yield session
```

上面只是设计思路，借助`FileLock`完成整个并发运行过程中唯一一次的前置动作，请根据实际项目需要补充自己的代码。

### 10.5.3.4 随机运行

`pytest-random-order` 插件允许以随机顺序执行测试用例，这个功能对于揭示测试之间的隐性依赖关系以及开发团队过分依赖测试执行顺序的情况非常有用。

#### 10.5.3.4.1 安装 pytest-random-order

使用 `pip` 安装 `pytest-random-order`：

```sh
pip install pytest-random-order
```

#### 10.5.3.4.2 主要特性

- **随机运行测试**：在每次测试会话中，测试用例将以随机顺序执行。
- **可重复的随机顺序**：可以通过提供一个种子值(`--random-order-seed`)来使随机执行的顺序可重复。
- **控制度**：可以选择随机执行整个测试会话的所有测试，或者仅随机执行某个模块或类中的测试。

#### 10.5.3.4.3 使用场景

- **发现测试间依赖**：识别可能由于测试执行顺序导致的隐藏问题，如状态泄露、共享资源冲突等。
- **测试弹性**：验证测试套件是否健壮，即无视测试顺序的不同都可以通过所有测试。
- **持续集成**：在CI流程中使用，确保测试独立性，并且尽可能揭露隐性问题。

#### 10.5.3.4.4 代码示例和注解

在 `pytest` 测试会话中，使用 `--random-order` 参数来随机运行测试：

```sh
pytest --random-order
```

如果希望随机排序但要保持顺序可重复性，可以指定一个种子值：

```sh
pytest --random-order-seed=<seed>
```

比如：

```shell
pytest --random-order --random-order-seed=12345
```

在这个例子中，`12345` 是一个种子值。此后每次使用同一个种子值运行 `pytest` 时，测试的随机顺序将会保持一致，只要测试用例集没有变化。

通常，在测试运行结束时，如果你启用了随机顺序插件，pytest 会打印用于该次测试顺序的种子。例如：

```shell
Using --random-order-seed=12345
```

这样当你想要复现测试用例的随机顺序时，就可以通过提供之前生成的种子来执行。这确保了你能够重现同样的顺序，从而方便调试和解决可能出现的顺序依赖问题。

对于希望以固定顺序进行的特定测试，可以使用 `@pytest.mark.order` 标记（需要 `pytest-order` 或相似插件）：

```python
# content of test_pytest_random_order.py
import pytest

@pytest.mark.order(1)
def test_should_run_first():
    # 这个测试将总是首先执行
    pass

def test_random1():
    pass

def test_random2():
    pass

def test_random3():
    pass

def test_random4():
    pass
```

运行结果参考如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v --random-order-seed=3 test_pytest_random_order.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
Using --random-order-bucket=module
Using --random-order-seed=3

metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'random-order': '1.1.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'repeat': '0.9.3', 'ordering': '0.6'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, random-order-1.1.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, repeat-0.9.3, ordering-0.6
collecting ... /root/code/chapter1-10/test_pytest_random_order.py:3: PytestUnknownMarkWarning: Unknown pytest.mark.order - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
  @pytest.mark.order(1)
collected 5 items

test_pytest_random_order.py::test_random1 PASSED
test_pytest_random_order.py::test_random1 PASSED
_________________________________________________________________________________ 1 of 5 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun __________________________________________________________________________________

test_pytest_random_order.py::test_random1 PASSED
test_pytest_random_order.py::test_should_run_first PASSED
test_pytest_random_order.py::test_should_run_first PASSED
_________________________________________________________________________________ 2 of 5 completed, 2 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun __________________________________________________________________________________

test_pytest_random_order.py::test_should_run_first PASSED
test_pytest_random_order.py::test_random4 PASSED
test_pytest_random_order.py::test_random4 PASSED
_________________________________________________________________________________ 3 of 5 completed, 3 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun __________________________________________________________________________________

test_pytest_random_order.py::test_random4 PASSED
test_pytest_random_order.py::test_random2 PASSED
test_pytest_random_order.py::test_random2 PASSED
_________________________________________________________________________________ 4 of 5 completed, 4 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun __________________________________________________________________________________

test_pytest_random_order.py::test_random2 PASSED
test_pytest_random_order.py::test_random3 PASSED
test_pytest_random_order.py::test_random3 PASSED
_________________________________________________________________________________ 5 of 5 completed, 5 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun __________________________________________________________________________________

test_pytest_random_order.py::test_random3 PASSED

=============================== 15 passed in 0.01s =============================
root@Gavin:~/code/chapter1-10#
```

如果希望分组测试用例，并随后随机化各组内的测试用例顺序，可以使用：

```shell
pytest --random-order --random-order-bucket
```

`--random-order-bucket`参数接受下面几种不同的值：

- `module`：按照模块随机化测试用例顺序。同一个模块的测试用例将首先被收集，然后作为一个整体随机化它们的顺序。
- `class`：按照类随机化测试用例顺序。同一个类的测试用例将首先被收集，然后作为一个整体随机化它们的顺序。
- `package`：按照包（即目录结构）随机化测试用例顺序。同一个包或子包内的测试用例将首先被收集，然后作为一个整体随机化它们的顺序。
- `global`：测试全部随机化。不做任何分组，所有的测试用例被汇集到一起并随机排序。
- `none`：不对测试用例执行顺序做任何干预，即保持 `pytest` 默认的顺序。

例如，如果你想要按照模块来随机化测试用例的执行顺序，你可以在运行 Pytest 时采用如下命令：

```shell
pytest --random-order --random-order-bucket=module
```

另一方面，如果你想要全局随机化测试用例（不考虑模块、类或包的边界），可以使用：

```shell
pytest --random-order --random-order-bucket=global
```

#### 10.5.3.4.5 注意事项

- **独立性**：确保你的测试没有依赖于特定的执行顺序，可以独立运行。
- **环境清理**：在测试结束后对环境进行彻底清理，以避免状态污染后续的测试。
- **数据隔离**：避免共享数据库或公共文件等资源，这些资源可能不安全地在测试间共享。
- **重现问题**：如果发现测试失败，需要记下当前的种子值，以便能在随后的调试过程中使用相同的顺序来重现问题。

`pytest-random-order` 是一个有价值的工具，对于提高测试的稳健性和可靠性有潜在的好处。然而，它可能暴露那些在某些顺序条件下不易察觉的问题，因此在集成到持续集成流程之前必须谨慎对待。

### 10.5.3.5 用例依赖

`pytest-dependency` 插件增加了对测试用例依赖管理的支持。通过这个插件，你可以指定某些测试是依赖于其他测试结果的，从而控制测试用例的执行顺序。

#### 10.5.3.5.1 安装 pytest-dependency

使用 `pip` 安装 `pytest-dependency`：

```sh
pip install pytest-dependency
```

#### 10.5.3.5.2 主要特性

- **声明依赖关系**：允许你声明测试用例之间的依赖关系。
- **跳过依赖未满足的测试**：当依赖的测试失败时，依赖于它的测试将被自动跳过。
- **灵活的使用**：支持在函数、类、模块级别上声明和使用依赖。
- **支持跨模块依赖**：允许在不同模块间声明依赖关系。

#### 10.5.3.5.3 使用场景

- **复杂的测试流程**：当不同的测试用例有明确的执行先后顺序时，比如初始化测试，准备测试数据等。
- **集成测试**：可能需要在一个整合环境中先运行一些设置或配置的测试。
- **资源生成和清理**：比如当一个测试生成了数据库中的数据，之后的测试将使用到这些数据。

#### 10.5.3.5.4 代码示例和注解

假设有一个测试文件 `test_dependency_v1.py`，包含以下内容：

```python
# content of test_dependency_v1.py
import pytest

# 声明一个"登陆"的测试
@pytest.mark.dependency()
def test_login():
    pass  # 执行登录逻辑，并断言登录成功
  
# 声明一个依赖于"登录"的测试
@pytest.mark.dependency(depends=["test_login"])
def test_dashboard():
    pass  # 执行用户已登录后的仪表盘显示逻辑，然后断言显示正确
```

在这种情况下，`test_dashboard` 测试用例依赖于 `test_login` 测试用例的执行和结果。如果 `test_login` 失败，`test_dashboard` 将自动被跳过。

也可以在类和模块级别声明依赖：

```python
# content of test_dependency_v2.py
import pytest

@pytest.mark.dependency(name="init")
def test_initialize():
    pass  # 某些初始化操作
  
@pytest.mark.dependency(depends=["init"])
class DashboardTests:
    def test_page1(self):
        pass
      
    def test_page2(self):
        pass
```

如果 `test_initialize` 测试失败，所有 `DashboardTests` 类中的测试都将被跳过。

#### 10.5.3.5.5 注意事项

- **明确标记依赖**：明确地标记那些应该被跳过的测试，以及它们依赖的先前测试。
- **避免过多依赖**：过分依赖可能会隐藏潜在的问题，测试用例应当尽量独立。
- **关注被跳过的测试**：跳过的测试不应当永久存在，需要持续地审查和维护。
- **依赖管理**：确保依赖关系在代码维护过程中保持正确和最新。

`pytest-dependency` 可以帮助创建更复杂的测试执行流程，同时保持测试逻辑的清晰，但它的使用应当恰当和克制。过多地依赖某些测试的成功，可能最终导致真正的问题被混淆或忽略。因此，当可能的时候，最好是设计出互相独立的测试用例。



### 10.5.3.6 即时显示失败和错误

`pytest-instafail` 插件能够在测试运行时立即显示失败的测试而不是等待整个测试会话完成。这对于长时间运行的测试会话特别有用，因为你能更快地获得失败的反馈，并开始针对性地解决问题。

#### 10.5.3.6.1 安装 pytest-instafail

通过 `pip` 安装 `pytest-instafail`：

```sh
pip install pytest-instafail
```

#### 10.5.3.6.2 主要特性

- **实时反馈**：测试失败时会立即显示输出，而不是在全部测试执行完毕后统一显示。
- **节省时间**：开发者可以在等待全部测试执行完毕前就开始分析和修复出现的问题。
- **易于集成**：只需通过简单的命令行参数启用，无需对已有的测试用例进行任何修改。

#### 10.5.3.6.3 使用场景

- **开发过程中**：在开发过程中快速发现测试失败，以便能够快速修复，减少等待时间。
- **持续集成**：在 CI 系统中使用，可以更早地在日志中看到失败的测试，而不必等到整个测试流程完成。
- **集成测试或系统测试**：这些测试往往运行时间较长，有时候甚至需要数小时，实时反馈能够显著提高效率。

#### 10.5.3.6.4 代码示例和注解

安装 `pytest-instafail` 后，你可以在命令行中使用 `--instafail` 参数来启动它：

```sh
pytest --instafail
```

当你运行此命令时，每当单个测试失败，你会立即在控制台上看到输出，包括失败的断言和堆栈跟踪。

不需要在你的测试代码中添加特定的装饰器或标记，`pytest-instafail` 将自动应用于所有测试。

#### 10.5.3.6.5 注意事项

- **输出管理**：如果测试用例很多且失败率较高，实时输出可能导致大量的日志信息，这有时会使得控制台输出看起来比较混乱。
- **日志记录**：在 CI 工具中使用时，需要确保实时输出不会干扰或覆盖测试结束后的完整报告。
- **与其他插件的潜在冲突**：一些修改测试输出行为的插件可能与 `pytest-instafail` 冲突。

`pytest-instafail` 是提高实时测试反馈效率的好工具，它可以帮助你尽可能快地发现问题，并开始进行故障排除。然而，对于某些情况，可能需要调整 CI 系统的日志收集配置，以确保失败的测试输出不会被误解或忽略。

### 10.5.3.7 多重断言 pytest-assume

`pytest-assume` 插件允许在单个测试用例中进行多个断言，而且不会在第一个失败的断言处停止运行后续的代码。这就意味着，即使中间的某个断言失败，接下来的断言也会执行，允许在一个测试中集中报告多个断言的结果。

#### 10.5.3.7.1 安装 pytest-assume

通过pip安装`pytest-assume`：

```sh
pip install pytest-assume
```

如果安装后运行用例提示：

```shell
AttributeError: module pytest has no attribute assume
```

请先卸载：

```shell
pip uninstall pytest-assume
```

再执行如下命令进行安装：

```shell
pip3 install pytest-assume -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
```

#### 10.5.3.7.2 主要特性

- **多重断言**: 在一个测试用例中执行多个断言，收集所有的失败情况，而不是在第一个失败处停止。
- **测试效率**: 提高测试效率，提供比常规断言更全面的失败反馈，减少反复运行测试的需求。
- **易于使用**: 使用`pytest.assume()`语法很自然地过渡到这种多断言风格。

#### 10.5.3.7.3 使用场景

- **数据验证**：当你需要在一个测试中对一个对象的多个属性进行验证时，这允许你即使有些验证失败也能继续进行其它验证。
- **批量测试**：在处理批量生成数据的测试并希望得到一个汇总报告时，`pytest-assume` 非常有用。
- **前端测试**: 在进行 UI 自动化测试时，你可能希望检查多个页面元素而不管某个元素的断言失败。

#### 10.5.3.7.4 代码示例与注解

在下面的示例中，我们使用`pytest.assume()`来进行多个断言：

```python
# content of test_assume.py
import pytest

def test_multiple_assumptions():
    pytest.assume(1 == 2, "One is not equal to Two")
    pytest.assume(True, "This will pass")
    pytest.assume(False, "This will fail")
    print("After all assumptions")
```

在这个测试用例中，即使第一个断言失败（`1 == 2`显然不成立），后续的断言也会执行。在运行后，所有的断言情况都会报告出来，而且还会有最后的打印输出"After all assumptions"。

#### 10.5.3.7.5 注意事项

- **最后测试输出**: 尽管测试中的断言可能失败，测试函数还是会执行到最后。因此，你需要检查你的测试输出，以了解所有断言的结果。
- **用例可读性**: 依然要考虑到测试用例的可读性，不要因为可以做到多重断言就在一个测试中塞入过多逻辑。
- **资源清理**: 确保不依赖断言来释放资源或执行必要的清理步骤，要使用fixture或try/finally等机制来确保资源被适当处理。

`pytest-assume` 插件提供了测试中更灵活的断言机制，可能会特别有助于复杂测试场景中的问题定位和修复。

### 10.5.3.8 多重断言 pytest-check

`pytest-check` 插件允许开发者在单个测试用例中累积多个失败检查，而不会在第一个断言失败时立即终止测试。这适用于想要在一个测试中执行多个断言，然后一起查看所有失败断言的场景。

#### 10.5.3.8.1 主要特性

- **软断言**：提供了“软断言”(`soft assertions`)的功能，它们不会在断言失败后立刻停止测试，允许后续的代码继续执行。
- **累积错误**：测试的所有错误都会被记录下来，并在测试执行完成后一起报告。
- **易于使用**：简单的断言风格，可以在不改变现有编码风格的情况下使用。

#### 10.5.3.8.2 安装 pytest-check

使用 `pip` 安装 `pytest-check`：

```sh
pip install pytest-check
```

#### 10.5.3.8.3 使用场景

- **数据驱动测试**：当遍历参数列表执行相同的断言集合时，可以用 `pytest-check` 来查看哪个参数集合失败。
- **复杂断言逻辑**：在需要进行一组断言来验证复杂逻辑时，允许测试继续运行以收集尽可能多的失败信息。
- **整体测试报告**：希望最后获得关于所有失败断言的综合信息，而不是只得到第一个失败点的信息。

#### 10.5.3.8.4 代码示例与注解

更改一个普通的 `assert` 语句，使用 `pytest-check` 提供的断言方法：

```python
# content of test_check.py
import pytest_check as check

def test_check_many_conditions():
    check.equal(1, 1)  # 判断两个值是否相等
    check.less(2, 1)  # 判断第一个值是否小于第二个值
    check.greater(2, 1)  # 判断第一个值是否大于第二个值
    print("End to check.") # 打印这句话，用于确认第二个断言失败后是否有执行到这里
```

在上面的示例中，如果任意断言失败，测试不会立即停止("End to check."会被打印出来)。`pytest-check` 会记录下所有的失败点，并在测试结束时一次性报告。

#### 10.5.3.8.5 注意事项

- **错误收集**：`pytest-check` 收集的失败会在测试用例的最后一起打印出来。务必检查完整的测试输出，以了解所有失败的断言。
- **复杂测试逻辑分离**：尽管 `pytest-check` 允许多个断言，在设计测试用例时仍应尽量保持单个测试用例的简单和清晰。
- **与pytest断言兼容性**：虽然 `pytest-check` 提供软断言，但它并不阻止你在需要时使用传统的断言语句，两者可以混用。

使用 `pytest-check` 插件可以在一个测试过程中提供对多个问题的全面视图，与传统的断言方法相比，它允许更灵活的错误处理和报告。这在执行多步验证的端到端测试或复杂集成测试中尤其有价值。

### 10.5.3.9 pytest-lazy-fixture

`pytest-lazy-fixture` 是一个用于延迟加载`pytest fixture`的插件，它使得在使用 `pytest` 编写测试时可以延迟 `fixture` 的创建直至实际需要时(如仅在需要时才加载fixture，而不是在每个测试用例之前都加载)。这在一些特定测试场景下非常有用，尤其是当你需要在测试参数化（`parametrization`）中使用 `fixtures`，但不想在测试参数化声明时立即实例化它们。

#### 10.5.3.9.1 安装 pytest-lazy-fixture


你可以使用 pip 来安装这个插件：

```shell
pip install pytest-lazy-fixture
```

#### 10.5.3.9.2 主要特性

* 提高测试执行效率：通过延迟加载`fixture`，可以减少不必要的`fixture`加载操作，从而提高测试的执行速度。
* 灵活的条件加载：可以根据不同的条件来决定是否加载`fixture`，从而更好地控制测试用例的行为。
* 无缝集成：`pytest-lazy-fixture`与`pytest`框架无缝集成，使用起来非常方便。
* 兼容性：`pytest-lazy-fixture`与其他`pytest`插件和功能兼容，可以与其他插件一起使用，以满足特定的测试需求。


#### 10.5.3.9.3 使用场景

* **优化测试性能**：对于一些创建代价较高的`fixture`，使用`pytest-lazy-fixture`可以在不影响测试的情况下，仅在必要时进行创建。
* **处理复杂的fixture依赖**：在`fixture`之间有复杂的依赖关系时，可以根据测试用例的需要动态决定加载哪个`fixture`。
* **参数化测试**：在使用 `@pytest.mark.parametrize` 时，能够更灵活地处理`fixture`作为参数。
  当你希望使用 `fixtures` 作为参数化测试的一部分，但又不想这些 fixtures 在所有测试用例中都被加载时。
  当你使用参数化让测试用例遍历不同的 `fixture` 组合，但是你希望避免不使用的 `fixture` 被初始化。
* **条件性 fixture 使用**：当某些 `fixtures` 的创建过程开销较大，仅在某些特定的测试用例中需要使用时。


#### 10.5.3.9.4 代码示例与注解


假设有两个`fixture`，但只希望根据测试用例的不同选择性地使用它们：

```python
# content of test_lazy_fixture_v1.py
import pytest

@pytest.fixture
def expensive_fixture():
    print("Creating expensive fixture")
    return "Expensive Data"

@pytest.fixture
def another_fixture():
    print("Creating another fixture")
    return "Another Data"

@pytest.mark.parametrize("my_fixture", [
    pytest.lazy_fixture('expensive_fixture'),
    pytest.lazy_fixture('another_fixture')
])
def test_example(my_fixture):
    assert my_fixture in ["Expensive Data", "Another Data"]
```

在这个示例中，`test_example` 被参数化以使用两个不同的fixture。通过 `pytest.lazy_fixture`，这些`fixture`会在测试函数实际调用时才初始化，从而实现延迟加载，运行效果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_lazy_fixture_v1.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 2 items

test_lazy_fixture_v1.py::test_example[expensive_fixture] Creating expensive fixture
PASSED
test_lazy_fixture_v1.py::test_example[another_fixture] Creating another fixture
PASSED

================================ 2 passed in 0.06s ============================
root@Gavin:~/code/chapter1-10#
```

再比如：假设我们有以下两个 `fixtures`：

```python
# content of conftest.py
import pytest

@pytest.fixture
def expensive_fixture():
    print("Setting up an expensive fixture")
    yield "data from expensive setup"
    print("Tearing down an expensive fixture")

@pytest.fixture(params=[1, 2])
def number_fixture(request):
    return request.param
```

现在，假设我们想要在单个测试函数中使用 `expensive_fixture`，但仅当 `number_fixture` 的状态为特定值时。

我们可以用 `pytest.mark.parametrize` 和 `pytest-lazy-fixture` 来实现：

```python
# content of test_lazy_fixture_v2.py
import pytest
from pytest_lazyfixture import lazy_fixture

@pytest.mark.parametrize("number,my_fixture", [
    (1, pytest.lazy_fixture('expensive_fixture')), 
    # expensive_fixture 只会在 number_fixture 为 1 时加载
    (2, None),
    # expensive_fixture 不会加载
])
def test_with_conditions(number, my_fixture):
    if number == 1:
        assert my_fixture == "data from expensive setup"
    else:
        assert my_fixture is None
```

在这个例子中，当 `number_fixture` 的值为 1 时，`expensive_fixture` 将被初始化，如果它的值为 2，`expensive_fixture` 则不会被创建，运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_lazy_fixture_v2.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 2 items

test_lazy_fixture_v2.py::test_with_conditions[1-expensive_fixture] Setting up an expensive fixture
PASSEDTearing down an expensive fixture

test_lazy_fixture_v2.py::test_with_conditions[2-None] PASSED

============================== 2 passed in 0.06s ==============================
root@Gavin:~/code/chapter1-10#
```


#### 10.5.3.9.5 注意事项

* **团队协作**：确定你的团队了解和同意使用 `pytest-lazy-fixture`，因为它增加了测试码的复杂性。
* **调试困难**：由于fixture的延迟加载，可能会使得问题的调试变得稍微复杂。
* **过度使用避免**：虽然延迟加载fixture很有用，但不应过度使用，以免影响代码的可读性和维护性。
* **注解加载条件**：确保理解如何和何时 fixtures 被初始化，避免在测试中引入隐藏的副作用，增加详细注解方便团队成员理解。

## 10.5.4 CI/CD相关插件

### 10.5.4.1 测试覆盖率 pytest-cov

`pytest-cov` 插件用于测量代码的测试覆盖率，这个插件实际上是 `coverage.py` 的一个`pytest`插件版，可以在测试运行时收集覆盖率数据。它是测试质量保证和持续集成流程中必不可少的工具。

#### 10.5.4.1 安装 pytest-cov

使用 `pip` 安装 `pytest-cov`：

```sh
pip install pytest-cov
```

#### 10.5.4.2 主要特性

- **覆盖率报告**：生成覆盖率数据报告，包括那些未被测试覆盖到的代码行。
- **多种报告格式**：支持多种输出格式，包括标准输出、HTML、XML、和注解源代码的报告。
- **并行测试支持**：与 `pytest-xdist` 插件结合使用时，支持在并行测试环境下聚合覆盖率数据。
- **易于集成**：易于与其他 `pytest` 插件和持续集成服务集成。

#### 10.5.4.3 使用场景

- **单元测试覆盖率**：在单元测试期间收集覆盖率数据以确保代码有被充分测试。
- **集成/系统测试覆盖率**：在进行更高级别的测试时测量覆盖率，以评估测试的有效性。
- **持续集成（CI）系统中**：持续集成中生成覆盖率报告，常用于代码质量评估和审查。

#### 10.5.4.4 示例和注解

运行 `pytest` 时使用 `--cov` 参数来测量覆盖率：

```sh
pytest --cov=my_package
```

上面的命令会运行测试并且收集名为 `my_package` 的包的覆盖率数据。

如果你还想要生成一个HTML覆盖率报告，可以添加 `--cov-report` 参数：

```sh
pytest --cov=my_package --cov-report html
```

该命令会生成一个 `htmlcov` 目录，其中包含了覆盖率报告的HTML页面。当然你也可以指定覆盖率报告目录：

```shell
pytest --cov=my_package --cov-report html:../report/coverage
```

如上命令会在当前目录的上一级目录`report`下产生`coverage`目录，目录下存放相关`html`文件，打开`index.html`文件，展示被测目录下代码覆盖率，参考如下：

<img class="shadow" src="/img/in-post/pytes-cov-html.png" width="800">

在测试代码中，你无需为 `pytest-cov` 做任何特殊修改。使用 `pytest-cov` 的关键之处在于运行 `pytest` 时的命令行选项配置。

#### 10.5.4.5 注意事项

- **测试真实性**：高覆盖率并不一定代表高质量的测试。覆盖率只能说明代码运行过，不能保证测试用例具有好的断言或是能够捕获重要的错误。
- **覆盖率目标**：应该设定合理的覆盖率目标，而非一味追求 100% 的覆盖率。
- **覆盖率的误解**：有时你可能需要使用 `.coveragerc` 文件来排除一些不应该计入覆盖率的代码，比如测试代码本身或是一些初始化脚本。
- **资源消耗**：收集覆盖率数据可能会增加测试运行的时间。

`pytest-cov` 是一个非常有用的工具，能够帮助开发者了解哪些代码没有被测试覆盖，并在开发中提供指导。它的正确使用可以极大地提高软件开发的质量和可靠性。

### 10.5.4.2 测试代码质量检查 pytest-pylint

`pytest-pylint` 是一个用于集成 `pylint` 静态代码分析工具到 `pytest` 测试框架中的插件。通过这个插件，你可以在运行测试时同时运行 `pylint` 检查，确保代码质量符合标准。

#### 10.5.4.2.1 安装 pytest-pylint

使用 `pip` 安装 `pytest-pylint`:

```sh
pip install pytest-pylint
```

#### 10.5.4.2.2 主要特性

- **自动化代码检查**: 将 `pylint` 静态代码分析集成到测试流程中，没有必要单独运行 `pylint`。
- **可配置性**: 支持自定义 `pylint` 配置文件，可以按照项目的具体需求配置规则。
- **易于使用**: 通过简单的命令行选项集成到 `pytest` 中，并在测试报告中直接显示结果。

#### 10.5.4.2.3 使用场景

- **持续集成(CI)流程**: 在 CI 中加入静态代码分析步骤，以确保提交的代码符合代码质量标准。
- **代码审查**: 在代码审查前自动检查代码质量问题，提高审查效率。
- **开发阶段**: 在本地开发阶段作为测试的一部分自动运行，协助发现潜在编程错误。

#### 10.5.4.2.4 示例和注解

在你的 `pytest` 会话中，使用 `--pylint` 参数来启用 `pytest-pylint`：

```sh
pytest --pylint
```

这样做将会在运行测试的同时运行 `pylint`，检查你的代码是否按照 `pylint` 的标准进行编写。

如果你希望将 `pylint` 检查限制在特定的文件或者模块上：

```sh
pytest --pylint -m pylint <file_or_module_name>
```

这将只在指定的文件或模块上运行 `pylint` 检查。

#### 10.5.4.2.5 注意事项

- **配置管理**: 需要正确配置 `.pylintrc` 文件以符合项目的具体规范。如果没有配置文件，`pylint` 将使用默认配置。
- **性能**: 静态代码分析可能会延长测试的运行时间。
- **错误正面化**: 使用 `pytest-pylint` 仅报告 `pylint` 发现的问题，它不会修复它们。需要开发者根据报告解决问题。
- **版本兼容性**: 需要确保 `pytest-pylint` 版本与项目中使用的 `pylint` 版本兼容。

使用 `pytest-pylint` 能够提高代码的质量和一致性，并且预防未来的问题和错误。然而，一个好的实践是将它与其他形式的测试（如单元测试、集成测试）结合使用，并非依赖单一的工具。

### 10.5.4.3 测试代码质量检查 pytest-flake8

`pytest-flake8` 是一个整合了 `flake8` 代码检查工具到 `pytest` 测试框架的插件。`flake8` 是一个流行的代码检查工具，它将 `pyflakes`、`pep8`、`mccabe` 等工具的功能合并到了一个工具中，可以检测代码中的错误、风格问题和太复杂的代码设计。

#### 10.5.4.3.1 安装 pytest-flake8

通过 `pip` 安装 `pytest-flake8`：

```sh
pip install pytest-flake8
```

#### 10.5.4.3.2 主要特性

- **集成代码检查**: 将 `flake8` 的代码检查集成到 `pytest` 测试流程中，不需要进行单独的命令行操作。
- **个性化配置**: 支持配置文件（比如 `setup.cfg` 或 `.flake8`），允许自定义检查规则和忽略某些错误。
- **方便的CLI选项**: 支持命令行参数来启用或配置 `flake8` 插件的行为。
- **自动PEP 8检查**：自动检查测试代码是否符合PEP 8风格规范。
- **功能扩展**：除了PEP 8规则，`flake8` 还提供了对`Pyflakes`和`McCabe`脚本的检查。
- **和`pytest`无缝集成**：像普通的`pytest`用例一样运行风格检查。

#### 10.5.4.3.3 使用场景

- **持续集成**: 在持续集成(CI)流程中，确保每次提交的代码都符合 `flake8` 的质量标准。
- **代码审查**: 运行 `pytest` 同时进行代码风格和质量检查，减少代码审查压力。
- **本地开发**: 开发者可以在每次测试时实时检查代码，更早地发现并修正问题。

#### 10.5.4.3.4 示例与注解

在你的 `pytest` 测试会话中，添加 `--flake8` 参数来启用 `pytest-flake8`：

```sh
pytest --flake8
```

此命令将会在运行测试的同时执行 `flake8` 代码检查，并将风格和质量问题作为测试失败的原因之一。

如果你想要限制 `flake8` 检查的范围，只需要把插件添加到你的 `pytest` 配置文件中（这些配置项也可以放在 `setup.cfg`、`tox.ini` 或 `.flake8` 文件中）：

```ini
[pytest]
# 添加 flake8 的配置
flake8-ignore = E501 E303
flake8-max-line-length = 120
exclude = tests/*
max-complexity = 10
```

#### 10.5.4.3.5 注意事项

- **选取感兴趣的错误**: 根据项目的需要，可以选择忽略某些不太重要的错误。这需要适当配置 `flake8`。
- **检查与测试平衡**: 在某些情况下，`flake8` 的代码检查可能会增加测试的运行时间，权衡是否在每次测试时启用，或者只在确定的里程碑或CI中运行。
- **避免过于严格**: 不一定要求代码完全符合 `flake8` 的所有标准，有些项目可能需要基于实际情况来适当放松规则。
- **兼容性问题**: 新版本的 `flake8` 可能会引入新的检查，需要确保你的配置与持续集成系统使用的版本保持一致。

`pytest-flake8` 是一个在自动化测试框架中增加代码静态检查的有用工具，可以帮助团队维护代码质量。通过整合到 `pytest` 的正常使用流程中，它提供了一种方便的方式来保证代码风格和质量都符合标准。

## 10.5.5 测试时间相关插件

### 10.5.5.1 pytest-timeout

`pytest-timeout` 插件主要功能是给测试用例设置一个时间限制，以防止测试无限期地运行下去，尤其是在出现挂起操作或极端性能下降的情况下。

#### 10.5.5.1.1  安装 pytest-timeout

使用 `pip` 安装 `pytest-timeout`：

```sh
pip install pytest-timeout
```

#### 10.5.5.1.2 主要特性

- **设置超时**：可以为整个测试会话或单个测试用例设置超时时间。
- **强制终止**：当测试达到指定时间限制时，该插件能够强制终止测试。
- **灵活性**：支持不同级别的超时设置，包括函数级别和会话级别。
- **多种超时策略**：提供不同的超时策略选择，如信号或多线程。

#### 10.5.5.1.3 使用场景

- **避免 CI 系统挂起**：在持续集成环境中，避免由于挂起的测试而导致的构建时间过长或卡住不前。
- **性能测试**：测试性能退化时，通过超时来监测或标记测试。
- **资源限制环境**：如资源限制的运行环境，保证资源不会被单个测试长时间占用。

#### 10.5.5.1.4 代码示例和注解

命令行使用实例：

在你的 `pytest` 命令中添加 `--timeout` 参数来指定超时时间（单位为秒）：

```sh
pytest --timeout=300
```

这意味着如果任何测试用例运行时间超过 300 秒，则会被强制停止。

Python 代码使用实例：

在你的单个测试函数上使用 `@pytest.mark.timeout` 装饰器来设置这个测试用例的时间限制：

```python
# content of test_timeout.py
import pytest
import time

@pytest.mark.timeout(5)
def test_example():
    # 执行一些可能会耗费时间的操作
    time.sleep(10)  # 故意设置超时，测试装饰器功能
    # 剩余的测试逻辑
```

在该例中，`test_example` 测试运行超过 5 秒，则`pytest-timeout` 会抛出一个异常：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_timeout.py 
Test session starts (platform: linux, Python 3.11.6, pytest 7.4.0, pytest-sugar 0.9.7)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'check': '2.2.2', 'instafail': '0.5.0', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'random-order': '1.1.0', 'pylint': '0.21.0', 'html': '4.1.1', 'progress': '1.2.5', 'flake8': '1.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'repeat': '0.9.3', 'resume': '0.0.1', 'ordering': '0.6', 'dependency': '0.6.0', 'timeout': '2.2.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, check-2.2.2, instafail-0.5.0, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, random-order-1.1.0, pylint-0.21.0, html-4.1.1, progress-1.2.5, flake8-1.1.1, metadata-3.0.0, assume-2.4.3, repeat-0.9.3, resume-0.0.1, ordering-0.6, dependency-0.6.0, timeout-2.2.0
collected 1 item

+++++++++++++++++++++++++++++++ Timeout ++++++++++++++++++++++++++++++++++++

~~~~~~~~~~~ Stack of Thread-1 (run_server) (140138430314176) ~~~~~~~~~~~~~~~
  File "/usr/lib/python3.11/threading.py", line 1002, in _bootstrap
    self._bootstrap_inner()
  File "/usr/lib/python3.11/threading.py", line 1045, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.11/threading.py", line 982, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/local/lib/python3.11/dist-packages/pytest_rerunfailures.py", line 439, in run_server
    conn, _ = self.sock.accept()
  File "/usr/lib/python3.11/socket.py", line 294, in accept
    fd, addr = self._accept()

++++++++++++++++++++++++++++++++++ Timeout +++++++++++++++++++++++++++++++++++

―――――――――――――――――――――――――――――― test_time_example ―――――――――――――――――――――――――――――

    @pytest.mark.timeout(5)
    def test_time_example():
        # 执行一些可能会耗费时间的操作
>       time.sleep(10)  # 故意设置超时，测试装饰器功能
E       Failed: Timeout >5.0s

test_timeout.py:7: Failed

 chapter1-10/test_timeout.py::test_time_example ⨯                 100% ██████████
=========================== short test summary info =========================
FAILED test_timeout.py::test_time_example - Failed: Timeout >5.0s

Results (5.06s):
       1 failed
         - chapter1-10/test_timeout.py:4 test_time_example
root@Gavin:~/code/chapter1-10#
```

#### 10.5.5.1.5 注意事项

- **阻塞操作**：确保了解测试中的阻塞操作，并合理设置超时时间。
- **合理设置超时值**：设置的超时值应该基于测试的正常运行时间和测试环境的性能，并留有一定的冗余。
- **调试方便性**：超时可能会干扰调试过程，因为它会强制杀死挂起的测试进程。
- **依赖外部资源的测试**：外部资源响应时间波动可能导致测试时而成功，时而因超时而失败。

`pytest-timeout` 插件提供了一种简单有效的方式来限制测试用例的执行时间，有助于及时发现和处理潜在的性能问题和挂起状态。然而，在设置超时之前，你应当对测试用例的预期运行时间有一个合理的估计，从而避免过早地终止本应成功的测试。

### 10.5.5.2 function-timeout

注意，`function-timeout`是一个Python库，它不是插件，在自动化项目编码过程中有可能使用到，所以归类此处进行介绍。

`function-timeout`库允许你为特定的函数调用设置超时限制。如果函数在给定的时间内没有返回，它会抛出一个异常，强制结束函数执行。

这个库在处理可能卡住或耗时过长的外部资源请求时特别有用，例如网络请求、耗时的计算或任何可能无限期运行的代码。

#### 10.5.5.2.1 安装 `function-timeout`

`function-timeout`可以通过pip进行安装：

```bash
pip install function-timeout
```

#### 10.5.5.2.2 使用 `function-timeout`

使用`function-timeout`的核心是`func_timeout`函数，你可以用它来包装任何可能需要超时处理的函数调用。

```python
from func_timeout import func_timeout, FunctionTimedOut

def my_long_running_function():
    # 函数内的某些操作可能会耗费较长时间...
    pass

try:
    # 设置函数超时限制为10秒
    result = func_timeout(10, my_long_running_function)
except FunctionTimedOut:
    print("The function call has timed out")
```

如果`my_long_running_function`函数在10秒内没有完成执行，`func_timeout`函数会抛出一个`FunctionTimedOut`异常。

这里讲述一个项目中碰到的问题，通过使用`function-timeout`解决掉。

现象：

在编写`S3 multipart upload`相关`test case`时，碰到一个`Quota`相关场景，即上传`S3 Object`超过了`Bucket Quota` 的设定，导致`thread hang`住，无法退出。 一般情况下，无`Quota`下，程序正常上传`Object`并退出，但碰到这种有`Quota`场景的，一旦超额，用例对应`multipart upload function` 卡住。 

如下，为多线程中的使用：

```python
# content of test_func_set_timeout.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import func_timeout
from func_timeout import func_set_timeout

@func_set_timeout(1)
def task():
    while True:
        print('hello world')
        time.sleep(1)


if __name__ == '__main__':
    try:
        task()
    except func_timeout.exceptions.FunctionTimedOut:
        print('task func_timeout')
```

执行后输出：

```shell
root@Gavin:~/code/chapter1-10# python3 test_func_set_timeout.py 
hello world
hello world
task func_timeout
root@Gavin:~/code/chapter1-10#
```

这样就可以不用中断主程序，可以继续执行后面的任务，也可以在超时后加上重试等功能，这就看自己需要了。

对应项目的测试用例基类（部分内容）：

```python
    if option in ['upload']:
        try:
            self.upload_file_multipart(file_path, object_name, bucket, thread_cnt)
        except func_timeout.exceptions.FunctionTimedOut:
            logging.debug("--  Upload failed by FunctionTimedOut")
```

在被调用function 头部增加装饰器`func_set_timeout`：

```shell
    @func_set_timeout(5)
    def upload_file_multipart(self, file_path, object_name, bucket, thread_cnt):
        filesize = os.stat(file_path).st_size
        mp = bucket.initiate_multipart_upload(object_name)
        q = self.init_queue(filesize)
        for i in range(0, thread_cnt):
            t = threading.Thread(target=self.upload_chunk, args=(file_path, mp, q, i))
            t.setDaemon(True)
            t.start()
        q.join()
        mp.complete_upload()
```

如上，完美解决掉thread hang死问题。

#### 10.5.5.2.3 可传递的参数

`func_timeout`函数除了接受超时时间和目标函数之外，还接受其他一些参数，例如：

- `args`（可选）: 一个元组，包含将传递给函数的位置参数。
- `kwargs`（可选）: 一个字典，包含将传递给函数的关键字参数。

```python
result = func_timeout(5, my_func, args=(arg1, arg2), kwargs={'foo': 'bar'})
```

在这个例子中，`my_func`函数将会接收`arg1`和`arg2`作为它的位置参数，以及一个名为`foo`的关键字参数。

#### 10.5.5.2.4 注意事项

- **线程和进程**: `function-timeout`的实现依赖于Python的线程或进程，这可能会影响其在特定应用中的可用性。
- **清理资源**: 由于函数可能会因为超时被强制结束，所以有必要确保所有的资源（如打开的文件或网络连接）都被清理干净，防止资源泄露。
- **调试难度**: 由于函数可能在任意时刻被打断，这可能给调试带来困难。

在使用 `function-timeout` 时，重要的是要了解使用此类工具可能对代码运行环境产生何种潜在影响，并确保代码逻辑和资源管理能够适应这些影响。此外，也请留意该库的兼容性和项目的维护状态，来确保它适合你项目的需求。在大多数情况下，合理使用 `function-timeout` 可以在不改变原有函数逻辑的情况下，添加额外的超时保护。

### 10.5.5.3 pytest-freezegun

`pytest-freezegun`插件用于在测试中冻结时间，基于freezegun库实现了对时间冻结的支持，它可以帮助我们解决与时间相关的测试问题，例如测试依赖于当前时间的函数或测试需要模拟过去或未来日期的功能。这个插件随时可以变化当前系统时间，freezer可以冰冻时间，freezer.move_to可以改变时间，解决验证某一时间点的代码触发，或未来时间的代码变化问题。它通过在测试函数上应用装饰器或使用上下文管理器的方式来冻结时间。

#### 10.5.5.3.1 安装 pytest-freezegun

安装pytest-freezegun非常简单，只需运行：

```shell
pip install pytest-freezegun
```

#### 10.5.5.3.2 主要特点

* **简单易用**：通过装饰器或上下文管理器轻松应用。
* **灵活性**：可以冻结到指定的日期和时间。
* **多用途**：适用于单元测试、集成测试等。


#### 10.5.5.3.3 使用场景

* **时间敏感的测试**：当测试函数依赖当前时间（如日志、时间戳生成）时。
* **日期相关功能**：如测试定期任务、生日提醒等。
* **时间旅行**：模拟未来或过去的日期来测试如缓存过期、报告生成等。

#### 10.5.5.3.4 代码示例与注解

**方法一：使用mark标记**

`pytest-freezegun`允许我们在测试中冻结时间，以便于测试与时间相关的功能。它通过在测试函数上应用装饰器来实现这一点。下面是一个简单的示例：

```python
# content of test_freezegun_mark.py
import pytest
import datetime


@pytest.mark.freeze_time("2024-01-04")
def test_current_date():
    current_date = datetime.datetime.now()
    assert current_date == datetime.datetime(2024, 1, 4)
```

在上述示例中，我们使用`@pytest.mark.freeze_time("2024-01-04")`冻结在指定的时间点（"2024-01-04"）,而实际上当前时间是"2024-01-05"。在冻结时间期间，`datetime.datetime.now()`将始终返回指定的时间，这样我们就可以测试基于时间的逻辑。

执行这条用例，你会发现是通过的，输出结果参考如下：

```shell
root@Gavin:~/code/chapter1-10# date
Fri Jan  5 09:55:40 AM CST 2024
root@Gavin:~/code/chapter1-10# pytest -s -v test_freezegun_mark.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'check': '2.2.2', 'instafail': '0.5.0', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'random-order': '1.1.0', 'freezegun': '0.4.2', 'pylint': '0.21.0', 'html': '4.1.1', 'progress': '1.2.5', 'flake8': '1.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'live': '0.6', 'repeat': '0.9.3', 'resume': '0.0.1', 'ordering': '0.6', 'dependency': '0.6.0', 'timeout': '2.2.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, check-2.2.2, instafail-0.5.0, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0, html-4.1.1, progress-1.2.5, flake8-1.1.1, metadata-3.0.0, assume-2.4.3, live-0.6, repeat-0.9.3, resume-0.0.1, ordering-0.6, dependency-0.6.0, timeout-2.2.0
collected 1 item

test_freezegun_mark.py::test_current_date PASSED
test_freezegun_mark.py::test_current_date PASSED
_________________________________________________________________________________ 1 of 1 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun __________________________________________________________________________________

test_freezegun_mark.py::test_current_date PASSED

=============================== 3 passed in 0.03s =============================
root@Gavin:~/code/chapter1-10#
```



**方法二：使用freezer fixture**

```python
# content of test_freezegun_freezer_fixture.py
import datetime

def test_time_travel(freezer):
    # 设置初始冻结时间
    freezer.move_to("2024-01-04")
    initial_time = datetime.datetime.now()
    assert initial_time == datetime.datetime(2024, 1, 4)

    # 将时间向前移动2天
    freezer.move_to("2024-01-02")
    new_time = datetime.datetime.now()
    assert new_time == datetime.datetime(2024, 1, 2)

    # 再次移动时间到过去，这次日期跨度大一些
    freezer.move_to("2023-06-09")
    past_time = datetime.datetime.now()
    assert past_time == datetime.datetime(2023, 6, 9)

    # 当前时间是2024-01-05，move to 未来，24年的除夕日
    freezer.move_to("2024-02-09")
    future_time = datetime.datetime.now()
    assert future_time == datetime.datetime(2024, 2, 9)
```

执行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_freezegun_freezer_fixture.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'check': '2.2.2', 'instafail': '0.5.0', 'xdist': '3.5.0', 'rerunfailures': '13.0', 'sugar': '0.9.7', 'random-order': '1.1.0', 'freezegun': '0.4.2', 'pylint': '0.21.0', 'html': '4.1.1', 'progress': '1.2.5', 'flake8': '1.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'live': '0.6', 'repeat': '0.9.3', 'resume': '0.0.1', 'ordering': '0.6', 'dependency': '0.6.0', 'timeout': '2.2.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, check-2.2.2, instafail-0.5.0, xdist-3.5.0, rerunfailures-13.0, sugar-0.9.7, random-order-1.1.0, freezegun-0.4.2, pylint-0.21.0, html-4.1.1, progress-1.2.5, flake8-1.1.1, metadata-3.0.0, assume-2.4.3, live-0.6, repeat-0.9.3, resume-0.0.1, ordering-0.6, dependency-0.6.0, timeout-2.2.0
collected 1 item

test_freezegun_freezer_fixture.py::test_time_travel PASSED
test_freezegun_freezer_fixture.py::test_time_travel PASSED
_________________________________________________________________________________ 1 of 1 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun __________________________________________________________________________________

test_freezegun_freezer_fixture.py::test_time_travel PASSED

=============================== 3 passed in 0.04s ===============================
root@Gavin:~/code/chapter1-10#
```

除了在特定时间点冻结时间外，`pytest-freezegun`还允许我们模拟时间的流逝。我们可以通过向`@freeze_time`装饰器传递一个字符串参数来指定时间的增量。下面是一个示例：

```python
import pytest
import datetime

@pytest.mark.freeze_time("2024-01-05")
def test_current_date():
    current_date = datetime.datetime.now()
    new_date = current_date + datetime.timedelta(days=5)
    assert new_date == datetime.datetime(2024, 1, 10)
```

在上述示例中，我们使用datetime.timedelta类来表示时间的增量。通过将增量传递给datetime.timedelta，我们可以模拟时间的流逝。

```python
# content of test_freezegun_set_time.py
import datetime
from freezegun import freeze_time

# 冻结时间为 2023-05-04
@freeze_time("2023-05-04")
def test_function():
    now = datetime.datetime.now()
    assert now == datetime.datetime(2023, 5, 4)

# 使用with语句
def test_another_function():
    with freeze_time("2023-05-04"):
        now = datetime.datetime.now()
        assert now == datetime.datetime(2023, 5, 4)
```

在这个例子中，`freeze_time` 装饰器/上下文管理器将当前时间设置为指定的日期（2023-05-04），无论实际日期如何。


#### 10.5.5.3.5 运行原理

`pytest-freezegun`插件通过使用`pytest`的`fixture`机制，为测试函数提供了方便的时间冻结功能。下面是`pytest-freezegun`实现原理的简要说明：

* pytest-freezegun定义了一个名为freezer的自定义fixture。这个fixture使用@pytest.fixture装饰器进行标记。
* 在fixture的实现中，`pytest-freezegun`使用`freezegun`库的`freeze_time`函数创建一个时间冻结器对象。并通过调用`start`方法开始冻结时间。
* 冻结后的时间对象被返回给测试函数，测试函数可以使用这个对象来模拟和控制时间的流逝。
* 当测试函数执行完毕后，`pytest`会自动清理`fixture`，并调用冻结器对象的`stop`方法停止时间冻结。

通过以上步骤，了解了`pytest-freezegun`插件实现`pytest`中对时间冻结的支持。我们来看以看源码：

```python
@pytest.fixture(name=FIXTURE_NAME)
def freezer_fixture(request):
    """
    Freeze time and make it available to the test
    """
    args = []
    kwargs = {}
    ignore = []

# If we've got a marker, use the arguments provided there
marker = get_closest_marker(request.node, MARKER_NAME)
if marker:
    ignore = marker.kwargs.pop('ignore', [])
    args = marker.args
    kwargs = marker.kwargs

# Always want to ignore _pytest
ignore.append('_pytest.terminal')
ignore.append('_pytest.runner')

# Freeze time around the test
freezer = freeze_time(*args, ignore=ignore, **kwargs)
frozen_time = freezer.start()
yield frozen_time
freezer.stop()
```

这个 fixture 的实现包含几个关键部分：

1. 初始化参数：

```python
args = []
kwargs = {}
ignore = []
```

这里初始化了三个列表和字典，用于存储将传递给 freeze_time 的参数和关键字参数。

2. 获取 Marker：

```python
marker = get_closest_marker(request.node, MARKER_NAME)
if marker:
    ignore = marker.kwargs.pop('ignore', [])
    args = marker.args
    kwargs = marker.kwargs
```

这部分代码检查是否有任何特定的 marker（如 @pytest.mark.some_marker）附加到测试函数上。如果有，它会使用这些 marker 提供的参数和关键字参数来配置 freeze_time。

3. 忽略列表：

```python
ignore.append('_pytest.terminal')
ignore.append('_pytest.runner')
```

这里往 ignore 列表中添加了特定的模块，意味着 freeze_time 在冻结时间时，会忽略这些模块。

4. 冻结时间：

```python
freezer = freeze_time(*args, ignore=ignore, **kwargs)
frozen_time = freezer.start()
yield frozen_time
```

这部分代码实际上启动了时间冻结。freeze_time 使用前面收集的参数和关键字参数来冻结时间。yield 关键字暂停了函数的执行，同时返回了冻结的时间给测试用例。

5. 结束冻结：

```python
freezer.stop()
```

一旦测试用例执行完毕，控制权回到 `freezer_fixture`，接下来执行 `freezer.stop()`，这会停止时间冻结并恢复到正常时间流。

#### 10.5.5.3.6 注意事项

* **非真实时间流逝**：在冻结时间期间，时间不会真实流逝。
* **时区问题**：确保考虑到时区差异，特别是在处理国际化应用时。
* **与其他时间相关库的兼容性**：比如与 `datetime`、`time` 库结合使用时的效果。
* **清理**：确保每个测试结束后时间恢复正常，以避免对其他测试的影响。通常，使用装饰器或上下文管理器可以自动处理。

`pytest-freezegun` 提供了一种简单有效的方式来处理在测试中涉及的时间和日期问题，使得这部分测试更加可靠和准确，帮助我们轻松地模拟时间，以便测试与时间相关的功能。通过冻结时间或模拟时间的流逝，我们可以编写准确、可靠的时间相关的测试。

## 10.5.6 构造测试数据相关

### 10.5.6.1 pytest-factoryboy

`pytest-factoryboy` 插件集成了 `factory_boy` 库，后者是一个用于设置测试数据的Python库。`factory_boy` 以声明式的方式允许开发者定义对象的工厂，这些对象的属性可以用于测试中的数据设置。

#### 10.5.6.1.1 安装 pytest-factoryboy

使用 `pip` 安装 `pytest-factoryboy`:

```sh
pip install pytest-factoryboy
```

#### 10.5.6.1.2 主要特性

- **集成工厂模式**：与 `factory_boy` 完美集成，提供了一种编写声明式工厂的方式用于在测试中创建对象。
- **模型工厂Fixtures**: 自动为每一个 `factory_boy` 工厂生成一个 `pytest` fixture。
- **依赖注入**：利用 `pytest` 的fixture机制，轻松实现依赖注入和测试隔离。
- **易于扩展**：可以自定义并覆盖工厂属性，甚至组合多个工厂来创建复杂对象。

#### 10.5.6.1.3 使用场景

- **单元测试和集成测试**：在任何需要测试数据库或需要模拟对象的地方使用，使得测试代码更加干净和可维护。
- **数据模型实例创建**：在使用如 Django 或 SQLAlchemy 等ORMs时，用于快速生成模型实例作为测试数据。
- **测试数据隔离**：确保测试之间互不干扰，每个测试用例都有其自己的数据环境。

#### 10.5.6.1.4 代码示例和注解

假设我们有以下的 `User` 模型和对应的 `UserFactory`：

```python
# content of models.py
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


# content of factories.py
import factory
from models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
```

接下来，我们在 `conftest.py` 中注册 `UserFactory` 为一个 pytest fixture：

```python
# content of conftest.py
import pytest
from pytest_factoryboy import register
from factories import UserFactory

register(UserFactory)
```

注册 `UserFactory` 后，`pytest-factoryboy` 将自动为你创建几个 fixtures：

- `user_factory` - 一个 factory 的实例，用于生成 `User` 对象。
- `user` - 一个 `User` 对象的实例，每个测试函数调用时都会重新生成。

现在，你可以在测试中使用这些 fixtures：

```python
# test_user.py
def test_user_creation(user):
    assert user.username.startswith('user')
    assert '@example.com' in user.email

def test_user_custom_username(user_factory):
    custom_user = user_factory(username='customuser')
    assert custom_user.username == 'customuser'
```

运行效果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_users.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'freezegun': '0.4.2', 'html': '4.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, freezegun-0.4.2, html-4.1.1, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0
collected 2 items

test_users.py::test_user_creation PASSED
test_users.py::test_user_custom_username PASSED

============================= 2 passed in 0.06s ==============================
root@Gavin:~/code/chapter1-10# 
```

在第一个测试中，我们使用了 `user` fixture，它会给我们一个带有默认设置的 `User` 对象。第二个测试中，我们使用 `user_factory` 来创建一个带有自定义 `username` 的 `User` 对象。

这样，你就可以使用 `pytest-factoryboy` 来轻松地在你的测试中创建和管理测试数据了。

#### 10.5.6.1.5 注意事项

- **理解 factory_boy**: 在使用 `pytest-factoryboy` 之前，应当了解 `factory_boy` 的工作原理和如何定义工厂。
- **避免过度复杂**: 在定义工厂时要注意其复杂度，保持工厂的简洁和明确，以免降低测试的可读性和可维护性。
- **清理和设置数据库状态**: 如果用于数据库操作，确保在测试运行前后清理数据库状态。
- **工厂维护**: 对数据模型的更改需要及时反映到工厂的定义上，否则可能导致测试失败。

`pytest-factoryboy` 插件能够为 `pytest` 测试带来 `factory_boy` 的强大功能，简化测试数据的创建和管理。

### 10.5.6.2 pytest-mock

`pytest-mock` 是一个基于 `unittest.mock` 库的 `pytest` 插件，该插件提供了方便的 mock 和 `spy` 功能，用于简化测试中的对象模拟过程。

#### 10.5.6.2.1 安装 pytest-mock

通过 `pip` 安装 `pytest-mock`:

```sh
pip install pytest-mock
```

#### 10.5.6.2.2 主要特性

- **简化 Mocking**: 提供了一个 `mocker` fixture，用于快捷地在测试中创建和使用 mock 对象。
- **与 `pytest` 结合**: 与 `pytest` 的 fixture 系统集成，使得每个测试函数可以使用独立的 mocks。
- **支持 Spy 功能**: 允许在保留对象原有功能的同时跟踪方法调用。
- **扩展 `unittest.mock`**: 本质上就是对 `unittest.mock` 的一个封装，所以你完全可以直接使用 `mock` 库的所有功能。

#### 10.5.6.2.3 使用场景

- **单元测试**: 当需要隔离测试中的某个组件时，可以用 mock 来模拟该组件的行为。
- **依赖隔离**: 对于外部服务或复杂资源的依赖，可以通过 mocks 来模拟，这样不会真的去触发外部调用。
- **行为验证**: 使用 spy 来验证某个对象的方法是否被调用，以及调用时的参数是否正确。
- **可控条件**: mock 对象可以预设返回值或者特定的异常，方便测试各种条件。

#### 10.5.6.2.4 代码示例和注解

以下是一个使用 `pytest-mock` 的基本例子，我们将创建一个模拟一个简单函数的测试：

```python
# content of mymodule.py
def external_api_call():
    # 假设这是一个调用外部API的函数
    pass

def function_to_test():
    # 这个函数在其内部调用了上面的外部API
    external_api_call()
    return 'result'
```

为了测试 `function_to_test` 而不实际执行 `external_api_call`，我们可以使用 `mocker` 来模拟 `external_api_call`：

```python
# content of test_mymodule.py
import mymodule

def test_function_to_test(mocker):
    # 使用 mocker 来模拟 external_api_call 函数
    mock_api_call = mocker.patch('mymodule.external_api_call')
    
    # 现在调用 function_to_test，external_api_call 将不会被真实调用，而是被模拟
    result = mymodule.function_to_test()
    
    # 确保模拟的函数被调用过一次
    mock_api_call.assert_called_once()
    
    # 断言 function_to_test 返回了预期的结果
    assert result == 'result'
```

在上面的测试中，我们使用了 `mocker.patch` 来替换 `mymodule` 中的 `external_api_call` 函数。`mocker.patch` 接受一个路径参数，表示要模拟的对象。在这个例子中，它模拟了 `mymodule.external_api_call` 函数，这样当 `function_to_test` 被调用时，它实际上不会执行真正的 `external_api_call`。

`mock_api_call.assert_called_once()` 是一个断言，确保模拟的函数在测试过程中被调用了一次。如果函数没有被调用，或者被调用了多次，测试将失败。

最后，`assert result == 'result'` 确认 `function_to_test` 返回了预期的结果。其运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_mymodules.py 
================================ test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'freezegun': '0.4.2', 'html': '4.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, freezegun-0.4.2, html-4.1.1, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 1 item

test_mymodules.py::test_function_to_test PASSED

================================ 1 passed in 0.05s ============================
root@Gavin:~/code/chapter1-10#
```

#### 10.5.6.2.5 注意事项

- **Mock的适用性**: 确保只在适当的时候使用 mocks，比如你需要隔离外部调用或者其他无法控制的组件（如网络请求、数据库调用等）。
- **过度使用**: 避免过度使用 mocks，因为这可能会导致你的测试过于脱离实际运行环境，减少测试的价值。
- **行为验证**: 当使用 `spy` 或断言 mock 调用时，要小心确保你的测试逻辑正确无误。

`pytest-mock` 使得在 `pytest` 测试中进行 mock 变得异常简单，与 `pytest` 的 fixture 系统完美配合，可以显著提高单元测试效率和可读性。

### 10.5.6.3 pytest-mock-resources

`pytest-mock-resources` 插件旨在为测试用例轻松创建和管理外部资源的 mock，这个插件很适合于需要对数据库进行集成测试但又不想依赖于一个真实数据库服务器的场景。使用 `pytest-mock-resources` 可以创建可管理的、可重复的数据库和消息队列等临时资源，以便进行访问和操作数据的测试，简化编写数据库和其他资源交互测试的过程，无需手动设置和拆解测试环境。

#### 10.5.6.3.1 安装 pytest-mock-resources

```bash
pip install pytest-mock-resources
```

#### 10.5.6.3.2 主要特性

- **简化数据库的测试设置：** 无需手动创建和配置测试数据库。
- **数据库隔离：** 每个测试函数都会得到一个清洁状态的数据库。
- **支持多种数据库：** 包括 PostgreSQL、MySQL 等。
- **可扩展和自定义：** 可以根据测试的需求灵活地定义fixture（如不同类型的数据库）。
- **复用**：允许你在多个测试中复用相同资源的配置，而不需要复制和粘贴相同的设置代码。
- **自动清理**：在测试完成后，临时创建的资源（如数据库）会自动销毁或回滚，保证了测试环境的清洁。

#### 10.5.6.3.3 使用场景

- **数据库测试**：当你需要对数据库层进行单元测试或集成测试，而且希望避免污染开发或生产数据库时。
- **消息队列测试**：用于测试消息队列的互动，如确保消息正确发布和接收等。
- **其他资源测试**：适用于任何需要模拟外部资源如`Redis`等，并且希望在测试完成后自动清理的场景。
- **集成测试：** 你需要对代码进行集成测试，该代码与数据库进行交互，而不想依赖真实的数据库环境。
- **并发测试：** 你希望同时运行多个测试用例，每个测试用例都有自己的隔离数据库环境。
- **CI/CD流程：** 在持续集成/持续部署过程中，快速、一致地设置和拆除数据库环境。

#### 10.5.6.3.4 代码示例和注解

以下是一个使用 `pytest-mock-resources` 来测试 `PostgreSQL` 数据库交互的示例：

```python
# content of test_PG_database.py
import pytest
from sqlalchemy import text

# 导入 create_postgres_fixture 函数
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.orm import sessionmaker

# 调用 create_postgres_fixture 创建一个数据库 Engine fixture
# 这里不需要传递任何参数，因为 create_postgres_fixture 会自动为我们创建一个隔离的、可以立即使用的 PostgreSQL 数据库实例
pg_engine = create_postgres_fixture()

# 创建一个 Pytest fixture，用于生成 database session
# 注意这里我们使用 pg_engine fixture 作为参数传递，
# pg_engine 返回的是 SQLAlchemy Engine 对象，在 Pytest 执行测试时会自动被创建
@pytest.fixture
def session(pg_engine):
    # 使用 sessionmaker 工厂函数创建 Session 类
    # 我们将 sqlalchemy Engine 绑定到 sessionmaker，以便于创建和数据库的会话
    Session = sessionmaker(bind=pg_engine)
    # 实例化 Session 类创建会话对象
    session = Session()
    # 使用 yield 关键词返回会话对象，测试函数会使用这个会话进行数据库操作
    # 在 yield 之后的代码会在测试函数调用完成后执行，类似于 teardown
    yield session
    # 测试完成后，关闭会话确保释放资源
    session.close()

# 测试函数使用 session fixture 进行数据库交云科技
def test_database_interaction(session):
    # 在数据库会话中执行 SQL 命令
    result = session.execute(text("SELECT 1")).fetchone()
    # 断言数据库返回的结果是否符合预期
    assert result == (1,)
    # 这个测试会在 pg_engine 代表的临时数据库上执行
```

在这个示例中，通过使用 `create_postgres_fixture` 可以创建一个 `PostgreSQL` 数据库测试固件，`engine` 和 `session` 固件分别用于创建引擎和数据库会话。测试函数 `test_database_interaction` 利用这些固件来测试数据库交互，断言是否能从数据库中选择出期望的值。

如上用例执行前尚需安装`PG`数据库，`Docker`和`python_on_whales`库文件，以`Ubuntu23`环境为例：

```shell
apt -y install postgresql-15
apt -y install docker.io
pip install python_on_whales
pip install psycopg2-binary
```

首次执行用例时，需要下载`docker client binary file`，请耐心等待运行结果：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_PG_database.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 1 item

test_PG_database.py::test_database_interaction /usr/local/lib/python3.11/dist-packages/python_on_whales/client_config.py:84: UserWarning: The docker client binary file was not found on your system. 
Docker on whales will try to download it for you. 
Don't worry, it won't be in the PATH and won't have anything to do with the package manager of your system. 
Note: We are not installing the docker daemon, which is a lot heavier and harder to install. We're just downloading a single standalone binary file.
If you want to trigger the download of the client binary file manually (for example if you want to do it in a Dockerfile), you can run the following command:
 $ python-on-whales download-cli 

  warnings.warn(
 12%|███████████████████▊                                                                                                                                                | 8.37M/69.2M [04:51<3:49:14, 4.42kiB/s]
```

这个过程取决于`binary file`的下载速度，下载完成后会执行上述用例。再次执行时，由于`binary file`已经存在，无需再次下载，直接运行用例，效果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_PG_database.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 1 item

test_PG_database.py::test_database_interaction PASSED

=============================== 1 passed in 16.35s ============================
root@Gavin:~/code/chapter1-10# 
```

再来看一个使用 `pytest-mock-resources` 来测试 `MySQL` 数据库创建表并插入一条记录的示例，其中使用的`MySQL`数据库为`Gavin`，用户名`root`，密码为空：

```python
# content of test_mysql_database.py
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 假设这个 fixture 会在 tests/conftest.py 文件中定义
# 这个 fixture 应该返回一个 SQLAlchemy 连接对象
@pytest.fixture
def mysql():
    # 替换为你的实际数据库连接字符串
    # connection_string = "mysql+pymysql://user:password@localhost/testdb"
    connection_string = "mysql+pymysql://root:@localhost/Gavin"
    engine = create_engine(connection_string)
    # 创建一个新的 session
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # 提供 session 给测试用例使用
    session.close()  # 测试完成后关闭 session

# 现在我们可以在测试函数中使用这个 fixture
def test_database_interaction(mysql):
    # 使用提供的mysql数据库 session 执行一些数据库操作
    connection = mysql

    # 假设我们有一个创建用户表的SQL命令
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL
    )
    """
    connection.execute(text(create_table_query))
    
    # 插入一条数据 
    insert_query = "INSERT INTO user (username) VALUES ('testuser')"
    connection.execute(text(insert_query))
    
    # 查询数据
    select_query = "SELECT username FROM user"
    result = connection.execute(text(select_query))
    
    # 断言我们插入的数据是否在表中 
    assert result.fetchone()[0] == 'testuser'
    
    # 关闭连接
    connection.close()  # 这行代码在 fixture 中不是必须的，因为 fixture 会处理关闭
```

在这个例子中，我们定义了一个名为 `mysql` 的 fixture，它创建了一个数据库引擎，并且打开了一个新的数据库 session。在测试函数 `test_database_interaction` 中，我们使用这个 session 来执行我们的测试数据库操作。测试完成后，fixture 会自动关闭 session。运行效果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_mysql_database.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 1 item

test_mysql_database.py::test_database_interaction PASSED

=============================== 1 passed in 0.09s =============================
root@Gavin:~/code/chapter1-10#
```

#### 10.5.6.3.5 注意事项

- **资源管理**：确保了解插件是如何管理临时资源的生命周期。例如，它可能使用 Docker 来管理数据库的生命周期，因此在使用之前你可能需要安装 Docker，所以要注意资源的管理和清理，避免测试后留下孤立资源。。
- **性能考虑**：自动创建和销毁资源可能会增加测试的执行时间，尤其是在大量资源创建时。考虑测试的并行化或固件的复用以优化性能。
- **与现有数据隔离**：确保这些模拟资源与你的现有开发或生产环境是隔离的，以避免意外的数据覆盖或损坏。

- **版本兼容性：** 确保你使用的 `pytest-mock-resources` 版本与你的 `python` 和 `pytest` 版本兼容。
- **数据安全性：** 尽管使用 mock 资源，但还是应确保不会泄露任何敏感数据，尤其是在CI/CD环境中。

### 10.5.6.4 pytest-faker

`pytest-faker`是一个用于在`pytest`测试中生成随机数据的插件，它可以帮助我们简化测试数据的创建过程，并提供多种类型的随机数据，如姓名、地址、电子邮件、日期等。`pytest-faker`基于`Faker`库，该库提供了一个丰富的随机数据生成器。

#### 10.5.6.4.1 安装 pytest-faker

```shell
pip install pytest-faker
```


#### 10.5.6.4.2 主要特性

* 简单易用：`pytest-faker`与 `pytest`框架无缝集成，可以直接在测试代码中使用。
* 多样化的数据类型：它提供了丰富的数据生成器，包括姓名、地址、电子邮件、日期、文本等，可以满足各种测试场景的数据需求。
* 可自定义的数据生成器：除了提供的默认数据生成器外，我们还可以根据自己的需求创建自定义的数据生成器。
* 数据一致性：`pytest-faker`生成的随机数据是一致的，这意味着每次生成的随机数据都是相同的，确保了测试的可重复性。
* 多语言支持：`Faker`库支持多种语言，因此`pytest-faker`也可以生成各种语言的随机数据。    


#### 10.5.6.4.3 使用场景

* 数据生成：在编写测试时，我们通常需要使用一些随机的测试数据。`pytest-faker`可以帮助我们生成各种类型的随机数据，以满足测试的需要。
* 数据覆盖：有时我们需要在测试中覆盖特定的数据场景，例如测试用户注册时的各种情况。`pytest-faker`可以提供各种数据生成器，帮助我们模拟不同的测试场景。
* 数据一致性：在测试中，我们通常需要使用相同的数据进行多次测试。`pytest-faker`可以生成一致的随机数据，以确保测试的可重复性。

#### 10.5.6.4.4 代码示例和注解


##### 10.5.6.4.1 测试数据生成

在编写测试用例时，我们需要创建各种类型的测试数据。`pytest-faker`可以帮助我们生成随机数据，使得测试数据更加多样化和真实。

```python
# content of test_faker_generate_data.py
import pytest
from faker import Faker

@pytest.fixture(scope="session")
def faker():
    """
    Create a Faker instance for generating fake data
    """
    return Faker()

def test_generate_name(faker):
    """
    Test generating a random name
    """
    name = faker.name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_generate_email(faker):
    """
    Test generating a random email address
    """
    email = faker.email()
    assert isinstance(email, str)
    assert "@" in email

def test_generate_phone_number(faker):
    """
    Test generating a random phone number
    """
    phone_number = faker.phone_number()
    assert isinstance(phone_number, str)
    assert len(phone_number) > 0
```

在这个示例中，我们首先定义了一个作用域为`session`的`fixture faker`，它使用`Faker`库创建一个`Faker`实例，用于生成虚假数据。

然后，我们编写了几个测试函数来测试生成不同类型的随机数据。在每个测试函数中，我们使用`faker fixture`作为参数，调用`Faker`实例的相应方法生成随机数据，并进行断言来验证生成的数据的类型和格式。其运行结果如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_faker_generate_data.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'faker': '2.0.0', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, faker-2.0.0, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 3 items

test_faker_generate_data.py::test_generate_name PASSED
test_faker_generate_data.py::test_generate_email PASSED
test_faker_generate_data.py::test_generate_phone_number PASSED

=============================== 3 passed in 0.08s =============================
root@Gavin:~/code/chapter1-10#
```


##### 10.5.6.4.2 自定义数据生成器

`pytest-faker`还支持自定义数据生成器，通过使用`@pytest.mark.parametrize`装饰器和`faker fixture`来生成自定义的测试数据。


```python
# content of test_faker_self_def_data.py
import pytest
from faker import Faker

@pytest.fixture(scope="session")
def faker():
    """
    Create a Faker instance for generating fake data
    """
    return Faker()

@pytest.mark.parametrize("name", ["John", "Jane", "Alice"])
def test_custom_name(faker, name):
    """
    Test generating a custom name by random
    """
    custom_name = faker.name()
    assert custom_name == name
```

在这个示例中，我们使用`@pytest.mark.parametrize`装饰器来指定测试函数的参数值，通过`faker fixture`生成自定义的测试数据。在这个例子中，我们测试生成自定义姓名，使用了三个不同的姓名进行参数化测试。由于随机生成的自定义姓名，与参数化中给定的名称断言会失败。


##### 10.5.6.4.3 数据本地化


`pytest-faker`支持多种不同语言的数据生成，可以通过设置`Faker`类的`locale`属性来指定数据的本地化。

```python
# content of test_faker_local_data.py
import pytest
from faker import Faker

@pytest.fixture(scope="session")
def faker():
    """
    Create a Faker instance for generating fake data
    """
    faker = Faker()
    faker.locale = 'zh_CN'  # 设置本地化为中文
    return faker

def test_generate_name(faker):
    """
    Test generating a random name in Chinese
    """
    name = faker.name()
    assert isinstance(name, str)
    assert len(name) > 0
```

在这个示例中，我们创建一个`Faker`实例，并将其本地化设置为中文（zh_CN）。`fixture`的作用域被设置为“session”，表示这个夹具在整个测试会话中只被实例化一次，并在所有需要它的测试中复用这一个实例。测试函数 `test_generate_name` 接收由 `pytest` 通过`fixture`构造的 `faker` 实例。生成一个随机的中文名字，然后进行两个断言：

* `assert isinstance(name, str)` 确保生成的名字是一个字符串类型。
* `assert len(name) > 0` 确保生成的名字不为空，也就是长度大于0。

其运行结果参考如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_faker_local_data.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'faker': '2.0.0', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, faker-2.0.0, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 1 item

test_faker_local_data.py::test_generate_name PASSED

============================== 1 passed in 0.08s ==============================
root@Gavin:~/code/chapter1-10#
```

##### 10.5.6.4.4 数据驱动测试

对于一些需要大量测试数据的功能，可以使用`pytest-faker`生成一定数量的测试数据，以便进行性能测试或负载测试。


```python
# content of test_faker_data_fill.py
import pytest

@pytest.mark.parametrize("num", [10, 100, 1000])
def test_generate_data(faker, num):
    """
    Test generating a specified number of random data
    """
    data = [faker.name() for _ in range(num)]
    assert len(data) == num
```

在这个示例中，我们使用`parametrize`装饰器来运行同一个测试函数多次，每次生成指定数量的随机数据。其运行结果参考如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_faker_data_fill.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'faker': '2.0.0', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, faker-2.0.0, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 3 items

test_faker_data_fill.py::test_generate_data[10] PASSED
test_faker_data_fill.py::test_generate_data[100] PASSED
test_faker_data_fill.py::test_generate_data[1000] PASSED

=============================== 3 passed in 0.26s ==============================
root@Gavin:~/code/chapter1-10#
```

再比如下面的测试用例，可以使用`pytest-faker`生成各种类型的测试数据，以覆盖更多测试场景。


```python
# content of test_faker_data_driven.py
import pytest

@pytest.mark.parametrize("name", [faker.name() for _ in range(10)])
def test_greet(name):
    """
    Test greeting a person with a random name
    """
    greeting = "Hello, " + name
    assert isinstance(greeting, str)
```

在这个示例中，我们使用`parametrize`装饰器来运行同一个测试函数多次，每次使用不同的随机姓名作为参数进行测试。其运行结果参考如下：

```shell
root@Gavin:~/code/chapter1-10# pytest -s -v test_faker_data_driven.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'Faker': '22.0.0', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'faker': '2.0.0', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, Faker-22.0.0, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, faker-2.0.0, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 10 items

test_faker_data_driven.py::test_greet[Jennifer Ingram] PASSED
test_faker_data_driven.py::test_greet[Jenna Olsen] PASSED
test_faker_data_driven.py::test_greet[Lindsay Lee] PASSED
test_faker_data_driven.py::test_greet[Michael Jones] PASSED
test_faker_data_driven.py::test_greet[Joshua Martin] PASSED
test_faker_data_driven.py::test_greet[David Russell] PASSED
test_faker_data_driven.py::test_greet[Barbara Hernandez] PASSED
test_faker_data_driven.py::test_greet[Troy Cooper] PASSED
test_faker_data_driven.py::test_greet[Joshua Proctor] PASSED
test_faker_data_driven.py::test_greet[Corey Boone] PASSED

============================== 10 passed in 0.11s =============================
root@Gavin:~/code/chapter1-10#
```


#### 10.5.6.4.5 注意事项


* 使用假数据时确保它们符合测试需要，例如格式和类型有效性。
* 当生成唯一性数据时（如数据库主键），确保在批量生成数据中处理可能的重复。
* 在可能的情况下使用随机但固定的种子(seed)来生成可重复的测试数据集。

## 10.5.7 测试报告相关

### 10.5.7.1 pytest-live

`pytest-live`插件使用 `pytest` 钩子（hook）生成实时执行结果，方便用户实时跟踪用例执行状态。

#### 10.5.7.1.1 安装 pytest-live

使用 `pip` 安装 `pytest-live`：

```sh
pip install pytest-live
```

#### 10.5.7.1.2 使用方法

```shell
pytest  --live=True --livetimestamp=True
```

比如我使用的是`XShell 7`，客户端是`Windows`，服务器端是`Ubuntu23`，如果想在客户端实时动态查看服务端的`html`报告，需要安装`Xmanager 7`，通过这个工具借助`Ubuntu`版本的f`irefox`打开`html`报告。最终生成的`html`报告参考如下：

<img class="shadow" src="/img/in-post/pytest-live.png" width="800">

### 10.5.7.2 pytest-testreport

`pytest-testreport`是`pytest`生成`html`测试报告的插件，它基于`unittestreport`风格的报告扩展而来)，自动收集用例执行的详细日志信息，以及相关错误和输出信息。

此插件与`pytest-html`插件存在冲突，使用`pytest-testreport`需卸载`pytest-html`插件，反之亦然。

#### 10.5.7.2.1 安装 pytest-testreport

```shell
pip install pytest-testreport
```

#### 10.5.7.2.2 参数介绍

* --report ：指定报告文件名
* --title ：指定报告标题
* --tester ：指定报告中的测试者
* --desc ：指定报告中的项目描述
* --template ：指定报告模板样式（1 or 2）

#### 10.5.7.2.3 使用方法

```shell
pytest -s -v --report=testreport.html --title="Html Report" --tester=Gavin --desc="This is a test" --template=2
```

请注意：

* `--report `只是指定报告名称，实际生成报告名称会在此参数前增加日期，比如：`2024-01-06_10_52_09testreport`
* 无法指定报告生成目录，默认在当前目录下`reports`目录下生成`html`报告

#### 10.5.7.2.4 报告展示

`--template=1`的效果：

<img class="shadow" src="/img/in-post/testreport_template1.png" width="800">

`--template=2`的效果：

<img class="shadow" src="/img/in-post/testreport_template2.png" width="800">



如果想指定报告生成路径，需做对`pytest-testreport`插件安装目录下文件``中代码做如下调整：

```shell
cd /usr/local/lib/python3.11/dist-packages/pytestTestreport
vim pytest_testreport.py
```

完整内容参考如下：

```python
# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
import pytest
from jinja2 import Environment, FileSystemLoader

test_result = {
    "title": "",
    "tester": "",
    "desc": "",
    "reportPath": "",
    "cases": {},
    'rerun': 0,
    "failed": 0,
    "passed": 0,
    "skipped": 0,
    "error": 0,
    "start_time": 0,
    "run_time": 0,
    "begin_time": "",
    "all": 0,
    "testModules": set()
}


def pytest_make_parametrize_id(config, val, argname):
    if isinstance(val, dict):
        return val.get('title') or val.get('desc')


def pytest_runtest_logreport(report):
    report.duration = '{:.6f}'.format(report.duration)
    test_result['testModules'].add(report.fileName)
    if report.when == 'call':
        test_result[report.outcome] += 1
        test_result["cases"][report.nodeid] = report
    elif report.outcome == 'failed':
        report.outcome = 'error'
        test_result['error'] += 1
        test_result["cases"][report.nodeid] = report
    elif report.outcome == 'skipped':
        test_result[report.outcome] += 1
        test_result["cases"][report.nodeid] = report


def pytest_sessionstart(session):
    start_ts = datetime.datetime.now()
    test_result["start_time"] = start_ts.timestamp()
    test_result["begin_time"] = start_ts.strftime("%Y-%m-%d %H:%M:%S")


def handle_history_data(report_dir, test_result):
    """
    处理历史数据
    :return:
    """
    try:
        with open(os.path.join(report_dir, 'history.json'), 'r', encoding='utf-8') as f:
            history = json.load(f)
    except:
        history = []
    history.append({'success': test_result['passed'],
                    'all': test_result['all'],
                    'fail': test_result['failed'],
                    'skip': test_result['skipped'],
                    'error': test_result['error'],
                    'runtime': test_result['run_time'],
                    'begin_time': test_result['begin_time'],
                    'pass_rate': test_result['pass_rate'],
                    })

    with open(os.path.join(report_dir, 'history.json'), 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=True)
    return history


def pytest_sessionfinish(session):
    """在整个测试运行完成之后调用的钩子函数,可以在此处生成测试报告"""
    report2 = session.config.getoption('--report')
    reportPath = session.config.getoption('--reportPath')

    if report2:
        test_result['reportPath'] = reportPath or "reports"
        test_result['title'] = session.config.getoption('--title') or '测试报告'
        test_result['tester'] = session.config.getoption('--tester') or '小测试'
        test_result['desc'] = session.config.getoption('--desc') or '无'
        templates_name = session.config.getoption('--template') or '1'
        name = report2
    else:
        return

    if not name.endswith('.html'):
        file_name = time.strftime("%Y-%m-%d_%H_%M_%S") + name + '.html'
    else:
        file_name = time.strftime("%Y-%m-%d_%H_%M_%S") + name

    if os.path.isdir(test_result['reportPath']):
        pass
    else:
        os.mkdir(test_result['reportPath'])
    file_name = os.path.join(test_result['reportPath'], file_name)
    test_result["run_time"] = '{:.6f} S'.format(time.time() - test_result["start_time"])
    test_result['all'] = len(test_result['cases'])
    if test_result['all'] != 0:
        test_result['pass_rate'] = '{:.2f}'.format(test_result['passed'] / test_result['all'] * 100)
    else:
        test_result['pass_rate'] = 0
    # 保存历史数据
    test_result['history'] = handle_history_data(test_result['reportPath'], test_result)
    # 渲染报告
    template_path = os.path.join(os.path.dirname(__file__), './templates')
    env = Environment(loader=FileSystemLoader(template_path))

    if templates_name == '2':
        template = env.get_template('templates2.html')
    else:
        template = env.get_template('templates.html')
    report = template.render(test_result)
    # print(file_name)
    with open(file_name, 'wb') as f:
        f.write(report.encode('utf8'))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    fixture_extras = getattr(item.config, "extras", [])
    plugin_extras = getattr(report, "extra", [])
    report.extra = fixture_extras + plugin_extras
    report.fileName = item.location[0]
    if hasattr(item, 'callspec'):
        report.desc = item.callspec.id or item._obj.__doc__
    else:
        report.desc = item._obj.__doc__
    report.method = item.location[2].split('[')[0]


def pytest_addoption(parser):
    group = parser.getgroup("testreport")
    group.addoption(
        "--reportPath",
        action="store",
        metavar="path",
        default=None,
        help="create html report file at given path.",
    )
    group.addoption(
        "--report",
        action="store",
        metavar="path",
        default=None,
        help="create html report file at given path.",
    )
    group.addoption(
        "--title",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a title of the repor",
    )
    group.addoption(
        "--tester",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a tester of the report",
    )
    group.addoption(
        "--desc",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a description of the report",
    )
    group.addoption(
        "--template",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a template of the report",
    )
```

携带上`--reportPath`参数示例：

```shell
pytest -s -v --report=_report.html --reportPath=../report --title="Html Report" --tester=Gavin --desc="This is a test" --template=2
```

### 10.5.7.3 pytest-html

`pytest-html` 是一个流行的 `pytest` 插件，它生成一个漂亮的 HTML 报告来展示测试结果。这使得测试结果更容易被分享和查看，特别是在集成到持续集成（CI）工作流程中时。

#### 10.5.7.3.1 安装 pytest-html

你可以使用 pip 来安装 `pytest-html`：

```shell
pip install pytest-html
```

安装完 `pytest-html` 插件之后，你可以通过在 pytest 命令中加入 `--html` 参数来生成HTML报告：

```shell
pytest --html=report.html --self-contained-html
```

这里的 `report.html` 就是生成报告的文件名，你可以根据需要指定其他文件名。 `--self-contained-html` 选项指示 `pytest` 在生成的` HTML`报告中直接嵌入所有 `CSS` 和` JavaScript` 内容，这样报告文件就不再依赖于外部或相对路径上的资源文件。报告可以在任何位置被打开，显示都应该是一致的，有一点需要注意，如果路径中含有中文，`HTML`报告中`Summary`处有可能显示为空。

#### 10.5.7.3.2 主要特性

当你使用了 `--html` 选项，`pytest-html` 会在测试运行结束后生成一个 HTML 文件，其中包括：

- 测试摘要：包括测试通过、失败、错误以及跳过的总数。
- 环境摘要：展示运行测试时的环境，如操作系统、Python 版本、pytest 版本等。
- 详细的测试结果：每一个测试的具体结果，以及相关的测试数据。
- 屏幕截图和日志文件（如果添加了相应的插件和/或标记）。

#### 10.5.7.3.3 扩展功能

`pytest-html` 插件还支持许多其他的功能和命令行选项，例如：

- `--self-contained-html`：在这个模式下，报告将会包含所有静态资源，如样式表和JavaScript文件，这意味着你可以将HTML报告复制或移动到其他地方，不用担心会丢失样式或脚本。
- 添加额外信息：你可以在测试中添加额外的信息，它们将会显示在HTML报告中。
- 日志捕获：如果测试捕获了日志，它们也会被包含在HTML报告中。
- 报告美化：通过自定义CSS，你可以进一步美化生成的HTML报告。

#### 10.5.7.3.4 插件定制化

##### 10.5.7.3.4.1 准备工作

###### 10.5.7.3.4.1.1 升级`py`库

不然在定制化期间会碰到如下报错：

```shell
ModuleNotFoundError: No module named 'py.xml'; 'py' is not a package
```

这是因为`pytest-html`的源码中有引用到`py.xml`这个文件，依赖`py`这个库。

使用命令：``pip install -U py`  安装`py`模块即可解决。

###### 10.5.7.3.4.1.2 准备测试用例

```python
# content of mathlib.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
```

```python
# content of test_mathlib_case.py
import mathlib
import pytest
import math

def test_add():
    """测试 add 函数，确保两个数相加的结果正确。"""
    assert mathlib.add(3, 4) == 7, "3 + 4 应该等于 7"

def test_subtract():
    """测试 subtract 函数，确保两个数相减的结果正确。"""
    assert mathlib.subtract(10, 5) == 5, "10 - 5 应该等于 5"

def test_multiply():
    """测试 multiply 函数，确保两个数相乘的结果正确。"""
    assert mathlib.multiply(2, 3) == 6, "2 * 3 应该等于 6"

def test_divide():
    """测试 divide 函数，确保两个数相除的结果正确。"""
    assert mathlib.divide(8, 2) == 4, "8 / 2 应该等于 4"

def test_divide_by_zero():
    """测试 divide 函数对于零作为除数的情况，应该抛出 ValueError 异常。"""
    with pytest.raises(ValueError):
        mathlib.divide(10, 0)

def test_add_floats():
    """测试 add 函数，确保它正确处理浮点数相加。"""
    assert mathlib.add(0.1, 0.2) == pytest.approx(0.3), "0.1 + 0.2 应该接近 0.3"

def test_truth():
    """测试一个表达式是否为真。"""
    assert mathlib.add(3, 4) > 0, "3 + 4 应该大于 0"

def test_falsy():
    """测试一个表达式是否为假。"""
    assert not mathlib.add(-1, 1), "-1 + 1 应该等于 0（假）"

def test_in_list():
    """测试列表是否包含某个元素。"""
    test_list = [0, 1, 2, 3]
    assert 2 in test_list, "列表应该包含元素 2"

def test_list_sort():
    """测试列表排序功能是否正常工作。"""
    test_list = [3, 2, 1]
    test_list.sort()
    assert test_list == [1, 2, 3], "列表应该排序为 [1, 2, 3]"

def test_sqrt():
    """测试 math.sqrt 函数的返回值是否正确。"""
    num = 25
    assert math.sqrt(num) == 5, "25 的平方根应该是 5"


def test_assert_failed():
    assert 1 == 2
```



##### 10.5.7.3.4.2 增加用例执行时间和描述信息

 在`conftest.py`脚本中使用测试函数`docstring`添加描述（`Description`）列，添加可排序时间（`Time`）列，并删除链接(Link)列：

```python
# content of conftest.py
import pytest
from py.xml import html
from datetime import datetime

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
```

如果不想删除链接(`Link`列，注释掉上述代码中两处`cells.pop()`即可。)

执行如下命令生成报告：

```shell
root@Gavin:~/code/chapter1-10/pytest_html_report# pytest -s -v test_mathlib_case.py --html=../../report/pytest_mathlib.html
```

报告展示效果：

<img class="shadow" src="/img/in-post/pytest-html-description.png" width="800">

##### 10.5.7.3.4.3 删除所有测试通过的结果

借助`pytest_html_results_table_row `挂钩删除所有单元格来删除结果。将下面内容写入到`conftest.py`中，会从报表中删除所有测试通过的结果：

```python
# content of conftest.py
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    if report.passed:
      del cells[:]
```

请注意：生成的HTML报告中会删除掉所有状态为“PASSED”的用例，也不计入统计。比如下面的报告，执行了12个用例，1个失败，报告中只会显示失败的用例：

<img class="shadow" src="/img/in-post/pytest-html-delete_passed.png" width="800">

##### 10.5.7.3.4.4 清空测试通过的日志输出

`pytest` 提供了一个名为 `pytest_html_results_table_row` 的钩子（hook）函数，允许你在在HTML报告中针对每个测试结果行(table row)进行自定义操作。

以下是一个简单地扩展插件的例子，演示了如何在HTML报告中清空通过的测试的日志输出：

```python
# content of conftest.py
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        # 如果测试通过，假设我们想要清空其中某些单元格的内容
        data[:] = [''] * len(data)
```

生成的HTML报告展示PASSED状态用例内容效果如下：

<img class="shadow" src="/img/in-post/pytest-html-del_passed_log.png" width="800">



由于有更好用的测试报告`Allure`，至于其他定制化操作，这里不再赘述，有需要的读者可以访问`pytest-html`官网：`https://pytest-html.readthedocs.io/en/latest/user_guide.html`。

#### 10.5.7.3.5 注意事项

- HTML报告是在测试完成后生成的，如果测试过程中出现了意外中断，报告可能不会生成或者生成的报告可能不完整。
- 对于包含大量测试的项目，生成的HTML报告可能会很大，加载时可能会有性能问题。
- 如果你使用的是自定义的测试插件或者装饰器，需要确保它们与 `pytest-html` 兼容，否则可能会出现报告中显示信息不全或者格式出错的情况。

总的来说，`pytest-html` 是一个非常实用的插件，能够为你的自动化测试提供明晰且美观的呈现效果。它扩展了 `pytest` 的基本功能，让共享和分析测试结果变得更加便捷。



## 10.5.8 其他插件

### 10.5.8.1 `pytest-picked`

`pytest-picked` 是一个可以根据Git状态选择要运行的测试的 `pytest` 插件。它会自动检测Git工作区和索引中变更的文件，并运行与这些变更文件相关联的测试。

#### 10.5.8.1.1 安装 pytest-picked

使用 `pip` 安装 `pytest-picked`：

```sh
pip install pytest-picked
```

#### 10.5.8.1.2 主要特性

- **基于Git选择测试**：插件会选择Git中未提交变更的文件相关的测试来运行，这能减少运行一整套测试集需要的时间。
- **提高开发效率**：允许开发者快速运行与当前开发任务直接相关的测试。
- **简化测试流程**：易于使用，开发者无需手动运行相关的测试，插件自动处理。

#### 10.5.8.1.3 使用场景

- **快速反馈**：当你正在开发新功能或修复bug时，仅运行那些与当前Git改动相关的测试，以便快速验证你的更改是否成功。
- **适用于大型项目**：在大型项目中，全套测试可能需要很长时间，使用 `pytest-picked` 可以显著缩短反馈循环。
- **持续集成优化**：加快CI构建流程，特别是当只需运行部分改动代码相关的测试时。

#### 10.5.8.1.4 示例和注解

安装了 `pytest-picked` 后，可以通过这种方式来运行 `pytest`：

```sh
pytest --picked
```

运行后，插件将只执行与Git工作区和索引中变更文件相关的测试。你可以看到类似这样的输出：

```shell
============================= test session starts ============================
platform linux -- Python 3.x.x, pytest-7.4.x, py-x.x.x, pluggy-x.x.x
rootdir: /path/to/your/repository
plugins: picked-x.x.x
collected 100 items / 95 deselected / 5 selected
```

此示例中，只有5个与代码变更相关的测试被选择和执行。

#### 10.5.8.1.5 注意事项

- **精确度**：该插件基于文件名称寻找匹配的测试，它假设测试位置与模块的命名有一个良好的、可预测的对应关系。
- **测试范围**：可能不会运行所有相关的测试，尤其是当涉及到公共模块或基类变化时，这可能会影响许多其他模块的行为。
- **Git状态**：需要养成良好的Git使用习惯，频繁提交小变更以确保 `pytest-picked` 能够有效工作。
- **独立性**：此插件更适合运行独立的单元测试，对于需要全面测试套件运行的集成测试可能不适用。

`pytest-picked` 插件可以有效提高在开发过程中的测试效率。然而，仅仅依赖它在CI/CD流程中可能不足够，你可能仍然需要运行全套的测试来确保软件质量。

### 10.5.8.2 pytest-base-url

`pytest-base-url` 是一个专供 `pytest` 使用的插件，用于在测试中提供一个基本 URL 的配置。这个插件通常用于 web 测试，可以在命令行中指定基本 URL，这样你的测试用例就可以使用这个 URL 来访问应用或服务。

#### 10.5.8.2.1 安装 pytest-base-url

使用 `pip` 安装 `pytest-base-url`：

```sh
pip install pytest-base-url
```

#### 10.5.8.2.2 主要特性

- **统一配置URL**: 在命令行中一次性指定基本 URL，使得所有的测试都可以使用这个 URL 而不需要重复配置。
- **多环境适用性**: 方便在不同的环境（开发、测试、生产）间切换，只需修改传入的 URL 即可。
- **简化测试参数**: 减少测试用例中URL的冗余，并简化测试用例的参数设置。

#### 10.5.8.2.3 使用场景

- **Web测试**: 当你的测试用例需要访问特定的 web 应用时，使用基础 URL 来简化测试代码。
- **自动化测试**: 在自动化测试脚本中，快速切换不同环境中的应用，比如本地开发环境和线上环境。
- **API测试**: 对外部API进行测试时，通过指定基本URL来轻松指定目标API的环境。

#### 10.5.8.2.4 示例和注解

在 `pytest` 命令行中添加 `--base-url` 参数来传递基本 URL：

```sh
pytest --base-url=http://g.cn
```

在你的测试代码中，你可以使用 `base_url` fixture：

```python
# content of test_base_url.py
import requests

def test_example(base_url):
    # 使用 base_url 进行测试逻辑
    response = requests.get(base_url + '/some/path')
    assert response.status_code == 200
```

在这个例子中，`base_url` fixture 被注入到测试函数中，你可以直接引用它而不需要手动配置 URL。测试执行时，`base_url` 的值将会是命令行中指定的那个。

#### 10.5.8.2.5 注意事项

- **确保 URL 可用性**: 在运行测试之前，确保所指定的 URL 可用，尤其是在持续集成环境中。
- **处理路径拼接**: 注意 URL 和路径间的正确拼接，例如使用 `urljoin` 等来正确处理路径拼接。
- **安全测试**: 当在生产环境中运行测试时要特别小心，避免测试数据对生产数据造成影响。

`pytest-base-url` 插件将基本的 URL 配置与测试逻辑分离，是进行 Web 自动化测试时不可或缺的工具。然而，我们需要注意在不同环境之间切换 URL 时要保持警惕，以免测试过程意外干扰到生产环境。



# 10.6 本章小结

本章节我们深入探讨了`pytest`框架中各种开源插件的使用。这些插件提供了丰富的功能和扩展性，可以帮助我们更高效地编写、执行和管理测试用例。

我们介绍了一些常用的`pytest`插件：

* 如`pytest-cov`、`pytest-html`和`pytest-xdist`。这些插件可以帮助我们生成测试覆盖报告、生成漂亮的HTML测试报告，并支持多线程或分布式测试执行；
* 如`pytest-random-order`和`pytest-ordering`，在测试用例中引入随机性，从而增加测试的覆盖范围和多样性的插件；
* 如`pytest-factoryboy`和`pytest-mock-resources`，用于构造测试数据相关；
* 如`pytest-live`和`pytest-html`，实时跟踪或查看测试用例执行结果报告
  等等。

通过使用这些开源插件，我们可以根据项目需求和测试场景的复杂性，灵活地扩展和定制`pytest`框架的功能。这些插件不仅提供了更强大的测试工具，也提高了测试代码的可读性、可维护性和可扩展性。
