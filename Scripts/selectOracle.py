#!/usr/bin/python
# coding=utf-8
import cx_Oracle

dsn = cx_Oracle.makedsn('172.16.2.19',"1521",'test')
conn = cx_Oracle.connect('sys','wisedu',dsn,cx_Oracle.SYSDBA)
# For DBA friendly : Clientinfo,Module and Action
conn.clientinfo = 'Python 2.4 on RedHat 5.4'
conn.module = 'cx_Oracle demo'
conn.action = 'BatchJob #1'

cursor = conn.cursor()
# cursor.execute('select sysdate from dual')

# 查看当前PGA的值
query = "select * from v$pgastat"
cursor.execute(query)

rows = cursor.fetchall()
print "查看当前PGA值"
for row in rows:
	print row[0],row[1],row[2]

# 查看当前SGA的值
query = 'select * from v$sga'
cursor.execute(query)
rows = cursor.fetchall()
print '''
查看当前SGA值
'''
for row in rows:
	print row[0],row[1]

# 列出当前占用PGA最大的进程
query = "select max(pga_used_mem), max(pga_alloc_mem), max(pga_max_mem) from v$process"
cursor.execute(query)
rows = cursor.fetchall()
print '''
列出当前占用PGA最多的进程
MAX(PGA_USED_MEM) MAX(PGA_ALLOC_MEM) MAX(PGA_MAX_MEM)
'''
for row in rows:
	print row[0],row[1],row[2]
	
# 查看当前并发连接数
query = "select count(*) from v$session where status = 'ACTIVE'"
cursor.execute(query)
rows = cursor.fetchall()
print '''
查看当前并发连接数
'''
for row in rows:
	print row[0]

# 查看BufferCache命中率	
query = '''SELECT a.value + b.value logical_reads, c.value phys_reads,
			ROUND (100 * (1 - c.value / (a.value + b.value)), 4) hit_ratio
			FROM v$sysstat a, v$sysstat b, v$sysstat c
			WHERE a.NAME = 'db block gets'
			AND b.NAME = 'consistent gets'
			AND c.NAME = 'physical reads'
'''
cursor.execute(query)
rows = cursor.fetchall()
print '''
查看BufferCache命中率'''
print '''
LOGICAL_READS PHYS_READS  HIT_RATIO'''
for row in rows:
	print row[0],row[1],row[2]

# 查看LibraryCache命中率
query = '''SELECT SUM (pins) total_pins, SUM (reloads) total_reloads,
			SUM (reloads) / SUM (pins) * 100 libcache_reload_ratio
			FROM v$librarycache
  '''
cursor.execute(query)
rows = cursor.fetchall()
print '''查看LibraryCache命中率
'''
print '''
TOTAL_PINS TOTAL_RELOADS LIBCACHE_RELOAD_RATIO'''
for row in rows:
	print row[0],row[1],row[2]
	
# 关闭连接
conn.close()
