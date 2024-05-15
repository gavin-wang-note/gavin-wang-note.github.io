---
title: Python Tips and Tricks
date: 2018-09-06 22:29:31
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: Python几个让你编程事半功倍的技巧
categories:
    - [python]
tags:
    - python
---


# Overview

分享一下在平时工作中所积累的技巧，供参考。


# 推导式

O(∩_∩)O哈哈~，开篇讲述一下推导式。

Python中的推导式（comprehensions）是一种简洁、高效地生成序列数据结构（如列表、字典、集合）的方法。

## 列表推导式（List comprehensions）

列表推导式是一个表达式，接一个 for 语句，然后有零到多个 for 或 if 语句。它的结果是一个列表，由 for 和 if 语句上下文中计算出来的表达式得来。例如：

```python
squares = [x**2 for x in range(10)]
```

上述列表推导式生成了一个包含从0到9（包括9）的所有数字的平方的列表。


## 字典推导式（Dict comprehensions）

类似于列表推导式，字典推导式也可以用来创建字典。以下是创建一个数字到其平方映射的字典的例子：

```python
squares_dict = {x: x**2 for x in range(5)}
```

这行代码生成了一个字典 {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}，它将0-4（包含4）的每个数字映射到它的平方。

## 集合推导式（Set comprehensions）

将列表推导式的中括号 [] 替换为大括号 {} 就可以创建集合。如下例：

```python
squares_set = {x**2 for x in range(5)}
```

上述例子中生成了一个集合 {0, 1, 4, 9, 16}，包含了0到4（包含4）的所有数字的平方。

## 条件推导式（Conditional comprehensions）

在推导式中使用 if 语句可以用来过滤条件。例如，下面这个例子生成了只包含偶数的平方的列表：

```python
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

上述例子中生成了一个列表 [0, 4, 16, 36, 64]，包含了0到9（包含9）的所有偶数的平方。

## 生成器推导式（Generator comprehensions）

生成器推导式是一种更高效的数据处理方式。它们与列表推导类似，但是使用圆括号 () 代替方括号 []。生成器推导式会返回一个生成器对象，可以通过 next() 函数或 for 循环来逐个获取元素，而不是一次性生成所有元素。因此，它们在处理大数据量时可以节省大量内存。

```python
squares_gen = (x**2 for x in range(10))
```

上述例子中生成了一个生成器对象 squares_gen。你可以使用 next(squares_gen) 来逐个获取值，或者直接在 for 循环中使用它。


# map()

**说明：**

这里简单介绍一下map，除了map之外，还有filter和reduce，未来有时间会整理一份这三个函数的使用方法与区别。

map() 是 Python 内置函数，用于将一个函数应用于一个输入列表（或其他可迭代对象）的所有元素。map() 函数的返回结果是一个 map 对象，是一个迭代器对象。

## map()基本用法

map() 函数的基本语法如下：

```python
map(function, iterable)
```

* function：一个函数，它接收一个参数
* iterable：一个或多个可迭代的对象

函数 function 将被应用到 iterable 的每一个元素。如果提供了额外的 iterable 参数，则 function 必须接收相同数量的参数，并且会被并行地应用于所有的 iterable 参数的元素。

例如，考虑以下场景，你有一个数字列表，你需要获取列表中所有数字的平方：

```python
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
```

在这个示例中，lambda x:x ** 2 是一个匿名函数，用于计算一个数的平方。map()函数将这个函数应用到列表numbers` 中的每一个元素。

要看到 map() 函数的返回结果，你可以将其转化为列表：

```python
print(list(squared))  # 输出: [1, 4, 9, 16, 25]
```

注意，map() 返回的是一个可迭代的 map 对象，所以转化为列表后可以直接打印。

## map()应用

根据条件在序列中筛选数据：

假设有一个数字列表 data, 过滤列表中的负数

```python
data = [1, 2, 3, 4, -5]
  
# 使用列表推导式
result = [i for i in data if i >= 0]
  
# 使用 fliter 过滤函数
result = filter(lambda x: x >= 0, data)
```

