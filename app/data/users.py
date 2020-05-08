from flask import current_app
from ..libs import hashids

# mock data
USERS = {
    hashids.encode(199412015852): {
        'name': 'Kalle Testarsson',
    },
    hashids.encode(199612240201): {
        'name': 'Therese Blom',
    },
    hashids.encode(197010108095): {
        'name': 'Some Name',
    },
    hashids.encode(197105016161): {
        'name': 'Filippa Unge',
    }
}
