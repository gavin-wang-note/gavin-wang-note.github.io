---
layout:     post
title:      "MPS API 测试用例数统计脚本"
subtitle:   "MPS 接口Test Case Count Script"
date:       2014-11-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
tags:
    - python
---


# 概述



上周写了一篇关于MPS 后端接口自动化用例设计与用例的编写，虽然有一个可视化的报告，但还缺少接口自动化测试用例分布统计信息，这次补上。当然可以集成到HTML report中，设置是CI/CD中，这样展示会更直观。





# HTML格式的统计




代码片段：

```python
#!/usr/bin/env python
#-*- coding:UTF-8 -*-

######################################
##  作用：    测试用例数统计脚本        ##
##  日期：      2014-11-09            ##
##  版本：      V1.0                  ##
##  作者：      Strayeagle            ##
##  日期：      2015-04-01            ##
##  版本：      V1.1                  ##
######################################


import os
import sys
import re
import time
from pylab import *  
import decimal
from common.stub.DataStub import DataStub
from common.util.PathUtil import getReportPath


#要处理的文件后缀名称，存入一个list中
exts = ['.py']



#所有测试用例文件列表
def all_case_files():
    test_case_files = []
    
    for root,dirs,files in os.walk(os.getcwd()):
        for fileName in files:
            #检查子目录
            if fileName.endswith('.py') and not fileName.endswith('__.py'):
                ##完整的文件路径（绝对路径）,并取lower
                fname = (root + os.sep + fileName).lower()
                test_case_files.append(fname)
                
    return  test_case_files


    
#读取文件，获取:4个空格开头， + def + 空格 + '(self):' 结尾的行记录的数量
def test_case_count(fname):
    count = 0
    for file_line in open(fname).xreadlines():
        m = re.match(r'^(\s{4})def(\s+)(test*)', file_line)
        if m is not None:
            count += 1
    return count




#所有测试用例总数
def all_case_counts(dir_tpye=None):
    count=0
    for root,dirs,files in os.walk(os.getcwd()):
        for fileName in files:
            #检查子目录
            ##完整的文件路径（绝对路径）,并取lower
            fname = (root + os.sep + fileName).lower()
            
            #测试用例的总数
            ext = fileName[fileName.rindex('.'):]
            if dir_tpye == 'all':
                try:
                    if(exts.index(ext) == 0):
                        c = test_case_count(fname)
                        count += c
                except:
                    pass
            elif dir_tpye == 'manager':
                if '_01_manager' in fname:
                    try:
                        if(exts.index(ext) == 0):
                            c = test_case_count(fname)
                            count += c
                    except:
                        pass
            elif dir_tpye == 'app':
                if '_02_app' in fname:
                    try:
                        if(exts.index(ext) == 0):
                            c = test_case_count(fname)
                            count += c
                    except:
                        pass
    return count

#获取各个用例分目录下对应的测试用例数，返回值为dict
def get_each_dir_case_count(dirList,test_case_files):
    
    case_count_dict = {}
    case_count_dict.clear()
    
    for each_case_file in test_case_files:
        for each_dir in dirList:
            if each_dir in each_case_file:
                count = test_case_count(each_case_file)
                if case_count_dict.has_key(each_dir):
                    cur_count = case_count_dict[each_dir] + count
                    after_dict = {each_dir:cur_count}
                    case_count_dict.update(after_dict)
                else:
                    case_count_dict[each_dir]=count
    
    return case_count_dict



def graph_pie(case_count_dict, pie_type=None):
    '''  绘制饼图  '''
    # make a square figure and axes   
    figure(1, figsize=(6,6))  
    labels = list(case_count_dict.keys())
    fracs = case_count_dict.values()
    
    if  pie_type == 'all':
        explode=(0, 0) 
        colors  = ["orange","green"]
        pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
        title('All TestCase', bbox={'facecolor':'0.8', 'pad':5})  
        savefig(getReportPath() + os.sep +'all_pie.png') 
        #plt.show()
        
    if  pie_type == 'manager':
        explode=(0, 0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) 
        colors  = ["pink","coral","yellow","orange","red","green","white"]
        # Pie Plot
        # autopct: format of "percent" string;
        pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
        title('Manager TestCase', bbox={'facecolor':'0.8', 'pad':5})
        savefig(getReportPath() + os.sep +'manager_pie.png')
        plt.cla()
        plt.clf()
        #plt.show()
        
    if  pie_type == 'app':
        explode=(0, 0, 0, 0)
        colors  = ["pink","coral","yellow","orange","red","green","white"]
        pie(fracs, explode=explode, labels=labels,  colors=colors, autopct='%1.1f%%', shadow=True)
        title('APP TestCase', bbox={'facecolor':'0.8', 'pad':5})  
        savefig(getReportPath() + os.sep +'app_pie.png')
        #plt.show()
        plt.cla()
        plt.clf()

def get_data():
    data = {}
    
    sql = 'select begintime,passed,total from report_history'
    select_data = DataStub().executeQuery(sql, bindParams=None)
    
    for each_data in select_data:
        rate_tmp = decimal.Decimal(each_data[1])/decimal.Decimal(each_data[-1])*100
        rate = '{0:.4}'.format(rate_tmp)
        data[each_data[0]] = rate
        
    return data


def line_draw(data):
    try:
        if len(data) <1:
            print u'SQLite查无数据，程序退出!'
            time.sleep(4)
            sys.exit()
    except:
        pass
    
    x = [i for i in range(len(data.values()))]
    y=list(data.values())
    
    # trick to get the axes
    #fig,ax = plt.subplots()
    fig = figure(figsize=(8, 4))  # image dimensions  
    ax = fig.add_subplot(111)
    ax.grid(True, color='#666666')
    xticks(size='x-small')
    yticks(size='x-small')
    axis(xmin=0)
        
    xticklabels = list(sorted(data.keys()))
    
    # plot data
    ax.plot(x,y)
    
    # set ticks and tick labels
    ax.set_xticks(x)
    
    ax.set_xticklabels(xticklabels,rotation=15)
    
    #主刻度间距设置
    if len(data) > 15 and len(data) < 60 :
        ax.xaxis.set_major_locator( MultipleLocator(3) )
    elif len(data) > 60:
        ax.xaxis.set_major_locator( MultipleLocator(5) )
        
    # 设置图的底边距
    plt.subplots_adjust(bottom = 0.15)
    
    #开启网格
    plt.grid(True)
    
    plt.xlabel('Time')
    plt.ylabel("Rate(%)")
    
    #自动调整label显示方式，如果太挤则倾斜显示
    fig.autofmt_xdate()
    
    #title('success rate', bbox={'facecolor':'0.8', 'pad':0})  
    title('success rate') 
    plt.savefig(getReportPath() + os.sep + 'rate_line.png')
    
    # show the figure
    #plt.show()
    plt.cla()
    plt.clf()

##---------------------  写报告    ------------------  ##
def write_starting_content(handle):
    handle.write('<h1>MPS - Statistical information automation</h1>\n')
    
    
def write_images(handle):
    #总用例分布，饼图
#     handle.write('<h2>The overall distribution of automated test cases</h2>\n')
#     handle.write('<img src="../report/all_pie.png" width="500px" height="500px alt="all testcase distribution graph">\n')
#     #web 后台用例分布，饼图
#     handle.write('<h2>The server automated test case distribution</h2>\n')
#     handle.write('<img src="../report/manager_pie.png" width="500px" height="500px alt="server testcase graph">\n')
#     #APP端用例分布，饼图
#     handle.write('<h2>APP automation test case distribution</h2>\n')
#     handle.write('<img src="../report/app_pie.png" width="500px" height="500px alt="app testcase graph">\n')    
#     #成功率曲线图
#     handle.write('<h2>Test case execution success ratio diagram of curves</h2>\n')
#     handle.write('<img src="../report/rate_line.png"  width="700px" height="400px alt="testcase execution rate graph">\n')




    handle.write('<div style=" float:left"><h2>Overall distribution of testcases</h2><img src="../report/all_pie.png" width="500px" height="500px alt="all testcase distribution graph"></div>')
    handle.write('<div style=" float:middle"><h2>Server testcase distribution</h2><img src="../report/manager_pie.png" width="500px" height="500px alt="server testcase graph"></div>')
    handle.write('<tr><td></td></tr>')
    handle.write('<div style=" float:left"><h2>APP testcase distribution</h2><img src="../report/app_pie.png" width="500px" height="500px alt="app testcase graph"></div>')
    handle.write('<div style=" float:middle"><h2>Testcase execution success ratio diagram of curves</h2><img src="../report/rate_line.png" width="700px" height="400px alt="testcase execution rate graph"></div>')


def write_summary_results(handle,total_testcase,manager_testcase,app_testcase):
    handle.write('<b>%s:</b> &nbsp;%s<br />\n' % ('report generated', time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
    handle.write('<h2>Results Summary</h2>')
    handle.write('<table>\n')
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('total testcases', total_testcase))
    handle.write('</table>\n')
    
    handle.write('<table>\n')
    handle.write('<tr><td><td>%s</td><td>%d</td></tr>\n' % ('- manager testcases', manager_testcase))
    handle.write('</table>\n')


    handle.write('<table>\n')
    handle.write('<tr><td><td>%s</td><td><td><td>%d</td></tr>\n' % ('- app testcases', app_testcase))
    handle.write('</table>\n') 

def write_stats_tables(handle, manager_distribution_dict,app_distribution_dict):
    handle.write('<p><br /></p>')
    handle.write('<table>\n')
    handle.write('<th>Manager testcase (Number)</th><th>APP testcase (Number)</th>\n')
    handle.write('<tr>\n')
    handle.write('<td>\n')   
    handle.write('<table>\n')
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('login', manager_distribution_dict['_login']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('account', manager_distribution_dict['_account']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('group', manager_distribution_dict['_group']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('course', manager_distribution_dict['_course']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('exam', manager_distribution_dict['_exam']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('notice', manager_distribution_dict['_notice']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('survey', manager_distribution_dict['_survey']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('registertion', manager_distribution_dict['_registration']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('classroom', manager_distribution_dict['_classroom']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('forum', manager_distribution_dict['_forum']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('news', manager_distribution_dict['_news']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('mission', manager_distribution_dict['_mission']))            
    handle.write('</table>\n')
    handle.write('</td>\n')
    handle.write('<td>\n')
    handle.write('<table>\n')
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('quick_push', app_distribution_dict['_01_quick_push']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('members', app_distribution_dict['_02_members']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('content', app_distribution_dict['_03_content']))
    handle.write('<tr><td>%s</td><td>%d</td></tr>\n' % ('news', app_distribution_dict['_02_news']))
    handle.write('</table>\n')
    handle.write('</td>\n')
    handle.write('</tr>\n')
    handle.write('</table>\n')
    
        
def write_head_html(handle):
    handle.write("""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>MPS Automated test case statistics - Results</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    <meta http-equiv="Content-Language" content="en" />
    <style type="text/css">
        body {
            background-color: #FFFFFF;
            color: #000000;
            font-family: Trebuchet MS, Verdana, sans-serif;
            font-size: 11px;
            padding: 10px;
        }
        h1 {
            font-size: 25px;
            margin-bottom: 0.5em;
            background: #FF9933;
            padding-left: 5px;
            padding-top: 2px;
        }
        h2 {
            font-size: 20px;
            background: #C0C0C0;
            padding-left: 5px;
            margin-top: 2em;
            margin-bottom: .75em;
        }
        h3 {
            font-size: 11px;
            margin-bottom: 0.5em;
        }
        h4 {
            font-size: 11px;
            margin-bottom: 0.5em;
        }
        p {
            margin: 0;
            padding: 0;
        }
        table {
            margin-left: 30px;
        }
        td {
            text-align: right;
            color: #000000;
            background: #FFFFFF;
            padding-left: 10px;
            padding-right: 8px;
            padding-bottom: 0px;
        }
        th {
            text-align: center;
            font-size: 12px;
            padding-right: 30px;
            padding-left: 30px;
            color: #000000;
            background: #C0C0C0;
        }
    </style>
</head>
<body>
""")
  


def write_closing_html(handle):
    handle.write("""\
<p><br /></p>
<hr />
</body>
</html>
""")



if __name__ == '__main__':
    
    test_case_files = all_case_files()
    
    all_dir_list = ['_01_manager','_02_app']
    manager_dir_list = ['_survey', '_account', '_course', '_classroom', '_forum', '_mission', '_login', '_notice', '_group', '_exam', '_registration', '_news'] 
    app_dir_list = ['_01_quick_push','_02_members','_03_content','_02_news']
    
    all_each_counts = get_each_dir_case_count(all_dir_list,test_case_files)
    manager_each_counts = get_each_dir_case_count(manager_dir_list,test_case_files)
    app_each_counts = get_each_dir_case_count(app_dir_list,test_case_files)
    
    #pie
    graph_pie(manager_each_counts,pie_type='manager')     # manager type pie
    graph_pie(app_each_counts,pie_type='app')             # app type pie
    graph_pie(all_each_counts,pie_type='all')             # all type pie
    #line
    data = get_data()
    line_draw(data)
    
    # write html report
    fh = open(getReportPath() + os.sep + 'Interface_Stat_Results.html', 'w')
    write_head_html(fh)
    write_starting_content(fh)
    write_summary_results(fh,all_case_counts('all'),all_case_counts('manager'),all_case_counts('app'))
    write_stats_tables(fh,manager_each_counts,app_each_counts)
    write_images(fh)
    fh.close()
```
