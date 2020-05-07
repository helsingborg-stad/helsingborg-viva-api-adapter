from .viva import Viva
from .my_pages import MyPages


class VivaApplication(Viva):

    def __init__(self,
                 wsdl='VivaApplication',
                 my_pages=MyPages,
                 application_type=str,
                 application_data=dict,
                 user=str
                 ):
        super(VivaApplication, self).__init__()

        self._service = self._get_service(wsdl)

        self._application_type = application_type
        self._application_data = application_data
        self._user_pnr = user

        self._application_types = {
            'new': self._new_application,
            'renew': self._new_re_application
        }

        self._my_pages = my_pages(user_pnr=self._user)

    def create(self):
        if self._validate(self._application_data) == True:
            return self._application_types[self._application_type]()

        return self._helpers.serialize_object({'error': 'Create application failed!'})

    def _new_application(self):
        response = self._service.NEWAPPLICATION(
            # Externt ID. Lagras som ID på ansökan. Kan lämnas tomt
            KEY='',

            # Aktuell användares personnummer
            USER=self._user_pnr,
            IP='127.0.0.1',

            # Ärendetyp. Lämna tomt för '01' = ekonomiskt bistånd
            CASETYPE='',

            SYSTEM=1,

            APPLICATION=self._application_data['APPLICATION']
        )

        return self._helpers.serialize_object(response)

    def _new_re_application(self, body=dict):
        my_pages = self._my_pages(user_pnr_hash=self._user_pnr)
        ssi = my_pages.person_cases['vivadata']['vivacases']['vivacase']['casessi']

        workflow_id = self._get_workflow_id()

        response = self._service.NEWREAPPLICATION(
            KEY=None,
            USER=self._user_pnr,
            IP='127.0.0.1',

            # Identifierar ärendet i Viva med servernamn, databassökväg och unikt id
            # See MyPages.PersonCases
            SSI=ssi,

            # Identifierar Ansökanperioden (Fortsatt ansökan)
            # See MyPages.PersonCases
            WORKFLOWID=workflow_id,

            # Period som ansökan avser
            PERIOD={
                'START': '2018-06-01',
                'END': '2018-06-30'
            },

            REAPPLICATION=body.REAPPLICATION,
        )

        return self._helpers.serialize_object(response)

    def _validate(self, data):
        return True

    def _get_workflow_id(self):
        return 1
