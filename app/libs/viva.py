import zeep.helpers as zeep_helpers
from flask import current_app
from zeep import Client, Settings

from .session import Session


class Viva(object):

    def __init__(self,
        session=Session,
        settings=Settings,
        current_app=current_app,
        zeep_helpers=zeep_helpers
    ):
        self._config = current_app.config['VIVA']
        self._helpers = zeep_helpers
        self._session = session()
        self._settings = settings(force_https=True)

    def _get_service(self, wsdl):
        transport = self._session.get_transport()
        wsdl_url = self._config['wsdl_url'] + '/' + wsdl + '?WSDL'
        client = Client(wsdl=wsdl_url, transport=transport, settings=self._settings)

        return client.service
