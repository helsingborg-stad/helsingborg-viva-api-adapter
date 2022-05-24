from dataclasses import dataclass, field

from app.libs.enum import ApplicationType


@dataclass
class DataClassApplication:
    operation_type: ApplicationType
    personal_number: str = ''
    workflow_id: str = ''
    attachments: list = field(default_factory=list)
    answers: list = field(default_factory=list)
    raw_data: str = ''
    raw_data_type: str = 'PDF'
