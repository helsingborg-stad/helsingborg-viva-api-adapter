from . import DataClassApplication
from . import Viva
from . import VivaMyPages
from . import VivaAttachments


from .application_answer import ApplicationAnswer, ApplicationAnswerCollection, ZeepApplication


from ..datetime_helper import milliseconds_to_date_string
from ..viva_error_helper import catch_viva_error


class VivaApplication(Viva):

    def __init__(self,
                 application: DataClassApplication,
                 my_pages: VivaMyPages = None,
                 viva_attachments: VivaAttachments = None,
                 wsdl='VivaApplication'):
        super(VivaApplication, self).__init__()

        if not isinstance(application, DataClassApplication):
            raise TypeError(
                f'{application} is not an instance of class DataClassApplication')

        if my_pages and not isinstance(my_pages, VivaMyPages):
            raise TypeError(
                f'{my_pages} is not an instance of class VivaMyPages')

        if viva_attachments and not isinstance(viva_attachments, VivaAttachments):
            raise TypeError(
                f'{viva_attachments} is not an instance of class VivaAttachments')

        self._my_pages = my_pages
        self._viva_attachments = viva_attachments
        self._service = self._get_service(wsdl)

        self._viva_soap_operation_types = {
            'basic': self._new_application,
            'recurrent': self._new_re_application,
            'completion': self._new_completion,
        }

        self._operation_type = application.operation_type
        self._workflow_id = application.workflow_id
        self._attachments = application.attachments
        self._answers = application.answers
        self._raw_data = application.raw_data
        self._raw_data_type = application.raw_data_type

    @catch_viva_error
    def submit(self):
        return self._viva_soap_operation_types[self._operation_type]()

    def _get_application(self):
        initial_application = {
            'OTHER': '',
            'RAWDATA': self._raw_data,
            'RAWDATATYPE': self._raw_data_type,
            'HOUSEHOLDINFO': ''
        }

        application = self._answers_to_zeep_dict()

        return {**initial_application, **application}

    def _save_completion_attachments(self):
        for attachment in self._attachments:
            self._viva_attachments.save(attachment=attachment)
        return True

    def _get_completion_attachments(self):
        completion_category = {
            'incomes': {
                'type': 'Inkomster',
                'name': 'Underlag på alla inkomster/tillgångar',
            },
            'expenses': {
                'type': 'Utgifter',
                'name': 'Underlag på alla sökta utgifter',
            },
            'completion': {
                'type': 'Komplettering',
                'name': 'Alla kontoutdrag för hela förra månaden och fram till idag',
            },
        }

        zeep_attachments = {'ATTACHMENTS': {'ATTACHMENT': []}}

        for attachment in self._attachments:
            name = attachment['name']
            category = attachment['category']
            completion_name = completion_category[category]['name']
            completion_type = completion_category[category]['type']

            zeep_attachments['ATTACHMENTS']['ATTACHMENT'].append({
                'ID': attachment['id'],
                'NAME': f'{name} - {completion_name}',
                'FILENAME': name,
                'TYPE': completion_type,
                'DESCRIPTION': name,
            })

        return zeep_attachments

    def _answers_to_zeep_dict(self):
        if not self._answers:
            return {}

        application_answer_collection = ApplicationAnswerCollection()
        for answer in self._answers:
            application_answer = ApplicationAnswer(
                value=answer['value'], tags=answer['field']['tags'])
            application_answer_collection.append(application_answer)

        zeep_dict = ZeepApplication(
            application_answer_collection=application_answer_collection)
        return zeep_dict

    def _new_application(self):
        response = self._service.NEWAPPLICATION(
            # Externt ID. Lagras som ID på ansökan. Kan lämnas tomt
            KEY='',

            # Aktuell användares personnummer
            USER=self._data['personal_number'],
            IP=self._data['client_ip'],

            # Ärendetyp. Lämna tomt för '01' = ekonomiskt bistånd
            CASETYPE='',

            SYSTEM=1,
            APPLICATION=self._data['application']
        )

        return self._helpers.serialize_object(response)

    def _new_re_application(self):
        personal_number = self._my_pages.get_personal_number()

        response = self._service.NEWREAPPLICATION(
            KEY='',
            USER=personal_number,
            IP='0.0.0.0',

            # Identifierar ärendet i Viva med servernamn, databassökväg och unikt id
            # See MyPages.PersonCases
            SSI=self._my_pages.get_casessi(),

            # Identifierar Ansökanperioden (Fortsatt ansökan)
            # See MyPages.PersonCases
            WORKFLOWID=self._workflow_id,

            # Period som ansökan avser
            PERIOD=self._my_pages.get_period(),

            REAPPLICATION=self._get_application(),

            # Noll eller metoder för att meddela klient/medsökande
            NOTIFYINFOS={
                'NOTIFYINFO': None
            }
        )

        return self._helpers.serialize_object(response)

    def _new_completion(self):
        self._save_completion_attachments()

        personal_number = self._my_pages.get_personal_number()
        case_ssi = self._my_pages.get_casessi()
        completion = self._get_completion_attachments()

        completion_response = self._service.NEWCOMPLETION(
            KEY='',
            USER=personal_number,
            IP='0.0.0.0',
            SSI=case_ssi,
            WORKFLOWID=self._workflow_id,
            COMPLETION=completion
        )

        return self._helpers.serialize_object(completion_response)
