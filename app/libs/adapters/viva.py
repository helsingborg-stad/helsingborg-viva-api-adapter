from app.libs.classes.viva_application_status import VivaApplicationStatus
from app.libs.data_domain.ekb_provider import EkbProvider
from app.libs.data_domain.ekb_status import EkbStatus
from app.libs.data_domain.ekb_mypages import EkbMyPages
from app.libs.classes.viva_my_pages import VivaMyPages


class VivaAdapter(EkbProvider):

    def get_status(self, personal_number: str) -> EkbStatus:
        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)
        return EkbStatus(viva_application_status.get())

    def get_mypages(self, personal_number: str) -> EkbMyPages:
        person: EkbMyPages = VivaMyPages(
            user=personal_number).person  # type: ignore
        return person
