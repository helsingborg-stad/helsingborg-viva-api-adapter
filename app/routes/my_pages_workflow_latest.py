from flask_restful import Resource

from ..libs import VivaMyPages

from ..libs import hash_to_personal_number
from ..libs import authenticate


class MyPagesWorkflowLatest(Resource):
    method_decorators = [authenticate]

    def get(self, hash_id):
        personal_number = hash_to_personal_number(hash_id=hash_id)
        my_pages = VivaMyPages(user=personal_number)
        latest_workflow = my_pages.get_latest_workflow()

        response = {
            'type': 'getWorkflowLatest',
            'attributes': {
                **latest_workflow,
            }
        }

        return response, 200
