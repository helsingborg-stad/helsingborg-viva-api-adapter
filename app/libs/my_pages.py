import xmltodict

from .hashids import parse_hash
from .viva import Viva


class MyPages(Viva):

    def __init__(self, wsdl='MyPages', user_pnr_hashed=str):
        super(MyPages, self).__init__()

        self._service = self._get_service(wsdl)

        self._user = parse_hash(hashid=user_pnr_hashed)
        self._pnr = self._user

        self.person_info = self._get_person_info()
        self.person_cases = self._get_person_cases()

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
