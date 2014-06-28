#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import DB, Encrypt
from time import sleep

def check_qps(host,port,user,passwd,db="",charset="utf8"):
    """统计各MySQL实例的QPS
    """
    db = DB(host,port,user,passwd,db,charset,cursorclass="")
    en = Encrypt()
    db.execute("SELECT ID,INET_NTOA(IP) AS IPADDR,PORT,USER,PASSWD FROM T_INSTANCE")
    rows = db.fetchall()
    for row in rows:
        db.execute("""SELECT UPTIME,QUESTIONS FROM T_QPS WHERE INSTID = {0}
            ORDER BY ID DESC LIMIT 1""".format(row.get('ID')))
        insertrow = db.fetchone()
        if insertrow == None:
            insertrow = dict()
        tmpdb = DB(row.get('IPADDR'),row.get('PORT'),row.get('USER'),en.decrypt(row.get('PASSWD')))
        tmpdb.execute("show global status like 'Uptime'")
        uprow = tmpdb.fetchone()
        tmpdb.execute("show global status like 'Questions'")
        qurow = tmpdb.fetchone()
        db.execute("""INSERT INTO T_QPS(INSTID,UPTIME,QUESTIONS,DIFFUPTIME,DIFFQUESTIONS)
            VALUES({0},{1},{2},{3},{4})""".format(
            row.get('ID'), uprow[1], qurow[1],
            int(uprow[1])-int(insertrow.get('UPTIME',0)),
            int(qurow[1])-int(insertrow.get('QUESTIONS', 0))
        ))
        db.commit()

def main():
    # 建议读取外部配置文件
    check_qps("localhost",3306,"root","123456","monitor")


if __name__ == "__main__":
    while True:
        main()
        sleep(10)
