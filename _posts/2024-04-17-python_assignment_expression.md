---
layout:     post
title:      "python assignment expression, :="
subtitle:   "python assignment expression, :="
date:       2024-04-17
author:     "Gavin Wang"
catalog:    true
img: "/medias/featureimages/173.jpg"
summary: python assignment expression, :=
categories:
    - [python]
tags:
    - python
---

# 概述

最近在看《流畅的python》第二版，上册，第二章节有提及到`:=`，书中举例了一个list中某个值的访问，搜索一下相关资料，学习一下。果真此运算符比书中所提及的功能要丰富的多，故mark一下。

# 前言

经资料查询，从Python 3.8开始，引入了一项新的语法特性："海象运算符"，它的正式名称是 Assignment Expressions（赋值表达式），标记为 `:=`。这个运算符允许你在表达式内进行变量赋值，从而可以在一个表达式中完成测试和赋值两个动作。由于它的外形像海象的眼睛和长牙，因此社区给它起了个昵称"海象运算符"。

海象运算符的一个典型用途是在条件语句中，它允许在测试某个条件的同时将其值赋给一个变量。不仅如此，它还可用于循环和其他许多场合，从而使代码更加简洁且易于理解。


# 场景一：列表推导式中元素访问

```python
[last := x for x in range(10)]
```

我们使用 `:=` 运算符将每个 x 的值赋给 last 变量。注意，这里的 last 实际上并没有在列表推导式中作为变量名 x 的别名使用，而是在整个推导式完成后，将最后一个元素的值赋给 last 变量。这个技巧允许我们在列表推导式完成后，通过 last 变量获取到这个新列表的最后一个元素。

生成的列表包含了从 0 到 9 的整数，如下所示：

```python
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

当你查询 last 变量时，它会返回列表中的最后一个元素，也就是 9。

再比如：

```python
>>> import re
>>> data = "Some example numbers: 10, 20, and 30"
>>> (match := re.findall(r'\d+', data))
['10', '20', '30']
>>> match
['10', '20', '30']
>>> 
```


# 场景二：在 while 循环中读取用户输入直到空行出现。

```python

# 传统的写法
user_input = input("Enter message: ")
while user_input:
    print(f'Echo: {user_input}')
    user_input = input("Enter message: ")


# 使用海象运算符
while (user_input := input("Enter message: ")):
    print(f'Echo: {user_input}')
```

在这个例子中，使用海象运算符让代码更简洁，减少了重复的 input 调用。

# 场景三：在 if 语句中使用，同时测试和赋值。

```python
data = "Some example numbers: 10, 20, and 30"

# 传统做法
match = re.search('(\d+)', data)
if match:
    print(f"Found a number: {match.group(1)}")

# 使用海象运算符
if match := re.search('(\d+)', data):
    print(f"Found a number: {match.group(1)}")
```

在上述例子中，使用海象运算符可以在判断条件真假时同时捕获正则表达式捕获组（在这里是数字）。

# 场景四：需要多次使用某个昂贵的计算结果时。

```python

# 传统做法
result = some_expensive_calculation_function()
if result:
    other_function(result)

# 使用海象运算符
if (result := some_expensive_calculation_function()):
    other_function(result)
```

在这个例子中，海象运算符让我们无需调用两次`some_expensive_calculation_function()`就能够重用其计算结果。


海象运算符提高了代码的可读性和编写效率，在合适的场景下使用可使得代码更加精简和优雅。然而，像所有新引入的语法特性一样，使用时应该注意代码的清晰性和易维护性，过度使用或者在不适当的情况下使用可能会增加代码的复杂性。



注意事项：

* 海象运算符只能用于 Python 3.8 及以上版本。
* 使用海象运算符时，应确保右侧的表达式是安全的，即不会引起异常。如果表达式可能抛出异常，那么使用海象运算符可能会导致代码的错误处理变得复杂。
* 海象运算符主要用于简化代码，但它并不总是必要的。在某些情况下，使用传统的多行赋值和条件语句可能更清晰。

总之，合理&慎重的使用它!

PS: 
写此文纯粹是好奇，但更推荐传统写法。
