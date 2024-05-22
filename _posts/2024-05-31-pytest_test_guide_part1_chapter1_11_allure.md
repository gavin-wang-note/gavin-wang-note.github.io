---
title: 《pytest测试指南》-- 章节1-11 pytest与Allure结合生成测试报告
date: 2024-05-31 23:00:00
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
summary: 《pytest测试指南》一书 章节1-11 Allure详解，以及pytest与Allure结合生成测试报告
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 第11章 pytest与Allure结合生成测试报告

# 11.1 Allure框架介绍

在测试自动化的世界里，创建直观、内容丰富的测试报告是至关重要的。测试报告不仅为测试结果提供透明度，还作为沟通工具，帮助开发者、测试人员和利益相关者之间建立信任。`Allure Framework` 是一个轻量级且富有表现力的测试报告工具，它可以提供清晰的分析和详细的测试报告。与许多测试框架（如 `pytest、JUnit、TestNG `等）兼容，`Allure` 让自动化测试结果更加易于理解和阅读，使得测试工程师和开发人员能够从中获取有用的信息，以便快速确定问题和改进点。

`Allure Framework` 具有如下特点：

- **丰富的报告内容**：报告不仅展示了测试是否通过，还展示了测试失败的原因，以及测试执行的具体步骤。
- **详细的测试步骤及附件**：允许用户为测试用例提供详细的步骤描述，并且可以添加附件（如屏幕截图、日志文件等），以便在分析测试结果时提供额外的上下文信息。
- **优雅的界面和交互效果**：Allure 提供了一个现代化的 Web 界面，支持多种交互操作，比如过滤器和搜索，可以快速找到所需的测试信息。
- **测试历史和趋势分析**：Allure 能够跟踪测试执行的历史记录，并提供趋势分析，帮助用户识别潜在的问题。
- **缺陷管理**：可以将测试结果链接到问题跟踪系统（如 JIRA），这将有助于跟踪和管理软件中的缺陷。
- **失败分类和重试机制分析**：支持对失败的测试用例进行分类，并能够分析测试用例因为重试而产生的状态变化。
- **环境信息**：可以捕获执行测试时的环境信息，如操作系统、浏览器版本、自定义变量等，这提供了关于测试条件的重要见解。
- **参数化测试的支持**：Allure 可以展示参数化测试的每个实例及其结果，使得具有不同参数的同一测试用例的结果清晰明了。
- **标签和严重性级别**：允许用户使用标签来组织测试，并设置不同的严重性级别（比如 blocker, critical, normal, minor, trivial），这有助于测试结果的优先级排序。
- **集成**：支持与不同的持续集成工具集成，比如 Jenkins、TeamCity，可以在构建流程完成后生成和查看测试报告。
- **开源且社区支持**：Allure 是一个开源项目，有着活跃的社区支持，不断有新功能和改进加入。

`allure-pytest` 作为一个充满活力的报告工具，将测试自动化提升到了新的层次，它所生成的详尽报告覆盖了从简单的测试结果到复杂的测试分析。在本章节中，我们将基于`allure 2.25.0` 版本探索 `allure-pytest` 的强大之处，并一步步指导你如何将其融入到你的 `pytest` 测试框架中，优雅地输出可视化的测试报告。

你将学习到:

- 如何安装和配置 `allure-pytest` 与 pytest 一同工作。
- `allure-pytest` 的基础知识及其为何受到广泛欢迎。
- 编写测试用例时如何使用 Allure 的注解和装饰器来增强报告内容。
- 如何生成并查看 Allure 报告，并从中获取有价值的洞察。

随着软件开发迈向敏捷和DevOps文化，测试自动化和持续集成成了质量保证的基石。`allure-pytest` 提供的详细和交互性报告正是这一转变的完美补充。让我们开始吧！

# 11.2 Allure如何生成报告

`Allure` 报告的生成通常涉及两个步骤：首先，运行测试以收集测试数据；其次，使用 `Allure` 命令行工具来生成可视化报告。以下是详细的步骤：

## 11.2.1 安装 Allure CLI 工具

你需要确保你已经安装了 `Allure` 命令行工具，可以访问如下网址：`https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/`

获取最新版本的`allure-commandline`，此处我们选择：`2.25.0`版本，下载并解压到`/usr/lib`目录下：

```shell
wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.25.0/allure-commandline-2.25.0.tgz
```

由于`Allure`是`Java`开发的，需要配置`JAVA_HOME`等环境变量，这里我们安装一下`jre-8u171-linux-x64.tar`，将`jre`解压到`/usr/lib`目录下，修改`~/.bashrc`，在尾部增加如下内容，并`source`一下`.bashrc`文件使得设置生效：

```shell
tar -zxvf jre-8u171-linux-x64.tar.gz -C /usr/lib
```

在`.bashrc`文件尾部增加如下内容：

```shell
export JAVA_HOME=/usr/lib/jre1.8.0_171
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
alias allure='/usr/lib/allure-2.25.0/bin/allure'
```

最后执行`source .bashrc`命令即可生效。

需要注意的是，具体的设置方式可能会根据你的操作系统有所不同。

## 11.2.2 集成 Allure 到你的测试框架中

如果你使用的是 `pytest`，那么你需要安装 `allure-pytest` 插件。这可以通过 pip 完成：

```sh
pip install allure-pytest
```

## 11.2.3 运行测试并生成数据

当你运行测试时，需要指定一个目录来存储 `Allure` 报告所需的结果文件。以下是一个使用 `pytest` 运行测试并生成结果文件的示例：

```sh
pytest --alluredir=/path/to/allure/results your_test_directory/
```

这将执行 `your_test_directory/` 下的所有测试，并将结果文件保存在指定的路径 `/path/to/allure/results` 中。

## 11.2.4 生成 Allure 报告

拥有了测试结果数据后，你可以使用 Allure CLI 生成报告：

```sh
allure serve /path/to/allure/results
```

上述命令将处理结果文件，并在默认浏览器中自动打开生成的 Allure 报告。你也可以先生成报告，然后手动打开它：

```sh
allure generate /path/to/allure/results -o /path/to/allure/report --clean
```

这将在 `/path/to/allure/report` 目录生成报告。如果使用 `--clean` 标志，它会在生成新报告之前清理老的报告文件。然后你可以使用任何Web服务器来提供这个目录的内容，或者简单地打开 `index.html` 文件来查看报告。

# 11.3 Allure 报告组成

`Allure` 报告由七部分构成，分别是：

* 概览（Overview)
* 类别（Categories）
* 测试套（Suites）
* 图表（Graphs）
* 时间刻度（Timeline）
* 功能（Behaviors）
* 包（Packages）

每个部分提供了不同的信息，以帮助你更好地理解和分析测试执行情况。下面是报告的各个组成部分以及它们的含义介绍。

## 11.3.1 概览（Overview）

这是进入报告时看到的第一屏内容，提供了测试执行的高层次摘要。包括以下几个部分：

