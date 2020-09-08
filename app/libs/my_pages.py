import xmltodict

from .viva import Viva


class MyPages(Viva):

    def __init__(self, wsdl='MyPages', user=str):
        super(MyPages, self).__init__()

        self._service = self._get_service(wsdl)

        self._user = user
        self._pnr = self._user

        self.person_info = self._get_person_info()
        self.person_cases = self._get_person_cases()
        self.person_caseworkflow = self._get_person_caseworkflow()

    def _get_person_info(self):
        response_info = self._service.PERSONINFO(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml'
        )

        return xmltodict.parse(response_info)

    def _get_person_cases(self):
        response_cases = self._service.PERSONCASES(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml',
            SYSTEM=1
        )

        return xmltodict.parse(response_cases)

    def _get_person_caseworkflow(self):
        if not self.person_cases['vivadata']['vivacases']:
            return False

        casessi = self.person_cases['vivadata']['vivacases']['vivacase']['casessi']

        response_caseworkflow = self._service.PERSONCASEWORKFLOW(
            USER=self._user,
            PNR=self._pnr,
            SSI={
                key.upper():value for key, value in casessi.items()
            },
            MAXWORKFLOWS=0,
            RETURNAS='xml'
        )

        return xmltodict.parse(response_caseworkflow)
