---
title: 《pytest测试指南》-- 第二章 2-5 与Jenkins结合完成CI构建 
date: 2024-06-06 23:00:00
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
summary: 《pytest测试指南》一书 第二章 2-5 与Jenkins结合完成CI构建 
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 5.1 CI/CD介绍

CI/CD（Continuous Integration and Continuous Delivery/Deployment）是现代软件开发流程中的关键环节。它的目标是通过自动化整合软件开发过程和持续交付，提高开发效率、质量和可靠性，同时缩短产品推向市场的时间。而CI/CD工具是实现这一目标的关键工具。

**CI/CD工具通常包括以下几个部分：**

* 持续集成（Continuous Integration，CI）工具：自动化自动构建和测试代码的工具，如Jenkins、Travis CI和CircleCI等。
* 持续交付（Continuous Delivery，CD）工具：自动化打包、发布和部署软件的工具，如Octopus Deploy和UrbanCode Deploy等。
* 持续部署（Continuous Deployment，CD）工具：自动化将软件部署到生产环境的工具，如AWS CodeDeploy和Azure DevOps等。

其中，Jenkins是CI/CD工具中最为流行的一个，开源、免费且可扩展性强，可用于构建、测试、分析和部署软件，支持多种插件和工具。

**使用CI/CD工具的好处包括：**

* 提高开发效率：减少手动操作，自动化整个软件开发过程，从而加快软件的开发、测试和发布速度。
* 提高软件质量：自动化测试和持续集成可以发现问题和错误，增加软件的稳定性和可靠性。
* 减少错误和风险：自动化构建、测试和发布过程可以减少人工操作失误导致的错误和风险，提高了软件的可靠性。
* 便于管理和协作：使用CI/CD工具可以更好地管理代码、版本和部署，也可以更方便地协作开发。
* 缩短产品上线时间：自动化构建和部署可以缩短产品推向市场的时间，从而提前占领市场份额。

**AKS-Release-Pipelines流程图示例：**

<img class="shadow" src="/img/in-post/jenkins/AKS-Release-Pipelines.webp" width="800">

Azure Kubernetes Service (AKS) 是一个托管的Kubernetes服务，它简化了在云中运行容器化应用程序的过程。AKS通过Azure DevOps或其他CI/CD工具，用户可以实现自动化的发布管道 (Release Pipelines) 来构建、测试和部署容器化应用程序到AKS集群。

AKS Release Pipelines的步骤包括：

* **源代码管理**: 使用Git仓库管理应用源代码，确保版本控制的准确性。
* **持续集成 (CI)**: 当源代码发生变更时，自动触发构建过程，进行代码编译，运行单元测试和静态代码分析等自动化步骤。
* **容器构建和推送**: CI过程包含构建Docker容器镜像，并将其推送到容器镜像仓库（如Azure Container Registry）。
* **环境特定配置**: 不同环境（如开发、测试、生产）可能需要不同的配置，通过参数化配置文件实现不同环境特定的部署。
* **持续部署 (CD)**: 使用Release Pipelines，在经过适当的测试和验证后自动部署到AKS集群。这通常包括部署Kubernetes yaml文件，启动Pods，服务等。
* **部署策略**: 实施部署策略，例如蓝绿部署、滚动更新或金丝雀测试等，以确保平滑的版本过渡和最小化对生产环境的潜在影响。
* **监控和日志**: 一旦应用被部署，使用Azure Monitor和日志服务来持续监控应用程序的性能和状态。
* **后续操作**: 包括回滚策略的执行（如果新发布的版本不稳定）和自动化的清理步骤。
* **安全与合规性**: 在整个流程中，确保遵循安全最佳实践，如使用安全的容器镜像、管理密钥和凭据等。

使用Azure DevOps构建AKS Release Pipelines的特点：

- **集成**: Azure DevOps提供与AKS的紧密集成，简化CI/CD流程的配置与管理。
- **灵活性**: 可以自定义管道以支持复杂的工作流，匹配开发团队的具体需求。
- **易用性**: 提供用户界面和YAML文件两种方式配置管道，易于管理和版本化。
- **可视化**: Azure DevOps提供管道执行过程的视觉化反馈，便于监测和调试。
- **扩展性**: 支持市场上的其他工具和服务，通过插件实时扩展功能。

