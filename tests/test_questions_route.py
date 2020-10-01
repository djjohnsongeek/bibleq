import unittest

from tests import db, app, client, login
from classes.User import User

class TestQuestionRoute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with app.app_context():

            # create a user
            cls.user = User(db, {
                'first_name': 'first',
                'last_name': 'last',
                'email': 'test@gmail.com',
                'password': 'TestPassword123',
                'confirm_pw': 'TestPassword123',
            })

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.trucate_table('users')

    def setUp(self):
        db.connect()

    def tearDown(self):
        db.close()

    def test_create_question_get_request(self):
        # redirect if no one is logged in
        response = client.get('/questions/create')
        self.assertEqual(response.status_code, 302)

        login('test@gmail.com', 'TestPassword123')

        response = client.get('/questions/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Ask a Question</h1>', response.data)