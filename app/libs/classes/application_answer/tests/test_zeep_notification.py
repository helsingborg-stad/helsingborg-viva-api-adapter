import pytest
from .. import ApplicationAnswer
from .. import ApplicationAnswerCollection
from .. import ZeepNotification


def anscoll(*args):
    return ApplicationAnswerCollection(*args)


def ans(value, tags):
    return ApplicationAnswer(value=value, tags=tags)


def assert_notification(actual, expected):
    assert expected["id"] == actual["id"]
    assert expected["adresstype"] == actual["adresstype"]
    assert expected["adress"] == actual["adress"]


def applicants():
    return [
        {
            "personalnumber": "19900102034444",
            "role": "applicant"
        },
        {
            "personalnumber": "19900102035555",
            "role": "coapplicant"
        }
    ]


def test_applicant_happy_path():
    notification = ZeepNotification(applicants(), application_answer_collection=anscoll(
        ans("yes", ["applicant", "nofification", "sms"]),
        ans("0708134506", ["applicant", "phonenumber"]),
    ))
    sms_notification = notification.get_sms("applicant")
    assert_notification(sms_notification, {
        "id": '19900102034444',
        "adresstype": 'sms',
        "adress": '0708134506'
    })


def test_coapplicant_happy_path():
    notification = ZeepNotification(applicants(), application_answer_collection=anscoll(
        ans("yes", ["coapplicant", "nofification", "sms"]),
        ans("0708134509", ["coapplicant", "phonenumber"]),
    ))
    sms_notification = notification.get_sms("coapplicant")
    assert_notification(sms_notification, {
        "id": '19900102035555',
        "adresstype": 'sms',
        "adress": '0708134509'
    })


def test_no_applicants():
    notification = ZeepNotification([], application_answer_collection=anscoll(
        ans("yes", ["applicant", "nofification", "sms"]),
        ans("0708134506", ["applicant", "phonenumber"]),
        ans("yes", ["coapplicant", "nofification", "sms"]),
        ans("0708134508", ["coapplicant", "phonenumber"]),
    ))
    assert notification.get_sms("applicant") == None
    assert notification.get_sms("coapplicant") == None


def test_notification_not_wanted_by_user():
    notification = ZeepNotification(applicants(), application_answer_collection=anscoll(
        ans("", ["applicant", "nofification", "sms"]),
        ans("0708134506", ["applicant", "phonenumber"]),
        ans("", ["coapplicant", "nofification", "sms"]),
        ans("0708134508", ["coapplicant", "phonenumber"]),
    ))
    assert notification.get_sms("applicant") == None
    assert notification.get_sms("coapplicant") == None


def test_no_or_empty_phonenumber_submitted():
    notification = ZeepNotification(applicants(), application_answer_collection=anscoll(
        ans("yes", ["applicant", "nofification", "sms"]),
        ans("", ["applicant", "phonenumber"]),
        ans("yes", ["coapplicant", "nofification", "sms"]),
    ))
    assert notification.get_sms("applicant") == None
    assert notification.get_sms("coapplicant") == None
