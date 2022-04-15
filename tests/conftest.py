import pytest

from app import create_app


@pytest.fixture(scope='module')
def test_client():
    app = create_app({
        'TESTING': True,
    })

    with app.test_client() as test_client:
        yield test_client
