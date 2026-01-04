---
title: pytest 标记的多种实现方式
date: 2028-07-18
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
summary: 多种方式实现 pytest mark
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 如何使用多个 Mark 标记装饰 pytest 测试用例

## 概述

在 `pytest` 中，`mark`（标记）是一种强大的机制，用于对测试用例进行分类、筛选和组织。有时我们需要为一个测试用例添加多个标记，比如同时标记为：
- `@pytest.mark.slow` （慢测试）
- `@pytest.mark.integration` （集成测试）
- `@pytest.mark.database` （数据库相关）

这允许我们在不同场景下灵活地运行特定子集的测试用例。

## 基础语法

**说明：**
本文以`pytest 9.0.2`做示例，并进行了验证，确保所有示例均可正常运行。

### 方式1：叠加多个装饰器（最常用）

```python
import pytest

@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.database
def test_user_registration():
    """这个测试用例同时被标记为 slow、integration 和 database"""
    # 测试逻辑
    assert True
```

**优点：**
- 代码清晰易读
- 每个标记独立明确
- 便于维护和修改

## 多种实现方式

### 方式2：使用多个独立的装饰器

```python
import pytest

# 使用循环动态添加装饰器
marks = [pytest.mark.ui, pytest.mark.slow, pytest.mark.integration]

# 手动应用每个装饰器
def test_dynamic_marks():
    pass

# 使用循环添加装饰器
for mark in marks:
    test_dynamic_marks = mark(test_dynamic_marks)

# 或者使用索引下标指定mark
@marks[0]
@marks[1]
def test_mark_method():
    pass
```

**注意：**

`pyest`的mark并不支持链式调用：

```python
# 错误的方式（会报错）：
# @pytest.mark.mark1.mark2.mark3  # ❌ 不支持这种链式调用
```

### 方式3：在类级别应用标记

```python
import pytest

# 所有测试方法都会继承这些标记
@pytest.mark.slow
@pytest.mark.integration
class TestUserAPI:
    
    @pytest.mark.database  # 额外添加数据库标记
    def test_create_user(self):
        """这个测试有 slow、integration 和 database 三个标记"""
        pass
    
    def test_get_user(self):
        """这个测试有 slow 和 integration 两个标记"""
        pass
```

### 方式4：使用 pytestmark 变量

```python
import pytest

# 在模块级别定义多个标记
pytestmark = [
    pytest.mark.integration,
    pytest.mark.api,
]

# 这个模块的所有测试都会自动添加 integration 和 api 标记
@pytest.mark.slow  # 额外添加 slow 标记
def test_endpoint():
    """这个测试有 integration、api 和 slow 三个标记"""
    pass
```

## 标记的组合使用

### 使用 pytest.param 进行参数化时添加多个标记

```python
import pytest

@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param(1, 1, marks=[pytest.mark.fast, pytest.mark.unit]),
        pytest.param(2, 4, marks=[pytest.mark.slow, pytest.mark.integration]),
        pytest.param(3, 9, marks=pytest.mark.slow),
    ]
)
@pytest.mark.math  # 所有参数化测试都有的标记
def test_square(input, expected):
    """不同参数可以有不同的标记组合"""
    assert input ** 2 == expected
```

### 使用自定义装饰器组合多个标记

```python
import pytest

# 创建组合标记的装饰器
def combined_marks(*marks):
    """将多个标记组合成一个装饰器"""
    def decorator(func):
        for mark in reversed(marks):
            func = mark(func)
        return func
    return decorator

# 使用自定义装饰器
@combined_marks(pytest.mark.slow, pytest.mark.integration, pytest.mark.database)
def test_complex_operation():
    """使用自定义装饰器一次性添加多个标记"""
    pass
```

## 自定义标记

### 注册自定义标记

在 `pytest.ini` 配置文件中注册标记：

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: integration tests
    database: tests that require database
    api: API tests
    smoke: smoke tests
    regression: regression tests
    unit: unit tests
	ui: UI tests
	fast: fast running test cases
	math: math tests
	dev: dev ENV
	prod: prod ENV
	security: security ENV
```

### 使用自定义标记

```python
import pytest

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.api
def test_api_endpoint():
    """使用自定义的 smoke、regression 和 api 标记"""
    pass
```

## 实际应用场景

### 场景1：按测试类型筛选

```python
import pytest

@pytest.mark.unit
@pytest.mark.fast
def test_calculate_sum():
    """快速单元测试"""
    pass

@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.database
def test_user_workflow():
    """慢速集成测试，需要数据库"""
    pass

# 运行命令：
# pytest -m "fast"          # 只运行快速测试
# pytest -m "integration"   # 只运行集成测试
# pytest -m "not slow"      # 排除慢速测试
```

### 场景2：测试套件组合

```python
import pytest

# 冒烟测试套件
@pytest.mark.smoke
@pytest.mark.api
def test_login():
    pass

# 回归测试套件  
@pytest.mark.regression
@pytest.mark.ui
def test_checkout_process():
    pass

# 运行命令：
# pytest -m "smoke"         # 冒烟测试
# pytest -m "regression"    # 回归测试
# pytest -m "smoke or regression"  # 两种都运行
```

### 场景3：按环境筛选

```python
import pytest

@pytest.mark.dev
@pytest.mark.fast
def test_dev_feature():
    """开发环境专用测试"""
    pass

