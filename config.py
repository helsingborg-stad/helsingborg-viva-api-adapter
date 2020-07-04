import os


class Config:
    SALT = os.environ.get('SALT')
    COOKIE_AUTH_NAME = os.environ.get('COOKIE_AUTH_NAME')
    ENV = os.environ.get('ENV')


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
