from typing import Any
from zeep.helpers import serialize_object


class VivaAttachments:

    def __init__(self, client: Any,  user: str) -> None:
        self._client = client
        self._user = user

    def save(self, attachment):
        viva_save_soap_response = self._client.SAVEDATA(
            SUSER=self._user,
            SIP='0.0.0.0',
            STEMP='5',
            SKEY=attachment['id'],
            SPARENTID='',
            SFILENAME=attachment['name'],
            SDATA=attachment['file_base64']
        )

        return serialize_object(viva_save_soap_response)
