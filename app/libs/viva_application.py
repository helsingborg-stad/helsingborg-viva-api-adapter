from .viva import Viva
from .datetime_helper import milliseconds_to_date_string


class VivaApplication(Viva):

    def __init__(self,
                 my_pages,
                 wsdl='VivaApplication',
                 application_type=str,
                 answers=list
                 ):
        super(VivaApplication, self).__init__()

        self._type = application_type
        self._types = {
            'basic': self._new_application,
            'recurrent': self._new_re_application
        }

        self._my_pages = my_pages
        self._answers = answers

        self._service = self._get_service(wsdl)

    def submit(self):
        return self._types[self._type]()

    def get_application_status(self):
        personal_number = self._my_pages.get_personal_number()

        response = self._service.APPLICATIONSTATUS(
            SUSER=personal_number,
            SPNR=personal_number,
            SCASETYPE='',
            SSYSTEM=1
        )

        return self._helpers.serialize_object(response)

    def _get_application(self):
        initial_application = {
            'OTHER': '',
            'RAWDATA': '',
            'RAWDATATYPE': 'PDF',
            'HOUSEHOLDINFO': ''
        }

        application = self._answers_to_application()

        return {**initial_application, **application}

    def _answers_to_application(self):
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
        if not self._answers:
            return False

        # rules for generating the viva application structure based on answer tags
        categories = set(['expenses', 'incomes', 'assets'])
        category_types = {
            'boende': 'Hyra',
            'el': 'El',
            'reskostnad': 'Reskostnad',
            'lon': 'Lön',
            'car': 'Bil',
            'mobile': 'Mobiltelefon'
        }
        user_inputs = set(['amount', 'date'])

        application = dict()

        for answer in self._answers:
            tags = answer['field']['tags']

            # EXPENSES | INCOMES
            category_list_name = [
                n for n in tags if n in categories].pop().upper()

            # EXPENSE | INCOME
            category_name = category_list_name[:-1]

            category_type = [t for t in tags if t in set(category_types)].pop()
            category_type_description = category_types[category_type]

            user_input = [v for v in tags if v in user_inputs].pop()
            if 'date' in user_input:
                answer['value'] = milliseconds_to_date_string(
                    int(answer['value']))

            # Partner
            applies_to = [a for a in tags if a == 'coapplicant']
            if applies_to:
                applies_to = applies_to.pop()
                category_type_description = category_type_description + ' partner'
            else:
                applies_to = 'applicant'

            if category_list_name not in application:
                application[category_list_name] = []

            items = [z for z in application[category_list_name]
                     if category_type == z[category_name]['TYPE']
                     and applies_to == z[category_name]['APPLIESTO']]

            if items:
                item = items.pop()
                item[category_name][user_input.upper()] = str(answer['value'])
            else:
                category = {
                    category_name: {
                        'TYPE': str(category_type),
                        'FREQUENCY': '',
                        'APPLIESTO': str(applies_to),
                        'DESCRIPTION': str(category_type_description),
                        'PERIOD': '',
                        user_input.upper(): str(answer['value']),
                    }
                }

                application[category_list_name].append(category)

        return application

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
            WORKFLOWID='',

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
