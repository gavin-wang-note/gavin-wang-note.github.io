---
layout:     post
title:      "fio 校验文件写完整性"
subtitle:   "fio verify"
date:       2023-06-07
author:     "Gavin"
catalog:    true
tags:
    - ceph
    - python
    - fio
---



# 概述

今天在整理电脑，发现了之前写的一个利用fio，模拟ceph集群发生OSD Down、UP期间，数据写入内容准确性校验，是否存在业务持续写入过程中，ceph集群发生异常，引发数据丢失的可能。


# 实践


脚本分为三部分，一部分是fio写，一部分是 restart ceph-osd，最后一部分是校验fio写文件内容准确性。


```
run_fio.py
restart_osd.py
check_fio.py
```


## run_fio.py

```
import time

from ezs3.command import do_cmd


fio_cmd = "fio --name=verify --rw=write --bssplit=128k/30:256k/30:512k/20:1m/20 --size=100G --numjobs=32 --ioengine=libaio --iodepth=16 --direct=1 --group_reporting --verify=md5 --filename=/dev/rbd0 --loops=1000"

for i in xrange(100):
    print "------- {} times to run fio  -------".format(i)
    do_cmd(fio_cmd)
    time.sleep(15)
```


## restart_osd.py


```
import time
import random

import logging
from ezs3.log import EZLog

from ezs3.cluster import ClusterManager
from ezs3.command import do_cmd

EZLog.init_handler(logging.INFO, "/root/osd_random_restart.log")
logger = EZLog.get_logger("restart_osd")


def get_osd_id_ip_map():
    """  Get all of OSD id  """
    osd_id_ip_map = {}
    all_osds_set = ClusterManager().get_osds()[-1]
    
    for key in all_osds_set:
        osd_id_ip_map[key.id] = key.ip

    logger.info("Get all of OSD id and ip mapping information : (%s)", osd_id_ip_map)
    return osd_id_ip_map


def get_osd_id(osd_id_ip_map):
    """  Get a OSD id by random  """
    slice_list = random.sample(osd_id_ip_map.keys(), 1)
    osd_id = slice_list[0]
    ip = osd_id_ip_map[osd_id]

    return osd_id, ip


def restart_osd(osd_id_ip_map, sleep_time=None):
    """  Restart the OSD  """
    sleep_time = 1800 if sleep_time is None else sleep_time

    for i in xrange(100):
        osd_id_ip_info = get_osd_id(osd_id_ip_map)
        osd_id = osd_id_ip_info[0]
        ip = osd_id_ip_info[1]

        logger.info("Will restart OSD : (%s), then sleep : (%s)", osd_id, sleep_time)
        cmd = "ssh {} /etc/init.d/ceph restart osd.{}".format(ip, osd_id)
        logger.info("Restart osd cmd is : (%s)", cmd)
        do_cmd(cmd, 300)
        time.sleep(sleep_time)


if __name__ == "__main__":
    all_osds = get_osd_id_ip_map()
    restart_osd(all_osds)
```


## check_fio.py

```
import sys
import time
import logging

from ezs3.log import EZLog
from ezs3.command import do_cmd

EZLog.init_handler(logging.INFO, "/root/read_check.log")
logger = EZLog.get_logger("check_fio")

fio_cmd = "fio --name=verify --rw=read --bssplit=128k/30:256k/30:512k/20:1m/20 --size=100G --numjobs=32 --ioengine=libaio --iodepth=16 --direct=1 --group_reporting --verify=md5 --filename=/dev/rbd0 > /root/fio_output.txt"


def fio_read_verify(sleep_time=None):
    """  FIO read verify  """
    sleep_time = 600 if sleep_time is None else sleep_time

    for i in xrange(10000):
        do_cmd(fio_cmd)
        fio_output = do_cmd("cat /root/fio_output.txt | grep 'err='", 60).strip()
        err = fio_output.split("err=")[1].split()[0]
        print("--  err is : ({})".format(err))
        if int(err) > 0:
            logger.error("[ERROR]  Find error in fio result when read verify")
            sys.exit(0)
        else:
            logger.info("Continue to sleep : (%s)", sleep_time)
            time.sleep(sleep_time)


if __name__ == "__main__":
    fio_read_verify()

```

