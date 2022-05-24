from app.libs.enum import ApplicationType

from . import DataClassApplication
from . import Viva
from . import VivaMyPages
from . import VivaAttachments

from .application_answer import ApplicationAnswer
from .application_answer import ApplicationAnswerCollection
from .application_answer import ZeepApplication
from .application_answer import ZeepNotification
from .application_answer import ZeepHousing

from .mappers.viva_persons_to_applicants_mapper import VivaPersonsToApplicantsMapper

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

        self._viva_soap_operation_types: ApplicationType = {
            ApplicationType.NEW: self._new_application,
            ApplicationType.RECURRING: self._new_re_application,
            ApplicationType.COMPLETION: self._new_completion,
        }

        self._operation_type = application.operation_type
        self._workflow_id = application.workflow_id
        self._personal_number = application.personal_number

        self._attachments = application.attachments
        self._answer_collection = self._set_answer_collection(
            answers=application.answers)
        self._raw_data = application.raw_data
        self._raw_data_type = application.raw_data_type

    @catch_viva_error
    def submit(self):
        return self._viva_soap_operation_types[self._operation_type]()

    def _set_answer_collection(self, answers):
        answer_collection = ApplicationAnswerCollection()

        for answer in answers or []:
            application_answer = ApplicationAnswer(
                value=answer['value'], tags=answer['field']['tags'])
            answer_collection.append(application_answer)

        return answer_collection

    def _create_recurring_application(self):
        initial_application = {
            'OTHER': '',
            'RAWDATA': self._raw_data,
            'RAWDATATYPE': self._raw_data_type,
            'HOUSEHOLDINFO': ''
        }

        application = self._get_zeep_application_dict()

        return {**initial_application, **application}

    def _create_new_application(self):
        initial_new_application = {
            'OTHER': '',
            'RAWDATA': self._raw_data,
            'RAWDATATYPE': self._raw_data_type,
        }

        housing = ZeepHousing(
            application_answer_collection=self._answer_collection)
        client = housing.get_client(self._personal_number)

        if not client:
            raise ValueError(f'Client can not be {client}. Verify your tags!')

        attachment_list = self._get_zeep_attachment_list()
        new_application = self._get_zeep_application_dict()

        return {**initial_new_application, **client, **new_application, **attachment_list}

    def _save_attachments(self):
        for attachment in self._attachments:
            self._viva_attachments.save(attachment=attachment)
        return True

    def _get_zeep_attachment_list(self):
        attachment_category_type = {
            'incomes': 'Inkomster',
            'expenses': 'Utgifter',
            'completion': 'Komplettering',
        }

        zeep_attachments = {'ATTACHMENTS': {'ATTACHMENT': []}}

        for attachment in self._attachments:
            name = attachment['name']
            category = attachment['category']
            completion_type = attachment_category_type[category]

            zeep_attachments['ATTACHMENTS']['ATTACHMENT'].append({
                'ID': attachment['id'],
                'NAME': name,
                'FILENAME': name,
                'TYPE': completion_type,
                'DESCRIPTION': name,
            })

        return zeep_attachments

    def _get_zeep_notfication_list(self):
        coapplicant = self._my_pages.get_case_person_on_type(
            viva_person_type='partner')
        applicant = self._my_pages.get_case_client()

        applicants_mapper = VivaPersonsToApplicantsMapper(
            applicant, coapplicant)

        notification = ZeepNotification(applicants=applicants_mapper.get_applicants(
        ), application_answer_collection=self._answer_collection)

        sms_notification_list = notification.get_sms_list()

        return sms_notification_list

    def _get_zeep_application_dict(self):
        zeep_dict = ZeepApplication(
            application_answer_collection=self._answer_collection)
        return zeep_dict

    def _new_application(self):
        self._save_attachments()
        new_application = self._create_new_application()

        response = self._service.NEWAPPLICATION(
            KEY='',
            USER=self._personal_number,
            IP='0.0.0.0',
            CASETYPE='',
            SYSTEM=1,
            APPLICATION=new_application,
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

            REAPPLICATION=self._create_recurring_application(),

            NOTIFYINFOS={
                'NOTIFYINFO': self._get_zeep_notfication_list()
            }
        )

        return self._helpers.serialize_object(response)

    def _new_completion(self):
        self._save_attachments()

        personal_number = self._my_pages.get_personal_number()
        case_ssi = self._my_pages.get_casessi()
        completion = self._get_zeep_attachment_list()

        completion_response = self._service.NEWCOMPLETION(
            KEY='',
            USER=personal_number,
            IP='0.0.0.0',
            SSI=case_ssi,
            WORKFLOWID=self._workflow_id,
            COMPLETION=completion
        )

        return self._helpers.serialize_object(completion_response)
