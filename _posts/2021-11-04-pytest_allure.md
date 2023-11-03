---
layout:     post
title:      "pytest with allure"
subtitle:   "pytest with allure"
date:       2021-11-04
author:     "Gavin"
catalog:    true
tags:
    - pytest
    - Automation
    - Allure 
---



# 概述



本文基于allure 2.13.2 版本介绍allure在pytest下的基本运用。

关于allure，详见官网： ``` https://github.com/allure-framework```。





# allure功能介绍



## allure 特性



allure有如下特性：



```
C:\Users\Wang>python
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2021, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import allure
>>> dir(allure)
['__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'attach', 'attachment_type', 'description', 'description_html', 'dynamic', 'epic', 'feature', 'id', 'issue', 'label', 'link', 'manual', 'parameter_mode', 'parent_suite', 'severity', 'severity_level', 'step', 'story', 'sub_suite', 'suite', 'tag', 'testcase', 'title']
>>>
```



介绍如下：



| 使用方法                  | 参数值             | 参数说明                                                     |
| ------------------------- | ------------------ | ------------------------------------------------------------ |
| allure.attach()           | 添加附件           | 给测试用例添加附件                                           |
| allure.attachment_type()  | 附件类型           | 支持txt/pdf/csv/html/xml/image/video等多种类型               |
| allure.description()      | 用例描述           | 传递一个字符串参数用来描述测试用例                           |
| allure.description_html() | 用例描述           | 传递一段HTML文本，这将在测试报告的"Description"部分渲染出来  |
| allure.dynamic()          | 动态指定标题和描述 | 在测试用例执行过程中动态指定标题和描述等标签的方法，主要指：allure.dynamic.description 和 allure.dynamic.title |
| allure.epic()             | epic描述           | 敏捷里的概念，定义史诗，相当于module级的标签                 |
| allure.feature()          | 模块名称           | 功能点的描述，往下是story                                    |
| allure.id()               | 人为给用例添加id   | **貌似添加后没有看到效果，未在实际工作中使用过，尚不知应用场景** |
| allure.issue()            | 缺陷链接           | 对应缺陷管理系统里的链接，如将JIRA里Bug的URL展示在html报告中 |
| allure.label()            | 给用例添加label    | **貌似添加后没有看到效果，未在实际工作中使用过，尚不知应用场景** |
| allure.link()             | 链接               | 定义一个链接，在html报告中展示                               |
| allure.manual()           |                    | **尚不知具体用途**                                           |
| allure.parameter_mode()   |                    | **尚不知具体用途**                                           |
| allure.parent_suite()     | 测试套             | 测试套的三个级别，爷爷父亲儿子中的爷爷这个级别               |
| allure.severity()         | 用例级别           | 测试用例的优先级别，blocker,critical,normal,minor,trivial 五个级别，使用方式：@allure.severity("BLOCKER") |
| allure.severity_level()   | 用例级别           | 测试用例的优先级别，blocker,critical,normal,minor,trivial 五个级别，使用方式：@allure.severity(allure.severity_level.CRITICAL) |
| allure.step()             | 操作步骤           | 测试用例的步骤，Step1，Step2，... StepN标记在用例中          |
| allure.story()            | 用户故事           | 用户故事，往下是title                                        |
| allure.sub_suite()        | 测试套             | 测试套的三个级别，爷爷父亲儿子中的儿子这个级别               |
| allure.suite()            | 测试套             | 测试套的三个级别，爷爷父亲儿子中的父亲这个级别               |
| allure.tag()              | Tag                | 给用例增加tag                                                |
| allure.testcase()         | 测试用例的链接     | 对应功能/性能测试用例系统里的test case URL，如testlink里的   |
| allure.title()            | 用例的标题         | 展示在html报告中的测试用例的标题名称                         |



## allure 实践



### allure为测试用例添加附件（attach）



#### allure.attach的用法



##### 用法一



语法：


``` allure.attach(body, name, attachment_type, extension) ```



参数解释：

