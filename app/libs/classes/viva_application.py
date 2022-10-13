from typing import List

from app.libs.enum import ApplicationType
from app.libs.classes.viva_application_data import DataClassApplication, Answer
from app.libs.classes.viva import Viva
from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.classes.viva_attachments import VivaAttachments
from app.libs.classes.application_answer.answer import ApplicationAnswer
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.zeep import ZeepApplication
from app.libs.classes.application_answer.zeep_notification import ZeepNotification
from app.libs.classes.mappers.viva_persons_to_applicants_mapper import VivaPersonsToApplicantsMapper
from app.libs.classes.application_answer.zeep_person_info import ZeepPersonInfo
from app.libs.viva_error_helper import catch_viva_error


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

    def _set_answer_collection(self, answers: List[Answer]):
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

        zeep_person_info = ZeepPersonInfo(
            application_answer_collection=self._answer_collection)

        client_info = zeep_person_info.create(
            personal_number=self._personal_number, type='client')

        if not client_info:
            raise ValueError(
                f'Client can not be {client_info}. Verify your tags!')

        partner_info = zeep_person_info.create(
            personal_number=self._personal_number, type='partner')

        children_info = zeep_person_info.create(
            personal_number=self._personal_number, type='children')

        attachment_list = self._get_zeep_attachment_list()
        new_application = self._get_zeep_application_dict()

        return {**initial_new_application, **client_info, **partner_info, **children_info, ** new_application, **attachment_list}

    def _save_attachments(self):
        for attachment in self._attachments:
            self._viva_attachments.save(attachment=attachment)
        return True

    def _get_zeep_attachment_list(self):
        attachment_category_type = {
            'incomes': 'Inkomster',
            'expenses': 'Utgifter',
            'completion': 'Komplettering',
            'undefined': '',
        }

        zeep_attachments = {'ATTACHMENTS': {'ATTACHMENT': []}}

        for attachment in self._attachments:
            name = attachment['name']
            category = attachment['category'] or 'undefined'
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
