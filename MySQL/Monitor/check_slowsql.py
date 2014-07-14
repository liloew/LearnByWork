#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import socket
import MySQLdb

from base import DB, Encrypt, parser_config


def check_slowsql(host,port,user,passwd,db):
    size = 1024
    en = Encrypt()
    db = DB(host,port,user,passwd,db)
    db.execute("SELECT ID,INET_NTOA(IP),PORT,SOCKETPORT FROM T_INSTANCE ORDER BY ID DESC")
    instrows = db.fetchall()
    for inst in instrows:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((inst[1],inst[3]))
            print "connected to:{0}\t{1}".format(inst[1],inst[3])
        except socket.error as e:
            print '\033[91m' + "Socket error:{0}\t{1} for host {2}".format(
                e.errno, e.strerror, inst[1]) +\
                '\033[0m'
            if e.errno == 111:
                continue
        s.send('GET LaSt SQL')
        data_collect = ""
        while True:
            data = s.recv(size)
            if not data: break
            data_collect += data
        json_collect = json.loads(data_collect)
        for row in json_collect:
            try:
                db.executemany("INSERT INTO T_SLOW(SLOWSQL,CMDTYPE,CHKTIME,SERVERID,INSTID,STATE,USERHOST,OBJID) VALUES(%s,%s,%s)", [ i[1] for i in sorted(row.items())])
            except MySQLdb.IntegrityError as e:
                print 'row:{0} occur error:{1}'.format(tuple(insertrow[1:]),e)
            state = db.commit()
            if not state:
                print 'UP ID:{0}'.format(insertrow[0])
                tmps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tmps.connect((inst[1],inst[3]))
                tmps.send('UP ID:{0}'.format(insertrow[0]))
                data = tmps.recv(size)
                tmps.close()
        s.close()

if __name__ == "__main__":
    cg = parser_config()
    en = Encrypt()
    check_slowsql(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
