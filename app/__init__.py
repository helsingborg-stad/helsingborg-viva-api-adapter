from flask import Flask
from flask_restful import Api


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    if app.config['ENV'] == 'development':
        app.config.from_object('config.DevConfig')
    elif app.config['ENV'] == 'test':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.ProdConfig')

    with app.app_context():

        from . import routes

        api = Api(app)

        # Viva adapter api endpoints
        api.add_resource(
            routes.MyPages,
            '/mypages/',
            '/mypages/<string:hash_id>',
        )

        api.add_resource(
            routes.MyPagesWorkflows,
            '/mypages/<string:hash_id>/workflows/',
            '/mypages/<string:hash_id>/workflows/<string:workflow_id>',
        )

        api.add_resource(
            routes.Applications,
            '/applications',
            '/applications/<string:hash_id>/status',
        )

        api.add_resource(
            routes.Attachments,
            '/attachments',
            '/attachments/<string:hash_id>/attachment/<string:attachment_id>',
        )

        api.add_resource(
            routes.TestCookie,
            '/testcookie/',
        )

        api.add_resource(
            routes.Index,
            '/',
        )

    return app
