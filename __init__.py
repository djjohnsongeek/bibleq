from flask import Flask, g

def create_app(test_config = None):
    app = Flask(__name__)

    # configure app
    app.config.from_object('config')

    # initialize database
    from classes.Database import db
    db.init(app.config)

    @app.before_request
    def before_each_request():
        g.db = db
        g.db.connect()

    @app.after_request
    def after_each_request(response):
        g.db.close()
        g.pop('db')
        
        return response

    # register routes
    from blueprints import auth
    app.register_blueprint(auth.blue_print)

    from blueprints import index
    app.register_blueprint(index.blue_print)

    return app