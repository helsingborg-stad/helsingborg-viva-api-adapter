import json

from app import create_app
from app.libs.data_domain.api_user import ApiUser
from app.libs.personal_number_helper import get_hash_ids
from tests.conftest import TestVivaProvider
from tests.unit.libs.classes.providers.test_viva_provider import create_viva_xml_person_cases_mock
from tests.unit.libs.classes.providers.test_viva_provider import create_viva_xml_person_application_mock

env = 'development'

# Test user
personal_number = 198602102389
first_name = 'Petronella'
last_name = 'Malteskog'


def test_user_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/[hashId]' page is requested (GET)
    THEN check that the response is a ekb user
    """

    provider = TestVivaProvider()
    provider.PERSONAPPLICATION = lambda USER, PNR, SSI, WORKFLOWID, RETURNAS: create_viva_xml_person_application_mock(
        mock_data={
            'start': '2023-04-01',
            'end': '2023-04-30',
        })

    provider.PERSONCASES = lambda USER, PNR, SYSTEM, RETURNAS: create_viva_xml_person_cases_mock(
        mock_data={
            'personal_number': personal_number,
            'first_name': first_name,
            'last_name': last_name,
        })

    provider.PERSONCASEWORKFLOW = lambda USER, PNR, SSI, MAXWORKFLOWS, RETURNAS: '''
        <vivadata>
            <vivacaseworkflows>
                <workflow></workflow>
            </vivacaseworkflows>
        </vivadata>
    '''

    flask_app = create_app(provider=provider, env=env)
    flask_app.testing = True

    with flask_app.test_client() as test_client:

        hash_id = get_hash_ids().encode(personal_number)
        response = test_client.get(f'/user/{hash_id}')

        data = json.loads(response.data)

        assert response.status_code == 200
        assert data == {
            'type': 'EkbUser',
            'attributes': {
                'id': '01-2021-09-30/R37992',
                'personalNumber': str(personal_number),
                'firstName': first_name,
                'lastName': last_name,
                'cases': [{
                    'period': {
                        'startDate': '2023-04-01',
                        'endDate': '2023-04-28'
                    },
                    'recievedISOTime': '2023-04-03T15:15:03+02:00',
                    'completion': {
                        'items': [{
                            'description': 'Underlag på alla sökta utgifter',
                            'received': False
                        }],
                        'description': 'Lämna in det här tack',
                        'receivedDate': '2023-04-04',
                        'dueDate': '2023-04-05',
                        'uploadedDocuments': [
                            'a.pdf',
                            'b.jpg'
                        ],
                        'isCompleted': False,
                        'isRandomCheck': False,
                        'isAttachmentPending': False,
                        'isDueDateExpired': True
                    },
                    'calculations': [{
                        'description': 'Beräkning 2022-12-03 - 2023-01-02 (RIKS), Att besluta 8 650,00 kr',
                        'incomes': [{
                            'date': ''
                        }],
                        'expenses': [],
                        'reductions': [],
                        'norms': [],
                        'note': ''
                    }],
                    'decisions': [{
                        'cause': {
                            'self': '',
                            'partner': '?'
                        },
                        'amount': 500,
                        'description': ''
                    }],
                    'payments': [{
                        'method': 'Avi',
                        'giveDate': '2023-04-20',
                        'description': ''
                    }],
                    'journalNotes': [{
                        'label': 'A',
                        'message': 'asd'
                    }]
                }],
                'relatedPersons': [{
                    'firstName': 'kompis',
                    'lastName': 'samma',
                    'personalNumber': '200001019999',
                    'type': 'partner'
                }, {
                    'firstName': 'lille',
                    'lastName': 'vän',
                    'personalNumber': '202001019999',
                    'type': 'child'
                }],
            },
        }
