#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import time
import socket
import MySQLdb
import pymongo
import datetime
import MySQLdb.cursors

def check_slow_table(host="localhost",port=3306,user="root", passwd="password",db="mysql",charset="utf8"):
    conn = MySQLdb.connect(
        host = host,
        port = port,
        user = user,
        passwd = passwd,
        db = db,
        charset = charset,
        cursorclass = MySQLdb.cursors.DictCursor
    )
    yesterday = datetime.date.today()-datetime.timedelta(1)
    cur = conn.cursor()
    SQL = """SELECT DATE_FORMAT(START_TIME,'%Y-%m-%d %H:%i:%S') AS STARTTIME,USER_HOST,TIME_FORMAT(QUERY_TIME,'%H:%i:%S') AS QUERYTIME,
        TIME_FORMAT(LOCK_TIME,'%H:%i:%S') AS LOCKTIME,ROWS_SENT,ROWS_EXAMINED,SQL_TEXT,0 AS STATE
        FROM slow_log WHERE START_TIME > '{0}'"""
    cur.execute(SQL.format(yesterday))
    return cur.fetchall()

def store_in_mongodb(result=None):
    if not result:
        return
    conn = pymongo.MongoClient("localhost",27017)
    db = conn.monitor
    for doc in result:
        db.slow_sql.insert(doc)
    conn.close()

def server(mongohost, mongoport):
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
        tmplist = list()
        conn = pymongo.MongoClient(mongohost, mongoport)
        db = conn['monitor']
        if data[0:12]  == "GET LaSt SQL":
            rows = db.slow_sql.find({"STATE": 0})
            for row in rows:
                row['_id'] = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)', r'{"$oid": "\1"}', str(row.get('_id')))
                tmplist.append(row)
            jsondata = json.dumps(tmplist, ensure_ascii=False)
            client.send(jsondata.encode("utf8"))
        elif data[0:6] == "UP ID:":
            print "UPDATE T_SLOW SET STATE=1 WHERE ID={0}".format(data.split(':')[1])
            db.slow_sql.update({'_id': data.split(':')[1]}, {"STATE": 1})
            client.send("ID: " + data.split(':')[1] + " has been executed.")
        client.close()
        conn.close()
        if time.strftime('%M') == '00':
            db.slow_sql.remove({'STATE': 1})

if __name__ == "__main__":
    result = check_slow_table()
    #store_in_mongodb(result)
    server('localhost', 27017)
