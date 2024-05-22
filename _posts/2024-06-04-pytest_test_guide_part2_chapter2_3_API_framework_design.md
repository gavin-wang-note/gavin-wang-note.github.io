---
title: 《pytest测试指南》-- 第二章 2-3 pytest+requests+allure自动化测试框架设计
date: 2024-06-04 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password: Huawei123!
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 第二章 2-3 pytest+requests+allure自动化测试框架设计
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 3.1 搭建自己的接口测试框架

## 3.1.1 为何要搭建自己的测试框架

搭建自己的自动化测试框架有几个关键原因，这些原因在提高测试过程的效率、可靠性和灵活性方面起着重要作用。以下是搭建自己的自动化测试框架的主要优势：

1. **定制化和灵活性**：每个项目或公司都有其独特的需求和挑战。一个定制化的测试框架可以特别针对这些需求进行设计，解决自身工作中的痛点、难点，提供更大的灵活性，以适应特定的测试环境、工具集成和报告需求。
2. **控制和维护**：拥有自己的框架意味着对测试过程和工具有完全的控制权。这使得团队可以根据项目的演变轻松地进行必要的调整和优化。
3. **集成和兼容性**：自建框架可以更好地与现有的开发和部署工具集成，例如持续集成/持续部署（CI/CD）管道、代码库、项目管理工具等。
4. **效率和速度**：定制框架可以优化以满足特定的性能要求，如测试执行速度、资源管理和并行执行，从而提高整体的测试效率。
5. **成本控制**：虽然最初的建立可能需要时间和资源的投入，但长期来看，一个有效的定制框架可以节省时间和资源，减少对外部工具和服务的依赖，从而控制成本。
6. **团队专业化**：构建和维护自己的框架使团队成员有机会深入了解测试的内部机制，提高他们的技能和知识。
7. **安全性和合规性**：对于处理敏感数据或需要遵守特定安全标准的项目，定制化的测试框架可以确保符合这些要求，提供更好的安全性和合规性。
8. **质量保证**：一个专门为特定项目或组织设计的框架可以更加精确地针对特定的质量标准和目标进行测试。
9. **技术/工具选择灵活**：不用纠结技术/工具选型，根据测试团队的技术实力和技术功底来选择，而不要以开发工程师的技术栈来选择。工具没有好坏之分，只有合适与否。

建立团队自己的框架富有挑战，如需要专门的知识、时间和资源进行开发和维护。因此，在决定是否搭建自己的框架时，需要权衡这些因素，考虑团队的能力、项目需求和长期目标。



## 3.1.2 如何规划框架

在开始编写代码之前，你应该明确你的测试目标、测试需求、测试数据的管理方式，以及如何报告测试结果。清晰的规划有助于确保你的测试框架满足项目需求。

### 3.1.2.1 规划

1.  **需求分析**

    - 确定API的功能、性能和安全测试需求。
    - 搞清楚API的业务逻辑、流程和关键操作，包括请求方法、参数、预期响应等。
    - 确定测试的范围和深度，尽量熟悉产品代码，增加业务逻辑理解，以便写出更有逻辑深度的测试用例。
    - 明确测试框架需要达成的业务目标，如提高测试效率、减少手动测试工作量等。
2.  **确定工具和技术栈**

    - 选择 `pytest` 作为测试运行器。
    - 选择合适的HTTP库，如 `requests`，用于发起API请求。
    - 确定管理测试数据和配置的格式，如 `JSON`, `YAML`, `CSV` 等。
    - 选定报告生成工具，如 `Allure`。
    - 确定使用的CI/CD工具，如 Jenkins, GitLab CI, GitHub Actions 等。
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

- 版本控制：使用版本控制系统（如Git）来管理代码变更。

7. **培训和文档**
   - 团队培训：确保团队成员了解和能够使用框架。
   - 文档编写：提供详细的框架使用文档和最佳实践指南。

8. **性能和效率**
   - 性能优化：确保测试运行时间和资源使用处于优化状态。
   - 并行执行：实现测试用例的并行执行以提高效率。

9. **风险管理**
   - 风险评估：识别和评估与自动化测试相关的潜在风险。
   - 备份计划：制定应对策略以应对可能出现的问题。

### 3.1.2.2 用例分层

一个典型的分层API测试框架通常包括以下几个层次：

1. **测试用例层（Test Case Layer）**
   - 这是最顶层，包括所有测试脚本和测试用例。
   - 测试用例应该是描述性的，说明了测试执行的步骤和预期结果。
   - 使用断言来验证API的响应与预期结果是否匹配。

2. **业务逻辑层（Business Logic Layer）或API封装层**:
   - 在这一层，将测试步骤组装成具体的业务流程。
   - 把对API端点的单独调用封装成函数，每个函数代表一个业务动作。
   - 每个业务函数可以组合多个API调用，封装成符合特定业务逻辑的操作。

3. **API接口层（API Interface Layer）**:
   - 这一层封装API请求的构建、发送和响应处理。
   - 它的职责包括构建请求头、请求体、处理查询参数、发送请求、获取响应和解析响应数据。
   - 通过这种方式，测试用例不直接与低层次的HTTP通信细节打交道。

4. **数据层（Data Layer）**:
   - 负责管理测试数据，包括但不限于请求载体、头信息、预期结果等。
   - 可以使用外部数据源，如文件、数据库或环境变量来灵活地管理测试数据。
   - 促进数据与测试逻辑的分离，便于管理和更新。

5. **配置层（Configuration Layer）**:
   - 包含测试框架的配置选项，如服务器URLs、测试环境设置、认证信息等。
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



## 3.1.3 CI/CD 工具选择

选择CI/CD工具时要考虑以下因素：

- **与现有环境的兼容性**: 若项目已托管在GitHub上，则GitHub可能是一个顺理成章的选择。
- **支持的功能**: 确认CI/CD工具支持必要的自动化构建、测试、部署功能。
- **社区和插件生态**: 工具的插件和社区支持情况可以大幅提高工作效率。
- **维护成本**: 熟悉、易于维护和扩展的工具将有益于长期项目健康。

根据这些因素，以下是一些常用且受欢迎的CI/CD工具：

- **Jenkins**: 强大、定制化高，插件丰富。
- **GitLab CI**: 与GitLab紧密集成，易于配置和使用。
- **GitHub Actions**: 与GitHub紧密集成，适合GitHub托管项目。
- **Travis CI**: 配置简单，对开源项目免费。
- **CircleCI**: 提供强大的构建环境，易于配置。



## 3.1.4 结合被测产品选择合适工具

在部署被测产品时，选择开源部署工具或决定自研测试工具，需要结合被测产品的特殊性进行仔细考虑。以下是一些关键因素，它们将影响这一决策：

### 3.1.4.1 产品特殊性质

* **技术栈**: 产品使用的技术和框架可能需要特定的工具支持。如果市面上的工具不支持产品的技术栈，可能需要自研工具。
* **应用领域**: 产品所属领域（如金融、医疗、航空等）可能有严格的法规和测试要求，这可能会推动自研一个遵循这些标准的测试工具。
* **功能复杂性**: 如果产品拥有高度复杂的业务逻辑或工作流程，现有的部署工具可能无法满足测试需求，这时候自研可能是更好的选择。
* **安全性**: 安全敏感类型的产品可能需要特制的测试工具以符合特定的加密和数据保护标准。
* **自定义需求**: 产品可能有独特的测试需求，比如特定的数据生成需求、模拟用户行为或整合第三方服务，这些需求可能无法通过现成的工具满足。

### 3.1.4.2 成本与资源

- **预算**: 自研测试工具可能需要更多的初期投资，但长期来看可能更经济，尤其是当你需要多个授权时。
- **维护和支持**: 自研工具需要内部资源进行持续维护。考虑团队是否有能力和时间来承担这些工作。
- **时间至市场**: 如果产品急需上线，可能没有足够的时间开发自研工具，此时可能更侧重于现成工具的快速部署。

### 3.1.4.3 团队技能

- **专业知识**: 团队是否有能力开发和维护自研的测试工具？如果团队缺乏必要的技能，购买商用工具可能是更好的选择。
- **培训成本**: 对于市面上现成的工具，团队可能需要培训以熟练使用。这是决策时需要考虑的另一个因素。

### 3.1.4.4 产品未来的方向

- **扩展性**: 如果预见到产品将会快速发展和变化，那么一个能够灵活适应变化的自研工具可能是更好的长期投资。
- **复用性**: 如果测试工具可以为公司中的其他项目或产品复用，自研可能会更加划算。

### 3.1.4.5 风险评估

- **风险管理**: 使用现成工具可能面临供应商的风险，比如支持的停止或者价格变化，而这些在自研工具中可以更好地控制。

综合这些因素，决策应该基于对现有资源、能力以及长期目标的深思熟虑。在某些情况下，最佳解决方案可能是采用现成工具作为起点，并根据需要进行定制。在其他情况下，完全自研或许能提供更大的灵活性和价值。这是一个需要多方面权衡的复杂决定，最好是团队成员之间共同商议后做出。



# 3.2 工具&框架选型

结合组内人员技能分布，最终决定：

* 开发&调试环境：`Linux（Ubuntu）`
* 代码存放Git：统一管理Git代码仓库，不同被测产品版本对应不同分支
* 框架选型：使用`pytest+request+allure`完成框架设计与报告输出
* Cobbler实现ISO的批量部署：支持`VM`的部署（`ESXi&PVE`）和物理机的部署
* CI/CD工具：使用Jenkins，基于pipeline完成用例的执行；定制化邮件报告输出




# 3.3 测试用例设计规约

**说明：**

如下规则/规约，非`pytest`要求，为笔者在过往工作经历中提炼的一些规则/规约，仅供参考。

## 3.3.1 规约要求

- DRY原则：Don't Repeat Yourself，意思就是不要写重复代码，重复代码写得越多，后续在自动化维护上耗费的代价也会越大。当发现有些代码需要在大于等于2个地方使用它时，建议把它封装为一个公共函数。

- 用例解耦：每个测试用例要能够独立执行，尽量不要与其他用例有任何顺序、依赖等关系。

- 用例无逻辑论：测试用例只是函数的调用，不含有任何业务逻辑，所有业务逻辑均在被调用函数中完成。测试用例中场景通过调用不同函数完成业务逻辑流程的构造，好处有二，其一：用例编写更简洁，逻辑更清晰；其二：业务随着产品迭代发生变更，只需修改被调函数，可避免大面积修改测试用例。

- 用例加检查点：每个用例都要添加检查点，否则用例就没有任何意义了，所有检查点均在相关公共类或基类函数中。`pytest`框架只需要使用python内置的assert进行断言检查就可以了。

- 用例与手工用例管理平台关联： 测试用例名称，需携带上手工用例管理平台的ID；测试用例`docstrings`需与手工用例管理平台的Test Case Title保持一致。如图“**测试用例名称与docstrings信息**”所示。

- 日志风格统一：自定义日志记录内容风格统一，且要有对齐要求，无法对齐以填空空格补齐。

- 代码规范要求：满足`python PEP8`基本要求，推荐`pylint`或`IDE`辅助检查。

- 测试用例文件名称、用例中定义的变量名称要整个Project全局唯一：对于测试用例中定义的变量，比如文件名称、图片名称、任务名称、目录名称、卷名称、Pool名称、cephfs 名称、用例执行过程中产生的文件的名称等等，要保持全局唯一，即所有用例中不出现同名的文件名、目录名、Pool 名等。当有用例出错时，可以根据这个名称，定位到是哪个用例产生了问题，因为具有唯一性，可以排除其他用例带来的干扰。



## 3.3.2 示例说明

### 3.3.2.1 用例与手工用例管理平台关联

<img class="shadow" src="/img/in-post/测试用例名称与doc信息.png" width="600">

<Center>测试用例名称与docstrings信息</Center>

如上图，```test_9143_same_daemon_different_signal```为`pytest`测试用例名称， 对应 `TestLink` 的用例为：```Sc-9143:Same daemon, different signal core file```，这部分信息写在 `docstrings`里，除此之外，可以借助allure增加用例的附属信息，包括Test Case Title，与上图中所示并不冲突。



### 3.3.2.2 日志风格统一

日志记录，执行具体操作的记录，开头增加[Action]，表明这条日志后面的动作是要执行某个具体的动作，如创建、删除、修改等动作；

检查相关的记录，开头增加[Check]，表明这条日志后面的动作是要进行一些检查点的检查;

断言记录的 log，对于出错的log，开头增加[ERROR]； 对于操作成功的 log，开头增加[Success]；对于不需要检查点的或需要跳过某些信息的log，开头增加[Skip]；

日志的具体对齐格式要求如下：

* [Prepare]后面跟2个空格
* [Action]后面跟3个空格
* [Start]后面跟4个空格
* [Check]后面跟4个空格
* [Success]后面跟2个空格
* [Skip]后面跟5个空格
* debug级别的log，内容前面跟2个--，之后再加2个空格，如`logging.debug('--  smb : (%s)', smb)`
* assert中，[ERROR] 后面跟 2个空格

在这样的规则要求下，日志的输出相对比较对齐，给阅读带来一定的便利性。



### 3.3.2.3 代码规范化要求

测试代码要满足`python PEP8`的基本要求，可以借助 `pylint`对代码进行检查，确保检查结果分值`=10`，满分是10分，命令示例如下：

```shell
pylint -r y testcasebase/Virtual_Storage/vs_user.py --rcfile=./pylintrc
```

MESSAGE_TYPE 有如下几种：

* (C) 惯例。违反了编码风格标准
* (R) 重构。写得非常糟糕的代码。
* (W) 警告。某些 Python 特定的问题。
* (E) 错误。很可能是代码中的错误。
* (F) 致命错误。阻止 `pylint` 进一步运行的错误



关于`pylint`的介绍，详请参考《Chapter 2-3 pylint》章节内容。



