---
layout:     post
title:      "Shell和Perl调用sqlplus的几种操作"
subtitle:   "Call sqlplus by Shell and Perl"
date:       2012-08-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# Shell调用sqlplus各种情况

## 1、最简单的shell里调用sqlplus

```shell
$ vi test1.sh

#!/bin/bash
sqlplus -S /nolog > result.log <<EOF
set heading off feedback off pagesize 0 verify off echo off
conn u_test/iamwangnc
select * from tab;
exit
EOF

$ chmod +x test1.sh
$ ./test1.sh
```

## 2、把sqlplus执行结果传递给shell方法一

注意sqlplus段使用老板键`了, 赋变量的等号两侧不能有空格.

```shell
$ vi test2.sh

#!/bin/bash
VALUE=`sqlplus -S /nolog <<EOF
set heading off feedback off pagesize 0 verify off echo off numwidth 4
conn u_test/iamwangnc
select count(*) from tab;
exit
EOF`
if [ "$VALUE" -gt 0 ]; then
        echo "The number of rows is $VALUE."
        exit 0
else
        echo "There is no row in the table."
fi

$ chmod +x test2.sh
$ ./test2.sh
```

## 3、把sqlplus执行结果传递给shell方法二

注意sqlplus段使用 col .. new_value .. 定义了变量并带参数exit, 然后自动赋给了shell的$?

```shell
$ vi test3.sh

#!/bin/bash
sqlplus -S /nolog > result.log <<EOF
set heading off feedback off pagesize 0 verify off echo off numwidth 4
conn u_test/iamwangnc
col coun new_value v_coun
select count(*) coun from tab;
exit v_coun
EOF
VALUE="$?"
echo "The number of rows is $VALUE."

$ chmod +x test3.sh
$ ./test3.sh
```

## 4、把shell程序参数传递给sqlplus

$1表示第一个参数, sqlplus里可以直接使用, 赋变量的等号两侧不能有空格不能有空格.

```shell
$ vi test4.sh

#!/bin/bash
NAME="$1"
sqlplus -S u_test/iamwangnc <<EOF
select * from tab where tname = upper('$NAME');
exit
EOF

$ chmod +x test4.sh
$ ./test4.sh ttt
```

## 5、为了安全要求每次执行shell都手工输入密码

```shell
$ vi test5.sh

#!/bin/bash
echo -n "Enter password for u_test:"
read PASSWD
sqlplus -S /nolog <<EOF
conn u_test/$PASSWD
select * from tab;
exit
EOF

$ chmod +x test5.sh
$ ./test5.sh
```

## 6、为了安全从文件读取密码

对密码文件设置权限, 只有用户自己才能读写.

```shell
$ echo 'iamwangnc' > u_test.txt
$ chmod g-rwx,o-rwx u_test.txt
$ vi test6.sh

#!/bin/bash
PASSWD=`cat u_test.txt`
sqlplus -S /nolog <<EOF
conn u_test/$PASSWD
select * from tab;
exit
EOF

$ chmod +x test6.sh
$ ./test6.sh
```

# Perl调用sqlplus各种情况

## 1、最简单的perl调用sqlplus

```shell
system(“sqlplus $user/$passwd\@$sid”);
```

## 2、通过文件句柄

```shell
    open(SQLPLUS, "|sqlplus -S $USER/$USERPASS\@$SID >/dev/null") || die "Execute sqlplus loging error!\n";
    print SQLPLUS "set feedback off\nset sqlnumber off\n";
    print SQLPLUS "set pagesize 0\n";
    print SQLPLUS "set trimspool off\n";
    print SQLPLUS "set sqlblanklines off\n";
    print SQLPLUS "spool $cur_path/dropjob.txt\n";
    print SQLPLUS "select 'drop job ' || job || ';' from user_jobs;\n";
    print SQLPLUS "spool $cur_path/dropobj.txt\n";    
    print SQLPLUS "select 'drop ' || object_type || ' ' || object_name || ';' from user_objects;\n";
    print SQLPLUS "spool off\n";
    close(SQLPLUS) || die "Execute sqlplus exit error!\n";  
```

