import os
import pytest
from typing import Any

from app import create_app
from app.libs.providers.viva_provider import AbstractVivaProvider


class TestVivaProvider(AbstractVivaProvider):
    APPLICATIONSTATUS: Any = callable
    PERSONAPPLICATION: Any = callable
    PERSONCASES: Any = callable
    PERSONINFO: Any = callable
    PERSONCASEWORKFLOW: Any = callable
    NEWAPPLICATION: Any = callable
    NEWREAPPLICATION: Any = callable
    NEWCOMPLETION: Any = callable
    SAVEDATA: Any = callable

    def create_client(self, wsdl_name: str) -> Any:
        return self


@pytest.fixture(scope='module')
def test_client():
    env = os.environ.get('ENV', 'development')
    provider = TestVivaProvider()

    flask_app = create_app(provider=provider, env=env)
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        yield test_client
