---
layout:     post
title:      "Advanced python functions"
subtitle:   "Advanced python functions"
date:       2017-05-03
author:     "Gavin Wang"
catalog:    true
top: false
hide: false 
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: map(), filter(), reduce()
categories:
    - [python]
tags:
    - python
---

# Overview

`map()，filter()`和`reduce()`是`Python`的三个高阶函数，介绍之。

# map()

`map()`函数是`Python`内置的一个高阶函数，它的作用是将一个函数应用于一个（或多个）可迭代对象（如列表、元组等）的所有元素上，并返回一个map对象。该对象是一个迭代器，可以通过转换为列表或元组来获取所有的结果，或者可以直接在循环中迭代获取每个元素的处理结果。

## 基本用法

```python
map(function_to_apply, iterable)
```

其中，`function_to_apply` 是一个函数，它接受一个参数并返回一个值；`iterable` 是一个可迭代对象，其所有元素都将被`function_to_apply`函数处理。

例如，如果你有一个数字列表并且想要得到这个列表中每个数字的平方，你可以使用 `map()` 函数来实现：

```python
def square(number):
    return number ** 2

numbers = [1, 2, 3, 4, 5]
squared = map(square, numbers)

# 将结果转换为列表
squared_list = list(squared)
print(squared_list)  # 输出: [1, 4, 9, 16, 25]
```

在这个例子中，`map()` 函数将 `square` 函数应用于 `numbers` 列表中的每一个元素。返回的`map`对象`map(square, numbers)`包含了每个数字平方的结果，通过`list()`函数转换为列表。

`map()` 是实现函数式编程风格的有用工具，使代码更加简洁和易读。


## `map()` 函数中的迭代器是如何工作的？


`map()` 函数返回的迭代器遵循 `Python` 的迭代器协议，这意味着结果是按需产生的，而不是一次性计算出所有结果。这种按需产生结果的特性被称为惰性求值（Lazy Evaluation）。下面是详细解释 `map()` 函数中迭代器的工作流程：

### 创建 map() 对象

当你调用 `map()` 函数时，`Python` 会创建一个 `map` 对象。这个对象记录了两件事情：

* 你想要执行的函数。
* 你想要函数作用的可迭代对象。

此时，任何实际的函数调用都还没有发生。

### 迭代 map() 对象

正如所有迭代器一样，`map()` 对象也实现了` __iter__()` 和 `__next__()` 两个方法，这是 `Python` 用来支持迭代的核心方法。

`__iter__()` 方法 返回迭代器自身。
`__next__()` 方法 被用来获取迭代器的下一个元素。

当你开始迭代 `map()` 对象时（例如，通过一个 `for` 循环，或者将其传递给 `list()`，或调用 `next()` 函数时），`map()` 对象的 `__next__()` 方法被调用。此时，`map()` 对象会调用你最初提供给它的函数，将函数应用于可迭代对象的下一个元素，并返回该函数的结果。

如果可迭代对象中的所有元素都已经被处理，`__next__()` 方法会引发一个 `StopIteration` 异常，这是 `Python` 用来通知迭代结束的信号。

例子:


```python
def double(x):
    return x * 2

# 创建 map 对象
result = map(double, [1, 2, 3, 4])

# 通过迭代来处理结果
for value in result:
    print(value)
```

在这个例子中，每次循环迭代时，`__next__()` 方法被调用，它会依次调用 `double()` 函数，传递给它列表 `[1, 2, 3, 4]` 中的下一个值，然后返回计算后的结果。

### 惰性求值的好处

这种按需（或惰性）求值的优点在于，它可以显著节省内存，尤其是当处理大量数据时。因为在任何给定时刻，只有一个元素会被处理，而不是先计算整个结果集。

惰性求值的另一个好处是，对于无限的或非常大的数据流，你仍然可以开始处理它们，而不需要等待所有的数据都准备好。

## `map()`函数的参数可以是匿名函数吗？

`map()`函数的参数可以是匿名函数。在`Python`中，匿名函数也称为`lambda`函数。`lambda`函数可以在不需要显式定义函数的情况下创建简单的函数。

利用`lambda`函数作为`map()`的参数可以让代码变得更加简洁。以下是一个使用lambda函数作为`map()`参数的例子：

```python
# 使用 lambda 函数计算列表中每个数值的平方
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)

# 转换为列表以方便查看结果
squared_list = list(squared)
print(squared_list)  # 输出: [1, 4, 9, 16, 25]
```

在这个例子中，`lambda x: x**2` 创建了一个匿名函数，用于计算传入的参数的平方值，并作为`map()`函数的第一个参数。`map()`将这个匿名函数应用于`numbers`列表中的每个元素，并返回一个新的迭代器，其包含了所有数值平方后的结果。


