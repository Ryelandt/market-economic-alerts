import requests
import logging
from datetime import datetime, timedelta
from typing import List
from app.models.event import Event

logger = logging.getLogger(__name__)


class AutoCalendarSource:
    BASE_URL = "https://financialmodelingprep.com/api/v3/economic_calendar"

    
    def __init__(self):
        self.api_key = os.environ.get("FMP_API_KEY")
        if not self.api_key:
            raise ValueError("FMP_API_KEY is missing")


    def fetch_events(self) -> List[Event]:
        now = datetime.utcnow()
        end = now + timedelta(days=1)

        params = {
            "from": now.strftime("%Y-%m-%d"),
            "to": end.strftime("%Y-%m-%d"),
            "apikey": self.api_key,
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.error(f"API error: {e}")
            return []

        events = []

        for item in data:
            if item.get("country") not in ("US", "EU"):
                continue
            if item.get("impact") != "High":
                continue

            events.append(
                Event(
                    datetime=datetime.fromisoformat(item["date"]),
                    currency="USD" if item["country"] == "US" else "EUR",
                    title=item["event"],
                    impact_level="HIGH",
                    description=item.get("description", ""),
                    risk="High volatility expected",
                    market_bias="RISK_OFF",
                )
            )

        return events
