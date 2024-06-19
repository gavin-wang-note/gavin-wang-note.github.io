---
title: Change theme from Jekyll to Hexo Matery
date: 2024-01-28 22:25:29
author: Gavin Wang
img: 
top: false
hide: false
cover: false
coverImg: 
password: 
toc: true
mathjax: false
summary: Blog从Jekyll切换到Hexo Matery主题 
categories: Markdown
tags:
  - Markdown
---

# 概述

之前的博客使用的是Jekyll，比较简约，今天看到一个蛮炫酷的主题，故而使用它，重新搭建了一下博客，并迁移了旧有博客中的文章内容(少部分博客地址发生了变化，导致相关文章的历史访问记录诸如访问量会从零开始计)。

# 过程

简单记录几个重要的点，防止自己以后忘记。 


## 去掉主页图片浮层

修改 `themes/hexo-theme-matery/source/css`下`matery.css`文件

```shell
.bg-cover:after {
    position: absolute;
    z-index: 1;
    width: 100%;
    height: 100%;
    display: block;
    left: 0;
    top: 0;
    /* content: ""; */
}
```

注释掉上面的`content: "";`内容即可。


## 去掉主页subtitle字样


修改 `themes/hexo-theme-matery/layout/_partial/bg-cover-content.ejs`中的如下内容：

```shell
            <div class="title center-align">
                <% if (config.subtitle && config.subtitle.length > 0) { %>
                <%= config.subtitle %>
                <% } else { %>
                    subtitle
                <% } %>
            </div>
```

修改为：

```shell
            <div class="title center-align">
                <% if (config.subtitle && config.subtitle.length > 0) { %>
                <%= config.subtitle %>
                <% } %>
            </div>
```


## 代码高亮

```shell
# syntax_highlighter: highlight.js
syntax_highlighter: 
highlight:
  line_number: false
  auto_detect: true
  tab_replace: ''
  wrap: true
  hljs: false
prismjs:
  enable: true
  preprocess: true
  line_number: false
  tab_replace: ''
  theme: 'okaidia'
marked:
  langPrefix: line-numbers language-
```

`syntax_highlighter:`为空，则表示禁用默认自带的`highlighter`代码高亮风格。如上为改用`prismjs`风格。


## 分类

页面想显示分类，有的时候还有子分类，参考如下：

并列分类：

```shell
categories:
- [Linux]
- [Tools]
```


并列+子分类：

```shell
categories:
- [Linux, Hexo]
- [Tools, PHP]
```



## 修改留言板页面展示内容

在`themes/hexo-theme-matery/layout/`，修改`contact.ejs`文件：

```shell
            <!--valine评论弹幕-->
            <% if (theme.valine && theme.valine.enable) { %>
                <p>
                    <b>畅所欲言</b><br>
                    <b>在这里可以留下你的足迹，欢迎在下方留言，欢迎交换友链</b><br>
                    <b>友链信息</b><br>
                    <b>博客名称: <%- config.title %></b><br>
                    <b>博客网址: <%- config.url %></b><br>
                    <b>博客头像: <%- config.url %>/medias/logo.png</b><br>
                    <b>博客介绍: 犹豫就会败北</b><br>
                </p>
                <div class="container">
                    <section id="custom" class="bb-section">
                        <div class="row">
                            <div class="col-md-5">
                                <form class="form-inline">
                                    <div class="form-group">
                                        文字：<input class="form-control" name="info" type="text" placeholder="hello, world"/>
                                    </div>
                                    <div class="form-group">
                                        链接：<input class="form-control" name="href" type="text" placeholder="https://github.com/blinkfox/hexo-theme-matery"/>
                                    </div>
                                    <div class="form-group">
                                        速度：<input  class="form-control"  name="speed" type="text" placeholder="5~20" value="16" />
                                    </div>
                                </form>
                                <div class="form-group">
                                    <button id="send"  class="btn" onclick="run()">留言</button>
                                    <button id="clear" class="btn " onclick="clear_barrage()"> 清除</button>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
```
调整为：

