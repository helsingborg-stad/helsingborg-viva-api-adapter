import re

from flask import current_app
from hashids import Hashids


hashids = Hashids(
    salt=current_app.config['SALT'],
    min_length=32
)


def parse_hash(hashid=int, env=current_app.config['ENV']):
    decoded = str(hashids.decode(hashid)[0])

    if env == 'development':
        regex = re.compile('([0-9]{8})([0-9]{4})')
        parts = regex.match(decoded).groups()

        # Ylva Jansson
        # In sync with Navet, BankId, AWS, and Viva
        # TODO
        # Move this check to separate handler
        if '195809262743' in decoded:
            return '-'.join(parts)
        else:
            return 'T'.join(parts)

    else:
        return decoded
