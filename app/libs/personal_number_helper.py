import re
from typing import Union
from hashids import Hashids

from flask import current_app

hashids_instance = None


def get_hash_ids() -> Hashids:
    global hashids_instance
    if hashids_instance is None:
        hashids_instance = Hashids(
            salt=current_app.config['SALT'], min_length=32)
    return hashids_instance


def decode_hash_id(hash_id: str) -> tuple:
    if not isinstance(hash_id, str):
        raise TypeError(
            f'expected hash_id to be of type string got {hash_id} instead')

    return get_hash_ids().decode(hash_id)


def hash_to_personal_number(hash_id: str) -> str:

    decoded_hash_id = decode_hash_id(hash_id)

    if len(decoded_hash_id) == 0:
        raise ValueError(
            f'Expected decoded_hash_id to have atleast one value (a,) got {decoded_hash_id} instead')

    personal_number = str(decoded_hash_id[0])

    return to_viva_formatted_personal_number(personal_number)


def split_personal_number(personal_number: str) -> Union[tuple, None]:
    # YYYYMMDDXXXX becomes [YYYYMMDD, XXXX]
    regex = re.compile('([0-9]{8})([0-9]{4})')
    match = regex.match(personal_number)
    return match.groups() if match else None


def to_viva_formatted_personal_number(personal_number: str) -> str:
    personal_number_split = split_personal_number(personal_number) or ()
    return '-'.join(personal_number_split)
