---
layout:     post
title:      "API获取Jenkins构建信息"
subtitle:   "Call API to get Jenkins build information"
date:       2020-05-08
author:     "Gavin Wang"
catalog:    true
categories:
    - [Jenkins]
    - [Automation]
tags:
    - Jenkins
    - Automation
---


# 概述

Jenkins 的 REST API 可以从外部调用 Jenkins 实例，一些库例如 jenkins-rest 和 java-client-api 封装了相关 API，可以在 Java 中操作 Jenkins。


# 详述

本文参考jenkins-rest库，将API根据获取的资源类型不同分为6个类别。

|  **API类型**  |  **说明**  |
| ----------- | ----------------- |
|JobsAP	| 任务管理（任务信息、创建、修改）|
|OBPluginManagerAPI | 插件管理（插件信息、安装插件）|
|QueueAPI | 任务队列相关（队列状态）|
|StatisticsAPI | Jenkins统计信息 |
|CrumbIssuerAPI | 系统哈希值信息（用于防御CSRF攻击）|
|SystemAPI | Jenkins系统状态（版本、路径）|

## 术语定义

| **名词**  |  **说明**  |
| ----------- | ----------------- |
|job | 任务|
|payload | 在POST请求中提交的数据|
|{optionalFolderPath} |  可选参数：任务所在目录的路径|
|{project_name} | 必须参数：任务名称|

注意:

* 在 GET/POST 时需要附加 HTTP 认证才能访问 API
* 本文使用的数据结构可以在 jenkins-rest/domain 中查看详细定义

## Jobs 相关 API

### job-info 获取任务信息

```GET http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/api/json ```

返回类型：JobInfo

|字段 | 类型 | 说明|
| ----------- | ----------------- | -------------|
|description | String | 描述|
|name | String | 项目名称 | |
|url | boolean | 路径 |
|buildable | String | 是否可构建|
|builds | List<BuildInfo> | 构建记录|
|lastBuild |BuildInfo | 上次构建记录|
|...... |  |  |

### build-info 获取构筑信息

```GET http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/{number}/api/json ```

返回类型：BuildInfo

|字段 | 类型 | 说明 |
| ----------- | ----------------- | -------------|
|artifacts | List | artifacts |
|actions | Lis | actions |
|building | boolean	路径 ||
|description | String | 描述 |
|...... | | |

### create 使用 XML 文件创建任务

从 XML 文件中加载任务配置并创建任务

```POST http://127.0.0.1:8080/createItem ```

#### 参数

|key | value |
| ---------- | ------------------|
|name|任务名称 |
|payload|XML配置文件 |

返回类型：RequestStatus

|字段 | 类型 | 说明 |
| ------- | -------------------- |
| value | Boolean |
| errors | List |

### get-config 获取任务配置文件

```GET http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/config.xml ```

返回类型： String

### update-config 更新任务配置文件

```POST http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/config.xml ```


#### 参数

| 字段 | 说明 |
| ----------- | --------------------------- |
| payload | XML配置文件|

返回类型：Boolean

### get-description 获取任务描述

```GET http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/description ```


返回类型：String

### set-description 设置任务描述

```POST http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/description ```

#### 参数

| key | value |
| --------- | --------------------------- |
| description | 描述|

返回类型：Boolean


### delete 删除任务

```POST http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/doDelete ```

返回类型：RequestStatus


### enable允许任务

```POST http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/enable ```

返回类型：Boolean


### disable 禁止任务

```POST http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/disable ```

返回类型：Boolean


### build 构建

```POST http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/build ```

返回类型： IntegerResponse

|字段 | 类型 | 说明 |
| ---------- | ------------------- | -----------------------|
| value | Integer  ||
| errors | List | |

### build-with-params  使用参数创建任务

```POST http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/buildWithParameters ```

#### 参数

| key | value |
| --------- | ------------------------------ |
|payload | Map<String, List<String>> properties|

