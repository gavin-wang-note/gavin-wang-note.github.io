---
layout:     post
title:      "给nose写一个类似Robot Framework的Wait Until Keyword Succeeds"
subtitle:   "Write a function same as `Wait Until Keyword Succeeds` in Robot Framework for nose"
date:       2018-06-18
author:     "Gavin Wang"
catalog:    true
categories:
    - [Automation]
    - [nose]
tags:
    - nose
    - Automation
---


# 前言

由于产品是异步请求，往往一个request下去，只是将某些信息写入到了KVStore中，之后由daemon读取KVStore进行判断是否有发生变化，如果有变化，daemon才采取行动。这里在写自动化校验设置是否apply下去，以及apply下去后是否有生效，就不能靠time.sleep来做了，主要问题是：

* 不确定要等待多久，等待久了，感觉是浪费时间，尤其用例很多的情况下，严重影响了用例的整体执行时间；等待短了，又没有成功的apply下去，或者apply下去了但还没有具体生效

鉴于此，就需要有一个类似于Robot Framework的```Wait Until Keyword Succeeds ```功能.

# 实践

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


from __future__ import unicode_literals

import time

from common.config import GetConfig as config

retry_interval = config.retry_interval
retry_timeout = config.retry_timeout


def assert_check(func):
    """
    :param func, string, a function name
    """
    @wraps(func)
    def inner(param, *args, **kwargs):
        """
        :param param, string, a parameter
        """
        for i in xrange(int(retry_timeout)):
            try:
                func(param, *args, **kwargs)
                break
            except Exception as ex:
                logging.warn("[WARN]  Not match, %s time(s) to retry, "
                             "exception is : (%s) : (%s)", (i + 1), ex.__str__, unicode(ex))
                logging.warn("[WARN]  In file (%s) of function (%s), "
                             "at line (%s)", func.func_code.co_filename,
                             func.func_name,
                             func.func_code.co_firstlineno)
                time.sleep(int(retry_interval))
                continue
        else:
            logging.info("[ERROR]  Retry timeout or AssertionError")
            # raise AssertionError('[RetryTimeOut] Failure expected, retry timeout')
            # Deliberately doing this, this will mark the use case status as failed,
            # otherwise it will affect the normal output of the html report (the entire html content is empty)
            eq_(1, 2, "[RetryTimeOut] Failure expected, retry timeout")

    return inner

```

这里是一个示例的片段，通过装饰器，在调用check函数之前，引用这个装饰器，从而达到间隔一定时间（retry_timeout）、执行一定次数（retry_interval）来实现类似RF```Wait Until Keyword Succeeds ```的功能

对应测试用例基类的检查操作示例如下：

```python
    @assert_check
    def check_snapshot(self, gateway_group, target_id, iscsi_id, snap_name, op_type):
        """
        Check snapshot created or delete result
        :param gateway_group, string, a gateway group name
        :param target_id, string, a target name
        :param iscsi_id, string, a volume name
        :param snap_name, string, a snapshot name for a iSCSI volume
        :param op_type, string, del or add
        """

        if op_type == 'add':
            logging.info("[Check]    Check snapshot created result")
        elif op_type == 'del':
            logging.info("[Check]    Check snapshot deleted result")

        info = get_volume_info(gateway_group, target_id, iscsi_id, translate_pool_id=True)
        pool = info['pool']
        image_name = info['rbd_img']

        rbd_res = do_cmd("rbd -p {} snap ls {}".format(pool, image_name), 30, True).strip()
        if op_type == 'add':
            assert_in(snap_name, rbd_res, "[ERROR]  Not found : ({}) in "
                                          "rbd_res : ({})".format(snap_name, rbd_res))
            logging.info("[Success]  Create snapshot : (%s) success", snap_name)
        elif op_type == 'del':
            assert_not_in(snap_name, rbd_res, "[ERROR]  Still found : ({}) in "
                                              "rbd_res : ({})".format(snap_name, rbd_res))
            logging.info("[Success]  Delete snapshot : (%s) success", snap_name)

```
