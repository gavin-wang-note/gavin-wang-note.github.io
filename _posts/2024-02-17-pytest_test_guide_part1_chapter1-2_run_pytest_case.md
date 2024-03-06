---
title: 《pytest测试指南》-- 章节1-2 pytest测试用例执行 
date: 2024-02-17 22:10:51
author: Gavin Wang
img: "/img/pytest/pytest-3.png"
top: false
hide: false
cover: true
coverImg:
password: Huawei123!
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 章节1-2 pytest测试用例执行。
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



在自动化测试项目中，测试框架运行时需要先搜索测试文件/模块（即测试用例目录下的.py文件），然后在测试文件/模块中搜索测试类或测试函数，接着在测试类中搜索测试函数/测试方法，最后加入到队列中，再按执行顺序执行测试。

所以，只有测试文件/模块、测试类、测试方法/测试函数都符合命名规则，框架才能去识别、执行测试用例。

接下来我们来了解一下 `pytest` 框架中的用例搜索和测试命名规则。

# 2.1 pytest 测试搜索规则

`pytest`默认搜索规则如下：

- 如果`pytest`执行命令中指定了目录，则从该指定目录中开始查找测试用例文件，如果没有指定，则从当前运行目录开始查找文件，最终的结果是找到整个项目中符合命名规则的测试用例。
- 会查找整个项目中符合命令规则的测试模块，再由 测试文件/模块-->测试类-->测试方法/测试函数 一层层递归查找。

# 2.2 pytest 测试默认命名规则

`pytest` 是遵循一定的命名规则来发现和识别测试用例的。以下是`pytest`的一些基本命名规则：

## 2.2.1 测试文件命名规则

- 测试文件通常以 `test_` 开头或以 `_test` 结尾（例如 `test_example.py` 或 `example_test.py`）。

## 2.2.2 测试类命名规则

- 测试类必须以 `Test` 开头，并且不能有 `__init__` 方法。
- 类中的测试方法必须以 `test` 开头。

例子：

```python
# 正确的测试类命名
class TestExample:

    # 正确的测试方法命名
    def test_functionality(self):
        assert True
        
# 错误的测试类命名，不会自动识别为测试类
class ExampleTest:

    # 即便方法命名正确，该方法也不会被执行
    def test_functionality(self):
        assert True
```

## 2.2.3 测试函数命名规则

- 测试函数必须以 `test` 开始。
- 测试函数应该使用描述性的名称，方便在测试报告中识别。

例子：

```python
# 正确的测试函数命名
def test_specific_functionality():
    assert 1 + 1 == 2
    
# 错误的测试函数命名，不会被自动识别为测试函数
def check_specific_functionality():
    assert 1 + 1 == 2
```

## 2.2.4 fixture命名规则

- `fixture` 是使用 `@pytest.fixture` 装饰器定义的函数，没有特定的命名要求，尽管通常会用表述性的名称来说明它们提供的上下文。
- 在测试函数或类中，`fixture` 通过名称被引用。

例子：

```python
@pytest.fixture
def example_fixture():
    # setup code
    return some_data

def test_needs_fixture(example_fixture):
    assert example_fixture == some_data
```

遵循这些命名规则是很重要的，因为`pytest`使用这种约定来自动识别和收集要执行的测试。不遵守这些规则可能会导致某些测试无法被`pytest`发现和执行。

汇总如下：

| 类型              | 规则                                                  | 示例                                                         |
| ----------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| 文件/测试模块     | test_开头 或者 _test 结尾                             | ```test_ad_account.py```，或以 _test 结尾，如：```ad_account_test.py``` |
| 测试类            | 必须以`Test`开头命名，且测试类中不能有 \__init__ 方法 | ```class TestAccountAD():```                                 |
| 测试方法/测试函数 | 必须以test_开头                                       | ```test_ad_ldap_settings()``` 或 ```testADLDAPSettings()```  |
| 包名              | 无要求，符合python命名规范即可                        |                                                              |

注意：

* 测试类中不可以添加`__init__`构造函数；
* 最好是将测试模块、测试方法/函数都以 test_ 开头命名，这样可读性会更强。



# 2.3 测试用例执行方式

`pytest`运行方式主要有三种，main()函数运行、终端运行和main()结合配置文件方式运行，接下来将以几个示例进行分别演示。

## 2.3.1 main()函数运行

* 运行所有测试用例：`pytest.main()`
* 运行指定路径的用例：`pytest.main( ["./路径"] )`
* 运行指定模块的用例：`pytest.main( ["模块名.py"] )`
* 运行指定用例：`pytest.main( [ " ./路径/模块名::类名::方法"] )`

### 2.3.1.1 pytest的main()函数介绍

在讲述main函数运行用例之前，我们先来看一下`pytest`的`main`函数（源码`src/_pytest/config/__init__.py`文件下）：

