---
layout:     post
title:      "Ununtu14.04 安装Jekyll及Github部署流程"
subtitle:   "Install Jekyll with Github"
date:       2019-11-20
author:     "Gavin"
catalog:    true
tags:
    - Jekyll
---


# Jekyll本地搭建开发环境以及Github部署流程

## 本地搭建Jekyll

本文以ubuntu14.04为例。

根据最新版本的要求， Jekyll 3 要求 Ruby 2.0.0 及以上的版本。但 Ubuntu 14.04 apt-get 默认提供的版本较低（1.9），所以需要从其他地方安装最新的版本。

### 安装 rbenv

从 Github 上 clone, 再添加路径 :

```
git clone git://github.com/sstephenson/rbenv.git ~/.rbenv

echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc

echo 'eval "$(rbenv init -)"' >> ~/.bashrc

source ~/.bashrc
```

然后我们需要一个 rbenv 插件 ruby-build 来编译并安装 Ruby .

```
git clone git://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build

echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc

source ~/.bashrc
```

安装 rbenv-gem-rehash . 当使用 gem 安装或卸载 Ruby package 时，这个插件自动调用 rbenv rehash .

```
git clone https://github.com/sstephenson/rbenv-gem-rehash.git ~/.rbenv/plugins/rbenv-gem-rehash
```



### 安装Node.js

官网提供的方法是：

```
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -

apt-get install -y nodejs
```

npm 也会被安装.

 

 

 

### 安装gem

说明：

**先跳过安装，如果没有****gem****，再来安装与设置环境变量**

```
apt-get install gem
```

 

设置gem环境变量

```
echo '# Install Ruby Gems to ~/gems' >> ~/.zshrc

echo 'export GEM_HOME="$HOME/gems"' >> ~/.zshrc

echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.zshrc

source ~/.zshrc
```

 

 

### 安装 Ruby 2.x 和 Jekyll 4.0

首先确定相关的依赖已经安装.

```
apt-get update

apt-get install build-essential libssl-dev libreadline-dev libyaml-dev libxml2-dev libxslt1-dev libffi-dev python-software-properties
```

然后运行下面的语句：

```
rbenv install 2.4.0

rbenv global 2.4.0
```

 

由于jekyll requires RubyGems version >= 2.7.0，需要更新gem

```
gem update --system
```

如果上面的命令不行，需要执行下面的命令：

```
gem install rubygems-update

update_rubygems
```

 

成功更新后，查看gem版本

```
root@code80:~# gem -v
3.0.6
```

 

#### 开始安装jekyll

```
gem install bundle

gem install jekyll
```

<img class="shadow" src="/img/in-post/install_jekyll_1.jpg" width="1200">
<img class="shadow" src="/img/in-post/install_jekyll_2.jpg" width="1200">

 

通过下面的方法检查安装是否成功.

```
root@code80:~# jekyll -v
jekyll 4.0.0
```



#### 使用Jekyll创建你的博客站点

```
jekyll new blog
```


说明：

  执行“jekyll new blog”会卡住很久，耐心等待一下（或者tmux里执行），成功后会看到：

<img class="shadow" src="/img/in-post/jeky_new_blog.jpg" width="1200">
 

 

#### 启动jekyll服务

```
cd blog

jekyll serve
```

 

会看到如下效果：

```
root@code80:~/blog# jekyll serve
Configuration file: /root/blog/_config.yml
            Source: /root/blog
       Destination: /root/blog/_site
 Incremental build: disabled. Enable with --incremental
      Generating... 
       Jekyll Feed: Generating feed for posts
                    done in 0.624 seconds.
 Auto-regeneration: enabled for '/root/blog'
    Server address: http://127.0.0.1:4000/
  Server running... press ctrl-c to stop.
```

 

#### 尝试web访问

由于jekyll将地址绑定到了127.0.0.1，导致局域网的其它机器并不能访问它的服务。但实际上只要改变运行jekyll的参数就可以了。