```shell
            <!--valine评论弹幕-->
            <% if (theme.valine && theme.valine.enable) { %>
                <p>
                    <b>在这里可以留下你的足迹，欢迎在下方留言</b><br>
                </p>
                <div class="container">
                    <section id="custom" class="bb-section">
                        <div class="row">
                            <div class="col-md-5">
                                <form class="form-inline">
                                    <div class="form-group">
                                        文字：<input class="form-control" name="info" type="text" placeholder="hello, world"/>
                                    </div>
                                    <div class="form-group">
                                        链接：<input class="form-control" name="href" type="text" placeholder="https://github.com/gavin-wang-note"/>
                                    </div>
                                    <div class="form-group">
                                        速度：<input  class="form-control"  name="speed" type="text" placeholder="5~20" value="16" />
                                    </div>
                                </form>
                                <div class="form-group">
                                    <button id="send"  class="btn" onclick="run()">留言</button>
                                    <button id="clear" class="btn " onclick="clear_barrage()"> 清除</button>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
```
改为你自己认为合适的内容即可。


## 打赏

替换掉`themes/hexo-theme-matery/source/medias/reward`目录下两个文件即可:

```shell
drwxr-xr-x 2 root root  4096 Jan 26 19:25 ./
drwxr-xr-x 7 root root  4096 Jan 26 19:35 ../
-rw-r--r-- 1 root root 57240 Jan 26 19:36 alipay.jpg
-rw-r--r-- 1 root root 34017 Jan 26 19:36 wechat.png
```

## 文章Front Format

修改`scaffolds/post.md`文件，添加如下内容：

```shell
---
title: {{ title }}
date: {{ date }}
author: 
img: 
coverImg: 
top: false 
cover: false 
toc: true 
mathjax: false
password: 
summary: 
keywords: 
tags: 
categories:
---
```

介绍如下：

| Options            | Defaults                 | Description（描述）                                          |
| ------------------ | ------------------------ | ------------------------------------------------------------ |
| title              | Markdown 的文件标题      | 文章标题,强烈建议填写此选项                                  |
| date（日期）       | 文件创建时的日期时间     | 发布时间,强烈建议填写这个选项,这是最好的,以确保它是全局唯一的 |
| author（作者）     |`_config.yml` 中的 author | 文章作者                                                     |
| img                | 文章封面 | 特征图像,用于显示在文章封面，如果不携带，系统自动从`themes/matery/source/medias/featureimages`中选取 |
| top                | true                     | 置顶文章(文章是否置顶),如果设置为True，它将被推荐作为在主页顶部。 |
| hide               | false                    | 这篇文章是否显示在首页,如果 隐藏 值是 True ,它将不会显示在首页，即被隐藏。 |
| cover（封面）      | false                    | v1.0.2版本新增，表示该文章是否需要加入到首页轮播封面中|
| coverImg           | null                     | v1.0.2版本新增，表示该文章在首页轮播封面需要显示的图片路径，如果没有，则默认使用文章的特色图片 |
| password           | null                     | 文章阅读密码，如果要对文章设置阅读验证密码的话，就可以设置 password 的值，该值必须是用 SHA256 加密后的密码，防止被他人识破。前提是在主题的 config.yml 中激活了 verifyPassword 选项 |
| toc                | true                     | 是否打开目录,你可以关掉一篇文章的TOC。 启用的前提是主题的 `_config.yml` 中 `toc` 是激活的（设置为True）|
| mathjax            | false                    | 是否启用数学公式支持,是否这篇文章开启 mathjax ,你需要打开它的主题 `_config.yml` 文件中相关配置。 |
| summary（总结）    | null                     | 文章摘要,自定义文章摘要内容,如果属性有一个值,明信片摘要将显示你设置的文本,否则程序会自动拦截部分文章的内容作为总结。 |
| categories（类别） | null                     | 文章分类,分类的主题代表一个大分类。 |
| tags（标签）       | null                     | 文章标签,可以有多个标签                                      |
| keywords（关键字） | Post Title               | 文章关键字和搜索引擎优化                                     |
| reprintPolicy      | cc_by                    | 文章分享政策,值可能是cc_by,cc_by_nd, cc_by_sa, cc_by_nc, cc_by_nc_nd cc_by_nc_sa, cc0中的一个。 |


