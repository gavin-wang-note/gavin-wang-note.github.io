---
title: python正则
date: 2015-10-03 15:37:29
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: python regex
categories:
    - [python]
tags:
    - python
---


# Overview

`Python`的正则表达式是使用`re`模块来实现的，这个模块提供了一系列功能，用于字符串搜索和操作，给出了一种灵活的方式来匹配指定模式的文本。


# Summary

下面是一个以Markdown格式编写的关于`Python`正则表达式的功能和用法的总结表格：


| 功能                       | 说明                                                                         | 示例代码                            |
|---------------------------|------------------------------------------------------------------------------|--------------------------------------|
| 导入模块                     | 导入`re`模块以使用正则表达式                                                      | `import re`                         |
| 基本匹配                     | 匹配字符串中是否存在给定的模式                                                   | `re.search(r'pattern', 'string')`   |
| 匹配开头                     | 匹配字符串的开头是否存在给定模式                                                 | `re.match(r'pattern', 'string')`    |
| 查找所有匹配项                 | 查找并返回字符串中所有匹配模式的项                                               | `re.findall(r'pattern', 'string')`  |
| 替换                        | 替换字符串中的匹配模式                                                         | `re.sub(r'pattern', 'repl', 'string')` |
| 编译正则表达式                  | 编译正则表达式以复用                                                            | `regex = re.compile(r'pattern')`    |
| 分组提取                     | 用括号对模式分组，并提取内容                                                     | `re.search(r'(group)', 'string')`   |
| 命名分组                     | 使用命名来分组并提取内容                                                         | `re.search(r'(?P<name>group)', 'string')` |
| 非贪婪匹配                    | 最少匹配，尽可能少的匹配字符                                                   | `re.findall(r'pattern??', 'string')` |
| 正向/反向查找（lookahead/lookbehind）| 断言前面或后面的字符但不包括在匹配中                                           | `re.search(r'pattern(?=after)', 'string')` |
| 可选匹配项                     | 匹配零个或一个给定模式                                                         | `re.search(r'pattern?', 'string')`   |
| 重复匹配项                     | 匹配零个或多个次数                                                             | `re.search(r'pattern*', 'string')`   |
| 匹配特定次数                   | 匹配一个模式在给定次数的情况                                                     | `re.search(r'pattern{3}', 'string')` |
| 字符类                        | 匹配任何指定的字符集合                                                         | `re.search(r'[aeiou]', 'string')`    |
| 排除特定字符                   | 不匹配指定的字符集合                                                           | `re.search(r'[^aeiou]', 'string')`   |
| 点号匹配任意单个字符             | 除换行以外的任何字符。可与`re.DOTALL`配合使用来包括换行                           | `re.search(r'.', 'string')`          |
| 斜杠特殊字符（如`\d`, `\w`, `\s`等） | 分别匹配数字、单词字符、空白字符等特殊字符集                                    | `re.search(r'\d', 'string')`         |


# 入门基础

## 1. 导入模块

在使用正则表达式之前，需要先导入`Python`中的`re`模块：

```python
import re
```

## 2. 常用函数

* re.search()：扫描整个字符串，返回第一个成功匹配的匹配对象。
* re.match()：从字符串的开始匹配，如果不在开头匹配成功则返回None。
* re.findall()：找到正则表达式匹配的所有子串，并以列表形式返回。
* re.sub()：用于替换字符串中的匹配项。

## 3. 简单匹配

使用`search`函数查找字符串中是否存在匹配的模式：

```python
# 查找字符串中的单词 "way"
text = "The best way to understand regex"
match = re.search(r'way', text)
if match:
    print("Found:", match.group())
```

# 进阶应用

## 1. 使用模式标识符

在编译一个正则表达式时，你可以指定一组影响匹配行为的选项，称为模式标识符：

* re.I或re.IGNORECASE：忽略大小写。
* re.M或re.MULTILINE：多行模式。
* re.S或re.DOTALL：使.匹配任何字符，包括换行符。

```python
# 忽略大小写进行匹配
case_insensitive_match = re.search(r'way', text, re.I)
```

## 2. 使用分组

通过括号来创建一个分组，你可以后续从匹配项中提取特定数据：

```python
# 匹配并提取域名
url = "Visit our website: https://www.example.com"
match = re.search(r'https://(www\..+\.com)', url)
if match:
    # 分组1匹配的文本
    domain = match.group(1)
    print("Domain name:", domain)
```

# 高级应用

## 1. lookahead和lookbehind断言

使用正向查找（lookahead）和反向查找（lookbehind）来断言字符串中前后的特定模式：

```python
# 使用正向查找找到`foo`后面跟着`bar`的匹配项
re.findall(r'foo(?=bar)', 'foobar')

# 使用反向查找找到前面有`bar`的`foo`匹配项
re.findall(r'(?<=bar)foo', 'barfoo')
```

## 2. 使用匿名和命名组

除了使用编号来指定分组，你也可以为它们命名：

```python
# 使用命名分组匹配整数和小数
pattern = r'(?P<integer>\d+)(\.(?P<decimal>\d+))?'
match = re.search(pattern, "The number is 42.314")

# 通过名字提取匹配的分组
if match:
    integer_part = match.group('integer')
    decimal_part = match.group('decimal')
```

## 3. 编译正则表达式

为了提升效率，可将经常使用的正则表达式编译。

```python
pattern = re.compile(r'way', re.I)
match = pattern.search(text)
```

## 4. re.findall()和re.finditer()

`findall`找到所有匹配项并作为列表返回，`finditer` 返回一个迭代器，每次迭代返回一个匹配对象：

```python
# 使用finditer逐个访问所有匹配项
iterator = re.finditer(r'\bway\b', text)
for match in iterator:
    print('Found:', match.group())
```

## 5. 使用re.sub()进行替换

使用`re.sub()`函数，按照正则表达式对字符串进行替换：

```python
# 替换邮箱地址为 [REDACTED]
text = "Contact: info@example.com"
new_text = re.sub(r'\S+@\S+', '[REDACTED]', text)
print(new_text)  # 输出: Contact: [REDACTED]
```

# Overall

记得总是对你的正则表达式进行测试，以确保其按预期工作。
