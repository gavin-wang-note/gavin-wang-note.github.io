---
layout:     post
title:      "Bash中的here document"
subtitle:   "Bash中 here document"
date:       2022-09-02
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - here document
---


# 引言

bash经常有这种需求，需要增加多行文字到某文件。
当然可以采用如下的命令去做：

``` 
    echo "This is line 1 " >>dest.conf
    echo "This is line 2 " >>dest.conf
    echo "This is line 3 " >>dest.conf
```

这样当然是可以的，但是显得很low，尤其是加入一段code 进某文件的时候，看起来特别扎眼。

here文档就是解决这个问题的。一直用，也没有理解，导致经常忘，这次将原理补上，很好的理解才能灵活的运用


# Here Docement

Here 文档，又称为heredoc，hereis，维基百科的介绍在此[https://zh.wikipedia.org/wiki/Here%E6%96%87%E6%A1%A3]。

简单地说，here document用于定义一个有复杂格式的字符串。如果你的字符串是有格式的，比如说有换行，有缩进，这时候，就是here document发挥作用了。
here文档最通用的语法是<<紧跟一个标识符，从下一行开始是想要引用的文字，然后再在单独的一行用相同的标识符关闭

对于上面的需求，就可以简单地这样是做：

```
    cat >>dest.conf << EOF
    This is line 1
    This is line 3
    This is line 3
    EOF
```

下面看下实际情况：

```
    root@node-191:/tmp# cat  >>dest.conf  << EOF
    > This is line 1 
    > This is line 2
    > This is line 3
    > EOF
    root@node-191:/tmp# cat dest.conf 
    This is line 1
    This is line 2
    This is line 3
```

<< EOF 可以看作是起始
最末尾的EOF可以看作是字符串结束，
两者之间的内容，要原封不动地写入文件，换行缩进都要保持。

#  应用场景

对于没有格式要求的场景，echo也可以，但是对于代码这种有格式要求的，在shell脚本中echo就特别不合时宜。
看如下shell脚本的片段，即完成了任务，有没有破坏代码的结构。

```
    cat >> /etc/default/functions  <<EOF
    ctdb_check_counter_limit () {
        _ctdb_counter_common
        _limit="${1:-${service_fail_limit}}"
        _quiet="$2"
        
        # unary counting!
        _size=$(stat -c "%s" "$_counter_file" 2>/dev/null || echo 0)
        if [ $_size -ge $_limit ] ; then
            echo "ERROR: more than $_limit consecutive failures for $service_name, marking cluster unhealthy"
            exit 1
        elif [ $_size -gt 0 -a -z "$_quiet" ] ; then
            echo "WARNING: less than $_limit consecutive failures ($_size) for $service_name, not unhealthy yet"
        fi
    }
    EOF
```

