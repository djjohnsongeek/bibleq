import os
import sys

from flask import Flask, url_for, g
import pymysql
import json

from bibleq.src.classes.Database import Database
from bibleq.src.classes.Question import Question

app = Flask(__name__)

# configure app
app.config.from_object('config')

# initialize database
db = Database(app.config)

@app.before_request
def before_each_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_each_request(response):
    g.db.close()
    g.pop('db')
    
    return response

from bibleq.src.blueprints import auth
app.register_blueprint(auth.blue_print)

@app.route('/')
def index():
    data = dict(
        poster_id = 1,
        writer_id = None,
        answer_id = None,
        body = "who is Jesus?",
        unfit_flag_counft = 0,
    )
    question = Question(g.db, data)
    question.create()

    return "created q"

if __name__ == '__main__':
    app.run()