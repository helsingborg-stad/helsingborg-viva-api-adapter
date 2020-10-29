from datetime import datetime

categories = set(['expenses', 'incomes', 'assets'])
category_types = {
    'boende': 'Hyra',
    'el': 'El',
    'reskostnad': 'Busskort',
    'lon': 'Lön',
    'car': 'Bil',
    'mobile': 'Mobiltelefon'
}
user_inputs = set(['amount', 'date'])
applies_to_type = 'coapplicant'


def parse_application_data(answers=list, period=dict, initial_data=dict):
    if not answers:
        return False

    start_date = datetime.fromtimestamp(
        period['start_date'] / 1000).strftime('%Y-%m-%d')
    end_date = datetime.fromtimestamp(
        period['end_date'] / 1000).strftime('%Y-%m-%d')

    period_string = f"{start_date} - {end_date}"

    data = dict()

    for answer in answers:
        tags = answer['field']['tags']

        category_list_name = [n for n in tags if n in categories].pop().upper()
        category_name = category_list_name[:-1]

        category_type = [t for t in tags if t in set(category_types)].pop()
        category_type_description = category_types[category_type]

        param_user_input = [v for v in tags if v in user_inputs].pop()
        if param_user_input == 'date':
            answer['value'] = datetime.fromtimestamp(
                answer['value'] / 1000).strftime('%Y-%m-%d')

        applies_to = [a for a in tags if a == applies_to_type]
        if applies_to:
            applies_to = applies_to.pop()
            category_type_description = category_type_description + ' partner'
        else:
            applies_to = 'applicant'

        if category_list_name not in data:
            data[category_list_name] = []

        item = [z for z in data[category_list_name]
                if category_type == z[category_name]['TYPE']
                and applies_to == z[category_name]['APPLIESTO']]

        if item:
            item[0][category_name][param_user_input.upper()] = str(answer['value'])
        else:
            category_data = {
                category_name: {
                    'TYPE': category_type,
                    'FREQUENCY': '',
                    'APPLIESTO': applies_to,
                    'DESCRIPTION': category_type_description,
                    'PERIOD': period_string,
                    param_user_input.upper(): str(answer['value'])
                }
            }

            data[category_list_name].append(category_data)

    return {**initial_data, **data}
