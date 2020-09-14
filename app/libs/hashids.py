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
        return 'T'.join(parts)
    else:
        return decoded
