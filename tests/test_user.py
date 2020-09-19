import unittest
import sys

from werkzeug.security import generate_password_hash, check_password_hash
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

    def tearDown(self):
        self.db.trucate_table('users')

        with self.app.app_context():
            self.db.close()

    def setUp(self):
        self.user_info1 = {
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@gmail.com',
            'password': 'aGoodPassw0rd',
            'confirm_pw': 'aGoodPassw0rd',
            'question_count': 0,
            'answer_count': 0,
            'account_level': 1,
        }

        self.user_info2 = {
            'first_name': 'First2',
            'last_name': 'Last2',
            'email': 'email@gmail.com2',
            'password': 'aGoodPassw0rd2',
            'confirm_pw': 'aGoodPassw0rd2',
            'question_count': 0,
            'answer_count': 0,
            'account_level': 1,
        }

        self.user_info3 = {
            'first_name': 'First3',
            'last_name': '',
            'email': 'email.com',
            'password': 'aGoodPassw0rd3',
            'confirm_pw': 'asdkfjadasdfasdf',
            'question_count': 0,
            'answer_count': 0,
            'account_level': 4,
        }

        with self.app.app_context():
            self.db.connect()

    def test_user_init(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)

        self.assertEqual(
            user.first_name,
            self.user_info1['first_name']
        )

        self.assertEqual(
            user.last_name,
            self.user_info1['last_name']
        )

        self.assertEqual(
            user.email,
            self.user_info1['email']
        )

        self.assertTrue(
            check_password_hash(
                user.password,
                self.user_info1['password']
            )
        )

        self.assertEqual(
            user.question_count,
            self.user_info1['question_count']
        )

        self.assertEqual(
            user.answer_count,
            self.user_info1['answer_count']
        )

        self.assertEqual(
            user.account_level,
            self.user_info1['account_level']
        )

        self.assertEqual(
            user.id,
            1,
        )

        self.assertIs(self.db, user.db)

    def test_user_CRUD(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)

            self.assertEqual(1, user.id)
            result = self.db.get_row('users', 'user_id', user.id)

            self.assertEqual(result['user_id'], user.id)
            self.assertEqual(result['first_name'], user.first_name)
            self.assertEqual(result['last_name'], user.last_name)

            # update
            user.update({
                'first_name': 'new',
                'last_name': 'new',
            })

            self.assertEqual(user.first_name, 'new')
            self.assertEqual(user.last_name, 'new')

            result = self.db.get_row('users', 'user_id', user.id)

            # ensure database was updated
            self.assertEqual(result['first_name'], 'new')
            self.assertEqual(result['last_name'], 'new')

            # delete
            user.delete()
            result = self.db.get_row('users', 'user_id', user.id)

            self.assertFalse(result)

    def test_user_get_all(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)
            user2 = User(self.db, self.user_info2)

            results = user.get_all(self.db)

            self.assertEqual(len(results), 2)

    def test_parse_user_info(self):
        with self.app.app_context():
            self.user_info1['confirm_pw'] = 'aGoodPassw0rd'

            self.assertDictEqual(
                self.user_info1,
                User.parse_user_info(self.user_info1)
            )

    def test_validate_name(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)

        errors = user._validate_name('')
        self.assertListEqual(
            errors,
            ['Name fields cannot be blank.'],
        )

        errors = user._validate_name('D' * 65)
        self.assertListEqual(
            errors,
            ['Name fields must be less then 64 characters.']
        )

        errors = user._validate_name('FirstName')
        self.assertListEqual(
            errors,
            []
        )
        pass

    def test_validate_email(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)

        errors = user._validate_email('email')
        self.assertListEqual(
            errors,
            ['Email is Invalid.']
        )

        errors = user._validate_email('email@gmail.com')
        self.assertListEqual(
            errors,
            ['User with this email already exists.']
        )

        errors = user._validate_email('e' * 65 + '@gmail.com')
        self.assertListEqual(
            errors,
            ['Email address is too long.']
        )

        errors = user._validate_email('e' * 65)
        self.assertListEqual(
            errors,
            ['Email is Invalid.', 'Email address is too long.']
        )

    def test_validate_integer(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)

        errors = user._validate_integer('string')
        self.assertListEqual(
            errors,
            ['An Integer was expected.']
        )

        errors = user._validate_integer(8, 1, 3)
        self.assertListEqual(
            errors,
            ['Integer value should be less then 3.']
        )

        errors = user._validate_integer(0, 1, 3)
        self.assertListEqual(
            errors,
            ['Integer value should be at least equal to 1.']
        )

        errors = user._validate_integer('1')
        self.assertListEqual(
            errors,
            []
        )

        errors = user._validate_integer(7)
        self.assertListEqual(
            errors,
            []
        )

        errors = user._validate_integer(7, 1, 10)
        self.assertListEqual(
            errors,
            []
        )

    def test_validate_password(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)
            pw_limit = self.app.config['PW_LIMIT']

            errors = user._validate_password(
                'aGoodPassW0rd',
                'aGoodPassW0rd'
            )
            self.assertListEqual(
                errors, []
            )

            errors = user._validate_password(
                'aGoodPassw0rd1',
                'aGoodPassW0rd'
            )
            self.assertListEqual(
                errors,
                ['Passwords do not match!']
            )

            errors = user._validate_password(
                'aGood11',
                'aGood11'
            )
            self.assertListEqual(
                errors,
                ['Password cannot be shorter then ' +
                f'10 characters or longer then {pw_limit}.']
            )

            errors = user._validate_password(
                'aGood11' + 'G' * 160,
                'aGood11' + 'G' * 160
            )
            self.assertListEqual(
                errors,
                ['Password cannot be shorter then ' +
                f'10 characters or longer then {pw_limit}.']
            )

            errors = user._validate_password(
                'abadpasswordwithn0caps',
                'abadpasswordwithn0caps'
            )
            self.assertListEqual(
                errors,
                ['Password must contain an upper and lowercase letter.']
            )

            errors = user._validate_password(
                'ABADPASSWORDWITH0LOWERS',
                'ABADPASSWORDWITH0LOWERS'
            )
            self.assertListEqual(
                errors,
                ['Password must contain an upper and lowercase letter.']
            )

            errors = user._validate_password(
                'aBadPassWordWithNoNums',
                'aBadPassWordWithNoNums'
            )
            self.assertListEqual(
                errors,
                ['Password must contain at least one number.']
            )

            errors = user._validate_password(
                'password',
                'pword'
            )
            self.assertListEqual(
                errors,
                [
                    'Passwords do not match!',
                    'Password cannot be shorter then ' +
                    f'10 characters or longer then {pw_limit}.',
                    'Password must contain an upper and lowercase letter.',
                    'Password must contain at least one number.'
                ]
            )

    def test_user_validate(self):
        with self.app.app_context():
            user = User(self.db, self.user_info1)

            # user is created within init
            errors = user.validate(self.user_info1)
            self.assertListEqual(
                errors,
                ['User with this email already exists.']
            )

            
            errors = user.validate(self.user_info3)
            self.assertListEqual(
                errors,
                [
                    'Name fields cannot be blank.',
                    'Email is Invalid.',
                    'Passwords do not match!',
                    'Integer value should be less then 3.',
                ]
            )

    def test_get_user_info(self):
        with self.app.app_context():

            # create users for testing
            user1 = User(self.db, self.user_info1)
            user2 = User(self.db, self.user_info2)

            # retrieve user info by id
            user_info = User.get_user_info(self.db, 1)

            self.assertEqual(user_info['first_name'], user1.first_name)
            self.assertEqual(user_info['last_name'], user1.last_name)
            
            # instatiate user from info
            user_obj = User(self.db, user_info)
            self.assertIsInstance(user_obj, User)

            # test user info retreval failure
            user_info = User.get_user_info(self.db, 3)
            self.assertIsNone(user_info)

            # fail to instantiate user from empty info
            with self.assertRaises(Exception):
                user_obj = User(self.db, user_info)
        
            # retrieve user info by email
            user_info = User.get_user_info(
                self.db, None, self.user_info1['email']
            )
            self.assertEqual(user_info['email'], user1.email)
            self.assertEqual(user_info['first_name'], user1.first_name)
            self.assertEqual(user_info['last_name'], user1.last_name)

            # instatiate user from info
            user_obj = User(self.db, user_info)
            self.assertIsInstance(user_obj, User)

            # get non existant user+info by email
            user_info = User.get_user_info(
                self.db, None, self.user_info3['email']
            )
            self.assertIsNone(user_info)

            user_info = User.get_user_info(db)
            self.assertIsNone(user_info)