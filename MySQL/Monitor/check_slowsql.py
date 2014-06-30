#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import MySQLdb

from base import DB, Encrypt


def check_slowsql():
    host = 'localhost'
    port = 7000
    size = 1024
    # 本地监控数据库,建议由配置文件中读取
    db = DB("localhost",3306,"root","123456","monitor")
    db.execute("SELECT ID,INET_NTOA(IP) FROM T_INSTANCE ORDER BY ID DESC")
    instrows = db.fetchall()
    for inst in instrows:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((inst[1],port))
        s.send('GET LaSt SQL')
        data_collect = ""
        while True:
            data = s.recv(size)
            if not data: break
            data_collect += data
        for row in data_collect.split('\n'):
            insertrow = row.split('\t')
            if len(insertrow) == 9:
                subinsertrow = insertrow[1:]
                subinsertrow.insert(0,inst[0])
                print inst[0],subinsertrow
                try:
                    db.executemany("INSERT INTO T_SLOW(INSTID,CNT,TIME,ROS,USR,SLOWSQL,CHKTIME,SQLHASH,STATE) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", subinsertrow)
                except MySQLdb.IntegrityError as e:
                    print 'row:{0} occur error:{1}'.format(tuple(insertrow[1:]),e)
                state = db.commit()
                if not state:
                    print 'UP ID:{0}'.format(insertrow[0])
                    tmps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    tmps.connect((host,port))
                    tmps.send('UP ID:{0}'.format(insertrow[0]))
                    data = tmps.recv(size)
                    tmps.close()
        s.close()

if __name__ == "__main__":
    check_slowsql()
