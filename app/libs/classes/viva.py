from zeep.client import Client

from app.libs.classes.session import AbstractSession


class Viva():

    def __init__(self, config, session: AbstractSession):
        self._config = config
        self._session = session

    def get_service(self, wsdl_name):
        transport = self._session.get_transport()
        wsdl_url = self._config.wsdl_url + '/' + wsdl_name + '?WSDL'
        client = Client(wsdl=wsdl_url, transport=transport)

        return client.service
