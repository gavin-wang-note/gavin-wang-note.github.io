---
layout:     post
title:      "获取Apache请求处理时间"
subtitle:   "Get elapsed time for Apache"
date:       2016-06-01
author:     "Gavin"
catalog:    true
tags:
    - Apache
---

# 引言

客户经常指责我们某些CGI请求处理的时间过长，我们需要一种快速的方法获取apache 对每一个请求处理的时间。事实上apache 可以打印出每一个请求的处理时间。

# 解决方法

/etc/apache2/apache2.conf中，在

```LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined ```

在这一行中增加 ``` %T.%D ``` 就可以打印每一个请求的处理时间。

修改后，conf 内容如下：

```
LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
LogFormat "%h %l %u %t \"%r\" %>s %O %T.%D \"%{Referer}i\" \"%{User-Agent}i\"" combined
LogFormat "%h %l %u %t \"%r\" %>s %O" common
LogFormat "%{Referer}i -> %U" referer
LogFormat "%{User-agent}i" agent
```

看下//var/log/apache2/access.log中的输出：

```
 10.16.17.43 - - [01/Jun/2016:13:41:51 +0800] "GET /cgi-bin/ezs3/json/list_shared_folder?gateway_group=virStorage&_=1464745951979 HTTP/1.1" 200 1322 0.932141 "https://10.16.17.11:8080/" "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"
```

# 其他

其他相关的参数和含义如下,可以前往 https://httpd.apache.org/docs/2.2/mod/modlogconfig.html 去学习。

