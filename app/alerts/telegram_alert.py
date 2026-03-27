import os
import json
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Fuseau explicite
PARIS_TZ = ZoneInfo("Europe/Paris")


def send_alert(event, level):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise RuntimeError("Telegram credentials not set")

    # Temps actuel et événement en heure locale
    now = datetime.now(tz=PARIS_TZ)
    event_time = event.datetime.astimezone(PARIS_TZ)

    # Alerte pré‑annonce (-30 min)
    if timedelta(minutes=0) <= (event_time - now) <= timedelta(minutes=30):
        prefix = "⏰ DANS 30 MINUTES\n\n"
    else:
        prefix = ""

    message = (
        f"{prefix}"
        f"🚨 ALERTE {level}\n\n"
        f"📅 {event.name}\n"
        f"⏰ {event_time.strftime('%d/%m %H:%M')}\n\n"
        "Impact probable :\n"
        + "\n".join(f"• {a}" for a in event.affected_assets)
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        response.read()
