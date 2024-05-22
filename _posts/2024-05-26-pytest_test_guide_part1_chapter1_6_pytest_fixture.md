---
title: 《pytest测试指南》-- 章节1-6 pytest fixture
date: 2024-05-26 23:00:00
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
summary: 《pytest测试指南》一书 章节1-6 pytest fixture详细介绍与示例说明
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 第6章 pytest精髓-fixture

在软件开发过程中，测试是保证代码质量的重要环节。在Python生态中，`pytest` 是最受欢迎的测试框架之一，它以其简单的语法、强大的功能和庞大的插件生态系统著称。`pytest `之所以受到广泛的推崇，不仅因为它使得单元测试的编写变得轻而易举，更因为它提供了丰富的内置 `fixture` 功能，极大地增强了测试的灵活性和表达能力。

`fixture` 是 `pytest` 中一个核心的概念，它们充当了测试函数中所需资源和状态的外部提供者。无论是数据库连接、临时文件目录，还是自定义数据的加载，`fixture` 都能够优雅且高效地管理它们的生命周期。这解放了开发者从繁琐的设置（`setup`）和拆解（`teardown`）流程，使得他们可以将关注点更多地放在测试逻辑本身，从而提升了测试代码的可读性、可维护性和可重用性。

# 6.1 什么是 pytest fixture?

在 `pytest` 中，fixture 指代一种函数，它可以由测试函数、类或整个模块共用。它们通过一个名为 `@pytest.fixture` 的装饰器来标记，并且可以被其他测试用例当作参数调用。这种机制跟 Python 内的函数参数传递有些相似，却有着更深层的测试资源管理策略。

`pytest` fixture 的魅力在于其“需求驱动”的加载机制。换言之，仅当测试用例明确要求使用某个 fixture 时，该 fixture 才会被激活并执行相关的代码。这种延迟激活确保了不会有不必要的资源配置和释放操作，节约了宝贵的测试时间。

# 6.2 pytest fixture 的强大之处

`pytest` 的 fixture 功能强大到难以置信，你可以利用它们做到以下几点：

1. **自动化资源管理：** 无论多复杂的资源配置，嵌套的fixture都能处理得井井有条。
2. **参数化测试：** 通过固件参数化，可以用少量的代码执行多变的测试用例。
3. **范围控制：** Fixtures 可以具有不同的生命周期，比如函数级别、类级别、模块级别或是全局会话级别，适应不同的测试场景。
4. **强大的依赖注入：** 它们为测试函数装配所需的组件提供了一种非常方便的方式。
5. **插件化的设计：** 自定义的 fixtures 可以很容易地封装成插件，供其他项目使用。

# 6.3 fixture介绍

fixture是`pytest`的大杀器，是`pytest`特有的功能，是`pytest`的精髓所在，`pytest`正是因为fixture的存在才表现的如此出色，很多测试人员放弃其他测试框架转向`pytest`正是因为fixture。`pytest`的fixture不同于unittest、nose中的配置、前置和销毁步骤。`pytest的fixture`非常灵活，测试任何规模稍大的软件系统，`pytest`的fixture都可以派上用场。它用`@pytest.fixture`标识，定义在函数前面，在函数运行前后由`pytest`执行的外壳函数，并将其返回值传递给测试函数。换句话说，`fixture` 被用来“装配”测试环境。

fixture有两种实现方式：

* xunit-style，跟unittest框架的机制非常相似，即setup/teardown系列

* 自己的fixture机制，以@pytest.fixture装饰器来声明

你可以根据自己的喜好，混合使用这两种风格，或单纯使用@pytest.fixture装饰器风格。

# 6.4 fixture的特性

fixture的主要的目的是为了提供一种可靠和可重复性的手法去运行那些最基本的测试内容。下面是一些关于 `fixture` 的关键特性：

* **重用性**： `fixture` 可以在多个测试中重用，包括不同的模块和类之间，避免了代码的重复，实现了共享。
* **作用域**： `fixture` 可以定义不同的作用域（scope），比如 `function`、`class`、`module` 或 `session`。不同作用域的 `fixture` 会在不同的测试阶段被调用和销毁。
* **参数化**： 可以对 `fixture` 进行参数化，允许在多个参数组合下测试相同的代码路径。
* **自动使用**： 使用 `@pytest.fixture(autouse=True)` 装饰器，可以让 `fixture` 自动对每个测试用例生效，而无需显式的引用。
* **资源管理**： `fixture` 通常用来进行资源管理，如打开和关闭文件，连接和断开数据库连接。使用 `yield` 语法，`fixture` 可以在 `yield` 之前设置资源，在 `yield` 之后清理资源。

以下是一个简单的 `fixture` 示例：

```python
# content of test_fixture_example.py
import pytest

@pytest.fixture
def supply_url():
    return "https://gavin-wang-note.github.io/"

def test_example(supply_url):
    url = supply_url
    # 使用 url 进行测试
    assert url == "https://gavin-wang-note.github.io/"
```

在此例中，`supply_url` 是一个 `fixture` 函数，它返回了一个字符串，用作测试时的 URL。`test_example` 测试函数使用 `supply_url` `fixture`。当测试函数被执行时，`pytest` 首先调用 `fixture` 函数 `supply_url` 并把返回值传递给 `test_example` 函数中的对应参数。

fixture的使用，大幅提高了测试代码的可维护性和可扩展性，一旦你掌握了fixture，自动化测试工作将变得得心应手。

# 6.5 fixture的优势

从功能上看来，它与setup、teardown相似，但是优势明显，如下：

## 6.5.1 命令灵活

对于setup.teardown，可以不起这两个名字，即不局限于setup和teardown这几个命名。

## 6.5.2 数据共享

* 在conftest.py配置里写的方法可以实现数据共享，不需要import导入，就能自动找到一些配置，可以跨文件共享。
* 按模块化的方式实现，每个fixture都可以互相调用。

## 6.5.3 实现参数化

@pytest.fixture()有5个参数，如下：

```python
@pytest.fixture(scope="", params="", autouse="", ids="", name="") 
```

### 6.5.3.1 scope

scope的层次及神奇的yield组合相当于各种setup和teardown，可以跨函数function，类class，模块module或整个测试session范围。

| 取值     | 范围     | 说明                                                         |
| -------- | -------- | ------------------------------------------------------------ |
| function | 函数级   | 每个函数或方法都会调用                                       |
| class    | 类级别   | 每个测试类只运行一次                                         |
| module   | 模块级别 | 每一个.py文件只调用一次                                      |
| package  | 包级     | 每一个python包只调用一次                                     |
| session  | 会话级   | 每次会话只需要运行一次，会话内所有方法及类、模块都共享这个方法 |

### 6.5.3.2 params

允许你在fixture中传入参数，可以是一个值、一个可迭代对象（如：列表，元组，字典列表[{},{},{}]，字典元组({},{},{})），甚至是一个函数。这使得一个 fixture 能够与多个参数组合使用。

### 6.5.3.3 autouse

自动执行fixture，默认False表示不开启，可以设置为True开启自动使用fixture功能，即使没有在测试用例中显式使用@pytest.mark.usefixtures装饰器，这样用例就不用每次都去传参了(自动调用fixture功能)。

### 6.5.3.4 ids

当与params结合使用时，ids可以提供一个字符串列表，用于为生成的测试用例设置不同的ID。这在参数化测试中很有用，可以让你轻松区分测试用例的不同参数组合。

### 6.5.3.5 name

给@pytest.fixture()标记的方法取一个别名。当fixture生成多个测试用例时（通过params或者ids），测试用例的名称将会基于这个name参数进行生成。



# 6.6 xunit-style 风格

`pytest` 支持`xUnit` 风格，这是一种结构化的测试编写风格，模式化自传统的 `xUnit` 系列测试框架，如 `JUnit` 和 `unittest` (Python标准库中的测试框架)。`xUnit` 风格在 `pytest` 中表现为测试类和对应测试方法。

很明显，这种风格是为了兼容unittest和nose框架的测试用例，pytest更推荐fixture风格，而非xunit-style风格。考虑到兼容性和个人喜好问题，以下是 `xUnit` 风格在 `pytest` 的具体应用介绍。

## 6.6.1 测试类
测试类是普通的 Python 类，名称以 `Test` 开头。类中的测试方法名称以 `test_` 开头。这些类不需要继承任何特定的基类。

## 6.6.2 固件方法
`xUnit` 风格的固件方法主要包括：

* `setup_function` 或者 `teardown_function`：每个测试方法之前/之后运行。

- `setup_method` 或 `teardown_method`: 每个测试方法之前/之后运行。
- `setup_class` 或 `teardown_class`: 每个测试类之前/之后运行，但只运行一次。
- `setup_module` 或 `teardown_module`: 每个模块之前/之后运行，但只运行一次。

`pytest` 也支持 `unittest` 框架中使用的 `setUp` 和 `tearDown` 方法。 

总结如下：

* 每个级别的setup/teardown都可以多次复用。
* 如果相应的初始化函数执行失败或者被跳过则不会执行teardown方法。

接下来，针对每种固件方法，逐一做示例。

### 6.6.2.1 function级别

在 `pytest` 中，`xunit-style` 的 `setup_function` 是一种特殊的固件函数，它在每个测试函数执行之前自动运行。这个函数通常用于为测试准备环境或初始化资源，这些资源在每个测试函数运行后不会保留，在 `teardown_function` 中可以进行清理。

要使用 `setup_function` 和 `teardown_function` 方法，你需要在你的测试模块中直接定义它们。`pytest` 会检测这些特殊的函数名并在每个测试函数执行前后自动调用它们。

下面是 `setup_function` 使用的一个例子：

```python
# content of test_functionLevel.py

# 这是你的function级别的 setup 函数
def setup_function(function):
    """
    setup_function 在每个 test_ 函数之前执行。
    """
    print(f"\nSetup: Starting test function {function.__name__}")

# 这是你的function级别的 teardown 函数
def teardown_function(function):
    """
    teardown_function 在每个 test_ 函数之后执行。
    """
    print(f"Teardown: Finished test function {function.__name__}")

# 这是一个测试函数
def test_example1():
    assert True  # 这里是你的测试逻辑

# 这是另一个测试函数
def test_example2():
    assert True  # 这里是你的测试逻辑
```

在上述例子中，`setup_function` 将在运行 `test_example1` 和 `test_example2` 之前被调用，`teardown_function` 将在两个测试函数运行完毕后分别被调用。通过 `function.__name__`，可以获取当前测试函数的名字，这样有助于在打印信息时了解当前是为哪个测试函数进行设置或清理。

输出结果：

```shell
root@Gavin:~/code/chapter1-6/xunit-stype# pytest -s -v test_functionLevel.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6/xunit-stype
collected 2 items    

test_functionLevel.py::test_example1 
Setup: Starting test function test_example1
PASSEDTeardown: Finished test function test_example1

test_functionLevel.py::test_example2 
Setup: Starting test function test_example2
PASSEDTeardown: Finished test function test_example2


================================ 2 passed in 0.01s ===========================
root@Gavin:~/code/chapter1-6/xunit-stype#
```

`setup_function` 非常适合用于需要在每个测试函数之前进行特别准备，但测试函数之间不应该共享状态的情景。比较推荐的做法是使用 `pytest` 的 `fixture` 机制，它提供了更灵活的资源管理和更强大的功能，例如参数化、作用域控制等。但在某些简单的、非共享设置或需要快速从 `xUnit` 风格的测试框架迁移到 `pytest` 时，`setup_function` 可以方便地被采用。

### 6.6.2.2 method级别

定义方法级别（method-level）的设置（setup）和清理（teardown）函数。

- `setup_method(self, method)`: 在每个测试方法之前执行。可以用于设置测试方法所需的状态或资源。
- `teardown_method(self, method)`: 在每个测试方法之后执行。用于清理 `setup_method` 中所设置的状态或资源。

这些函数分别在每个测试方法之前和之后运行，用于准备测试环境和清理资源。这与 `xUnit` 测试框架中的类似概念相对应。

以下是一个 `pytest` 中使用 `xUnit` 风格方法级别设置和清理函数的示例：

```python
root@Gavin:~/code/chapter1-6/xunit-stype# cat test_methodLevel.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


class TestExample:
    def setup_method(self, method):
        # 这里进行测试方法开始前的设置
        print(f"Setting up for {method.__name__}")

    def teardown_method(self, method):
        # 这里进行测试方法结束后的清理
        print(f"Tearing down {method.__name__}")

    def test_method1(self):
        # 测试方法一
        assert True

    def test_method2(self):
        # 测试方法二
        assert True
root@Gavin:~/code/chapter1-6/xunit-stype#
```

在这个例子中，`setup_method` 在 `test_method1` 和 `test_method2` 运行之前被调用，`teardown_method` 在这两个测试方法运行之后被调用。可以通过 `method.__name__` 获取当前执行的测试方法的名称。

输出结果：

```shell
root@Gavin:~/code/chapter1-6/xunit-stype# pytest -s -v test_methodLevel.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6/xunit-stype
collected 2 items

test_methodLevel.py::TestExample::test_method1 Setting up for test_method1
PASSEDTearing down test_method1

test_methodLevel.py::TestExample::test_method2 Setting up for test_method2
PASSEDTearing down test_method2

=============================== 2 passed in ===================================
root@Gavin:~/code/chapter1-6/xunit-stype#
```

**注意事项：**

