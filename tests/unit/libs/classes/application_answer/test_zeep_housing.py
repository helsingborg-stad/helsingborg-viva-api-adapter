from app.libs.classes.application_answer.answer import ApplicationAnswer
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.zeep_housing import ZeepHousing


def answer_collection(*args):
    return ApplicationAnswerCollection(*args)


def answer(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


def test_housing_list_client_happy_path():
    """
    GIVEN a ZeepHousing object
    WHEN submitting a new application
    THEN check that housing object is in the correct Viva format
    """

    personal_number = '19860303-2395'

    housing = ZeepHousing(application_answer_collection=answer_collection(
        answer('Milton', ['housing', 'firstName', 'client']),
        answer('Herlitz', ['housing', 'lastName', 'client']),
        answer('Gamla vägen 3', ['housing', 'address', 'client']),
        answer('12345', ['housing', 'postalCode', 'client']),
        answer('Helsingborg', ['housing', 'postalAddress', 'client']),
        answer('+46700121212', ['housing', 'telephone', 'client']),
        answer('nobody@example.com', ['housing', 'email', 'client']),
    ))

    assert housing.get_client(personal_number, 'client') == {
        'CLIENT': {
            'PNUMBER': '19860303-2395',
            'FNAME': 'Milton',
            'LNAME': 'Herlitz',
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


def test_housing_list_client_email_and_phone_number_excluded():
    """
    GIVEN a ZeepHousing object
    WHEN submitting a new application without email and phone number
    THEN check that housing object is in the correct Viva format
    """

    personal_number = '19860303-2391'

    housing = ZeepHousing(application_answer_collection=answer_collection(
        answer('Milton', ['housing', 'firstName', 'client']),
        answer('Herlitz', ['housing', 'lastName', 'client']),
        answer('Min gata 1', ['housing', 'address', 'client']),
        answer('12345', ['housing', 'postalCode', 'client']),
        answer('Helsingborg', ['housing', 'postalAddress', 'client']),
    ))

    assert housing.get_client(personal_number, 'client') == {
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


def test_housing_list_partner_happy_path():
    """
    GIVEN a ZeepHousing object
    WHEN submitting a new application
    THEN check that housing object is in the correct Viva format
    """

    personal_number = '19860303-1234'

    housing = ZeepHousing(application_answer_collection=answer_collection(
        answer('Kajsa', ['housing', 'firstName', 'partner']),
        answer('Kavat', ['housing', 'lastName', 'partner']),
        answer('Gamla vägen 3', ['housing', 'address', 'partner']),
        answer('12345', ['housing', 'postalCode', 'partner']),
        answer('Helsingborg', ['housing', 'postalAddress', 'partner']),
        answer('+46700121212', ['housing', 'telephone', 'partner']),
        answer('nobody@example.com', ['housing', 'email', 'partner']),
    ))

    assert housing.get_client(personal_number, 'partner') == {
        'PARTNER': {
            'PNUMBER': '19860303-1234',
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


def test_housing_list_partner_email_and_phone_number_excluded():
    """
    GIVEN a ZeepHousing object
    WHEN submitting a new application without email and phone number
    THEN check that housing object is in the correct Viva format
    """

    personal_number = '19860303-1234'

    housing = ZeepHousing(application_answer_collection=answer_collection(
        answer('Kajsa', ['housing', 'firstName', 'partner']),
        answer('Kavat', ['housing', 'lastName', 'partner']),
        answer('Min gata 1', ['housing', 'address', 'partner']),
        answer('12345', ['housing', 'postalCode', 'partner']),
        answer('Helsingborg', ['housing', 'postalAddress', 'partner']),
    ))

    assert housing.get_client(personal_number, 'partner') == {
        'PARTNER': {
            'PNUMBER': '19860303-1234',
            'FNAME': 'Kajsa',
            'LNAME': 'Kavat',
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
