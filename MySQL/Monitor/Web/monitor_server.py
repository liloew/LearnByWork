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
        self.render("index.html")

class JsonHandler(BaseHandler):
    """
    """
    def get(self):
        instid = self.get_argument("instid")
        SQL = "SELECT INSTANCE,CNT,CHECKTIME FROM T_CONNECTION WHERE INSTANCE={0}"
        self.db.execute(SQL.format(instid))
        rows = self.db.fetchall()
        data = list()
        labels = list()
        for row in rows:
            data.append(row[1])
            labels.append(row[2].strftime("%Y-%m-%d %H:%M:%S"))
        json_dump = [{"labels": labels, "data": data}]
        jsdata = json.dumps(json_dump)
        self.write(jsdata)

class Application(tornado.web.Application):
    """
    """
    def __init__(self):
        """
        """
        handlers = [
            (r"/", HomeHandler),
            (r"/json", JsonHandler),
        ]
        settings = dict(
            title = "MySQL Monitor",
            debug = True,
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
