---
layout:     post
title:      "Allure Severity Level"
subtitle:   "Allure Severity Level"
date:       2023-11-28
author:     "Gavin Wang"
catalog:    true
img: "/img/pytest/allure.jpg"
summary: Modify Allure Severity Level
categories: 
    - [Automation]
    - [Allure]
tags:
    - Automation
    - Allure
---


# 概述

之前项目中一直使用allure来完成html可视化报告的输出，对于一些测试用例级别，如Bigtera使用的是TestLink，设置用例的级别为：

* Release Acceptance Test(RAT)
* Functional Acceptance Simple Test(FAST)
* Task-Oriented Function Test(TOFT)
* Force-Error Test(FET)
* Boundary Test
* Volume Test
* Stress Test 
    
大概可以分为：RAT > FAST > TOFT = Boundary = FET > Volume = Stress 


也有的公司将用例级别定义为P0, P1, P2之类的级别，数字越小表明功能越核心，描述如下：

* P0： 核心功能测试用例（冒烟测试），确定此版本是否可测的测试用例，此部分测试用例如果fail会阻碍大部分其他测试用例的验证
* P1： 高优先级测试用例，最常执行以保证功能性是稳定的；基本功能测试，和重要的错误、边界测试
* P2： 中优先级测试用例，更全面的验证功能的各个方面，异常测试，边界、中断、断网、容错、UI等测试用例
* P3:  一般错误，错误不是很明星，小问题，客户要求改善需求体验等问题
* P4:  增加用户体验的建议问题，类似enhancement


说了这么多，马上到本文要探讨的核心问题了：

allure支持的用例级别为:

* blocker
* critical
* normal
* minor
* trivial

如何将各家自定义的用例级别与allure进行关联呢？

就是说，如何在allure中显示P0/P1/P2/P3 或者 RAT/FAST/TOFT/FET 之类的级别信息在allure html报告中？

一直想解决这个问题，但是allure原生就不支持哦。

# 过程

搜索到一篇文章：``` https://github.com/allure-framework/allure-js/issues/428 ```

这篇文章介绍了作者如上的想法，结果作者以失败而告终。所以：

* 修改js文件
* 修改自己编写的测试用例中的自带级别

上述两个方法，都是无法满足要求的。

于是我找了allure的源码：

``` allure2-2.24.1/allure-generator/src/main/javascript/components/graph-severity-chart/SeverityChartView.js ```

这个js文件中定义了用例的级别：

``` const severities = ["blocker", "critical", "normal", "minor", "trivial"]; ```

在 ``` allure2-2.24.1/allure-generator/src/main/java/io/qameta/allure/severity/SeverityLevel.java ```文件中定义了一个枚举类型：

```shell
public enum SeverityLevel implements Serializable {

    BLOCKER("blocker"),
    CRITICAL("critical"),
    NORMAL("normal"),
    MINOR("minor"),
    TRIVIAL("trivial");
```


在allure安装好的路径下，查看了allure lib目录下的jar包，有一个名称为 ``` allure-generator-2.24.1.jar ```， 这个文件很显然是``` allure2-2.24.1/allure-generator/src/main/java/io/qameta/allure/severity/SeverityLevel.java ``` 所生成的jar包。

到这里，理论上修改java和js文件，重新编译生成jar包，替换掉  ``` allure-generator-2.24.1.jar ```， 理论上是可以解决掉本文讨论的问题。由于个人没有java开发环境与IDE，就没有再继续往下尝试了。


# 综述

{% note success %}
方法一： 修改源码
{% endnote %}

修改 allure java源码重新生成jar。


{% note success %}
方法二： 修改用例中级别
{% endnote %}

修改测试用例中用例级别，使之匹配allure，比如直接修改数据库。

个人而言，看需要，对于一些无伤大雅的信息展示，无需花费过多时间，打磨更健壮的自动化测试框架才是重中之重，像更换allure默认logo，修改测试用例级别等等一些动作，都是锦上添花，有更好，无则也没啥损失。

