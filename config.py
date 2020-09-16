import os


class Config:
    SALT = os.environ.get('SALT')
    COOKIE_AUTH_NAME = os.environ.get('COOKIE_AUTH_NAME')


class DevConfig(Config):
    DEBUG = True
    STAGE = 'dev'
    VIVA = {
        'wsdl_url': os.environ.get('DEV_WSDL_URL'),
        'login': {
            'url': os.environ.get('DEV_LOGIN_POST_URL'),
            'username': os.environ.get('DEV_LOGIN_POST_USERNAME'),
            'password': os.environ.get('DEV_LOGIN_POST_PASSWORD'),
        },
    }


class TestConfig(Config):
    DEBUG = False
    STAGE = 'test'
    VIVA = {
        'wsdl_url': os.environ.get('TEST_WSDL_URL'),
        'login': {
            'url': os.environ.get('TEST_LOGIN_POST_URL'),
            'username': os.environ.get('TEST_LOGIN_POST_USERNAME'),
            'password': os.environ.get('TEST_LOGIN_POST_PASSWORD'),
        },
    }


class ProdConfig(Config):
    DEBUG = False
    STAGE = 'prod'
    VIVA = {
        'wsdl_url': os.environ.get('PROD_WSDL_URL'),
        'login': {
            'url': os.environ.get('PROD_LOGIN_POST_URL'),
            'username': os.environ.get('PROD_LOGIN_POST_USERNAME'),
            'password': os.environ.get('PROD_LOGIN_POST_PASSWORD'),
        },
    }
