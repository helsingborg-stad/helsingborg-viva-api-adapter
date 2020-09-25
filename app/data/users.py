from flask import current_app
from ..libs import hashids

# mock data
USERS = [
    {
        'name': 'Ylva Jansson',
        'pnr': 195809262743,
        'mypages_url': '/mypages/' + hashids.encode(195809262743),
    },
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
        'info': 'Ongoing application, in relation to with Joel Holmgren',
    },
    {
        'name': 'Joel Holmgren',
        'pnr': 199612011214,
        'mypages_url': '/mypages/' + hashids.encode(199612011214),
        'info': 'Ongoing application, in relation to with Petra Hansson',
    },
    {
        'name': 'Felix Persson',
        'pnr': 196912191118,
        'mypages_url': '/mypages/' + hashids.encode(196912191118),
        'info': 'Ongoing application',
    },
    {
        'name': 'Victor Blixt',
        'pnr': 197503014552,
        'mypages_url': '/mypages/' + hashids.encode(197503014552),
        'info': 'Ongoing application, calculations',
    },
    {
        'name': 'Anna Berg',
        'pnr': 199809081400,
        'mypages_url': '/mypages/' + hashids.encode(199809081400),
        'info': 'Ongoing application',
    },
    {
        'name': 'Love Johansson',
        'pnr': 196510102426,
        'mypages_url': '/mypages/' + hashids.encode(196510102426),
        'info': 'New case created as of 2020-09-15. First application period created as of 2020-09-15',
    },
]