# 3.4 框架设计介绍

## 3.4.1 框架目录结构

```shell
.
├── doc
│   └── pytest_Automation_Documentation.pdf
├── jenkins
│   ├── edit_email_template.py
│   ├── jenkins_build_properties.sh
│   ├── pytest_80_pipeline
│   ├── rsync_pytest.sh
│   ├── rsync_report.sh
│   ├── v1.1_allure-pipeline-report.groovy
│   └── v1.1_Jenkinsfile.txt
├── python_3rd_lib
│   ├── allure-commandline-2.13.2.zip
│   ├── allure-pytest-2.8.11.tar
│   ├── allure-python-commons-2.8.11.tar.gz
│   ├── astroid-1.5.3.tar.gz
│   ├── ........其他安装包.........
│   ├── toml-0.10.2.tar.gz
│   ├── unzip-6.0-21.el7.x86_64.rpm
│   ├── unzip_6.0-4ubuntu2.5_amd64.deb
│   ├── wcwidth-0.2.2.tar.gz
│   └── zipp-1.0.0.tar.gz
├── report
│   └── pytest_autotest.log
└── src
    ├── clear_pyc.py
    ├── common
    │   ├── aws_cli.py
    │   ├── bigtera_api.py
    │   ├── bigtera_cluster.py
    │   ├── bigtera_errors.py
    │   ├── config.py
    │   ├── http_session.py
    │   ├── __init__.py
    │   ├── login.py
    │   ├── path_util.py
    │   ├── tools
    │   │   ├── __init__.py
    │   │   └── trivial.py
    │   └── util.py
    ├── config
    │   ├── autotest_11_12_13.config
    │   ├── autotest_15_16_17.config
    │   ├── autotest_18_19_20.config
    │   ├── autotest_21_22_23.config
    │   ├── autotest_24_25_26.config
    │   ├── autotest_57_58_59.config
    │   ├── autotest_centos_11_12_13.config
    │   ├── autotest_centos_15_16_17.config
    │   ├── autotest_centos_18_19_20.config
    │   ├── autotest_centos_21_22_23.config
    │   ├── autotest_centos_24_25_26.config
    │   ├── autotest_centos_57_58_59.config
    │   └── autotest.config
    ├── conftest.py
    ├── __init__.py
    ├── prepare
    │   ├── create_cluster
    │   │   ├── create_cluster.py
    │   │   ├── __init__.py
    │   │   └── test_cluster_creation_wizard.py
    │   ├── __init__.py
    │   └── setup_cluster
    │       ├── __init__.py
    │       ├── recreate_raid.py
    │       └── test_config_cluster.py
    ├── .pylintrc
    ├── pytest.ini
    ├── run.py
    ├── testcase
    │   ├── Basic_Stability_Test
    │   │   ├── case_1_Cluster_Full_Scenario
    │   │   │   └── __init__.py
    │   │   ├── case_2_Daemon_Action
    │   │   │   ├── __init__.py
    │   │   │   └── test_restart_mds_mon_mgr.py
    │   │   ├── case_3_Disconnect_Network
    │   │   │   └── __init__.py
    │   │   ├── case_4_Shutdown_Node
    │   │   │   └── __init__.py
    │   │   ├── __init__.py
    │   │   ├── test_01_assign_gw_vs.py
    │   │   ├── test_02_kv_store.py
    │   │   └── test_03_os_command.py
    │   ├── conftest.py
    │   ├── Function_Test
    │   │   ├── case_01_Ezs3_Console
    │   │   │   ├── __init__.py
    │   │   │   ├── test_01_cluster_management.py
    │   │   │   ├── test_02_diagnostic.py
    │   │   │   ├── test_03_network_settings.py
    │   │   │   ├── test_04_system_tools.py
    │   │   │   ├── test_05_terminal_console.py
    │   │   │   └── test_06_upgrade.py
    │   │   ├── case_02_Accounts
    │   │   │   ├── __init__.py
    │   │   │   ├── test_01_SDS_admin_account_settings.py
    │   │   │   ├── test_02_account_ad.py
    │   │   │   ├── test_03_account_ldap.py
    │   │   │   ├── test_04_common_account_settings.py
    │   │   │   ├── test_05_login_with_SDS_admin_account.py
    │   │   │   └── test_06_s3_migrate.py
    │   │   ├── case_03_Hosts
    │   │   │   ├── 01_Cluster_Hosts
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── test_01_cluster_hosts.py
    │   │   │   │   ├── test_02_cluster_hosts_no_license.py
    │   │   │   │   ├── test_03_backup_config.py
    │   │   │   │   ├── test_04_backup_config_backend.py
    │   │   │   │   └── test_05_cluster_hosts_osd_not_join_pool.py
    │   │   │   ├── ...... 等等 其他目录与子目录 ......
    └── testcasebase
        ├── Account
        │   ├── account.py
        │   ├── __init__.py
        │   └── sds_admin.py
        ├── Basic_Stability
        │   ├── ctdb.py
        │   ├── enable_disable_role.py
        │   ├── __init__.py
        │   ├── kvstore.py
        │   ├── network.py
        │   ├── os_command.py
        │   └── restart_mds_mon.py
        ├── ...... 等等 其他目录与子目录 ......
        └── Virtual_Storage
            ├── configuration.py
            ├── __init__.py
            ├── iSCSI.py
            ├── kerberos.py
            ├── share_folder.py
            ├── virtual_storage.py
            ├── vs_group.py
            ├── vs_user.py
            └── zero_copy.py

63 directories, 372 files
```

各层目录与文件的详细介绍，请参考下文。

## 3.4.2 第一层目录介绍

### 3.4.2.1 第一层目录总览

```shell
.
├── doc
├── jenkins
├── python_3rd_lib
├── report
└── src
```

* `doc`：用于存放文档类内容，比如当前测试框架设计的介绍，再比如一些关于`pytest`相关内容介绍，`API`文档之类的内容等等。
* `jenkins`：存放CI/CD所需内容，诸如Jenkins发送邮件的模板，同步代码和汇总测试报告数据的相关脚本等文件。
* `python_3rd_lib`：由于产品与外网隔离，且需运行在产品ISO部署节点上，每次均需安装一些自动化所需的必要包才能进行自动化测试，以及配合产品携带上一些第三方和自研测试工具，辅助存储产品的功能验证。
* `report`：存放自动化用例运行期间产生的日志文件，Allure原始报告数据信息。
* `src`：为测试框架代码所在目录。

### 3.4.2.2 `jenkins`目录介绍

`jenkins`目录下文件参考如下：

```shell
  -rw-r--r-- 1 root root  3278 Jan  9 17:14 edit_email_template.py
  -rw-r--r-- 1 root root  2050 Jan  9 17:14 jenkins_build_properties.sh
  -rw-r--r-- 1 root root 14675 Jan  9 17:14 pytest_80_pipeline
  -rw-r--r-- 1 root root   537 Jan  9 17:14 rsync_pytest.sh
  -rw-r--r-- 1 root root   989 Jan  9 17:14 rsync_report.sh
  -rw-r--r-- 1 root root  7759 Jan  9 17:14 v1.1_allure-pipeline-report.groovy
  -rw-r--r-- 1 root root 13823 Jan  9 17:14 v1.1_Jenkinsfile.txt
```

* `edit_email_template.py`：用于产生`pylint`趋势图，作为邮件的附件发送到相关人员。
* `jenkins_build_properties.sh`：用于获取被测版本信息、Jenkins任务启动&结束时间等相关信息，用于Jenkins中Allure插件生成可视化HTML报告使用。
* `pytest_80_pipeline`：为`json`格式示例文件，此文件被Cobbler使用，作为被安装系统的基础配置信息。

* `rsync_pytest.sh`：同步Jenkins获取Git Server上最新代码到各个被测存储节点。
* `rsync_report.sh`：Jenkins Server用例执行结束后，将各个存储节点的测试报告原始数据同步到Jenkins Server上，汇总为一份完整的原始测试报告数据。
* `v1.1_allure-pipeline-report.groovy`：邮件模板，`edit_email_template.py`会更新此模板，形成完整的邮件报告，从而完成定制化模板的开发。此文件存放于Jenkins安装目录的`email-templates`目录下，比如：`/var/lib/jenkins/email-templates`。
* `v1.1_Jenkinsfile.txt`：Jenkins 创建pipeline任务，对应pipeline Script内容。

`jenkins`目录下各个文件内容参考如下。

#### 3.4.2.2.1 `edit_email_template.py`

此文件会在CI构建过程收尾阶段，被其他脚本调用，用于产生发送邮件所需的`pylint`质量趋势图，其内容如下：

```python
# content of edit_email_template.py
import os
import io
import re
import sys
import base64
import subprocess
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def get_build_ids(jenkins_build_path):
    build_ids = []

    files = os.listdir(jenkins_build_path)
    build_id_dirs = [f for f in files if os.path.isdir(os.path.join(jenkins_build_path, f))]
    build_id_dirs.sort()

    return build_id_dirs


def get_pylint_issues(jenkins_build_path):
    issues = {}
    build_ids = get_build_ids(jenkins_build_path)

    for each_build_id in build_ids:
        file_path = jenkins_build_path + os.sep + each_build_id + os.sep + 'pylint-outstanding-issues.xml'

        if not os.path.exists(file_path):
            print("[ERROR]  Not find the path : ({})".format(file_path))
            sys.exit(1)
        grep_cmd = 'cat {} | grep "</issue>" | wc -l'.format(file_path)
        outstanding_issues = subprocess.run(grep_cmd, shell=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, universal_newlines=True)
        issues[each_build_id] = int(outstanding_issues.stdout)

    return issues


def sort_result(issues):
    # Sort build id from small to biger
    build_ids_tmp = sorted(issues)
    build_ids = list(map(int, build_ids_tmp))
    build_ids.sort()

    # Base on build id, get volues from dict
    issue_no = []
    for each_build_id in build_ids:
        for (k, v) in issues.items():
            if int(k) == each_build_id:
                issue_no.append(v)
    print("--  build_ids : ({}), issue_no : ({})".format(build_ids, issue_no))
    return build_ids, issue_no


def generate_chart(issues):
    build_ids, issue_no = sort_result(issues)

    fig = plt.figure(figsize=(15, 7.5))
    ax = fig.add_subplot(111)
    ax.stackplot(
        build_ids,
        issue_no,
        colors=("#f4b8b8", ),
        labels=('issues', ),
    )
    ax.legend()
    # ax.set_title("History")    ax.set_xlabel("Builds")
    ax.set_ylabel("Counts")
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.set_major_locator(MultipleLocator(1))

    if max(issue_no) > 15:
        ax.yaxis.set_minor_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(5))
    else:
        ax.yaxis.set_major_locator(MultipleLocator(1))

    output = io.BytesIO()
    plt.savefig(output, bbox_inches='tight')
    output.seek(0)
    encoded = base64.b64encode(output.read())

    return f"data:image/jpg;base64,{encoded.decode('utf8')}"


def update_email_template(file, old_str, new_str):
    if not os.path.exists(file):
        print("[ERROR]  File : ({}) not eixt, exit!!!".format(file))
        sys.exit(2)

    with open(file, "r", encoding="utf-8") as file_old, open("%s.bak" % file, "w", encoding="utf-8") as file_new:
        for line in file_old:
            file_new.write(re.sub(old_str, new_str, line))
        os.remove(file)
        os.rename("%s.bak" % file, file)


if __name__ == "__main__":
    jenkins_build_path = sys.argv[1]
    email_template_path = sys.argv[2]
    old_str = sys.argv[3]
    # print(jenkins_build_path, email_template_path, old_str)

    issues = get_pylint_issues(jenkins_build_path)
    res = generate_chart(issues)

    update_email_template(email_template_path, old_str, res)
```

#### 3.4.2.2.2 `jenkins_build_properties.sh`

用于获取CI构建的起始和结束时间，被测产品版本信息，用例执行结果分布（PASS, FAILED, ERROR, SKIP, BROKEN等）状态。其内容参考如下：

```shell
# content of jenkins_build_properties.sh
#!/bin/bash

scriptrootpath=$1
# like this : scriptrootpath=/work/automation-test/pytest_8.0/pytest_framework
if [[ $1 == "" ]] && [[ "pytest_framework" =~ $1 ]]; then
    echo -e "usage: jenkins_build_properties.sh scriptrootpath"
    exit
fi

if [ ! -d ${scriptrootpath} ]; then
    mkdir ${scriptrootpath}
    chown -R jenkins.jenkins ${scriptrootpath}
fi


# Get automation start and end time for jenkins report'
time_file="$scriptrootpath/report/time.txt"
START_TIME=`cat ${time_file} | head -n 1`
echo START_TIME=${START_TIME} > $scriptrootpath/build.properties
END_TIME=`tac ${time_file} | head -n 1`
echo END_TIME=${END_TIME} >> $scriptrootpath/build.properties

# Record version
version_file="$scriptrootpath/report/version.txt"
PRODUCT_VERSION=`cat ${version_file}`
echo PRODUCT_VERSION=${PRODUCT_VERSION} >> $scriptrootpath/build.properties

export_file="$scriptrootpath/report/html/export/prometheusData.txt"
result_file="$scriptrootpath/report/result.txt"

test_counts=`cat ${export_file} | grep launch_retries_run | awk '{print $NF}'`
test_pass=`cat ${export_file} | grep launch_status_passed | awk '{print $NF}'`
test_fail=`cat ${export_file} | grep launch_status_failed | awk '{print $NF}'`
test_skip=`cat ${export_file} | grep launch_status_skipped | awk '{print $NF}'`
test_broken=`cat ${export_file} | grep launch_status_broken | awk '{print $NF}'`
test_unknown=`cat ${export_file} | grep launch_status_unknown | awk '{print $NF}'`
time_duration=`cat ${export_file} | grep launch_time_duration | awk '{print $NF}'`

echo TEST_COUNTS=${test_counts} >> $scriptrootpath/build.properties
echo TEST_PASS=${test_pass} >> $scriptrootpath/build.properties
echo TEST_FAIL=${test_fail} >> $scriptrootpath/build.properties
echo TEST_SKIP=${test_skip} >> $scriptrootpath/build.properties
echo TEST_BROKEN=${test_broken} >> $scriptrootpath/build.properties
echo TEST_UNKNOWN=${test_unknown} >> $scriptrootpath/build.properties
echo TIME_DURATION=${time_duration} >> $scriptrootpath/build.properties
```

