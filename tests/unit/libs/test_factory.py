import os

from app import create_app
from tests.conftest import TestVivaProvider


def test_factory():
    env = os.environ.get('ENV', 'development')
    provider = TestVivaProvider()

    assert not create_app(provider=provider, env=env).testing
    assert create_app(provider=provider, test_config={'TESTING': True}).testing