总的来说，CI/CD工具是现代软件开发流程不可或缺的一部分，选择合适的工具和流程，对于提高开发效率、质量和可靠性有着非常重要的作用。

# 5.2 CI/CD系列工具介绍

下面对CI/CD工具TeamCity、Jenkins、Bamboo、CircleCI、Travis CI以及Codeship做一些简单的介绍与对比。

## 5.2.1 TeamCity

TeamCity 是由 JetBrains 开发的一款专业的 CI/CD 工具。 TeamCity 适用于.NET 和Java 开发团队，也支持其他语言的开发者。与其他CI/CD 工具相比，TeamCity 拥有更好的用户界面和更丰富的插件，支持开发团队一起协作完成持续交付流程。

优点：

* 易于安装和部署，具有良好的UI界面和灵活的插件机制；
* 可以集成多种开发语言和应用程序，支持多种构建工具和测试框架；
* 支持分布式构建，具有可扩展性和高可用性。

缺点：

* 价位较高，对于小型企业或个人项目来说可能会比较昂贵；
* 配置可能较为繁琐。

## 5.2.2 Jenkins

Jenkins 是一款开源的 CI/CD 工具。它具有自动化构建、测试和部署软件的能力，支持多种工具和语言，还有大量的插件可供集成。

优点：

* 基于开源，免费使用；
* 具有强大的灵活性和可扩展性，支持多种语言和技术栈；
* 拥有一个庞大的用户社区，用户之间可以分享自定义插件和解决方案。

缺点：

* 需要大量的配置、扩展和管理工作；
* 有时会出现稳定性、可靠性或安全性问题。

## 5.2.3 Bamboo

Bamboo 是 Atlassian 公司为企业级开发者提供的 CI/CD 工具。它提供了自动构建、测试和发布软件的能力，支持多种编程语言和框架。 Bamboo 是 JIRA、BitBucket、Confluence 等 Atlassian 产品的组成部分，因此可以非常方便地集成这些产品。

优点：

* 集成 Atlassian 系列产品，方便开发人员使用；
* 支持多种语言及测试、构建框架；
* 可以支持分布式构建，可以进行可视化的构建计划。

缺点：

* 收费较高，对于小型企业和个人开发者可能有些昂贵；
* Bamboo 对第三方插件的支持相对较少。

## 5.2.4 CircleCI

CircleCI 是免费的 CI/CD 工具，支持多种编程语言和框架。它可以运行在公共云服务中，也可以在私有环境中使用，支持分布式构建和部署。

优点：

* 支持多种编程语言和框架；
* 提供了免费版本，适合小型团队和个人开发者使用；
* 很容易使用和自定义。

缺点：

* 免费版本提供的功能较少，可能无法满足大型企业和复杂系统所需；
* 对自定义环境和其他技术的支持较少。

## 5.2.5 Travis CI

Travis CI 是一款免费的 CI/CD 工具。它是完全托管的，可以使用代码仓库进行部署。它支持多种语言和框架，并提供了集成测试、持续交付和部署等功能。

优点：

* 免费使用；
* 支持多种编程语言和框架；
* 强大的GitHub 集成。

缺点：

* 私有仓库版本较为昂贵，对于小型团队来说可能不那么适合；
* 在本地运行 Travis CI 的配置可能会比较复杂。

## 5.2.6 Codeship

Codeship 是一款基于云的 CI/CD 工具，支持多种编程语言。它可以在 Google Kubernetes Engine（GKE）集群上部署，还可以部署到 AWS、Heroku、Google Cloud Platform、OpenShift、Bitbucket Pipelines、GitHub、GitLab 等云端仓库。

优点：

* 可以在网络中去搭建；
* 支持多种编程语言；
* 部署到多个云端存储库和 GKE 上非常方便。

缺点：

* 付费计划相对较昂贵，并且各个计划的特性可能相对较少；
* 各种用户界面可能有些繁琐。

