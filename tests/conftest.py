import pytest

from app import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        yield test_client
