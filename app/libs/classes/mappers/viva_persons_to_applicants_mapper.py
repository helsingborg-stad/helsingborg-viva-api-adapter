class VivaPersonsToApplicantsMapper():
    def __init__(self, applicant, coapplicant):
        self._applicant = applicant
        self._coapplicant = coapplicant

    def get_applicants(self):
        return list(a for a in [self._get_applicant(), self._get_coapplicant()] if a)

    def _get_applicant(self):
        if self._applicant:
            return {
                'role': 'applicant',
                'personalnumber': self._applicant['pnumber']
            }
        return None

    def _get_coapplicant(self):
        if self._coapplicant:
            return {
                'role': 'coapplicant',
                'personalnumber': self._coapplicant['pnumber']
            }

        return None
