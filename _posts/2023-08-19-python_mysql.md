---
layout:     post
title:      "python操作mysql数据库基础操作"
subtitle:   "python operation mysql database basic operation"
date:       2023-08-19
author:     "Gavin"
catalog:    true
tags:
    - python
    - mysql
---




# OverView

Recently in the revision mysql database, deployed a set of environments, review the installation and deployment, the basic operation of the database sql commands and backup, recovery operations. Incidentally, with the help of pyhton access to the mysql database basic operation of the package, in case of future needs.


# Code Example

```
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import MySQLdb as mdb


class MysqlDB(object):
    """ Basic methods of operating mysql databases """

    def __init__(self , host="localhost", username="root", password="", port=3306, database="MMSDB"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.con = None
        self.cur = None
        try:
            self.con = mdb.connect(host=self.host, user=self.username, passwd=self.password, port=self.port, db=self.database)
            # All queries are run on top of cursor, a module that connects to con.
            self.cur = self.con.cursor()
        except:
            raise "DataBase connect error,please check the db config."

    def close(self):
        """ Close database connection """
        if not  self.con:
            self.con.close()
        else:
            raise "DataBase doesn't connect,close connectiong error;please check the db config."

    def get_version(self):
        """ Get version info of database """
        self.cur.execute("SELECT VERSION()")
        return self.getOneData()

    def get_one_data(self):
        """ Get the result of the previous query as a single result. """
        data = self.cur.fetchone()
        return data

    def creat_table(self, tablename, attrdict, constraint):
        """
        Creating database tables

            args:
                tablename : table name
                attrdict : Attribute key-value pairs,{'book_name':'varchar(200) NOT NULL'...}
                constraint ：primary key constraint,PRIMARY KEY(`id`)
        """
        if self.isExistTable(tablename):
            return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr,value in attrdict.items():
            sql_mid = sql_mid + '`'+attr + '`'+' '+ value+','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s ('%tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print 'creatTable:'+sql
        self.executeCommit(sql)

    def execute_sql(self,sql=''):
        """
        Execute a sql statement that returns a result set against a read operation

            args:
                sql : sql statement
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchall()
            return records
        except mdb.Error,e:
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print error

    def execute_commit(self,sql=''):
        """
        Execute database sql statements and rollback for failed updates, 
        deletions, transactions, etc.
        """
        try:
            self.cur.execute(sql)
            self.con.commit()
        except mdb.Error, e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print "error:", error
            return error

    def insert(self, tablename, params):
        """
        Creating database tables

            args:
                tablename : table name
                key: attribute key
                value: value of the attribute
        """
        key = []
        value = []
        for tmpkey, tmpvalue in params.items():
            key.append(tmpkey)
            if isinstance(tmpvalue, str):
                value.append("\'" + tmpvalue + "\'")
            else:
                value.append(tmpvalue)
        attrs_sql = '('+','.join(key)+')'
        values_sql = ' values('+','.join(value)+')'
        sql = 'insert into %s'%tablename
        sql = sql + attrs_sql + values_sql
        print '_insert:'+sql
        self.executeCommit(sql)

    def select(self, tablename, cond_dict='', order='', fields='*'):
        """
        Query data from table

            args：
                tablename  : table name
                cond_dict  : query condition
                order      : sort condition

            example：
                print mydb.select(table)
                print mydb.select(table, fields=["name"])
                print mydb.select(table, fields=["name", "age"])
                print mydb.select(table, fields=["age", "name"])
        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                consql = consql+k + '=' + v + ' and'
        consql = consql + ' 1=1 '
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                raise "fields input error, please input list fields."
        sql = sql + consql + order
        print 'select:' + sql
        return self.executeSql(sql)

    def insert_many(self,table, attrs, values):
        """
        Inserting Multiple Data

            args：
                tablename  : tbale name
                attrs      : property key
                values     : attribute value

            example：
                table='test_mysqldb'
                key = ["id" ,"name", "age"]
                value = [[101, "liuqiao", "25"], [102,"liuqiao1", "26"], [103 ,"liuqiao2", "27"], [104 ,"liuqiao3", "28"]]
                mydb.insertMany(table, key, value)
        """
        values_sql = ['%s' for v in attrs]
        attrs_sql = '('+','.join(attrs)+')'
        values_sql = ' values('+','.join(values_sql)+')'
        sql = 'insert into %s'% table
        sql = sql + attrs_sql + values_sql
        print 'insertMany:'+sql
        try:
            print sql
            for i in range(0,len(values),20000):
                    self.cur.executemany(sql,values[i:i+20000])
                    self.con.commit()
        except mdb.Error,e:
            self.con.rollback()
            error = 'insertMany executemany failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print error

    def delete(self, tablename, cond_dict):
        """
        Delete data

            args：
                tablename  : table name 
                cond_dict  : Delete Conditional Dictionary

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                mydb.delete(table, params)

        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where%s" % (tablename, consql)
        print sql
        return self.executeCommit(sql)

    def update(self, tablename, attrs_dict, cond_dict):
        """
        Update data

            args:
                tablename : table name
                attrs_dict : update attribute key-value pair dictionary
                cond_dict : Update the condition dictionary

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                cond_dict = {"name" : "liuqiao", "age" : "18"}
                mydb.update(table, params, cond_dict)

        """
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            attrs_list.append("`" + tmpkey + "`" + "=" +"\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)
        print "attrs_sql:", attrs_sql
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + "`" + tablename +"`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        print sql
        return self.executeCommit(sql)

    def drop_table(self, tablename):
        """
        Drop a table

            args：
                tablename  : table name
        """
        sql = "DROP TABLE  %s" % tablename
        self.executeCommit(sql)

    def delete_table(self, tablename):
        """
        Empty database table

            args：
                tablename  : table name
        """
        sql = "DELETE FROM %s" % tablename
        self.executeCommit(sql)

    def is_exist_table(self, tablename):
        """
        Determine if a data table exists

            args:
                tablename : table name

            Return.
                True if the table exists, False if it doesn't.
        """
        sql = "select * from %s" % tablename
        result = self.executeCommit(sql)
        if result is None:
            return True
        else:
            if re.search("doesn't exist", result):
                return False
            else:
                return True
```

