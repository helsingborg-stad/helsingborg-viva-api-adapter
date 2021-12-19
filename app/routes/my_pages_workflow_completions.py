from flask_restful import Resource

from ..libs import VivaMyPages

from ..libs import hash_to_personal_number
from ..libs import authenticate


class MyPagesWorkflowCompletions(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id, workflow_id=None):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        self.my_pages = VivaMyPages(user=personal_number)

        self.workflow_id = workflow_id

        return self._get_workflow_completions()

    def _get_workflow_completions(self):

        response = {
            'type': 'getWorkflowCompletions',
            'attributes': {
                **self.my_pages.get_workflow_completions(workflow_id=self.workflow_id),
            }
        }

        return response, 200
