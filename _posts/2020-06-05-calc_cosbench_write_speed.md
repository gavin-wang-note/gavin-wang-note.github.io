---
layout:     post
title:      "统计cosbench写速度"
subtitle:   "Statistics cosbech write speed"
date:       2020-06-05
author:     "Gavin"
catalog:    true
tags:
    - cosbench
    - shell
    - python
---


# 概述

BTW，今天是24节气的芒种，因新型冠状病毒疫情影响，高考延后了1个月。

言归正传，测试任务要求如下：

需要知道当前集群，单一bucket中，存放1000万object，存放2000万object，存放3000万object，。。。。一直到存放110million个object，即每间隔存放1000万笔记录情况下，RGW性能是否伴随单一bucket中object数量的增加，写性能存在下降状况?

最初我测试的时候，是组织了11个xml文件，每个xml文件中总共写1000万笔，单笔object大小10K，在cosbench web界面上提交11个任务，这样综合起来就是110million的object了，测试效果统计RGW写速度如下：

<img class="shadow" src="/img/in-post/rgw_write_speed_v7.0_1.png" width="1200">

参数调整后效果:

<img class="shadow" src="/img/in-post/rgw_write_speed_v7.0_2.png" width="1200">

环境信息与说明：
  
3节点集群，每个节点4块8T盘组RAID5（64K srip size），每个节点8组RAID5；
每个节点有2块3.5T NVME SSD，和2块480G intel 4600 SSD

带NVME的，比如2+1 EC 3.5TNVME，表示使用每个2块3.5T的NVME作为OSD journal&cache， intel 480G 4600独立组成OSD，作为S3 index pool；

不带NVME，比如2Replicate 480G SSD，表示没有使用NVME设备，使用480G SSD作为OSD journal&cache，这个场景更贴合当前客户实施要求的硬件配置

图中的X坐标，每一千万个object采样一次获取的OPS值，从0到1.1亿，采样11个点

上述测试结果，是在7.0版本测试验证，发现7.0版本的性能，同场景下远高于8.0版本的，所以就交由Henry大神进行RGW性能调优，后来他使用shell写了支script，实现自动提交cosbench任务，比我的土方法方便多了，这里抄袭一下他的输出贴出来：


目录结构如下:

```
root@node244:~/henry# ll
total 20
drwxr-xr-x  2 root root 4096 Jun  4 16:16 ./
drwx------ 13 root root 4096 Jun  4 15:35 ../
-rwxr-xr-x  1 root root  825 Jun  4 09:55 cosbench.sh*
-rw-r--r--  1 root root 1878 Jun  4 09:51 roundN_10K_10Mfiles_Write.xml.in
-rw-r--r--  1 root root 1913 Jun  4 15:30 workload.xml
root@node244:~/henry# 
```


roundN_10K_10Mfiles_Write.xml.in 文件内容参考如下:

```
root@node244:~/henry# cat roundN_10K_10Mfiles_Write.xml.in 
<?xml version="1.0" encoding="UTF-8"?>
<workload name="HM_round@@@ROUND@@@_10M_files_write_once" description="HM_round@@@ROUND@@@_10M_files_write_once">
<storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_1@@@/" />

  <workflow>
		<!-- ******************************* -->
  	<!-- 1mch 20wrks 60threads write job -->
		<!-- ******************************* -->

    <workstage name="10K-40wrks-write-init">
        <work name="10mch-40wrks-160threads-write-init" type="init" workers="1" interval="10" division="container" runtime="0" rampup="0" rampdown="0" driver="driver1"  config="cprefix=tmo;containers=r(1,1)" />
    </workstage>

    <workstage name="10K-40wrks-write-WRITEJOB">
        <work name="write1" type="write" workers="40" interval="10" division="object" totalOps="350000" rampup="0" rampdown="0" driver="driver1">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_1@@@/" />
            <operation type="write" ratio="100" division="object" config="cprefix=tmo;oprefix=round@@@ROUND@@@_10KB_;containers=s(1,1);objects=r(1,350000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write2" type="write" workers="40" interval="10" division="object" totalOps="350000" rampup="0" rampdown="0" driver="driver1">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_2@@@/" />
            <operation type="write" ratio="100" division="object" config="cprefix=tmo;oprefix=round@@@ROUND@@@_10KB_;containers=s(1,1);objects=r(350001,700000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
        <work name="write3" type="write" workers="40" interval="10" division="object" totalOps="300000" rampup="0" rampdown="0" driver="driver1">
            <auth type="none" config="" />
            <storage type="s3" config="accesskey=@@@ACCESS_KEY@@@;secretkey=@@@SECRET_KEY@@@;endpoint=http://@@@ENDPOINT_3@@@/" />
            <operation type="write" ratio="100" division="object" config="cprefix=tmo;oprefix=round@@@ROUND@@@_10KB_;containers=s(1,1);objects=r(700001,1000000);sizes=c(10240)B;createContainer=false;" id="none" />
        </work>
    </workstage>

	</workflow>
</workload>

root@node244:~/henry#
```

说明:

