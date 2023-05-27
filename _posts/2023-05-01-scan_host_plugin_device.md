---
layout:     post
title:      "快速识别热插拔硬盘"
subtitle:   "Scan host plugin disk"
date:       2023-05-01
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - shell
---

# 概述

虚拟机添加硬盘，无需重启，识别新硬盘（热插拔）

# 脚本

```
#/bin/bash
# ReScan all SCSI/SATA Hosts
for SHOST in /sys/class/scsi_host/host*; do
    echo -n "Scanning ${SHOST##*/}..."
    echo "- - -" > ${SHOST}/scan
    echo Done
done

```
