class DataFetcher():

    def __init__(self, db):
        self.conn = db.conn

    def get_answered_questions(self):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM questions WHERE answer_id != null;"
        )
        results = cur.fetchall()
        cur.close()

        return results
        
    def get_unanswered_questions(self):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM questions WHERE answer_id = null;"
        )
        results = cur.fetchall()
        cur.close()

        return results