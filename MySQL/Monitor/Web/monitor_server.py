#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import tornado
import MySQLdb
import os.path
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options
from base import DB


define("port", default=8080, help="Web listen port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    """基本的类
    """
    def initialize(self):
        """初始化数据库
        """
        self.db = DB("localhost",3306,"root","123456","monitor")

class HomeHandler(BaseHandler):
    """Web主页的Handler
    """
    def get(self):
        SQL = """SELECT ID,INSTANCE,EVENT_NAME,EVENT_BODY,LEVEL,RECEIVER FROM T_ALERT limit 10"""
        self.db.execute(SQL)
        alertrows = self.db.fetchall()
        SQL = """SELECT ID FROM T_INSTANCE"""
        self.db.execute(SQL)
        instrows = self.db.fetchall()
        self.db.execute("SELECT ID,STATE FROM T_INSTANCE")
        piperows = self.db.fetchall()
        i = 0
        listpipe = list()
        for row in piperows:
            listpipe.append(list(row))
        for ls in listpipe:
            ls.append(i)
            i += 1
        self.render("index.html",alerts=alertrows,instance=instrows,pipe=listpipe)

class ReplicateHandler(BaseHandler):
    """
    """
    def get(self):
        SQL = "SELECT ID,INSTTYPE,IP,PORT,USER,PASSWD FROM T_INSTANCE WHERE INSTTYPE='SLAVE'"
        self.db.execute(SQL)
        rows = self.db.fetchall()
        if len(rows) == 0:
            self.write("No slave")
            return
        self.render("replication.html", firstslave=rows[0], slaveinstances=rows)

class JsonHandler(BaseHandler):
    """
    """
    def get(self):
        instid = self.get_argument("instid", default=None)
        if instid:
            SQL = """SELECT * FROM (
                SELECT INSTANCE,SUM(CNT),DATE_FORMAT(CHECKTIME,'%Y-%m-%d %H:%i') AS DATEFORMAT
                FROM T_CONNECTION
                WHERE INSTANCE={0}
                GROUP BY INSTANCE,DATEFORMAT
                ORDER BY DATEFORMAT DESC
                LIMIT 30) G
                ORDER BY G.DATEFORMAT ASC"""
            self.db.execute(SQL.format(instid))
            rows = self.db.fetchall()
            data = list()
            labels = list()
            for row in rows:
                data.append(int(row[1]))
                labels.append(row[2])
            json_dump = {"labels": labels, "data": data}
            jsdata = json.dumps(json_dump)
            self.write(jsdata)
            return
        slaveinstid = self.get_argument("slaveinstid", default=None)
        if slaveinstid:
            SQL = """SELECT * FROM 
                (SELECT ID,INSTANCE,SQLTHREAD,IOTHREAD,BEHIND,CHECKTIME FROM T_REPLICAT WHERE INSTANCE={0} ORDER BY ID DESC LIMIT 30) G
                ORDER BY ID ASC"""
            self.db.execute(SQL.format(slaveinstid))
            rows = self.db.fetchall()
            data = list()
            labels = list()
            for row in rows:
                data.append(int(row[4]))
                labels.append(row[5].strftime('%Y-%m-%d %H:%M:%S'))
            json_dump = {"labels": labels, "data": data}
            jsdata = json.dumps(json_dump)
            self.write(jsdata)

class PipeHandler(BaseHandler):
    """
    """
    def get(self):
        pass

class Application(tornado.web.Application):
    """
    """
    def __init__(self):
        """
        """
        handlers = [
            (r"/", HomeHandler),
            (r"/json", JsonHandler),
            (r"/replicate", ReplicateHandler),
        ]
        settings = dict(
            title = "MySQL Monitor",
            debug = True,
            autoreload = True,
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "template"),
        )

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    """
    """
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
