---
title: 自己总结的《pytest测试指南》一书，800余页
date: 2999-12-31 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: true
hide: false
cover: true
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 历经十八个月的辛勤耕耘，一部800余页的《pytest测试指南》完稿。本书不仅提供了pytest的全面介绍，更深入细致地探讨了具体的API项目实践。此外，书中还详尽阐述了如何将pytest与Jenkins相结合，以实现持续集成（CI）的完美落地。这是一部从基础入门到实际项目应用的完整手册，每一页、每一章节都凝聚心血、精心雕琢。对于渴望深入掌握pytest的读者而言，本书无疑是一份不可多得的宝贵资源，值得细细品读。 
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

在工作之余，我投入了大约一年半的时间，断断续续地撰写了这些内容。好记性不如烂笔头，因此将这些知识详细地记录在了数百页的文档中，以便自己随时回顾和复习。

# 本书全部链接

## 前言 

[《pytest测试指南》-- 前言 PREFACE](https://gavin-wang-note.github.io/2023/12/18/pytest_test_guide_preface/)

## 第一部分 pytest基础篇

[《pytest测试指南》-- 第一章节 前言 PREFACE](https://gavin-wang-note.github.io/2023/12/18/pytest_test_guide_part1_preface/)

[《pytest测试指南》-- 第一章节1-1 初识pytest](https://gavin-wang-note.github.io/2024/01/21/pytest_test_guide_part1_chapter1_getting_to_known_pytest/)

[《pytest测试指南》-- 第一章节1-2 pytest测试用例执行](https://gavin-wang-note.github.io/2024/02/17/pytest_test_guide_part1_chapter1_2_run_pytest_case/)

[《pytest测试指南》-- 第一章节1-3 pytest参数详解](https://gavin-wang-note.github.io/2024/03/03/pytest_test_guide_part1_chapter1_3_1_pytest_params/)

[《pytest测试指南》-- 第一章节1-4 pytest测试用例标记](https://gavin-wang-note.github.io/2024/05/24/pytest_test_guide_part1_chapter1_4_pytest_mark/)

[《pytest测试指南》-- 第一章节1-5 pytest断言](https://gavin-wang-note.github.io/2024/05/25/pytest_test_guide_part1_chapter1_5_pytest_assert/)

[《pytest测试指南》-- 第一章节1-6 pytest fixture](https://gavin-wang-note.github.io/2024/05/26/pytest_test_guide_part1_chapter1_6_pytest_fixture/)

[《pytest测试指南》-- 第一章节1-7 pytest内置fixture](https://gavin-wang-note.github.io/2024/05/27/pytest_test_guide_part1_chapter1_7_pytest_internal_fixture/)

[《pytest测试指南》-- 第一章节1-8 pytest参数化](https://gavin-wang-note.github.io/2024/05/28/pytest_test_guide_part1_chapter1_8_pytest_parameterize/)

[《pytest测试指南》-- 第一章节1-9 pytest 配置文件](https://gavin-wang-note.github.io/2024/05/29/pytest_test_guide_part1_chapter1_9_pytest_conftest_pytest_ini/)

[《pytest测试指南》-- 第一章节1-10 pytest常用插件介绍](https://gavin-wang-note.github.io/2024/05/30/pytest_test_guide_part1_chapter1_10_pytest_plugin/)

[《pytest测试指南》-- 第一章节1-11 pytest与Allure结合生成测试报告](https://gavin-wang-note.github.io/2024/05/31/pytest_test_guide_part1_chapter1_11_allure/)

## 第二部分 接口自动化实践

[《pytest测试指南》-- 第二章 前言](https://gavin-wang-note.github.io/2024/06/01/pytest_test_guide_part2_chapter2_preface/)

[《pytest测试指南》-- 第二章 2-1 API与requests模块介绍](https://gavin-wang-note.github.io/2024/06/02/pytest_test_guide_part2_chapter2_1_api_and_requests_module/)

[《pytest测试指南》-- 第二章 2-2 代码质量与规范化检查工具-pylint](https://gavin-wang-note.github.io/2024/06/03/pytest_test_guide_part2_chapter2_2_code_quality_normalization_checker/)

[《pytest测试指南》-- 第二章 2-3 pytest+requests+allure自动化测试框架设计](https://gavin-wang-note.github.io/2024/06/04/pytest_test_guide_part2_chapter2_3_api_framework_design/)

[《pytest测试指南》-- 第二章 2-4 Cobbler部署与使用](https://gavin-wang-note.github.io/2024/06/05/pytest_test_guide_part2_chapter2_4_cobbler_deploy_iso/)

[《pytest测试指南》-- 第二章 2-5 与Jenkins结合完成CI构建](https://gavin-wang-note.github.io/2024/06/06/pytest_test_guide_part2_chapter2_5_jenkins_ci_cd/)

## 附录

[《pytest测试指南》-- 附录1 pytest如何debug](https://gavin-wang-note.github.io/2024/06/07/pytest_test_guide_appendice_1_debug/)

[《pytest测试指南》-- 附录2 pytest hook介绍](https://gavin-wang-note.github.io/2024/06/08/pytest_test_guide_appendice_2_pytest_hook/)


# 其他

对于`pytest hook`的详细介绍与应用，敬请期待我的另外一篇汇总博文(预计2024年10月底释出)，将分门别类的详细介绍各个`hook`的使用场景和案例。


# 目录结构

```shell
前言 PREFACE	16
自动化是什么	16
为什么要做自动化测试	16
什么项目适合自动化测试	17
本书介绍了什么	18
本书适用于哪些人群	18
序	19
第1章 初识pytest	19
第2章 pytest测试用例执行	19
第3章 pytest参数详解	20
第4章 pytest测试用例标记	20
第5章 pytest断言	20
第6章 pytest精髓-fixture	20
第7章 pytest内置fixture	20
第8章 pytest参数化	20
第9章 pytest配置文件	20
第10章 pytest插件	21
第11章 pytest与Allure结合生成测试报告	21
第12章 API与requests模块介绍	21
第13章 代码质量与规范化检查工具-pylint	21
第14章 pytest+requests+allure自动化测试框架设计	21
第15章 Cobbler部署与使用	21
第16章 与Jenkins结合完成CI构建	22
第1章 初识pytest	22
1.1 常见几种测试框架对比	22
1.2 初识pytest	26
1.2.1 pytest是什么	26
1.2.2 pytest框架结构	27
1.2.3 pytest的优点和特点	29
1.2.4 pytest的官网及资料地址	30
1.3 关于nose 与 pytest	30
1.4 部署pytest	31
1.4.1 环境说明	31
1.4.2 pytest安装	31
1.5 pytest入门	32
1.5.1 基本用法	32
1.5.2 参数化测试	32
1.5.3 测试预期的异常	32
1.5.4 使用 fixture 处理测试前后的准备和清理	33
1.5.5 跳过测试或有条件地跳过测试	33
1.6 本章小结	34
第2章 pytest测试用例执行	34
2.1 pytest 测试搜索规则	35
2.2 pytest 测试默认命名规则	35
2.2.1 测试文件命名规则	35
2.2.2 测试类命名规则	35
2.2.3 测试函数命名规则	35
2.2.4 fixture命名规则	36
2.3 测试用例执行方式	37
2.3.1 main()函数运行	37
2.3.2 pytest命令行运行	44
2.3.3 使用配置文件运行程序	46
2.4 pytest用例的状态	50
2.4.1 PASSED（.）	50
2.4.2 FAILED（F）	50
2.4.3 SKIPPED（s）	50
2.4.4 XFAIL（x）	50
2.4.5 XPASS（X）	50
2.4.6 ERROR（E）	51
2.5 pytest执行结束时返回的状态码	53
2.5.1 pytest exit code用途	53
2.5.2 pytest exit code含义	53
2.5.3 示例参考	55
2.6 测试用例执行顺序	57
2.6.1 pytest 默认执行顺序	57
2.6.2 自定义执行顺序	61
2.6.3 涉及多个目录/文件下执行顺序	61
2.7 本章小结	62
第3章 pytest参数详解	63
3.1 pytest 参数介绍与示例	64
3.1.1 查看pytest所有可用参数	64
3.1.2 分类汇总	71
3.2 pytest help信息介绍	72
3.2.1 positional arguments	72
3.2.2 general 相关参数	72
3.2.3 Reporting 相关参数	93
3.2.4 pytest-warnings 相关参数	123
3.2.5 collection 相关参数	129
3.2.6 test session debugging and configuration 相关参数	146
3.2.7 logging 相关参数	156
3.2.8 [pytest] ini-options 相关参数	166
3.2.9 Environment variables 相关参数	199
3.3 本章小结	203
第4章 pytest测试用例标记	203
4.1 标记（markers）	203
4.1.1 内置标记	204
4.1.2 自定义标记	204
4.2 标记的使用	205
4.2.1 -m 参数执行指定标记的用例	205
4.2.2 跳过（skip）测试	206
4.2.3 标记用例为预期失败	223
4.3 其他标记	230
4.4 测试实践	230
4.4.1 不想被 pytest 执行的文件	230
4.4.2 问题的解法	231
4.5 信息汇总	234
4.5.1 标记使用对比信息汇总	234
4.5.2 pytest 中跳过和忽略测试用例的区别	235
4.6 各种跳过的用法和差异对比	236
4.7 本章小结	238
第5章 pytest断言	239
5.1 什么是断言	239
5.2 断言的时机	240
5.3 断言分类	242
5.3.1 真值断言	242
5.3.2 等值断言	242
5.3.3 不等断言	242
5.3.4 大于/小于断言	242
5.3.5 成员断言	243
5.3.6 身份断言	243
5.3.7 近似值断言	243
5.3.8 组合断言	243
5.3.9 异常断言	243
5.3.10 警示断言	244
5.3.11 自定义断言消息	245
5.4 借鉴nose framework断言	245
5.4.1 nose assert信息	245
5.4.2 nose assert示例	246
5.5 多重校验插件之pytest-assume	250
5.5.1 安装pytest-assume	251
5.5.2 解决无法import assume问题	253
5.5.3 使用pytest-assume	254
5.5.4 pytest-assume teardown的坑	259
5.6 多重校验插件之pytest-check	263
5.6.1 安装pytest-check	263
5.6.2 使用pytest-check	263
5.6.3 示例	264
5.6.4 小结	266
5.7 pytest-check解决pytest-assume teardown的坑	266
5.8 pytest-assume与pytest-check区别	268
5.8.1 使用方式	268
5.8.2 语法风格	268
5.8.3 错误报告	268
5.8.4 内部实现	269
5.8.5 选择如何使用	269
5.9 assert优劣对比	269
5.10 本章小结	270
第6章 pytest精髓-fixture	271
6.1 什么是 pytest fixture?	271
6.2 pytest fixture 的强大之处	271
6.3 fixture介绍	272
6.4 fixture的特性	272
6.5 fixture的优势	273
6.5.1 命令灵活	273
6.5.2 数据共享	273
6.5.3 实现参数化	273
6.6 xunit-style 风格	274
6.6.1 测试类	274
6.6.2 固件方法	275
6.6.3 推荐做法	281
6.7 pytest的fixture实现方式	282
6.7.1 定义fixture	282
6.7.2 调用fixture	283
6.7.3 fixture函数源码解析	284
6.7.4 pytest fixture四种作用域	287
6.7.5 使用params传递参数	295
6.7.6 自动调用fixture	300
6.7.7 params与ids	302
6.7.8 params与name	306
6.7.9 fixture几种清理	309
6.7.10 fixture的并列与嵌套	311
6.8 在不同层级上重写fixture	325
6.8.1 重写conftest.py中的fixture	325
6.8.2 在模块层级重写fixture	331
6.8.3 参数化重写fixture	332
6.8.4 参数化fixture重写非参数化fixture，反之亦然	334
6.9 conftest.py	336
6.9.1 conftest.py 文件的查找和加载机制	336
6.9.2 conftest.py使用场景	336
6.9.3 conftest.py中fixture的作用域	337
6.9.4 不同位置conftest.py文件的作用域	338
6.9.5 conftest.py使用方法	338
6.9.6 conftest.py结语	342
6.10 本章小结	342
第7章 pytest内置fixture	343
7.1 pytest 内置 fixture 按功能分类	343
7.1.1 基础测试设置与清理	344
7.1.2 记录测试套件属性	344
7.1.3 配置和测试功能	344
7.1.4 高级测试执行控制	345
7.2 内置fixture详解	345
7.2.1 基础测试设置与清理	345
7.2.2 高级测试执行控制	366
7.2.3 配置和测试功能	367
7.2.4 记录测试套件属性	381
7.2.5 临时目录相关	395
7.3 本章小结	402
第8章 pytest参数化	403
8.1 参数化的概念	403
8.2 使用 parameterize 的优势	403
8.3 pytest.mark.parameterize 的用法	403
8.4 常见的参数化示例	404
8.4.1 只传递一个参数	404
8.4.2 多个参数	408
8.4.3 参数化	415
8.5 parametrize源码详解	417
8.6 argnames参数	423
8.6.1 测试一般函数行为	423
8.6.2 边界值和错误情况	424
8.6.3 参数化多重模块或类	425
8.6.4 兼容性测试	427
8.6.5 等价类划分	429
8.6.6 异常和特殊条件测试	431
8.6.7 常见的argnames语法异常	433
8.7 argvalues参数	435
8.7.1 正常情况下为argvalues赋值	435
8.7.2 特殊情况 - 参数化特定值导致的异常	436
8.7.3 argvalues来自pytest.param	437
8.7.4 argvalues来自外部	438
8.7.5 使用 pytest.mark.parametrize 的 argvalues 参数注意事项	441
8.8 indirect参数	441
8.8.1 示例一：基本使用场景	441
8.8.2 示例二：测试不同用户权限	442
8.8.3 小结	443
8.9 ids参数	443
8.9.1 ids 长度	443
8.9.2 ids 相同	445
8.9.3 使用中文作为ids	446
8.9.4 通过函数生成ids	447
8.9.5 ids 覆盖	448
8.9.6 ids 的作用	454
8.9.7 注意事项和进一步说明	456
8.10 scope参数	456
8.10.1 module级别	457
8.10.2 未指定scope	458
8.11 pytest_generate_tests hook方法	458
8.11.1 pytest 参数化方式	458
8.11.2 pytest_generate_tests hook方法介绍	459
8.12 优化范本	463
8.13 参数化最佳实践	464
8.14 本章小结	465
第9章 pytest配置文件	466
9.1 pytest 配置文件分类	466
9.2 哪些内容可以放在 pytest.ini 文件中	467
9.3 配置文件pytest.ini	469
9.3.1 应用场景	470
9.3.2 pytest.ini 使用方法	470
9.3.3 结合使用 conftest.py 和 pytest.ini	474
9.3.4 使用 pytest.ini 的优势	475
9.3.5 小结	475
9.4 配置文件pyproject.toml	475
9.5 配置文件tox.ini	477
9.6 配置文件 setup.cfg	479
9.6.1 setup.cfg 文件的结构	479
9.6.2 pytest 配置示例	479
9.6.3 setuptools 和 pytest 结合的完整配置示例	480
9.7 pytest配置文件读取顺序	481
9.7.1 配置文件读取顺序	481
9.7.2 覆盖默认的配置文件读取顺序	482
9.8 pytest的warning处理机制	483
9.8.1 使用pytest配置文件忽略特定警告	483
9.8.2 使用pytest配置文件禁用warnings插件方式	483
9.8.3 在命令行中使用-W选项	483
9.8.4 在代码中使用warnings模块处理警告	483
9.8.5 使用pytest.mark.filterwarnings忽略特定测试的警告	484
9.8.6 忽略所有告警	484
9.8.7 禁用 warning 实践	485
9.9 本章小结	488
第10章 pytest插件	488
10.1 插件分类	489
10.1.1 内置插件	489
10.1.2 第三方插件	489
10.1.3 自开发的插件	490
10.2 查看可用的插件	490
10.3 加载/禁用插件	490
10.4 pytest启动时插件发现顺序	490
10.5 pytest常用插件介绍	491
10.5.1 进度条相关插件	491
10.5.2 用例执行顺序相关插件	495
10.5.3 用例运行相关插件	503
10.5.4 CI/CD相关插件	539
10.5.5 测试时间相关插件	544
10.5.6 构造测试数据相关	556
10.5.7 测试报告相关	573
10.5.8 其他插件	585
10.6 本章小结	588
第11章 pytest与Allure结合生成测试报告	589
11.1 Allure框架介绍	589
11.2 Allure如何生成报告	590
11.2.1 安装 Allure CLI 工具	590
11.2.2 集成 Allure 到你的测试框架中	591
11.2.3 运行测试并生成数据	591
11.2.4 生成 Allure 报告	591
11.3 Allure 报告组成	591
11.3.1 概览（Overview）	592
11.3.2 类别（Categories）	593
11.3.3 测试套（Suites）	594
11.3.4 图表（Graphs）	595
11.3.5 时间刻度（Timeline）	598
11.3.6 功能（Behaviors）	599
11.3.7 包（Packages）	599
11.4 Allure功能介绍	600
11.4.1 帮助 --help	600
11.4.2 Environment	603
11.4.3 Categories	605
11.4.4 Allure属性	606
11.4.5 Allure 实践	608
11.4.6 综合示例	628
11.5 结语	630
11.5.1 设置测试套中显示内容	630
11.5.2 设置报告中功能项显示内容	630
11.5.3 设置具体用例显示内容	630
11.5.4 设置用例级别	630
11.6 注意事项	631
11.7 本章小结	631
第12章 API与requests模块介绍	631
12.1 什么是API	632
12.2 API的组成	634
12.3 API的主要特点	636
12.4 API的工作流程	637
12.5 API的分类	638
12.6 Web API	639
12.6.1 RESTful API	640
12.6.2 SOAP API	643
12.6.3 GraphQL API	646
12.7 认证与授权之Cookie、Session、Token、JWT	648
12.7.1 认证与授权	648
12.7.2 授权实现方式	650
12.8 API测试	662
12.8.1 HTTP 请求方法	663
12.8.2 HTTP状态码	664
12.8.3 Python的requests库介绍	665
12.8.4 基于requests实现HTTP请求	675
12.9 本章小结	678
第13章 代码质量与规范化检查工具-pylint	678
13.1 pylint介绍	679
13.1.1 pylint是什么	679
13.1.2 核心特性	679
13.1.3 安装pylint	679
13.1.4 基本使用	679
13.1.5 消息类型	679
13.1.6 输出解析	680
13.1.7 配置	680
13.1.8 禁止检查	680
13.1.9 与IDE集成	680
13.1.10 CI/CD集成	680
13.1.11 使用Pylint注意事项	680
13.2 pylint配置文件 .pylintrc	681
13.2.1 .pylintrc 文件	681
13.2.2 常用的配置参数和示例	682
13.2.3 在代码中覆盖.pylintrc配置	683
13.2.4 生成默认的.pylintrc文件	683
13.2.5 综合管理Pylint消息	683
13.3 pylint错误消除	683
13.3.1 生成初始的.pylintrc文件（如果还没有）	683
13.3.2 编辑.pylintrc文件内的[MESSAGES CONTROL]部分	683
13.3.3 告警的错误码及描述	684
13.3.4 示例说明如何消除告警	684
13.3.5 检查告警ID	684
13.3.6 应用.pylintrc文件的配置	685
13.3.7 修复pylint告警实践	685
13.4 本章小结	686
第14章 pytest+requests+allure自动化测试框架设计	686
14.1 搭建自己的接口测试框架	686
14.1.1 为何要搭建自己的测试框架	686
14.1.2 如何规划框架	687
14.1.3 CI/CD 工具选择	690
14.1.4 结合被测产品选择合适工具	691
14.2 工具&框架选型	692
14.3 测试用例设计规约	693
14.3.1 规约要求	693
14.3.2 示例说明	694
14.4 框架设计介绍	695
14.4.1 框架目录结构	695
14.4.2 第一层目录介绍	698
14.4.3 第二层目录介绍	720
14.4.4 Allure报告	750
14.4.5 框架设计小结	751
14.5 本章小结	756
第15章 Cobbler部署与使用	756
15.1 Cobbler介绍	756
15.2 Cobbler工作原理	757
15.3 Cobbler目录结构简介	760
15.3.1 Cobbler配置文件目录	760
15.3.2 Cobbler数据目录	761
15.3.3 Cobbler日志文	761
15.4 部署Cobbler	761
15.4.1 IP规划	761
15.4.2 查看系统信息	762
15.4.3 配置IP	762
15.4.4 配置 ssh	764
15.4.5 关闭防火墙、selinux等	765
15.4.6 安装wget	765
15.4.7 安装epel源	765
15.4.8 新增一个分区，增加ISO自动挂载	765
15.4.9 安装cobbler	766
15.4.10 启动相关服务并设置开机自启	766
15.4.11 检查cobbler配置	766
15.4.12 安装其他包	768
15.4.13 重启cobblerd并同步检查	768
15.4.14 通过cobbler来管理dhcp	768
15.4.15 配置DHCP服务	768
15.5 部署Nginx	769
15.5.1 安装Nginx	769
15.5.2 设置开机启动	769
15.5.3 配置Nginx	770
15.6 手动安装实践	772
15.6.1 安装CentOS7	772
15.6.2 Ububtu 安装	777
15.7 自动化安装脚本的使用	781
15.7.1 必要的安装包	781
15.7.2 相关脚本/模板准备	781
15.7.3 配置文件准备	783
15.7.4 批量部署脚本代码说明	786
15.7.5 安装过程	788
15.7.6 与Jenkins的结合	795
15.8 本章小结	796
第16章 与Jenkins结合完成CI构建	797
16.1 CI/CD介绍	797
16.2 CI/CD系列工具介绍	799
16.2.1 TeamCity	799
16.2.2 Jenkins	800
16.2.3 Bamboo	800
16.2.4 CircleCI	801
16.2.5 Travis CI	801
16.2.6 Codeship	801
16.2.7 CI/CD工具大比拼	802
16.3 部署Jenkins	802
16.3.1 安装Ubuntu 22.04	802
16.3.2 安装必要的软件包	803
16.3.3 配置Jenkins	804
16.4 Groovy介绍	805
16.4.1 Jenkins Script Console	805
16.4.2 管道脚本（Pipelines）	805
16.4.3 动态作业生成	806
16.4.4 插件开发	806
16.4.5 管理和配置	806
16.4.6 示例脚本	806
16.4.7 安全注意事项	806
16.4.8 小结	806
16.5 pipline介绍	807
16.5.1 pipeline 的主要特点	807
16.5.2 Jenkins Pipeline 核心概念	807
16.5.3 Pipeline 的两种语法	808
16.5.4 Jenkinsfile 示例	808
16.5.5 小结	809
16.6 项目实践	809
16.6.1 Jenkins pipline style Project 配置	813
16.6.2 Email 模板	816
16.6.3 效果展示	817
16.7 本章小结	822
```

