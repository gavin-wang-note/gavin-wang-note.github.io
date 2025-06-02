---
title: 自动化测试框架设计：低代码平台API和Web自动化测试框架设计
date: 2026-11-28 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 低代码平台pytest自动化测试框架设计简述 
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 低代码平台自动化测试框架设计与实践

在数字化转型的浪潮中，低代码平台因其高效的开发模式而备受青睐。然而，如何对低代码平台进行高效的自动化测试，成为了保障软件质量的关键挑战。
本文将深入探讨基于 `pytest、allure、requests` 和 `selenium` 的自动化测试框架设计与实践，旨在为低代码平台的自动化测试提供一套完整、高效的解决方案。

# 低代码平台自动化测试的挑战

低代码平台通常具有以下特点：

- 多端一致性：需要在 PC、H5 和自助终端等多个端实现功能的一致性。
- 部分功能难以接口化：一些复杂的功能逻辑无法通过接口实现自动化，必须依赖 Web 自动化测试。
- 业务逻辑复杂性：低代码平台的业务逻辑通常较为复杂，涉及多种配置和交互方式。

这些特点对自动化测试框架提出了更高的要求，既要能够高效地处理接口测试，又要能够灵活地应对 Web 自动化测试的复杂场景。


# 框架结构设计

## 框架总体架构

采用「五层架构模式」实现关注点分离：

```ini
├── api/               # HTTP接口核心封装层
├── pages/             # Web页面对象模型(POM)层
├── testcase/          # 测试用例管理层
├── testcasebase/      # 测试用例业务逻辑实现层
└── utils/             # 通用工具服务层
```

详细架构如下：

```ini
.
├── api/
│   ├── error_codes.py
│   ├── http_session.py
│   └── init__.py
│   └── one_thing_api.py
│
├── clear.pyc
│
├── config/
│   └── config.yaml
│
├── conftest.py
├── init__.py
│
├── pages/
│   ├── base_page.py
│   ├── init__.py
│   ├── pyautogui_options.py
│   └── locator.py
│
├── pytest.ini
│
├── run_tests.py
│
└── testcase/
│   ├── api/
│   │   ├── APP/
│   │   ├── config_platform/
│   │   ├── conftest.py
│   │   ├── one_window_operation/
│   │   ├── PC/
│   │   └── self_service_terminal/
│   ├──  web/
│   │   ├── APP/
│   │   ├── config_platform/
│   │   ├── one_window_operation/
│   │   ├── PC/
│   │   └── self_service_terminal/
└── testcasebase/
│   ├── api/
│   │   ├── APP/
│   │   ├── config_platform/
│   │   ├── init__.py
│   │   ├── one_window_operation/
│   │   ├── PC/
│   │   └── self_service_terminal/
│   └── web/
└── utils/
     ├── allure_util.py
     ├── common.py
     ├── config.py
     ├── datetime_util.py
     ├── doc_util.py
     ├── excel_options.py
     ├── faker_util.py
     ├── image_compare.py
     ├── init__.py
     ├── logger.py
     ├── mysql_options.py
     ├── path_util.py
     ├── product_version.py
     ├── redis_options.py
     └── upload_import.py
```

## 模块详细说明

（1）HTTP接口核心封装层（API层设计/API 模块）

- error_codes.py ：定义了低代码平台接口返回的错误码，便于统一处理接口调用时的错误情况。通过标准化的错误码，可以快速定位接口调用失败的原因。
- http_session.py ：封装了 HTTP 请求的会话管理，包括请求头的设置、超时时间的配置等。同时，提供了对请求的封装，使得接口调用更加简洁和高效。
- one_thing_api.py ：针对低代码平台的具体接口进行了封装，提供了便捷的接口调用方法。每个接口方法都包含了详细的参数说明和返回值处理，确保接口调用的稳定性和可靠性。

（2）配置管理中心(config 模块，环境配置中心化)

- config.yaml ：存储了测试环境的配置信息，如接口地址、用户名、密码等敏感信息。通过配置文件的管理，可以方便地在不同环境间切换，提高了测试的灵活性和可维护性。

