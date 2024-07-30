---
layout:     post
title:      "linux 下批量删除文件中空格"
subtitle:   "Linux delete space for files"
date:       2016-01-18
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
    - shell
---


# 概述


Linux下如何快速、批量删除文件中的空格？



# shell示例代码


```shell
#!/usr/bin/bash

ls|while read i;do  
    mv "$i" $(echo $i|tr -d ' ') 2>/dev/null  

done 
```
