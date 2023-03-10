from abc import ABC, abstractmethod
from .ekb_status import EkbStatus
from .ekb_mypages import EkbMyPages


class EkbProvider(ABC):

    @abstractmethod
    def get_status(self, id: str) -> EkbStatus:
        pass

    @abstractmethod
    def get_mypages(self, id: str) -> EkbMyPages:
        pass
