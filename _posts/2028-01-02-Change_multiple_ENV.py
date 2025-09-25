---
title: Pytest多环境配置切换方案
date: 2028-01-02 23:00:00
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: Pytest多环境配置切换方案(YAML)
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# YAML 配置文件方案实现

`YAML` 配置文件方案是一种很好的方式，特别适合管理复杂的多环境配置。下面我提供完整的实现方案供参考：

## 方案结构

```
├── config
│   ├── environments.yaml
│   └── settings.py
├── conftest.py
├── pytest.ini
├── tests
│   └── test_example.py
└── utils
    └── environment.py
```

## 1. 环境配置文件 (config/environments.yaml) 

```yaml
default: &default
  base_url: http://default.api.example.com
  api_version: v1
  timeout: 30
  debug: false

dev:
  <<: *default
  base_url: http://dev.api.example.com
  debug: true

qa:
  <<: *default
  base_url: http://qa.api.example.com
  timeout: 60

prod:
  <<: *default
  base_url: http://prod.api.example.com
  timeout: 45
  debug: false

staging:
  <<: *default
  base_url: http://staging.api.example.com
```

## 2. 配置管理模块 (config/settings.py)

```python
import os
from pathlib import Path
from typing import Dict, Any
import yaml


class Config:
    """配置管理类"""
    
    def __init__(self, config_file=None):
        self.config_dir = Path(__file__).parent
        if config_file:
            self.config_path = Path(config_file)
        else:
            self.config_path = self.config_dir / "environments.yaml"
        self._config = None
        
    def load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件未找到: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def get_config(self, env: str = None) -> Dict[str, Any]:
        """获取指定环境的配置"""
        if self._config is None:
            self._config = self.load_config()
        
        # 如果没有指定环境，尝试从环境变量获取
        if env is None:
            env = os.environ.get("TEST_ENV", "default")
        
        # 获取环境配置，如果不存在则使用默认配置
        env_config = self._config.get(env)
        if env_config is None:
            if env != "default":
                print(f"警告: 环境 '{env}' 未找到，使用默认配置")
            env_config = self._config.get("default", {})
            
        return env_config


# 创建全局配置实例
config_manager = Config()
```

## 3. 环境工具模块 (utils/environment.py)

```python
import os
from pathlib import Path
from typing import Dict, Any
import yaml


class Config:
    """配置管理类"""
    
    def __init__(self, config_file=None):
        self.config_dir = Path(__file__).parent
        if config_file:
            self.config_path = Path(config_file)
        else:
            self.config_path = self.config_dir / "environments.yaml"
        self._config = None
        
    def load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件未找到: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def get_config(self, env: str = None) -> Dict[str, Any]:
        """获取指定环境的配置"""
        if self._config is None:
            self._config = self.load_config()
        
        # 如果没有指定环境，尝试从环境变量获取
        if env is None:
            env = os.environ.get("TEST_ENV", "default")
        
        # 获取环境配置，如果不存在则使用默认配置
        env_config = self._config.get(env)
        if env_config is None:
            if env != "default":
                print(f"警告: 环境 '{env}' 未找到，使用默认配置")
            env_config = self._config.get("default", {})
            
        return env_config


# 创建全局配置实例
config_manager = Config()
[wls@QA-APP-92 fun9]$ cat utils/environment.py 
from typing import Dict, Any
from config.settings import config_manager


def get_environment_config(env: str = None) -> Dict[str, Any]:
    """
    获取环境配置
    
    Args:
        env: 环境名称，如不指定则从环境变量或默认值获取
        
    Returns:
        环境配置字典
    """
    return config_manager.get_config(env)


def validate_config(config: Dict[str, Any]) -> bool:
    """
    验证配置是否有效
    
    Args:
        config: 配置字典
        
    Returns:
        配置是否有效
    """
    required_keys = ["base_url"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"配置缺少必需键: {key}")
    
    if not config["base_url"].startswith(("http://", "https://")):
        raise ValueError(f"base_url 格式不正确: {config['base_url']}")
    
    return True
```

## 4. Pytest 配置 (conftest.py)

