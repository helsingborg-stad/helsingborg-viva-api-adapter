import zeep.helpers as zeep_helpers
from flask import current_app
from zeep.client import Client
from zeep.settings import Settings

from .session import Session


class Viva():

    def __init__(self,
                 settings=Settings,
                 session=Session,
                 current_app=current_app,
                 zeep_helpers=zeep_helpers
                 ):
        self._settings = settings(strict=False, xml_huge_tree=True)
        self._config = current_app.config['VIVA']
        self._helpers = zeep_helpers
        self._session = session()

    def _get_service(self, wsdl):
        transport = self._session.get_transport()
        wsdl_url = self._config['wsdl_url'] + '/' + wsdl + '?WSDL'
        client = Client(wsdl=wsdl_url, transport=transport)

        return client.service
