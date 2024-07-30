---
layout:     post
title:      "Jenkins部署pipeline并发执行pytest自动化用例"
subtitle:   "Jenkins pipeline parallel job for pytest automation"
date:       2020-05-13
author:     "Gavin Wang"
catalog:    true
categories:
    - [Automation]
    - [Jenkins]
tags:
    - Jenkins
    - pipeline
    - pytest
    - Automation
---


# 概述

目前现有自动化用例数比较多了，在free style jenkins project中顺次执行，耗时1天左右，很明显，耗时太久，急需用例能够并发执行，从而实现节约时间。

本文介绍如何通过pipeline project，实现现有用例执行流程的改造，实现并发执行。

# 改造涉及内容

针对当前automation project，需要做如下内容调整：

* (1) run.py中，提取出reboot client，生成pylint数据操作

* (2) Jenkins节点中email-templates发送email内容groovy脚本调整

* (3) 测试代码config目录下autotest.conf，含有多个，命名格式为autotest_ip.conf

* (4) 测试代码jenkins目录下生成build properties文件，以及rsync脚本要做修改，主要是路径问题

说明：

第(1)点： 以前用例是顺次执行的，只需要执行一次，一旦调整成并发后，存在每个执行node均会执行一次的情况；

第(3)点： 每个执行用例的集群节点，需要mv autotest_ip.conf为autotest.conf 

第(4)点:  free style与pipeline的jenkins project，所需要的workspace与jobspace是不一样的

# 需要Jenkins安装的插件

Warnings，pipeline相关插件，具体安装本文忽略。

# 改造过程

## 流程示意图

<img class="shadow" src="/img/in-post/pipeline_project_parallel_circuit.png" width="800">


## Jenkins project配置

<img class="shadow" src="/img/in-post/pipeline_project_config1.png" width="1200">

<img class="shadow" src="/img/in-post/pipeline_project_config2.png" width="1200">

<img class="shadow" src="/img/in-post/pipeline_project_config3.png" width="1200">

<img class="shadow" src="/img/in-post/pipeline_project_config4.png" width="1200">

<img class="shadow" src="/img/in-post/pipeline_project_config5.png" width="1200">

<img class="shadow" src="/img/in-post/pipeline_project_config6.png" width="1200">

## pipelint Jenkinsfile

新增了Jenlinsfile，具体内容示例参考如下：

