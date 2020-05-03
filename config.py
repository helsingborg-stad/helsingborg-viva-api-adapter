import os

class Config:
  # Base
  SALT = os.environ.get('SALT')
  COOKIE_AUTH_NAME = os.environ.get('COOKIE_AUTH_NAME')

class DevConfig:
  DEBUG = True
  STAGE = 'dev'
  WSDL_URL = os.environ.get('DEV_WSDL_URL')
  LOGIN_POST_URL = os.environ.get('DEV_LOGIN_POST_URL')
  LOGIN_POST_USERNAME = os.environ.get('DEV_LOGIN_POST_USERNAME')
  LOGIN_POST_PASSWORD = os.environ.get('DEV_LOGIN_POST_PASSWORD')

class ProdConfig:
  DEBUG = False
  STAGE = 'prod'
  WSDL_URL = os.environ.get('PROD_WSDL_URL')
  LOGIN_POST_URL = os.environ.get('PROD_LOGIN_POST_URL')
  LOGIN_POST_USERNAME = os.environ.get('PROD_LOGIN_POST_USERNAME')
  LOGIN_POST_PASSWORD = os.environ.get('PROD_LOGIN_POST_PASSWORD')
