from dataclasses import dataclass, field
from typing import List


@dataclass
class EkbCase:
    id: str = ''


@dataclass
class EkbPerson:
    personalNumber: str = ''
    firstName: str = ''
    lastName: str = ''
    role: str = ''


@dataclass
class EkbUser:
    personalNumber: str = ''
    firstName: str = ''
    lastName: str = ''
    cases: List[EkbCase] = field(default_factory=list)
    persons: List[EkbPerson] = field(default_factory=list)