- body：要写入附件的内容
- name：附件名字
- attachment_type：附件类型，是allure.attachment_type其中的一种
- extension：附件的扩展名



##### 用法二



语法：

``` allure.attach.file(source, name, attachment_type, extension) ```



参数解释：

- source：文件路径，相当于传一个文件
- name：附件名字
- attachment_type：附件类型，是allure.attachment_type其中的一种
- extension：附件的扩展名



#### allure.attachment_type的所有值


```
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



#### allure.attach使用举例



##### 测试用例中添加文本附件



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

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


<img class="shadow" src="/img/in-post/allure/attach_text.png" width="1200">



##### 测试用例中添加html附件



```
def test_mutiple_attachments():
    allure.attach.file(r"C:\Users\Wang\Pictures\OIP-C.jpg", attachment_type=allure.attachment_type.JPG)

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



<img class="shadow" src="/img/in-post/allure/attach_image.png" width="1200">

如上图所示，html部分可以嵌套图片，也可以写静态文本。





### allure添加测试用例步骤(allure.step)



在编写自动化测试用例的时候经常会遇到需要编写流程性测试用例的场景，一般流程性的测试用例的测试步骤比较多，在测试用例中添加详细的步骤会**提高测试用例的可阅读性**。

allure提供的装饰器@allure.step()是allure测试报告框架非常有用的功能，它能帮助我们在测试用例中对测试步骤进行详细的描述。



代码示例：



```
    def test_566_rollback_snapshot(self):
        """  Sc-566:Snapshot can be rollbacked correctly  """
        with allure.step("Clean unavailable link device"):
            self.client_unlink_unavailable_device_link(self.client_ip_root_password, self.ssh_port, self.client_ip)

        with allure.step("Client umount mount point"):
            self.client_umount_san_device(gateway_group=self.gateway_group, target_id=self.target_id,
                                          iscsi_id=self.iscsi_id, password=self.client_ip_root_password,
                                          port=self.ssh_port, client_ip=self.client_ip,
                                          mount_point=self.mount_point, check_device=False)
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
            self.client_write_file_to_san(password=self.client_ip_root_password, port=self.ssh_port,
                                          client_ip=self.client_ip, mount_point=self.mount_point,
                                          file_name='before_snap.txt', file_content='before_snap')
        time.sleep(60)
        before_md5 = self.get_file_md5(password=self.client_ip_root_password, port=self.ssh_port,
                                       client_ip=self.client_ip, mount_point=self.mount_point,
                                       file_name='before_snap.txt')

        with allure.step("Take a snapshot"):
            self.create_snapshot(gateway_group=self.gateway_group, target_id=self.target_id,
                                 iscsi_id=self.iscsi_id, snap_name='pytest-snapshot02')

        with allure.step("Client umount mount point,"):
            #  if no this step, when logout target will raise in use error in centos
            self.client_umount_san_device(gateway_group=self.gateway_group, target_id=self.target_id,
                                          iscsi_id=self.iscsi_id, password=self.client_ip_root_password,
                                          port=self.ssh_port, client_ip=self.client_ip,
                                          mount_point=self.mount_point, check_device=False)

        with allure.step("Client disconnect the target"):
            self.client_login_logout_target(password=self.client_ip_root_password, port=self.ssh_port,
                                            client_ip=self.client_ip, target_id=self.target_id,
                                            op_type='logout')

        with allure.step("Disable the volume, then rollback snapshot"):
            self.disable_iscsi_volume(target_id=self.target_id, iscsi_id=self.iscsi_id)
            self.rollback_snap(gateway_group=self.gateway_group, target_id=self.target_id,
                               iscsi_id=self.iscsi_id)

        with allure.step("Enable the volume"):
            self.enable_iscsi_volume(gateway_group=self.gateway_group, target_id=self.target_id,
                                     iscsi_id=self.iscsi_id)

        with allure.step("Client connect to the target"):
            self.client_login_logout_target(password=self.client_ip_root_password, port=self.ssh_port,
                                            client_ip=self.client_ip, target_id=self.target_id,
                                            op_type='login')


            self.client_mount_san_device(gateway_group=self.gateway_group, target_id=self.target_id,
                                         iscsi_id=self.iscsi_id, password=self.client_ip_root_password,
                                         port=self.ssh_port, client_ip=self.client_ip,
                                         mount_point=self.mount_point)

        # Get file of md5
        after_md5 = self.get_file_md5(password=self.client_ip_root_password, port=self.ssh_port,
                                      client_ip=self.client_ip, mount_point=self.mount_point,
                                      file_name='before_snap.txt')

        with allure.step("Check md5"):
            errr_msg = "[ERROR]  before_md5 is : ({}), after_md5 is : ({}),  " \
                       "md5 is not same when reconnect to target : ({})".format(before_md5,
                                                                                after_md5,
                                                                                self.target_id)
            eq_(before_md5, after_md5, errr_msg)

        with allure.step("Client umount"):
            self.client_umount_san_device(gateway_group=self.gateway_group, target_id=self.target_id,
                                          iscsi_id=self.iscsi_id, password=self.client_ip_root_password,
                                          port=self.ssh_port, client_ip=self.client_ip,
                                          mount_point=self.mount_point)

        with allure.step("Client disconnect the target"):
            self.client_login_logout_target(password=self.client_ip_root_password, port=self.ssh_port,
                                            client_ip=self.client_ip, target_id=self.target_id,
                                            op_type='logout')

        with allure.step("Delete all snapshot"):
            self.delete_snapshot(gateway_group=self.gateway_group, target_id=self.target_id,
                                 iscsi_id=self.iscsi_id, delete_all_snap=True)
```