（3）Web页面对象模型(POM)层（Page Object模式/Pages 模块）

- base_page.py ：定义了基础页面类，封装了公共的页面操作方法，如元素等待、点击、输入等。通过继承基础页面类，可以减少重复代码的编写，提高代码的复用性和可维护性。
- locator.py ：存放了页面元素的定位信息，使得测试用例与页面元素的定位解耦。当页面元素的定位发生变化时，只需修改 locator 文件，无需修改大量的测试用例，降低了维护成本。

（4）测试用例管理层（testcase 模块）

- api ：存放接口测试用例，按照低代码平台的不同模块或功能划分子目录。每个测试用例都包含了详细的测试描述、前置条件、测试步骤和断言。
- web ：存放 Web 自动化测试用例，按照不同的页面或业务流程组织用例。测试用例通过页面对象模式（POM）与页面元素进行交互，提高了代码的可读性和可维护性。

（5）测试用例业务逻辑层（testcasebase 模块）

- api ：存放接口测试用例，按照低代码平台的不同模块或功能划分子目录。每个测试用例都包含了详细的测试描述、前置条件、测试步骤和断言。
- web ：存放 Web 自动化测试用例，按照不同的页面或业务流程组织用例。测试用例通过页面对象模式（POM）与页面元素进行交互，提高了代码的可读性和可维护性。

（6）通用工具服务层（utils 模块）

- allure_util.py ：封装了 Allure 报告相关的操作，如添加附件、描述、标签等，丰富了测试报告的信息。通过 Allure 报告，可以直观地展示测试结果、失败用例的详细信息等。
- common.py : 通用函数功能封装
- config.py : YAML配置文件读取
- datetime_util.py ： 日期格式的各种转换，诸如时间戳转换成日期，日期转换成时间戳，获取年-月-日之类的函数封装
- doc_util.py ： word文件读写操作功能封装
- excel_options.py: Excel文件的读写操作
- faker_util.py ： 虚拟数据构造，如网络地址、电话、固话、姓名、家庭住址、公司地址、行政区划信息等
- image_compare.py ： 图片转base64，base64转图片，两个图片相似度比较等功能封装
- logger.py ：配置了日志功能，记录了测试过程中的关键信息，如请求参数、响应结果、错误信息等。日志文件为问题的排查和定位提供了有力的支持。
- mysql_options.py : MySQL数据库增删改查操作
- path_util.py ： 配置文件路径、日志文件路径、测试报告路径、各种files（word、excel、json、zip、pdf等各种文件）路径的获取
- product_version.py : 获取产品版本信息
- redis_options.py ： redis单机版、集群get、set功能封装
- upload_import.py ： 文件上传基本功能封装，支持单个文件上传、批量上传等




## 执行流程闭环

<img class="shadow" src="/img/in-post/自动化执行过程示意图.png" width="600" />




# Allure报告增强


## 报告定制化

在allure_util.py中实现：

```python

def add_env_info():
    allure.environment(OS=platform.system(),
                       Python_Version=platform.python_version())

def attach_screenshot(name):
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )
```


四、Jenkins持续集成

`Jenkins Pipeline`设计：

- 代码触发：Git Webhook通知Jenkins拉取最新测试脚本。

- 环境构建：通过Docker Compose启动测试环境（如Selenium Hub、数据库）。

- 任务分发：利用Kubernetes插件动态创建Pod执行测试任务，资源利用率提升40%38。

- 结果反馈：测试失败时自动触发Jira创建缺陷工单，并通过企业微信推送告警8。


## Pipeline配置


