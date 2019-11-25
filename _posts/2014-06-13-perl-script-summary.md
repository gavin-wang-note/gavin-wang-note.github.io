---
layout:     post
title:      "Perl常用代码汇总"
subtitle:   "Perl common code summary"
date:       2014-06-13
author:     "Gavin"
catalog:    true
tags:
    - perl
---

# 概述

初学perl，汇总了一下，在工作中使用perl写测试脚本常用到的一些代码块信息。


# 相关代码案例

## 文件操作



### 查找指定目录下文件夹

```
use File::Find;
my @files;

sub want
{
#push @files,$_ if -d $_;
push @files,$_ if -d $_ and !/^\.{1,2}/;
}

find(\&want,'/home/wyz/');
print "\nfiles:@files\n";
```



### 找出目录下所有文件

```
my @file_names=grep {-f and -T} glob '*';
print "\nfile_names:@file_names\n";
```



### 获取指定目录下所有文件

```
#!/usr/bin/perl
use warnings;
use strict;
use File::Find;

my $dir = shift || die "Please input a directory!!!";

find (\&handle,$dir);

sub handle
{
    print $File::Find::name,"\n" if -f $_;
}
```



## 获取脚本当前路径

```
use File::Basename;
my $dir = File::Basename::dirname($0);
print $dir;
```



## 创建目录

```
  #文件存放路径
  unless (-d "$USER.load")
  {
      mkdir("$USER.load", 0755) || die "Make directory $USER.load error.\n";
  }
  chdir "$USER.load";
```



## 文件句柄
​       

```
 for(my $i=1; $i<=$scalar;$i++)
         {                                                                                              
            open(SQLPLUS, "|sqlplus -S $USER/$USERPASS\@$SID >/dev/null") || die "Execute sqlplus error!\n";
            print SQLPLUS "set feedback off\nset sqlnumber off\n";
            print SQLPLUS "set pagesize 0\n";
            print SQLPLUS "set trimspool off\n";
            print SQLPLUS "set sqlblanklines off\n";
            print SQLPLUS "spool $array[$i].wyz_tmp\n";
            print SQLPLUS "desc $array[$i]\n";
            print SQLPLUS "spool off\n";
            close(SQLPLUS) || die "Execute sql error!\n";
         }
```



## 从配置文件获取数据

```
use FindBin qw ($Bin);                                                          #解决AIX未安装Config::IniFiles模块问题
use lib "$Bin/syslib";
use Config::IniFiles;

#从配置文件中获取信息
my $cfg = Config::IniFiles->new( -file => "$cur_path/config/init.cfg" );

my $DB_USER=$cfg->val('COMPARE_DATA','DB_USER') || '';                          #连接数据库的用户名
my $DB_PASS=$cfg->val('COMPARE_DATA','DB_PASS') || '';                          #连接数据库的用户名对应的口令
my $DB_IDENTIFIED=$cfg->val('COMPARE_DATA','DB_IDENTIFIED') || '';              #连接数据库的标识
my $PROC_TYPE=$cfg->val('COMPARE_DATA','PROC_TYPE') || '';                      #产品类型
my $IS_SCENE=$cfg->val('COMPARE_DATA','IS_SCENE') || '';                        #是否使用现网数据
my $BEFORE_AFTER_VERSION=$cfg->val('COMPARE_DATA','BEFORE_AFTER_VERSION') || '';#升级前版本号
my $UPDATE_TO_VERSION=$cfg->val('COMPARE_DATA','UPDATE_TO_VERSION') || '';      #升级后版本号
```



## 定义日志

```
my $start_date = ostime(time);                                                  #时间，日志内容中使用，年月日时分秒
my $logtime=shortTimeString(time);                                              #时间，日志文件命名使用,年月日时分
my $script_log="$script_dir/update_db_$logtime.log";                            #定义脚本执行过程中日志记录信息


```



## 年月日小时分秒，用于日志文件内容中记录的时间

```
sub ostime 
{
 my ($tm) = @_;
 my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($tm);
 return sprintf("%04d-%02d-%02d %02d:%02d:%02d", $year+1900, $mon+1, $mday, $hour, $min, $sec);
}
```



## 年月日小时分，用于日志文件命名

```
sub shortTimeString 
{
 my ($tm) = @_;
 my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($tm);
 return sprintf("%04d_%02d_%02d_%02d_%02d", $year+1900, $mon+1, $mday, $hour, $min);
}
```



