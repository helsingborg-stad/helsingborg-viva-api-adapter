from app.libs.providers.viva_provider import AbstractVivaProvider


class TestVivaProvider(AbstractVivaProvider):

    def create_client(self):
        return self


# APPLICATIONSTATUS
def test_application_status_new_application_path():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = (
        lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 1)

    assert viva_provider.get_status('19900102034444') == [
        {'code': 1, 'description': 'Application allowed'}]


def test_application_status_recurring_application_path():
    viva_provider = TestVivaProvider()
    viva_provider.APPLICATIONSTATUS = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: 897

    result = viva_provider.get_status('19900102034444')

    assert result[0]['code'] == 1


# MY PAGES
def test_mypages_path():

    viva_provider = TestVivaProvider()
    viva_provider.MYPAGES = lambda SUSER, SPNR, SCASETYPE, SSYSTEM: {}

    assert viva_provider.get_mypages('19900102034444') == {}
