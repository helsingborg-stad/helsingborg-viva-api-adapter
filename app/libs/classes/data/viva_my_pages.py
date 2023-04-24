from dataclasses import dataclass, field
from typing import List


@dataclass
class VivaMyPagesSoapResponse:
    vivadata: dict = field(default_factory=dict)


@dataclass
class VivaCase:
    idunique: str
    idenclair: str
    client: dict
    persons: dict
