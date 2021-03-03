import xmltodict
from zeep.exceptions import Fault

from .viva import Viva


class VivaMyPages(Viva):

    def __init__(self, wsdl='MyPages', user=str):
        super(VivaMyPages, self).__init__()

        self._service = self._get_service(wsdl)

        self._user = user
        self._pnr = self._user

        self.person_info = self._get_person_info()
        self.person_cases = self._get_person_cases()
        self.person_booked_payments = self._get_person_booked_payments()
        self.person_caseworkflow = self._get_person_caseworkflow()
        self.person_application = self._get_person_application()

    def get_workflow(self, workflow_id=str):
        if not workflow_id:
            raise Fault(message='workflow_id is missing', code=400)

        if not self.person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']:
            raise Fault(message='No workflows found', code=404)

        workflows = self.person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']

        if not type(workflows) is list:
            workflows = [workflows]

        workflow = next(
            (item for item in workflows if item['workflowid'] == workflow_id), None)

        if not workflow:
            raise Fault(
                message=f'workflow with id: {workflow_id} not found', code=404)

        return workflow

    def get_phone_number(self):
        viva_case = self.person_cases['vivadata']['vivacases']['vivacase']

        if not viva_case:
            raise Fault(message='Viva case not found', code=404)

        if not type(viva_case['phonenumbers']) is dict:
            return ''

        return viva_case['phonenumbers']['phonenumber']['number']

    def get_personal_number(self):
        if not self.person_info['vivadata']['vivaperson']['pnumber']:
            return False

        return self.person_info['vivadata']['vivaperson']['pnumber']

    def get_period(self):
        if not self.person_application['vivadata']['vivaapplication']:
            return False

        period = self.person_application['vivadata']['vivaapplication']['period']

        return {
            key.upper(): value for key, value in period.items()
        }

    def get_casessi(self):
        if not self.person_cases['vivadata']['vivacases']:
            return False

        casessi = self.person_cases['vivadata']['vivacases']['vivacase']['casessi']

        return {
            key.upper(): value for key, value in casessi.items()
        }

    def _get_person_info(self):
        response_info = self._service.PERSONINFO(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml'
        )

        return xmltodict.parse(response_info)

    def _get_person_cases(self):
        response_cases = self._service.PERSONCASES(
            USER=self._user,
            PNR=self._pnr,
            RETURNAS='xml',
            SYSTEM=1
        )

        return xmltodict.parse(response_cases)

    def _get_person_caseworkflow(self):
        if not self.get_casessi():
            return False

        response_caseworkflow = self._service.PERSONCASEWORKFLOW(
            USER=self._user,
            PNR=self._pnr,
            SSI=self.get_casessi(),
            MAXWORKFLOWS=0,
            RETURNAS='xml'
        )

        return xmltodict.parse(response_caseworkflow)

    def _get_person_booked_payments(self):
        response_booked_payments = self._service.PERSONBOOKEDPAYMENTS(
            PUSER=self._user,
            PPNR=self._pnr,
            PSYSTEM=1,
            PRETURNAS='xml',
        )

        return xmltodict.parse(response_booked_payments)

    def _get_person_application(self):
        if not self.get_casessi():
            return False

        response_application = self._service.PERSONAPPLICATION(
            USER=self._user,
            PNR=self._pnr,
            SSI=self.get_casessi(),
            WORKFLOWID='',
            RETURNAS='xml',
        )

        return xmltodict.parse(response_application)
