---
title: pytest下按功能点和作者统计用例编写分布情况
date: 2027-02-07 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 按功能点和作者统计用例分布信息
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 概述

为了规范测试用例的编写，增加一要求，实现如下功能:

1、按功能点统计用例分布
2、按用例编写作者统计用例编写数量

为了实现上述要求，借助`pytest`相关`hook`和`matplotlib`实现图形绘制功能。

# 代码实现

## 代码树结构

```shell
.
├── conftest.py
├── __ini__.py
├── pytest.ini
├── run.py
├── testcase
│   ├── api
│   └── web
└── utils
    ├── allure_util.py
    ├── __init__.py
    └── path_util.py
```

## conftest.py

在`conftest.py`文件中实现用例分布统计操作，并借助`matplotlib`绘制饼图，代码参考如下：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""顶层conftest.py文件，实现环境信息记录、用例执行结果统计等功能"""

import os
import sys
import time
import base64
import atexit
import logging
import tempfile
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict

import pytest
import allure
import matplotlib.pyplot as plt

from utils.path_util import get_report_path

sys.path.append(os.path.abspath('.'))

# 设置模块日志级别为INFO, 避免pytest生成的日志文件中含有其他模块的debug log
logging.getLogger('faker').setLevel(logging.INFO)
logging.getLogger('pyppeteer').setLevel(logging.INFO)
logging.getLogger('websockets').setLevel(logging.INFO)
logging.getLogger('asyncio').setLevel(logging.INFO)
logging.getLogger('matplotlib').setLevel(logging.INFO)
logging.getLogger('PIL').setLevel(logging.INFO)

# 初始化统计信息
test_stats = {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0, 'errors': 0, 'broken': 0}

# 存储每个作者的用例数、文件数和行数信息
line_counts = 0
case_counts = defaultdict(int)
file_counts = defaultdict(int)
feature_counts = defaultdict(int)
total_case_counts = defaultdict(int)
total_feature_counts = defaultdict(int)


# 注册自定义命令行参数
def pytest_addoption(parser):
    """注册自定义命令行参数"""
    parser.addoption(
        "--automation-type",
        action="store",
        default=None,
        choices=['api', 'web'],
        help="指定自动化测试类型: api 或 web"
    )


def pytest_collection_modifyitems(config, items):
    """根据传递的参数类型，收集对应类型的测试用例"""
    automation_type = config.getoption("--automation-type")
    if automation_type == "web":
        # 保留 testcase/web 目录下的测试用例，跳过其他
        items[:] = [item for item in items if os.path.join("testcase", "web") in item.location[0]]
    elif automation_type == "api":
        # 保留 testcase/api 目录下的测试用例，跳过其他
        items[:] = [item for item in items if os.path.join("testcase", "api") in item.location[0]]
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")

    # 统计用例分布，对于参数化的用例，统计为1个
    parametrized_method_names = set()
    feature_parametrized_names = set()
    for item in items:
        author = item.get_closest_marker('author')
        feature = item.get_closest_marker('feature')
        # By author:
        if author:
            author_name = author.args[0]
            parametrized = item.get_closest_marker('parametrize')
            if parametrized:
                method_name = item.originalname if hasattr(item, 'originalname') else item.name
                if method_name not in parametrized_method_names:
                    parametrized_method_names.add(method_name)
                    case_counts[author_name] += 1
            else:
                case_counts[author_name] += 1
        else:
            cls_author = item.parent.get_closest_marker('author') if item.parent else None
            if cls_author:
                parametrized = item.get_closest_marker('parametrize')
                if parametrized:
                    method_name = item.originalname if hasattr(item, 'originalname') else item.name
                    if method_name not in parametrized_method_names:
                        parametrized_method_names.add(method_name)
                        case_counts[cls_author.args[0]] += 1
                else:
                    case_counts[cls_author.args[0]] += 1
            else:
                case_counts["未知"] += 1

        # By feature
        if feature:
            feature_name = feature.args[0]
            parametrized = item.get_closest_marker('parametrize')
            if parametrized:
                # 有 feature，又有参数化的
                method_name = item.originalname if hasattr(item, 'originalname') else item.name
                if method_name not in feature_parametrized_names:
                    feature_parametrized_names.add(method_name)
                    feature_counts[feature_name] += 1
            else:
                # 有 feature，但没有参数化的
                feature_counts[feature_name] += 1
        else:
            # parent有feature/parameter的
            cls_feature = item.parent.get_closest_marker('feature') if item.parent else None
            if cls_feature:
                parametrized = item.get_closest_marker('parametrize')
                if parametrized:
                    method_name = item.originalname if hasattr(item, 'originalname') else item.name
                    if method_name not in feature_parametrized_names:
                        feature_parametrized_names.add(method_name)
                        feature_counts[cls_feature.args[0]] += 1
                else:
                    feature_counts[cls_feature.args[0]] += 1
            else:
                # 没有feature，但有参数化的
                parametrized = item.get_closest_marker('parametrize')
                if parametrized:
                    method_name = item.originalname if hasattr(item, 'originalname') else item.name
                    if method_name not in feature_parametrized_names:
                        feature_parametrized_names.add(method_name)
                        feature_counts["未知"] += 1
                    else:
                        feature_counts["未知"] += 1
                else:
                    # 既没有feature，也没有参数化的
                    feature_counts["未知"] += 1

    # 对于参数化用例，按参数化后的数量统计
    for item in items:
        method_author = item.get_closest_marker('author')
        feature = item.get_closest_marker('feature')
        # By Author
        if method_author:
            total_case_counts[method_author.args[0]] += 1
        else:
            cls = item.parent
            class_author = cls.get_closest_marker('author') if cls else None
            if class_author:
                total_case_counts[class_author.args[0]] += 1
            else:
                total_case_counts["未知"] += 1
    
        # By Feature
        if feature:
            total_feature_counts[feature.args[0]] += 1
        else:
            cls = item.parent
            class_feature = cls.get_closest_marker('parametrize') if cls else None
            if class_feature:
                total_feature_counts[class_feature.args[0]] += 1
            else:
                total_feature_counts["未知"] += 1


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """pytest统计每个测试阶段（setup/call/teardown）的执行结果"""
    if report.when == 'call':  # 'call' 阶段代表测试用例的执行阶段
        test_stats['total'] += 1
        if report.passed:
            test_stats['passed'] += 1
        elif report.failed:
            if report.when == 'call':
                test_stats['failed'] += 1
        elif report.skipped:
            test_stats['skipped'] += 1
        elif report.broken:
            test_stats['broken'] += 1


def count_lines_in_file(file_path):
    """统计文件中行数"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)


