from tests.conftest import TestVivaProvider
from app.libs.data_domain.ekb_user import EkbUser
from app.libs.data_domain.ekb_mypages import EkbMyPages


def create_viva_xml_mock() -> str:
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


def create_viva_xml_alt_mock() -> str:
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


def create_viva_xml_person_application_mock(mock_data: dict) -> str:
    return f'''
    <vivadata>
        <vivaapplication>
            <period>
                <start>{mock_data['start']}</start>
                <end>{mock_data['end']}</end>
            </period>
            <rawdata></rawdata>
        </vivaapplication>
    </vivadata>'''


def create_viva_xml_person_cases_mock(mock_data: dict) -> str:
    return f'''
    <vivadata>
        <vivacases>
            <vivacase>
                <casessi>
                    <server></server>
                    <path></path>
                    <id></id>
                </casessi>
                <client>
                    <pnumber>{mock_data['personal_number']}</pnumber>
                    <fname>{mock_data['first_name']}</fname>
                    <lname>{mock_data['last_name']}</lname>
                </client>
                <persons></persons>
            </vivacase>
        </vivacases>
    </vivadata>'''


def create_viva_xml_person_case_workflow() -> str:
    return '''
    <vivadata>
        <vivacaseworkflows>
            <workflow>
                <workflowid>65BF6A21294B682CC125897B003604A8</workflowid>
                <application>
                    <receiveddate>2023-02-21T16:20:42+01:00</receiveddate>
                    <periodstartdate>2023-03-01</periodstartdate>
                    <periodenddate>2023-03-31</periodenddate>
                    <otherperiod></otherperiod>
                    <requestingcompletion></requestingcompletion>
                    <completiondate></completiondate>
                    <completionreceiveddate></completionreceiveddate>
                    <completionsreceived></completionsreceived>
                    <completionsuploaded></completionsuploaded>
                    <completions></completions>
                    <completiondescription></completiondescription>
                    <completionduedate></completionduedate>
                    <islockedwithoutcompletionreceived></islockedwithoutcompletionreceived>
                    <islocked>2023-02-23T10:54:20+01:00</islocked>
                </application>
            </workflow>
        </vivacaseworkflows>
    </vivadata>'''


def test_application_status_new_application_allowed():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 1

    result = viva_provider.get_status('198602102389')
    assert result == [{
        'code': 1,
        'description': 'Application allowed',
    }]


def test_application_status_user_not_found():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: -1

    result = viva_provider.get_status('198602102389')
    assert result == [{
        'code': -1,
        'description': 'Error (for example that the person is not in the personal register)',
    }]


def test_application_status_recurring_application_allowed():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 897

    result = viva_provider.get_status('198602102389')

    assert result == [
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

    assert result == [
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
def test_viva_provider_get_mypages():

    viva_provider = TestVivaProvider()
    viva_provider.PERSONAPPLICATION = lambda USER, PNR, SSI, WORKFLOWID, RETURNAS: create_viva_xml_alt_mock()
    viva_provider.PERSONCASES = lambda USER, PNR, SYSTEM, RETURNAS: create_viva_xml_mock()

    assert viva_provider.get_mypages(id='123') == EkbMyPages(**{
        'application': {
            'vivacases': {
                'vivacase': {
                    'casessi': {
                        'server': 'abc',
                    },
                },
            },
        },
        'cases': {
            'vivacases': {
                'vivacase': {
                    'casessi': {
                        'personCases': 'abc123',
                    },
                },
            },
        },
    })


def test_viva_provider_get_user():
    personal_number = '198602102389'
    first_name = 'Petronella'
    last_name = 'Malteskog'

    viva_provider = TestVivaProvider()
    viva_provider.PERSONAPPLICATION = lambda USER, PNR, SSI, WORKFLOWID, RETURNAS: create_viva_xml_person_application_mock(
        mock_data={
            'start': '2023-04-01',
            'end': '2023-04-30',
        })
    viva_provider.PERSONCASEWORKFLOW = lambda USER, PNR, SSI, MAXWORKFLOWS, RETURNAS: create_viva_xml_person_case_workflow()
    viva_provider.PERSONCASES = lambda USER, PNR, SYSTEM, RETURNAS: create_viva_xml_person_cases_mock(
        mock_data={
            'personal_number': personal_number,
            'first_name': first_name,
            'last_name': last_name,
        })

    assert viva_provider.get_user(id=personal_number) == EkbUser(**{
        'personal_number': personal_number,
        'first_name': first_name,
        'last_name': last_name,
        'cases': {
            'workflowid': '65BF6A21294B682CC125897B003604A8',
            'application': {
                'receiveddate': '2023-02-21T16:20:42+01:00',
                'periodstartdate': '2023-03-01',
                'periodenddate': '2023-03-31',
                'otherperiod': None,
                'requestingcompletion': None,
                'completiondate': None,
                'completionreceiveddate': None,
                'completionsreceived': None,
                'completionsuploaded': None,
                'completions': None,
                'completiondescription': None,
                'completionduedate': None,
                'islockedwithoutcompletionreceived': None,
                'islocked': '2023-02-23T10:54:20+01:00',
            },
        },
        'persons': [],
    })
