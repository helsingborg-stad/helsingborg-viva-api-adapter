import pytest
from .viva_persons_to_applicants_mapper import VivaPersonsToApplicantsMapper


def test_happy_path():
    applicant = {
        "pnumber": "19860307-2391",
        "fname": "Jesper",
        "lname": "Jeppsson"
    }

    coapplicant = {
        "pnumber": "19860307-2383",
        "fname": "Sara",
        "lname": "Jeppsson",
        "type": "partner",
        "startdate": "2021-03-26T14:45:13+01:00",
        "enddate": None
    }
    mapper = VivaPersonsToApplicantsMapper(applicant, coapplicant)
    applicants = mapper.get_applicants()
    assert applicants == [
        {
            "role": "applicant",
            "personalnumber": "19860307-2391"
        },
        {
            "role": "coapplicant",
            "personalnumber": "19860307-2383"
        }
    ]


def test_no_coapplicant():
    applicant = {
        "pnumber": "19860307-2391",
        "fname": "Jesper",
        "lname": "Jeppsson"
    }
    mapper = VivaPersonsToApplicantsMapper(applicant, None)
    applicants = mapper.get_applicants()
    assert applicants == [
        {
            "role": "applicant",
            "personalnumber": "19860307-2391"
        }
    ]


def test_no_applicant():
    coapplicant = {
        "pnumber": "19860307-2383",
        "fname": "Sara",
        "lname": "Jeppsson",
        "type": "partner",
        "startdate": "2021-03-26T14:45:13+01:00",
        "enddate": None
    }
    mapper = VivaPersonsToApplicantsMapper(None, coapplicant)
    applicants = mapper.get_applicants()
    assert applicants == [
        {
            "role": "coapplicant",
            "personalnumber": "19860307-2383"
        }
    ]
    return
