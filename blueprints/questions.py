from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app
)

from classes.Util import Util

blue_print = Blueprint('questions', __name__, url_prefix='/questions')


@blue_print.route('/create', methods=('GET', 'POST'))
def create():
    if not Util.authenticate(session, current_app.config['USER_ACCNT']):
        flash('Your must login to ask a new question.', 'info')
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        flash('Your Question has been created.', 'info')

    return render_template('questions/create_question.html')
