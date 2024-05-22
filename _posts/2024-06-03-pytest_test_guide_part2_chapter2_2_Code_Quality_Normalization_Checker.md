---
title: 《pytest测试指南》-- 第二章 2-2 代码质量与规范化检查工具-pylint 
date: 2024-06-03 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 第二章 2-2 代码质量与规范化检查工具-pylint
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

为了保证代码质量与规范化，借助pylint生成代码质量结果，根据结果调整代码；此外可以结合Jenkins，完成pylint历史代码质量统计与监控。接下来本章节介绍pylint，以及pylint配置文件和常见 pylint 错误如何消除， 对于如何与Jenkins结合，请参考后续章节《与Jenkins结合完成CI构建》。

# 2.1 pylint介绍

## 2.1.1 pylint是什么

Pylint是一个流行的Python代码静态分析工具，它检查Python代码中的各种问题，从语法错误到代码风格问题，乃至于一些代码设计的推荐改进点。Pylint通过静态分析来捕获编程错误，帮助提升代码质量和遵循编码标准，如PEP 8。

## 2.1.2 核心特性

- 检查代码错误
- 查找代码 smells 或不良代码实践
- 审查代码复杂度和重复代码
- 验证是否遵循了编码标准（例如PEP 8）
- 提供重构建议
- 支持插件扩展，可以添加自定义检查

## 2.1.3 安装pylint

可以通过pip轻松安装Pylint：

```shell
pip install pylint
```

## 2.1.4 基本使用

使用Pylint非常简单，只需要在命令行中运行以下命令，并传入要检查的Python文件或模块：

```shell
pylint mymodule.py
```

这将输出一系列的消息，如错误（E），警告（W），重构建议（R），和约定（C）。

## 2.1.5 消息类型

Pylint结果中的消息大致分为以下几种类型：

- **(C) Conventions**：违反了编程标准和风格指南。
- **(R) Refactor**：代码可能需要重构，可能含有不必要的复杂性或冗余。
- **(W) Warnings**：警示可能的错误，如Python语法的弃用。
- **(E) Errors**：往往指代码中会导致程序无法运行的严重问题。
- **(F) Fatal**：导致Pylint无法进一步运行分析的错误，如文件无法加载。
- **(I) Information**：只是提供一些附加信息，通常是对代码的一些统计信息。

## 2.1.6 输出解析

运行Pylint后，你会得到一份详细报告，包括：

- 文件的评分（10分满分），分数低表示需要改进的地方较多。
- 每个问题标识符和消息描述
- 触发问题的代码行数和列数

## 2.1.7 配置

Pylint可以通过`pylintrc`或`.pylintrc`文件进行详细配置，你可以禁用某些消息或者设置作用域限制。

## 2.1.8 禁止检查

在代码中，可以使用特殊注释`# pylint: disable=`来忽略特定类型的检查。

示例：

```python
# pylint: disable=wildcard-import, method-hidden
from mymodule import *
...
```

## 2.1.9 与IDE集成

很多开发环境和编辑器提供了与Pylint的集成，自动在编写代码时进行检查。例如，VS Code可以利用插件来实现这一点。

## 2.1.10 CI/CD集成

Pylint也可以集成到持续集成/持续部署流程中，自动检查每次提交的代码，确保代码质量始终满足设置的标准。

## 2.1.11 使用Pylint注意事项

- 某些Pylint警告可能是误报，开发者需要对警告进行评估是否合理。
- 避免为了提高Pylint分数而过度重构工作正常的代码。
- 在需要时适当禁用Pylint检查，但不应滥用。

Pylint是一个非常有力的工具，有助于维持和改进代码的质量。然而，就像任何工具一样，最佳实践是了解何时使用它，何时根据项目的特定需求采取适当的行动。

# 2.2 pylint配置文件 .pylintrc

Pylint是一个非常强大的Python代码静态分析工具，它可以识别代码中的错误，执行代码风格检查，以及标记可疑的代码段；它可以高度定制化，让你可以根据自己的需求来调整要应用的规则。

## 2.2.1 .pylintrc 文件

`.pylintrc` 文件是Pylint的配置文件，你可以在这里设置各种参数以定制化Pylint的行为。这个文件通常位于项目的根目录下，Pylint在运行时会查找这个文件以获取配置。你也可以通过`--rcfile`参数来显式的指定配置文件的位置。如果没有`.pylintrc`文件，Pylint会使用默认设置。

.pylintrc文件包含了一系列的配置选项，下面是这个文件的主要部分：

