---
title: 软件开发测试流程
date: 2015-12-01
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password: "meipian"
toc: true
mathjax: false
summary: 本文介绍一下软件开发测试的基本流程，各家公司大同小异
categories:
    - [测试]
tags:
    - 测试
---


# 概述

各家开发、测试流程虽有差异，但主心骨基本相同。

本文简单介绍一下软件开发、测试基本流程，供参考。

# 完整的项目测试流程

理想情况下，完整的项目流程类似是这样的：

<img class="shadow" src="/img/in-post/完整的项目流程.png" width="1200">


# 需求阶段

在这个阶段中，产品经理主导，测试跟开发参与需求评审。

在需求评审的过程中，需要了解需求的细节和设计逻辑，同时对于有疑问的地方要提出疑问，达成对需求理解的一致。

需求评审结束后，开发先评估工时，然后测试要根据需求文档并结合开发的工作量，来完成测试工时的评估。

排期表规范：

包含角色：产品、设计、前后端、测试等（根据具体的项目来定）

关键时间节点：

- 产品：需求串讲时间，项目上线时间
- 开发：开发起止时间，前后端联调时间
- 测试：提测时间，测试起止时间

# 开发阶段

排期定好之后，就进入开发阶段了。

首先，开发同学会先出一个整体的技术设计方案，包含本次需求的设计思路和实现逻辑等。

这时一般会有技术评审的环节（开发主导，产品和测试参与），在技术评审的时候，可以对开发的技术设计提出疑问，从而获得更加全面的了解，了解越多，测试用例设计才会更全面。

技术评审之后，测试要制定测试方案（测试范围、测试手段、测试时间等）。

然后编写测试用例是很重要的一部分。

编写用例可以用excel或xmind，建议测试团队统一标准。

测试用例完成后，需要跟开发和产品拉会，进行用例评审。

用例评审的目的是找出遗漏点和逻辑理解不一致的地方，最终统一对预期效果的理解。

# 测试阶段

开发完成后，接下来就是提测。

在提测环节，建议制定测试准入（也称为提测规范）。

为什么要制定提测规范：为了规范开发的提测质量，加强前期质量控制，降低提测后因提测质量问题造成的风险。

## 测试准入标准（根据实际业务增减）

- 开发人员按需求及原型图完成软件的业务流程及功能的开发
- 开发人员编码结束，并已完成单元测试，并提供自测功能报告
- 软件的基本业务流程可以运行通过（冒烟测试），功能操作正确，且符合需求
- 开发人员需提供软件的最新版本，并安装测试通过
- 开发人员需提供接口文档、部署文档、提测申请、提测功能列表
- 提测质量达标之后，就正式进入测试了。

测试一般分为后端测试（接口测试）和前端测试，后端测试通过之后再进行前端测试。

怎样才算合格的测试，同样也需要制定测试准出标准（测试完成标准）

## 测试准出标准

- 所有功能和业务流程都按需求实现
- 测试用例都已经执行完成，测试执行覆盖率为100%
- 测试发现的所有 BUG 问题中，致命、严重、都已被修复且被验证通过
- 允许遗留不影响业务流程的轻微bug，但是需要有解决方案及时间点
- 完成测试后，出具测试报告

# 发布阶段

测试完成后，就进入发布阶段。

发布规范包含以下几点：

- 发布时间：为了避免上线后有问题及时修复，发布日期建议避开周五及节假日前两天，上线时间避开用户活跃高峰期
- 发布流量控制：为了避免线上问题影响到线上用户，建议小流量灰度发布，在线上回归没有问题后再逐步放量
- 项目上线后，建议做一次项目复盘，看看那些地方做得不好，要分析原因并找到解决方案；那些地方做得好，以后继续保持。

通过复盘这个环节，可以总结经验并更好地规范项目流程。