def count_files_and_lines(root_dir='.'):
    """统计文件数和行数"""
    global line_counts  # pylint: disable=W0603
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_counts[file_path] += 1
                line_counts += count_lines_in_file(file_path)


def pytest_sessionfinish(session):
    """测试会话结束时的操作，主要用于统计完成的测试结果信息。"""
    tz = ZoneInfo("Asia/Shanghai")
    start_time = session.config.start_time  # 测试开始时间
    end_time = datetime.now(tz=tz)  # 测试结束时间
    duration = end_time - start_time  # 测试持续时间

    # 获取已声明的alluredir命令行参数值
    allure_dir = session.config.getoption('--alluredir')
    if not allure_dir:
        print('Allure results directory not found. Ensure you are using `--alluredir` option with pytest.')
        return

    # environment.properties内容生成使用的初始化信息
    test_environment_ip = "192.168.1.101"  # 被测环境的ip，根据实际情况调用函数获取
    product_version = "v1.0.0"  # 根据实际情况调用函数获取

    env_data = {
        'Environment IP': test_environment_ip,
        'Product Version': product_version,
        'Test Start Time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
        'Test End Time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
        'Test Duration (seconds)': str(duration.total_seconds()),
        'Total Cases': str(test_stats['total']),
        'Passed Cases': str(test_stats['passed']),
        'Failed Cases': str(test_stats['failed']),
        'Skipped Cases': str(test_stats['skipped']),
        'Broken Cases': str(test_stats['broken']),
    }

    # 写入环境信息
    if allure_dir:
        with open(os.path.join(allure_dir, 'environment.properties'), 'w', encoding='utf-8') as env_file:
            for key, value in env_data.items():
                env_file.write(f'{key}={value}\n')

    # 统计author, feature分布信息, 用例规模
    dash_count = 100
    print("-" * dash_count)
    authors = list(case_counts.keys())
    total_cases = sum(case_counts.values())
    total_parametrized_cases = sum(total_case_counts.values())
    count_files_and_lines()
    with_allure = hasattr(session.config, 'allurelistener')
    if with_allure:
        with allure.step('用例统计信息'):
            for author in authors:
                count = case_counts[author]
                percentage = (count / total_cases) * 100 if total_cases > 0 else 0
                message = f'{author} 编写的用例数（{count}），占比（{percentage:.2f}%)'
                allure.attach(message, '用例统计信息', allure.attach_type.TEXT)
            allure.attach(f'总代码行数: ({line_counts}', '总代码行数')
            allure.attach(f'总Python文件数: ({len(file_counts)})', '总Python文件数')
            allure.attach(f'总用例数(非参数化后): ({total_cases})', '总用例数(非参数化后)')
            allure.attach(f'总用例数(含参数化后): ({total_parametrized_cases})', '总用例数(含参数化后)')
    else:
        for author in authors:
            count = case_counts[author]
            percentage = (count / total_cases) * 100 if total_cases > 0 else 0
            print(f'作者 ({author}) 编写的用例数: {count}(个), 占比: {percentage:.2f}%')
        print(f'总代码数(行): {line_counts}')
        print(f'总 python 文件数(个): {len(file_counts)}')
        print(f'总用例数(个): {total_cases}; 参数化总用例数(个): {total_parametrized_cases}')
    print("-" * dash_count)

    statistics_file = os.path.join(get_report_path(), "Statistics.txt")
    desc_content = """
对于测试用例使用了pytest.mark.parametrize，在统计测试用例数量上做了区分，说明如下，
- 非参数化，表示对参数化的用例，计数按1个用例计算
- 含参数化，表示对参数化的用例，计数按参数化后的用例数进行计算，如一个用例参数化出来10个用例，并计为10

"""
    with open(statistics_file, "w", encoding='utf-8') as f:
        f.write("-" * 44 + "  统计总览  " + "-" * 40 + "\n")
        f.write(f"代码规模（行）：{line_counts}\n")
        f.write(f"用例总数（个）：{total_cases}\n")
        f.write(f"\t非参数化（{total_cases}）\n")
        f.write(f"\t含参数化（{total_parametrized_cases}）\n\n")
        f.write("-" * 44 + "  用例分布  " + "-" * 40 + "\n")
        f.write("   按作者：\n")
        f.write(f"\t非参数化\t作者\t\t用例数(个)\t占比(%)\n")

        for author in authors:
            count = case_counts[author]
            percentage = (count / total_cases) * 100 if total_cases > 0 else 0
            # 使用格式化字符串来对其
            f.write(f"\t{author}\t{count}\t{percentage:.2f}%\n".format(
                author=author if author else '未知',
                count=count,
                percentage=percentage
            ))

        f.write(f"\t含参数化\t作者\t\t用例数(个)\t占比(%)\n")
        for author in authors:
            count = total_case_counts[author]
            percentage = (count / total_parametrized_cases) * 100 if total_parametrized_cases > 0 else 0
            # 使用格式化字符串来对齐列
            f.write(f"\t\t{author}\t\t{count}\t\t{percentage:.2f}%\n".format(
                author=author if author else '未知',
                count=count,
                percentage=percentage
            ))                  

        f.write("\n   按功能：\n")
        f.write("\t非参数化\t功能点\t\t用例数（个）\t占比（%）\n")
        for each_feature in feature_counts:
            count = feature_counts[each_feature]
            percentage = (count / total_cases) * 100 if total_cases > 0 else 0
            # 使用格式化字符串来对齐列
            f.write(f"\t\t{each_feature}\t\t{count}\t\t{percentage:.2f}%\n".format(
                each_feature=each_feature if each_feature else '未知',
                count=count,
                percentage=percentage
            ))
        f.write("\n\t含参数化\t功能点\t\t用例数（个）\t占比（%）\n")
        for each_feature in feature_counts:
            count = total_feature_counts[each_feature]
            percentage = (count / total_parametrized_cases) * 100 if total_parametrized_cases > 0 else 0
            # 使用格式化字符串来对齐列
            f.write(f"\t\t{each_feature}\t\t{count}\t\t{percentage:.2f}%\n".format(
                each_feature=each_feature if each_feature else '未知',
                count=count,
                percentage=percentage
            ))
        f.write(desc_content)
    
        # 生成饼图
        generate_cycle_chart(case_counts, feature_counts)


