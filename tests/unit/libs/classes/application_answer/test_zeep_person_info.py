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

    client_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer('198603032395', ['personInfo', 'personalNumber', 'client']),
        answer('Milton', ['personInfo', 'firstName', 'client']),
        answer('Herlitz', ['personInfo', 'lastName', 'client', 'client']),
        answer('Gamla vägen 3', ['personInfo', 'address', 'client']),
        answer('12345', ['personInfo', 'postalCode', 'client']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'client']),
        answer('+46700121212', ['personInfo', 'phoneNumber', 'client']),
        answer('Mobiltelefon', ['personInfo', 'phoneType', 'client']),
        answer('nobody@example.com', ['personInfo', 'email', 'client']),
    ))

    assert client_person_info.create() == {
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


def test_person_info_list_client_email_and_phone_number_excluded():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application without email and phone number
    THEN check that person_info object is in the correct Viva format
    """

    client_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer('198603032391', ['personInfo', 'personalNumber', 'client']),
        answer('Milton', ['personInfo', 'firstName', 'client']),
        answer('Herlitz', ['personInfo', 'lastName', 'client']),
        answer('Min gata 1', ['personInfo', 'address', 'client']),
        answer('12345', ['personInfo', 'postalCode', 'client']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'client']),
    ))

    assert client_person_info.create() == {
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
            'PHONENUMBERS': {
                'PHONENUMBER': {
                    'NUMBER': '',
                    'SMS': False,
                    'TYPE': '',
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

    partner_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer('198603031234', ['personInfo', 'personalNumber', 'partner']),
        answer('Kajsa', ['personInfo', 'firstName', 'partner']),
        answer('Kavat', ['personInfo', 'lastName', 'partner']),
        answer('Gamla vägen 3', ['personInfo', 'address', 'partner']),
        answer('12345', ['personInfo', 'postalCode', 'partner']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'partner']),
        answer('+46700121212', ['personInfo', 'phoneNumber', 'partner']),
        answer('Mobiltelefon', ['personInfo', 'phoneType', 'partner']),
        answer('nobody@example.com', ['personInfo', 'email', 'partner']),
    ), person_type='partner')

    assert partner_person_info.create() == {
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


def test_person_info_list_partner_email_and_phone_number_excluded():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application without email and phone number
    THEN check that person_info object is in the correct Viva format
    """

    partner_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer('198603031234', ['personInfo', 'personalNumber', 'partner']),
        answer('Kajsa', ['personInfo', 'firstName', 'partner']),
        answer('Kavat', ['personInfo', 'lastName', 'partner']),
        answer('Min gata 1', ['personInfo', 'address', 'partner']),
        answer('12345', ['personInfo', 'postalCode', 'partner']),
        answer('Helsingborg', ['personInfo', 'postalAddress', 'partner']),
    ), person_type='partner')

    assert partner_person_info.create() == {
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
            'PHONENUMBERS': {
                'PHONENUMBER': {
                    'NUMBER': '',
                    'SMS': False,
                    'TYPE': '',
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

    children_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer('201201011234', ['personInfo', 'personalNumber', 'children']),
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
            'CHILD': [
                {
                    'PNUMBER': '20120101-1234',
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
            ],
        },
    }


def test_person_info_list_many_children_happy_path():
    """
    GIVEN a ZeepPersonInfo object
    WHEN submitting a new application
    THEN check that person_info object is in the correct Viva format
    """

    children_person_info = ZeepPersonInfo(application_answer_collection=answer_collection(
        answer('201201011234', ['personInfo',
               'personalNumber', 'children', 'group:0']),
        answer('Barn', ['personInfo', 'firstName',
               'children', 'group:someTagName:0']),
        answer('Barnsson', ['personInfo', 'lastName',
               'children', 'group:loremIpsum:dolor:0']),
        answer('Min gata 1', ['personInfo', 'address', 'children', 'group:0']),
        answer('12345', ['personInfo', 'postalCode', 'children', 'group:0']),
        answer('Helsingborg', ['personInfo',
               'postalAddress', 'children', 'group:0']),
        answer('+46700121212', ['personInfo',
               'phoneNumber', 'children', 'group:0']),
        answer('Mobiltelefon', ['personInfo',
               'phoneType', 'children', 'group:0']),
        answer('20010101-4321', ['personInfo',
               'personalNumber', 'children', 'group:1']),
        answer('Barn2', ['personInfo', 'firstName', 'children', 'group:1']),
        answer('Barnsson2', ['personInfo', 'lastName', 'children', 'group:1']),
        answer('Min gata 1', ['personInfo', 'address', 'children', 'group:1']),
        answer('12345', ['personInfo', 'postalCode',
               'children', 'group:dolor:set:amet:1']),
        answer('Helsingborg', ['personInfo',
               'postalAddress', 'children', 'group:children:1']),
        answer('+46733556677', ['personInfo',
               'phoneNumber', 'children', 'group:1']),
        answer('Fast', ['personInfo',
               'phoneType', 'children', 'group:1']),
    ), person_type='children')

    assert children_person_info.create() == {
        'CHILDREN': {
            'CHILD': [
                {
                    'PNUMBER': '20120101-1234',
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
                    'PNUMBER': '20010101-4321',
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
