from dataclasses import dataclass, field
from typing import Dict


@dataclass
class EkbMyPages:
    cases: Dict[str, str] = field(default_factory=dict)
    application: Dict[str, str] = field(default_factory=dict)
