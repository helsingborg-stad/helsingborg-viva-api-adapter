
def test_index_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response status code is 200
    """

    response = test_client.get('/')
    assert response.status_code == 200