## 5.2.7 CI/CD工具大比拼

| Tools     | Language Support | Build Time | Ease-of-Use | Customizability | Features | Price      |
| --------- | ---------------- | ---------- | ----------- | --------------- | -------- | ---------- |
| TeamCity  | 多语言           | 快         | 中等        | 非常好          | 非常好   | 付费       |
| Jenkins   | 多语言           | 慢         | 中等        | 非常好          | 非常好   | 免费       |
| Bamboo    | 多语言           | 快         | 中等        | 非常好          | 良好     | 付费       |
| CircleCI  | 多语言           | 中等       | 非常好      | 较好            | 良好     | 免费和付费 |
| Travis CI | 多语言           | 快         | 非常好      | 良好            | 良好     | 免费和付费 |
| Codeship  | 多语言           | 快         | 较好        | 较好            | 良好     | 付费       |

根据上表中的对比，我们可以得出以下结论：

- 如果你想要一个价格便宜的 CI / CD 工具，可以选择 Jenkins、Travis CI 或 CircleCI。
- 如果你正在寻找功能强大、高度可定制和性能最好的 CI / CD 工具，则应选择 TeamCity 或 Bamboo。
- 如果你需要在多个云端仓库和集群之间部署应用程序，则 Codeship 可能是最佳选择之一。

综上所述，在选择 CI/CD 工具时，应根据公司、团队和项目的特定需求进行决策，其中有些工具比其他工具更适合于特定的应用程序和用例。



# 5.3 部署Jenkins

介绍了几种CI/CD工具，接下来基于工作中项目安排，在Ubuntu 22 上安装 Jenkins 2.375.3 。

## 5.3.1 安装Ubuntu 22.04

具体安装过程，本文忽略，安装好后，OS信息如下：

```shell
 Static hostname: jenkins
       Icon name: computer-vm
         Chassis: vm
      Machine ID: 5876152df2764a3a80c0788e54f81f62
         Boot ID: fb9b1e97473f40df811b0980474c029d
  Virtualization: vmware
Operating System: Ubuntu 22.04.1 LTS              
          Kernel: Linux 5.15.0-43-generic
    Architecture: x86-64
 Hardware Vendor: VMware, Inc.
  Hardware Model: VMware Virtual Platform
```



## 5.3.2 安装必要的软件包


如下，列出了必要的软件安装（没有完整的记录下来，可能不全）：

```shell
apt-get update
apt-get install git -y
apt-get install libpcsclite1 -y
apt-get install ca-certificates-java -y
apt-get install fonts-dejavu-extra -y --fix-missing
apt-get install libllvm13 -y
apt-get install fonts-dejavu-extra -y
apt-get install openjdk-11-jre-headless -y
apt-get install openjdk-11-jre -y
apt-get install libdrm-amdgpu1 libdrm-nouveau2 libdrm-radeon1 libglapi-mesa libsensors5 libvulkan1 -y
apt-get install libgl1 -y
apt-get install libglvnd0 -y
apt-get install plocate -y
apt-get install git-lfs -y
apt-get install expect -y
apt-get install spawn -y
apt-get install sshpass -y  
apt-get install allure-commandline -y
apt-get install python3-pip -y
apt install jenkins -y
```

为了支持Email对pylint 绘图功能，需要安装matlpotib, 相关安装包信息参考如下：


```shell
ca-certificates-java_20190909ubuntu1.1_all.deb
contourpy-1.0.7-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
cycler-0.11.0-py3-none-any.whl
default-jre-headless_1.11-72build2_amd64.deb
fonts-dejavu-extra_2.37-2build1_all.deb
fonttools-4.38.1.dev0-py3-none-any.whl
g++-11_11.3.0-1ubuntu1~22.04_amd64.deb
java-common_0.72build2_all.deb
libgl1-mesa-dri_22.0.5-0ubuntu0.3_amd64.deb
libllvm13_13.0.1-2ubuntu2_amd64.deb
libpython3.10-dev_3.10.6-1~22.04.2_amd64.deb
matplotlib-3.7.1.tar.gz
numpy-1.24.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
openjdk-11-jre-headless_11.0.17+8-1ubuntu2~22.04_amd64.deb
python3.10-minimal_3.10.6-1~22.04.2_amd64.deb
```

