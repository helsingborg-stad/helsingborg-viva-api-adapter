from .. import ApplicationAnswer
from .. import ApplicationAnswerCollection
from .. import ZeepApplication


def answer_collection(*args):
    return ApplicationAnswerCollection(*args)


def answer(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


def test_get_posts_answer_amount_value_happy_path():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer(678.45, ['expenses', 'reskostnad', 'amount']),
    ))

    posts = zeep_dict._get_posts(post_group_name='EXPENSES')

    assert posts == [
        {
            'TYPE': 'reskostnad',
            'FREQUENCY': 12,
            'DATE': '',
            'PERIOD': '',
            'APPLIESTO': 'applicant',
            'DESCRIPTION': 'Reskostnad',
            'AMOUNT': 678.45,
        },
    ]


def test_get_posts_answer_amount_value_is_empty():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer('', ['expenses', 'bredband', 'amount']),
    ))

    posts = zeep_dict._get_posts(post_group_name='EXPENSES')

    assert posts == []


def test_get_post_answer_amount_value_happy_path():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer('5000', ['expenses', 'akuttandvard', 'amount']),
    ))

    posts = zeep_dict._get_post(
        post_type='akuttandvard', post_type_attributes={})

    assert posts == {
        'TYPE': 'akuttandvard',
        'FREQUENCY': 12,
        'DATE': '',
        'PERIOD': '',
        'APPLIESTO': 'applicant',
        'DESCRIPTION': 'Akut tandvård',
    }


def test_get_post_type_answers_happy_path():
    answer_item = answer(6745, ['expenses', 'bostad', 'amount'])
    zeep_dict = ZeepApplication(
        application_answer_collection=answer_collection(answer_item))

    posts = zeep_dict._get_post_type_answers(
        post_name='bostad', post_group_name='EXPENSES')

    assert posts == [answer_item]


def test_answer_amount_value_is_float():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer(678.45, ['expenses', 'reskostnad', 'amount']),
    ))

    assert zeep_dict == {
        'EXPENSES': {
            'EXPENSE': [
                {
                    'TYPE': 'reskostnad',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Reskostnad',
                    'AMOUNT': 678.45,
                }
            ],
        }
    }


def test_answer_amount_value_is_int():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer(1234, ['expenses', 'boende', 'amount'])
    ))

    assert zeep_dict == {
        'EXPENSES': {
            'EXPENSE': [
                {
                    'TYPE': 'boende',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Hyra',
                    'AMOUNT': 1234,
                }
            ],
        }
    }


def test_answer_amount_value_is_string():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer('1234', ['expenses', 'boende', 'amount']),
    ))

    assert zeep_dict == {
        'EXPENSES': {
            'EXPENSE': [
                {
                    'TYPE': 'boende',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Hyra',
                    'AMOUNT': 1234,
                },
            ],
        },
    }


def test_answer_amount_value_is_empty():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer('', ['expenses', 'annat', 'amount']),
    ))

    assert zeep_dict == {}


def test_answer_description_value_happy_path():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer('Stångkorv', ['expenses', 'annat', 'description']),
        answer(900.12, ['expenses', 'annat', 'amount']),
    ))

    assert zeep_dict == {
        'EXPENSES': {
            'EXPENSE': [
                {
                    'TYPE': 'annat',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Stångkorv 900.12',
                    'AMOUNT': 900.12,
                },
            ],
        },
    }


def test_answer_description_value_is_empty():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer('', ['expenses', 'annat', 'description']),
        answer(900, ['expenses', 'annat', 'amount']),
    ))

    assert zeep_dict == {
        'EXPENSES': {
            'EXPENSE': [
                {
                    'TYPE': 'annat',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': '900.0',
                    'AMOUNT': 900.0,
                },
            ],
        },
    }


def test_answer_description_value_default_happy_path():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer(700, ['expenses', 'annat', 'amount']),
    ))

    assert zeep_dict == {
        'EXPENSES': {
            'EXPENSE': [
                {
                    'TYPE': 'annat',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Övrig utgift',
                    'AMOUNT': 700.0,
                },
            ],
        },
    }