# filter函数

`filter()`函数是`Python`内置的另一个非常有用的高阶函数，它允许对可迭代对象（如列表、元组等）中的元素进行过滤，挑选出符合特定条件的元素组成一个新的迭代器返回。

## 基本用法

filter()函数的基本语法为：

```python
filter(function, iterable)
```

* `function`：一个返回布尔值（`True` 或 `False`）的函数，用于判断可迭代对象中的每个元素是否符合条件。对于每个元素，`function` 的返回结果决定了该元素是否被包含在返回的迭代器中。如果 `function` 是 `None`，那么所有返回“真”的元素将会被返回。
* `iterable`：要从中过滤元素的可迭代对象。

## 返回值

`filter()` 返回一个迭代器，其内容是经过 `function` 函数检验后返回 `True` 的那些元素。

## 示例

### 过滤偶数

以下示例使用 `filter()` 函数从列表中过滤出偶数：

```python
# 定义一个判断偶数的函数
def is_even(num):
    return num % 2 == 0

# 可迭代对象
numbers = [1, 2, 3, 4, 5, 6]

# 使用filter()过滤偶数
even_numbers = filter(is_even, numbers)

# 因为filter()返回的是迭代器，所以要用list()转换成列表
even_list = list(even_numbers)
print(even_list)  # 输出: [2, 4, 6]
```

### 移除空字符串

还可以使用 filter() 函数来移除列表中的空字符串：

```python
# 可迭代对象
strings = ["apple", "", "banana", None, "cherry", ""]

# 使用filter()移除空字符串或None
non_empty_strings = filter(None, strings)

print(list(non_empty_strings))  # 输出: ['apple', 'banana', 'cherry']
```

这里将 `None` 作为 `function` 传入 `filter()`，`Python` 会默认将每个元素转换为布尔值来判断其是否符合条件（即是否为 “真”）。

### 注意事项

* 由于 `filter()` 函数返回的是一个迭代器，你可能需要将其转换为列表或其他类型的序列，以便进一步处理或打印。
* 如果筛选逻辑很简单，你也可以考虑使用列表推导式或生成器表达式，它们通常更简洁，而且易于理解。
* filter() 函数使得基于条件的元素过滤变得简单，并且可以用于任何可迭代的对象，是Python数据处理工具箱中的重要工具之一。


# reduce函数

`reduce()`函数是`Python`中的一个高阶函数，旨在将一个接受两个参数的函数累积地应用到一个序列的所有项上，从而将序列减少为单一的值。`reduce()`函数属于`functools`模块，因此使用前需要先导入该模块。

## 基本用法

reduce()函数的基本语法如下：

```python
from functools import reduce

reduce(function, iterable[, initializer])
```

* `function`: 这是一个接收两个参数并返回一个值的函数。对于序列中的每个元素，`reduce()`都会将上一次`function`函数调用的返回值和序列的下一个元素作为参数传给`function`函数。
* `iterable`: 要应用`function`的可迭代对象。
* `initializer`: (可选) 一个初始值，如果提供了此值，它会作为计算的初始累积值，而序列的第一个元素将作为第一次调用`function`的第二个参数。(如果序列为空，则返回`initializer`；如果未提供`initializer`且序列为空，则抛出`TypeError`)。

## 示例

使用 `reduce()`计算列表所有元素的乘积

下面的示例展示了如何使用reduce()函数计算一个列表所有元素的乘积：

```python
from functools import reduce

# 定义一个乘法函数
def multiply(x, y):
    return x * y

numbers = [1, 2, 3, 4, 5]

# 使用reduce()计算乘积
product = reduce(multiply, numbers)
print(product)  # 输出: 120
```

在这个例子中，`reduce()`函数依次将`multiply()`函数应用于列表`numbers`的每个元素和累积的乘积上，从而计算出所有元素的乘积。

## 使用 reduce() 与 lambda 函数

`reduce()` 通常与匿名函数lambda一起使用，使代码更加简洁：

```python
from functools import reduce

# 使用lambda函数计算乘积
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)

print(product)  # 输出: 120
```

## 注意事项

* `reduce()`是功能强大的函数。但是，它不是解决所有问题的最佳选择。在某些情况下，使用循环或其他`Python`内置函数（如sum()）可能会更直观、更易读。
* 尽管`reduce()`可能看起来很“魔法”，但过度使用它可能会使代码难以理解和维护，特别是对于不熟悉函数式编程概念的人来说。
* `reduce()`函数的加入为`Python`编程提供了强大的数据处理能力，特别是在进行累积操作时。


## 如何在reduce()函数中使用initializer参数？

`reduce()`函数在`functools`模块中，它的全用法为：

```python
reduce(function, iterable[, initializer])
```