这里要注意一下xml文档中的 'workload name="HM_round@@@ROUND@@@_10M_files_write_once"'，此处的workload name对应的内容，一定不能含有空格，因为后面有个shell脚本去cat archive里面的内容，脚本并没有对空格目录做转移处理，建议规避一下，避免使用空格。


cosbench.sh内容如下:

```
root@node244:~/henry# cat cosbench.sh
#!/bin/bash

INFILE=roundN_10K_10Mfiles_Write.xml.in
CLI=/root/0.4.2.c4/cli.sh
EP1=1.6.17.246
EP2=1.6.17.247
EP3=1.6.17.248
ACCESS_KEY=BHP0VGIGL5TGU1I82S9H
SECRET_KEY=Q5o9c2haivMQeKLiAbBOzKrF7Nfqu0gbInKT1xWL

ssh root@${EP1} ceph status
ssh root@${EP1} ceph df
for round in {1..100}
do
    while (( $(${CLI} info |& grep PROCESSING | wc -l) >= 1 )); do
        echo "[WARN]  Has more than one cosbench task in running status, sleep 60s"
        sleep 60
    done

    sed "s/@@@ROUND@@@/${round}/g" ${INFILE} | \
    sed "s/@@@ENDPOINT_1@@@/${EP1}/g" | \
    sed "s/@@@ENDPOINT_2@@@/${EP2}/g" | \
    sed "s/@@@ENDPOINT_3@@@/${EP3}/g" | \
    sed "s/@@@ACCESS_KEY@@@/${ACCESS_KEY}/g" | \
    sed "s/@@@SECRET_KEY@@@/${SECRET_KEY}/g" > workload.xml
    ${CLI} submit workload.xml
    date
    sleep 60

    while (( $(${CLI} info |& grep PROCESSING | wc -l) >= 1 )); do
        echo "[WARN]  Has more than one cosbench task in running status, sleep 60s"
        sleep 60
    done

    ssh root@${EP1} ceph status
    ssh root@${EP1} ceph df
done

root@node244:~/henry#
```

# 统计cosbench写速度


终于到本文主题了，既然有了上面的测试script方便QA提交测试任务，那统计RGW写速度，以前写了一个python来统计，不是很通用，因为import了产品的function，一旦脱离产品环境运行cosbench，python脚本就没法执行了，今天重写了个统计cosbench写速度的shell脚本，内容如下：


{% raw %}```
root@node244:~# cat calc_cosbench_speed.sh 
#!/bin/bash

ARCHIVE=/root/0.4.2.c4/archive/
HISTORY=run-history.csv

HISTORY_FILE=${ARCHIVE}${HISTORY}

if [ ! -f ${HISTORY_FILE} ]; then
  echo ""
  echo -e "\033[31m [ERROR]  !!! Not find file : ${HISTORY_FILE} \033[0m"
  echo ""
  exit 1
fi

while read line
do
    # echo $line
    if [[ x"$line" =~ x"Id" ]]; then
        continue
    else
        task_id=`echo $line | awk -F"," '{{print $1}}'`
        task_name=`echo $line | awk -F"," '{{print $2}}'`
        TASK_STATUS=`echo $line | awk -F"," '{{print $7}}'`
        work_dir=${ARCHIVE}${task_id}-${task_name}

        # echo ${task_id}, ${task_name}, ${TASK_STATUS}, ${work_dir}

        if [[ -d ${work_dir} ]]; then
            if [[ x"${TASK_STATUS}" == x"finished" ]]; then
                TOTAL_OBJS=`cat ${work_dir}/driver*.csv | grep write | grep -v init | awk -F',' '{{print $3}}' | awk '{sum += $1};END {print sum}'`
                # echo ${TOTAL_OBJS}

                START_TIME=`echo $line | awk -F"," '{{print $4}}'`
                END_TIME=`echo $line | awk -F"," '{{print $5}}'`
                START_TIME_STR=`date -d "${START_TIME}" +%s`
                END_TIME_STR=`date -d "${END_TIME}" +%s`
                COST_TIME=`expr ${END_TIME_STR} - ${START_TIME_STR}`
                # echo ${COST_TIME}
                WRITE_SPEED=`echo | awk "{print (${TOTAL_OBJS} / ${COST_TIME})}"`

                echo ""
                echo -e "\033[32m   Task : (${task_id}-${task_name}), write total objects : (${TOTAL_OBJS}), cost time : (${COST_TIME}(s)), write speed : (${WRITE_SPEED}) \033[0m"
                echo ""
            else
                echo -e "\033[33m   [WARN]  Task : (${task_id}-${task_name}) status is not finished, but : (${TASK_STATUS}), please pay more attention!!! \033[0m"
                echo ""
            fi
        else
            echo -e "\033[31m [ERROR]   !!! Not find cosbench archive folder : ${work_dir}  \033[0m"
            exit 1
        fi
    fi
done < ${HISTORY_FILE}
``` {% endraw %}

执行效果如下:

<img class="shadow" src="/img/in-post/calc_cosbench_speed_output.png" width="1200">


# python脚本

今天（2020-06-18）使用python改写了一版，参考如下:


