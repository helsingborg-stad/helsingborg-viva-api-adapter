from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaMyPages
from ..libs import hash_to_personal_number


class MyPagesWorkflows(Resource):
    def get(self, hash_id, workflow_id=None):
        if not workflow_id:
            return self._get_workflows_list(hash_id=hash_id)

        return self._get_workflows_details(hash_id=hash_id, workflow_id=workflow_id)

    def _get_workflows_list(self, hash_id):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)
            my_pages = VivaMyPages(user=personal_number)

            if my_pages.person_caseworkflow:
                workflows = my_pages.person_caseworkflow['vivadata']['vivacaseworkflows']['workflow']
            else:
                workflows = []

            response = {
                'type': 'getWorkflows',
                'attributes': {
                    'workflows': workflows,
                }
            }

            return response, 200

        except Fault as fault:
            return self._fault_response(fault=fault)

    def _get_workflows_details(self, hash_id, workflow_id):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)
            my_pages = VivaMyPages(user=personal_number)

            response = {
                'type': 'getWorkflowDetials',
                'attributes': {
                    'workflow_id': workflow_id,
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
