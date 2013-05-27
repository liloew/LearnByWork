#!/usr/bin/python
# -*- coding=utf-8 -*-

import cx_Oracle
import threading
from random import choice

class CALL(threading.Thread):

	def __init__(self,arg):

		super(CALL, self).__init__()
		self.__db = cx_Oracle.connect('user','passwd','tnsnames',threaded=True)
		self.__cursor = self.__db.cursor()
		self.ykth = arg
		

	def __exit__(self):

		self.__cursor.close()
		self.__db.close()

	def run(self):

		global ykth
		result = self.__cursor.var(cx_Oracle.STRING)
		#result = self.__cursor.var(cx_Oracle.CURSOR)
		#tmp = choice(ykth)
		self.__cursor.callproc('username.p_xjgl_xjsh_JDJS_grdscai',(3,2012,self.ykth,'system',result))
		print result,self.ykth
		
class GET():

	def __init__(self):

		self.__db = cx_Oracle.connect('username','passwd','tnsnames')
		self.__cursor = self.__db.cursor()

	def get(self):

		self.__cursor.execute('select ykth from dscai_xh')
		rows = self.__cursor.fetchall()
		return rows

#if __name__ == '__main__':

	#insta1 = CALL()
def main(num):
	insta2= GET()
	ykth = insta2.get()
	ls_thread = [] 
	for i in range(num,num+50):
		t = CALL(arg=int(ykth[i][0]))
		print i
		#t.run(final)
		t.start()
		ls_thread.append(t)
	for x in ls_thread:
		x.join()

if __name__ == '__main__':

	for k in range(3750,3753):
		#print 50*k
		#main(50*k)
		main(k)
