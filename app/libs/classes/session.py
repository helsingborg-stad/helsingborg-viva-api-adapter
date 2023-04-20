import requests
from abc import abstractmethod, ABC
from flask import current_app
from zeep.transports import Transport
from zeep.cache import SqliteCache

from app.cache import cache


class AbstractSession(ABC):

    @abstractmethod
    def __init__(self, config) -> None:
        self._config = config

    @abstractmethod
    def get_transport(self):
        pass


class Session(AbstractSession):

    _cookie = None

    def __init__(self, config):
        self._config = config

    def get_transport(self):
        self._cookie = self._get_cookie()

        session = requests.Session()
        session.cookies.set(self._config.cookie_auth_name, self._cookie)

        transport = Transport(
            session=session, cache=SqliteCache('/tmp/viva_sqlite.db'))

        return transport

    @cache.memoize(timeout=300)
    def _get_cookie(self):
        current_app.logger.debug(msg='COOKIE')
        login_config = self._config.login

        response = requests.post(
            login_config.url,
            data={
                'username': login_config.username,
                'password': login_config.password,
            },
            allow_redirects=False,
        )

        cookie = response.cookies[self._config.cookie_auth_name]
        return cookie

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, self._cookie)
