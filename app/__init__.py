from flask import Flask
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin

from app.cache import cache
from app.api import CustomFlaskRestfulApi
from app.libs.providers.ekb_abc_provider import EkbABCProvider


def create_app(provider: EkbABCProvider, test_config=None, env=None) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=False)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        if env == 'development':
            app.config.from_object('config.DevConfig')
        elif env == 'test':
            app.config.from_object('config.TestConfig')
        else:
            app.config.from_object('config.ProdConfig')

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='EKB API',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.2',
            info={
                'description': 'Viva to EKB API',
            }
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
        'components': {
            'security_scheme': {
                'ApiKeyAuth': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'X-API-KEY',
                },
            },
        },
    })

    cache.init_app(app)
    docs = FlaskApiSpec(app)

    with app.app_context():
        api = CustomFlaskRestfulApi(app)

        from app.routes.user import User
        from app.routes.my_pages import MyPages
        from app.routes.my_pages_workflows import MyPagesWorkflows
        from app.routes.my_pages_workflow_latest import MyPagesWorkflowLatest
        from app.routes.my_pages_workflow_completions import MyPagesWorkflowCompletions
        from app.routes.applications import Applications
        from app.routes.status import Status
        from app.routes.completions import Completions
        from app.routes.attachments import Attachments
        from app.routes.check_cookie import CheckCookie
        from app.routes.to_hashid import ToHashId
        from app.routes.index import Index

        api.add_resource(
            User,
            '/user/<string:hash_id>',
            resource_class_kwargs={'provider': provider},
        )

        api.add_resource(
            MyPages,
            '/mypages/',
            '/mypages/<string:hash_id>',
            resource_class_kwargs={'provider': provider},
        )

        api.add_resource(
            MyPagesWorkflows,
            '/mypages/<string:hash_id>/workflows',
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
            Status,
            '/applications/<string:hash_id>/status',
            resource_class_kwargs={'provider': provider},
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
            '/testcookie',
        )

        api.add_resource(
            ToHashId,
            '/tohashid/<int:personal_number>',
        )

        api.add_resource(
            Index,
            '/',
        )

    docs.register(User)

    return app
