---
layout:     post
title:      "Slow to open CIFS"
subtitle:   "Slow to open CIFS"
date:       2016-04-21
author:     "Gavin"
catalog:    true
tags:
    - python
---

# Overview

I encountered a scenario where the client feedback that the client side is slow to open CIFS, write a script to verify it.


# Script of monitor_cifs_open_time.py

```
#!/usr/bin/env python
# -*- coding:UTF-8  -*-

import time
import subprocess
from datetime import datetime


def cost_time():

    start_time = time.time()
    p = subprocess.Popen('ls -l /mnt/windows_cifs', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in p.stdout.readlines():

        if 'total' in line:
            #print line
            end_time= time.time()
            cost_time = end_time - start_time
            print '[{}] cost_time {}'.format(datetime.now(), cost_time)

            break

    time.sleep(10)


if __name__ == '__main__':
    for i in xrange(1000):
        cost_time()
```
