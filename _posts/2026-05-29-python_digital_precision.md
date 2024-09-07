---
layout:     post
title:      "Python计算精度问题"
subtitle:   "Python计算精度问题"
date:       2026-05-29
author:     "Gavin Wang"
catalog:    true
img:
summary: "一个因Python计算精度而引发的问题小结"
categories:
    - [python]
tags:
    - python
---

# 概述

今天测试订单时发现一个蛮有趣的问题：

`python` 对最大浮点数是后2位的所有数值进行累加求和，最后求和结果出现了小数点后10位。

这是什么情况？

我来详细描述一下问题：

`record["payAmount"]`的数值打印展示效果如下：

```shell
0.01
0.03
0.03
0.0
0.01
0.01
1000.0
0.01
0.01
0.0
500.0
0.01
100.0
100.0
0.03
0.02
0.01
0.01
0.01
0.01
0.01
2000.0
```

我要对字典中的这个数值累计求和，得到最后结果，分别尝试了下面的两个方法，如下。

## 测试1：sum方法求和

```python
with open("res.txt") as f:
    data = f.read()
    data_dict = json.loads(data)

total_cash = sum(each_pay['payAmount'] for each_cash in data_dict['data']['records'])
print(f"Total cash: {total_cash}")
```

得到的结果是“125008.90999999814”:

```shell
root@Gavin:~# python3 cash.py 
Total cash: 125008.90999999814
root@Gavin:~# 
```


## 测试2：各值叠加

```python
with open("res.txt") as f:
    data = f.read()
    data_dict = json.loads(data)

# total_cash = sum(each_cash['payAmount'] for each_cash in data_dict['data']['records'])
# print(f"Total cash: {total_cash}")

total_pay_amount = 0.0
for record in data_dict['data']['records']:
    total_pay_amount += record["payAmount"]
print(f"Total cash: {total_pay_amount}")

```

得到的结果是：

```shell
root@Gavin:~# python3 cash.py 
Total cash: 124908.92999999814
root@Gavin:~# 
```

# root cause

问题出在哪里呢？

这里有两个问题：

（1）同样一组数据，两次求和方式得到的结果不一致

（2）所有的数值（`record["payAmount"]`），精度最大是小数点后两位，比如0.01，最小是后一位，比如100.0，但是计算出来的结果却是小数点后10位

最初是发现（2）计算结果精度不对，所以才尝试了上面的两种方法，又碰到了（1）的问题。

为何确保计算结果的准确性，我将所有的值写入到一个`cash.txt`文件：

```shell
for record in data_dict['data']['records']:
    with open('cash.txt', "a+") as w:
        w.write(str(record['payAmount']) + '\n')
```

然后使用了`awk`进行求和，并保留了原有精度（浮点后2位）：

```shell
root@Gavin:~# awk '{sum += $1} END {printf "Total: %.2f\n", sum}' cash.txt
Total: 124808.80
root@Gavin:~# 
```

到了这里我还是不放心，将生成的`cash.txt`文件下载到了本地，贴到`excel`中进行求和计算，得到如下图所示的结果：

<img class="shadow" src="/img/in-post/excel_sum.png" width="800">

此时`awk`和`excel`计算的两处结果能够核对的上了，说明`python`计算结果确实是出问题了。

知道了问题所在，要如何破解？

这里就涉及到`python`高精度求和问题了，如下：

```shell
>>> # 浮点数精度问题示例
>>> result = 0.1 + 0.2
>>> print(result)  # 输出 0.30000000000000004 而不是精确的 0.3
0.30000000000000004
>>> 
```

对于参与求和的数越多，于是累计的误差就出现了。

# python高精度计算

`Python`中的高精度计算通常涉及到处理超出标准浮点数表示范围的数值，或者需要比标准浮点数更高的精度。`Python`提供了几种方法来处理高精度计算：

1. **decimal模块**：
   - `decimal` 模块提供了 `Decimal` 数据类型，用于十进制浮点算术。它允许用户自定义精度，并且可以避免二进制浮点数表示中的某些问题。
   - `Decimal` 类型在金融计算中特别有用，因为它可以精确表示货币值，避免因浮点数精度问题导致的误差。
   - 使用 `getcontext()` 可以设置精度（即小数点后的位数），并控制四舍五入的行为。

2. **fractions模块**：
   - `fractions` 模块提供了 `Fraction` 类，用于创建和操作有理数（分子和分母都是整数的数）。
   - `Fraction` 类在需要精确分数计算时非常有用，比如在处理需要精确比例或比率的计算时。

3. **math模块**：
   - `math` 模块提供了一些基本的数学运算函数，如 `sqrt`、`pow` 等，它们使用浮点数进行计算。
   - 虽然 `math` 模块不直接提供高精度计算，但它的一些函数在处理高精度数据时可以提供辅助。

4. **numpy库**：
   - `numpy` 是一个广泛使用的科学计算库，它提供了高精度的数据类型，如 `numpy.float64`。
   - `numpy` 也支持数组和矩阵运算，这在进行大规模数值计算时非常有用。

5. **第三方库**：
   - 除了Python标准库，还有许多第三方库提供了高精度计算功能，如 `mpmath` 库，它提供了多精度浮点数和高精度数学运算。


## 使用Decimal模块

为了解决`python`的浮点数误差问题，可以使用 `decimal` 模块：

```python
from decimal import Decimal, getcontext

# 设置精度
getcontext().prec = 4

# 精确计算
result = Decimal('0.1') + Decimal('0.2')
print(result)  # 输出 0.3
```

## 使用Fractions模块

对于需要精确分数计算的场景，可以使用 `fractions` 模块：

```python
from fractions import Fraction

# 精确分数计算
result = Fraction(1, 10) + Fraction(2, 10)
print(result)  # 输出 3/5
```

# 本次问题解决方法

本着简单至上的原则，本文代码做如下调整即可：

```python
import os
import json

with open("res.txt") as f:
    data = f.read()
    data_dict = json.loads(data)

total_cash = sum(float(each_cash['payAmount']) for each_cash in data_dict['data']['records'])

print(f"Total amount: {total_cash:.2f}")
```

计算结果如下：

```shell
root@Gavin:~# vim cash_v3.py 
root@Gavin:~# python3 cash_v3.py 
Total amount: 124808.80
root@Gavin:~#
```
