from flask import current_app
from classes.User import User


class Question():

    def __init__(self, db, data):
        self.db = db

        self.errors = self._validate(data)

        if not self.errors:
            self.id = None
            self.poster_id = data['poster_id']
            self.writer_id = data.get('writer_id')
            self.answer_id = data.get('answer_id')
            self.title = data['title']
            self.body = data['body']
            self.unfit_flag_count = data.get('unfit_flag_count', 0)
        
            self.create()

    def create(self):
        cur = self.db.conn.cursor()
        sql = ('INSERT INTO questions ('
               'original_poster_id, writer_id,'
               'answer_id, title, body, unfit_flag_count)'
               'VALUES (%s, %s, %s, %s, %s, %s)')

        cur.execute(
            sql,
            (
                self.poster_id,
                self.writer_id,
                self.answer_id,
                self.title,
                self.body,
                self.unfit_flag_count
            )
        )

        self.db.conn.commit()
        self.id = self.db.get_last_insert_id()

        cur.close()

    @staticmethod
    def get_question_info(db, key):
        key_type = type(key)
        sql = 'SELECT * FROM questions WHERE '

        if key_type == int:
            sql = sql + 'question_id = %s;'
        elif key_type == str:
            sql = sql + 'title = %s;'
        else:
            return None

        cur = db.conn.cursor()

        cur.execute(sql, (key, ))
        question_info = cur.fetchone()
        cur.close()

        return question_info

    def _validate(self, question_data):
        errors = []

        errors.extend(self._validate_title(question_data['title']))
        errors.extend(self._validate_body(question_data['body']))
        errors.extend(self._validate_poster(question_data['poster_id']))

        return errors

    def _validate_body(self, body):
        errors = []

        if not body:
            errors.append('The question\'s body cannot be blank.')

        return errors

    def _validate_title(self, title):
        errors = []

        if not title:
            errors.append('The question\'s title cannot be blank.')
        elif len(title) > current_app.config['Q_TILE_MAX_LEN']:
            errors.append(
                'The question\'s title must be less then 65 characters.'
            )

        question_info = self.get_question_info(self.db, title)
        if question_info:
            errors.append('This question already exists')

        return errors

    def _validate_poster(self, poster_id):
        errors = []
        user_info = User.get_user_info(self.db, poster_id)

        if not user_info:
            errors.append('Invalid user, new question was not created.')

        return errors
