import base64
from . import Viva
from ..datetime_helper import milliseconds_to_date_string


class VivaApplication(Viva):

    def __init__(self, my_pages, wsdl='VivaApplication', application=dict):
        super(VivaApplication, self).__init__()

        self._type = application_type
        self._types = {
            'basic': self._new_application,
            'recurrent': self._new_re_application
        }
        self._my_pages = my_pages
        self._answers = answers
        self._service = self._get_service(wsdl)

        if isinstance(application, dict):
            self._type = application['application_type']
            self._types = {
                'basic': self._new_application,
                'recurrent': self._new_re_application
            }

            self._workflow_id = application['workflow_id']
            self._answers = application['answers']
            self._raw_data = application['raw_data']
            self._raw_data_type = application['raw_data_type'].upper()

    def submit(self):
        return self._types[self._type]()

    def get_application_status(self):
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

    def _answers_to_zeep_dict(self):
        """
        Building Viva specific data structure from answers

        From this:
        "answers": [
        {
            "field": {
                "tags": [
                    "expenses",
                    "boende",
                    "date"
                ]
            },
            "value": 1601994748326
        },
        {
            "field": {
                "tags": [
                    "expenses",
                    "boende",
                    "amount"
                ]
            },
            "value": 8760
        },
        ..
        ..
        ..

        To this:
        "EXPENSES": [
            {
            "EXPENSE": {
                "TYPE": "Mobiltelefon",
                "DESCRIPTION": "avtal",
                "APPLIESTO": "coapplicant",
                "FREQUENCY": 12,
                "PERIOD": "2020-05-01 - 2020-05-31",
                "AMOUNT": 199,
                "DATE": "2020-05-08"
            }
            },
            {
            "EXPENSE": {
                "TYPE": "Mobiltelefon",
                "DESCRIPTION": "avtal",
                "APPLIESTO": "applicant",
                "FREQUENCY": 12,
                "PERIOD": "2020-05-01 - 2020-05-31",
                "AMOUNT": 169,
                "DATE": "2020-05-08"
            }
            }
        ],
        ..
        ..
        ..

        """
    
        group_names = set(['expenses', 'incomes', 'assets', 'otherapplications', 'occupations', 'attachments'])
        group_item_types = {
            'boende': 'Hyra',
            'el': 'El',
            'reskostnad': 'Reskostnad',
            'hemforsakring': 'Hemförsäkring',
            'bredband': 'Bredband',
            'lon': 'Lön',
            'car': 'Bil',
            'mobile': 'Mobiltelefon',
            'annat': 'Övrigt',
            'other_attachments': 'Övriga underlag',
        }

        zeep_dict = {}

        if not self._answers:
            return zeep_dict


        for group_name in group_names:  
            group_answers = self._filter_answer_by_tag_name(self._answers, group_name)
            if group_answers:
                group_key = group_name.upper()
                group_items = self._format_answers_to_group_items(group_answers, group_item_types)
                group_item_key = group_key[:-1]
                keyed_group_items = self._keyed_dicts_in_list(group_item_key, item_list)
                zeep_dict[group_key] = group_items

        return zeep_dict

    def _format_answers_to_group_items(self, answer_list, types):
        item_list = []
        for answer in answer_list:
            tags = answer['field']['tags']

            item_type = self._find_group_item_type_from_tags(tags, types)
            item_index = self._find_group_item_index(item_list, item_type)
        
            item = { 
                'TYPE': item_type,
                'FREQUENCY': '',
                'DATE': '',
                'PERIOD': '',
                'APPLIESTO': 'applicant'
            }

            if item_index is not None:
                item = item_list[item_index]

            if 'coapplicant' in tags:
                item['APPLIESTO'] = 'coapplicant'
            
            if 'date' in tags:
                item['DATE'] = milliseconds_to_date_string(answer['value'])
            
            if 'amount' in tags:
                item['AMOUNT'] = str(answer['value'])

            item_list = _update_or_append_group_item(item_list, item)
        return item_list
    
    def _keyed_dicts_in_list(key_name, dict_list):
        keyed_dict_list = [{key_name: d} for d in dict_list]
        return keyed_dict_list
    
    def _filter_answer_by_tag_name(answers, group_name):
        filtered_answers = list(filter(lambda answer: group_name in answer['field']['tags'], answers))
        return filtered_answers

    def _find_group_item_type_from_tags(values, types):
        group_item_type = next((t for t in types if t in set(values)), None)
        return group_item_type

    def _find_group_item_index(group_dict, group_item_type):
        index = next((index for (index, d) in enumerate(group_dict) if d["TYPE"] == group_item_type), None)
        return index
    
    def _update_or_append_group_item(group_list, group_item):
        group_item_index = _find_group_item_index(group_list, group_item['TYPE'])
        
        if group_item_index is None: 
            group_list.append(group_item)
            return group_list

        group_list[group_item_index] = group_item
        return group_list

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
