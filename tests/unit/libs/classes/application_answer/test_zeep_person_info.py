from app.libs.classes.application_answer.answer import ApplicationAnswer
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.zeep_person_info import ZeepPersonInfo


def answer_collection(*args):
    return ApplicationAnswerCollection(*args)


def answer(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


def test_person_info_list_client_happy_path():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application
    THEN check that person_info object is in the correct Viva format
    """

    personal_number = '19860303-2395'

    client_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer(personal_number, ['personInfo', 'personalNumber', 'client']),
        answer('Milton', ['personInfo', 'firstName', 'client']),
        answer('Herlitz', ['personInfo', 'lastName', 'client', 'client']),
        answer('Gamla vägen 3', ['personInfo', 'address', 'client']),
        answer('12345', ['personInfo', 'postalCode', 'client']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'client']),
        answer('+46700121212', ['personInfo', 'telephone', 'client']),
        answer('nobody@example.com', ['personInfo', 'email', 'client']),
    ))

    assert client_person_info.create() == {
        'CLIENT': {
            'PNUMBER': personal_number,
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


def test_person_info_list_client_email_and_phone_number_excluded():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application without email and phone number
    THEN check that person_info object is in the correct Viva format
    """

    personal_number = '19860303-2391'

    client_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer(personal_number, ['personInfo', 'personalNumber', 'client']),
        answer('Milton', ['personInfo', 'firstName', 'client']),
        answer('Herlitz', ['personInfo', 'lastName', 'client']),
        answer('Min gata 1', ['personInfo', 'address', 'client']),
        answer('12345', ['personInfo', 'postalCode', 'client']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'client']),
    ))

    assert client_person_info.create() == {
        'CLIENT': {
            'PNUMBER': personal_number,
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
            'PHONENUMBERS': {
                'PHONENUMBER': {
                    'NUMBER': '',
                    'SMS': False,
                    'TYPE': 'Mobiltelefon',
                }
            },
            'EMAIL': {
                'EMAIL': '',
                'NOTIFY': False,
            },
            'FOREIGNCITIZEN': False,
            'RESIDENCEPERMITTYPE': '',
            'RESIDENCEPERMITDATE': '',
            'CIVILSTATUS': 'G',
            'ALTCIVILSTATUS': '',
        },
    }


def test_person_info_list_partner_happy_path():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application
    THEN check that person_info object is in the correct Viva format
    """

    personal_number = '19860303-1234'

    partner_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer(personal_number, ['personInfo', 'personalNumber', 'partner']),
        answer('Kajsa', ['personInfo', 'firstName', 'partner']),
        answer('Kavat', ['personInfo', 'lastName', 'partner']),
        answer('Gamla vägen 3', ['personInfo', 'address', 'partner']),
        answer('12345', ['personInfo', 'postalCode', 'partner']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'partner']),
        answer('+46700121212', ['personInfo', 'telephone', 'partner']),
        answer('nobody@example.com', ['personInfo', 'email', 'partner']),
    ), person_type='partner')

    assert partner_person_info.create() == {
        'PARTNER': {
            'PNUMBER': personal_number,
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


def test_person_info_list_partner_email_and_phone_number_excluded():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application without email and phone number
    THEN check that person_info object is in the correct Viva format
    """

    personal_number = '19860303-1234'

    partner_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer(personal_number, ['personInfo', 'personalNumber', 'partner']),
        answer('Kajsa', ['personInfo', 'firstName', 'partner']),
        answer('Kavat', ['personInfo', 'lastName', 'partner']),
        answer('Min gata 1', ['personInfo', 'address', 'partner']),
        answer('12345', ['personInfo', 'postalCode', 'partner']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'partner']),
    ), person_type='partner')

    assert partner_person_info.create() == {
        'PARTNER': {
            'PNUMBER': personal_number,
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
            'PHONENUMBERS': {
                'PHONENUMBER': {
                    'NUMBER': '',
                    'SMS': False,
                    'TYPE': 'Mobiltelefon',
                },
            },
            'EMAIL': {
                'EMAIL': '',
                'NOTIFY': False,
            },
            'FOREIGNCITIZEN': False,
            'RESIDENCEPERMITTYPE': '',
            'RESIDENCEPERMITDATE': '',
            'CIVILSTATUS': 'G',
            'ALTCIVILSTATUS': '',
        },
    }