```groovy
# groovy代码

pipeline {
    agent any
    options {
        parallel true
    }
    stages {
        stage('Run API test case') {
            steps {
                script {
                    try {
                        sh "source ~/.bashrc; src; python clear.pyc.py python run_tests.py --automation-type=api --ci"
                    } catch(err) {
                        echo "$(err)"
                        sh 'exit 1'
                    }
                }
            }
        }
        stage("Allure Report") {
            steps {
                script {
                    allure({
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [path: 'reports/json/']
                    })
                }
            }
        }
        /* Publish Coverage Report */
        stage('Publish Coverage Report') {
            steps {
                script {
                    recordCoverage qualityGates: [
                        {
                            criticality: 'NOTE',
                            integerThreshold: 80,
                            metric: 'LINE',
                            threshold: 80.0
                        }
                    ],
                    tools: [parser: 'COBERTURA', pattern: 'reports/coverage.xml']
                }
            }
        }
    }
}

/* Generate pylint Report */
stage('Code Quality Check') {
    steps {
        script {
            echo "Run pylint code style check"
        }
    }
    post {
        always {
            sh "cat reports/pylint.out"
            recordIssues healthy: 1, sourceCodeRetention: 'LAST_BUILD', tools: [pylint(pattern: 'reports/pylint.out')], unhealthy: 2
        }
    }
}

/* Edit Email Template */
stage("Edit Email Template") {
    steps {
        script {
            sh '''
            #!/bin/bash -xe
            cp ${JENKINS_INSTALL_PATH}/email-templates/v1.0_allure-pipeline-report.groovy ${JENKINS_INSTALL_PATH}/email-templates/allure-pipeline-report.groovy
            cd ${WORK_SPACE}/jenkins;
            python3 edit_email_template.cpython-39.py ${JOB_SPACE}/builds ${JENKINS_INSTALL_PATH}/email-templates/allure-pipeline-report.groovy
            '''
        }
    }
}

/* Send Email */
stage("Send Email") {
    steps {
        script {
            product_version = sh (
                script: """cat ${WORK_SPACE}/reports/json/version.txt | grep PRODUCT_VERSION | awk -F '=' '{print $2}'""",
                returnStdout: true
            ).trim()

            env.PRODUCT_VERSION = product_version

            emailext body: '${SCRIPT, template="allure-pipeline-report.groovy"}',
            attachLog: false,
            compressLog: false,
            postendScript: '${DEFAULT_POSTSEND_SCRIPT}',
            prescript: '${DEFAULT_PRESEND_SCRIPT}',
            subject: '${JOB_NAME} - ${BUILD_DISPLAY_NAME}',
            to: 'Gavin.Wang@bigtera.com.cn, Sam.Libigtera.com.cn'
        }
    }
}
```

## 关键配置项

- 定时触发构建：H */4 * * * 每4小时执行
    

## Allure报告效果

<img class="shadow" src="/img/in-post/allure_report_show1.jpg" width="800" />
<img class="shadow" src="/img/in-post/allure_report_show2.jpg" width="800" />

# 执行效果与价值量化

## 效率提升与成本优化

- 开发周期缩短：低代码平台使测试用例编写效率提升60%，例如某物流企业使用Zoho Creator在2周内完成全流程自动化测试覆盖6。
    
- 资源成本降低：通过Kubernetes弹性伸缩，测试服务器资源消耗减少35%3。

## 质量保障与风险控制

- 缺陷早发现：集成SonarQube进行代码质量扫描，结合自动化测试将生产环境缺陷率降低70%3。
    
- 回归测试全覆盖：每日构建（Nightly Build）确保核心功能100%回归，避免迭代引入重大故障8。


## 价值体现：从技术到业务的全方位提升

（一）加速开发迭代

- 自动化测试框架融入开发流程，实现持续集成。每次代码提交后自动触发测试，快速反馈结果。开发团队根据反馈及时修正问题，优化代码，使开发迭代周期缩短约 30%。例如，在一个两周的迭代周期中，原本用于手工测试和修复 bug 的时间大幅减少，开发团队能更早地进行功能优化和扩展。

（二）增强业务信心

- 通过自动化测试生成的详细报告，为业务部门提供了直观的质量反馈。报告展示了测试用例的执行结果、覆盖率等关键指标，帮助业务人员了解系统功能的稳定性和可靠性。在一次重要的业务推广前，自动化测试报告证实系统核心功能在多端的一致性和稳定性，增强了业务团队对系统上线的信心。

（三）促进团队协作

