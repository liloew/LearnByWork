#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb

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
    def commit(self):
        """
        """
        self.conn.commit()
    def rollback(self):
        """
        """
        self.conn.rollback()
    def __del__(self):
        """
        """
        self.conn.close()
