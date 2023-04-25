from flask_restful import Resource

from app.libs.providers.viva_abc_provider import AbstractVivaProvider
from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.classes.mappers.viva_workflow_completions_mapper import VivaWorkflowCompletionsMapper
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


class MyPagesWorkflowCompletions(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: AbstractVivaProvider) -> None:
        self.provider = provider

    def get(self, hash_id, workflow_id=None):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        my_pages = VivaMyPages(
            client=self.provider.create_client(wsdl_name='MyPages'), user=personal_number)

        workflow = my_pages.get_workflow(workflow_id=workflow_id)

        completions_mapper = VivaWorkflowCompletionsMapper(
            viva_workflow=workflow)

        completion_list = completions_mapper.get_completion_list()

        response = {
            'type': 'workflow',
            'attributes': {
                'completions': {
                    'requested': completion_list,
                    'description': completions_mapper.description,
                    'receivedDate': completions_mapper.received_date,
                    'dueDate': completions_mapper.due_date,
                    'attachmentUploaded': completions_mapper.get_completion_uploaded(),
                    'isCompleted': not completion_list,
                    'isRandomCheck': completions_mapper.is_random_check,
                    'isAttachmentPending': completions_mapper.is_attachment_pending,
                    'isDueDateExpired': completions_mapper.is_due_date_expired,
                },
            }
        }

        return response, 200
