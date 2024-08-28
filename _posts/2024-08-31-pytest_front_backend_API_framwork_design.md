---
title: 前后端产品API自动化测试框架设计
date: 2024-08-31
author: Gavin Wang
img: "/img/pytest/pytest-22.jpg"
top: true
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 被测产品有前后端Web，针对前后端API，基于pytest+requests+allure进行自动化测试框架设计与测试用例编写
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

此次被测产品是一个拥有前后端`Web`管理的平台，但并不会去做`Web`自动化，依然选择`API`自动化。
针对此次被测产品，需要基于`pytest`设计一套测试框架，最终选择老朋友`pytest+requests+allure`实现，毕竟用了这么多年比较顺手，开发效率也高。

# 框架规划

在开始编写代码之前，你应该明确你的测试目标、测试需求、测试数据的管理方式，以及如何报告测试结果。清晰的规划有助于确保你的测试框架满足项目需求。

## 规划

1.  **需求分析**

    - 确定`API`的功能、性能和安全测试需求。
    - 搞清楚`API`的业务逻辑、流程和关键操作，包括请求方法、参数、预期响应等。
    - 确定测试的范围和深度，尽量熟悉产品代码，增加业务逻辑理解，以便写出更有逻辑深度的测试用例。
    - 明确测试框架需要达成的业务目标，如提高测试效率、减少手动测试工作量等。
2.  **确定工具和技术栈**

    - 选择 `pytest` 作为测试运行器。
    - 选择合适的HTTP库，如 `requests`，用于发起API请求。
    - 确定管理测试数据和配置的格式，如 `JSON`, `YAML`, `CSV` 等。
    - 选定报告生成工具，如 `Allure`。
    - 确定使用的CI/CD工具，如 `Jenkins, GitLab CI, GitHub Actions` 等。
3.  **设计框架结构**
    - 模块化设计：设计易于维护和扩展的模块化测试框架。
    - 数据管理：规划如何处理测试数据，如使用数据驱动测试。
    - 代码复用：确保测试脚本中有高度的代码复用性。
    - 日志和报告：实现详细的日志记录和清晰的测试报告。

4.  **制定测试计划**
    - 制定测试计划可以帮助确保测试过程的有序进行。
    - 测试计划应包括测试目标、范围、工具和技术、时间表、资源分配等信息。

5.  **开发和实现**

    - 脚本编写：开发自动化测试脚本。
    - 测试用例开发：根据业务逻辑和用户场景编写测试用例，测试用例应清晰表述业务意图，避免复杂的代码逻辑。
    - 代码重用性：代码模块化，公共代码应抽象成函数或方法以便复用。
    - 业务逻辑层的抽象：将复杂的API调用链抽象成多个简单的业务逻辑函数。
    - 框架验证：验证测试框架的有效性和完整性，及时发现和修复任何错误，完善测试报告。
    - 可扩展性：框架应支持新增测试用例和功能的扩展。

6.  **维护和更新**
    - 持续维护：定期更新和维护测试脚本和框架以适应应用的变化。
    - 反馈循环：建立反馈机制以持续优化测试流程。

- 版本控制：使用版本控制系统（如`Git`）来管理代码变更。

7. **培训和文档**
   - 团队培训：确保团队成员了解和能够使用框架。
   - 文档编写：提供详细的框架使用文档和最佳实践指南。

8. **性能和效率**
   - 性能优化：确保测试运行时间和资源使用处于优化状态。
   - 并行执行：实现测试用例的并行执行以提高效率。

9. **风险管理**
   - 风险评估：识别和评估与自动化测试相关的潜在风险。
   - 备份计划：制定应对策略以应对可能出现的问题。

## 用例分层

一个典型的分层API测试框架通常包括以下几个层次：

1. **测试用例层（Test Case Layer）**
   - 这是最顶层，包括所有测试脚本和测试用例。
   - 测试用例应该是描述性的，说明了测试执行的步骤和预期结果。
   - 使用断言来验证`API`的响应与预期结果是否匹配。