```
 root@code80:~/blog# jekyll serve -w --host=172.17.73.80
Configuration file: /root/blog/_config.yml
            Source: /root/blog
       Destination: /root/blog/_site
 Incremental build: disabled. Enable with --incremental
      Generating... 
       Jekyll Feed: Generating feed for posts
                    done in 0.49 seconds.
 Auto-regeneration: enabled for '/root/blog'
    Server address: http://172.17.73.80:4000/
  Server running... press ctrl-c to stop.
```



 

通过172.17.73.80这个地址，访问web：

<img class="shadow" src="/img/in-post/default_ui.jpg" width="1200">

 

至此，jekyll安装好了。

 

## 使用Jekyll写博文

### 博文结构

我们进入blog目录后，会发现Jekyl的结构如下：

<img class="shadow" src="/img/in-post/default_tree.jpg" width="1200">

 

 

### 博文发布测试

我们进入_post目录，撰写的markdown语法的博文都放在这里。默认会有一篇测试文章：2019-11-21-welcome-to-jekyll.markdown.

 

现在写两个新的md文档

```
-rw-r--r-- 1 root root 3319 Nov 21 21:20 2019-11-20-nose-progress-bar.md

-rw-r--r-- 1 root root 5018 Nov 21 21:20 2019-11-21-write-nose-test-case-role.md
```

然后刷新一下浏览器、发现页面并没有变化.因为我们还没有通过Jekyll build去生成。


### jekyll build

默认情况下，服务会以前台的方式挂起，如果希望用后台进程运行服务，我们可以使用 --detach参数，缩写参数为-B(应该是Background的首字母)

```
jekyll serve build --detach -w --host=172.17.73.80
```

或者

```
jekyll serve build -B -w --host=172.17.73.80
```

注意：

  如果用vagrant虚拟机去安装jekyll，那么启动服务时还需要加上-H参数，指定访问主机号为0.0.0.0，即jekyll serve build -B -H 0.0.0.0,否则vagrant下可能启动失败

再查看首页，发现已经有三篇文章了！

<img class="shadow" src="/img/in-post/3_test_file.jpg" width="1200">

### 博文头信息

打开一个markdown,可以看见开头有如下几个东东。

```
---

layout: post

title: "Welcome to Jekyll!"

date:  2019-11-21 20:52:45 +0800

categories: jekyll update

---
```

layout表示使用的是post布局，title是文章标题，date是自动生成的日期，categories是该文章生成html文件后存放的目录，可以去_site/jekyll/update下找到对应日期下面的html文档。当然你也可以只设置jekyll单一的目录，甚至是更多级别的目录，用空格分开即可。头信息设置完成后就可以书写正文了。

如果每次都输入这些头信息，还要去整理格式，那么一定很烦躁，这种重复性的东西我们就把它自动化，通过Rakefile去解决，它类似shell这样的脚本，可以使用交互模式。以下是我的Rakefile,可以复制后命名为Rakefile，放在站点根目录直接使用，也可以修改为适合自己的Rakefile：

 

```
task :default => :new

require 'fileutils'

desc "创建新 post"

task :new do

 puts "请输入要创建的 post URL："

  @url = STDIN.gets.chomp

  puts "请输入 post 标题："

  @name = STDIN.gets.chomp

  puts "请输入 post 子标题："

  @subtitle = STDIN.gets.chomp

  puts "请输入 post 分类，以空格分隔："

  @categories = STDIN.gets.chomp

  puts "请输入 post 标签："

  @tag = STDIN.gets.chomp

  @slug = "#{@url}"

  @slug = @slug.downcase.strip.gsub(' ', '-')

  @date = Time.now.strftime("%F")

  @post_name = "_posts/#{@date}-#{@slug}.md"

  if File.exist?(@post_name)

​      abort("文件名已经存在！创建失败")

  end

  FileUtils.touch(@post_name)

  open(@post_name, 'a') do |file|

​      file.puts "---"

​      file.puts "layout: post"

​      file.puts "title: #{@name}"

​      file.puts "subtitle: #{@subtitle}"

​      file.puts "author: Gavin"

​      file.puts "date: #{Time.now}"

​      file.puts "categories: #{@categories}"

​      file.puts "tag: #{@tag}"

​      file.puts "---"

  end

  exec "vi #{@post_name}"

end
```

 

