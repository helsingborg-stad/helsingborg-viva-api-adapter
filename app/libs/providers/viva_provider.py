from app.libs.providers.ekb_abc_provider import EkbABCProvider
from app.libs.data_domain.ekb_status import EkbStatus
from app.libs.data_domain.ekb_mypages import EkbMyPages
from app.libs.classes.viva_application_status import VivaApplicationStatus
from app.libs.classes.viva_my_pages import VivaMyPages


class VivaProvider(EkbABCProvider):

    def get_status(self, id: str) -> EkbStatus:
        viva_application_status = VivaApplicationStatus(
            personal_number=id)

        status: EkbStatus = viva_application_status.get()  # type: ignore

        return status

    def get_mypages(self, id: str) -> EkbMyPages:
        person: EkbMyPages = VivaMyPages(user=id).person  # type: ignore

        return person
