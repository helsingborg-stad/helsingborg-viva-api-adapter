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
        'name': 'Victor Blixt (AMF Viva-test)',
        'info': 'Child: Yessica Blixt',
        **insert_pnr_and_endpoints(197503014552),
    },
    {
        'name': 'Ali Al-Jabi (AMF Viva-test)',
        'info': 'Partner with Pernilla Al-Jabi. Child Sara Al-Jabi',
        **insert_pnr_and_endpoints(198010139395),
    },
    {
        'name': 'Pernilla Al-Jabi (AMF Viva-test)',
        'info': 'Coapplicant with Ali Al-Jabi. Child: Sara Al-Jabi',
        **insert_pnr_and_endpoints(198210023126),
    },
    {
        'name': 'Per Nilsson (AMF Viva-test)',
        'info': 'Partner with Sudden Karlsson',
        **insert_pnr_and_endpoints(198307286172),
    },
    {
        'name': 'Sudden Karlsson (AMF Viva-test)',
        'info': 'Coapplicant with Per Nilsson',
        **insert_pnr_and_endpoints(197503245057),
    },
    {
        'name': 'Jan Tootsie (AMF Viva-test)',
        'info': 'Single',
        **insert_pnr_and_endpoints(197404142338),
    },
    {
        'name': 'Harald Unge (AMF Viva-test)',
        'info': 'Single - Developer tester',
        **insert_pnr_and_endpoints(197005012336),
    },
    {
        'name': 'Vera Toth (AMF Viva-test)',
        'info': 'Single - Developer tester',
        **insert_pnr_and_endpoints(196001198685),
    },
    {
        'name': 'Petra Hansson (AMF Viva-test)',
        'info': 'Partner with Joel Holmgren',
        **insert_pnr_and_endpoints(199604014440),
    },
    {
        'name': 'Joel Hansson (AMF Viva-test)',
        'info': 'Coapplicant with Petra Holmgren',
        **insert_pnr_and_endpoints(199612011214),
    },
    {
        'name': 'Harald Unge (HBGWorks Viva-test)',
        'info': 'Single - Developer tester',
        **insert_pnr_and_endpoints(197005018697),
    },
    {
        'name': 'Sara Jeppsson (HBGWorks Viva-test)',
        'info': 'Coapplicant with Jesper Jeppsson',
        **insert_pnr_and_endpoints(198603072383),
    },
    {
        'name': 'Fredrik Test (HBGWorks Viva-test)',
        'info': 'Partner with Mikaela Test. Child: Chloé Test',
        **insert_pnr_and_endpoints(197101174659),
    },
    {
        'name': 'Mikaela Test (HBGWorks Viva-test)',
        'info': 'Coapplicant to Fredrik Test. Child: Chloé Test',
        **insert_pnr_and_endpoints(197505018387),
    },
    {
        'name': 'Stina Månsson (HBGWorks Viva-test)',
        'info': 'Partner with Bertil Göransson',
        **insert_pnr_and_endpoints(198310011906),
    },
    {
        'name': 'Bertil Göransson (HBGWorks Viva-test)',
        'info': 'Coapplicant to Stina Månsson',
        **insert_pnr_and_endpoints(197910315352),
    },
    {
        'name': 'Jesper Jeppsson (HBGWorks Viva-test)',
        'info': 'Partner with Sara Jeppsson',
        **insert_pnr_and_endpoints(198603072391),
    },
    {
        'name': 'Anna Berg (HBGWorks Viva-test)',
        'info': 'Single - Child: Olivia Berg',
        **insert_pnr_and_endpoints(199809083125),
    },
    {
        'name': 'Sandra Kranz (HBGWorks Viva-test)',
        'info': 'Single - Child: Malin Urbansson',
        **insert_pnr_and_endpoints(198602272380),
    },
    {
        'name': 'Evil Dude',
        'info': 'Testing when peronal number does not exists in VIVA',
        **insert_pnr_and_endpoints(199901019999),
    },
]
