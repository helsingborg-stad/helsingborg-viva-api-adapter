from . import ApplicationAnswerCollection


class ZeepHousing(dict):
    def __init__(self, application_answer_collection: ApplicationAnswerCollection):
        super().__init__(self)
        self.application_answer_collection = application_answer_collection

    def _get_first_matching_answer_by_tags(self, tags):
        answers_by_tags = self.application_answer_collection.filter_by_tags(
            tags)
        return next((answer for answer in answers_by_tags if answer.value), None)

    def get_client(self, personal_number: str):
        housing_answer = self._get_first_matching_answer_by_tags(tags=[
                                                                 'housing'])
        if not housing_answer:
            return None

        housing = {
            'CLIENT': {
                'PNUMBER': personal_number,
                'ADDRESSES': {'ADDRESS': {'TYPE': 'FB', 'CO': ''}},
                'FOREIGNCITIZEN': False,
                'RESIDENCEPERMITTYPE': '',
                'RESIDENCEPERMITDATE': '',
                'CIVILSTATUS': 'G',
                'ALTCIVILSTATUS': '',
                'PHONENUMBERS': None,
                'EMAIL': {'EMAIL': '', 'NOTIFY': ''},
            },
        }

        first_name = self._get_first_matching_answer_by_tags(
            tags=['housing', 'firstName'])
        if first_name:
            housing['CLIENT']['FNAME'] = first_name.value

        last_name = self._get_first_matching_answer_by_tags(
            tags=['housing', 'lastName'])
        if last_name:
            housing['CLIENT']['LNAME'] = last_name.value

        address = self._get_first_matching_answer_by_tags(
            tags=['housing', 'address'])
        if address:
            housing['CLIENT']['ADDRESSES']['ADDRESS']['ADDRESS'] = address.value

        postalCode = self._get_first_matching_answer_by_tags(
            tags=['housing', 'postalCode'])
        if postalCode:
            housing['CLIENT']['ADDRESSES']['ADDRESS']['ZIP'] = postalCode.value

        city = self._get_first_matching_answer_by_tags(
            tags=['housing', 'city'])
        if city:
            housing['CLIENT']['ADDRESSES']['ADDRESS']['CITY'] = city.value

        e_mail = self._get_first_matching_answer_by_tags(
            tags=['housing', 'email'])
        if e_mail:
            housing['CLIENT']['EMAIL'] = {
                'EMAIL': e_mail.value, 'NOTIFY':  False}

        phonenumber_answer = self._get_first_matching_answer_by_tags(
            tags=['housing', 'telephone'])
        if phonenumber_answer:
            housing['CLIENT']['PHONENUMBERS'] = {'PHONENUMBER': {
                'NUMBER': phonenumber_answer.value, 'TYPE': 'Mobiltelefon', 'SMS': False}}

        return housing
