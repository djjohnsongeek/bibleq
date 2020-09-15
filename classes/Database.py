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

    def commit(self):
        self.conn.commit()

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
            self.commit()
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

    def fetch_all_rows(self, table: str) -> list:
        ''' Ensure table is validated first '''
        self.connect()

        cur = self.conn.cursor()
        cur.execute(
            f'SELECT * FROM {table};'
        )
        result = cur.fetchall()

        return result

    def trucate_table(self, table: str) -> list:
        ''' Ensure table is validated first '''
        self.connect()

        cur = self.conn.cursor()
        cur.execute(
            f'TRUNCATE {table};'
        )
        self.commit()
        cur.close()

    def get_last_insert_id(self):
        self.connect()
        cur = self.conn.cursor()

        cur.execute(
            'SELECT LAST_INSERT_ID();'
        )
        result = cur.fetchone()
        cur.close()

        return result['LAST_INSERT_ID()']

    def update_row(self, table, id_col, fields):
        ''' Ensure table and fields are validated '''

        # TODO seperate sql generation off
        sql = f'UPDATE {table} '

        count = 1
        for field in fields:
            if count == 1:
                sql = sql + f'SET {field} = %s, '
            else:
                sql = sql + f'{field} = %s, '

            count = count + 1

        sql = sql.rstrip(', ')
        sql = sql + f' WHERE {id_col["field_name"]} = %s;'

        sql_values = list(fields.values())
        sql_values.append(id_col['id'])

        cur = self.conn.cursor()
        cur.execute(sql, sql_values)
        cur.close()

    def get_row(self, table, id_col, row_id):
        sql = f'SELECT * FROM {table} WHERE {id_col} = '
        sql = sql + '%s;'

        cur = self.conn.cursor()
        cur.execute(sql, (row_id))

        result = cur.fetchone()
        cur.close()

        return result

    def get_rows(self, table, where_statement=None):

        sql = f'SELECT * FROM {table} '
        if where_statement:
            sql = sql + where_statement

        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()

        return result


db = Database()
