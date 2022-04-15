import os
from flask import Flask

from app.cache import cache
from app.api import CustomFlaskRestfulApi


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        if app.config['ENV'] == 'development':
            app.config.from_object('config.DevConfig')
        elif app.config['ENV'] == 'test':
            app.config.from_object('config.TestConfig')
        else:
            app.config.from_object('config.ProdConfig')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cache.init_app(app)

    with app.app_context():
        api = CustomFlaskRestfulApi(app)

        from . import routes

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
            routes.MyPagesWorkflowLatest,
            '/mypages/<string:hash_id>/workflows/latest',
        )

        api.add_resource(
            routes.MyPagesWorkflowCompletions,
            '/mypages/<string:hash_id>/workflows/<string:workflow_id>/completions',
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
            routes.ToHashId,
            '/tohashid/<int:personal_number>',
        )

        api.add_resource(
            routes.Index,
            '/',
        )

    return app
