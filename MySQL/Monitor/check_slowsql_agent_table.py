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

class check_slow_sql(Object):
    """
    """
    def __init__(mongohost="localhost", mongoport=27017, dbhost="localhost", dbport=3306, dbuser, dbpasswd, database="mysql"):
        self.mongohost = mongohost
        self.mongoport = mongoport
        self.dbhost    = dbhost
        self.dbport    = dbport
        self.dbuser    = dbuser
        self.dbpasswd  = dbpasswd
        self.db        = database
        self.result    = list()
    def mongo_connect():
        """
        """
        try:
            self.mgconn    = pymongo.MongoClient(self.mghost, self.mgport)
        except pymongo.errors.ConnectionFailure as e:
            print e
    def mysql_connect():
        """
        """
        try:
            self.mysqlconn = MySQLdb.connect(
                host = self.dbhost,
                port = self.dbport,
                user = self.dbuser,
                passwd = self.dbpasswd,
                db = self.database,
                charset = "utf8",
                cursorclass = MySQLdb.cursors.DictCursor
            )
            self.cur = self.mysqlconn.cursor()
        except MySQLdb.Error as e:
            print e
    def check_slow_table():
        yesterday = datetime.date.today()-datetime.timedelta(1)
        SQL = """SELECT DATE_FORMAT(START_TIME,'%Y-%m-%d %H:%i:%S') AS STARTTIME,USER_HOST,TIME_FORMAT(QUERY_TIME,'%H:%i:%S') AS QUERYTIME,
            TIME_FORMAT(LOCK_TIME,'%H:%i:%S') AS LOCKTIME,ROWS_SENT,ROWS_EXAMINED,SQL_TEXT,0 AS STATE
            FROM slow_log WHERE START_TIME > '{0}'"""
        self.cur.execute(SQL.format(yesterday))
        rows = self.cur.fetchall()
        for row in rows:
            self.result.append(row)
    def store_in_mongodb():
        if self.result == []:
            return
        db = self.mgconn.monitor
        for doc in self.result:
            db.slow_sql.insert(doc)
        self.mgconn.close()
        # Init the self.result as if it may insert twice
        self.result = list()
    def server(mongohost, mongoport):
        host = ''
        port = 7000
        backlog = 5
        size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(backlog)
        while 1:
            client, address = s.accept()
            data = client.recv(size)
            # Del the object and recreate it, do nothing if error
            try:
                del(l)
            except NameError as e:
                pass
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
            # Insert and remove from MongoDB at special time
            if time.strftime('%M') == '00':
                store_in_mongodb()
                db.slow_sql.remove({'STATE': 1})

if __name__ == "__main__":
    css = check_slow_sql(dbuser="root", dbpasswd="123456")
    css.server('localhost', 27017)