#### 3.4.2.2.3 文件同步

由于用例运行在多套不同的存储集群中，需要将测试代码同步到各套存储集群的某个节点上，用例运行接收后再将各套存储节点产生的日志和报告合并起来，形成一份完整的测试日志和测试报告。相关`rsync`脚本参考如下：

```shell
# content of rsync_pytest.sh
#!/usr/bin/expect

if {$argc!=4} {
    send_user "usage: rsync_pytest code_path remote_host remote_user remote_password\n"
    exit
}

set code_path [lindex $argv 0]
set host [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]

set timeout 600

# spawn rsync -av --delete ../../pytest_framework  ${username}@${host}:/root/
spawn rsync -av --delete ${code_path} ${username}@${host}:/root/

expect {
"(yes/no)?" { send "yes\r"; exp_continue}
"password:" { send "$password\r" }
}

expect eof
```



```shell
# content of rsync_report.sh
#!/usr/bin/expect

if {$argc!=6} {
    send_user "usage: rsync_report remote_host remote_user remote_password report_path jenkins_work_space jenkins_ip\n"
    exit
}

set timeout 600

set host [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set report_path [lindex $argv 3]
set jenkins_work_space [lindex $argv 4]
set jenkins_host [lindex $argv 5]
set jenkins_username "jenkins"
set jenkins_password "1"
set root_password "p@ssw0rd"


spawn ssh ${username}@${host}

expect {
"(yes/no)?" { send "yes\r"; exp_continue}
"password:" { send "$password\r" }
}

expect {
"btadmin*" { send "su -\r" }
}

expect {
"Password:" { send "${root_password}\r" }
}

expect {
"root*" { send "rsync -av ${report_path} ${jenkins_username}@${jenkins_host}:${jenkins_work_space}\r" }
}

expect {
"password:" { send "${jenkins_password}\r"}
}

expect {
"root*" { send "exit\r" }
}

expect {
"btadmin*" {send "exit\r"}
}
expect eof
```

如上脚本所使用的环境变量，均来自Jenkins的工程的配置，这部分信息，请参考本书“与Jenkins结合完成CICD构建”章节相关内容。

#### 3.4.2.2.4 `v1.1_allure-pipeline-report.groovy`

此文件为Jenkins发送邮件所使用的模板，分几个区域展示：

* project信息
* 被测版本信息
* CI起始时间
* 触发原因
* 本次构建较上一次测试代码有哪些commit变化
* 构建产生的附件信息
* 测试用例状态分布，含用例总数，通过数，通过率等信息
* 各种趋势图（Allure history trend，pylint warnings trend，code coverage）

此文件内容参考如下：

```shell
# content of v1.1_allure-pipeline-report.groovy
<STYLE>
  BODY, TABLE, TD, TH, P {
    font-family: Calibri, Verdana, Helvetica, sans serif;
    font-size: 12px;
    color: black;
  }
  .console {
    font-family: Courier New;
  }
  .filesChanged {
    width: 10%;
    padding-left: 10px;
  }
  .section {
    width: 100%;
    border: thin black dotted;
  }
  .td-title-main {
    color: white;
    font-size: 200%;
    padding-left: 5px;
    font-weight: bold;
  }
  .td-title {
    color: white;
    font-size: 120%;
    font-weight: bold;
    padding-left: 5px;
    text-transform: uppercase;
  }
  .td-title-tests {
    font-weight: bold;
    font-size: 120%;
  }
  .td-header-maven-module {
    font-weight: bold;
    font-size: 120%;    
  }
  .td-maven-artifact {
    padding-left: 5px;
  }
  .tr-title {
    background-color: <%= (build.result == null || build.result.toString() == 'SUCCESS') ? '#27AE60' : build.result.toString() == 'FAILURE' ? '#E74C3C' : '#f4e242' %>;
  }
  .test {
    padding-left: 20px;
  }
  .test-fixed {
  	font-weight: bold;
    font-size: 120%;
    color: #27AE60;
  }
  .test-failed {
  	font-weight: bold;
    font-size: 120%;
    color: #FF0000;
  }
  .test-passed {
  	font-weight: bold;
    font-size: 120%;
    color: #008000;
  }
  .test-skiped {
  	font-weight: bold;
    font-size: 120%;
    color: #3366ff;
  }
  .test-broken {
   	font-weight: bold;
    font-size: 120%;
    color: #800000;
  }
</STYLE>
<BODY>
  <!-- BUILD RESULT -->
  	<%
        def envOverrides = it.getAction("org.jenkinsci.plugins.workflow.cps.EnvActionImpl").getOverriddenEnvironment()
        product_version = envOverrides["PRODUCT_VERSION"]
    %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title-main" colspan=2>
        BUILD ${build.result ?: 'COMPLETED'}
      </td>
    </tr>
    <tr>
      <td>URL:</td>
      <td><A href="${rooturl}${build.url}">${rooturl}${build.url}</A></td>
    </tr>
    <tr>
      <td>Project:</td>
      <td>${project.name}</td>
    </tr>
    <tr>
    <tr>
      <td>Product Version:</td>
      <td>${product_version}</td>
    </tr>
    <tr>
      <td>Date:</td>
      <td>${it.timestampString}</td>
    </tr>
    <tr>
      <td>Duration:</td>
      <td>${build.durationString}</td>
    </tr>
    <tr>
      <td>Cause:</td>
      <td><% build.causes.each() { cause -> %> ${hudson.Util.xmlEscape(cause.shortDescription)} <%  } %></td>
    </tr>
  </table>
  <br/>

  <!-- CHANGE SET -->
  <%
  def changeSets = build.changeSets
  if(changeSets != null) {
    def hadChanges = false %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">CHANGES</td>
    </tr>
    <% changeSets.each() { 
      cs_list -> cs_list.each() { 
        cs -> hadChanges = true %>
    <tr>
      <td>
        Revision
        <%= cs.metaClass.hasProperty('commitId') ? cs.commitId : cs.metaClass.hasProperty('revision') ? cs.revision : cs.metaClass.hasProperty('changeNumber') ? cs.changeNumber : "" %>
        by <B><%= cs.author %></B>
      </td>
      <td>${cs.msgAnnotated}</td>
    </tr>
        <% cs.affectedFiles.each() {
          p -> %>
    <tr>
      <td class="filesChanged">${p.editType.name}</td>
      <td>${p.path}</td>
    </tr>
        <% }
      }
    }
    if ( !hadChanges ) { %>
    <tr>
      <td colspan="2">No Changes</td>
    </tr>
    <% } %>
  </table>
  <br/>
  <% } %>

<!-- ARTIFACTS -->
  <% 
  def artifacts = build.artifacts
  if ( artifacts != null && artifacts.size() > 0 ) { %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title">BUILD ARTIFACTS</td>
    </tr>
    <% artifacts.each() {
      f -> %>
      <tr>
        <td>
          <a href="${rooturl}${build.url}artifact/${f}">${f}</a>
      </td>
    </tr>
    <% } %>
  </table>
  <br/>
  <% } %>

<!-- MAVEN ARTIFACTS -->
  <%
  try {
    def mbuilds = build.moduleBuilds
    if ( mbuilds != null ) { %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title">BUILD ARTIFACTS</td>
    </tr>
      <%
      try {
        mbuilds.each() {
          m -> %>
    <tr>
      <td class="td-header-maven-module">${m.key.displayName}</td>
    </tr>
          <%
          m.value.each() { 
            mvnbld -> def artifactz = mvnbld.artifacts
            if ( artifactz != null && artifactz.size() > 0) { %>
    <tr>
      <td class="td-maven-artifact">
              <% artifactz.each() {
                f -> %>
        <a href="${rooturl}${mvnbld.url}artifact/${f}">${f}</a><br/>
              <% } %>
      </td>
    </tr>
            <% }
          }
        }
      } catch(e) {
        // we don't do anything
      } %>
  </table>
  <br/>
    <% }
  } catch(e) {
    // we don't do anything
  } %>

<!-- Allure Result -->
<%
  lastAllureReportBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureReportBuildAction.class)
  if (lastAllureReportBuildAction) {
    allureResultsUrl = "${rooturl}${build.url}allure"
    allureLastBuildSuccessRate = String.format("%.2f", lastAllureReportBuildAction.getPassedCount() * 100f / lastAllureReportBuildAction.getTotalCount())
  }
%>

<%
pylintResultsUrl = "${build.environment['JOB_URL']}warnings50/trendGraph"
coberturaResultsUrl = "${rooturl}${build.url}cobertura"
%>

<%
   def total = lastAllureReportBuildAction.getPassedCount() + lastAllureReportBuildAction.getFailedCount() + lastAllureReportBuildAction.getSkipCount() + lastAllureReportBuildAction.getBrokenCount()
%>

  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="7">Test Cases Status</td>
    </tr>
    <tr>
        <td class="td-title-tests">Name</td>
        <td class="test-fixed">Total</td>
        <td class="test-passed">Passed</td>
        <td class="td-title-tests">Success Rate</td>
        <td class="test-failed">Failed</td>
        <td class="test-skiped">Skipped</td>
        <td class="test-broken">Broken</td>
      </tr>
    <tr>    	
      <td>${project.name}</td>
      <td class="test-fixed">${total}</td>
      <td class="test-passed">${lastAllureReportBuildAction.getPassedCount()}</td>
      <td  class="test-fixed">${allureLastBuildSuccessRate}% </td>
      <td class="test-failed">${lastAllureReportBuildAction.getFailedCount()}</td>
      <td class="test-skiped">${lastAllureReportBuildAction.getSkipCount()}</td>
      <td  class="test-broken">${lastAllureReportBuildAction.getBrokenCount()}</td>
    </tr>
  </table>

<br> </br>

<!-- CI of Allure/Pyline/Cobertura -->
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">Allure history trend</td>
    </tr>
  </table>

  <table>
    <tr>
       <img lazymap="${allureResultsUrl}/graphMap" src="${allureResultsUrl}/graph" width="500px" height="200px"/>
    </tr>
  </table>

<br> </br>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">PyLint Warnings Trend</td>
    </tr>
  </table>

  <table>
    <tr>
        <img src="EMAIL_BASE64_IMG_REPLACE" width="500px" height="200px"/>
    </tr>
  </table>

<br> </br>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">Code Coverage</td>
    </tr>
  </table>

  <table>
    <tr>
        <img lazymap="${coberturaResultsUrl}/graphMap" src="${coberturaResultsUrl}/graph" width="500px" height="200px"/> 
   </tr>
  </table>

<!-- CONSOLE OUTPUT -->
  <%
  if ( build.result == hudson.model.Result.FAILURE ) { %>
  <table class="section" cellpadding="0" cellspacing="0">
    <tr class="tr-title">
      <td class="td-title">CONSOLE OUTPUT</td>
    </tr>
    <% 	build.getLog(100).each() {
      line -> %>
	  <tr>
      <td class="console">${org.apache.commons.lang.StringEscapeUtils.escapeHtml(line)}</td>
    </tr>
    <% } %>
  </table>
  <br/>
  <% } %>
</BODY>
```

#### 3.4.2.4.5 `v1.1_Jenkinsfile.txt`

此文件为创建pipeline风格的Jenkins工程

