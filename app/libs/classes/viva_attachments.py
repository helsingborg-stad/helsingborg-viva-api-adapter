from zeep.exceptions import Fault

from . import Viva


class VivaAttachments(Viva):

    def __init__(self, user, wsdl='VivaAttachment'):
        super(VivaAttachments, self).__init__()

        self._service = self._get_service(wsdl)
        self._user = user

    def save(self, attachment=dict):
        if not isinstance(attachment, dict):
            raise Fault(message='Invalid attachment dict')

        viva_save_soap_response = self._service.SAVEDATA(
            SUSER=self._user,
            SIP='0.0.0.0',
            STEMP='5',
            SKEY=attachment['id'],
            SPARENTID='',
            SFILENAME=attachment['name'],
            SDATA=attachment['file_base64']
        )

        return self._helpers.serialize_object(viva_save_soap_response)
