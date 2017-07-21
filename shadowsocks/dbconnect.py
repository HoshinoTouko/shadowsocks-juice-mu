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
        cur = DBconnect.conn.cursor()
        cur.execute('select %s from %s' % ', '.join(DBconnect.alias), DBconnect.table )
        result = cur.fetchall()
        cur.close()
        return result

    def runSql(self, sql):
        cur = DBconnect.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
    

db = DBconnect()
print db.fetchAll()
