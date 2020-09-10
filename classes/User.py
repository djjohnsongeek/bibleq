import re

from flask import current_app

from classes.Util import Util


class User():

    def __init__(self, db, user_params):

        self.db = db

        self.first_name = user_params['first_name']
        self.last_name = user_params['last_name']
        self.email = user_params['email']
        self.account_level = user_params['account_level']
        self.question_count = user_params.get('question_count', 0)
        self.answer_count = user_params.get('answer_count', 0)
        self.password = user_params['password']
        self.id = None

    def create(self):
        cur = self.db.conn.cursor()
        sql = ('INSERT INTO users'
               '(first_name, last_name, email, '
               'password, question_count, '
               'answer_count, account_level) '
               'VALUES (%s, %s, %s, %s, %s, %s, %s);')

        cur.execute(sql, (
            self.first_name,
            self.last_name,
            self.email,
            self.password,
            self.question_count,
            self.answer_count,
            self.account_level,)
        )

        self.db.conn.commit()
        self.id = self.db.get_last_insert_id()

        cur.close()

    def update(self, **fields):
        self.db.update_row(
            'users',
            {'user_id': self.id},
            fields
        )

        pass

    @staticmethod
    def parse_user_info(form_data):

        user_info = {
            'first_name': form_data.get('first_name'),
            'last_name': form_data.get('last_name'),
            'email': form_data.get('email'),
            'password': form_data.get('password'),
            'confirm_pw': form_data.get('confirm_pw'),
            'account_level': current_app.config['USER_ACCNT'],
            'question_count': 0,
            'answer_count': 0,
        }

        return user_info

    def delete(self):
        cur = self.db.conn.cursor()
        sql = 'DELETE FROM users WHERE user_id = %s;'
        result = cur.execute(sql, self.id)

        if result == 1:
            self.db.conn.commit()
            result = True
        else:
            result = False

        cur.close()
        return result

    @staticmethod
    def get_all(db):
        cur = db.conn.cursor()

        cur.execute(
            'SELECT * FROM users;'
        )

        results = cur.fetchall()
        cur.close()

        return results

    # validation methods
    @staticmethod
    def validate(user_info):
        errors = []

        errors.extend(
            User.validate_name(user_info['first_name']))

        errors.extend(
            User.validate_name(user_info['last_name']))

        errors.extend(
            User.validate_email(user_info['email']))

        errors.extend(
            User.validate_password(
                user_info['password'],
                user_info['confirm_pw'])
            )

        errors.extend(
            User.validate_integer(user_info['question_count']))

        errors.extend(
            User.validate_integer(user_info['answer_count']))

        errors.extend(
            User.validate_integer(
                user_info['account_level'],
                start=1,
                end=3)
            )

        return errors

    @staticmethod
    def validate_name(name):
        errors = []

        if not name:
            errors.append('Name field cannot be blank')

        if len(name) > 64:
            errors.append(
                'Name fields must be less then 64 characters'
            )

        return errors

    @staticmethod
    def validate_email(email):
        errors = []
        # regex from https://emailregex.com/
        # basic validation, not full-proof
        regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]'
                           r'+\.[a-zA-Z0-9-.]+$)')

        if not regex.match(email):
            errors.append('Email is Invalid')

        if len(email) > 64:
            errors.append('Email address is too long')

        return errors

    @staticmethod
    def validate_password(password, confirm_pw):
        errors = []
        app = current_app

        if password != confirm_pw:
            errors.append('Passwords do not match!')

        if (len(password) < app.config['PW_LENGTH'] or
            len(password) > app.config['PW_LIMIT']):

            errors.append(f'Password cannot be shorter then '
                          f'{app.config["PW_LENGTH"]} characters '
                          f'or longer then {app.config["PW_LIMIT"]}.')

        if (not Util.contains_upper(password)
           or not Util.contains_lower(password)):

            errors.append('Password must contain an upper '
                          'and lowercase letter.')

        if not Util.contains_num(password):
            errors.append('Password must contain at least one number.')

        return errors

    @staticmethod
    def validate_integer(integer, start=None, end=None):
        errors = []

        try:
            integer = int(integer)
        except TypeError:
            errors.append('An Integer was expected.')
            return errors

        if start and integer < start:
            errors.append(f'Integer value should be at '
                          f' least equal to {start}.')

        if end and integer > end:
            errors.append(f'Integer value should be less then {end}.')

        return errors

    # add get user?