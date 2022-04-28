from dataclasses import dataclass, field


@dataclass
class DataClassApplication:
    operation_type: str
    personal_number: str = ''
    workflow_id: str = ''
    attachments: list = field(default_factory=list)
    answers: list = field(default_factory=list)
    raw_data: str = ''
    raw_data_type: str = 'PDF'
