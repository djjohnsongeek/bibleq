from flask import (
    Blueprint,
    render_template,
)

blue_print = Blueprint('home', __name__)


@blue_print.route('/', methods=('GET',))
def index():
    return render_template('index.html')