再比如学生的数学分数以字典形式存储，筛选其中分数大于 80 分的同学

```python
from random import randint
  
d = {x: randint(50, 100) for x in range(1, 21)}
r = {k: v for k, v in d.items() if v > 80}
```

# zip()

Python内置函数zip()是一个生成器，用于将两个或更多个可迭代对象的元素配对生成新的可迭代对象，即生成一个元组的迭代器，其中第i个元组包含来自每个参数序列或可迭代对象的第i个元素。

当所输入可迭代对象中最短的一个被耗尽时，迭代器将停止迭代。

## zip()的基础用法

```python
numbers = [1, 2, 3]
letters = ['a', 'b', 'c']
zipped = zip(numbers, letters)

print(list(zipped))  # 输出：[(1, 'a'), (2, 'b'), (3, 'c')]
```

这段代码将列表numbers和letters中的元素配对，然后将配对的元组放入到新的列表中。

## zip()用于不等长输入

如果输入的列表长度不相等，zip()会在最短的列表耗尽后停止：

```python
numbers = [1, 2, 3]
letters = ['a', 'b']
zipped = zip(numbers, letters)

print(list(zipped))  # 输出：[(1, 'a'), (2, 'b')]
```

这里，由于letters列表只有两个元素，所以返回的结果只包含两个元组，numbers中的3被忽略了。

## zip()用于大于两个的输入

zip()函数同样可以接受两个以上的输入序列：

```python
numbers = [1, 2, 3]
letters = ['a', 'b', 'c']
floats = [4.0, 5.0, 6.0]
zipped = zip(numbers, letters, floats)

print(list(zipped))  # 输出：[(1, 'a', 4.0), (2, 'b', 5.0), (3, 'c', 6.0)]
```

在这个例子中，我们将三个列表中的元素配对，生成了一个包含三个元素的元组列表。每个元组都包含来自所有输入列表的对应元素。

## 使用zip()进行解压

zip()函数的一个常见用法是和*运算符（解包运算符）一起使用来解压序列。基本上，这意味着你可以使用zip()将配对的元组序列转换回两个独立的序列（列表、元组等）：

```python
zipped_list = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers, letters = zip(*zipped_list)

print(numbers)  # 输出：(1, 2, 3)
print(letters)  # 输出：('a', 'b', 'c')
```

这个例子展示了如何将之前通过zip()函数打包的列表zipped_list解压回两个独立的元组。

## 在迭代中同时使用zip()

zip()函数在同时迭代多个序列时特别有用。通过zip()，你可以更为优雅地执行操作，而不是使用索引。例如，比较两个列表中相同位置上元素的大小：

```python
list1 = [1, 2, 3, 4]
list2 = [4, 2, 2, 5]

for x, y in zip(list1, list2):
    if x > y:
        print(f'{x} is greater than {y}')
    elif x < y:
        print(f'{x} is less than {y}')
    else:
        print(f'{x} is equal to {y}')
```

这样，你可以同时迭代list1和list2中的元素，并进行比较。

## 对字典的键值对进行翻转

zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。

```python
from random import randint, sample
  
s1 = {x: randint(1, 4) for x in sample("abfcdrg", randint(1, 5))}
d = {k: v for k, v in zip(s1.values(), s1.keys())}
```


## 小结

zip()是Python中一个非常强大且有用的内置函数，它使得在处理多个序列时，代码更加清晰，易读，并且Pythonic。无论是进行并行迭代，还是需要将数据形式互相转换时，zip()都可以被有效地使用。


# pprint

Python内置的pprint模块提供了一个“漂亮打印（pretty printer）”的功能，用于生成数据结构的格式化表示，使其更易于阅读。这对于调试，或者当你需要以易于理解的格式输出复杂的数据结构（如深层嵌套的字典或列表）时非常有用。

## 基本用法

要使用pprint模块的基本功能，你需要先导入该模块，然后使用pprint()函数。这里有一个简单的例子展示如何使用它打印一个复杂的数据结构：

