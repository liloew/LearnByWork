#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import psutil
import MySQLdb
import netifaces as ni
class DB(object):
        """封装MySQL连接
        """
        def __init__(self,host,port,user,passwd,db="",charset="utf8"):
                """
                """
                self.host    = host
                self.port    = port
                self.user    = user
                self.passwd  = passwd
                self.db      = db
                self.cur     = None
                self.conn    = None
                self.charset = charset
                try:
                        self.conn = MySQLdb.connect(
                                host    = self.host,
                                port    = self.port,
                                user    = self.user,
                                passwd  = self.passwd,
                                db      = self.db,
                                charset = self.charset
                        )
                except MySQLdb.Error as e:
                        print "Errors in DB.__init__:%s" % e
        def execute(self, SQL=None):
                """
                """
                if not SQL:
                        print "You must give at least one SQL."
                self.cur = self.conn.cursor()
                try:
                        return self.cur.execute(SQL)
                except MySQLdb.OperationalError as e:
                        print "{0}\t{1},connect again\n".format(e[0], e[1])
                        self.__init__(
                                self.host,
                                self.port,
                                self.user,
                                self.passwd,
                                self.db,
                                self.charset
                        )
                        self.cur = self.conn.cursor()
                        return self.cur.execute(SQL)
        def fetchall(self):
                """
                """
                return self.cur.fetchall()
        def fetchone(self):
                return self.cur.fetchone()
        def close(self):
                """
                """
                self.conn.close()
        def __del__(self):
                """
                """
                self.conn.close()

class OS_Info(object):
        """操作系统相关信息
        """
        def __init__(self):
                """
                """
                pass
        def get_info(self):
                """
                """
                # CPU
                cpu = dict(zip(("user","nice","system","idle","iowait","irq","softirq","steal","guest"), psutil.cpu_times_percent(interval=2,percpu=False)))
                # 内存
                memory = dict(zip(("total","available","percent","used","free","active","inactive","buffers","cached"), psutil.virtual_memory()))
                swap = dict(zip(("total","used","free","percent","sin","sout"), psutil.swap_memory()))
                # 网络流量
                nw = ni.gateways()['default'][2][1]
                current_bytes = psutil.net_io_counters(pernic=True)[nw][1]
                time.sleep(60)
                previous, current_bytes = current_bytes, psutil.net_io_counters(pernic=True)[nw][1]
                # 网络连接数
                connections = len(psutil.net_connections())
                return cpu, memory, swap, connections
class DB_Info(object):
        """数据库信息
        """
        def __init__(self,host,port=3306,user="",passwd="",db="",charset="utf8"):
                """
                """
                self.db = DB(host,port,user,passwd,db,charset)
        def get_info(self):
                """
                """
                self.db.execute("show status")
                rows = self.db.fetchall()
                self.db.close()
                return dict([(row[0].upper(),row[1]) for row in rows])
if __name__ == "__main__":
        os_info = OS_Info()
        print os_info.get_info()
        #db_info = DB_Info("DB_HOST",3306,"DB_USER","DB_PASSWD")
        #db_info.get_info()
