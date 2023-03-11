from typing import List
from abc import ABC, abstractmethod
from app.libs.data_domain.ekb_status import EkbStatus
from app.libs.data_domain.ekb_mypages import EkbMyPages


class EkbABCProvider(ABC):

    @abstractmethod
    def get_status(self, id: str) -> List[EkbStatus]:
        pass

    @abstractmethod
    def get_mypages(self, id: str) -> EkbMyPages:
        pass
