---
layout:     post
title:      "python字段反转去重"
subtitle:   "revert dict then delete duplicate"
date:       2020-10-02
author:     "Gavin"
catalog:    true
tags:
    - python
---


# 前言

最近在写script支持cobbler全自动部署OS，由于profile与system对应关系是1:N，下次执行自动安装前会清理掉对应的profile与system，但当有其他人使用了script生成的profile后，就形成了一个profile对应多个system，回头再删profile时出错，因为这个profile有被其他system占用，删除失败了。解决方法就是找处profile关联的system，先删除掉system，再删除profile。

这个过程碰到一个问题，如何获取cobbler profile与system的map关系（虽然可以通过cobbler CGI来获取map关系，但太重了点）。

# 问题所在

如下为测试示例获取到的profile与system的字典信息：

```
{'test02': 'Scaler-8.0-latest-x86_64', 'Scaler-CentOS-8.0-latest-x86_64': 'Scaler-CentOS-8.0-latest-x86_64', 'Scaler-8.0-latest-x86_64': 'Scaler-8.0-latest-x86_64', 'test01': 'Scaler-8.0-latest-x86_64'}
```

而我预期的映射关系是：

```
{'Scaler-CentOS-8.0-latest-x86_64': ['Scaler-CentOS-8.0-latest-x86_64'], 'Scaler-8.0-latest-x86_64': ['test02', 'Scaler-8.0-latest-x86_64', 'test01']}
```

# 解决方法

```
from collections import defaultdict
reversed_dict = defaultdict(list)
for key,value in mydict.iteritems():
    reversed_dict[value].append(key)
```
