from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException


class CustomApi(Api):

    def handle_error(self, err):
        print(err)  # log every exception raised in the application
        if isinstance(err, HTTPException):
            return jsonify({
                'message': getattr(
                    err, 'description', HTTP_STATUS_CODES.get(err.code, '')
                )
            }), err.code

        # If msg attribute is not set,
        # consider it as Python core exception and
        # hide sensitive error info from end user
        if not getattr(err, 'message', None):
            return jsonify({
                'message': 'Server has encountered some error'
            }), 500

        # Handle application specific custom exceptions
        return jsonify(**err.kwargs), err.http_status_code


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

        api = CustomApi(app)

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
        )

        api.add_resource(
            routes.ApplicationStatus,
            '/applications/<string:hash_id>/status',
        )

        api.add_resource(
            routes.Completions,
            '/applications/<string:hash_id>/completions',
        )

        api.add_resource(
            routes.Attachments,
            '/attachments',
        )

        api.add_resource(
            routes.Attachment,
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