```ini
# content of v1.1_Jenkinsfile.txt
#!groovy

ip_list = IPS.split(',')
ips_size = ip_list.size()

def cluster1_ip = ip_list[0..2][1]
def cluster2_ip = ip_list[4..6][1]
def cluster3_ip = ip_list[7..9][1]
def cluster4_ip = ip_list[10..12][1]
def cluster5_ip = ip_list[13..15][1]

def cluster_ip = "${cluster1_ip} ${cluster2_ip} ${cluster3_ip} ${cluster4_ip} ${cluster5_ip}"

/* !!! WARNING !!!
  Introduce the -n parameter, because 03Hosts and 05RRS will involve the fourth node,
  so 3Hosts and 05RRS need to be executed in a cluster 
*/

pipeline {
    agent any

    options {
        timestamps()
        }

    stages {
        /* IP check */
        stage("IP Cheeck") {
                steps {
                    script {
                            sh """
                                if [[ ${ips_size} != 16 ]]; then
                                    echo "IPS is not enough, but give (${ips_size}) nodes to run case"
                                    exit 1
                                fi
                            """
                            }
                       }
            }

        /* Install VM by PVE */
        stage("Initialize") {
                steps {
                    script {
                            sh """
                            #!/bin/bash -xe
                            echo "Call batch_install_vs.py to install ISO."
                            # sshpass -p 1 ssh -p 22 172.17.75.236 -l root \${BAT_INSTALL}
                            """
                        }
                }
            }

        /* Get code */
        stage("Checkout") {
                steps {
                    retry(2) {
                        timeout(activity: false, time: 60, unit: 'MINUTES') {
                            checkout([$class: 'GitSCM',
                                branches: [[name: GIT_BRANCH]],
                                browser: [$class: 'GitLab', repoUrl: GIT_WEB, version: '12.8'],
                                doGenerateSubmoduleConfigurations: false,
                                extensions: [
                                    [$class: 'CleanBeforeCheckout', deleteUntrackedNestedRepositories: true],
                                    [$class: 'SubmoduleOption', recursiveSubmodules: true],
                                    [$class: 'GitLFSPull'],
                                    [$class: 'PruneStaleBranch']
                                ],
                                submoduleCfg: [],
                                userRemoteConfigs: [[url: GIT_URL]]
                            ])
                        }
                    }
                }
            }

        /* scp code to nodes */
        stage("Sync Code to Cluster Nodes") {
                steps {
                    script {                            
                            sh """
                            #!/bin/bash -xe
                            cd \${WORK_SPACE};
                            rm -rf build.properties;
                            rm -rf report;
                            cd jenkins;
                            chmod a+x *.sh;
                            for each_ip in ${cluster_ip}
                                do
                                    echo "Scp code to node : \${each_ip}"
                                    ssh-keygen -f '$HOME/.ssh/known_hosts' -R \${each_ip};
                                    ./rsync_pytest.sh \${WORK_SPACE} \${each_ip} root p@ssw0rd
                                    sleep 1
                                done
                            """
                        }
                    }
            }

        // Parallel Stage
        stage('Parallel Stage to Run Cases') {
            failFast true
            parallel {
                stage('Run test case on Cluster1') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster1_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster1_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_11_12_13.config config/autotest.config;python run.py -t \"testcase/Basic_Stability_Test testcase/Function_Test/case_01_Ezs3_Console/ testcase/Function_Test/case_04_Virtual_Storages/01_Configuration testcase/Function_Test/case_06_Configuration/01_Cluster_Management testcase/Function_Test/case_03_Hosts/\" -n True \'"
                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }


                    }
                }
                stage('Run test case on Cluster2') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster2_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster2_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_15_16_17.config config/autotest.config;python run.py -t \"testcase/Function_Test/case_02_Accounts/ testcase/Function_Test/case_04_Virtual_Storages/02_FC testcase/Function_Test/case_04_Virtual_Storages/04_Virtual_Storages testcase/Function_Test/case_05_Remote_DR/ testcase/Function_Test/case_06_Configuration/03_Pool testcase/Function_Test/case_07_Statistics_Logs testcase/Function_Test/case_11_CSI testcase/Function_Test/case_10_S3/test_05_datasearch.py \"\'"

                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }
                    }
                }
                stage('Run test case on Cluster3') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster3_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster3_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_18_19_20.config config/autotest.config;python run.py -t \"testcase/Function_Test/case_04_Virtual_Storages/03_NAS \"\'"
                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }


                    }
                }
                stage('Run test case on Cluster4') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster4_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster4_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_21_22_23.config config/autotest.config;rm -rf testcase/Function_Test/case_10_S3/test_05_datasearch.py;python run.py -t \"testcase/Function_Test/case_10_S3/ \"\'"
                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }
                    }
                }
                stage('Run test case on Cluster5') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster5_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster5_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_24_25_26.config config/autotest.config;python run.py -t \"testcase/Function_Test/case_09_Enhance/ testcase/Function_Test/case_04_Virtual_Storages/05_iSCSI testcase/Function_Test/case_08_Customized_Features testcase/Function_Test/case_99_others \"\'"
                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }
                    }
                }
            }
        }

    /* Merge report */
        stage("Merge Report") {
            steps {
                script {
                    sh """
                        #!/bin/bash -xe
                        JENKINS_IP=`cat \${JENKINS_INSTALL_PATH}/jenkins.model.JenkinsLocationConfiguration.xml | grep jenkinsUrl | awk -F ':' '{{print \$2}}' | sed 's#/##g'`
                        rm -rf \${WORK_SPACE}/report/*
                        cd \${WORK_SPACE}/jenkins;
                        for each_ip in ${cluster_ip}
                            do
                                echo "Scp report from : (\${each_ip}) to jenkins node"
                                ./rsync_report.sh \${each_ip} btadmin btadmin \${REPORT_DIR} \${WORK_SPACE} \${JENKINS_IP};
                            done
                        ./jenkins_build_properties.sh \${WORK_SPACE}
                        """
                    }
            }
        }

        stage("Allure Report") {
            steps {
                script {
                    allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: 'report/json']]
                       ])
                    }
                }
        }

        /* Publish Cobertura Coverage Report */
        stage("Publish Cobertura Coverage Report") {
            steps {
                script {
                       cobertura([
                               autoUpdateHealth: false,
                               autoUpdateStability: false,
                               coberturaReportFile: 'report/coverage.xml',
                               conditionalCoverageTargets: '70, 0, 0',
                               failUnhealthy: false,
                               failUnstable: false,
                               lineCoverageTargets: '80, 0, 0',
                               maxNumberOfBuilds: 0,
                               methodCoverageTargets: '80, 0, 0',
                               onlyStable: false,
                               sourceEncoding: 'ASCII',
                               zoomCoverageChart: false
                       ])
                    }
                }
        }

        /* Generate pylint Report */
        stage('Code Quality Check') {
            steps {
                script{
                    echo "Run pylint code style check"
        		    // Ignore pylint comments via "-d C"
                    /*
        		    sh '''
        		    	. .venv/bin/activate
        			    pylint -d C -f parseable ${SOURCE_ROOT} --exit-zero | tee ${PYLINT_REPORT}
        		    '''
                    */
                }
        	}

        	post { 
                always {
                   sh 'cat report/pylint.out'
                   recordIssues healthy: 1, tools: [pyLint(name: 'PyLint', pattern: 'report/pylint.out')], unhealthy: 2
                }
            }
        }

    /* Edit Email Template */
        stage("Edit Email Template") {
            steps {
                script {
                    sh """
                        #!/bin/bash -xe
                        cp \${JENKINS_INSTALL_PATH}/email-templates/v1.1_allure-pipeline-report.groovy \${JENKINS_INSTALL_PATH}/email-templates/allure-pipeline-report.groovy
                        cd \${WORK_SPACE}/jenkins; 
                        python3 edit_email_template.py \${JOB_SPACE}/builds \${JENKINS_INSTALL_PATH}/email-templates/allure-pipeline-report.groovy EMAIL_BASE64_IMG_REPLACE
                        """
                    }
            }
        }

        /* Send Email */
        stage("Send Email") {
            steps {
                script {
                        /*
                        build_status = sh (
                            script: """curl http://127.0.0.1:8080/job/${JOB_NAME}/lastBuild/api/json | json_pp | grep result | sed 's/   \"result" : \"//g' | sed 's/",//g'""",
                            returnStdout: true
                            ).trim()
                        echo "build status  ${build_status}"
                       */

                       product_version = sh (
                            script: """sshpass -p btadmin ssh -p 22 ${cluster1_ip} -l btadmin ezs3-version""",
                            returnStdout: true
                            ).trim()
                        env.PRODUCT_VERSION = product_version

                        emailext([
                                // attachLog: true,
                                // attachmentsPattern: 'report/cgi_response_elapsed_time.txt,report/pytest_autotest.log.gz',
                                attachmentsPattern: 'report/cgi_response_elapsed_time.txt',
                                body: '${SCRIPT, template="allure-pipeline-report.groovy"}',
                                compressLog: true,
                                postsendScript: '$DEFAULT_POSTSEND_SCRIPT',
                                presendScript: '$DEFAULT_PRESEND_SCRIPT',
                                replyTo: '$PROJECT_DEFAULT_REPLYTO',
                                // subject: '${env.PROJECT_DEFAULT_SUBJECT}',
                                subject: '${JOB_NAME} - ${BUILD_DISPLAY_NAME}',
                                to: 'Gavin.Wang@163.com'
                       ])
                    }
                }
        }
    }
}
```

请注意，上述文件中的`report/cgi_response_elapsed_time.txt`为自动化用例所产生，用于记录API请求响应时间分布的原始文件，计算出耗时比较长的Top 10的API。



## 3.4.3 第二层目录介绍

### 3.4.3.1 第二层目录总览

这里主讲一下`src`目录结构：

```shell
.
├── clear_pyc.py
├── common
├── config
├── conftest.py
├── __init__.py
├── pytest.ini
├── run.py
├── testcase
└── testcasebase
```

介绍如下：

`clear_pyc.py`： 用于清理`pytest cache`目录，支持递归。

`conftest.py`：顶层`conftest.py`，记录用例起始与用例名称到`report`目录下日志文件中。

`pytest.ini`：配置文件，指定`pytest`运行参数，日志格式，以及mark标记信息。

`run.py`：整个自动化测试框架的入口，运行测试用例，并支持自动安装python_3rd_lib目录下三方文件和部署自研工具包等。



### 3.4.3.2 `pytest` 配置文件

以下为我的自动化项目中使用的 `pytest.ini` 文件内容，参考如下：

```ini
[pytest]
log_cli = false
log_level = NOTSET
log_file = ../report/pytest_autotest.log
log_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_date_format=%Y-%m-%d %H:%M:%S
log_file_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_file_date_format=%Y-%m-%d %H:%M:%S
log_cli_level = INFO
log_cli_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_cli_date_format=%Y-%m-%d %H:%M:%S

norecursedirs = .svn .git
console_output_style = count
addopts =-vrs --show-progress --cache-clear --full-trace -p no:warnings
markers =
    run
    last
    second_to_last
    margration
    NAS
    iSCSI
    S3
    FC
    Account
```

这里我主要使用：

* log记录日志，规定了log level&format&path
* 要忽略扫描测试用例的目录（如上，忽略了`.svn` 和 `.git `目录，因为`pytest`会全目录扫描，指定忽略相关目录，避免无效扫描）
* console output style

```ini
[pytest]
console_output_style = classic  # 经典样式
console_output_style = progress # 带有进度指示器的经典演示
console_output_style = count    # 像progress,但将进度显示为已完成的测试数，而不是百分比
```

具体选择哪种，根据个人喜好。

* `addopts` 更改默认命令行选项，经常要用到某些参数，又不想重复输入

```shell
addopts =  -vv        #以更详细的显示运行结果
           -m smoke   #被标记为 smoke 的用例
          --disable-warnings           # 禁用所有warnings，不建议使用，禁用范围过大, 等同于上面的 “-p no:warnings”
          --alluredir allure_results   # allure报告路径
          --maxfail=2 -rf              # 2个用例失败后退出，并给出详细信息
          --full-trace                 # 不截断任何的tracebacks，打印更详细的错误堆栈信息，默认是截断

```

当前项目中我使用的内容参考如下：

```shell
addopts =-vrs --show-progress --cache-clear --full-trace -p no:warnings
```

需要安装`pytest-progress`插件。

* `markers`自定义一些用例标记，方便自己只执行指定标记的测试用例，当前项目中我使用的参考如下：

```ini
markers =
    run
    last
    second_to_last
    margration
    NAS
    iSCSI
    S3
    FC
    Account
```

请根据自己测试需要，标记符合自己产品的相关标记，如上仅供参考。

`conftest.py`内容参考：

```python
import os
import pytest
import logging


@pytest.fixture(scope='package', autouse=True)
def testsuite_setup_teardown():
    logging.info('------------------- Start to run test case ----------------------\n')
    yield
    logging.info('------------------- End to run test case ------------------------')


@pytest.fixture(scope='function', autouse=True)
def testcase_setup_teardown():
    case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

    logging.info('----------------------- Begin -----------------------------------')
    logging.info('Current test case name : (%s)', case_name)
    yield
    logging.info('----------------------- End -------------------------------------\n')
```

这里定义了两个`fixture`

* `testsuite_setup_teardown`用户记录用例执行时的起始和结束信息。

* `testcase_setup_teardown`记录每个测试用例的名称。

### 3.4.3.3 `common`目录介绍

```shell
root@Gavin:~/framework/src/common# ll
total 220
drwxr-xr-x 3 root root  4096 Jan  9 17:15 ./
drwxr-xr-x 8 root root  4096 Jan  9 17:15 ../
-rw-r--r-- 1 root root 19830 Jan  9 17:15 aws_cli.py
-rw-r--r-- 1 root root 24225 Jan  9 17:15 bigtera_api.py
-rw-r--r-- 1 root root 86401 Jan  9 17:15 bigtera_cluster.py
-rw-r--r-- 1 root root  5714 Jan  9 17:15 bigtera_errors.py
-rw-r--r-- 1 root root  9229 Jan  9 17:15 config.py
-rw-r--r-- 1 root root 14820 Jan  9 17:15 http_session.py
-rw-r--r-- 1 root root     0 Jan  9 17:15 __init__.py
-rw-r--r-- 1 root root   711 Jan  9 17:15 path_util.py
drwxr-xr-x 2 root root  4096 Jan  9 17:15 tools/
-rw-r--r-- 1 root root 24187 Jan  9 17:15 util.py
root@Gavin:~/framework/src/common#
```

所有公共类的封装，如登录会话session，报告路径，`API` 接口，错误码，配置文件读取，访问亚马逊`AWS S3`等。

由于需要登录后才能访问存储，这里使用requests模块封装了login session，以及HTTP的接口操作，内容参考如下：

