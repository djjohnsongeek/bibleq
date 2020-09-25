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

from classes.User import User

blue_print = Blueprint('auth', __name__, url_prefix='/auth')


@blue_print.route('/register', methods=('GET', 'POST'))
def register():
    # register a new user
    if request.method == 'POST':
        new_user = User(g.db, User.parse_user_info(request.form))

        if not new_user.errors:
            flash('Account created. Please login.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Account creation failed.', 'info')
            for error_msg in new_user.errors:
                flash(error_msg, 'error')

    # display register form
    return render_template('auth/register.html')


@blue_print.route('/login', methods=('GET', 'POST'))
def login():
    # process login request
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_info = User.get_user_info(g.db, email)

        if user_info is None:
            flash('Login failed.', 'error')
        else:
            auth = security.check_password_hash(
                user_info['password'],
                password
            )

            if auth:
                session.clear()

                del user_info['password']
                session['user'] = user_info
                flash('Logged in!', 'info')

                return redirect(url_for('home.index'))
            else:
                flash('Invalid Password.', 'error')

    # display login form
    return render_template('auth/login.html')


@blue_print.route('/logout', methods=('GET',))
def logout():
    message = None

    if session.get('user', None):
        message = 'You have been logged out!'

    session.clear()

    if message:
        flash(message, 'info')

    return redirect(url_for('home.index'))