2. **业务逻辑层（Business Logic Layer）或API封装层**:
   - 在这一层，将测试步骤组装成具体的业务流程。
   - 把对API端点的单独调用封装成函数，每个函数代表一个业务动作。
   - 每个业务函数可以组合多个`API`调用，封装成符合特定业务逻辑的操作。

3. **API接口层（API Interface Layer）**:
   - 这一层封装API请求的构建、发送和响应处理。
   - 它的职责包括构建请求头、请求体、处理查询参数、发送请求、获取响应和解析响应数据。
   - 通过这种方式，测试用例不直接与低层次的`HTTP`通信细节打交道。

4. **数据层（Data Layer）**:
   - 负责管理测试数据，包括但不限于请求载体、头信息、预期结果等。
   - 可以使用外部数据源，如文件、数据库或环境变量来灵活地管理测试数据。
   - 促进数据与测试逻辑的分离，便于管理和更新。

5. **配置层（Configuration Layer）**:
   - 包含测试框架的配置选项，如服务器`URLs`、测试环境设置、认证信息等。
   - 通常包括环境配置文件，如`.ini`、`.yaml`或`.json`，使得在不同环境下无需修改测试代码即可运行。

6. **工具层（Utility Layer）**:
   - 包含一组实用工具和助手函数，这些可以在测试用例中进行重复使用。
   - 可以包括日志记录、日期转换、字符串处理等通用的辅助功能。

7. **报告层（Reporting Layer）**:
   - 自动生成测试报告，通常在测试用例执行结束后进行。
   - 可利用一些库如 `pytest-html` 或 `Allure` 来生成详细的报告，包括测试结果、失败用例的截图等。

分层的好处：

* **提高代码的可重用性。** 分层可以提高代码的可重用性。例如，数据层中的代码可以被服务层和业务层重用
* **提高代码的可读性和可维护性。** 分层可以提高代码的可读性和可维护性。这有助于更容易理解和维护代码
* **提高测试效率。** 分层可以提高测试效率。这有助于更快地发现和修复错误。

## 测试用例设计规约

**说明：**

如下规则/规约，非`pytest`要求，为笔者在过往工作经历中提炼的一些规则/规约，仅供参考。

- DRY原则：`Don't Repeat Yourself`，意思就是不要写重复代码，重复代码写得越多，后续在自动化维护上耗费的代价也会越大。当发现有些代码需要在大于等于2个地方使用它时，建议把它封装为一个公共函数。

- 用例解耦：每个测试用例要能够独立执行，尽量不要与其他用例有任何顺序、依赖等关系。

- 用例无逻辑论：测试用例只是函数的调用，不含有任何业务逻辑，所有业务逻辑均在被调用函数中完成。测试用例中场景通过调用不同函数完成业务逻辑流程的构造，好处有二，其一：用例编写更简洁，逻辑更清晰；其二：业务随着产品迭代发生变更，只需修改被调函数，可避免大面积修改测试用例。

- 用例加检查点：每个用例都要添加检查点，否则用例就没有任何意义了，所有检查点均在相关公共类或基类函数中。`pytest`框架只需要使用`python`内置的`assert`进行断言检查就可以了。

- 用例与手工用例管理平台关联： 测试用例名称，需携带上手工用例管理平台的`ID`；测试用例`docstrings`需与手工用例管理平台的`Test Case Title`保持一致。如图“**测试用例名称与`docstrings`信息**”所示。

- 日志风格统一：自定义日志记录内容风格统一，且要有对齐要求，无法对齐以填空空格补齐。

- 代码规范要求：满足`python PEP8`基本要求，推荐`pylint`或`IDE`辅助检查。

- 测试用例文件名称、用例中定义的变量名称要整个`Project`全局唯一：对于测试用例中定义的变量，要保持全局唯一，当有用例出错时，可以根据这个名称，定位到是哪个用例产生了问题，因为具有唯一性，可以排除其他用例带来的干扰。


## 框架目录结构

基于上述描述与设计原则，此产品的测试框架目录结构参考如下：

