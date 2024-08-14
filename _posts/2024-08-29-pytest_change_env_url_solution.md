---
title: pytest自动化测试执行环境切换的几种解决方案
date: 2024-08-29 19:33:46
author: Gavin Wang
img: "/img/pytest/pytest-9.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest自动化测试执行环境切换的几种解决方案
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

在实际企业的测试项目中，自动化测试的代码往往需要在不同的环境中进行切换，比如多套测试环境、`PROD`环境、`SIT`环境等等，并且在`DevOps`理念中，往往自动化都会与`Jenkins`（或其他工具）结合进行`CI/CD`，这里就有个问题了：一套代码情况下，如果为每套环境设置各自独立的环境配置？

当自动化代码写完成后，期望能够在不同的环境运行，这时应该把`base_url`单独拿出来，有两种方案：通过配置文件和支持命令行参数执行。

接下来我将详细讲述一下这两个方案。

# 方案一：借助pytest-base-url插件

`pytest-base-url`是`pytest`里面提供的一个管理`base-url`的一个非常实用的插件，详细信息可参考[官网](https://pypi.org/project/pytest-base-url/)。


## 安装pytest-base-url插件

需要安装`pytest-base-url`插件，如果没安装，执行如下命令进行安装：

```shell
pip install pytest-base-url
```

## 使用插件pytest-base-url

* 直接在用例里面使用`base_url`参数，当成`fixture`使用
* 写在`pytest.ini`文件中

我们来看一下示例：

### 当成fixture使用

```python
# test_demo.py
import requests
def test_example(base_url):
    assert 200 
== requests.get(base_url).status_code
```

命令行执行的时候加上 --base-url 参数

pytest --base-url http://www.example.com

此时执行用例被跳过，出现如下信息：

```shell
root@Gavin:~/test# pytest -s -v --base-url https://www.bing.com test_base_url.py 
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .* *** WARNING: sensitive url matches https://www.bing.com ***
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-28-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': 'https://www.bing.com', 'Driver': None, 'Capabilities': {}}
baseurl: https://www.bing.com
rootdir: /root/test
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

test_base_url.py::test_example SKIPPED (This test is destructive and the target URL is considered a sensitive environment. If this test is not destructive, add the 'nondestructive' marker to it. Sensitive URL: https://www.bing.com)

=================================================================================================================== 1 skipped in 0.60s ===================================================================================================================
root@Gavin:~/test#
```


解决方法是测试用例增加`@pytest.mark.nondestructive`，[参考链接](https://github.com/pytest-dev/pytest-selenium/issues/62)：

```python
import pytest
import requests


@pytest.mark.nondestructive
def test_example(base_url):
    assert 200 == requests.get(base_url).status_code
```

此时执行测试用例：

```shell
root@Gavin:~/test# pytest -s -v --base-url http://www.bing.com test_base_url.py 
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .* *** WARNING: sensitive url matches http://www.bing.com ***
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-28-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': 'http://www.bing.com', 'Driver': None, 'Capabilities': {}}
baseurl: http://www.bing.com
rootdir: /root/test
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

test_base_url.py::test_example PASSED

=================================================================================================================== 1 passed in 0.83s ====================================================================================================================
root@Gavin:~/test#
```


### pytest.ini 配置文件

在`pytest.ini`配置文件中添加`base_url`地址

#### pytest.ini文件内容
[pytest]
base_url = http://www.bing.com

这样在命令行执行时候

就可以不用带上`--base-url`参数

```shell
root@Gavin:~/test# pytest test_base_url.py 
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .* *** WARNING: sensitive url matches http://www.bing.com ***
baseurl: http://www.bing.com
rootdir: /root/test
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

test_base_url.py .                                                                                                                                                                                                                                 [100%]

=================================================================================================================== 1 passed in 0.80s ====================================================================================================================
root@Gavin:~/test#
```

**说明：**
  测试用例中`@pytest.mark.nondestructive`还是要有的。

# 方案二：使用pytest命令行参数

这里有多种方式，比如借助`sys.args`或`argparse`实现参数的传递。这里介绍`pytest`的`addoption`。

## 实现步骤

1、添加一个新的命令行选项，如`--target_url`，来接收环境值
2、在`conftest.py`文件中，使用`pytest_addoption`函数添加新选项，并使用`pytest_configure`函数获取选项值，存储到`pytest`配置中
3、在测试用例中，通过`pytest.config`获取环境值

## 代码示例

```python

# Content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption("--target_url",action="store", default="sit",
                     choices=["dev", "test", "pre", "prod"], help="set the environment for test cases")

def pytest_configure(config):
    """配置pytest环境变量"""
    # 添加环境配置到pytest环境变量中
    target_url = config.getoption("--target_url")


@pytest.fixture(scope="session", autouse=True)
def base_url(pytestconfig):
    # 从配置中获取环境变量
    target_url = pytestconfig.getoption('target_url').lower()
    print(f"target_url : ({target_url})")
    if target_url == "dev":
        return "https://dev.example.com"
    elif target_url == "test":
        return "https://test.example.com"
    elif target_url == "prod":
        return "https://prod.example.com"
    elif target_url == "pre":
        return "https://pre.example.com"
```


```python
# 在测试用例中
import pytest
import requests


@pytest.mark.nondestructive
def test_example(base_url):
    assert 200 == requests.get(base_url).status_code
```

命令行执行测试并指定环境：

```shell
pytest --target_url=dev
```

或者

```shell
pytest --target_url=test
```


# 方案三： 使用配置文件进行环境配置

使用配置文件（如`JSON, YAML, .env`等）来管理不同环境的配置，通过命令行参数或`env`环境变量指定读取哪个配置文件。

## 步骤

1、创建配置文件：为每个环境创建配置文件。
2、使用`python-dotenv`或相似库读取配置：根据输入读取相应环境的配置。
3、在测试用例中，使用读取的配置进行测试。

**说明：**:

1、请事先安装dotenv，安装命令： `pip install pytest-dotenv`
2、`dotenv`工作的核心是一个名为`.env`的文件。在这个文件中，你可以定义环境变量的键值对，`dotenv`将会读取这些信息并将其加载到Python环境中。这样，当你的应用运行时，这些环境变量就像是被设置在操作系统环境中一样。`.env`内容示例参考如下：

```shell
DB_HOST=localhost
DB_USER=root
DB_PASS=s1mpl3
```

## 示例代码

### 创建环境文件

`touch`如下`.env.xxx`文件(项目根目录下)，并写入相关内容：

`.env.dev`:

```plaintext
BASE_URL=https://dev.example.com
```

`.env.test`:

```plaintext
BASE_URL=https://test.example.com
```

`.env.prod`

```plaintext
BASE_URL=https://prod.example.com
```
`conftest.py`:

```python
# Content of conftest.py

import os

import pytest

from dotenv import load_dotenv


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")


@pytest.fixture(scope="session", autouse=True)
def load_env(pytestconfig):
    env = pytestconfig.getoption("--env")
    env_file = ".env." + env
    # 确认env_file的路径是否正确
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_path, env_file)
    # 确认加载状态
    load_status = load_dotenv(env_path)
    print(f"Loading .env file: {env_path}, Status: {load_status}")


@pytest.fixture(scope="session", autouse=True)
def base_url(load_env):
    return os.environ.get('BASE_URL')
```

在命令行执行测试，并指定环境：

```shell
pytest --env=dev
```

这种方法可以很方便地在不同运行时环境之间切换配置，同时也避免了在代码内部硬编码环境配置信息。


**注意**:

关于`dotenv`使用上的一些坑，[参考链接](https://zhuanlan.zhihu.com/p/656008764)


# 方案四：使用环境变量TEST_ENV

系统环境变量可用于存储当前测试环境的信息，测试脚本可根据环境变量读取不同的配置。

## 步骤

1、在系统中设置环境变量（例如`TEST_ENV`）。
2、在测试脚本中，根据环境变量获取相应配置。

## 示例代码

```python
# Content of conftest.py
# 设置环境变量 TEST_ENV
import os
import pytest

@pytest.fixture(scope="session")
def base_url():
    target_url = os.environ.get('TEST_ENV', 'test')  # 如果未设置，则默认为'test'
    if target_url == "dev":
        return "https://dev.example.com"
    elif target_url == "test":
        return "https://test.example.com"
    elif target_url == "prod":
        return "https://prod.example.com"
```

在命令行中设置环境变量并执行测试：

```shell
# Unix shell
export TEST_ENV=dev && pytest

# Windows Command Line
set TEST_ENV=dev && pytest
```

# 方案五：使用Python配置模块


利用`Python`配置文件，成功地根据切换环境或条件导入不同的配置。

## 示例代码

```python
# Content of config/dev.py
BASE_URL = "https://dev.example.com"
```

```python
# Content of config/test.py
BASE_URL = "https://test.example.com"
```

```python
# Content of config/prod.py
BASE_URL = "https://prod.example.com"
```


```python
# Content of conftest.py
import pytest
import importlib

def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Set the environment")

@pytest.fixture(scope="session", autouse=True)
def base_url(request):
    env = request.config.getoption("--env")
    config_module = f"config.{env}"
    config = importlib.import_module(config_module)
    return config.BASE_URL
```

选择性导入模块，根据命令行参数`--env`动态选择配置模块。



# 注意点

* 出于安全考虑，不要将敏感信息（如密码、密钥等）直接写入 `.env` 文件中。相反，应该使用更安全的方法来管理这些敏感信息，例如使用环境变量或者配置管理服务。
* `.env`文件不应该被提交到版本控制系统中，因为它可能包含敏感信息。通常，需要在`.gitignore`文件中添加`.env`来确保它不会被意外提交。

# 结语

这些方式提供了灵活地处理不同测试环境的多个策略。

选择适合的方法取决于具体的测试需求、团队习惯以及项目的复杂性。
