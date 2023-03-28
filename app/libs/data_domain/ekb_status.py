from dataclasses import dataclass
from typing import List


@dataclass
class EkbStatusItem:
    code: int
    description: str


@dataclass
class EkbStatus(dict):
    status: List[EkbStatusItem]
