---
title: 如何将fixture中变量传递到参数化的测试用例中
date: 2027-05-31 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 将fixture中定义的变量，传递到参数化用例中
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# pytest 中 fixture 变量传递到参数化测试用例的实现与应用

# 背景介绍

在复杂的测试场景中，我们通常需要在测试用例执行前准备一系列的测试资源，并且希望这些资源能够被多个测试用例复用。同时，为了提高测试的覆盖率和效率，我们还希望能够对测试用例进行参数化，以实现不同的输入组合和测试场景。

笔者目前碰到一个应用场景：

测试用例中需要使用`fixture`中的变量，由于场景的需要，此变量有多个，我不可能为每一个变量值写一个测试用例，于是乎最终需求是：
如何实现`pytest`中`fixture`变量传递到参数化测试用例中。


本文将基于`pytest` 框架提供的强大的 `fixture` 和参数化功能，让我们能够优雅地实现这种需求。

# 代码示例 

## fixture定义

在`pytest`中，`fixture`用于创建和管理测试所需的资源，代码片段如下所示:

```python
def release_form(configuration_platform_session):
    # 代码省略
    # .............................
    # 创建第二个表单
    create_form_2nd = self.create_form(configuration_platform_session, form_name_2nd, model_name)
    form_id_2nd = create_form_2nd['FORM_ID']
    self.stop_form(configuration_platform_session, form_id_2nd, form_name_2nd)
    
    # 新增一个备用状态的表单
    create_form_3rd = self.create_form(configuration_platform_session, form_name_3rd, model_name)
    form_id_3rd = create_form_3rd['FORM_ID']
    self.stop_form(configuration_platform_session, form_id_3rd, form_name_3rd)
    
    # 新增第四个表单，用于同名验证使用
    create_form_4th = self.create_form(configuration_platform_session, form_name_4th, model_name)
    form_id_4th = create_form_4th['FORM_ID']
    logging.info("[Setup] [End]: 完成前置条件的准备")
    
    # 将变量存储到类变量中
    cls = request.cls  # 获取测试类
    cls.form_name_1st = form_name_1st
    cls.form_name_2nd = form_name_2nd
    cls.form_name_3rd = form_name_3rd
    cls.form_name_4th = form_name_4th
    cls.form_id_1st = form_id_1st
    cls.form_id_2nd = form_id_2nd
    cls.form_id_3rd = form_id_3rd
    cls.form_id_4th = form_id_4th
    cls.model_name = model_name
    
    yield
    
    logging.info("[Teardown] [Begin]: 开始删除表单和表单模板")
    # 先删除表单
    self.delete_form(configuration_platform_session, form_id_1st, form_name_1st)
    self.stop_form(configuration_platform_session, form_id_2nd, form_name_2nd)  # 已发布状态表单需先停用，再删除
    self.delete_form(configuration_platform_session, form_id_2nd, form_name_2nd)
    self.delete_form(configuration_platform_session, form_id_3rd, form_name_3rd)
    self.delete_form(configuration_platform_session, form_id_4th, form_name_4th)
```

## 将类变量赋值给示例变量

`setup_method`在每个测试方法执行前运行，用于将类变量赋值给实例变量。

```python
def setup_method(self):
    """在每个测试方法执行前，将类变量赋值给实例变量"""
    self.model_name = self.__class___.model_name  # pylint: disable=E1101,W0201
```

## pytest参数化测试

### 参数化示例1

`pytest`的参数化功能允许我们使用不同的输入值运行同一个测试函数，代码片段参考如下：


```python
@allure_attributes(
    severity='normal',
    testcase=(f'{zentao_base_url}/zentao/testcase-view-844.html', '表单修改，必填校验')
)
@ pytest.mark.parametrize("form_id", ["form_id_1st", "form_id_2nd", "form_id_3rd"])
def test_edit_form_verify_required_field(self, configuration_platform_session, form_id, fix_form_name):
    """表单修改，必填校验"""
    form_id_value = getattr(self, form_id)
    self.update_form(configuration_platform_session,
                     form_id=form_id_value,
                     form_name="",
                     model_name=self.model_name,
                     is_normal_scene=False)
```

在这个示例中，借助`getattr(self, form_id)`获取到`fixture`中定义的变量，此时`form_id`参数被赋予了三个值：`form_id_1st`、`form_id_2nd`和`form_id_3rd`。对于每个值，测试函数`test_edit_form_verify_required_field`都会执行一次。

### 参数化示例2

```python
@allure_attributes(
    severity='normal',
    testcase=(f'{zentao_base_url}/zentao/testcase-view-845.html', '表单修改，表单名称重复校验')
)
@ pytest.mark.parametrize("form_id, form_name", [
    ("form_id_1st", "form_name_4th"),
    ("form_id_2nd", "form_name_4th"),
    ("form_id_3rd", "form_name_4th")
])
def test_edit_form_verify_name_dup(self, configuration_platform_session, form_id, form_name):
    """表单修改，表单名称重复校验"""
    form_id_value = getattr(self, form_id)
    form_name_value = getattr(self, form_name)
    self.update_form(configuration_platform_session,
                     form_id=form_id_value,
                     form_name=form_name_value,  # 修改表单名称为已经存在的第四个表单名称
                     model_name=self.model_name,
                     is_normal_scene=False)
```

在这个示例中，`form_id`和`form_name`参数被赋予了三组值。对于每组值，测试函数`test_edit_form_verify_name_dup`都会执行一次。

# getattr函数的使用

`getattr`函数用于获取对象的属性值。在上面的代码片段中，`getattr`被用于从实例中获取表单`ID`和名称的值。

```python
form_id_value = getattr(self, form_id)
form_name_value = getattr(self, form_name)
```


