import json

from app import create_app
from app.libs.personal_number_helper import get_hash_ids

from tests.conftest import TestVivaProvider
from tests.unit.libs.classes.providers.test_viva_provider import create_viva_xml_person_cases_mock
from tests.unit.libs.classes.providers.test_viva_provider import create_viva_xml_person_application_mock

env = 'development'

# Test user
personal_number = 198602102389
first_name = 'Petronella'
last_name = 'Malteskog'


def test_my_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mypages' page is requested (GET)
    THEN check that the response status code is 200
    """

    provider = TestVivaProvider()
    provider.PERSONAPPLICATION = lambda USER, PNR, SSI, WORKFLOWID, RETURNAS: create_viva_xml_person_application_mock(
        mock_data={
            'start': '2023-01-01',
            'end': '2023-01-31',
        })

    provider.PERSONCASES = lambda USER, PNR, SYSTEM, RETURNAS: create_viva_xml_person_cases_mock(
        mock_data={
            'personal_number': personal_number,
            'first_name': first_name,
            'last_name': last_name,
        })

    flask_app = create_app(provider=provider, env=env)
    flask_app.testing = True

    with flask_app.test_client() as test_client:

        hash_id = get_hash_ids().encode(personal_number)
        response = test_client.get(f'/mypages/{hash_id}')

        data = json.loads(response.data)

        assert response.status_code == 200
        assert data == {
            'type': 'myPages',
            'attributes': {
                'cases': {
                    'vivacases': {
                        'vivacase': {
                            'casessi': {
                                'server': None,
                                'path': None,
                                'id': None,
                            },
                            'client': {
                                'pnumber': str(personal_number),
                                'fname': first_name,
                                'lname': last_name,
                            },
                            'persons': None
                        },
                    },
                },
                'application': {
                    'vivaapplication': {
                        'period': {
                            'start': '2023-01-01',
                            'end': '2023-01-31',
                        },
                        'rawdata': None,
                    },
                },
            },
        }
