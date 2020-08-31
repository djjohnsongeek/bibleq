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