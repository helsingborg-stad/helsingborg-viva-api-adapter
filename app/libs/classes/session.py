import requests
from flask import current_app
from flask_caching import Cache
from zeep.transports import Transport
from zeep.cache import SqliteCache

cache = Cache(current_app)


class Session(object):

    _cookie = None

    def __init__(self, transport=Transport, requests=requests, current_app=current_app):
        self._config = current_app.config
        self._requests = requests
        self._transport = transport
        self._sqlite_cache = SqliteCache('/tmp/viva_sqlite.db')

    def get_transport(self):
        self._cookie = self._get_cookie()

        cookie_jar = self._requests.cookies.RequestsCookieJar()
        cookie_jar.set(self._config['COOKIE_AUTH_NAME'], self._cookie)

        session = self._requests.Session()
        session.cookies = cookie_jar
        transport = self._transport(session=session, cache=self._sqlite_cache)

        return transport

    @cache.memoize(timeout=300)
    def _get_cookie(self):
        current_app.logger.debug(msg='COOKIE')
        login_conf = self._config['VIVA']['login']

        response = self._requests.post(
            login_conf['url'],
            data={
                'username': login_conf['username'],
                'password': login_conf['password'],
            },
            allow_redirects=False,
        )

        cookie = response.cookies[self._config['COOKIE_AUTH_NAME']]
        return cookie

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, self._cookie)
