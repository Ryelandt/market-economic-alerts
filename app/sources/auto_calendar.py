import os
import json
import urllib.parse
import urllib.request
from datetime import datetime, date
from app.models.event import EconomicEvent

FRED_BASE_URL = "https://api.stlouisfed.org/fred/releases"


def fetch_events():
    """
    Fetch macroeconomic events from FRED (official US source).
    Falls back cleanly if API is unavailable.
    Returns a list of EconomicEvent.
    """

    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("FRED_API_KEY not set, no automatic calendar available")
        return []

    params = {
        "api_key": api_key,
        "file_type": "json",
        "limit": 50
    }

    url = f"{FRED_BASE_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print("FRED API error:", e)
        return []

    events = []
    today = date.today()

    for r in data.get("releases", []):
        name = r.get("name", "")

        # Filtrage strict : uniquement les événements vraiment market movers
        if "Consumer Price Index" in name:
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
            importance = 3
        elif "Employment Situation" in name:
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
            importance = 3
        else:
            continue  # ignore le bruit

        # FRED ne fournit pas l’heure → on reste volontairement simple
        event_datetime = datetime.now()

        # Optionnel : ne garder que les événements du jour
        if event_datetime.date() != today:
            continue

        events.append(
            EconomicEvent(
                name=name,
                datetime=event_datetime,
                country="US",
                importance=importance,
                forecast=None,
                actual=None,
                affected_assets=assets
            )
        )

    return events