- `setup_method` 和 `teardown_method` 是基于每个测试方法运行的，适合用于需要在每个测试方法之前或之后执行的操作。
- 对于需要跨多个测试方法共享的设置和清理操作，可以考虑使用类级别（`setup_class`/`teardown_class`）或模块级别（`setup_module`/`teardown_module`）的方法。
- 虽然 `pytest` 支持这种 `xUnit` 风格的设置和清理方法，但它更推荐使用 `fixture` 机制，因为 `fixture` 提供了更灵活和强大的功能，例如参数化、作用域控制和依赖注入。

总的来说，方法级别的设置和清理函数在 `pytest` 中为使用 `xUnit` 风格的测试提供了一种方便的方式，尤其是在从其他 `xUnit` 风格的测试框架迁移时。

### 6.6.2.3 class级别

定义类级别（class-level）的设置和清理函数：

- `setup_class(cls)`: 在测试类的所有测试方法执行之前调用一次。用于设置测试类共用的状态或资源。
- `teardown_class(cls)`: 在测试类的所有测试方法执行之后调用一次。用于清理 `setup_class` 中设置的状态或资源。

这些函数在整个测试类的开始和结束时运行一次，用于准备或清理整个类中的所有测试方法所共用的资源或状态。

以下是一个使用 `xUnit` 风格类级别设置和清理函数的 `pytest` 测试示例：

```python
# content of test_classLevel.py
class TestExample:
    @classmethod
    def setup_class(cls):
        # 这里进行类开始前的设置
        cls.shared_resource = {}
        print("Setting up for the test class")

    @classmethod
    def teardown_class(cls):
        # 这里进行类结束后的清理
        print("Tearing down the test class")

    def test_method1(self):
        # 测试方法一
        assert True

    def test_method2(self):
        # 测试方法二
        assert True
```

在这个例子中，`setup_class` 在类的所有测试方法开始之前被调用一次，而 `teardown_class` 在所有测试方法执行完毕之后被调用一次。这样可以共享 `setup_class` 中创建的资源，例如 `shared_resource`，在整个测试类中。

输出结果：

```shell
root@Gavin:~/code/chapter1-6/xunit-stype# pytest -s -v test_classLevel.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6/xunit-stype
collected 2 items

test_classLevel.py::TestExample::test_method1 Setting up for the test class
PASSED
test_classLevel.py::TestExample::test_method2 PASSEDTearing down the test class

============================ 2 passed in 0.01s ================================
root@Gavin:~/code/chapter1-6/xunit-stype#
```

**注意事项：**

- 类级别的设置和清理适合用于那些在类中所有测试方法间共享的资源或状态。
- 对于需要在每个测试方法之前或之后执行的个别设置或清理，应使用方法级别的 `setup_method` 和 `teardown_method`。
- 与方法级别的设置/清理函数相比，类级别的函数在整个测试类中只执行一次，可以提高测试的效率，尤其是在资源创建和销毁代价较高时。
- `pytest` 支持 `xUnit` 风格的设置和清理方法，但通常建议使用 `fixture` 机制，因为它提供了更高的灵活性和功能，例如参数化和依赖管理。

类级别的设置和清理函数在 `pytest` 中为使用 `xUnit` 风格的测试提供了方便的方式，特别适合那些需要在测试类级别共享资源或状态的场景。

### 6.6.2.4 module级别

模块级别（module-level）的设置和清理函数：

- `setup_module(module)`: 在模块的所有测试开始之前执行一次。
- `teardown_module(module)`: 在模块的所有测试运行之后执行一次。

这些函数对于全模块范围的资源初始化和清理非常有用，比如启动或关闭数据库连接。

以下是一个使用 `xUnit` 风格模块级别设置和清理函数的 `pytest` 测试示例：

```python
# content of test_moduleLevel.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


def setup_module(module):
    print('\nsetup_module() for {}'.format(module.__name__))


def teardown_module(module):
    print('teardown_module() for {}'.format(module.__name__))


def test_case_1():
    print('test_case_1()')


def test_case_2():
    print('test_case_2()')


class TestClass(object):

    def test_case_3(self):
        print('self.test_case_3()')

    def test_case_4(self):
        print('self.test_case_4()')

```

在这个例子中，`setup_module` 在此测试模块中的所有测试开始之前被调用一次，而 `teardown_module` 在所有测试执行之后被调用一次。

输出结果：

```shell
root@Gavin:~/code/chapter1-6/xunit-stype# pytest -s -v test_moduleLevel.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6/xunit-stype
collected 4 items

test_moduleLevel.py::test_case_1 
setup_module() for test_moduleLevel
test_case_1()
PASSED
test_moduleLevel.py::test_case_2 test_case_2()
PASSED
test_moduleLevel.py::TestClass::test_case_3 self.test_case_3()
PASSED
test_moduleLevel.py::TestClass::test_case_4 self.test_case_4()
PASSEDteardown_module() for test_moduleLevel

================================= 4 passed in 0.01s ============================
root@Gavin:~/code/chapter1-6/xunit-stype#
```



## 6.6.3 推荐做法

尽管 `pytest` 支持 `xUnit` 风格的测试，但更倾向于推荐使用 `pytest` 的 `fixture` 。`fixture` 提供了更大的灵活性，可以更容易的进行参数化，以及在测试函数之间共享测试数据和状态。它们可以通过装饰器直接使用，并可以避免使用全局状态，使得测试代码更加模块化和可维护。

总的来说，对于习惯于 `xUnit` 测试模式或从其他 `xUnit` 类框架迁移的团队来说，`pytest` 的 `xUnit`-style 支持提供了熟悉和易于上手的方法。然而，为了充分利用 `pytest` 的先进特性，鼓励开发者采用更具 `pytest` 风格的固件和测试编写方法。



# 6.7 pytest的fixture实现方式

通过@pytest.fixture装饰器来定义fixture，一个函数被@pytest.fixture装饰，那么这个函数就是fixture。

使用fixture时，分为二个部分：fixture定义、fixture调用。

除此之外，还有fixture的共享机制，嵌套调用机制，接下来我们逐一介绍。

## 6.7.1 定义fixture

* fixture通过函数实现。

* 使用@pytest.fixture进行装饰。

  ```python
  import pytest
  
  @pytest.fixture()
  def login_init():
      print("Start login option")
      yield 
      print("End of login")
  ```

* 前置准备工作代码和后置清理工作代码，都写在一个函数里面。

* 通过yeild关键字，区分前置代码和后置代码 。

    yeild之前的代码为前置代码，yeild之后的代码为后置代码。

    在实际应用场景当中，可以只有前置准备工作代码，也可以只有后置清理工作代码。

* fixture有4个作用域

  测试会话(session)、测试模块(module)、测试类(class)、测试用例(function)

  测试会话：pytest执行测试用例的整个过程，称为会话。比如pytest收集到了20条用例并执行完成，这个过程称为测试会话。
  
  设置fixture的作用域：通过@pytest.fixture(scope=作用域)来设置。默认情况下，scope=function
  
* fixture的返回值设置：yeild 返回值

   当测试用例当中，要使用fixture里生成的数据时，则需要fixture返回数据。
   
   若有数据返回则：yeild 返回值

## 6.7.2 调用fixture

在fixture定义好之后，可以明确：

* fixture处理了哪些前置准备工作、哪些后置清理工作
* fixture作用在哪个范围(是测试函数？还是测试类？还是测试会话？还是测试模块？)

在以上两点都定下来了之后，接下来就是在测试用例当中，根据需要调用不同的fixture。

调用方法有两种：

* 在测试用例/测试类上面加上：@pytest.mark.usefixture("fixture的函数名字")
* 将fixture函数名，作为测试用例函数的参数

第二种用法，主要是用参数来接收fixture的返回值，以便在测试用例中使用。

第一种方法示例如下：

```python
import pytest

@pytest.fixture()
def login_init():
    print("Start login option")
    yield 
    print("End of login")


@pytest.mark.usefixtures("login_init")
def test_login_case():
    print("This is a test case")
```

第二种方法示例如下：

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "www.google.com"


@pytest.fixture()
def fixture_driver():
    driver = webdriver.Chrome()
    driver.get(URL)
    yield driver
    driver.close()


def test_case(fixture_driver):
    # fixture_driver 作为参数传入测试用例，接收此函数的返回值driver
    # 即在当前测试用例内部，fixture_driver就是fixture返回的driver对象
    driver.find_elements(By.XPATH, 'item1').click()
```

上例中只传递一个fixture 函数作为参数，也可传递多个fixture作为参数：

```python
@pytest.fixture()
def user():
    user = "Gavin"
    return user


@pytest.fixture()
def pwd():
    pwd = "123456"
    return pwd


@pytest.fixture()
def role():
    role = 'QA'
    return role


def test_trans_fixture(user, pwd, role):
    """   pass more than one fixture function   """
    print(user, pwd, role)
    assert "Gavin" in str(user)
    assert pwd == "123456"
    assert role == 'Software Tester Enginer'
```



## 6.7.3 fixture函数源码解析

上面的示例演示了`fixture`的基本使用方法，接下来是`@pytest.fixture()`方法的源码：

```python
def fixture(  # noqa: F811
    fixture_function: Optional[FixtureFunction] = None,
    *,
    scope: "Union[_ScopeName, Callable[[str, Config], _ScopeName]]" = "function",
    params: Optional[Iterable[object]] = None,
    autouse: bool = False,
    ids: Optional[
        Union[Sequence[Optional[object]], Callable[[Any], Optional[object]]]
    ] = None,
    name: Optional[str] = None,
) -> Union[FixtureFunctionMarker, FixtureFunction]:
    """Decorator to mark a fixture factory function.

    This decorator can be used, with or without parameters, to define a
    fixture function.

    The name of the fixture function can later be referenced to cause its
    invocation ahead of running tests: test modules or classes can use the
    ``pytest.mark.usefixtures(fixturename)`` marker.

    Test functions can directly use fixture names as input arguments in which
    case the fixture instance returned from the fixture function will be
    injected.

    Fixtures can provide their values to test functions using ``return`` or
    ``yield`` statements. When using ``yield`` the code block after the
    ``yield`` statement is executed as teardown code regardless of the test
    outcome, and must yield exactly once.

    :param scope:
        The scope for which this fixture is shared; one of ``"function"``
        (default), ``"class"``, ``"module"``, ``"package"`` or ``"session"``.

        This parameter may also be a callable which receives ``(fixture_name, config)``
        as parameters, and must return a ``str`` with one of the values mentioned above.

        See :ref:`dynamic scope` in the docs for more information.

    :param params:
        An optional list of parameters which will cause multiple invocations
        of the fixture function and all of the tests using it. The current
        parameter is available in ``request.param``.

    :param autouse:
        If True, the fixture func is activated for all tests that can see it.
        If False (the default), an explicit reference is needed to activate
        the fixture.

    :param ids:
        Sequence of ids each corresponding to the params so that they are
        part of the test id. If no ids are provided they will be generated
        automatically from the params.

    :param name:
        The name of the fixture. This defaults to the name of the decorated
        function. If a fixture is used in the same module in which it is
        defined, the function name of the fixture will be shadowed by the
        function arg that requests the fixture; one way to resolve this is to
        name the decorated function ``fixture_<fixturename>`` and then use
        ``@pytest.fixture(name='<fixturename>')``.
    """
    fixture_marker = FixtureFunctionMarker(
        scope=scope,
        params=tuple(params) if params is not None else None,
        autouse=autouse,
        ids=None if ids is None else ids if callable(ids) else tuple(ids),
        name=name,
        _ispytest=True,
    )

    # Direct decoration.
    if fixture_function:
        return fixture_marker(fixture_function)

    return fixture_marker
```

这个函数定义了一个用于创建fixture的装饰器，参数控制fixture的行为以及它在测试中的使用方式，它有如下参数：

- **fixture_function (OptionalFixtureFunction)**: 实际将被转换成fixture的函数。
- **scope**: 决定fixture的生命周期。可以是`"function"`, `"class"`, `"module"`, `"package"` 或 `"session"`，也可以是一个返回这些字符串之一的可调用对象，允许动态确定范围。这影响了fixture的前置和后置时间。
- **params (OptionalIterable[object])**: 如果提供，fixture将被参数化，这意味着fixture函数将被多次调用，每次使用不同的参数，这对于测试不同场景非常有用。
- **autouse (bool)**: 如果为`True`，则对所有可以看到它的测试自动使用fixture函数。如果为`False`（默认值），则需要明确引用以激活fixture。
- **ids (OptionalUnion[Sequence[Optional[object], Callable[Any, Optionalobject]]])**: 为每个参数集提供一个唯一的标识符，这在参数化fixture时特别有用。
- **name (Optionalstr)**: 可以为fixture提供一个自定义名称。如果不设置，默认使用装饰函数的名称。这在自动名称可能与其他函数冲突或希望使用更具描述性的名称时非常有用。

**函数主要组成部分：**

- **FixtureFunctionMarker**: 这是一个内部类，代表pytest中的一个fixture，它包含了关于fixture的信息，如它的范围、参数和其他选项。
- **直接装饰检查**：如果提供了`fixture_function`，则直接将`fixture_marker`应用于它，将该函数转换为fixture。



## 6.7.4 pytest fixture四种作用域

fixture使用语法如下：

```python
fixture(scope='function'，params=None，autouse=False，ids=None，name=None)
```

上文有提到fixture的5种作用域，分别是function，class，module，package和session，如何使用fixture功能实现不同层级的数据共享呢？接下来将以示例方式一一介绍。



### 6.7.4.1 function级别

function默认模式为@pytest.fixture() 函数级别，即scope="function"，scope可以不写。每一个函数或方法都会调用，每个测试用例执行前都会执行一次function级别的fixture。



```python
root@Gavin:~/code/chapter1-6# cat test_fixture_function.py
import pytest


