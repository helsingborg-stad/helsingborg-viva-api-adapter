from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import VivaMyPages
from ..libs import hash_to_personal_number


class MyPagesWorkflows(Resource):
    def get(self, hash_id, workflow_id=None):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        self.my_pages = VivaMyPages(user=personal_number)

        self.workflow_id = workflow_id

        if not self.workflow_id:
            return self._get_workflow_list()

        return self._get_workflow_details()

    def _get_workflow_list(self):
        try:
            workflow_list = self.my_pages.get_workflow_list()

            if not type(workflow_list) is list:
                workflow_list = [workflow_list]

            response = {
                'type': 'getWorkflows',
                'attributes': {
                    'workflows': workflow_list,
                }
            }

            return response, 200

        except Fault as fault:
            return self._fault_response(fault=fault)

        except Exception as error:
            my_error = {}
            my_error['message'] = f'{error}'
            my_error['code'] = 500

            return my_error, my_error['code']

    def _get_workflow_details(self):
        try:
            response = {
                'type': 'getWorkflowDetials',
                'attributes': {
                    **self.my_pages.get_workflow(workflow_id=self.workflow_id),
                }
            }

            return response, 200

        except Fault as fault:
            return self._fault_response(fault=fault)

        except Exception as error:
            my_error = {}
            my_error['message'] = f'{error}'
            my_error['code'] = 500

            return my_error, my_error['code']

    def _fault_response(self, fault):
        return {
            'message': fault.message,
            'code': fault.code
        }, fault.code
