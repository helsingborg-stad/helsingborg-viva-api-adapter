from flask import current_app
from ..libs import hashids_instance


def insert_pnr_and_endpoints(personal_number):
    return {
        'pnr': personal_number,
        'mypages_url': '/mypages/' + hashids_instance.encode(personal_number),
        'mypages_workflows_url': '/mypages/' + hashids_instance.encode(personal_number) + '/workflows',
        'applications_status_url': '/applications/' + hashids_instance.encode(personal_number) + '/status',
    }


# mock data
USERS = [
    {
        'name': 'Evil Dude',
        'info': 'Testing when peronal number does not exists in VIVA',
        **insert_pnr_and_endpoints(199901019999),
    },
    {
        'name': 'Ylva Jansson',
        'info': 'Test complete case flow',
        **insert_pnr_and_endpoints(195809262743),
    },
    {
        'name': 'Felix Persson',
        'info': 'Test Flight',
        **insert_pnr_and_endpoints(196912191118),
    },
    {
        'name': 'Harald Unge',
        'info': 'Ongoing application',
        **insert_pnr_and_endpoints(197005012336),
    },
    {
        'name': 'Victor Blixt',
        'info': 'Ongoing application, calculations',
        **insert_pnr_and_endpoints(197503014552),
    },
    {
        'name': 'Vera Toth',
        'info': 'Completion testing',
        **insert_pnr_and_endpoints(196001198685),
    },
    {
        'name': 'Petra Hansson',
        'info': 'Ongoing application, in relation to with Joel Holmgren',
        **insert_pnr_and_endpoints(199604014440),
    },
    {
        'name': 'Joel Holmgren',
        'info': 'Ongoing application, in relation to with Petra Hansson',
        **insert_pnr_and_endpoints(199612011214),
    },
    {
        'name': 'Kalle Testarsson',
        **insert_pnr_and_endpoints(199412015852),
    },
    {
        'name': 'Therese Blom',
        **insert_pnr_and_endpoints(199612240201),
    },
    {
        'name': 'Ahmad Saloui',
        **insert_pnr_and_endpoints(197010108095),
    },
    {
        'name': 'Filippa Unge',
        **insert_pnr_and_endpoints(197105016161),
    },
    {
        'name': 'Anna Berg',
        'info': 'Ongoing application',
        **insert_pnr_and_endpoints(199809081400),
    },
    {
        'name': 'Love Johansson',
        **insert_pnr_and_endpoints(196510102426),
    },
]
