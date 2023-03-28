from abc import abstractmethod
from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.data_domain.ekb_status import EkbStatus
from app.libs.data_domain.ekb_mypages import EkbMyPages
from app.libs.classes.viva_application_status import VivaApplicationStatus
from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.classes.viva import Viva


class AbstractVivaProvider(EkbABCProvider):

    @abstractmethod
    def create_client(self):
        pass

    def get_status(self, id: str) -> EkbStatus:
        viva_application_status = VivaApplicationStatus(
            personal_number=id, client=self.create_client())

        status: EkbStatus = viva_application_status.get()  # type: ignore

        return status

    def get_mypages(self, id: str) -> EkbMyPages:
        person: EkbMyPages = VivaMyPages(user=id).person  # type: ignore

        return person


class VivaProvider(AbstractVivaProvider):

    def create_client(self):
        viva = Viva()
        return viva._get_service(wsdl_name='VivaApplication')
