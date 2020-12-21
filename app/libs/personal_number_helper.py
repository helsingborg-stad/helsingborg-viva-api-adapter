import re
from hashids import Hashids

from flask import current_app

hashids_instace = Hashids(salt=current_app.config['SALT'], min_length=32)


def hash_to_personal_number(hash_id=str):
    raise_error = Fault(message='Invalid request', code=400)

    if not hash_id:
        raise raise_error

    if current_app.config['ENV'] in ['development', 'test']:
        personal_number = to_test_personal_number(personal_number)

        return personal_number
    except Exception:
        raise raise_error


def to_test_personal_number(personal_number=str):
    regex = re.compile('([0-9]{8})([0-9]{4})')
    parts = regex.match(personal_number).groups()

    if '195809262743' in personal_number:
        # Ylva Jansson
        # Special person in VIVA test
        # yyyymmdd-nnnn
        return '-'.join(parts)
    else:
        # VIVA test format
        # yyyymmddTnnnn
        return 'T'.join(parts)
