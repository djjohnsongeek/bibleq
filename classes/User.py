from flask import current_app

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
            'first_name' : form_data.get('first_name'),
            'last_name' : form_data.get('last_name'),
            'email': form_data.get('email'),
            'password': form_data.get('password'),
            'confirm_pw': form_data.get('confirm_pw'),
            'account_level': current_app.config['USER_ACCNT'],
            'question_count': 0,
            'answer_count': 0,
        }

        return user_info


    @staticmethod
    def delete(self, user):
        cur = self.db.conn.cursor()
        sql = 'DELETE FROM users WHERE user_id = %s;'
        cur.execute(sql, user.id)
        cur.close()

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

        errors = errors + User.validate_name(user_info['first_name'])
        errors = errors + User.validate_name(user_info['last_name'])
        errors = errors + User.validate_email(user_info['email'])
        errors = errors + User.validate_password(user_info['password'], user_info['confirm_pw'])
        errors = errors + User.validate_integer(user_info['question_count'])
        errors = errors + User.validate_integer(user_info['answer_count'])
        errors = errors + User.validate_integer(user_info['account_level'], start=1, end=3)

        return errors

    @staticmethod
    def validate_name(name):
        pass

    @staticmethod
    def validate_email(email):
        pass

    @staticmethod
    def validate_password(password, confirm_pw):
        pass

    @staticmethod
    def validate_integer(integer, start=None, end=None):
        pass