```python
import pprint

data = [{
    'name': 'John',
    'age': 30,
    'city': 'New York'
}, {
    'name': 'Jane',
    'age': 25,
    'city': 'Paris'
}]

pprint.pprint(data)
```

上述代码输出效果如下：

```shell
>>> pprint.pprint(data)
[{'age': 30, 'city': 'New York', 'name': 'John'},
 {'age': 25, 'city': 'Paris', 'name': 'Jane'}]
>>> 
```

## 小结

pprint.pprint()函数将自动为你格式化输出，使其更加易读。与标准的print()函数相比，pprint()对于复杂数据结构的输出会自动换行并适当缩进。


## 定制化

pprint模块提供了多种方式来定制输出格式。PrettyPrinter类提供了更多的定制选项，包括控制输出宽度，深度，以及每行元素的数量。你可以创建一个PrettyPrinter实例，并用它来打印数据：


```python
pp = pprint.PrettyPrinter(indent=4, width=41, depth=2)
pp.pprint(data)
```

在这个例子中，我们指定了缩进为4个空格，最大宽度为41字符，以及最大深度为2。当数据结构的深度超过depth参数时，pprint会用...来标示更深层的内容。

## 排序字典键

默认情况下，从Python 3.8开始，pprint会根据字典中键的插入顺序来打印字典。在更早的版本中（或如果你需要不同的行为），你可以通过sort_dicts=False参数来控制是否需要对字典键进行排序。例如：

```python
pprint.pprint(data, sort_dicts=True)
```

这个例子将确保字典中的键在打印时按照升序排序。

## pprint() 和 pformat()


除了pprint()函数，pprint模块还提供了一个pformat()函数，它返回一个格式化后的字符串而不是直接打印。这在你需要将格式化后的字符串用于日志记录、存储或通过网络发送时非常有用：

```python
formatted_str = pprint.pformat(data)
print(formatted_str)
```

这样，你就能获取到格式化后的字符串并且可以自由地使用它。


## 小结

总的来说，pprint模块是一个非常有用的工具，特别是在处理复杂的数据结构时。它通过提供清晰的格式化输出，增强了Python的可读性和调试能力。通过使用pprint.PrettyPrinter类和相关的函数，你可以精确地控制输出的格式，使其满足你的具体需求。



# sh

Python 的 sh 模块是一个第三方库，它提供了一个简单易用的接口来执行 shell 命令。它允许你从 Python 脚本中运行命令行指令，并捕获它们的输出。

## 安装

首先，你需要安装 sh 模块。你可以使用 pip 来安装它：

```shell 
pip install sh
```

## 使用

sh 模块提供了几个函数来执行命令，其中最常用的是 sh() 函数。以下是一些基本的用法示例：


### 执行命令并捕获输出

```python
import sh

result = sh.sh('echo "Hello, World!"')
print(result)
```

这将输出：

```plaintext
Hello, World!
```

### 获取命令的输出

sh.sh() 函数返回一个 sh.Result 对象，其中包含了命令的输出、错误、退出状态等信息。

```python
output = sh.sh('ls')
print(output.stdout)  # 命令的标准输出
print(output.stderr)  # 命令的标准错误输出
print(output.exit_code)  # 命令的退出状态码
```

## 执行多个命令

你可以使用分号 ; 或者 && 来在一行中执行多个命令。

```python
output = sh.sh('echo "First"; echo "Second"')
print(output.stdout)
```

## 使用管道

sh 模块支持使用管道 | 来将一个命令的输出传递给另一个命令。

```python
output = sh.sh('ls | grep "test"')
print(output.stdout)
```

## 捕获错误

如果你想要捕获命令执行中的错误，可以使用 sh.ErrorReturnCode 异常。

```python
try:
    output = sh.sh('cat non_existent_file.txt')
except sh.ErrorReturnCode as e:
    print("An error occurred:", e)
```

**注意事项:**

* 使用 sh 模块时，应该小心处理用户输入，以避免潜在的安全风险，如 shell 注入攻击。
* sh 模块主要用于简单的命令行操作。对于更复杂的 shell 脚本任务，你可能需要使用 Python 的 subprocess 模块，它提供了更多的灵活性和控制。