## 记录日志

```
sub LOG {
 my ($text) = @_;
 my $time = ostime time;
 print "\n[$time] $text\n";

 open(UPDATELOG,">>$script_log") or die("打开日志文件[$script_log]出错: $!");
 print UPDATELOG "\n[$time] $text\n";
 close UPDATELOG;
}
```



## 文件属性信息

```
use warnings;
use strict;

die "请输入文件名称\n" unless(@ARGV>=1);

print "\n检测文件信息:\n";

foreach my $file(@ARGV)
{
    if(-e $file)
    {
        print "\n存在文件:$file\n";
        

    if(-f $file)
    {
        print "可读\n" if(-r $file);
        print "可写\n" if(-w $file);
        print "可执行\n" if(-x $file);
        
        print "文件大小是:", -s $file,"Bytes\n";
        
        my @time=timeconv(-A $file);
        print "\n距离上次访问文件 $file 时间是 $time[0] 天 $time[1] 小时 $time[2] 分 $time[3] 秒.\n";
        
        @time=timeconv(-M $file);
        print "\n距离上次修改文件 $file 时间是 $time[0] 天 $time[1] 小时 $time[2] 分 $time[3] 秒.\n";          
    }
}
elsif(-d $file)
{
    print "\n$file 是个目录\n";
}
else
{
    print "\n$file 不存在\n";
}

}


sub timeconv
{
    my $time=shift;
    my $days=int($time);
    $time=($time-$days)*24;
    

    my $hours=int($time);
    $time=($time-$hours)*60;
    
    my $minutes=int($time);
    $time=($time-$minutes)*60;
    
    my $seconds=int($time);
    return ($days,$hours,$minutes,$seconds);    

}
```



# 操作系统相关

## 获取操作系统名称
```
use Sys::Hostname;
print hostname,"\n";
```



### 操作系统类型

```
chomp(my $OS_Type = $^O);
```

$OS_Type打印结果为：linux/MSWin32/SUNOS等



## 自动关机

```
use Win32;

my $machine = Win32::NodeName();
my $timeout = 3600;
if($ARGV[0])
{
    $timeout = $ARGV[0];
}

my $message = Win32::MsgBox("即将在 $timeout 秒后自动关机.
如想取消，请进入dos界面执行 shutdown -a 操作.");
Win32::InitiateSystemShutdown($machine,$message,$timeout,1,1);
```

说明：
  Win32::InitiateSystemShutdown
   (MACHINE, MESSAGE, TIMEOUT, FORCECLOSE, REBOOT)

   Shutsdown the specified MACHINE, notifying users with the supplied
   MESSAGE, within the specified TIMEOUT interval. Forces closing of
   all documents without prompting the user if FORCECLOSE is true, and
   reboots the machine if REBOOT is true. This function works only on WinNT.



## 生成随机密码

### 产生随机密码
```
my @input=(1..9,'a'..'z');
my $passwd= join '',map {$input[int rand @input]} 0..7;
print "\n随机密码为:$passwd\n";
```

这里的 0..7，约束了密码的长度，输出长度为8，rand后面的@input是个标量，即长度。



# Usage

## 方法1

```
#!/usr/bin/perl
use warnings;
use strict;

die "\n\tUsage: perl $0 parameter1 parameter2 parameter3\n\n" unless(@ARGV==3);   

print "\ntest\n\n";
```



## 方法2

```
my $file = $ARGV[0] or die "\n  [ERROR]   请脚本名称后面携带CSV文件!\n\n";
```



# 判断脚本是否已经有在运行

```
exit if 2 == grep { /perl/ }  qx{ ps aux|grep $0 };
```

具体示例如下述

```
print "程序已运行，退出!\n" and exit if 2==grep {/$0/i} `ps -ef | grep $0 | grep -v grep`;
```



# 数组

## 文件内容放入数组

```
my $FH;
my @bug_array;

open($FH,"tmp.csv") or die "\nOpen file faild,$!\n\n";
{
    @bug_array=<$FH>;
    @bug_array=sort @bug_array;
}
close($FH);


redo
my $response;

{
   print "\n是否继续:[yes/no]\n";
   chomp($response=<STDIN>);
   $response=lc($response);

   $response eq "yes" or $response eq "y" or $response eq "n" or $response eq "no" or
   print "\n只能输入y/yes/n/no中的一个，请重新输入:\n" and redo;
}

print "\n你选择了 $response\n"
```



