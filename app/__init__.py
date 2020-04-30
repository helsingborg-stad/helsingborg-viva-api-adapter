import os
from flask import Flask
from flask_restful import Api

# routes
from . import routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Hello Dude!'

    api = Api(app)

    # Endpoints TEST
    api.add_resource(
        routes.Students,
        '/students/'
    )

    api.add_resource(
        routes.Student,
        '/students/<string:student_id>'
    )

    # Viva
    api.add_resource(
        routes.viva.MyPages,
        '/viva/mypages/<string:hash_id>'
    )

    return app
