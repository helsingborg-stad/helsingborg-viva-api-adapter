from dataclasses import dataclass, field
from typing import List

from app.libs.data_domain.ekb_case import EkbCase


@dataclass
class EkbPerson:
    personal_number: str
    first_name: str
    last_name: str
    role: str


@dataclass
class EkbUser:
    id: str
    personal_number: str
    first_name: str
    last_name: str
    cases: List[EkbCase]
    persons: List[EkbPerson]