# @pytest.fixture(scope="function")等价于@pytest.fixture()
@pytest.fixture(scope="function")
def function_scope():
    """   Use-case level fixtures that scope individual test cases  """
    print("\nBefore function Level")
    yield
    print("After function Level")

# test_01会引用function_autouse函数，test_02没有用修饰器修饰，故不会引用
def test_case01(function_scope):
    print("func 1 print")

def test_case02():
    print("func 2 print")
```

上述用例，定义了一个名称为function_scope的fixture，test_case01使用了这个fixture，test_case02则没有，执行效果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_function.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 2 items

test_fixture_function.py::test_case01 
Before function Level
func 1 print
PASSEDAfter function Level

test_fixture_function.py::test_case02 func 2 print
PASSED

================================ 2 passed in 0.01s ===========================
root@Gavin:~/code/chapter1-6
```

### 6.7.4.2 class级别

fixture的scope值还可以是class，此时则fixture定义的动作就会在测试类class的所有用例之前和之后运行。

**注意：**

测试类中只要有一个测试用例的参数中使用了class级别的fixture，则在整个测试类的所有测试用例都会调用fixture函数。

#### 6.7.4.2.1 用例类中的测试用例调用fixture

执行fixture定义的动作，以及此测试类的所有用例结束后同样要运行fixture指定的动作。

```python
# content of test_fixture_class_level_autouse1.py
import pytest


@pytest.fixture(scope="class")
def class_level_autouse():
    """  A class-level fixture that scopes the entire class  """
    print("\n class Before")
    yield
    print("class after")


class TestClassAutoFixture:
    # class级别的fixture任意一个用例引用即可
    def test_class_auto_fixture_1(self, class_level_autouse):
        print("class 1 print")


    def test_class_auto_fixture_2(self):
        print("class 2 print")
```



测试类中的第1条测试用例引用了fixture修饰的函数，则整个测试类的所有测试用例都会执行fixture函数的前置操作，在所有用例执行完成后，都会执行fixture函数的后置操作。

输出效果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_class_level_autouse1.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 2 items

test_fixture_class_level_autouse1.py::TestClassAutoFixture::test_class_auto_fixture_1 
 class Before
class 1 print
PASSED
test_fixture_class_level_autouse1.py::TestClassAutoFixture::test_class_auto_fixture_2 class 2 print
PASSEDclass after

=============================== 2 passed in 0.01s =============================
root@Gavin:~/code/chapter1-6#
```

#### 6.7.4.2.2 用例类外的测试用例调用fixture

如果在类外的函数中去使用class级别的fixture，则此时在测试类外每个测试用例中，fixture跟function级别的fixture作用是一致的，即在类外的函数中引用了class级别的fixture，则在此函数之前和之后同样去执行fixture定义的对应的操作。

```python
# content of test_fixture_class_level_autouse2.py
import pytest


@pytest.fixture(scope="class")
def class_scope():
    """  A class-level fixture that scopes the entire class  """
    print("\n class Before")
    yield
    print("class after")


class TestClassAutoFixture:
    # class级别的fixture任意一个用例引用即可
    def test_class_auto_fixture_1(self, class_scope):
        print("class 1 print")


    def test_class_auto_fixture_2(self):
        print("class 2 print")


def test_class_auto_fixture(class_scope):
    print("class 3 print")
```

如下文所示，测试类外的函数引用了class级别的fixture，则它的作用会等同于function级别的fixture，运行结果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_class_level_autouse2.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items

test_fixture_class_level_autouse2.py::TestClassAutoFixture::test_class_auto_fixture_1 
 class Before
class 1 print
PASSED
test_fixture_class_level_autouse2.py::TestClassAutoFixture::test_class_auto_fixture_2 class 2 print
PASSEDclass after

test_fixture_class_level_autouse2.py::test_class_auto_fixture 
 class Before
class 3 print
PASSEDclass after

================================ 3 passed in 0.01s ============================
root@Gavin:~/code/chapter1-6#
```

### 6.7.4.3 module级别

在Python中module即.py文件（可以理解为当前的.py文件为一个测试suit，因为这个.py文件里含有一个或多个测试用例集合），当fixture定义为module时，则此fixture将在当前文件中起作用。

这里需要特别说明的是，当fixture的scope定义为module时，只要当前文件中有一个测试用例使用了fixture，不管这个用例是在类外，还是在类中，都会在当前文件（模块）的所有测试用例执行之前去执行fixture定义的行为，以及当前文件的所有用例结束之后同样去执行fixture定义的对应操作。

```python
# content of test_fixture_module_scope.py
import pytest


@pytest.fixture(scope="module")
def module_scope():
    """  Applies to the entire py file  """
    print("\nBefore module Level")
    yield
    print("After module Level-")
    
    
# 测试类外和测试类内的函数方法都调用了module级别的fixture，但整个py文件只会生效一次fixture。
def test_module_scope_out_class(module_scope):
    print("Yest case of scope")


class TestScope1:
    def test_scope_01(self):
        print("case scope 01")

    def test_scope_02(self, module_scope):
        print("case scope 02")

    def test_scope_03(self):
        print("case scope 03")
```

输出结果：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_module_scope.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 4 items

test_fixture_module_scope.py::test_module_scope_out_class 
Before module Level
Yest case of scope
PASSED
test_fixture_module_scope.py::TestScope1::test_scope_01 case scope 01
PASSED
test_fixture_module_scope.py::TestScope1::test_scope_02 case scope 02
PASSED
test_fixture_module_scope.py::TestScope1::test_scope_03 case scope 03
PASSEDAfter module Level-

============================== 4 passed in 0.01s =============================
root@Gavin:~/code/chapter1-6#
```

若类中的方法分别调用了class级别的fixture和module级别的fixture，则会两个fixture都生效：

```python
# 顺序在前面fixture会先执行
def test_scope_01(self, module_scope, class_scope): 
    print("case scope 01")
```

若类中的方法同时调用了function级别、class级别、module级别的fixture，则3种fixture会同时生效：

```python
# 顺序在前面fixture会先执行
def test_scope_02(self, module_scope, class_scope, function_scope):  
    print("case scope 02")
```



### 6.7.4.4 session级别(使用conftest.py共享fixture)

当fixture的scope定义为session时，是指在当前目录下的所有用例之前和之后执行fixture对应的操作。

**fixture为session级别是可以跨.py模块调用**的，也就是当我们有多个.py文件的测试用例时，如果多个用例只需调用一次fixture，那就可以设置为scope="session"，并且写到conftest.py文件里。

使用方式：

* 定义测试用例文件
* 构建conftest.py内容

**说明：**

在指定目录下创建**conftest.py（固定命名，不可修改）**文件，然后在conftest.py文件中定义fixture方法，将scope指定为session，此时在当前目录下只要有一个用例使用了此fixture，则就会在当前目录下所有用例之前和之后会执行fixture定义的对应的操作。

```python
# content of conftest.py
import pytest

@pytest.fixture(scope="session")
def session_scope():
    """  A session-level fixture that works for all test cases in that directory  """
    print("\nUse case pre-operations at the session level")
    yield
    print("Post-operation of use cases at the session level")
```

上述定义了session级别的fixture，存放于该用例文件的同一个目录下的conftest.py文件中，该目录下的任一用例文件中的任一测试用例，引用了这个session级别的fixture，则这个session级别的fixture会针对这整个用例文件生效。若存放在根目录下，则针对整个工程的所有用例都生效。

```python
# content of test_fixture_session_scope.py
class TestSessionScopeFixture:
    # session级别的fixture任意一个用例引用即可
    def test_session_scope_fixture_1(self, session_scope):
        print("session 1 print")

    def test_session_scope_fixture_2(self):
        print("session 2 print")


def test_session_scope_fixture():
    print("session 3 print")
```

运行结果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_session_scope.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items

test_fixture_session_scope.py::TestSessionScopeFixture::test_session_scope_fixture_1 
Use case pre-operations at the session level
session 1 print
PASSED
test_fixture_session_scope.py::TestSessionScopeFixture::test_session_scope_fixture_2 session 2 print
PASSED
test_fixture_session_scope.py::test_session_scope_fixture session 3 print
PASSEDPost-operation of use cases at the session level

=============================== 3 passed in 0.01s =============================
root@Gavin:~/code/chapter1-6#
```



## 6.7.5 使用params传递参数

上一节我们介绍了fixture的scope，接下来介绍params。```fixture(scope='function'，params=None，autouse=False，ids=None，name=None)```，从使用方法来看，params是可选参数，默认为None，可以不携带。如果在一系列测试用例的执行中，每轮执行都使用同一个fixture，但是有不同的依赖场景，则可以考虑对fixture进行参数化，这种方式适用于对多场景的功能模块进行详细测试，即它允许你使用同一套测试代码来测试不同的输入。通过参数化，可以创建更健壮、灵活的测试用例，同时避免代码重复。



通过 `params` 参数传递一个可迭代对象，其中包含了不同的数据集，`pytest` 会为每个参数值运行一次测试函数。在fixture的声明函数中，使用requst.param获取当前使用的入参。

### 6.7.5.1 单一测试方法使用测试数据

每次执行同一个测试用例都使用不同的测试数据，使用 `params` 参数化测试，如下例，假设你有一个函数 `add`，需要测试这个函数的不同输入：

```python
# content of test_fixture_params.py
import pytest

# 测试的目标函数
def add(a, b):
    return a + b

# 参数化的 fixture
@pytest.fixture(params=[(1, 2, 3), (4, 5, 9), (10, 20, 30)])
def add_data(request):
    return request.param

def test_add(add_data):
    # 解包 add_data 中的参数
    a, b, expected = add_data
    assert add(a, b) == expected
```

在这个例子中，`add_data` fixture 被参数化为三组不同的值。每组值都是一个包含两个输入和一个预期输出的元组。`test_add` 测试函数会使用这些值来测试 `add` 函数。`pytest` 将为 `params` 中的每个元组运行一次 `test_add` 函数。

**访问参数值：**

在 fixture 函数内部，可以通过 `request.param` 访问当前的参数值。在上面的例子中，`request.param` 会是 `(1, 2, 3)`、`(4, 5, 9)` 或 `(10, 20, 30)` 中的一个。

运行结果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_params.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items

test_fixture_params.py::test_add[add_data0] PASSED
test_fixture_params.py::test_add[add_data1] PASSED
test_fixture_params.py::test_add[add_data2] PASSED

============================= 3 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-6#
```

### 6.7.5.2 多个测试方法公用测试数据

在上述测试代码中，只有test_add一个测试方法公共了三组测试数据，如果再增加一个或多个测试方法，依然可以被一个或多个测试方法公用，参考示例如下：

```python
root@Gavin:~/code/chapter1-6# cat test_fixture_params_multi_functions.py 
import pytest

# 测试的目标函数
def add(a, b):
    return a + b

# 参数化的 fixture
@pytest.fixture(params=[(1, 2, 3), (4, 5, 9), (10, 20, 30)])
def add_data(request):
    return request.param

def test_add(add_data):
    # 解包 add_data 中的参数
    a, b, expected = add_data
    assert add(a, b) == expected


def test_assert_data(add_data):
    a, b, expected = add_data
    assert a*b == expected


def test_subtraction_parameters(add_data):
    a, b, expected = add_data
    assert expected - a == b
root@Gavin:~/code/chapter1-6#
```

运行结果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_params_multi_functions.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 9 items

test_fixture_params_multi_functions.py::test_add[add_data0] PASSED
test_fixture_params_multi_functions.py::test_add[add_data1] PASSED
test_fixture_params_multi_functions.py::test_add[add_data2] PASSED
test_fixture_params_multi_functions.py::test_assert_data[add_data0] FAILED
test_fixture_params_multi_functions.py::test_assert_data[add_data1] FAILED
test_fixture_params_multi_functions.py::test_assert_data[add_data2] FAILED
test_fixture_params_multi_functions.py::test_subtraction_parameters[add_data0] PASSED
test_fixture_params_multi_functions.py::test_subtraction_parameters[add_data1] PASSED
test_fixture_params_multi_functions.py::test_subtraction_parameters[add_data2] PASSED
=============================== FAILURES =======================================
_______________________________ test_assert_data[add_data0] ____________________

add_data = (1, 2, 3)

    def test_assert_data(add_data):
        a, b, expected = add_data
>       assert a*b == expected
E       assert (1 * 2) == 3

test_fixture_params_multi_functions.py:20: AssertionError
_______________________________ test_assert_data[add_data1] ____________________

add_data = (4, 5, 9)

    def test_assert_data(add_data):
        a, b, expected = add_data
>       assert a*b == expected
E       assert (4 * 5) == 9

test_fixture_params_multi_functions.py:20: AssertionError
________________________________ test_assert_data[add_data2] ___________________

add_data = (10, 20, 30)

    def test_assert_data(add_data):
        a, b, expected = add_data
>       assert a*b == expected
E       assert (10 * 20) == 30

test_fixture_params_multi_functions.py:20: AssertionError
=============================== short test summary info ========================
FAILED test_fixture_params_multi_functions.py::test_assert_data[add_data0] - assert (1 * 2) == 3
FAILED test_fixture_params_multi_functions.py::test_assert_data[add_data1] - assert (4 * 5) == 9
FAILED test_fixture_params_multi_functions.py::test_assert_data[add_data2] - assert (10 * 20) == 30
=========================== 3 failed, 6 passed in 0.15s =========================
root@Gavin:~/code/chapter1-6#
```