def calculate_percentages(values):
    """计算百分比"""
    total = sum(values)
    return ["{0:.1f}%".format((value / total) * 100) if total else 0 for value in values]


def plot_donut_chart(ax, data, colors, title):
    """定义一个函数来绘制甜甜圈图并显示数量"""
    labels = []
    sizes = []
    for label, size in data.items():
        labels.append(f"{label} ({size})")
        sizes.append(size)
    explode = [0.01] * len(sizes)  # 稍微突出显示每个部分
    calculate_percentages(sizes)  # 计算百分比
    ax.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%',
           startangle=140, pctdistance=0.87)
    # 设置标题
    ax.set_title(title)


def generate_cycle_chart(case_counts, feature_counts):
    """绘制饼图的主函数"""
    # 设置中文字体为黑体，防止中文显示乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 设置负号正常显示
    plt.rcParams['axes.unicode_minus'] = False

    # 定义颜色
    colors1 = plt.cm.Paired(range(len(case_counts)))  # pylint: disable=E1101
    colors2 = plt.cm.Paired(range(len(feature_counts)))  # pylint: disable=E1101

    # 创建图形和子图
    _, axs = plt.subplots(1, 2, figsize=(24, 12), subplot_kw=dict(aspect="equal"))  # pylint: disable=R1735

    # 绘制两个甜甜圈图
    plot_donut_chart(axs[0], case_counts, colors1, "测试用例分布")
    plot_donut_chart(axs[1], feature_counts, colors2, "功能用例分布")

    # Save image
    img_name = os.path.join(get_report_path(), "testcase_distribution.webp")
    plt.savefig(img_name, format='webp')  # 保存为webp格式