# list转字符串

在Python中，如果你想将列表中的所有元素连接成一个字符串，可以使用join()方法，它是str类型的一个方法。

join()方法接受一个可迭代参数（如列表），并将其连接成一个字符串。它是通过将每个元素转化成字符串，然后使用调用join()方法的字符串作为分隔符将它们连接起来。

考虑以下例子：

```python
list1 = ['Hello', 'world', '!']
str1 = ' '.join(list1)
print(str1)  # 输出：'Hello world !'
```

在这个例子中，我们使用空格（' '）作为分隔符，将list1中的所有元素连接成了一个字符串。

注意，join()方法只能用于字符串的列表。如果列表中包含非字符串元素，则需要在使用join()前将它们转化为字符串。例如：

```python
list2 = [1, 2, 3, 4, 5]
str2 = ''.join(str(e) for e in list2)
print(str2) # 输出：'12345'
```

上述代码通过列表推导式将`list2`中的所有元素转化为字符串，然后用空字符串（''）作为分隔符将它们连接起来。

# 频率统计

Python的collections模块提供了一系列扩展的容器类型，它提供了比通常的内置类型（如列表、字典和元组）更丰富的功能。其中一个非常有用的类是Counter，它主要用于对可哈希对象进行计数。

## Counter类

Counter是一个字典子类，用于计算可哈希对象的频率。它是自动的哈希表，用于计数对象。元素作为键存储在Counter对象中，它们的计数作为值。

## 基本用法

```python
from collections import Counter

# 创建一个Counter对象
c = Counter(['apple', 'orange', 'banana', 'apple', 'orange', 'apple'])
print(c)
# 输出：Counter({'apple': 3, 'orange': 2, 'banana': 1})

# 也可以直接用字符串初始化
c = Counter("abracadabra")
print(c)
# 输出：Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
```

## 访问计数

```python
# 获取任何元素的计数
print(c['a'])  # 输出：5

# 访问不存在的键，不会报错而是返回0
print(c['z'])  # 输出：0
```

## 更新计数

你可以更新Counter对象中的元素计数。使用update()方法可以增加计数，而减少计数则可以通过从Counter对象中减去另一个Counter对象来完成。

```python
c.update(['a', 'b'])
print(c)
# 输出：Counter({'a': 6, 'b': 3, 'r': 2, 'c': 1, 'd': 1})

c.subtract(['a', 'b'])
print(c)
# 输出：Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
```

## 方法和操作

Counter对象支持类似于字典的方法，并提供了一些有用的额外功能，如elements()、most_common()等：

```python
# 获取计数最多的n个元素
print(c.most_common(2))
# 输出：[('a', 5), ('b', 2)]

# 获取所有元素的迭代器
print(list(c.elements()))
# 输出：['a', 'a', 'a', 'a', 'a', 'b', 'b', 'r', 'r', 'c', 'd']
```

## 其他collections类

除了Counter之外，collections模块还提供了许多其他有用的类：

* namedtuple()：为元组中的每个位置命名，提供更具可读性的元组子类。
* OrderedDict：字典的子类，保留了他们被添加的顺序。
* defaultdict：字典的子类，为字典查询提供了一个默认值。
* deque：类似列表的容器，支持从头部和尾部高效地添加和删除元素。


## Counter示例

对某英文文章单词进行统计，找到出现次数最高的单词以及出现的次数

```python
import re
from collections import Counter
  
# 统计某个文章中英文单词的词频
with open("test.txt", "r", encoding="utf-8") as f:
  d = f.read()
  
# 所有的单词列表
total = re.split("\W+", d)
result = Counter(total)
print(result.most_common(10))
```

# 繁体字转简体字,简体字转繁体字

在Python中，繁体字与简体字之间的转换可以通过第三方库完成。一个常用的库是OpenCC，它能够在不同中文字符集之间进行转换，包括繁体字、简体字等。

## 安装OpenCC

首先，你需要安装opencc-python-reimplemented库，这是OpenCC的Python接口。可以通过pip命令安装：

```shell
pip install opencc-python-reimplemented
```

