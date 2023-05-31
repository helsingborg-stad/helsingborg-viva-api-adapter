from app.libs.data_domain.api_user import ApiCase, ApiCompletion, ApiPerson, ApiUser, DateSpan
from app.libs.data_domain.ekb_case import EkbCase
from app.libs.data_domain.ekb_user import EkbPerson, EkbUser


class EkbUserToApiUserMapper():
    ekbUser: EkbUser

    def __init__(self, ekbUser: EkbUser) -> None:
        self.ekbUser = ekbUser
        pass

    def map_ekb_person_to_api_person(self, ekbPerson: EkbPerson) -> ApiPerson:
        return ApiPerson(
            firstName=ekbPerson.first_name,
            lastName=ekbPerson.last_name,
            personalNumber=ekbPerson.personal_number,
            type=ekbPerson.role
        )

    def map_ekb_case_to_api_case(self, ekbUser: EkbUser, ekbCase: EkbCase) -> ApiCase:
        return ApiCase(
            period=DateSpan(
                startDate=ekbCase.time_span.start if ekbCase.time_span.start is not None else '',
                endDate=ekbCase.time_span.end if ekbCase.time_span.end is not None else ''
            ),
            calculations=[],
            completion=ApiCompletion(
                items=[],
                description='',
                receivedDate='',
                dueDate='',
                uploadedDocuments=[],
                isCompleted=False,
                isRandomCheck=False,
                isAttachmentPending=False,
                isDueDateExpired=False,
            ),
            decisions=[],
            relatedPersons=[self.map_ekb_person_to_api_person(
                person) for person in ekbUser.persons],
            journalNotes=[],
            payments=[],
            recievedISOTime=ekbCase.received_date if ekbCase.received_date else ''
        )

    def get_api_user(self) -> ApiUser:
        mappedCases = [self.map_ekb_case_to_api_case(
            self.ekbUser, case) for case in self.ekbUser.cases]

        id = self.ekbUser.cases[0].id if len(self.ekbUser.cases) > 0 else ''

        return ApiUser(
            personalNumber=self.ekbUser.personal_number,
            firstName=self.ekbUser.first_name,
            lastName=self.ekbUser.last_name,
            cases=mappedCases,
            id=id,
            relatedPersons=[]
        )