```python
# content of http_session.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  HTTP request  """

from __future__ import unicode_literals

import sys
import json
import time
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from bigtera_errors import HttpCode
from config import GetConfig as config
from bigtera_api import LoginInterface


class HttpSession(requests.Session):
    """  http request session  """

    def __init__(self):
        super(HttpSession, self).__init__()
        # Not verify SSL certificate
        self.verify = False

        # timeout time
        self.timeout = (60, 600)

        # session information
        self.session = ""

    def login_session(self, http_flag=False, is_root=False):
        """
        Login Session
        :param http_flag, bool, True means zero copy
        :param is_root, bool, True means login with OS root account
        """
        login_url = LoginInterface().login_interface
        if http_flag:
            login_url = login_url.replace("https", 'http')

        if is_root:
            public_ips = config.public_ips
            public_ip = public_ips.split()[1]
            login_url = login_url.replace("localhost", public_ip)

        if is_root:
            login_data = {"user_id": 'root', "password": config.root_pass}
        else:
            login_data = {"user_id": config.user_id, "password": config.password}

        self.session = requests.session()
        self.session.keep_alive = False
        self.session.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})

        logging.info("[Login]    login_url: %s, login_data: %s", login_url, json.dumps(login_data))
        response = self.session.request("POST", login_url, json=login_data, verify=False)

        return self.session

    def http_request(self, session, http_method, url, params=None, data=None):
        """
        Send HTTP request, support GET/POST
        :param session, instance, session instance
        :param http_method, string, GET/POST/PUT/DELETE/PATCH and so on
        :param url, string, http request url
        :param params, string, HTTP GET request data
        :param data, string, HTTP POST request data
        """
        params = {} if params is None else params
        data = {} if data is None else data

        # set SSL Verify to False
        session.verify = False

        # Set session keep alive to False
        session.keep_alive = False

        response = session.request(http_method, url, params=params, json=data)

        if response.status_code == HttpCode.UNAUTHORIZED:
            session = self.login_session()
            response = session.request(http_method, url, params=params, json=data)

        if http_method in ["GET"]:
            logging.info("[CGI]      Send GET request, URL is (%s)", response.url)
        elif http_method in ["PATCH"]:
            logging.info("[CGI]      Send PATCH request, URL is (%s)", response.url)
        elif http_method in ["POST"]:
            logging.info("[CGI]      Send POST request, URL is (%s), data is : (%s)", response.url, data)

        logging.info("[CGI]      Status code is : (%s), reason is : (%s), text is : "
                     "(%s)", response.status_code, response.reason, response.text.strip())

        return response
```

#### 3.4.3.1 `path_util.py`文件

用于获取`config`和`report`路径，内容参考如下：

```python
# content of path_util.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""  Path Util  """

from __future__ import unicode_literals

import os


__all__ = ["get_config_path"]


def get_config_path():
    """
    获取config文件的路径.
    先获得当前的文件的路径，由于config和common同一级，把common替换为config即可.
    """
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep + "config" + os.sep


def get_report_path():
    """
    获取测试报告的路径.report的路径应该在当前../report
    """
    report_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) \
                  + os.sep + "report" + os.sep
    return report_path
```

#### 3.4.3.2 `util.py`文件

抽象公共类，诸如时间转换（字符串转时间，时间转字符串等），冗余磁盘检测，格式化磁盘，删除`dm`设备，多路径配置&检测，loop check以及fixture的定义等等。

这里介绍一下loop check，因为请求是异步的，请问发起后，优先更新`KVStore`，相关daemon根据定时器，到点了执行`KVStore`中更新的数据，并apply下去，这就造成了前端页面发起请求，相关数据也在页面展示（来自`KVStore`），而相关实体内容并没有及时创建出来，这个时候如果去检测，大概率会失败。比如说创建一个`NAS`目录，去检测Linux系统相关`NAS Folder`是否被export出来，相关的`NAS config`是否被更新，都需要一定的间隔时间（定时器5秒执行一次），在间隔时间内去检查，往往无法达到预期目的，所以这里增加一个loop check，通过装饰器来完成，内容参考如下：

```python
def assert_check(func):
    """
    :param func, string, a function name
    """
    @wraps(func)
    def inner(param, *args, **kwargs):
        """
        :param param, string, a parameter
        """
        for i in xrange(int(retry_timeout)):
            try:
                func(param, *args, **kwargs)
                break
            except Exception as ex:
                logging.warn("[WARN]  Not match, %s time(s) to retry, "
                             "exception is : (%s) : (%s)", (i + 1), ex.__str__, unicode(ex))
                logging.warn("[WARN]  In file (%s) of function (%s), "
                             "at line (%s)", func.func_code.co_filename,
                             func.func_name,
                             func.func_code.co_firstlineno)
                if 'failed to get ceph quorum' in unicode(ex) and i == 3:
                    logging.warn("[WARN]  Run ceph command failed with -100, "
                                 "restart all ceph-mon in cluster")
                    do_cmd(config.restart_mon, 60, True)
                time.sleep(int(retry_interval))
                continue
        else:
            logging.info("[ERROR]  Retry timeout or AssertionError")
            # raise AssertionError('[RetryTimeOut] Failure expected, retry timeout')
            # Deliberately doing this, this will mark the use case status as failed,
            # otherwise it will affect the normal output of the html report (the entire html content is empty)
            eq_(1, 2, "[RetryTimeOut] Failure expected, retry timeout")

    return inner
```

这样在测试基类里做检查点的时候，可以以装饰器的方式来调用：

```python
    @assert_check
    def check_search_filename(self, result, folder_list, option):
        if option == 'by_path':    
            logging.info("[Check]    Start to check file when add folder quota")
        elif option == 'by_key':
            logging.info("[Check]    Start to check file when search folder quota")

        kv_store_folder_name = []
        file_num = len(result[option])

        for i in xrange(file_num):
            kv_store_folder_name.append(result[option][i]['path'])
        
        kv_store_folder_name.sort()
        folder_list.sort()
        logging.debug("--  kv_store_folder_name is  : (%s), folder_list "
                      "is : (%s)", kv_store_folder_name, folder_list)
        
        eq_(kv_store_folder_name, folder_list,
            "[ERROR]  Check folder name is not correct,"
            "KVStore folder name is : {}, actual is : {}".format(kv_store_folder_name, folder_list))
        
        logging.info("[Success]  Check file search for setting folder quota success")

```

#### 3.4.3.3 `bigtera_api.py`文件

此文件按功能分类，分门别类的记录各个功能点的API，示例参考如下：

```python
class LoginInterface(object):
    """  Login API  """

    def __init__(self):
        pass

    login_interface = config.host + '/auth'


class ClusterInterface(object):
    """  Cluster API  """

    def __init__(self):
        pass

    software_info = config.host + '/host'
    cluster_info = config.host + '/cgi-bin/ezs3/json/cluster_info'
    gwgroup_list = config.host + '/cluster/vs'
    general_health = config.host + '/cgi-bin/ezs3/json/general_health'
    general = config.host + '/cluster/host
```

#### 3.4.3.4 `bigtera_cluster.py`

此文件封装存储产品`ceph`的相关动作，诸如`mark osd out， mark out in，make osd full/near full，cephfs `挂载点检测，`ceph crush map`相关检查，PG状态检查，集群状态检查等等。这里只给出代码片段做参考：

```python
    @staticmethod
    def check_ctdb_status(node_nums=None):
        """
        :param node_nums, int, enabled of ctdb node numbers
        """
        node_nums = 3 if node_nums is None else node_nums

        restart_btnas_agent()

        logging.info("[Check]    Check ctdb health status from file of : (%s)", __file__)

        cmd = "ctdb status | grep pnn | sed 's/(THIS NODE)//g' | awk '{print $NF}' | grep OK | wc -l"
        ctdb_ok_count = do_cmd(cmd).strip()

        err_msg = "[Check]    WARN: ctdb is not health, expect OK counts : ({}), but actually " \
                  "is : ({}), will check again".format(node_nums, ctdb_ok_count)

        if int(ctdb_ok_count) < int(node_nums):
            try:
                ctdb_status = do_cmd("ctdb status", 30)
                logging.debug("--  ctdb status : (%s)", ctdb_status)
            except Exception as ex:
                logging.warn("[WARN]  Get ctdb status exception : (%s)", str(ex))

        assert_greater_equal(int(ctdb_ok_count), int(node_nums), err_msg)

        logging.info("[Check]    Success, ctdb health is OK")
```

#### 3.4.3.5 `bigtera_errors.py`

此文件记录产品错误码，所有的用例基类中从此文件中引用状态码，内容片段参考如下：

```python
class HttpCode(object):
    """ Define HTTP Status Code  """
    def __init__(self):
        pass

    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    Forbidden = 403
    NotFound = 404
    PASSWD_EMPTY = 405
    CONFLICT = 409
    InternalServerError = 500
    GatewayTimeout = 504


class StatusCode(object):
    """  Define response of return_code """
    def __init__(self):
        pass

    SUCCESS = 0
    PASSWD_NO_MATCH = 2
    AUTH_ERROR = 3
    USER_ID_TOO_SHORT = 5

    REMOVE_ISCSI_VOL_ERROR = 11
    ENABLE_ISCSI_VOL_ERROR = 'Enable iSCSI LUN Failed'
    DELETE_USER_ERROR = 18

    ADD_ISCSI_VOL_ERROR = 23
    ADD_ISCSI_TARGET_ERROR = 24
```

#### 3.4.3.6 `config.py`