- **报告统计（ALLURE REPORT）**: 显示测试的总体情况，如总共运行了多少测试用例，以及它们中有多少通过、失败、跳过或引发了错误，以环形图展示，不同颜色对应不同用例执行状态，并显示百分比。
- **测试套（SUITES）**：按失败用例数从多到少顺序展示`Top 10`的用例执行结果。
- **趋势（TREND）**: 展示了一段时间内测试结果的趋势。
- **类别（CATEGORIES）**: 显示了失败的测试用例中分布的问题类型，如产品缺陷（`Product defects`）和测试缺陷（`Test defects`），主要为`Critical`级别错误的用例信息。
- **运行器（EXECUTORS）**：展示运行用例的载体，如`Jenkins`，并有具体的`Build ID`与链接跳转。
- **环境（ENVIRONMENT）**：自定义环境变量，比如测试环境的IP地址、开始运行时间、结束时间、产品版本信息等个人自定义数据。
- **特性场景（FEATURES BY STORIES）**：跳转到Behaviors页面`Product defects`和`Test defects`数据。

Overview如下图所示：

<img class="shadow" src="/img/in-post/allure_overview.png" width="800">


## 11.3.2 类别（Categories）

类别（Categories）是用于将测试结果分组的一种方式。这个特性使得用户能够根据不同的标准对测试用例进行分类。例如，根据用例是否成功、失败的原因、是否跳过执行等，可以将测试结果分组。类别有助于快速找到特定类型的问题，从而专注于解决高优先级的测试失败。

类别通常是在报告生成前预先定义好的，并且具有以下几个特点：

* **自定义性**：用户可以根据测试结构和需求来创建自己的类别。
* **灵活性**：类别可以基于多种条件来定义，例如失败类型（如断言错误、测试环境问题、编码异常等），测试的严重性等级等。
* **可配置性**：类别通过 Allure 配置文件进行设置，该文件指定了哪些类型的测试错误应该属于哪个类别。

在 Allure 报告中，一旦分类设置完成并且测试执行，失败的测试用例会根据配置文件中的规则被归入不同的类别。当查看报告时，我们可以选择 "Categories" 选项：

- 每个类别都会列出归入该类别的测试用例。
- 用户可以点击类别名称展开和查看具体的用例。
- 对于每个测试用例，我们可以查看失败的详细信息、附件和其他相关数据。

例如，分类可以用来区分如下问题：

- **产品缺陷**：失败的测试用例揭示了产品代码中的错误。
- **测试缺陷**：测试用例编写有误，导致不合理的失败。
- **环境问题**：由于配置错误、外部服务不可用等环境问题而导致的失败。
- **忽略的测试**：被标为 @Ignore 或其他方式明确跳过的测试。
- **中断的测试**：由于某些意外中断测试执行的情况。

在报告中展示如下图所示：

<img class="shadow" src="/img/in-post/allure_categories.png" width="800">

通过为你的项目定制类别，你将能够更有效地组织测试结果，并快速定位与分析测试失败的原因。这在大型项目和复杂测试场景中尤其有用，因为它减少了在失败堆栈中手动搜索的需要，并通过将相关的失败聚集在一起以提高解决问题的效率。

## 11.3.3 测试套（Suites）

在 Allure 报告中，测试套件（Suites）是指一套相关联的测试用例集合。这个概念是从传统的单元测试框架借鉴过来的，其中一个套件通常会包含一组具有相同测试目的或测试同一个功能模块的单元测试。在使用 Allure with pytest 时，测试套件的概念类似，但更加灵活和广泛。

每一个测试套件可以包含一个或多个测试用例。在Allure报告中，通常会显示如下信息：

* **套件名称（Suite Name）**：
  对应于TestFixture或者Python模块的名称。这对于组织和识别相关测试很有帮助。

* **子套件（Sub Suites）**：
  可以进一步细化套件结构。比如Python中某个类或者方法可以定义成子套件。

* **测试用例（Test Cases）**：
  这是测试套件中最细粒度的单元，通常对应于一个测试函数或方法。

* **测试步骤（Test Steps）**：
  测试用例可能会细分为更细的操作步骤，尤其在使用了Allure装饰器来标注步骤的情况下。

* **持续时间（Duration）**：
  报告中通常会显示每个测试套件及其包含的测试用例的执行时间，这有助于识别性能问题或某些异常耗时的测试。

* **测试结果（Test Result）**：
  包含了测试用例的执行结果，比如：passed（通过）、failed（失败）、skipped（跳过）等。

* **附件（Attachments）**：
  如果测试用例生成了附件，如截图、日志等，它们将与相应的测试用例关联显示。

在 Allure 报告中，测试套件通过可视化的方式来组织测试用例，通过这种组织结构可以帮助用户在一个单独的视图中看到所有相关测试的状态。这对于识别特定的功能或组件的稳定性、修复测试中的问题、以及观察测试进展非常有用。

通常，在 pytest 中，一个测试文件会被看做是一个套件，文件中不同的类可能对应子套件，类中的测试方法就是具体的测试用例。

在报告中展示如下图所示：

<img class="shadow" src="/img/in-post/allure_suits.png" width="800">



## 11.3.4 图表（Graphs）

Allure 报告的图表（Graphs）部分提供了一种直观的方式来分析测试结果的各种方面。图表通过可视化地展示测试数据，让用户能够快速洞察测试的各种维度，比如严重性分布、持续时间趋势、测试状态概述等。以下是图表部分常见的几种图表及其解释：

* **状态（STATUS）**:
  状态环形图展示了在一系列的测试执行过程中不同测试状态的占比情况，按`Faild, Broken, Passed, Skipped, Unknown`五种维度展示。

* **严重性（SEVERITY）**:
  这个图表显示了不同严重性级别的测试用例随着时间的变化趋势。它有助于理解在不同严重级别下测试用例执行结果的分布，以`block,critical,normal,minor,trivial`五种级别柱状图展示。

* **持续时间（DURATION）**:
  持续时间柱状图是展示测试用例执行时间分布图，这个图表有助于识别和监控哪些用例比较消耗时间，横轴单位为分钟，纵轴单位为对应时间段内用例的数量。

* **持续时间趋势（DURATION TREND）**:
  持续时间趋势图是展示测试执行时间随测试迭代逐渐变化的趋势。这个图表有助于识别和监控可能影响测试速度的问题和性能瓶颈。
* **检测结果趋势（RETRIES TREND）**:
  在测试中使用了重试机制时，重试趋势图表展示了测试用例从失败到成功需要重试的次数。
* **失败分类（CATEGORIES TREND）**:
  失败分类图表显示的是按照预先定义的失败类型分类的测试用例失败情况，有助于快速识别最常见的失败原因。

* **摘要（Summary）**:
  摘要图展示了全部测试用例按照结果状态分类的摘要信息，通常包括通过、失败、跳过等状态的用例数量。

* **趋势（Trend）**:
  对测试用例的可靠性和稳定性进行跟踪，趋势图将展示测试用例的比例随时间的变化。

各个图表参加下图：

<img class="shadow" src="/img/in-post/allure_status_severity.png" width="800">

<img class="shadow" src="/img/in-post/allure-duration_and_trend.png" width="800">

<img class="shadow" src="/img/in-post/allure_retries_categories_trend.png" width="800">

<img class="shadow" src="/img/in-post/allure_trend.png" width="800">

这些图表不仅能提供单次测试运行的快照，还能展示随着时间推移和多次测试迭代的趋势。这些数据对于测试团队持续改进测试实践、提升软件质量、优化自动化测试策略等方面非常有价值。

## 11.3.5 时间刻度（Timeline）

