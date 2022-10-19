from typing import List, Union
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.answer import ApplicationAnswer
from app.libs.personal_number_helper import to_viva_formatted_personal_number


class ZeepPersonInfo(dict):

    def __init__(self, application_answer_collection: ApplicationAnswerCollection,
                 person_type: str = 'client', find_by_tag: str = 'personInfo') -> None:
        super().__init__(self)
        self.application_answer_collection = application_answer_collection
        self.find_by_tag = find_by_tag
        self.person_type = person_type

    def create(self) -> Union[dict, None]:
        creater_mapping = {
            'client': self._create_applicant,
            'partner': self._create_applicant,
            'children': self._create_children,
        }

        return creater_mapping[self.person_type]() or None

    def _create_applicant(self):
        applicantAnswers: List[ApplicationAnswer] = self.application_answer_collection.filter_by_tags(
            tags=[self.find_by_tag])

        if not applicantAnswers:
            return None

        return {
            self.person_type.upper(): {
                'PNUMBER': to_viva_formatted_personal_number(self._get_value(answers=applicantAnswers, tags=['personalNumber'])),
                'FOREIGNCITIZEN': False,
                'RESIDENCEPERMITTYPE': '',
                'RESIDENCEPERMITDATE': '',
                'CIVILSTATUS': 'G',
                'ALTCIVILSTATUS': '',
                'PHONENUMBERS': {
                    'PHONENUMBER': {
                        'TYPE': 'Mobiltelefon',
                        'NUMBER': self._get_value(answers=applicantAnswers, tags=['telephone']),
                        'SMS': False
                    }
                },
                'EMAIL': {
                    'EMAIL': self._get_value(answers=applicantAnswers, tags=['email']),
                    'NOTIFY': False
                },
                'FNAME': self._get_value(answers=applicantAnswers, tags=['firstName']),
                'LNAME': self._get_value(answers=applicantAnswers, tags=['lastName']),
                'ADDRESSES': {
                    'ADDRESS': {
                        'TYPE': 'FB',
                        'CO': '',
                        'ADDRESS': self._get_value(answers=applicantAnswers, tags=['address']),
                        'ZIP': self._get_value(answers=applicantAnswers, tags=['postalCode']),
                        'CITY': self._get_value(answers=applicantAnswers, tags=['postalAddress'])
                    }
                }
            }
        }

    def _create_children(self):
        child_answers: List[ApplicationAnswer] = self.application_answer_collection.filter_by_tags(
            tags=[self.find_by_tag, 'children'])
        if not child_answers:
            return None

        child = [self._create_child(answers)
                 for answers in self._create_grouped_answers(child_answers)]

        return {
            self.person_type.upper(): {
                'CHILD': child if len(child) > 1 else child[0],
            },
        }

    def _create_grouped_answers(self, answers: List[ApplicationAnswer]) -> List[List[ApplicationAnswer]]:
        grouped_answers: List[List[ApplicationAnswer]] = []

        for answer in answers:
            group_tag: str = answer.get_tag_starting_with('group:')
            group_index = int(group_tag.split(':')[1]) if group_tag else 0

            if len(grouped_answers) <= group_index:
                grouped_answers.append([answer])
            else:
                grouped_answers[group_index].append(answer)

        return grouped_answers

    def _create_child(self, answers: List[ApplicationAnswer]) -> dict:
        return {
            'PNUMBER': to_viva_formatted_personal_number(self._get_value(answers, tags=['personalNumber'])),
            'FNAME': self._get_value(answers, tags=['firstName']),
            'LNAME': self._get_value(answers, tags=['lastName']),
            'ADDRESSES': {
                'ADDRESS': {
                    'TYPE': 'FB',
                    'CO': '',
                    'ADDRESS': self._get_value(answers, tags=['address']),
                    'ZIP': self._get_value(answers, tags=['postalCode']),
                    'CITY': self._get_value(answers, tags=['postalAddress'])
                },
            },
            'PHONENUMBERS': {
                'PHONENUMBER': {
                    'TYPE':  self._get_value(answers, tags=['phoneType']),
                    'NUMBER': self._get_value(answers, tags=['phoneNumber']),
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

    def _get_value(self, answers: List[ApplicationAnswer], tags: List[str]) -> str:
        search_tags = [*tags, self.person_type]
        answer = next(
            (answer for answer in answers if answer.has_all_tags(search_tags)), None)
        return str(answer.value) if answer else ''