{% raw %}```
root@node244:~/75# cat calc_cosbench_speed.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from __future__ import unicode_literals

import os
import sys
import time


ARCHIVE_PATH = "/root/0.4.2.c4/archive"
HISTORY = "run-history.csv"

HISTORY_FILE = ARCHIVE_PATH + os.sep + HISTORY

if not os.path.exists(HISTORY_FILE):
    print("\033[31m \n  [ERROR]  Not find path for : ({}) \033[0m \n".format(HISTORY_FILE))
    sys.exit(1)

his_content = os.popen("cat {}".format(HISTORY_FILE)).read()
for each_line in his_content.strip().split("\n"):
    if each_line.startswith("Id"):
        continue

    try:
        line_list = each_line.split(',')
        task_id = line_list[0]
        task_name = line_list[1]
        task_state = line_list[6].strip()

        if task_state == 'finished':
            work_dir = "{}/{}-{}".format(ARCHIVE_PATH, task_id, task_name)
            start_time = line_list[3]
            end_time = line_list[4]

            start_time_array = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time_array = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_times_tamp = time.mktime(start_time_array)
            end_times_tamp = time.mktime(end_time_array)
            time_diff = end_times_tamp - start_times_tamp

            total_objs_cmd = "cat {}/driver*.csv | grep write | grep -v init " \
                             "| awk -F',' '{{print $3}}'".format(work_dir)
            count_str = os.popen(total_objs_cmd).read().strip()
            couts_str_list = count_str.split("\n")
            couts_str_int = map(int, couts_str_list)
            total_objs = sum(couts_str_int)

            write_speed = total_objs / time_diff

            print("\033[32m  Task : ({}-{}), total: ({}), elapsed : ({}s), "
                  "speed : ({}) \033[0m\n".format(task_id, task_name, total_objs, time_diff, write_speed))
        else:
            print("\033[33m  [WARN]  Task : ({}-{}) status is not finished, but : ({}), "
                  "please pay more attention \033[0m\n".format(task_id, task_name, task_state))

    except Exception as ex:
        print("\n\033[31m \n  [ERROR]  Parase file of '{}' "
              "exception : ({}) \033[0m\n".format(HISTORY_FILE, str(ex)))
        sys.exit(1)


if __name__ == "__main__":
    pass

``` {% endraw %}

执行效果如下:

<img class="shadow" src="/img/in-post/calc_cosbench_speed_output_py.png" width="1200">



# 改进

(2020-06-28)在使用过程中，碰到两个问题：

由于cosnbench controller log level默认是INFO，导致运行cosbench这台机器根分区空间满，引发cosbench任务卡住，不得不清理空间，三处了mission log信息，引发archive中run-history.csv文件内容有缺失，即少了某个/某些任务，导致统计脚本异常，没法继续统计后续存在的任务了

修改后的脚本内容如下：

{% raw %}```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from __future__ import unicode_literals

import os
import sys
import time


ARCHIVE_PATH = "/root/0.4.2.c4/archive"
HISTORY = "run-history.csv"

HISTORY_FILE = ARCHIVE_PATH + os.sep + HISTORY

if not os.path.exists(HISTORY_FILE):
    print("\033[31m \n  [ERROR]  Not find path for : ({}) \033[0m \n".format(HISTORY_FILE))
    sys.exit(1)

his_content = os.popen("cat {}".format(HISTORY_FILE)).read().strip()
for each_line in his_content.split("\n"):
    if each_line.startswith("Id"):
        continue

    try:
        line_list = each_line.split(',')
        task_id = line_list[0]
        task_name = line_list[1]
        task_state = line_list[6].strip()

        if task_state == 'finished':
            work_dir = "{}/{}-{}".format(ARCHIVE_PATH, task_id, task_name)
            start_time = line_list[3]
            end_time = line_list[4]

            start_time_array = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time_array = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_times_tamp = time.mktime(start_time_array)
            end_times_tamp = time.mktime(end_time_array)
            time_diff = end_times_tamp - start_times_tamp

            total_objs_cmd = "cat {}/driver*.csv | grep write | grep -v init " \
                             "| awk -F',' '{{print $3}}'".format(work_dir)
            count_str = os.popen(total_objs_cmd).read().strip()
            if count_str:
                counts_str_list = count_str.split("\n")
                counts_str_int = map(int, counts_str_list)
                total_objs = sum(counts_str_int)

                write_speed = total_objs / time_diff

                print("\033[32m  Task : ({}-{}), total: ({}), elapsed : ({}s), "
                      "speed : ({}) \033[0m".format(task_id, task_name, total_objs, time_diff, write_speed))
            else:
                print("\033[33m  [WARN]  Not found task : ({}-{}), please pay more attention \033[0m\n".format(task_id, task_name))
                continue
        else:
            print("\033[33m  [WARN]  Task : ({}-{}) status is not finished, but : ({}), "
                  "please pay more attention \033[0m\n".format(task_id, task_name, task_state))

    except Exception as ex:
        print("\n\033[31m \n  [ERROR]  Parase file of '{}' "
              "exception : ({}) \033[0m\n".format(HISTORY_FILE, str(ex)))
        sys.exit(1)


if __name__ == "__main__":
    pass

``` {% endraw %}