def pytest_configure(config):
    """pytest 初始化钩子"""
    # 修改本地时区
    tz = ZoneInfo("Asia/Shanghai")
    config.start_time = datetime.now(tz=tz)
```

## pytest.ini文件

```python
[pytest]
log_level = NOTSET
log_level = INFO
log_file = report/automation_test.log
log_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_date_format=%Y-%m-%d %H:%M:%S
log_file_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_file_date_format=%Y-%m-%d %H:%M:%S
log_cli_level = INFO
log_cli_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_cli_date_format=%Y-%m-%d %H:%M:%S
addopts = -vrs --show-progress --cache-clear --full-trace -p no:warnings
norecursedirs = .svn .git

markers =
    feature:feature.
    authon:author.
```

## run.py

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import sys
import time
import argparse
import subprocess

import shutil
import pytest


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='执行自动化测试')
    parser.add_argument('--automation-type', required=True, choices=['api', 'web'],
                        help='指定测试类型: api 或 web')
    parser.add_argument('--alluredir', default='report/allure_raw',
                        help='Allure报告数据存储目录')
    parser.add_argument('--report-dir', default='report/html_report',
                        help='生成的HTML报告目录')
    parser.add_argument('--clean', action='store_true',
                        help='清除历史报告数据')
    parser.add_argument('pytest_args', nargs=argparse.REMAINDER,
                        help='传递给pytest的额外参数')
    
    args = parser.parse_args()
    
    # 获取传递的pytest参数（跳过第一个元素，因为它是脚本名称）
    pytest_args = args.pytest_args[1:] if args.pytest_args else []
    
    # 清理历史报告
    if args.clean:
        clean_report_dirs(args.alluredir, args.report_dir)
    
    # 确保报告目录存在
    os.makedirs(args.alluredir, exist_ok=True)
    os.makedirs(args.report_dir, exist_ok=True)
    
    # 构造pytest命令参数
    pytest_cmd = [
        '-c', 'pytest.ini',  # 明确指定配置文件
        f'--automation-type={args.automation_type}',
        f'--alluredir={args.alluredir}',
        *pytest_args
    ]
    
    print(f"执行命令: pytest {' '.join(pytest_cmd)}")
    
    # 执行pytest测试
    exit_code = pytest.main(pytest_cmd)
    
    # 生成Allure报告
    if os.path.exists(args.alluredir) and os.listdir(args.alluredir):
        generate_allure_report(args.alluredir, args.report_dir)
        print(f"报告已生成: file://{os.path.abspath(args.report_dir)}/index.html")
    else:
        print("警告: Allure报告目录为空，未生成报告")
    
    sys.exit(exit_code)


def clean_report_dirs(*dirs):
    """清理报告目录"""
    for d in dirs:
        if os.path.exists(d):
            print(f"清理目录: {d}")
            shutil.rmtree(d)


def generate_allure_report(alluredir, report_dir):
    """生成Allure HTML报告"""
    cmd = [
        'allure', 'generate', 
        '--clean', 
        alluredir, 
        '-o', report_dir
    ]
    print(f"生成Allure报告: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
```

