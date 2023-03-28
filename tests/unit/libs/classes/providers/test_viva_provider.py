from typing import Any
from app.libs.providers.viva_provider import AbstractVivaProvider


class TestVivaProvider(AbstractVivaProvider):
    APPLICATIONSTATUS: Any = callable
    PERSONAPPLICATION: Any = callable
    PERSONCASES: Any = callable

    def create_client(self, wsdl_name: str):
        return self


def create_viva_xml_mock():
    return '<vivadata><vivacases><vivacase><casessi><server>abc</server></casessi></vivacase></vivacases></vivadata>'


def test_application_status_new_application():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 1

    assert viva_provider.get_status('19900102034444') == [
        {'code': 1, 'description': 'Application allowed'}]


def test_application_status_recurring_application():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 897

    result = viva_provider.get_status('19900102034444')

    assert result[0]['code'] == 1


# MY PAGES
def test_get_mypages():

    viva_provider = TestVivaProvider()
    viva_provider.PERSONAPPLICATION = lambda USER, PNR, SSI, WORKFLOWID, RETURNAS: create_viva_xml_mock()
    viva_provider.PERSONCASES = lambda USER, PNR, SYSTEM, RETURNAS: create_viva_xml_mock()

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
                            'server': 'abc',
                        },
                    },
                },
            },
        },
    }
