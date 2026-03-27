import os
import json
import urllib.parse
import urllib.request
from datetime import datetime, date, time, timedelta, timezone
from app.models.event import EconomicEvent

FRED_BASE_URL = "https://api.stlouisfed.org/fred/releases"

PARIS_TZ = timezone(timedelta(hours=1))


def fetch_events():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("FRED_API_KEY not set")
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

    today = date.today()
    events = []

    for r in data.get("releases", []):
        name = r.get("name", "")

      

        # 🇺🇸 US — publications à 14h30
        if "Consumer Price Index" in name:
            event_time = time(14, 30)
            importance = 3
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
        
        elif "Employment Situation" in name:
            event_time = time(14, 30)
            importance = 3
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
        
        elif "Retail Sales" in name:
            event_time = time(14, 30)
            importance = 2
            assets = ["EURUSD", "XAUUSD"]
        
        # 🇪🇺 Europe — matin / début d’après‑midi
        elif "ECB" in name or "European Central Bank" in name:
            event_time = time(14, 15)
            importance = 3
            assets = ["EURUSD", "XAUUSD"]
        
        elif "Germany" in name and "Consumer Price" in name:
            event_time = time(8, 00)
            importance = 2
            assets = ["EURUSD"]
        
        # 🇺🇸 Soir US
        elif "FOMC Statement" in name:
            event_time = time(20, 00)
            importance = 3
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
        
        elif "FOMC Press Conference" in name:
            event_time = time(20, 30)
            importance = 3
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
        
        else:
            continue
        
        event_datetime = datetime.combine(today, event_time, PARIS_TZ)

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
