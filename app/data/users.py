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
        'info': 'Single - BankID on test iPhone',
        **insert_pnr_and_endpoints(195809262743),
    },
    {
        'name': 'Felix Persson',
        'info': 'Single - Test Flight',
        **insert_pnr_and_endpoints(196912191811),
    },
    {
        'name': 'Harald Unge',
        'info': 'Single - Developer tester',
        **insert_pnr_and_endpoints(197005018697),
    },
    {
        'name': 'Vera Toth',
        'info': 'Single - Developer tester',
        **insert_pnr_and_endpoints(196001198685),
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
        'name': 'Jesper Jeppsson',
        'info': 'Partner with Sara Jeppsson',
        **insert_pnr_and_endpoints(198603072391),
    },
    {
        'name': 'Sara Jeppsson',
        'info': 'Coapplicant with Jesper Jeppsson',
        **insert_pnr_and_endpoints(198603072383),
    },
    {
        'name': 'Anna Berg',
        'info': 'Single - Child: Olivia Berg',
        **insert_pnr_and_endpoints(199809083125),
    },
    {
        'name': 'Sandra Kranz',
        'info': 'Single - Child: Malin Urbansson',
        **insert_pnr_and_endpoints(198602272380),
    },
]
