import xmltodict
from typing import Any
from werkzeug.exceptions import NotFound

from app.cache import cache


class VivaMyPages:
    def __init__(self, client: Any, user: str) -> None:
        self._client = client

        self._user = user
        self._pnr = self._user

        self.person_cases = self._get_person_cases()
        self.person_application = self._get_person_application()

    @property
    def person(self) -> dict:
        return {
            'cases': self.person_cases['vivadata'] if self.person_cases['vivadata'] else None,
            'application': self.person_application['vivadata'] if self.person_application['vivadata'] else None,
        }

    @property
    def user(self) -> dict:
        client = self.get_case_client()
        persons = self.get_case_persons() if self.get_case_persons() else []
        cases = self.get_workflow_list() if self.get_workflow_list() else []

        return {
            'personal_number': client['pnumber'] if client['pnumber'] else None,
            'first_name': client['fname'] if client['fname'] else None,
            'last_name': client['lname'] if client['lname'] else None,
            'persons': persons,
            'cases': cases,
        }

    def get_case_client(self):
        return self.person_cases['vivadata']['vivacases']['vivacase']['client']

    def get_case_persons(self):
        viva_persons = self.person_cases['vivadata']['vivacases']['vivacase']['persons']

        if not viva_persons:
            return []

        if isinstance(viva_persons['person'], dict):
            return [viva_persons['person']]

        return viva_persons['person']

    def get_case_person_on_type(self, viva_person_type):
        person_list = self.get_case_persons()
        person = next(
            (person for person in person_list if person['type'] == viva_person_type), None)

        return person

    def get_workflow(self, workflow_id=None):
        assert isinstance(
            workflow_id, str), f'workflow_id should be type str. Got {type(workflow_id)}'

        workflow_list = self.get_workflow_list()

        if not isinstance(workflow_list, list):
            workflow_list = [workflow_list]

        workflow = next(
            (item for item in workflow_list if item['workflowid'] == workflow_id), None)

        if not workflow:
            raise NotFound(
                description=f'workflow with id: {workflow_id} not found')

        return workflow

    def get_workflow_list(self):
        person_caseworkflow = self._get_person_caseworkflow(limit=6)
        workflows = person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']
        return workflows if workflows else []

    def get_latest_workflow(self):
        try:
            person_caseworkflow = self._get_person_caseworkflow(limit=1)
            return person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']
        except KeyError:
            raise NotFound(description='Workflow not found')

    def get_personal_number(self):
        person_case = self.person_cases['vivadata']['vivacases']['vivacase']

        if not person_case['client']:
            message = 'Personal number not found'
            raise NotFound(description=message)

        return person_case['client']['pnumber']

    def get_period(self):
        person_applicaton = self.person_application

        if not person_applicaton['vivadata']['vivaapplication']:
            return False

        period = person_applicaton['vivadata']['vivaapplication']['period']

        return {
            key.upper(): value for key, value in period.items()
        }

    def get_casessi(self):
        if not self.person_cases['vivadata']['vivacases']:
            message = 'Person cases not found'

            raise NotFound(description=message)

        casessi = self.person_cases['vivadata']['vivacases']['vivacase']['casessi']

        return {
            key.upper(): value for key, value in casessi.items()
        }

    def _get_person_info(self):
        """NOT IMPLEMENTED"""
        response_info = self._client.PERSONINFO(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml',
        )

        return xmltodict.parse(response_info)

    @cache.memoize(timeout=3600)  # 1 hour
    def _get_person_cases(self):
        service_response = self._client.PERSONCASES(
            USER=self._user,
            PNR=self._pnr,
            SYSTEM=1,
            RETURNAS='xml',
        )

        return xmltodict.parse(service_response)

    def _get_person_caseworkflow(self, limit=None):
        assert isinstance(
            limit, int), f'{limit} should be type int. Got {type(limit)}'

        service_response = self._client.PERSONCASEWORKFLOW(
            USER=self._user,
            PNR=self._pnr,
            SSI=self.get_casessi(),
            MAXWORKFLOWS=int(limit),
            RETURNAS='xml'
        )

        return xmltodict.parse(service_response)

    @cache.memoize(timeout=300)  # 5 minutes
    def _get_person_application(self):
        service_response = self._client.PERSONAPPLICATION(
            USER=self._user,
            PNR=self._pnr,
            SSI=self.get_casessi(),
            WORKFLOWID='',
            RETURNAS='xml',
        )

        return xmltodict.parse(service_response)

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, self._user)
