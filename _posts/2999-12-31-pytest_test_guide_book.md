---
title: 自己总结的《pytest测试指南》
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
summary: 自己总结的《pytest测试指南》一书，超级详细的pytest介绍，以及具体API项目实践和Jenkins CI/CD落地，完整的一套从入门到项目实践的详细记载，值得详细阅读。
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

工作之余，前前后后大约一年半的时间，断断续续的写了这些内容，好记性不如烂笔头，600余页，自己留存下来偶尔看看温习温习。

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

对于`pytest hook`的详细介绍与应用，敬请期待我的另外一篇汇总博文，将分门别类的详细介绍各个`hook`的使用场景和案例。
