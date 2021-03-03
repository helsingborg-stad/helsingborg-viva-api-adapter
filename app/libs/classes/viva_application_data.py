from dataclasses import dataclass, field
from typing import List


@dataclass
class DataClassApplication:
    operation_type: str
    workflow_id: str = ''
    attachments: list = field(default_factory=list)
    answers: list = field(default_factory=list)
    raw_data: str = ''
    raw_data_type: str = 'PDF'
