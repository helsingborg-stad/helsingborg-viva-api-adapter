from flask_restful import Resource

from ..libs import VivaMyPages

from ..libs import hash_to_personal_number
from ..libs import authenticate


class MyPagesWorkflowLatest(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        self.my_pages = VivaMyPages(user=personal_number)

        return self._get_workflow_latest()

    def _get_workflow_latest(self):
        workflow_latest = self.my_pages.get_workflow_latest()

        response = {
            'type': 'getWorkflowLatest',
            'attributes': {
                'workflowLatest': workflow_latest,
            }
        }

        return response, 200
