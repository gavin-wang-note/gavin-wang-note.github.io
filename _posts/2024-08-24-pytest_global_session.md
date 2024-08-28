---
title: pytest设计API自动化测试框架时前后端全局session的应用
date: 2024-08-24
author: Gavin Wang
img: "/img/pytest/pytest-25.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 在产品前后端API测试框架设计过程中，如何让前后端使用各自独立的一个全局session，而且要确保整个用例执行过程中只有一个前端和一个后端session？
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

最近针对有前后端的产品来设计一款`API`自动化测试框架，基于`pytest`。

产品有前端，也有后端，前端有一套登录认证，后端另外一套登录认证。

如何使用各自独立的一个`session`，完成整个测试框架下用例的执行呢？即后端用户登录，有一个`session`，后端所有的操作都是基于此`session`；相应的前端有一个账号登录，有一个`session`，前端所有的操作基于此前端登录产生的`session`。
这两个`session`互相独立，互不干扰，有些类似我们使用了两个账号登录了`Web`的前后端（前端用户账号，后端管理员账号），基于此而做的各种`Web`页面操作，前后端各自一个`session`，各自动作。

在过往框架设计过程中，往往发生各自基类使用各自的登录`session`，如果基类比较多，会造成在用例执行初期产生大量的`session`，一是造成资源浪费，二来也没有使用多个`session`的必要，基于此而写的本文：

主题：
如何在`pytest`测试框架中使用一个全局`session`？

# Solution

我的解决方案如下：

1.封装`HttpSession`基类，实现前端（`front end`）和后端（`back end`）登录动作
2.借助`pytest fixture`和`conftest.py`特性，使用`yield`返回前后端各自所需的`session`

# Code view

## http_session.py代码片段

```python
    def backend_token_verify(self):
        """Product validation of the desired effect after sliding the slider"""

        # Update http request header info, hard code of Authorization
        header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate',
'Content-Type': 'application/x-www-form-urlencoded',
'Cache-Control': 'no-cache',
'isToken': 'false',
'Authorization': 'Basic Ym9zczpib3Nz',
'tenant-id': '1',
'Connection': 'keep-alive',
'Pragma': 'no-cache',
}
        self.backend_session.headers.update(header)

        s_key, point_json, token = self.backend_check_slide()
        x_str = aes_decrypt(s_key, point_json)
        code_str = f'{token}---{x_str}'
        source_code = aes_encrypt(s_key, code_str)
        code = urllib.parse.quote(source_code).replace('/', '%2F')

        # Splice token url and send request
        token_url = self.backend_base_url + CONFIG['auth']['token'].\
                    replace('ADMIN', self.user).replace('CODE', code)
        request_body = {"password": CONFIG['admin_credentials']['password']}
        data = urllib.parse.urlencode(request_body)
        res = self.backend_session.post(token_url, data=data, headers=self.backend_session.headers)

        if res.status_code != HttpCode.OK:
            err_msg = "[ERROR]  Login failed, login data: %s, http " \
                      "status code: %s", data, res.status_code
            logging.exception(err_msg)

        # Update header
        new_token = res.json()['access_token']
        self.backend_session.headers.update({'Authorization': f'Bearer {new_token}'})

        return self.backend_session

    def front_login_auth(self, phone=None):
        """
        Front login by phone numbeer and verification code
        :param phone, int, a phone number
        """
        phone = generate_phone_number() if phone is None else phone
        # Get and check verification code
        verification_code = self.front_get_verification_code(phone)
        self.front_check_verification_code(phone, verification_code)

        logging.info("[Action]   Start to login by phone: (%s) and "
                     "verification code:(%s)", phone, verification_code)

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; ' \
                          'rv:129.0) Gecko/20100101 Firefox/129.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Authorization': 'Basic YXBwOmFwcA==',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
        }
        self.front_session.headers.update(header)

        login_url = self.front_base_url + CONFIG['login']['auth'].replace('PHONENO', phone).\
                    replace('CODE', verification_code)
        login_res = self.front_session.post(login_url, headers=self.front_session.headers)

        if login_res.status_code != HttpCode.OK:
            err_msg = "[ERROR]  Front login failed, http status code: %s", login_res.status_code
            logging.exception(err_msg)

        # Update Auth from the response of token
        new_token = login_res.json()['access_token']
        tenant_id = login_res.json()['tenantId']
        update_header = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Authorization": f"Bearer {new_token}",
            "TENANT-ID": str(tenant_id)
        }
        self.front_session.headers.update(update_header)
        logging.debug("==  front headers: (%s)", self.front_session.headers)

        return self.front_session
```

如上，封装了前后端各自的`session`，接下来借助`pytest`的`fixture`特性，放在代码顶层目录下`conftest.py`文件中。

## fixture和conftest.py结合

`Content of conftest.py`:

```python
@pytest.fixture(scope='session', autouse=True)
def backend_session():
    session = HttpSession()
    try:
        session.backend_token_verify()
        yield session
    finally:
        session.backend_logout()


@pytest.fixture(scope='session', autouse=True)
def front_session():
    session = HttpSession()
    phone = generate_phone_number()
    try:
        session.front_login_auth(phone)
        yield session
    finally:
        session.front_logout()
```

这里将封装的前后端`session`，放在`fixture`中，这两个`fixture`分别被命名为`backend_session`和`front_session`

## 使用全局session

`fixture`中有了全局`session`，要如何使用呢？

在编写测试用例基类和测试用例时，需要传递对应的`fixture`，即前端`session`传递`front_session`，后端传递`backend_session`，对应测试用例基类和测试用例，参考如下：

测试用例基类：

```python
    def get_category_tags(self, backend_session):
        """Get all of the category names"""
        logging.info("[Action]   Start to get all of the category names")
        tag_names = {}
        data = {"size":200,"current":1,"query":{"bizType":1,"type":2}}
        res = backend_session.send_request('POST', self.promote_url['tag'], json=data)
        for each_tag in res.json()['data']['records']:
            tag_names[each_tag['tagName']] = each_tag['tagNo']

        return tag_names

    def get_categroy_random(self, backend_session):
        """Get category tag by random"""
        tag_names = self.get_category_tags(backend_session)
        random_name = random.choice(list(tag_names.keys()))
        random_tag = tag_names[random_name]

        return random_tag
```

测试用例：

```python
class TestPromoteTemplate():
    """Test case of promote template"""
    promote_template = PromoteTemplateManager()

    def test_create_promote_template(self, backend_session):
        """Create a promote template"""
        template_name, role_name, agent_tag_library_no, _ = self.promote_template.create_promote_template(backend_session)

        # List the promote template
        record = self.promote_template.list_promote_template(backend_session,
                                                             template_name=template_name,
                                                             role_name=role_name,
                                                             agent_tag_library_no=agent_tag_library_no)

        self.promote_template.delete_promote_template(backend_session, template_no=record['templateNo'])
```

# 结语

当然还有其他的方法，这里就不再赘述。

如果你担心`session`时效比较短，或者用例比较多情况下执行起来耗时较久导致`session`过期，没关系，可以在`HttpSession`封装`session`时判断相应状态码，如果是401，再重新登录一次，从而完成新`session`的产生。
