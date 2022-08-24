from datetime import datetime


def milliseconds_to_date_string(milliseconds: int) -> str:
    """
    return format: year-month-date
    """
    try:
        seconds = milliseconds / 1000
        date = datetime.fromtimestamp(seconds).strftime('%Y-%m-%d')
        return date
    except Exception as e:
        raise e


def generate_period_string(period) -> str:
    if not period.start_date or not period.end_date:
        return ''

    start_date = milliseconds_to_date_string(period.start_date)
    end_date = milliseconds_to_date_string(period.end_date)

    return f"{start_date} - {end_date}"
