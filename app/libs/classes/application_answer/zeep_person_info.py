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
        creater_mapping = {
            'client': self._create_applicant,
            'partner': self._create_applicant,
            'children': self._create_children,
        }

        return creater_mapping[self.person_type]()

    def _create_applicant(self):
        answer = self._get_first_matching_answer_by_tags(tags=[
            self.find_by_tag])

        if not answer:
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

    def _create_children(self):
        answers_with_children = self.application_answer_collection.filter_by_tags(
            tags=[self.find_by_tag, 'children'])
        if not answers_with_children:
            return None

        for answer in answers_with_children:
            group = answer.get_tag_starting_with(value='group:')

            if not group in self:
                pass

        child = {
            'PNUMBER': self._get_value(tags=['personalNumber']),
            'FNAME': self._get_value(tags=['firstName']),
            'LNAME': self._get_value(tags=['lastName']),
            'ADDRESSES': {
                'ADDRESS': {
                    'TYPE': 'FB',
                    'CO': '',
                    'ADDRESS': self._get_value(tags=['address']),
                    'ZIP': self._get_value(tags=['postalCode']),
                    'CITY': self._get_value(tags=['postalAddress'])
                },
            },
            'PHONENUMBERS': {
                'PHONENUMBER': {
                    'TYPE':  self._get_value(tags=['phoneType']),
                    'NUMBER': self._get_value(tags=['phoneNumber']),
                    'SMS': False
                },
            },
            'EMAIL': {
                'EMAIL': '',
                'NOTIFY': False
            },
            'FOREIGNCITIZEN': False,
            'RESIDENCEPERMITTYPE': '',
            'RESIDENCEPERMITDATE': '',
            'CIVILSTATUS': '',
            'ALTCIVILSTATUS': '',
            'REGISTEREDATHOUSEHOLDADDRESS': '',
            'ALTERNATELYWITHPARENTS': '',
            'ISPARTTIMECHILD': '',
            'PARTTIMECHILDDAYS': '',
        }

        return {
            'CHILDREN': {
                'CHILD': '',
            },
        }

    def _get_value(self, tags: List[str]) -> str:
        search_tags = [*tags, self.person_type, self.find_by_tag]
        answer = self._get_first_matching_answer_by_tags(tags=search_tags)
        return answer.value if answer else ''