```python
def main(
    args: Optional[Union[List[str], "os.PathLike[str]"]] = None,
    plugins: Optional[Sequence[Union[str, _PluggyPlugin]]] = None,
) -> Union[int, ExitCode]:
    """Perform an in-process test run.

    :param args:
        List of command line arguments. If `None` or not given, defaults to reading
        arguments directly from the process command line (:data:`sys.argv`).
    :param plugins: List of plugin objects to be auto-registered during initialization.

    :returns: An exit code.
    """
    try:
        try:
            config = _prepareconfig(args, plugins)
        except ConftestImportFailure as e:
            exc_info = ExceptionInfo.from_exc_info(e.excinfo)
            tw = TerminalWriter(sys.stderr)
            tw.line(f"ImportError while loading conftest '{e.path}'.", red=True)
            exc_info.traceback = exc_info.traceback.filter(
                filter_traceback_for_conftest_import_failure
            )
            exc_repr = (
                exc_info.getrepr(style="short", chain=False)
                if exc_info.traceback
                else exc_info.exconly()
            )
            formatted_tb = str(exc_repr)
            for line in formatted_tb.splitlines():
                tw.line(line.rstrip(), red=True)
            return ExitCode.USAGE_ERROR
        else:
            try:
                ret: Union[ExitCode, int] = config.hook.pytest_cmdline_main(
                    config=config
                )
                try:
                    return ExitCode(ret)
                except ValueError:
                    return ret
            finally:
                config._ensure_unconfigure()
    except UsageError as e:
        tw = TerminalWriter(sys.stderr)
        for msg in e.args:
            tw.line(f"ERROR: {msg}\n", red=True)
        return ExitCode.USAGE_ERROR
```

`main` 函数是 `pytest` 测试的编程入口点，允许从 Python 代码中直接运行测试，以下是对代码各部分的详细解释。

#### 2.3.1.1.1 参数部分

```python
def main(
    args: Optional[Union[List[str], "os.PathLike[str]"]] = None,
    plugins: Optional[Sequence[Union[str, _PluggyPlugin]]] = None,
) -> Union[int, ExitCode]:
```

`args`：这个参数可以是字符串列表，也可以是支持路径协议的对象（比如 `Path` 对象或任何实现了 `__fspath__` 方法的对象）。这个参数是可选的（`Optional`），如果为空 (`None`)，`pytest` 将默认读取命令行参数 (`sys.argv`)。

`plugins`: 这个参数可以是插件对象（`_PluggyPlugin`）的序列，或者是插件模块名的字符串列表，它是用来在初始化时自动注册提供的插件。这个参数也是可选的。

返回值：函数返回一个整数 (`int`) 或 `ExitCode` 枚举实例。这代表了`pytest`运行后的退出码，用来指示测试的整体结果。

#### 2.3.1.1.2 函数实现

接下来的代码块是`main`函数的实际实现：

```python
try:
    try:
        config = _prepareconfig(args, plugins)
        # ...
```

这里，函数通过调用 `_prepareconfig` 函数来准备测试运行的配置，`args` 和 `plugins` 参数在此环节被使用。

如果在配置阶段发生了导入错误（`ConftestImportFailure`），它会捕获异常，向终端（`stderr`）输出相关的错误信息，并返回一个特定的退出码（`ExitCode.USAGE_ERROR`）。

如果配置成功，会执行这部分代码：

```python
ret: Union[ExitCode, int] = config.hook.pytest_cmdline_main(config=config)
```

这行代码是运行测试的关键调用，它使用`pytest`的内部钩子（`hook`）机制来执行命令行主函数流程。这个流程会执行解析后的配置文件和插件中定义的测试用例。

最后，代码块还包含了这样的结构，用于确保在测试运行完成后执行取消配置操作：

```python
finally:
    config._ensure_unconfigure()
```

最终，若函数执行过程中引发了 `UsageError` 异常，则会显示一个错误消息，并返回 `USAGE_ERROR` 的退出码。其它情况下，函数返回测试的退出码 （`ret`），表示测试运行的结果。

### **2.3.1.2 main() 命令行参数详情**

说明：

下述命令行参数只是部分，更详细的参数介绍，请参考下一章节内容，此处仅做部分示例先介绍一下。

* -s: 显示程序中的print/logging输出
* -v: 丰富信息模式, 输出更详细的用例执行信息
* -q: 安静模式, 不输出环境信息
* -x: 出现一条测试用例失败就退出测试。调试阶段非常有用
* -k：可以使用and、not、or等逻辑运算符，区分：匹配范围（文件名、类名、函数名）

当传入参数 `-s -v -x` 时，相当于命令行输入 `pytest -s -v -x`：

```python
if __name__ == '__main__':
    pytest.main(["-s", "-v", "-x"])
```

当传入参数 `-q` 时，相当于命令行输入 `pytest -q`：

```python
if __name__ == '__main__':
        pytest.main(["-q"])
```

运行当前目录和子目录下所有（`test_*.py` 和 `*_test.py`）的用例：

```python
if __name__ == '__main__':
    pytest.main(["./"])
    # pytest.main() 默认也可以
```

也可以参数、路径/文件一起指定，参考如下：

比如匹配包含`migration`的用例(匹配目录名、模块名、类名、用例名)：

```python
pytest.main(['-k','migration', '-v'])
```

比如匹配`test_loop_device.py`模块下包含`migration`的用例：

```python
pytest.main(['-k','migration',"./test_loop_device.py", '-v'])
```

### 2.3.1.3 示例参考