## allure功能封装

为了避免用例编写的时候，使用`allure`传递太多的装饰器，这里封装了一层`allure`，代码参考如下：

```python
# allure_util.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

""" Allure 信息的封装 """

import json

import allure

from typing import Any
from pathlib import Path
from allure_commons.types import AttachmentType


def get_file_properties(filepath: Path) -> tuple[str, str, str]:
    """
    获取文件属性信息
    filepath.name：返回路径的最后一部分，包括文件扩展名。
                   例如，如果 filepath 是 /path/to/file.txt，那么 filepath.name 将会是 file.txt。
    filepath.stem：返回路径的最后一部分，不包括文件扩展名。
                   继续上面的例子，filepath.stem 将会是 file。
    filepath.suffix.lstrip('.')：返回文件的扩展名，包括前面的点（.）。
                   lstrip('.') 方法用于去除扩展名前的点。例如，如果 filepath 是 /path/to/file.txt，
                   那么 filepath.suffix 将会是 .txt，lstrip('.') 将会移除点，最终结果是 txt。
    """
    return filepath.name, filepath.stem, filepath.suffix.lstrip('.')


def serialize_var(var: Any) -> str:
    """
    序列化字符串（字典或数字）。字典被转换为格式化的 JSON 字符串，而数字则被转换为其字符串表示
    """
    return json.dumps(var, ensure_ascii=False, indent=2) if isinstance(var, dict) else str(var)


@allure.step('{step}')
def report_step(step: str, var: Any) -> None:
    """  记录测试过程中的单个动作步骤，并将其变量以 JSON 格式附加到 Allure 报告中  """
    with allure.step(step):
        allure.attach.body(
            body=serialize_var(var),
            name='json_serialize',
            attachment_type=AttachmentType.JSON,
        )


def attach_to_report(body: Any, name: str = 'attachment',
                     attachment_type: AttachmentType = AttachmentType.JSON) -> None:
    """ 附件内容到Allure report. """
    allure.attach(
        body=body,
        name=name,
        attachment_type=attachment_type
    )


def attach_file_to_report(filepath: Path, name: str | None = None) -> None:
    """  附件文件到Allure report.  """
    name = name or filepath.name
    _, _, file_type = get_file_properties(filepath)
    attach_type = AttachmentType.TEXT if file_type == 'txt' else getattr(AttachmentType,
                                                                         file_type.upper(),
                                                                         AttachmentType.JSON)

    allure.attach.file(
        source=str(filepath),
        name=name,
        attachment_type=attach_type
    )


def allure_attributes(**kwargs):
    """  定义allure报告展示属性信息的装饰器  """
    def decorator(func):
        for key, value in kwargs.items():
            if hasattr(allure, key):
                if isinstance(value, tuple) and len(value) == 2:
                    # Assuming tuple contains (url, name)
                    dec = getattr(allure, key)(value[0], name=value[1])
                else:
                    dec = getattr(allure, key)(value)
                func = dec(func)
            else:
                raise AttributeError(f"Allure does not have the attribute '{key}'")
        return func
    return decorator


"""
# 使用方法
@allure_attributes(
    feature='登录功能',
    story='用户正常登录',
    title='正常情况下用户能够登录',
    severity='critical',
    link=('https://documentation.mysite.com/login-feature', '登录模块文档'),
    issue=('https://issue-tracker.mysite.com/issues/123', '登录失败的已知Bug'),
    testcase=('https://test-tracker.mysite.com/case/456', '登录成功的测试案例')
)
def test_login_functionality():
    pass
"""
```

