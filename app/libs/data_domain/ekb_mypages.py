from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Dict


@dataclass
@dataclass_json
class EkbMyPages:
    cases: Dict[str, str] = field(default_factory=dict)
    application: Dict[str, str] = field(default_factory=dict)