## 简体转繁体

使用OpenCC进行简体字到繁体字的转换如下：

```python
from opencc import OpenCC
cc = OpenCC('s2t')  # 定义转换方向为简体到繁体
converted = cc.convert('简体中文转换成繁体中文')
print(converted)
```

## 繁体转简体

同样，你也可以将繁体字转换为简体字：

```python
cc = OpenCC('t2s')  # 定义转换方向为繁体到简体
converted = cc.convert('繁體中文轉換成簡體中文')
print(converted)
```

## 转换方向

OpenCC支持以下转换方向：

* s2t : 简体中文到繁体中文
* t2s : 繁体中文到简体中文
* s2tw : 简体中文到台湾正体
* tw2s : 台湾正体到简体中文

等等，更多转换方向可以在OpenCC的文档中找到。

## 除了OpenCC，还有哪些用于中文字符集转换的工具？

除了OpenCC，还有一些其他工具和库可用于中文字符集的转换，包括简体和繁体中文之间的转换。下面列出了一些常用的选项：

## 1. HanLP

HanLP不仅提供了中文字符集的转换功能，还是一个全方位的中文自然语言处理库，支持词性标注、命名实体识别等多种功能。

HanLP的简繁转换需要使用到特定的API，它包含更广泛的自然语言处理功能。

## 2. hanziconv

hanziconv 是一个轻量级的Python库，提供了简单易用的繁简转换功能。

```shell
pip install hanziconv
```

```python
from hanziconv import HanziConv

print(HanziConv.toSimplified('漢字轉換器'))  # 繁体到简体
print(HanziConv.toTraditional('汉字转换器'))  # 简体到繁体
```

## 3. cjklib

cjklib 提供了中日韩文字符处理的工具，包括读音信息、字符数据以及中文字符集的转换。

```shell
pip install cjklib
```

cjklib 的使用更偏向于学术研究和详细的字符信息处理，对于一般的繁简转换来说，可能功能略显复杂。

## 4. langconv & zhconv (Python 2)

对于Python2的用户，langconv（简繁转换）和zhconv（更适合网络爬虫）是历史上曾被较广泛使用的库，这两个库基于MediaWiki的繁简转换表实现，但它们在Python3上可能需要做一些修改才能使用。

```python
# langconv 示例（对于Python 3可能需要进行修改才能运行）
from langconv import *

# 简体转繁体
traditional_sentence = Converter('zh-hant').convert(simplified_sentence)
print(traditional_sentence)

# 繁体转简体
simplified_sentence = Converter('zh-hans').convert(traditional_sentence)
print(simplified_sentence)
```

## 小结

每个库和工具都有其优势和特点，选择哪一个取决于你的具体需求、Python版本以及你希望集成的其他功能。对于简单的繁简转换来说，hanziconv 因其简洁易用而受到推荐；而如果你需要更全面的自然语言处理功能，则可能会倾向于选择HanLP。


# 文件查找

在Python中，有多种方法可以查找文件。这里需要的主要库是os和glob。

## 使用os.walk()

os.walk()是一种简单的遍历目录树的方式，对于查找文件特别有用。以下是如何使用os.walk()查找特定文件的方法：

```python
import os

def find_file(filename, search_path):
   for root, dir, files in os.walk(search_path):
      if filename in files:
         return os.path.join(root, filename)
            
result = find_file('my_file.txt', '/path/to/directory')
```

在这个例子中，os.walk()会遍历/path/to/directory中的所有子目录并检查每个目录中的文件。当找到与filename匹配的文件时，会返回该文件的完整路径。

## 使用glob.glob()

glob模块是另一种查找文件的方式，它支持Unix风格的路径名模式。这对于需要匹配特定模式的文件名（如查找所有.txt文件）非常有用：

```python
import glob

def find_files(pattern, path):
    return glob.glob(f'{path}/**/{pattern}', recursive=True)

results = find_files('*.txt', '/path/to/directory')
```

在这个示例中，glob.glob() 用于查找 /path/to/directory 中的所有 .txt 文件。星号 * 是一个通配符，表示任何字符（除了目录分隔符）。 {pattern} 是文件名模式，这里我们搜索所有的 .txt 文件。

