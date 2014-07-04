#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, atexit
from signal import SIGTERM 
from time import sleep
from base import DB, Encrypt, parser_config
from check_qps import check_qps
from check_slowsql import check_slowsql

from daemon import Daemon

def run_check():
    cg = parser_config()
    en = Encrypt()

    while True:
        #check_slowsql(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
        check_qps(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
        sleep(60)
#######################################################
# fork a child process
def child():
   print 'A new child ',  os.getpid( )
   os._exit(0)  

def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            pids = (os.getpid(), newpid)
            print "parent: %d, child: %d" % pids
        if raw_input( ) == 'q': break
#######################################################


class MyDaemon(Daemon):
    """
    """
    def run(self):
        cg = parser_config()
        en = Encrypt()
        while True:
            check_qps(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
            sleep(60)

if __name__ == "__main__":
    daemon = MyDaemon("/tmp/monitor.pid")
    daemon.start()
