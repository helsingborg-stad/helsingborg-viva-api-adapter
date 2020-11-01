from datetime import datetime

from .viva import Viva
from .my_pages import MyPages
from .helpers import date_from_milliseconds


class VivaApplication(Viva):

    def __init__(self,
                 wsdl='VivaApplication',
                 my_pages=MyPages,
                 application_type=str,
                 data=dict
                 ):
        super(VivaApplication, self).__init__()

        self._service = self._get_service(wsdl)
        self._my_pages = my_pages

        self._type = application_type
        self._data = data

        self._types = {
            'basic': self._new_application,
            'recurrent': self._new_re_application
        }

    def create(self):
        if self._validate(self._data) == True:
            return self._types[self._type]()

        return self._helpers.serialize_object({'error': 'Create application failed!'})

    def _new_application(self):
        response = self._service.NEWAPPLICATION(
            # Externt ID. Lagras som ID på ansökan. Kan lämnas tomt
            KEY='',

            # Aktuell användares personnummer
            USER=self._data['personal_number'],
            IP=self._data['client_ip'],

            # Ärendetyp. Lämna tomt för '01' = ekonomiskt bistånd
            CASETYPE='',

            SYSTEM=1,
            APPLICATION=self._data['application']
        )

        return self._helpers.serialize_object(response)

    def _new_re_application(self):
        my_pages = self._my_pages(user=self._data['personal_number'])

        try:
            ssi = my_pages.person_cases['vivadata']['vivacases']['vivacase']['casessi']
        except Exception:
            return self._helpers.serialize_object({'error': 'SSI not found'})

        start_date = date_from_milliseconds(self._data['period']['start_date'])
        end_date = date_from_milliseconds(self._data['period']['end_date'])

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
            WORKFLOWID=self._workflow_id,

            # Period som ansökan avser
            PERIOD={
                'START': start_date,
                'END': end_date
            },

            REAPPLICATION=self._data['application'],

            # Noll eller metoder för att meddela klient/medsökande
            NOTIFYINFOS={
                'NOTIFYINFO': {
                    'ID': self._data['personal_number'],
                    'ADDRESS': '',
                    'ADDRESSTYPE': ''
                }
            }
        )

        return self._helpers.serialize_object(response)

    def _validate(self, data):
        return True
