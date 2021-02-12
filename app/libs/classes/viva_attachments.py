from zeep.exceptions import ValidationError
from . import Viva


class VivaAttachments(Viva):

    def __init__(self, my_pages, wsdl='VivaAttachment'):
        super(VivaAttachments, self).__init__()

        self._my_pages = my_pages
        self._service = self._get_service(wsdl)

    def save(self, attachment=dict):
        if not isinstance(attachment, dict):
            raise ValidationError('Invalid attachment')

        viva_save_soap_response = self._service.SAVEDATA(
            SUSER=self._my_pages.get_personal_number(),
            SIP='0.0.0.0',
            STEMP='5',
            SKEY=attachment['attachment_id'],
            SPARENTID='',
            SFILENAME=attachment['file_name'],
            SDATA=attachment['file_base64']
        )

        return self._helpers.serialize_object(viva_save_soap_response)

    def get(self, attachment_id=str):
        viva_get_soap_response = self._service.GETDATA(
            SUSER=self._my_pages.get_personal_number(),
            GKEY=attachment_id
        )

        return self._helpers.serialize_object(viva_get_soap_response)