recursive=True 参数让 glob 在所有子目录中查找匹配的文件，就像 os.walk() 那样。

**注意：**

glob.glob() 返回的是所有匹配的文件路径列表，而 os.walk() 则是在找到第一个匹配的文件后就返回。根据你的需求，你可能需要只找到第一个匹配的文件，或者返回所有匹配的文件列表。

## 使用 os.listdir() 和 fnmatch()

os.listdir() 可以列出一个目录中的所有文件和子目录，并且可以与 fnmatch 模块结合，用来对文件名进行模式匹配。

```python
import os
import fnmatch

def find_file(pattern, path):
    result = []
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, pattern):
            result.append(os.path.join(path, filename))
    return result

results = find_file('*.txt', '/path/to/directory')
```

这段代码会查找指定目录 /path/to/directory 中所有匹配 *.txt 模式的文件，并将它们的完整路径添加到 result 列表中。

fnmatch.fnmatch() 函数检查文件名是否符合Unix filename pattern匹配。

**注意**:

* 当目录结构非常大时，进行文件搜索操作可能会比较耗时。
* 如果你正在处理非常特定的需求（如文件属性或创建日期），可能需要编写更复杂的文件搜索逻辑。
* Python的 Pathlib 模块在 Python 3.4 中引入，提供了面向对象的文件系统路径处理方法。以下是使用 Pathlib 查找文件的简化示例：

```python
from pathlib import Path

def find_files(pattern, path):
    return Path(path).rglob(pattern)

results = find_files('*.txt', '/path/to/directory')
for result in results:
    print(result)  # prints the full path to each matching file
```

Path.rglob() 方法用于递归搜索符合给定模式的所有文件，这里 rglob 类似于带有 recursive=True 参数的 glob.glob()。

选择最佳方法取决于你的具体需求、可能的性能考虑以及你对代码的个人偏好。

# 时间转换

直接上之前自动化测试框架中的封装好的函数：

```python
import time
import datetime


def sec2str(secs):
    """
    Change the seconds to a time format :%Y-%m-%d %H:%M:%S
    :param secs, int, a seconds time, such as 1535705378.02
    """
    if int(secs) < 0:         
        return ""

    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(secs))


def get_date_time(**kwargs):
    """  Return a data time, format is '%Y-%m-%d %H:%M:%S'  """
    date_time = (datetime.datetime.now() + datetime.timedelta(**kwargs)).strftime('%Y-%m-%d %H:%M:%S')
    logging.debug("--  Current date time is : (%s)", date_time)
    return date_time


def change_timestamp_to_time(timestamp):
    """
    Change the timestamp to time, such as 1479264792 to 2016-11-16 10:53:12
    :param timestamp, string, a timestamp
    """ 
    time_struct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)

            
def change_date_time_to_timestamp(date_time):
    """         
    Change time to timestamp 
    :param date_time, string, a time, such as 2016-11-16 10:53:12
    """
    time_arry = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_arry)
    return timestamp
```

# 随机生成

## 随机验证码的生成

在Python中，生成随机验证码涉及到两个主要步骤：生成随机字符，然后将这些字符连接成一个字符串。常用的方法是使用Python内置的random和string模块。

以下是一个简单的例子，生成一个包含大小写字母和数字的6位随机验证码：

```python
import random
import string

# 验证码由数字和字母（大写和小写）组成
chars = string.ascii_letters + string.digits

# 随机生成六位验证码
code = ''.join(random.choice(chars) for _ in range(6))

print(code)  # 类似输出：'a3BZ9d'
```

这段代码的工作原理如下：

* string.ascii_letters是string模块中的一个预定义字符串，包含所有ASCII码的大小写字母。
* string.digits 是一个包含所有数字的字符串。
* random.choice(chars) 会从 chars 字符串中随机挑选一个字符

如果你想生成一个包含特殊字符的随机验证码，可以通过在字符集中加入特殊字符来实现。Python的string模块中已经定义了一些常用字符集，例如字母和数字，而特殊字符则需要你根据需求自定义添加。

