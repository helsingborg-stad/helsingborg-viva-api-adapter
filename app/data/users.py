from flask import current_app
from ..libs import hashids

# mock data
USERS = [
    {
        'name': 'Kalle Testarsson',
        'mypages_url': '/mypages/' + hashids.encode(199412015852),
    },
    {
        'name': 'Therese Blom',
        'mypages_url': '/mypages/' + hashids.encode(199612240201),
    },
    {
        'name': 'Ahmad Saloui',
        'mypages_url': '/mypages/' + hashids.encode(197010108095),
    },
    {
        'name': 'Filippa Unge',
        'mypages_url': '/mypages/' + hashids.encode(197105016161),
    }
]
