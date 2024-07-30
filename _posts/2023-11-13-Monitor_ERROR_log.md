---
layout:     post
title:      "python监听日志变化"
subtitle:   "Monitor Log Changes"
date:       2023-11-13
author:     "Gavin Wang"
catalog:    true
summary: 借助python监听产品异常日志，方便测试过程中及时捕获异常操作日志，避免遗漏
categories:
    - [python]
tags:
    - python
---


# 概述

测试过程中需要监控多个日志内容，防止有异常信息在测试过程中被错过，于是构思了这支Script，用于监控给定的Log，当发现list kws中定义的关键字时，自动发送钉钉告警到群组。


# 代码示例

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import time
import argparse
import requests


parser = argparse.ArgumentParser(description='Monitor exception from log files')
parser.add_argument("file_full_path", type=str)
args = parser.parse_args()


def send_notification(content):
    url = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx"
    data = {
        "msgtype": "text",
        "text": {
            "content": "监控报警: 在[{}]中发现异常日志：[{}]".format(args.file_full_path, content)
         }
    }

    res = requests.post(url, json=data)


def follow(file_handler):
    file_handler.seek(0, 2)
    while True:
        line = file_handler.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line



if __name__  == '__main__':
    kws = ["ERROR", "exception =", "INFO", "DEBUG"]  # Level of INFO and DEBUG, just for debug the script

    print("Monitor log : {}".format(args.file_full_path))
    with open(args.file_full_path, "r") as log_file:
        log_lines = follow(log_file)
        for line in log_lines:
            if (any(kw in line for kw in kws)):
                # print(line)
                send_notification(content)
```



执行过程示例如下：

```shell
[qatest@iZbp1fl8ef9wkdizi6soq1Z ~]$ python monitor_debug_log.py "/mnt/logs/marketingservice/debug.log"
/usr/lib/python2.7/site-packages/requests/__init__.py:91: RequestsDependencyWarning: urllib3 (1.25.3) or chardet (2.2.1) doesn't match a supported version!
  RequestsDependencyWarning)
Monitor log : /mnt/logs/marketingservice/debug.log

```