```shell
root@Gavin:~/code# ll
total 40
drwxr-xr-x  4 root root  4096 Dec  4 13:53 ./
drwx------ 11 root root  4096 Dec  4 13:53 ../
drwxr-xr-x  2 root root  4096 Dec  4 13:53 chapter1-2/
-rw-r--r--  1 root root   582 Dec  2 10:30 clear_pyc.py
-rw-r--r--  1 root root   505 Dec  4 13:40 main.py
-rw-r--r--  1 root root 13688 Dec  2 18:30 .pylintrc
drwxr-xr-x  2 root root  4096 Dec  4 11:26 tools/
root@Gavin:~/code# cd chapter1-2/
root@Gavin:~/code/chapter1-2# ls -l
total 4
-rw-r--r-- 1 root root 716 Dec  4 11:57 test_case_run.py
root@Gavin:~/code/chapter1-2# 
```

在`/root/cood/chapter1-2`目录下创建了 ``` test_case_run.py ``` 文件，在上一层目录(`/root/code`)下创建了 ``` main.py``` 文件：

 ``` test_case_run.py ``` 文件内容如下：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
Here's an example of how a pytest test case runs
"""


def test_list_length_check():
    """  Test case of 'List length checking'  """
    assert len(list(range(6))) > len(list(range(1, 10, 3)))


def test_lowercase_alphabet():
    """  Test case of lowercase alphabet  """
    lowercase_alphabet = [chr(i) for i in range(97, 123)]
    assert 'a' in lowercase_alphabet, f"[ERROR]  The letter 'a' is not in : {lowercase_alphabet}."


def test_uppercase_alphabet():
    """  Test case of uppercase alphabet  """
    uppercase_alphabet = [chr(i) for i in range(65, 91)]
    assert 'a' not in uppercase_alphabet, f"[ERROR]  The letter 'a' not in : {uppercase_alphabet}"


class TestClass():
    """  Test class   """
    def test_lower_character(self):
        """  Check the lower character  """
        assert 'a' in "Apple".lower()

    def test_check_os_type(self):
        """  OS should be Linux  """
        assert 'Linux' == platform.system()
```

说明：

`chr(i)`的作用是将`ascii`码转换为对应字母，字母a对应的ASCII码是97，因此`chr(97)`就代表了字母a。

问：

如果我不知道字母a对应的ASCII码是97，那么我们应该怎么快速生成一个a到z的字符列表呢？

答：

使用函数 `ord()`，这个函数可以说是`chr()`的逆运算了，它的作用是返回一个字符对应的ASCII码。
于是我们就可以这样获得一个a到z的字符列表了：

```lowercase_alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]```

同理，我们也可以快速生成一个'A'到'Z'的列表：

```uppercase_alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1)]```



``` main.py``` 文件内容如下：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
This is a main function.
Example of how to execute test cases through the main function.
"""

import pytest


if __name__ == '__main__':
    # # 执行所有函数
    pytest.main()

    # # 执行指定testcase路径下的用例
    pytest.main(["./chapter1-2"])

    # # 执行模块
    pytest.main(["./chapter1-2/test_case_run.py"])

    # # 执行类
    pytest.main(["./chapter1-2/test_case_run.py::TestClass"])

    # 只执行 test_uppercase_alphabet 用例
    pytest.main(["./chapter1-2/test_case_run.py::test_uppercase_alphabet"])

    # 只执行类下的某个用例
    pytest.main(["./chapter1-2/test_case_run.py::TestClass::test_check_os_type"])
```

执行效果如下：

```shell
root@Gavin:~/code# python3 main.py 
================================ test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

chapter1-2/test_case_run.py .....                                       [100%]

================================= 5 passed in 0.01s ===========================
================================= test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

chapter1-2/test_case_run.py .....                                       [100%]

================================== 5 passed in 0.01s ===========================
================================== test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

chapter1-2/test_case_run.py .....                                       [100%]

================================== 5 passed in 0.01s ===========================
================================== test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 2 items

chapter1-2/test_case_run.py ..                                          [100%]

================================== 2 passed in 0.00s ===========================
================================== test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

chapter1-2/test_case_run.py .                                           [100%]

================================== 1 passed in 0.00s ===========================
================================== test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

chapter1-2/test_case_run.py .                                           [100%]

================================== 1 passed in 0.00s ===========================
root@Gavin:~/code#
```



 ## 2.3.2 pytest命令行运行

* 运行所有测试用例：`pytest`
* 运行指定路径的用例：`pytest ./路径`
* 运行指定模块的用例：`pytest 模块名`
* 运行指定用例：`pytest ./路径/模块名::类名::方法`

依然是上面的测试用例，执行效果如下： 

### **2.3.2.1 运行所有测试用例**

直接执行`pytest`命令，如下所示：

```shell
root@Gavin:~/code/chapter1-2# pytest
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

test_case_run.py .....                                                  [100%]

============================= 5 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-2#
```

因为当前目录下只有这一个测试用例文件，所以只执行了上面的`test_case_run.py`文件。

### **2.3.2.2 运行指定路径的测试用例**

给`pytest`指定目录，则会执行此目录下所有的测试用例，如下所示：

```shell
root@Gavin:~/code/chapter1-2# cd ..
root@Gavin:~/code# pytest chapter1-2/
================================= test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

