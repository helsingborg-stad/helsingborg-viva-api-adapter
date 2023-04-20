import requests
from abc import abstractmethod, ABC
from flask import current_app
from zeep.transports import Transport
from zeep.cache import SqliteCache

from app.cache import cache


class AbstractSession(ABC):

    @abstractmethod
    def __init__(self, config: dict) -> None:
        self._config = config

    @abstractmethod
    def get_transport(self):
        pass


class Session(AbstractSession):

    _cookie = None

    def __init__(self, config: dict):
        self._config = config

    def get_transport(self):
        self._cookie = self._get_cookie()

        session = requests.Session()
        session.cookies.set(self._config['COOKIE_AUTH_NAME'], self._cookie)

        transport = Transport(
            session=session, cache=SqliteCache('/tmp/viva_sqlite.db'))

        return transport

    @cache.memoize(timeout=300)
    def _get_cookie(self):
        current_app.logger.debug(msg='COOKIE')
        login_conf = self._config['VIVA']['login']

        response = requests.post(
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
