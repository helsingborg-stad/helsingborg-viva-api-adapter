from flask_restful import Resource
from zeep.exceptions import Fault

from ..libs import MyPages as VivaMyPages
from ..libs import hash_to_personal_number

from .. import data


class MyPagesCalculations(Resource):
    def get(self, hash_id, workflow_id):
        try:
            personal_number = hash_to_personal_number(hash_id=hash_id)
            my_pages = VivaMyPages(user=personal_number)

            response = {
                'jsonapi': {
                    'version': '1.0',
                },
                'data': {
                    'type': 'getWorkflowCalculations',
                    'attributes': {
                        'workflow_id': workflow_id,
                        'calculations': my_pages.get_workflow_calculations(workflow_id=workflow_id),
                    }
                }
            }

            return response, 200

        except Fault as fault:
            return {
                'message': fault.message,
                'code': fault.code
            }, fault.code