### 6.7.5.3 有效的测试数据和预期失败的测试数据

使用参数化的fixture来为测试提供多组数据，同时也可以通过`pytest.mark.xfail`标记来预设某些测试数据可能会失败。这样做可以明确区分测试用例中的预期行为和已知的问题，而不需要完全排除这些测试用例。

以下是一个代码示例，结合`params`和`pytest.mark.xfail`来处理有效的测试数据和预期失败的测试数据：

```python
# content of test_fixture_params_mark_xfail.py
import pytest

# 测试的目标函数
def add(a, b):
    return a + b

# 参数化的 fixture，包括预期成功和预期失败的测试数据
@pytest.fixture(params=[
    pytest.param((1, 2, 3), id='positive numbers'),
    pytest.param((1, -1, 0), id='positive and negative'),
    pytest.param((0, 0, 0), id='both zeros'),
    pytest.param((-1, -2, -3), marks=pytest.mark.xfail(reason="Negative numbers expected to fail"), id='negative numbers')
])
def add_data(request):
    return request.param

def test_add(add_data):
    a, b, expected = add_data
    assert add(a, b) == expected
```

在这个代码中：

- 我们定义了一个`add`函数，它接受两个数字并返回它们的和。
- 通过`@pytest.fixture`使用`params`参数，我们提供了一组测试数据，包括预期通过的测试（例如两个正数相加）和一个预期失败的测试（例如两个负数相加）。
- 对于预期失败的测试，我们使用了`pytest.param`，并为这个特定的参数配上了`marks=pytest.mark.xfail`。这会标记这组参数为预期失败的测试用例，并附上一个理由。使用参数`reason`，我们为预期失败的测试案例提供了一个明确的解释。
- 在测试函数`test_add`中，我们从fixture `add_data`中提取参数，并断言`add`函数返回的结果是否和预期值相等。

当你运行此测试时，`pytest`将执行所有四个测试用例。其中，标记为`xfail`的那个测试（negative numbers）将不影响整个测试套件的结果，即使它可能（根据标记）失败了。这样做允许你在不影响整体测试结果的情况下识别和记录已知的问题。

其执行结果参考如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_params_mark_xfail.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 4 items

test_fixture_params_mark_xfail.py::test_add[positive numbers] PASSED
test_fixture_params_mark_xfail.py::test_add[positive and negative] PASSED
test_fixture_params_mark_xfail.py::test_add[both zeros] PASSED
test_fixture_params_mark_xfail.py::test_add[negative numbers] XPASS (Negative numbers expected to fail)

========================== 3 passed, 1 xpassed in 0.02s =======================
root@Gavin:~/code/chapter1-6#
```



## 6.7.6 自动调用fixture

pytest允许测试者设置一段代码以供多个测试用例使用，而不需要在每个测试用例中重复相同的设置代码，这就是fixture，但当用例很多的时候，用例调用fixture每次都传fixture参数，会很麻烦。fixture里面有个参数autouse，默认是False没开启的，使用 `autouse` 参数可以使 fixture 自动地应用到测试中，而无需显式在测试用例函数的参数列表中声明它。

autouse设置为True，自动调用fixture功能，这意味着对于每个测试函数，无论是在同一模块还是某个范围（由 `scope` 参数定义）内的测试，此 fixture 都会在测试函数执行前自动运行，**包括类中的测试用例和类以外的测试用例**。我们来看一个示例：

```python
# content of test_fixture_autouse.py
import pytest


@pytest.fixture(autouse=True, scope="function")
def function_autouse():
    """   When autouse is True, each test case, this applies to every test case   """
    print("\n---Before---")
    yield
    print("---After---")

# function_autouse 函数的autouse=True时，无论是否使用usefixtures引用function_autouse, 
# 还是传递 function_autouse 到测试用例，都会执行function_autouse
@pytest.mark.usefixtures("function_autouse")
def test_case01():
    print("Test case 1")

def test_case02():
    print("Test case 2")

class Test:
    def test_case03(self):
        print("Test case 3")
```

定义了一个fixture function_autouse，并设置autouse=True，在测试用例test_case01例借助@pytest.mark.usefixtures装饰器显示的使用fixture function_autouse，测试方法test_case02 和测试类Test下的测试用例图test_case03并没有显示注入fixture function_autouse。由于fixture function_autouse设置了autouse=True，test_fixture_autouse.py文件中的所有测试用例都会执行fixture function_autouse。

运行效果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_autouse.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items

test_fixture_autouse.py::test_case01 
---Before---
Test case 1
PASSED---After---

test_fixture_autouse.py::test_case02 
---Before---
Test case 2
PASSED---After---

test_fixture_autouse.py::Test::test_case03 
---Before---
Test case 3
PASSED---After---

============================== 3 passed in 0.01s =============================
root@Gavin:~/code/chapter1-6#
```

**注意事项：**

- 当你有多个标记为 `autouse=True` 的 fixtures 时，它们将按照声明的顺序被执行。
- 即使 fixture 被自动使用，你仍然可以通过明确指名来显式地调用它，这样做主要是为了在测试中获取到由该 fixture 返回的数据。
- 在合理使用 `autouse=True` 时，要注意不要滥用，因为这可能会导致测试执行环境变得复杂，特别是在处理多个测试文件和更大的测试套件时，可能难以跟踪哪些 fixtures 正在使用和导致潜在的侧面效应。

## 6.7.7 params与ids

在 `pytest` 中使用 `params` 时，可以通过配合 `ids` 参数来给每组参数传递一个自定义的标识符。这使得测试结果更清晰易读，因为每组参数的意图和区别可以通过其 `id` 被更清楚地展示。 

当然也可以通过`@pytest.mark.parametrize`装饰器实现参数化，关于`@pytest.mark.parametrize`，我们会在下一章节中详细介绍。

使用`ids` 的好处在于：它为每组参数定义了一个易读的名称，当测试结果被打印出来时，这些名称将会显示，帮助你快速识别每个测试用例。`params` 和 `ids` 的使用方法又稍有不同，接下来的示例中，我们一探差异。

```python
# content of test_fixture_ids.py
import pytest

# 测试的目标函数
def multiply(a, b):
    return a * b

# 参数化的fixture
@pytest.fixture(params=[
    (1, 2, 2),
    (2, 3, 6),
    (3, 3, 9)
], ids=[
    "positive numbers",
    "more positive numbers",
    "identical numbers"
])
def mult_data(request):
    return request.param

# 使用fixture的测试函数
def test_multiply(mult_data):
    a, b, expected = mult_data
    assert multiply(a, b) == expected
```

在这个例子中，我们用 `@pytest.fixture` 装饰了 `mult_data` 函数，并用 `params` 参数传递了一个列表，该列表中包含了多个元组，每个元组代表一组参数值。同时，我们使用 `ids` 参数为每组参数提供一个描述性的标识符。

如果你希望自定义每个参数集的 `id`，例如基于参数值，你可以传一个函数给 `ids` 参数。这个函数将会接受一个参数（就是参数化的值）并且返回一个字符串：

```python
# content of test_fixture_ids_customizations.py
import pytest

# 测试的目标函数
def multiply(a, b):
    return a * b

# 自动生成ids的函数
def idfn(fixture_value):
    return "params: {0}".format(fixture_value)

# 参数化的fixture，使用函数自动生成ids
@pytest.fixture(params=[
    (1, 2, 2),
    (2, 3, 6),
    (3, 3, 9)
], ids=idfn)
def mult_data(request):
    return request.param

# 使用fixture的测试函数
def test_multiply(mult_data):
    a, b, expected = mult_data
    assert multiply(a, b) == expected
```

这样在测试结果中，例如，第一组参数将会有一个名字 `params: (1, 2, 2)`，帮助你更好地了解每个测试的背景。

两者执行效果参考如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_ids.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items

test_fixture_ids.py::test_multiply[positive numbers] PASSED
test_fixture_ids.py::test_multiply[more positive numbers] PASSED
test_fixture_ids.py::test_multiply[identical numbers] PASSED

============================== 3 passed in 0.01s =============================
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_ids_customizations.py 
============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items

test_fixture_ids_customizations.py::test_multiply[params: (1, 2, 2)] PASSED
test_fixture_ids_customizations.py::test_multiply[params: (2, 3, 6)] PASSED
test_fixture_ids_customizations.py::test_multiply[params: (3, 3, 9)] PASSED

============================== 3 passed in 0.01s =============================
root@Gavin:~/code/chapter1-6#
```

**综合应用示例**

**场景描述**

购买AI智能体，支付状态有三种：

* 下单未支付
* 成功支付
* 支付失败/放弃支付

这三种状态对应数据库中三种值，分别为0，1，2。 利用ids方式，来简化测试用例。

**代码示例**

```python
# content of test_AI_agent_order_status.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


def init_data(fixture_value):
    if fixture_value == 0:
        return "NoPay"
    elif fixture_value == 1:
        return "PaySuccess"
    elif fixture_value == 2:
        return "DropPay"


@pytest.fixture(params=[0, 1, 2], ids=init_data)
def my_AI_fixture(request):
    req_param = request.param
    print("\nParameter : [{}], status is : [{}]".format(req_param, req_param))
    yield req_param
    print("\n----------------------------------------")


def test_case_01(my_AI_fixture):
    print("\nRun [{}] test case".format(my_AI_fixture))
```

运行结果：

```shell
root@Gavin:~/code/chapter1-6# pytest -vrs test_AI_agent_order_status.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items

test_AI_agent_order_status.py::test_case_01[NoPay] PASSED                [ 33%]
test_AI_agent_order_status.py::test_case_01[PaySuccess] PASSED           [ 66%]
test_AI_agent_order_status.py::test_case_01[DropPay] PASSED              [100%]

============================== 3 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-6#
```


利用 -k 参数，指定要指定的测试用例：

```shell
root@Gavin:~/code/chapter1-6# pytest -vrs -k "PaySUccess" test_AI_agent_order_status.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 3 items / 2 deselected / 1 selected

test_AI_agent_order_status.py::test_case_01[PaySuccess] PASSED          [100%]

========================== 1 passed, 2 deselected in 0.01======================
root@Gavin:~/code/chapter1-6#
```

 在当前Linux下“pytest-7.4.0”版本，-k 后面字符串使用单引号或者双引号都可以；但对于Windows下的“pytest-7.4.2”版本，单引号会报错。建议统一使用双引号。

## 6.7.8 params与name

`pytest` 允许你通过 `name` 参数为 fixture 赋予一个别名，这样你就可以使用一个与 fixture 函数名称不同的名称来引用 fixture。使用 `name` 参数的一个理由是避免命名冲突，或者当你想要为 fixture 提供一个更具描述性的名称时。

当你为 `@pytest.fixture` 装饰器提供 `name` 参数时，你可以使用该名称作为 fixture 的引用，而不是使用函数名。这在函数名可能与你想要在测试中使用的名称冲突时非常有用。

下面是一个如何使用 `name` 参数声明 fixture 并在测试函数中引用它的例子：

```python
# content of test_fixture_name.py
import pytest

# 这是一个模拟的 create_database_connection 函数
def create_database_connection():
    """假设这是创建数据库连接的函数"""
    print("Creating database connection...")
    return "database_connection"

@pytest.fixture(name="db_connection")
def setup_database_connection():
    """设置数据库连接的 fixture，注意使用了 name 参数"""
    try:
        connection = create_database_connection()
        yield connection
    finally:
        print("Closing database connection...")
        # 这里你会关闭真实的数据库连接
        # connection.close()

def test_database_query(db_connection):
    """测试数据库查询"""
    # 这里将模拟数据库查询
    assert db_connection == "database_connection"
```

在编写实际代码时，你会将 `create_database_connection` 替换为实际创建数据库连接的逻辑，并确保测试函数中使用数据库连接的方式是正确的。在这个简化的示例中，我们只是假设 `create_database_connection` 返回了一个字符串，并在测试中验证这个字符串是否等于预期的值。其执行结果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_name.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 1 item

test_fixture_name.py::test_database_query Creating database connection...
PASSEDClosing database connection...

============================== 1 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-6#
```

`name` 参数的好处在于可以提供更加语义化的命名，或者在装饰器和实际的测试函数之间提供清晰的界限。在大型的测试套件中，可能存在多个具有类似或通用功能的 fixture，通过提供一个 `name`，可以帮助在不同部分之间做出明确的区分。

如果不使用 `name` 参数，fixture 的名称将默认为函数名。如果有一个全局的变量或者导入的模块与你的 fixture 函数同名，可能会发生命名冲突。此时，使用 `name` 参数就显得尤为重要。

```python
import pytest
from some_module import cleanup

@pytest.fixture(name="cleanup")
def prepare_and_cleanup():
    prepare_something()
    yield
    cleanup()
```