在 Allure 报告中，时间刻度（Timeline）部分提供了对测试执行时间的详细视图。这个功能特别有助于了解测试用例是如何在时间上分布的，尤其是在并行测试执行的情况下。时间轴可以展示每个测试用例的执行时间和顺序，从而帮助识别性能问题、并行执行的效率，以及可能的资源争用问题。

时间轴主要包括以下几个方面的信息：

* **测试用例的开始和结束时间**： 每个测试用例的执行时间在时间轴上以条形图的方式展示，可以清楚地看到每个测试用例的开始和结束时间。

* **测试持续时间**： 时间轴显示了每个测试用例实际花费的时间，这对于检测长时间运行的测试用例非常有用。

* **测试的并行执行**： 在进行并行测试时，时间轴可以帮助你识别测试用例是如何被同时执行的。这对于优化测试套件的并行性能非常重要。

* **时间分布**： 时间轴显示了测试用例在整个测试周期内的分布情况，有助于识别测试过程中的任何异常延迟或拥堵。

* **详细的测试信息**： 点击特定的测试用例，可以查看该用例的更多详细信息，如状态、失败原因等。

时间刻度（Timeline）如下图所示：

<img class="shadow" src="/img/in-post/allure_timeline.png" width="800">

时间轴视图对于测试管理和优化非常重要，尤其是在持续集成/持续部署（CI/CD）的环境中。它不仅可以帮助团队识别性能问题，还可以优化测试执行策略，例如，通过更好的分配测试用例到不同的运行环境中，或者调整并行运行的测试用例数量。



## 11.3.6 功能（Behaviors）

在 Allure  报告中，功能（Behaviors）部分提供了一种独特的视角来查看和组织测试结果，这种视角有助于更清晰地了解测试覆盖的业务范围，以及每个用例的详细信息，诸如用例的Overview，History和Retries三大分类信息，Overview为用例当前状态，History为此用例的历史执行状态，Retries为此用例历史上retry记录，如下图所示：

<img class="shadow" src="/img/in-post/allure_Behaviors.png" width="800">



## 11.3.7 包（Packages）

在 Allure 的 HTML 报告中，"Packages"（包）部分提供了一种按照测试架构的组件视角来审视和组织测试结果的方式。这里的 "包" 通常反映了测试用例在源代码中的实际布局，比如根据 Python 包和模块的结构进行分组。这有助于理解测试用例之间的逻辑分组，它基于测试代码在物理文件系统中的组织方式。

"Packages" 部分主要提供以下信息：

* **包结构视图**：
  这个视图显示了项目源代码中包和模块的层次结构。通常，这会以一种类似于文件系统浏览器的界面显示，其中展开的树形结构代表了不同级别的包和子包。

* **测试用例分布**：
  "Packages" 视图也展示了属于特定包（例如 Python 中的模块）的测试用例。你可以看到每个包里面有哪些测试用例，以及它们的状态（通过、失败、跳过等）。

* **详细的测试结果**：
  点击特定的测试用例或包，你能获得更多的细节（比如测试步骤、附件、失败信息等），以及对该用例进行了哪些操作。

* **代码组件的测试覆盖情况**：
  通过审查各个包中的测试用例状态，可以评估不同代码组件的测试覆盖情况和质量。如果一个包中大部分的测试用例都失败了，这可能是一个值得关注的信号。

在报告中展示如下图所示：

<img class="shadow" src="/img/in-post/allure_packages.png" width="800">

"Packages" 视图有助于开发人员和测试工程师在较高的层次上进行问题诊断，因为它们可以轻松地识别出哪些代码组件可能存在问题，并快速导航到具体的问题用例。

# 11.4 Allure功能介绍

## 11.4.1 帮助 --help

当你从命令行运行 `allure -h` 时，你实际上是在调用 Allure 命令行工具（Allure Commandline），而不是 `allure-pytest` 插件。Allure Commandline 用于生成、查看和管理 Allure 报告。

下面是一般当你执行 `allure -h` 或 `allure --help` 时可能会看到的输出。我将提供一个概览，但请注意命令和参数可能会随着版本更新而发生变化。在运行实际命令以获得最新的帮助信息，参考如下：

```shell
root@Gavin:~# allure -h
Could not parse arguments: Expected a command, got -h
Usage: allure [options] [command] [command options]
  Options:
    --help
      Print commandline help.
    -q, --quiet
      Switch on the quiet mode.
      Default: false
    -v, --verbose
      Switch on the verbose mode.
      Default: false
    --version
      Print commandline version.
      Default: false
  Commands:
    generate      Generate the report
      Usage: generate [options] The directories with allure results
        Options:
          -c, --clean
            Clean Allure report directory before generating a new one.
            Default: false
          --config
            Allure commandline config path. If specified overrides values from 
            --profile and --configDirectory.
          --configDirectory
            Allure commandline configurations directory. By default uses 
            ALLURE_HOME directory.
          --profile
            Allure commandline configuration profile.
          -o, --report-dir, --output
            The directory to generate Allure report into.
            Default: allure-report
          --single-file
            Generate Allure report in single file mode.
            Default: false

    serve      Serve the report
      Usage: serve [options] The directories with allure results
        Options:
          --config
            Allure commandline config path. If specified overrides values from 
            --profile and --configDirectory.
          --configDirectory
            Allure commandline configurations directory. By default uses 
            ALLURE_HOME directory.
          -h, --host
            This host will be used to start web server for the report.
          -p, --port
            This port will be used to start web server for the report.
            Default: 0
          --profile
            Allure commandline configuration profile.

    open      Open generated report
      Usage: open [options] The report directory
        Options:
          -h, --host
            This host will be used to start web server for the report.
          -p, --port
            This port will be used to start web server for the report.
            Default: 0

    plugin      Generate the report
      Usage: plugin [options]
        Options:
          --config
            Allure commandline config path. If specified overrides values from 
            --profile and --configDirectory.
          --configDirectory
            Allure commandline configurations directory. By default uses 
            ALLURE_HOME directory.
          --profile
            Allure commandline configuration profile.


root@Gavin:~#
```

常见的 Allure Commandline 参考下表：

| 命令          | 用法               | 选项                       | 描述                         |
| ------------- | ------------------ | -------------------------- | ---------------------------- |
| generate      | generate [options] | -c, --clean                | 清除现有报告目录并生成新报告 |
|               |                    | --config                   | Allure命令行配置路径         |
|               |                    | --configDirectory          | Allure命令行配置文件目录     |
|               |                    | --profile                  | Allure命令行配置文件         |
|               |                    | -o, --report-dir, --output | 指定生成的报告目录路径       |
| serve         | serve [options]    | --config                   | Allure命令行配置路径         |
|               |                    | --configDirectory          | Allure命令行配置文件目录     |
|               |                    | -h, --host                 | 指定报告服务的域名           |
|               |                    | -p, --port                 | 指定报告服务的端口           |
|               |                    | --profile                  | Allure命令行配置文件         |
| open          | open [options]     | -h, --host                 | 指定打开报告的主机           |
|               |                    | -p, --port                 | 指定打开报告的端口           |
| plugin        | plugin [options]   | --config                   | Allure命令行配置路径         |
|               |                    | --configDirectory          | Allure命令行配置文件目录     |
|               |                    | --profile                  | Allure命令行配置文件         |
| -h, --help    |                    |                            | 打印帮助信息                 |
| -q, --quiet   |                    |                            | 后台静默模式                 |
| -v, --verbose |                    |                            | 开启详细日志模式             |
| --version     |                    |                            | 打印命令行版本               |

