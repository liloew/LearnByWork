#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import time
import socket
import MySQLdb
import pymongo
import datetime
import MySQLdb.cursors

def log_rotate(host, port, user, passwd, rotatype=0):
    """rotate the general_log and slow_log
       `rotate` -> 0: no rotate any log
                   1: rotate the slow log
                   2: rotate general and slow log
    """
    try:
        conn = MySQLdb.connect(
            host = host,
            port = port,
            user = user,
            passwd = passwd,
            db = "mysql",
            charset = "utf8"
        )
        cur = conn.cursor()
    except MySQLdb.Error as e:
        print e
    today = time.strftime('%Y%m%d')
    GNL_SQL = ['DROP TABLE IF EXISTS general_log_{0}'.format(today), 'DROP TABLE IF EXISTS general_log_backup',
        'CREATE TABLE general_log_{0} LIKE general_log'.format(today),
        'RENAME TABLE general_log TO general_log_backup, general_log_{0} TO general_log'.format(today)]
    SLW_SQL = ['DROP TABLE IF EXISTS slow_log_{0}'.format(today), 'DROP TABLE IF EXISTS slow_log_backup',
        'CREATE TABLE slow_log_{0} LIKE slow_log'.format(today),
        'RENAME TABLE slow_log TO slow_log_backup, slow_log_{0} TO slow_log'.format(today)]
    if rotatetype > 1:
        try:
            cur.execute("SELECT NOW()")
        except MySQLdb.OperationalError as e:
            conn = MySQLdb.connect(
                host = host,
                port = port,
                user = user,
                passwd = passwd,
                db = "mysql",
                charset = "utf8"
            )
            cur = conn.cursor()
        # Rotate the general log
        for sql in GNL_SQL:
            cur.execute(sql)
            conn.commit()
    if rotatetype > 0:
        # Rotate the slow log
        for sql in SLW_SQL:
            cur.execute(sql)
        conn.commit()
    conn.close()
    return True


class check_slow_sql(object):
    """
    """
    def __init__(self,dbuser, dbpasswd, mongoport=27017, dbhost="localhost", database="mysql", mongohost="localhost", dbport=3306):
        self.mghost = mongohost
        self.mgport = mongoport
        self.dbhost    = dbhost
        self.dbport    = dbport
        self.dbuser    = dbuser
        self.dbpasswd  = dbpasswd
        self.db        = database
        self.result    = list()
        # Init the MongoDB and MySQL connection
        self.mongo_connect()
        self.mysql_connect()
    def mongo_connect(self):
        """
        """
        try:
            self.mgconn    = pymongo.MongoClient(self.mghost, self.mgport)
        except pymongo.errors.ConnectionFailure as e:
            print e
    def mysql_connect(self):
        """
        """
        try:
            self.mysqlconn = MySQLdb.connect(
                host = self.dbhost,
                port = self.dbport,
                user = self.dbuser,
                passwd = self.dbpasswd,
                db = self.db,
                charset = "utf8",
                cursorclass = MySQLdb.cursors.DictCursor
            )
            self.cur = self.mysqlconn.cursor()
        except MySQLdb.Error as e:
            print e
    def check_slow_table(self):
        yesterday = datetime.date.today()-datetime.timedelta(1)
        SQL = """SELECT DATE_FORMAT(START_TIME,'%Y-%m-%d %H:%i:%S') AS STARTTIME,USER_HOST,TIME_FORMAT(QUERY_TIME,'%H:%i:%S') AS QUERYTIME,
            TIME_FORMAT(LOCK_TIME,'%H:%i:%S') AS LOCKTIME,ROWS_SENT,ROWS_EXAMINED,SQL_TEXT,0 AS STATE
            FROM slow_log WHERE START_TIME > '{0}'"""
        try:
            self.cur.execute(SQL.format(yesterday))
        except MySQLdb.OperationalError as e:
            self.mysql_connect()
            self.cur.execute(SQL.format(yesterday))
        rows = self.cur.fetchall()
        for row in rows:
            self.result.append(row)
    def check_general_table(self):
        yesterday = datetime.date.today()-datetime.timedelta(1)
        SQL = """SELECT EVENT_TIME,USER_HOST,THREAD_ID,SERVER_ID,COMMAND_TYPE,ARGUMENT
            FROM general_log
            WHERE COMMAND_TYPE = 'Query'
            AND EVENT_TIME > '{0}'"""
        try:
            self.cur.execute(SQL.format(yesterday))
        except MySQLdb.OperationalError as e:
            self.mysql_connect()
            self.cur.execute(SQL.format(yesterday))
        rows = self.cur.fetchall()
        for row in rows:
            self.result.append(row)
    def store_in_mongodb(self,tp):
        if self.result == []:
            return
        db = self.mgconn.monitor
        if tp == 1:
            for doc in self.result:
                db.slow_sql.insert(doc)
        elif tp == 2:
            for doc in self.result:
                db.general_sql.insert(doc)
        self.mgconn.close()
        # Init the self.result as if it may insert twice
        self.result = list()
    def server(self,sockhost="localhost", sockport=7000):
        backlog = 5
        size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((sockhost,sockport))
        s.listen(backlog)
        while 1:
            client, address = s.accept()
            data = client.recv(size)
            # Del the object and recreate it, do nothing if error
            tmplist = list()
            try:
                db = self.mgconn['monitor']
            except pymongo.errors.ConnectionFailure as e:
                mongo_connect()
                db = self.mgconn['monitor']
            # Only process the special request
            if data[0:12]  == "GET LaSt SQL":
                rows = db.slow_sql.find({"STATE": 0})
                for row in rows:
                    # Delete the Objectid function in the document
                    row['_id'] = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)', r'{"$oid": "\1"}', str(row.get('_id')))
                    tmplist.append(row)
                jsondata = json.dumps(tmplist, ensure_ascii=False)
                client.send(jsondata.encode("utf8"))
            elif data[0:6] == "UP ID:":
                print "UPDATE T_SLOW SET STATE=1 WHERE ID={0}".format(data.split(':')[1])
                db.slow_sql.update({'_id': data.split(':')[1]}, {"STATE": 1})
                client.send("ID: " + data.split(':')[1] + " has been executed.")
            client.close()
            self.mgconn.close()
            # Insert and remove from MongoDB at special time when there exists client connection
            if time.strftime('%M') == '00':
                self.check_slow_table()
                self.store_in_mongodb(1)
                db.slow_sql.remove({'STATE': 1})
            # rotate the log at 01:00 because the database backup at 02:30
            if time.strftime("%H") == '01':
                log_rotate(self.dbhost, self.dbport, self.dbuser, self.dbpasswd, 1)
            try:
                del(tmplist)
            except NameError as e:
                pass

if __name__ == "__main__":
    css = check_slow_sql("root", "123456")
    css.server("0.0.0.0", 7000)
