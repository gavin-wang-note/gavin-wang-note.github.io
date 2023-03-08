---
layout:     post
title:      "Ubuntu 22.04上部署、配置Jenkins"
subtitle:   "Deploy Jenkins in Ubuntu 22.04"
date:       2023-03-08
author:     "Gavin"
catalog:    true
tags:
    - jenkins
---

# 概述



本文基于Ubuntu 22 安装 Jenkins 2.375.3，记录下部署与调试过程   。



# 准备工作

## 安装Ubuntu 22.04

OS信息如下：

```
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



## 安装必要的软件包


如下，列出了必要的软件安装（没有完整的记录下来，可能不全）：

```
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


```
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



# 配置Jenkins


Jenkins 安装好后，访问8080端口，按提示一步一步往下走，此处不做额外赘述。



## Jenkins Plugin 的安装

**需要安装如下插件与工具：**

```
allure
Cobertura Coverage
Violations Plugin # Pylint
AnsiColor         # 颜色
Next Build Number Plugin
```

一些基础的Plug，像git, pipline 之类的安装，此处不做赘述。



**install allure commandline：**

安装包手动下载下来：``` https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.21.0/allure-commandline-2.21.0.tgz ```

在Jenkins上使用root 用户，安装到/usr/lib/下，参考如下：

``` /usr/lib/allure-2.21.0/lib/allure-commandline-2.21.0.jar ```




## 修改 expect spawn ssh时prompt无法通过问题

修改vim /etc/ssh/ssh_config

``` StrictHostKeyChecking ask   -->改为 StrictHostKeyChecking no ```

并重启ssh服务，以此来避免expect 中执行spawn交互失败。





## Jenkins 邮箱配置

Jenkins 当前登录UI用户的邮箱，需要和全局配置里设置的邮箱用户名保持一致，否则会报错，参考如下：

<p><img class="shadow" src="/img/in-post/jenkins_email_config.png" width="1200" /></p>



参考如下：

``` https://naiveskill.com/jenkins-pipeline-email-notification/ ```



## Jenkins 匿名用户权限配置


为了让Email端能够正常展示出allure trend，pylint error，以及CODE COVERAGE信息，需要对匿名用户开放一定的权限：


<p><img class="shadow" src="/img/in-post/Jenkins_permission.png" width="1200" /></p>



## Email 模板

为了让CI结果更好的展示，基于官方模板(```https://github.com/jenkinsci/email-ext-plugin/blob/master/src/main/resources/hudson/plugins/emailext/templates/groovy-html.template ```)，
增加了allure, pylint 和 CODE COVERAGE信息，自定义了一个EMail模板，存放在Jenkins install path()下：


```
jenkins@jenkins:/var/lib/jenkins$ cd email-templates/
jenkins@jenkins:/var/lib/jenkins/email-templates$ ls -l
total 120
-rw-rw-r-- 1 jenkins jenkins  6292 Feb 17 15:49 allure-report.groovy
-rw-r--r-- 1 jenkins jenkins 69669 Mar  7 18:57 v1.0_allure-pipeline-report.groovy
-rw-r--r-- 1 jenkins jenkins  7759 Mar  7 22:24 v1.1_allure-pipeline-report.groovy
jenkins@jenkins:/var/lib/jenkins/email-templates$ 
jenkins@jenkins:/var/lib/jenkins/email-templates$ 
```



其中，**v1.1_allure-pipeline-report.groovy** 为当前使用模板，里面有定义一个需要被替换的内容：

```
  <table>
    <tr>
        <img src="EMAIL_BASE64_IMG_REPLACE" width="500px" height="200px"/>
    </tr>
  </table>
```

此处内容，需要借助 **edit_email_template.py**  这个代码来生成base64 image并替换，最终被pipline 处的EMail 使用。

需要借助 **edit_email_template.py**  的原因在于，新版本的Jenkins，对于pylint结果产生的图形，是基于canvas，并不是一个静态图片，无法通过HTML中的img src来直接指定。





# 实践

如下，以Lab 实际配置截图：

<p><img class="shadow" src="/img/in-post/jenkins_job_config.png" width="1200" /></p>



总共设置了String类型的如下参数：


* GIT_WEB  --> http://1.22.21.9/pytest_framework
* GIT_URL  --> git@1.22.21.9:pytest_framework.git
* GIT_BRANCH --> 8.3
* REPORT_DIR --> /root/${JOB_NAME}/report                                        # Jenkins install path
* WORK_SPACE --> ${JENKINS_INSTALL_PATH}/workspace/pytest_8.3_pipeline           # Jenkins work space
* JOB_SPACE --> ${JENKINS_INSTALL_PATH}/jobs/pytest_8.3_pipeline                 # pytest job space
* BAT_INSTALL -->  /root/batch_install/batch_install.py /root/batch_install/config/pytest/pytest_8.3_pipeline_195_cone # Bat install OS by Cobbler
* IPS --> 12.71.57.11,12.71.57.12,12.71.57.13,12.71.57.14,12.71.57.15,12.71.57.16,12.71.57.17,12.71.57.18              # Cluster hosts IP,split by,
* CODE_DIR --> /root/${JOB_NAME}/src                                             # pytest code dir which will be runned


**Email Template**

在官方模板 ``` https://github.com/jenkinsci/email-ext-plugin/blob/master/src/main/resources/hudson/plugins/emailext/templates/groovy-html.template ``` 的基础上，增加了三张图。


**pipline Script**

{% raw %}```
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
  so 03Hosts and 05RRS need to be executed in a cluster 
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
                            sshpass -p 1 ssh -p 22 12.71.57.236 -l root \${BAT_INSTALL}
                            """
                        }
                }
            }

        /* Get code */
        stage("Code Checkout") {
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
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster1_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_11_12_13.config config/autotest.config;python run.py -t \"testcase/Function_Test/case_03_Hosts/\" -n True \'"
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
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster2_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_15_16_17.config config/autotest.config;python run.py -t \"testcase/Function_Test/case_11_CSI testcase/Function_Test/case_10_S3/test_05_datasearch.py \"\'"

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
                                sh "sshpass -p p@ssw0rd ssh -p 22 -l root ${cluster5_ip} \'cd ${CODE_DIR}; dpkg -i ../python_3rd_lib/python-configobj_4.7.2+ds-3build1_all.deb;cp config/autotest_24_25_26.config config/autotest.config;python run.py -t \"testcase/Function_Test/case_99_others \"\'"
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

        stage("Generate Allure Report") {
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
                                to: 'zhangsan@163.com'
                       ])
                    }
                }
        }
    }
}
``` {% endraw %}



如果想生成3个维度的数据，示例代码如下：


{% raw %}```
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
``` {% endraw %}


# 效果展示



最终EMail 邮寄出来的内容如下：

全部成功状态下：

<p><img class="shadow" src="/img/in-post/jenkins_build_success.png" width="1200" /></p>


部分用例失败状态下：

<p><img class="shadow" src="/img/in-post/jenkins_build_unstable.png" width="1200" /></p>