## 5.3.3 配置Jenkins


Jenkins 安装好后，访问8080端口，根据提示信息，按提示一步一步往下走，此处不做额外赘述。

### 5.3.3.1 Jenkins Plugin 的安装

**需要安装如下插件与工具：**

```shell
allure
Cobertura Coverage
Violations Plugin # Pylint
AnsiColor         # 颜色
Next Build Number Plugin
```

一些基础的plugin，像git, pipline 之类的安装，此处不做赘述。

**install allure commandline：**

安装包手动下载下来：``` https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.21.0/allure-commandline-2.21.0.tgz ```

在Jenkins上使用root 用户，安装到/usr/lib/下，参考如下：

``` /usr/lib/allure-2.21.0/lib/allure-commandline-2.21.0.jar ```


### 5.3.3.2 修改 expect spawn ssh时prompt无法通过问题

修改vim /etc/ssh/ssh_config

``` StrictHostKeyChecking ask   -->改为 StrictHostKeyChecking no ```

并重启ssh服务，以此来避免expect 中执行spawn交互失败。

### 5.3.3.3 Jenkins 邮箱配置

Jenkins 当前登录UI用户的邮箱，需要和全局配置里设置的邮箱用户名保持一致，否则会报错，参考如下：

<img class="shadow" src="/img/in-post/jenkins/jenkins_email_config.png" width="800">

Jenkins 匿名用户权限配置，为了让Email端能够正常展示出allure trend，pylint error，以及CODE COVERAGE信息，需要对匿名用户开放一定的权限：

<img class="shadow" src="/img/in-post/jenkins/Jenkins_permission.png" width="800">



# 5.4 Groovy介绍

Groovy 是一种强大的编程语言，它与 Java 完全兼容，但提供了更多的动态特性。在 Jenkins 中，Groovy 被广泛用于多种场景，从简单的脚本到复杂的 Jenkins 管道（Pipelines）和作业配置。以下是一些 Groovy 在 Jenkins 中应用的简单介绍和示例：

## 5.4.1 Jenkins Script Console

Jenkins 提供了一个称为 "Script Console" 的强大功能，管理员可以在此运行 Groovy 脚本。这对于执行系统管理任务、直接访问 Jenkins 对象模型、以及执行各种动态脚本非常有用。例如，ni可以列出所有作业，检索特定作业的详细信息，清理工作空间等。

## 5.4.2 管道脚本（Pipelines）

Jenkins 管道是一系列定义整个构建过程的步骤。Groovy 被用于定义 Pipeline 的语法。通过 Jenkinsfile，用户可以编写 Groovy 脚本来定义各个阶段和任务，实现复杂的持续集成和持续部署（CI/CD）流程。

## 5.4.3 动态作业生成

Groovy 脚本可用于动态生成 Jenkins 作业。通过编写 Groovy 脚本，可以根据需要动态创建、修改或删除作业。这对于管理大量相似的作业特别有用。

## 5.4.4 插件开发

Groovy 也用于开发 Jenkins 插件。由于其与 Java 的兼容性，以及简化的语法，它是编写 Jenkins 插件的流行选择。

## 5.4.5 管理和配置

Groovy 脚本可以用来修改、更新和检索 Jenkins 的配置。它提供了直接操作和访问 Jenkins 内部结构的能力，包括用户、作业配置、节点信息等。

## 5.4.6 示例脚本

**获取所有作业名称：**

在 Jenkins 的 Script Console 中运行以下 Groovy 脚本将返回所有作业的名称：

```ini
Jenkins.instance.items.each{ job -> 
  println(job.name)
}
```

输出结果示例如下：