在上述示例中，`cleanup` 来自另一个模块和作为 fixture 函数的本地定义冲突，因此使用 `name="cleanup"` 为 fixture 赋予别名，使得在调用 fixture 时可以避免命名冲突。当在测试中引用 `cleanup` 时，实际上引用的是 `prepare_and_cleanup` fixture，而不是 `some_module.cleanup` 函数。

`name` 参数提供了在定义 fixtures 时更灵活的命名策略，有助于避免命名冲突，并且保持代码的可读性和组织性。

**请注意：**

声明 fixture 时添加了 `name` 参数后，就必须始终使用这个别名来引用它。

我们来看一个示例，测试过程如下：

```python
# content of test_fixture_name_not_usename.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.fixture(params=['Parameter1', 'Parameter2'], ids=["id-01", "id-02"], name="Test_Fixture_Name_Daemon")
def my_fixture(request):
    return request.param


def test_fixtures_03(my_fixture):
    print('\n Run test_fixtures_03')
    print(my_fixture)
```

如上，代码执行时报如下错误信息：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_name_not_usename.py 
============================== test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code/chapter1-6
collected 1 item

test_fixture_name_not_usename.py::test_fixtures_03 ERROR

================================= ERRORS ========================================
______________________ ERROR at setup of test_fixtures_03 _______________________
file /root/code/chapter1-6/test_fixture_name_not_usename.py, line 12
  def test_fixtures_03(my_fixture):
E       fixture 'my_fixture' not found
>       available fixtures: Test_Fixture_Name_Daemon, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, session_scope, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/root/code/chapter1-6/test_fixture_name_not_usename.py:12
============================= short test summary info ===========================
ERROR test_fixture_name_not_usename.py::test_fixtures_03
============================= 1 error in 0.01s ==================================
root@Gavin:~/code/chapter1-6#
```

## 6.7.9 fixture几种清理

`pytest` 提供了几种方法来实现 `fixture` 的清理逻辑：使用 `yield`、`with` 语句以及 `addfinalizer` 方法。这些方法都可以确保在测试过程中打开的资源得到适当的释放。下面是每种方法的介绍、代码示例和 yield 与 addfinalizer 间的区别。

### 6.7.9.1 使用 `yield` 的 `fixture`

使用 `yield` 是实现 `fixture` 清理逻辑的推荐方法。在 `yield` 之前的代码是设置代码，之后的代码是清理代码。

```python
# content of yield_fixture.py
# 使用 yield 的 fixture
import pytest

@pytest.fixture
def resource():
    print("Setting up")
    resource = acquire_resource()
    yield resource
    print("Tearing down")
    release_resource(resource)

def acquire_resource():
    return "resource"

def release_resource(resource):
    pass
```

在上述代码中，`resource` `fixture` 创建了一个资源，并在 `yield` 之后释放了它。`yield` 关键字后面的表达式会被返回给请求这个 `fixture` 的测试函数。一旦测试用例结束，`fixture` 将继续执行 `yield` 之后的代码，即清理代码。

### 6.7.9.2 使用 `with` 语句的 `fixture`

在某些情况下，需要使用支持上下文管理（context manager）的资源。在这些情况下，可以结合 `with` 语句与 `fixture` 使用。with 语句帮助确保资源正确关闭，即使测试引发了异常。

```python
# content of test_with_yield_fixture.py
# 使用 with 语句的 fixture
import pytest

@pytest.fixture
def resource_with_context_manager():
    print("Setting up with context manager")
    with open('file.txt', 'w') as file:
        yield file
    # 文件在上下文退出时自动关闭

def test_example(resource_with_context_manager):
    assert not resource_with_context_manager.closed
```

在这个例子中，`fixture` 打开一个文件，并将其作为生成器返回。`with` 语句确保即使测试中出现异常，文件也会被正确关闭。

### 6.7.9.3 使用 `addfinalizer` 方法的 `fixture`

`addfinalizer` 允许你在 fixture 函数中注册一个或多个清理函数（finalizer），这些函数会在测试结束时自动执行。`addfinalizer` 的主要优势是清理代码的调用时机更灵活，它是在 `fixture` 函数之中注册的一个清理回调。

```python
# content of addfinalizer_fixture.py
# 使用 addfinalizer 的 fixture
import pytest

@pytest.fixture
def resource_with_addfinalizer(request):
    print("Setting up")
    resource = acquire_resource()

    def resource_finalizer():
        print("Tearing down")
        release_resource(resource)
    # 注册清理函数
    request.addfinalizer(resource_finalizer)

    return resource
```

在此代码中，我们定义了一个清理函数 `resource_finalizer`，使用 `request` 对象的 `addfinalizer()` 方法注册这个函数作为测试完毕后的回调。`addfinalizer` 允许注册多个独立的清理函数，并在 fixture 作用域结束时按先进后出的顺序运行。相比于 `yield`，`addfinalizer` 的灵活性在于可以在 `fixture` 函数的任何地方添加清理逻辑，而 yield 只能在一个地方提供。

### 6.7.9.4 yield 与 addfinalizer 的比较

以下是 `yield` 与 `addfinalizer` 在 `pytest` 中使用的对比：

| 特性             | yield                                               | addfinalizer                                |
| ---------------- | --------------------------------------------------- | ------------------------------------------- |
| 简便性           | 使用简单，可读性强                                  | 较为复杂，灵活性更高                        |
| 异常安全         | 如果 `yield` 前的代码抛出异常，清理代码可能不会执行 | 清理函数总会执行，即使之前的代码抛出了异常  |
| 清理函数数量     | 一次只能指定一块清理代码                            | 可以添加多个清理函数                        |
| 清理函数执行顺序 | 清理代码块中的代码按书写顺序执行                    | 清理函数按注册的相反顺序执行（LIFO）        |
| 注册位置         | 只能在 `yield` 后添加清理代码                       | 在 `fixture` 函数任何位置都可以注册清理函数 |
| 清理的复杂性     | 清理逻辑相对简单                                    | 可以定义复杂的清理逻辑                      |

这两种方法都提供了实现 `fixture` 清理步骤的有效方式。`yield` 提供了快速、直观的方法来写设置和清理代码，而 `addfinalizer` 提供更大的灵活性，但可能会使代码略显复杂。

总的来说，yield 被认为是更简洁、读起来更直观的方法。然而，当需要更高灵活性，或者当需要在不同点注册多个清理逻辑时，addfinalizer 提供了更强大的功能。选择使用哪一种方法取决于具体的测试需求和个人偏好。

### 6.7.9.5 总结

不同的清理方式适用于不同的应用场景。通常，使用 `yield` 方法已足够满足大部分测试清理需求，并且代码较为简洁。但是当遇到需要精细控制的情况——比如需要注册多个清理步骤，或者清理步骤的顺序很重要时——使用 `addfinalizer` 方法会更为合适。而使用 `with` 语句则适用于上下文管理器支持的情况，例如文件操作或数据库会话。在选择哪种方式时，考虑资源的性质，以及清理步骤的具体需求。



## 6.7.10 fixture的并列与嵌套

`fixture` 不但支持共享 ，还可以“并列”（side by side）使用，也可以“嵌套”（nested）。

`fixture` 并列：一个测试场景同时调用多个`fixture` 。

`fixture`嵌套：一个`fixture` ，可以做另外一个`fixture` 的参数。

### 6.7.10.1 并列的 fixture

“并列”意味着两个或多个`fixture`在同一测试函数中独立地使用，互不影响。测试函数可以同时接受多个`fixture`作为参数，此时每个`fixture`负责设置和清理自己的测试环境或数据。这些`fixture`的执行顺序取决于它们在测试函数参数列表中的顺序。

```python
# content of test_fixture_side_by_side.py
import pytest

@pytest.fixture
def fixture_one():
    print("\nSetup fixture_one")
    yield
    print("\nTeardown fixture_one")

@pytest.fixture
def fixture_two():
    print("\nSetup fixture_two")
    yield
    print("\nTeardown fixture_two")

def test_multiple_fixtures(fixture_one, fixture_two):
    print("\nRunning test with multiple fixtures")
```

在这个示例中，`fixture_one`和`fixture_two`作为并列的修饰器并传递到`test_multiple_fixtures`测试函数。设置 (setup) 部分会按照参数在函数中的顺序执行，然后是测试函数本身的执行，最后是清理 (teardown) 部分，即先执行`fixture_one`的setup，再执行`fixture_two`的setup，接着执行`fixture_two`的teardown和`fixture_one`的teardown，其执行结果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_side_by_side.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_fixture_side_by_side.py::test_multiple_fixtures 
Setup fixture_one

Setup fixture_two

Running test with multiple fixtures
PASSED
Teardown fixture_two

Teardown fixture_one

============================ 1 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-6#
```

### 6.7.10.2 嵌套的 fixture

“嵌套”意味着一个`fixture`可以使用另一个`fixture`，这种情况下，内部的（嵌套的）`fixture`会先于外部的`fixture`执行其设置和清理过程。对于嵌套`fixture`的设置部分，会以嵌套顺序执行，而清理过程则会以相反的顺序执行。

```python
# content of test_fixture_nested_example.py
import pytest

@pytest.fixture
def outer_fixture():
    print("\nSetup outer_fixture")
    yield
    print("\nTeardown outer_fixture")

@pytest.fixture
def inner_fixture(outer_fixture):
    print("\nSetup inner_fixture")
    yield
    print("\nTeardown inner_fixture")

def test_nested_fixture(inner_fixture):
    print("\nRunning test with nested fixture")
```

在这个例子中，`inner_fixture`使用了`outer_fixture`，因此在执行`inner_fixture`之前会先执行`outer_fixture`的设置部分。当测试运行完成后，会先执行`inner_fixture`的清理过程，然后是`outer_fixture`的清理过程。执行结果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_fixture_nested_example.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_fixture_nested_example.py::test_nested_fixture 
Setup outer_fixture

Setup inner_fixture

Running test with nested fixture
PASSED
Teardown inner_fixture

Teardown outer_fixture

=============================== 1 passed in 0.01s ===========================
root@Gavin:~/code/chapter1-6#
```

再来看一个比较接近实战级别的测试用例，如下示例通过`selenium webdriver`访问对应URL 获取GET请求信息并透过`yield`返回`driver`，用例中调用 `fixture_button` 时`fixture_driver` 作为 `fixture_button` 的参数被触发，效果同上一个测试用例。

```python
# content of test_fixture_webdriver_nested.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "www.google.com"


@pytest.fixture()
def fixture_driver():
    driver = webdriver.Chrome()
    driver.get(URL)
    yield driver
    driver.close()


@pytest.fixture()
def fixture_button(fixture_driver):
    # fixture_driver 作为 fixture_button 的参数，当用例中调用 fixture_button 时，
    # fixture_button 会自动调用 fixture_driver
    print("I'm fixture_button, start")
    yield fixture_driver
    print("I'm fixture_button, end")
```

### 6.7.10.3 多个fixture的实例化顺序

由于存在fixture的并列、嵌套以及作用域（scope），如何理解这些复杂关系以及fixture的执行顺序变得尤为重要，但请记住，多个fixture的实例化顺序遵循如下规则：

* **作用域优先级原则**： 高级别作用域（scope）的 `fixture` 将优先实例化。`pytest` 支持四种级别的作用域：`function`、`class`、`module` 和 `session`。作为最高级别，`session` 作用域的 `fixture` 在测试会话开始时实例化，并在所有测试完成后进行清理。`module` 作用域的 `fixture` 在相应模块的首次调用时实例化，直到该模块的所有测试用例运行完成后才清理。`class` 作用域的 `fixture` 用于类中的测试，而 `function` 作用域的 `fixture` 对于每个测试函数都会单独实例化和清理。这种层次化管理确保了不同范围内的测试资源可以有效利用。

* **声明顺序和依赖关系原则**： 当多个 `fixture` 有相同的作用域时，它们的实例化顺序首先基于它们在测试函数或 `fixture` 函数中的声明顺序。`fixture` 按照它们在参数列表中的顺序实例化，前提是没有任何相互依赖关系。如果 `fixture` 之间存在依赖关系，如一个 `fixture` 作为另一个 `fixture` 的输入参数，则被依赖的 `fixture` 先被实例化，即使被依赖的 `fixture` 后声明。

* **自动使用 (autouse) 原则**： 设置了 `autouse=True` 属性的 `fixture` 无需在测试函数中显式声明，它会被自动应用到相应作用域内的所有测试函数中。如果作用域内存在多个 `autouse=True`的 `fixture`，它们将按声明顺序实例化。此外，这些自动使用的 `fixture` 会在同级别作用域中非自动使用 `fixture` 实例化之前激活，确保了所需的测试环境或前置条件始终在测试开始之前满足。

* **参数化 (parametrization) 原则**： 对于参数化的 `fixture`，`pytest` 会为每个参数值生成一个 `fixture` 实例。如果在测试函数中使用了参数化的 `fixture`，`pytest` 将为每个参数值运行测试函数一次，实例化相应的 `fixture`，即使有多个参数也会保持这种独立运行的特性。

* **清理 (teardown) 顺序原则**： `fixture` 的清理顺序与实例化顺序相反。这意味着最后实例化的 `fixture` 会首先进行清理，这是为了保持资源释放的逻辑与生命周期管理的一致性。

先来看一个示例代码：

```python
# content of test_multiple_fixture_instantiation_order.py
import pytest

