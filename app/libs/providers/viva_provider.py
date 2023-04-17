from app.libs.providers.viva_abc_provider import AbstractVivaProvider
from app.libs.classes.viva import Viva


class VivaProvider(AbstractVivaProvider):

    def create_client(self, wsdl_name: str):
        viva = Viva()
        return viva._get_service(wsdl_name=wsdl_name)
