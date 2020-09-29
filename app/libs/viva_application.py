from .viva import Viva
from .my_pages import MyPages


class VivaApplication(Viva):

    def __init__(self,
                 wsdl='VivaApplication',
                 my_pages=MyPages,
                 application_type=str,
                 application_data=dict,
                 personal_number=str,
                 client_ip=str,
                 workflow_id=str,
                 period=dict,
                 ):
        super(VivaApplication, self).__init__()

        self._service = self._get_service(wsdl)
        self._my_pages = my_pages

        self._application_type = application_type
        self._application_data = application_data
        self._personal_number = personal_number
        self._client_ip = client_ip
        self._workflow_id = workflow_id
        self._period = period

        self._application_types = {
            'basic': self._new_application,
            'recurrent': self._new_re_application
        }

    def create(self):
        if self._validate(self._application_data) == True:
            return self._application_types[self._application_type]()

        return self._helpers.serialize_object({'error': 'Create application failed!'})

    def _new_application(self):
        response = self._service.NEWAPPLICATION(
            # Externt ID. Lagras som ID på ansökan. Kan lämnas tomt
            KEY='',

            # Aktuell användares personnummer
            USER=self._personal_number,
            IP='127.0.0.1',

            # Ärendetyp. Lämna tomt för '01' = ekonomiskt bistånd
            CASETYPE='',

            SYSTEM=1,

            APPLICATION=self._application_data['APPLICATION']
        )

        return self._helpers.serialize_object(response)

    def _new_re_application(self):
        my_pages = self._my_pages(user=self._personal_number)

        try:
            ssi = my_pages.person_cases['vivadata']['vivacases']['vivacase']['casessi']
        except Exception:
            return self._helpers.serialize_object({'error': 'SSI not found'})

        response = self._service.NEWREAPPLICATION(
            KEY='',
            USER=self._personal_number,
            IP=self._client_ip,

            # Identifierar ärendet i Viva med servernamn, databassökväg och unikt id
            # See MyPages.PersonCases
            SSI={
                'SERVER': ssi['server'],
                'PATH': ssi['path'],
                'ID': ssi['id']
            },

            # Identifierar Ansökanperioden (Fortsatt ansökan)
            # See MyPages.PersonCases
            WORKFLOWID=ssi['id'],

            # Period som ansökan avser
            PERIOD={
                'START': self._period['start_date'],
                'END': self._period['end_date']
            },

            REAPPLICATION=self._application_data,

            # Noll eller metoder för att meddela klient/medsökande
            NOTIFYINFOS={
                'NOTIFYINFO': {
                    'ID': self._personal_number,
                    'ADDRESS': '',
                    'ADDRESSTYPE': ''
                }
            }
        )

        return self._helpers.serialize_object(response)

    def _validate(self, data):
        return True