### 2.2.1.1 [MASTER]

这部分包含了和Pylint运行有关的一般设置。

例如：

- `ignore`：可以指定要忽略的文件模式。
- `load-plugins`：可以指定要加载的Pylint插件。
- `persistent`：决定是否写入历史信息文件。
- `jobs`：指定并行执行Pylint检查的进程数（例如，jobs=4将使用四个进程）。

### 2.2.1.2 [MESSAGES CONTROL]

在这个部分，你可以选择启用或禁用具体的消息（例如，某个具体的警告或错误）。

例如：

- `disable`：禁用特定的消息。
- `enable`：启用特定的消息。

### 2.2.1.3 [BASIC]

这部分包含了基本的代码分析设置，比如代码行的长度限制和函数参数数量限制等。

例如：

- `max-line-length`：设置允许的最大代码行长度。
- `function-rgx`：正则表达式，用于匹配函数名并制定函数命名样式。

### 2.2.1.4 [VARIABLES]

涉及变量的命名规范和声明规则。

### 2.2.1.5 [FORMAT]

涉及代码格式，例如：

- `indent-string`：指定用于缩进的字符串，比如`' '` (space) 或`'\t'` (tab)。

### 2.2.1.6 [DESIGN]

设置与代码设计相关的模式，比如设置允许的最大父类数量，或者函数内变量的最大数量等。

### 2.2.1.7 [EXCEPTIONS]

定义对异常处理的检查规则。

### 2.2.1.8 [SIMILARITIES]

这一部分用于检查和标记相似和重复的代码段。

### 2.2.1.9 [SPELLING]

涉及到拼写检查的设置。

## 2.2.2 常用的配置参数和示例

例如，如果你想要忽略所有的`missing-docstring`警告，你的`.pylintrc`文件中的`[MESSAGES CONTROL]`部分可以这样设置：

```ini
[MESSAGES CONTROL]
disable=missing-docstring
```

如果你希望修改代码行最大长度的检查，可以设置`[FORMAT]`部分的相关选项：

```ini
[FORMAT]
max-line-length=120
```

如果你打算只启用一部分特定的警告，你可以进行如下设置：

```ini
[MESSAGES CONTROL]
enable=trailing-whitespace,unused-import
```

要配置忽略文件或目录，可以在`[MASTER]`部分中设置：

```ini
[MASTER]
ignore=tests/*
```

## 2.2.3 在代码中覆盖.pylintrc配置

你还可以在代码中使用特定的注释来临时使Pylint忽略某些警告：

```python
# pylint: disable=specific-warning,another-one
```

在上面的代码中，`specific-warning`和`another-one`代表你想要Pylint跳过的特定警告的名称。

## 2.2.4 生成默认的.pylintrc文件

如果你想生成一个默认配置的`.pylintrc`文件，可以在命令行中运行以下命令：

```shell
pylint --generate-rcfile > .pylintrc
```

然后你可以开始编辑这个文件，根据你的需要修改各种设置。

## 2.2.5 综合管理Pylint消息

操作`.pylintrc`文件可以让你精细管理Pylint的消息，这在维护一致的代码风格和规范中非常重要。在大型项目中，这些配置可以帮助团队成员遵循一致的代码标准，从而提高代码的可读性和维护性。

# 2.3 pylint错误消除

为了在`.pylintrc`文件中消除各种告警，通常你需要按以下步骤操作：

## 2.3.1 生成初始的`.pylintrc`文件（如果还没有）

在项目根目录下运行以下命令来生成初始的`.pylintrc`文件（如果你还没有这个文件）：

```bash
pylint --generate-rcfile > .pylintrc
```

## 2.3.2 编辑`.pylintrc`文件内的[MESSAGES CONTROL]部分

配置文件`.pylintrc`中有一个专门的部分`[MESSAGES CONTROL]`用于控制告警信息的显示。以下是示例如何修改这一部分内容来消除特定的告警：

```ini
[MESSAGES CONTROL]
disable=
    C0111, # missing-docstring
    W0702, # bare-except
    E1101, # no-member
```

这样的配置将会禁用三种告警：缺少文档字符串、裸露的except语句以及成员不存在提示。

## 2.3.3 告警的错误码及描述

Pylint的错误码通常有一个特定的前缀，表示告警的类别：

- `C` (Convention)：不符合编码风格约定的编码。
- `R` (Refactor)：代码需要重构的地方。
- `W` (Warning)：可能的代码运行错误。
- `E` (Error)：确定的代码运行错误。
- `F` (Fatal)：阻碍Pylint进一步运行的错误。

