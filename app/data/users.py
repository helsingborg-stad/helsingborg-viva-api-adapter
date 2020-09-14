from flask import current_app
from ..libs import hashids

# mock data
USERS = [
    {
        'name': 'Kalle Testarsson',
        'pnr': 199412015852,
        'mypages_url': '/mypages/' + hashids.encode(199412015852),
    },
    {
        'name': 'Therese Blom',
        'pnr': 199612240201,
        'mypages_url': '/mypages/' + hashids.encode(199612240201),
    },
    {
        'name': 'Ahmad Saloui',
        'pnr': 197010108095,
        'mypages_url': '/mypages/' + hashids.encode(197010108095),
    },
    {
        'name': 'Filippa Unge',
        'pnr': 197105016161,
        'mypages_url': '/mypages/' + hashids.encode(197105016161),
    },
    {
        'name': 'Petra Hansson',
        'pnr': 199604014440,
        'mypages_url': '/mypages/' + hashids.encode(199604014440),
    },
    {
        'name': 'Joel Holmgren',
        'pnr': 199612011214,
        'mypages_url': '/mypages/' + hashids.encode(199612011214),
    },
]
