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
            raise Fault(message='workflow_id missing', code=400)

        if not self.person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']:
            raise Fault(message='no workflows found', code=404)

        workflows = self.person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']

        workflow = next(
            (item for item in workflows if item['workflowid'] == workflow_id), None)

        if not workflow:
            raise Fault(
                message=f'workflow with id: {workflow_id} not found', code=404)

        status = dict()

        if 'calculations' in workflow:
            status['calculations'] = list(workflow['calculations'].values())

        if 'decision' in workflow:
            status['decision'] = [workflow['decision']]

        if 'payments' in workflow:
            status['payments'] = list(workflow['payments'].values())

        if 'journals' in workflow:
            status['journals'] = list(workflow['journals'].values())

        return status

    def get_phone_number(self):
        if not self.person_cases['vivadata']['vivacases']:
            return False

        return self.person_cases['vivadata']['vivacases']['vivacase']['phonenumbers']['phonenumber']['number']

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
