class User():

    def __init__(self, db, data):

        self.db = db

        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.account_level = data['account_level']
        self.question_count = data['question_count']
        self.answer_count = data['answer_count']
        self.password = data['password']

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

        cur.close()

    def validate_user(self, user_data):
        pass



