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

blue_print = Blueprint('question', __name__, url_prefix='/question')


@blue_print.route('/create', methods=('GET',))
def create():
    return render_template('questions/create_question.html')
