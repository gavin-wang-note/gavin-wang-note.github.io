---
layout:     post
title:      "Testlink support Excel import/export test cases"
subtitle:   "Testlink support Excel import/export test cases"
date:       2023-05-19
author:     "Gavin"
catalog:    true
tags:
    - Testlink
    - Python 
---


# Overview

Testlink is used for writing and maintaining manual test cases. Sometimes, in order to write more efficiently, you need to export the Testlink Excel template, edit Excel directly on this basis, and finally import it to Testlink. XML is similar, but it happens that Testlink only supports import and export of XML files, not Excel.

Therefore, this article provides a python script that allows Test to support the import and export of Excel.

This article ignores the part that involves modifications to Testlink; this article only provides the python script:

It includes two tools, one is to transfer xml to excel, the other is to do the opposite
Testlink version using with this tool is TestLink 1.9.10(El D1eG0).

*  **LIMITATION: excel2testlinkxml.py supports at most 2-layer hierarchy for now.**

```
TestSuite
 > Subsuite1 
   >> TestCase1
   >> TestCase2
 > Subsuite2
   >> TestCase1
   >> TestCase2
 > Subsuite3 
   >> TestCase1
   >> TestCase2
```


# Scripts

## excel2testlinkxml

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xlrd
from lxml import etree


input=raw_input("Input file name:")
# test_suite_name=raw_input("Input test suite name:")
# if test_suite_name=='':
    # test_suite_name="Gateway VM Deployment"

f_in = xlrd.open_workbook(input)
sheet = f_in.sheet_by_index(0)

# create XML
#testsuite = etree.Element('testsuite', name=test_suite_name)

xmlroot = None

for seq in range(1, sheet.nrows):
    # print(sheet.row_values(seq))
    print seq
    try:
        suite_ = sheet.row_values(seq)[0]
        case_ = sheet.row_values(seq)[1]
        pre_ = sheet.row_values(seq)[2]
        step_ = sheet.row_values(seq)[3]
        expect_ = sheet.row_values(seq)[4]
        keywords_ = sheet.row_values(seq)[5]
        
        
        if suite_ != '':
            if xmlroot == None:
                xmlroot = etree.Element('testsuite', name=suite_)
                testsuite_ = xmlroot
            else:
                testsuite_ = etree.SubElement(xmlroot, 'testsuite', name=suite_)
            continue
        if case_ == '':
            continue
        
        # To make lines
        pre_ = '<![CDATA[<p>\n' + pre_.replace('\n','</p>\n<p>\n') + '</p>\n]]>'
        step_ = '<![CDATA[<p>\n' + step_.replace('\n','</p>\n<p>\n') + '</p>\n]]>'
        expect_ = '<![CDATA[<p>\n' + expect_.replace('\n','</p>\n<p>\n') + '</p>\n]]>'
        
        test_case = etree.SubElement(testsuite_, 'testcase', name=case_)
        preconditions = etree.SubElement(test_case, 'preconditions')
        preconditions.text = u'{0}'.format(pre_)
        steps = etree.SubElement(test_case, 'steps')
        step = etree.SubElement(steps, 'step')
        step_number = etree.SubElement(step, 'step_number')
        step_number.text = u'1'
        actions = etree.SubElement(step, 'actions')
        actions.text = u'{0}'.format(step_)
        expectedresults = etree.SubElement(step, 'expectedresults')
        expectedresults.text = u'{0}'.format(expect_)
        keywords = etree.SubElement(test_case, 'keywords')
        keyword_list = keywords_.split('\n')
        for kw in keyword_list:
            keyword = etree.SubElement(keywords, 'keyword', name=kw)
    except Exception as e:
        print("line:", seq)
        print(str(e))
        for item in sys.exc_info():
            print item

s = etree.tostring(xmlroot, pretty_print=True)
s = s.replace('&lt;', '<')   # 临时强制修改，将来碰到内容中包含大于小于的可能会导致XML格式错误，导入失败。
s = s.replace('&gt;', '>')
f_out = open('output.xml', 'w')
f_out.write(s)
```


## testlinkxml2excel

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
from collections import OrderedDict
from xlwt import Workbook
from lxml import etree

pattern = re.compile(r'<p>\n</p>\n|</p>|<p>\n')


class XML2ExcelManager:

    def __init__(self, xml_file_name):
        self._tree = etree.parse(xml_file_name)
        self.root = self._tree.getroot()
#        suite_depth = 0
        self.content = []
        
    def xmlnode_to_list(self, node):
        columns = (
           ("suitename", ""),
           ("casename", ""),
           ("preconditions", ""),
           ("steps", ""),
           ("expected", ""),
           ("keywords", ""),
           ("caseid", "")
        )
        line = OrderedDict(columns)
        if node.tag == 'testsuite':
            line["suitename"] = node.get("name")
            self.content.append(line)
        if node.tag == 'testcase':
            line["casename"] = node.get("name")
            line["caseid"] = node.find("externalid").text
            line["preconditions"] = node.find("preconditions").text
            line["steps"] = node.find("steps/step/actions").text \
                if node.find("steps/step/actions") is not None else ""
            line["expected"] = node.find("steps/step/expectedresults").text \
                if node.find("steps/step/expectedresults") is not None else ""
            line["keywords"] = []
            for keyword in node.findall("keywords/keyword"):
                line["keywords"].append(keyword.get("name"))
            self.content.append(line)
        for child in node.getchildren():
            self.xmlnode_to_list(child)

    def write_list_to_excel(self, excel_file_name):
        excel = Workbook()
        sheet1 = excel.add_sheet('Sheet1')
        # write title name
        row = sheet1.row(0)
        for idx, key in enumerate(self.content[0]):
            row.write(idx, key)

        for i in range(len(self.content)):
            row = sheet1.row(i+1)  # Offset for title
            for idx, key in enumerate(self.content[i]):
                val = self.content[i][key]
                if key != "keywords":  # Because keywords is list, not string
                    val = pattern.sub('', val)
                else:
                    val = '\n'.join(val)
                row.write(idx, val)
        excel.save(excel_file_name)

if __name__ == '__main__':
    f_xml = raw_input("Input xml name:")
    xem = XML2ExcelManager(f_xml)
    xem.xmlnode_to_list(xem.root)
    xem.write_list_to_excel('output.xls')

```
