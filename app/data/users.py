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
        'name': 'Anna Berg',
        'info': 'Single - Child: Olivia Berg',
        **insert_pnr_and_endpoints(199809083125),
    },
    {
        'name': 'Bo Kvast',
        'info': 'Single - Navet',
        **insert_pnr_and_endpoints(199803312397),
    },
    {
        'name': 'Felix Persson',
        'info': 'Single',
        **insert_pnr_and_endpoints(196912191811),
    },
    {
        'name': 'Harald Unge',
        'info': 'Single',
        **insert_pnr_and_endpoints(197005018697),
    },
    {
        'name': 'Maria Johansson',
        'info': 'Single',
        **insert_pnr_and_endpoints(196709132887),
    },
    {
        'name': 'Sandra Kranz',
        'info': 'Single - Child: Malin Urbansson',
        **insert_pnr_and_endpoints(198602272380),
    },
    {
        'name': 'Ylva Jansson',
        'info': 'Single - Navet',
        **insert_pnr_and_endpoints(195809262743),
    },
    {
        'name': 'Bruno Heed',
        'info': 'Partner with Jenny Färm',
        **insert_pnr_and_endpoints(198602102397),
    },
    {
        'name': 'Jenny Färm',
        'info': 'Partner with Bruno Heed',
        **insert_pnr_and_endpoints(199803092387),
    },
    {
        'name': 'Fredrik Test',
        'info': 'Partner with Mikaela Test. Child: Chloé Test',
        **insert_pnr_and_endpoints(197101174659),
    },
    {
        'name': 'Mikaela Test',
        'info': 'Coapplicant to Fredrik Test. Child: Chloé Test',
        **insert_pnr_and_endpoints(197505018387),
    },
    {
        'name': 'Sara Jeppsson',
        'info': 'Coapplicant with Jesper Jeppsson',
        **insert_pnr_and_endpoints(198603072383),
    },
    {
        'name': 'Jesper Jeppsson',
        'info': 'Partner with Sara Jeppsson',
        **insert_pnr_and_endpoints(198603072391),
    },
    {
        'name': 'Stina Månsson',
        'info': 'Partner with Bertil Göransson',
        **insert_pnr_and_endpoints(198310011906),
    },
    {
        'name': 'Bertil Göransson',
        'info': 'Coapplicant to Stina Månsson',
        **insert_pnr_and_endpoints(197910315352),
    },
    {
        'name': 'Evil Dude',
        'info': 'Testing when peronal number does not exists in VIVA',
        **insert_pnr_and_endpoints(199901019999),
    },
]
