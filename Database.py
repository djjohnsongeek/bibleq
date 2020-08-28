from flask import current_app
import pymysql

def get_db():
    db = pymysql.connect(
        host = current_app.config['MYSQL_HOST'],
        user = current_app.config['MYSQL_USER'],
        password = current_app.config['MYSQL_PASSWORD'],
        port = current_app.config['MYSQL_PORT'],
        db = current_app.config['MYSQL_DB'],
        charset = current_app.config['MYSQL_CHARSET'],
        cursorclass = pymysql.cursors.DictCursor,
    )

    return db