#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import DB, Encrypt

def main(host,port,user,passwd="",db="",charset="utf8"):
    """
    """
    db = DB(host,port,user,passwd,db,charset)
    cnt = db.execute("SHOW SLAVE STATUS")
    if cnt == 0:
        return None
    row = db.fetchone()
    replicat_status = dict(zip(
        ("SLAVE_IO_STATE","MASTER_HOST","MASTER_USER","MASTER_PORT","CONNECT_RETRY",
        "MASTER_LOG_FILE","READ_MASTER_LOG_POS","RELAY_LOG_FILE","RELAY_LOG_POS",
        "RELAY_MASTER_LOG_FILE","SLAVE_IO_RUNNING","SLAVE_SQL_RUNNING","REPLICATE_DO_DB",
        "REPLICATE_IGNORE_DB","REPLICATE_DO_TABLE","REPLICATE_IGNORE_TABLE",
        "REPLICATE_WILD_DO_TABLE","REPLICATE_WILD_IGNORE_TABLE","LAST_ERRNO","LAST_ERROR",
        "SKIP_COUNTER","EXEC_MASTER_LOG_POS","RELAY_LOG_SPACE","UNTIL_CONDITION",
        "UNTIL_LOG_FILE","UNTIL_LOG_POS","MASTER_SSL_ALLOWED","MASTER_SSL_CA_FILE",
        "MASTER_SSL_CA_PATH","MASTER_SSL_CERT","MASTER_SSL_CIPHER","MASTER_SSL_KEY",
        "SECONDS_BEHIND_MASTER","MASTER_SSL_VERIFY_SERVER_CERT","LAST_IO_ERRNO","LAST_IO_ERROR",
        "LAST_SQL_ERRNO","LAST_SQL_ERROR","REPLICATE_IGNORE_SERVER_IDS","MASTER_SERVER_ID")
    ,row))
    # Here must be an insert if any SQL_THREAD,IO_THREAD or delay
    return replicat_status

if __name__ == "__main__":
    mon_db = DB("localhost",3306,"root","123456","monitor")
    en = Encrypt()
    mon_db.execute("SELECT ID,INET_NTOA(IP),PORT,USER,PASSWD FROM T_INSTANCE WHERE INSTTYPE='SLAVE'")
    rows = mon_db.fetchall()
    for row in rows:
        print main(row[1],row[2],row[3],en.decrypt(row[4]))
