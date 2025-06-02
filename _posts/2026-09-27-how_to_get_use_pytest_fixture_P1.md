---
title: 测试类中获取共享fixture中session 
date: 2026-09-27 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 获取config.py中共享fixture中session
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


在 `pytest` 中，可以通过 `request` 对象的 `getfixturevalue` 方法动态获取 `conftest.py` 中定义的 `fixture`。以下是完整的代码示例和详细说明，展示如何在测试类的 `fixture` 中使用 `request.getfixturevalue` 来获取 `conftest.py` 中的 `fixture`。

# 项目结构

```shell
project/
├── conftest.py
└── tests/
    └── test_example.py
```

# 1. 在 conftest.py 中定义 fixture

在 `conftest.py` 中定义一个 `fixture`，用于模拟登录操作并返回一个 `session`。

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def login_session():
    # 前置操作：模拟登录并获取 session
    session = "模拟的登录 session"
    print(f"登录成功，获取 session: {session}")
    yield session
    # 后置操作：清理资源
    print("登出，清理 session")
```

# 2. 在测试类中使用 request.getfixturevalue 获取 fixture

在测试类中，定义一个 `fixture`，用于测试类的前置和后置操作，并在其中通过 `request.getfixturevalue` 获取 `conftest.py` 中定义的 `fixture`。

```python
# tests/test_example.py
import pytest

class TestAPI:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, request):
        # 动态获取 conftest.py 中的 fixture
        login_session = request.getfixturevalue("login_session")
        
        # 前置操作：使用 login_session 发起 API 请求
        print(f"使用 session: {login_session} 发起前置 API 请求")
        # 这里可以执行其他前置操作
        yield
        # 后置操作：执行清理
        print("执行后置清理操作")

    def test_api_request(self):
        print("测试 API 请求")
        assert True  # 示例断言

    def test_another_api_request(self):
        print("测试另一个 API 请求")
        assert True  # 示例断言
```

# 3. 运行测试

运行测试时，`pytest` 会自动识别 `conftest.py` 中的 `fixture`，并在测试类的 `fixture` 中通过 `request.getfixturevalue` 获取 `login_session`。

# 代码说明

1. **`conftest.py` 的作用**：`conftest.py` 是 `pytest` 的特殊文件，用于定义共享的 `fixture`，这些 `fixture` 可以被同一目录及其子目录下的所有测试文件使用。
2. **`fixture` 的作用域**：在示例中，`scope="session"` 表示该 `fixture` 在整个测试会话中只执行一次。
3. **动态获取 `fixture`**：在测试类的 `fixture` 中，通过 `request.getfixturevalue("login_session")` 动态获取 `conftest.py` 中定义的 `login_session`。
4. **前置和后置操作**：在测试类的 `fixture` 中，通过 `yield` 之前的代码执行前置操作，`yield` 之后的代码执行后置操作。
5. **`autouse=True`**：`autouse=True` 表示该 `fixture` 会自动应用于测试类中的所有测试方法，无需显式传递参数。

# 示例输出

运行测试后，输出如下：

```shell
登录成功，获取 session: 模拟的登录 session
使用 session: 模拟的登录 session 发起前置 API 请求
测试 API 请求
执行后置清理操作
使用 session: 模拟的登录 session 发起前置 API 请求
测试另一个 API 请求
执行后置清理操作
登出，清理 session
```

# 总结

通过 `request.getfixturevalue` 方法，可以在测试类的 `fixture` 中动态获取 `conftest.py` 中定义的 `fixture`，从而完成测试类的前置和后置操作。这种方式提供了更大的灵活性，尤其是在需要动态获取多个 `fixture` 或在复杂的测试场景中非常有用。

