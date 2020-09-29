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
        with app.app_context():
            db.connect()

    def tearDown(self):
        with app.app_context():
            db.trucate_table('questions')
            db.close()

    def test_question_init(self):
        # also tests create
        question_data = {
            'title': 'Test Question Title',
            'body': 'Testing Body Text',
            'poster_id': 1,
        }

        # test init works
        with app.app_context():
            new_question = Question(db, question_data)

        self.assertEqual(new_question.errors, [])
        self.assertEqual(new_question.id, 1)
        self.assertEqual(new_question.title, question_data['title'])
        self.assertEqual(new_question.body, question_data['body'])
        self.assertEqual(new_question.poster_id, 1)
        self.assertEqual(new_question.unfit_flag_count, 0)
        self.assertIsNone(new_question.answer_id)
        self.assertIsNone(new_question.writer_id)

        # test init created questiong row in db
        with app.app_context():
            question_info = Question.get_question_info(db, 1)

        self.assertEqual(question_info['title'], question_data['title'])
        self.assertEqual(question_info['body'], question_data['body'])
        self.assertEqual(
            question_info['original_poster_id'],
            question_data['poster_id']
        )

        self.assertEqual(question_info['question_id'], 1)

        # error when question already in db
        question_data['title'] = 'Test Question Title'
        with app.app_context():
            new_question = Question(db, question_data)

        self.assertEqual(
            new_question.errors,
            ['This question already exists']
        )
        with self.assertRaises(AttributeError):
            new_question.title

        # errors when q title is too long
        question_data['title'] = 128 * 'TooLong'
        with app.app_context():
            new_question = Question(db, question_data)

        self.assertEqual(
            new_question.errors,
            ['The question\'s title must '
             'be less then 65 characters.']
        )

        # errors when title, body are blank, user is nonexistant
        question_data['title'] = ''
        question_data['body'] = ''
        question_data['poster_id'] = 5
        with app.app_context():
            new_question = Question(db, question_data)

        self.assertEqual(
            new_question.errors,
            [
                'The question\'s title cannot be blank.',
                'The question\'s body cannot be blank.',
                'Invalid user, new question was not created.',
            ]
        )
        
    def test_get_question_info(self):
        with app.app_context():
            question_info = Question.get_question_info(db, 1)
            self.assertIsNone(question_info)
            
            question_info = Question.get_question_info(db, 'Test Question?')
            self.assertIsNone(question_info)

            Question(db,
                {
                    'title': 'Test Question?',
                    'body': 'Test Body',
                    'poster_id': 1,
                }
            )

            question_info = Question.get_question_info(db, 'Test Question?')
            self.assertTrue(question_info)

            question_info = Question.get_question_info(db, 1)
            self.assertTrue(question_info)