```ini
pytest_8.0_pipeline
pytest_8.2_pipeline
pytest_8.3_pipeline
Result: [org.jenkinsci.plugins.workflow.job.WorkflowJob@748e0cf7[pytest_8.0_pipeline], org.jenkinsci.plugins.workflow.job.WorkflowJob@57759099[pytest_8.2_pipeline], org.jenkinsci.plugins.workflow.job.WorkflowJob@33684a91[pytest_8.3_pipeline]]
```

其中`pytest_8.0_pipeline`，`pytest_8.2_pipeline`，`pytest_8.3_pipeline`为当前Jenkins中的3个Project名称。

## 5.4.7 安全注意事项

- 运行 Groovy 脚本提供了非常强大的能力，但也带来了安全风险。确保只有信任的用户才能执行脚本。
- 在生产环境中使用 Groovy 脚本时，应该确保代码经过审查，并且理解其对系统的潜在影响。

## 5.4.8 小结

Groovy 在 Jenkins 中提供了极大的灵活性和强大的功能。无论是进行简单的任务，还是构建复杂的自动化流程，Groovy 都是一个极具价值的工具。然而，使用它需要对 Jenkins 的内部结构和 Groovy 语言都有一定的理解。通过实践和学习，你可以充分利用 Groovy 在 Jenkins 中的潜力，优化你的开发和部署流程。

# 5.5 pipline介绍

Jenkins pipeline 是一种由一系列插件组成的套件，用于支持实现和集成连续交付管道到 Jenkins 中。它为 Jenkins 提供了一个强大的工具，用户可以使用 pipeline 插件定义整个构建/部署的生命周期。pipeline 提高了 Jenkins 的使用灵活性，并为复杂的工作流提供了编码方式。

## 5.5.1 pipeline 的主要特点

**代码化的配置（pipeline as Code）**
Jenkins pipeline 允许你将构建过程的定义保存为代码，通常是在一个名为 `Jenkinsfile` 的文本文件中。这样的定义可以随着项目的源码一起存放在版本控制系统中。

**耐久性和暂停能力**
pipeline 能在Jenkins主服务器或者代理服务器上执行的过程中，即使遇到重新启动或网络问题等意外情况，也能保持其状态。这意味着构建流程可以暂停，等待用户输入或在其他特定条件下恢复。

**可扩展性**
pipeline 提供了一个固定的、可扩展的环境，用户可以通过共享代码库或自定义插件进一步增强。

**可视化和丰富的反馈**
pipeline 插件为每一次构建提供了丰富的可视化反馈，这使得查看和了解构建的进度和状态变得非常直观，包括更容易地找到构建失败的原因。

## 5.5.2 Jenkins Pipeline 核心概念

**Pipeline**: 一个由多个阶段（stages）组成的流程，用于描述如何构建、测试和部署应用。

**Stage**: Pipelines 中的一个阶段，通常用于描述一个完整步骤，如构建、测试或部署。

**Step**: 阶段中的一个操作，可以是执行脚本、复制文件或者其他指令。

**Jenkinsfile**: 存储在源代码控制仓库中的文本文件，包含了定义整个Pipeline的代码。

**Node**: 指定执行Pipeline或其阶段的主机。

**Agent**: 代表一个Jenkins环境，Pipeline或某些阶段会在其中执行。

## 5.5.3 Pipeline 的两种语法

**声明式（Declarative）**
以声明方式定义 pipeline，它有一个较为严格的、预定义的结构让用户填充，有助于编写简洁的 pipeline 代码。它提供了一个由 `pipeline { ... }` 包围的代码块，在其中定义所有的阶段（stages）和步骤（steps）。

**脚本式（Scripted）**
提供了更多的灵活性和控制力。Scripted pipeline 是基于 Groovy 的，使用了 Groovy 的流程控制语句。它从一个 `node { ... }` 代码块开始，在这个代码块中可以运行命令、脚本或者定义函数等。

## 5.5.4 Jenkinsfile 示例

一个简单的声明式 pipeline，参考如下：

```groovy
pipeline {
    agent any // 指定由任何可用的代理执行

    environment {
        // 设置环境变量
        MY_VARIABLE = "some-value"
    }

    stages {
        stage('Build') {
            steps {
                // 执行构建步骤
                echo 'Building..'
                script {
                    // 执行 Groovy 脚本
                }
            }
        }
        stage('Test') {
            steps {
                // 执行测试步骤
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                // 执行部署步骤
                echo 'Deploying..'
            }
        }
    }

    post {
        // 构建完成后的操作
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
    }
}
```

