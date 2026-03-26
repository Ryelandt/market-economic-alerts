from datetime import datetime
from app.models.event import EconomicEvent

def fetch_events():
    return [
        EconomicEvent(
            name="US CPI",
            datetime=datetime(2026, 3, 26, 14, 30),
            country="US",
            importance=3,
            forecast=3.1,
            actual=None,
            affected_assets=["EURUSD", "XAUUSD", "BTCUSDT"]
        ),
        EconomicEvent(
            name="ECB Interest Rate Decision",
            datetime=datetime(2026, 3, 26, 15, 45),
            country="EU",
            importance=3,
            forecast=None,
            actual=None,
            affected_assets=["EURUSD"]
        )
    ]
