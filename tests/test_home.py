import unittest

from tests import db, app, client


class TestHomeRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # setup app and test client
        cls.db = db
        cls.app = app
        cls.client = client

    def test_index(self):
        response = self.client.get('/')
        self.assertIn(b'<h1>Bible Q</h1>', response.data)