## 11.4.2 Environment

环境变量参数，设置运行环境参数，比如可以显示被测版本信息，什么时间开始测试，什么时间测试结束，耗时多久之类的信息。默认为空，需要创建environment.properties文件，或者environment.xml文件，并把文件存放存储结果的path中，如果不携带，则展示为空，如下图所示：


<img class="shadow" src="/img/in-post/environment_empty.png" width="800">



### 11.4.2.1 environment.properties

```shell
PRODUCT_VERSION=VirtualStor Scaler V8.0-269
START_TIME=2021-11-03 21:36:57
END_TIME=2021-11-04 06:29:46
TEST_COUNTS=2596
TEST_PASS=2537
TEST_FAIL=31
TEST_SKIP=27
TEST_BROKEN=1
TEST_UNKNOW=0
TIME_DURATION=31969
```

### 11.4.2.2 environment.xml

```shell
<environment>
    <parameter>
        <key>PRODUCT_VERSION</key>
        <value>VirtualStor Scaler V8.0-269</value>
    </parameter>
    <parameter>
        <key>START_TIME</key>
        <value>2021-11-03 21:36:572</value>
    </parameter>
    <parameter>
        <key>END_TIME</key>
        <value>2021-11-04 06:29:46</value>
    </parameter>
    <parameter>
        <key>TEST_COUNTS</key>
        <value>2596</value>
    </parameter>
    <parameter>
        <key>TEST_PASS</key>
        <value>2537</value>
    </parameter>
    <parameter>
        <key>TEST_FAIL</key>
        <value>31</value>
    </parameter>
    <parameter>
        <key>TEST_SKIP</key>
        <value>27</value>
    </parameter>
    <parameter>
        <key>TEST_BROKEN</key>
        <value>1</value>
    </parameter>
    <parameter>
        <key>TEST_UNKNOW</key>
        <value>0</value>
    </parameter>
    <parameter>
        <key>TIME_DURATION</key>
        <value>31969</value>
    </parameter>
</environment>
```

## 11.4.3 Categories

将测试用例结果进行分类,默认情况下，有两类缺陷：

* Product defects 产品缺陷（测试结果：failed）
* Test defects 测试缺陷（测试结果：error/broken）

可以创建自定义缺陷分类的，将 `categories.json` 文件添加到`allure-results`目录即可（和上面`environment.properties`放同一个目录），示例参考如下：

```shell
[
  {
    "name": "Ignored tests", 
    "matchedStatuses": ["skipped"] 
  },
  {
    "name": "Infrastructure problems",
    "matchedStatuses": ["broken", "failed"],
    "messageRegex": ".*bye-bye.*" 
  },
  {
    "name": "Outdated tests",
    "matchedStatuses": ["broken"],
    "traceRegex": ".*FileNotFoundException.*" 
  },
  {
    "name": "Product defects",
    "matchedStatuses": ["failed"]
  },
  {
    "name": "Test defects",
    "matchedStatuses": ["broken"]
  }
]
```

参数的含义

- **name**：分类名称，可以是中文
- **matchedStatuses**：测试用例的运行状态，默认["failed", "broken", "passed", "skipped", "unknown"]
- **messageRegex**：测试用例运行的错误信息，默认是 .* ，是通过正则去匹配的
- **traceRegex**：测试用例运行的错误堆栈信息，默认是 .* ，也是通过正则去匹配的

结合上面文件后，放在report原始文件目录下，生成的可视化报告参考如下：

<img class="shadow" src="/img/in-post/environment_OK.png" width="800">



## 11.4.4 Allure属性

allure有如下属性：

```shell
root@Gavin:~# python3
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import allure
>>> dir(allure)
['__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'attach', 'attachment_type', 'description', 'description_html', 'dynamic', 'epic', 'feature', 'id', 'issue', 'label', 'link', 'manual', 'parameter_mode', 'parent_suite', 'severity', 'severity_level', 'step', 'story', 'sub_suite', 'suite', 'tag', 'testcase', 'title']
>>> 
```

介绍如下：

| 使用方法                  | 参数值                                         | 参数说明                                                     |
| ------------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| allure.attach()           | 添加附件                                       | 给测试用例添加附件                                           |
| allure.attachment_type()  | 附件类型                                       | 支持txt/pdf/csv/html/xml/image/video等多种类型               |
| allure.description()      | 用例描述                                       | 传递一个字符串参数用来描述测试用例                           |
| allure.description_html() | 用例描述                                       | 传递一段HTML文本，这将在测试报告的"Description"部分渲染出来  |
| allure.dynamic()          | 动态指定标题和描述                             | 在测试用例执行过程中动态指定标题和描述等标签的方法，主要指：allure.dynamic.description 和 allure.dynamic.title |
| allure.epic()             | epic描述                                       | 敏捷里的概念，定义史诗，相当于module级的标签                 |
| allure.feature()          | 模块名称                                       | 功能点的描述，往下是story                                    |
| allure.id()               | 人为给用例添加id（唯一标识）                   | 这个标识符将显示在 Allure 报告中，使得识别和引用这个具体的测试更加方便。 |
| allure.issue()            | 缺陷链接                                       | 对应缺陷管理系统里的链接，如将JIRA里Bug的URL展示在html报告中 |
| allure.label()            | 给用例添加label                                | 指定多种类型的标签，例如功能、故事、严重性级别、测试用例ID、发行版本等。 |
| allure.link()             | 链接                                           | 定义一个链接，在html报告中展示                               |
| allure.manual()           | 指示一个测试用例是手动执行的，而不是自动化测试 | 将手动测试用例纳入到自动生成的 Allure 测试报告中，从而在报告中提供一个更全面的测试覆盖视图 |
| allure.parameter_mode()   | 处理多种输入条件                               | 在测试用例中使用多组不同的输入参数，从而可以对同一个测试用例进行多次测试，每次使用不同的数据 |
| allure.parent_suite()     | 测试套                                         | 测试套的三个级别，爷爷父亲儿子中的爷爷这个级别               |
| allure.severity()         | 用例级别                                       | 测试用例的优先级别，blocker,critical,normal,minor,trivial 五个级别，使用方式：@allure.severity("BLOCKER") |
| allure.severity_level()   | 用例级别                                       | 测试用例的优先级别，blocker,critical,normal,minor,trivial 五个级别，使用方式：@allure.severity(allure.severity_level.CRITICAL) |
| allure.step()             | 操作步骤                                       | 测试用例的步骤，Step1，Step2，... StepN标记在用例中          |
| allure.story()            | 用户故事                                       | 用户故事，往下是title                                        |
| allure.sub_suite()        | 测试套                                         | 测试套的三个级别，爷爷父亲儿子中的儿子这个级别               |
| allure.suite()            | 测试套                                         | 测试套的三个级别，爷爷父亲儿子中的父亲这个级别               |
| allure.tag()              | Tag                                            | 给用例增加tag                                                |
| allure.testcase()         | 测试用例的链接                                 | 对应功能/性能测试用例系统里的test case URL，如testlink里的   |
| allure.title()            | 用例的标题                                     | 展示在html报告中的测试用例的标题名称                         |

## 11.4.5 Allure 实践

### 11.4.5.1 Allure为测试用例添加附件（attach）