以下是一些常见的Pylint告警信息及其描述：

- `C0111 (missing-docstring)`: 代码中缺少模块、类、函数或方法的文档字符串。
- `W0702 (bare-except)`: 使用了`except:`而没有具体指定异常类型。
- `E1101 (no-member)`: 一个对象被赋予了一个Pylint认为不存在的成员。

## 2.3.4 示例说明如何消除告警

假设你的代码中有多处缺少文档字符串的情况，Pylint检查时会提醒缺少docstring，并为之分配一个ID，比如`C0111`。如果你认为这个检查在某些情况下可以忽略（比如私有函数），可以在`.pylintrc`文件中禁用它：

```ini
[MESSAGES CONTROL]
# 禁用缺少文档字符串的告警
disable=missing-docstring
```

此外，如果你想要对某个具体的文件或代码段忽略这个告警，可以在文件或代码段的顶部添加如下注释：

```python
# pylint: disable=missing-docstring
```

或者，如果你只想忽略某个具体函数或类的这个告警：

```python
class MyClass:
    # pylint: disable=missing-docstring
    def my_method(self):
        pass
```

## 2.3.5 检查告警ID

当你不确定告警的ID时，可以让Pylint输出它的所有默认消息和相应的ID。这可以通过以下命令完成：

```bash
pylint --list-msgs
```

## 2.3.6 应用`.pylintrc`文件的配置

配置完`.pylintrc`文件后，再次运行Pylint时，它将应用新的规则：

```bash
pylint your_module.py
```

Pylint将根据`.pylintrc`文件中的设置来执行检查，并忽略你指定的告警。

这样，你可以细致地控制每条告警的显示与否，以便在保证代码质量的同时，减少不必要的噪音。



## 2.3.7 修复pylint告警实践

假如存在如下一个示例告警：

```shell
root@Gavin:~/code# pylint --rcfile=.pylintrc chapter1-5/test_nose_assert.py 
************* Module .pylintrc
.pylintrc:1:0: E0015: Unrecognized option found: argument-name-hint, attr-name-hint, class-attribute-name-hint, class-name-hint, const-name-hint, function-name-hint, inlinevar-name-hint, method-name-hint, module-name-hint, variable-name-hint (unrecognized-option)
************* Module test_nose_assert
chapt1-5/test_nose_assert.py:63:28: C0303: Trailing whitespace (trailing-whitespace)
chapt1-5/test_nose_assert.py:1:0: C0114: Missing module docstring (missing-module-docstring)
chapt1-5/test_nose_assert.py:1:0: C0103: Module name "test_nose_assert" doesn't conform to '(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$' pattern (invalid-name)
chapt1-5/test_nose_assert.py:6:0: E0401: Unable to import 'tools' (import-error)
```

如何消除上述告警？

```shell
E0015 -->  在.pylintrc文件中增加```disable=E0015```
C0303: Trailing whitespace (trailing-whitespace) --> 文件中含有多余空格，多数发生于某行的尾部
```

如上，在.pylintrc文件中增加后，再次执行`pylint --rcfile=.pylintrc chapter1-5/test_nose_assert.py` 观察效果。



# 2.4 本章小结

本章节中，我们深入探讨了pylint工具的核心特性、基本使用、配置文件以及错误消除等方面。

我们首先介绍了pylint的核心特性。pylint是一个Python代码静态分析工具，用于检测潜在的问题和错误。它可以帮助开发人员提高代码的质量和可维护性，并遵循PEP 8代码风格指南，这些特性使pylint成为了优化Python代码的重要工具。

接着，我们学习了pylint的基本使用方法。我们了解了如何安装pylint，并使用命令行界面来分析Python代码。我们还学习了如何指定要分析的文件或目录，并设置分析的规则和报告输出的格式。

我们进一步讨论了pylint的配置文件。配置文件允许我们自定义分析的规则、忽略特定的错误和警告，以及指定报告的输出路径和格式。我们学习了如何创建和编辑配置文件，并通过示例展示了常见的配置选项和用法。

最后，我们探讨了pylint提供的错误消除功能。pylint可以为我们提供详细的错误信息和建议，帮助我们理解和解决代码中的问题。我们了解了如何解读和理解pylint的错误报告，并根据报告中的信息进行代码修复和改进。

通过本章的学习，我们对pylint工具的核心特性、基本使用、配置文件和错误消除有了更深入的了解。使用pylint可以帮助我们提高Python代码的质量和可维护性，减少潜在的错误和问题。
