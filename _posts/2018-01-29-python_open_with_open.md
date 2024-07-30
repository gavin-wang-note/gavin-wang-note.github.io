---
layout:     post
title:      "Python文件操作：'with open()'与'open()'的区别"
subtitle:   "Difference of 'with open()' and 'open()'"
date:       2018-01-29
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
tags:
    - python
---


# 概述



在Python中，文件操作是非常常见的任务，Python提供了`open()`函数和`with`语句。`with open()`与`open()`在文件操作中有什么区别呢？



# `open()`函数



`open()`函数是Python内置的用于打开文件的函数。它接受两个参数：文件名和模式。模式可以是`'r'`（只读，默认值），`'w'`（写入，如果文件存在则清空内容），`'a'`（追加，如果文件存在则在末尾追加内容）或`'x'`（创建，如果文件存在则返回错误）。

详细模式信息如下：



| 模式 | 可做操作                    | 若文件不存在       | 是否覆盖       |
| ---- | --------------------------- | ------------------ | -------------- |
| r    | 只读                        | error              | -              |
| r+   | 读写                        | error              | 是             |
| w    | 只写                        | create             | 是             |
| w+   | 读写                        | create             | 是             |
| a    | 只写                        | create，尾部追加写 |                |
| a+   | 读写                        | create             | 否，尾部追加写 |
| wb   | 只写二进制字符串，写入bytes | create             | 是             |
| rb   | 只读二进制字符串，返回bytes | error              | -              |



使用`open()`函数打开文件后，你可以使用文件对象的`read()`、`write()`、`close()`等方法进行文件操作。

示例：

```python
file = open('example.txt', 'r')
content = file.read()
file.close()
```



# `with open()`语句



`with open`语句是Python中一种简洁的文件操作方式。它使用`with`关键字和`open()`函数，可以简化文件操作的代码。`with open`语句会在执行完文件操作后自动关闭文件，避免了手动关闭文件的操作。

使用`with open`语句时，不需要指定文件名和模式，只需将文件名和模式作为`open()`函数的参数即可。

示例：

```python
with open('example.txt', 'r') as file:
    content = file.read()
```



上述示例代码，与如下代码效果同样：



```python
try:
    file = open('example.txt', 'r')
    file.read()
finally:
    if file:
        file.close()
```



一对比，`with open`更简洁。





# `with open()`与`open()`的区别



`with open`语句与`open()`函数在文件操作上有很多相似之处，但它们之间有几个重要的区别：

1. 自动关闭：`with open`语句会在退出`with`块时自动关闭文件，而`open()`函数需要手动调用`close()`方法关闭文件。
2. 上下文管理：`with open`语句使用了上下文管理器，可以更好地处理异常和资源管理。在`with`块中发生的异常会被传递到`with`语句之外，而`open()`函数的异常则需要在文件操作中处理。
3. 代码可读性：`with open`语句使代码更简洁，可读性更强。它避免了手动关闭文件和处理异常的繁琐操作。



摘抄自网络上的解释：



```shell
Unlike `open()` where you have to close the file with the `close()` method, the `with` statement closes the file for you without you telling it to.

This is because the `with` statement calls 2 built-in methods behind the scene – `__enter()__` and `__exit()__`.

The `__exit()__` method closes the file when the operation you specify is done.
```



# 关于上下文



在Python中，`__exit__()`和`__entry__()`是面向对象的编程语言特性，称为“特殊方法”。它们主要用于定义对象在进入和退出上下文管理器（如`with`语句）时的行为。

`__exit__()`方法在对象离开上下文管理器时被调用，而`__entry__()`方法在对象进入上下文管理器时被调用。这两个方法可以用于执行资源清理、状态管理或其他需要在进入和退出上下文管理器时执行的操作。

以下是一个简单的例子，说明如何在Python中使用`__exit__()`和`__entry__()`方法：


```python
class MyContext:
    def __init__(self):
        self.count = 0

    def __entry__(self):
        print("Entering context")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        self.count += 1
        return False  # 返回False表示异常应该被继续传播

# 使用with语句
with MyContext() as ctx:
    print("Inside with block")
    raise ValueError("An error occurred")

print("After with block")
```

输出：

```shell
Entering context
Inside with block
Exiting context
1
After with block
```

在这个例子中，定义了一个名为`MyContext`的类，该类具有`__entry__()`和`__exit__()`方法。当我们使用`with`语句创建一个`MyContext`对象的上下文管理器时，`__entry__()`方法会在进入上下文管理器时被调用，而`__exit__()`方法会在离开上下文管理器时被调用。

