import re

from flask import current_app
from hashids import Hashids


hashids_instace = Hashids(
    salt=current_app.config['SALT'],
    min_length=32
)


def hash_to_personal_number(hash_id=str):
    personal_number = str(hashids_instace.decode(hash_id)[0])
    return personal_number


def get_test_personal_number(personal_number=str):
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


def get_personal_number(hash_id=str):
    personal_number = hash_to_personal_number(hash_id=hash_id)
    if current_app.config['ENV'] == 'development' or current_app.config['ENV'] == 'test':
        personal_number = get_test_personal_number(
            personal_number=personal_number)
    return personal_number