#### 11.4.5.1.1 allure.attach的用法

**用法一：**

语法：

```shell
allure.attach(body, name, attachment_type, extension)
```

参数解释：

- body：要写入附件的内容
- name：附件名字
- attachment_type：附件类型，是allure.attachment_type其中的一种
- extension：附件的扩展名

**用法二：**

语法：

``` shell
allure.attach.file(source, name, attachment_type, extension)
```

参数解释：

- source：文件路径，相当于传一个文件
- name：附件名字
- attachment_type：附件类型，是allure.attachment_type其中的一种
- extension：附件的扩展名

#### 11.4.5.1.2 allure.attachment_type的所有值


```shell
    TEXT = ("text/plain", "txt")
    CSV = ("text/csv", "csv")
    TSV = ("text/tab-separated-values", "tsv")
    URI_LIST = ("text/uri-list", "uri")
    HTML = ("text/html", "html")

    XML = ("application/xml", "xml")
    JSON = ("application/json", "json")
    YAML = ("application/yaml", "yaml")
    PCAP = ("application/vnd.tcpdump.pcap", "pcap")
    PDF = ("application/pdf", "pdf")

    PNG = ("image/png", "png")
    JPG = ("image/jpg", "jpg")
    SVG = ("image/svg-xml", "svg")
    GIF = ("image/gif", "gif")
    BMP = ("image/bmp", "bmp")
    TIFF = ("image/tiff", "tiff")

    MP4 = ("video/mp4", "mp4")
    OGG = ("video/ogg", "ogg")
    WEBM = ("video/webm", "webm")
```

#### 11.4.5.1.3 allure.attach使用举例

##### 11.4.5.1.3.1 测试用例中添加文本附件

```python
# content of test_allure_attach.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure


@pytest.fixture()
def attach_for_text():
    allure.attach(body="前置条件，这是一段文本", name="Test文本01", attachment_type=allure.attachment_type.TEXT)
    yield
    allure.attach(body="后置条件，这是一段文本", name="Test文本02", attachment_type=allure.attachment_type.TEXT)


def test_attachment_text(attach_for_text):
    assert True
```

效果如下图所示：

<img class="shadow" src="/img/in-post/allure/attach_text.png" width="800">

##### 11.4.5.1.3.2 测试用例中添加html附件

```python
# content of test_allure_multiple_attachments.py
import allure

def test_mutiple_attachments():
    allure.attach.file(r"/root/Pictures/OIP-C.jpg", attachment_type=allure.attachment_type.JPG)

    allure.attach("""<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>My test page</title>
  </head>
  <body>
    <img src="https://ts1.cn.mm.bing.net/th/id/R-C.2c7e4d41fc29592168145efb4c27f825?rik=EfVURrooBsEe%2bg&riu=http%3a%2f%2fimg.juimg.com%2ftuku%2fyulantu%2f110611%2f9120-110611114P085.jpg&ehk=ruz2W6AZs%2bLUNeJ83%2ferKheRxWYQyYFYt5GGHhnu4BI%3d&risl=&pid=ImgRaw&r=0" alt="My test image" />
  </body>
</html>
""",
attachment_type=allure.attachment_type.HTML)
```

效果如下图所示：

<img class="shadow" src="/img/in-post/allure/attach_image.png" width="800">

如上图所示，html部分可以嵌套图片，也可以写静态文本。

### 11.4.5.2 Allure添加测试用例步骤(allure.step)

在编写自动化测试用例的时候经常会遇到需要编写流程性测试用例的场景，一般流程性的测试用例的测试步骤比较多，在测试用例中添加详细的步骤会**提高测试用例的可阅读性**。

allure提供的装饰器@allure.step()是allure测试报告框架非常有用的功能，它能帮助我们在测试用例中对测试步骤进行详细的描述。

代码示例：

```python
def test_566_rollback_snapshot(self):
    """  Sc-566:Snapshot can be rollbacked correctly  """
    with allure.step("Clean unavailable link device"):
        self.client_unlink_unavailable_device_link(self.client_ip_root_password, self.ssh_port, self.client_ip)

    with allure.step("Client umount mount point"):
        self.client_umount_san_device(gateway_group=self.gateway_group, target_id=self.target_id,                                                                 iscsi_id=self.iscsi_id,                                                                   password=self.client_ip_root_password,
                                      port=self.ssh_port, client_ip=self.client_ip,
                                      mount_point=self.mount_point,
                                      check_device=False)
    with allure.step("Client login target"):
        self.client_login_logout_target(self.client_ip_root_password, self.ssh_port,
                                        self.client_ip, self.target_id, op_type='logout')
        self.client_login_logout_target(self.client_ip_root_password, self.ssh_port,
                                        self.client_ip, self.target_id, op_type='login')

    with allure.step("Client mkfs the device, then input a file, and get the md5 for the file"):
        self.client_mkfs_san_device(gateway_group=self.gateway_group, target_id=self.target_id, 
                                    iscsi_id=self.iscsi_id, password=self.client_ip_root_password,
                                    port=self.ssh_port, client_ip=self.client_ip)
        self.client_mount_san_device(gateway_group=self.gateway_group, target_id=self.target_id, 
                                     iscsi_id=self.iscsi_id, password=self.client_ip_root_password,
                                     port=self.ssh_port, client_ip=self.client_ip,
                                     mount_point=self.mount_point)

    with allure.step("Copy some files to the mapped drive"):
        self.client_write_file_to_san(password=self.client_ip_root_password,
                                      port=self.ssh_port, client_ip=self.client_ip, 
                                      mount_point=self.mount_point,
                                      file_name='before_snap.txt',
                                      ile_content='before_snap')
    time.sleep(60)
    before_md5 = self.get_file_md5(password=self.client_ip_root_password, 
                                   port=self.ssh_port, client_ip=self.client_ip,
                                   mount_point=self.mount_point,
                                   file_name='before_snap.txt')

    with allure.step("Take a snapshot"):
        self.create_snapshot(gateway_group=self.gateway_group, target_id=self.target_id,
                             iscsi_id=self.iscsi_id, snap_name='pytest-snapshot02')

    with allure.step("Client umount mount point,"):
        #  if no this step, when logout target will raise in use error in centos
        self.client_umount_san_device(gateway_group=self.gateway_group,
                                      target_id=self.target_id,
                                      iscsi_id=self.iscsi_id,
                                      password=self.client_ip_root_password,
                                      port=self.ssh_port, client_ip=self.client_ip,
                                      mount_point=self.mount_point,
                                      check_device=False)

    with allure.step("Client disconnect the target"):
        self.client_login_logout_target(password=self.client_ip_root_password, 
                                        port=self.ssh_port, client_ip=self.client_ip,
                                        target_id=self.target_id,
                                        op_type='logout')

    with allure.step("Disable the volume, then rollback snapshot"):
        self.disable_iscsi_volume(target_id=self.target_id, iscsi_id=self.iscsi_id)
        self.rollback_snap(gateway_group=self.gateway_group,
                           target_id=self.target_id, iscsi_id=self.iscsi_id)

    with allure.step("Enable the volume"):
        self.enable_iscsi_volume(gateway_group=self.gateway_group,
                                 target_id=self.target_id, iscsi_id=self.iscsi_id)

    with allure.step("Client connect to the target"):
        self.client_login_logout_target(password=self.client_ip_root_password,
                                        port=self.ssh_port, client_ip=self.client_ip,
                                        target_id=self.target_id,
                                        op_type='login')


        self.client_mount_san_device(gateway_group=self.gateway_group,
                                     target_id=self.target_id,
                                     iscsi_id=self.iscsi_id,
                                     password=self.client_ip_root_password,
                                     port=self.ssh_port, client_ip=self.client_ip,
                                     mount_point=self.mount_point)

    # Get file of md5
    after_md5 = self.get_file_md5(password=self.client_ip_root_password,
                                  port=self.ssh_port, client_ip=self.client_ip,
                                  mount_point=self.mount_point,
                                  file_name='before_snap.txt')

    with allure.step("Check md5"):
        errr_msg = "[ERROR]  before_md5 is : ({}), after_md5 is : ({}),  " \
                   "md5 is not same when reconnect to target : ({})".format(before_md5, after_md5,  self.target_id)
        eq_(before_md5, after_md5, errr_msg)

    with allure.step("Client umount"):
        self.client_umount_san_device(gateway_group=self.gateway_group,
                                      target_id=self.target_id,
                                      iscsi_id=self.iscsi_id,
                                      password=self.client_ip_root_password,
                                      port=self.ssh_port, client_ip=self.client_ip,
                                      mount_point=self.mount_point)

    with allure.step("Client disconnect the target"):
        self.client_login_logout_target(password=self.client_ip_root_password,
                                        port=self.ssh_port, client_ip=self.client_ip,
                                        target_id=self.target_id,
                                        op_type='logout')

    with allure.step("Delete all snapshot"):
        self.delete_snapshot(gateway_group=self.gateway_group,
                             target_id=self.target_id, iscsi_id=self.iscsi_id,
                             delete_all_snap=True)
```

