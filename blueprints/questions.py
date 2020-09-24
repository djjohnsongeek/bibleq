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

from classes.Util import Util
from classes.Question import Question

blue_print = Blueprint('questions', __name__, url_prefix='/questions')


@blue_print.route('/create', methods=('GET', 'POST'))
def create():
    if not Util.authenticate(session, current_app.config['USER_ACCNT']):
        flash('You must login to ask a new question.', 'info')
        return redirect(url_for('home.index'))

    if request.method == 'POST':

        q_data = {
            'title': request.form.get('question_title'),
            'body': request.form.get('question_body'),
            'poster_id': session['user']['user_id'],
            'writer_id': None,
            'answer_id': None,
            'unfit_flag_cont': 0,
        }
        new_question = Question(g.db, q_data)

        if not new_question.errors:
            flash('Your Question has been created.', 'info')
        else:
            for error in new_question.errors:
                flash(error, 'error')

    return render_template('questions/create_question.html')
