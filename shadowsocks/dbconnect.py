import config
import cymysql
import logging

class DBconnect:
    conn = cymysql.connect(
        host = config.DB_HOST, 
        user = config.DB_USER, 
        passwd = config.DB_PASS, 
        db = config.DB_NAME,
        port = config.DB_PORT,
    )
    alias = config.DB_ALIAS
    table = config.DB_TABLE
    if config.S_ENABLE_CUSTOM_METHOD:
        alias.append('method')

    def __init__(self):
        pass
        
    def fetchAll(self):
        result = []
        try:
            conn = cymysql.connect(
                host = config.DB_HOST, 
                user = config.DB_USER, 
                passwd = config.DB_PASS, 
                db = config.DB_NAME,
                port = config.DB_PORT,
            )
            cur = conn.cursor()
            cur.execute('SELECT %s FROM %s' % (', '.join(DBconnect.alias), DBconnect.table))
            result = cur.fetchall()
            cur.close()
            conn.close()
        except:
            logging.error('Cannot connect to database')
        return result

    def runSql(self, sql):
        result = []
        try:
            conn = cymysql.connect(
                host = config.DB_HOST, 
                user = config.DB_USER, 
                passwd = config.DB_PASS, 
                db = config.DB_NAME,
                port = config.DB_PORT,
            )
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.commit()
            conn.close()
        except expression as identifier:
            logging.error('Cannot connect to database')
        return result
