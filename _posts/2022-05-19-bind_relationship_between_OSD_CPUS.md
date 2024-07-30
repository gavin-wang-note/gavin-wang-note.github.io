---
layout:     post
title:      "获取OSD与CPU绑定关系"
subtitle:   "bind relationship between OSD and CPUS"
date:       2022-05-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [ceph]
tags:
    - ceph
---


# 代码


这里代码转自(https://blog.51cto.com/zphj1987/3212869)，在它基础上增加了+号的颜色显示(高亮)，表明当前ceph-osd运行在对应On-line CPU(s)上.


## CPU信息

```shell
[root@node163 ~]# lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                48
On-line CPU(s) list:   0-47
Thread(s) per core:    2
Core(s) per socket:    12
Socket(s):             2
NUMA node(s):          2
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 85
Model name:            Intel(R) Xeon(R) Gold 5118 CPU @ 2.30GHz
Stepping:              4
CPU MHz:               2244.518
BogoMIPS:              4600.00
Virtualization:        VT-x
L1d cache:             32K
L1i cache:             32K
L2 cache:              1024K
L3 cache:              16896K
NUMA node0 CPU(s):     0-11,24-35
NUMA node1 CPU(s):     12-23,36-47
Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb cat_l3 cdp_l3 invpcid_single pti intel_ppin ssbd mba ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx smap clflushopt clwb intel_pt avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts pku ospke md_clear flush_l1d
```

代码块

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import json
import psutil
import commands
from prettytable import PrettyTable

def main():
    if len(sys.argv) == 1:
        printosdcputable("process")
    elif sys.argv[1] == 't':
        printosdcputable("thread")

def printosdcputable(choose):
    print choose
    row = PrettyTable()
    row.header = True
    cpulist = ["OSD\CPU"]
    corelist=["Core ID"]
    phylist = ["Physical ID"]
    emplist=["-----------"]
    for cpupro in range(psutil.cpu_count()):
        cpulist.append("%s" %cpupro )

        coreid=commands.getoutput('egrep \'processor|physical id|core id\' /proc/cpuinfo | cut -d : -f 2 | paste - - -  | awk  \'$1==%s {print $3 }\'' %cpupro)
        corelist.append("%s" %coreid)

        phyid = commands.getoutput('egrep \'processor|physical id|core id\' /proc/cpuinfo | cut -d : -f 2 | paste - - -  | awk  \'$1==%s {print $2 }\'' % cpupro)
        phylist.append("%s" %phyid)
        emplist.append("--")

    row.field_names = cpulist
    row.add_row(corelist)
    row.add_row(phylist)
    row.add_row(emplist)

    for root, dirs, files in os.walk('/var/run/ceph/'):
        for name in files:
            if "osd"  in name and "pid" in name :
                osdlist = []
                osdthlist=[]
                for osdcpu in range(psutil.cpu_count()):
                    osdlist.append(" ")
                    osdthlist.append("0")
                pidfile=root + name
                osdid=commands.getoutput('ls  %s|cut -d "." -f 2 2>/dev/null'  %pidfile )
                osdpid = commands.getoutput('cat %s  2>/dev/null' %pidfile)
                osd_runcpu = commands.getoutput('ps -o  psr -p %s |grep -v PSR 2>/dev/null' %osdpid)
                th_list = commands.getoutput('ps -o  psr -L  -p %s |grep -v PSR|awk \'gsub(/^ *| *$/,"")\'  2>/dev/null' % osdpid)

                osdname="osd."+osdid
                osdlist[int(osd_runcpu)]="\033[31m+\033[0m"
                for osdth in th_list.split('\n'):
                    osdthlist[int(osdth)] = int(osdthlist[int(osdth)])+1
                osdlist.insert(0,osdname)
                osdthlist.insert(0,osdname)
                if choose == "process":
                    row.add_row(osdlist)
                elif choose == "thread":
                    row.add_row(osdthlist)
    print row

if __name__ == '__main__':
    main()
```



# 运行结果

<img class="shadow" src="/img/in-post/osd_cpu_bind_relationship.png" width="1200">
