---
layout:     post
title:      "pytest 之 pytest.ini"
subtitle:   "pytest pytest.ini"
date:       2023-10-27
author:     "Gavin"
catalog:    true
tags:
    - pytest
    - Automation
---


#  概述

pytest 配置文件可以改变 pytest 的运行方式，它是一个固定的文件（名称固定，只能是 pytest.ini），读取配置信息，按指定的方式去运行。

pytest.ini 放在项目的根目录下。

简而言之，如果 pytest.ini 有该参数值，在执行的时候，先读取配置文件中的参数，然后取其他地方的（主函数/命令行中）。


# 注意点

pytest.ini 不能使用任何中文符号，包括汉字、空格、引号、冒号等等。

pytest 里面有些文件是非 test 文件

* pytest.ini：pytest 的主配置文件，可以改变 pytest 的默认行为
* conftest.py：测试用例的一些 fixture 配置
* _init_.py：识别该文件夹为 python 的 package 包
* tox.ini 与 pytest.ini 类似，用 tox 工具时候才有用
* setup.cfg 也是 ini 格式文件，影响 setup.py 的行为
    

# 哪些内容可以放在 pytest.ini 文件中


pytest.ini 文件中的内容，来自于 ``` pytest --help```， 具体信息，请查阅help，每个参数都有描述说明。

# pytest.ini示例


以下为我的project中使用的 pytest.ini 文件内容，参考如下：

```
[pytest]
log_cli = false
log_level = NOTSET
log_file = ../report/pytest_autotest.log
log_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_date_format=%Y-%m-%d %H:%M:%S
log_file_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_file_date_format=%Y-%m-%d %H:%M:%S
log_cli_level = INFO
log_cli_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_cli_date_format=%Y-%m-%d %H:%M:%S

norecursedirs = .svn .git
console_output_style = count
addopts =-vrs --show-progress --cache-clear --full-trace -p no:warnings
```

这里我主要使用：

(1) log记录日志，规定了log level&format&path
(2) 要忽略扫描测试用例的目录（如上，忽略了.svn 和 .git 目录，因为pytest会全目录扫描，指定忽略相关目录，避免无效扫描）
(3) colsole output style

```
[pytest]
console_output_style = classic  #经典样式
console_output_style = progress #带有进度指示器的经典演示
console_output_style = count    #像progress,但将进度显示为已完成的测试数，而不是百分比
```

(4) addopts 更改默认命令行选项，经常要用到某些参数，又不想重复输入

```
addopts =  -vv        #以更详细的显示运行结果
           -m smoke   #被标记为 smoke 的用例
          --disable-warnings           # 禁用所有warnings，不建议使用，禁用范围过大, 等同于上面的 “-p no:warnings”
          --alluredir allure_results   # allure报告路径
          --maxfail=2 -rf              # 2个用例失败后退出，并给出详细信息
          --full-trace                 # 不截断任何的tracebacks，打印更详细的错误堆栈信息，默认是截断

```



# 关于 warnning


官网（https://docs.pytest.org/en/7.4.x/how-to/capture-warnings.html#pytest-mark-filterwarnings）给的示例：
```
import warnings
import pytest


def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


# @pytest.mark.filterwarnings("ignore:api v1")
def test_one():
    assert api_v1() == 1

```

## 禁用warnings的方式

```
# 禁用所有warnings，通常不使用，禁用范围过大
pytest  --disable-warnings

# 使用-W选项忽略warning， :: 表示具体的警告类名称   :表示匹配告警中msg的子串
pytest -W ignore::UserWarning
pytest -W "ignore:api v1"   # 这里的 "api v1"，为上面示例代码中 'warnings.warn(UserWarning("api v1, should use functions from v2"))' 的子串，下同
```

## 使用装饰器@pytest.mark.filterwarnings

```
# : 表示匹配告警信息中的msg的子串
@pytest.mark.filterwarnings("ignore:api v1") 

# :: 表示匹配告警信息中的告警类的类名，例如给出代码示例中的告警即可使用如下方式过滤告警

@pytest.mark.filterwarnings("ignore::UserWarning")
```



## 在pytest.ini中进行告警过滤，该文件需要存放到项目根目录

```
[pytest]
filterwarnings =
    ignore::UserWarning
    ignore::urllib3.exceptions.InsecureRequestWarning
```


## pytest.ini 中禁用warnings插件方式

```
[pytest]
addopts = -p no:warnings
```