以下是一个示例，展示了如何生成一个包含大小写字母、数字和特定特殊字符的随机验证码：

```python
import random
import string

# 定义验证码的组成部分：包括大小写字母、数字、特殊字符
chars = string.ascii_letters + string.digits + "!@#$%^&*()"

# 随机生成一个六位长度的验证码
code = ''.join(random.choice(chars) for _ in range(6))

print(code)  # 示例输出：'aB3!$@'
```

这里，通过string.ascii_letters和string.digits增加了字母和数字，加号（+）被用于字符串的连接，"!@#$%^&*()"是一个包含特殊字符的字符串。random.choice(chars)将从这个组合的字符串中随机选择字符，range(6)定义了验证码的长度为6个字符。

此外，如果你想生成包含更多或不同特殊字符的验证码，只需调整包含在chars字符串中的特殊字符即可。

**注意：**

在使用特殊字符时，要确保所选特殊字符与你的应用场景兼容。某些场合可能对可用的特殊字符有限制。

## 生成随机IP地址

```python
def random_IP():
    random_list = random.sample(range(1,256)*4, 4)
    str_random_list= map(str, random_list)
    return '.'.join(str_random_list)
```

## 随机的生成指定长度的Ascii和数字

```python
def rand_low_ascii(length=10):
    """
    随机的生成指定长度的Ascii和数字.
    len指定的是生成的字符串的长度.
    :param length, string, Randomly generated string length, default is 10
    """
    return ''.join([choice(ascii_lowercase) for i in xrange(length)])
```



## 随机生成指定长度的数字

```python
def rand_alpha(length=9):
    """
    随机生成指定长度的数字
    :param length, string, The length of the randomly generated number, default is 9
    """
    return ''.join([choice(digits) for i in xrange(length)])
```



## 随机返回类的一个成员值

```python
def random_member(ClassName):
    """
    抽取类中的成员，随机返回一个成员值
    注：一定要保证类有__doc__值
    :param ClassName, object, a class name
    """
    member = ClassName.__dict__
    if member.get('__module__') is not None:
        del member['__module__']
    if member.get('__doc__') is not None:
        del member['__doc__']
    membertuple = member.items()
    randomvalue = membertuple[random.randint(0, len(membertuple)-1)]

    return randomvalue[1]
```

# 去除列表中重复元素

在Python中，可以通过多种方式去除列表中的重复元素。以下是几种常见的方法：

## 方法1. 使用集合(set)

将列表转换成集合会自动移除重复元素，因为集合里的元素是唯一的。但是，这种方法会丢失原始列表的顺序。

```python
my_list = [1, 2, 2, 3, 4, 4, 5]
my_set = set(my_list)
unique_list = list(my_set)
print(unique_list)  # 输出：[1, 2, 3, 4, 5]
```

## 方法2. 使用字典

字典的键也是唯一的。通过将列表元素作为字典的键，可以移除重复元素。这种方法同样会丢失原始列表的顺序，但在Python 3.7+中，字典是有序的，因此可以保持顺序。

```python
my_list = [1, 2, 2, 3, 4, 4, 5]
unique_list = list(dict.fromkeys(my_list))
print(unique_list)  # 输出：[1, 2, 3, 4, 5]
```

## 方法3. 列表推导式

使用列表推导式检查元素是否已经在新列表中，从而保留元素的原始顺序。这种方法适用于较小的列表，对于大列表可能效率较低。

```python
my_list = [1, 2, 2, 3, 4, 4, 5]
unique_list = []

[unique_list.append(x) for x in my_list if x not in unique_list]

print(unique_list)  # 输出：[1, 2, 3, 4, 5]
```

## 方法4. 使用collections.OrderedDict

从Python 3.7开始，字典是有序的。但在早期版本中，可以使用collections.OrderedDict来保持原始列表的顺序。

```python
from collections import OrderedDict

my_list = [1, 2, 2, 3, 4, 4, 5]
unique_list = list(OrderedDict.fromkeys(my_list))
print(unique_list)  # 输出：[1, 2, 3, 4, 5]
```