这里借助with allure.step() 来完成添加step动作。

上述这个示例代码能否再精简呢？答案是肯定的，如何精简？

这里提供一下思路：

如果这个py文件中含有很多的test case，每个test case都需要增加allure.step，且step里描述的内容相同，可以在被调用的各个函数里增加step动作，test case里完全是函数的调用。

示例如下：

比如上例中的 delete_snapshot 函数，可以将class中定义function时，增加allure.step步骤，参考如下：

```python
    @allure.step("Delete snapshot")
    def delete_snapshot(self, gateway_group=None, target_id=None, iscsi_id=None,                                 snap_name=None, expected_return_code=None, delete_all_snap=None):
        """
        Delete a snapshot
        :param gateway_group, string, a gateway group name
        :param target_id, string, a target name
        :param iscsi_id, string, a iSCSI volume name
        :param expected_return_code, string, status code of return_code
        :param delete_all_snap, bool. True or False, default is False
        :param snapshot_name, string, snapshot name
        """
```

这样的话，在测试用例里调用此函数时，无需再额外增加@allure.step()步骤，有一定的用例编写简化作用。当然也可以在 delete_snapshot 函数里面定义内部的step，形成step的嵌套，这样阅读性会更高一些。

allure.step也**支持添加描述且通过占位符传递参数**，示例代码如下：

```python
# content of test_step_v1.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure


import pytest
import allure


@allure.step('Delete volume:"{0}" under Target:"{1}" from VirtualStoreage:"{2}"')
def step_title_with_delete_volume_name(arg1, arg2, arg3):
    pass


def test_delete_volume():
    step_title_with_delete_volume_name('iscsi-name01', 'iqn.2021-11.abc:1', 'Default')
    step_title_with_delete_volume_name('iscsi-name02', 'iqn.2021-11.target:ESXi', 'NewVS01')
    step_title_with_delete_volume_name('iscsi-name03', 'iqn.2021-11.target:PVE', 'NewVS02')
```

效果图如下：

<img class="shadow" src="/img/in-post/allure/step_parameter.png" width="800">



也可以设置传递一个/多个可选参数，不传则为None，示例如下：

```python
# content of test_step_v2.py
import allure

@allure.step('这是一个带描述语的step，并且通过占位符传递参数：positional = "{0}",keyword = "{key}"')
def step_title_with_placeholder(arg1, key=None):
    pass


def test_step_with_placeholder():
    step_title_with_placeholder(1, key="something")
    step_title_with_placeholder(2)
    step_title_with_placeholder(3, key="anything")
```

**小结：**

* allure.step支持step嵌套，即step下可以嵌套step
* allure.step支持添加描述且通过占位符传递参数

### 11.4.5.3 Allure为测试用例添加描述（description）

#### 11.4.5.3.1 Allure添加描述的三种方式

- 使用装饰器@allure.description，传递一个字符串参数用来描述测试用例
- 使用装饰器@allure.description_html，传递一段HTML文本，这将在测试报告的"Description"部分渲染出来
- 直接在测试用例方法中通过编写文档注释的方式来添加描述

我一般使用第三种，直接将Testlink上用例标题放在这里，即有title的效果，又有description效果。如果使用，具体看个人需要（如下所示）。

```python
    @allure.severity('RAT')
    @allure.link(testlink_url+'?tprojectPrefix='+testlink_prefix+'&item=testcase&id='+testlink_prefix+'-432')
    def test_432_create_nfs_folder_mode_async(self):
        """  Sc-432:Create NFS share folder, mode is async  """
        folder_name = 'pytest-' + rand_low_ascii(6)
        self.create_share_folder(folder_name, nfs='true', mode='async')
        self.delete_folder(folder_name)
        self.mds_mgr.check_cluster_state()
```

#### 11.4.5.3.2 代码示例

```python
# content of test_description.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure


@allure.description("""
这是通过传递字符串参数的方式添加的一段描述语，
使用的是装饰器@allure.description，可以换行
""")
def test_description_provide_string():
    assert 1 > 0


@allure.description_html("""
<h1>Test with some complicated html description</h1>
<table style="width:100%" border="1">
  <tr>
    <th>Name</th>
    <th>Age</th>
    <th>Sex</th>
  </tr>
  <tr align="center">
    <td>Json</td>
    <td>28</td>
    <td>男</td>
  </tr>
  <tr align="center">
    <td>Cathy</td>
    <td>23</td>
    <td>女</td>
  </tr>
</table>
""")
def test_description_privide_html():
    assert 1 == 1


def test_description_docstring():
    """
    这是通过文本注释的方式添加的描述语
    同样支持多行描述
    大家好，我是Gavin
    """
    assert True
```

allure效果图展示如下：

<img class="shadow" src="/img/in-post/allure/description_provide_string.png" width="800">

上面的测试报告是通过装饰器@allure.description传递字符串参数来添加描述语的方式。

<img class="shadow" src="/img/in-post/allure/description_docstring.png" width="800">

上面的测试报告是通过直接在测试用例方法中编写文档注释来添加描述语的方式。

<img class="shadow" src="/img/in-post/allure/description_privide_html.png" width="800">

上面的测试报告是通过装饰器@allure.description_html传递一段HTML文本来添加描述语的方式，这段HTML会渲染在报告的"Description"部分。

#### 11.4.5.3.3 Allure动态更新描述语(allure.dynamic.description)

```python
# content of test_dynamic_description.py
import allure

@allure.description("这是更新前的描述内容，在使用allure.dynamic.description后将会被更新成新的描述内容")
def test_dynamic_description():
    assert True
    allure.dynamic.description("这是通过使用allure.dynamic.description更新后的描述内容")
```

