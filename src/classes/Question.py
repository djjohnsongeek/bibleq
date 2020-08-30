class Question():
    

    def __init__(self, db, data):
        self.conn = db.conn

        self.poster_id = data["poster_id"]
        self.writer_id = data["writer_id"]
        self.answer_id = data.get("answer_id", None)
        self.body = data["body"]
        self.unfit_flag_count = data.get("unfit_flag_count", 0)

    def create(self):
        cur = self.conn.cursor()
        sql = """
                INSERT INTO questions (
                    original_poster_id, writer_id, answer_id, body, unfit_flag_count)
                VALUES (%s, %s, %s, %s, %s)
              """

        cur.execute(sql, (self.poster_id, self.writer_id, self.answer_id, self.body, self.unfit_flag_count))
        self.conn.commit()
        
        cur.close()