from typing import List, Any
from zeep.helpers import serialize_object

from app.libs.enum import ApplicationType
from app.libs.classes.viva_application_data import DataClassApplication, Answer
from app.libs.classes.viva_my_pages import VivaMyPages
from app.libs.classes.viva_attachments import VivaAttachments
from app.libs.classes.application_answer.answer import ApplicationAnswer
from app.libs.classes.application_answer.collection import ApplicationAnswerCollection
from app.libs.classes.application_answer.zeep import ZeepApplication
from app.libs.classes.application_answer.zeep_notification import ZeepNotification
from app.libs.classes.mappers.viva_persons_to_applicants_mapper import VivaPersonsToApplicantsMapper
from app.libs.classes.application_answer.zeep_person_info import ZeepPersonInfo
from app.libs.viva_error_helper import catch_viva_error


class VivaApplication:

    def __init__(self,
                 client: Any,
                 application: DataClassApplication,
                 my_pages: VivaMyPages,
                 viva_attachments: VivaAttachments) -> None:

        self._client = client
        self._my_pages = my_pages
        self._viva_attachments = viva_attachments

        self._viva_soap_operation_types = {
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

        household_info = self._get_zeep_household_info()
        attachment_list = self._get_zeep_attachment_list()
        new_application = self._get_zeep_application_dict()

        return {**initial_new_application, **household_info, **new_application, **attachment_list}

    def _save_attachments(self):
        for attachment in self._attachments:
            self._viva_attachments.save(attachment=attachment)
        return True

    def _get_zeep_household_info(self):
        client_zeep_person_info = ZeepPersonInfo(
            application_answer_collection=self._answer_collection)
        client_info = client_zeep_person_info.create()
        if not client_info:
            raise ValueError(
                'Invalid client info. Please verify answer tags.')

        partner_zeep_person_info = ZeepPersonInfo(
            application_answer_collection=self._answer_collection, person_type='partner')
        partner_info = partner_zeep_person_info.create() or {}

        children_zeep_person_info = ZeepPersonInfo(
            application_answer_collection=self._answer_collection, person_type='children')
        children_info = children_zeep_person_info.create() or {}

        return {
            **client_info,
            **partner_info,
            **children_info,
        }

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

        response = self._client.NEWAPPLICATION(
            KEY='',
            USER=self._personal_number,
            IP='0.0.0.0',
            CASETYPE='',
            SYSTEM=1,
            APPLICATION=new_application,
        )

        return serialize_object(response)

    def _new_re_application(self):
        personal_number = self._my_pages.get_personal_number()

        response = self._client.NEWREAPPLICATION(
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

        return serialize_object(response)

    def _new_completion(self):
        self._save_attachments()

        personal_number = self._my_pages.get_personal_number()
        case_ssi = self._my_pages.get_casessi()
        completion = self._get_zeep_attachment_list()

        completion_response = self._client.NEWCOMPLETION(
            KEY='',
            USER=personal_number,
            IP='0.0.0.0',
            SSI=case_ssi,
            WORKFLOWID=self._workflow_id,
            COMPLETION=completion
        )

        return serialize_object(completion_response)
