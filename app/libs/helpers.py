from datetime import datetime


def date_from_milliseconds(milliseconds=int):
    seconds = milliseconds / 1000

    try:
        date = datetime.fromtimestamp(seconds).strftime('%Y-%m-%d')
    except Exception as e:
        raise e

    return date
