---
layout:     post
title:      "自动部署cosbench并提交任务与结果处理解析"
subtitle:   "Auto deoloy cosbench, submit task and analyser result"
date:       2022-01-28
author:     "Gavin"
catalog:    true
tags:
    - Cosbench
---



# 概述

每次跑S3 Performance时，总要花费蛮多时间在构造xml以及xml调测上，避免xml内容有误影响测试。

此次直接将整个过程（部署jre，部署cosbench，提交任务，自动收集存储信息以及对cosbench测试结果处理），整合成一套完整测试script，提高下工作效率。


## Script directory structure


```
[root@node243 bak_cosbench]# tree ./
./
├── 00_run.sh
├── 01_check_expect_installed.sh
├── 02_deploy_jre.sh
├── 03_deploy_cosbench.sh
├── 04_deplay_nmon.sh
├── 05_submit_cosbench_task.sh
├── 06_collect_result.sh
├── 07_analyser_cosbench_result.sh
├── 08_restart_cosbench.sh
├── config
│   ├── 100M_size_object_write_read_mix_files.xml.ini
│   ├── 10M_size_object_write_read_mix_files.xml.ini
│   ├── 120Million_only_write.xml.ini
│   ├── 1G_size_object_write_read_mix_files.xml.ini
│   ├── 1M_size_object_write_read_mix_files.xml.ini
│   ├── 500M_size_object_write_read_mix_files.xml.ini
│   ├── controller_template.conf
│   ├── dry_run.xml
│   ├── parameters.conf
│   └── small_object_write_read_mix_files.xml.ini
├── packages
│   ├── 0.4.2.c4.tar.gz
│   ├── binfmt-support_2.1.6-1_amd64.deb
│   ├── expect-5.44.1.15-5.el6_4.x86_64.rpm
│   ├── jre-8u171-linux-x64.tar.gz
│   ├── ksh-20120801-143.el7_9.x86_64.rpm
│   ├── ksh-2020.0.0-4.ky10.x86_64.rpm
│   ├── ksh_93u+20120801-2ubuntu0.16.04.1_amd64.deb
│   ├── nmon_14g+debian-1build1_amd64.deb
│   ├── nmon-16g-3.el7.x86_64.rpm
│   ├── nmonchart40.tar
│   └── tcl-8.5.7-6.el6.x86_64.rpm
├── README.md
├── subin
│   ├── expect_scp.sh
│   └── expect_ssh.sh
└── xml_files
    └── 60workers_4KB_workload.xml

4 directories, 34 files
```


# SOP

1. Prepare test environment

  * Install Kylin V10 or CentOS 7 or Ubuntu 16.04 as clients, client number is suggested same as that of gateways
  * The IP address of clients must be sequential
  * Yum/apt-get install some packages, including expect under packages dir(00_run.sh done) 
  * Install nmon,ksh on each storage nodes(00_run.sh done)



2. Create a S3 account in web UI

  * Only support S3



3. Create a pool, then set as S3 pool

  * Not care EC pool or Replicate pool



4. Enable ssh for root on Storage nodes

  * vim /etc/ssh/sshd_config to enable ssh for root(Default, after create cluster, forbidden root account to ssh)






# Content 

## parameter.conf

This conf defines items below:

1. Info of clients and storage nodes
2. Config nmonchart result path
3. Some parameter for generating cosbench XML, such as workers, runtime, ini xml files, mix ratio and so on
2. S3 AKEY&SKEY


## Script info

Scripts are usually executed by order of the number prefixed to the filename.

### 00_run.sh:

This script can be treated as a set which is constituted by the following scripts. You can modify the steps to fill the concrete requirements.


### 01_check_expect_installed.sh

This scripe is used to install some packages on each cosbench client, such as expect, tcl, nc, net-tools and sshpass.


### 02_deploy_jre.sh 

This script is used to copy jre(jre-8u171-linux-x64.tar.gz) to all clients according to parameter.conf.
Since this script uses expect to interact, it is requested to install expect has not been installed on this client.