此文件为获取`src/autotest.config`件中配置信息，方便测试基类直接引用。内容片段参考如下：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
Get config form autotest.config
"""

from __future__ import unicode_literals

from configobj import ConfigObj

from path_util import get_config_path


class GetConfig(object):
    """  Get config information from config file  """
    def __init__(self):
        pass

    config = ConfigObj(get_config_path() + "autotest.config")

    # Cluster
    root_pass = config['CLUSTER']['root_pass']
    ssh_port = config['CLUSTER']['ssh_port']
    cluster_name = config['CLUSTER']['cluster_name']
    public_iface = config['CLUSTER']['public_iface']
    storage_iface = config['CLUSTER']['storage_iface']
    osd_device = config['CLUSTER']['osd_device']
```

### 3.4.3.4 config目录介绍

此目录下存放自动化测试环境的配置文件`autotest.config`，包括但不限制于集群配置、客户端配置、AD/LDAP配置、检查周期、集群服务启用/停用等相关配置信息，全部在这个配置文件中。

```shell
-rw-r--r-- 1 root root 7383 Jan  9 17:15 autotest_11_12_13.config
-rw-r--r-- 1 root root 7399 Jan  9 17:15 autotest_15_16_17.config
-rw-r--r-- 1 root root 7399 Jan  9 17:15 autotest_18_19_20.config
-rw-r--r-- 1 root root 7399 Jan  9 17:15 autotest_21_22_23.config
-rw-r--r-- 1 root root 7400 Jan  9 17:15 autotest_24_25_26.config
-rw-r--r-- 1 root root 7400 Jan  9 17:15 autotest_57_58_59.config
-rw-r--r-- 1 root root 7409 Jan  9 17:15 autotest_centos_11_12_13.config
-rw-r--r-- 1 root root 7409 Jan  9 17:15 autotest_centos_15_16_17.config
-rw-r--r-- 1 root root 7409 Jan  9 17:15 autotest_centos_18_19_20.config
-rw-r--r-- 1 root root 7409 Jan  9 17:15 autotest_centos_21_22_23.config
-rw-r--r-- 1 root root 7410 Jan  9 17:15 autotest_centos_24_25_26.config
-rw-r--r-- 1 root root 7411 Jan  9 17:15 autotest_centos_57_58_59.config
-rw-r--r-- 1 root root 7383 Jan  9 17:15 autotest.config
```

由于有5套测试环境，以及支持`Ubuntu`和`CentOS`版本，各个配置文件中的 IP 相关地址信息迥异，最终各套存储环境会将`autotest_xx.config`的文件重命名为`autotest.config`。其内容参考如下：

```ini
[CLUSTER]
root_pass = "password@123!" # 被测集群 root 密码，务必要正确
ssh_port = 22
cluster_name = PYTEST # 被测集群名称，仅适用于新建集群情况下；在已有集群下跑用例，不用改
osd_device = sdb # 哪个分区被用于创建 OSD，仅适用于全新安装系统后 pytet 自动创建集群用
public_iface = bond0 # public interface 网口名称，务必要正确
storage_iface = bond1 # storage interface 网口名称，务必要正确
rep_no = 2 # 集群副本数，默认 2 副本
ntp_server_ip = 202.120.2.101 # NTP server 地址
dns_ip = 172.17.75.100 # DNS IP 地址
storage_ips = "10.10.1.97 10.10.1.98 10.10.1.99" # 存储节点 storage 网络，以单个空格分割
public_ips = "172.17.75.97 172.17.75.98 172.17.75.99" # 存储节点 public 网络，以单个空格分割
license = "3TYRSI-7IA0OW-109QON-LAZ8RV-27AICZ-FQBB3U-DLJW2D,3TYY0Z-Y3MUPS-0QRA8N-B5A8MT-7KOA1V-D9
T0RD-18X7QLW,3TZ49H-OOZOQO-1H5HY2-BAD4SB-236PCQ-VXNNGG-IY0LEH" # 这里是 Controller 试用license

[LOGING]
host = https://localhost:8080 # 访问存储 UI 的地址，无须修改
user_id= admin # 访问 UI 的管理员账号
password = admin # 访问 UI 的管理员账号对应的密码

[AD/LDAP]
ad_server_addr = 172.17.75.231 # AD 的相关设置
port = 389
ad_base_dns = "DC=hype,DC=com"
ad_admin_account = "hype\Administrator"
ad_admin_passwd = "Test#123"
ad_search_dn = "CN=Users,DC=hype,DC=com"
ad_acl_folder = 'Shares'
ad_acl_user = 'zhangsan'
ad_acl_user_passwd = 'bigteratest@321'
ac_guest_folder = 'Guest'
ldap_server_addr = 172.17.75.199 # LDAP 的相关设置
ldap_base_dns = "dc=bigtera-os,dc=com"
ldap_admin_account = "cn=admin,dc=bigtera-os,dc=com"
ldap_admin_passwd = "12345678"
ldap_search_dn = "dc=bigtera-os,dc=com"

[TAKEOVERIP]
# ctdb takeover ip
takeover_ips = "172.17.73.91/24 172.17.73.92/24 172.17.73.93/24" #GW 接管 IP 地址，以空格分割
# S3 takeover IP
s3_takeover_ips = "172.17.73.94/24,94 172.17.73.95/24,95 172.17.73.96/24,96" # S3 的接管
IP 地址，以空格分割，格式必须是 IP/掩码位数

[SNMP] # 这部分只要产品不发生变化，这里就不需要更改
mib_id = ".2.25.31690.11968.43142.4581.44107.2.42453.50459"
snmp_cluster_number = ".1.1"
snmp_product_name = ".1.2"
snmp_product_version = ".1.3"
snmp_fsid = ".1.4"
snmp_cluster_health = ".1.5"
snmp_cluster_disk_total_size = ".1.6"
snmp_cluster_disk_user_size = ".1.7"
snmp_read_io = ".1.8"
snmp_write_io = ".1.9"
snmp_read_throughput = ".1.10"
snmp_write_throughput = ".1.11"

[CLIENTS]
# If cluster node is physical machine, the 'white_list_ip' must be physical machine client;
# Else, must be a VM client, otherwise, some QoS test case maybe run failed
white_list_ip = 172.17.73.254 # 客户端 IP 地址，注意网络带宽，如果是物理机，使用万兆网络
white_ip_root_password = "password123!" # 上个客户端地址 root 用户对应的密码
white_second_ip = 172.17.75.126 # 第二个客户端，iSCSI ACL 使用
white_second_ip_root_password = "Bigtera[!@#]" # 第二个客户端 root 密码
black_list_ip = 172.17.75.127 # 第三个客户端，iSCSI ACL 使用
black_ip_root_password = "Bigtera[!@#]" # 第三个客户端 root 密码
# For VM in ESXi
esxi_ip = '172.17.75.111' # Client（对应上面的 white_list_ip 参数）是 VM，这个 VM 所在的
ESXi 宿主机的 IP 地址
esxi_root_passwd = 'trend#11' # ESXi 宿主机 root 密码
esxi_vm_host_name = 'Ubuntu_client' # Client 在 ESXi 侧
的名称
# For a physical machine
ipmi_ip = "172.17.75.221" # Physical client 是物理机（对应上面的 white_list_ip 参数），这个物理机
的 IPMI 地址
ipmi_user = 'ADMIN' # IPMI 的系统管理员账号名称
ipmi_user_passwd = 'ADMIN' # IPMI 系统管理员账号的密码

[BACKUP] # pytest 用例执行过程中备份文件的存档目录，这里不需要修改
backup_base_path = "/tmp/pytest_backup/"
ezs3_log_backup = "/tmp/pytest_backup/log_ezs3/"
test_case_output_path = "/tmp/pytest_backup/test_case_output"

[RETRY]
retry_interval = 5 # 间隔 5 秒尝试一次，做 check 或 mount 之类的动作
retry_timeout = 40 # 总共尝试次数，默认 40 次

[KERBEROS]
kerberos_server_ip = "172.17.75.240"
kerberos_domain_name = "NJQA.COM"
kerberos_account = "root/admin"
kerberos_domain_account_pw = "password@123
kerberos_username = "root"
kerberos_client_ip1 = "172.17.75.241"
kerberos_client_ip2 = "172.17.75.242"

[CSI]
all_nodes = '172.17.73.172 172.17.73.173 172.17.73.174'
k8s_password = 'p@ssw0rd'

[DAEMON_SERVICE] # 服务的重启、停止相关动作，不同版本的操作系统指令不一样
[DAEMON_SERVICE]
# restart or stop or start deamon service
restart_ezrpc = "systemctl restart ezrpc.service"
restart_btmonitor = "systemctl restart bt-monitor.service"
restart_csmonitor = "systemctl restart csmonitor.service"
restart_btnas_agent = "systemctl restart btnas-agent.service"
restart_ezfs_recycle_flusher = "systemctl restart ezfs-recycle-flusher.service"
restart_eziscsi = "systemctl restart eziscsi.service"
restart_eziscsi_rbd_clean = "systemctl restart eziscsi-rbd-cleaner.service"
restart_apache = "systemctl restart apache2.service"
restart_apache_centos = "systemctl restart httpd.service"
restart_rgw = "systemctl restart ceph-radosgw@radosgw.0.service"
restart_smart_monitor = "systemctl restart bt-disk-monitor.service"
start_smart_monitor = "systemctl start bt-disk-monitor.service"
stop_smart_monitor = "systemctl stop bt-disk-monitor.service"
restart_ezs3_agent = "systemctl restart ezs3-agent.service"
restart_ipmi_agent = "systemctl restart bt-ipmi-agent.service"
restart_ctdb = "systemctl restart ctdb.service"
start_ctdb = "systemctl start ctdb.service"
stop_ctdb = "systemctl stop ctdb.service"
restart_btnas_snap_agent = "systemctl restart btnas-snap-agent.service"

restart_multipath_tool = "systemctl restart multipath-tools"
restart_resolvconf = "systemctl restart systemd-resolved.service"

restart_ganesha = "systemctl restart nfs-ganesha.service"

# For ceph service
# ceph_start = "systemctl start ceph"
start_mon = "systemctl start ceph-mon.target"
start_mds = "systemctl start ceph-mds.target"
start_mgr = "systemctl start ceph-mgr.target"
start_osd = "systemctl start ceph-osd.target"
start_all_osd = "onnode -p all 'systemctl -all start ceph-osd.target'"
start_all_mon = "onnode -p all 'systemctl -all start ceph-mon.target'"
start_all_mds = "onnode -p all 'systemctl -all start ceph-mds.target'"
start_all_mgr = "onnode -p all 'systemctl -all start ceph-mgr.target'"
# # Start all of ceph service on all node(osd, mon and mds)
start_all_ceph_service = "onnode -p all 'systemctl -all start ceph.target'"
restart_all_ceph_service = "onnode -p all 'systemctl -all restart ceph.target'"

restart_mon = "systemctl -all restart ceph-mon.target"
restart_mds = "systemctl -all restart ceph-mds.target"
restart_mgr = "systemctl -all restart ceph-mgr.target"

stop_mon = "systemctl -all stop ceph-mon\*.service ceph-mon.target"
stop_mgr = "systemctl -all stop ceph-mgr\*.service ceph-mgr.target"
stop_mds = "systemctl -all stop ceph-mds\*.service ceph-mds.target"
stop_osd = "systemctl -all stop ceph-osd\*.service ceph-osd.target"

start_assign_osd = "systemctl start ceph-osd@"
stop_assign_osd = "systemctl stop ceph-osd@"

# # For keepalived
stop_keepalived = "systemctl stop keepalived"

[REMOTE_CLUSTER]
# some test case need remote cluster
remote_ip = 172.17.75.101
remote_ip_root_password = "password@123"
remote_ip_root = 'root'
remote_ip_port = 22
```

### 3.4.3.5 `testcase`目录介绍

```ini
├── Basic_Stability_Test
│   ├── case_1_Cluster_Full_Scenario
│   ├── case_2_Daemon_Action
│   ├── case_3_Disconnect_Network
│   ├── case_4_Shutdown_Node
│   ├── __init__.py
│   ├── test_01_assign_gw_vs.py
│   ├── test_02_kv_store.py
│   └── test_03_os_command.py
├── conftest.py
├── Function_Test
│   ├── case_01_Ezs3_Console
│   ├── case_02_Accounts
│   ├── case_03_Hosts
│   ├── case_04_Virtual_Storages
│   ├── case_05_Remote_DR
│   ├── case_06_Configuration
│   ├── case_07_Statistics_Logs
│   ├── case_08_Customized_Features
│   ├── case_09_Enhance
│   ├── case_10_S3
│   ├── case_11_CSI
│   ├── case_99_others
│   └── __init__.py
└── __init__.py

19 directories, 7 files
```

此目录下存放产品具体的功能测试用例，目前分为两个目录，一个是稳定性用例相关，一个是功能性测试用例相关。如果有其他场景，比如性能测试场景，可以再单独创建一目录用户与存放具体场景测试用例。

此目录下用例，均为具体测试函数的调用，用例中不含有任何业务逻辑，所有的业务逻辑在`testcasebase`目录下。我们来看一下此目录子目录下的某个测试用例：

```python
Function_Test/case_02_Accounts# cat test_02_account_ad.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
Test case for AD account
"""

from __future__ import unicode_literals

from src.common.bigtera_errors import StatusCode
from src.common.config import GetConfig as config
from src.testcasebase.Account.account import AccountManager


class TestAccountAD(AccountManager):
    """  test case for: common account settings  """
    user_id = config.ad_acl_user

    @classmethod
    def teardown_class(cls):
        AccountManager().unset_ad_ldap()

    def test_60_ad_ldap_setting(self):
        """  8_3-60 : AD/LDAP settings  """
        self.set_ad_ldap()

    def test_12488_search_a_user_from_ad(self):
        """  8_3-12488 : Search a user from AD  """
        self.set_ad_ldap()
        self.search_user_from_ad()

    def test_import_user_from_ad(self):
        """  8_3-61:Import user from AD/LDAP  """
        self.clean_user(self.user_id)
        self.import_user_from_ad(self.user_id)
        self.delete_user(self.user_id)

    def test_import_dup_user_from_ad(self):
        """  8_3-62:Import duplicated user from AD/LDAP  """
        self.clean_user(self.user_id)
        self.import_user_from_ad(self.user_id)
        # import AD/LDAP user again
        self.import_user_from_ad(self.user_id, expect_return_code=StatusCode.USER_ID_DUPLICATE_ERROR)
        self.delete_user(self.user_id)

    def test_11888_not_set_ad_configuration_search_ad_user(self):
        """  8_3-11888 Not set AD configration, search AD user  """
        # Not config AD/LDAP configuration
        self.set_ad_ldap(enabled=False)
        # Try to search a AD/LDAP user
        self.search_user_from_ad(self.user_id, expect_return_code=StatusCode.ERROR_CONFIG_NOT_ENABLED)
        # Configuration AD/LDAP
        self.set_ad_ldap(enabled=True)
```

所有用例，纯粹是测试函数的调用，这样的好处是：当业务逻辑发生变化，只要修改被调函数，而不是修改测试用例，做到测试用例与逻辑的隔离。

### 3.4.3.6 `testcasebase`目录介绍

```ini
.
├── Account
│   ├── account.py
│   ├── __init__.py
│   └── sds_admin.py
├── Basic_Stability
│   ├── ctdb.py
│   ├── enable_disable_role.py
│   ├── __init__.py
│   ├── kvstore.py
│   ├── network.py
│   ├── os_command.py
│   └── restart_mds_mon.py
├── Cluster_Configuration
│   ├── cluster_management.py
│   ├── file_system_operation_log.py
│   ├── incremental_recovery.py
│   ├── __init__.py
│   ├── inspection_report.py
│   ├── load_balance.py
│   ├── mail.py
│   ├── maintenance_mode.py
│   ├── node_power_monitor.py
│   ├── notification.py
│   ├── ntp.py
│   ├── pool.py
│   ├── qos.py
│   ├── s3_domain.py
│   ├── s3_placement.py
│   ├── s3_takeover_ip.py
│   ├── snmp.py
│   └── wechat.py
├── CSI_Driver
│   ├── csi.py
│   └── __init__.py
├── Enhancement
│   ├── ezs3_coredump.py
│   ├── hwcheck.py
│   ├── __init__.py
│   ├── logrotate.py
│   └── sosreport.py
├── Ezs3_Console
│   └── __init__.py
├── Host_Configuration
│   ├── current_license.py
│   ├── datasearch.py
│   ├── enclosure_status.py
│   ├── hosts.py
│   ├── __init__.py
│   ├── raid.py
│   ├── roles.py
│   └── storage_info.py
├── __init__.py
├── Remote_Replication
│   ├── __init__.py
│   ├── remote_replication_server.py
│   ├── remote_replication_task.py
│   └── remote_SSH_Keys.py
├── S3
│   ├── aws_cli.py
│   ├── bucket_access_logging.py
│   ├── __init__.py
│   └── S3.py
├── Statistics_Logs
│   ├── cluster_statistics.py
│   ├── dashboard.py
│   ├── host_statistics.py
│   ├── __init__.py
│   ├── logs.py
│   └── virtual_storage_statistic.py
└── Virtual_Storage
    ├── configuration.py
    ├── __init__.py
    ├── iSCSI.py
    ├── kerberos.py
    ├── share_folder.py
    ├── virtual_storage.py
    ├── vs_group.py
    ├── vs_user.py
    └── zero_copy.py

12 directories, 68 files
```

`testcasebase`目录下，按产品功能点分类，各个子目录下编写测试用例基类，实现功能点的业务逻辑，其所产生的函数被测试用例调用，组织穿插起来形成业务逻辑。

我们以`vs_user.py`代码片段作为示例，讲述一下基类的书写套路：

编写发起创建用户HTTP请求数据，将`API`各个字段定义好：

```python
    @staticmethod
    def add_vs_user_data(user_id, display_name, password, confirm_password):
        """
        add a vs user data
        :param user_id, string, account id
        :param display_name, string, an account display name
        :param password, int or string, password for an account
        :param confirm_password, int or string, password for an account
        """

        data = {
            'user_name': user_id,
            'display_name': display_name,
            'password': password,
            'confirm_password': confirm_password
        }

        return data
