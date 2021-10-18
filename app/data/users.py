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
        'name': 'Bo Kvast (Dan)',
        'info': 'Single',
        **insert_pnr_and_endpoints(199803312397),
    },
    {
        'name': 'Petronella Malteskog (Dan)',
        'info': 'Single',
        **insert_pnr_and_endpoints(198602102389),
    },
    {
        'name': 'Bror Christiansson (Dan)',
        'info': 'Single - Child: Sanna Backman',
        **insert_pnr_and_endpoints(198602132394),
    },
    {
        'name': 'Bruno Heed (Dan)',
        'info': 'Partner with Jenny Färm',
        **insert_pnr_and_endpoints(198602102397),
    },
    {
        'name': 'Jenny Färm (Dan)',
        'info': 'Partner with Bruno Heed',
        **insert_pnr_and_endpoints(199803092387),
    },
    {
        'name': 'Kurt Håkansson (Maria)',
        'info': 'Partner with Ulla Ek',
        **insert_pnr_and_endpoints(198602192398),
    },
    {
        'name': 'Ulla Ek (Maria)',
        'info': 'Partner with Kurt Håkansson',
        **insert_pnr_and_endpoints(198602179882),
    },
    {
        'name': 'Maria Johansson (Maria)',
        'info': 'Single',
        **insert_pnr_and_endpoints(196709132887),
    },
    {
        'name': 'Ylva Jansson (Maria)',
        'info': 'Single',
        **insert_pnr_and_endpoints(195809262743),
    },
    {
        'name': 'Sandra Kranz (Kenth)',
        'info': 'Single - Child: Malin Urbansson',
        **insert_pnr_and_endpoints(198602272380),
    },
    {
        'name': 'Sara Jeppsson',
        'info': 'Partner with Jesper Jeppsson',
        **insert_pnr_and_endpoints(198603072383),
    },
    {
        'name': 'Jesper Jeppsson',
        'info': 'Partner with Sara Jeppsson',
        **insert_pnr_and_endpoints(198603072391),
    },
    {
        'name': 'Evil Dude',
        'info': 'Testing when peronal number does not exists in VIVA',
        **insert_pnr_and_endpoints(199901019999),
    },
]
