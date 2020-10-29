def parse_application_data(answers=list, period=str):
    data = dict()
    period_string = f"{period['start_date']} - {period['end_date']}"

    for answer in answers:
        tags = answer['field']['tags']

    return data