在此 `Jenkinsfile` 中，我们定义了一个有三个阶段的 pipeline：构建（Build）、测试（Test）和部署（Deploy），还设置了环境变量和构建后要执行的操作。

## 5.5.5 小结

pipeline 是 Jenkins 中实现自动化的一种非常强大的方式。通过 `Jenkinsfile`，团队可以编写重复使用、源码版本控制的构建声明，整个构建流程可以像代码一样被管理和审查。

pipeline 提供了一种统一的方式来定义构建、测试和发布软件所需的所有步骤，使得持续集成和持续部署流程更加便捷和可靠。



# 5.6 项目实践

自动化测试框架设计好了，用例数也逐渐增多了，接下来就要检测这些用例与产品对接测试效果如何。通过自动化测试用例的持续集成，能够做到如下效果：

* 快速反馈

CI环境可以在代码提交后立即运行自动化测试，这样可以尽早发现问题，并能迅速给予开发者反馈。快速发现bug和其他问题可以让团队更及时地解决它们，避免问题累积。

* 构建可靠性

通过在每次提交后执行自动化测试，可以确保代码的修改没有破坏现有的功能。这有助于提高构建的总体质量和可信任度。

* 提升开发效率

自动化测试可以减少手动测试的需要，从而节省大量时间和劳动力。这让测试人员可以专注于更复杂的测试场景和质量保障任务。

* 缩短发布周期

在CI环境中，由于自动化测试的高效性，测试可以频繁且持续地运行，这有助于缩短从代码开发到产品发布的周期。

* 风险控制

自动化测试提供了一个安全网，帮助避免因快速的开发节奏而可能造成的严重缺陷或回归问题，从而更有效地控制项目风险。

* 持续的质量保障

CI与自动化测试相结合，可以确保产品质量在整个开发周期中保持一致，即使是在项目后期或在频繁的变更之后也能保证质量。

* 跨团队协作

自动化测试在CI流程中可以作为跨团队协作的基础，测试结果为所有团队成员提供了一个共同的理解基础，比如开发者、测试者和产品经理。

* 文档替代

良好编写的测试用例可以作为系统行为的活文档。当新的开发者加入团队时，他们可以通过查看自动化测试来理解系统功能和业务逻辑。

* 更频繁的部署

在CI流程中整合自动化测试，可以帮助实现更频繁和有信心的代码部署，这是实现持续交付（Continuous Delivery）的重要一步。

针对被测产品，站在测试视角，整个自动化工程的CI过程如下图所示：

<img class="shadow" src="/img/in-post/jenkins/CI构建流程-精简版.png" width="800">



关于“部署测试环境并运行测试用例”，部署的是5套集群：


<img class="shadow" src="/img/in-post/jenkins/部署测试环境并运行测试用例.png" width="800">



说明如下：

* 第一步：IP地址检测

  判断Jenkins配置中给定的IP地址列表是否满足数量要求。

* 第二步：Git拉取最新code

  从Git Server上拉取对应分支最新的自动化测试框架代码到Jenkins Server上，确保每次CI使用的测试代码都是最新的。

* 第三步：批量部署ISO

  通过Cobbler批量部署ISO，支持物理机批量部署，支持ESXi上VM批量部署，也支持PVE上VM的批量部署，具体需要取决于研发团队硬件资源分配情况，如果资源充足，则使用物理设备；其他情况则考虑虚拟化设备。

* 第四步：rsync code

  通过rsync命令，将最新代码同步到各套存储节点的中间节点（人为设定的需求）。

* 第五步：部署测试环境并运行测试用例

  五套测试环境并行（总共16台机器，第一套集群环境由于涉及到节点添加到集群和移除处集群，需要4台设备），从创建各自的集群到运行各自指定的测试用例，五套环境合起来是一个完整的测试用例集合，这样做的目的在于节约用例的总体执行时间。