allure html展示效果如下：

<img class="shadow" src="/img/in-post/allure/dynamic_description.png" width="800">

如果assert失败或用例执行失败，是不会动态更新描述信息的：

<img class="shadow" src="/img/in-post/allure/dynamic_description_failed.png" width="800">

### 11.4.5.4 Allure为测试用例添加标题

通过使用装饰器@allure.title可以为测试用例自定义一个更具有阅读性的易读的标题。

#### 11.4.5.4.1 allure.title的三种使用方式

- 直接使用@allure.title为测试用例自定义标题
- @allure.title支持通过占位符的方式传递参数，可以实现测试用例标题参数化，动态生成测试用例标题
- @allure.dynamic.title动态更新测试用例标题

#### 11.4.5.4.2 allure.title使用方式示例

##### 11.4.5.4.2.1 直接使用@allure.title为测试用例自定义标题

```python
# content of test_allure_title.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure


@allure.title("自定义测试用例标题")
def test_case_with_title():
    assert True
```

这个最常用，也是最简单的方式。效果图如下：

<img class="shadow" src="/img/in-post/allure/step_title.png" width="800">

##### 11.4.5.4.2.2 allure.title占位符传递参数，参数化测试用例标题

```python
# content of test_allure_param_title.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure


@allure.title("参数化测试用例标题：参数1 = {param1} and 参数2 = {param2}")
@pytest.mark.parametrize("param1, param2, expected", [(1, 1, 2), (1, 3, 5)])
def test_with_parametrize_title(param1, param2, expected):
    assert param1 + param2 == expected
```

展示效果如下：

<img class="shadow" src="/img/in-post/allure/step_title_parameter.png" width="800">


##### 11.4.5.4.2.3 allure.dynamic.title动态更新标题

```python
# content of test_allure_dynamic_title.py
import allure

@allure.title("这个标题将会被成功执行的测试用例中的标题替所代替")
def test_with_dynamic_title():
    assert True
    allure.dynamic.title("断言成功后，标题将会被替换成这个标题")
```

效果图如下：

<img class="shadow" src="/img/in-post/allure/step_dynamic_title.png" width="800">


#### 11.4.5.4.3 Allure集成缺陷管理系统和测试管理系统(allure.link、allure.issue、allure.testcase)

allure测试报告框架提供了@allure.link、@allure.issue、@allure.testcase 这三个装饰器，可以用来与缺陷管理系统和测试管理系统集成，做到更好的自动化管理。

这三个装饰器，使用方法基本一致，但仍然不建议混用，用例相关用@allure.testcase，Bug相关用@allure.issue，其他则使用@allure.link，形成习惯。

代码示例：

```python
# content of test_allure_link.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure

@allure.link("http://47.99.40.56:8721/List_of_Functional_Requirements-V1.2.html")
def test_with_link():
    """
    @allure.link() 指定与测试用例关联的链接，直接贴上对应的URL即可
    :return:
    """
    assert True


@allure.link("http://47.99.40.56:8721/List_of_Functional_Requirements-V1.2.html", name="需求列表V1.2的链接，点击访问")
def test_with_link_named():
    """
    @allure.link() 通过指定name的方式来指定关联链接，测试报告中用name替换实际URL展示
    :return:
    """
    assert True


@allure.issue("http://47.99.40.56:8721/bug-view-1446.html")
def test_with_issue_link():
    """
    @allure.issue() 可以与缺陷管理系统相关联，指定与该测试用例相关联的bug链接地址
    :return:
    """
    assert True


@allure.testcase("http://47.99.40.56:8721/test-case-2166.html")
def test_with_testcase_link():
    """
    @allure.testcase() 可以与测试用例管理工具相关联，指定与该测试用例关联的测试用例地址
    :return:
    """
    assert True
```

效果如下：

<img class="shadow" src="/img/in-post/allure/allure_link.png" width="800">

上图是allure.link的效果。

<img class="shadow" src="/img/in-post/allure/allure_issue.png" width="800">

上图是allure.issue的效果，用于提示是一个Bug。

<img class="shadow" src="/img/in-post/allure/allure_testcase.png" width="800">

上图显示allure.testcase的链接，会有一个类似存储的icon。

这几个装饰器的相同点都显示在“Links”下方展示，除了allure.link没有图标外，其他两个都有图标。



#### 11.4.5.4.4 Allure的Tag标记(allure.story、allure.feature、severity)

执行测试用例时，希望能够更加灵活的指定执行某些测试用例（如指定测试用例的级别，用例路径，用例标签/标记等），pytest支持我们通过使用marker装饰器@pytest.mark来实现这个需求，而allure也同样提供了三种类似的方法来实现这个需求。

##### 11.4.5.4.4.1 Allure的三种方式

Allure 则提供了 3 种类型的标记装饰器来标记测试，并且可以同步展示到测试报告内：

* BDD（行为驱动开发）风格的标签
* 严重程度（Severity）的标签
* 自定义的标签（allure.title）

##### 11.4.5.4.4.2 BDD风格的标签


* @allure.epic：敏捷里面的概念，定义史诗，相当于module级的标签
* @allure.feature：功能点的描述，可以理解成模块，相当于class级的标签
* @allure.story：故事，可以理解为场景，相当于method级的标签

allure提供的两个装饰器：@allure.feature和@allure.story，可以将用例根据Feature和Story分类，通过将name使用epic_ 开头的前缀就能够指定Feature和Story属于哪一个epic。

他俩的关系：

epic是feature父级，feature是story父级，是包含关系，效果跟书籍的目录或者项目结构相似。

如果使用allure和pytest来组织的自动化框架，**推荐使用Allure的标记来标记用例，替换@pytest.mark.xxx**，因为功能一致，且allure 标记功能可以直接**展示到html报告**内。

```python
# content of test_allure_tag.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure


def test_without_any_annotations_that_wont_be_executed():
    """
    没有任何注解
    :return:
    """
    pass


@allure.story('epic_1')
def test_with_epic_1():
    """
    通过指定name为epic_前缀的方式来指定story属于哪一个epic
    :return:
    """
    pass


@allure.story('story_1')
def test_with_story_1():
    """
    指定该测试用例属于的story
    :return:
    """
    pass


@allure.story('story_2')
def test_with_story_2():
    """
    指定该测试用例属于的story
    :return:
    """
    pass


@allure.feature('feature_2')
@allure.story('story_2')
def test_with_story_2_and_feature_2():
    """
    指定该测试用例属于的feature和story
    :return:
    """
    pass
```



11.4.5.4.4.3 拓展：命令行方式

与@pytest.mark.xxx相同，也可以通过命令行来运行指定epic、feature、story标记的用例：

```shell
–allure-epics
–allure-features
–allure-stories
```

**只运行 epic 名为 epic1 的测试用例**

``` pytest --alluredir ./report/allure --allure-epics=epic1 ```

**只运行 feature 名为 模块级 的测试用例**

``` pytest --alluredir ./report/allure --allure-features=模块级 ```

**只运行 story1、story2 的测试用例（也可以不用=号 空格即可）**

``` pytest tests.py --allure-stories story1,story2```

**指定 feature和story**

``` pytest tests.py --allure-features feature1,feature2 --allure-stories story1 ```



