import unittest

from bibleq import create_app
from classes.Database import db
from classes.User import User


class TestUserClass(unittest.TestCase):
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
        pass

    def tearDown(self):
        pass


# test user init
# test user create
# test user update
# test user delete
# test user get_all
# test parse user info
# test val name
# test val email
# test val int
# test validate