@pytest.mark.prod
@pytest.mark.slow
@pytest.mark.security
def test_prod_security():
    """生产环境安全测试"""
    pass

# 运行命令：
# pytest -m "dev"           # 开发环境测试
# pytest -m "prod"          # 生产环境测试
```

## 注意事项

### 1. 标记名称规范
- 使用小写字母
- 可以使用下划线连接多个单词
- 避免使用 pytest 保留字

### 2. 标记冲突处理
如果多个标记有冲突，pytest 会按照以下优先级：
1. 最内层装饰器（最靠近函数的）优先
2. 类标记会被方法标记覆盖（如果需要）

### 3. 命令行使用技巧

```bash
# 运行带有特定标记的测试
pytest -m "slow and integration"

# 运行没有某个标记的测试
pytest -m "not database"

# 运行多个标记组合的测试
pytest -m "smoke or regression"

# 运行同时具有多个标记的测试
pytest -m "slow and integration and database"

# 排除多个标记
pytest -m "not slow and not integration"
```

### 4. pytest 9.0.2 中的注意事项
- 不支持 `@pytest.mark.mark1.mark2.mark3` 这样的链式调用
- 必须使用多个独立的装饰器
- 可以使用 `pytestmark` 在模块级别批量应用标记
- 可以使用 `pytest.param` 的 `marks` 参数为参数化测试的不同参数应用不同标记

### 5. 性能考虑
标记本身对测试性能影响很小，但：
- 避免过度使用标记
- 标记应该有意义，便于维护
- 定期清理不再使用的标记

## 完整示例

### 示例项目结构

```
tests/
├── conftest.py
├── pytest.ini
├── test_unit.py
├── test_integration.py
└── test_api.py
```

### pytest.ini 配置

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: integration tests
    database: tests that require database
    api: API tests
    smoke: smoke tests
    regression: regression tests
    unit: unit tests
	ui: UI tests
	fast: fast running test cases
	math: math tests
	dev: dev ENV
	prod: prod ENV
	security: security ENV
```

### 测试文件示例

```python
# test_example.py
import pytest
import time

class TestMathOperations:
    """数学运算测试类"""
    
    @pytest.mark.unit
    @pytest.mark.fast
    @pytest.mark.smoke
    def test_addition(self):
        """快速单元测试，冒烟测试"""
        assert 1 + 1 == 2
    
    @pytest.mark.unit
    @pytest.mark.fast
    @pytest.mark.regression
    def test_subtraction(self):
        """快速单元测试，回归测试"""
        assert 5 - 3 == 2


class TestUserOperations:
    """用户操作测试类"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.database
    @pytest.mark.regression
    def test_create_user(self):
        """慢速集成测试，需要数据库，回归测试"""
        # 模拟慢速操作
        time.sleep(0.5)
        assert True
    
    @pytest.mark.api
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_user_login(self):
        """API集成测试，冒烟测试"""
        assert True


# 使用自定义装饰器组合标记
def api_test(*marks):
    """自定义装饰器：组合api测试的常用标记"""
    def decorator(func):
        func = pytest.mark.api(func)
        func = pytest.mark.integration(func)
        for mark in marks:
            func = mark(func)
        return func
    return decorator

@api_test(pytest.mark.slow, pytest.mark.database)
def test_api_with_database():
    """使用自定义装饰器组合多个标记"""
    pass


# 使用参数化与多个标记组合
@pytest.mark.parametrize(
    "user_type,expected",
    [
        pytest.param(
            "admin", 
            True, 
            marks=[pytest.mark.api, pytest.mark.integration]
        ),
        pytest.param(
            "user", 
            False, 
            marks=[pytest.mark.api, pytest.mark.unit]
        ),
    ]
)
@pytest.mark.security  # 所有测试都有的标记
def test_permission_check(user_type, expected):
    """权限检查测试"""
    # 测试逻辑
    pass
```

### 运行示例

```bash
# 运行所有冒烟测试
pytest -v -m "smoke"

# 运行所有快速的非数据库测试
pytest -v -m "fast and not database"

# 运行集成测试或API测试
pytest -v -m "integration or api"

# 运行同时是回归测试且需要数据库的测试
pytest -v -m "regression and database"

# 生成测试报告
pytest -v -m "smoke or regression" --html=report.html
```

### 查看标记信息

```bash
# 查看所有可用的标记
pytest --markers

# 查看测试收集情况（包含标记信息）
pytest --collect-only

# 查看特定标记的测试
pytest -m smoke --collect-only
```

## 总结

在 `pytest 9.0.2` 中，为测试用例添加多个标记的正确方法是：

1. **使用多个独立的装饰器**（推荐）：
   ```python
   @pytest.mark.mark1
   @pytest.mark.mark2
   @pytest.mark.mark3
   ```

2. **在类级别应用标记**，让所有方法继承：
   ```python
   @pytest.mark.class_mark
   class TestClass:
       pass
   ```

3. **使用 `pytestmark` 变量**在模块级别批量应用标记

4. **使用 `pytest.param` 的 `marks` 参数**为参数化测试的不同参数应用不同标记

5. **创建自定义装饰器**来组合常用标记

避免使用不支持的链式调用语法 `@pytest.mark.mark1.mark2.mark3`，这会导致 `AttributeError`。

通过合理使用多个标记，你可以：
1. 灵活组织测试套件
2. 按需运行特定测试
3. 提高测试执行效率
4. 更好地管理测试资源
5. 实现持续集成中的智能测试选择
