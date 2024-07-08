---
title: pytest+requests+Allure实现API自动化测试框架设计
date: 2024-06-18 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-3.png"
top: true
hide: false
cover: true
coverImg:
password:
toc: true
mathjax: false
summary: 基于pytest+requests+Allure设计API自动化测试框架
categories:
    - [Automation]
    - [API]
    - [pytest]
tags:
    - Automation
    - API
    - pytest
---

# 前言

`pytest`是一个功能强大的`Python`测试框架，它提供了丰富的插件支持和灵活的测试用例管理。而`requests`库则是`Python`中用于发送`HTTP`请求的第三方库，它简单易用，支持多种认证方式和数据格式。在众多自动化测试工具中，`pytest`结合`requests`库已成为实现`API`接口级自动化测试的流行选择。

本文将基于`pytest+allure+requests`实现`OrangeHRM`的`API`自动化测试框架的设计与开发工作, 同时兼容`Linux`和`Windows`平台下测试用例的运行(`run_tests.py`做兼容)。

PS：

做好框架的分层设计，再加上这种自动化设计对我并没有什么难度，实在提不起太多兴趣去多写文章内容，简要概况一下，仅供参考。


# API自动化测试框架结构

测试框架目录结构示例如下：

```shell
root@Gavin:~/automation/API# tree -L 2
.
├── clear_pyc.py
├── configs           # 存放配置文件
│   ├── config.yaml   # 测试环境配置
│   └── __init__.py
├── conftest.py       # pytest fixtures配置
├── __init__.py
├── jenkins           # CI/CD构建所需的相关脚本
│   ├── edit_email_template.py
│   ├── Jenkinsfile.txt
│   ├── rsync_code.sh
│   ├── rsync_report.sh
│   └── v1.1_allure-pipeline-report.groovy
├── logs              # 存放日志文件
│   └── api_test.log
├── pytest.ini        # pytest主配置文件
├── README.md
├── reports           # Allure测试报告
│   ├── coverage.xml  # Jenkins页面展示代码覆盖率信息
│   ├── html          # Allure html测试报告
│   ├── json          # Allure测试报告原始文件
│   └── pylint.out    # Jenkins页面展示pylint信息
├── requirements.txt  # 项目依赖文件
├── run_tests.py      # 测试用例执行总入口
├── testcasebase      # 
│   ├── __init__.py
│   └── personal_info_management.py
├── tests             # 测试用例目录
│   ├── __init__.py
│   ├── test_debug.py
│   ├── test_employee.py
│   └── test_login.py
└── utils             # 通用、公共的模块
    ├── api_client.py # 请求封装类
    ├── common.py     # 公共方法
    ├── config.py     # 解析yaml配置文件
    ├── error_codes.py # 定义产品错误码
    ├── __init__.py
    └── mysql_options.py # mysql数据库相关操作封装
```

# 部分代码示例片段

## requirements.txt

`requirements.txt`内容参考如下：

```shell
root@Gavin:~/automation/API# cat requirements.txt 
pytest==8.0.2
requests==2.31.1
allure-pytest==2.13.2
PyYAML==6.0.1
allure-pytest==2.13.2
allure-python-commons==2.13.2
pylint==2.17.4
Faker=24.0.0
PyMySQL=1.1.0
tzlocal=5.2
root@Gavin:~/automation/API# 
```

## config.yaml

```shell
root@Gavin:~/automation/API/configs# cat config.yaml 
# OrangeHRM服务配置
orangehrm_base_url: "http://192.168.23.130/orangehrm-5.6"
admin_credentials:
  username: "admin"
  password: "Huawei123!"

# mysql信息
mysql:
  host: 192.168.23.130  # 数据库地址，请根据实际情况填写
  user: orange          # 数据库用户名，请根据实际情况填写
  password: orange      # 数据库密码，请根据实际情况填写
  dbname: hrm           # 数据库名，请根据实际情况填写

# 个人信息管理系统
employees:
  add_employee: "/web/index.php/api/v2/pim/employees"
  modify_personal_details: "/web/index.php/api/v2/pim/employees/EmployeeID/personal-details"
  list_employees: "/web/index.php/api/v2/pim/employees?limit=50&offset=0&model=detailed&includeEmployees=onlyCurrent&sortField=employee.firstName&sortOrder=ASC"
  modify_contact_details: "/web/index.php/api/v2/pim/employee/EmployeeID/contact-details"
  get_contact_details: "/web/index.php/api/v2/pim/employee/EmployeeID/contact-details"
  add_emergency_contacts: "/web/index.php/api/v2/pim/employees/EmployeeID/emergency-contacts"
  get_emergency_contacts: "/web/index.php/api/v2/pim/employees/EmployeeID/emergency-contacts?limit=50&offset=0"
  add_dependents: "/web/index.php/api/v2/pim/employees/EmployeeID/dependents"
  get_dependents: "/web/index.php/api/v2/pim/employees/EmployeeID/dependents?limit=50&offset=0"
  add_job_details: "/web/index.php/api/v2/pim/employees/EmployeeID/job-details"
  get_job_details: "/web/index.php/api/v2/pim/employees/EmployeeID/job-details"
  add_salary_components: "/web/index.php/api/v2/pim/employees/EmployeeID/salary-components"
  get_salary_components: "/web/index.php/api/v2/pim/employees/EmployeeID/salary-components?limit=50&offset=0"
  add_supervisors: "/web/index.php/api/v2/pim/employees/EmployeeID/supervisors"
  get_supervisors: "/web/index.php/api/v2/pim/employees/EmployeeID/supervisors?limit=50&offset=0"
  add_subordinates: "/web/index.php/api/v2/pim/employees/EmployeeID/subordinates"
  get_subordinates: "/web/index.php/api/v2/pim/employees/EmployeeID/subordinates?limit=50&offset=0"
  add_work_experiences: "/web/index.php/api/v2/pim/employees/EmployeeID/work-experiences"
  get_work_experiences: "/web/index.php/api/v2/pim/employees/2/work-experiences?limit=50&offset=0"

# 休假
vacation:
  save_leave_period: "/web/index.php/api/v2/leave/leave-period"

# 时间


# 招聘


# 我的信息


# 绩效
root@Gavin:~/automation/API/configs#
```

