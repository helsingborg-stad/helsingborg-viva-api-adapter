import re

from flask import current_app
from hashids import Hashids


hashids_instace = Hashids(
    salt=current_app.config['SALT'],
    min_length=32
)


def personal_number_from_hash(hash_id=int):
    return str(hashids_instace.decode(hash_id)[0])


def make_test_personal_number(personal_number):
    regex = re.compile('([0-9]{8})([0-9]{4})')
    parts = regex.match(personal_number).groups()

    # Ylva Jansson
    # In sync with Navet, BankId, AWS, and Viva
    if '195809262743' in personal_number:
        return '-'.join(parts)
    else:
        return 'T'.join(parts)
