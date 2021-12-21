import xmltodict
from zeep.exceptions import Fault

from .viva import Viva


class VivaMyPages(Viva):

    def __init__(self, wsdl='MyPages', user=str):
        super(VivaMyPages, self).__init__()

        self._service = self._get_service(wsdl)

        self._user = user
        self._pnr = self._user

        self.person_cases = self._get_person_cases()
        self.person_application = self._get_person_application()

    def get_case_client(self):
        return self.person_cases['vivadata']['vivacases']['vivacase']['client']

    def get_case_persons(self):
        viva_persons = self.person_cases['vivadata']['vivacases']['vivacase']['persons']

        if not viva_persons:
            return []

        if isinstance(viva_persons['person'], dict):
            return [viva_persons['person']]

        return viva_persons['person']

    def get_case_person_on_type(self, type):
        person_list = self.get_case_persons()
        person = next(
            (person for person in person_list if person['type'] is type), None)

        if not person:
            raise Fault(
                message=f'No person found with specified type: {type}', code=404)

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
            raise Fault(
                message=f'workflow with id: {workflow_id} not found', code=404)

        return workflow

    def get_workflow_list(self):
        try:
            person_caseworkflow = self._get_person_caseworkflow(limit=6)
            return person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']
        except KeyError:
            raise Fault(message='No workflows found', code=404)

    def get_latest_workflow(self):
        try:
            person_caseworkflow = self._get_person_caseworkflow(limit=1)
            return person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']
        except KeyError:
            raise Fault(message='Workflow not found', code=404)

    def get_personal_number(self):
        person_case = self.person_cases['vivadata']['vivacases']['vivacase']

        if not person_case['client']:
            raise Fault(message='Not found', code=404)

        return person_case['client']['pnumber']

    def get_period(self):
        person_applicaton = self._get_person_application()

        if not person_applicaton['vivadata']['vivaapplication']:
            return False

        period = person_applicaton['vivadata']['vivaapplication']['period']

        return {
            key.upper(): value for key, value in period.items()
        }

    def get_casessi(self):
        if not self.person_cases['vivadata']['vivacases']:
            raise Fault(message='Person cases not found', code=404)

        casessi = self.person_cases['vivadata']['vivacases']['vivacase']['casessi']

        return {
            key.upper(): value for key, value in casessi.items()
        }

    def _get_person_info(self):
        response_info = self._service.PERSONINFO(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml',
        )

        return xmltodict.parse(response_info)

    def _get_person_cases(self):
        service_response = self._service.PERSONCASES(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml',
            SYSTEM=1
        )

        person_cases = xmltodict.parse(service_response)

        person_cases_status = int(person_cases['vivadata']['status'])
        if not person_cases_status == 1:
            raise Fault(
                message=f'PERSONCASES STATUS: {person_cases_status}', code=500)

        return person_cases

    def _get_person_caseworkflow(self, limit=None):
        assert isinstance(
            limit, int), f'{limit} should be type int. Got {type(limit)}'

        response_caseworkflow = self._service.PERSONCASEWORKFLOW(
            USER=self._user,
            PNR=self._pnr,
            SSI=self.get_casessi(),
            MAXWORKFLOWS=int(limit),
            RETURNAS='xml'
        )

        return xmltodict.parse(response_caseworkflow)

    def _get_person_application(self):
        response_application = self._service.PERSONAPPLICATION(
            USER=self._user,
            PNR=self._pnr,
            SSI=self.get_casessi(),
            WORKFLOWID='',
            RETURNAS='xml',
        )

        return xmltodict.parse(response_application)
