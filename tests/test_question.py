import unittest

from tests import app, db
from classes.User import User
from classes.Question import Question

class TestQuestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create a user for testing
        user_info = {
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@gmail.com',
            'password': 'aGoodPassw0rd',
            'confirm_pw': 'aGoodPassw0rd',
            'question_count': 0,
            'answer_count': 0,
            'account_level': 1,
        }

        with app.app_context():
            User(db, user_info)
    
    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.connect()
            db.trucate_table('users')
            db.trucate_table('questions')
            db.close()

    def setUp(self):
        question_data = {
            'title': 'Test Question Title',
            'body': 'Testing Body Text',
            'poster_id': 1,
        }

        with app.app_context():
            db.connect()

            self.new_question = Question(
                db,
                question_data
            )

    def tearDown(self):
        with app.app_context():
            db.trucate_table('questions')
            db.close()

    def test_question_init(self):
        question_data = {
            'title': 'Test Question Title2',
            'body': 'Testing Body Text2',
            'poster_id': 1,
        }

        # test init works
        with app.app_context():
            new_question = Question(db, question_data)

        self.assertEqual(new_question.errors, [])
        self.assertEqual(new_question.id, 2)
        self.assertEqual(new_question.title, question_data['title'])
        self.assertEqual(new_question.body, question_data['body'])
        self.assertEqual(new_question.poster_id, 1)
        self.assertEqual(new_question.unfit_flag_count, 0)
        self.assertIsNone(new_question.answer_id)
        self.assertIsNone(new_question.writer_id)

        # test init created questiong row in db
        with app.app_context():
            question_info = Question.get_question_info(db, 2)

        self.assertEqual(question_info['question_id'], 2)
        self.assertEqual(question_info['title'], question_data['title'])
        self.assertEqual(question_info['body'], question_data['body'])
        self.assertEqual(
            question_info['original_poster_id'],
            question_data['poster_id']
        )
        
    def test_get_question_info(self):
        with app.app_context():
            # no info exists
            question_info = Question.get_question_info(db, 2)
            self.assertIsNone(question_info)
            
            question_info = Question.get_question_info(db, 'Test Question?')
            self.assertIsNone(question_info)

            # info exists
            question_info = Question.get_question_info(db, 'Test Question Title')
            self.assertTrue(question_info)

            question_info = Question.get_question_info(db, 1)
            self.assertTrue(question_info)

    def test_validate(self):
        with app.app_context():
            # no errors
            question_data = {
                'title': 'Test Question Title2',
                'body': 'Testing Body Text2',
                'poster_id': 1,
            }
            errors = self.new_question._validate(question_data)
            self.assertEqual(errors, [])

            # error are returned
            question_data['title'] = 'Test Question Title'
            errors = self.new_question._validate(question_data)
            self.assertTrue(errors)

    def test_validate_poster(self):
        with app.app_context():

            errors = self.new_question._validate_poster(1)
            self.assertEqual(errors, [])

            errors = self.new_question._validate_poster(5)
            self.assertEqual(
                errors,
                ['Invalid user, new question was not created.']
            )
    
    def test_validate_title(self):
        with app.app_context():
            # no errors
            errors = self.new_question._validate_title('Question?')
            self.assertEqual(errors, [])

            # question title exists
            errors = self.new_question._validate_title('Test Question Title')
            self.assertEqual(
                errors,
                ['This question already exists']
            )

            # title is too long
            errors = self.new_question._validate_title(128 * 'TooLong')
            self.assertEqual(
                errors,
                ['The question\'s title must '
                'be less then 65 characters.']
            )

            # title is blank
            errors = self.new_question._validate_title('')
            self.assertEqual(
                errors,
                ['The question\'s title cannot be blank.']
            )

    def test_validate_body(self):
        with app.app_context():

            errors = self.new_question._validate_body('Body')
            self.assertEqual(errors, [])
            
            errors = self.new_question._validate_body('')
            self.assertEqual(errors, ['The question\'s body cannot be blank.'])