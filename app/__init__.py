from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from requests.exceptions import ConnectionError


class ExtendedFlaskRestfulApi(Api):

    def handle_error(self, error):
        print('Error: ', error)

        if isinstance(error, HTTPException):
            return {
                'message': getattr(
                    error, 'description', HTTP_STATUS_CODES.get(error.code, '')
                )
            }, error.code

        if isinstance(error, ConnectionError):
            return {
                'message': getattr(
                    error, 'description', HTTP_STATUS_CODES.get(502, '')
                )
            }, 502

        if not getattr(error, 'message', None):
            return {
                'message': 'Server has encountered some error'
            }, 500

        # Handle application specific custom exceptions
        return jsonify(**error.kwargs), error.http_status_code


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

        api = ExtendedFlaskRestfulApi(app)

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
