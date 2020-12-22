from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import MyPages as VivaMyPages
from ..libs import hash_to_personal_number


class MyPagesStatus(Resource):
    def get(self, hash_id, workflow_id):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)
            my_pages = VivaMyPages(user=personal_number)

            response = {
                'type': 'getWorkflowStatus',
                'attributes': {
                    'workflow_id': workflow_id,
                    **my_pages.get_workflow_status(workflow_id=workflow_id),
                }
            }

            return response, 200

        except Fault as fault:
            return {
                'message': fault.message,
                'code': fault.code
            }, fault.code
