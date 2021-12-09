from . import ApplicationAnswerCollection
from .. import VivaMyPages

# Hämta svar som har tag = notifcation (notifcation,coapplicant)
# Personnummer för samtliga sökande
# Matcha mobilnummer med personnummer


class ZeepNotification(list):
    VIVA_ADRESS_TYPE_SMS = 'sms'

    def __init__(self, applicants: list, application_answer_collection: ApplicationAnswerCollection = {}):
        super().__init__(self)
        self.application_answer_collection = application_answer_collection
        self.applicants = applicants

    def _get_first_matching_answer_by_tags(self, tags):
        answers_by_tags = self.application_answer_collection.filter_by_tags(
            tags)
        return next(
            (answer for answer in answers_by_tags if answer.value), None)

    def _get_applicant(self, role):
        return next(
            (applicant for applicant in self.applicants if applicant["role"] == role), None)

    def get_sms(self, applicant_tag):
        notification_answer = self._get_first_matching_answer_by_tags(
            tags=["nofification", "sms", applicant_tag])
        if not notification_answer:
            return None

        phonenumber_answer = self._get_first_matching_answer_by_tags(
            tags=["phonenumber", applicant_tag])

        if not phonenumber_answer:
            return None

        applicant = self._get_applicant(role=applicant_tag)
        if not applicant:
            return None

        return {
            "id": applicant['personalnumber'],
            "adress": phonenumber_answer.value,
            "adresstype": self.VIVA_ADRESS_TYPE_SMS
        }