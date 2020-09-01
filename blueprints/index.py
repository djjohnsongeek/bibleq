from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    g,
)

import werkzeug.security as security
from classes.DataFetcher import DataFetcher
from classes.Question import Question

blue_print = Blueprint('index', __name__)
    
@blue_print.route('/', methods = ('GET',))
def index():
    db = g.db
    path = r'C:\Users\Johnson\Projects\flask-app\bibleq\models\bibleq_schema.sql'

    result = db.execute_sql_file(path)
    if result:
        message = 'success'
    else:
        message = 'failure'
    
    return message