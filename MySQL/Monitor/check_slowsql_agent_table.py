#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors

def check_table(host,port,user,passwd,db,charset="utf8",cursorclass=None):
    """
    """
    try:
        conn = MySQLdb.connect(
            host    = host,
            port    = port,
            user    = user,
            passwd  = passwd,
            db      = db,
            charset = charset,
            cursorclass = cursorclass or MySQLdb.cursors.DictCursor
        )
        cur = conn.cursor()
    except MySQLdb.Error as e:
        print "Errors in DB.__init__:%s" % e
    cur.execute("SELECT * FROM mysql.general_log")
    return cur.fetchall()


if __name__ == "__main__":
    result = check_table("127.0.0.1",3309,"root","123456","mysql")
    for row in result:
        dictrow = row.get('argument')
        if dictrow.split(' ')[0].upper() == 'UPDATE':
            print "UPDATE {0}\t{1}".format(dictrow.split(' ')[1], dictrow)
        if dictrow.split(' ')[0].upper() == 'INSERT':
            print "INSERT {0}\t{1}".format(dictrow.split(' ')[2], dictrow)
        if dictrow.split(' ')[0].upper() == 'DELETE':
            print "DELETE {0}\t{1}".format(dictrow.split(' ')[2], dictrow)
