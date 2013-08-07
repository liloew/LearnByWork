#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class mysql():

	def __init__(self,hostname='localhost',user='root',passwd=None,db=None):

		self.hostname = hostname
		self.user	  = user
		self.passwd	  = passwd
		self.db		  = db
		#try:
			#						Hostname	user   password	 database
		self.conn = MySQLdb.connect(self.hostname,self.user,self.passwd,self.db,
				use_unicode=True,charset='utf8'
				)
		#except :
			#pass

		self.cursor = self.conn.cursor()

	def select(self,tb=None,id=None,date=None):

		id = id or ''
		date = date or time.strftime('%Y-%m-%d', time.gmtime())
		#sql = "select count(*) from %s where id=%s and date='%s'" % (tb,id,date)
		# for production `date` should left(date,10),yyyy-mm-dd
		sql = "select count(*) from %s where id=%s and left(date,10)='%s'" \
				 % (tb,id,date)
		self.cursor.execute(sql)
		result = self.cursor.fetchone()
		return result[0]
	
	def insert(self,table=None,id=None,date=None,goods=None,price=None):

		tb = table or ''
		id = id or ''
		date = date or time.strftime('%Y-%m-%d %H:%M', time.gmtime())
		#sql = "insert into %s values(%s,'%s','%s',%s)" % (tb,id,date,goods,price)
		sql = "insert into %s values(%s,'%s',\"%s\",%s)" % (tb,id,date,goods,price)
		self.cursor.execute(sql)
		# We should use the character of autocommit
		self.conn.commit()

	def delete(self,table=None,id=None,date=None):

		tb = table or ''
		id = id or ''
		date = date or time.strftime('%Y-%m-%d', time.gmtime())
		sql = "delete from %s where id=%s and date='%s'" % (tb,id,date)
		self.cursor.execute(sql)
		self.conn.commit()

	def disconnect(self):

		self.cursor.close()
		self.conn.close()

if __name__ == '__main__':
	ms = mysql(hostname='192.168.88.129',user='lilo',passwd='19890929',db='test')
	#ms.select('jd',10024,'2013-06-02 20:18')
	#ms.insert('jd','10010')
	#ms.delete('jd','10010','2013-06-02 13:46')
