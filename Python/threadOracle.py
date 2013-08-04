#!/usr/bin/python
# -*- coding=utf-8 -*-
#####################################################################
#			# create or replace procedure insert_date(i in number)  #
#			# is													#
#			# begin													#
#			#   insert into T_DATE values(i, sysdate);				#
#			#   commit;												#
#			# end;													#
#####################################################################
import threading
import cx_Oracle
from Queue import Queue
# Just for measuring the preformance
import time

dsn = cx_Oracle.makedsn('DBHost',"Port",'sid')
conn = cx_Oracle.connect('user','passwd',dsn,threaded=True)
conn.autocommit = True
# For DBA friendly : Clientinfo,Module and Action
conn.clientinfo = 'Python 2.4 on RedHat 5.4'
conn.module = 'cx_Oracle demo'
conn.action = 'BatchJob #1'


class AsyncInsert(threading.Thread):
	def __init__(self, cur, input):
		threading.Thread.__init__(self)
		self.cur = cur
		self.input = input

	def run(self):
		while True:
			if q.empty():
				self.cur.close()
				break
			self.cur.callproc("insert_date", [q.get()])
			# Python >= 2.6
			#q.task_done()


# OK,let's go.
start = time.time()
q = Queue()

# Get ID
sql = 'SELECT object_id FROM T_OBJECT'
cur1 = conn.cursor()
result = cur1.execute(sql)
for r in result:
	q.put(r[0])
cur1.close()

# How many threads
for input in xrange(20):
	cur = conn.cursor()
	th = AsyncInsert(cur, input)
	th.start()
	th.join()

# 关闭连接
conn.close()
# How long it take
print "This consume %f seconds." % (time.time() - start)