返回类型： IntegerResponse


### last-build-number 获取上次构建序号

```GET http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/lastBuild/buildNumber ```

返回类型：Integer

### last-build-timestamp 获取上次构建时间戳

```GET http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/lastBuild/buildTimestamp ```

返回类型：String

### progressive-text 获取构建控制台输出

```GET http://127.0.0.1:8080/{optionalFolderPath}job/{project_name}/lastBuild/logText/progressiveText ```

返回类型：ProgressiveText

|字段 | 类型 | 说明 |
| -------- | ------------------ | ------------------------ |
| text | String | 控制台输出|
| size | Integer | 字数 |
| hasMoreData | Boolean | 是否有更多数据 |

### CrumbIssuer 系统哈希值信息（用于防御CSRF攻击）

* CrumbIssuerApi
* path: /crumbIssuer/api/xml

#### crumb

```GET http://127.0.0.1:8080/crumbIssuer/api/xml?{key}={value} ```


##### 参数

| key | value |
| ---------| ----------------------- |
| xpath | concat(//crumbRequestField,":",//crumb) |

返回类型：Crumb

| 字段 | 类型 |
| ---------| ----------------------- |
| value | String |
| errors | List |

### PluginManager 插件管理（插件信息、安装插件）

* PluginManagerApi
* path: /pluginManager

#### plugins 插件列表

```GET http://127.0.0.1:8080/pluginManager/api/json ```

返回类型：List<Plugin>

| 字段 | 类型 | 说明 |
| ------------ | ------------------- | ------------------------ |
| active | Boolean | |
| backupVersion	String | |
| bundled | Boolean | |
| deleted | Boolean | |
| downgradable | Boolean | |
| enabled | Boolean | |
| longName | String | |
| ...... | | |

### installNecessaryPlugins 安装插件

```POST http://127.0.0.1:8080/pluginManager/installNecessaryPlugins ```

#### 参数

```payload: <jenkins><install plugin="{pluginID}"/></jenkins> ```

| 字段 | 说明 |
| ------------ | --------------------- |
| {pluginID} | 要安装的插件ID |

返回类型：RequestStatus

### Queue 任务队列相关（队列状态）

* QueueApi
* path: /queue

#### queue 所有任务队列信息

```GET http://127.0.0.1:8080/queue/api/json ```

返回类型：List<QueueItem>

| 字段 | 类型 | 说明 |
| ------------ | ------------------- | ------------------------ |
| blocked | Boolean | 是否阻塞 |
| buildable | Boolean | 是否可构建 |
| id | Integer	| |
| inQueueSince | Long | |
| params | Map<String, String> | 任务参数 |
| task | Task | Task中包含任务名称和URL|
| ...... | |  |

### item 任务队列信息

```GET http://127.0.0.1:8080/queue/item/{queueId}/api/json ```

#### 参数

| 字段 | 说明 |
| ------------ | ------------------------- |
| {queueId} | 任务队列ID |

返回类型：QueueItem

### cancel 取消任务队列 | 

```POST http://127.0.0.1:8080/cancelItem?id={id} ```

#### 参数

| 字段 | 说明 |
| -------- | ------------------------- |
| {id} | 任务队列ID|

返回类型：RequestStatus

### Statistics 统计信息

* StatisticsApi
* path: /

#### overall-load

```GET http://127.0.0.1:8080/overallLoad/api/json ```

返回类型：OverallLoad

| 字段 | 类型 | 说明 |
| -------- | -------------- | -------------------- |
| availableExecutors | Map<String, String> | |
| busyExecutors | Map<String, String>  |  |
| connectingExecutors | Map<String, String> |  |
| definedExecutors | Map<String, String> | |
| idleExecutors | Map<String, String> |  |
| onlineExecutors | Map<String, String> |  |
| queueLength | Map<String, String> | |
| totalExecutors | Map<String, String> | |
| totalQueueLength | Map<String, String> | |

#### System 系统信息

* path: /

返回类型：SystemInfo

| 字段 |  类型 | 说明 |
| ------------- | --------------------- | --------------------- |
| hudsonVersion | String | |
| jenkinsVersion | String | |
| jenkinsSession | String | |
| instanceIdentity | String | |
| sshEndpoint | String | |
| server | String | |


# 举几个例子

## 获取jenkins job状态

```oot@node248:~# curl http://172.12.12.234:8080/job/pytest_7.0/lastBuild/api/xml --user jenkins:1```

结果示例如下:

```shell
<freeStyleBuild _class='hudson.model.FreeStyleBuild'><action _class='hudson.model.CauseAction'><cause _class='hudson.model.Cause$UserIdCause'><shortDescription>Started by user jenkins</shortDescription><userId>jenkins</userId><userName>jenkins</userName></cause></action><action></action><action _class='hudson.plugins.git.util.BuildData'><buildsByBranchName><refsremotesoriginmaster _class='hudson.plugins.git.util.Build'><buildNumber>68</buildNumber><marked><SHA1>6388b644c4405a31611f179dca6c1e485ad92aa5</SHA1><branch><SHA1>6388b644c4405a31611f179dca6c1e485ad92aa5</SHA1><name>refs/remotes/origin/master</name></branch></marked><revision><SHA1>6388b644c4405a31611f179dca6c1e485ad92aa5</SHA1><branch><SHA1>6388b644c4405a31611f179dca6c1e485ad92aa5</SHA1><name>refs/remotes/origin/master</name></branch></revision></refsremotesoriginmaster></buildsByBranchName><lastBuiltRevision><SHA1>6388b644c4405a31611f179dca6c1e485ad92aa5</SHA1><branch><SHA1>6388b644c4405a31611f179dca6c1e485ad92aa5</SHA1><name>refs/remotes/origin/master</name></branch></lastBuiltRevision><remoteUrl>git@10.1.12.10:yunzeng_wang/pytest_framework.git</remoteUrl><scmName></scmName></action><action _class='hudson.plugins.git.GitTagAction'></action><action></action><action></action><action></action><action></action><action></action><action></action><action _class='hudson.plugins.violations.ViolationsBuildAction'></action><action></action><action></action><action></action><artifact><displayPath>allure-report.zip</displayPath><fileName>allure-report.zip</fileName><relativePath>allure-report.zip</relativePath></artifact><building>false</building><displayName>#68</displayName><duration>87155647</duration><estimatedDuration>85209450</estimatedDuration><fullDisplayName>pytest_7.0 #68</fullDisplayName><id>68</id><keepLog>false</keepLog><number>68</number><queueId>343</queueId><result>UNSTABLE</result><timestamp>1588762417068</timestamp><url>http://172.12.12.234:8080/job/pytest_7.0/68/</url><builtOn></builtOn><changeSet _class='hudson.plugins.git.GitChangeSetList'><kind>git</kind></changeSet><culprit><absoluteUrl>http://172.12.12.234:8080/user/shengdan061</absoluteUrl><fullName>shengdan061</fullName></culprit><culprit><absoluteUrl>http://172.12.12.234:8080/user/yunzeng_wang</absoluteUrl><fullName>yunzeng_wang</fullName></culprit></freeStyleBuild>root@node248:~#
root@node248:~#
```

## 获取某一个构建版本号为56的构建结果

```curl http://172.12.12.234:8080/job/pytest_7.0/56/api/xml --user jenkins:1 ```


## 获取最后一次构建的版本号：

```curl http://172.12.12.234:8080/job/pytest_7.0/lastBuild/buildNumber --user jenkins:1 ```


## 获取某个项目所有构建版本号的结果

```curl http://172.12.12.234:8080/job/pytest_7.0/api/xml --user jenkins:1 ```

说明：

* 以上pytest_7.0为项目名称，jenkins:1是访问jenkins server的账号和密码

