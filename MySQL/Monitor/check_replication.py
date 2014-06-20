#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base import DB
class DB_Info(object):
        """数据库信息
        """
        def __init__(self,host,port=3306,user="",passwd="",db="",charset="utf8"):
                """
                """
                self.db = DB(host,port,user,passwd,db,charset)
        def get_status(self):
                """
                """
                self.db.execute("show status")
                rows = self.db.fetchall()
                return dict([(row[0].upper(),row[1]) for row in rows])

def main():
    db_info = DB_Info("192.168.2.30",3306,"root","Sunline")
    print db_info.get_replication()

if __name__ == "__main__":
    main()
