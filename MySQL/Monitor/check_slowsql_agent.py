#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import time
import socket
import sqlite3
import string
import hashlib
import os.path
import subprocess

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
    cur.execute("""CREATE TABLE IF NOT EXISTS T_SLOW_FILE(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FILENAME TEXT, -- COMMENT '处理的SLOW LOG文件名'
        CHKTIME DATETIME DEFAULT CURRENT_TIMESTAMP --  COMMENT '检测时间'
    )""")
    conn.commit()
    conn.close()

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
                conn = sqlite3.connect(db_file)
                cur  = conn.cursor()
                cur.execute(SQL, record)
                conn.commit()
                conn.close()
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

def slow_dump(in_file="",out_file=""):
    """`in_file` the MySQL Slow log file
        `out_file` the MySQL Slow dump file
    """
    f = open(out_file, 'w')
    p = subprocess.Popen('/usr/bin/mysqldumpslow ' + in_file, shell=True, universal_newlines=True, stdout=f)
    ret_code = p.wait()
    f.flush()
    f.close()
    return ret_code

def find_slow_file(path=".", db_file="/tmp/mysqlslow-sqlite3.db"):
    """ `path` the MySQL datadir
        `db_file` the SQLite3 db file.
    """
    files = next(os.walk(path))[2]
    filelist = list()
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    pattern = re.compile(r".*slow.*\d{8}$")
    for f in files:
        if pattern.search(f):
            filelist.append(os.path.join(path, f))
    for f in filelist:
        cur.execute("SELECT COUNT(*) FROM T_SLOW_FILE WHERE FILENAME = ?", (f,))
        row = cur.fetchone()
        if row[0] == 0:
            cur.execute("INSERT INTO T_SLOW_FILE(FILENAME) VALUES(?)", (f,))
            conn.commit()
            slow_dump(f, "/tmp/" + f.split("/")[-1] + ".dump")
            insert_row(slow_file="/tmp/" + f.split("/")[-1] + ".dump")
    conn.close()

def server(db_file='/tmp/mysqlslow-sqlite3.db'):
    host = ''
    port = 7000
    backlog = 5
    size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(backlog)
    while 1:
        if time.strftime('%M') == '00':
            find_slow_file("/var/lib/mysql")
        client, address = s.accept()
        data = client.recv(size)
        conn = sqlite3.connect(db_file)
        cur  = conn.cursor()
        tmprow = ''
        lastrow = ''
        if data[0:12]  == "GET LaSt SQL":
            cur.execute("SELECT * FROM T_SLOW WHERE STATE = 0")
            rows = cur.fetchall()
            for row in rows:
                tmprow = '\t'.join(str(w) for w in row)
                lastrow = '\n'.join((tmprow,lastrow))
            client.send(lastrow)
        elif data[0:6] == "UP ID:":
            print "UPDATE T_SLOW SET STATE=1 WHERE ID={0}".format(data.split(':')[1])
            cur.execute("UPDATE T_SLOW SET STATE=1 WHERE ID=?", (data.split(':')[1],))
            conn.commit()
            client.send("ID: " + data.split(':')[1] + " has been executed.")
        client.close()
        conn.close()
        if int(time.strftime('%d')) % 10 == 0 and time.strftime('%H:%M') == '02:00':
            delete()


if __name__ == '__main__':
    if not os.path.isfile('/tmp/mysqlslow-sqlite3.db'):
        init()
    server()
