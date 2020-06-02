from .Viva import Viva
from .my_pages import MyPages


class VivaApplication(Viva):

    def __init__(self, wsdl='VivaApplication', usr=str, pnr=str, my_pages=MyPages):
        super(VivaApplication, self).__init__()
        self._service = self._get_service(wsdl)

        self.usr = usr
        self.pnr = pnr

        self._my_pages = my_pages(usr, pnr)
        self._person_cases = self._get_person_cases()
        self._ssi = self._get_ssi()
        self._workflow_id = self._get_workflow_id()

    def _get_person_cases(self):
        return self._my_pages.person_cases

    def _get_ssi(self):
        return self._person_cases['vivadata']['vivacases']['vivacase']['casessi']

    def _get_workflow_id(self):
        return self._person_cases['vivadata']

    def new_application(self, key, application, ip='127.0.0.1'):
        response_new_application = self._service.NEWAPPLICATION(
            KEY=key,        # Externt ID. Lagras som ID på ansökan. Kan lämnas tomt
            USER=user,      # Aktuell användares personnummer
            IP=ip,          # Aktuell användares IP-adress
            CASETYPE='',    # Ärendetyp. Lämna tomt för '01' = ekonomiskt bistånd
            SYSTEM=1,
            APPLICATION=application,
        )

        return self._helpers.serialize_object(response_new_application)

    def new_re_application(self, key, period, re_application, ip='127.0.0.1'):

        response_new_re_application = self._service.NEWREAPPLICATION(
            # Externt ID. Lagras som ID på ansökan. Kan lämnas tomt
            KEY=key,

            # Aktuell användares personnummer
            USER=user,

            # Aktuell användares IP-adress
            IP=ip,

            # Identifierar ärendet i Viva med servernamn, databassökväg och unikt id
            # See MyPages.PersonCases
            SSI=self._ssi,

            # Identifierar Ansökanperioden (Fortsatt ansökan)
            # See MyPages.PersonCases
            WORKFLOWID=self._workflow_id,

            # Period som ansökan avser
            PERIOD={
                'START': '2018-06-01',
                'END': '2018-06-30'
            },

            REAPPLICATION=re_application,
        )

        return self._helpers.serialize_object(response_new_re_application)
