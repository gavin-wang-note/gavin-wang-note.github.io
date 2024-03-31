---
title: Allure属性装饰器优化
date: 2024-04-01 00:53:31
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: Pythonic的Allure特性封装
categories:
    - [Automation]
    - [Allure]
tags:
    - Automation
    - Allure
---

# 概述

Allure HTML报告的强大之处在于它提供了丰富的属性来详细描述测试用例的每一个方面。这些属性不仅让报告内容更加全面，还增加了测试用例的可追溯性、可读性和沟通效率。通过精确的标签，团队成员可以快速理解每个测试的目的、重要性以及与之相关的问题。

# Allure示例

下面，我们提供一个代码示例，使用pytest编写一个测试用例，并用Allure装饰器来注解，从而丰富报告内容：

```python
import pytest
import allure

@allure.feature('登录功能')
@allure.story('用户正常登录')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://documentation.mysite.com/login-feature', name='登录模块文档')
@allure.issue('https://issue-tracker.mysite.com/issues/123', '登录失败的已知Bug')
@allure.testcase('https://test-tracker.mysite.com/case/456', '登录成功的测试案例')
@allure.title('正常情况下用户能够登录')
def test_login_functionality():
    pass
```

在上述代码中，我们使用了如下Allure装饰器：

* @allure.feature 标记了此测试属于哪个较大的功能模块。
* @allure.story 描述了具体的用户故事或测试场景。
* @allure.title 提供了对测试用例简明扼要的描述。
* @allure.severity 标出了测试用例的严重程度或优先级。
* @allure.link 提供了相关功能的文档链接。
* @allure.issue 提供了与已知Bug关联的链接。
* @allure.testcase 提供了测试案例的追踪链接。

当运行这个测试并生成Allure报告时，所有这些细节都会在报告中呈现，使其他团队成员能够轻松查看测试用例的所有相关信息。

# 优化

要使代码更 Pythonic 并优化用于 Allure 特性设置的代码重复，你可以创建一个装饰器工厂函数，将所有 Allure 相关的设置封装起来。这样的封装可以让你的测试用例代码更简洁、易读，并减少重复代码。以下是一个改进的例子：

```python
import pytest
import allure

def allure_attributes(feature, story, title, severity, link=None, issue=None, test_case=None):
    def wrap(func):
        func = allure.feature(feature)(func)
        func = allure.story(story)(func)
        func = allure.title(title)(func)
        func = allure.severity(severity)(func)
        if link:
            func = allure.link(link[0], name=link[1])(func)
        if issue:
            func = allure.issue(issue[0], name=issue[1])(func)
        if test_case:
            func = allure.testcase(test_case[0], name=test_case[1])(func)
        return func
    return wrap

@allure_attributes(
    feature='登录功能',
    story='用户正常登录',
    title='正常情况下用户能够登录',
    severity=allure.severity_level.CRITICAL,
    link=('https://documentation.mysite.com/login-feature', '登录模块文档'),
    issue=('https://issue-tracker.mysite.com/issues/123', '登录失败的已知Bug'),
    test_case=('https://test-tracker.mysite.com/case/456', '登录成功的测试案例')
)
def test_login_functionality():
    pass
```

这里，allure_attributes 函数是一个装饰器工厂函数，它允许你传递所有需要的参数，并在内部应用相应的 Allure 装饰器。这样所有的 Allure 相关设置都被整齐地封装进一个单独的声明中，使得最终的测试用例函数保持其清晰和目的性。


## 再次优化

上述的优化，每次都要传递那么几个固定的参数，不利于后期的拓展，毕竟allure能携带的属性信息还是非常的多的。考虑到此，再次优化一下,希望通过`**kwargs`来传递不确定的Allure属性参数，这将提供更大的灵活性。


```python
import pytest
import allure

def allure_attributes(**kwargs):
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
```

在这个版本中，allure_attributes函数通过`**kwargs`接收任意数量的命名参数，这些参数应对应于Allure提供的装饰器。该装饰器在内部检查了Allure模块是否拥有对应的属性，并适当地对函数应用了装饰器，以此来附加相应的测试元数据。