其中，`initializer`参数是一个可选的值，会作为函数处理的初始值。如果提供了`initializer`参数，它会在迭代过程的开始被放在序列的前面。如果序列为空，则`initializer`就是最终的结果。

下面是如何在reduce()函数中使用initializer参数的例子：

```python
from functools import reduce

# 函数: 对两个数求和
def add(x, y):
    return x + y

# 可迭代对象: 数字列表
numbers = [1, 2, 3, 4, 5]

# 包含初始值的reduce操作
sum_with_initial = reduce(add, numbers, 10)  # 使用10作为初始值

print(sum_with_initial)  # 输出: 25
```

在这个例子中，`reduce()`函数将add函数应用于列表`numbers`中的元素，而10被作为累加的起始值。初始值在这种情况下很有用，例如，当你需要确保`reduce()`的结果永远不会是0或是空值，或者当你想要给总和、乘积等添加一个起始量。如果`numbers`列表为空，`reduce()`函数将返回初始值10。

在实际应用中，initializer参数常见于需要在结果中包含某些边界条件或默认值的场景。


## reduce()函数能应用于哪些类型的可迭代对象？

在`Python`中，`reduce()`函数能应用于任何可迭代对象（`iterable`），这包括但不限于以下类型：

列表（List）：最常见的可迭代类型之一，由一系列有序元素组成。

```python
   from functools import reduce
   numbers = [1, 2, 3, 4, 5]
   product = reduce(lambda x, y: x * y, numbers)
```

元组（Tuple）：和列表类似，但一旦创建便不可改变，术语称为“不可变（immutable）”。

```python
   numbers_tuple = (1, 2, 3, 4, 5)
   sum_result = reduce(lambda x, y: x + y, numbers_tuple)
```

字符串（String）：字符串也是可迭代的，可以在reduce()中使用字符串序列。

```python
   chars = "12345"
   concatenated = reduce(lambda x, y: x + y, chars)
```

字典（Dictionary）：虽然字典是无序的，但可以迭代其键（keys）、值（values）或键-值对（items）。

```python
   ages = {'Alice': 21, 'Bob': 25, 'Charlie': 22}
   total_age = reduce(lambda x, y: x + y, ages.values())
```

集合（Set）：集合是无序的集合类型，不包含重复元素。

```python
   numbers_set = {1, 2, 3, 4, 5}
   sum_set = reduce(lambda x, y: x + y, numbers_set)
```

生成器（Generator）：生成器是一种特殊的迭代器，可以动态地生成值。

```python
   gen = (x for x in range(1, 6))  # 生成器表达式
   sum_gen = reduce(lambda x, y: x + y, gen)
```

因为reduce()只需要从可迭代对象连续取出元素来应用函数，所以只要对象能支持迭代，reduce()就能应用上。


# Overall

## 异同点

- 相似之处：
  - 所有这三个函数都属于函数式编程的范畴。
  - 它们都需要至少两个参数：一个函数和一个可迭代对象。
  - 在应用于大型数据集时，都可以提高代码的效率和可读性。

- 不同点：
  - `map()` 和 `filter()` 返回的是迭代器，而 `reduce()` 返回的是单一的结果值。
  - `map()` 对可迭代对象中的每个元素应用相同的函数，`filter()` 通过给定的函数过滤元素，`reduce()` 则使用给定的函数累积元素。
  - `reduce()` 需要从 `functools` 模块导入，而 `map()` 和 `filter()` 是 Python 的内置函数。
  - `filter()` 与 `map()` 不同，因为它基于给定函数的返回值是True还是False来决定是否保留每个元素，而`map()`则对每个元素应用给定的函数并返回结果。

## 总结



| 函数名     | 描述                                                                                               |  语法    | 使用示例                                                                  | 返回值类型            |
|----------|----------------------------------------------------------------------------------------------------|----------------------------------------------------|-------------------------------------------------------------------------|----------------------|
| map()    | 对可迭代对象的每个元素应用给定的函数，并以迭代器形式返回结果。                                                 | `map(function, iterable)`          | `map(lambda x: x**2, [1, 2, 3, 4, 5])`                                   | map对象（迭代器）       |
| filter() | 从可迭代对象中过滤出那些使给定函数返回True的元素，并以迭代器形式返回这些元素。                                       | `filter(function or None, iterable)`                   | `filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])`                          | filter对象（迭代器）    |
| reduce() | 使用给定的函数将一个可迭代对象的元素累积地应用，从第一个元素开始，后续每次应用到前一次的结果上，最终将序列减少为单一的值。 |`reduce(function, iterable[, initializer])`  | `from functools import reduce` <br> `reduce(lambda x, y: x + y, [1,2,3,4,5])` | 单一值                |
