from app.libs.classes.application_answer.answer import ApplicationAnswer
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.zeep import ZeepApplication


def answer_collection(*args):
    return ApplicationAnswerCollection(*args)


def answer(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


# _get_posts

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


# _get_post

def test_get_post_happy_path():
    zeep_dict = ZeepApplication(
        application_answer_collection=answer_collection())

    post_type = zeep_dict._get_post(post_type='annan', post_type_attributes={})

    assert post_type == {
        'TYPE': 'annan',
        'FREQUENCY': 12,
        'DATE': '',
        'PERIOD': '',
        'APPLIESTO': 'applicant',
        'DESCRIPTION': 'Övrig inkomst',
    }


# _get_post_type_collection

def test_get_post_type_collection_happy_path():
    zeep_dict = ZeepApplication(
        application_answer_collection=answer_collection())

    post_type_collection = zeep_dict._get_post_type_collection(
        post_type='bostad', post_answers=[])

    assert post_type_collection == {}


#  _get_post_type_answers

def test_get_post_type_answers_happy_path():
    answer_item = answer(6745, ['expenses', 'bostad', 'amount'])
    zeep_dict = ZeepApplication(
        application_answer_collection=answer_collection(answer_item))

    posts = zeep_dict._get_post_type_answers(
        post_name='bostad', post_group_name='EXPENSES')

    assert posts == [answer_item]


def test_get_post_type_answers_empty_args():
    zeep_dict = ZeepApplication(
        application_answer_collection=answer_collection())

    posts = zeep_dict._get_post_type_answers(post_name='', post_group_name='')

    assert posts == []


# ZeepApplication

def test_happy_path():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer(678.45, ['expenses', 'reskostnad', 'amount']),
        answer('100', ['expenses', 'annat', 'amount']),

        # Should be ignored
        answer('', ['expenses', 'reskostnad',
               'amount', 'group:reskostnadapplicant']),

        answer('Swish', ['incomes', 'annan', 'description',
               'swish', 'group:swishapplicant']),
        answer('1000', ['incomes', 'annan', 'amount',
               'swish', 'group:swishapplicant']),

        answer('Swish', ['incomes', 'annan', 'description',
               'swish', 'group:swishcoapplicant']),
        answer('COAPPLICANT', ['incomes', 'annan', 'appliesto',
               'swish', 'group:swishcoapplicant']),
        answer('200', ['incomes', 'annan', 'amount',
               'swish', 'group:swishcoapplicant']),
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
                },
                {
                    'TYPE': 'annat',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Övrig utgift',
                    'AMOUNT': 100.0,
                },
            ],
        },
        'INCOMES': {
            'INCOME': [
                {
                    'TYPE': 'annan',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Swish',
                    'AMOUNT': 1000.0,
                },
                {
                    'TYPE': 'annan',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'coapplicant',
                    'DESCRIPTION': 'Swish',
                    'AMOUNT': 200.0,
                },
            ],
        },
    }


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
        answer('1234,20', ['expenses', 'bredband', 'amount']),
        answer('765.34', ['incomes', 'underhallsbidrag', 'amount']),
        answer('bad text2000 bad text', [
               'incomes', 'aldreforsorjningsstod', 'amount']),
        answer('bad text123,12', ['incomes', 'lon', 'amount']),
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
                {
                    'TYPE': 'bredband',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Bredband',
                    'AMOUNT': 1234.2,
                },
            ],
        },
        'INCOMES': {
            'INCOME': [
                {
                    'TYPE': 'lon',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Lön',
                    'AMOUNT': 123.12,
                },
                {
                    'TYPE': 'aldreforsorjningsstod',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Äldreförsörjningsstöd',
                    'AMOUNT': 2000,
                },
                {
                    'TYPE': 'underhallsbidrag',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Underhållsstöd',
                    'AMOUNT': 765.34,
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
                    'DESCRIPTION': 'Stångkorv',
                    'AMOUNT': 900.12,
                },
            ],
        },
    }


def test_answer_description_value_is_empty():
    zeep_dict = ZeepApplication(application_answer_collection=answer_collection(
        answer('', ['expenses', 'annat', 'description']),
        answer(900, ['expenses', 'annat', 'amount']),
        answer('', ['incomes', 'annan', 'description', 'group:0']),
        answer('1900', ['incomes', 'annan', 'amount', 'group:0']),
        answer('Sålt smöret', ['incomes', 'annan', 'description', 'group:1']),
        answer('2900', ['incomes', 'annan', 'amount', 'group:1']),
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
                    'AMOUNT': 900.0,
                },
            ],
        },
        'INCOMES': {
            'INCOME': [
                {
                    'TYPE': 'annan',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Övrig inkomst',
                    'AMOUNT': 1900.0,
                },
                {
                    'TYPE': 'annan',
                    'FREQUENCY': 12,
                    'DATE': '',
                    'PERIOD': '',
                    'APPLIESTO': 'applicant',
                    'DESCRIPTION': 'Sålt smöret',
                    'AMOUNT': 2900.0,
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
