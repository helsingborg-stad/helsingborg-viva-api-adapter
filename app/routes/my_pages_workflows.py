from flask_restful import Resource

from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


class MyPagesWorkflows(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id, workflow_id=None):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        self.my_pages = VivaMyPages(user=personal_number)

        self.workflow_id = workflow_id

        if not self.workflow_id:
            return self._get_workflow_list()

        return self._get_workflow_details()

    def _get_workflow_list(self):
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

    def _get_workflow_details(self):
        response = {
            'type': 'getWorkflowDetials',
            'attributes': {
                **self.my_pages.get_workflow(workflow_id=self.workflow_id),
            }
        }

        return response, 200
