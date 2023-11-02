---
layout:     post
title:      "pytest 之 fixture"
subtitle:   "pytest of fixture"
date:       2023-10-25
author:     "Gavin"
catalog:    true
tags:
    - Automation
    - pytest
---



# 概述



## pytest的fixture是什么？

fixture是pytest的大杀器，是pytest特有的功能，是精髓所在，fixture有两种实现方式：

* xunit-style，跟unittest框架的机制非常相似，即setup/teardown系列
  
* 自己的fixture机制，以@pytest.fixture装饰器来申明

主要的目的是为了提供一种可靠和可重复性的手法去运行那些最基本的测试内容。





## pytest优势



从功能上看来，它与setup、teardown相似，但是优势明显，如下：



### **命令灵活**

​        对于setup.teardown，可以不起这两个名字，即不局限于setup和teardown这几个命名



### **数据共享**

​    （1）在conftest.py配置里写的方法可以实现数据共享，不需要import导入，就能自动找到一些配置，可以跨文件共享

​    （2）按模块化的方式实现，每个fixture都可以互相调用



### **实现参数化**

​    @pytest.fixture()有5个参数，如下：

```@pytest.fixture(scope="", params="", autouse="", ids="", name="") ```



**(1) scope**

scope的层次及神奇的yield组合相当于各种setup和teardown，可以跨函数function，类class，模块module或整个测试session范围



| 取值     | 范围     | 说明                                                         |
| -------- | -------- | ------------------------------------------------------------ |
| function | 函数级   | 每个函数或方法都会调用                                       |
| class    | 类级别   | 每个测试类只运行一次                                         |
| module   | 模块级别 | 每一个.py文件只调用一次                                      |
| package  | 包级     | 每一个python包只调用一次                                     |
| session  | 会话级   | 每次会话只需要运行一次，会话内所有方法及类、模块都共享这个方法 |



**(2) params**

参数化（支持，列表，元组，字典列表[{},{},{}]，字典元组({},{},{}) )

params将在下一篇文章中进行描述。



**(3) autouse**

自动执行fixture，默认False表示不开启，可以设置为True开启自动使用fixture功能，这样用例就不用每次都去传参了(自动调用fixture功能)。

使用autouse时，需要慎重，避免范围失控。



**(4) ids**

参数化时，给每一个值设置一个变量名

ids将在下篇文章，和params一起进行描述。



**(5) name**

给@pytest.fixture()标记的方法取一个别名，意义不大





# xunit-style 风格

官方文档：

 ``` https://docs.pytest.org/en/stable/how-to/xunit_setup.html#xunitsetup ```



总结如下：

* 每个级别的setup/teardown都可以多次复用
* 如果相应的初始化函数执行失败或者被跳过则不会执行teardown方法



## function级别



示例：

```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


def setup_function(function):
    print('\nDo something before function')


def teardown_function(function):
    print('Do something after function')


def test_case_1():
    print('  Test function-1')


def test_case_2():
    print('  Test function-2')

```



文件命名为test_functionLevel.py



**输出结果：**



```
# pytest -sq test_functionLevel.py

Do something before function
  Test function-1
.Do something after function

Do something before function
  Test function-2
.Do something after function

2 passed in 0.02s
```



**说明**：

  通过输出结果我们可以总结：

  * setup_function会在每一个测试函数前执行初始化操作
  * teardown_function会在每一个测试函数执行后执行销毁工作



## method级别



示例:




```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


class TestMethod(object):

    def setup_method(self, method):
        print('\nBefore')

    def teardown_method(self, method):
        print('After')

    def test_case_1(self):
        print('Test case1')

    def test_case_2(self):
        print('Test case2')
```



文件命名为test_methodLevel.py



**输出结果**




```
Before
Test case1
.After

Before
Test case2
.After

2 passed in 0.00s
```



**说明**：



  通过输出结果我们可以总结：

  * setup_method会在每一个测试方法前执行初始化操作
  * teardown_method会在每一个测试方法执行后执行销毁工作，且方法级别的fixture是作用在测试类中的方法上的



## class级别



示例



```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


class TestClass(object):

    @classmethod
    def setup_class(cls):
        print('\nsetup_class() for {}'.format(cls.__name__))

    @classmethod
    def teardown_class(cls):
        print('teardown_class() for {}'.format(cls.__name__))

    def test_case_1(self):
        print('self.test_case_1()')

    def test_case_2(self):
        print('self.test_case_2()')
```



文件命名为test_classLevel.py



**输出结果**



```
# pytest -sq test_classLevel.py

setup_class() for TestClass
self.test_case_1()
.self.test_case_2()
.teardown_class() for TestClass

2 passed in 0.02s
```