* 第六步：汇总测试结果

  汇总各个集群节点上用例执行结果对应的json文件到Jenkins Server，所有节点的数据合集是一套完整的测试用例执行结果。

* 第七步：：Publish Coverage Report& Code Quality Check

  l利用pytest-cov插件产生Coverage Report，利用pylint插件产生Code Quality Check信息，记录为xml文件，并被Jenkins解析与图形化展示使用。

* 第八步：Send Email

  发送CI构建结果到相关人员，从而及时获悉此次的CI构建结果，知悉被测版本与用例执行成功信息。

## 5.6.1 Jenkins pipline style Project 配置

如下，以南京 Lab 实际配置截图：

<img class="shadow" src="/img/in-post/jenkins/jenkins_job_config.png" width="800">

总共设置了String类型的参数，参考示例如下：

```shell
GIT_WEB  --> http://10.22.21.9/pytest_framework
GIT_URL  --> git@10.22.21.9:pytest_framework.git
GIT_BRANCH --> 8.3
REPORT_DIR --> /root/${JOB_NAME}/report                           # Jenkins install path
WORK_SPACE --> ${JENKINS_INSTALL_PATH}/workspace/pytest_8.3_pipeline # Jenkins work space
JOB_SPACE --> ${JENKINS_INSTALL_PATH}/jobs/pytest_8.3_pipeline       # pytest job space
BAT_INSTALL -->  /root/batch_install/batch_install.py /root/batch_install/config/pytest/pytest_8.3_pipeline_195_cone # Bat install OS by Cobbler
IPS --> 172.11.75.11,172.11.75.12,172.11.75.13,172.11.75.14,172.11.75.15,172.11.75.16,172.11.75.17,172.11.75.18              # Cluster hosts IP,split by,
CODE_DIR --> /root/${JOB_NAME}/src                # pytest code dir which will be runned
```

**关于批量安装**

`batch_install.py`脚本，请参考本书的“Cobbler部署与使用”想章节内容。

**关于pipline Script**

这部分内容，请参考“pytest+requests+allure自动化测试框架设计”章节中的`v1.1_allure-pipeline-report.groovy`文件内容。

**关于邮件新增图例**

如果想生成3个维度的数据，示例代码参考如下：


```python
import base64
import io
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def generate_chart(x, excellent, satisfactory, failing):
    fig = plt.figure(figsize=(15, 7.5))
    ax = fig.add_subplot(111)
    ax.stackplot(
        x,
        excellent, satisfactory, failing,
        colors=("#c0e2c1", "#fff8ba", "#f4b8b8"),
        labels=('Excellent', 'Satisfactory', 'Failing'),
    )
    ax.legend()
    # ax.set_title("History")    ax.set_xlabel("Builds")
    ax.set_ylabel("Amounts")
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    output = io.BytesIO()
    plt.savefig(output, bbox_inches='tight')
    output.seek(0)
    encoded = base64.b64encode(output.read())
    return f"data:image/jpg;base64,{encoded.decode('utf8')}"


if __name__ == "__main__":
    x = [79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102]
    excellent = [0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3]
    satisfactory = [0,0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2]
    failing = [0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,93]
    res = generate_chart(x, excellent, satisfactory, failing)
    print(res)
```

请根据实际情况进行修改与调整，以期匹配自己的需求。

## 5.6.2 Email 模板

为了让CI结果更好的展示，基于官方模板(```https://github.com/jenkinsci/email-ext-plugin/blob/master/src/main/resources/hudson/plugins/emailext/templates/groovy-html.template ```)，增加了三张图，分别是：

* Allure history trend
* pylint warnings trend
* code coverage

<img class="shadow" src="/img/in-post/jenkins/邮件新增的3种图.png" width="800">

此自定义的EMail模板，存放在Jenkins 安装路径下：


