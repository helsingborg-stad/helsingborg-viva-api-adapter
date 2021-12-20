from flask_restful import Resource

from ..libs import VivaMyPages

from ..libs import VivaWorkflowCompletionsMapper
from ..libs import hash_to_personal_number
from ..libs import authenticate


class MyPagesWorkflowCompletions(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id, workflow_id=None):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        my_pages = VivaMyPages(user=personal_number)

        workflow = my_pages.get_workflow(workflow_id=workflow_id)

        completion_mapper = VivaWorkflowCompletionsMapper(
            viva_workflow=workflow)

        completion_list = completion_mapper.get_completion_list()

        response = {
            'type': 'getWorkflowCompletions',
            'attributes': {
                'requested': completion_list,
                'isRandomCheck': completion_mapper.is_random_check(),
                'completed': not completion_list,
            }
        }

        return response, 200
