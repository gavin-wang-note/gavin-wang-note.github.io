---
layout:     post
title:      "awk引用shell中变量"
subtitle:   "Awk refers to variables in the shell"
date:       2020-07-01
author:     "Gavin"
catalog:    true
tags:
    - shell
    - awk
    - ceph
---


# 概述

在网上找了一个统计pool下pg分布的脚本，拿来使用了一下，发现可以在ceph J版上执行，在L版报错，原脚本内容参考如下:

{% raw %}```
ceph pg dump | egrep -v "^[0-9]*  " | awk '
/^pg_stat/ { col=1; while($col!="up") {col++}; col++ }
/^[0-9a-f]+.[0-9a-f]+/ { match($0,/^[0-9a-f]+/); pool=substr($0, RSTART, RLENGTH); poollist[pool]=0;
up=$col; i=0; RSTART=0; RLENGTH=0; delete osds; while(match(up,/[0-9]+/)>0) { osds[++i]=substr(up,RSTART,RLENGTH); up = substr(up, RSTART+RLENGTH) }
for(i in osds) {array[osds[i],pool]++; osdlist[osds[i]];}
}
END {
printf("\n");
printf("pool :\t"); for (i in poollist) printf("%s\t",i); printf("| SUM \n");
for (i in poollist) printf("--------"); printf("-------------\n");
for (i in osdlist) { printf("osd.%i\t", i); sum=0;
for (j in poollist) { printf("%i\t", array[i,j]); sum+=array[i,j]; poollist[j]+=array[i,j] }; printf("| %i\n",sum) }
for (i in poollist) printf("--------"); printf("--------------\n");
printf("SUM :\t"); for (i in poollist) printf("%s\t",poollist[i]); printf("|\n");
}'
``` {% endraw %}

本文讲述awk如何引用shell变量，来解决上面这个脚本对我们产品的兼容问题。

# 实践

修改后的脚本参考如下:

{% raw %}```
ceph_version=`ceph -v | awk '{{print $3}}'`

if [[ ${ceph_version} =~ '10.' ]]; then
    pg_stat="pg_stat"
    up="up"
elif [[ ${ceph_version} =~ '12.' ]]; then
    pg_stat="PG_STAT"
    up="UP"
fi

ceph pg dump | egrep -v "^[0-9]*  " | awk '
/^'$pg_stat'/ { col=1; while($col!="'"$up"'") {col++}; col++ }
/^[0-9a-f]+.[0-9a-f]+/ { match($0,/^[0-9a-f]+/); pool=substr($0, RSTART, RLENGTH); poollist[pool]=0;
up=$col; i=0; RSTART=0; RLENGTH=0; delete osds; while(match(up,/[0-9]+/)>0) { osds[++i]=substr(up,RSTART,RLENGTH); up = substr(up, RSTART+RLENGTH) }
for(i in osds) {array[osds[i],pool]++; osdlist[osds[i]];}
}
END {
printf("\n");
printf("pool :\t"); for (i in poollist) printf("%s\t",i); printf("| SUM \n");
for (i in poollist) printf("--------"); printf("-------------\n");
for (i in osdlist) { printf("osd.%i\t", i); sum=0;
for (j in poollist) { printf("%i\t", array[i,j]); sum+=array[i,j]; poollist[j]+=array[i,j] }; printf("| %i\n",sum) }
for (i in poollist) printf("--------"); printf("--------------\n");
printf("SUM :\t"); for (i in poollist) printf("%s\t",poollist[i]); printf("|\n");
}'
``` {% endraw %}


# awk引用shell中变量

## 方法1： {% raw %}```"'$var'" ``` {% endraw %}

这种写法大家无需改变用'括起awk程序的习惯,是老外常用的写法.如:

{% raw %}```
var="test"

awk 'BEGIN{print "'$var'"}'
``` {% endraw %}

这种写法其实就是把一对单引号分成了两段单引号，中间的shell变量直接按照shell变量的引用方式即可，但是如果var中含空格,为了shell不把空格作为分格符,便应该如下使用:

{% raw %}```
var="thisis a test"

awk 'BEGIN{print "'"$var"'"}'    （也就是在shell变量的两边加上一对双引号即可）
``` {% endraw %}

## 方法2：export变量

使用ENVIRON["var"]形式, (ENVIRON为awk中的内置环境变量数组)

如:                                                                     

{% raw %}```
var="thisis a test";export $var

awk 'BEGIN{print ENVIRON["var"]}'
``` {% endraw %}

## 方法3：使用-v选项

如:

{% raw %}```
var="thisis a test"

awk –v nvar="$var"  'BEGIN{print nvar}'
``` {% endraw %}

这样便把系统变量定义成了awk变量.

如果在awk是这种格式的话 ``` awk  'script'  filename ``` 也可以这样引用shell变量

{% raw %}```
awk 'script' awkvar="shellvar" filename

awk 'END{print awkvar}' awkvar="$shellvar" filename
``` {% endraw %}



# 还有一个python版本

参考如下:

{% raw %}```
#!/usr/bin/env  python
import sys 
import os
import json

ceph_version_cmd = "ceph -v | awk '{{print $3}}'"
_vers = os.popen(ceph_version_cmd).read()
if '10.' in _vers:
    cmd = '''
ceph pg dump | awk ' /^pg_stat/ { col=1; while($col!="up") {col++}; col++ } /^[0-9a-f]+\.[0-9a-f]+/ {print $1,$col}'
'''
elif '12.' in _vers:
    cmd = '''
ceph pg dump | awk ' /^PG_STAT/ { col=1; while($col!="UP") {col++}; col++ } /^[0-9a-f]+\.[0-9a-f]+/ {print $1,$col}'
'''

body = os.popen(cmd).read()
SUM = {}
for line in  body.split('\n'):
   if not line.strip():
     continue
   SUM[line.split()[0]] = json.loads(line.split()[1])
pool = set()
for  key in  SUM:
  pool.add(key.split('.')[0])
mapping = {}
for number in pool:
  for k,v in SUM.items():
    if k.split('.')[0] == number:
       if number in mapping:
           mapping[number] += v
       else:
           mapping[number] = v
MSG = """%(pool)-6s: %(pools)s | SUM
%(line)s
%(dy)s
%(line)s
%(sun)-6s: %(end)s |"""
pools = " ".join(['%(a)-6s' % {"a": x} for x in sorted(list(mapping))])
line = len(pools) + 20
MA = {}
OSD = []
for p in mapping:
    osd = sorted(list(set(mapping[p])))
    OSD += osd
    count = sum([mapping[p].count(x) for x in osd])
    osds = {}
    for x in osd:
        osds[x] = mapping[p].count(x)
    MA[p] = {"osd": osds, "count": count}
MA = sorted(MA.items(), key=lambda x:x[0])
OSD = sorted(list(set(OSD)))
DY = ""
for osd in OSD:
    count = sum([x[1]["osd"].get(osd,0) for x in MA])
    w = ["%(x)-6s" % {"x": x[1]["osd"].get(osd,0)} for x in MA]
    #print w
    w.append("| %(x)-6s" % {"x": count})
    DY += 'osd.%(osd)-3s %(osds)s\n' % {"osd": osd, "osds": " ".join(w)}
SUM = " ".join(["%(x)-6s" % {"x": x[1]["count"]} for x in MA])
msg = {"pool": "pool", "pools": pools, "line": "-" * line, "dy": DY, "end": SUM, "sun": "SUM"}
print MSG % msg
``` {% endraw %}
