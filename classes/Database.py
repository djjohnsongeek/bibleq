import pymysql


class DatabaseTransitionError(Exception):
    """ Raised when current db is switched while a connection is active """
    def __init__(self):
        self.message = "Database cannot be switched " \
                       "while a connection is open."


class Database:

    def __init__(self):
        self.conn = None
        self.databases = {
            'dev': 'bibleq',
            'test': 'bibleq_test'
        }
        self.current_db = None

    def connect(self):
        if self.conn is None:
            self.conn = pymysql.connect(
                host=self.params['host'],
                user=self.params['user'],
                password=self.params['password'],
                port=self.params['port'],
                db=self.params['db'],
                charset=self.params['charset'],
                cursorclass=self.params['cursorclass'],
                autocommit=False,
            )

    def close(self):
        if self.conn is not None:
            self.conn.close()
        self.conn = None

    def init(self, app_config: dict):
        self.params = dict(
            host=app_config['MYSQL_HOST'],
            user=app_config['MYSQL_USER'],
            password=app_config['MYSQL_PASSWORD'],
            port=app_config['MYSQL_PORT'],
            db=app_config['MYSQL_DB'],
            charset=app_config['MYSQL_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.schema_path = app_config['SCHEMA_SQL_PATH']

        if app_config['TESTING']:
            self.set_db('test')
        else:
            self.set_db('dev')

    def set_db(self, db_name: str):
        if self.conn is None:
            self.current_db = self.databases[db_name]
            self.params['db'] = self.current_db
        else:
            raise DatabaseTransitionError

    def execute_sql_file(self, file_path: str) -> bool:
        statements = self.parse_sql_file(file_path)
        self.connect()
        cur = self.conn.cursor()

        result = self.execute_statements(cur, statements)

        if result:
            self.conn.commit()
        else:
            self.conn.rollback()

        cur.close()

        return result

    def execute_statements(self, cur, statements):

        for statement in statements:
            try:
                cur.execute(statement)
            except pymysql.err.OperationalError:
                return False

        return True

    def parse_sql_file(self, file_path: str) -> list:
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

    def fetch_all_rows(self, table_name: str) -> list:
        ''' Ensure table_name is validated first '''
        self.connect()

        cur = self.conn.cursor()
        cur.execute(
            f'SELECT * FROM {table_name};'
        )
        result = cur.fetchall()

        return result

    def trucate_table(self, table_name: str) -> list:
        ''' Ensure table_name is validated first '''
        self.connect()

        cur = self.conn.cursor()
        cur.execute(
            f'TRUNCATE {table_name};'
        )
        self.conn.commit()
        cur.close()


db = Database()
