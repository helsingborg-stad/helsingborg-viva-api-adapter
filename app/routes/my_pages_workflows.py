from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaMyPages
from ..libs import hash_to_personal_number


class MyPagesWorkflows(Resource):
    def get(self, hash_id, workflow_id=None):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        my_pages = VivaMyPages(user=personal_number)

        if not workflow_id:
            return self._get_workflows_list(my_pages=my_pages)

        return self._get_workflows_details(my_pages=my_pages, workflow_id=workflow_id)

    def _get_workflows_list(self, my_pages=VivaMyPages):
        try:
            if my_pages.person_caseworkflow:
                workflows = my_pages.person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']
            else:
                workflows = []

            if not type(workflows) is list:
                workflows = [workflows]

            response = {
                'type': 'getWorkflows',
                'attributes': {
                    'workflows': workflows,
                }
            }

            return response, 200

        except Fault as fault:
            return self._fault_response(fault=fault)

    def _get_workflows_details(self, my_pages=VivaMyPages, workflow_id=str):
        try:
            response = {
                'type': 'getWorkflowDetials',
                'attributes': {
                    **my_pages.get_workflow(workflow_id=workflow_id),
                }
            }

            return response, 200

        except Fault as fault:
            return self._fault_response(fault=fault)

    def _fault_response(self, fault):
        return {
            'message': fault.message,
            'code': fault.code
        }, fault.code
