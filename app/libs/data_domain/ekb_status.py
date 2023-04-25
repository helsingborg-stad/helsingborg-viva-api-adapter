from dataclasses import dataclass, field
from typing import List


@dataclass
class EkbStatusItem:
    code: int
    description: str


@dataclass
class EkbStatus(dict):
    status: List[EkbStatusItem] = field(default_factory=list)
