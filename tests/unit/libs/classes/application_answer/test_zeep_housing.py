from app.libs.classes.application_answer.answer import ApplicationAnswer
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.zeep_housing import ZeepHousing


def answer_collection(*args):
    return ApplicationAnswerCollection(*args)


def answer(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


def test_housing_list_happy_path():
    """
    GIVEN a ZeepHousing object
    WHEN submitting a new application
    THEN check that housing object is in the correct Viva format
    """

    personal_number = '19860303-2395'

    housing = ZeepHousing(application_answer_collection=answer_collection(
        answer('Kajsa', ['housing', 'firstName']),
        answer('Kavat', ['housing', 'lastName']),
        answer('Gamla vägen 3', ['housing', 'address']),
        answer('12345', ['housing', 'postalCode']),
        answer('Helsingborg', ['housing', 'postalAddress']),
        answer('+46700121212', ['housing', 'telephone']),
        answer('nobody@example.com', ['housing', 'email']),
    ))

    assert housing.get_client(personal_number) == {
        'CLIENT': {
            'PNUMBER': '19860303-2395',
            'FNAME': 'Kajsa',
            'LNAME': 'Kavat',
            'ADDRESSES': {
                'ADDRESS': {
                    'TYPE': 'FB',
                    'ADDRESS': 'Gamla vägen 3',
                    'CO': '',
                    'ZIP': '12345',
                    'CITY': 'Helsingborg',
                },
            },
            'PHONENUMBERS': {
                'PHONENUMBER': {
                    'TYPE': 'Mobiltelefon',
                    'NUMBER': '+46700121212',
                    'SMS': False,
                },
            },
            'EMAIL': {
                'EMAIL': 'nobody@example.com',
                'NOTIFY': False,
            },
            'FOREIGNCITIZEN': False,
            'RESIDENCEPERMITTYPE': '',
            'RESIDENCEPERMITDATE': '',
            'CIVILSTATUS': 'G',
            'ALTCIVILSTATUS': '',
        },
    }


def test_housing_list_email_and_phone_number_excluded():
    """
    GIVEN a ZeepHousing object
    WHEN submitting a new application without email and phone number
    THEN check that housing object is in the correct Viva format
    """

    personal_number = '19860303-2391'

    housing = ZeepHousing(application_answer_collection=answer_collection(
        answer('Milton', ['housing', 'firstName']),
        answer('Herlitz', ['housing', 'lastName']),
        answer('Min gata 1', ['housing', 'address']),
        answer('12345', ['housing', 'postalCode']),
        answer('Helsingborg', ['housing', 'postalAddress']),
    ))

    assert housing.get_client(personal_number) == {
        'CLIENT': {
            'PNUMBER': '19860303-2391',
            'FNAME': 'Milton',
            'LNAME': 'Herlitz',
            'ADDRESSES': {
                'ADDRESS': {
                    'TYPE': 'FB',
                    'ADDRESS': 'Min gata 1',
                    'CO': '',
                    'ZIP': '12345',
                    'CITY': 'Helsingborg',
                },
            },
            'PHONENUMBERS': None,
            'EMAIL': {'EMAIL': '', 'NOTIFY': ''},
            'FOREIGNCITIZEN': False,
            'RESIDENCEPERMITTYPE': '',
            'RESIDENCEPERMITDATE': '',
            'CIVILSTATUS': 'G',
            'ALTCIVILSTATUS': '',
        },
    }
