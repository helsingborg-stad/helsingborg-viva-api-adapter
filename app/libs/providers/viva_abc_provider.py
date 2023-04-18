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

    def get_status(self, id: str) -> List[EkbStatus]:
        viva_application_status = VivaApplicationStatus(
            personal_number=id, client=self.create_client(wsdl_name='VivaApplication'))

        return viva_application_status.get()

    def get_mypages(self, id: str) -> EkbMyPages:
        return VivaMyPages(
            client=self.create_client(wsdl_name='MyPages'), user=id).person  # type: ignore

    def get_user(self, id: str) -> EkbUser:
        return EkbUser(
            personalNumber=id,
            firstName='Petronella',
            lastName='Malteskog',
            cases=[],
            persons=[]
        )