```

然后编写发起HTTP具体请求，请求接收后判断响应状态码，并增加各种检查点的检查：

```python
    def add_vs_user(self, vs_id=None, user_id=None, display_name=None, password=None,
                    confirm_password=None, expect_http_code=None, expect_err_message=None,
                    need_check=None):
        """
        add a vs user
        :param vs_id, string, virtual storage name, such as Default
        :param user_id, string, account id
        :param display_name, string, an account display name
        :param password, int or string, password for an account
        :param confirm_password, int or string, password for an account
        :param expect_http_code, string, expected http return code, default is 204, NO_CONTENT
        :param expect_err_message, string, error message for failed response
        :param need_check, bool, check account created result, default is True
        """
        vs_id = defaults.EZGATEWAY_DEFGROUP_NAME if vs_id is None else vs_id
        user_id = rand_low_ascii(6) if user_id is None else user_id
        display_name = user_id if display_name is None else display_name
        password = '1' if password is None else password
        confirm_password = password if confirm_password is None else confirm_password
        expect_http_code = HttpCode.NO_CONTENT if expect_http_code is None else expect_http_code
        need_check = True if need_check is None else need_check

        add_vs_user_data = self.add_vs_user_data(user_id=user_id,
                                                 display_name=display_name,
                                                 password=password,
                                                 confirm_password=confirm_password)
        add_vs_user_url = AccountInterface().add_vs_user.replace("VS_NAME", vs_id)

        logging.info('[Action]   Add a vs user : (%s)', user_id)

        # If ctdb BANNED, restart ctdb
        ClusterInfo().restart_banned_ctdb()

        add_vs_user_request = HttpSession().http_request(self.session, 'POST', add_vs_user_url,
                                                         data=add_vs_user_data)
        logging.info('[Check]    Check response when add a vs user')
        add_user_err_msg = '[ERROR] Add a vs user: (%s) failed, ' \
                           'backend return: (%s)', user_id, add_vs_user_request.text
        eq_(expect_http_code, add_vs_user_request.status_code, add_user_err_msg)

        if expect_http_code == HttpCode.NO_CONTENT:
            if need_check is True:
                logging.info('[Check]    Check vs account sync result')
                self.check_user_sync_system(user_id=user_id, vs_name=vs_id)
                self.check_user_sync_samba(user_id, vs_name=vs_id)
                self.check_user_sync_rados(user_id)
                self.check_user_in_ezs3_pool(user_id, vs_name=vs_id)
                logging.info('[Success]  Add a vs user success, normal synchronization.')

            return user_id
        else:
            expect_err_message = '' if expect_err_message is None else expect_err_message
            res_err_msg = json.loads(add_vs_user_request.text)['message']
            assert_in(expect_err_message, res_err_msg,
                      "[ERROR]  Expect error message : ({}), actually ({})".format(expect_err_message, res_err_msg))
            logging.info('[Success]    Check error message success from response.')
            return
```

上述代码中的`check_`开头的：

```python

                self.check_user_sync_system(user_id=user_id, vs_name=vs_id)
                self.check_user_sync_samba(user_id, vs_name=vs_id)
                self.check_user_sync_rados(user_id)
                self.check_user_in_ezs3_pool(user_id, vs_name=vs_id)
```

为具体功能检查点，如果此检查点可全局通用，存放到`common/util.py`文件中。

各个检查点代码参考示例如下：

```python
    @assert_check
    def check_user_in_ezs3_pool(self, user_id, vs_name=None):
        """
        :param user_id, string, user ids
        :param vs_name, string, a vs name
        """
        vs_name = defaults.DEFAULT_POOL_NAME if vs_name is None else vs_name

        account = do_cmd("rados -p .ezs3 get samba.account.{} -".format(vs_name), 10, True).strip()
        account = json.loads(account)
        assert_in(user_id, account['accounts'], "[ERROR]  Not find Samba account in .ezs3 pool, "
                                                "backend return: ({})".format(account))
        logging.info("[Success]  Find Samba account in .ezs3 pool.")
```

```python
    @assert_check
    def check_user_sync_rados(self, user_id):
        """
        rados pool of .users.uid
        :param user_id, string, user ids
        """
        user_in_rados = do_cmd("rados -p default.rgw.users.uid ls | grep {}".format(user_id), 10, True)

        logging.info("[Check]    [Add User]  Check user in rados : "
                     "rados -p default.rgw.users.uid ls | grep %s", user_id)
        err_msg = '[ERROR]  Found samba account : (%s) in radosgw', user_id
        assert_not_in(user_id, user_in_rados.strip(), err_msg)

        logging.info("[Success]  Samba account does not need to sync to radosgw.")
```

这里借助`@assert_check`装饰器，完成loop check，loop check次数取决于配置文件`autotest.conf`中的设定：

```ini
[RETRY]
retry_interval = 5
retry_timeout = 40
```

意味着每次间隔5秒检查一次，如果检查通过则退出，做下一个检查点的检测；如果检查失败，最多检测40次，超过40次后，记录异常日志，主动 raise Exception 并退出当前用例的执行，进而执行下一个测试用例。

所有用例基类的编码思路均如此，即：

* 第一步：构造HTTP请求消息体；
* 第二步：发起HTTP请求消息，检查响应状态码；
* 第三步：根据业务需求，在第二步基础上，增加各种业务逻辑检查。

这里要注意一个问题，避免监测点中嵌套检查点，因为`@assert_check`装饰器是5秒*40次，如果发生assert_check嵌套，在一些特殊用例执行失败情况下，会导致此用例耗时太久。此种情况需注意，做好防护动作。

### 3.4.3.7`run.py`

此文件为测试用例执行总入口，囊括了被测环境检查，网络检查，安装包是否具备，重启客户端，运行测试用例等诸多步骤，任意一步出错则立即退出运行。其执行过程大致如下：

```shell
[2023-04-19T10:56:43.387Z] -------------------------------------------------------------
[2023-04-19T10:56:43.387Z] [Step 1]  Restart client, and clean unavailable scsi session
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     1-1 [Check]    Power off then power on for client : 172.17.75.1
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]         [Success]  Reboot pytest client success
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     1-2 [Check]    Check network of client : 172.17.75.1
[2023-04-19T10:56:43.387Z]         [Success]  Client of (172.17.75.1) works well
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     1-3 [Clean]    Delete all of iqn on client, make sure client will not try to re-establish the discard connection
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z] -------------------------------------------------------------
[2023-04-19T10:56:43.387Z] [Step 2]  Check test case execution node.
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-1 [Check]    Client : (172.17.75.1) should install fio, multipath-tools, 
[2023-04-19T10:56:43.387Z]                    openssh-server, open-iscsi and  NFS and CIFS
[2023-04-19T10:56:43.387Z]         [Success]  Client : (172.17.75.1) installed fio, multipath-tools, 
[2023-04-19T10:56:43.387Z]                    openssh-server, open-iscsi and  NFS and CIFS 
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-2 [Check]    The running node must be non-first and non-last node
[2023-04-19T10:56:43.387Z]         [Success]  Check the running node IP address successfully
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-3 [Check]    The network between all nodes should be smooth
[2023-04-19T10:56:43.387Z]         [Success]  Public IP of : (172.17.75.11) reachable
[2023-04-19T10:56:43.387Z]         [Success]  Public IP of : (172.17.75.12) reachable
[2023-04-19T10:56:43.387Z]         [Success]  Public IP of : (172.17.75.13) reachable
[2023-04-19T10:56:43.387Z]         [Success]  Storage IP of : (1.1.1.11) reachable
[2023-04-19T10:56:43.387Z]         [Success]  Storage IP of : (1.1.1.12) reachable
[2023-04-19T10:56:43.387Z]         [Success]  Storage IP of : (1.1.1.13) reachable
[2023-04-19T10:56:43.387Z]         [Success]  The forth node's storage IP can be used
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-4 [Check]    Check public and storage network interface on each node
[2023-04-19T10:56:43.387Z]         [Success]  Public and Storage interface is correct on node (172.17.75.11)
[2023-04-19T10:56:43.387Z]         [Success]  Public and Storage interface is correct on node (172.17.75.12)
[2023-04-19T10:56:43.387Z]         [Success]  Public and Storage interface is correct on node (172.17.75.13)
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-5 [Check]    Check OSD device on each node, make sure the disk partition exist.
[2023-04-19T10:56:43.387Z]                    If OSD disk partition size gap on each node can not be too large, 
[2023-04-19T10:56:43.387Z]                    otherwise PG is difficult to reach a healthy state in a short time
[2023-04-19T10:56:43.387Z]         [Success]  Check OSD device on each node success
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-6 [Check]    Service of apache on each node should be in running state
[2023-04-19T10:56:43.387Z]         [Success]  Service of Apache2 is running on node (172.17.75.11)
[2023-04-19T10:56:43.387Z]         [Success]  Service of Apache2 is running on node (172.17.75.12)
[2023-04-19T10:56:43.387Z]         [Success]  Service of Apache2 is running on node (172.17.75.13)
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-7 [Check]    Check ESXi host IP config or IPMI IP config in config/autotest.config
[2023-04-19T10:56:43.387Z]         [Success]  ESXi host information is correct in config/autotest.config
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-8 [Check]    Check AD and LDAP reachable or not in config/autotest.config
[2023-04-19T10:56:43.387Z]         [Success]  AD   : (172.17.75.231) reachable
[2023-04-19T10:56:43.387Z]         [Success]  LDAP : (172.17.75.199) reachable
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-9 [Check]    Check DNS IP in config/autotest.config
[2023-04-19T10:56:43.387Z]         [Success]  DNS IP : (172.17.75.6) is available in config/autotest.config
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-10 [Check]    Check takeover IP in config/autotest.config
[2023-04-19T10:56:43.387Z]          [Success]  Takeover IP is available in config/autotest.config
[2023-04-19T10:56:43.387Z]          [Success]  S3 takeover IP is available in config/autotest.config
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-11 [Check]    Check public and storage interface from config/autotest.config
[2023-04-19T10:56:43.387Z]          [Success]  Public and storage interface are correct in config/autotest.config
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-12 [Check]    Check public interface BW performance and DNS ip segment
[2023-04-19T10:56:43.387Z]          [Success]  Use correct public interface and config dns ip correct in config/autotest.config
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-13 [Check]    Local host IP should configed in config/autotest.config
[2023-04-19T10:56:43.387Z]          [Success]  Check public and storage IP address in config/autotest.config success
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-14 [Check]    Check the node of cluster IP should not be as client
[2023-04-19T10:56:43.387Z]          [Success]  Check IP and interface success in config/autotest.config
[2023-04-19T10:56:43.387Z] 
[2023-04-19T10:56:43.387Z]     2-15 [Check]    Client : (172.17.75.1) should has file of (/root/.ssh/id_dsa.pub)
[2023-04-19T10:56:43.387Z]          [Success]  Client : (172.17.75.1) has file of (/root/.ssh/id_dsa.pub)

