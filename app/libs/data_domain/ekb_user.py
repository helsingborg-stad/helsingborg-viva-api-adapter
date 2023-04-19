from dataclasses import dataclass, field
from typing import List


@dataclass
class EkbCase:
    id: str = ''

    def __iter__(self):
        return iter(self.__dict__.items())


@dataclass
class EkbPerson:
    personal_number: str = ''
    first_name: str = ''
    last_name: str = ''
    role: str = ''

    def __iter__(self):
        return iter(self.__dict__.items())


@dataclass
class EkbUser:
    personal_number: str = ''
    first_name: str = ''
    last_name: str = ''
    cases: List[EkbCase] = field(default_factory=list)
    persons: List[EkbPerson] = field(default_factory=list)
