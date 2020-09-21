import unittest

from bibleq import create_app
from classes.Database import db


class TestHomeRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # setup app and test client
        cls.db = db
        cls.app = create_app({
            'TESTING': True,
            'MYSQL_DB': 'bibleq_test',
            'TEST_SQL_PATH': r'C:\Users\Johnson\Projects\flask-'
                             r'app\bibleq\tests\temp\test.sql',
        })
        cls.client = cls.app.test_client()

        # setup database
        cls.db.init(cls.app.config)
        cls.db.execute_sql_file(cls.db.schema_path)

    def test_index(self):
        response = self.client.get('/')
        self.assertIn(b'<h1>Bible Q</h1>', response.data)
