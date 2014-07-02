#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from base import DB, Encrypt, parser_config

def check(host,port,user,passwd="",db="",charset="utf8"):
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
    return replicat_status

def main():
    # 建议读取外部配置文件以获取监控服务器配置
    cg = parser_config()
    en = Encrypt()
    mon_db = DB(cg.get("host"), int(cg.get("port")), cg.get("user"), en.decrypt(cg.get("passwd")), cg.get("db"))
    mon_db.execute("SELECT ID,INET_NTOA(IP),PORT,USER,PASSWD FROM T_INSTANCE WHERE INSTTYPE='SLAVE'")
    rows = mon_db.fetchall()
    for row in rows:
        replicat_status = check(row[1],row[2],row[3],en.decrypt(row[4]))
        if replicat_status:
            mon_db.execute("""INSERT INTO T_REPLICAT(INSTANCE,IOTHREAD,SQLTHREAD,BEHIND)
                VALUES('{0}','{1}','{2}',{3})""".format(row[0],replicat_status.get('SLAVE_IO_RUNNING'),
                replicat_status.get('SLAVE_SQL_RUNNING'),replicat_status.get('SECONDS_BEHIND_MASTER')))
    mon_db.commit()

if __name__ == "__main__":
    while True:
        main()
        sleep(30)