# Session scope fixture
@pytest.fixture(scope="session")
def session_fixture():
    print("\n[Setup] session_fixture")
    yield
    print("\n[Teardown] session_fixture")

# Module scope fixture
@pytest.fixture(scope="module")
def module_fixture():
    print("\n[Setup] module_fixture")
    yield
    print("\n[Teardown] module_fixture")

# Function scope fixture
@pytest.fixture
def function_fixture():
    print("\n[Setup] function_fixture")
    yield
    print("\n[Teardown] function_fixture")

# Fixture with a parameter
@pytest.fixture(params=["param1", "param2"])
def parametrized_fixture(request):
    param = request.param
    print(f"\n[Setup] parametrized_fixture with {param}")
    yield param
    print(f"\n[Teardown] parametrized_fixture with {param}")

# Nested fixture
@pytest.fixture
def nested_fixture(function_fixture, parametrized_fixture):
    print("\n[Setup] nested_fixture")
    yield f"nested-{parametrized_fixture}"
    print("\n[Teardown] nested_fixture")

# Test function using multiple fixtures
def test_complex_fixtures(session_fixture, module_fixture, nested_fixture):
    print("\nRunning test with complex fixtures")
```

这个示例稍微复杂一些，解释说明如下：

**作用域不同的 `fixture`**:

- `session_fixture`: 作用域为整个测试会话，只在会话开始时设置一次，结束时清理一次。
- `module_fixture`: 作用域为整个模块，对于每个模块设置一次，模块结束时清理。
- `function_fixture`: 默认作用域，每个测试函数运行时设置，结束时清理。

**参数化的 `fixture` (`parametrized_fixture`)**:

- 这个 `fixture` 对于每个参数（"param1" 和 "param2"）都会运行一次。它演示了如何对 `fixture` 进行参数化。

**嵌套 `fixture` (`nested_fixture`)**:

- `nested_fixture` 依赖于 `function_fixture` 和 `parametrized_fixture`。在它的设置部分运行之前，这两个依赖的 `fixture` 会首先运行。
- 这个 `fixture` 演示了嵌套 `fixture` 的特性，它合并了从依赖的 `fixture` 获得的数据。

**测试函数 `test_complex_fixtures`**:

- 这个测试函数使用了 `session_fixture`、`module_fixture` 和 `nested_fixture`。
- 根据 `fixture` 在函数参数中的顺序，`pytest` 首先实例化 `session_fixture`（如果会话中尚未实例化），然后是 `module_fixture`（如果模块中尚未实例化），最后是 `nested_fixture` 及其依赖的 `fixture`。

**执行流程**:

- 当运行 `test_complex_fixtures` 时，首先根据作用域实例化 `session_fixture` 和 `module_fixture`（如果尚未实例化）。
- 接着按顺序实例化 `nested_fixture` 的依赖（`function_fixture` 和 `parametrized_fixture`），然后是 `nested_fixture` 本身。
- 在测试执行完成后，首先按相反顺序进行 `fixture` 的清理，先是 `nested_fixture`，然后是它的依赖，最后是 `session_fixture` 和 `module_fixture`（如果是会话或模块的最后一个测试）。

运行结果：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_multiple_fixture_instantiation_order.py 
============================== test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_multiple_fixture_instantiation_order.py::test_complex_fixtures[param1] 
[Setup] session_fixture

[Setup] module_fixture

[Setup] function_fixture

[Setup] parametrized_fixture with param1

[Setup] nested_fixture

Running test with complex fixtures
PASSED
[Teardown] nested_fixture

[Teardown] parametrized_fixture with param1

[Teardown] function_fixture

test_multiple_fixture_instantiation_order.py::test_complex_fixtures[param2] 
[Setup] function_fixture

[Setup] parametrized_fixture with param2

[Setup] nested_fixture

Running test with complex fixtures
PASSED
[Teardown] nested_fixture

[Teardown] parametrized_fixture with param2

[Teardown] function_fixture

[Teardown] module_fixture

[Teardown] session_fixture

============================= 2 passed in 0.02s ============================
root@Gavin:~/code/chapter1-6#
```

再来看一个例子，这次部分`fixture`携带上`autouse=True`参数：

```python
# content of test_multiple_fixture_instantiation_order2.py
import pytest

# Session scope fixture; automatically used for all tests in the session
@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    print("\nSetting up session_fixture")
    yield
    print("\nTearing down session_fixture")

# Module scope fixture; not automatically used, must be explicitly declared
@pytest.fixture(scope="module")
def module_fixture():
    print("\nSetting up module_fixture")
    yield
    print("\nTearing down module_fixture")

# Test function scope fixture; automatically used for all tests in the module
@pytest.fixture(autouse=True)
def function_fixture():
    print("\nSetting up function_fixture")
    yield
    print("\nTearing down function_fixture")

# A parametrized fixture that is used explicitly
@pytest.fixture(params=[1, 2])
def parametrized_fixture(request):
    param = request.param
    print(f"\nSetting up parametrized_fixture with param {param}")
    yield param
    print(f"\nTearing down parametrized_fixture with param {param}")

# Nested fixture depending on module_fixture and parametrized_fixture
@pytest.fixture
def nested_fixture(module_fixture, parametrized_fixture):
    print("\nSetting up nested_fixture")
    yield f"nested with param {parametrized_fixture}"
    print("\nTearing down nested_fixture")

# Test function using multiple fixtures
def test_example(nested_fixture):
    print("\nRunning test_example")
```

**解释和说明：**

在这个示例中，我们定义了一系列的 `fixture`，每一个都有不同的作用域和用法：

1. `session_fixture`: 会话（session）范围的 `fixture`，会在整个测试会话的开始自动设置一次，并在结束时自动清理。
2. `module_fixture`: 模块（module）范围的 `fixture`，将在模块中的第一个需要它的测试开始时设置，并在模块中的最后一个测试完成后清理。
3. `function_fixture`: 函数（function）范围的 `fixture`，并且由于设定了 `autouse=True`，它将自动用于模块中的每个测试函数。
4. `parametrized_fixture`: 参数化的 `fixture`，它将根据参数生成多个环境实例。此 `fixture` 必须在测试函数中显式声明才能使用。
5. `nested_fixture`: 依赖于 `module_fixture` 以及 `parametrized_fixture` 的嵌套 `fixture`。它将在调用 `parametrized_fixture` 为每个参数生成实例，并在 `module_fixture` 后面设置。
6. `test_example`: 使用 `nested_fixture` 的测试函数。尽管 `nested_fixture` 是显式声明在测试函数中的唯一 `fixture`，它实际上还暗含了 `module_fixture` 和 `parametrized_fixture` 的使用，因为它依赖于这两个 `fixture`。

**实例化顺序规则**:

- `session_fixture` 由于其作用域和 `autouse=True` 属性，它会在所有其他 `fixture` 之前设置。
- `function_fixture` 同样由于 `autouse=True` 会在测试函数运行之前设置，但由于作用域限制为函数，它会在每个涉及它的测试函数之前设置并在每个测试函数之后清理。
- 对于 `test_example` 来说，`module_fixture` 将在 `nested_fixture` 之前设置，因为后者依赖于前者。
- `parametrized_fixture` 会为其所有参数生成实例，但只在 `nested_fixture` 实例化时才会进行，因此顺序排在 `module_fixture` 之后。
- 在清理过程中，与设置顺序相反，嵌套的 `fixture` 首先清理，之后是模块和函数范围的 `fixture`，会话范围的 `fixture` 最后清理。

运行结果：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_multiple_fixture_instantiation_order2.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_multiple_fixture_instantiation_order2.py::test_example[1] 
Setting up session_fixture

Setting up module_fixture

Setting up function_fixture

Setting up parametrized_fixture with param 1

Setting up nested_fixture

Running test_example
PASSED
Tearing down nested_fixture

Tearing down parametrized_fixture with param 1

Tearing down function_fixture

test_multiple_fixture_instantiation_order2.py::test_example[2] 
Setting up function_fixture

Setting up parametrized_fixture with param 2

Setting up nested_fixture

Running test_example
PASSED
Tearing down nested_fixture

Tearing down parametrized_fixture with param 2

Tearing down function_fixture

Tearing down module_fixture

Tearing down session_fixture

============================== 2 passed in 0.02s ============================
root@Gavin:~/code/chapter1-6#
```

### 6.7.10.4 fixture返回工厂函数

**应用场景：**

当你想要在测试过程中动态创建一些配置可变的对象时，可以使用 `fixture` 来返回一个工厂函数。工厂函数允许你按需生成对象，并在测试中应用不同的配置或状态。这种方式在你需要根据测试用例的不同需求来重用和定制对象时非常有用，例如：

- 创建具有不同初始数据的数据库实例。
- 生成带有各种设置的模拟对象或服务。
- 动态构建带有特定配置的测试环境或上下文。

上述内容理解起来可能有点晦涩，我们再举两个例子帮助读者理解一下：

* 如果有一个需要基于不同国家创建日期格式化的情况发生，就可以用工厂函数来根据国家信息返回正确的日期格式化对象，比起直接实例化具体的日期格式化类，工厂函数方式更加简洁和灵活。
* 如果一个测试用例多次使用到同一个`fixture`实例，相较于返回数据，返回一个产生数据的工厂函数会更好。

**示例代码：**

```python
# content of test_fixture_factory.py
import pytest

# 假设我们有一个简单的用户模型类
class User:
    def __init__(self, name, is_admin=False):
        self.name = name
        self.is_admin = is_admin

# 返回一个工厂函数的 fixture，可创建具有不同名称和权限的 User 对象
@pytest.fixture
def user_factory():
    
    created_users = []

    def _create_user(name, is_admin=False):
        user = User(name, is_admin)
        created_users.append(user)
        return user

    yield _create_user

    # 清理代码：在测试完成后，你可以执行所需的清理工作，比如删除数据库中的用户记录。
    for user in created_users:
        print(f"Deleting user {user.name} from database...")

# 测试函数中使用工厂函数来创建用户
def test_new_user(user_factory):
    alice = user_factory("Alice")
    bob = user_factory("Bob", is_admin=True)
    assert not alice.is_admin
    assert bob.is_admin
```

**详细解释：**

上述代码包含了以下几个关键点：

* `User` 类代表了一个简单的用户模型，其中包含用户的名字和权限（是否为管理员）。
* `user_factory` 是一个 `fixture`，它返回了 `_create_user` 工厂函数。该工厂函数接受一个名字和一个可选的管理员状态，用以创建不同类型的 `User` 对象。
* `created_users` 列表用于追踪所有由工厂函数创建的 `User` 对象。
* 在 `yield` 后面的代码块执行测试函数运行完成后的清理工作。在本例中，它只是打印出一条消息表示删除用户，但在真实应用中，你可能需要执行一些数据库清理操作。
* 在测试 `test_new_user` 中，我们调用 `user_factory` 来创建两个 `User` 对象：一个普通用户 `Alice` 和一个管理员 `Bob`。然后检查它们的权限是否符合预期。

通过使用 `fixture` 返回工厂函数，可以根据测试函数中的具体要求动态生成合适的测试对象。这种方式保持了测试代码的可读性和灵活性，还可以根据需要进行适当的资源清理。

### 6.7.10.5 利用pytest.mark.usefixtures叠加**调用多个fixture**

如果一个方法或者一个class用例想要同时调用多个fixture，可以使用@pytest.mark.usefixtures()进行叠加。注意叠加顺序，先执行的放底层，后执行的放上层。

**请注意：**

* 与直接传入fixture不同的是，@pytest.mark.usefixtures无法获取到被fixture装饰的函数的返回值。
* @pytest.mark.usefixtures的使用场景是：被测试函数需要多个fixture做前后置工作时使用。

```python
# content of test_pytest_mark_usefixtures_stacking_calls_multiple_fixtures.py
import  pytest


@pytest.fixture()
def fixture_func_1():
    print("Before Function 1")
    yield
    print("After Function 1")

@pytest.fixture()
def fixture_func_2():
    print("Before function 2")
    yield
    print("After Function 2")

@pytest.fixture()
def fixture_func_3():
    print("Before Function 3")
    yield
    print("After Function 3")


@pytest.mark.usefixtures("fixture_func_3")  # 最后执行fixture_func_3
@pytest.mark.usefixtures("fixture_func_2")  # 再执行fixture_func_2
@pytest.mark.usefixtures("fixture_func_1")  # 先执行fixture_func_1
def test_func():
    print("This is test case")
```



输出结果：



```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_pytest_mark_usefixtures_stacking_calls_multiple_fixtures.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_pytest_mark_usefixtures_stacking_calls_multiple_fixtures.py::test_func Before Function 1
Before function 2
Before Function 3
This is test case
PASSEDAfter Function 3
After Function 2
After Function 1

=============================== 1 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-6#
```

# 6.8 在不同层级上重写fixture

在 `pytest` 中，你可以在不同的层级（如会话、包或模块级别）上重写 `fixture`。这样做可以针对不同的测试场景定制 `fixture` 的行为，而且更深层级的 `fixture` 会覆盖上层级的 `fixture`。这使得你能够为不同的测试案例优化测试环境，同时保持代码的可读性和易维护性。

## 6.8.1 重写conftest.py中的fixture

假设我们正在测试一个web应用，需要在多数测试中使用SQLite数据库进行测试。不过，对于特定的一组测试，我们想要使用具有不同数据库配置的MySQL数据库。在这种情况下，我们可以在较高层级定义一个使用SQLite的 `fixture`，并在需要用MySQL测试的特定模块级别上重写这个 `fixture`。

项目的目录结构可能如下：

```shell
/tests/
    conftest.py
    test_general.py
    /mysql_specific/
        conftest.py
        test_mysql.py
