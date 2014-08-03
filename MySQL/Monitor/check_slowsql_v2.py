#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 无客户端化慢查询监控
import time
import MySQLdb
import hashlib
from base import DB,Encrypt,parser_config

def check_slow(host,port,user,passwd):
    if host and port and user and passwd:
        db = DB(host=host,port=port,user=user,passwd=passwd,db="mysql")
    else:
        print "You mst give all parmaters as host,port,user,passwd."
        exit(1)
    try:
        sql = "select start_time,user_host,query_time,lock_time,rows_sent,rows_examined,db,last_insert_id,insert_id,server_id,sql_text from slow_log"
        db.execute(sql)
        return db.fetchall()
    except MySQLdb.OperationalError as e:
        print e

def store_slow(results,instid,conn):
    if type(results) != list:
        rows = list(results)
    sql = 'INSERT INTO T_SLOW(INSTID,STARTTIME,LOCKTIME,QUERYTIME,USER_HOST,ROWS_SENT,ROWS_EXAMINED,ONDB,SQL_TEXT,OBJID) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
    for i in xrange(len(rows)):
        row = rows.pop()
        #print instid, row
        print(sql % (instid,time.strftime('%Y-%m-%d %H:%M:%S'),row[3],row[2],row[1],row[4],row[5],row[6],row[10],hashlib.sha1(row[10]).hexdigest()))
        conn.execute(sql % (instid,time.strftime('%Y-%m-%d %H:%M:%S'),row[3],row[2],row[1],row[4],row[5],row[6],row[10],hashlib.sha1(row[10]).hexdigest()))
        conn.commit()


def main():
    cg = parser_config()
    en = Encrypt()
    monitordb = DB(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
    monitordb.execute("SELECT ID,INET_NTOA(IP) AS IPADDR,PORT,USER,PASSWD FROM T_INSTANCE")
    #check_qps(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
    insts = monitordb.fetchall()
    for inst in insts:
        #rows = check_slow('10.1.2.9',3306,'root','password')
        rows = check_slow(inst[1],inst[2],inst[3],en.decrypt(inst[4]))
        store_slow(rows,inst[0],monitordb)

if __name__ == '__main__':
    main()