## 文章加密

借助`hexo-blog-encrypt`完成文章的加密工作，需要安装:
`npm install hexo-blog-encrypt`

同时，需要在博客的根目录下的`_config.yml`文件中，增加如下内容：

```shell
# Security
encrypt: # hexo-blog-encrypt
  silent: false
  abstract: 这里有东西被加密了，需要输入密码才能查看哦。
  message: 您好, 这里需要输入密码，解密后方可查看内容。
  tags:
  - {name: tagName, password: 密码A}
  - {name: tagName, password: 密码B}
  theme: flip
  wrong_pass_message: 抱歉，密码错误！
  wrong_hash_message: 抱歉, 这个文章不能被校验, 不过你还是能看看解密后的内容。
```

`theme`有如下几种风格可选择:

```shell
default
blink
shrink
flip
up
surge
wave
xray
```

根据个人喜好选择即可，具体信息，请参考[官网](https://www.npmjs.com/package/hexo-blog-encrypt)。

> **请留意：**


主题中的`_config.yml`文件，需关闭如下选项：

```shell
verifyPassword:
  enable: false
```

文章中，需增加如下内容：

```shell
password: 123456
theme: flip
```

这里`theme`中的`flip`，需要和上文中根目录下的`_config.yml`中`theme`的值保持一致。

由于本地访问是http方式，推到github上是https方式访问，故而本地http访问时输入密码无任何反应，这是正常现象，推到github上时OK的。



## markdown的支持

主要做了如下安装动作：

```shell
npm un hexo-renderer-marked --save
npm i hexo-renderer-markdown-it --save
npm i markdown-it-footnote --save
npm i markdown-it-footnote --save
npm i markdown-it-footnote --save
npm i markdown-it-named-headings --save
npm i markdown-it-checkbox --save
npm i markdown-it-sub markdown-it-sup --save
npm i markdown-it-imsize --save
npm i markdown-it-mark --save
npm i markdown-it-ins --save
npm i markdown-it-abbr --save
npm i markdown-it-deflist --save
npm i markdown-it-expandable --save
```

请务必执行`npm list`命令检查是否安装成功，如下则表示安装成功：

```shell
hexo-site@0.0.0 /root/gavin-wang-note.github.io
├── browser-sync@3.0.2
├── hexo-blog-encrypt@3.1.9
├── hexo-browsersync@0.3.0
├── hexo-deployer-git@4.0.0
├── hexo-filter-github-emojis@3.0.5
├── hexo-generator-archive@2.0.0
├── hexo-generator-category@2.0.0
├── hexo-generator-feed@3.0.0
├── hexo-generator-index@3.0.0
├── hexo-generator-searchdb@1.4.1
├── hexo-generator-sitemap@3.0.1
├── hexo-generator-tag@2.0.0
├── hexo-permalink-pinyin@1.1.0
├── hexo-renderer-ejs@2.0.0
├── hexo-renderer-markdown-it@7.1.1
├── hexo-renderer-pug@3.0.0
├── hexo-renderer-stylus@3.0.1
├── hexo-server@3.0.0
├── hexo-theme-landscape@1.0.0
├── hexo-wordcount@6.0.1
├── hexo@7.1.1
├── markdown-it-abbr@2.0.0
├── markdown-it-checkbox@1.1.0
├── markdown-it-deflist@3.0.0
├── markdown-it-expandable@1.0.2
├── markdown-it-footnote@4.0.0
├── markdown-it-imsize@2.0.1
├── markdown-it-ins@4.0.0
├── markdown-it-mark@4.0.0
├── markdown-it-named-headings@1.1.0
├── markdown-it-sub@2.0.0
└── markdown-it-sup@2.0.0
```

更多信息，我参考的是这篇文章[点击跳转](https://seayj.cn/articles/33818/#!)。


## 图片增加加载过程

我参考的是这篇文章[点击跳转](https://lovelijunyi.gitee.io/posts/b8ec.html)中的`增加载入动画`章节内容。


## 调整页面分页

修改`{主题}layout/_partial/paging.ejs`文件内容，注释掉旧有的

```ejs
<div class="center-align b-text-gray"><%- page.current %> / <%- page.total %></div>
```

添加如下内容：

```ejs
        <div class="page-info col m4 l4 hide-on-small-only">

        <!-- Modify by Gavin, 2024-02-01
            <div class="center-align b-text-gray"><%- page.current %> / <%- page.total %></div>
        -->

        <!-- Add new content like the fallowing  -->
        <div class="center-align b-text-gray">
            <a href="/">«1</a>

            <% const displayPageNumber = 9; %>
            <% const middle = Math.floor(displayPageNumber / 2); %>
            <% const startPage = Math.max(2, page.current - middle + 1); %>
            <% const endPage = Math.min(page.total-1, startPage + displayPageNumber - 2); %>

            <% if (startPage > 2) { %>
                <span>...</span>
            <% } %>

            <% for(var i = startPage; i <= endPage; i++) { %>
                <% if (page.current == i) { %>
                    <span><%= i %></span>
                <% } else { %>
                    <a href="/page/<%= i %>"><%= i %></a>
                <% } %>
            <% } %>

            <% if (endPage < page.total - 1) { %>
                <span>...</span>
            <% } %>

            <a href="/page/<%= page.total %>"><%= page.total %>»</a>
        </div>
```

展示效果如下：

<img class="shadow" src="/img/in-post/pagination.png" width="1200">



## 兼容Jekyll URL

由于我是从Jekyll切换到Hexo的，Jekyll文件的命名格式是：`2021-05-05-abc_def_ghi.md`，切换到hexo后，文章链接展示为`https://xxx/2021/02/05/2021-05-05-abc-def-ghi`， 而Jekyll中文章链接展示的链接为`https://xxx/2021/02/05/abc_def_ghi`。
为了保证旧文章链接的有效性，需要修改Hexo文章展示的URL。

先修改博客根目录下的`_config.yml`文件：

```shell
permalink_pinyin:
  enable: true
  separator: '_' # default: '-'
```

将上面的`separator`使用中划线修改为下划线。


接着在博客根目录下的scrpits创建refinepermalink.js文件，写入如下内容：

```shell
hexo.extend.filter.register('before_post_render', function(data){
	  // 检查日期，如果早于new_format_date，则不做改变
	  var new_format_date = new Date('2000-05-01');
	  if (new Date(data.date) < new_format_date) return data;

	  // 对于日期晚于new_format_date的文章，尝试解析出纯标题部分作为slug
	  var matched = data.source.match(/(\d{4}-\d{2}-\d{2})-(.*)\.md$/);
	  if(matched && matched[2]) {
		      // 重写slug
		      // data.slug = matched[2].replace(/-/g, '_');
		      data.slug = matched[2];
		    }

	  return data;
});
```


重启hexo(hexo clean; hexo g; hexo s)，即可生效。


## top文章按时间倒序排序

目前置顶的文章，是安装时间先后顺序排序的，现在想按时间倒序排序。


找到主题目录下`layout/_widget/recommend.ejs`文件，增加三行代码。

修改前：

```javascript
<%
    // get all top posts.
    var topPosts = [];
    if (theme.recommend.useConfig) {
        topPosts = site.data.recommends;
    } else {
        site.posts.forEach(function (post) {
            if (post.top) {
                topPosts.push(post);
            }
        });
    }

    var topPostsCount = topPosts.length;
%>
```


修改后:

```javaseript
<%
    // get all top posts.
    var topPosts = [];
    if (theme.recommend.useConfig) {
        topPosts = site.data.recommends;
    } else {
        site.posts.forEach(function (post) {
            if (post.top) {
                topPosts.push(post);
            }
        });
    }

    // 对置顶文章按日期进行倒序排序
    topPosts.sort(function(a, b) {
        return b.date - a.date;
    });

    var topPostsCount = topPosts.length;
%>
```

然后重启hexo即可。


## 修改 “关于” 页面的 “其他技能” 标签底色

在“分类” 和 “标签”页面，所有的Tag都是有底色的，但是“关于”页面中的“其他技能”却没有底色（都是白色）。

这里修改一下，使用的底色保持和“分类” 和 “标签”页面一致。

找到`themes/matery/layout/_widget\my-skills.ejs`文件，在文件内容的开头处，增加如下内容：

```javascript
    <div class="title center-align" data-aos="zoom-in-up">
<%
var colorArray = ['#F9EBEA', '#F5EEF8', '#D5F5E3', '#E8F8F5', '#FEF9E7', '#F8F9F9', '#82E0AA', '#D7BDE2', '#A3E4D7', '#85C1E9', '#F8C471', '#F9E79F', '#FFF'];
var getColor = function() {
    return colorArray[Math.floor(Math.random() * colorArray.length)];
}
%>
```

再找到这行内容：`<% if (site.tags) { %>`，删除这行下的如下内容：

```javascript
    <div class="other-skills chip-container" data-aos="zoom-in-up">
        <div class="sub-title center-align"><i class="fa fa-book"></i>&nbsp;&nbsp;<%- __('otherSkills') %></div>
        <div class="tag-chips center-align">
            <% site.tags.map(function(tag) { %>
            <% if (!isInArray(topSkillArr, tag.name)) { %>
            <a href="<%- url_for(tag.path) %>">
                <span class="chip center-align waves-effect waves-light chip-default"><%- tag.name %></span>
            </a>
            <% } %>
            <% }); %>
        </div>
    </div>
```

增加如下内容：

```javascript
    <div class="other-skills chip-container" data-aos="zoom-in-up">
        <div class="sub-title center-align"><i class="fa fa-book"></i>&nbsp;&nbsp;<%- __('otherSkills') %></div>
        <div class="tag-chips center-align">
            <% site.tags.each(function(tag, index) { %>
            <% if (!isInArray(topSkillArr, tag.name)) { %>
            <a href="<%- url_for(tag.path) %>">
                <span class="chip center-align waves-effect waves-light chip-default" style="background-color: <%- getColor(index) %>"><%- tag.name %></span>
            </a>
            <% } %>
            <% }); %>
        </div>
    </div>
```


然后访问下对应页面，即可看到效果。


## 增加文章统计

在`Hexo`家目录下（如：`~/gavin-wang-note.github.io/`），执行如下命令创建统计页：

```shell
hexo new page stat
```

然后在文件内容的双线内添加：

```shell
type: stat
layout: stat
```

在主题目录的`layout/`文件夹下新建`stat.ejs`模板文件，然后用`vim`也好，用其他工具也好，写入以下内容：

```ejs
<style type="text/css">
    /* don't remove. */
    .about-cover {
        height: 75vh;
    }
</style>

<%- partial('_partial/bg-cover') %>

<main class="content">
    <div class="container chip-container">
        <div class="card">
            <div class="card-content">
                <div class="tag-title center-align">
                    <i class="<%= theme.stat.icon %>"></i>&nbsp;&nbsp;<%= theme.stat.title %>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-content">
                <% if (theme.stat.text) { %>
                <style>
                    #stat-text {
                        -webkit-text-size-adjust: 100%;
                        line-height: 1.5;
                        font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
                        font-weight: normal;
                        --fa-font-brands: normal 400 1em/1 "Font Awesome 6 Brands";
                        --fa-font-regular: normal 400 1em/1 "Font Awesome 6 Free";
                        --fa-font-solid: normal 900 1em/1 "Font Awesome 6 Free";
                        color: 
#34495e;
                        text-align: center;
                        float: left;
                        box-sizing: border-box;
                        padding: 0 .75rem;
                        min-height: 1px;
                        opacity: .6;
                        font-size: 1.1rem;
                        width: 83.3333333333%;
                        left: auto;
                        right: auto;
                        margin-left: 8.3333333333%;
                    }
                </style>
                <div id="stat-text">
                    <div class="row">
                        <div class="col l8 offset-l2 m10 offset-m1 s10 offset-s1 center-align text">
                            <%= theme.stat.text %>
                        </div>
                    </div>
                </div>
                <br>
                <hr>
                <% } %>

                <%- page.content %>

                <% if (theme.stat.show_post) { %>
                <h1 id="<%= theme.stat.title %>"><a href="#<%= theme.stat.title %>" class="headerlink" title="<%= theme.stat.title %>"></a><%= theme.stat.title %></h1>
                <%
                    var article_posts = [];
                    site.posts.forEach(post => {
                        article_posts.push(post);
                    });
                    
                    for (var i = 0; i < article_posts.length - 1; i++) {
                        for (var j = 1; j < article_posts.length - i; j++) {
                            if (article_posts[j].date > article_posts[j-1].date) {
                                var tmp = article_posts[j];
                                article_posts[j] = article_posts[j-1];
                                article_posts[j-1] = tmp;
                            }
                        }
                    }
                    
                    var post_date_index = null;
                    article_posts.forEach(post => {
                        pwd = post.password;
                        if ((!(pwd && pwd.length > 0))&&(post.hide != true)) {
                            if (date(post.date, 'YYYY-MM') != post_date_index) {
                                post_date_index = date(post.date, 'YYYY-MM');
                %>

                <h2 id="<%= post_date_index %>"><a href="#<%= post_date_index %>" class="headerlink" title="<%= post_date_index %>"></a><%= post_date_index %></h2>
                            <% } %>
                <p>
                    <code><%= date(post.date, 'YYYY-MM-DD') %></code>&ensp;-
                    <a href="<%- url_for(post.path) %>"><%= post.title %></a>
                </p>
                        <% } %>
                    <% }); %>
                <% } %>

            </div>
        </div>

        <style type="text/css">
            #posts-chart,
            #categories-chart,
            #tags-chart {
                width: 100%;
                height: 300px;
                margin: 0.5rem auto;
                padding: 0.5rem;
            }
        </style>
        <div class="card">
            <div class="card-content">
                <div class="chart col s12 m6 l4" data-aos="zoom-in-up">
                    <div id="posts-chart"></div>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-content">
                <div class="chart col s12 m6 l4" data-aos="zoom-in-up">
                    <div id="tags-chart"></div>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-content">
                <div class="chart col s12 m6 l4" data-aos="zoom-in-up">
                    <div id="categories-chart"></div>
                </div>
            </div>
        </div>
        <!-- <div class="card">
            <div class="card-content">
                
            </div>
        </div> -->
    </div>

    <% if (site.categories && site.categories.length > 0) { %>
    <%- partial('_widget/category-radar') %>
    <% } %>

            
    <script type="text/javascript" src="<%- theme.jsDelivr.url %><%- url_for(theme.libs.js.echarts) %>"></script>
    <script>
        let postsChart = echarts.init(document.getElementById('posts-chart'));
        let categoriesChart = echarts.init(document.getElementById('categories-chart'));
        let tagsChart = echarts.init(document.getElementById('tags-chart'));
    
        <%
        /* calculate postsOption data. */
        var startDate = moment().subtract(1, 'years').startOf('month');
        var endDate = moment().endOf('month');
    
        var monthMap = new Map();
        var dayTime = 3600 * 24 * 1000;
        for (var time = startDate; time <= endDate; time += dayTime) {
            var month = moment(time).format('YYYY-MM');
            if (!monthMap.has(month)) {
                monthMap.set(month, 0);
            }
        }
    
        // post and count map.
        site.posts.forEach(function (post) {
            var month = post.date.format('YYYY-MM');
            if (monthMap.has(month)) {
                monthMap.set(month, monthMap.get(month) + 1);
            }
        });
    
        // xAxis data and yAxis data.
        var monthArr = JSON.stringify([...monthMap.keys()]);
        var monthValueArr = JSON.stringify([...monthMap.values()]);
        %>
    
        let postsOption = {
            title: {
                text: '<%- __("postPublishChart")  %>',
                top: -5,
                x: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: <%- monthArr %>
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: '<%- __("postsNumberName")  %>',
                    type: 'line',
                    color: ['#6772e5'],
                    data: <%- monthValueArr %>,
                    markPoint: {
                        symbolSize: 45,
                        color: ['#fa755a','#3ecf8e','#82d3f4'],
                        data: [{
                            type: 'max',
                            itemStyle: {color: ['#3ecf8e']},
                            name: '<%- __("maximum")  %>'
                        }, {
                            type: 'min',
                            itemStyle: {color: ['#fa755a']},
                            name: '<%- __("minimum")  %>'
                        }]
                    },
                    markLine: {
                        itemStyle: {color: ['#ab47bc']},
                        data: [
                            {type: 'average', name: '<%- __("average")  %>'}
                        ]
                    }
                }
            ]
        };
    
        <%
        /* calculate categoriesOption data. */
        var categoryArr = [];
        site.categories.map(function(category) {
            categoryArr.push({'name': category.name, 'value': category.length})
        });
    
        var categoryArrJson = JSON.stringify(categoryArr);
        %>
    
        let categoriesOption = {
            title: {
                text: '<%- __("categoriesChart")  %>',
                top: -4,
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            series: [
                {
                    name: '<%- __("categories")  %>',
                    type: 'pie',
                    radius: '50%',
                    color: ['#6772e5', '#ff9e0f', '#fa755a', '#3ecf8e', '#82d3f4', '#ab47bc', '#525f7f', '#f51c47', '#26A69A'],
                    data: <%- categoryArrJson %>,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
    
        <%
        /* calculate tagsOption data. */
        // get all tags name and count,then order by length desc.
        var tagArr = [];
        site.tags.map(function(tag) {
            tagArr.push({'name': tag.name, 'value': tag.length});
        });
        tagArr.sort((a, b) => {return b.value - a.value});
    
        // get Top 10 tags name and count.
        var tagNameArr = [];
        var tagCountArr = [];
        for (var i = 0, len = Math.min(tagArr.length, 10); i < len; i++) {
            tagNameArr.push(tagArr[i].name);
            tagCountArr.push(tagArr[i].value);
        }
    
        var tagNameArrJson = JSON.stringify(tagNameArr);
        var tagCountArrJson = JSON.stringify(tagCountArr);
        %>
    
        let tagsOption = {
            title: {
                text: '<%- __("top10TagsChart")  %>',
                top: -5,
                x: 'center'
            },
            tooltip: {},
            xAxis: [
                {
                    type: 'category',
                    data: <%- tagNameArrJson %>
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    type: 'bar',
                    color: ['#82d3f4'],
                    barWidth : 18,
                    data: <%- tagCountArrJson %>,
                    markPoint: {
                        symbolSize: 45,
                        data: [{
                            type: 'max',
                            itemStyle: {color: ['#3ecf8e']},
                            name: '<%- __("maximum")  %>'
                        }, {
                            type: 'min',
                            itemStyle: {color: ['#fa755a']},
                            name: '<%- __("minimum")  %>'
                        }],
                    },
                    markLine: {
                        itemStyle: {color: ['#ab47bc']},
                        data: [
                            {type: 'average', name: '<%- __("average")  %>'}
                        ]
                    }
                }
            ]
        };
    
        // render the charts
        postsChart.setOption(postsOption);
        categoriesChart.setOption(categoriesOption);
        tagsChart.setOption(tagsOption);
    </script>
            
</main>
```

在主题配置文件中(`~/gavin-wang-note.github.io/themes/matery/_config.yml`)添加：

```yaml
# 统计
stat:
  title: 文章统计  # 标题
  text: 身处不幸的时候，更应该竭尽全力。  # 一言
  icon: far fa-bar-chart  # 图标
  show_post: true  # 是否显示文章统计
```

此处参考了这篇文章[小蝉博客](https://zwxo.github.io/articles/41278/)

## 配置二级菜单栏

直接修改主题（如我的主题`themes/matery`目录下）`_config.yml`文件即可，内容参看如下：

```shell
# 配置菜单导航的名称、路径和图标icon.
menu:
  Index:
    url: /
    icon: fas fa-home
  统计:
    url: /stat
    icon: fas fa-list-alt
  文章:
    icon: fas fa-bars
    children:
      - name: 归档
        url: /archives
        icon: fas fa-archive
      - name: 分类
        url: /categories
        icon: fas fa-bookmark
      - name: 标签
        url: /tags
        icon: fas fa-tags
  About:
    icon: fas fa-star
    children:
      - name: 知我
        url: /about
        icon: fas fa-user-circle
      - name: 友链
        url: /friends
        icon: fas fa-address-book
      - name: 收藏
        url: /goodpapers
        icon: fas fa-coffee
```
