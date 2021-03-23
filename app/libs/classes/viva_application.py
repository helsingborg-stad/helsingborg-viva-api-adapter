from zeep.exceptions import Fault

from . import DataClassApplication
from . import Viva
from . import VivaMyPages
from . import VivaAttachments

from ..datetime_helper import milliseconds_to_date_string


class VivaApplication(Viva):

    def __init__(self,
                 application: DataClassApplication,
                 my_pages: VivaMyPages,
                 viva_attachments: VivaAttachments = None,
                 wsdl='VivaApplication'):
        super(VivaApplication, self).__init__()

        if not isinstance(application, DataClassApplication):
            raise Fault(
                message='application should be an instance of DataClassApplication', code=500)

        if not isinstance(my_pages, VivaMyPages):
            raise Fault(
                message='my_pages should be an instance of VivaMyPages', code=500)

        if viva_attachments and not isinstance(viva_attachments, VivaAttachments):
            raise Fault(
                message='viva_attachments should be an instance of VivaAttachments', code=500)

        self._my_pages = my_pages
        self._viva_attachments = viva_attachments
        self._service = self._get_service(wsdl)

        self._viva_soap_operation_types = {
            'basic': self._new_application,
            'recurrent': self._new_re_application,
            'completion': self._new_completion,
            'status': self._get_application_status,
        }

        self._operation_type = application.operation_type
        self._workflow_id = application.workflow_id
        self._attachments = application.attachments
        self._answers = application.answers
        self._raw_data = application.raw_data
        self._raw_data_type = application.raw_data_type

    def submit(self):
        return self._viva_soap_operation_types[self._operation_type]()

    def _get_application_status(self):
        """
        ApplicationStatus förklaring:

        -1 - fel (t.ex. person finns inte i personregistret)

        eller summan av:
        1 - ansökan tillåten
        2 - autosave finns (man har påbörjat en ansökan)
        4 - väntar signering (avser medsökande: sökande har signerat en ansökan som inkluderar medsökande)
        8 - väntar att medsökande ska signera (avser sökande medan hen väntar på att medsökande ska signera)
        16 - ansökan inskickad
        32 - ansökan mottagen(/registrerad i Viva)
        64 - komplettering begärd
        128 - ärende finns (försörjningsstödsärende)
        256 - ett ärende är aktiverat på web (egenskap på ärendet som gör att det visas på Mina sidor)
        512 - ärendet tillåter e-ansökan  (egenskap på ärendet som gör att det går att skapa fortsatt ansökan)

        2, 4 och 8 blir bara aktuella när man parkerar eller autosparar ansökan i Viva.

        Det är bara när ApplicationStatus innehåller 1 (summan är udda) som ansökan kan lämnas in.

        128 + 256 + 512 kommer i princip alltid att vara med eftersom ett ärende som tillåter e-ansökan är en förutsättning för fortsatt ansökan.

        När ApplicationStatus bara är 1 finns inget ärende och man kan lämna in en grundansökan.
        """

        personal_number = self._my_pages.get_personal_number()

        status_number = self._service.APPLICATIONSTATUS(
            SUSER=personal_number,
            SPNR=personal_number,
            SCASETYPE='01',  # 01 = EKB
            SSYSTEM=1
        )

        status_description = {
            1: 'Ansökan tillåten',
            2: 'Autosave',
            4: 'Väntar signering',
            8: 'Väntar att medsökande ska signera',
            16: 'Ansökan inskickad',
            32: 'Ansökan mottagen/registrerad',
            64: 'Komplettering begärd',
            128: 'Arende finns (försörjningsstödsärende)',
            256: 'Ett ärende är aktiverat på webben',
            512: 'Ärendet tillåter e-ansökan',
        }

        statuses = list()

        if status_number > 128:
            key = 128
            statuses.append({
                'code': key,
                'description': status_description[key]
            })
            status_number -= key

        if status_number > 256:
            key = 256
            statuses.append({
                'code': key,
                'description': status_description[key]
            })
            status_number -= key

        if status_number > 512:
            key = 512
            statuses.append({
                'code': key,
                'description': status_description[key]
            })
            status_number -= key

        if status_number in status_description:
            statuses.append({
                'code': status_number,
                'description': status_description[status_number]
            })
        else:
            statuses.append({
                'code': status_number,
                'description': 'N/A'
            })

        return self._helpers.serialize_object(statuses)

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

            # lon:0, get lon
            item_type = element_type_tag.split(':')[0]
            

            item = element_item_dict.get(element_type_tag, {
                'TYPE': item_type,
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

            element_item_dict[element_type_tag] = item

        element_item_list = self._convert_dict_to_list(dict=element_item_dict)
        return element_item_list

    def _filter_answer_by_tag_name(self, tag_name=str):
        filtered_answer_list = list(
            filter(lambda answer: tag_name in answer['field']['tags'], self._answers))
        return filtered_answer_list

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
            'annat': 'Övrigt',
            'other_attachments': 'Övriga underlag',
        }

        tag = next(
            (tag for tag in tag_list if tag.split(':')[0] in element_type_list.keys()), None)

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
                'NOTIFYINFO': {
                    'ID': personal_number,
                    'ADDRESS': self._my_pages.get_phone_number(),
                    'ADDRESSTYPE': 'sms'
                }
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

class Answers(object):
