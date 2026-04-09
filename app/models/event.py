from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict


@dataclass
class Event:
    datetime: datetime
    currency: str
    title: str
    impact_level: str  # LOW | MEDIUM | HIGH
    description: str
    risk: str
    market_bias: str  # RISK_ON | RISK_OFF | NEUTRAL

    def to_dict(self) -> Dict:
        return asdict(self)

    def __repr__(self) -> str:
        return (
            f"Event({self.datetime}, {self.currency}, "
            f"{self.title}, impact={self.impact_level})"
        )