## 方法5. 使用pandas库

如果你在使用pandas库，可以利用它移除重复元素并保持顺序。

```python
import pandas as pd

my_list = [1, 2, 2, 3, 4, 4, 5]
unique_list = pd.Series(my_list).drop_duplicates().tolist()

print(unique_list)  # 输出：[1, 2, 3, 4, 5]
```

选择哪种方法取决于你的具体需求，包括是否需要保持列表的原始顺序、列表的大小以及是否已经在使用如pandas这样的第三方库。


# 根据字典中值的大小，对字典中的项进行排序


比如班级中学生的数学成绩以字典的形式存储，请按数学成绩从高到底进行排序

方法1: 利用 zip 将字典转化为元组，再用 sorted 进行排序

```python
from random import randint
  
data = {x: randint(60, 100) for x in "xyzfafs"}
sorted(data)
data = sorted(zip(data.values(), data.keys()))
```

方法2: 利用 sorted 函数的 key 参数

```python
from random import randint
  
data = {x: randint(60, 100) for x in "xyzfafs"}
data.items()
sorted(data.items(), key=lambda x: x[1])
```

# 在多个字典中找到公共键

实际场景：在足球联赛中，统计每轮比赛都有进球的球员

第一轮：{"C罗": 1, "苏亚雷斯":2, "托雷斯": 1..}
第二轮：{"内马尔": 1, "梅西":2, "姆巴佩": 3..}
第三轮：{"姆巴佩": 2, "C罗":2, "内马尔": 1..}


```python
# 定义每轮比赛的球员和进球数的字典
round1 = {"C罗": 1, "苏亚雷斯": 2, "托雷斯": 1}
round2 = {"内马尔": 1, "梅西": 2, "姆巴佩": 3}
round3 = {"姆巴佩": 2, "C罗": 2, "内马尔": 1}

# 将每轮比赛的字典存储在一个列表中
rounds = [round1, round2, round3]

# 获取所有轮次的键的集合
keys_sets = [set(rnd.keys()) for rnd in rounds]

# 使用集合的交集找出所有轮次中共有的键
common_keys = set.intersection(*keys_sets)

# 输出共有的键，即在多个轮次中都有进球的球员
print("公共的键（球员）:", common_keys)

# 统计公共键在整个比赛轮次中的进球总数
total_goals = {key: 0 for key in common_keys}

for rnd in rounds:
    for player, goals in rnd.items():
        if player in common_keys:
            total_goals[player] += goals

# 输出每个球员的总进球数
print("球员的总进球数：")
for player, goals in total_goals.items():
    print(f"{player}: {goals}")
```

# 使用 enumerate 获取迭代器索引和值

在迭代时获取索引和对应的值，在迭代一些可迭代对象时（例如list，dict），可通过内置enumerate来获取迭代元素的索引值

```python
for index, value in enumerate(names):
    print(index, value)
```


# 使用列表解析展平列表

将嵌套的列表展平为一维列表。

```python
nested_list = [[1, 2, 3], [4, 5], [6, 7, 8]]
flattened_list = [num for sublist in nested_list for num in sublist]
print(flattened_list)
```

结果:

```shell
[1, 2, 3, 4, 5, 6, 7, 8]
```

还有一种方式可以连接两个列表

```python
a = [1, 2, 3]  
b = [5, 6, 7]  
  
c = [*a, *b]  
print(c)
```

结果:

```shell
[1, 2, 3, 5, 6, 7]
```

# 重复

## 重复列表

```python
>>> [1,2,3] * 4
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
```

## 重复字符串

```python
>>> 'dog eat dog;' * 3
'dog eat dog;dog eat dog;dog eat dog;'
>>> 
```

# 字典合并

```python
>>> a= {"a":1}
>>> b= {"b":2}
>>> {**a, **b}
{'a': 1, 'b': 2}
>>>
```

# 字符串反转

```python
>>> s = "This is a dog eat dog world!"
>>> s[::-1]
'!dlrow god tae god a si sihT'
>>> 
```