chapter1-2/test_case_run.py .....                                        [100%]

================================ 5 passed in 0.01s =============================
root@Gavin:~/code#
```

### **2.3.2.3 运行指定模块的用例**

执行`pytest 模块/文件名`，如下所示：

```shell
root@Gavin:~/code/chapter1-2# pytest test_case_run.py 
============================== test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

test_case_run.py .....                                                  [100%]

============================== 5 passed in 0.01s ===============================
root@Gavin:~/code/chapter1-2#
```

### **2.3.2.4 运行指定用例**

有两种方式：

* 不在`class`下的测试用例指定：`pytest ./路径/模块名::函数名`
* 在`class`下的测试用例指定：`pytest ./路径/模块名::类名::函数名`

`pytest ./路径/模块名::函数名` 方式，示例如下：

```shell
root@Gavin:~/code/chapter1-2# pytest test_case_run.py::test_uppercase_alphabet
============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_case_run.py .                                                      [100%]

============================== 1 passed in 0.00s =============================
root@Gavin:~/code/chapter1-2#
```

`pytest ./路径/模块名::类名::函数名` 方式，示例如下：

```shell
root@Gavin:~/code/chapter1-2# pytest test_case_run.py::TestClass::test_lower_character
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_case_run.py .                                                      [100%]

