---
title: 《pytest测试指南》-- 附录1 pytest如何debug 
date: 2024-06-07 23:00:00
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
summary: 《pytest测试指南》一书 附录1 pytest debug的几种手法
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

`pytest` 是一个非常流行的 Python 测试框架，它提供了丰富的测试功能。不可避免的，测试过程中可能会遇到错误和问题，这时候就需要对测试用例进行调试。幸运的是，`pytest` 提供了几种工具和技巧来帮助调试。

## 使用 `--pdb` 选项

`pytest` 提供了一个命令行选项 `--pdb`，当使用这个选项运行测试时，如果遇到失败的测试，`pytest` 将会自动进入调试器，让你可以立即开始调试。

```shell
pytest --pdb my_test_file.py
```

这将运行 `my_test_file.py` 文件中的测试，并在第一个失败的测试处进入 Python 调试器 (`pdb`)。在这里，你可以像在任何 `pdb` 会话中那样使用调试命令，比如：

- `l(ist) [first[, last]]`：列出源代码。不带参数时，列出11行代码；带一个参数时，列出从该行开始的11行代码；带两个参数时，列出指定范围的代码。
- `n(ext)`：继续执行程序，直到达到下一行。
- `c(ont(inue))`：继续执行程序，直到遇到下一个断点。
- `s(tep)`：执行当前行，并在可能的话停在第一个能停的地方（例如函数或方法调用中）。
- `r(eturn)`：继续执行，直到当前函数返回。
- `p(rint) expression`：打印表达式的值。
- `q(uit)`：放弃程序运行，退出调试器。
- `h(elp) [command]`：提供命令的帮助信息，不带参数时列出所有命令。

在Python 3.7及以上版本中，你可以在代码中的任何位置使用 `breakpoint()` 函数来设置断点。当 `pytest` 运行到这行代码时，它会自动进入调试模式。

```python
def test_example():
    # ... 一些测试代码 ...
    breakpoint()  # 测试运行到这里会暂停并进入调试模式
    # ... 更多的测试代码 ...
```

在 Python 3.6 及以下版本，需要手动导入 `pdb` 并调用 `pdb.set_trace()`：

```python
import pdb

def test_example():
    # ... 一些测试代码 ...
    pdb.set_trace()  # 测试运行到这里会暂停并进入调试模式
    # ... 更多的测试代码 ...

def calculate_division(a, b):
    breakpoint()  # 设置断点
    return a / b
```

## 使用 `pytest.set_trace()` 进行更精细的控制

`pytest` 也提供了它自己的 `set_trace` 方法，它可以在 `pdb` 调试器中提供更好的集成，比如更清晰的堆栈跟踪和更好的输出格式。

```python
import pytest

def test_example():
    # ... 一些测试代码 ...
    pytest.set_trace()  # 测试运行到这里会暂停并进入调试模式
    # ... 更多的测试代码 ...
```

## 使用 `--trace` 选项

如果你想在每个测试的开始时自动进入调试器，可以使用 `--trace` 选项。这将在每个测试之前自动调用 `pytest.set_trace()`，非常适合那些想逐个步骤运行整个测试的情况。

```shell
pytest --trace my_test_file.py
```

## 使用 `pytest.fail()` 输出额外信息

`pytest.fail()` 函数可以在测试中任意位置调用，它会立即标记测试为失败，并可以提供额外的输出信息。这对于调试复杂的问题非常有用，因为你可以在测试失败时输出有用的调试信息。

```python
import pytest

def test_example():
    if not some_condition():
        pytest.fail("some_condition is not met, debug info: ...")
```

## 配置日志输出

`pytest` 允许你控制日志的输出级别，这可以通过命令行选项来完成，如 `--log-cli-level`。

```shell
pytest --log-cli-level=DEBUG my_test_file.py
```

这将会在控制台上输出 `DEBUG` 级别的日志信息，这可以帮助你理解测试失败的上下文。



## `PYTEST_CURRENT_TEST` 

