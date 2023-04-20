from flask import current_app

from app.libs.providers.viva_abc_provider import AbstractVivaProvider
from app.libs.classes.viva import Viva
from app.libs.classes.session import Session


class VivaProvider(AbstractVivaProvider):

    def create_client(self, wsdl_name: str):
        config = current_app.config['VIVA']

        session = Session(config=config)

        viva = Viva(config=config, session=session)
        return viva.get_service(wsdl_name=wsdl_name)
