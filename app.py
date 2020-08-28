import os

from flask import Flask
# from flaskext.mysql import MySQL

app = Flask(__name__)

# configure app
app.config.from_object('config')

# mysql = MySQL()
# mysql.init_app(app)

# use blueprints

@app.route('/')
def index():
    print(app.config["DEBUG"])
    return "index"

@app.route('/hello')
def hello():
    # cursor = mysql.get_db().cursor()
    return 'Hello World'


if __name__ == '__main__':
    app.run()