```

根目录下的 `conftest.py` 文件定义了全局 `db` `fixture`：

```python
# /tests/conftest.py
import pytest
import sqlite3

@pytest.fixture
def db():
    print("Setting up SQLite db")
    connection = sqlite3.connect(":memory:")
    yield connection
    connection.close()
```

现在我们写了一些使用 SQLite 的测试用例：

```python
# /tests/test_general.py
def test_general(db):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT)")
    # ...更多的测试代码...
    db.commit()
```

对于特定的 MySQL 测试，我们将在子目录 `/mysql_specific` 内重写 `db` `fixture`：

```python
# /tests/mysql_specific/conftest.py
import pytest
import pymysql

@pytest.fixture
def db():
    print("Setting up MySQL db")
    connection = pymysql.connect(host='localhost', user='root', password='', db='Gavin')
    yield connection
    connection.close()
```

最后，我们将使用新的 `db` `fixture` 编写针对 MySQL 的测试用例：

```python
# /tests/mysql_specific/test_mysql.py
def test_mysql(db):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    # ...更多的测试代码...
    db.commit()
```

在这个例子中，在 `tests/` 目录下的 `conftest.py` 中定义了一个涉及 SQLite 数据库的全局 `db` `fixture`。这个 `fixture` 在整个测试会话中能够被所有的测试用例共享。

然而，我们想对 `/tests/mysql_specific/` 目录下的测试用例使用 MySQL 数据库。为了满足这种特殊需求，我们在该目录下的 `conftest.py` 中重写了 `db` `fixture`，它现在使用 `pymysql` 库设置 MySQL 数据库连接。由于 `pytest` 的 `fixture` 查找机制遵循从测试函数开始向上查找直至找到第一个 `fixture` 的策略，`/mysql_specific/` 目录下的测试用例将使用覆盖了的 MySQL 版本的 `db` `fixture`。

为确保上述代码能够有效执行，还需要做一些额外准备工作：

**安装mysql server和 pymysql：**

```shell
apt install mysql-server
pip install pymysql
```

准备一脚本用于创建mysql db(Gavin)和一张表(t_student)：

```python
# content of create_mysql_db_table.py
import pymysql
# 建立数据库连接 写自己的Navicat主机、用户名、密码、字符集参数
con = pymysql.connect(host='localhost', user='root',
                      passwd='', charset='utf8')
# 创建游标对象
cur = con.cursor()
# 检查数据库是否已经存在
cur.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'Gavin'")
result = cur.fetchone()
# 如果数据库不存在，则创建它
if not result:
    cur.execute('create database Gavin character set utf8')
# 切换到数据库
cur.execute('use Gavin')
#编写创建表的sql
sql = """
    create table t_student(
    sno int primary key auto_increment,
    sname varchar(30) not null,
    age int(20),
    score float(3,1)
    ) 
    """
#执行sql
try:
    cur.execute(sql)
    print("创建表成功")
except Exception as e:
    print(e)
    print("创建失败")
finally:
    cur.close()
    con.close()
```

**解决mysql 1698错误：**

```shell
root@Gavin:~/code/chapter1-6# python3 create_mysql_db_table.py 
Traceback (most recent call last):
  File "/root/code/chapter1-6/create_mysql_db_table.py", line 3, in <module>
    con = pymysql.connect(host='localhost', user='root',
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pymysql/connections.py", line 358, in __init__
    self.connect()
  File "/usr/local/lib/python3.11/dist-packages/pymysql/connections.py", line 664, in connect
    self._request_authentication()
  File "/usr/local/lib/python3.11/dist-packages/pymysql/connections.py", line 954, in _request_authentication
    auth_packet = self._read_packet()
                  ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pymysql/connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/dist-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/dist-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.OperationalError: (1698, "Access denied for user 'root'@'localhost'")
root@Gavin:~/code/chapter1-6# 
root@Gavin:~/code/chapter1-6# 
root@Gavin:~/code/chapter1-6# mysql -u root 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 8.0.35-0ubuntu0.23.10.1 (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> USE mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

mysql> exit;
Bye
root@Gavin:~/code/chapter1-6# service mysql restart
```

**然后执行创建db与table操作：**

```shell
root@Gavin:~/code/chapter1-6# python3 create_mysql_db_table.py 
创建表成功
root@Gavin:~/code/chapter1-6#
```

**查看创建的数据库与表信息：**

```shell
root@Gavin:~/code/chapter1-6/tests# mysql -uroot -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 18
Server version: 8.0.35-0ubuntu0.23.10.1 (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> use Gavin;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+-----------------+
| Tables_in_Gavin |
+-----------------+
| t_student       |
+-----------------+
1 row in set (0.00 sec)

mysql> exit;
Bye
root@Gavin:~/code/chapter1-6/tests# 
```

最后，分别执行上述两个测试用例，其执行效果如下：

```shell
root@Gavin:~/code/chapter1-6/tests# pytest -s -v test_general.py 
======================== test session starts ==================================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_general.py::test_general Setting up SQLite db
PASSED

========================== 1 passed in 0.01s ==================================
root@Gavin:~/code/chapter1-6/tests#pytest -s -v mysql_specific/test_mysql.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

mysql_specific/test_mysql.py::test_mysql Setting up MySQL db 'Gavin'
PASSED

=============================== 1 passed in 0.03s =============================
root@Gavin:~/code/chapter1-6/tests#
```

执行完`mysql_specific/test_mysql.py`后会看到在mysql Gavin这个db中出现一个新表user：

```shell
mysql> use Gavin;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+-----------------+
| Tables_in_Gavin |
+-----------------+
| t_student       |
| users           |
+-----------------+
2 rows in set (0.00 sec)

mysql>
```

## 6.8.2 在模块层级重写fixture

在 `pytest` 中，如果你在 `conftest.py` 文件和同一模块的其他测试文件中定义了同名的 `fixture`，那么在这个模块内，测试用例将会使用测试文件中定义的 `fixture`。这是因为 `pytest` 在解析 `fixture` 时，会优先选择更接近测试函数的 `fixture` 定义。不过，如果你在模块中的 `fixture` 需要访问 `conftest.py` 中定义的同名 `fixture`，你可以使用 `pytest` 的 `usefixtures` 装饰器或者直接返回 `conftest.py` 中 `fixture` 的值。但请注意，同模块级访问并重写 `conftest.py` 中的同名 `fixture` 是一种不常见的做法，通常情况下应避免这样做。

假设你的 `conftest.py` 里有如下 `fixture`：

```python
# content of conftest.py
import pytest

@pytest.fixture
def my_fixture():
    return "original fixture value"
```

在同一模块的测试文件中，你可以这样定义一个新的 `fixture` 来覆盖原始 `fixture`：

```python
# content of test_module.py
import pytest

# 这个 fixture 名称不同于 conftest.py 中的 fixture
@pytest.fixture
def conftest_my_fixture(my_fixture):
    # 访问并返回 conftest.py 中的 fixture 值
    return my_fixture  # 这里 my_fixture 会调用 conftest.py 中的 fixture

# 在 test_module.py 中重写 my_fixture ，并访问 conftest_my_fixture
@pytest.fixture
def my_fixture(conftest_my_fixture):
    # 附加一些改动到原始值
    return f"modified {conftest_my_fixture}"

def test_my_fixture(my_fixture):
    # 测试现在使用重写过的 my_fixture
    assert my_fixture == "modified original fixture value"
```

在这个示例中：

- `conftest_my_fixture` 用于访问和返回 `conftest.py` 里定义的 `my_fixture`。
- 当我们在 `test_module.py` 中定义 `my_fixture` 时，`my_fixture` 将使用 `test_module.py` 中定义的 `fixture`。我们可以在这个新定义中通过访问 `conftest_my_fixture` 以获取 `conftest.py` 中的原始值，并对其进行修改。
- `test_my_fixture` 测试函数会调用新定义的 `my_fixture` `fixture`，其值已经是修改过的字符串。

其执行结果参考如下：

```shell
root@Gavin:~/code/chapter1-6/module_overwrite_fixture# pytest -s -v test_module.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_module.py::test_my_fixture PASSED

============================== 1 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-6/module_overwrite_fixture#
```

这种方法在不同的层级重写 `fixture` 时允许你访问和修改高层级或全局 `fixture` 的值，同时保持了 `pytest` 的 `fixture` 查找和使用机制的一致性。不过，通常不鼓励这样重写 `fixture`，因为它会使得测试代码中的依赖关系变得复杂且难以理解。如果可能，最好的做法是设计独立的 `fixture`，仅在需要时使用 `fixture` 参数显式覆盖或增强。

## 6.8.3 参数化重写fixture

在 `pytest` 中，你实际上不能在用例的参数中“重写”一个 `fixture`，因为用例的参数是用于接收 `fixture` 的值，而不是定义或改变它们。然而，你可以使用**参数化 (parametrization)** 来对 `fixture` 进行“重写”或调整，这样可以在执行测试用例时传递不同的参数到 `fixture` 中。

**使用场景：**

假设我们正在进行一个网络服务的测试，我们希望对同一个API端点使用不同的查询字符串参数来执行测试。我们可以通过参数化一个 `fixture` 来实现这一点，这样我们的测试函数就可以接受不同的 `fixture` 实例，每个实例都使用一个不同的查询参数。

**代码示例与注解：**

下面是如何用参数化来实现这一点的示例：

定义一个 `conftest.py` 文件，其中包含一个带参数的 `api_query` `fixture`：

```python
# content of conftest.py

import pytest

# 这是基础的 API query fixture，参数将决定具体的查询字符串
@pytest.fixture(params=["query1", "query2", "query3"])
def api_query(request):
    # 基于提供的参数构造 query 字符串
    query_string = f"?type={request.param}"
    return query_string
```

在测试文件中，使用 `api_query` `fixture`：

```python
# content of test_api.py

# 这个测试用例将被三次执行，每次使用一个不同的query_string
def test_api(api_query):
    url = f"http://example.com/api" + api_query
    # 模拟发送 API 请求（这里用打印 URL 代替）
    print(f"Requesting {url}")
    # ... 发送请求并断言响应 ...
    assert True
```

**运行效果：**

```shell
root@Gavin:~/code/chapter1-6/parameterize_overwrite_fixture# pytest -s -v test_api.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_api.py::test_api[query1] Requesting http://example.com/api?type=query1
PASSED
test_api.py::test_api[query2] Requesting http://example.com/api?type=query2
PASSED
test_api.py::test_api[query3] Requesting http://example.com/api?type=query3
PASSED

============================= 3 passed in 0.02s ==============================
root@Gavin:~/code/chapter1-6/parameterize_overwrite_fixture#
```

`pytest` 会解析 `conftest.py` 中的参数化 `fixture`，并且将每个参数值逐一传递到 `api_query` `fixture` 中，生成不同的查询字符串。测试用例 `test_api` 将被执行三次，每一次使用的 `api_query` 参数都不一样，分别对应 `["query1", "query2", "query3"]`。

通过这种方法，我们能够动态地生成不同的测试场景，从而节省编码时间且保持测试代码简洁。这种“重写 fixture 参数”的方式不仅可以用于字符串，也可以用于对象、配置字典等复杂结构，使得我们的测试更加灵活且能够覆盖更广泛的情况。

## 6.8.4 参数化fixture重写非参数化fixture，反之亦然

在 `pytest` 中，一个参数化的 `fixture` 可以重写非参数化的 `fixture`，反之亦然。这允许测试者根据测试需求调整 `fixture` 的行为，无论是为了提供不同的配置选项，还是为了生成不同的测试案例。

### 6.8.4.1 使用场景

* **参数化的fixture重写非参数化的fixture**: 假设你在进行Web应用的测试，你有一个通用的 `fixture` 用于设置浏览器。现在，对于某一组特定的测试，你希望能够测试不同类型的浏览器，比如 Chrome、Firefox 和 Safari。在这种情况下，你可以使用参数化的 `fixture` 来重写原有的非参数化 `fixture`。
* **非参数化的fixture重写参数化的fixture**: 假设你已经有了一个参数化的数据库配置 `fixture`，它可以根据不同的参数设置不同的数据库。然而，对于某些特定的测试，你可能只想使用一个特定的数据库配置。在这种情况下，你可以使用一个非参数化的 `fixture` 来重写原有的参数化 `fixture`，从而为这些特定的测试提供一个固定的配置。

### 6.8.4.2 参数化的fixture重写非参数化的fixture

**非参数化的 `conftest.py`:**

```python
# content of conftest.py
import pytest

@pytest.fixture
def browser():
    print("Open a Chrome browser for testing")
    yield "Chrome"
    print("Close the browser")
```

**参数化的 `test_browser.py`:**

```python
# content of test_browser.py
import pytest

# 参数化的 fixture 覆盖了非参数化的 fixture
@pytest.fixture(params=["Chrome", "Firefox", "Safari"])
def browser(request):
    print(f"Open a {request.param} browser for testing")
    yield request.param
    print("Close the browser")

def test_browser(browser):
    print(f"Testing on {browser}")
    assert browser in ["Chrome", "Firefox", "Safari"]
```

在这个例子中，原始的 `browser` `fixture` 仅仅设置了 Chrome 浏览器。通过在 `test_browser.py` 中定义一个同名的参数化 `fixture`，我们重写了原始的 `fixture`，使其可以根据参数打开不同的浏览器。这样，`test_browser` 会针对每种浏览器类型运行一次。

### 6.8.4.3 非参数化的fixture重写参数化的fixture

**参数化的 `conftest.py`:**

```python
# content of conftest.py
import pytest

# 参数化的数据库配置 fixture
@pytest.fixture(params=["dev", "test", "prod"])
def db_config(request):
    configs = {
        "dev": "Development DB",
        "test": "Test DB",
        "prod": "Production DB"
    }
    yield configs[request.param]
```

**非参数化的 `test_specific_db.py`:**

```python
# content of test_specific_db.py
import pytest

# 重写参数化的 fixture 以提供特定的数据库配置
@pytest.fixture
def db_config():
    print("Using Test DB for this specific test")
    yield "Test DB"

def test_db(db_config):
    print(f"Testing with {db_config}")
    assert db_config == "Test DB"
```

在这个例子中，`conftest.py` 文件中的 `db_config` `fixture` 是参数化的，它可以为不同的数据库环境提供配置。然而，在 `test_specific_db.py` 中，我们重写了 `db_config` `fixture` 以确保所有测试都使用测试数据库。这对于那些只适用于特定环境的测试来说非常有用。

通过上述示例，我们可以看到，无论是参数化覆盖非参数化，还是非参数化覆盖参数化，`pytest` 提供了极大的灵活性来根据测试的具体需求调整 `fixture` 的行为。这种能力使得 `pytest` 成为一个非常强大且灵活的测试框架。


# 6.9 conftest.py文件

`conftest.py` 是 `pytest` 中一个用于存放配置信息，如固件 (fixtures)，钩子函数 (hook functions)，以及其它的插件代码的特殊文件。它不是普通的 python 模块，而是一个特殊的 pytest 插件，允许用户在不改变测试用例代码的情况下，共享在多个文件中使用的测试固件或钩子，比如你可以在这个文件里面编写fixture函数，这个fixture函数的作用，就相当于Unittest框架里面的`setup()`前置函数和`teardown()`后置函数，虽然pytest框架也有`setup()`前置函数和`teardown()`后置函数，但是在实际工作中没必要写在测试用例文件中，直接写在`conftests.py`里面就好了，pytest框架会自动去找`conftest.py`文件里面的东西，这样更灵活。

在实际工作中，通常`conftest.py`和`@pytest.fixture()`结合使用，实现全局的前后置应用。

本章节将详细介绍 `conftest.py` 的使用方法和代码实例，帮助理解其在自动化测试中的应用。



## 6.9.1 `conftest.py` 文件的查找和加载机制

`pytest` 会自动发现项目目录及子目录中的所有 `conftest.py` 文件，并在测试开始前加载它们。只会加载每个目录中的最顶层 `conftest.py` 文件，也就是说，在子目录中的 `conftest.py` 会覆盖父目录中的配置。

## 6.9.2 conftest.py使用场景

`conftest.py`的应用场景非常广泛，包含但不限于：

* 每个用例需共用到的token/session/cookie

* 每个用例需共用到的测试用例数据

* 每个用例需共用到的配置信息

* 当需要对多个测试文件共享固件时

* 当需要在钩子中插入逻辑以配置测试行为、执行额外的初始化或资源清理时

* 当需要注册自定义标记或配置命令行参数时

* 定制钩子函数来添加`pytest`的行为

* 搜集并处理测试需要的数据

* 导入外部的插件或自定义的插件

* 管理测试用的配置数据和状态信息

  ....

以下是广泛使用 `conftest.py` 的几种典型场景：

* 共享固件：在 `conftest.py` 中定义的固件可以被同一目录以及子目录中的所有测试用例共享使用。
* 存放自定义钩子函数：用户可以自定义钩子函数，用于扩展或修改 `pytest` 的内置行为。
* 注册自定义标记：在 `conftest.py` 中可以定义和注册自定义标记 (markers)，便于标记和过滤测试用例。
* 添加命令行选项：通过 `conftest.py`，可以向 `pytest` 命令行接口添加自定义选项。
* 集成外部的插件：加载和配置外部 `pytest` 插件。



## 6.9.3 conftest.py中fixture的作用域

 fixture的scope参数也适用`conftest.py`文件中fixture的特性，即有如下范围：

| 取值     | 范围     | 说明                                                         |
| -------- | -------- | ------------------------------------------------------------ |
| function | 函数级   | 每个函数或方法都会调用                                       |
| class    | 类级别   | 每个测试类只运行一次                                         |
| module   | 模块级别 | 每一个.py文件只调用一次                                      |
| package  | 包级     | 每一个python包只调用一次                                     |
| session  | 会话级   | 每次会话只需要运行一次，会话内所有方法及类、模块都共享这个方法 |



## 6.9.4 不同位置conftest.py文件的作用域

一个项目可以包含多个 `conftest.py` 文件，每个文件的作用域仅限于它所在的目录和子目录里的测试模块。当运行测试时，`pytest` 会收集所有相关目录下的 `conftest.py` 文件，并相应地应用它们提供的配置。

* 在测试框架的根目录创建`conftest.py`文件，文件中的`fixture`的作用范围是所有测试模块

-  在某个单独的测试文件夹里创建`conftest.py`文件，文件中`fixture`的作用范围，就仅局限于该测试文件夹里的测试模块；该测试文件夹外的测试模块，或者该测试文件夹外的测试文件夹，是无法调用到这个`conftest.py`文件中的`fixture`。
-  如果测试框架的根目录和子包中都有`conftest.py`文件，并且这两个`conftest.py`文件中都有一个同名的`fixture`，实际生效的是测试框架中子包目录下的`conftest.py`文件中配置的`fixture`（即此场景下子目录下的`conftest.py`会覆盖父目录的`conftest.py`）



## 6.9.5 conftest.py使用方法

### 6.9.5.1 共享fixture

固件可以设定不同的作用域（函数级别、类级别、模块级别、会话级别）。例如，定义一个会话级别的固件，为全局数据库连接提供配置：

```python
# conftest.py
import pytest
import mydatabase

@pytest.fixture(scope="session")
def db():
    return mydatabase.connect()
```

再比如：

```python
# conftest.py
import pytest

@pytest.fixture(scope="module")
def database():
    from myapp import create_db
    db = create_db()
    yield db
    db.close()

@pytest.fixture(scope="session")
def client():
    from myapp import Client
    return Client()

```

例如，你有一个web应用需要在测试之前登录，你可以创建一个`fixture`来管理这个过程。

```python
# conftest.py
import pytest
from myapp import create_app
from myapp.models import User

@pytest.fixture(scope='module')
def client():
    app = create_app('testing')
    client = app.test_client()

    with app.app_context():
        user = User(email='test@example.com', password='password')
        user.save()

    return client
```

这样在同一目录下的所有测试模块中，只要需要登录，就可以使用`client fixture`来复用这段登录代码。

### 6.9.5.2 自定义参数

使用 `conftest.py`，可以添加自定义命令行选项，如下所示：

```python
def pytest_addoption(parser):
    parser.addoption("--custom", action="store", default="default",
                     help="The custom option to pass something.")
```

这样，就可以通过 `--custom` 标志在命令行中选择性地运行自定义测试：

```bash
pytest --custom
```



### 6.9.5.3 钩子函数

可以在 `conftest.py` 中定义一个自定义的测试收集钩子，该钩子会在收集所有测试项之后执行：

```python
# conftest.py
def pytest_collection_modifyitems(items):
    for item in items:
        # 添加自定义行为，例如跳过某些特定的测试
        if "skip" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="This test is skipped."))
