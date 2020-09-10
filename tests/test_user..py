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

    def tearDown(self):
        self.db.trucate_table('users')

    def test_user_init(self):
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

        self.assertEqual(
            user.password,
            self.user_info1['password']
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
            None,
        )

        self.assertIs(self.db, user.db)

    def test_user_CRUD(self):
        user = User(self.db, self.user_info1)

        # create
        user.create()

        self.assertEqual(1, user.id)
        result = self.db.get_row('users', 'user_id', user.id)

        self.assertEqual(result['user_id'], user.id)
        self.assertEqual(result['first_name'], user.first_name)
        self.assertEqual(result['last_name'], user.last_name)

        # update
        user.update(first_name='new', last_name='new')

        self.assertEqual(user.first_name, 'new')
        self.assertEqual(user.last_name, 'new')

        # delete
        user.delete()
        result = self.db.get_row('users', 'user_id', user.id)

        self.assertFalse(result)

    def test_user_get_all(self):
        user = User(self.db, self.user_info1)
        user.create()

        user2 = User(self.db, self.user_info2)
        user2.create()

        results = user.get_all(self.db)

        self.assertEqual(len(results), 2)

    def test_parse_user_info(self):
        self.user_info1['confirm_pw'] = 'aGoodPassw0rd'

        self.assertDictEqual(
            self.user_info1,
            User.parse_user_info(self.user_info1)
        )

    def test_validate_name(self):
        errors = User.validate_name('')
        self.assertListEqual(
            errors,
            ['Name field cannot be blank.'],
        )

        errors = User.validate_name('D' * 65)
        self.assertListEqual(
            errors,
            ['Name fields must be less then 64 characters.']
        )

        errors = User.validate_name('FirstName')
        self.assertListEqual(
            errors,
            []
        )
        pass

    def test_validate_email(self):
        errors = User.validate_email('email')
        self.assertListEqual(
            errors,
            ['Email is Invalid.']
        )

        errors = User.validate_email('email@gmail.com')
        self.assertListEqual(
            errors,
            []
        )

        errors = User.validate_email('e' * 65 + '@gmail.com')
        self.assertListEqual(
            errors,
            ['Email address is too long.']
        )

        errors = User.validate_email('e' * 65)
        self.assertListEqual(
            errors,
            ['Email is Invalid.', 'Email address is too long.']
        )

    def test_validate_integer(self):
        errors = User.validate_integer('string')
        self.assertListEqual(
            errors,
            ['An Integer was expected.']
        )

        errors = User.validate_integer(8, 1, 3)
        self.assertListEqual(
            errors,
            ['Integer value should be less then 3.']
        )

        errors = User.validate_integer(0, 1, 3)
        self.assertListEqual(
            errors,
            ['Integer value should be at least equal to 1.']
        )

        errors = User.validate_integer('1')
        self.assertListEqual(
            errors,
            []
        )

        errors = User.validate_integer(7)
        self.assertListEqual(
            errors,
            []
        )

        errors = User.validate_integer(7, 1, 10)
        self.assertListEqual(
            errors,
            []
        )

    def test_validate_password(self):
        errors = User.validate_password(
            'aGoodPassW0rd',
            'aGoodPassW0rd'
        )
        self.assertListEqual(
            errors, []
        )

        errors = User.validate_password(
            'aGood',
            'aGoodPassW0rd'
        )
        self.assertListEqual(
            errors,
            ['Passwords do not match!']
        )

        errors = User.validate_password(
            'aGood11',
            'aGood11'
        )
        self.assertListEqual(
            errors,
            ['Passwords cannot be shorter then ' +
             '10 characters or longer then 164.']
        )

        errors = User.validate_password(
            'aGood11' + 'G' * 160,
            'aGood11' + 'G' * 160
        )
        self.assertListEqual(
            errors,
            ['Passwords cannot be shorter then ' +
             '10 characters or longer then 164.']
        )

        errors = User.validate_password(
            'abadpasswordwithn0caps',
            'abadpasswordwithn0caps'
        )
        self.assertListEqual(
            errors,
            ['Password must contain an upper and lowercase letter.']
        )

        errors = User.validate_password(
            'ABADPASSWORDWITH0LOWERS',
            'ABADPASSWORDWITH0LOWERS'
        )
        self.assertListEqual(
            errors,
            ['Password must contain an upper and lowercase letter.']
        )

        errors = User.validate_password(
            'aBadPassWordWithNoNums',
            'aBadPassWordWithNoNums'
        )
        self.assertListEqual(
            errors,
            ['Password must contain at least one number.']
        )

        errors = User.validate_password(
            'password',
            'pword'
        )
        self.assertListEqual(
            errors,
            [
                'Passwords do not match!',
                'Passwords cannot be shorter then ' +
                '10 characters or longer then 164.',
                'Password must contain an upper and lowercase letter.',
                'Password must contain at least one number.'
            ]
        )

    def test_user_validate(self):
        errors = User.validate(self.user_info1)

        self.assertListEqual(
            errors, []
        )

        errors = User.validate(self.user_info3)
        self.assertListEqual(
            errors,
            [
                'Name field cannot be blank.',
                'Email is Invalid.',
                'Passwords do not match!',
                'Integer value should be less then 3.',
            ]
        )
