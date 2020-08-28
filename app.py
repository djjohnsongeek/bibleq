import os

from flask import Flask
import pymysql
import json
import Database

app = Flask(__name__)

# configure app
app.config.from_object('config')


@app.route('/')
def index():
    cursor = Database.get_db().cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='bibleq';")
    result = cursor.fetchall()
    cursor.close()
    return json.dumps(result)

@app.route('/hello')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run()