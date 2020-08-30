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

blue_print = Blueprint('auth', __name__, url_prefix='/auth')

@blue_print.route('/register', methods = ('GET', 'POST'))
def register():
    data_fetcher = DataFetcher(g.db)
    answered_qs = data_fetcher.get_answered_questions()
    unanswered_qs = data_fetcher.get_unanswered_questions()
    return "register"


@blue_print.route('/login', methods = ('GET', 'POST'))
def login():
   return "login"

@blue_print.route('/logout')
def logout():
    return "logout"
