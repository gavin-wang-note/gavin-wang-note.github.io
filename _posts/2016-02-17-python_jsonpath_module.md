---
title: python jsonpath解析json数据
date: 2016-02-17 12:29:59
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: 使用 JSONPath 进行 JSON 数据查询和解析(多层级读取key的value)
categories:
    - [python]
tags:
    - python
---


`JSONPath`是一门用于查询和操作`JSON`数据的先进语言。它为`JSON`提供了类似`XPath`对`XML`的查询功能，使我们能以简洁和方便的方式来查询和操作复杂的`JSON`结构。

# 什么是 JSONPath？

首先，要理解`JSONPath`，我们需要从它的名字开始。

`JSONPath`名字的由来是基于正是类似`XPath`的查询语言，不过`JSONPath`是用来查询`JSON`数据的。

`JSONPath`通过清晰、易读的查询表达式，为遍历复杂的`JSON`数据提供了简单方便的方式。通过使用`JSONPath`，你可以轻松查询和提取`JSON`数据中你感兴趣的部分。

# 使用场景

* 当你处理大型的`JSON`数据结构，并且需要定位到某个特定的值。
* 当你需要从`JSON`响应中提取数据以便进一步处理或断言，例如在自动化测试中的`API`测试。
* 当你在开发中使用`JSON`作为配置文件，并且想要读取特定的配置。
* 当你在数据分析中使用`JSON`格式的数据源，并且需要提取特定字段的信息。

# 使用说明

`JSONPath`的语法采用了点符号（.）或者方括号（[]）作为分隔符来访问`JSON`对象中的特定属性。类似`JavaScript`访问对象属性的符号。其中，点符号用来指向当前元素的简单字段，而方括号可用来处理包含特殊字符的字段名或访问数组索引。

表达式一般由一个美元符号（$）开始，它表示`JSONPath`表达式的根对象，然后跟着一个或多个子元素。

`JSONPath`的语法总结如下：

* 根节点：用 $ 表示。
* 字段选择：用字段名表示，如 store.book。
* 数组索引：用数字表示，如 store.book[1]。
* 通配符：用 * 表示，匹配任何字段或任何元素。
* 切片：用 [start:end:step] 表示，如 store.book[0:2]。
* 函数调用：用 @ 表示，如 @.length。

更详细信息，参考下图：

<img class="shadow" src="/img/in-post/jsonpath语法规则.png" width="800">


# 示例代码1

获取所有书的作者

```python
import jsonpath

# 提供的 JSON 数据
data = {
  "store": {
    "book": [
      {
        "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      {
        "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}

# JSONPath 表达式
authors = jsonpath.jsonpath(data, '$.store.book[*].author')

# 输出所有作者
print(authors)

# 获取所有物品的价格

# JSONPath 表达式
prices = jsonpath.jsonpath(data, '$.store..price')

# 输出所有价格
print(prices)
```

上述代码运行效果参考如下：

```shell
root@Gavin:~/test# python3 jsonpath_test.py 
['Nigel Rees', 'Evelyn Waugh']
[8.95, 12.99, 19.95]
root@Gavin:~/test#
```

**注释**:

* 符号 * 代表通配符，可以匹配所有元素。
* .. 是一个深度搜索运算符，允许你取得路径中任意位置的元素。
* jsonpath.jsonpath() 函数返回的是一个列表，包含所有匹配到的元素。



# 代码示例2

```python
book_dict = {
        "book": [
                {"category": "reference",
                 "author": "Nigel Rees",
                 "title": "Sayings of the Century",
                 "price": 8.95
                 },
                {"category": "fiction",
                 "author": "Evelyn Waugh",
                 "title": "Sword of Honour",
                 "price": 12.99
                 },
                {"category": "fiction",
                 "author": "Herman Melville",
                 "title": "Moby Dick",
                 "isbn": "0-553-21311-3",
                 "price": 8.99
                 },
                {"category": "fiction",
                 "author": "J. R. R. Tolkien",
                 "title": "The Lord of the Rings",
                 "isbn": "0-395-19395-8",
                 "price": 22.99
                 }
        ],
        "bicycle": {
                "color": "red",
                "price": 19.95
        }
}

from jsonpath import jsonpath

# 获取price的所有值
print(jsonpath(book_dict, '$..price'))

# 获取book下面所有元素
print(jsonpath(book_dict, "$.book.*"))

# 获取book下面所有price的值
print(jsonpath(book_dict, "$.book[*].price"))
print(jsonpath(book_dict, "$.book..price"))

# 获取第1本书所有信息
print(jsonpath(book_dict, "$.book[0]"))

# 获取第2~3本书所有信息
print(jsonpath(book_dict, "$.book[1:3]"))

# 获取最后一本书
print(jsonpath(book_dict, "$.book[(@.length-1)]"))

# 获取包含了isbn的所有书
print(jsonpath(book_dict, "$.book[?(@.isbn)]"))

# 获取书的价格小于10的书
print(jsonpath(book_dict, "$.book[?(@.price<10)]"))
'''

上述代码运行效果：

```shell
root@Gavin:~/test# python3 e2.py
[8.95, 12.99, 8.99, 22.99, 19.95]
[{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}, {'category': 'fiction', 'author': 'Evelyn Waugh', 'title': 'Sword of Honour', 'price': 12.99}, {'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}, {'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
[8.95, 12.99, 8.99, 22.99]
[8.95, 12.99, 8.99, 22.99]
[{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}]
[{'category': 'fiction', 'author': 'Evelyn Waugh', 'title': 'Sword of Honour', 'price': 12.99}, {'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}]
[{'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
[{'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}, {'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
[{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}, {'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}]
root@Gavin:~/test# 
```

# 总结

`JSONPath`是处理`JSON`数据时非常有力的工具，特别是在你需要查询和提取数据的场合。它可以帮助你快速定位到你感兴趣的数据，无论这些数据是嵌套的还是在大型的`JSON`结构中。通过学习和使用`JSONPath`，你会在处理`JSON`数据时变得更有效率和精确。

`JSONPath`对于数据的遍历、抓取具有非常好的灵活性，挖掘出其中的价值变得简单和直接。在实际使用中，请一定要根据你的具体数据结构来调整查询表达式。
