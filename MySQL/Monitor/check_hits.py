#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from base import DB, Encrypt, parser_config
from time import sleep
import datetime

def check_hitrate(host,port,user,passwd,db="",charset="utf8"):
    """
    """
    db = DB(host,port,user,passwd,db,charset,cursorclass="")
    en = Encrypt()
    db.execute("SELECT ID,INET_NTOA(IP) AS IPADDR,PORT,USER,PASSWD FROM T_INSTANCE")
    rows = db.fetchall()
    sql = "INSERT INTO T_HITRATE VALUES(NULL,'%s','%s','%s')"
    for row in rows:
        tmpdb = DB(row.get('IPADDR'),row.get('PORT'),row.get('USER'),en.decrypt(row.get('PASSWD')))
        tmpdb.execute("show global status like 'Qcache_hits'")
        hits = tmpdb.fetchone()
        tmpdb.execute("show global status like 'Com_select'")
        selects = tmpdb.fetchone()
        try:
            hit_rate = int(hits[1])/int(hits[1]+selects[1])
        except ZeroDivisionError:
            hit_rate = 0
        # 00.0%
        db.execute(sql % (row.get('ID'),datetime.datetime.now(), int(hit_rate)))
        db.commit()

def main():
    cg = parser_config()
    en = Encrypt()
    check_hitrate(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))


if __name__ == "__main__":
    while True:
        main()
        sleep(30)
