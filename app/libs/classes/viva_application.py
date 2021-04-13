from zeep.exceptions import Fault

from . import DataClassApplication
from . import Viva
from . import VivaMyPages
from . import VivaAttachments

from ..datetime_helper import milliseconds_to_date_string


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
        try:
            for attachment in self._attachments:
                self._viva_attachments.save(attachment=attachment)
            return True
        except Exception as error:
            raise error

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
        zeep_dict = {}

        if not self._answers:
            return zeep_dict

        application_element_list = set(
            ['expenses', 'incomes', 'otherapplications', 'occupations', 'attachments'])

        for element in application_element_list:

            filtered_answer_list = self._filter_answer_by_tag_name(
                tag_name=element)

            if filtered_answer_list:
                element_name = element.upper()
                element_item_name = element_name[:-1]

                element_item_list = self._format_answer_list_to_element_item_list(
                    answer_list=filtered_answer_list)

                zeep_dict[element_name] = {
                    element_item_name: element_item_list}

        return zeep_dict

    def _format_answer_list_to_element_item_list(self, answer_list=list):
        element_item_dict = dict()

        for answer in answer_list:
            tag_list = answer['field']['tags']

            element_type_tag = self._find_tag_by_element_type(
                tag_list=tag_list)

            if element_type_tag is None:
                continue

            dict_item_key = element_type_tag

            group_tag = self._find_group_tag(tag_list)
            if group_tag:
                dict_item_key = f'{dict_item_key}#{group_tag}'

            item = element_item_dict.get(dict_item_key, {
                'TYPE': element_type_tag,
                'FREQUENCY': 12,
                'DATE': '',
                'PERIOD': '',
                'APPLIESTO': 'applicant',
                'DESCRIPTION': ''
            })

            if 'coapplicant' in tag_list:
                item['APPLIESTO'] = 'coapplicant'

            if 'date' in tag_list:
                item['DATE'] = milliseconds_to_date_string(answer['value'])

            if 'amount' in tag_list:
                item['AMOUNT'] = str(answer['value'])

            element_item_dict[dict_item_key] = item

        element_item_list = self._convert_dict_to_list(dict=element_item_dict)
        return element_item_list

    def _filter_answer_by_tag_name(self, tag_name=str):
        filtered_answer_list = list(
            filter(lambda answer: tag_name in answer['field']['tags'], self._answers))
        return filtered_answer_list

    def _find_group_tag(self, tag_list):
        group_tag = next(
            (tag for tag in tag_list if tag.startswith('group:')), None)
        return group_tag

    def _find_tag_by_element_type(self, tag_list):
        element_type_list = {
            'boende': 'Hyra',
            'el': 'El',
            'reskostnad': 'Reskostnad',
            'hemforsakring': 'Hemförsäkring',
            'bredband': 'Bredband',
            'akassa': 'A-kassa/Fackförening',
            'lakarvard': 'Läkarvård',
            'medicin': 'Medicinkostnader',
            'barnomsorg': 'Barnomsorg',
            'barnomsorgsskuld': 'Barnomsorg',
            'bostadslan': 'Bostadslån',
            'hyresskuld': 'Skuld hyra',
            'fackskuld': 'Skuld a-kassa/fackavgift',
            'elskuld': 'Skuld el',
            'lon': 'Lön',
            'swish': 'Swish',
            'bil': 'Bil',
            'mobile': 'Mobiltelefon',
            'annat': 'Övrig utgift',
            'annan': 'Övrig inkomst',
            'other_attachments': 'Övriga underlag',
        }

        tag = next(
            (tag for tag in tag_list if tag in element_type_list.keys()), None)

        return tag

    def _convert_dict_to_list(self, dict):
        return [value for key, value in dict.items()]

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
        try:
            if self._save_completion_attachments():
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
        except Exception as error:
            raise error
