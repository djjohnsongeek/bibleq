from pprint import pprint
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
    g,
)

import werkzeug.security as security

from classes.User import User

blue_print = Blueprint('auth', __name__, url_prefix='/auth')


@blue_print.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_data = {
            'first_name' : request.form.get('first_name'),
            'last_name' : request.form.get('last_name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm_pw': request.form.get('confirm_pw'),
            'account_level': current_app.config['USER_ACCNT'],
            'question_count': 0,
            'answer_count': 0,
        }

        user = User(g.db, user_data)
        user.create()

        flash('Account created', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@blue_print.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('auth/login.html')


@blue_print.route('/logout', methods=('GET',))
def logout():
    return 'logout'
