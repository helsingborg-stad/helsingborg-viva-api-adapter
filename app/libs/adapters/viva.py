from app.libs.classes.viva_application_status import VivaApplicationStatus
from app.libs.data_domain.ekb_status import EkbStatus
from app.libs.data_domain.ekb_mypages import EkbMyPages
from app.libs.classes.viva_my_pages import VivaMyPages


class VivaAdapter():

    def get_status(self, personal_number: str) -> EkbStatus:

        viva_application_status = VivaApplicationStatus(
            personal_number=personal_number)
        return EkbStatus(viva_application_status.get())

    def get_mypages(self, personal_number: str) -> EkbMyPages:
        my_pages = VivaMyPages(user=personal_number)

        x = EkbMyPages()
        x.cases = my_pages.person_cases['vivadata']
        x.application = my_pages.person_application['vivadata']
        return x.
