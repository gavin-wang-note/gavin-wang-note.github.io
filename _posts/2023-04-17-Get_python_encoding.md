---
layout:     post
title:      "一行命令获取python当前默认的编码格式"
subtitle:   "Get python preferred encoding"
date:       2023-04-17
author:     "Gavin"
catalog:    true
tags:
    - JBOD
---

# 实践

Python2.x

```
python -c 'import locale; print(locale.getpreferredencoding())'
```

Python 3.x

```
python3 -c 'import locale; print(locale.getpreferredencoding())'
```
