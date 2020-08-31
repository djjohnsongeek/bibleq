import pymysql

class Database:
    conn = None

    def connect(self):
        self.conn = pymysql.connect(
            host = self.db_params['host'],
            user = self.db_params['user'],
            password = self.db_params['password'],
            port = self.db_params['port'],
            db = self.db_params['db'],
            charset = self.db_params['charset'],
            cursorclass = self.db_params['cursorclass'],
        )

    def close(self):
        self.conn.close()
        self.conn = None

    def init(self, app_config):
        self.db_params = dict(
            host = app_config['MYSQL_HOST'],
            user = app_config['MYSQL_USER'],
            password = app_config['MYSQL_PASSWORD'],
            port = app_config['MYSQL_PORT'],
            db = app_config['MYSQL_DB'],
            charset = app_config['MYSQL_CHARSET'],
            cursorclass = pymysql.cursors.DictCursor,
        )
    
    # parse sql
    # init db
    # populate db

db = Database()