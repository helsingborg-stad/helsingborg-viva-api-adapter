from datetime import datetime
from .helpers import date_from_milliseconds

# Viva category pattern
categories = set(['expenses', 'incomes', 'assets'])
category_types = {
    'boende': 'Hyra',
    'el': 'El',
    'reskostnad': 'Reskostnad',
    'hemforsakring': 'Hemförsäkring',
    'aldreforsorjningsstod': 'Äldreförsörjningsstöd',
    'akassa': 'A-kassa',
    'barnomsorg': 'Barnomsorg',
    'bredband': 'Bredband',
    'medicin': 'Medicin',
    'akuttandvard': 'Akut tandvård',
    'tandvard': 'Tandvård',
    'annantandvard': 'Annan tandvård',
    'lakarvard': 'Läkarvård',
    'lon': 'Lön',
    'bil': 'Bil',
    'lagenhet': 'Lägenhet',
    'motorcykel': 'Motorcykel',
    'hus': 'Hus',
    'mobile': 'Mobiltelefon',
    'annan': 'Övrigt',
}
user_inputs = set(['amount', 'date', 'description'])
applies_to_type = 'coapplicant'

initial_data = {
    'RAWDATA': '',
    'RAWDATATYPE': 'PDF',
    'HOUSEHOLDINFO': '',
    'OTHER': '',
}


def parse_application(answers=list, period=dict, initial_data=initial_data):
    """
    Helper function for building the Viva specific data structure from
    answers list stored in AWS DynamoDB cases data structure.

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
    if not answers:
        return False

    data = dict()

    start_date = date_from_milliseconds(period['start_date'])
    end_date = date_from_milliseconds(period['end_date'])
    period_string = f"{start_date} - {end_date}"

    for answer in answers:
        tags = answer['field']['tags']

        category_list_name = [n for n in tags if n in categories].pop().upper()
        category_name = category_list_name[:-1]

        category_type = [t for t in tags if t in set(category_types)].pop()
        category_type_description = category_types[category_type]

        param_user_input = [v for v in tags if v in user_inputs].pop()
        if 'date' in param_user_input:
            answer['value'] = date_from_milliseconds(int(answer['value']))

        applies_to = [a for a in tags if a == applies_to_type]
        if applies_to:
            applies_to = applies_to.pop()
            category_type_description = category_type_description + ' partner'
        else:
            applies_to = 'applicant'

        if category_list_name not in data:
            data[category_list_name] = []

        items = [z for z in data[category_list_name]
                 if category_type == z[category_name]['TYPE']
                 and applies_to == z[category_name]['APPLIESTO']]

        if items:
            item = items.pop()
            item[category_name][param_user_input.upper()] = str(answer['value'])
        else:
            category_data = {
                category_name: {
                    'TYPE': str(category_type),
                    'FREQUENCY': '',
                    'APPLIESTO': str(applies_to),
                    'DESCRIPTION': str(category_type_description),
                    'PERIOD': str(period_string),
                    param_user_input.upper(): str(answer['value']),
                }
            }

            data[category_list_name].append(category_data)

    return {**initial_data, **data}
