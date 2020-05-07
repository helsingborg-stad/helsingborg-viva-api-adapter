import xmltodict
import re

from .viva import Viva
from .. import data


class MyPages(Viva):

    _hashids = data.hashids

    def __init__(self, wsdl='MyPages', user_pnr_hash=str):
        super(MyPages, self).__init__()

        self._service = self._get_service(wsdl)

        self._user = MyPages._parse_hash(user_pnr_hash)
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

    @classmethod
    def _parse_hash(cls, number=int):
        decoded = str(cls._hashids.decode(number)[0])
        regex = re.compile('([0-9]{8})([0-9]{4})')
        parts = regex.match(decoded).groups()
        formated = 'T'.join(parts)
        return formated
