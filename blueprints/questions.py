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

from classes.Question import Question

blue_print = Blueprint('questions', __name__, url_prefix='/questions')


@blue_print.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        flash('Your Question has been created.', 'info')

    return render_template('questions/create_question.html')
