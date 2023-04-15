from typing import Any
from app.libs.providers.viva_provider import AbstractVivaProvider


class TestVivaProvider(AbstractVivaProvider):
    APPLICATIONSTATUS: Any = callable
    PERSONAPPLICATION: Any = callable
    PERSONCASES: Any = callable
    PERSONINFO: Any = callable
    PERSONCASEWORKFLOW: Any = callable

    def create_client(self, wsdl_name: str):
        return self


def create_viva_xml_person_application_mock():
    return '''
    <vivadata>
        <vivacases>
            <vivacase>
                <casessi>
                    <server>abc</server>
                </casessi>
            </vivacase>
        </vivacases>
    </vivadata>'''


def create_viva_xml_person_cases_mock():
    return '''
    <vivadata>
        <vivacases>
            <vivacase>
                <casessi>
                    <personCases>abc123</personCases>
                </casessi>
            </vivacase>
        </vivacases>
    </vivadata>'''


def test_application_status_new_application_allowed():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 1

    result = viva_provider.get_status('198602102389')
    assert result.status == [{
        'code': 1,
        'description': 'Application allowed',
    }]


def test_application_status_user_not_found():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: -1

    result = viva_provider.get_status('198602102389')
    assert result.status == [{
        'code': -1,
        'description': 'Error (for example that the person is not in the personal register)',
    }]


def test_application_status_recurring_application_allowed():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 897

    result = viva_provider.get_status('198602102389')

    assert result.status == [
        {
            'code': 1,
            'description': 'Application allowed'
        },
        {
            'code': 128,
            'description': 'Case available (income support)'
        },
        {
            'code': 256,
            'description': 'Case is activated on the web. Is displayed on My Pages'
        },
        {
            'code': 512,
            'description': 'The case allows e-application. Is possible to create a continued application'
        }
    ]


def test_application_status_recurring_application_completions():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 832

    result = viva_provider.get_status('198602102389')

    assert result.status == [
        {
            'code': 64,
            'description': 'Completion requested'
        },
        {
            'code': 256,
            'description': 'Case is activated on the web. Is displayed on My Pages'
        },
        {
            'code': 512,
            'description': 'The case allows e-application. Is possible to create a continued application'
        }
    ]


# VIVA
def test_viva_mypages():

    viva_provider = TestVivaProvider()
    viva_provider.PERSONAPPLICATION = lambda USER, PNR, SSI, WORKFLOWID, RETURNAS: create_viva_xml_person_application_mock()
    viva_provider.PERSONCASES = lambda USER, PNR, SYSTEM, RETURNAS: create_viva_xml_person_cases_mock()

    assert viva_provider.get_mypages(id='123') == {
        'application': {
            'vivadata': {
                'vivacases': {
                    'vivacase': {
                        'casessi': {
                            'server': 'abc',
                        },
                    },
                },
            },
        },
        'cases': {
            'vivadata': {
                'vivacases': {
                    'vivacase': {
                        'casessi': {
                            'personCases': 'abc123',
                        },
                    },
                },
            },
        },
    }
