---
layout:     post
title:      "Python中的append()和extend()方法介绍"
subtitle:   "Python中的append()和extend()方法介绍"
date:       2019-03-10 20:00:00
author:     "Gavin Wang"
catalog:    true
img: ""
summary: Python中的append()和extend()方法介绍
categories:
    - [python]
tags:
    - python
---

# 概述

在`Python`中，`append()`和`extend()`是两个用于向列表添加元素的方法，但它们之间存在一些关键的区别。本文将详细解释这两个方法的不同之处，并提供示例以帮助理解它们的用法。

# append()方法

`append()`方法用于将一个对象添加到列表的末尾。这个对象可以是任何数据类型，包括数字、字符串、元组、列表等。当使用`append()`时，该对象作为一个单独的元素被添加到列表中。

## 示例

```python
# 创建一个初始列表
my_list = [1, 2, 3]

# 使用append()方法添加一个元素
my_list.append(4)

# 打印更新后的列表
print(my_list)  # 输出: [1, 2, 3, 4]

# 添加一个列表作为元素
my_list.append([5, 6])

# 打印更新后的列表
print(my_list)  # 输出: [1, 2, 3, 4, [5, 6]]
```


在上面的例子中，我们首先向列表`my_list`中添加了一个整数4。然后，我们添加了一个列表[5, 6]作为一个新的元素。

## extend()方法

与`append()`不同，`extend()`方法用于将一个可迭代对象（如列表、元组、字符串等）的所有元素添加到现有列表的末尾。`extend()`会展开这个可迭代对象，将其元素逐个添加到列表中。

## 示例

```python
# 创建一个初始列表
my_list = [1, 2, 3]

# 使用extend()方法添加一个列表
my_list.extend([4, 5])

# 打印更新后的列表
print(my_list)  # 输出: [1, 2, 3, 4, 5]

# 添加一个字符串
my_list.extend('ab')

# 打印更新后的列表
print(my_list)  # 输出: [1, 2, 3, 4, 5, 'a', 'b']
```

在这个例子中，我们使用`extend()`将列表[4, 5]中的元素逐个添加到`my_list`中。接着，我们添加了一个字符串'ab'，它的每个字符也被逐个添加到了列表中。

# 主要区别

* 元素添加方式：`append()`将整个对象作为一个单独的元素添加到列表末尾，而`extend()`将可迭代对象的元素逐个添加到列表末尾。
* 参数类型：`append()`接受任何类型的单个对象，而`extend()`接受一个可迭代对象。
* 用途：当你需要将一个对象作为一个整体添加到列表时，使用`append()`。当你需要将一个可迭代对象的所有元素添加到列表中时，使用`extend()`。

# 小结

`append()`和`extend()`都是向列表添加元素的强大工具，但它们适用于不同的场景。了解它们的区别可以帮助你更有效地使用`Python`的列表操作。记住，选择使用`append()`还是`extend()`取决于你想要如何添加元素到你的列表中。
