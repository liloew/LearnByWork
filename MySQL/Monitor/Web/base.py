#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb


class DB(object):
    """
    """
    def __init__(self,host="localhost",port=3306,user="",passwd="",db="",charset="utf8"):
        """初始化MySQL数据库
        """
        self.host    = host
        self.port    = port
        self.user    = user
        self.passwd  = passwd
        self.db      = db
        self.charset = charset
        try:
            self.conn = MySQLdb.connect(
                host    = self.host,
                user    = self.user,
                passwd  = self.passwd,
                db      = self.db,
                charset = self.charset
            )
            self.cur = self.conn.cursor()
        except MySQLdb.Error as e:
            print "Errors in DB.__init__:%s" % e
    def execute(self,SQL=""):
        """执行具体的SQL
        """
        if not SQL:
            print "You must give at least one SQL."
        try:
            self.cur.execute(SQL)
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
        """获取全部结果集
        """
        return self.cur.fetchall()
    def fetchone(self):
        """获取单条记录
        """
        return self.cur.fetchone()
    def close(self):
        """关闭数据库连接
        """
        self.conn.close()
    def commit(self):
        """commit事务
        """
        self.conn.commit()
    def rollback(self):
        """rollback当前事务
        """
        self.conn.rollback()
    def __del__(self):
        """销毁连接对象
        """
        self.conn.rollback()
        self.conn.close()
