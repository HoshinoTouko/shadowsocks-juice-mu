import config
import cymysql

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
        conn = cymysql.connect(
            host = config.DB_HOST, 
            user = config.DB_USER, 
            passwd = config.DB_PASS, 
            db = config.DB_NAME,
            port = config.DB_PORT,
        )
        cur = conn.cursor()
        cur.execute('select %s from %s' % (', '.join(DBconnect.alias), DBconnect.table))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def runSql(self, sql):
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
        conn.close()
    
