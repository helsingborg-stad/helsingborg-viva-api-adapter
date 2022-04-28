from app.libs.classes.application_answer import ApplicationAnswer
from app.libs.classes.application_answer import ApplicationAnswerCollection
from app.libs.classes.application_answer import ZeepHousing


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

    housing = ZeepHousing(application_answer_collection=answer_collection(
        answer('Kajsa', ['housing', 'firstName']),
        answer('Kavat', ['housing', 'lastName']),
        answer('Gamla vägen 3', ['housing', 'address']),
        answer('12345', ['housing', 'postalCode']),
        answer('Helsingborg', ['housing', 'city']),
        answer('+46700121212', ['housing', 'telephone']),
        answer('nobody@example.com', ['housing', 'email']),
    ))

    assert housing.get_client() == {
        'CLIENT': {
            'FNAME': 'Kajsa',
            'LNAME': 'Kavat',
            'ADDRESSES': {
                'ADDRESS': [
                    {
                        'TYPE': 'P',
                        'ADDRESS': 'Gamla vägen 3',
                        'CO': '',
                        'ZIP': '12345',
                        'CITY': 'Helsingborg',
                    }
                ],
            },
            'PHONENUMBERS': {
                'PHONENUMBER': [
                    {
                        'TYPE': 'Mobiltelefon',
                        'NUMBER': '+46700121212',
                        'SMS': False,
                    }
                ],
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