## api_client.py

```python
root@Gavin:~/automation/API/utils# cat api_client.py 
import sys
import logging
import requests

from utils.config import CONFIG
from utils.error_codes import HttpCode



class OrangeHRMAPIClient(object):
    def __init__(self):
        # Not verify SSL certificate
        self.verify = False

        # timeout time
        self.timeout = (60, 600)

        # Other info
        self.base_url = CONFIG['orangehrm_base_url']
        self.session = requests.Session()

    def login(self):
        # 获取配置中的信息
        username = CONFIG['admin_credentials']['username']
        password = CONFIG['admin_credentials']['password']

        login_endpoint = f"{self.base_url}/web/index.php/auth/login"
        auth_endpoint = f"{self.base_url}/web/index.php/auth/validate"
        try:
            login_res = self.session.get(login_endpoint)
            token = login_res.text.split('token=')[-1].split('\n')[0].replace("&quot;", "").replace('"', '')
            self.session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})

            auth_payload = {
                '_token': token,
                'username': username,
                'password': password
            }

            # Adjust as needed for actual endpoint and method
            response = self.session.post(auth_endpoint, data=auth_payload)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

            # After a successful login, the session will include authentication details
            if response.status_code != HttpCode.OK: 
                err_msg = f"[ERROR]  Login failed, login data : (auth_payload), http status code: ({response.status_code})"
                logging.exception(err_msg)
                sys.exit(1)
            return self.session
        except requests.HTTPError as err:
            logging.error(f"HTTP错误: %s", err)
        except requests.RequestException as err:
            logging.error(f"请求错误: %s", err)

    def send_request(self, method, endpoint, **kwargs):
        """
        封装的HTTP请求发送函数
        :param method: 请求方法，如 'get', 'post', 'put', 'delete'。
        :param endpoint: API 端点。
        :param kwargs: 其他请求参数，如 data, json, headers 等。
        :return: 请求响应。
        """
        try:
            # 根据方法构建请求函数
            request_func = getattr(self.session, method.lower())

            # 发送请求
            response = request_func(f"{self.base_url}{endpoint}", **kwargs)
            response.raise_for_status()  # 检查响应状态码

            return response
        except AttributeError:
            logging.error(f"不支持的方法: %s", method)
        except requests.HTTPError as err:
            logging.error(f"HTTP错误: %s", err)
        except requests.RequestException as err:
            logging.error(f"请求错误: %s", err)
root@Gavin:~/automation/API/utils#
```



## run_tests.py

```python
root@Gavin:~/automation/API# cat run_tests.py 
import os
import sys
import platform
import argparse
import subprocess


def run_pylint(allure_dir):
    """
    生成Pylint报告
    :param allure_dir:
    :return:
    """
    pylint_cmd = 'pylint --rcfile=.pylintrc -f parseable -d I0011,R0801 ./'
    if 'windows' in platform.platform().lower():
        # Windows 平台，使用 subprocess 获取输出并写入文件
        process = subprocess.Popen(pylint_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        with open(f"{allure_dir}/pylint.out", "w") as outfile:
            for line in process.stdout:
                # 将输出写入文件和控制台
                sys.stdout.buffer.write(line)
                outfile.write(line.decode())
        process.wait()
    else:
        # Linux/macOS 平台，直接使用原始命令
        process = subprocess.run(f"{pylint_cmd} | tee {allure_dir}/pylint.out",
                                  shell=True, check=True)

def run_pytest(tests_path, allure_dir):
    """
    运行pytest以及生成Allure和覆盖率报告
    :param tests_path: 测试用例的路径
    :param allure_dir: 报告输出的目录
    """
    env = os.environ.copy()
    if not os.path.exists(allure_dir):
        os.mkdir(allure_dir)

    # 定义命令行参数
    pytest_cmd = [
        'pytest',
        tests_path,
        f'--alluredir={allure_dir}/json',
        '--cov=.',
        f'--cov-report=xml:{allure_dir}/coverage.xml'
    ]

    # 运行pytest
    print(f"{pytest_cmd}")
    subprocess.run(pytest_cmd, env=env)

    # 生成Pylint报告
    run_pylint(allure_dir)

# 主函数，用来解析命令行参数并运行测试
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run pytest with allure and coverage')
    parser.add_argument(
        '--tests_path',
        action='store',
        default='tests',         # 默认执行tests目录下的所有测试
        help='Specify path to tests'
    )
    parser.add_argument(
        '--allure_dir',
        action='store',
        default='reports',        # 默认将报告输出到reports目录下
        help='Specify directory to output reports'
    )
    args = parser.parse_args()

    run_pytest(args.tests_path, args.allure_dir)
    print("---------------- end ----------")
root@Gavin:~/automation/API#
```

代码内容比较多，其他内容就不贴了。

# 执行效果

参考如下的`gif`展示效果(点击查看大图效果更好)：

<img class="shadow" src="/img/in-post/gif/API.gif" width="1200">
