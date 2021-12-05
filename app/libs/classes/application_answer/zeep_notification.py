from . import ApplicationAnswerCollection
from .. import VivaMyPages

# Hämta svar som har tag = notifcation (notifcation,coapplicant)
# Personnummer för samtliga sökande
# Matcha mobilnummer med personnummer


class ZeepNotification(dict):

    ADRESS_TYPE_SMS = 'sms'
    EMPTY_NOTIFCATION = {
        'id': '',
        'adress': '',
        'adresstype': ADRESS_TYPE_SMS,
    }

    def __init__(self, my_pages: VivaMyPages, application_answer_collection: ApplicationAnswerCollection = {}):
        super().__init__(self)
        self.application_answer_collection = application_answer_collection
        self._my_pages = my_pages
        self._create()

    def _create(self):
        # [{
        #     field: {
        #         tags: ['noti', 'coapplicant']
        #     },
        #     value: '0148184184'
        # },
        #     {
        #     field: {
        #         tags: ['noti', 'applicant']
        #     },
        #     value: '0148184184'
        # }]
        # get answers with tags ['notification', 'sms']
        notification_answers = self._get_notification_answers()

        # get persons with role and personalnumber
        notification_list = self._get_notification_list(
            answers=notification_answers)

        return notification_list

    def _get_notification_list(self, answers):
        if (answers):
            for answer in answers:

                for person in persons:
                    if answer.has_tag(person.role):
                        notification_list.append({
                            id: person.personalNumber,
                            addresstype: 'sms',
                            address: answer.value
                        })

    def _get_notification_answers(self):
        tags = ['notification', 'sms']
        return self.application_answer_collection.filter_by_tags(tags=tags)

    def _get_persons(self):
        persons = self._my_pages.person_cases['vivadata']['vivacases']['vivacase']
