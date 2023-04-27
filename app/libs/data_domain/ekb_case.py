from dataclasses import dataclass
from typing import Union


@dataclass
class TimeSpan:
    start: Union[str, None] = None
    end: Union[str, None] = None


@dataclass
class EkbCase:
    id: str
    time_span: TimeSpan
    received_date: Union[str, None] = None
    locked_date: Union[str, None] = None
    description: Union[str, None] = None
