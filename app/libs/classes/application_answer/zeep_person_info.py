from typing import List
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.answer import ApplicationAnswer


class ZeepPersonInfo(dict):
    def __init__(self, application_answer_collection: ApplicationAnswerCollection,
                 person_type: str = 'client', find_by_tag: str = 'personInfo') -> None:
        super().__init__(self)
        self.application_answer_collection = application_answer_collection
        self.find_by_tag = find_by_tag
        self.person_type = person_type

    def _get_first_matching_answer_by_tags(self, tags: List[str]) -> ApplicationAnswer:
        answers_by_tags = self.application_answer_collection.filter_by_tags(
            tags=tags)
        return next((answer for answer in answers_by_tags if answer.value), None)

    def create(self):
        person_info_answers = self._get_first_matching_answer_by_tags(tags=[
                                                                      self.find_by_tag])

        if not person_info_answers:
            return None

        return {
            self.person_type.upper(): {
                'PNUMBER': self._get_value(tags=['personalNumber']),
                'FOREIGNCITIZEN': False,
                'RESIDENCEPERMITTYPE': '',
                'RESIDENCEPERMITDATE': '',
                'CIVILSTATUS': 'G',
                'ALTCIVILSTATUS': '',
                'PHONENUMBERS': {
                    'PHONENUMBER': {
                        'TYPE': 'Mobiltelefon',
                        'NUMBER': self._get_value(tags=['telephone']),
                        'SMS': False
                    }
                },
                'EMAIL': {
                    'EMAIL': self._get_value(tags=['email']),
                    'NOTIFY': False
                },
                'FNAME': self._get_value(tags=['firstName']),
                'LNAME': self._get_value(tags=['lastName']),
                'ADDRESSES': {
                    'ADDRESS': {
                        'TYPE': 'FB',
                        'CO': '',
                        'ADDRESS': self._get_value(tags=['address']),
                        'ZIP': self._get_value(tags=['postalCode']),
                        'CITY': self._get_value(tags=['postalAddress'])
                    }
                }
            }
        }

    def _get_value(self, tags: List[str]) -> str:
        search_tags = [*tags, self.person_type, self.find_by_tag]
        answer = self._get_first_matching_answer_by_tags(tags=search_tags)
        return answer.value if answer else ''
