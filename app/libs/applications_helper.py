cost_types = ['EXPENSES', 'INCOMES']


def parse_application_data(answers, period_string=str):
    data = dict()

    for answer in answers:
        tags = answer['field']['tags']

        if tags in cost_types:
            print('HEPP')

            # create a single income or expense and add it to the array passed thorugh initial_data
            # applies_to = 'coapplication' if 'Partner' in key else 'applicant'

            # data.append(
            #     {
            #         parent_key[:-1]: {
            #             'TYPE': key,
            #             'APPLIESTO': applies_to,
            #             'PERIOD': period_string,
            #             'FREQUENCY': 12,
            #             'AMOUNT': value['amount'],
            #             'DATE': value['date'],
            #             'DESCRIPTION': '',
            #         }
            #     }
            # )

    return data
