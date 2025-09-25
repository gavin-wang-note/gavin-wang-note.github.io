---
title: 为何用例执行入口程序没有加载pytest.ini文件
date: 2028-04-30 21:00:00
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: run_tests.py作为用例执行总入口，为何没有加载当前目录下的pytest.ini文件？
categories:
    - [pylint]
    - [Automation]
tags:
    - pylint
    - Automation
---




# 概述

今天巡检`CI`，发现如下日志片段：

```shell
testcase/administrator_terminal/test_random_inspect_check.py:21: PytestUnknownMarkWarning: Unknown pytest.mark.author - is this a typo? To register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
@pytest.mark.author("张三")

testcase/test_annual_report.py:22: PytestUnknownMarkWarning: Unknown pytest.mark.feature - is this a typo? You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
@pytest.mark.feature("年报填写")

testcase/test_annual_report.py:23: PytestUnknownMarkWarning: Unknown pytest.mark.author - is this a typo? You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
@pytest.mark.author("李四")

testcase/test_save_branch_corp_info.py:21: PytestUnknownMarkWarning: Unknown pytest.mark.feature - is this a typo? You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

检测了本地`pytest.ini`文件：

```shell
[jenkins@Gavin src]$ cat pytest.ini
[pytest]
, 其他配置项信息
addopts = -vrsXX -p no:warnings --show-progress --alluredir=..reports/json --clean-alluredir
norecursedirs = .svn .idea .git
console_output_style = count

markers =
    feature
    author
```
`pytest.ini`文件里明明有`feature`和`author`，为何还是会有这个告警呢？


# 问题排查过程

## Step1. 查询当前支持的markers信息

执行如下命令：

```shell
pytest --markers
```

看到结果信息参考如下（部分记录）：

```shell
[jenkins@Gavin src]$ pytest --markers
@pytest.mark.feature:

@pytest.mark.author:

--------- 后面省略  -------------
```

从上述记录来看，说明已经正确加载了`pytest.ini`，相关`markers`也是正确的，这只能说明`pytest`命令行执行，默认能够加载`pytest.ini`文件，由于项目为了支持`CI`，增加了用例执行入口`run_tests.py`，所以接下来需要检测一下，执行`run_tests.py`与`pytest`命令行之间的差异。


## Step2. 检查run_tests.py与pytest命令行


先执行`run_tests.py`，控制台输出参考如下：

```shell
[jenkins@Gavin src]$ python run_tests.py
pytest args: ['--alluredir', '/var/lib/jenkins/workspace/News/reports/json', '--clean-alluredir', '--cov=.', '--cov-report=xml:/var/lib/jenkins/workspace/News/reports/coverage.xml']

platform linux -- Python 3.9.18, pytest=8.3.3, pluggy=1.0.0
test session starts
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
rootdir: /var/lib/jenkins/workspace/News
configfile: pytest.ini
plugins: base-url-2.1.0, anyio-4.6.2.post1, timeout-2.3.1, rerunfailures-14.0, repeat-0.9.3, random-order-1.1.1, pylint-0.21.0, progress-1.2.4, playwright-0.5.2, picked-0.5.0, order-1.0.0, instafail-0.5.0, freezegun-0.4.2, cov-5.0.0, check-2.4.1, Faker-30.8.0, allure-pytest-2.13.5
collected 3 items

testcase/administrator_terminal/test_random_inspect_check.py F
testcase/test_annual_report.py F
testcase/test_save_branch_corp_info.py F

