import unittest
from bibleq import create_app
from classes.Database import db

class DataBaseTests(unittest.TestCase):
    db = db

    @classmethod
    def setUpClass(self):
        self.app = create_app({
            'TESTING': True,
            'MYSQL_DB': 'bibleq',
        })

        with self.app.app_context():
            self.db.init(self.app.config)
            self.db.connect()

            cur = self.db.conn.cursor()
            cur.execute('CREATE DATABASE bibleq_test;')
            self.db.conn.commit()
            cur.close()

            self.db.close()
        
        self.db.db_params['db'] = 'bibleq_test'
        self.app.config['MYSQL_DB'] = 'bibleq_test'
    
    @classmethod
    def tearDownClass(self):
        pass
    
    def setUp(self):
        self.db.connect()

    def tearDown(self):
        self.db.close()

    def test_test(self):
        pass

    