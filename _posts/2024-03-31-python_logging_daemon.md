---
title: python logging的一个daemon
date: 2024-03-31 11:43:00
author: Gavin Wang
img:
top: false
hide: false 
cover: false
coverImg:
password:
toc: true 
mathjax: false
summary: 简单示例一个python的logging模块示例
categories:
    - [python]
tags:
    - python
---


# 概述

使用了这么多年的pytest了，过往的每个Project一直都有在记录整个Automation运行过程log信息。pytest集成了python的logging模块，使用起来更方便一些。
今天闲来无事，看到个图形，想把它记录到log中，故而单独使用python的logging模块小试一下。


# python logging模块简介


## 日志级别

Python 标准库 logging 用作记录日志，默认分为六种日志级别（括号为级别对应的数值）：
* NOTSET（0）
* DEBUG（10）
* INFO（20）
* WARNING（30）
* ERROR（40）
* CRITICAL（50）

logging 执行时输出大于等于设置的日志级别的日志信息，如设置日志级别是 INFO，则 INFO、WARNING、ERROR、CRITICAL 级别的日志都会输出。


## logging流程


* Logger：日志，暴露函数给应用程序，基于日志记录器和过滤器级别决定哪些日志有效。
* LogRecord ：日志记录器，将日志传到相应的处理器处理。
* Handler ：处理器, 将(日志记录器产生的)日志记录发送至合适的目的地。
* Filter ：过滤器, 提供了更好的粒度控制,它可以决定输出哪些日志记录。
* Formatter：格式化器, 指明了最终输出中日志记录的布局。


<p><img class="shadow" src="/img/in-post/python_logging_flow.png" width="1200" /></p>


说明：

* 判断 Logger 对象执行方法（如图中的 info()）时对于设置的级别是否可用，如果可用，则往下执行，否则，流程结束。
* 创建 LogRecord 对象，如果注册到 Logger 对象中的 Filter 对象过滤后返回 False，则不记录日志，流程结束，否则，则向下执行。
* LogRecord 对象将 Handler 对象传入当前的 Logger 对象，（图中的子流程）如果 Handler 对象的日志级别大于设置的日志级别，再判断注册到 Handler 对象中的 Filter 对象过滤后是否返回 True 而放行输出日志信息，否则不放行，流程结束。
* 如果传入的 Handler 大于 Logger 中设置的级别，也即 Handler 有效，则往下执行，否则，流程结束。
* 判断这个 Logger 对象是否还有父 Logger 对象，如果没有（代表当前 Logger 对象是最顶层的 Logger 对象 root Logger），流程结束。否则将 Logger 对象设置为它的父 Logger 对象，重复上面的 3、4 两步，输出父类 Logger 对象中的日志输出，直到是 root Logger 为止。


## 日志输出格式

日志的输出格式可以使用设置，默认格式为下图所示。

* WARNING:日志级别
* root:Logger实例名称
* warn message:日志消息内容


# 代码示例

```python
import logging
from logging.handlers import TimedRotatingFileHandler

class CustomLogger:
    _handlers_checked = set()

    def __init__(self, logger_name='sampleLogger', log_file='app.log', level=logging.INFO, console_output=False):
        self.logger_name = logger_name
        if logger_name not in CustomLogger._handlers_checked:
            self._setup_logger(log_file, level, console_output)
            CustomLogger._handlers_checked.add(logger_name)

    def _setup_logger(self, log_file, level, console_output):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(level)
        logger.propagate = False

        # Setup the file handler.
        file_handler = TimedRotatingFileHandler(
            log_file, when='D', interval=1, backupCount=5, encoding='utf-8'
        )
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter('[%(asctime)s]-[%(name)s:%(lineno)d]-[%(levelname)-8s]-%(message)s'))
        logger.addHandler(file_handler)

        # Conditional setup for the console handler.
        if console_output:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(logging.Formatter('[%(asctime)s]-[%(name)s:%(lineno)d]-[%(levelname)-8s]-%(message)s'))
            logger.addHandler(stream_handler)

        self.logger = logger

    def log(self, msg, level='info'):
        getattr(self.logger, level)(msg)

# Usage example:
log_filename = 'my_application.log'
log_level = logging.INFO
console_output = False

my_logger = CustomLogger(log_file=log_filename, level=log_level, console_output=console_output)
my_logger.log('这是一条信息日志。', 'info')
my_logger.log('这是一条警告日志。', 'warning')
my_logger.log(r"""

                                                              _ooOoo_
                                                             o8888888o
                                                             88" . "88
                                                             (| -_- |)
                                                              O\ = /O
                                                          ____/`---'\____
                                                        .   ' \\| |// `.
                                                         / \\||| : |||// \
                                                       / _||||| -:- |||||- \
                                                         | | \\\ - /// | |
                                                       | \_| ''\---/'' | |
                                                        \ .-\__ `-` ___/-. /
                                                     ___`. .' /--.--\ `. . __
                                                  ."" '< `.___\_<|>_/___.' >'"".
                                                 | | : `- \`.;`\ _ /`;.`/ - ` : | |
                                                   \ \ `-. \_ __\ /__ _/ .-` / /
                                           ======`-.____`-.___\_____/___.-`____.-'======
                                                              `=---='

                                           .............................................
                                                  佛祖保佑             永无BUG
                                           .............................................
""")
```

日志效果参考如下：

```shell
[2024-03-31 11:46:29,741]-[sampleLogger:37]-[INFO    ]-这是一条信息日志。
[2024-03-31 11:46:29,741]-[sampleLogger:37]-[WARNING ]-这是一条警告日志。
[2024-03-31 11:46:29,741]-[sampleLogger:37]-[INFO    ]-
                                                              _ooOoo_
                                                             o8888888o
                                                             88" . "88
                                                             (| -_- |)
                                                              O\ = /O
                                                          ____/`---'\____
                                                        .   ' \\| |// `.
                                                         / \\||| : |||// \
                                                       / _||||| -:- |||||- \
                                                         | | \\\ - /// | |
                                                       | \_| ''\---/'' | |
                                                        \ .-\__ `-` ___/-. /
                                                     ___`. .' /--.--\ `. . __
                                                  ."" '< `.___\_<|>_/___.' >'"".
                                                 | | : `- \`.;`\ _ /`;.`/ - ` : | |
                                                   \ \ `-. \_ __\ /__ _/ .-` / /
                                           ======`-.____`-.___\_____/___.-`____.-'======
                                                              `=---='

                                           .............................................
                                                  佛祖保佑             永无BUG
                                           .............................................
```