[2023-04-19T10:56:56.228Z] -------------------------------------------------------------
[2023-04-19T10:56:56.228Z] [Step 3]  Check DNS setting in order to connect to WWW to install some packages
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     [Success]  DNS works well
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z] -------------------------------------------------------------
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z] [Step 4]  Install packages ...
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-1. Upgrade apt source 
[2023-04-19T10:56:56.228Z]          Has been run 'apt-get update' before, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-2. Install unzip
[2023-04-19T10:56:56.228Z]          unzip has been installed, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-3. Install and upgrade python-pip
[2023-04-19T10:56:56.228Z]          python-pip has been installed, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-4. Install lazy-object-proxy
[2023-04-19T10:56:56.228Z]          lazy-object-proxy has been installed, skip 
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-5. Install python-configobj
[2023-04-19T10:56:56.228Z]          python-configobj has been installed(CentOS), skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-6. Install more-itertools
[2023-04-19T10:56:56.228Z]          Has been installed more_itertools-5.0.0, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-7. Install zipp
[2023-04-19T10:56:56.228Z]          Has been installed zipp, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-8. Install pyparsing
[2023-04-19T10:56:56.228Z]          Has been installed pyparsing, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-9. Install py-1.8.1
[2023-04-19T10:56:56.228Z]          Has been installed py-1.8.1, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-10. Install isort-4.3.21
[2023-04-19T10:56:56.228Z]           Has been installed isort-4.3-21, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-11. Install packaging-20.3
[2023-04-19T10:56:56.228Z]           Has been installed packaging-20.3, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-12. Install funcsigs-1.0.2
[2023-04-19T10:56:56.228Z]           Has been installed funcsigs-1.0.2, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-13. Install wcwidth
[2023-04-19T10:56:56.228Z]           wcwidth has been installed, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-14. Install pytest
[2023-04-19T10:56:56.228Z]           pytest-4.6.11 has been installed, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-15. Install pytest-progress
[2023-04-19T10:56:56.228Z]           Plugin of progress has been installed, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-16. Install JDK
[2023-04-19T10:56:56.228Z]           Has been installed JDK, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-17. Install allure-python-commons
[2023-04-19T10:56:56.228Z]           Has been installed allure python commons, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-18. Install enum34
[2023-04-19T10:56:56.228Z]           enum34 has been installed, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-19. Install allure_pytest
[2023-04-19T10:56:56.228Z]           Has been installed allure_pytest, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-20. Install allure_command
[2023-04-19T10:56:56.228Z]           Has been installed allure_command, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-21. Install pytest-repeat
[2023-04-19T10:56:56.228Z]           Has been installed pytest-repeat, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-22. Install pytest-timeout
[2023-04-19T10:56:56.228Z]           Has been installed pytest-timeout, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-23. Install configparser
[2023-04-19T10:56:56.228Z]           Has been installed configparser, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-24. Install scandir
[2023-04-19T10:56:56.228Z]           Has been installed scandir, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-25. Install pv at client : 172.17.75.4
[2023-04-19T10:56:56.228Z]           PV has been installed on client 172.17.75.4, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-26. Install astroid-1.5.3
[2023-04-19T10:56:56.228Z]           Has been installed astroid-1.5.3, skip
[2023-04-19T10:56:56.228Z] 
[2023-04-19T10:56:56.228Z]     4-27. Install mccabe-0.6.1-py2.7.egg
[2023-04-19T10:56:56.228Z]           Has been installed mccabe-0.6.1, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-28. Install pylint
[2023-04-19T10:56:56.229Z]           pylint-1.7.6 has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-29. Install coverage
[2023-04-19T10:56:56.229Z]     4-30. Install attrs
[2023-04-19T10:56:56.229Z]           attrs has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-31. Install pluggy
[2023-04-19T10:56:56.229Z]           pluggy has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-32. Install pathlib2
[2023-04-19T10:56:56.229Z]           pathlib2 has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-33. Install importlib_metadata
[2023-04-19T10:56:56.229Z]           importlib_metadata-1.6.0 has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-34. Install six
[2023-04-19T10:56:56.229Z]     4-35. Remove old ssh key from /root/.ssh/known_hosts for client : 172.17.75.4
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-36. Install stress
[2023-04-19T10:56:56.229Z]           stress has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-37. Install pytest-cov
[2023-04-19T10:56:56.229Z]           pytest_cov-2.10.0 has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-38. Install pytest-ordering
[2023-04-19T10:56:56.229Z]           pytest-ording has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-39. Install openldap-clients
[2023-04-19T10:56:56.229Z]           Skip this for Ubuntu 
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-40. Install syslog-tool
[2023-04-19T10:56:56.229Z]           Install syslog-tool success
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-41. Install filechunkio
[2023-04-19T10:56:56.229Z]           filechunkio has been installed, skip
[2023-04-19T10:56:56.229Z] 
[2023-04-19T10:56:56.229Z]     4-42. Install func-timeout
[2023-04-19T10:56:56.229Z]           func-timeout has been installed, skip
[2023-04-19T11:06:26.142Z] -------------------------------------------------------------
[2023-04-19T11:06:26.142Z] [Step 5] [Check]    Check if the report directory is deleted
[2023-04-19T11:06:26.142Z] 
[2023-04-19T11:06:26.142Z]       [SKIP]     No need to delete report directory
[2023-04-19T11:06:26.142Z] -------------------------------------------------------------
[2023-04-19T11:06:26.142Z] [Step 6]  Start checking that the cluster environment meets the requirements for automation case execution
[2023-04-19T11:06:26.142Z]     6-1 [Check]    Not create cluster. First, create cluster, then create&enable OSD/MDS service.
[2023-04-19T11:06:26.142Z] 
[2023-04-19T11:06:26.142Z]     6-2 [Check]    Check all PG state
[2023-04-19T11:06:26.692Z]         [Success]  ALL PG is active+clean.
[2023-04-19T11:06:26.692Z] 
[2023-04-19T11:06:26.692Z]     6-4 [Check]    Restart RGW service
[2023-04-19T11:06:26.692Z] 
[2023-04-19T11:06:27.744Z]     6-5 [Check]    Check apache conf
[2023-04-19T11:06:28.244Z]         [Success]  Has been changed KeepAlive from On to Off on node : (1.1.1.18)
[2023-04-19T11:06:28.244Z]         [Success]  Has been changed KeepAlive from On to Off on node : (1.1.1.19)
[2023-04-19T11:06:28.244Z]         [Success]  Has been changed KeepAlive from On to Off on node : (1.1.1.20)
[2023-04-19T11:06:28.244Z] 
[2023-04-19T11:06:28.244Z]     6-6 [Check]    Check  session timeout in /usr/lib/cgi-bin/ezs3/index.py
[2023-04-19T11:06:28.882Z] 
[2023-04-19T11:06:28.882Z] -------------------------------------------------------------
[2023-04-19T11:06:35.145Z] [Step 7]  Start to run test cases
[2023-04-19T11:06:35.145Z] 
[2023-04-19T11:06:35.145Z]     7-1 Start to run part of test case
[2023-04-19T11:06:35.145Z] 
[2023-04-19T11:06:35.145Z]     7-2 Start to Generate pylint output
[2023-04-19T11:06:35.145Z] -------------------------------------------------------------
```

## 3.4.4 Allure报告

Allure报告原始数据存放于`report`目录下，分为两个目录：`json`  和`html`，`json`  存放原始数据，`html`存放Allure Command Line生成的可视化的HTML报告。此目录下还有`pytest_autotest.log`和`coverage.xml`两个文件，`pytest_autotest.log`为自动化测试用例运行过程中输出的日志，日志级别可根据`pytest.ini`自行定义，`coverage.xml`用于Jenkins生成Code Coverage 报告。

`run.py`代码示例片段如下：

```python
if not part:
    run_all_cmd = "PYTHONPATH=. py.test --cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc --ignore={} --alluredir ../report/json {}".format(skip_path, source_path)

    print("    7-1 Start to run all of test case\n")
    os.system(run_all_cmd)
else:
    if cls_health:
        run_part_cmd = "PYTHONPATH=. py.test --cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc --deselect=prepare --alluredir ../report/json {}".format(case_file)
    else:
        run_part_cmd = "PYTHONPATH=. py.test --cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc --alluredir ../report/json {}".format(case_file)
```

完整的Allure HTML报告总览如下：


<img class="shadow" src="/img/in-post/allure_overview.png" width="800">


## 3.4.5 框架设计小结

### 3.4.5.1 目录结构示例与说明

- `src/` - 存放源代码文件，此目录下是应用程序的主体代码，含`testcasebase/, testcase/,common/, config/, report/`等目录。

- `testcasebase/` - 存放测试用例基类，提供测试用例所需的共用函数。
  - **测试基类的角色**
  - **抽象公共方法**：`TestcaseBase` 类中应封装所有通用的测试方法，如设置环境、清理资源、登录操作、数据库访问等，这些方法会被多个测试用例复用。如这些方法通用率比较高，推荐存放到`common/`目录下。

  - **环境准备与恢复**：在基类中定义 `setUp` 和 `tearDown` 方法来支持测试环境的准备和清理逻辑，在每个测试用例执行前后自动进行环境的搭建和恢复。

  - **错误处理和日志记录**：基类可以提供统一的错误处理和日志记录机制，帮助诊断测试失败的原因。

  - **断言封装**：基类可以提供可复用的断言方法，简化各种验证步骤，并提供更清晰、描述性更强的测试输出。

  - **结构和内容**

    - **模块化设计**：`TestcaseBase` 可以进一步模块化，例如，分为不同的小模块处理UI操作、API调用、数据库交互等。
  - **配置管理**：基类可以整合配置管理，从`config/` 目录加载测试配置，提供给所有的测试用例。
    - **数据管理**：可以包含数据驱动测试的辅助功能，如加载外部测试数据、参数化帮助函数等。

  - **测试基类的使用**
- **继承机制**：测试用例通过继承`TestcaseBase`基类获得其提供的所有公共方法和工具，无需在每个测试用例中重复相同的代码。

- **扩展功能**：具体测试用例可以扩展基类中的方法以适应特定的测试需求，例如添加新的断言或覆盖基类的通用方法。

- **共享测试上下文**：基类可以用来保存测试过程中需要共享的状态或上下文信息，如登录用户的会话信息。

- **日志和报告工具**：集成日志记录器以记录测试执行的详细信息，有助于快速定位问题；同时集成报告工具来生成可读性强的测试报告。

- **维护和可扩展性**

  - **代码复用**：通过基类，减少了测试用例中的重复代码，促进了代码的复用，减轻了维护负担。
    - **灵活性和可扩展性**：基类为添加新的功能、工具或修改现有实现提供了更大的灵活性，使得测试框架可以更容易地随着项目的发展而成长。

- `testcase/` - 存放具体的测试用例，每个用例都扩展自 `testcasebase/` 下的基类，并调用其中定义的函数。

  - **测试用例编写指导**
    - **单一职责原则**：每个测试用例应当只测试一个功能点或场景，保障测试的聚焦性和清晰性。

    - **自描述性**：测试用例的命名和结构应当具备高度自描述性，包括类名、方法名、变量名、用例doc信息，甚至注释，都应该清晰表明测试的意图和预期行为。
    - **复用和抽象**：通过继承`TestcaseBase`类，每个测试用例可以复用公共的设置（`setUp`）和清理（`tearDown`）代码（推荐使用`pytest`的`fixture`实现），测试数据准备，以及自定义的断言方法等。
    - **数据驱动**：采用数据驱动的测试方法，使用外部数据源参数化测试用例，使得一个测试方法能够验证不同的输入。

  - **测试用例组织结构**
    - **功能分类**：按照被测试系统的功能模块来分类测试用例，例如登录功能的测试用例放在`testcase/auth/`目录下。
    - **业务场景**：模拟真实的业务场景来编写测试用例，不仅仅是功能验证，也包括完整的业务流程测试。
    - **复杂度分级**：根据测试复杂度进行分级，如基础验证、集成测试、端到端流程等。

  - **测试用例执行策略**
    - **并行执行**：配置测试用例支持并行运行，以提高测试执行效率。
    - **筛选和标记**：采用标记机制（如在`pytest`中使用标记），允许开发者或测试者选择性地执行一部分测试用例。
    - **依赖管理**：在测试用例或者测试类级别控制依赖关系，确保在执行某些测试之前已经执行了依赖的测试。

  - **测试用例与`TestcaseBase`的交互**
    - **预处理和后处理**：使用`TestcaseBase`提供的`setUp`和`tearDown`方法，来执行所有测试用例前后需要完成的通用操作。
    - **继承的改进**：在`TestcaseBase`基类中定义的方法可能不完全适用于所有用例，需要在具体的子类中重写这些方法。
    - **调用和扩展**：如果`TestcaseBase`基类中的某些方法接近但不完全满足需求，可以在子类中通过调用这些方法的基础上进行扩展和定制。

- `common/`-存放公共类或函数，支持测试活动，不仅仅被测试用例所使用，也可能被测试框架的其他组成部分使用。

  - **实用工具类（Utility Classes）**：包括日志记录器、配置读取器、网络请求发送器等，它们封装了特定功能，可被测试用例和测试基类公用。

  - **数据提供者（Data Providers）**：为测试用例提供输入数据，可能包括读取和解析外部数据文件（如 CSV, JSON）的函数，或者产生随机测试数据的工具。

  - **数据库操作**：封装了数据库连接和操作的通用函数，方便在测试中操作数据库，执行数据准备和验证。

  - **环境设置（Environment Setup）**：包含搭建和管理测试环境所需的脚本和配置，如创建或销毁测试用数据库、服务器。

- `config/`-存放测试环境所需的配置文件，变更测试环境只需更新此配置文件即可。

  - **配置文件的角色**

    - **环境定义**：配置文件可以定义不同的测试环境，例如开发、测试、生产等，包括API端点、服务器地址、数据库连接信息等。
    - **测试参数化**：配置文件可以包含测试过程中要用到的一些参数，例如默认的用户凭证、执行测试的浏览器类型、等待时间上限等。
    - **特性开关**：借助配置文件可以控制特定测试的开关，以便在不同的趋势或阶段启用或禁用测试。

  - **配置文件的类型**

    - **YAML或JSON文件**：提供了良好结构的格式，使得配置的阅读和写作更为清晰，这在自动化测试中非常流行。
    - **INI或Properties文件**：简单的键值对格式，便于小型或简化的配置需求。
    - **环境变量文件**：例如`.env`文件，可用于存储敏感信息，不应该被纳入版本控制系统。

  - **配置管理实践**

    - **配置的继承与覆盖**：基础配置可包含所有环境共用的设置，而环境特定的配置可以覆盖或扩展这些基础配置。
    - **配置模板化**：提供配置模板作为起点，用户可以复制并修改这些模板来创建环境特定的配置文件。
    - **版本控制**：非敏感信息的配置文件应该纳入版本控制，以跟踪变更历史和共享配置状态。

  - **配置文件的动态加载和解析**

    - **配置加载工具**：使用配置加载器库（例如Python的`configparser`模块）来读取和解析配置文件。
    - **环境适应性**：根据环境变量或命令行参数动态选择加载的配置文件，方便在不同环境下运行测试。
    - **配置校验**：在加载配置时进行校验，确保配置值满足预期格式和约束，避免配置错误导致测试失败。

  - **配置文件的安全性**

    - **敏感数据保护**：对于包含敏感数据的配置（如密码、私钥），应确保通过安全的方式管理，例如使用环境变量或密钥管理系统。
    - **配置文件的访问控制**：设立适当的文件权限，限制对配置文件的访问，只有测试系统和授权用户可以读取配置信息。

- `report/`-日志和报告。

  - **详细日志**：在基类中配置日志记录，为测试执行过程中的关键事件提供日志输出。这有助于了解失败的原因和上下文。

  - **结果报告**：集成一个报告工具，将测试结果以人类可读的格式输出，比如HTML或XML报告。许多测试框架提供了结果报告的功能扩展。

### 3.4.5.2 测试执行和管理

- 使用测试运行器（如 `pytest, JUnit, TestNG` 等）来执行测试用例。
- 集成持续集成系统（例如` Jenkins, CircleCI` 等），自动运行测试集。
- 引入测试覆盖率工具，确保代码覆盖率达到预设的标准。
- 通过标签（`tags`）或属性（`attributes`）组织和过滤测试，以支持不同场景或环境下的测试执行。
- 使用断言库来提供清晰的测试断言，方便结果验证和问题诊断。
- 使用`pylint`提高测试代码质量与健壮性，间接地促进测试过程的稳定性和可靠性。



# 3.5 本章小结

本章节中，我们详细介绍了搭建自己的接口测试框架的相关内容，包括设计与规划、用例设计规约以及存储软件的接口级自动化测试框架设计。

我们首先强调了搭建接口测试框架的重要性，它可以帮助我们自动化执行接口测试，提高测试效率和准确性。我们了解到一个好的框架需要经过设计和规划，以确保可扩展性、可维护性和可重用性。

接着，我们深入探讨了用例设计规约的重要性。用例设计规约是定义和规范接口测试用例的方法和标准，它可以帮助我们编写清晰、可读性强的测试用例，提高测试的可靠性和可维护性。

我们还介绍了存储软件的接口级自动化测试框架设计。这种框架设计可以帮助我们对存储软件的接口进行自动化测试，以确保其正常运行和功能完整性。我们详细讨论了该框架的设计原则、架构和关键组件，以及如何实现测试用例的编写和执行。

通过这些丰富的设计思想，有利于实现自动化测试，提高软件开发和维护的效率，同时通过清晰的目录结构和测试实现，确保团队内部沟通和协作顺畅，为软件开发的质量保证提供稳定、高效和扩展性强的支持。
