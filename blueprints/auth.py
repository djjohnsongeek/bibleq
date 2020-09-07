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
        user_info = User.parse_user_info(request.form)
        errors = User.validate(user_info)

        if not errors:
            user = User(g.db, user_info)
            user.create()
            flash('Account created', 'info')

        return redirect(url_for('auth.login'))

    User.get_all(g.db)
    return render_template('auth/register.html')


@blue_print.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('auth/login.html')


@blue_print.route('/logout', methods=('GET',))
def logout():
    return 'logout'
