import unittest

from flask import session

from bibleq import create_app
from classes.Database import db
from classes.User import User


class TestAuthRoute(unittest.TestCase):

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

        # set domain name
        cls.domain_name = cls.app.config['APP_URL']

        # create a test user
        with cls.app.app_context():
            User(cls.db, {
                'first_name': 'first',
                'last_name': 'last',
                'email': 'test@gmail.com',
                'password': 'TestPassword123',
                'confirm_pw': 'TestPassword123',
            })

    # helper methods
    def login(self, email, password):
        return self.client.post(
            "/auth/login", data={
                "email": email,
                "password": password
            }
        )

    def register_test_user(self):
        return self.client.post(
            '/auth/register',
            data={
                'first_name': 'first2',
                'last_name': 'last2',
                'email': 'test2@gmail.com',
                'password': 'TestPassword234',
                'confirm_pw': 'TestPassword234',
            },
            follow_redirects=True
        )

    def setUp(self):
        self.db.connect()

    def tearDown(self):
        self.db.close()

    def test_register_get(self):
        response = self.client.get('/auth/register')
        confirm_pw_input = (b'<input type="password" name="confirm_pw" '
                            b'placeholder="Confirm Password"><br/>')
        page_header = b'<h1>Create Account</h1'

        self.assertEqual(200, response.status_code)
        self.assertIn(confirm_pw_input, response.data)
        self.assertIn(page_header, response.data)

    def test_register_post(self):
        # successfull user creation
        response = self.register_test_user()

        self.assertEqual(200, response.status_code)
        self.assertIn(b'<h1>Login</h1>', response.data)
        self.assertIn(b'Account created. Please login.', response.data)

        user_info = User.get_user_info(self.db, None, 'test2@gmail.com')

        self.assertEqual('first2', user_info['first_name'])
        self.assertEqual('last2', user_info['last_name'])

        # failed user creation
        response = self.client.post(
            '/auth/register',
            data={
                'first_name': 'first',
                'last_name': 'last',
                'email': 'test2@gmail.com',
                'password': 'TestPassword234',
                'confirm_pw': 'TestPassword123',
            },
            follow_redirects=True
        )

        self.assertEqual(200, response.status_code)
        self.assertIn(b'<h1>Create Account</h1>', response.data)
        self.assertIn(b'Account creation failed.', response.data)
        self.assertIn(b'Passwords do not match!', response.data)
        self.assertIn(b'User with this email already exists.', response.data)

        # remove all users
        self.db.trucate_table('users')

    def test_get_login(self):
        # GET Request
        response = self.client.get('/auth/login')
        self.assertEqual(200, response.status_code)
        self.assertIn(
            b'<button type="submit">Login</button>',
            response.data
        )

    def test_post_login(self):
        # no one is logged in
        with self.client:
            self.client.get('/')
            self.assertIsNone(session.get('user', None))

        # login
        response = self.login('test@gmail.com', 'TestPassword123')
        self.assertEqual(302, response.status_code)

        with self.client:
            self.client.get('/')
            self.assertTrue(session.get('user', None))

        # logout, clean out registered users
        self.client.get('/auth/logout')

    def test_logout(self):
        # test logout link when no one is logged in
        response = self.client.get('/auth/logout', follow_redirects=True)

        self.assertEqual(200, response.status_code)
        self.assertIn(b'<h1>Bible Q</h1', response.data)
        self.assertNotIn(b'You have been logged out!', response.data)

        # logout when someone is logged in
        self.login('test@gmail.com', 'TestPassword123')
        response = self.client.get('/auth/logout', follow_redirects=True)

        self.assertEqual(200, response.status_code)
        self.assertIn(b'<h1>Bible Q</h1', response.data)
        self.assertIn(b'You have been logged out!', response.data)
        with self.client:
            self.client.get('/')
            self.assertIsNone(session.get('user', None))
