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

# user current_app insite a request to access app
import werkzeug.security as security

blue_print = Blueprint('auth', __name__, url_prefix='/auth')


@blue_print.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        flash('Account created', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@blue_print.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('auth/login.html')


@blue_print.route('/logout', methods=('GET',))
def logout():
    return 'logout'
