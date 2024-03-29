from typing import List
from abc import abstractmethod

from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.data_domain.ekb_user import EkbUser
from app.libs.data_domain.ekb_status import EkbStatus
from app.libs.data_domain.ekb_mypages import EkbMyPages
from app.libs.classes.viva_application_status import VivaApplicationStatus
from app.libs.classes.viva_my_pages import VivaMyPages


class AbstractVivaProvider(EkbABCProvider):

    @abstractmethod
    def create_client(self, wsdl_name: str):
        pass

    def get_status(self, id: str) -> EkbStatus:
        viva_application_status = VivaApplicationStatus(
            client=self.create_client(wsdl_name='VivaApplication'))

        return EkbStatus(
            status=viva_application_status.get(personal_number=id))

    def get_mypages(self, id: str) -> EkbMyPages:
        viva_person = VivaMyPages(client=self.create_client(
            wsdl_name='MyPages'), user=id).person

        return EkbMyPages(
            cases=viva_person['cases'],
            application=viva_person['application'],
        )

    def get_user(self, id: str) -> EkbUser:
        viva_user = VivaMyPages(client=self.create_client(
            wsdl_name='MyPages'), user=id).user

        return EkbUser(
            personal_number=viva_user['personal_number'],
            first_name=viva_user['first_name'],
            last_name=viva_user['last_name'],
            persons=viva_user['persons'],
            cases=viva_user['cases'],
        )
