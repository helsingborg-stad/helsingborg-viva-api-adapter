import re
from hashids import Hashids

from flask import current_app

#hashids_instance = Hashids(salt=current_app.config['SALT'], min_length=32)
hashids_instance = None


def getHashIds():
    if hashids_instance == None:
        hashids_instance = Hashids(
            salt=current_app.config['SALT'], min_length=32)
    return hashids_instance


def decode_hash_id(hash_id: str = None):
    if not isinstance(hash_id, str):
        raise TypeError(
            f'expected hash_id to be of type string got {hash_id} instead')

    return getHashIds().decode(hash_id)


def hash_to_personal_number(hash_id=None):

    decoded_hash_id = decode_hash_id(hash_id)

    if len(decoded_hash_id) == 0:
        raise ValueError(
            f'Expected decoded_hash_id to have atleast one value (a,) got {decoded_hash_id} instead')

    personal_number = str(decoded_hash_id[0])

    viva_personal_number = to_viva_formatted_personal_number(personal_number)
    return viva_personal_number


def split_personal_number(personal_number=str):
    # YYYYMMDDXXXX parts becomes [YYYYMMDD, XXXX]
    regex = re.compile('([0-9]{8})([0-9]{4})')
    parts = regex.match(personal_number).groups()
    return parts


def to_viva_formatted_personal_number(personal_number=str):
    personal_number_split = split_personal_number(personal_number)
    return '-'.join(personal_number_split)
