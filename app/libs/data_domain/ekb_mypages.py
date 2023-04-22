from dataclasses import dataclass, field


@dataclass
class EkbMyPages:
    cases: dict = field(default_factory=dict)
    application: dict = field(default_factory=dict)
