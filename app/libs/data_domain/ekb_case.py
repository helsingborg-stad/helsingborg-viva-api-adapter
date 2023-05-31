from dataclasses import dataclass
from typing import Union


@dataclass
class TimeSpan:
    start: str
    end: str


@dataclass
class EkbCase:
    id: str
    time_span: TimeSpan
    received_date: str
    locked_date: str
    description: str
