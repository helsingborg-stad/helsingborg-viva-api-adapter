from .. import ApplicationAnswer
from .. import ApplicationAnswerCollection
from .. import ZeepApplication


def answer_collection(*args):
    return ApplicationAnswerCollection(*args)


def answer(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


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