============================== 1 passed in 0.00s ==============================
root@Gavin:~/code/chapter1-2#
```



## 2.3.3 使用配置文件运行程序

### 2.3.3.1 配置文件规则

借助`pytest.ini`全局配置文件，更改`pytest`默认行为，用例在执行时，遵循如下参数读取规则：

* 如`pytest.ini`有该参数值，在执行的时候，先读取配置文件中的参数；
* 如没有，则取其他地方的（主函数/命令行中）。



说明：

* 文件名是固定的，不允许更改；
* 存放路径：必须放在根目录（或代码执行入口的顶层目录）



### 2.3.3.2 配置文件格式

`pytest.ini` 文件内容：

```shell
[pytest]
addopts  =  -vs            # 命令行参数，多个命令用空格分隔
testpaths = ./             # 测试用例的路径
python_files = test*.py    # 配置测试搜索的模块文件名称（模块名的规则）
python_class = Test*       # 配置测试搜索的类名 （类名的规则）
python_function = test     # 配置测试搜索的测试函数名 （方法名的规则）
```

说明：

* 上述配置文件中 **井号** 前的空格和后面的注释内容，在实际使用时需删除掉，这里为了方便大家理解而加；
* 上述配置文件表示，执行所有路径下按照`pytest`默认规则命名的测试用例。这相当于主函数`pytest.main()`和终端运行的`pytest`；
* 主函数和终端命令运行程序时，都会读取配置文件的信息，因此可以根据情况修改配置参数来执行对应的测试用例，在main函数和终端无需在添加参数。



### 2.3.3.3 示例参考

在原有目录下新增一 ``` test_sample.py``` 测试用例文件，内容如下：

```python
root@Gavin:~/code# cd chapter1-2/
root@Gavin:~/code/chapter1-2# ll
total 36
drwxr-xr-x 2 root root 4096 Dec 5 08:58 ./
drwxr-xr-x 7 root root 4096 Dec 5 19:17 ../
-rw-r--r-- 1 root root 1014 Dec 3 19:10 test_case_run.py
-rw-r--r-- 1 root root  744 Dec 4 08:51 test_order_sample_1.py
-rw-r--r-- 1 root root  239 Dec 4 08:12 test_order_sample_2.py
-rw-r--r-- 1 root root  248 Dec 4 08:12 test_sample.py
-rw-r--r-- 1 root root  226 Dec 4 08:12 test_script.py
-rw-r--r-- 1 root root 1009 Dec 4 08:12 test_various_statuses.py
-rw-r--r-- 1 root root  389 Dec 4 08:12 test_with_exit.py
root@Gavin:~/code/chapter1-2# 
root@Gavin:~/code/chapter1-2# cat test_sample.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
Here's a test sample
"""


def increasing_by_one(x):
    """  Increasing by one  """
    return x + 1


def test_answer():
    """  Test case of an answer   """
    assert increasing_by_one(3) == 5
root@Gavin:~/code/chapter1-2#
```

只执行`test_sample.py`模块的用例。将配置文件中的`testpaths`参数值更改为`./chapter1-2`，将`python_files`的参数值改为`test_sample.py`； 或者将` testpaths` 直接修改为 `./chapter1-2/test_sample.py`，如下文所示，两者效果相同：

```shell
[pytest]
addopts  =  -vs
testpaths = ./chapter1-2
python_files = test_sample.py
python_classes = Test*
python_functions = test
```

效果同上：

```shell
[pytest]
addopts  =  -vs
testpaths = ./chapter1-2/test_sample.py
python_files = test*
python_classes = Test*
python_functions = test
```

执行效果如下： ![chatp1-2-pytest_ini_run_cases](../image/chatp1-2-pytest_ini_run_cases.png)

附带执行文本，有一行`configfile: pytest.ini`记录，表明有使用`pytest.ini`文件：

```shell
root@Gavin:~/code/chapter1-2# pytest
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_sample.py::test_answer FAILED

=============================== FAILURES ======================================
_______________________________ test_answer ___________________________________

    def test_answer():
        """  Test case of an answer   """
>       assert increasing_by_one(3) == 5
E       assert 4 == 5
E        +  where 4 = increasing_by_one(3)

test_sample.py:16: AssertionError
=============================== short test summary info =======================
FAILED test_sample.py::test_answer - assert 4 == 5
=============================== 1 failed in 0.03s =============================
root@Gavin:~/code/chapter1-2#
```

`pytest`可以通过不同颜色和输出信息直观地展示这些状态。在使用命令行运行`pytest`时，可以通过命令行标志来调整输出的详细程度。例如，`-v`或`--verbose`可以提供更详细的输出。最终报告会显示每个状态的总计摘要，告知你测试套件的整体健康情况。



# 2.4 pytest用例的状态

在使用`pytest`执行测试时，测试用例可以有几种不同的状态，它们指示了测试的结果和执行情况。下面是详细的解释：

## 2.4.1 PASSED（.）

- **PASSED** 表示测试用例已成功执行且所期望的断言（assertions）全部为真（true）。这是理想状态，表示测试符合预期。

## 2.4.2 FAILED（F）

- **FAILED** 状态意味着测试用例中的至少一个断言不为真，即测试结果与期望不符。`pytest`在这种情况下会提供详细的失败报告，包括出错的代码位置和相应的错误信息。

## 2.4.3 SKIPPED（s）

- **SKIPPED** 测试是那些没有执行的测试。测试用例可能被有意地跳过，原因可能包括：
  - 条件跳过：使用如`@pytest.mark.skip`装饰器，可以在满足某个条件时跳过测试。
  - 条件跳过如果：使用`@pytest.mark.skipif`装饰器，在特定条件成立时跳过测试。
  - 依赖性跳过：使用`pytest.skip()`函数，可以在测试函数或设置代码中进行动态跳过决策。
  - 不满足测试要求：如果没有满足运行测试的必要条件，`pytest`可能会选择跳过某些测试。

## 2.4.4 XFAIL（x）

- **XFAIL** 状态表示测试用例因为被标记为预期会失败（使用`@pytest.mark.xfail`）而失败了，但这被认为是正常的。使用`xfail`是为了标识那些由于已知缺陷或待实现的功能而可能失败的测试，但您不希望这些失败影响整体测试套件的状态。

## 2.4.5 XPASS（X）

- **XPASS** 状态意味着被标记为`@pytest.mark.xfail`的测试实际上通过了。这通常是意外的，并且可能指示之前的一个问题已被解决，或者标记不再适用。

## 2.4.6 ERROR（E）

- **ERROR** 状态不是指测试用例中的断言失败，而是指在运行测试用例之前（如在设置/夹具或拆卸函数中）或运行测试用例之后（测试完成之后的拆卸步骤）发生了错误。比如说，测试环境的配置问题或外部资源无法访问，这些错误会导致测试无法正常进行。

示例：

创建一个名称为 `test_various_statuses.py` 的文件，并粘贴以下代码：

```python
root@Gavin:~/code/chapter1-2# cat test_various_statuses.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


import pytest


# 这个测试会通过
def test_passed():
    assert True


# 这个测试会失败
def test_failed():
     assert False


# 这个测试主动抛异常会失败
def test_failed_raise():
    raise Exception("An unexpected error occurred")


# 这个测试会被标记为预期失败，但如果通过了，它将被标记为XPASS
@pytest.mark.xfail
def test_xpass():
   assert True


# 这个测试被标记为预期失败，并且它确实失败了，因此它将被标记为XFAIL
@pytest.mark.xfail
def test_xfailed():
    assert False


# 这个测试会被跳过
@pytest.mark.skip(reason="This test is skipped for demonstration purposes")
def test_skipped():
    assert True


# 使用一个会发生错误的fixture
@pytest.fixture
def error_fixture():
    raise Exception("Error in fixture")


# 这个测试使用了一个错误的fixture，即使测试代码本身是正常的
def test_with_error_fixture(error_fixture):
    assert True
root@Gavin:~/code/chapter1-2#
```

现在，运行这个测试文件：

```bash
pytest test_various_statuses.py
```

你会看到以下各种结果状态：

```shell
test_various_statuses.py::test_passed PASSED
test_various_statuses.py::test_failed FAILED
test_various_statuses.py::test_failed_raise FAILED
test_various_statuses.py::test_xpass XPASS
test_various_statuses.py::test_xfailed XFAIL
test_various_statuses.py::test_skipped SKIPPED (This test is skipped for demonstration purposes)
test_various_statuses.py::test_with_error_fixture ERROR
```

- `test_passed` 会标示绿色的 `.`（点）表示成功（`PASSED`）。
- `test_failed` 会标示为红色的 `F` 表示失败（`FAILED`）。
- `test_failed_raise` 会标示为红色的 `F` 表示失败（`FAILED`）。
- `test_xpass` 会标示为黄色的 `X` 表示预期失败却通过了（`unexpectedly passing or XPASS`）。
- `test_xfailed` 会标示为黄色的 `x` 表示预期失败（`expected fail or XFAIL`）。
- `test_skipped` 会标示为黄色的 `s`，表示被跳过（`SKIPPED`）。
- `test_with_error_fixture` 也会标示为红色的 `E`，表示错误（`ERROR`）因为使用的 `fixture` 引入了错误。

使用这个示例代码，您可以看到 `pytest` 不同状态的用例运行结果。这些状态在实际的持续集成（CI）过程中非常有用，因为它们提供有关测试运行情况的详细信息。



# 2.5 pytest执行结束时返回的状态码

## 2.5.1 pytest exit code用途

在使用`pytest`框架的时候，经常会涉及对`pytest`命令进行二次封装，比如写一个shell或者Python脚本调用`pytest`。这样做的好处是可以为用户提供几个运行场景，简化`pytest`的命令行参数使用。封装脚本需要对实际运行的`pytest`命令进行退出码判断，然后进行逻辑判断再返回给实际用户查看。

那么下面我们来分享下`pytest`的退出码。

## 2.5.2 pytest exit code含义

准确的说，`pytest exit code`是`pytest.main`函数的返回值，这个值可以用来了解测试的结果，比如下面的测试示例：

```python
import pytest

# 执行特定的测试文件
exit_code = pytest.main(['testcases/Accounts/test_ldap.py'])

# 检查返回码来判断测试结果
if exit_code == 0:
    print("All tests passed!")
else:
    print("There were some test failures.")
```

如上用例，根据`exit_code`的结果打印不同内容。

`pytest`中，`pytest.main`返回值有如下几个状态值：

- 0 ：所有用例执行完毕，全部通过。
- 1 ：所有用例执行完毕，存在Failed状态的测试用例。
- 2 ：用户中断了测试的执行。
- 3 ：测试执行过程发生了内部错误。
- 4 ：`pytest` 命令行使用错误。
- 5 ：未采集到任何可用测试用例文件。

如下图所示，分别展示了Exit code 0，Exit code 1 和 Exit code 5 三种用例执行返回的exit code： ![pytest_exit_code](../image/pytest_exit_code.png)

文本内容参考如下：

```shell
root@Gavin:~/code/chapter1-2# pytest test_sample.py
============================== test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-2
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_sample.py F                                                      [100%]

=============================== FAILURES ====================================
_______________________________ test_answer _________________________________

    def test_answer():
        """  Test case of an answer   """
>       assert increasing_by_one(3) == 5
E       assert 4 == 5
E        +  where 4 = increasing_by_one(3)

test_sample.py:16: AssertionError
=============================== short test summary info ======================
FAILED test_sample.py::test_answer - assert 4 == 5
=============================== 1 failed in 0.03s ============================
root@Gavin:~/code/chapter1-2# echo $?
1
root@Gavin:~/code/chapter1-2# pytest test_case_run.py
=============================== test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-2
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

test_case_run.py .....                                               [100%]

================================ 5 passed in 0.01s ===========================
root@Gavin:~/code/chapter1-2# echo $?
0
root@Gavin:~/code/chapter1-2# mkdir tmp
root@Gavin:~/code/chapter1-2# cd tmp/
root@Gavin:~/code/chapter1-2/tmp# pytest
================================ test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-2/tmp
plugins: check-2.2.2, metadata-3.0.0
collected 0 items

================================= no tests ran in 0.00s ======================
root@Gavin:~/code/chapter1-2/tmp# echo $?
5
root@Gavin:~/code/chapter1-2/tmp#
```

## 2.5.3 示例参考

在 Jenkins 中，你可以为自动化测试任务设置一个构建步骤来运行 `pytest` 命令。Jenkins 会根据 `pytest` 返回的退出代码来判定构建任务的成功或失败。通常，退出代码为 `0` 意味着成功，而任何非零的退出代码都表示失败，提早退出，避免不必要时间的浪费。

如果你想要 Jenkins 识别特定的 `pytest` 退出代码并采取相应行动，你可以用 Jenkins Pipeline 或是传统的构建步骤来设定。这里提供一个 Jenkins Pipeline 脚本的示例，展示如何根据不同的 `pytest` 退出代码执行不同的后续步骤。

首先，编写一个包含 `pytest.exit()` 语句的测试脚本（代表测试用例或测试用例集）：

```python
# Content of test_with_exit.py
import pytest

def test_pass():
    # 一个会通过的测试
    assert 1 == 1

def test_exit():
    # 基于某个条件我们可能想退出测试
    should_exit = True
    if should_exit:
        pytest.exit("Exiting due to a custom condition!", returncode=5)

def test_normal_fail():
    # 一个会失败的测试
    assert 1 == 2
```

然后，在 Jenkins Pipeline 脚本中，你可以这样使用：

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                script {
                    // 运行 pytest 并捕捉退出代码
                    try {
                        sh label: 'Run pytest', script: 'pytest test_with_exit.py'
                    } catch (exc) {
                        // 捕获退出代码
                        def exitCode = exc.getExitStatus()

                        // 根据不同的退出代码采取不同的策略
                        if (exitCode == 0) {
                            echo 'All tests passed!'
                        } else if (exitCode == 5) {
                            echo 'Exited on custom condition!'
                            // 这里可以添加更多逻辑，例如发送通知或对环境进行清理等
                        } else {
                            echo "Exited with error code: ${exitCode}"
                            // 处理通用的失败情况，可能会抛出异常或标记构建失败
                            throw exc
                        }
                    }
                }
            }
        }
    }
}
```

这个脚本做了以下几点：

* 在 'Test' 阶段，使用了 `sh` 步骤来运行 `pytest` 命令。
* 使用 `try-catch` 块来捕获可能抛出的异常。
* 检查捕捉到的异常的退出代码，然后根据退出代码采取相应的行动。

如果 `pytest` 正常退出并且所有测试都通过，则退出代码为 `0`，脚本将打印 "All tests passed!"。

如果由于特定条件触发 `pytest.exit()`，并使用了自定义的退出代码（在本例中为 `5`），则脚本会打印 "Exited on custom condition!"，然后可以执行一些特定的清理步骤或发送通知。

对于其他非零退出代码，脚本会打印出相应的错误代码，并可能会抛出异常，从而标记 Jenkins 任务失败。

通过这种方式，你可以让 Jenkins 根据 `pytest` 的退出代码来执行不同的后续操作，从而达到更细致控制构建行为的目的。

**请注意：**

上述测试用例代码中设置的 `5` 退出代码并不代表 `pytest` 的标准退出代码中的 `5`（没有收集到任何测试）；这里的 `5` 仅是作为一个示例，你可以根据需要设置不同的退出代码。

# 2.6 测试用例执行顺序

在`unittest`框架中，默认按照`ACSII`码的顺序加载测试用例并执行，顺序为：0~9、AZ、a~z，测试目录、测试模块、测试类、测试方法/测试函数都按照这个规则来加载测试用例。

而 `pytest` 中的用例执行顺序与`unittest` 是不一样的，`pytest`有默认的执行顺序（.py文件中测试函数从上到下顺次执行），还可以自定义执行顺序（比如借助第三方插件`pytest-order的@pytest.mark.order(1)`）。

## 2.6.1 pytest 默认执行顺序

测试目录、测试模块，按照排序顺序执行2。

我们先看目录下只有一个测试文件的执行顺序：

```python
root@Gavin:~/code/chapt1-2# cat test_order_sample_1.py 
#!/usr/bin/env python
# -*- conding:UTF-8 -*-

"""
Example of test case execution order.
"""

def test_case_sample01():
    """  Test case of sample01  """
    print("This is a sample test case 01.")


def test_case_sample03():
    """  Test case of sample03  """
    print("This is a sample test case 03.")


def test_case_sample02():
    """  Test case of sample02  """
    print("This is a sample test case 02.")
root@Gavin:~/code/chapt1-2# 
```



用例的编写顺序是 `test_case_sample01` --> `test_case_sample03` --> `test_case_sample02`， 执行的时候也是这个顺序：

```shell
root@Gavin:~/code/chapter1-2# pytest -vs test_order_sample_1.py 
============================== test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-2
plugins: check-2.2.2, metadata-3.0.0
collected 3 items

test_order_sample_1.py::test_case_sample01 This is a sample test case 01.
PASSED
test_order_sample_1.py::test_case_sample03 This is a sample test case 03.
PASSED
test_order_sample_1.py::test_case_sample02 This is a sample test case 02.
PASSED

================================ 3 passed in 0.01s =============================
root@Gavin:~/code/chapter1-2#
```

可以看出`test_case_sample02`在`test_case_sample03`之后执行，是按照用例在`py`文件中编写顺序来执行的。

再看一个带有测试类和测试方法的混合体用例：

```python
root@Gavin:~/code/chapter1-2# cat test_order_sample_1.py 
#!/usr/bin/env python
# -*- conding:UTF-8 -*-

"""
Example of test case execution order.
"""

def test_case_sample01():
    """  Test case of sample01  """
    print("This is a sample test case 01.")


def test_case_sample03():
    """  Test case of sample03  """
    print("This is a sample test case 03.")


def test_case_sample02():
    """  Test case of sample02  """
    print("This is a sample test case 02.")
    

class TestOrderCases():
    """  This is a test order class  """
    def test_class_case01(self):
        """  Test case01 under test class  """
        print("Test case01 under test class.")
        
    def test_case02_under_class(self):
        """  Test case02 under test class  """
        print("Test case02 under test class.")
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-2# pytest -vs test_order_sample_1.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-2
plugins: check-2.2.2, metadata-3.0.0
collected 5 items

test_order_sample_1.py::test_case_sample01 This is a sample test case 01.
PASSED
test_order_sample_1.py::test_case_sample03 This is a sample test case 03.
PASSED
test_order_sample_1.py::test_case_sample02 This is a sample test case 02.
PASSED
test_order_sample_1.py::TestOrderCases::test_class_case01 Test case01 under test class.
PASSED
test_order_sample_1.py::TestOrderCases::test_case02_under_class Test case02 under test class.
PASSED
=============================== 5 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-2#
```

从结果看，依然是按照文件中用例编写顺序执行。如果你还有所怀疑，接下来以ASCII码乱序写一个测试用例，观察其执行顺序：

```python
root@Gavin:~/code/chapter1-2# cat test_order_sample_2.py 
#!/usr/bin/env python
# -*- conding:UTF-8 -*-

"""
Example of test case execution order.
"""

def test_C_case01():
    pass


def test_A_case02():
    pass


def test_a_case03():
    pass
```

执行结果如下：

```shell
root@Gavin:~/code/chapter1-2# pytest -vs test_order_sample_2.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-2
plugins: check-2.2.2, metadata-3.0.0
collected 3 items

test_order_sample_2.py::test_C_case01 PASSED
test_order_sample_2.py::test_A_case02 PASSED
test_order_sample_2.py::test_a_case03 FAILED

=============================== FAILURES ======================================
_______________________________ test_a_case03 _________________________________

    def test_a_case03():
>       assert len(list(range(10))) > len(list(range(1,20,2)))
E       assert 10 > 10
E        +  where 10 = len([0, 1, 2, 3, 4, 5, ...])
E        +    where [0, 1, 2, 3, 4, 5, ...] = list(range(0, 10))
E        +      where range(0, 10) = range(10)
E        +  and   10 = len([1, 3, 5, 7, 9, 11, ...])
E        +    where [1, 3, 5, 7, 9, 11, ...] = list(range(1, 20, 2))
E        +      where range(1, 20, 2) = range(1, 20, 2)

test_order_sample_2.py:17: AssertionError
============================== short test summary info ========================
FAILED test_order_sample_2.py::test_a_case03 - assert 10 > 10
========================= 1 failed, 2 passed in 0.04s =========================
root@Gavin:~/code/chapter1-2#
```

如上所示，并没有安装ASCII码顺序执行，依然是用例的编写顺序进行执行。

## 2.6.2 自定义执行顺序

`pytest` 框架支持自定义测试用例的执行顺序，需要借助`pytest-order`插件；如果用例之间有相互依赖关系的，需要借助`pytest-dependency`插件。

详细信息，请参见本书《pytest插件》章节内容。

## 2.6.3 涉及多个目录/文件下执行顺序

当 `pytest` 收集多个测试文件夹中的测试文件时，它遵循以下基本的规则决定执行顺序：

### 2.6.3.1 目录顺序

按文件系统的遍历顺序执行目录。通常情况下，这会是字母顺序，但也可能受到文件系统和操作系统的影响。也就是说，如果有两个目录 `dirA` 和 `dirB`，它们包含测试文件，并且 `dirA` 在字母顺序中位于 `dirB` 之前，那么 `dirA` 中的测试会先执行。

### 2.6.3.2 子目录顺序

如果目录包含子目录，在父目录的字典顺序后将遵循子目录的字典顺序。

### 2.6.3.3 文件顺序

在单个目录或子目录中寻找所有 `test_*.py` 或 `*_test.py` 文件。这些文件按照文件系统中的字典顺序（通常是 ASCII 排序）进行排序。这意味着文件是按照它们的名字来执行的，所以 `test_a.py` 会在 `test_b.py` 之前运行。

### 2.6.3.4 类排序

#### 2.6.3.4.1 类与测试函数的顺序

在每个测试文件里，测试类（以 `Test` 开头的类）按照它们在文件中出现的顺序被收集，同样的规则也适用于类外的测试函数。

#### 2.6.3.4.2 测试方法顺序

在每个测试类里，测试方法（即以 `test` 开头的函数）按照字典顺序被收集和执行。

这是 `pytest` 默认的收集和执行顺序。然而，在某些情况下，测试开发者可能需要根据特定逻辑或依赖关系来运行测试，这时候就需要使用额外的插件如 `pytest-order`，或者是通过自定义收集的钩子（如 `pytest_collection_modifyitems`）来改变收集和执行的顺序。

**请注意：**

尽管我们可以通过插件和钩子来影响测试收集的过程，但强制规定测试执行的顺序可能会导致测试之间产生隐形的依赖，这不被认为是最佳实践。测试用例应该尽量保持独立和自包含，以避免这些问题。



# 2.7 本章小结

在本章节中，我们详细介绍了`pytest`测试框架中测试用例的搜索规则，以及`pytest`如何自动搜索指定目录及其子目录下的测试用例文件。我们还介绍了`pytest`执行测试用例的几种不同方式，以及测试用例执行结果状态。同时，在文章中我们探讨了执行返回状态码的含义，解决了测试用例因各种原因失败导致的错误状态码。通过这些知识，我们可以更有效地编写、组织和管理我们的测试用例，以便更全面地测试我们的代码，确保代码质量和稳定性。
值得注意的是，`pytest`还提供了许多其他的高级功能和使用技巧，例如`fixture`用法、参数化测试、`mock`对象等，都有助于我们编写更精确、更全面的测试用例，但本章节中并未介绍，读者可以继续阅读后续章节以便可以深入了解`pytest`，以掌握更全面的`pytest`知识和技能。

总之，`pytest`是一个灵活、强大、易于学习和使用的Python测试框架。通过本文的介绍，你可以对`pytest`有更深入、更全面的认识，以便更好地为您的项目编写高质量的测试用例，确保代码的正确性和可用性，满足用户和客户的需求。

