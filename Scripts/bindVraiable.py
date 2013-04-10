#!/usr/bin/python
# coding=utf-8
import cx_Oracle

dsn  = cx_Oracle.makedsn('192.168.88.198',"1521",'lilo')
conn = cx_Oracle.connect('lilo','lilo',dsn)
# For DBA friendly : Clientinfo,Module and Action
conn.clientinfo = 'Python 2.4 on RedHat 5.4'
conn.module     = 'cx_Oracle demo'
conn.action     = 'BatchJob #1'

# 此处同时测试了打开多个游标的情况
cursor1 = conn.cursor()
cursor2 = conn.cursor()
# 有表T2:
       # ID NAME
       # 123 lilo
       # 124 Li Luo
       # 125 Luo Li
       # 126 Test
       # 201 Hello
       # 202 World

# 定义绑定变量
bindV = {'id': 125, 'name':'Luo Li'}
query = "select * from t2 where ID = :id and NAME = :name"

result = cursor1.execute(query, bindV)
rows   = result.fetchall()
print '''第一个绑定变量查询:
'''
for row in rows:
        print row 

query  = "select * from t2 where ID = :id or NAME = :name"
result = cursor2.execute(query, ID=124, NAME='lilo')
rows   = result.fetchall()
print '''第二个绑定变量查询:
'''
for row in rows:
        print row 

conn.close()