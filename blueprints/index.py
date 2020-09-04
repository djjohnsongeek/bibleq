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
from classes.Question import Question

blue_print = Blueprint('index', __name__)


@blue_print.route('/', methods=('GET',))
def index():
    return "index"
