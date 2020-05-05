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

        if not Session._cookie == None:
            return Session._cookie

        response = self._requests.post(
            self._config['VIVA']['login']['url'],
            data={
                'username': self._config['VIVA']['login']['username'],
                'password': self._config['VIVA']['login']['password'],
            },
            allow_redirects=False
        )

        Session._cookie = response.cookies[self._config['COOKIE_AUTH_NAME']]

        return Session._cookie