**说明:**

通过输出结果我们可以总结：

  * setup_class会在测试类执行前执行一次初始化操作
  * teardown_class会在测试类执行后执行一次销毁工作，且class级别的fixture需要使用@classmethod装饰



## module级别



示例



```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


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



文件命名为test_moduleLevel.py



**输出结果**



```
# pytest -sq test_moduleLevel.py

setup_module() for test_moduleLevel
test_case_1()
.test_case_2()
.self.test_case_3()
.self.test_case_4()
.teardown_module() for test_moduleLevel

4 passed in 0.02s
```



**说明:**



通过输出结果我们可以总结：

  * setup_module会在测试函数或类执行前执行一次初始化操作
  * teardown_module会在测试函数或类执行后执行一次销毁工作





# pytest的fixture实现方式



通过@pytest.fixture装饰器来定义fixture，一个函数被@pytest.fixture装饰，那么这个函数就是fixture。

使用fixture时，分为二个部分：fixture定义、fixture调用。

除此之外，还有fixture的共享机制，嵌套调用机制。



## 定义fixture



* fixture通过函数实现

* 使用@pytest.fixture进行装饰

  ```
  import pytest
  
  @pytest.fixture()
  def login_init():
      print("Start login option")
      yield 
      print("End of login")
  ```

  

* 前置准备工作代码和后置清理工作代码，都写在一个函数里面

* 通过yeild关键字，区分前置代码和后置代码 。yeild之前的代码为前置代码，yeild之后的代码为后置代码

​        在实际应用场景当中，可以只有前置准备工作代码，也可以只有后置清理工作代码。

* fixture有4个作用域

  测试会话(session)、测试模块(module)、测试类(class)、测试用例(function)

​       测试会话：pytest执行测试用例的整个过程，称为会话。

​       比如pytest收集到了20条用例并执行完成，这个过程称为测试会话。

​       设置fixture的作用域：通过@pytest.fixture(scope=作用域)来设置。默认情况下，scope=function

* fixture的返回值设置：yeild 返回值

​        当测试用例当中，要使用fixture里生成的数据时，则需要fixture返回数据。

​        若有数据返回则：yeild 返回值



## 调用fixture



在fixture定义好之后，可以明确：

* fixture处理了哪些前置准备工作、哪些后置清理工作
* fixture作用在哪个范围(是测试函数？还是测试类？还是测试会话？还是测试模块？)



在以上两点都定下来了之后，接下来就是在测试用例当中，根据需要调用不同的fixture。



调用方法有两种：

* 在测试用例/测试类上面加上：@pytest.mark.usefixture("fixture的函数名字")
* 将fixture函数名，作为测试用例函数的参数



第2种用法，主要是用参数来接收fixture的返回值，以便在测试用例中使用。



第一种方式案例如下：



```
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





第二种方案如下：



```
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



```
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





## **fixture嵌套**



fixture不但支持共享 ，还支持嵌套使用。**嵌套使用即：一个fixture，可以做另外一个fixture的参数。**



如下图所示：名为init2的fixture，可以作为init的参数。

并且，init当中，将init2的返回值，同样返回。



```
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





## Fixture的其他用法





### 提供灵活的类似setup和teardown功能



pytest的fixture另一个强大的功能就是在函数执行前后增加操作，类似setup和teardown操作，但是比setup和teardown的操作更加灵活。具体使用方式是同样定义一个函数，然后用装饰器标记为fixture，然后在此函数中使用一个yield语句，yield语句之前的就会在测试用例之前使用，yield之后的语句就会在测试用例执行完成之后再执行。



```
import pytest

@pytest.fixture()
def run_function():
    print("Run before function...")
    yield
    print("Run after function...")

def test_case_1(run_function):
    print("case 1")

def test_case_2():
    print("case 2")

def test_case_3(run_function):
    print("case 3")
```



输出结果如下：



```
# pytest -sq test_fixture.py
Run before function...
case 1
.Run after function...
case 2
.Run before function...
case 3
.Run after function...

3 passed in 0.02s
```



从结果可以看出，"test case 2" 并没有执行 run_function 这个fixture，因为没有传递这个fixture作为函数到 test_case_2；还有另外一个原因：run_function  这个fixture中没有携带autouse和scope参数，默认请看下 autouse=False, scope="function"，如果更改成如下示例，就是另外一番场景了:



```
import pytest

@pytest.fixture(autouse=True, scope='function')
def run_function():
    print("Run before function...")
    yield
    print("Run after function...")

def test_case_1(run_function):
    print("case 1")

def test_case_2():
    print("case 2")

def test_case_3(run_function):
    print("case 3")