这里借助with allure.step() 来完成添加step动作。

上述这个示例代码能否再精简呢？答案是肯定的，如果精简？

这里提供一下思路：

如果这个py文件中含有很多的test case，每个test case都需要增加allure.step，且step里描述的内容相同，可以在被调用的各个函数里增加step动作，test case里完全是函数的调用。



示例如下：

比如上例中的 delete_snapshot 函数，可以将class中定义function时，增加allure.step步骤，参考如下：



```
    @allure.step("Delete snapshot")
    def delete_snapshot(self, gateway_group=None, target_id=None, iscsi_id=None, snap_name=None,
                        expected_return_code=None, delete_all_snap=None):
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

```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

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



<img class="shadow" src="/img/in-post/allure/step_parameter.png" width="1200">



也可以设置传递一个/多个可选参数，不传则为None，示例如下：



```
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





### allure为测试用例添加描述（description）



#### allure添加描述的三种方式：

- 使用装饰器@allure.description，传递一个字符串参数用来描述测试用例
- 使用装饰器@allure.description_html，传递一段HTML文本，这将在测试报告的"Description"部分渲染出来
- 直接在测试用例方法中通过编写文档注释的方式来添加描述



我一般使用第三种，直接将Testlink上用例标题放在这里，即有title的效果，又有description效果。如果使用，具体看个人需要（如下所示）。



```
    @allure.severity('RAT')
    @allure.link(testlink_url+'?tprojectPrefix='+testlink_prefix+'&item=testcase&id='+testlink_prefix+'-432')
    def test_432_create_nfs_folder_mode_async(self):
        """  Sc-432:Create NFS share folder, mode is async  """
        folder_name = 'pytest-' + rand_low_ascii(6)
        self.create_share_folder(folder_name, nfs='true', mode='async')
        self.delete_folder(folder_name)
        self.mds_mgr.check_cluster_state()
```





#### 示例



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

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



<img class="shadow" src="/img/in-post/allure/description_provide_string.png" width="1200">

上面的测试报告是通过装饰器@allure.description传递字符串参数来添加描述语的方式。




<img class="shadow" src="/img/in-post/allure/description_docstring.png" width="1200">

上面的测试报告是通过直接在测试用例方法中编写文档注释来添加描述语的方式。





<img class="shadow" src="/img/in-post/allure/description_privide_html.png" width="1200">

上面的测试报告是通过装饰器@allure.description_html传递一段HTML文本来添加描述语的方式，这段HTML会渲染在报告的"Description"部分。





#### allure动态更新描述语(allure.dynamic.description)



```
@allure.description("这是更新前的描述内容，在使用allure.dynamic.description后将会被更新成新的描述内容")
def test_dynamic_description():
    assert True
    allure.dynamic.description("这是通过使用allure.dynamic.description更新后的描述内容")
