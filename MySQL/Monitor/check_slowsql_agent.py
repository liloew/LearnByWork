#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sqlite3
import string
import time
import hashlib
import os.path

def init(db_file='/tmp/mysqlslow-sqlite3.db'):
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS T_SLOW(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CNT INTEGER, -- COMMENT '执行次数'
        TIME REAL, --  COMMENT 'SQL所有时间'
        ROS INTEGER, --  COMMENT '该SQL获取的记录数'
        USR TEXT, --  COMMENT '执行SQL的用户'
        SQL TEXT, --  COMMENT 'SQL文本'
        CHKTIME DATETIME DEFAULT CURRENT_TIMESTAMP, --  COMMENT '检测时间'
        SQLHASH TEXT, -- COMMENT 'SQL的SHA1键值'
        STATE INTEGER DEFAULT 0 -- COMMENT '是否已失效'
    )""")

def insert_row(db_file='/tmp/mysqlslow-sqlite3.db',slow_file='/tmp/master-slow.log.dump'):
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    record = []
    sql = ""
    SQL = "INSERT INTO T_SLOW(CNT,TIME,ROS,USR,SQL,SQLHASH) VALUES(?,?,?,?,?,?)"
    with open(slow_file,'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0:5] == '\n':
                record.append(cnt)
                record.append(ttm)
                record.append(ros)
                record.append(usr)
                record.append(sql.strip())
                record.append(hashlib.sha1(sql.strip()).hexdigest())
                cur.execute(SQL, record)
                conn.commit()
                sql = ""
                record = []
            elif line[0:5] == 'Count':
                cnt = line.split('  ')[0].split(' ')[1]
                ttm = line.split('  ')[1].split('=')[1].split('s ')[0]
                ros = line.split('  ')[3].split(', ')[0].split('=')[1].split(' ')[0]
                usr = line.split('  ')[3].split(', ')[1].split('\n')[0]
            else:
                sql += line.replace('\n',' ')

def delete(db_file='/tmp/mysqlslow-sqlite3.db'):
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    cur.execute("DELETE FROM T_SLOW WHERE ID=1")
    conn.commit()
    conn.close()

def server(db_file='/tmp/mysqlslow-sqlite3.db'):
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    host = ''
    port = 7000
    backlog = 5
    size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(backlog)
    while 1:
        client, address = s.accept()
        data = client.recv(size)
        if data[0:12]  == "GET LaSt SQL":
            cur.execute("SELECT * FROM T_SLOW WHERE STATE = 0")
            rows = cur.fetchall()
            for row in rows:
                print row
        elif data[0:6] == "UP ID:":
            cur.execute("UPDATE T_SLOW SET STATE=1 WHERE ID=?", (data.split(':')[1][:-2],))
            conn.commit()
        client.close()
    if int(time.strftime('%d')) % 10 == 0 and time.strftime('%H:%M') == '02:00':
        delete()

if __name__ == '__main__':
    if not os.path.isfile('/tmp/mysqlslow-sqlite3.db'):
        init()
    insert_row()
    server()
