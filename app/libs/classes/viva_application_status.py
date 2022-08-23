from flask import current_app

from app.libs.classes.viva import Viva


class VivaApplicationStatus(Viva):
    def __init__(self, wsdl='VivaApplication', personal_number=None):
        super(VivaApplicationStatus, self).__init__()

        if not isinstance(personal_number, str):
            raise TypeError('personal_number should be type string')

        self._personal_number = personal_number
        self._service = self._get_service(wsdl)

    def get(self):
        current_app.logger.debug('APPLICATIONSTATUS')
        """
        ApplicationStatus förklaring:
        -1 - fel (t.ex. person finns inte i personregistret)

        eller summan av:
        1 - ansökan tillåten
        2 - autosave finns (man har påbörjat en ansökan)
        4 - väntar signering (avser medsökande: sökande har signerat en ansökan som inkluderar medsökande)
        8 - väntar att medsökande ska signera (avser sökande medan hen väntar på att medsökande ska signera)
        16 - ansökan inskickad
        32 - ansökan mottagen(/registrerad i Viva)
        64 - komplettering begärd
        128 - ärende finns (försörjningsstödsärende)
        256 - ett ärende är aktiverat på web (egenskap på ärendet som gör att det visas på Mina sidor)
        512 - ärendet tillåter e-ansökan  (egenskap på ärendet som gör att det går att skapa fortsatt ansökan)

        2, 4 och 8 blir bara aktuella när man parkerar eller autosparar ansökan i Viva.

        Det är bara när ApplicationStatus innehåller 1 (summan är udda) som ansökan kan lämnas in.
        128 + 256 + 512 kommer i princip alltid att vara med eftersom ett ärende som tillåter e-ansökan är en förutsättning för fortsatt ansökan.

        När ApplicationStatus bara är 1 finns inget ärende och man kan lämna in en grundansökan.
        """

        status_code = self._service.APPLICATIONSTATUS(
            SUSER=self._personal_number,
            SPNR=self._personal_number,
            SCASETYPE='01',  # 01 = EKB
            SSYSTEM=1
        )

        status_description = {
            -1: 'Error (for example that the person is not in the personal register)',
            1: 'Application allowed',
            2: 'Auto save',
            4: 'Awaiting signing',
            8: 'Waiting for co-applicants to sign',
            16: 'Application submitted',
            32: 'Application received / registered',
            64: 'Completion requested',
            128: 'Case available (income support)',
            256: 'Case is activated on the web',
            512: 'The case allows e-application',
        }

        status_list = []

        if not self._is_negative(status_code):
            for bit in self._bits(status_code):
                status_list.append({
                    'code': bit,
                    'description': status_description[bit]
                })
        else:
            status_list.append({
                'code': status_code,
                'description': status_description[status_code]
            })

        return self._helpers.serialize_object(status_list)

    def _is_negative(self, number):
        return float(number) < 0

    def _bits(self, number):
        while number:
            bit = number & (~number+1)
            yield bit
            number ^= bit
