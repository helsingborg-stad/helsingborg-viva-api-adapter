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
                'description': completion_mapper.description,
                'receivedDate': completion_mapper.received_date,
                'dueDate': completion_mapper.due_date,
                'attachmentUploaded': completion_mapper.get_completion_uploaded(),
                'isCompleted': not completion_list,
                'isRandomCheck': completion_mapper.is_random_check,
                'isAttachmentPending': completion_mapper.is_attachment_pending,
                'isDueDateExpired': completion_mapper.is_due_date_expired,
            }
        }

        return response, 200