```shell
.
├── clear_pyc.py
├── common
├── config
├── conftest.py
├── __init__.py
├── pytest.ini
├── report
├── run.py
├── testcase
└── testcasebase
```

- clear_pyc.py： `python&pytest cache`文件清理

- conftest.py: 存放前端和后端登录认证`session`信息

- common： 封装公共类

- config： yaml配置文件，存放被测环境`MySQL`数据库、`redis`、前端用户账密、后端管理员账密以及前后端`API`

- pytest.ini： 此配置文件预设`pytest`相关参数

- report： 生成的用例执行过程中的日志、`allure json`报告、代码覆盖率和`pylint`报告等信息

- run.py：所有测试用例执行入口，可根据指定参数执行指定测试用例，默认执行全部测试用例，以及生成·allure、pylint·和代码覆盖率报告

- testcase： 按功能点创建目录，目录下存放对应功能的测试用例，测试用例是`testcasebase`下函数的调用

- testcasebase: 按功能点创建目录，目录下存放对应功能的业务逻辑以及业务功能检查点

## 框架部分源码介绍

`conftest.py`内容片段：

```python
@pytest.fixture(scope='session', autouse=True)
def boss_session():
    session = HttpSession()
    try:
        session.boss_token_verify()
        yield session
    finally:
        session.boss_logout()


@pytest.fixture(scope='session', autouse=True)
def front_session():
    session = HttpSession()
    phone = generate_phone_number()
    try:
        session.front_login_auth(phone)
        yield session
    finally:
        session.front_logout()
```

这里定义了前端的`session`和后端的`session`，两个`session`互相独立不干扰，真正的做到了整个`pytest session`中只存在一个前端的`session`和一个后端的`session`。

`run.py`代码片段：

```python
import os
import sys
import platform
import argparse
import subprocess

from common.util import mkdir_path


def run_pylint(allure_dir):
    """
    Generate Pylint report
    :param allure_dir:
    :return:
    """
    pylint_cmd = 'pylint --rcfile=.pylintrc -f parseable -d I0011,R0801 ./'
    if 'windows' in platform.platform().lower():
        # Windows, use subprocess to get output then write to a file
        process = subprocess.Popen(pylint_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        with open(f"{allure_dir}/pylint.out", "w") as outfile:
            for line in process.stdout:
                # Write the output to a file and console
                sys.stdout.buffer.write(line)
                outfile.write(line.decode())
        process.wait()
    else:
        # Linux or macOS
        process = subprocess.run(f"{pylint_cmd} | tee {allure_dir}/pylint.out",
                                  shell=True, check=True)

def run_pytest(tests_path, allure_dir):
    """
    Run pytest cases and generate Allure HTML report and code coverage report
    :param tests_path, string, a test case path
    :param allure_dir, string, allure html report dir
    """
    env = os.environ.copy()
    mkdir_path(allure_dir)

    # Define parameters to run test cases
    pytest_cmd = [
        'pytest',
        tests_path,
        f'--alluredir={allure_dir}/json',
        '--cov=.',
        f'--cov-report=xml:{allure_dir}/coverage.xml'
    ]

    # Run pytest test cases
    print(f"{pytest_cmd}")
    subprocess.run(pytest_cmd, env=env)

    # Generate Allure report
    allure_command = f"allure generate {allure_dir}/json -o {allure_dir}/html --clean"
    subprocess.run(allure_command, capture_output=True, text=True, check=True, env=env, shell=True)

    # Generate Pylint report
    run_pylint(allure_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run pytest with allure and coverage')
    parser.add_argument(
        '--tests_path',
        action='store',
        default='testcase',
        help='Specify path to tests'
    )
    parser.add_argument(
        '--allure_dir',
        action='store',
        default='report',
        help='Specify directory to output reports'
    )
    args = parser.parse_args()

    run_pytest(args.tests_path, args.allure_dir)
    print("---------------- The End ----------------")
```

# 其他

考虑到项目保密原则，以及我个人对整个测试框架的规划与设计能力，并不存在啥技能瓶颈，实在没什么深入的东西值得我赘述的，这里就不费笔墨去介绍了。

