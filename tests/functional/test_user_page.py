import json

from app.libs.personal_number_helper import get_hash_ids, hash_to_personal_number

# Test user: Petronella Malteskog
personal_number = 198602102389


def test_user_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/[hashId]' page is requested (GET)
    THEN check that the response is a user
    """

    hash_id = get_hash_ids().encode(personal_number)
    response = test_client.get(f'/user/{hash_id}')

    data = json.loads(response.data)

    expected_personal_number = hash_to_personal_number(hash_id=hash_id)

    assert response.status_code == 200
    assert data == {
        'type': 'EkbUser',
        'attributes': {
            'personalNumber': expected_personal_number,
            'firstName': 'Petronella',
            'lastName': 'Malteskog',
            'cases': [],
            'persons': [],
        },
    }