```shell
#!groovy

ip_list = IPS.split(',')
ips_size = ip_list.size()

def cluster1_ip = ip_list[0..2][1]
def cluster2_ip = ip_list[3..5][1]

def cluster_ip = "${cluster1_ip} ${cluster2_ip}"

pipeline {
    agent any

    options {
        timestamps()
        }

    stages {
        /* IP check */
        stage("IP Cheeck") {
                agent { label "master" }
                steps {
                    script {
                            sh """
                                if [[ ${ips_size} != 6 ]]; then
                                    echo "IPS is not enough, but give (${ips_size}) nodes to run case"
                                    exit 1
                                fi
                            """
                            }
                       }
            }

        /* Install VM by PVE */
        stage("Initialize") {
                agent { label "master" }
                steps {
                    script {
                            sh """
                            #!/bin/bash -xe
                            echo "Call batch_install_vs.py to install ISO."
                            sshpass -p 1 ssh -p 22 17.1.1.235 -l root \${BAT_INSTALL}
                            """
                        }
                }
            }

        /* Get code */
        stage("Checkout") {
                agent { label "master" }
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
        stage("Scp") {
                agent { label "master" }
                steps {
                    script {                            
                            sh """
                            #!/bin/bash -xe
                            cd \${WORK_SPACE};
                            rm -rf build.properties;
                            rm -rf report;
                            cd jenkins;
                            chmod a+x *;
                            for each_ip in ${cluster_ip}
                                do
                                    echo "Scp code to node : \${each_ip}"
                                    ssh-keygen -f '/var/lib/jenkins/.ssh/known_hosts' -R \${each_ip};
                                    ./rsync_pytest.sh \${WORK_SPACE} \${each_ip} root p@ssw0rd
                                    sleep 1
                                done
                            """
                        }
                    }
            }

        // Parallel Stage
        stage('Parallel Stage') {
            failFast true
            parallel {
                stage('Run test case on Cluster1') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster1_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster1_ip} \'cd ${CODE_DIR};python run.py -t testcase/Function_Test/case_02_Accounts/test_02_account_ad.py\'"
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
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster2_ip} \'cd ${CODE_DIR};cp config/autotest_106.config config/autotest.config;python run.py -t testcase/Function_Test/case_02_Accounts/test_03_account_ldap.py\'"

                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }
                    }
                }
                /*
                stage('Run test case on Cluster3 : ${cluster3_ip}') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster3_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root 172.17.75.96 uname -r"
                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }


                    }
                }
                stage('Run test case on Cluster4 : ${cluster4_ip}') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster4_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root 172.17.75.96 uname -r"
                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }


                    }
                }
                stage('Run test case on Cluster5 : ${cluster5_ip}') {
                    steps {
                        script {
                            try {
                                echo "Run test case on node : ${cluster5_ip}"
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root 172.17.75.96 uname -r"
                            }catch(err){
                                echo "${err}"
                                sh 'exit 1'
                            }
                        }


                    }
                }
                */
            }
        }

    /* Merge report */
        stage("Merge Report") {
            agent { label "master" }
            steps {
                script {
                        sh """
                        #!/bin/bash -xe
                        cd \${WORK_SPACE}/jenkins;
                        for each_ip in ${cluster_ip}
                            do
                                echo "Scp report from : (\${each_ip}) to jenkins node"
                                ./rsync_report.sh \${each_ip} root p@ssw0rd \${REPORT_DIR} \${WORK_SPACE} \${JOB_SPACE};
                                ./jenkins_build_properties.sh \${WORK_SPACE}
                            done
                        """
                    }
            }
        }


        stage("Allure Report") {
            agent { label "master" }
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
            agent { label "master" }
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
            agent { label "master" }
            steps {
                script{
                    echo "Run pylint code style check"
        		    // Ignore pylint comments via "-d C"
                    /*
        		    sh """
        		    	. .venv/bin/activate
        			    pylint -d C -f parseable ${SOURCE_ROOT} --exit-zero | tee ${PYLINT_REPORT}
        		    """
                    */
                }
        	}

        	post { 
                always { 
                       // Requires Warnings plugin since Violations plugin is deprecated
        			   // http://wiki.jenkins-ci.org/x/G4CGAQ
        			   warnings canComputeNew: false, canResolveRelativePaths: false, canRunOnFailed: true, categoriesPattern: '', defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', parserConfigurations: [[parserName: 'PyLint', pattern: "report/pylint.out"]], unHealthy: ''
                }
            }
        }

        /* Send Email */
        stage("Send Email") {
            agent { label "master" }
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
                            script: """sshpass -p btadminuser ssh -p 22 ${cluster1_ip} -l btadminuser ezs3-version""",
                            returnStdout: true
                            ).trim()
                        env.PRODUCT_VERSION = product_version

                        emailext([
                                attachLog: true,
                                attachmentsPattern: 'report/cgi_response_elapsed_time.txt,report/pytest_autotest.log.gz',
                                body: '${SCRIPT, template="allure-pipeline-report.groovy"}',
                                compressLog: true,
                                postsendScript: '$DEFAULT_POSTSEND_SCRIPT',
                                presendScript: '$DEFAULT_PRESEND_SCRIPT',
                                replyTo: '$PROJECT_DEFAULT_REPLYTO',
                                subject: '${JOB_NAME} - ${BUILD_DISPLAY_NAME}',
                                to: 'user01@bigtera.com.cn user02@bigtera.com.cn user03@bigtera.com.cn'
                       ])
                    }
                }
        }
    }
}
```

## email template

Jenkins server处，对应的email template内容参考如下:

