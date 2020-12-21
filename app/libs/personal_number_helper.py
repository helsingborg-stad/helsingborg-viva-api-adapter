import re
from flask import jsonify
from hashids import Hashids
from zeep.exceptions import Fault

from flask import current_app

hashids_instace = Hashids(salt=current_app.config['SALT'], min_length=32)


def hash_to_personal_number(hash_id=str):
    if not hash_id:
        raise Fault(message='invalide hash_id', code=400)

    try:
        personal_number = str(hashids_instace.decode(hash_id)[0])
        if current_app.config['ENV'] in ['development', 'test']:
            personal_number = to_test_personal_number(personal_number)

        return personal_number
    except Exception as e:
        raise Fault(e.args, code=500)


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
