from app import create_app


def test_factory():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