```shell
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<style type="text/css">
/*base css*/
    body
    {
      margin: 0px;
      padding: 15px;
    }

    body, td, th
    {
      font-family: "Lucida Grande", "Lucida Sans Unicode", Helvetica, Arial, Tahoma, sans-serif;
      font-size: 10pt;
    }

    th
    {
      text-align: left;
    }

    h1
    {
      margin-top: 0px;
    }
    a
    {
      color:#4a72af
    }
/*div styles*/

.status{background-color:<%= 
            build.result.toString() == "SUCCESS" ? 'green' : 'red' %>;font-size:28px;font-weight:bold;color:white;width:720px;height:52px;margin-bottom:18px;text-align:center;vertical-align:middle;border-collapse:collapse;background-repeat:no-repeat}
.status .info{color:white!important;text-shadow:0 -1px 0 rgba(0,0,0,0.3);font-size:32px;line-height:36px;padding:8px 0}
</style>
<body>
<div class="content round_border">
                <div class="status">
                        <p class="info">pytest automation build <%= build.result.toString().toLowerCase() %></p>
                </div>

                <%
                    def envOverrides = it.getAction("org.jenkinsci.plugins.workflow.cps.EnvActionImpl").getOverriddenEnvironment()
                    product_version =  envOverrides["PRODUCT_VERSION"]
                %>

                <!-- status -->
                        <table>
                                <tbody>
                                        <tr>
                                                <th>Project:</th>
                                                <td>${project.name}</td>
                                        </tr>
                                        <tr>
                                                <th>Build ${build.displayName}:</th>
                                                <td><a
                                                        href="${rooturl}${build.url}">${rooturl}${build.url}</a></td>
                                        </tr>
                                        <tr>
                                                <th>Product Version:</th>
                                                <!--
                                                <td><%=build.environment['PRODUCT_VERSION']%></td> -->
                                                <td>${product_version}</td>
                                        </tr>
                                        <tr>
                                                <th>Date of build:</th>
                                                <td>${it.timestampString}</td>
                                        </tr>
                                        <tr>
                                                <th>Build duration:</th>
                                                <td>${build.durationString}</td>
                                        </tr>
                                        <tr>
                                                <td colspan="2">&nbsp;</td>
                                        </tr>
                                </tbody>

                        </table>
                <!-- main -->
        <% def artifacts = build.artifacts
            if(artifacts != null && artifacts.size() > 0) { %>

                        <b>Build Artifacts:</b>
                        <ul>
            <%          artifacts.each() { f -> %>
                <li><a href="${rooturl}${build.url}artifact/${f}">${f}</a></li>
            <%          } %>
                        </ul>
        <% } %>
  <!-- artifacts -->

<% 
  lastAllureReportBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureReportBuildAction.class)
  lastAllureBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureBuildAction.class)

  if (lastAllureReportBuildAction) {
    allureResultsUrl = "${rooturl}${build.url}allure"
    allureLastBuildSuccessRate = String.format("%.2f", lastAllureReportBuildAction.getPassedCount() * 100f / lastAllureReportBuildAction.getTotalCount())
  }
%>

<%
pylintResultsUrl = "${build.environment['JOB_URL']}warnings50/trendGraph"
coberturaResultsUrl = "${rooturl}${build.url}cobertura"
%>

<% if (lastAllureReportBuildAction) { %>
<h2>Allure Results</h2>
<table>
            <tbody>
                        <tr>
                            <th>Total Allure tests run:</th>
                            <td><a href="${allureResultsUrl}">${lastAllureReportBuildAction.getTotalCount()}</a></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #ffff00;">Failed:</span></th>
                            <td><span style="color: #000000; background-color: #ffff00;">${lastAllureReportBuildAction.getFailedCount()} </span></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #008000;">Passed:</span></th>
                            <td><span style="color: #000000; background-color: #008000;">${lastAllureReportBuildAction.getPassedCount()} </span></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #3366ff;">Skipped:</span></th>
                            <td><span style="color: #000000; background-color: #3366ff;">${lastAllureReportBuildAction.getSkipCount()} </span></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #ff0000;">Broken:</span></th>
                            <td><span style="color: #000000; background-color: #ff0000;">${lastAllureReportBuildAction.getBrokenCount()} </span></td>
                        </tr>
                        <tr>
                            <th>Success rate: </th>
                            <td>${allureLastBuildSuccessRate}%  </td>
                        </tr>

            </tbody>
</table>

<br>
<img lazymap="${allureResultsUrl}/graphMap" src="${allureResultsUrl}/graph" alt="Allure results trend"/>
</br>

<br>
<font size=4><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pylint history trend</b></font>
</br>
<br>
<img src="${pylintResultsUrl}/png?url=PRIORITY"/>
</br>

<br>
<font size=4><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Code Coverage history trend</b></font>
</br>
<br>
<img lazymap="${coberturaResultsUrl}/graphMap" src="${coberturaResultsUrl}/graph"/>
</br>
<% } %>                  
  <!-- content -->
  <!-- bottom message -->
</body>
```

## 运行效果

Jenkins pipeline project流程图：

<img class="shadow" src="/img/in-post/pipeline_Process_rendering.png" width="1200">

Jenkins send email效果图：

<img class="shadow" src="/img/in-post/pipeline_send_email1.png" width="1200">

<img class="shadow" src="/img/in-post/pipeline_send_email2.png" width="1200">