```



定义钩子来处理测试的各个阶段，例如自定义测试收集阶段的行为：

```python
def pytest_collection_modifyitems(config, items):
    if config.getoption("--custom") != "default":
        # 自定义收集规则，比如跳过某些特定的测试
        skip_marker = pytest.mark.skip(reason="Need --custom option to run")
        for item in items:
            if "custom" in item.keywords:
                item.add_marker(skip_marker)
```

在上述代码中，定义了两个固件：`database` 和 `client`。`database` 固件具有模块作用域，意味着它在单个测试模块中只会被调用一次，而 `client` 固件则在整个测试会话中都可用。

再比如下面的示例：

```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "env(name): mark test to run only on named environment")
```

该函数会在测试开始之前被调用，你可以在这里做一些配置化的工作。这里我们定义了一个名为"env"的marker，可以用来标记只在特定环境下运行的测试。

钩子函数还允许你在测试流程中的特定时刻注入代码，对测试行为进行自定制。

**代码示例：**

```python
# conftest.py
def pytest_configure(config):
    # 项目初始化时的配置
    config.addinivalue_line("markers", "slow: Mark test as slow to run")

def pytest_report_header(config):
    # 测试报告的标题
    return "项目名称: 我的测试项目"
```

这里定义了两个钩子函数：`pytest_configure` 用于在测试运行之前进行一些配置，如定义自定义标记；`pytest_report_header` 可以在测系报告中添加一些自定义的头部信息。

### 6.9.5.4 自定义标记 (marker) 注册示例

如果要引入一个名为 `slow` 的新 marker 以标记运行缓慢的测试，可以在 `conftest.py` 中注册该 marker，然后使用：

```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: mark test as slow to run"
    )
```



在 `conftest.py` 中可以定义自定义标记，这些标记可以用于特殊的测试用例，比如标记执行速度缓慢的测试。

**代码示例：**

```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark tests as slow")

```

定义了一个名为 `slow` 的标记后，在测试函数上使用 `@pytest.mark.slow` 即可应用该标记。

**使用自定义标记的测试用例：**

```python
# test_example.py
import pytest

@pytest.mark.slow
def test_example(database):
    assert database.is_connected()
```

### 6.9.5.5 小贴士

- 定义固件时，如果你希望它能够被多个测试函数复用，请确保设置适当的作用域（例如 `session`，`module` 等）。
- 如果在一个大型项目中使用多个 `conftest.py` 文件，请注意它们的作用域和覆盖规则，以避免产生混乱。
- 钩子函数和自定义标记在处理复杂的测试用例选择或测试环境定制时，可提供极大的灵活性。



## 6.9.6 conftest.py结语

`conftest.py` 是 `pytest` 测试框架中一个强有力的工具，它提供了一种组织和共享测试代码的优雅方式，同时也大大增强了 `pytest` 的配置灵活性和测试代码的再利用性。它是 `pytest` 自动化测试项目的强大支持工具，尤其是在测试项目规模较大，或者需要高度定制测试行为时。通过掌握 `conftest.py`，合理地使用 `conftest.py` 文件，可以更高效地编写和管理测试代码，确保测试的高可维护性和扩展性。

**conftest.py文件须知：**


* conftest.py文件名字是固定的，不能做任何修改，把hook或者fixture写在这个文件里，就会自动去调用
* 文件和用例文件在同一个目录下，那么conftest.py作用于整个目录，即所有同目录测试文件运行前都会执行conftest.py文件
* conftest.py文件不能被其他文件导入
* pytest框架中的`setup()/teardown()`函数，`setup_class()/teardown_class()`函数，他们是作用于所有用例或者所有类的
* `@pytest.fixtrue()`的作用域是既可以部分用例，也可以全部用例的前后置
* `conftest.py`文件和`@pytest.fxtrue()`装饰器结合使用，作用于全局用例的前后置
* 可以跨.py文件调用，有多个.py文件调用时，可让conftest.py只调用了一次fixture，或调用多次fixture；

conftest.py与运行的用例要在同一个pakage下，并且有__init__.py文件；

* 不需要import导入conftest.py，pytest用例会自动识别该文件，放到项目的根目录下就可以全局目录调用了，如果放到某个package下，那就在package内有效，可有多个conftest.py
* 所有同目录测试文件运行前都会执行conftest.py文件



# 6.10 本章小结

本章节中，我们深入探讨了`pytest`中的`fixture`机制，并介绍了它的重要性和用法。`fixture`是`pytest`中一个强大而灵活的概念，它提供了在测试执行过程中管理和共享资源的机制。它通过使用装饰器 `@pytest.fixture`，可以在测试用例执行前后进行设置和清理操作，诸如创建和初始化对象、连接和断开数据库、模拟网络请求等。通过将`fixture`作为参数传递给测试用例，我们可以在测试用例中访问`fixture`提供的资源和功能。这种方式使得我们可以更好地组织和管理测试用例的依赖关系。

我们还介绍了`fixture`的多种用法和特性。例如，我们可以使用 `autouse` 参数使`fixture`自动应用于所有测试用例，或者使用 `scope` 参数控制`fixture`的作用范围。`fixture`还支持参数化，使我们能够根据不同的测试场景提供不同的fixture实例。

`pytest`中的`fixture`机制是测试代码编写中不可或缺的一部分。它提供了一个强大而灵活的方式来管理和共享资源，使我们能够更好地组织和执行测试用例。通过充分理解和运用`fixture`，我们可以提高测试代码的可读性、可维护性和可扩展性。建议在编写测试用例时，根据测试用例的需求和依赖关系，合理地设计和使用`fixture`。我们还提醒在`fixture`中遵循良好的资源管理实践，确保资源的正确释放和清理，以避免资源泄漏和测试干扰。