```



allure html展示效果如下：



<img class="shadow" src="/img/in-post/allure/dynamic_description.png" width="1200">

如果assert失败或用例执行失败，是不会动态更新描述信息的：



<img class="shadow" src="/img/in-post/allure/dynamic_description_failed.png" width="1200">





### allure为测试用例添加标题



通过使用装饰器@allure.title可以为测试用例自定义一个更具有阅读性的易读的标题。



#### allure.title的三种使用方式

- 直接使用@allure.title为测试用例自定义标题
- @allure.title支持通过占位符的方式传递参数，可以实现测试用例标题参数化，动态生成测试用例标题
- @allure.dynamic.title动态更新测试用例标题



#### allure.title使用方式示例



##### 直接使用@allure.title为测试用例自定义标题



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

import pytest
import allure


@allure.title("自定义测试用例标题")
def test_case_with_title():
    assert True
```



这个最常用，也是最简单的方式。效果图如下：



<img class="shadow" src="/img/in-post/allure/step_title.png" width="1200">



##### allure.title占位符传递参数，参数化测试用例标题



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

import pytest
import allure


@allure.title("参数化测试用例标题：参数1 = {param1} and 参数2 = {param2}")
@pytest.mark.parametrize("param1, param2, expected", [(1, 1, 2), (1, 3, 5)])
def test_with_parametrize_title(param1, param2, expected):
    assert param1 + param2 == expected
```



展示效果如下：



<img class="shadow" src="/img/in-post/allure/step_title_parameter.png" width="1200">


##### allure.dynamic.title动态更新标题



```
@allure.title("这个标题将会被成功执行的测试用例中的标题替所代替")
def test_with_dynamic_title():
    assert True
    allure.dynamic.title("断言成功后，标题将会被替换成这个标题")