```



输出结果:



```
# pytest -sq test_fixture.py
Run before function...
case 1
.Run after function...
Run before function...
case 2
.Run after function...
Run before function...
case 3
.Run after function...

3 passed in 0.02s
```



下文会介绍到autouse的用法，此处不做更详细描述。





### 利用pytest.mark.usefixtures叠加**调用多个fixture**



如果一个方法或者一个class用例想要同时调用多个fixture，可以使用@pytest.mark.usefixtures()进行叠加。注意叠加顺序，先执行的放底层，后执行的放上层。需注意：



① 与直接传入fixture不同的是，@pytest.mark.usefixtures无法获取到被fixture装饰的函数的返回值；

② @pytest.mark.usefixtures的使用场景是：被测试函数需要多个fixture做前后置工作时使用；

```text
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



```
# pytest -sq test_fixture3.py
Before Function 1
Before function 2
Before Function 3
This is test case
.After Function 3
After Function 2
After Function 1

1 passed in 0.02s
```





### fixture自动使用autouse=True

当用例很多的时候，每次都传这个参数，会很麻烦。fixture里面有个参数autouse，默认是False没开启的，可以设置为True开启自动使用fixture功能，这样用例就不用每次都去传参了。

autouse设置为True，自动调用fixture功能，所有用例都会生效，**包括类中的测试用例和类以外的测试用例**。



示例：



```text
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





输出结果：



```
# pytest -sq test_fixture4.py

---Before---
Test case 1
.---After---

---Before---
Test case 2
.---After---

---Before---
Test case 3
.---After---

3 passed in 0.00s
```





### Pytest fixture四种作用域



```text
fixture(scope='function'，params=None，autouse=False，ids=None，name=None)
```



上文有提到fixture的5种作用域，这里直接展示示例。



#### function级别

function默认模式为@pytest.fixture() 函数级别，即scope="function"，scope可以不写。每一个函数或方法都会调用，每个测试用例执行前都会执行一次function级别的fixture。



```text
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



输出结果：



```
# pytest -sq test_fixture_scope_function.py

Before function Level
func 1 print
.After function Level
func 2 print
.
2 passed in 0.01s
```







#### class级别



fixture的scope值还可以是class，此时则fixture定义的动作就会在测试类class的所有用例之前和之后运行。



**注意：**

测试类中只要有一个测试用例的参数中使用了class级别的fixture，则在整个测试类的所有测试用例都会调用fixture函数。



##### 用例类中的测试用例调用fixture



执行fixture定义的动作，以及此测试类的所有用例结束后同样要运行fixture指定的动作



```text
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



输出结果如下：



```
# pytest -sq test_class_level_autouse1.py

 class Before
class 1 print
.class 2 print
.class after

2 passed in 0.02s
```



##### 用例类外的测试用例调用fixture



如果在类外的函数中去使用class级别的fixture，则此时在测试类外每个测试用例中，fixture跟function级别的fixture作用是一致的，即在类外的函数中引用了class级别的fixture，则在此函数之前和之后同样去执行fixture定义的对应的操作。



```text
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



```
# pytest -sq test_class_level_autouse2.py

 class Before
class 1 print
.class 2 print
.class after

 class Before
class 3 print
.class after

3 passed in 0.02s
```



#### module级别



在Python中module即.py文件（可以理解为当前的.py文件为一个测试suit，因为这个.py文件里含有一个或多个测试用例集合），当fixture定义为module时，则此fixture将在当前文件中起作用。

这里需要特别说明的是，当fixture的scope定义为module时，只要当前文件中有一个测试用例使用了fixture，不管这个用例是在类外，还是在类中，都会在当前文件（模块）的所有测试用例执行之前去执行fixture定义的行为以及当前文件的所有用例结束之后同样去执行fixture定义的对应操作。



```text
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



```
# pytest -sq test_module_scope.py

Before module Level
Yest case of scope
.case scope 01
.case scope 02
.case scope 03
.After module Level-

4 passed in 0.01s

```



若类中的方法分别调用了class级别的fixture和module级别的fixture，则会两个fixture都生效：

```text
# 顺序在前面fixture会先执行
def test_scope_01(self, module_scope, class_scope): 
    print("case scope 01")
```



若类中的方法同时调用了function级别、class级别、module级别的fixture，则3种fixture会同时生效：

```text
# 顺序在前面fixture会先执行
def test_scope_02(self, module_scope, class_scope, function_scope):  
    print("case scope 02")
