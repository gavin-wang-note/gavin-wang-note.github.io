---
layout:     post
title:      "shell中|&含义"
subtitle:   "What's the '|&' means in shell"
date:       2020-06-30
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
    - [shell]
tags:
    - Linux
    - shell
---



# 概述

今天细看了同事Henry编写的一个shell脚本，看到如下片断内容：


```shell
    while (( $(${CLI} info |& grep PROCESSING | wc -l) >= 1 )); do
        sleep 60
    done
```

这里有一个```'|&' ```，不明觉厉~  (#^.^#)

# 我的疑惑

```'|&' ``` 是什么意思？


man了下bash，得到如下信息：


```shell
   Pipelines
       A pipeline is a sequence of one or more commands separated by one of the control operators | or |&.  The format for a pipeline is:

              [time [-p]] [ ! ] command [ [|?|&] command2 ... ]

       The  standard  output of command is connected via a pipe to the standard input of command2.  This connection is performed before any redirections specified by the command (see REDIRECTION below).  If |& is used, command's standard error, in addition to its
       standard output, is connected to command2's standard input through the pipe; it is shorthand for 2>&1 |.  This implicit redirection of the standard error to the standard output is performed after any redirections specified by the command.

       The return status of a pipeline is the exit status of the last command, unless the pipefail option is enabled.  If pipefail is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status, or zero if all
       commands  exit  successfully.   If  the  reserved word !  precedes a pipeline, the exit status of that pipeline is the logical negation of the exit status as described above.  The shell waits for all commands in the pipeline to terminate before returning a
       value.

       If the time reserved word precedes a pipeline, the elapsed as well as user and system time consumed by its execution are reported when the pipeline terminates.  The -p option changes the output format to that specified by POSIX.  When the shell is in posix
       mode,  it  does  not  recognize time as a reserved word if the next token begins with a `-'.  The TIMEFORMAT variable may be set to a format string that specifies how the timing information should be displayed; see the description of TIMEFORMAT under Shell
       Variables below.

       When the shell is in posix mode, time may be followed by a newline.  In this case, the shell displays the total user and system time consumed by the shell and its children.  The TIMEFORMAT variable may be used to specify the format of the time information.

       Each command in a pipeline is executed as a separate process (i.e., in a subshell).
```

这里解释的非常清楚了，```'|&' ``` 等价于  ```'2>&1|' ```，前者是后者的简写方式，将标准错误输出(stderr)隐式重定向到标准输出(stdout)是在命令指定的任何重定向之后执行的。


# 其他信息

最早是csh/tcsh里有这个特性，被bash和zsh学过来了，ksh里```'|&' ``` 是另外一种用法，表示的是协同处理。

如果你的shell不支持这种特性，一旦脚本中含有```'|&' ```，执行时报错：

```Syntax error: "&" unexpected ```