`pytest` 有一个内置的环境变量叫做 `PYTEST_CURRENT_TEST`，在测试运行时，这个环境变量用于存储当前正在运行的测试项的名称和路径，通常用于调试目的，比如当你想要在日志信息中包含当前执行的测试项名称时，也可以在测试失败时在 teardown 钩子中对其进行检查和使用，或者在一些特殊情况下，你需要在测试执行时获知哪个测试正在运行。

`PYTEST_CURRENT_TEST` 环境变量的值包含了测试文件的路径、模块名称、类名称（如果适用）和测试函数或方法的名称。格式通常如下所示：

```shell
file_path::module_name::class_name::function_name
```

如果测试不在类内部，那么格式将会排除类名称：

```shell
file_path::function_name
```

如果你有以下的测试用例：

```python
# content of test_env_example.py

def test_example():
    assert True
```

当 `test_example` 运行时，`PYTEST_CURRENT_TEST` 现在的值可能如下：

```shell
test_env_example.py::test_example
```

并且如果你想在每个测试函数开始或结束时打印其名称，你可以使用 `pytest` 钩子：

```python
# content of conftest.py
import os
import pytest

# 钩子函数，在每个测试调用时运行
def pytest_runtest_call(item):
    current_test = os.environ.get('PYTEST_CURRENT_TEST')
    # 注意：在测试开始之前，'current_test' 可能是 None。确保你在 'pytest_runtest_call' 钩子或之后的钩子中访问它。
    if current_test:
        test_name = current_test.split(' ')[0]
        print(f"\nRUNNING TEST: {test_name}")

# 钩子函数，在生成每个测试报告时运行
def pytest_runtest_logreport(report):
    if report.when == 'call':
        current_test = os.environ.get('PYTEST_CURRENT_TEST')
        if current_test:
            test_name = current_test.split(' ')[0]
            print(f"\nTEST REPORT FOR: {test_name}")
```

在该代码中，我们使用 `pytest_runtest_call` 和 `pytest_runtest_logreport` 钩子，在每个测试开始之前和结束之后获取和打印出当前测试的名称，如下：

```shell
collected 1 item

test_env_example.py::test_example 
RUNNING TEST: chapter1-12/test_env_example.py::test_example
PASSED
TEST REPORT FOR: chapter1-12/test_env_example.py::test_example
```

**请注意：**

- `PYTEST_CURRENT_TEST` 更多的是为了内部使用或调试，不建议在测试逻辑中依赖它，因为这可能会违反测试的独立性原则。
- 使用该环境变量可能会与 `pytest` 的某些并行执行机制不兼容，比如当使用 `pytest-xdist` 插件进行并行测试时。

`PYTEST_CURRENT_TEST` 环境变量为 `pytest` 用户提供了一种方法来获得当前正在执行的测试项的详细信息。这可以用于日志记录、调试，以及在测试执行环境中识别当前的测试状态。然而，一般情况下，推荐使用 `pytest` 提供的钩子和内置的 fixture 来访问关于当前测试的信息，而不是直接依赖环境变量。



# 其他调试方法

`pytest`是基于Python 开发的一款自动化框架，自然一些程序的调测离不开Python 其他的调试方法，接下来我们将详细介绍`pysnooper`和`snoop`调试库，这些工具和技术可以帮助自动化开发者更高效地进行调试。

## pysnooper

`PySnooper` 是一个非常实用的 Python 调试库，它的主要功能是自动记录函数的执行过程，无需在代码中设置断点，这对于理解复杂函数的行为或者追踪错误来源非常有帮助。

### 安装 pysnooper

``` shell
pip install pysnooper
```

### 利用pysnooper调试


示例代码


```python
# content of debug_pysnooper.py
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pysnooper


@pysnooper.snoop()
def remove_dup_element(a_list):
    return {}.fromkeys(a_list).keys()


if __name__ == '__main__':
    a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
    remove_dup_element(a_list)
```


输出结果：

