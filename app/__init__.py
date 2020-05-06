import os
from flask import Flask
from flask_restful import Api


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    if app.config['ENV'] == 'development':
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_object('config.ProdConfig')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():

        # routes
        from . import routes

        api = Api(app)

        # Viva
        api.add_resource(
            routes.MyPages,
            '/viva/mypages/<string:hash_id>'
        )

        api.add_resource(
            routes.Applications,
            '/viva/applications'
        )

        return app
