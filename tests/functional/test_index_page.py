from app import create_app


def test_index_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    flask_app = create_app()
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