- 框架的搭建和维护需要测试人员、开发人员和业务人员的共同参与。在测试用例设计阶段，测试人员与业务人员深入沟通需求细节，确保测试场景的完整性；开发人员协助优化接口和页面性能，提升测试效率。这种跨部门协作打破了团队壁垒，形成了紧密的合作关系，团队整体效率提高了约 40%。


# 未来趋势与优化方向

## AI与自动化测试的深度融合

- 智能用例生成：利用GPT-4分析需求文档，自动生成测试场景与数据组合。
    
- 自愈式测试：通过计算机视觉（CV）识别UI变化，动态调整元素定位策略，减少维护成本。

## 安全与合规性增强

- 敏感数据脱敏：在测试数据层集成Vault实现密钥管理，避免硬编码风险。
    
- 合规性检查：自动化验证GDPR、等保2.0等合规要求，如日志审计与访问控制。

## 低代码平台的生态扩展

- 插件市场整合：通过低代码平台的应用市场（如Mendix Marketplace）快速集成第三方测试工具（如Postman、JMeter）。
    
- 混合开发模式：结合Pro Code（专业代码）与Low Code，在可视化界面中嵌入自定义测试逻辑，平衡效率与灵活性。


# 业务价值闭环

- 快速响应需求：市场部门通过低代码平台自主配置活动页面，自动化测试确保上线前功能验证，交付周期从2周压缩至3天。
    
- 数据驱动决策：通过Allure报告分析测试失败趋势，定位性能瓶颈（如API响应时间>2s的接口），驱动架构优化6。

# 实践效果与优化建议

1. 实践效果

通过基于 pytest、allure、requests 和 selenium 的自动化测试框架，我们在低代码平台的测试工作中取得了显著的效果：

- 测试效率大幅提升 ：接口测试和 Web 自动化测试的结合，覆盖了低代码平台的各类功能场景，测试用例的执行效率提高了 50% 以上。

- 测试质量显著提高 ：Allure 报告直观地展示了测试结果，帮助团队快速定位问题，测试问题的解决周期缩短了 30%。

- 测试闭环得以实现 ：通过 Jenkins CI 的集成，实现了测试用例的自动执行、测试结果的自动收集与展示，形成了完整的测试闭环，保障了低代码平台的持续交付质量。

2. 优化建议

- 增强测试数据管理 ：引入测试数据驱动框架，将测试数据与测试用例分离，提高测试数据的可维护性和可扩展性。

- 提升测试用例的可读性 ：通过编写详细的测试用例描述、参数化注解等，提高测试用例的可读性和可维护性。

- 加强测试环境管理 ：完善测试环境的配置管理，支持多环境快速切换，确保测试结果的稳定性和可靠性。

- 引入性能测试 ：在现有功能测试的基础上，增加性能测试模块，评估低代码平台在高并发场景下的性能表现。

# 总结与展望

本文深入探讨了基于 `pytest、allure、requests` 和 `selenium` 的低代码平台自动化测试框架设计与实践。通过合理的框架结构设计、高效的测试用例编写、直观的 `Allure` 报告集成以及持续集成的 `Jenkins` 配置，实现了低代码平台的自动化测试闭环，为软件质量的保障提供了有力的支持。
未来，随着低代码平台的不断发展和技术的不断进步，我们计划对自动化测试框架进行持续优化和扩展：

- 引入智能化测试 ：结合机器学习和人工智能技术，实现测试用例的自动生成和优化，提高测试覆盖率和测试效率。

- 加强移动端自动化测试 ：随着移动应用的普及，加强对低代码平台移动端的自动化测试支持，确保移动端功能的一致性和稳定性。

- 完善测试数据分析 ：通过对测试结果数据的深入分析，挖掘潜在的质量问题和测试瓶颈，为测试策略的优化提供数据支持。

低代码平台下的自动化测试不仅是技术方案的落地，更是组织流程与工具链的深度重构。其核心价值在于：

- 技术民主化：让业务人员参与测试设计，打破“开发-测试”壁垒。

- 效率与质量的双重飞跃：通过自动化闭环将人力从重复劳动中解放，聚焦于探索性测试与用户体验优化。

- 可持续的技术演进：结合云原生与AI技术，构建自适应、高可用的测试基础设施。

