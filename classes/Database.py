import pymysql

class DatabaseTransitionError(Exception):
    """ Raised when current db is switched while a connection is active """
    def __init__(self):
        self.message = "Database cannot be switched while a connection is open."

class Database:

    def __init__(self):
        self.conn = None
        self.testing = False
        self.databases = {
            'dev': 'bibleq',
            'test': 'bibleq_test'
        }
        self.current_db = None

    def connect(self):
        if self.conn is None:
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
        if self.conn is not None:
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
        self.schema_path = app_config['SCHEMA_SQL_PATH']

        if app_config['TESTING']:
            self.testing = True
            self.set_db('test')
        else:
            self.testing = False
            self.set_db('dev')

    def set_db(self, db_name):
        if self.conn is None:
            self.current_db = self.databases[db_name]
        else:
            raise DatabaseTransitionError


    def execute_sql_file(self, file_path):
        statements = self.parse_sql_file(file_path)
        self.connect()

        cur = self.conn.cursor()

        try:
            for statement in statements:
                cur.execute(statement)
        except:
            result = False
        else:
            result = True
        finally:
            if result: self.conn.commit()
            cur.close()

        return result

    def parse_sql_file(self, file_path):
        DELIMITER = ';'
        NEW_LINE = '\n'
        COMMENT_PREFIX = ('--', '/*')

        statements = []

        with open(file_path) as f:
            statement = ''
            for line in f:
                # skip empty or comment lines
                if line == NEW_LINE or line.startswith(COMMENT_PREFIX):
                    continue

                statement = statement + line.rstrip(NEW_LINE)

                if statement.endswith(DELIMITER):
                    statements.append(statement)
                    statement = ''

        return statements

    def init_test_db(self):
        self.connect()

        cur = self.conn.cursor()
        cur.execute('CREATE DATABASE bibleq_test;')

        self.conn.commit()
        self.conn.close()
        self.db_params['db'] = 'bibleq_test'
        self.execute_sql_file(self.schema_path)
    # populate db

db = Database()