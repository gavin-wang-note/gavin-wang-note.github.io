---
layout:     post
title:      "Perl脚本实现oracle RMAN自动备份"
subtitle:   "rman auto backup by Perl script"
date:       2011-03-11
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


通过rman，实现定期自动备份，直接上脚本

[oracle@mmsc103:~/rmanbak](mailto:oracle@mmsc103:~/rmanbak)> vi backup.pl

```
#!/usr/bin/perl
##################################################
###    作用：rman定时任务脚本         ###
###    日期：2011-03-11           ###
###    作者：wyz              ###
##################################################

#获取系统当前时间
my ($sec,$min,$hour,$day,$month,$year)= localtime(time());
$year+=1900;
$month=sprintf("%02d",$month+1);
$day=sprintf("%02d",$day);
$hour=sprintf("%02d",$hour);
$min=sprintf("%02d",$min);
$sec=sprintf("%02d",$sec);
my $daytime = "$year$month$day$hour$min$sec";

system("/opt/oracle/product/11g/bin/rman  cmdfile = '/opt/oracle/rmanbak/everydaybak.rman' msglog=/opt/oracle/rmanbak/everydaybak_$daytime.log");
```

```
oracle@mmsc103:~/rmanbak](mailto:oracle@mmsc103:~/rmanbak)> more everydaybak.rman
#script.:fullbakup.rman
# creater:wangyunzeng
# date:2011-03-11
# desc:backup all database datafile in archive with rman
# connect database
connect target rman/rman;
connect catalog [rman/rman@mmsgdb](mailto:rman/rman@mmsgdb);

#start backup database
run
{
allocate channel t1 type disk; 
configure controlfile autobackup format for device type disk to '/opt/oracle/rmanbak/controlfile_bak_%F';            
backup database format 'fullbak_%s_%p_%u'  (archivelog all );
crosscheck backupset;
delete noprompt obsolete;
delete noprompt archivelog until time "sysdate -3";
release channel t1;     
}
#end
```
