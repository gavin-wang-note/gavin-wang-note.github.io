---
title: 浏览器中header信息转换为json
date: 2017-03-12 16:22:18
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 将浏览器中复制下来的原始header信息转换为json格式
categories:
    - [python]
tags:
    - python
---

# 前言

当写API自动化的时候，在构建自动化测试框架之初，总会碰到要把浏览器中访问对应产品的header信息写入到requests或者是httpx的header中，方便后续构造HTTP请求时能够携带正确的header信息到产品，从而实现类似诸如登录会话保持。

这里需要从浏览器中拷贝下来当前产品的header信息，然后一个一个的贴到封装的header代码初始化的地方，虽然工作量比较小，但我这里还是写了支script，方便我完整的将header信息放到初始化处，免得少贴了内容，来来回来一遍又一遍的执行代码调试HTTP请求能否成功。


# 工作过程

## 从浏览器F12中获取header信息

以Firefox browser为例，F12--> 选择对应接口，右键点击 -->  复制值 --> 复制请求头


## 将上述内容报存

文件命名为header.search，如：

```shell
GET /tholo/pytest-flake8/spoofed_commit_check/d730278626fe02a3545e9fc79999fa5ec9c30a29 HTTP/2
Host: github.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0
Accept: text/html
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br, zstd
Referer: https://github.com/tholo/pytest-flake8
X-Requested-With: XMLHttpRequest
Connection: keep-alive
Cookie: _octo=GH1.1.408032656.1695809589; logged_in=no; _device_id=3a906646e633cfc8d1773e1699957c29; _gh_sess=fanO9iUDx5TxUkSX%2BvsGj3aaJDwnOQ2WFv6ck7RfQCbvnZiTntz9UTdQcP7%2BMDMEvh1J%2BzSq35kY5EvV9yKzzyItORIbH9xVVLEQOcc5ooZNSp54FFfmKr4NKYX3mMGbi1K3Y%2BRKuLAu6LQfw4Du14CtVJ5JGRTTfsmXW0JzRqgA3UzAEu1Ee2LQZhOjO4E%2F3eAEteb5x6Kj7i6axGqxzfxjZK4ASCSnoyjMV%2BSaQ6KMwHKvrlzOp%2BcUgmd7ilZXzMrr7ud8r3xDlkA5UgzUt5eyW97Jlm8FWPksXNmvbzf2SkfN--tZ0KDmNL2YBIogJF--uAfNfk5ICybh9PUMqWi3Gw%3D%3D; preferred_color_mode=light; tz=Asia%2FShanghai
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=4
Pragma: no-cache
Cache-Control: no-cache
```

## 执行转换脚本

```python
root@Gavin:~# cat change_header_to_json.py 
#!/usr/bin/env python

import os
import sys
import json


file_name = "./header.search"
head_json = "./header.json"


def file_check():
    if not os.path.exists(file_name):
        print(f"[ERROR]  Not find file : {file_name}, exit!!!")
        sys.exit(1)


def read_file_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


def format_header_to_json():
    header_content = read_file_content(file_name)

    # 使用字典推导式将每一行转换为键值对，分割点为第一个": "序列
    headers = {line.split(": ")[0]: line.split(": ")[1] for line in header_content.strip().split("\n") if ':' in line}

    # 将字典转换为JSON并写入文件
    with open(head_json, "w", encoding="utf-8") as json_file:
        json.dump(headers, json_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    format_header_to_json()
```


## 查看生成的json文件

```shell
root@Gavin:~# cat header.json 
{
    "Host": "github.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept": "text/html",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://github.com/tholo/pytest-flake8",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Cookie": "_octo=GH1.1.408032656.1695809589; logged_in=no; _device_id=3a906646e633cfc8d1773e1699957c29; _gh_sess=fanO9iUDx5TxUkSX%2BvsGj3aaJDwnOQ2WFv6ck7RfQCbvnZiTntz9UTdQcP7%2BMDMEvh1J%2BzSq35kY5EvV9yKzzyItORIbH9xVVLEQOcc5ooZNSp54FFfmKr4NKYX3mMGbi1K3Y%2BRKuLAu6LQfw4Du14CtVJ5JGRTTfsmXW0JzRqgA3UzAEu1Ee2LQZhOjO4E%2F3eAEteb5x6Kj7i6axGqxzfxjZK4ASCSnoyjMV%2BSaQ6KMwHKvrlzOp%2BcUgmd7ilZXzMrr7ud8r3xDlkA5UgzUt5eyW97Jlm8FWPksXNmvbzf2SkfN--tZ0KDmNL2YBIogJF--uAfNfk5ICybh9PUMqWi3Gw%3D%3D; preferred_color_mode=light; tz=Asia%2FShanghai",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=4",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}root@Gavin:~#
```

如此，直接将格式化好的文件内容放在相关代码中header调试处：

```shell
self.session.headers.update('上述header内容')
```

# 小结

上述脚本用处不大，纯粹是为了温习一下python的字典推导式和with关键字读写文件。

