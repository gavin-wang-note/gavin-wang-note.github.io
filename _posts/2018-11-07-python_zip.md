---
layout:     post
title:      "python zip 函数介绍"
subtitle:   "python zip"
date:       2018-11-07
author:     "Gavin Wang"
catalog:    true
img: ""
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: python zip 函数详解 
categories:
    - [python]
tags:
    - python
---


# 概述

Python 提供了一个名为 zip() 的内置函数，它是处理并行迭代的利器。在数据处理、机器学习预处理，甚至是日常编程任务中，zip() 函数常被用来将多个可迭代对象（如列表、元组、字典等）中对应的元素打包成一个个元组，然后返回由这些元组组成的迭代器。

# 基本用法

zip() 函数接受两个或更多的可迭代对象作为参数，并返回一个Zip迭代器。


```python
zip(*iterables)
```

*iterables：一个或多个可迭代对象。

假设有两个列表，需要对它们进行并行迭代，你可以这样使用 zip()：

```python
names = ['Alice', 'Bob', 'Charlie']
scores = [85, 90, 88]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

这段代码会输出：

```plaintext
Alice: 85
Bob: 90
Charlie: 88
```

再比如：

```python   
list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]

zipped_lists = zip(list1, list2)

for item in zipped_lists:
    print(item)
```

输出将会是：


```plaintext
('a', 1)
('b', 2)
('c', 3)
```

# 使用场景

* 对数据进行成对的处理：当你有两个列表并希望以成对的方式执行操作时。
* 修复不一致的数据：有时你可能会得到长度不一致的数据集，可以使用zip()函数和fillvalue参数来使它们具有相同的长度。
* 多个字典的合并：如果你有几个特定频率分布的字典，可以通过zip合并它们。


# zip() 深入

* 处理不等长的可迭代对象：当 zip() 用于长度不一的可迭代对象时，它会停在最短的可迭代对象完成迭代的位置。如果你需要处理到最长的可迭代对象结束，可以使用 itertools.zip_longest()。
* 解压数据：zip() 能够与 `*` 操作符结合来用于解压数据，即将打包的元组序列解压为多个可迭代对象。

```python
packed_data = [('Alice', 85), ('Bob', 90), ('Charlie', 88)]
names, scores = zip(*packed_data)

print(list(names))   # 输出: ['Alice', 'Bob', 'Charlie']
print(list(scores))  # 输出: [85, 90, 88]
```

# 进阶用例

* 字典的并行迭代：zip() 可以用来同时遍历字典的键和值。

```python
students = {'Alice': 85, 'Bob': 90, 'Charlie': 88}

for name, score in zip(students.keys(), students.values()):
    print(f"{name}: {score}")
```

* 数据转置：如果有一个包含多个列表的列表，并且你想将它转置，即行列互换，可以使用 zip() 实现。

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed_matrix = zip(*matrix)

print(list(transposed_matrix))
# 输出: [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
```

# zip的其他使用

## 将Zipped数据转换为列表

如果你需要将zip()的结果在记忆化的形式（如列表）中使用，可以用list()来显式地转化。


```python
zipped_lists = list(zip(list1, list2))
print(zipped_lists)
```

将输出：

```plaintext   
[('a', 1), ('b', 2), ('c', 3)]
```

## 不相等长度的列表

如果给zip()提供的可迭代对象长度不一，它将在所有输入迭代器中元素都耗尽时停止运行，不会产生错误。

```python    
list1 = ['a', 'b', 'c', 'd']
list2 = [1, 2]

zipped_lists = zip(list1, list2)
print(list(zipped_lists))
```

输出将会是：

```plaintext    
[('a', 1), ('b', 2)]
```

要注意的是，这个例子里'c'和'd'被忽略，因为列表2中没有足够的元素。

## 填充参数

为了处理可迭代对象长度不一致的情况，zip()提供了一个fillvalue参数。如果输入迭代器中的某个迭代器已无元素可用，则所生成的元组会使用这个fillvalue指定的值填充。

``` python    
list1 = ['a', 'b', 'c', 'd']
list2 = [1, 2]

zipped_lists = zip(list1, list2, fillvalue=None)
print(list(zipped_lists))
```

这将输出：

```plaintext    
[('a', 1), ('b', 2), ('c', None), ('d', None)]
```

## 解压zipped对象

你可以采用与zip相反的操作：*操作符将zipped对象解压回原来的可迭代对象（需要输入项为iterable）。


```python    
zipped_lists = [('a', 1), ('b', 2), ('c', 3)]

list1, list2 = zip(*zipped_lists)

print(list(list1))  # ['a', 'b', 'c']
print(list(list2))  # [1, 2, 3]
```


# 注意事项

* 由于 `zip()` 返回的是迭代器，对其直接打印或多次使用将不会得到预期结果。迭代器一次迭代完后就会耗尽，因而需要转换为列表或元组以便多次访问或打印。
* 在处理大数据时，请慎重使用转换为列表或元组的操作，因为这将消耗更多内存。

# 总结

zip() 函数是Python编程中一个简洁而强大的工具，可以优雅地解决许多和并行迭代相关的常见问题。它不仅使代码更加Pythonic，还具有很高的灵活性，是处理多个序列数据时不可或缺的一部分。不过，掌握其特性和使用场景是发挥其最大功效的关键。
