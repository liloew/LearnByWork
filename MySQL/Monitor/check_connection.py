#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from base import DB, Encrypt, parser_config

def main():
    en = Encrypt()
    cg = parser_config()
    db = DB(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
    SQL = "SELECT ID,INET_NTOA(IP),PORT,USER,PASSWD FROM T_INSTANCE"
    db.execute(SQL)
    rows = db.fetchall()
    for row in rows:
        tmpdb = DB(row[1],row[2],row[3],en.decrypt(row[4]))
        tmpdb.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.PROCESSLIST")
        cnt = tmpdb.fetchone()
        db.execute("""INSERT INTO T_CONNECTION(INSTANCE,CNT)
            VALUES({0}, {1})""".format(row[0], cnt[0]))
        db.commit()

if __name__ == "__main__":
    while True:
        main()
        sleep(30)
