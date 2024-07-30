---
title: markdown文件实现标题缩一级功能
date: 2024-04-09 21:03:19
author: Gavin Wang
img: "/img/markdown/markdown1.jpg"
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: 替换markdown中#以实现标题缩一级功能
categories:
    - [python]
tags:
    - python 
---

# 概述

因为最近在整理文档，使用markdown格式编写pytest相关知识点，一个md文件为一个系统性的知识点，现在准备把这些文件合并成一个md文件，各个章节的标题都要缩一级。由于篇幅比较长，接近800页，手工操作会非常耗时，也容易出错，遂写了这个脚本，帮我替换文件中的#，达到md文件缩一级别的目的。
操作手法也比较简单，查看markdown文件的源码，拷贝下来贴到文件a.txt中，然后对这个文件进行替换处理，同时要关注文章中有哪些内容也是一#开头的，需要忽略一下，避免误替换。方法也简单，比如：

```shell
cat a.txt |grep '^#' |grep [0-9] |grep -v '-' |grep -v 'content' | grep -v '注释' | grep -Evi 'Centos7|This kickstart file|AMD6|S3 takeover IP|/usr/bin/env|没有用修饰器修饰，故不会引用|添加 flake8 的配置|下面我们定义了30个独立的测试用例|应为200，表示成功删除，无返回内容' >b.txt
```

检查下b.txt文件，是否还有其他误替换的，再反过滤即可。

# 代码实现

如果使用Shell命令，会比较复杂一些，这里使用python实现。直接上代码（比较粗糙，临时顶替，能用就好^-^）

```python
import re


def should_replace(line):
    exclude_patterns = [
        '-',
        'content',
        '注释',
        'Centos7',
        'This kickstart file',
        'AMD6',
        'S3 takeover IP',
        '/usr/bin/env',
        '没有用修饰器修饰，故不会引用',
        '添加 flake8 的配置',
        '下面我们定义了30个独立的测试用例',
        '应为200，表示成功删除，无返回内容',
        'Get file of md5',
        '将是',
        'This test will be',
        '检查结果是否为',
        '一般来说，0 表示测试通',
        'cells.insert',
        'Add funcargs as fixtur',
        'Safari',
        'Edge',
        '假设有效的用户名和密码',
        '键名看起来像 ',
        '只会在 number_fixture',
        '设置函数超时限制',
        '将时间向前移动',
        '发起GET请求并设定连接超',
        '这个测试将会运行10次'
    ]
    if line.strip().startswith("#") and any(char.isdigit() for char in line):
        if not any(re.search(pattern, line, re.IGNORECASE) for pattern in exclude_patterns):
            return True
    return False


def process_file(input_filepath, output_filepath):
    with open(input_filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    new_lines = []
    for line in lines:
        # 首先确认行是否符合替换的条件
        if should_replace(line):
            # 使用 re.sub 替换行开头第一个 '#' 为 '##'
            # 注意这里的正则表达式
            # '\A#' 匹配字符串开头的 '#'
            # '\A##*#' 匹配字符串开头的连续 '#'，但至少需要有一个 '#'
            line = re.sub(r'\A#', '##', line, count=1)
        new_lines.append(line)

    # 写入新文件
    with open(output_filepath, 'w', encoding='utf-8') as new_file:
        new_file.writelines(new_lines)

# 使用方法：
process_file('a.txt', 'output_filename.txt'
```


解释如下：

在这里，我们使用 \A# 正则表达式来确保我们只匹配每一行开头的第一个 #。\A 是正则表达式中用于匹配字符串开始位置的特殊符号。
count=1 参数确保只替换第一次匹配到的 #。这样，如果一行以多个 # 开头，只会将行开头的第一个 # 替换成 ##。其他的 # 将保持不变。

最后，将调整后的内容写入新文件（output_filepath），而不是覆盖原来的文件。
