from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class EconomicEvent:
    name: str
    datetime: datetime
    country: str
    importance: int  # 1 = faible, 3 = fort
    forecast: Optional[float]
    actual: Optional[float]
    affected_assets: List[str]
