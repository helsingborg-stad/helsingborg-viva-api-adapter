from zeep.exceptions import ValidationError
from . import Viva


class VivaAttachments(Viva):

    def __init__(self, my_pages, wsdl='VivaAttachment', attachment=dict):
        super(VivaAttachments, self).__init__()

        self._my_pages = my_pages
        self._service = self._get_service(wsdl)

        if not isinstance(attachment, dict):
            raise ValidationError('Invalid attachment')

        self.attachment = attachment

    def save(self):
        viva_soap_response = self._service.SAVEDATA(
            SUSER=self._my_pages.get_personal_number(),
            SIP='0.0.0.0',
            STEMP='1',
            SKEY=self.attachment['attachment_id'],
            SPARENTID='',
            SFILENAME=self.attachment['file_name'],
            SDATA=self.attachment['file_base64']
        )

        return self._helpers.serialize_object(viva_soap_response)
