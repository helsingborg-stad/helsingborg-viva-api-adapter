from flask_restful import Resource

from app.libs.providers.viva_abc_provider import AbstractVivaProvider
from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.personal_number_helper import hash_to_personal_number
from app.libs.authenticate_helper import authenticate


class MyPagesWorkflowLatest(Resource):
    method_decorators = [authenticate]

    def __init__(self, provider: AbstractVivaProvider) -> None:
        self.provider = provider

    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        my_pages = VivaMyPages(client=self.provider.create_client(
            wsdl_name='MyPages'), user=personal_number)
        latest_workflow = my_pages.get_latest_workflow()

        response = {
            'type': 'workflow',
            'attributes': {
                'latestWorkflow': latest_workflow,
            }
        }

        return response, 200
