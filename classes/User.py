import re

from flask import current_app
from werkzeug.security import generate_password_hash

from classes.Util import Util


class User():

    def __init__(self, db, user_params):
        self.db = db
        self.errors = None

        if not user_params.get('user_id', None):
            self.errors = self.validate(user_params)

        if not self.errors:
            self.id = user_params.get('user_id', None)
            self.first_name = user_params['first_name']
            self.last_name = user_params['last_name']
            self.email = user_params['email']
            self.account_level = user_params.get('account_level', 1)
            self.question_count = user_params.get('question_count', 0)
            self.answer_count = user_params.get('answer_count', 0)
            self.password = user_params['password']

            if not user_params.get('user_id', None):
                self.create()

    def create(self):
        cur = self.db.conn.cursor()
        sql = ('INSERT INTO users'
               '(first_name, last_name, email, '
               'password, question_count, '
               'answer_count, account_level) '
               'VALUES (%s, %s, %s, %s, %s, %s, %s);')
        self.password = generate_password_hash(self.password)

        cur.execute(sql, (
            self.first_name,
            self.last_name,
            self.email,
            self.password,
            self.question_count,
            self.answer_count,
            self.account_level,)
        )

        self.db.commit()
        self.id = self.db.get_last_insert_id()

        cur.close()

    def update(self, fields):
        id_column = {
            'field_name': 'user_id',
            'id': self.id,
        }
        self.db.update_row('users', id_column, fields)

        # update instance attributes
        for field in fields.items():
            self.__setattr__(field[0], field[1])

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
    def get_user_info(db, key):
        ''' key can be either int or str (user_id or email) '''

        # test_auth_post fails w/o this
        if db.conn is None:
            db.connect()

        cur = db.conn.cursor()
        sql = 'SELECT * FROM users WHERE '

        arg_type = type(key)

        if arg_type == int:
            sql = sql + 'user_id = %s;'
        elif arg_type == str:
            sql = sql + 'email = %s;'
        else:
            return None

        value = key

        cur.execute(sql, (value,))
        result = cur.fetchone()
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

    # validation methods
    def validate(self, user_info):
        errors = []

        errors.extend(
            self._validate_name(user_info['first_name'])
        )

        errors.extend(
            self._validate_name(user_info['last_name'])
        )

        errors.extend(
            self._validate_email(user_info['email'])
        )

        errors.extend(
            self._validate_password(
                user_info['password'],
                user_info['confirm_pw']
            )
        )

        q_count = user_info.get('question_count', 0)
        errors.extend(
            self._validate_integer(q_count)
        )

        a_count = user_info.get('answer_count', 0)
        errors.extend(
            self._validate_integer(a_count)
        )

        level = user_info.get('account_level', 1)
        errors.extend(
            self._validate_integer(level, start=1, end=3)
        )

        return errors

    def _validate_name(self, name):
        errors = []

        if not name:
            errors.append('Name fields cannot be blank.')

        if len(name) > 64:
            errors.append(
                'Name fields must be less then 64 characters.'
            )

        return errors

    def _validate_email(self, email):
        errors = []

        # regex from https://emailregex.com/
        # basic validation, not full-proof
        regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]'
                           r'+\.[a-zA-Z0-9-.]+$)')

        if not regex.match(email):
            errors.append('Email is Invalid.')

        if len(email) > 64:
            errors.append('Email address is too long.')

        user_info = self.get_user_info(self.db, email)
        if user_info:
            errors.append('User with this email already exists.')

        return errors

    def _validate_password(self, password, confirm_pw):
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

    def _validate_integer(self, integer, start=None, end=None):
        errors = []

        try:
            integer = int(integer)
        except ValueError:
            errors.append('An Integer was expected.')
            return errors

        if start and integer < start:
            errors.append(f'Integer value should be at '
                          f'least equal to {start}.')

        if end and integer > end:
            errors.append(f'Integer value should be less then {end}.')

        return errors

    # 'load' user from database