```python
import pytest
from typing import Dict, Any
from utils.environment import get_environment_config, validate_config


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--env",
        action="store",
        default="default",
        help="设置测试环境: default, dev, qa, prod, staging"
    )
    # 修改选项名称以避免冲突
    parser.addoption(
        "--env-config",
        action="store",
        default=None,
        help="指定自定义配置文件路径"
    )


def pytest_configure(config):
    """Pytest配置钩子"""
    # 设置自定义配置文件路径（如果提供了）
    env_config_file = config.getoption("--env-config")
    if env_config_file:
        from config.settings import config_manager
        config_manager.config_path = env_config_file


@pytest.fixture(scope="session")
def env_config(request) -> Dict[str, Any]:
    """获取环境配置的session级fixture"""
    env = request.config.getoption("--env")
    config = get_environment_config(env)
    
    # 验证配置
    validate_config(config)
    
    return config


@pytest.fixture(scope="function")
def api_client(env_config):
    """创建API客户端fixture"""
    # 这里可以初始化API客户端，例如使用requests.Session
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    session = requests.Session()
    
    # 配置重试策略
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # 设置默认超时
    session.timeout = env_config.get("timeout", 30)
    
    yield session
    
    # 测试结束后关闭会话
    session.close()
```

## 4. 测试用例示例 (tests/test_example.py)

```python
import pytest
from typing import Dict, Any
from utils.environment import get_environment_config, validate_config


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--env",
        action="store",
        default="default",
        help="设置测试环境: default, dev, qa, prod, staging"
    )
    # 修改选项名称以避免冲突
    parser.addoption(
        "--env-config",
        action="store",
        default=None,
        help="指定自定义配置文件路径"
    )


def pytest_configure(config):
    """Pytest配置钩子"""
    # 设置自定义配置文件路径（如果提供了）
    env_config_file = config.getoption("--env-config")
    if env_config_file:
        from config.settings import config_manager
        config_manager.config_path = env_config_file


@pytest.fixture(scope="session")
def env_config(request) -> Dict[str, Any]:
    """获取环境配置的session级fixture"""
    env = request.config.getoption("--env")
    config = get_environment_config(env)
    
    # 验证配置
    validate_config(config)
    
    return config


@pytest.fixture(scope="function")
def api_client(env_config):
    """创建API客户端fixture"""
    # 这里可以初始化API客户端，例如使用requests.Session
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    session = requests.Session()
    
    # 配置重试策略
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # 设置默认超时
    session.timeout = env_config.get("timeout", 30)
    
    yield session
    
    # 测试结束后关闭会话
    session.close()
[wls@QA-APP-92 fun9]$ cat tests/test_example.py 
def test_api_endpoint(env_config, api_client):
    """测试API端点"""
    base_url = env_config["base_url"]
    endpoint = "/health"
    
    response = api_client.get(f"{base_url}{endpoint}")
    
    assert response.status_code == 200
    assert response.json().get("status") == "OK"


def test_api_with_dynamic_data(env_config, api_client):
    """测试带动态数据的API"""
    base_url = env_config["base_url"]
    endpoint = "/data"
    
    # 使用测试数据
    test_data = {"key": "value"}
    
    response = api_client.post(
        f"{base_url}{endpoint}",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code in [200, 201]
    assert "id" in response.json()


class TestAPI:
    """API测试类"""
    
    def test_multiple_endpoints(self, env_config, api_client):
        """测试多个端点"""
        base_url = env_config["base_url"]
        
        # 测试健康检查端点
        health_response = api_client.get(f"{base_url}/health")
        assert health_response.status_code == 200
        
        # 测试数据端点
        data_response = api_client.get(f"{base_url}/data")
        assert data_response.status_code == 200
```

## 5. Pytest 配置文件 (pytest.ini)

```python
[pytest]
addopts = -v --tb=short
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

## 6. 使用示例和运行方式

## 使用说明

1. **基本用法**：
   ```bash
   pytest --env=dev
   pytest --env=qa
   pytest --env=prod
   ```

2. **使用自定义配置文件**：
   ```bash
   pytest --env=dev --env-config=/path/to/custom-config.yaml
   ```

3. **带详细输出**：
   ```bash
   pytest -v --env=dev
   ```

4. **使用环境变量**：
   ```bash
   export TEST_ENV=qa
   pytest  # 会自动使用qa环境
   ```


## 方案优势

1. **配置集中管理**：所有环境配置在一个 YAML 文件中
2. **继承和覆盖**：支持默认配置和环境特定配置的合并
3. **类型安全**：配置以字典形式提供，易于访问
4. **灵活性**：支持自定义配置文件路径
5. **可扩展性**：易于添加新的环境或配置项
6. **验证功能**：内置配置结构验证

## 依赖安装

```bash
pip install pytest pyyaml requests
```

这个 YAML 配置方案提供了非常清晰和灵活的多环境管理方式，特别适合复杂的项目配置需求。