## path_util.py

配置文件、报告相关路径的获取。

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""  Path Util  """

from __future__ import unicode_literals

import os


__all__ = ["get_config_path"]


def get_config_path():
    """
    获取config文件的路径.
    先获得当前的文件的路径，由于config和common同一级，把common替换为config即可.
    """
    return os.path.dirname(os.path.realpath(__file__)) + os.sep + "config" + os.sep


def get_report_path():
    """
    获取测试报告的路径.report的路径应该在当前../report
    """
    report_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) \
                  + os.sep + "report" + os.sep
    return report_path
```

## 测试用例编写

测试用例编写要求，参考如下:

```python
# -*- coding:UTF-8 -*-

import pytest

from utils.allure_util import allure_attributes


@allure_attributes(
    feature='数据管理--查询功能',
    story='数据查询'
)
@pytest.mark.feature("数据查询功能")
@pytest.mark.author("SI.Li")
class TestDataQuery:
    """数据查询测试"""

    @allure_attributes(
        severity='critical',
        testcase=('http://example.com/testcase-view-201.html', '查询成功测试')
    )
    def test_query_success(self):
        """数据查询成功测试"""
        assert 'result' is not None

    @allure_attributes(
        severity='normal',
        testcase=('http://example.com/testcase-view-202.html', '查询失败测试')
    )
    def test_query_failure(self):
        """数据查询失败测试"""
        assert 3 == 3
```


## 统计效果

**运行时打屏统计信息参考如下：**

```shell
root@Gavin:~/automation/test# python3 run.py --automation-type=api --alluredir=report/json
执行命令: pytest -c pytest.ini --automation-type=api --alluredir=report/json
/usr/local/lib/python3.11/dist-packages/pytest_asyncio/plugin.py:208: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))
/usr/local/lib/python3.11/dist-packages/pytest_progress.py:155: PytestDeprecationWarning: The hookimpl ProgressTerminalReporter.pytest_report_teststatus uses old-style configuration options (marks or attributes).
Please use the pytest.hookimpl(tryfirst=True) decorator instead
 to configure the hooks.
 See https://docs.pytest.org/en/latest/deprecations.html#configuring-hook-specs-impls-using-markers
  @pytest.mark.tryfirst
=================================================================================== test session starts ====================================================================================
platform linux -- Python 3.11.6, pytest-8.3.4, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.3.4', 'pluggy': '1.5.0'}, 'Plugins': {'gui': '0.1.0', 'random-order': '1.1.1', 'cov': '5.0.0', 'asyncio': '0.24.0', 'instafail': '0.5.0', 'order': '1.3.0', 'metadata': '3.1.1', 'Faker': '35.0.0', 'check': '2.3.1', 'rerunfailures': '14.0', 'lazy-fixture': '0.6.3', 'pretty': '1.2.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.3.0', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/automation/test
configfile: pytest.ini
plugins: gui-0.1.0, random-order-1.1.1, cov-5.0.0, asyncio-0.24.0, instafail-0.5.0, order-1.3.0, metadata-3.1.1, Faker-35.0.0, check-2.3.1, rerunfailures-14.0, lazy-fixture-0.6.3, pretty-1.2.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.3.0, picked-0.5.0, assume-2.4.3, anyio-4.3.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT, default_loop_scope=None
collected 6 items                                                                                                                                                                          

testcase/api/test_api_request.py::TestAPIRequest::test_get_request PASSED                                                                                                            [ 16%]
_______________________________________________________ 1 of 6 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _______________________________________________________

testcase/api/test_api_request.py::TestAPIRequest::test_post_request PASSED                                                                                                           [ 33%]
_______________________________________________________ 2 of 6 completed, 2 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _______________________________________________________

testcase/api/test_query_db.py::TestDataQuery::test_query_success PASSED                                                                                                              [ 50%]
_______________________________________________________ 3 of 6 completed, 3 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _______________________________________________________

testcase/api/test_query_db.py::TestDataQuery::test_query_failure PASSED                                                                                                              [ 66%]
_______________________________________________________ 4 of 6 completed, 4 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _______________________________________________________

testcase/api/test_upload_files.py::TestFileUpload::test_upload_success PASSED                                                                                                        [ 83%]
_______________________________________________________ 5 of 6 completed, 5 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _______________________________________________________

testcase/api/test_upload_files.py::TestFileUpload::test_upload_failure PASSED                                                                                                        [100%]
_______________________________________________________ 6 of 6 completed, 6 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _______________________________________________________
----------------------------------------------------------------------------------------------------
作者 (Wu.Wang) 编写的用例数: 2(个), 占比: 33.33%
作者 (SI.Li) 编写的用例数: 2(个), 占比: 33.33%
作者 (Liu.Zhao) 编写的用例数: 2(个), 占比: 33.33%
总代码数(行): 1034
总 python 文件数(个): 10
总用例数(个): 6; 参数化总用例数(个): 6
----------------------------------------------------------------------------------------------------
/root/automation/test/conftest.py:370: UserWarning: Glyph 27979 (\N{CJK UNIFIED IDEOGRAPH-6D4B}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式
/root/automation/test/conftest.py:370: UserWarning: Glyph 35797 (\N{CJK UNIFIED IDEOGRAPH-8BD5}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式
/root/automation/test/conftest.py:370: UserWarning: Glyph 29992 (\N{CJK UNIFIED IDEOGRAPH-7528}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式
/root/automation/test/conftest.py:370: UserWarning: Glyph 20363 (\N{CJK UNIFIED IDEOGRAPH-4F8B}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式
/root/automation/test/conftest.py:370: UserWarning: Glyph 20998 (\N{CJK UNIFIED IDEOGRAPH-5206}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式
/root/automation/test/conftest.py:370: UserWarning: Glyph 24067 (\N{CJK UNIFIED IDEOGRAPH-5E03}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式
/root/automation/test/conftest.py:370: UserWarning: Glyph 21151 (\N{CJK UNIFIED IDEOGRAPH-529F}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式
/root/automation/test/conftest.py:370: UserWarning: Glyph 33021 (\N{CJK UNIFIED IDEOGRAPH-80FD}) missing from font(s) DejaVu Sans.
  plt.savefig(img_name, format='webp')  # 保存为webp格式

==================================================================================== 6 passed in 17.69s ====================================================================================
生成Allure报告: allure generate --clean report/json -o report/html_report
Report successfully generated to report/html_report
报告已生成: file:///root/automation/test/report/html_report/index.html
```

**Statistics.txt文件内容参考如下：**

```shell
root@Gavin:~/automation/test/report# cat Statistics.txt 
--------------------------------------------  统计总览  ----------------------------------------
代码规模（行）：689
用例总数（个）：6
	非参数化（6）
	含参数化（6）

--------------------------------------------  用例分布  ----------------------------------------
   按作者：
	非参数化	作者		用例数(个)	占比(%)
	Wu.Wang	2	33.33%
	SI.Li	2	33.33%
	Liu.Zhao	2	33.33%
	含参数化	作者		用例数(个)	占比(%)
		Wu.Wang		2		33.33%
		SI.Li		2		33.33%
		Liu.Zhao		2		33.33%

   按功能：
	非参数化	功能点		用例数（个）	占比（%）
		API request feature		2		33.33%
		Data query		2		33.33%
		Upload feature		2		33.33%

	含参数化	功能点		用例数（个）	占比（%）
		API request feature		2		33.33%
		Data query		2		33.33%
		Upload feature		2		33.33%

对于测试用例使用了pytest.mark.parametrize，在统计测试用例数量上做了区分，说明如下，
- 非参数化，表示对参数化的用例，计数按1个用例计算
- 含参数化，表示对参数化的用例，计数按参数化后的用例数进行计算，如一个用例参数化出来10个用例，并计为10
```

**饼图绘制展示效果，参考如下：**

<img class="shadow" src="/img/in-post/testcase_distribution.webp" width="1200" />

**说明：**

- 图中乱码问题没有解决掉，可以使用英文代替汉字规避一下。

