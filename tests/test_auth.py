import unittest

from bibleq import create_app
from classes.Database import db
from classes.User import User

# TODO check url with response.headers['Location']
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

    def setUp(self):
        self.db.connect()

    def tearDown(self):
        self.db.close()

    def test_register_get(self):
        response = self.client.get('/auth/register')

        confirm_pw_input = (b'<input type="password" name="confirm_pw" '
                            b'placeholder="Confirm Password"><br/>')
        page_header = b'<h1>Create Account</h1'
        # page_url = self.domain_name + response.headers.get('Location')

        self.assertEqual(200, response.status_code)
        # self.assertEqual(page_url, self.domain_name + '/auth/register')
        self.assertIn(confirm_pw_input, response.data)
        self.assertIn(page_header, response.data)

    def test_register_post(self):
        # successfull user creation
        response = self.client.post(
            '/auth/register',
            data = {
                'first_name': 'Daniel',
                'last_name': 'Johnson',
                'email': 'danieleejohnson@gmail.com',
                'password': 'DJohnson1234',
                'confirm_pw': 'DJohnson1234',
            },
            follow_redirects=True
        )
        # page_url = self.domain_name + response.headers.get('Location')

        self.assertEqual(200, response.status_code)
        # self.assertEqual(page_url, self.domain_name + '/auth/login')
        self.assertIn(b'<h1>Login</h1>', response.data)
        self.assertIn(b'Account created. Please login.', response.data)

        user_info = User.get_user_info(self.db, 1, None)

        self.assertEqual('Daniel', user_info['first_name'])
        self.assertEqual('Johnson', user_info['last_name'])

        # failed user creation
        response = self.client.post(
            '/auth/register',
            data = {
                'first_name': 'Daniel',
                'last_name': 'Johnson',
                'email': 'danieleejohnson@gmail.com',
                'password': 'DJOhnson1234',
                'confirm_pw': 'DJohnson1234',
            },
            follow_redirects = True
        )

        self.assertEqual(200, response.status_code)
        self.assertIn(b'<h1>Create Account</h1>', response.data)
        self.assertIn(b'Account creation failed.', response.data)
        self.assertIn(b'Passwords do not match!', response.data)
        self.assertIn(b'User with this email already exists.', response.data)

    def test_logout(self):
        # test logout link when no one is logged in
        response = self.client.get('/auth/logout', follow_redirects=True)

        self.assertEqual(200, response.status_code)
        self.assertIn(b'<h1>Bible Q</h1', response.data)
        self.assertNotIn(b'You have been logged out!', response.data)

        # TODO test logout when someone is logged in
        # login()
        # response = self.client.get('/auth/logout', follow_redirects=True)

        # self.assertEqual(200, response.status_code)
        # self.assertIn(b'<h1>Bible Q</h1', response.data)
        # self.assertIn(b'You have been logged out!', response.data)