= FAILURES =
------- 后面内容省略 --------
```

入口文件`run_tests.py`是调用`pytest.main(pytest_args)`函数，部分代码片段如下：

```python
def run_pytest():
    """
    1. Run pytest testcases
    2. Generate Allure HTML report
    3. Generate code coverage report
    4. Generate pylint result
    """

    # ... 前面的代码

    # Define pytest args
    json_path = os.path.join(report_base_path, "json")
    html_path = os.path.join(report_base_path, "html")
    cov_path = os.path.join(report_base_path, "coverage.xml")
    pytest_args = ["--alluredir", f"{json_path}",
                   "--clean-alluredir",
                   f"--automation-type={args.automation_type}",
                   r"--cov=.",
                   f"--cov-report=xml:{cov_path}"]

    if args.automation_type.lower() == "web":
        test_path = os.path.join("testcase", "web")
        pytest_args.append(test_path)
    elif args.automation_type.lower() == "api":
        test_path = os.path.join("testcase", "api")
        pytest_args.append(test_path)

    print(f"pytest args: {pytest_args}")

    return_code = pytest.main(pytest_args)
    if return_code not in [ExitCode.OK, ExitCode.TESTS_FAILED]:
        print(f"Run pytest with return code: {return_code}")
        sys.exit(return_code)

    # ... 后面的代码


if __name__ == '__main__':
    # ENV Check
    check_urls()

    # Run test case
    run_pytest()
```

看到这样一行信息：`pytest args: ['--alluredir', '/var/lib/jenkins/workspace/News/reports/json', '--clean-alluredir', '--cov=.', '--cov-report=xml:/var/lib/jenkins/workspace/News/reports/coverage.xml']`，这个就是执行的`pytest`命令行，而且也清楚的看到，控制台输出的信息中，缺少`configfile: pytest.ini`信息。





单独执行控制台输出的`pytest args`命令：

```shell
[jenkins@Gavin src]$ pytest --alluredir=/var/lib/jenkins/workspace/News/reports/json --clean-alluredir --cov=. --cov-report=xml:/var/lib/jenkins/workspace/News/reports/coverage.xml

platform linux -- Python 3.9.18, pytest=8.3.3, pluggy=1.0.0 -- /usr/bin/python3
test session starts
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
rootdir: /var/lib/jenkins/workspace/News/src
configfile: pytest.ini
plugins: base-url-2.1.0, anyio-4.6.2.post1, timeout-2.3.1, rerunfailures-14.0, repeat-0.9.3, random-order-1.1.
------- 后面内容省略 --------
```

这里我们清楚的看到，控制台输出的信息中，是有`configfile: pytest.ini`信息的。

到此，可以分析出，单独执行`pytest`命令行，默认加载了`pytest.ini`文件，但是执行自行开发的`run_tests.py`文件，就没有加载`pytest.ini`文件，原因出在什么地方呢？



## 原因分析

### 根因

从上述日志信息中，我发现了关键线索：

通过 `run_tests.py` 执行时：

```shell
rootdir: /var/lib/jenkins/workspace/News
configfile: pytest.ini
```

直接执行 `pytest` 命令时：

```shell
rootdir: /var/lib/jenkins/workspace/News/src
configfile: pytest.ini
```

虽然文件都在 `src` 目录，但通过 `run_tests.py` 执行时，`pytest` 错误地将项目根目录 (`/var/lib/jenkins/workspace/News`) 识别为 `rootdir`，而不是正确的 `src` 目录，具体说，就是 `pytest` 的 `rootdir` 检测机制出现了偏差！

### 在 conftest.py 中添加诊断

```python
def pytest_configure(config):
    """Pytest 初始化钩子"""
    print("=== pytest配置诊断 ===")
    print(f"rootdir: {config.rootdir}")
    print(f"inipath: {config.inipath}")
    print(f"config file: {config.inicfg.get('markers', 'NOT FOUND')}")
    
    # ... 原有代码
```


再次分别执行`run_tests.py`和`pytest`命令行，得到如下输出信息：


```shell
[jenkins@Gavin src]$ python run_tests.py
current path: (/var/lib/jenkins/workspace/News/src)
pytest args: ['--alluredir', '/var/lib/jenkins/workspace/News/reports/json', '--clean-alluredir', '--cov=.', '--cov-report=xml:/var/lib/jenkins/workspace/News/reports/coverage.xml']
----- pytest 配置诊断-----
rootdir: /var/lib/jenkins/workspace/News
inipath: None
config file: (None, 'Not found')
platform linux -- Python 3.9.18, pytest-8.3.3, pluggy-1.0.0
test session starts
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
rootdir: /var/lib/jenkins/workspace/News
plugins: base-url-2.1.0, anyio-4.6.2.post1, timeout-2.3.1, rerunfailures-14.0, repeat-0.9.3, random-order-1.1.1, pylint-0.21.0, progress-1.2.4, playwright-0.5.2, picked-0.5.0, order-1.3.0, instafail-0.5.0, freezegun-0.4.2, cov-5.0.0, check-2.4.1, Faker-30.8.0, allure-pytest-2.13.5
collected 3 items

