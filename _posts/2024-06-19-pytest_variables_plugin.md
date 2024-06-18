---
title: pytest-Variables插件与实战介绍
date: 2024-06-19 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-25.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 介绍pytest-Variables插件的功能、应用场景及实战示例
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# Overview

`pytest-variables` 是一个`pytest`插件，旨在使配置变量的管理更加简便和高效。通过配合使用此插件，你可以轻松地将配置信息（如`API`密钥、数据库连接字符串等）加载到测试环境中，从而实现测试代码与配置数据的分离。

在之前的博文中，有两篇文章，使用了`pytest-variables`插件，传递手机终端配置信息到测试用例，以此来区分不同的手机终端设备，详见对应博文：

[pytest+Appium2.5.1+Allure实现APP GUI自动化测试框架设计](https://gavin-wang-note.github.io/2024/04/20/pytest_appium_allure_app_gui/)

[多手机终端设备下测试用例名称区分](https://gavin-wang-note.github.io/2024/05/07/refine_appium_framework/)


# 功能介绍

- **加载变量**：从指定的`YAML`或`JSON`文件中加载配置变量，并作为`pytest fixture`提供给测试用例使用。
- **命令行选项**：通过命令行选项 `--variables` 指定配置文件路径。
- **集合管理**：能够在同一个文件中管理多个配置信息集合，便于根据不同环境、场景进行选择。

# 应用场景

- **API 测试**：通过配置文件管理`API`密钥、配置信息等，使得测试代码更简洁。
- **数据库测试**：从配置文件中加载数据库连接字符串、表名等信息，在不同测试场景中复用。
- **跨环境测试**：为不同测试环境（如开发、测试、生产）分别设置配置文件，方便管理和切换。

# 实战示例

接下来，我们将通过一个实际的例子详细展示 `pytest-variables` 插件的使用方法，包括如何安装、配置和在测试用例中使用。

在使用之前，请执行如下命令安装此插件：

```shell
pip install pytest-variables
```

## API测试应用场景

假设我们有一个`RESTful API`服务，需要在测试中使用不同的`API`密钥和`URL`进行测试。我们将通过 `pytest-variables` 插件来管理这些配置信息。

### 第一步：创建配置文件

创建一个`YAML`文件（如 `config.yaml`），定义多个配置集合，如 `default`、`dev` 和 `prod`，用于存储配置信息：

**config.yaml**

```yaml
default:
  api_key: "your_default_api_key"
  base_url: "https://api.example.com"

dev:
  api_key: "your_dev_api_key"
  base_url: "https://dev.api.example.com"

prod:
  api_key: "your_prod_api_key"
  base_url: "https://prod.api.example.com"
```

### 第二步：编写测试代码

创建一个`conftest.py`文件，通过 `--subset` 选项选择特定的配置部分：

**conftest.py内容**

```python
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--subset",
        action="store",
        default="default",
        help="Subset in the variables file to use"
    )

@pytest.fixture(scope="session")
def variables_subset(pytestconfig, variables):
    subset = pytestconfig.getoption("--subset")
    
    if subset not in variables:
        pytest.fail(f"Requested subset '{subset}' not found in the variables.")
    
    return variables[subset]
```

创建一个测试文件（例如 `test_api.py`），在测试用例中使用 `pytest-variables` 插件加载的配置信息：
   - 使用 `pytest fixture` 加载从配置文件中获取的配置信息。
   - 在测试用例中利用这些 `fixture` 来配置请求的 `URL` 和头信息，从而实现环境配置与测试代码分离。

**test_api.py**

```python
import requests
import pytest

@pytest.fixture(scope='session')
def base_url(variables_subset):
    return variables_subset['base_url']

@pytest.fixture(scope='session')
def api_key(variables_subset):
    return variables_subset['api_key']

def test_get_request(base_url, api_key):
    """测试GET请求"""
    url = f"{base_url}/some_endpoint"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    assert response.status_code == 200
    assert 'data' in response.json()

def test_post_request(base_url, api_key):
    """测试POST请求"""
    url = f"{base_url}/another_endpoint"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"param1": "value1", "param2": "value2"}
    response = requests.post(url, json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()['success'] is True
```

### 第三步：运行测试

在命令行中使用 `--variables` 选项运行`pytest`，指定配置文件和所需的配置集合，从而针对不同环境运行测试。

运行针对开发环境的测试：

```shell
pytest --variables=config.yaml --subset=dev
```

运行针对生产环境的测试：

```shell
pytest --variables=config.yaml --subset=prod
```

但此时用例执行会被SKIP：

```shell
root@Gavin:~/test/variables# pytest -s -v --variables=config.yaml --subset=prod
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/test/variables
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                        

test_api.py::test_get_request SKIPPED (This test is destructive and the target URL is considered a sensitive environment. If this test is not destructive, add the 'nondestructive' marker to it. Sensitive URL: https://prod.api.example.com)
test_api.py::test_post_request SKIPPED (This test is destructive and the target URL is considered a sensitive environment. If this test is not destructive, add the 'nondestructive' marker to it. Sensitive URL: https://prod.api.example.com)

=================================================================================================================== 2 skipped in 0.33s ===================================================================================================================
root@Gavin:~/test/variables# 
root@Gavin:~/test/variables# 
root@Gavin:~/test/variables# 
root@Gavin:~/test/variables# pytest -s -v --variables=config.yaml --subset=dev
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/test/variables
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                        

test_api.py::test_get_request SKIPPED (This test is destructive and the target URL is considered a sensitive environment. If this test is not destructive, add the 'nondestructive' marker to it. Sensitive URL: https://dev.api.example.com)
test_api.py::test_post_request SKIPPED (This test is destructive and the target URL is considered a sensitive environment. If this test is not destructive, add the 'nondestructive' marker to it. Sensitive URL: https://dev.api.example.com)

=================================================================================================================== 2 skipped in 0.31s ===================================================================================================================
root@Gavin:~/test/variables#
```

这是因为`pytest`发现测试用例会对敏感环境产生破坏性的影响。因此，有必要将这些破坏性测试和非破坏性测试区分开。同时通过标记（`marker`）来控制这些测试的执行。


### 使用 pytest 标记管理破坏性测试和非破坏性测试

- 区分破坏性和非破坏性测试：使用 `pytest` 的 `mark` 特性标记这些测试。
- 配置 `pytest`：在 `pytest.ini` 文件中注册自定义标记并配置相应的规则。
- 在敏感环境中跳过破坏性测试。


#### 第一步：添加 pytest.ini 配置文件

在项目根目录下创建一个 `pytest.ini` 文件，并注册 `nondestructive` 标记。

**pytest.ini**

```ini
[pytest]
markers =
    nondestructive: Mark the test as nondestructive (safe to run in sensitive environments)
```

#### 第二步：修改测试用例

使用 `pytest.mark.nondestructive` 标记非破坏性测试用例。

**test_api.py**

```python
import requests
import pytest

@pytest.fixture(scope='session')
def base_url(variables_subset):
    return variables_subset['base_url']

@pytest.fixture(scope='session')
def api_key(variables_subset):
    return variables_subset['api_key']

@pytest.mark.nondestructive
def test_get_request(base_url, api_key):
    """非破坏性测试GET请求"""
    url = f"{base_url}/some_endpoint"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    assert 'data' in response.json()

def test_post_request(base_url, api_key):
    """破坏性测试POST请求"""
    url = f"{base_url}/another_endpoint"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"param1": "value1", "param2": "value2"}
    response = requests.post(url, json=payload, headers=headers)
    
    assert response.status_code == 201
    assert response.json()['success'] is True
```

#### 第三步：修改conftest.py文件

根据环境变量或配置文件，动态跳过破坏性测试。

**修改conftest.py内容**

```python
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--subset",
        action="store",
        default="default",
        help="Subset in the variables file to use"
    )
    parser.addoption(
        "--skip-destructive",
        action="store_true",
        default=False,
        help="Skip tests marked as destructive if set"
    )

@pytest.fixture(scope="session")
def variables_subset(pytestconfig, variables):
    subset = pytestconfig.getoption("--subset")
    
    if subset not in variables:
        pytest.fail(f"Requested subset '{subset}' not found in the variables.")
    
    return variables[subset]

def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-destructive"):
        skip_destructive = pytest.mark.skip(reason="Skipping destructive tests in sensitive environment")
        for item in items:
            if not item.get_closest_marker("nondestructive"):
                item.add_marker(skip_destructive)
```

#### 第四步：运行测试

在敏感环境中运行测试时，使用 `--skip-destructive` 参数来跳过破坏性测试。

```shell
pytest --variables=config.yaml --subset=dev --skip-destructive
```

**说明：**

- `pytest.ini`：注册了 `nondestructive` 标记。
- 测试用例：使用 `@pytest.mark.nondestructive` 标记非破坏性测试。
- `conftest.py`：
  `pytest_addoption` 增加了 `--skip-destructive` 选项，用于控制是否跳过破坏性测试;
  `pytest_collection_modifyitems` 根据 `--skip-destructive` 选项动态修改测试项，跳过未标记 `nondestructive` 的测试。
- 运行测试：通过 `--skip-destructive` 参数控制测试执行，确保在敏感环境中只执行非破坏性测试。


## 数据库配置管理应用场景

在为应用程序进行数据库相关测试时，不同的测试环境（如本地开发、测试环境和生产环境）可能使用不同的数据库配置。通过 `pytest-variables` 插件，我们可以将这些配置集中管理，简化测试代码，并提高测试灵活性。

### 实战示例：数据库配置管理

#### 步骤 1：创建配置文件

首先，我们将多个环境的数据库配置信息存储在一个 YAML 文件中。

**db_config.yaml**

```yaml
default:
  db_host: "localhost"
  db_port: 5432
  db_user: "user_default"
  db_password: "password_default"
  db_name: "test_db_default"

dev:
  db_host: "dev.db.example.com"
  db_port: 5432
  db_user: "user_dev"
  db_password: "password_dev"
  db_name: "test_db_dev"

prod:
  db_host: "prod.db.example.com"
  db_port: 5432
  db_user: "user_prod"
  db_password: "password_prod"
  db_name: "test_db_prod"
```

#### 步骤 2：配置 pytest

通过 `pytest.ini` 文件注册 `nondestructive` 标记，并指定 pytest 变量。

**pytest.ini**

```ini
[pytest]
markers =
    nondestructive: Mark the test as nondestructive (safe to run in sensitive environments)
```

#### 步骤 3：编写conftest.py文件

通过 `conftest.py` 文件读取 `--variables` 和 `--subset` 命令行参数，并提供配置数据的 fixture。

**文件conftest.py内容**

```python
import pytest
import yaml

def pytest_addoption(parser):
    parser.addoption(
        "--subset",
        action="store",
        default="default",
        help="Subset in the variables file to use"
    )

@pytest.fixture(scope="session")
def variables_subset(pytestconfig, variables):
    """Fixture to get a specific subset of the variables."""
    subset = pytestconfig.getoption("--subset")
    
    if subset not in variables:
        pytest.fail(f"Requested subset '{subset}' not found in the variables.")
    
    return variables[subset]

@pytest.fixture(scope="session")
def db_config(variables_subset):
    """Fixture to provide database configuration"""
    return {
        "host": variables_subset['db_host'],
        "port": variables_subset['db_port'],
        "user": variables_subset['db_user'],
        "password": variables_subset['db_password'],
        "database": variables_subset['db_name']
    }
```

#### 步骤 4：编写测试用例

通过 `db_config fixture` 使用数据库配置，并编写实际的测试用例。

**test_db.py**

```python
import pytest
import psycopg2

@pytest.fixture(scope='session')
def db_connection(db_config):
    """Fixture to set up a database connection."""
    conn = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        dbname=db_config['database']
    )
    yield conn
    conn.close()

@pytest.mark.nondestructive
def test_db_connection(db_connection):
    """Non-destructive test to check database connection."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()
    assert result == (1,)

def test_db_insert(db_connection):
    """Destructive test to check database insert operation."""
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO test_table (column1, column2) VALUES (%s, %s) RETURNING id;", ('value1', 'value2'))
    db_connection.commit()
    cursor.execute("SELECT column1, column2 FROM test_table WHERE column1=%s AND column2=%s;", ('value1', 'value2'))
    result = cursor.fetchone()
    assert result == ('value1', 'value2')
```

#### 步骤 5：运行测试

使用以下命令运行测试，并指定`YAML`配置文件和配置子集。

运行针对开发环境的测试：

```shell
pytest --variables=db_config.yaml --subset=dev
```

运行针对生产环境的测试：

```shell
pytest --variables=db_config.yaml --subset=prod
```

**解释:**

1. **`db_config.yaml`文件**：存储多个环境下的数据库配置信息。
2. **`pytest.ini`文件**：注册 `nondestructive` 标记，用于区分破坏性和非破坏性测试。
3. **`conftest.py`文件**：
   - `pytest_addoption`：添加 `--subset` 命令行参数，选择需要使用的配置子集。
   - `variables_subset` fixture：返回特定的配置子集。
   - `db_config fixture`：从配置子集中提供数据库连接信息。
4. **`test_db.py`文件**：
   - `db_connection fixture`：根据配置提供数据库连接，并在测试结束后关闭连接。
   - `test_db_connection` 测试：非破坏性测试，验证数据库连接有效性。
   - `test_db_insert` 测试：破坏性测试，验证插入操作。



# 小结

通过 `pytest-variables` 插件，可以轻松地管理测试环境中的配置信息，将其与实际测试代码分离开来。这种方式不仅使代码更加简洁易读，而且提高了测试的灵活性和可维护性。