def test_person_info_list_children_happy_path():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application
    THEN check that person_info object is in the correct Viva format
    """

    personal_number = '20120101-1234'

    children_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer(personal_number, ['personInfo', 'personalNumber', 'children']),
        answer('Barn', ['personInfo', 'firstName', 'children']),
        answer('Barnsson', ['personInfo', 'lastName', 'children']),
        answer('Min gata 1', ['personInfo', 'address', 'children']),
        answer('12345', ['personInfo', 'postalCode', 'children']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'children']),
        answer('+46700121212', ['personInfo',
               'phoneNumber', 'children']),
        answer('Mobiltelefon', ['personInfo', 'phoneType', 'children']),
    ), person_type='children')

    assert children_person_info.create() == {
        'CHILDREN': {
            'CHILD': {
                'PNUMBER': personal_number,
                'FNAME': 'Barn',
                'LNAME': 'Barnsson',
                'ADDRESSES': {
                    'ADDRESS': {
                        'TYPE': 'FB',
                        'ADDRESS': 'Min gata 1',
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
                    'EMAIL': '',
                    'NOTIFY': False,
                },
                'FOREIGNCITIZEN': False,
                'RESIDENCEPERMITTYPE': '',
                'RESIDENCEPERMITDATE': '',
                'CIVILSTATUS': '',
                'ALTCIVILSTATUS': '',
                'REGISTEREDATHOUSEHOLDADDRESS': '',
                'ALTERNATELYWITHPARENTS': '',
                'ISPARTTIMECHILD': '',
                'PARTTIMECHILDDAYS': '',
            },
        },
    }


def test_person_info_list_many_children_happy_path():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application
    THEN check that person_info object is in the correct Viva format
    """

    personal_number_first_child = '20120101-1234'
    personal_number_second_child = '20010101-1234'

    children_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer(personal_number_first_child, ['personInfo',
               'personalNumber', 'children', 'group:0']),
        answer('Barnsson2', ['personInfo', 'lastName', 'children', 'group:1']),
        answer('Barn', ['personInfo', 'firstName', 'children', 'group:0']),
        answer('Barnsson', ['personInfo', 'lastName', 'children', 'group:0']),
        answer('Min gata 1', ['personInfo', 'address', 'children', 'group:0']),
        answer('12345', ['personInfo', 'postalCode', 'children', 'group:0']),
        answer('Helsingborg', ['personInfo',
               'postalAddress', 'children', 'group:0']),
        answer('+46700121212', ['personInfo',
               'phoneNumber', 'children', 'group:0']),
        answer('Mobiltelefon', ['personInfo',
               'phoneType', 'children', 'group:0']),
        answer(personal_number_second_child, ['personInfo',
               'personalNumber', 'children', 'group:1']),
        answer('Barn2', ['personInfo', 'firstName', 'children', 'group:1']),
        answer('Min gata 1', ['personInfo', 'address', 'children', 'group:1']),
        answer('12345', ['personInfo', 'postalCode', 'children', 'group:1']),
        answer('Helsingborg', ['personInfo',
               'postalAddress', 'children', 'group:1']),
        answer('+46733556677', ['personInfo',
               'phoneNumber', 'children', 'group:1']),
        answer('Fast', ['personInfo',
               'phoneType', 'children', 'group:1']),
    ), person_type='children')

    assert children_person_info.create() == {
        'CHILDREN': {
            'CHILD': [
                {
                    'PNUMBER': personal_number_first_child,
                    'FNAME': 'Barn',
                    'LNAME': 'Barnsson',
                    'ADDRESSES': {
                        'ADDRESS': {
                            'TYPE': 'FB',
                            'ADDRESS': 'Min gata 1',
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
                        'EMAIL': '',
                        'NOTIFY': False,
                    },
                    'FOREIGNCITIZEN': False,
                    'RESIDENCEPERMITTYPE': '',
                    'RESIDENCEPERMITDATE': '',
                    'CIVILSTATUS': '',
                    'ALTCIVILSTATUS': '',
                    'REGISTEREDATHOUSEHOLDADDRESS': '',
                    'ALTERNATELYWITHPARENTS': '',
                    'ISPARTTIMECHILD': '',
                    'PARTTIMECHILDDAYS': '',
                },
                {
                    'PNUMBER': personal_number_second_child,
                    'FNAME': 'Barn2',
                    'LNAME': 'Barnsson2',
                    'ADDRESSES': {
                        'ADDRESS': {
                            'TYPE': 'FB',
                            'ADDRESS': 'Min gata 1',
                            'CO': '',
                            'ZIP': '12345',
                            'CITY': 'Helsingborg',
                        },
                    },
                    'PHONENUMBERS': {
                        'PHONENUMBER': {
                            'TYPE': 'Fast',
                            'NUMBER': '+46733556677',
                            'SMS': False,
                        },
                    },
                    'EMAIL': {
                        'EMAIL': '',
                        'NOTIFY': False,
                    },
                    'FOREIGNCITIZEN': False,
                    'RESIDENCEPERMITTYPE': '',
                    'RESIDENCEPERMITDATE': '',
                    'CIVILSTATUS': '',
                    'ALTCIVILSTATUS': '',
                    'REGISTEREDATHOUSEHOLDADDRESS': '',
                    'ALTERNATELYWITHPARENTS': '',
                    'ISPARTTIMECHILD': '',
                    'PARTTIMECHILDDAYS': '',
                },
            ],
        },
    }
