import pytest
from .. import ApplicationAnswer
from .. import ApplicationAnswerCollection
from .. import ZeepNotification


def answer_collection(*args):
    return ApplicationAnswerCollection(*args)


def answer(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


def applicants():
    return [
        {
            'personalnumber': '19900102034444',
            'role': 'applicant'
        },
        {
            'personalnumber': '19900102035555',
            'role': 'coapplicant'
        }
    ]


def test_sms_list_happy_path():
    notification = ZeepNotification(applicants(), application_answer_collection=answer_collection(
        answer(True, ['applicant', 'nofification', 'sms']),
        answer('0708134506', ['applicant', 'phonenumber']),
        answer(True, ['coapplicant', 'nofification', 'sms']),
        answer('0708134509', ['coapplicant', 'phonenumber']),
    ))

    assert notification.get_sms_list(applicant_tags=['applicant', 'coapplicant']) == [
        {
            'ID': '19900102034444',
            'ADDRESS': '0708134506',
            'ADDRESSTYPE': 'sms',
        },
        {
            'ID': '19900102035555',
            'ADDRESS': '0708134509',
            'ADDRESSTYPE': 'sms',
        }
    ]


def test_applicant_happy_path():
    notification = ZeepNotification(applicants(), application_answer_collection=answer_collection(
        answer(True, ['applicant', 'nofification', 'sms']),
        answer('0708134506', ['applicant', 'phonenumber']),
    ))

    assert notification.get_sms('applicant') == {
        'ID': '19900102034444',
        'ADDRESS': '0708134506',
        'ADDRESSTYPE': 'sms',
    }


def test_coapplicant_happy_path():
    notification = ZeepNotification(applicants(), application_answer_collection=answer_collection(
        answer(True, ['coapplicant', 'nofification', 'sms']),
        answer('0708134509', ['coapplicant', 'phonenumber']),
    ))

    assert notification.get_sms('coapplicant') == {
        'ID': '19900102035555',
        'ADDRESS': '0708134509',
        'ADDRESSTYPE': 'sms',
    }


def test_no_applicants():
    notification = ZeepNotification([], application_answer_collection=answer_collection(
        answer(True, ['applicant', 'nofification', 'sms']),
        answer('0708134506', ['applicant', 'phonenumber']),
        answer(True, ['coapplicant', 'nofification', 'sms']),
        answer('0708134508', ['coapplicant', 'phonenumber']),
    ))
    assert notification.get_sms('applicant') is None
    assert notification.get_sms('coapplicant') is None


def test_notification_not_wanted_by_user():
    notification = ZeepNotification(applicants(), application_answer_collection=answer_collection(
        answer('', ['applicant', 'nofification', 'sms']),
        answer('0708134506', ['applicant', 'phonenumber']),
        answer('', ['coapplicant', 'nofification', 'sms']),
        answer('0708134508', ['coapplicant', 'phonenumber']),
    ))
    assert notification.get_sms('applicant') is None
    assert notification.get_sms('coapplicant') is None


def test_no_or_empty_phonenumber_submitted():
    notification = ZeepNotification(applicants(), application_answer_collection=answer_collection(
        answer(True, ['applicant', 'nofification', 'sms']),
        answer('', ['applicant', 'phonenumber']),
        answer(True, ['coapplicant', 'nofification', 'sms']),
    ))
    assert notification.get_sms('applicant') is None
    assert notification.get_sms('coapplicant') is None


def test_sms_list_applicant_only():
    notification = ZeepNotification(applicants(), application_answer_collection=answer_collection(
        answer(True, ['applicant', 'nofification', 'sms']),
        answer('0708134506', ['applicant', 'phonenumber']),
    ))

    assert notification.get_sms_list(applicant_tags=['applicant']) == [
        {
            'ID': '19900102034444',
            'ADDRESS': '0708134506',
            'ADDRESSTYPE': 'sms',
        }
    ]


def test_sms_list_coapplicant_only():
    notification = ZeepNotification(applicants(), application_answer_collection=answer_collection(
        answer(True, ['coapplicant', 'nofification', 'sms']),
        answer('0708134509', ['coapplicant', 'phonenumber']),
    ))

    assert notification.get_sms_list(applicant_tags=['coapplicant']) == [
        {
            'ID': '19900102035555',
            'ADDRESS': '0708134509',
            'ADDRESSTYPE': 'sms',
        }
    ]