### 03_deploy_cosbench.sh

Execute it to install cosbench on all clients if have no cosbench installed before.
If has been installed cosbench, if cosbench in running status, do nothing; if not running, will replace controller.conf then start cosbench.
The first client as cosbench controller and driver, other nodes run driver.
Will stop and disable firewall, if firewall in running status, each cosbench node can't connect to each other.


### 04_deplay_nmon.sh

Execute it to install nmon,ksh,nmonchart on all clients if have no nmon installed before.
Use nmon to collect monitor data from each storage node.
nmonchart needs ksh, so install ksh on each storage node.
Use nmonchart to chart nmon data on each storage node. 
    (1) After charted, mush be opened by Google browser
    (2) Needs to be able to access Google because needs Google plug-ins online(Can use nmon analyser to save excel)


### 05_submit_cosbench_task.sh

Execute it to generate cosbench xml, then submit cosbench task, then run nmon to monitor storage on each storage node.
Support dry run or not, suggest to dry run, prevent problems in direct running, and run completely after ensuring that there are no problems in the whole process.


### 06_collect_result.sh

Execute it to collect nmon result from storage nodes


### 07_analyser_cosbench_result.sh

Execute it to analyser cosbench rest result on cosbench controller node

### 08_restart_cosbench.sh

If wants to restart all of cosbench service, you can run this script to do it.
This action will not clean archive and log on each cosbench node by default, if to delete archive or log dir, should pass a parameter to shell, like as:./08_restart_cosbench.sh del.


### config/

```
controller_template.conf --> Generate controller.conf then sync to the controller node
dry_run.xml                                    --> For dry run
1M_size_object_write_read_mix_files.xml.ini    --> Template of cosbench xml to generate cosbench task of xml files (Under xml_files)
10M_size_object_write_read_mix_files.xml.ini   --> Template of cosbench xml to generate cosbench task of xml files (Under xml_files)
100M_size_object_write_read_mix_files.xml.ini  --> Template of cosbench xml to generate cosbench task of xml files (Under xml_files)
500M_size_object_write_read_mix_files.xml.ini  --> Template of cosbench xml to generate cosbench task of xml files (Under xml_files)
1G_size_object_write_read_mix_files.xml.ini    --> Template of cosbench xml to generate cosbench task of xml files (Under xml_files)
120Million_only_write.xml.ini                  --> Template of cosbench xml to generate cosbench task of xml files (Under xml_files)
small_object_write_read_mix_files.xml.ini      --> Template of cosbench xml to generate cosbench task of xml files (Under xml_files)
```

For cosbench xml files(under xml_files), can decide the running sequence by specfying proper filename.

### packages/

Include expect, nmon, nmonchart, ksh and other tools.

#### subin/

Some internal functions used by scripts.


# An example of script output