```shell
jenkins@jenkins:/var/lib/jenkins$ cd email-templates/
jenkins@jenkins:/var/lib/jenkins/email-templates$ ls -l
total 120
-rw-rw-r-- 1 jenkins jenkins  6292 Feb 17 15:49 allure-report.groovy
-rw-r--r-- 1 jenkins jenkins  7759 Mar  7 22:24 v1.1_allure-pipeline-report.groovy
jenkins@jenkins:/var/lib/jenkins/email-templates$ 
```

其中，**v1.1_allure-pipeline-report.groovy** 为当前使用模板，里面有定义一个需要被替换的内容：

```shell
  <table>
    <tr>
        <img src="EMAIL_BASE64_IMG_REPLACE" width="500px" height="200px"/>
    </tr>
  </table>
```

此处内容，需要借助 **edit_email_template.py**  这个代码来生成base64 image并替换，最终被pipline 处的EMail 使用。

需要借助 **edit_email_template.py**  的原因在于，新版本的Jenkins，对于pylint结果产生的图形，是基于canvas，并不是一个静态图片，无法通过HTML中的img src来直接指定。

## 5.6.3 效果展示

### 5.6.3.1 Jenkins 工程效果图

Stage View：


<img class="shadow" src="/img/in-post/jenkins/CI project Stage View.png" width="800">

### 5.6.3.2 Allure报告在Jenkins中的展示

<img class="shadow" src="/img/in-post/jenkins/CI Allure Report展示.png" width="800">

### 5.6.3.3 Code Coverage测试代码覆盖率

code coverage原始文件由`run.py`产生：

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

借助Jenkins pipeline script代码完成数据的展示：

```shell
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
```

最终展示效果如下：

<img class="shadow" src="/img/in-post/jenkins/CI Code Coverage展示片段.png" width="800">

### 5.6.3.4 pylint告警趋势图

pylint原始数据由`run.py`入口脚本生成：

```python
    # Generate pylint output
    print("    8-2 Start to Generate pylint output\n")

    try:
        do_cmd("pylint --rcfile={}/.pylintrc -f parseable -d I0011,R0801 "
               "{}/ | tee {}/../report/pylint.out".format(source_path, source_path, source_path))
    except Exception as ex:
        print("      Generate pylint failed, backend return : ({})\n".format(str(ex)))
```

然后借助pipeline script中如下代码将讲过传递给Jenkins中pylint插件：

```shell


        /* Generate pylint Report */
        stage('Code Quality Check') {
            steps {
                script{
                    echo "Run pylint code style check"
                }
        	}

        	post { 
                always {
                   sh 'cat report/pylint.out'
                   recordIssues healthy: 1, tools: [pyLint(name: 'PyLint', pattern: 'report/pylint.out')], unhealthy: 2
                }
            }
        }
```

展示效果如下（没有告警）：

<img class="shadow" src="/img/in-post/jenkins/CI pylint Trend.png" width="800">

### 5.6.3.5 发送邮件效果图

最终EMail 邮寄出来的内容如下（关键信息做了脱敏，请见谅）：

全部成功状态下：

<img class="shadow" src="/img/in-post/jenkins/jenkins_build_success.png" width="800">

部分用例失败状态下：

<img class="shadow" src="/img/in-post/jenkins/jenkins_build_unstable.png" width="800">



# 5.7 本章小结

本章节中，我们详细介绍了CI/CD工具大比拼，Jenkins的部署方法以及Groovy和pipeline的介绍。我们还介绍了分布式存储软件接口自动化测试框架与Jenkins的结合实例。

首先，我们进行了CI/CD工具的比较和评估，了解了不同工具的特点和适用场景。我们强调了Jenkins作为一个流行的CI/CD工具，具有灵活性和可扩展性，并提供了丰富的插件生态系统。

接着，我们详细介绍了Jenkins的部署方法。我们了解了如何安装和配置Jenkins服务器，还学习了如何创建和管理Jenkins的作业和构建过程。

最后，我们介绍了分布式存储软件接口自动化测试框架与Jenkins的结合实例。我们了解了如何利用Jenkins的构建流程和插件来自动化执行接口测试，并与分布式存储软件的测试框架集成。这种结合可以实现每天自动、批量部署最新产品ISO，并进行接口自动化测试，发送定制化测试报告到相关人员。


