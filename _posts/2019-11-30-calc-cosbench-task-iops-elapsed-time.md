---
layout:     post
title:      "统计cosbench每个任务的IOPS和耗时"
subtitle:   "Calc cosbench task IOPS and elapsed time"
date:       2019-11-30
author:     "Gavin"
catalog:    true
tags:
    - cosbench
    - S3
---

# 前言

近期针对前方客户提出的具体S3测试要求，测试了一下S3性能，使用的是cosbench工具。在测试过程中，排除客户的要求外，我们自身也想知道，当前硬件条件下，每间隔1,000,00,00个object，IOPS和耗时是多久，比如：1到1千万，1千万到2千万，。。。1亿到1.1亿个object, and so on。
由于测试场景比较多，而且测试时长也会很久，所有写了这个脚本，统计一下不同level object数据下的IOPS和耗时（当然，cosbench的任务是每间隔1千万提交一次，即一个xml里写1千万个object，直到数据量过亿,所以cosbench提交的是多个任务来完成数据过亿的测试）。


# 脚本内容

```
root@fireware:~# cat calc_cosbench_task_time.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import sys
from datetime import datetime

from ezs3.command import do_cmd


def get_start_end_time():
    all_work_dict = {}

    all_csv_file = do_cmd("find {} -iname *WRITEJOB.csv -print".format(archive_home), 30).strip()
    for each_csv in all_csv_file.split('\n'):
        work_id = each_csv.split('/')[-2].split('-')[0]
        {% raw %}start_time = do_cmd("cat '{}' | awk -F ',' '{{print $1}}' | grep -v 'Timestamp' |  sed '/^$/d' | head -n 1".format(each_csv), 30).strip()
        end_time = do_cmd("tac '{}' | awk -F ',' '{{print $1}}' | grep -v 'Timestamp' | head -n 1".format(each_csv), 30).strip() {% endraw %}
        all_work_dict[work_id] = [start_time, end_time]

    sorted(all_work_dict.items(), lambda x, y: cmp(x[0], y[0]))
    return all_work_dict


# def calc_elapsed_time(all_work_dict):
#     elapsed_time_dict = {}
# 
#     for each_key in all_work_dict.items():
#         start_at = each_key[1][0]
#         stop_at = each_key[1][1]
# 
#         if start_at and stop_at:
#             start = datetime.strptime(start_at, '%H:%M:%S')
#             end = datetime.strptime(stop_at, '%H:%M:%S')
#             elapsed_time = (end-start).seconds
# 
#             elapsed_time_dict[each_key[0]] = elapsed_time
#         else:
#             elapsed_time_dict[each_key[0]] = 0
# 
#     sorted(elapsed_time_dict.items(), lambda x, y: cmp(x[0], y[0]))
#     return elapsed_time_dict
# 
# 
# def calc_ops():
#     ops_dict = {}
#     all_csv_file = do_cmd("find {} -iname *W.csv -print".format(archive_home), 30).strip()
# 
#     for each_csv in all_csv_file.split('\n'):
#         cur_work_op_list = []
#         work_id = each_csv.split('/')[-2].split('-')[0]
#         {% raw %}ops_info = do_cmd("cat '{}' | awk '{{print $1}}' | awk -F ',' '{{print $14}}' | grep -v Throughput".format(each_csv), 30).strip() {% endraw %}
#         ops_dict[work_id] = sum(map(float, ops_info.split("\n")))
# 
#     return ops_dict


def calc_elapsed_time_ops(all_work_dict):
    elapsed_time_ops_dict = {}
    ops_dict = {}
    all_csv_file = do_cmd("find {} -iname *W.csv -print".format(archive_home), 30).strip()

    for each_csv in all_csv_file.split('\n'):
        cur_work_op_list = []
        work_id = each_csv.split('/')[-2].split('-')[0]
        {% raw %}ops_info = do_cmd("cat '{}' | awk '{{print $1}}' | awk -F ',' '{{print $14}}' | grep -v Throughput".format(each_csv), 30).strip() {% endraw %}
        sum_ops = sum(map(float, ops_info.split("\n")))
        
        ops_dict[work_id] = sum(map(float, ops_info.split("\n")))

        for each_key in all_work_dict.items():
            start_at = each_key[1][0]
            stop_at = each_key[1][1]
            if start_at and stop_at:
                start = datetime.strptime(start_at, '%H:%M:%S')
                end = datetime.strptime(stop_at, '%H:%M:%S')
                elapsed_time = (end-start).seconds
            else:
                elapsed_time_dict[each_key[0]] = 0

            if each_key[0] == work_id:
                time_and_ops = '{}/{}'.format(sum_ops, elapsed_time)
                elapsed_time_ops_dict[work_id] = time_and_ops
    sorted(elapsed_time_ops_dict.items(), lambda x, y: cmp(x[0], y[0]))
    return elapsed_time_ops_dict



if __name__ == '__main__':
    archive_home = "/root//0.4.2.c4/archive/"
    ls_info = do_cmd("ls -l {}".format(archive_home), 30, True).split('\n')

    if not os.path.exists(archive_home):
        print "\n    [ERROR]  Not find cosbench archive path, exit!\n"
        sys.exit(0)
    elif 'total 0' in ls_info:
        print "\n    [ERROR]  Not find cosbench archive files, exit!\n"
        sys.exit(0)

    all_work_dict = get_start_end_time()
    # elapsed_time_dict = calc_elapsed_time(all_work_dict)
    # ops = calc_ops()

    time_and_ops = calc_elapsed_time_ops(all_work_dict)
    # print("All work dict is : ({})\n".format(all_work_dict))
    # print("Elapsed time is : ({})\n".format(elapsed_time_dict))
    # print("OPS is : ({})\n".format(ops))
    print("OPS and elapsed time is : ({})\n".format(time_and_ops))
```


# 输出信息

```
root@fireware:~# python calc_cosbench_task_time.py 
OPS and elapsed time is : ({'w11': '2504.92/4070', 'w10': '2514.82/4060', 'w7': '2519.07/4050', 'w6': '2579.88/3960', 'w5': '2593.13/3940', 'w4': '2606.27/3910', 'w3': '2636.37/3870', 'w2': '2623.56/3890', 'w1': '5387.47/1890', 'w9': '2540.3/4010', 'w8': '2524.32/4050'})

root@fireware:~#
```

说明：
*吐出的信息中，以“'w11': '2504.92/4070'”为示例：
* * w11，表示的是cosbench的w11这个任务
* * 2504.92/4070, 表示这个任务的IOPS是2504.92，耗时了4070秒