```



效果图如下：



<img class="shadow" src="/img/in-post/allure/step_dynamic_title.png" width="1200">




#### allure集成缺陷管理系统和测试管理系统(allure.link、allure.issue、allure.testcase)



allure测试报告框架提供了@allure.link、@allure.issue、@allure.testcase 这三个装饰器，可以用来与缺陷管理系统和测试管理系统集成，做到更好的自动化管理。

这三个装饰器，使用方法基本一致，但仍然不建议混用，用例相关用@allure.testcase，Bug相关用@allure.issue，其他则使用@allure.link，形成习惯。



代码示例：



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

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



<img class="shadow" src="/img/in-post/allure/allure_link.png" width="1200">

上图是allure.link的效果。



<img class="shadow" src="/img/in-post/allure/allure_issue.png" width="1200">



上图是allure.issue的效果，用于提示是一个Bug。



<img class="shadow" src="/img/in-post/allure/allure_testcase.png" width="1200">



上图显示allure.testcase的链接，会有一个类似存储的icon。

这几个装饰器的相同点都显示在“Links”下方展示，除了allure.link没有图标外，其他两个都有图标。





#### allure的Tag标记(allure.story、allure.feature、severity)



执行测试用例时，希望能够更加灵活的指定执行某些测试用例（如指定测试用例的级别，用例路径，用例标签/标记等），pytest支持我们通过使用marker装饰器@pytest.mark来实现这个需求，而allure也同样提供了三种类似的方法来实现这个需求。



##### allure的三种方式



Allure 则提供了 3 种类型的标记装饰器来标记测试，并且可以同步展示到测试报告内：

* BDD（行为驱动开发）风格的标签
* 严重程度（Severity）的标签
* 自定义的标签（allure.title）


​        

##### BDD风格的标签



    @allure.epic：敏捷里面的概念，定义史诗，相当于module级的标签
    @allure.feature：功能点的描述，可以理解成模块，相当于class级的标签
    @allure.story：故事，可以理解为场景，相当于method级的标签



allure提供的两个装饰器：@allure.feature和@allure.story，可以将用例根据Feature和Story分类，通过将name使用epic_ 开头的前缀就能够指定Feature和Story属于哪一个epic。

他俩的关系：

epic是feature父级，feature是story父级，是包含关系，效果跟书籍的目录或者项目结构相似。

如果使用allure和pytest来组织的自动化框架，**推荐使用allure的标记来标记用例，替换@pytest.mark.xxx**，因为功能一致，且allure 标记功能可以直接**展示到html报告**内



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

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



**拓展：命令行方式**



与@pytest.mark.xxx相同，也可以通过命令行来运行指定epic、feature、story标记的用例：

    –allure-epics
    –allure-features
    –allure-stories



**只运行 epic 名为 epic1 的测试用例**



``` pytest --alluredir ./report/allure --allure-epics=epic1 ```



**只运行 feature 名为 模块级 的测试用例**



``` pytest --alluredir ./report/allure --allure-features=模块级 ```



**只运行 story1、story2 的测试用例（也可以不用=号 空格即可）**



``` pytest tests.py --allure-stories story1,story2```



**指定 feature和story**



``` pytest tests.py --allure-features feature1,feature2 --allure-stories story1 ```





##### Severity markers



使用@allure.severity来标识测试用例的严重等级，严重等级是allure.severity_level枚举中的一个。



allure划分用例等级为5个：

- blocker：阻塞缺陷（功能未实现，无法下一步）
- critical：严重缺陷（功能点缺失）
- normal：一般缺陷（边界情况，格式错误）
- minor：次要缺陷（界面错误与ui需求不符）
- trivial：轻微缺陷（必须项无提示，或者提示不规范）



**说明：**

​    一些手工用例编写平台，如testlink，它里面定义的测试用例的级别名称，和allure指定的这五种名称是不一样的，是无法直接使用外部的用例级别的，只能使用上面的测试用例的级别。



示例：



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

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



<img class="shadow" src="/img/in-post/allure/allure_level.png" width="1200">




## 综合示例



从网上找了个示例(https://zhuanlan.zhihu.com/p/652835522)，做参考一下：



```
#!/usr/bin/env python
# -*- coding:GB2312 -*-

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
    @allure.link('百度一下，你就知道', LinkType.ISSUE, '我是link_ISSUE')
    @allure.label('我是label')
    @allure.issue('百度一下，你就知道', '我是issue')
    @allure.description('我是description')
    @allure.severity(Severity.BLOCKER)
    @allure.tag('我是tag')
    @allure.testcase('百度一下，你就知道', 'testcase')
    def test_01(self):
        self.assert_one(1, 1)

    @allure.step('我是断言')
    def assert_one(self, a, b):
        assert a == b

    @allure.id('我是id')
    @allure.title('我是title')
    @allure.link('百度一下，你就知道', LinkType.LINK, '我是link')
    @allure.label('我是label')
    @allure.issue('百度一下，你就知道', '我是issue')
    @allure.description('我是description')
    @allure.severity('我是severity')
    @allure.tag('我是tag')
    @allure.testcase('百度一下，你就知道', '我是testcase')
    def test_02(self):
        allure.dynamic.mro()
        allure.dynamic.title('我是修改后的title')
        allure.dynamic.link('百度一下，你就知道', LinkType.LINK, '我是修改后的link')
        allure.dynamic.label('我是修改后的label')
        allure.dynamic.issue('百度一下，你就知道', '我是修改后的issue')
        allure.dynamic.description('我是修改后的description')
        allure.dynamic.severity('我是修改后的severity')
        allure.dynamic.tag('我是修改后的tag')
        allure.dynamic.testcase('百度一下，你就知道', '我是修改后的testcase')
        assert 1 > 1