testcase/administrator_terminal/test_random_inspect_check.py F
testcase/test_annual_report.py F
testcase/test_save_branch_corp_info.py F

----- 后面省略 -----
```


```shell
[jenkins@Gavin src]$ pytest --alluredir=/var/lib/jenkins/workspace/News/reports/json --clean-alluredir --cov=. --cov-report=xml:/var/lib/jenkins/workspace/News/reports/coverage.xml
----- pytest 配置诊断-----
rootdir: /var/lib/jenkins/workspace/News/src
inipath: /var/lib/jenkins/workspace/News/src/pytest.ini
config file: ('feature\\nauthor', 'Not found')
----- 后面省略 -----
```

从日志，验证了上面的陈述，非常明确的看出来：`pytest`命令行正确加载了`pytest.ini`文件，而`run_tests.py`的`inipath`是`None`，虽然当前路径都是：`/var/lib/jenkins/workspace/News/src`，但是`rootdir`前者是`rootdir: /var/lib/jenkins/workspace/News`,后者是`rootdir: /var/lib/jenkins/workspace/News/src`，当然无法正常加载`src`目录下的`pytest.ini`文件了。



## pytest 的 rootdir 检测机制详解

### 什么是 rootdir？

`rootdir` 是 `pytest` 确定项目根目录的机制，它是 `pytest` 查找配置文件（如 `pytest.ini`、`pyproject.toml`、`tox.ini`）的**起点目录**。

### rootdir 检测规则

pytest 按照以下顺序确定 `rootdir`：

1. **从当前目录开始向上搜索**，寻找包含以下任意文件的目录：
   - `pytest.ini`
   - `pyproject.toml`（包含 `[tool.pytest.ini_options]`）
   - `tox.ini`（包含 `[pytest]` 部分）
   - `setup.cfg`（包含 `[tool:pytest]` 部分）

2. **如果找不到配置文件**，则寻找包含以下文件的目录：
   - `.pytest_cache` 目录
   - `setup.py`
   - 其他项目标识文件

3. **如果以上都找不到**，则使用当前工作目录作为 `rootdir`

### 我的具体情况分析

从我的诊断信息来看：

**直接执行 pytest 命令时：**
```
当前目录: /var/lib/jenkins/workspace/News/src
rootdir检测: 在src目录找到pytest.ini → rootdir = /var/lib/jenkins/workspace/News/src
```

**通过 run_tests.py 执行时：**
```
当前目录: /var/lib/jenkins/workspace/News/src (脚本位置)
但rootdir检测结果: /var/lib/jenkins/workspace/News
```

### 为什么会出现这种偏差？

#### 可能原因 1：Python 导入路径影响

当通过 `run_tests.py` 执行时，Python 的导入系统可能改变了 pytest 的目录检测逻辑：

```python
# run_tests.py 中的导入可能影响了路径
import pytest
from config.settings import CONFIG  # 这些导入可能改变了搜索路径
from utils.path_util import get_report_path
```

#### 可能原因 2：pytest 插件加载顺序

某些 pytest 插件可能在配置文件加载之前就执行了操作：

```python
# 在conftest.py中查看插件加载顺序
def pytest_configure(config):
    print("已加载的插件:", [x for x in dir(config.pluginmanager) if 'plugin' in x.lower()])
