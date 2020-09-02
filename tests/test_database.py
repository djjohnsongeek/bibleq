import unittest
import os

import pymysql

from bibleq import create_app
from classes.Database import db
from classes.Database import DatabaseTransitionError

class DataBaseTests(unittest.TestCase):
    db = db

    @classmethod
    def setUpClass(cls):
        cls.app = create_app({
            'TESTING': True,
            'MYSQL_DB': 'bibleq_test'
        })

        cls.db.init(cls.app.config)
        
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        with self.app.app_context():
            self.db.connect()

    def tearDown(self):
        with self.app.app_context():
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
            r'C:\Users\Johnson\Projects\flask-app\bibleq\models\bibleq_schema.sql'
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
        # assert raises error
        with self.assertRaises(FileNotFoundError):
            self.db.parse_sql_file('test.sql')

        # create test sql file
        with open('test.sql', 'w') as f:
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
            f.write(') ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n')
        pass

        # ensure it is parsed correctly
        statements = self.db.parse_sql_file('test.sql')
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
                ') ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'
            ]
        )

        os.remove('test.sql')

    # test execute slq file
    # test set_db
    # test init
    