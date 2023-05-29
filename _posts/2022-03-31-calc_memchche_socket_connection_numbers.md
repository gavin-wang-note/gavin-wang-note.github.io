---
layout:     post
title:      "Get memchche socket connection numbers"
subtitle:   "Get memchche socket connection numbers"
date:       2022-03-21
author:     "Gavin"
catalog:    true
tags:
    - python
---


# Overview

Recently, during the testing process, we encountered the memory leak issue, and RD located that the number of connections established by the memcache socket was too many and could not be released normally, which led to memory leak over time.

So wrote a test script to run continuously in the cluster environment to monitor the status of the memcache socket connections.


# Script of check_con-socket_numbers.py

```
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import subprocess
from collections import defaultdict
from operator import itemgetter

command = "ss -t4pH '( dport = :memcache )'"
output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
stats = defaultdict(int)
sum = 0
for line in output.stdout.splitlines():
    process = line.split()[-1]
    if not process.startswith("users"):
        continue
    pname = process.split('"')[1]
    stats[pname] += 1
    sum += 1

print("Connections:")
for stat in sorted(stats.items(), key=itemgetter(1), reverse=True):
    print("{:>15}: {}".format(stat[0], stat[1]))

print("{:>15}: {}".format("summary", sum))
```