```



allure html report 显示效果如下：



<img class="shadow" src="/img/in-post/allure/allure_full_example.png" width="1200">




# 帮助 --help



| 命令         | 描述                                 |
| ------------ | ------------------------------------ |
| generate     | 根据给定的allure结果目录生成报告     |
| serve        | 启动报告，可在浏览器中查看生成的报告 |
| open         | 打开生成的报告，默认使用浏览器       |
| plugin       | 生成插件报告                         |
| --help       | 打印命令行的帮助信息                 |
| -q,--quite   | 开启静默模式，减少信息的输出         |
| -v,--verbose | 开启详细模式，增加输出信息           |
| --version    | 显示当前allure的版本信息             |



详细帮助参考下图：



<img class="shadow" src="/img/in-post/allure/allure_help.png" width="1200">





## 报告打开



### 系统默认目录下生成测试报告并打开



```
allure serve path
```



示例如下：



```
C:\Users\Wang>allure serve report/json -o report/html
Generating report to temp directory...
-o does not exists
report\html does not exists
Report successfully generated to C:\Users\Wang\AppData\Local\Temp\8019254791336321592\allure-report
Starting web server...
2021-11-04 11:13:00.556:INFO::main: Logging initialized @1698ms to org.eclipse.jetty.util.log.StdErrLog
Server started at <http://192.168.2.178:2970/>. Press <Ctrl+C> to exit
^C终止批处理操作吗(Y/N)? y
```





### 在指定目录下生成测试报告，使用open打开



```
allure generate “存储结果的path” -c -o  “在path生成html报告”
allure open “在path生成的html报告”
```



示例如下：



```
C:\Users\Wang>allure generate report/json -o report/html
Report successfully generated to report\html
C:\Users\Wang>allure open report\html
Starting web server...
2021-11-04 11:17:37.560:INFO::main: Logging initialized @160ms to org.eclipse.jetty.util.log.StdErrLog
Server started at <http://192.168.2.178:2999/>. Press <Ctrl+C> to exit
```





## Environment



环境变量参数，设置运行环境参数，比如可以显示被测版本信息，什么时间开始测试，什么时间测试结束，耗时多久之类的信息。默认为空，需要创建environment.properties文件，或者environment.xml文件，并把文件存放`存储结果的path`中。



<img class="shadow" src="/img/in-post/allure/environment_empty.png" width="1200">




### environment.properties



```
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



### environment.xml



```
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



## Categories



将测试用例结果进行分类,默认情况下，有两类缺陷：

1. Product defects 产品缺陷（测试结果：failed）
2. Test defects 测试缺陷（测试结果：error/broken）



可以创建自定义缺陷分类的，将 categories.json 文件添加到allure-results目录即可（和上面environment.properties放同一个目录），示例参考如下：



```
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



<img class="shadow" src="/img/in-post/allure/environment_OK.png" width="1200">




# 结语



## 设置测试套中显示内容




@allure.parent_suite,@allure.suite,@allure.sub_suite对应的是allure报告中的测试套的三个级别.爷爷父亲儿子.然后下一级就是测用例的标题。

由于@allure.epic, @allure.feature, @allure.story,@allure.title的存在，上面这三个装饰器很少使用。




## 设置报告中功能项显示内容




@allure.epic, @allure.feature, @allure.story,@allure.title对应功能中的一级菜单,二级菜单,三级菜单,用例标题




## 设置具体用例显示内容




@allure.id 用例id,@allure.link 用例的超链接,@allure.label 用例的标签
@allure.issue 记录用例的问题(超链接),@allure.description 用例的描述
@allure.severity 用例的优先级,@allure.tag 用例的标记,@allure.testcase 记录用例的地址(超链接)
@allure.description_html 用例的描述的网址(超链接),若存在description_html则@allure.description不显示





## 设置用例级别



@allure.severity的参数说明，'blocker'、 'critical'、'normal'、'minor'、'trivial'，从左到右言级别依次降低






# 参考链接



https://github.com/allure-framework

https://qualitysphere.gitee.io/ext/allure/

https://github.com/orgs/allure-framework/discussions


