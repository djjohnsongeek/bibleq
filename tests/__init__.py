from bibleq import create_app
from classes.Database import db

# helper functions
def login(email, password):
    return client.post(
        "/auth/login", data={
            "email": email,
            "password": password
        }
    )

app = create_app({
    'TESTING': True,
    'MYSQL_DB': 'bibleq_test',
    'TEST_SQL_PATH': r'C:\Users\Johnson\Projects\flask-'
                     + r'app\bibleq\tests\temp\test.sql',
})
client = app.test_client()

db.init(app.config)
db.execute_sql_file(db.schema_path)
db.close()
