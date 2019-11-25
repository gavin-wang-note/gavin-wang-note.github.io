---
layout:     post
title:      "绑定与还原网卡配置文件"
subtitle:   "Bond and restore NIC interface"
date:       2013-05-08
author:     "Gavin"
catalog:    true
tags:
    - perl
---

# 概述

在网关测试组工作期间，产品支持SUSE9/SUSE10/SUSE11平台，每次部署环境，都要进行网卡配置操作，虽然有指导手册，无奈比较懒，不想浪费心力在手动配置上，于是酝酿出这个脚本，实现自动进行网卡的绑定动作，一旦绑定失败，自动还原。

# 直接上脚本

```
#!/usr/bin/perl
use warnings;
use strict;
use Sys::Hostname;
use Socket;


################################################################################
#    ######################################################################    #
#   #      说明：   完成网卡文件的备份、绑定、回滚等操作                   #   #
#   #      使用：   perl   network_bond.pl                                 #   #
#   #      AUTH：   wangyunzeng                                            #   #
#   #      VER ：   1.0                                                    #   #
#   #      TIME：   2012-06-11   18:50   create                            #   #
#   #      VER ：   1.1                                                    #   #
#   #      TIME：   2013-05-08   18:05   增加SUSE9/11平台绑定网卡操作      #   #
#    ######################################################################    #
################################################################################

#定义全局变量
chomp(my $OS_Type = $^O);                                                       #操作系统类型
my $cornel;                                                                     #内核版本号,2013-05-08

my $host=hostname();                                                            #修改获取大网IP可能错误问题，2013-05-08
my $IP_A=inet_ntoa(scalar gethostbyname ($host || 'localhost'));
chomp($IP_A);


#判断当前登录用户，非root，退出
my $localuser = getlogin || (getpwuid($<))[0] || die "Can't find a user here!!!\n";

if($localuser ne "root")
{
  print "\n当前登录用户非root，退出！\n\n";
  exit;
}
else
{
   print "\n【说明】
       1、本脚本仅支持SUSE9/SUSE10/SUSE11平台
       
       2、本脚本将Fabric平面网卡绑定成bond0，将Base平面网卡绑定成bond1
       
       3、本脚本备份原网卡配置文件，备份在 /etc/sysconfig 目录下，network_日期.tar.gz
          如果绑定失败，请登录usm，到 /etc/sysconfig 目录下解压后重启网卡既可. \n\n";
       
   
   ##判断操作系统类型
   if($OS_Type =~ /linux/)
   {
      chomp($cornel=`cat /etc/SuSE-release  | head -1`);                        #内核版本号
      
      ##获取系统时间  
      my ($sec,$min,$hour,$day,$month,$year)= localtime(time());
      
      $year+=1900;
      $month=sprintf("%02d",$month+1);
      $day=sprintf("%02d",$day);
      $hour=sprintf("%02d",$hour);
      $min=sprintf("%02d",$min);
      $sec=sprintf("%02d",$sec);
      
      my $daytime = "$year$month$day";
      
      chdir "/etc/sysconfig"; 
      if(! -f "network_ $daytime.tar.gz")
      {
         system("tar zcf network_$daytime.tar.gz network");
      }

      &bak_check;
   }
   else
   {
      print "\n当前仅支持ATAE SUSE平台下网卡绑定操作!\n\n";
      exit;
   }
}


#################################################################################
###                                  定义子例程                               ###
#################################################################################

sub bak_check()
{
  if( -f "/etc/sysconfig/network/ifcfg-bond0")
  {
    print "\n存在网卡绑定文件ifcfg-bond0! \n\n";
    print "\n可能已经绑定网卡，程序退出.\n\n";
    exit;
  }
  
  if( -f "/etc/sysconfig/network/ifcfg-bond1")
  {
    print "\n存在网卡绑定文件ifcfg-bond1! \n\n";
    print "\n可能已经绑定网卡，程序退出.\n\n";
    exit;
  }

  chdir "/etc/sysconfig/network"; 
  
  print "\n开始备份网卡文件.\n\n";
 
  #创建目录
  unless (-d "bak")                                                             #如果目录不存在，创建目录
  {
    mkdir("bak", 0755) || die "Make directory bak error,$!.\n";
  }

  #增加SUSE9和SUSE11平台的支持与判断
  if($cornel=~m/Server 10/i || $cornel=~m/Server 9/i )
  {
    system("cp ifcfg-eth-id-* ./bak/");
  }
  elsif($cornel=~m/Server 11/i)
  {
    system("cp ifcfg-eth[0-9] ./bak/");
  }
  
  
  #判断备份是否成功,成功则继续
  #my $ifcfg_cut=`ls ./bak/ifcfg-eth-id-* | wc -l`;
  my $ifcfg_cut=`ls ./bak/ifcfg-eth* | wc -l`;                                  #SUSE11 文件名称发生变化,2013-05-08
  chomp($ifcfg_cut);

  if($ifcfg_cut >= 1)
  {
    print "\n备份网卡文件成功\n\n";
    
    #绑定网卡
    &bond;
    
    #清理文件
    &clear;
    
    #重启网卡
    print "\n重启网卡......\n\n";
    system("rcnetwork restart");
    
    #打印绑定后的网卡信息
    print "\n绑定后的网卡信息如下:\n\n";
    system("ifconfig -a");
  
    
    print "\n完成网卡的绑定.\n\n";
   
  }
  else
  {
    print "\n备份网卡文件失败,退出!\n\n";
    exit;
  }
}


sub bond()
{
   system("/var/adm/autoinstall/scripts/eth_alias.sh  | grep -v Update | grep -v PMC  > eth.tmp");
   system("ifconfig -a | grep -v RX | grep -v dropped | grep -v UP | grep -v collisions | grep -v Interrupt | grep -v \"127.0.0.1\" > ifconfig.txt");
   
   ##网卡名
   my $eth_A= `cat eth.tmp | grep Fabric1 |  awk \-F \" \" \'\{print \$1\}\'`;
   my $eth_B= `cat eth.tmp | grep Fabric2 |  awk \-F \" \" \'\{print \$1\}\'`;
   my $eth_C= `cat eth.tmp | grep Base1 |  awk \-F \" \" \'\{print \$1\}\'`;
   my $eth_D= `cat eth.tmp | grep Base2 |  awk \-F \" \" \'\{print \$1\}\'`;
   
   chomp($eth_A);
   chomp($eth_B);
   chomp($eth_C);
   chomp($eth_D);
   
   
   ##总线
   my $Fabric1_A1=` more eth.tmp | grep Fabric1 | awk -F \" \" \'\{print \$2\}\' | awk \-F \"\,\" \'\{print \$1\}\' `;
   my $Fabric1_A2=` more eth.tmp | grep Fabric1 | awk -F \" \" \'\{print \$2\}\' | awk \-F \"\,\" \'\{print \$2\}\' `;
   my $Base1_A1=` more eth.tmp | grep Base1 | awk -F \" \" \'\{print \$2\}\' | awk \-F \"\,\" \'\{print \$1\}\' `;
   my $Base1_A2=` more eth.tmp | grep Base1 | awk -F \" \" \'\{print \$2\}\' | awk \-F \"\,\" \'\{print \$2\}\' `;
   
   chomp($Fabric1_A1);
   chomp($Fabric1_A2);
   chomp($Base1_A1);
   chomp($Base1_A2);
   
   ##10转16进制
   my $Fabric_ZX_1=`echo "obase=16;$Fabric1_A1"|bc`;
   my $Fabric_ZX_2=`echo "obase=16;$Fabric1_A2"|bc`;
   my $Base_ZX_1=`echo "obase=16;$Base1_A1"|bc`;    
   my $Base_ZX_2=`echo "obase=16;$Base1_A2"|bc`;
   
   ##全部转换成小写 add by wangyunzeng  2012-11-06
   ##-----begin-----##
   $Fabric_ZX_1=lc($Fabric_ZX_1);
   $Fabric_ZX_2=lc($Fabric_ZX_2);
   $Base_ZX_1=lc($Base_ZX_1);
   $Base_ZX_2=lc($Base_ZX_2);
   ##------end------##
      
   chomp($Fabric_ZX_1);
   chomp($Fabric_ZX_2);
   chomp($Base_ZX_1);
   chomp($Base_ZX_2);
   
   
   ## 拼接
   my $Fabric_ZX0="0$Fabric_ZX_1:0$Fabric_ZX_2.0";
   my $Fabric_ZX1="0$Fabric_ZX_1:0$Fabric_ZX_2.1";
   my $Base_ZX0="0$Base_ZX_1:0$Fabric_ZX_2.0";
   my $Base_ZX1="0$Base_ZX_1:0$Fabric_ZX_2.1";

   
   ##MAC
   my $eth_A_MAC=`cat ifconfig.txt | grep $eth_A | head -1 | awk \-F \" \" \'\{print \$5\}\'`;
   my $eth_B_MAC=`cat ifconfig.txt | grep $eth_B | head -1 | awk \-F \" \" \'\{print \$5\}\'`;
   my $eth_C_MAC=`cat ifconfig.txt | grep $eth_C | head -1 | awk \-F \" \" \'\{print \$5\}\'`;
   my $eth_D_MAC=`cat ifconfig.txt | grep $eth_D | head -1 | awk \-F \" \" \'\{print \$5\}\'`;
   
   chomp($eth_A_MAC);
   chomp($eth_B_MAC);
   chomp($eth_C_MAC);
   chomp($eth_D_MAC);
   
   ##IP地址,修改SUSE11平台ifconfig显示大网地址在小网地址后，获取大网地址错误问题，注释掉原cat和chomp操作，2013-05-08
   #my $IP_A=`cat ifconfig.txt | grep "inet addr" | head -1  | awk -F \" \" \'\{print \$2\}\' | sed \'s\/addr\:\/\/\'`;
   my $IP_C=`cat ifconfig.txt | grep "inet addr" | sort -r | head -1  | awk -F \" \" \'\{print \$2\}\' | sed \'s\/addr\:\/\/\'`;
   #chomp($IP_A);
   chomp($IP_C);
   
   #print "\n$IP_A\n";
   #print "\n$IP_C\n";
   
   ##写bind文件
   open(BOND0,">ifcfg-bond0") || die "\nOpen file failed:$!\n\n";
      print BOND0 "BOOTPROTO='static'\n";
      print BOND0 "STARTMODE='onboot'\n";
      print BOND0 "WIRELESS='no'\n";
      print BOND0 "device='bond0'\n";
      print BOND0 "IPADDR='$IP_A'\n";
      print BOND0 "NETMASK='255.255.254.0'\n";
      print BOND0 "REMOTE_IPADDR=''\n";
      print BOND0 "BONDING_MASTER='yes'\n";
      print BOND0 "BONDING_MODULE_OPTS='mode=1 miimon=200'\n";
      
      #增加SUSE11平台网卡绑定操作
      if($cornel=~m/Server 10/i  || $cornel=~m/Server 9/i )
      {
        print BOND0 "BONDING_SLAVE0=' bus-pci-0000:$Fabric_ZX0'\n";
        print BOND0 "BONDING_SLAVE1=' bus-pci-0000:$Fabric_ZX1'\n";
      }
      elsif($cornel=~m/Server 11/i)
      {
        print BOND0 "BONDING_SLAVE0='$eth_A'\n";
        print BOND0 "BONDING_SLAVE1='$eth_B'\n";  
      }

   close(BOND0);


   
   
   open(BOND1,">ifcfg-bond1") || die "\nOpen file failed:$!\n\n";
      print BOND1 "BOOTPROTO='static'\n";
      print BOND1 "STARTMODE='onboot'\n";
      print BOND1 "WIRELESS='no'\n";
      print BOND1 "device='bond1'\n";
      print BOND1 "IPADDR='$IP_C'\n";
      print BOND1 "NETMASK='255.255.255.0'\n";
      print BOND1 "REMOTE_IPADDR=''\n";
      print BOND1 "BONDING_MASTER='yes'\n";
      print BOND1 "BONDING_MODULE_OPTS='mode=1 miimon=200'\n";
      
      #增加SUSE11平台网卡绑定操作
      if($cornel=~m/Server 10/i  || $cornel=~m/Server 9/i )
      {
        print BOND1 "BONDING_SLAVE0=' bus-pci-0000:$Base_ZX0'\n";
        print BOND1 "BONDING_SLAVE1=' bus-pci-0000:$Base_ZX1'\n"; 
      }
      elsif($cornel=~m/Server 11/i)
      {
        print BOND1 "BONDING_SLAVE0='$eth_C'\n";
        print BOND1 "BONDING_SLAVE1='$eth_D'\n";  
      }

   close(BOND1);
   
   
   ##写网卡文件
   #增加SUSE11平台支持,2013-05-08
   if($cornel=~m/Server 10/i  || $cornel=~m/Server 9/i )
   {
    open(ETHA,">ifcfg-$eth_A-id-$eth_A_MAC") || die "\nOpen file failed:$! \n\n";
   }
   elsif($cornel=~m/Server 11/i)
   {
    open(ETHA,">ifcfg-$eth_A") || die "\nOpen file ifcfg-$eth_A failed:$! \n\n";
   }
   #open(ETHA,">ifcfg-$eth_A-id-$eth_A_MAC") || die "\nOpen file failed:$! \n\n";
       print ETHA "DEVICE='$eth_A'\n";
       print ETHA "BOOTPROTO='static'\n"; 
       print ETHA "STARTMODE='onboot'\n";
   close(ETHA);
   
  if($cornel=~m/Server 10/i  || $cornel=~m/Server 9/i )
   {
    open(ETHB,">ifcfg-$eth_B-id-$eth_B_MAC") || die "\nOpen file failed:$! \n\n";
   }
   elsif($cornel=~m/Server 11/i)
   {
    open(ETHB,">ifcfg-$eth_B") || die "\nOpen file failed:$! \n\n";
   }
   #open(ETHB,">ifcfg-$eth_B-id-$eth_B_MAC") || die "\nOpen file failed:$! \n\n";
       print ETHB "DEVICE='$eth_B'\n";
       print ETHB "BOOTPROTO='static'\n";                                                 
       print ETHB "STARTMODE='onboot'\n";
   close(ETHB);
   
  if($cornel=~m/Server 10/i  || $cornel=~m/Server 9/i )
   {
    open(ETHC,">ifcfg-$eth_C-id-$eth_C_MAC") || die "\nOpen file failed:$! \n\n";
   }
   elsif($cornel=~m/Server 11/i)
   {
    open(ETHC,">ifcfg-$eth_C") || die "\nOpen file failed:$! \n\n";
   }   
   #open(ETHC,">ifcfg-$eth_C-id-$eth_C_MAC") || die "\nOpen file failed:$! \n\n";
       print ETHC "DEVICE='$eth_C'\n";
       print ETHC "BOOTPROTO='static'\n";                                                 
       print ETHC "STARTMODE='onboot'\n";
   close(ETHC);
   
  if($cornel=~m/Server 10/i  || $cornel=~m/Server 9/i )
   {
    open(ETHD,">ifcfg-$eth_D-id-$eth_D_MAC") || die "\nOpen file failed:$! \n\n";
   }
   elsif($cornel=~m/Server 11/i)
   {
    open(ETHD,">ifcfg-$eth_D") || die "\nOpen file failed:$! \n\n";
   }   
   #open(ETHD,">ifcfg-$eth_D-id-$eth_D_MAC") || die "\nOpen file failed:$! \n\n";
       print ETHD "DEVICE='$eth_D'\n";
       print ETHD "BOOTPROTO='static'\n";                                                 
       print ETHD "STARTMODE='onboot'\n";
   close(ETHD);
}

#文件清理
sub clear
{
  if($cornel=~m/Server 10/i  || $cornel=~m/Server 9/i )
  {
    ##删除原网卡配置文件
    system("rm  -f ifcfg-eth-id-*");
  }
  #elsif($cornel=~m/Server 11/i)
  #{
  #  ##删除原网卡配置文件
  #  system("rm  -f ifcfg-eth[0-9]");
  #}
  #else
  #{
  #  print "\n不支持的操作系统类型，程序退出!\n";
  #  exit
  #}

  ##清理其他文件
  unlink("eth.tmp");
  unlink("ifconfig.txt");
}
```