```shell
root@Gavin:~/code/chapter1-12# python3 debug_pysnooper.py 
Source path:... /root/code/chapter1-12/debug_pysnooper.py
Starting var:.. a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
14:32:33.017424 call         8 def remove_dup_element(a_list):
14:32:33.018634 line         9     return {}.fromkeys(a_list).keys()
14:32:33.019145 return       9     return {}.fromkeys(a_list).keys()
Return value:.. dict_keys([10, 9, 1, 2, 3, 5, 6, 7, 8])
Elapsed time: 00:00:00.002518
root@Gavin:~/code/chapter1-12# 
```

它将每一行变量的值都输出到屏幕上，仅仅需要写一行代码（使用装饰器）就可以实现这个方便的调试功能，比起一行行写print，方便了很多。

如果代码执行过程比较长，输出到屏蔽不方便的话，可以输出到log文件中，在装饰器那行加上log文件路径即可：

```python
@pysnooper.snoop('/var/log/output.log')
def remove_dup_element(a_list):
    return {}.fromkeys(a_list).keys()
```

下面是一个如何在 `pytest` 测试中使用 `PySnooper` 的例子：

```python
# content of test_debug_with_pysnooper.py
import pytest
import pysnooper

# 被测试的函数
def complex_function(a, b):
    result = a + b  # 这里是一些复杂的逻辑
    return result

# 测试函数
@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (4, 5, 9)])
@pysnooper.snoop()  # 添加装饰器来跟踪测试函数
def test_complex_function(a, b, expected):
    assert complex_function(a, b) == expected
```

在这个例子中，`test_complex_function` 测试了 `complex_function` 函数。通过添加 `@pysnooper.snoop()` 装饰器，测试的执行过程会被记录下来。默认情况下，`PySnooper` 会把跟踪信息打印到标准输出，但你也可以通过传递参数来指定输出文件：

```shell
@pysnooper.snoop(output='snoop_log.txt')
```

这样，所有的跟踪信息就会被写入到 `snoop_log.txt` 文件中，不会污染你的测试输出。

需要注意的是，虽然 `PySnooper` 对调试单独的函数非常有用，但在大型测试套件中过度使用可能会生成难以管理的大量输出。因此，最好只在调试特定的问题时临时使用它，而不是在所有测试中都使用。



## snoop

`snoop` 是一个用于 Python 的调试库，它可以让开发者更容易地理解代码的行为。与传统的调试器如 `pdb` 不同，`snoop` 通过在代码中添加装饰器自动记录函数内部的活动来帮助调试，而无需单步执行。这使得它尤其适合对复杂函数或存在问题的代码进行详细的运行时分析。

### 安装 snoop

``` shell
pip install snoop
```

### 利用snoop调试


示例代码：

```python
# content of debug_snoop.py
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import snoop


@snoop
def remove_dup_element(a_list):
    return {}.fromkeys(a_list).keys()


if __name__ == '__main__':
    a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
    remove_dup_element(a_list)
```


输出结果：


```shell
root@Gavin:~/code/chapter1-12# python3 debug_snoop.py 
14:38:26.92 >>> Call to remove_dup_element in File "/root/code/chapter1-12/debug_snoop.py", line 8
14:38:26.92 ...... a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
14:38:26.92 ...... len(a_list) = 14
14:38:26.92    8 | def remove_dup_element(a_list):
14:38:26.92    9 |     return {}.fromkeys(a_list).keys()
14:38:26.92 <<< Return value from remove_dup_element: dict_keys([10, 9, 1, 2, 3, 5, 6, 7, 8])
root@Gavin:~/code/chapter1-12# 
```

以下是一个简单的示例来演示如何在`pytest`测试中使用`snoop`：

```python
# content of test_debug_with_snoop.py
# 假设这是你要测试的函数
def function_to_test(x):
    y = x + 1
    z = y * y
    return z

# 这是pytest的测试函数
import snoop
import pytest

@snoop
def test_function_to_test():
    assert function_to_test(3) == 16  # 3 + 1 = 4, 4 * 4 = 16
```

当你运行`pytest`时，`test_function_to_test`函数中的`snoop`装饰器会自动记录函数的执行过程，并将详细的跟踪信息打印到控制台。

