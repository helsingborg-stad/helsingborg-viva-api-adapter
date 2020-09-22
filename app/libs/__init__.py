import re


from .hashids import parse_hash
from .viva_application import VivaApplication
from .my_pages import MyPages


def make_test_pnr(pnr):
    regex = re.compile('([0-9]{8})([0-9]{4})')
    parts = regex.match(pnr).groups()
    return 'T'.join(parts)
