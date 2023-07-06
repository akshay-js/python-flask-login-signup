import os

from flask import Flask, g
from .routes.routes import user_bp
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["JWT_SECRET_KEY"] = "super-secret"
    jwt = JWTManager(app)

    app.debug = False
    from . import db
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(user_bp, url_prefix='/api')
    return app