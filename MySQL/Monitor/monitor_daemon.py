#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from base import DB, Encrypt, parser_config
from check_qps import check_qps
from check_slowsql import check_slowsql


def run_check():
    cg = parser_config()
    en = Encrypt()

    while True:
        check_slowsql(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
        check_qps(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
        sleep(60)


if __name__ == "__main__":
    run_check()
