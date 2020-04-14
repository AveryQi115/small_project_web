import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    # instance_relative_config should point to instance file path(no need to push to a remote repository)
    app = Flask(__name__, instance_relative_config=True)

    # dev is for security settings in flask, when the project comes to be used,dev should be set to a random number
    # database relate to database files path
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # config py is for formal configuration if exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
