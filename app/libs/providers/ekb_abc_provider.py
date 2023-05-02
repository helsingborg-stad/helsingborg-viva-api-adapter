from abc import ABC, abstractmethod
from app.libs.data_domain.ekb_status import EkbStatus
from app.libs.data_domain.ekb_mypages import EkbMyPages
from app.libs.data_domain.ekb_user import EkbUser


class EkbABCProvider(ABC):

    @abstractmethod
    def get_status(self, id: str) -> EkbStatus:
        pass

    @abstractmethod
    def get_mypages(self, id: str) -> EkbMyPages:
        pass

    @abstractmethod
    def get_user(self, id: str) -> EkbUser:
        pass
