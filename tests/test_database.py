import unittest
import os

import pymysql

from bibleq import create_app
from classes.Database import db
from classes.Database import DatabaseTransitionError


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = db
        cls.app = create_app({
            'TESTING': True,
            'MYSQL_DB': 'bibleq_test',
            'TEST_SQL_PATH': r'C:\Users\Johnson\Projects\flask-'
                             r'app\bibleq\tests\temp\test.sql',
        })

        cls.db.init(cls.app.config)
        cls.db.execute_sql_file(cls.db.schema_path)

    def setUp(self):
        with self.app.app_context():
            self.db.connect()

            cur = self.db.conn.cursor()

            sql = 'INSERT INTO error_logs (message, level) VALUES (%s, %s);'
            values = [
                ('Log 1', 1),
                ('Log 2', 2),
                ('Log 3', 3),
            ]
            cur.executemany(sql, values)

            sql = ('INSERT INTO emails (subject, body, description) '
                   'VALUES (%s, %s, %s);')
            values = [
                ('Subject 1', 'Body 1', 'Description 1'),
                ('Subject 2', 'Body 2', 'Description 2'),
                ('Subject 3', 'Body 3', 'Description 3'),
            ]
            cur.executemany(sql, values)

            self.db.commit()

    def tearDown(self):
        with self.app.app_context():
            self.db.trucate_table('error_logs')
            self.db.trucate_table('emails')

            self.db.close()

    def test_init(self):
        self.assertDictEqual(
            self.db.params,
            {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'port': 3308,
                'db': 'bibleq_test',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor,
            }
        )

        self.assertEqual(
            self.db.schema_path,
            r'C:\Users\Johnson\Projects\flask-'
            r'app\bibleq\models\bibleq_schema.sql'
        )

    def test_connect(self):
        self.assertTrue(self.db.conn)

    def test_close(self):
        self.assertTrue(self.db.conn)

        self.db.close()
        self.assertIsNone(self.db.conn)

        self.db.close()
        self.assertIsNone(self.db.conn)

    def test_set_db(self):
        with self.assertRaises(DatabaseTransitionError):
            self.db.set_db('prod')

        self.db.close()
        self.db.set_db('dev')

        self.assertEqual(self.db.params['db'], 'bibleq')
        self.assertEqual(self.db.current_db, 'bibleq')

        self.db.set_db('dev')

    def test_parse_sql_file(self):
        file_name = self.app.config['TEST_SQL_PATH']

        # assert raises error
        with self.assertRaises(FileNotFoundError):
            self.db.parse_sql_file('not_corrent_path.sql')

        # create test sql file
        with open(file_name, 'w') as f:
            f.write('-- this is a comment\n')
            f.write('/* this is a comment */ \n')
            f.write('\n')
            f.write('SET SQL_MODE = NO_AUTO_VALUE_ON_ZERO;\n')
            f.write('DROP TABLE IF EXISTS `account_types`;\n')
            f.write('CREATE TABLE IF NOT EXISTS `account_types` (\n')
            f.write('`level_id` int(10) UNSIGNED NOT NULL,\n')
            f.write('  `name` char(8) NOT NULL,\n')
            f.write('  `description` tinytext NOT NULL,\n')
            f.write('  PRIMARY KEY (`level_id`)\n')
            f.write(
                ') ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 '
                'COLLATE=utf8mb4_0900_ai_ci;\n')
        pass

        # ensure it is parsed correctly
        statements = self.db.parse_sql_file(file_name)
        self.assertListEqual(
            statements,
            [
                'SET SQL_MODE = NO_AUTO_VALUE_ON_ZERO;',
                'DROP TABLE IF EXISTS `account_types`;',
                'CREATE TABLE IF NOT EXISTS `account_types` ('
                '`level_id` int(10) UNSIGNED NOT NULL,'
                '  `name` char(8) NOT NULL,'
                '  `description` tinytext NOT NULL,'
                '  PRIMARY KEY (`level_id`)'
                ') ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 '
                'COLLATE=utf8mb4_0900_ai_ci;'
            ]
        )

        os.remove(file_name)

    def test_execute_sql_file(self):
        # create test SQL file
        file_name = self.app.config['TEST_SQL_PATH']
        with open(file_name, 'w') as f:
            f.write('INSERT INTO account_types (level_id, name, description)'
                    ' VALUES (1, "User", "Basic");\n')
            f.write('INSERT INTO account_types (level_id, name, description)'
                    ' VALUES (2, "Writer", "Writes");\n')
            f.write('INSERT INTO account_types (level_id, name, description)'
                    ' VALUES (3, "Manager", "Manages");\n')
            f.write('INSERT INTO account_types (level_id, name, description)'
                    ' VALUES (4, "Admin", "Administrates");\n')

        # execute the file
        result = self.db.execute_sql_file(file_name)
        self.assertTrue(result)

        # verify rows were inserted (this also tests fetch_all_rows)
        results = db.fetch_all_rows('account_types')
        self.assertEqual(len(results), 4)

        # remove inserted rows (this also tests truncate table)
        os.remove(file_name)
        self.db.trucate_table('account_types')

        # verify rows are gone
        results = self.db.fetch_all_rows('account_types')
        self.assertFalse(results)

        # create another test sql file
        with open(file_name, 'w') as f:
            f.write('INSERT INTO account_types (level_id, name, description)'
                    ' VALUES (1, "User", "Special");\n')
            f.write('INSERT INTO account_types (level_id, name, error)'
                    ' VALUES (1, "User", "Basic");\n')

        # test exception
        with self.assertRaises(FileNotFoundError):
            self.db.execute_sql_file('incorrect_file')

        # test returns false
        result = self.db.execute_sql_file(file_name)
        self.assertFalse(result)

        # verify nothing was commited
        results = self.db.fetch_all_rows('account_types')
        self.assertFalse(results)

    def test_get_last_insert_id(self):
        # insert a row
        self.db.execute_statements(
            self.db.conn.cursor(),
            [
                'INSERT INTO error_logs (message, level) ' +
                'VALUES ("error message", 1);',
            ]
        )

        # validate row id value
        last_inserted_id = self.db.get_last_insert_id()
        self.assertEqual(last_inserted_id, 4)

    def test_get_row(self):
        row = self.db.get_row('error_logs', 'log_id', 1)

        self.assertEqual(row['message'], 'Log 1')
        self.assertEqual(row['level'], 1)

        row = self.db.get_row('emails', 'email_id', 2)

        self.assertEqual(row['subject'], 'Subject 2')
        self.assertEqual(row['body'], 'Body 2')
        self.assertEqual(row['description'], 'Description 2')

    def test_get_rows(self):
        rows = self.db.get_rows('error_logs')
        self.assertEqual(len(rows), 3)

        rows = self.db.get_rows('error_logs', 'WHERE level < 3;')
        self.assertEqual(len(rows), 2)

        rows = self.db.get_rows('emails', 'WHERE subject = "Subject 3";')
        self.assertEqual(len(rows), 1)
