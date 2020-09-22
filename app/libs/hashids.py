import re

from flask import current_app
from hashids import Hashids


hashids = Hashids(
    salt=current_app.config['SALT'],
    min_length=32
)


def parse_hash(hashid=int):
    return str(hashids.decode(hashid)[0])
