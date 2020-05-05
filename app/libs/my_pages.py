import xmltodict

from .viva import Viva


class MyPages(Viva):

    def __init__(self, wsdl='MyPages', user_pnr=str):
        super(MyPages, self).__init__()

        self._service = self._get_service(wsdl)

        self._user = user_pnr
        self._pnr = user_pnr

        self.person_info = self.get_person_info()
        self.person_cases = self.get_person_cases()

    def get_person_info(self):
        response_info = self._service.PERSONINFO(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml'
        )

        return xmltodict.parse(response_info)

    def get_person_cases(self):
        response_cases = self._service.PERSONCASES(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml',
            SYSTEM=1
        )

        return xmltodict.parse(response_cases)
