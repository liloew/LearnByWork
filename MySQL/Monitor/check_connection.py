#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import DB, Encrypt

def main():
    en = Encrypt()
    db = DB("localhost",3306,"root","123456","monitor")
    SQL = "SELECT ID,INET_NTOA(IP),PORT,USER,PASSWD FROM T_INSTANCE"
    db.execute(SQL)
    rows = db.fetchall()
    for row in rows:
        tmpdb = DB(row[1],row[2],row[3],en.decrypt(row[4]))
        db.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.PROCESSLIST")
        cnt = db.fetchone()
        db.execute("""INSERT INTO T_CONNECTION(INSTANCE,CNT)
            VALUES({0}, {1})""".format(row[0], cnt[0]))
        db.commit()

if __name__ == "__main__":
    main()
