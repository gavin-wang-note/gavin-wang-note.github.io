---
layout:     post
title:      "清除Oracle数据库中所有表、视图、触发器"
subtitle:   "Clean all of tables/views/trigger"
date:       2013-01-25
author:     "Gavin"
catalog:    true
tags:
    - perl
    - oracle
---


# 概述

在网关组做产品测试的时候，经常要安装环境，部署产品，其中涉及到产品部署刷库，由于组内有多套产品，每套产品所需的表名称皆不仅相同，又互补兼容，在切换到另外一个产品进行测试的时候，不想重做数据库，或者重做表空间来进行数据数据的清理，故而想用一个脚本来清理掉当前数据库环境中的所有的表、视图以及触发器，更换被测产品时，直接先抹掉当前数据，执行下个产品的刷库脚本即可。


# 清理脚本

使用perl语言编写（那个时候，组内都用perl，初学，水平有限，望请海涵。。。）

直接上脚本


```
#!/usr/bin/perl
use warnings;
use strict;
use Cwd;

################################################################################
#    ######################################################################    #
#   #      说明：   清除当前数据库用户中所有表、视图、存储过程等数据       #   #
#   #      使用：   perl   cls_db.pl                                       #   #
#   #      AUTH：   wangyunzeng                                            #   #
#   #      VER ：   1.0                                                    #   #
#   #      TIME：   2013-01-25   14:52   create                            #   #
#    ######################################################################    #
################################################################################


#说明
$~="CLEAR";
write;
format CLEAR =

--------------------------------------------------------------------------------
说明：
    
    此脚本，清除数据库应用用户下所有资源，包括：表、视图、存储过程、包、包体、

    JOB、Sequence、TRIGGER

--------------------------------------------------------------------------------
.

#当前路径
my $cur_path=getcwd;

#输入数据库用户。口令与SID信息，并校验
my $USER=$ARGV[0];
my $USERPASS=$ARGV[1];
my $SID =$ARGV[2];


#使用方法
if(@ARGV !=3)
{
    print "\n【使用方法】
    
         perl cls_db.pl username  passwd  sid\n\n";
    
    exit;
}
else
{
    #检查下
    &check;
            
    system("which sqlplus>/dev/null");
    if($? eq "0")
    {
        #print '-' x 80,"\n";
        
        #先导出，然后再清理
        print "\n是否需要导出当前用户下数据，[yes/no]?\n\n";
        
        my $response=<STDIN>;
        $response=lc($response);
        chomp($response);
        
        if($response eq "y" || $response eq "yes")
        {
            if(-f "$cur_path/exp_$USER.dmp")
            {
                system("rm -f $cur_path/exp_$USER.dmp");
            }
            print "\n开始导出数据到dmp文件\n";
            system("exp $USER/$USERPASS\@$SID file=$cur_path/exp_$USER.dmp");
        }
        elsif($response eq "n" || $response eq "no")
        {
            print "\n不需要导出当前用户下数据到dmp文件.\n";
        }
        else
        {
            print "\n[yes/no]输入错误，不进行备份操作，直接进行清理.\n\n";
        }
        
        print '-' x 80,"\n";
        
        print "\n开始清理当前数据库下所有对象.......\n";
        
        
        #调用子函数
        &expinfo;
        &dropops;
        
        print '-' x 80,"\n";
    }
    else
    {
       print "\n不支持的数据库类型，程序退出!\n\n";
       print '-' x 60,"\n";
       exit;
    }   
}



####################################定义子函数##################################
##对输入的用户名、口令和SID校验
sub check
{
   if(!$USER || $USER eq "" || $USER eq "sys" || $USER eq "system" || $USER eq "scott" || $USER eq "sysman" || $USER eq "rman")
   {
       print "\n输入数据库用户名有误，不能为空、不能为sys、system、scott、sysman或rman用户，程序退出执行!\n\n";
       exit;
   }
   elsif(!$USERPASS || $USERPASS eq "")
   {
       print "\n输入数据库口令有误，不能为空，程序退出执行!\n\n";
       exit;    
   }
   elsif(!$SID || $SID eq "")
   {
       print "\n输入数据库SID有误，不能为空，程序退出执行!\n\n";
       exit;      
   }
}


##导出当前数据库中表名、视图名等到文件
sub expinfo
{
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
}

##执行删除操作
sub dropops
{
    ##判断文件是否存在
    (-f "$cur_path/dropjob.txt") || die "\n File [dropjob.txt] is not eixt,$!\n\n";
    (-f "$cur_path/dropobj.txt") || die "\n File [dropobj.txt] is not eixt,$!\n\n";
    
    system("cat $cur_path/dropjob.txt $cur_path/dropobj.txt > $cur_path/dropinfo.txt");
    
    unlink("$cur_path/dropjob.txt");
    unlink("$cur_path/dropobj.txt");
    
    #执行清理操作
    open(SQLPLUS, "|sqlplus -S $USER/$USERPASS\@$SID >/dev/null") || die "Execute sqlplus loging error!\n";
    print SQLPLUS "\@$cur_path/dropinfo.txt\n";
    close(SQLPLUS) || die "Execute sqlplus exit error!\n";     
}
```