如果你想将`snoop`的输出重定向到文件中，可以在装饰器中提供一个输出文件名：

```shell
@snoop(output='function_trace.log')
def test_function_to_test():
    assert function_to_test(3) == 16
```

这样，所有的调试信息将会被写入到`function_trace.log`文件中，而不是打印到控制台。

请记住，当你在调试完毕后，可能需要移除或注释掉`snoop`装饰器，特别是在生产代码或大规模的测试套件中，以避免产生不必要的性能影响和日志文件。使用`snoop`时应该是一个临时的调试措施，而不是你的测试代码的常态。



# pysnooper vs. snoop vs. pdb

对三个流行的 Python 调试工具进行详细的对比分析。

## pysnooper

pysnooper 是一个简单的调试工具，旨在通过自动化的日志记录来简化调试过程。

- **特点**:
  - 自动记录函数调用、变量值和执行时间等。
  - 无需设置断点，添加装饰器即可使用。
  - 输出日志至标准输出或者文件。
- **优势**:
  - 易于设置和使用，适合快速调试和跟踪。
  - 无需更改现有的代码逻辑。
- **局限**:
  - 日志可能会非常冗长，难以用于大型项目的全面调试。

## snoop

snoop 是 pysnooper 的改进和替代工具，提供类似的跟踪功能，但有更多的高级特性。

- **特点**:
  - 提供丰富的配置选项，如进行条件跟踪等。
  - 支持临时变量和表达式的跟踪。
  - 支持彩色输出，使得日志更加易读。
- **优势**:
  - 更高级的跟踪控制。
  - 更多的输出定制化选项。
- **局限**:
  - 跟 pysnooper 一样，输出可能较多，不适合在生产环境中使用。

## pdb

pdb 是 Python 自带的交互式源代码调试器，是官方标准库的一部分。

- **特点**:
  - 提供了丰富的命令用于控制代码执行、设置断点、查看和修改变量等。
  - 允许开发者逐行执行代码，并在任意位置停止。
  - 开发者可以在断点处与解释器进行交互。
- **优势**:
  - 无需任何外部依赖，是 Python 开发环境的核心一部分。
  - 提供深入的调试能力，适用于复杂的代码问题。
- **局限**:
  - 学习曲线相比自动化的跟踪工具要陡峭。
  - 调试过程可能较为繁琐，特别是对于大型应用。

以下表格比较了这三种调试工具的主要特性和使用场景：


| 特性/工具 | PySnooper        | snoop                          | pdb                          |
| --------- | ---------------- | ------------------------------ | ---------------------------- |
| 类型      | 自动日志记录工具 | 自动日志记录工具               | 交互式调试工具               |
| 主要用途  | 简单的代码跟踪   | 高级代码跟踪                   | 深入代码调试                 |
| 设置      | 装饰器           | 装饰器，上下文管理器           | 代码内断点，命令行           |
| 输出      | 标准输出/文件    | 标准输出/文件，支持彩色输出    | 控制台                       |
| 调试控制  | 无需交互         | 更详细的跟踪控制，如条件跟踪等 | 完全交互式，多命令           |
| 学习曲线  | 低               | 低                             | 中到高                       |
| 适用性    | 小型项目快速调试 | 复杂跟踪需求，但又需便利性     | 复杂问题调试或需要交互式环境 |

选择哪个调试工具取决于调试任务的复杂性、你对调试过程控制的需求以及个人对调试工具的熟悉度。


这个表只是一个简单的概述，具体哪个工具更适合你的开发环境和工作流程可能还需要更深入的研究和个人实践。



# 本章小结

本章介绍了`pytest`的调试方法，以及`python`常用的调试方法：

- **pysnooper** 和 **snoop** 都侧重于自动日志记录，易于使用，对初级开发者友好，非常适合于快速调试和问题定位。
- **pdb** 提供了更为深入和细致的调试控制，适合有经验的开发者针对复杂问题进行调试。

各个调试工具各有所长，选择合适的调试工具取决于你的具体调试需求，以及你愿意投入的时间和学习精力。