```



#### session级别(使用conftest.py共享fixture)



当fixture的scope定义为session时，是指在当前目录下的所有用例之前和之后执行fixture对应的操作。



**fixture为session级别是可以跨.py模块调用**的，也就是当我们有多个.py文件的用例的时候，如果多个用例只需调用一次fixture，那就可以设置为scope="session"，并且写到conftest.py文件里。



使用方式：

* 定义测试用例文件
* 构建conftest.py内容



**说明：**

在指定目录下创建**conftest.py（固定命名，不可修改）**文件，然后在conftest.py文件中定义fixture方法，将scope指定为session，此时在当前目录下只要有一个用例使用了此fixture，则就会在当前目录下所有用例之前和之后会执行fixture定义的对应的操作。

```text
import pytest

@pytest.fixture(scope="session")
def session_scope():
    """  A session-level fixture that works for all test cases in that directory  """
    print("\nUse case pre-operations at the session level")
    yield
    print("Post-operation of use cases at the session level")
```



定义了session级别的fixture，存放于该用例文件的同一个目录下的conftest.py文件中，该目录下的任一用例文件中的任一测试用例，引用了这个session级别的fixture，则这个session级别的fixture会针对这整个用例文件会生效。若存放在根目录下，则针对整个工程的所有用例都会生效。

```text
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



```
# pytest -sq test_fixture_session_scope.py

Use case pre-operations at the session level
session 1 print
.session 2 print
.session 3 print
.Post-operation of use cases at the session level

3 passed in 0.01s
```





#### ids参数-修改用例结果名称



将在下一篇文字中，结合@pytest.mark.parametrize() 进行描述，本文忽略。



#### name参数-重命名fixture函数名称



将在下一篇文字中，结合@pytest.mark.parametrize() 进行描述，本文忽略。



#### params参数-提供返回值供测试函数调用



 将在下一篇文字中，结合@pytest.mark.parametrize() 进行描述，本文忽略。





#### 内置fixture



##### tmpdir和tmpdir_factory

内置的tmpdir和tmpdir_factory负责在测试开始运行前创建临时文件目录，并在测试结束后删除。

如果测试代码要对文件进行读/写操作，那么可以使用tmpdir或tmpdir_factory来创建文件或目录。单个测试使用tmpdir，多个测试使用tmpdir_factory。tmpdir的作用范围是函数级别，tmpdir_factory的作用范围是会话级别。



```text
def test_tmpdir(tmpdir):
    # tmpdir already has a path name associated with it
    # join() extends the path to include a filename
    # the file is created when it's written to
    a_file = tmpdir.join('something.txt')

    # you can create directories
    a_sub_dir = tmpdir.mkdir('anything')

    # you can create files in directories (created when written)
    another_file = a_sub_dir.join('something_else.txt')

    # this write creates 'something.txt'
    a_file.write('contents may settle during shipping')

    # this write creates 'anything/something_else.txt'
    another_file.write('something different')

    # you can read the files as well
    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'


def test_tmpdir_factory(tmpdir_factory):
    # you should start with making a directory
    # a_dir acts like the object returned from the tmpdir fixture
    a_dir = tmpdir_factory.mktemp('mydir')

    # base_temp will be the parent dir of 'mydir'
    # you don't have to use getbasetemp()
    # using it here just to show that it's available
    base_temp = tmpdir_factory.getbasetemp()
    print('base:', base_temp)

    # the rest of this test looks the same as the 'test_tmpdir()'
    # example except I'm using a_dir instead of tmpdir

    a_file = a_dir.join('something.txt')
    a_sub_dir = a_dir.mkdir('anything')
    another_file = a_sub_dir.join('something_else.txt')

    a_file.write('contents may settle during shipping')
    another_file.write('something different')

    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'
```



##### pytestconfig



内置的pytestconfig可以通过命令行参数、选项、配置文件、插件、运行目录等方式来控制pytest。

pytestconfig是request.config的快捷方式，它在pytest文档里有时候被称为“pytest配置对象”。

要理解pytestconfig如何工作，可以添加一个自定义的命令行选项，然后在测试中读取该选项。



```text
def pytest_addoption(parser):
    """  Add a command line option  """
    parser.addoption(
        "--env", default="test", choices=["dev", "test", "pre"], help="enviroment parameter")
```



以 pytest_addoption 添加的命令行选项必须通过插件来实现，或者在项目顶层目录的conftest.py文件中完成。它所在的conftest.py不能处于测试子目录下。



上述是一个传入测试环境的命令行选项，接下来可以在测试用例中使用这些选项。



```text
def test_option(pytestconfig):
    print('the current environment is:', pytestconfig.getoption('env'))

pytest -sq test_config.py::test_option
```



由于前面的 pytest_addoption 中定义的env的默认参数是test，所以通过 pytestconfig.getoption 获取到的env的值就是test。