```

#### 可能原因 3：工作目录的微妙变化

虽然我认为二者的工作目录相同，但可能存在细微差异：

```python
# 添加详细诊断
import os
print("os.getcwd():", os.getcwd())
print("__file__:", __file__)
print("abspath(__file__):", os.path.abspath(__file__))
print("dirname(abspath(__file__)):", os.path.dirname(os.path.abspath(__file__)))
```

#### 可能原因 4：Jenkins 环境变量影响

CI 环境中可能存在特殊的环境变量：

```python
# 检查环境变量
import os
print("PYTHONPATH:", os.environ.get('PYTHONPATH', 'Not set'))
print("PWD:", os.environ.get('PWD', 'Not set'))
```
## 解决方案

无论哪种原因，问题总得需要解决，接下来，提供几个解决方案，彻底解决当前遇见的问题。


### 方案1：在 conftest.py 中强制注册标记（最可靠）

在 `conftest.py` 的 `pytest_configure` 函数开头添加：

```python
def pytest_configure(config):
    """Pytest 初始化钩子"""
    # 关键修复：强制注册自定义标记，避免因rootdir检测问题导致的警告
    print("=== 强制注册pytest自定义标记 ===")

    # 添加自己所需的标记，确保自定义标记被注册
    markers = [
        "feature: 功能标记",
        "author: 作者标记", 
        "dependency: 依赖标记"
    ]

    for marker in markers:
        config.addinivalue_line("markers", marker)

    # 调试信息：确认配置加载
    print(f"pytest rootdir: {config.rootdir}")
    print(f"inipath: {config.inipath}")

    # ... 原有代码
```

### 方案2：修改 run_tests.py 中的 pytest 调用方式

在 `run_tests.py` 的 `run_pytest()` 函数中修改：

```python
def run_pytest():
    # ... 前面的代码
    
    # 修改pytest调用，确保正确的工作目录上下文    
    # 保存当前目录
    original_cwd = os.getcwd()
    
    try:
        # 确保在src目录中执行pytest
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # 运行pytest
        return_code = pytest.main(pytest_args)
        
    finally:
        # 恢复原始目录
        os.chdir(original_cwd)
    
    # ... 后面的代码
```


### 方案3：在 pytest 参数中显式指定配置文件

修改 `run_tests.py` 中的 `pytest_args`，携带`-c`参数，指定固定路径的`pytest.ini`文件:

```python
def run_pytest():
    # ... 前面的代码
    
    # 获取pytest.ini的绝对路径
    pytest_ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pytest.ini')
    # or
    # pytest_ini_path = os.path.join(os.getcwd(), 'pytest.ini')
    
    pytest_args = [
        "-c", pytest_ini_path,  # 显式指定配置文件
        "--alluredir", f"{json_path}",
        "--clean-alluredir",
        f"--automation-type={args.automation_type}",
        r"--cov=.",
        f"--cov-report=xml:{cov_path}"
    ]
    
    # ... 后面的代码
```


### 方案4：使用 subprocess 调用 pytest（最彻底）

修改 `run_tests.py`，使用 `subprocess` 而不是 `pytest.main()`：

```python
def run_pytest():
    # ... 前面的代码
    
    # 使用subprocess确保完整的pytest环境
    import subprocess
    
    # 构建完整的pytest命令
    pytest_cmd = [sys.executable, '-m', 'pytest'] + pytest_args
    
    # 在src目录下执行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    result = subprocess.run(
        pytest_cmd, 
        cwd=script_dir,  # 关键：指定工作目录
        capture_output=True,
        text=True
    )
    
    # 输出结果
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return_code = result.returncode
    
    # ... 后面的代码
```




### 解决方案的核心

既然 `rootdir` 检测出现了偏差，最可靠的解决方案是**不依赖自动检测**，而是：

1. **在 conftest.py 中强制注册标记**（不依赖配置文件）
2. **显式指定配置文件路径**（绕过自动检测）
3. **确保正确的执行上下文**（控制工作目录）

这就是为什么我之前推荐在 `conftest.py` 中强制注册标记是最可靠的方案 - 它完全绕过了 `pytest` 的 `rootdir` 检测机制，直接确保标记被正确注册。

