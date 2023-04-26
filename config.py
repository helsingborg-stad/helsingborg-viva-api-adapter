import os
from typing import Union
from dataclasses import dataclass


@dataclass
class VivaLoginConfig:
    url: Union[str, None]
    username: Union[str, None]
    password: Union[str, None]


@dataclass
class VivaConfig:
    wsdl_url: Union[str, None]
    cookie_auth_name: Union[str, None]
    login: Union[VivaLoginConfig, None]


class DevConfig:
    SALT = os.environ.get('DEV_SALT')
    DEBUG = True
    STAGE = 'dev'
    PUBLIC_KEY_FILE = os.environ.get('DEV_PUBLIC_KEY_FILE')
    VIVA = VivaConfig(
        wsdl_url=os.environ.get('DEV_WSDL_URL'),
        cookie_auth_name=os.environ.get('DEV_COOKIE_AUTH_NAME'),
        login=VivaLoginConfig(
            url=os.environ.get('DEV_LOGIN_POST_URL'),
            username=os.environ.get('DEV_LOGIN_POST_USERNAME'),
            password=os.environ.get('DEV_LOGIN_POST_PASSWORD'),
        )
    )


class TestConfig:
    SALT = os.environ.get('TEST_SALT')
    DEBUG = False
    STAGE = 'test'
    PUBLIC_KEY_FILE = os.environ.get('TEST_PUBLIC_KEY_FILE')
    VIVA = VivaConfig(
        wsdl_url=os.environ.get('TEST_WSDL_URL'),
        cookie_auth_name=os.environ.get('DEV_COOKIE_AUTH_NAME'),
        login=VivaLoginConfig(
            url=os.environ.get('TEST_LOGIN_POST_URL'),
            username=os.environ.get('TEST_LOGIN_POST_USERNAME'),
            password=os.environ.get('TEST_LOGIN_POST_PASSWORD'),
        )
    )


class ProdConfig:
    SALT = os.environ.get('PROD_SALT')
    DEBUG = False
    STAGE = 'prod'
    PUBLIC_KEY_FILE = os.environ.get('PROD_PUBLIC_KEY_FILE')
    VIVA = VivaConfig(
        wsdl_url=os.environ.get('PROD_WSDL_URL'),
        cookie_auth_name=os.environ.get('PROD_COOKIE_AUTH_NAME'),
        login=VivaLoginConfig(
            url=os.environ.get('PROD_LOGIN_POST_URL'),
            username=os.environ.get('PROD_LOGIN_POST_USERNAME'),
            password=os.environ.get('PROD_LOGIN_POST_PASSWORD'),
        )
    )
