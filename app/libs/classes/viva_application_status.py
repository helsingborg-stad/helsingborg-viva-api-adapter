from typing import Any

"""
ApplicationStatus förklaring (taget direkt från Cambio):
-1 - fel (t.ex. person finns inte i personregistret)

eller summan av:
1 - ansökan tillåten
2 - autosave finns (man har påbörjat en ansökan)
4 - väntar signering (avser medsökande: sökande har signerat en ansökan som inkluderar medsökande)
8 - väntar att medsökande ska signera (avser sökande medan hen väntar på att medsökande ska signera)
16 - ansökan inskickad
32 - ansökan mottagen/registrerad i Viva
64 - komplettering begärd
128 - ärende finns (försörjningsstödsärende)
256 - ett ärende är aktiverat på web (egenskap på ärendet som gör att det visas på Mina sidor)
512 - ärendet tillåter e-ansökan (egenskap på ärendet som gör att det går att skapa fortsatt ansökan)

2, 4 och 8 blir bara aktuella när man parkerar eller autosparar ansökan i Viva.

Det är bara när ApplicationStatus innehåller 1 (summan är udda) som ansökan kan lämnas in.
128 + 256 + 512 kommer i princip alltid att vara med eftersom ett ärende som tillåter e-ansökan är en förutsättning för fortsatt ansökan.

När ApplicationStatus bara är 1 finns inget ärende och man kan lämna in en grundansökan.
"""

STATUS_DESCRIPTION = {
    -1: 'Error (for example that the person is not in the personal register)',
    1: 'Application allowed',
    2: 'Auto save',
    4: 'Awaiting signing',
    8: 'Waiting for co-applicants to sign',
    16: 'Application submitted',
    32: 'Application received/registered in Viva',
    64: 'Completion requested',
    128: 'Case available (income support)',
    256: 'Case is activated on the web. Is displayed on My Pages',
    512: 'The case allows e-application. Is possible to create a continued application',
}


class VivaApplicationStatus():
    def __init__(self, client: Any):
        self._client = client

    def get(self, personal_number: str):
        status_code = self._client.APPLICATIONSTATUS(
            SUSER=personal_number,
            SPNR=personal_number,
            SCASETYPE='01',  # 01 = EKB
            SSYSTEM=1
        )

        status_list = []

        if self._is_negative(status_code):
            status_list.append({
                'code': status_code,
                'description': STATUS_DESCRIPTION[status_code]
            })
            return status_list

        for bit in self._bits_generator(status_code):
            status_list.append({
                'code': bit,
                'description': STATUS_DESCRIPTION[bit]
            })

        return status_list

    def _is_negative(self, number):
        return float(number) < 0

    def _bits_generator(self, number):
        while number:
            bit = number & (~number+1)
            yield bit
            number ^= bit
