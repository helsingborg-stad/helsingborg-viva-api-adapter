import json
from app import create_app


def test_user_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/[hashId]' page is requested (GET)
    THEN check that the response is a user
    """

    flask_app = create_app()
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        response = test_client.get(
            '/user/RPwl497dEgao8B0ma7RJykVr6b5LJ1Nq', headers={'X-Api-Key': 'abc123Testing'})

        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['type'] == 'EkbUser'