```
root@node243:~/cosbench# ./06_analyser_cosbench_result.sh 

----------------------------------------------------------------------------------- 
w1-QA_30workers_4K_30M_files_mix, cost_time:6H:22M:54S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4844.17         19.8417         6.05333              6.05333             
READ         3750.24         15.361          7.99                 7.94                
MIX_WRITE    1615.27         6.61614         10.1133              10.1133             
MIX_READ     1615.91         6.61874         8.31667              8.26333             
MIX_SUM      3231.18         13.2349         9.215                9.18833             

----------------------------------------------------------------------------------- 
w2-QA_30workers_100K_30M_files_mix, cost_time:6H:42M:30S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4020.6          411.709         7.32333              6.24667             
READ         3060.55         313.4           9.79667              8.9                 
MIX_WRITE    1378.69         141.178         11.5067              10.3833             
MIX_READ     1380.04         141.316         10.1067              9.17667             
MIX_SUM      2758.73         282.494         10.8067              9.78                

----------------------------------------------------------------------------------- 
w3-QA_30workers_200K_30M_files_mix, cost_time:7H:27M:26S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        3300.63         675.969         8.96333              7.02333             
READ         2171.91         444.807         13.8033              12.14               
MIX_WRITE    1103.61         226.021         13.14                11.0667             
MIX_READ     1103.17         225.929         13.9167              12.15               
MIX_SUM      2206.78         451.95          13.5283              11.6083             

----------------------------------------------------------------------------------- 
w4-QA_30workers_1024K_1M_Size_file_mix, cost_time:1H:46M:52S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        1377.91         1444.84         21.67                12.9667             
READ         1131.47         1186.44         26.5067              18.1567             
MIX_WRITE    555.8           582.804         25.1833              17.31               
MIX_READ     553.6           580.493         28.79                20.2333             
MIX_SUM      1109.4          1163.3          26.9867              18.7717             

----------------------------------------------------------------------------------- 
w5-QA_30workers_10240K_10M_Size_file_mix, cost_time:1H:13M:25S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        204.93          2148.8          146.457              90.3733             
READ         264.15          2769.83         113.58               60.35               
MIX_WRITE    108.17          1134.28         155.517              107.767             
MIX_READ     108.23          1134.85         121.68               70.4                
MIX_SUM      216.4           2269.13         138.598              89.0833             

----------------------------------------------------------------------------------- 
w6-QA_30workers_1048576K_1G_Size_file_mix, cost_time:1H:0M:43S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        3.02            3242.78         9933.77              595.353             
READ         5.64            6063.25         5313.1               173.7               
MIX_WRITE    1.97            2113.94         10108.3              656.83              
MIX_READ     1.98            2128.27         5094.47              188.393             
MIX_SUM      3.95            4242.21         7601.37              422.612             

----------------------------------------------------------------------------------- 
w7-QA_60workers_4K_30M_files_mix, cost_time:5H:46M:56S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        7500.32         30.7213         7.86333              7.86                
READ         6762.72         27.7001         8.86667              8.81333             
MIX_WRITE    2714.85         11.12           13.1667              13.1667             
MIX_READ     2714.38         11.1181         8.8                  8.74667             
MIX_SUM      5429.23         22.2381         10.9833              10.9567             

----------------------------------------------------------------------------------- 
w8-QA_60workers_100K_30M_files_mix, cost_time:6H:5M:42S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        5878.1          601.918         10.07                8.96                
READ         5407.74         553.752         11.0867              10.19               
MIX_WRITE    2345.29         240.157         14.3533              13.25               
MIX_READ     2342.65         239.887         11.1033              10.17               
MIX_SUM      4687.94         480.044         12.7283              11.71               

----------------------------------------------------------------------------------- 
w9-QA_60workers_200K_30M_files_mix, cost_time:6H:35M:58S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4841.97         991.636         12.2533              10.0967             
READ         3732.87         764.49          16.0667              14.4033             
MIX_WRITE    1911.44         391.463         15.9167              13.9                
MIX_READ     1910.73         391.317         15.3533              13.6167             
MIX_SUM      3822.17         782.78          15.635               13.7583             

----------------------------------------------------------------------------------- 
w10-QA_60workers_1024K_1M_Size_file_mix, cost_time:1H:32M:31S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        2286.75         2397.82         26.1367              17.3733             
READ         2057.05         2156.98         29.1633              21.0633             
MIX_WRITE    970.74          1017.9          28.4233              20.61               
MIX_READ     971.96          1019.17         33.2367              25.2167             
MIX_SUM      1942.7          2037.07         30.83                22.9133             

----------------------------------------------------------------------------------- 
w11-QA_60workers_10240K_10M_Size_file_mix, cost_time:1H:2M:21S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        351.36          3684.35         170.743              112.857             
READ         463.98          4865.07         129.313              74.13               
MIX_WRITE    181.99          1908.39         185.35               133.583             
MIX_READ     181.88          1907.17         144.337              89.06               
MIX_SUM      363.87          3815.56         164.843              111.322             

----------------------------------------------------------------------------------- 
w12-QA_60workers_1048576K_1G_Size_file_mix, cost_time:0H:54M:29S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4.88            5244.88         12283.6              796.11              
READ         8.17            8773.49         7343.07              289.537             
MIX_WRITE    3.08            3309.76         12663.9              908.077             
MIX_READ     3.07            3298.88         6822.43              307.493             
MIX_SUM      6.15            6608.64         9743.18              607.785             

----------------------------------------------------------------------------------- 
w13-QA_90workers_4K_30M_files_mix, cost_time:5H:43M:51S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        8321.29         34.084          10.6733              10.6733             
READ         9075.99         37.1753         9.90667              9.85333             
MIX_WRITE    3224.43         13.2073         18.1733              18.1733             
MIX_READ     3223.7          13.2043         9.60667              9.55333             
MIX_SUM      6448.13         26.4116         13.89                13.8633             

----------------------------------------------------------------------------------- 
w14-QA_90workers_100K_30M_files_mix, cost_time:5H:50M:24S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6638.6          679.793         13.4167              12.3433             
READ         7174.2          734.637         12.5367              11.6167             
MIX_WRITE    2848.65         291.702         19.08                17.94               
MIX_READ     2847.38         291.571         12.3867              11.43               
MIX_SUM      5696.03         583.273         15.7333              14.685              

----------------------------------------------------------------------------------- 
w15-QA_90workers_200K_30M_files_mix, cost_time:6H:27M:17S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        5517.32         1129.95         16.1767              14.0433             
READ         4825.51         988.266         18.6433              16.97               
MIX_WRITE    2412.23         494.026         20.0233              17.95               
MIX_READ     2410.53         493.676         17.1667              15.38               
MIX_SUM      4822.76         987.702         18.595               16.665              

----------------------------------------------------------------------------------- 
w16-QA_90workers_1024K_1M_Size_file_mix, cost_time:1H:28M:31S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        2749.42         2882.99         32.6367              24.3267             
READ         2716.61         2848.58         33.1233              25.18               
MIX_WRITE    1261.77         1323.06         33.17                25.36               
MIX_READ     1260.83         1322.08         38.08                30.1033             
MIX_SUM      2522.6          2645.14         35.625               27.7317             

----------------------------------------------------------------------------------- 
w17-QA_90workers_10240K_10M_Size_file_mix, cost_time:0H:59M:48S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        441.86          4633.24         203.613              146.33              
READ         618.08          6481.08         145.607              88.1033             
MIX_WRITE    229.29          2404.25         226.43               173.55              
MIX_READ     228.46          2395.61         166.75               109.23              
MIX_SUM      457.75          4799.86         196.59               141.39              

----------------------------------------------------------------------------------- 
w18-QA_90workers_1048576K_1G_Size_file_mix, cost_time:0H:52M:54S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        5.79            6215.07         15550.1              1077.36             
READ         8.92            9568.5          10100.1              395.867             
MIX_WRITE    3.57            3834.26         16124.7              1270.8              
MIX_READ     3.54            3798.35         9215.03              424.67              
MIX_SUM      7.11            7632.61         12669.9              847.737             

----------------------------------------------------------------------------------- 
w19-QA_120workers_4K_30M_files_mix, cost_time:5H:39M:31S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        8870.99         36.3356         13.39                13.39               
READ         10861.7         44.4896         11.04                10.99               
MIX_WRITE    3566.18         14.6071         23.3                 23.3                
MIX_READ     3564            14.5982         10.22                10.16               
MIX_SUM      7130.18         29.2053         16.76                16.73               

----------------------------------------------------------------------------------- 
w20-QA_120workers_100K_30M_files_mix, cost_time:5H:49M:25S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        7035.11         720.395         16.9133              15.81               
READ         8539.16         874.411         14.0433              13.1233             
MIX_WRITE    3174.51         325.07          24.3433              23.2233             
MIX_READ     3175.41         325.162         13.32                12.3567             
MIX_SUM      6349.92         650.232         18.8317              17.79               

----------------------------------------------------------------------------------- 
w21-QA_120workers_200K_30M_files_mix, cost_time:6H:20M:43S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        5936.71         1215.84         20.0867              18.08               
READ         5625.23         1152.05         21.3233              19.6533             
MIX_WRITE    2737.41         560.621         25.1433              23.0967             
MIX_READ     2732.54         559.625         18.5967              16.7933             
MIX_SUM      5469.95         1120.25         21.87                19.945              

----------------------------------------------------------------------------------- 
w22-QA_120workers_1024K_1M_Size_file_mix, cost_time:1H:26M:48S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        3042.73         3190.53         39.3433              31.2733             
READ         3240.65         3398.06         37.02                29.3                
MIX_WRITE    1461.43         1532.42         39.86                32.18               
MIX_READ     1459.29         1530.18         42.2033              34.4067             
MIX_SUM      2920.72         3062.6          41.0317              33.2933             

----------------------------------------------------------------------------------- 
w23-QA_120workers_10240K_10M_Size_file_mix, cost_time:0H:58M:43S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        485.49          5090.78         247.103              191.573             
READ         721.01          7560.35         166.423              106.4               
MIX_WRITE    258.56          2711.11         274.45               220.973             
MIX_READ     259.18          2717.8          189.177              129.63              
MIX_SUM      517.74          5428.91         231.813              175.302             

----------------------------------------------------------------------------------- 
w24-QA_120workers_1048576K_1G_Size_file_mix, cost_time:0H:52M:30S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6.16            6618.53         19470.7              1419.07             
READ         9.43            10130.3         12720.5              486.747             
MIX_WRITE    3.65            3928.62         20438.5              1707.93             
MIX_READ     3.8             4079.41         11920.9              535.357             
MIX_SUM      7.45            8008.03         16179.7              1121.64             

[WARN]  Task : (w25-1200million_4k_data_filling) status is not finished, but : (terminated), please pay more attention 


[WARN]  Task : (w26-1200million_4k_data_filling) status is not finished, but : (terminated), please pay more attention 


[WARN]  Task : (w27-120million_4k_data_filling) status is not finished, but : (terminated), please pay more attention 


[WARN]  Task : (w28-120million_4k_data_filling) status is not finished, but : (cancelled), please pay more attention 


Task: (w29-120million_4k_data_filling), write total objects: (120000000), cost time: (14195(s)), write speed: (8453.68) 


[WARN]  Task : (w30-QA_120workers_4K_30M_files_mix) status is not finished, but : (cancelled), please pay more attention 


----------------------------------------------------------------------------------- 
w31-QA_120workers_4K_30M_files_mix, cost_time:6H:3M:26S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        5388.65         22.0719         22.1933              22.1933             
READ         11093.4         45.4386         10.81                10.76               
MIX_WRITE    3714.16         15.2132         22.7667              22.7667             
MIX_READ     3711.56         15.2025         9.40333              9.35                
MIX_SUM      7425.72         30.4157         16.085               16.0583             

----------------------------------------------------------------------------------- 
w32-QA_120workers_100K_30M_files_mix, cost_time:5H:27M:24S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        7803.41         799.069         15.2333              14.1267             
READ         8556.41         876.177         14.0167              13.1067             
MIX_WRITE    3406.95         348.871         22.28                21.1367             
MIX_READ     3406.42         348.817         12.8033              11.8367             
MIX_SUM      6813.37         697.688         17.5417              16.4867             

----------------------------------------------------------------------------------- 
w33-QA_120workers_200K_30M_files_mix, cost_time:5H:54M:16S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6372.15         1305.02         18.6967              16.5867             
READ         5594.51         1145.76         21.4433              19.7367             
MIX_WRITE    2853.54         584.404         23.5533              21.4633             
MIX_READ     2849.95         583.669         18.3933              16.5333             
MIX_SUM      5703.49         1168.07         20.9733              18.9983             

----------------------------------------------------------------------------------- 
w34-QA_120workers_1024K_1M_Size_file_mix, cost_time:1H:20M:49S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        3349.24         3511.92         35.7333              27.55               
READ         3228.21         3385.03         37.1633              29.3633             
MIX_WRITE    1532.84         1607.3          34.9367              27.1433             
MIX_READ     1537.16         1611.83         43.1167              35.1867             
MIX_SUM      3070            3219.13         39.0267              31.165              

----------------------------------------------------------------------------------- 
w35-QA_120workers_10240K_10M_Size_file_mix, cost_time:0H:55M:8S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        537.52          5636.43         223.167              164.657             
READ         738.94          7748.37         162.39               102.293             
MIX_WRITE    251.73          2639.46         276.8                221.483             
MIX_READ     252.38          2646.39         199.35               138.473             
MIX_SUM      504.11          5285.85         238.075              179.978             

----------------------------------------------------------------------------------- 
w36-QA_120workers_1048576K_1G_Size_file_mix, cost_time:0H:50M:14S                    
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6.91            7414.56         17379.5              1282.79             
READ         9.36            10045           12829.2              436.01              
MIX_WRITE    3.79            4072.14         19156.8              1636.76             
MIX_READ     3.92            4208.96         12083.9              543.213             
MIX_SUM      7.71            8281.1          15620.4              1089.99             

Task: (w37-120million_4k_data_filling), write total objects: (120000000), cost time: (13965(s)), write speed: (8592.91) 


----------------------------------------------------------------------------------- 
w40-QA_DRY_RUN_30workers_4K_30M_files_mix, cost_time:0H:2M:9S                      
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4098.54         16.7876         6.97333              6.97333             
READ         10856.8         44.4696         2.75667              2.69667             
MIX_WRITE    2143.91         8.78142         7.10667              7.10667             
MIX_READ     5025.76         20.5855         2.87333              2.82                
MIX_SUM      7169.67         29.3669         4.99                 4.96333             

----------------------------------------------------------------------------------- 
w41-QA_DRY_RUN_30workers_100K_30M_files_mix, cost_time:0H:2M:12S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4688.9          480.144         6.24667              5.12333             
READ         8137.48         833.279         3.68                 2.85333             
MIX_WRITE    1670.89         171.099         8.70667              7.66                
MIX_READ     3881.14         397.428         3.91667              3.04667             
MIX_SUM      5552.03         568.527         6.31167              5.35333             

----------------------------------------------------------------------------------- 
w43-QA_DRY_RUN_30workers_4K_30M_files_mix, cost_time:0H:2M:12S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6433.48         26.3515         4.53                 4.53                
READ         11056.4         45.2869         2.70667              2.65333             
MIX_WRITE    2145.06         8.78618         7.1                  7.1                 
MIX_READ     5018.76         20.5568         2.88                 2.82667             
MIX_SUM      7163.82         29.343          4.99                 4.96333             

----------------------------------------------------------------------------------- 
w48-QA_DRY_RUN_30workers_4K_30M_files_mix, cost_time:0H:2M:16S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6500.63         26.6266         4.47333              4.47333             
READ         11065           45.3222         2.70333              2.65333             
MIX_WRITE    2131.74         8.73162         7.17333              7.17333             
MIX_READ     4972.22         20.3662         2.89                 2.83333             
MIX_SUM      7103.96         29.0978         5.03167              5.00333             

----------------------------------------------------------------------------------- 
w49-QA_DRY_RUN_30workers_4K_30M_files_mix, cost_time:0H:2M:14S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6492.76         26.5944         4.48                 4.48                
READ         11006.1         45.0812         2.71333              2.66                
MIX_WRITE    2126.64         8.71073         7.17333              7.17333             
MIX_READ     4988.68         20.4336         2.89                 2.83333             
MIX_SUM      7115.32         29.1443         5.03167              5.00333             

----------------------------------------------------------------------------------- 
w50-QA_DRY_RUN_30workers_100K_30M_files_mix, cost_time:0H:2M:17S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4912.96         503.087         5.97                 4.88333             
READ         8085.7          827.976         3.70333              2.89                
MIX_WRITE    1668.04         170.808         8.7                  7.65333             
MIX_READ     3904.94         399.866         3.90333              3.03                
MIX_SUM      5572.98         570.674         6.30167              5.34167             

----------------------------------------------------------------------------------- 
w51-QA_DRY_RUN_30workers_200K_30M_files_mix, cost_time:0H:2M:19S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        3957.27         810.449         7.45333              5.58667             
READ         6894.38         1411.97         4.34333              2.94667             
MIX_WRITE    1386.41         283.936         10.4267              8.61                
MIX_READ     3239.48         663.446         4.74                 3.18                
MIX_SUM      4625.89         947.382         7.58333              5.895               

----------------------------------------------------------------------------------- 
w52-QA_DRY_RUN_30workers_1024K_30M_files_mix, cost_time:0H:2M:18S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        1434.56         1504.25         20.8067              12.1233             
READ         2703.91         2835.25         11.0867              4.41                
MIX_WRITE    601.08          630.281         22.06                14.8167             
MIX_READ     1412.91         1481.54         11.8                 4.75667             
MIX_SUM      2013.99         2111.82         16.93                9.78667             

----------------------------------------------------------------------------------- 
w53-QA_DRY_RUN_30workers_10240K_30M_files_mix, cost_time:0H:2M:33S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        198.32          2079.51         151.25               87.06               
READ         335.44          3517.29         89.4633              27.0367             
MIX_WRITE    89.43           937.714         145.71               96.7367             
MIX_READ     218.16          2287.54         77.7433              25.52               
MIX_SUM      307.59          3225.25         111.727              61.1283             

----------------------------------------------------------------------------------- 
w54-QA_DRY_RUN_30workers_4K_30M_files_mix, cost_time:0H:2M:17S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        6181.75         25.3205         4.71                 4.71                
READ         11059.2         45.2983         2.70667              2.65667             
MIX_WRITE    2117.66         8.67393         7.29333              7.29333             
MIX_READ     4926.28         20.178          2.88                 2.83333             
MIX_SUM      7043.94         28.8519         5.08667              5.06333             

----------------------------------------------------------------------------------- 
w55-QA_DRY_RUN_30workers_100K_30M_files_mix, cost_time:0H:2M:19S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4950.13         506.893         5.92333              4.83                
READ         8129.49         832.46          3.68333              2.85333             
MIX_WRITE    1650.2          168.981         8.92                 7.87                
MIX_READ     3839.86         393.201         3.92                 3.04                
MIX_SUM      5490.06         562.182         6.42                 5.455               

----------------------------------------------------------------------------------- 
w56-QA_DRY_RUN_30workers_200K_30M_files_mix, cost_time:0H:2M:20S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        4048.56         829.145         7.28                 5.38667             
READ         6835.65         1399.94         4.38333              2.95                
MIX_WRITE    1395.3          285.759         10.3233              8.49333             
MIX_READ     3263.39         668.343         4.72333              3.15333             
MIX_SUM      4658.69         954.102         7.52333              5.82333             

----------------------------------------------------------------------------------- 
w57-QA_DRY_RUN_30workers_1024K_30M_files_mix, cost_time:0H:2M:21S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        1470.29         1541.7          20.3033              11.7467             
READ         2693.39         2824.22         11.1367              4.42333             
MIX_WRITE    602.11          631.362         22.18                14.8933             
MIX_READ     1401.31         1469.38         11.8333              4.77667             
MIX_SUM      2003.42         2100.74         17.0067              9.835               

----------------------------------------------------------------------------------- 
w58-QA_DRY_RUN_30workers_10240K_30M_files_mix, cost_time:0H:2M:35S                     
             IOPS            BW(MB/s)        avg_res_time(ms)     avg_proc_time(ms)   
WRITE        200.65          2103.96         149.527              85.38               
READ         339.92          3564.32         88.26                27.0233             
MIX_WRITE    92.2            966.762         146.957              96.5833             
MIX_READ     208.41          2185.4          78.9067              25.44               
MIX_SUM      300.61          3152.16         112.932              61.0117             
root@node243:~/cosbench# 

```