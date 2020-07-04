import requests
from flask import current_app
from zeep.transports import Transport


class Session(object):

    _cookie = None

    def __init__(self, transport=Transport, requests=requests, current_app=current_app):
        self._config = current_app.config
        self._requests = requests
        self._transport = transport

    def get_transport(self):
        cookie = self._get_cookie()

        cookie_jar = self._requests.cookies.RequestsCookieJar()
        cookie_jar.set(self._config['COOKIE_AUTH_NAME'], cookie)

        session = self._requests.Session()
        session.cookies = cookie_jar
        transport = Transport(session=session)

        return transport

    def _get_cookie(self):
        if Session._cookie is None:
            login_conf = self._config['VIVA']['login']

            response = self._requests.post(
                login_conf['url'],
                data={
                    'username': login_conf['username'],
                    'password': login_conf['password'],
                },
                allow_redirects=False,
            )

            Session._cookie = response.cookies[self._config['COOKIE_AUTH_NAME']]

        return Session._cookie