### 如何使用Rake

输入一下命令：

```
rake new
```

 

rake会启动交互模式，让你依次输入title，subtitle，author，categories，tag等信息，并为你创建好具有头信息的markdown文件。如下一样:

```
请输入要创建的 post URL：

testurl

请输入 post 标题：

testpost

请输入 post 子标题：

subtitle  

请输入 post 分类，以空格分隔：

jekyll

请输入 post 标签：

技术
```

 

我们查看_post目录，发现已经有一篇2019-11-21-testurl.md文章，打开看下

```
---

layout: post

title: testpost

subtitle: subtitle

author: gavin

date: 2019-11-21 21:39:27 +0800

categories: jekyll

tag: 技术

---
```

 

  

## 使用Github pages服务生成个人博客

### 创建我们的仓库

 
<img class="shadow" src="/img/in-post/my_pro.jpg" width="1200">

 

如此，我们已经可以通过浏览器输入 [http://username.github.io](https://link.jianshu.com/?t=http://username.github.io)访问博客主页。那么我就访问https://gavin-wang-note.github.io/

如下图所示，就是我的默认博客首页：

<img class="shadow" src="/img/in-post/my_default_blog_ui.jpg" width="1200">

 

这里我使用了他人的pro，更换了一些图片，代替上面默认的风格，展示如下：

<img class="shadow" src="/img/in-post/my_new_pro.jpg" width="1200">


 

### 将本地jekyll代码部署到Github上的仓库

前面我们已经详细地说明如何搭建Jekyll，我们可以在本地开发测试，推送代码到仓库，发布到线上。

### 克隆仓库到本地

请确保本地安装了git客户端，克隆你的username.github.com仓库到本地。

```
git clone https://github.com/username/username.github.com.git
```

 

### 拷贝本地的jekyll目录到版本库

删除username.github.com下面的示例文件(README.md,不要删除，绑定域名会用到):

```
rm -rf _site index.html _config.yml
```

拷贝本地blog(这个是前面本地搭建的blog，后续等同，不再说明)下的所有目录及文件到username.github.com

```
cp -r /root/blog/* username.github.com
```

此时你会看见当前存在username.github.com这个目录，我们启动jekyll服务（启动前确保其他目录下没有jekyll服务，可以`ps aux|grep jekyll`查看进程,有的话,用`kill -9 进程号`杀掉）:

```
cd username.github.com

jekyll serve -B -w --host=172.17.73.80
```

现在我们打开http://172.17.73.80:4000,即可看见我们在Github上创建的主页，理论上和[http://username.github.com](https://link.jianshu.com?t=http:/username.github.com) 访问的应该是一模一样的。

 

### 本地Jekyll站点部署到Github Pages上（相当于线上环境）

```
git add --all       #添加到暂存区 

git commit -m "提交jekyll默认页面" #提交到本地仓库

git push origin master     #线上的站点是部署在master下面的

```

稍等10分钟左右，Github Pages有一定时间缓存,我们刷新username.github.io看看,已经ok了！
 

 

## 问题

### Jekyll因MissingDependencyException启动失败

<img class="shadow" src="/img/in-post/jekyll_start_failed.jpg" width="1200">
 

 

主要是这一句：

```
The jekyll-theme-cayman theme could not be found
```

 

那就使用gem去安装它

```
gem install jekyll-theme-cayman
```

<img class="shadow" src="/img/in-post/install_jekyll-theme-cayman.jpg" width="1200">

 

成功安装后，再次启动Jekyll

<img class="shadow" src="/img/in-post/start_jekyll_again.jpg" width="1200">

 

后续如果缺失其他模块，可根据trace信息，使用gem进行安装。

 

# 参考文档

https://jekyllrb.com/docs/installation/ubuntu/

https://www.digitalocean.com/community/tutorials/how-to-install-ruby-on-rails-with-rbenv-on-ubuntu-14-04

https://blog.csdn.net/sinat_34439107/article/details/78440836

https://www.jianshu.com/p/f37a96f83d51
