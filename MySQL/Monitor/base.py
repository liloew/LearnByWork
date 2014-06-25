#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import MySQLdb

from Crypto.Cipher import AES

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

class Encrypt(object):
    """AES加密解密类
    """
    def __init__(self):
        # You may get it by os.urandom(), but it must be constant
        self.key = "MySQL Monitor v1"
        # BLOCK_SIZE must be 16, 24 or 32, here is len(self.key)
        self.BLOCK_SIZE = 16
        self.cipher = AES.new(self.key)
        self.PADDING = '{'
    def pad(self,str):
        """padding the str to 16X for AES encrypt
        """
        if not str:
            return
        return str + (self.BLOCK_SIZE - len(str) % self.BLOCK_SIZE) * self.PADDING
    def encrypt(self,passwd):
        """Encrypt the 16 bytes passwd
        """
        if not passwd:
            return
        return base64.b64encode(self.cipher.encrypt(self.pad(passwd)))
    def decrypt(self,passwd):
        """Decrypt the encryption passwd to original
        """
        if not passwd:
            return
        return self.cipher.decrypt(base64.b64decode(passwd)).rstrip(self.PADDING)