##### 11.4.5.4.4.3 Severity markers

使用@allure.severity来标识测试用例的严重等级，严重等级是allure.severity_level枚举中的一个。

allure划分用例等级为5个：

- blocker：阻塞缺陷（功能未实现，无法下一步）
- critical：严重缺陷（功能点缺失）
- normal：一般缺陷（边界情况，格式错误）
- minor：次要缺陷（界面错误与ui需求不符）
- trivial：轻微缺陷（必须项无提示，或者提示不规范）

**说明：**

一些手工用例编写平台，如testlink，它里面定义的测试用例的级别名称，和allure指定的这五种名称是不一样的，是无法直接使用外部的用例级别的，只能使用上面的测试用例的级别。


示例：

```python
# content of test_severity_markers_tag.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest
import allure


def test_with_no_severity_label():
    """
    不定义任何severity标签
    :return:
    """
    pass


@allure.severity(allure.severity_level.BLOCKER)
def test_with_blocker_severity():
    """
    定义severity标签为BLOCKER
    :return:
    """
    pass


@allure.severity(allure.severity_level.CRITICAL)
def test_with_critical_severity():
    """
    定义severity标签为CRITICAL
    :return:
    """
    pass


@allure.severity(allure.severity_level.TRIVIAL)
def test_with_trivial_severity():
    """
    定义severity标签为TRIVIAL
    :return:
    """
    pass


@allure.severity(allure.severity_level.NORMAL)
def test_with_normal_severity():
    """
    定义severity标签为NORMAL
    :return:
    """
    pass


@allure.severity(allure.severity_level.MINOR)
def test_with_minior_severity():
    """
    定义severity标签为MINOR
    :return:
    """
    pass

@allure.severity(allure.severity_level.NORMAL)
class TestClassWithNormalSeverity(object):
    """
    定义类的severity标签为NORMAL
    """

    def test_inside_the_normal_severity_test_class(self):
        pass

    @allure.severity(allure.severity_level.CRITICAL)
    def test_inside_the_normal_severity_test_class_with_overriding_critical_severity(self):
        pass
```

severity装饰器可以用在函数、方法和类上面。

通过使用--allure-severities 命令行选项指定运行哪些测试用例，如果命令行选项的值有多个就用逗号分隔。

比如：

<img class="shadow" src="/img/in-post/allure/allure_level.png" width="800">




## 11.4.6 综合示例

如下为一综合示例，参考如下：

```python
# content of test_allure_comprehensive_example.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import allure
import pytest
from allure_commons.types import LinkType, Severity


@allure.parent_suite('我是parent_suite')
@allure.suite('我是suite')
@allure.sub_suite('我是sub_suite')
@allure.epic('我是epic')
@allure.feature('我是feature')
@allure.story('我是story')
class TestAllureDemo:
    @allure.id('我是id')
    @allure.title('我是title')
    @allure.link('Google一下，你就知道', LinkType.ISSUE, '我是link_ISSUE')
    @allure.label('我是label')
    @allure.issue('Google一下，你就知道', '我是issue')
    @allure.description('我是description')
    @allure.severity(Severity.BLOCKER)
    @allure.tag('我是tag')
    @allure.testcase('Google一下，你就知道', 'testcase')
    def test_01(self):
        self.assert_one(1, 1)

    @allure.step('我是断言')
    def assert_one(self, a, b):
        assert a == b

    @allure.id('我是id')
    @allure.title('我是title')
    @allure.link('Google一下，你就知道', LinkType.LINK, '我是link')
    @allure.label('我是label')
    @allure.issue('Google一下，你就知道', '我是issue')
    @allure.description('我是description')
    @allure.severity('我是severity')
    @allure.tag('我是tag')
    @allure.testcase('Google一下，你就知道', '我是testcase')
    def test_02(self):
        allure.dynamic.mro()
        allure.dynamic.title('我是修改后的title')
        allure.dynamic.link('Google一下，你就知道', LinkType.LINK, '我是修改后的link')
        allure.dynamic.label('我是修改后的label')
        allure.dynamic.issue('Google一下，你就知道', '我是修改后的issue')
        allure.dynamic.description('我是修改后的description')
        allure.dynamic.severity('我是修改后的severity')
        allure.dynamic.tag('我是修改后的tag')
        allure.dynamic.testcase('Google一下，你就知道', '我是修改后的testcase')
        assert 1 > 1
```

allure html report 显示效果如下：

<img class="shadow" src="/img/in-post/allure/allure_full_example.png" width="800">




# 11.5 结语

## 11.5.1 设置测试套中显示内容


@allure.parent_suite,@allure.suite,@allure.sub_suite对应的是allure报告中的测试套的三个级别.爷爷父亲儿子.然后下一级就是测用例的标题。

由于@allure.epic, @allure.feature, @allure.story,@allure.title的存在，上面这三个装饰器很少使用。


## 11.5.2 设置报告中功能项显示内容


@allure.epic, @allure.feature, @allure.story,@allure.title对应功能中的一级菜单,二级菜单,三级菜单,用例标题


## 11.5.3 设置具体用例显示内容

@allure.id 用例id,@allure.link 用例的超链接,@allure.label 用例的标签
@allure.issue 记录用例的问题(超链接),@allure.description 用例的描述
@allure.severity 用例的优先级,@allure.tag 用例的标记,@allure.testcase 记录用例的地址(超链接)
@allure.description_html 用例的描述的网址(超链接),若存在description_html则@allure.description不显示

## 11.5.4 设置用例级别

@allure.severity的参数说明，'blocker'、 'critical'、'normal'、'minor'、'trivial'，从左到右言级别依次降低

# 11.6 注意事项

- Allure命令行工具需要单独安装。
- 生成的是中间结果文件，需要使用Allure CLI将这些结果转换成HTML报告。
- 兼容性：确保 `allure-pytest` 插件版本与你的pytest版本兼容。
- 报告存储：大量测试可能产生大量数据，需要考虑报告的存储问题。
- 安全问题：报告文件可能包含敏感数据，注意保护隐私和安全。



# 11.7 本章小结

本章节我们介绍了`Allure`测试报告框架的特点和优势，了解了Allure测试报告框架的一些高级功能，如历史记录和趋势分析。这些功能帮助团队了解测试的进展和质量，并进行测试结果的比较和分析，学习了如何使用`pytest`与`Allure`测试报告框架结合生成详细而美观的测试报告。

`Allure`提供了强大的测试报告功能，包括可视化的测试结果、丰富的图表和图形展示，以及对多种语言和平台的支持。我们学习了如何在`pytest`中集成`Allure`，并生成`Allure`测试报告。我们使用`pytest-allure`插件来生成`Allure`的Json格式测试结果，并通过allure-commandline工具生成HTML格式的报告。

我们了解了如何使用`Allure`注解来丰富测试报告的内容。通过添加@allure.feature、@allure.story和@allure.step等注解，我们可以更好地组织和展示测试用例的相关信息，使报告更加清晰和易读。还学习了如何添加附件信息到测试报告中，通过添加截图、日志文件等附件，我们可以提供更详细的测试结果和调试信息，帮助团队更好地分析和解决问题。

通过将`pytest`与Allure`结合使用，我们可以轻松生成详细而美观的测试报告，提供更好的测试结果展示和分析。这有助于团队更好地评估测试的状态和质量，及时发现和解决问题。
