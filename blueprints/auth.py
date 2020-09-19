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
    # register a new user
    if request.method == 'POST':
        new_user = User(g.db, User.parse_user_info(request.form))

        if not new_user.errors:
            flash('Account created. Please login.', 'info')
        else:
            flash('Account creation failed.', 'info')
            for error_msg in new_user.errors:
                flash(error_msg, 'error')

        return redirect(url_for('auth.login'))
        
    # display register form
    return render_template('auth/register.html')


@blue_print.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('auth/login.html')


@blue_print.route('/logout', methods=('GET',))
def logout():
    return 'logout'
