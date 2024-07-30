---
layout:     post
title:      "unittest,pytest,nose,robot framework简介"
subtitle:   "unittest,pytest,nose,robot framework summary"
date:       2020-02-06
author:     "Gavin Wang"
catalog:    true
categories:
    - [Automation]
tags:
    - Automation
---

# unittest,pytest,nose,robot framework简介

unittest: Python自带，最基础的单元测试框架

nose: 基于unittest开发，易用性好，有许多插件

pytest: 同样基于unittest开发，易用性好，信息更详细，插件众多

robot framework：一款基于Python语言的关键字驱动测试框架，有界面，功能完善，自带报告及log清晰美观

# 对比

| 项目             | unittest                                                 | nose                                                         | pytest                                                       | robot framework                                              |
| ---------------- | -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 用例编写         | 继承unittest.TestCase类需要组织各种testSuite断言种类繁多 | test开头的方法即可                                           | test开头的方法即可                                           | robot格式，文本文件                                          |
| 执行器           | 自己写run_all_tests+discover+CommandParser+...           | nosetests ...                                                | py.test ...                                                  | pybot ...                                                    |
| 用例发现Discover | 支持                                                     | 支持                                                         | 支持                                                         | 支持                                                         |
| 跳过用例         | unittest.skip()unittest.skipIf()raise uniitest.SkipTest  | from nose.plugins.skip import SkipTestraise SkipTest         | @pytest.mark.skipif( condition)@pytest.mark.xfail            | -                                                            |
| Fixtures         | setUp/tearDown@classmethodsetUpClass...                  | 支持                                                         | @pytest.fixture(session="session", autouse=True)fixture的作用域：function、module、session ，autouse=True使得函数将默认执行 | [Setup] ...[Teardown] ...                                    |
| 用例标签tags     | 借助unittest.skip()+comandParser实现                     | attrib标签from nose.plugins.attrib import attr@attr(speed='slow')def test_big_download(): pass$ nosetests -a speed=slow | @pytest.mark.webtest自定义一个mark，如下，然后 py.test -v -m webtest 只运行标记了webtest的函数， py.test -v -m "not webtest" 来运行未标记webtest的 | [Tags] test level1pybot -i/--include tagName C:\TF-Testpybot -e/--exculde level1 *.robot排除 |
| 超时机制Timeout  | 自己实现                                                 | from nose.tools import timedimport time@timed(1)def test_lean_5():time.sleep(2)pass | pip install pytest-timeout@pytest.mark.timeout(60)或 pytest --timeout=300 | [Timeout] 3 seconds                                          |
| 参数化           | 结合ddt使用                                              | 结合ddt使用                                                  | @pytest.mark.parametrize("a,b,expected", testdata)def test_timedistance_v0(a, b, expected):diff = a - bassert diff == expected | [Template] 1 2 3                                             |
| 报告             | HTMLTestRunner                                           | pip install nose-htmloutput--with-html --html-file=          | pip install -U pytest-htmlpy.test --html=./report.html       | 支持，默认自动生成                                           |
|日志log |自己实现 |--nologcapture 不使用log--logging-format=FORMAT使用自定义的格式显示日志--logging-datefmt=FORMAT 和上面类类似，多了日期格式--logging-filter=FILTER日志过滤，一般很少用，可以不关注--logging-clear-handlers 也可以不关注--logging-level=DEFAULT log的等级定义 |pytest test_add.py --resultlog=./log.txtpytest test_add.py --pastebin=all |支持，默认自动生成|
|只列出用例collect-only | 无 |nosetests --collect-only/nosetests -v --with-id |--collect-only -v | -|
|失败用例重跑rerun failures |无 |nosetests -v --failed |pip install -U pytest-rerunfailures@pytest.mark.flaky(reruns=5)py.test --rerun=3 |robot --rerunfailed|
|baseline对比 |无 |无 |无 |无|
|并发 |改造unittest使用协程并发，或使用线程池+Beautiful Report |命令行并发 |pytest-xdist：分发到不用的cpu或机器上 |命令行并发|
|xml报告 |无 |--with-xunit | --xunit-file=... /pytest+Allure |--junit-xml=|
|Selenium支持 |无 |无 |pytest-selenium |robotframework-seleniumlibraryrobotframwork-selenium2library|

# 总结

总体来说，unittest比较基础，二次开发方便，适合高手使用；pytest/nose更加方便快捷，效率更高，适合小白及追求效率的公司；robot framework由于有界面及美观的报告，易用性更好，灵活性及可定制性略差。



