---
layout:     post
title:      "Oracle案例--sqlldr导入数据报错"
subtitle:   "Oracle troubleshoot--sqlldr import data error"
date:       2010-06-07
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

qlldr导入数据报错

# 表象

```
Record 47: Rejected - Error on table NAPTR_MMS, column SEQUENCENO.   
Column not found before end of logical record (use TRAILING NULLCOLS)
Record 48: Rejected - Error on table NAPTR_MMS, column SEQUENCENO.   
Column not found before end of logical record (use TRAILING NULLCOLS)
Record 49: Rejected - Error on table NAPTR_MMS, column SEQUENCENO.   
Column not found before end of logical record (use TRAILING NULLCOLS)
Record 50: Rejected - Error on table NAPTR_MMS, column SEQUENCENO.   
Column not found before end of logical record (use TRAILING NULLCOLS)
Record 51: Rejected - Error on table NAPTR_MMS, column SEQUENCENO.   
Column not found before end of logical record (use TRAILING NULLCOLS)
```

# 原因

因为要导入的trim_naptr_datafile.xls文件中，列字段是不定长的，需要使用trailing nullcols。

# 解决方法

```
Load      data　                                             
infile      '/opt/oracle/trim_naptr_datafile.xls'            
append  into  table  NAPTR_MMS                               
fields  terminated  by  '|'  
TRAILING NULLCOLS                                
(                                                            
   E164NUMBER  CHAR,                                             
   PRIORITY    ,                                             
   PREFERENCE  ,                                             
　  FLAGS        CHAR,                                           
   SERVICES    CHAR,                                             
   REGEXP      CHAR,                                             
   REPLACEMENT CHAR,                                             
   SEQUENCENO  CHAR,                                             
   TTL  
)
```

在ctl文件中增加了"TRAILING NULLCOLS "这行内容。

