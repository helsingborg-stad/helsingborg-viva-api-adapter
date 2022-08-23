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

        from app.routes.my_pages import MyPages
        from app.routes.my_pages_workflows import MyPagesWorkflows
        from app.routes.my_pages_workflow_latest import MyPagesWorkflowLatest
        from app.routes.my_pages_workflow_completions import MyPagesWorkflowCompletions
        from app.routes.applications import Applications
        from app.routes.application_status import ApplicationStatus
        from app.routes.completions import Completions
        from app.routes.attachments import Attachments
        from app.routes.check_cookie import CheckCookie
        from app.routes.to_hashid import ToHashId
        from app.routes.index import Index

        # Viva adapter api endpoints
        api.add_resource(
            MyPages,
            '/mypages/',
            '/mypages/<string:hash_id>',
        )

        api.add_resource(
            MyPagesWorkflows,
            '/mypages/<string:hash_id>/workflows/',
            '/mypages/<string:hash_id>/workflows/<string:workflow_id>',
        )

        api.add_resource(
            MyPagesWorkflowLatest,
            '/mypages/<string:hash_id>/workflows/latest',
        )

        api.add_resource(
            MyPagesWorkflowCompletions,
            '/mypages/<string:hash_id>/workflows/<string:workflow_id>/completions',
        )

        api.add_resource(
            Applications,
            '/applications',
        )

        api.add_resource(
            ApplicationStatus,
            '/applications/<string:hash_id>/status',
        )

        api.add_resource(
            Completions,
            '/applications/<string:hash_id>/completions',
        )

        api.add_resource(
            Attachments,
            '/attachments',
        )

        api.add_resource(
            CheckCookie,
            '/testcookie/',
        )

        api.add_resource(
            ToHashId,
            '/tohashid/<int:personal_number>',
        )

        api.add_resource(
            Index,
            '/',
        )

    return app
